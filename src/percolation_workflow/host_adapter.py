"""A small, filesystem-backed boundary for real host-agent integrations.

This module only persists protocol envelopes.  It does not call a model provider,
bind an agent, or invent a result.  The existing bridge and coordinator remain
the authority for workflow transitions; this adapter is the durable hand-off
boundary around them.
"""
from __future__ import annotations

from collections.abc import Iterable, Mapping
import json
import os
from pathlib import Path
import re
import tempfile
from typing import Any, Protocol, runtime_checkable

from .agent_bridge import prepare_requests
from .research import next_actions
from .store import StateStore


PROTOCOL_VERSION = 1
_SAFE_COMPONENT = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")


@runtime_checkable
class HostAdapter(Protocol):
    """Injectable host boundary used by a coordinator or a real host runtime."""

    def dispatch(self, store: StateStore | None = None, *, limit: int = 4) -> list[dict[str, Any]]:
        """Persist the currently dispatchable host requests."""

    def write_callback(self, envelope: Mapping[str, Any], *, store: StateStore | None = None) -> Path:
        """Persist one raw callback envelope in the callback inbox."""


def _require_text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a nonempty string")
    return value


def _safe_component(value: Any, field: str) -> str:
    value = _require_text(value, field)
    if not _SAFE_COMPONENT.fullmatch(value):
        raise ValueError(f"{field} is not a safe inbox identifier")
    return value


def _json_bytes(value: Mapping[str, Any]) -> bytes:
    return (json.dumps(dict(value), ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _atomic_create(path: Path, payload: bytes) -> Path:
    """Create *path* without replacement, after atomically staging its bytes.

    A hard-link commit is used because it fails if the destination already
    exists, unlike ``Path.replace``.  The temporary file is in the same
    directory, so the commit cannot cross filesystems.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        try:
            os.link(temporary, path)
        except FileExistsError:
            raise FileExistsError(f"envelope already exists: {path.name}") from None
        if os.name != "nt":
            try:
                directory_fd = os.open(path.parent, os.O_RDONLY)
                try:
                    os.fsync(directory_fd)
                finally:
                    os.close(directory_fd)
            except OSError:
                pass
        return path
    finally:
        temporary.unlink(missing_ok=True)


class FilesystemHostAdapter:
    """Persist dispatches and callbacks below one private filesystem root.

    ``root`` gets two subdirectories by default: ``dispatch`` for outbound
    envelopes and ``callback-inbox`` for inbound envelopes.  A ``StateStore``
    can be supplied at construction time or to each operation, which keeps the
    adapter straightforward to inject in tests and coordinators.
    """

    def __init__(self, root: str | Path, *, store: StateStore | None = None,
                 dispatch_dir: str | Path | None = None,
                 callback_inbox: str | Path | None = None):
        self.root = Path(root).resolve()
        self.store = store
        self.dispatch_dir = Path(dispatch_dir).resolve() if dispatch_dir is not None else self.root / "dispatch"
        self.callback_inbox = (Path(callback_inbox).resolve() if callback_inbox is not None
                               else self.root / "callback-inbox")

    def _store(self, store: StateStore | None) -> StateStore:
        resolved = store or self.store
        if resolved is None:
            raise ValueError("a StateStore is required")
        return resolved

    @staticmethod
    def build_dispatch_envelope(action: Mapping[str, Any], request: Mapping[str, Any]) -> dict[str, Any]:
        """Validate and combine a ``next_actions`` item with its bridge request."""
        if action.get("kind") != "dispatch_agent":
            raise ValueError("only dispatch_agent actions can become dispatch envelopes")
        for field in ("request_id", "attempt_id", "protocol_version", "manifest_sha256"):
            if field not in request:
                raise ValueError(f"dispatch request is missing {field}")
        request_id = _safe_component(request["request_id"], "request_id")
        attempt_id = _require_text(request["attempt_id"], "attempt_id")
        if type(request["protocol_version"]) is not int or request["protocol_version"] != PROTOCOL_VERSION:
            raise ValueError("unsupported dispatch protocol version")
        if (action.get("request_id") != request_id or
                ("attempt_id" in action and action.get("attempt_id") != attempt_id)):
            raise ValueError("dispatch action and request correlation mismatch")
        if action.get("node_id") != request.get("node_id"):
            raise ValueError("dispatch action and request node mismatch")
        if action.get("agent_id") != request.get("agent_id"):
            raise ValueError("dispatch action and request agent mismatch")
        return {
            "protocol_version": PROTOCOL_VERSION,
            "kind": "agent_dispatch",
            "event_id": request.get("event_id"),
            "request_id": request_id,
            "attempt_id": attempt_id,
            "manifest_sha256": request.get("manifest_sha256"),
            "action": dict(action),
            "request": dict(request),
        }

    def write_dispatch_envelope(self, action: Mapping[str, Any], request: Mapping[str, Any]) -> Path:
        envelope = self.build_dispatch_envelope(action, request)
        request_id = _safe_component(envelope["request_id"], "request_id")
        path = self.dispatch_dir / f"{request_id}.json"
        payload = _json_bytes(envelope)
        try:
            return _atomic_create(path, payload)
        except FileExistsError:
            # Re-running a coordinator may rediscover the same request.  It is
            # safe to reuse an identical durable envelope, never to overwrite it.
            if path.read_bytes() == payload:
                return path
            raise ValueError(f"dispatch request_id was reused with different payload: {request_id}") from None

    def persist_dispatch(self, actions: Iterable[Mapping[str, Any]],
                         requests: Mapping[str, Mapping[str, Any]] | Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
        """Persist dispatch actions and return the exact envelopes written."""
        if isinstance(requests, Mapping):
            request_by_id = dict(requests)
        else:
            request_by_id = {}
            for request in requests:
                request_id = _safe_component(request.get("request_id"), "request_id")
                if request_id in request_by_id:
                    raise ValueError(f"duplicate dispatch request_id: {request_id}")
                request_by_id[request_id] = request
        result = []
        for action in actions:
            if action.get("kind") != "dispatch_agent":
                continue
            request_id = _safe_component(action.get("request_id"), "request_id")
            try:
                request = request_by_id[request_id]
            except KeyError as exc:
                raise ValueError(f"dispatch action has no request: {request_id}") from exc
            self.write_dispatch_envelope(action, request)
            result.append(self.build_dispatch_envelope(action, request))
        return result

    def dispatch(self, store: StateStore | None = None, *, limit: int = 4) -> list[dict[str, Any]]:
        """Prepare pending bridge requests, then persist their host dispatches.

        This invokes no agent and does not create a result.  ``prepare_agent``
        is the research-layer action that authorizes creating bridge requests;
        the second ``next_actions`` call exposes the resulting dispatch action.
        """
        resolved_store = self._store(store)
        if limit < 1:
            raise ValueError("positive dispatch limit required")
        actions = next_actions(resolved_store)
        if any(action.get("kind") == "prepare_agent" for action in actions):
            prepare_requests(resolved_store, limit=limit)
            actions = next_actions(resolved_store)
        state = resolved_store.load()
        return self.persist_dispatch(actions, state.agent_requests)

    def _validate_callback(self, envelope: Mapping[str, Any], store: StateStore) -> tuple[str, str]:
        required = ("protocol_version", "kind", "request_id", "attempt_id", "event_id",
                    "agent_id", "manifest_sha256", "payload")
        missing = [field for field in required if field not in envelope]
        if missing:
            raise ValueError(f"callback envelope missing {', '.join(missing)}")
        if type(envelope["protocol_version"]) is not int or envelope["protocol_version"] != PROTOCOL_VERSION:
            raise ValueError("unsupported callback protocol version")
        if envelope["kind"] != "agent_result":
            raise ValueError("unsupported callback kind")
        request_id = _safe_component(envelope["request_id"], "request_id")
        attempt_id = _require_text(envelope["attempt_id"], "attempt_id")
        event_id = _safe_component(envelope["event_id"], "event_id")
        agent_id = _require_text(envelope["agent_id"], "agent_id")
        if not isinstance(envelope["payload"], dict):
            raise ValueError("callback payload must be an object")
        state = store.load()
        try:
            request = state.agent_requests[request_id]
        except KeyError as exc:
            raise ValueError(f"callback belongs to unknown request: {request_id}") from exc
        if request.get("attempt_id") != attempt_id:
            raise ValueError("callback belongs to a different attempt")
        if request.get("protocol_version") != envelope["protocol_version"]:
            raise ValueError("callback protocol does not match dispatch request")
        if request.get("manifest_sha256") != envelope["manifest_sha256"]:
            raise ValueError("callback belongs to a different verification manifest")
        bound_agent = request.get("agent_id")
        if envelope.get("protocol_version") == PROTOCOL_VERSION and not bound_agent:
            raise ValueError("version 1 callback requires a bound host agent")
        if bound_agent is not None and bound_agent != agent_id:
            raise ValueError("callback belongs to a different host agent")
        return request_id, event_id

    def write_callback(self, envelope: Mapping[str, Any], *, store: StateStore | None = None) -> Path:
        """Atomically place the unmodified callback object in the inbox.

        The adapter intentionally does not call ``record_result``: the durable
        coordinator will consume the inbox through ``host_cycle`` and perform
        the terminal-result validation there.
        """
        if not isinstance(envelope, Mapping):
            raise ValueError("callback envelope must be an object")
        request_id, event_id = self._validate_callback(envelope, self._store(store))
        path = self.callback_inbox / f"{event_id}.json"
        # request_id is validated as part of the correlation check; retaining
        # it in this check makes the intended filename/inbox boundary explicit.
        _safe_component(request_id, "request_id")
        return _atomic_create(path, _json_bytes(envelope))

    # Explicit aliases make the persistence boundary easy to discover without
    # creating a second implementation or changing the older coordinator API.
    persist_callback = write_callback
    write_callback_envelope = write_callback


__all__ = ["HostAdapter", "FilesystemHostAdapter", "PROTOCOL_VERSION"]
