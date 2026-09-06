"""Durable, ordered upload ledger for the Prove2Me-compatible boundary.

The transport is intentionally injected.  A real HTTP adapter can implement
the provider's queued-job polling and token refresh, while this ledger keeps
the important invariant local: every action is recorded before the external
call and after its response, and reruns use the same action key.
"""
from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import secrets
import tempfile
import time
from typing import Any, Protocol
from urllib.error import HTTPError
from urllib.parse import urlencode, quote
from urllib.request import Request, urlopen


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _atomic_json(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = (json.dumps(dict(value), ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    fd, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


class UploadTransport(Protocol):
    """Provider adapter; it must make ``operation_key`` idempotent."""

    def execute(self, action: Mapping[str, Any], *, operation_key: str,
                context: Mapping[str, Any]) -> Mapping[str, Any]:
        """Submit and, if necessary, poll one terminal provider operation."""


class Prove2MeError(RuntimeError):
    """Base class for errors at the authenticated Prove2Me boundary."""


class Prove2MeHTTPError(Prove2MeError):
    def __init__(self, status: int, body: Any):
        self.status = status
        self.body = body
        super().__init__(f"Prove2Me HTTP {status}: {body}")


class Prove2MeRetryableError(Prove2MeError):
    """A queued operation ended in the provider's retryable ERROR state."""

    def __init__(self, response: Mapping[str, Any]):
        self.response = dict(response)
        super().__init__(f"Prove2Me operation returned ERROR: {self.response}")


class Prove2MeTerminalError(Prove2MeError):
    """A queued operation was terminally rejected by the provider."""

    def __init__(self, response: Mapping[str, Any]):
        self.response = dict(response)
        super().__init__(f"Prove2Me operation failed: {self.response}")


class Prove2MeIndeterminateError(Prove2MeError):
    """A request may have reached the server, but returned no durable id."""


def _canonical_action_digest(action: Mapping[str, Any]) -> str:
    data = json.dumps(dict(action), ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), default=str).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def _multipart_form(fields: Mapping[str, Any], *, file_field: str,
                    filename: str, content: bytes) -> tuple[bytes, str]:
    """Build the small multipart body needed by ``POST /verify``."""
    boundary = "--------------------------" + secrets.token_hex(12)
    chunks: list[bytes] = []
    for name, value in fields.items():
        chunks.extend([
            f"--{boundary}\r\n".encode("utf-8"),
            f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode("utf-8"),
            str(value).encode("utf-8"),
            b"\r\n",
        ])
    chunks.extend([
        f"--{boundary}\r\n".encode("utf-8"),
        (f'Content-Disposition: form-data; name="{file_field}"; '
         f'filename="{filename}"\r\n').encode("utf-8"),
        b"Content-Type: text/plain; charset=utf-8\r\n\r\n",
        content,
        b"\r\n",
        f"--{boundary}--\r\n".encode("utf-8"),
    ])
    return b"".join(chunks), f"multipart/form-data; boundary={boundary}"


class Prove2MeTransport:
    """Authenticated HTTP transport for the public Prove2Me API.

    The class deliberately has no implicit credential discovery and no default
    write path.  Supply an access-token provider (or an API key) and an
    ``operation_store`` when durable remote resumption is wanted.  The store
    records a provider job/submission id *before polling*, which prevents a
    lost polling connection from causing a second submission.  If the network
    fails after the server accepted a request but before an id is returned, the
    next call raises :class:`Prove2MeIndeterminateError` instead of guessing
    and duplicating a contribution.
    """

    _PUBLISH_TERMINAL = {"PUBLISHED", "FAILED", "ERROR"}
    _VERIFY_TERMINAL = {"ACCEPTED", "SKETCH_ACCEPTED", "CE", "WA",
                        "SORRY", "FAILED", "ERROR"}

    def __init__(self, *, access_token: str | None = None,
                 token_provider: Any = None, refresh_token: Any = None,
                 api_key: str | None = None,
                 base_url: str = "https://prove2.me/api/v1",
                 operation_store: str | Path | None = None,
                 opener: Any = urlopen, timeout_seconds: float = 30.0,
                 poll_timeout_seconds: float = 900.0,
                 poll_interval_seconds: float = 3.0,
                 sleep: Any = time.sleep,
                 monotonic: Any = time.monotonic,
                 user_agent: str = "percolation-proof-workflow/0.1"):
        from urllib.parse import urlsplit
        parsed = urlsplit(base_url)
        if parsed.scheme != "https" or parsed.netloc.lower() != "prove2.me":
            raise ValueError("Prove2Me credentials may only target https://prove2.me")
        self.base_url = base_url.rstrip("/")
        self.access_token = access_token
        self._refresh_override: str | None = None
        self.token_provider = token_provider
        self.refresh_token = refresh_token
        self.api_key = api_key
        self.opener = opener
        self.timeout_seconds = float(timeout_seconds)
        self.poll_timeout_seconds = float(poll_timeout_seconds)
        self.poll_interval_seconds = float(poll_interval_seconds)
        self.sleep = sleep
        self.monotonic = monotonic
        self.user_agent = user_agent
        self.operation_store = Path(operation_store).resolve() if operation_store else None
        self.journal: dict[str, Any] = {"schema_version": 1, "operations": {}}
        if self.operation_store and self.operation_store.is_file():
            self.journal = json.loads(self.operation_store.read_text(encoding="utf-8"))
            if (self.journal.get("schema_version") != 1 or
                    not isinstance(self.journal.get("operations"), dict)):
                raise ValueError("Prove2Me operation store is malformed")

    def _save_journal(self) -> None:
        if self.operation_store is None:
            return
        _atomic_json(self.operation_store, self.journal)

    def _record(self, key: str, action: Mapping[str, Any], **updates: Any) -> dict[str, Any]:
        operations = self.journal["operations"]
        record = operations.get(key)
        digest = _canonical_action_digest(action)
        if record is None:
            record = {"operation_key": key, "action_sha256": digest,
                      "status": "submitting", "updated_at": _now()}
            operations[key] = record
        elif record.get("action_sha256") != digest:
            raise ValueError(f"Prove2Me action changed after operation began: {key}")
        record.update(updates)
        record["updated_at"] = _now()
        self._save_journal()
        return record

    def _token(self) -> str:
        token = (self._refresh_override if self._refresh_override is not None else
                 (self.token_provider() if self.token_provider is not None else self.access_token))
        if token:
            return str(token)
        if self.api_key:
            body = json.dumps({"api_key": self.api_key}).encode("utf-8")
            _, response = self._request_once("POST", "/agent/refresh", body=body,
                                             content_type="application/json", auth=False)
            token = response.get("access_token") or response.get("token")
            if not token:
                raise Prove2MeError("/agent/refresh returned no access token")
            self.access_token = str(token)
            self._refresh_override = self.access_token
            return self.access_token
        raise Prove2MeError("Prove2Me transport has no access token or API key")

    def _request_once(self, method: str, path: str, *, body: bytes | None = None,
                      content_type: str | None = None, query: Mapping[str, Any] | None = None,
                      auth: bool = True, idempotency_key: str | None = None) -> tuple[int, dict[str, Any]]:
        url = self.base_url + "/" + path.lstrip("/")
        if query:
            url += "?" + urlencode({key: str(value) for key, value in query.items()})
        headers = {"Accept": "application/json", "User-Agent": self.user_agent}
        if content_type:
            headers["Content-Type"] = content_type
        if auth:
            headers["Authorization"] = "Bearer " + self._token()
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        request = Request(url, data=body, headers=headers, method=method)
        try:
            response = self.opener(request, timeout=self.timeout_seconds)
            status = int(response.getcode() if hasattr(response, "getcode") else response.status)
            raw = response.read()
            if hasattr(response, "close"):
                response.close()
        except HTTPError as exc:
            raw = exc.read()
            status = int(exc.code)
        except OSError as exc:
            raise Prove2MeError(f"Prove2Me network failure: {exc}") from exc
        try:
            parsed = json.loads(raw.decode("utf-8")) if raw else {}
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            parsed = {"raw": raw.decode("utf-8", errors="replace")}
            if not 200 <= status < 300:
                raise Prove2MeHTTPError(status, parsed) from exc
        if not isinstance(parsed, dict):
            parsed = {"value": parsed}
        if not 200 <= status < 300:
            raise Prove2MeHTTPError(status, parsed)
        return status, parsed

    def _request_json(self, method: str, path: str, *, payload: Mapping[str, Any] | None = None,
                      query: Mapping[str, Any] | None = None, auth: bool = True,
                      idempotency_key: str | None = None) -> dict[str, Any]:
        body = json.dumps(dict(payload), ensure_ascii=False).encode("utf-8") if payload is not None else None
        for attempt in range(2):
            try:
                return self._request_once(method, path, body=body,
                                          content_type="application/json" if body is not None else None,
                                          query=query, auth=auth,
                                          idempotency_key=idempotency_key)[1]
            except Prove2MeHTTPError as exc:
                if exc.status != 401 or not auth or attempt:
                    raise
                if self.refresh_token is not None:
                    token = self.refresh_token()
                    if not token:
                        raise Prove2MeError("token refresh returned no access token") from exc
                    self.access_token = str(token)
                    self._refresh_override = self.access_token
                    continue
                if self.api_key:
                    self.access_token = None
                    self._refresh_override = None
                    continue
                raise
        raise AssertionError("unreachable request retry")

    def _poll(self, path: str, *, query: Mapping[str, Any] | None = None,
              terminal: set[str]) -> dict[str, Any]:
        deadline = self.monotonic() + self.poll_timeout_seconds
        while True:
            response = self._request_json("GET", path, query=query)
            status = str(response.get("status", "")).upper()
            if status in terminal:
                return response
            if self.monotonic() >= deadline:
                raise Prove2MeError(f"Prove2Me polling timed out: {path}")
            self.sleep(self.poll_interval_seconds)

    @staticmethod
    def _payload(action: Mapping[str, Any], *, field: str) -> dict[str, Any]:
        value = action.get("payload")
        if value is None:
            value = action.get(field)
        if value is not None:
            if not isinstance(value, Mapping):
                raise ValueError(f"{field} payload must be an object")
            return dict(value)
        excluded = {"key", "kind", "depends_on", "module", "name", "solution",
                    "solution_path", "file_path", "theorem_id", "proof_type", "form",
                    "lookup_theorem_id"}
        return {key: value for key, value in action.items() if key not in excluded}

    @staticmethod
    def _job_id(response: Mapping[str, Any], action: Mapping[str, Any]) -> str:
        jobs = response.get("jobs")
        if isinstance(jobs, list):
            name = action.get("name") or action.get("theorem_name") or action.get("definition_name")
            matches = [job for job in jobs if isinstance(job, Mapping) and
                       (name is None or job.get("name") == name)]
            if len(matches) != 1 or not matches[0].get("job_id"):
                raise Prove2MeError("publish response did not contain one matching job")
            return str(matches[0]["job_id"])
        if response.get("job_id"):
            return str(response["job_id"])
        raise Prove2MeError("publish response contained no job_id")

    def _finish_publish(self, record: Mapping[str, Any], key: str,
                        action: Mapping[str, Any], *, require_theorem_id: bool) -> dict[str, Any]:
        response = self._poll("/publish-jobs/" + quote(str(record["job_id"]), safe=""),
                              terminal=self._PUBLISH_TERMINAL)
        status = str(response.get("status", "")).upper()
        if status == "PUBLISHED" and require_theorem_id and not response.get("theorem_id"):
            raise Prove2MeError("PUBLISHED theorem job contained no theorem_id")
        if status == "ERROR":
            self._record(key, action, status="retryable_error", response=dict(response), job_id=None)
            raise Prove2MeRetryableError(response)
        if status != "PUBLISHED":
            self._record(key, action, status="failed", response=dict(response))
            raise Prove2MeTerminalError(response)
        self._record(key, action, status="succeeded", response=dict(response))
        return dict(response)

    def _theorem_id(self, action: Mapping[str, Any], context: Mapping[str, Any]) -> str:
        if action.get("theorem_id"):
            return str(action["theorem_id"])
        name = action.get("name")
        own_key = f"theorem:{name}" if isinstance(name, str) else None
        candidates = [context.get(own_key)] if own_key else []
        candidates.extend(context.values())
        for response in candidates:
            if isinstance(response, Mapping) and response.get("theorem_id"):
                if not name or response.get("theorem_name") in (None, name):
                    return str(response["theorem_id"])
        if not action.get("lookup_theorem_id"):
            raise Prove2MeError(f"no theorem_id available for solution {name!r}")
        if not isinstance(name, str) or not name:
            raise ValueError("theorem lookup requires action.name")
        hits = self._request_json("GET", "/theorems", query={"q": name.rsplit(".", 1)[-1]})
        rows = hits.get("theorems") or hits.get("results") or []
        matches = [row for row in rows if isinstance(row, Mapping) and
                   row.get("theorem_name") == name and row.get("theorem_id")]
        if len(matches) != 1:
            raise Prove2MeError(f"exact theorem lookup was not unique for {name}")
        return str(matches[0]["theorem_id"])

    @staticmethod
    def _solution_bytes(action: Mapping[str, Any]) -> tuple[str, bytes]:
        path = action.get("solution_path") or action.get("file_path")
        if path is not None:
            source = Path(path)
            if not source.is_file():
                raise FileNotFoundError(source)
            return source.name, source.read_bytes()
        solution = action.get("solution")
        if isinstance(solution, str):
            return "solution.lean", solution.encode("utf-8")
        raise ValueError("verify_solution action needs solution_path, file_path, or solution")

    def _execute_publish(self, action: Mapping[str, Any], *, operation_key: str,
                         definition: bool) -> dict[str, Any]:
        record = self.journal["operations"].get(operation_key)
        if record is not None and record.get("action_sha256") != _canonical_action_digest(action):
            raise ValueError(f"Prove2Me action changed after operation began: {operation_key}")
        if record and record.get("status") == "succeeded":
            return dict(record["response"])
        if record and record.get("status") == "failed":
            raise Prove2MeTerminalError(record.get("response", {}))
        if record and record.get("status") == "submitting":
            raise Prove2MeIndeterminateError(
                f"{operation_key} has no provider id after a prior submission attempt")
        if record and record.get("job_id"):
            return self._finish_publish(record, operation_key, action,
                                        require_theorem_id=not definition)
        # Provider ERROR is explicitly retryable; the next execution gets a
        # fresh job while retaining the same local operation key.
        self._record(operation_key, action, status="submitting", job_id=None)
        payload = self._payload(action, field="definition_payload" if definition else "problem_payload")
        if definition:
            payload.setdefault("definition_name", action.get("name") or action.get("module"))
            response = self._request_json("POST", "/submit-definition", payload=payload,
                                          idempotency_key=operation_key)
        else:
            payload.setdefault("theorem_name", action.get("name"))
            response = self._request_json("POST", "/submit-problem", payload=payload,
                                          idempotency_key=operation_key)
            errors = response.get("errors")
            if isinstance(errors, list) and errors:
                self._record(operation_key, action, status="failed", response=dict(response))
                raise Prove2MeTerminalError(response)
        job_id = self._job_id(response, action)
        self._record(operation_key, action, status="polling", job_id=job_id,
                     submission_response=dict(response))
        record = self.journal["operations"][operation_key]
        return self._finish_publish(record, operation_key, action,
                                    require_theorem_id=not definition)

    def _execute_verify(self, action: Mapping[str, Any], *, operation_key: str,
                        context: Mapping[str, Any]) -> dict[str, Any]:
        record = self.journal["operations"].get(operation_key)
        if record is not None and record.get("action_sha256") != _canonical_action_digest(action):
            raise ValueError(f"Prove2Me action changed after operation began: {operation_key}")
        if record and record.get("status") == "succeeded":
            return dict(record["response"])
        if record and record.get("status") == "failed":
            raise Prove2MeTerminalError(record.get("response", {}))
        if record and record.get("status") == "submitting":
            raise Prove2MeIndeterminateError(
                f"{operation_key} has no provider id after a prior submission attempt")
        if record and record.get("submission_id"):
            response = self._poll("/verify", query={"submission_id": record["submission_id"]},
                                  terminal=self._VERIFY_TERMINAL)
            return self._finish_verify(record, operation_key, action, response)
        self._record(operation_key, action, status="submitting", submission_id=None)
        theorem_id = self._theorem_id(action, context)
        filename, content = self._solution_bytes(action)
        fields: dict[str, Any] = {"theorem_id": theorem_id,
                                  "proof_type": action.get("proof_type", "prove")}
        if action.get("explanation") is not None:
            fields["explanation"] = action["explanation"]
        extra = action.get("form") or {}
        if not isinstance(extra, Mapping):
            raise ValueError("verify_solution form must be an object")
        fields.update(extra)
        body, content_type = _multipart_form(fields, file_field="file",
                                             filename=filename, content=content)
        response = self._request_once("POST", "/verify", body=body,
                                      content_type=content_type,
                                      idempotency_key=operation_key)[1]
        submission_id = response.get("submission_id") or response.get("id")
        if not submission_id:
            raise Prove2MeError("verify response contained no submission_id")
        self._record(operation_key, action, status="polling", submission_id=str(submission_id),
                     submission_response=dict(response))
        record = self.journal["operations"][operation_key]
        terminal = self._poll("/verify", query={"submission_id": str(submission_id)},
                              terminal=self._VERIFY_TERMINAL)
        return self._finish_verify(record, operation_key, action, terminal)

    def _finish_verify(self, record: Mapping[str, Any], key: str,
                       action: Mapping[str, Any], response: Mapping[str, Any]) -> dict[str, Any]:
        status = str(response.get("status", "")).upper()
        if status in {"ACCEPTED", "SKETCH_ACCEPTED"}:
            self._record(key, action, status="succeeded", response=dict(response))
            return dict(response)
        if status == "ERROR":
            self._record(key, action, status="retryable_error", response=dict(response),
                         submission_id=None)
            raise Prove2MeRetryableError(response)
        self._record(key, action, status="failed", response=dict(response))
        raise Prove2MeTerminalError(response)

    def execute(self, action: Mapping[str, Any], *, operation_key: str,
                context: Mapping[str, Any]) -> Mapping[str, Any]:
        kind = action.get("kind")
        if kind == "submit_definition":
            return self._execute_publish(action, operation_key=operation_key, definition=True)
        if kind == "submit_theorem":
            return self._execute_publish(action, operation_key=operation_key, definition=False)
        if kind == "verify_solution":
            return self._execute_verify(action, operation_key=operation_key, context=context)
        raise ValueError(f"unsupported Prove2Me upload action kind: {kind!r}")


class UploadLedger:
    """A crash-resumable action ledger with strict action identity."""

    def __init__(self, path: str | Path):
        self.path = Path(path).resolve()
        self.data: dict[str, Any] = {"schema_version": 1, "actions": {}, "events": []}
        if self.path.is_file():
            self.data = json.loads(self.path.read_text(encoding="utf-8"))
            self._validate()

    def _validate(self) -> None:
        if self.data.get("schema_version") != 1 or not isinstance(self.data.get("actions"), dict):
            raise ValueError("upload ledger schema is malformed")
        if not isinstance(self.data.get("events", []), list):
            raise ValueError("upload ledger events are malformed")
        for key, record in self.data["actions"].items():
            if not isinstance(key, str) or not isinstance(record, dict):
                raise ValueError("upload ledger action record is malformed")
            if record.get("status") not in {"pending", "in_flight", "succeeded", "failed"}:
                raise ValueError(f"invalid upload action status: {key}")
            if record.get("key") != key or not isinstance(record.get("action"), dict):
                raise ValueError(f"upload ledger action identity is malformed: {key}")

    def save(self) -> None:
        self._validate()
        _atomic_json(self.path, self.data)

    def prepare(self, actions: Sequence[Mapping[str, Any]]) -> None:
        """Install an immutable ordered action list before external calls."""
        keys = []
        for action in actions:
            key = action.get("key")
            if not isinstance(key, str) or not key.strip() or key in keys:
                raise ValueError("upload actions require unique nonempty keys")
            if not isinstance(action.get("kind"), str):
                raise ValueError(f"upload action has no kind: {key}")
            dependencies = action.get("depends_on", [])
            if not isinstance(dependencies, list) or any(not isinstance(dep, str) for dep in dependencies):
                raise ValueError(f"upload action dependencies are malformed: {key}")
            keys.append(key)
        key_set = set(keys)
        for action in actions:
            if any(dep not in key_set for dep in action.get("depends_on", [])):
                raise ValueError(f"upload action has an unknown dependency: {action['key']}")
        for action in actions:
            key = action["key"]
            prior = self.data["actions"].get(key)
            if prior is None:
                self.data["actions"][key] = {"key": key, "action": dict(action),
                                              "status": "pending", "attempts": 0}
            elif prior.get("action") != dict(action):
                raise ValueError(f"upload action changed after ledger creation: {key}")
        self.data["ordered_keys"] = keys
        self.data["events"].append({"kind": "plan_prepared", "keys": keys, "at": _now()})
        self.save()

    def _context(self, action: Mapping[str, Any]) -> dict[str, Any]:
        context = {}
        for dep in action.get("depends_on", []):
            record = self.data["actions"][dep]
            if record.get("status") != "succeeded":
                raise RuntimeError(f"upload dependency is not complete: {dep}")
            context[dep] = record.get("response")
        return context

    def run(self, actions: Sequence[Mapping[str, Any]], transport: UploadTransport) -> dict[str, Any]:
        """Execute in order; a rerun safely retries pending/in-flight/failed keys."""
        self.prepare(actions)
        for action in actions:
            key = action["key"]
            record = self.data["actions"][key]
            if record.get("status") == "succeeded":
                continue
            context = self._context(action)
            record.update(status="in_flight", attempts=int(record.get("attempts", 0)) + 1,
                          started_at=_now(), operation_key=key)
            self.data["events"].append({"kind": "action_started", "key": key,
                                        "attempt": record["attempts"], "at": _now()})
            self.save()
            try:
                response = transport.execute(action, operation_key=key, context=context)
                if not isinstance(response, Mapping):
                    raise ValueError("upload transport must return an object response")
                record.update(status="succeeded", response=dict(response), finished_at=_now())
                self.data["events"].append({"kind": "action_succeeded", "key": key,
                                            "at": _now()})
                self.save()
            except Exception as exc:
                record.update(status="failed", error=repr(exc), finished_at=_now())
                self.data["events"].append({"kind": "action_failed", "key": key,
                                            "error": repr(exc), "at": _now()})
                self.save()
                raise
        return {"schema_version": 1, "status": "complete",
                "ordered_keys": list(self.data.get("ordered_keys", [])),
                "actions": self.data["actions"]}


__all__ = ["Prove2MeError", "Prove2MeHTTPError", "Prove2MeIndeterminateError",
           "Prove2MeRetryableError", "Prove2MeTerminalError", "Prove2MeTransport",
           "UploadLedger", "UploadTransport"]
