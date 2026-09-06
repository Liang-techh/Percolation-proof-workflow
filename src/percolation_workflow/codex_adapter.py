"""Run a durable dispatch envelope through the installed Codex CLI.

The mathematical workflow remains provider-neutral, but this module is the
concrete host adapter used by the local Codex installation.  It binds the
request before starting the process, preserves the exact JSONL transcript and
final message outside the state checkpoint, and writes one version-1 callback
for the existing coordinator.  A successful process without a structured
candidate/decomposition is deliberately reported as an agent error: plain
natural-language completion is not a workflow result.
"""
from __future__ import annotations

import json
import hashlib
import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import subprocess
import tempfile
import threading
import time
from datetime import datetime, timezone
from collections.abc import Mapping
from typing import Any

from .agent_bridge import bind_agent, renew_agent
from .host_adapter import FilesystemHostAdapter
from .store import StateStore


_LEASE_LOCK = threading.Lock()


def _codex_environment() -> dict[str, str]:
    """Pass through the host environment and make the installed elan root explicit."""
    environment = dict(os.environ)
    elan_home = Path.home() / ".elan"
    if elan_home.is_dir():
        environment.setdefault("ELAN_HOME", str(elan_home))
    return environment


def infer_manifest_project(store: StateStore) -> Path | None:
    """Resolve the single Lean project declared by a bound portable manifest.

    This is deliberately narrow: only the manifest path already authenticated
    into the workflow state is consulted, and the result must look like a Lean
    project.  Multi-project isolated verification still requires an explicit
    request-to-project map.
    """
    state = store.load()
    identity = state.manifest
    if not isinstance(identity, dict) or not isinstance(identity.get("path"), str):
        return None
    relative = Path(identity["path"])
    if relative.is_absolute() or "\\" in identity["path"]:
        return None
    manifest_path = (store.path.resolve().parent / relative).resolve()
    project = manifest_path.parent
    if (not manifest_path.is_file() or not project.is_dir()
            or not (project / "lakefile.toml").is_file()
            or not (project / "lean-toolchain").is_file()):
        return None
    expected = identity.get("sha256")
    if not isinstance(expected, str) or _digest(manifest_path.read_bytes()) != expected:
        return None
    return project


def _text_output(value: str | bytes | None) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value


def _structured_message(message: str) -> dict[str, Any] | None:
    """Decode the bounded JSON object requested by the Codex prompt."""
    candidates = [message.strip()]
    if "```" in message:
        for block in message.split("```")[1::2]:
            stripped = block.strip()
            if stripped.startswith("json"):
                stripped = stripped[4:].lstrip()
            candidates.append(stripped)
    for candidate in candidates:
        try:
            value = json.loads(candidate)
        except (TypeError, json.JSONDecodeError):
            continue
        if isinstance(value, dict):
            return value
    return None


def _codex_events(stdout: str) -> tuple[str | None, bool, list[dict[str, Any]]]:
    """Return the provider thread id and parseable JSONL events."""
    thread_id = None
    terminal_seen = False
    terminal_types = {"turn.completed", "turn.failed", "turn.cancelled", "response.completed",
                      "task_complete", "task.completed", "error"}
    events = []
    for line in stdout.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(event, dict):
            continue
        events.append(event)
        if event.get("type") in terminal_types:
            terminal_seen = True
        if event.get("type") in {"thread.started", "thread_start"}:
            value = event.get("thread_id") or event.get("threadId")
            if isinstance(value, str) and value.strip():
                thread_id = value
    return thread_id, terminal_seen, events


def _atomic_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
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


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _lean_snapshot(project: Path) -> dict[str, str]:
    """Hash source Lean files, excluding generated/cache directories."""
    result = {}
    for path in project.rglob("*.lean"):
        resolved = path.resolve()
        if (not resolved.is_file() or not resolved.is_relative_to(project)
                or any(part in {".lake", ".git", "__pycache__"} for part in path.parts)):
            continue
        relative = resolved.relative_to(project).as_posix()
        result[relative] = _digest(resolved.read_bytes())
    return result


def discover_candidate_bundle(project: str | Path, before: Mapping[str, str]) -> dict[str, Any]:
    """Discover a changed Lean entrypoint and its supporting source bundle.

    A proof agent may need to edit a theorem entrypoint plus private support
    declarations in another Lean file.  Discovery remains fail-closed: multiple
    changed files are accepted only when exactly one is a conventional
    ``Candidate.lean``/``Solution.lean`` entrypoint; otherwise the agent must
    name the files explicitly.
    """
    project = Path(project).resolve()
    if not project.is_dir():
        raise ValueError("candidate discovery project does not exist")
    after = _lean_snapshot(project)
    changed = [project / relative for relative, digest in after.items()
               if before.get(relative) != digest]
    changed = [path for path in changed if path.suffix == ".lean"]
    if not changed:
        raise ValueError("automatic candidate discovery found no changed Lean source")
    conventional = [path for path in changed if path.name.lower() in {"candidate.lean", "solution.lean"}]
    if len(changed) == 1:
        entrypoint = changed[0]
    elif len(conventional) == 1:
        entrypoint = conventional[0]
    else:
        raise ValueError("automatic candidate discovery is ambiguous: "
                         + ", ".join(path.relative_to(project).as_posix() for path in changed))
    return {"entrypoint": entrypoint, "sources": sorted(changed)}


def discover_candidate(project: str | Path, before: Mapping[str, str]) -> Path:
    """Backward-compatible single-entrypoint view of bundle discovery."""
    return discover_candidate_bundle(project, before)["entrypoint"]


def _valid_decomposition(value: Any) -> bool:
    if not isinstance(value, dict) or not isinstance(value.get("sketch"), str):
        return False
    children = value.get("children")
    return isinstance(children, list) and all(
        isinstance(child, dict) and isinstance(child.get("name"), str)
        and isinstance(child.get("statement"), str)
        for child in children)


def _run_codex_process(command: list[str], project: Path, store: StateStore,
                       request_id: str, agent_id: str, lease_seconds: int,
                       timeout_seconds: int | None, *, started_marker: Path | None = None,
                       finished_marker: Path | None = None,
                       transcript_path: Path | None = None,
                       stderr_path: Path | None = None) -> tuple[int, bytes, bytes, bool, int]:
    """Run Codex while renewing its durable host lease.

    Real subprocess pipes are drained by dedicated readers and mirrored to the
    run sidecars as bytes arrive.  The returned byte strings remain available
    for the callback digest and existing callers; the sidecars are the durable
    in-progress journal used after an abrupt coordinator/host interruption.
    """
    process = subprocess.Popen(command, cwd=project, env=_codex_environment(),
                               stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    if started_marker is not None and isinstance(getattr(process, 'pid', None), int):
        _atomic_bytes(started_marker, (json.dumps({
            'schema_version': 1, 'request_id': request_id, 'agent_id': agent_id,
            'pid': process.pid, 'command': command, 'started_at': datetime.now(timezone.utc).isoformat()
        }, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))

    def finish(result: tuple[int, bytes, bytes, bool, int]) -> tuple[int, bytes, bytes, bool, int]:
        if finished_marker is not None:
            _atomic_bytes(finished_marker, (json.dumps({
                'schema_version': 1, 'request_id': request_id, 'agent_id': agent_id,
                'exit_code': result[0], 'timed_out': result[3],
                'finished_at': datetime.now(timezone.utc).isoformat()
            }, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
        return result

    streams = []
    stream_threads = []
    stream_buffers: dict[str, list[bytes]] = {"stdout": [], "stderr": []}
    stream_paths = {"stdout": transcript_path, "stderr": stderr_path}

    def drain(name: str, stream: Any) -> None:
        path = stream_paths[name]
        handle = None
        try:
            if path is not None:
                path.parent.mkdir(parents=True, exist_ok=True)
                handle = path.open("wb")
            while True:
                # Codex stdout is JSONL. ``read(65536)`` on Windows pipes can
                # wait for the full buffer or EOF, defeating the live journal;
                # readline makes each emitted event durable immediately.
                chunk = stream.readline()
                if not chunk:
                    break
                if isinstance(chunk, str):
                    chunk = chunk.encode("utf-8", errors="replace")
                stream_buffers[name].append(chunk)
                if handle is not None:
                    handle.write(chunk)
                    handle.flush()
                    os.fsync(handle.fileno())
        finally:
            if handle is not None:
                handle.close()

    real_pipes = all(getattr(process, name, None) is not None for name in ("stdout", "stderr"))
    if real_pipes:
        for name in ("stdout", "stderr"):
            streams.append(threading.Thread(target=drain, args=(name, getattr(process, name)),
                                             name=f"codex-{name}-journal", daemon=True))
        for thread in streams:
            thread.start()
        stream_threads = streams

    def collect_streams() -> tuple[bytes, bytes]:
        for thread in stream_threads:
            thread.join()
        # The reader threads close their journal files, but ``Popen`` keeps
        # the parent-side pipe wrappers open until explicitly closed.  Close
        # them after the readers have drained EOF so long-running supervisors
        # do not accumulate file descriptors (or ResourceWarnings in tests).
        for name in ("stdout", "stderr"):
            stream = getattr(process, name, None)
            if stream is not None and not stream.closed:
                stream.close()
        return b"".join(stream_buffers["stdout"]), b"".join(stream_buffers["stderr"])

    started = time.monotonic()
    deadline = started + timeout_seconds if timeout_seconds is not None else None
    renew_interval = max(0.5, min(30.0, lease_seconds / 3.0))
    renewals = 0
    while True:
        wait_for = renew_interval
        if deadline is not None:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                process.kill()
                if real_pipes:
                    process.wait()
                    stdout, stderr = collect_streams()
                else:
                    stdout, stderr = process.communicate()
                return finish((124, stdout or b"", (stderr or b"") + b"\ncodex exec timed out", True, renewals))
            wait_for = min(wait_for, remaining)
        try:
            process.wait(timeout=wait_for)
            break
        except subprocess.TimeoutExpired:
            with _LEASE_LOCK:
                renew_agent(store, request_id, agent_id, lease_seconds=lease_seconds)
            renewals += 1
    if real_pipes:
        stdout, stderr = collect_streams()
    else:
        stdout, stderr = process.communicate()
    return finish((process.returncode, stdout or b"", stderr or b"", False, renewals))


def _prompt(request: dict[str, Any], project: Path) -> str:
    return """You are a proof worker in a durable theorem-DAG workflow.

Work only inside the assigned project. Read the dispatch data below, inspect
the existing Lean files, and either prove the assigned theorem or repair the
latest failed attempt. Run the exact Lean command needed for the candidate.
Do not weaken the theorem, add an axiom, use sorry/admit, import a forbidden
existing proof, or edit the workflow state/manifest. The coordinator will run
the independent verifier after you return.

At the end, return ONLY one JSON object (no Markdown) with exactly these keys:
{"candidate":null,"decomposition":null,"error":null}.
Put the candidate object in candidate when a Lean source is ready, the ordered
decomposition object in decomposition when this is a planning response, and a
diagnostic string in error when neither is ready; use null for the other keys.
Candidate objects have project/source and may include a complete sources list;
project must be exactly the assigned project path and source must be an absolute filesystem path such as
"C:\\...\\Candidate.lean". Never put Lean source code in source; source is
ONLY a path to the file you edited. If exactly one Lean file changed during
the run, you may use source:"AUTO" and the host adapter will discover that
file from a before/after hash snapshot. For a multi-file candidate, use source
for the entrypoint and sources for every changed Lean file; source:"AUTO"
discovers that bundle when there is exactly one conventional Candidate.lean or
Solution.lean entrypoint and rejects ambiguity. Decomposition children have
name/statement/proof_sketch.
The source must really contain the candidate proof. If Lean cannot be made to
compile, return {"error":"..."} and explain the exact diagnostic in the
final message; do not claim a candidate.

Assigned project: """ + str(project) + "\n\nDispatch request:\n" + json.dumps(
        request, ensure_ascii=False, indent=2, sort_keys=True)


def run_codex_dispatch(store: StateStore, dispatch_file: str | Path, callback_dir: str | Path,
                       *, project: str | Path, codex_executable: str = "codex",
                       sandbox: str = "workspace-write", lease_seconds: int = 3600,
                       timeout_seconds: int | None = None,
                       output_dir: str | Path | None = None,
                       _bound_agent_id: str | None = None) -> dict[str, Any]:
    """Execute one dispatch envelope and enqueue its validated callback."""
    dispatch_path = Path(dispatch_file).resolve()
    envelope = json.loads(dispatch_path.read_text(encoding="utf-8"))
    if not isinstance(envelope, dict) or envelope.get("kind") != "agent_dispatch":
        raise ValueError("dispatch file must contain an agent_dispatch envelope")
    request = envelope.get("request")
    if not isinstance(request, dict):
        raise ValueError("dispatch envelope is missing request")
    for field in ("request_id", "attempt_id", "manifest_sha256", "protocol_version"):
        if field not in request:
            raise ValueError(f"dispatch request is missing {field}")
    if request["request_id"] != envelope.get("request_id") or request["attempt_id"] != envelope.get("attempt_id"):
        raise ValueError("dispatch envelope/request correlation mismatch")
    if request["protocol_version"] != 1:
        raise ValueError("unsupported dispatch protocol version")
    project_path = Path(project).resolve()
    if not project_path.is_dir():
        raise ValueError("assigned Codex project directory does not exist")
    if not isinstance(sandbox, str) or sandbox not in {"read-only", "workspace-write", "danger-full-access"}:
        raise ValueError("unsupported Codex sandbox")
    if timeout_seconds is not None and (type(timeout_seconds) is not int or timeout_seconds < 1):
        raise ValueError("timeout_seconds must be a positive integer")
    if timeout_seconds is not None and timeout_seconds >= lease_seconds:
        raise ValueError("timeout_seconds must be shorter than lease_seconds")

    request_id = request["request_id"]
    if not isinstance(request_id, str) or not request_id:
        raise ValueError("dispatch request_id must be nonempty")
    agent_id = _bound_agent_id or f"codex-cli-{request_id}"

    run_root = Path(output_dir).resolve() if output_dir is not None else dispatch_path.parent / "codex-runs"
    run_dir = run_root / request_id / request["attempt_id"]
    run_dir.mkdir(parents=True, exist_ok=True)
    before_snapshot = _lean_snapshot(project_path)
    transcript_path = run_dir / "stdout.jsonl"
    stderr_path = run_dir / "stderr.txt"
    final_path = run_dir / "final-message.txt"
    schema_path = run_dir / "output-schema.json"
    schema = {
        "type": "object",
        "properties": {
            "candidate": {"type": ["object", "null"], "properties": {
                "project": {"type": "string"}, "source": {"type": "string"},
                "sources": {"type": "array", "items": {"type": "string"}}},
                "required": ["project", "source"], "additionalProperties": False},
            "decomposition": {"type": ["object", "null"], "properties": {
                "sketch": {"type": "string"}, "children": {"type": "array", "items": {
                    "type": "object", "properties": {
                        "name": {"type": "string"}, "statement": {"type": "string"},
                        "proof_sketch": {"type": "string"}},
                    "required": ["name", "statement", "proof_sketch"], "additionalProperties": False}}},
                "required": ["sketch", "children"], "additionalProperties": False},
            "error": {"type": ["string", "null"]},
        },
        "required": ["candidate", "decomposition", "error"],
        "additionalProperties": False,
    }
    _atomic_bytes(schema_path, (json.dumps(schema, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    command = [codex_executable, "exec", "--json", "--ephemeral", "--skip-git-repo-check",
               "-C", str(project_path), "-s", sandbox, "--output-schema", str(schema_path),
               "-o", str(final_path), _prompt(request, project_path)]
    if _bound_agent_id is None:
        bind_agent(store, request_id, agent_id, lease_seconds=lease_seconds,
                   host_run_dir=str(run_dir))
    else:
        bound = store.load().agent_requests.get(request_id)
        if (not isinstance(bound, dict) or bound.get("status") != "bound"
                or bound.get("agent_id") != agent_id):
            raise ValueError("pre-bound Codex request does not have the expected active agent")
    started_at = datetime.now(timezone.utc).isoformat()
    exit_code = 1
    stdout = b""
    stderr = b""
    timed_out = False
    renewals = 0
    try:
        exit_code, stdout, stderr, timed_out, renewals = _run_codex_process(
            command, project_path, store, request_id, agent_id, lease_seconds, timeout_seconds,
            started_marker=run_dir / 'started.json', finished_marker=run_dir / 'finished.json',
            transcript_path=transcript_path, stderr_path=stderr_path)
        if isinstance(stdout, str):
            stdout = stdout.encode("utf-8", errors="replace")
        if isinstance(stderr, str):
            stderr = stderr.encode("utf-8", errors="replace")
    except OSError as exc:
        exit_code = 127
        stderr = repr(exc).encode("utf-8")
    _atomic_bytes(transcript_path, stdout)
    _atomic_bytes(stderr_path, stderr)
    final_message = final_path.read_text(encoding="utf-8") if final_path.is_file() else ""
    _atomic_bytes(run_dir / "command.json",
                  (json.dumps(command, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    stdout_text = _text_output(stdout)
    thread_id, terminal_seen, events = _codex_events(stdout_text)
    structured = _structured_message(final_message)
    process_ok = exit_code == 0 and not timed_out
    candidate = structured.get("candidate") if isinstance(structured, dict) else None
    candidate_discovered = False
    candidate_valid = (isinstance(candidate, dict) and isinstance(candidate.get("project"), str)
                       and isinstance(candidate.get("source"), str))
    if candidate_valid and candidate.get("source") == "AUTO":
        try:
            bundle = discover_candidate_bundle(project_path, before_snapshot)
            candidate["source"] = str(bundle["entrypoint"])
            candidate["sources"] = [str(path) for path in bundle["sources"]]
            candidate_discovered = True
        except ValueError:
            candidate_valid = False
    if candidate_valid:
        candidate_project = Path(candidate["project"]).resolve()
        candidate_source = Path(candidate["source"]).resolve()
        candidate_valid = (candidate_project == project_path and candidate_source.suffix == ".lean"
                           and candidate_source.is_file() and candidate_source.is_relative_to(project_path))
        candidate_sources = candidate.get("sources")
        if candidate_sources is None:
            candidate_sources = [candidate["source"]]
        candidate_valid = candidate_valid and isinstance(candidate_sources, list) and bool(candidate_sources)
        normalized_sources: list[Path] = []
        if candidate_valid:
            for value in candidate_sources:
                if not isinstance(value, str):
                    candidate_valid = False
                    break
                path = Path(value).resolve()
                if (path.suffix != ".lean" or not path.is_file() or
                        not path.is_relative_to(project_path) or path in normalized_sources):
                    candidate_valid = False
                    break
                normalized_sources.append(path)
            candidate_valid = candidate_valid and candidate_source in normalized_sources
    decomposition_valid = _valid_decomposition(structured.get("decomposition")) if isinstance(structured, dict) else False
    structured_result = (isinstance(structured, dict) and terminal_seen and
                         (candidate_valid or decomposition_valid))
    has_workflow_result = process_ok and structured_result
    terminal_message = final_message if final_message else _text_output(stderr).strip()
    if process_ok and has_workflow_result:
        terminal = {"completed": terminal_message}
    else:
        if not process_ok:
            reason = f"codex exec exited {exit_code}"
        elif not terminal_seen:
            reason = "missing terminal JSONL event"
        elif isinstance(candidate, dict) and not candidate_valid:
            reason = "candidate is outside the assigned project or has no Lean source"
        elif isinstance(structured, dict) and isinstance(structured.get("decomposition"), dict) and not decomposition_valid:
            reason = "decomposition schema is invalid"
        else:
            reason = "structured candidate/decomposition missing"
        terminal = {"errored": f"{reason}: {terminal_message[-4000:]}"}
    callback = {
        "protocol_version": 1,
        "kind": "agent_result",
        "request_id": request_id,
        "attempt_id": request["attempt_id"],
        "event_id": f"codex-{request_id}-{request['attempt_id']}",
        "agent_id": agent_id,
        "manifest_sha256": request["manifest_sha256"],
        "payload": {"status": {agent_id: terminal}, "host_execution": {
            "exit_code": exit_code,
            "terminal_event_seen": terminal_seen,
            "stdout_sha256": _digest(stdout),
            "stdout_bytes": len(stdout),
            "stderr_sha256": _digest(stderr),
            "stderr_bytes": len(stderr),
            "lease_renewals": renewals,
        }},
        "host_metadata": {
            "adapter": "codex-cli",
            "provider_thread_id": thread_id,
            "exit_code": exit_code,
            "timed_out": timed_out,
            "event_count": len(events),
            "terminal_event_seen": terminal_seen,
            "lease_renewals": renewals,
            "candidate_discovery": "changed-lean-bundle" if candidate_discovered else None,
            "command_path": str(run_dir / "command.json"),
            "stdout_path": str(transcript_path),
            "stderr_path": str(stderr_path),
            "final_message_path": str(final_path),
            "schema_path": str(schema_path),
        },
    }
    if has_workflow_result:
        if isinstance(candidate, dict):
            callback["candidate"] = candidate
        if isinstance(structured.get("decomposition"), dict):
            callback["decomposition"] = structured["decomposition"]
    metadata = {
        "request_id": request_id,
        "attempt_id": request["attempt_id"],
        "agent_id": agent_id,
        "provider_thread_id": thread_id,
        "process_exit_code": exit_code,
        "timed_out": timed_out,
        "terminal_event_seen": terminal_seen,
        "event_count": len(events),
        "lease_renewals": renewals,
        "stdout_sha256": _digest(stdout),
        "stdout_bytes": len(stdout),
        "stderr_sha256": _digest(stderr),
        "stderr_bytes": len(stderr),
        "started_at": started_at,
        "finished_at": datetime.now(timezone.utc).isoformat(),
    }
    _atomic_bytes(run_dir / "metadata.json",
                  (json.dumps(metadata, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    callback_path = FilesystemHostAdapter(run_dir.parent, store=store,
                                          callback_inbox=callback_dir).write_callback(callback)
    return {"request_id": request_id, "agent_id": agent_id, "exit_code": exit_code,
            "provider_thread_id": thread_id, "structured": has_workflow_result,
            "callback": str(callback_path), "run_dir": str(run_dir)}


def run_codex_batch(store: StateStore, dispatch_dir: str | Path, callback_dir: str | Path,
                    *, project: str | Path | None = None,
                    project_map: dict[str, str | Path] | None = None,
                    limit: int = 4, max_workers: int = 2,
                    codex_executable: str = "codex", sandbox: str = "workspace-write",
                    lease_seconds: int = 3600, timeout_seconds: int | None = None,
                    output_dir: str | Path | None = None) -> list[dict[str, Any]]:
    """Run several durable dispatches in parallel after serial binding.

    Binding is intentionally coordinator-serialized because each state save
    advances the optimistic revision.  Only the provider processes run in the
    pool; their callbacks remain independent atomic files for ``host-cycle``.
    """
    if type(limit) is not int or limit < 1 or type(max_workers) is not int or max_workers < 1:
        raise ValueError("limit and max_workers must be positive integers")
    directory = Path(dispatch_dir).resolve()
    if not directory.is_dir():
        raise ValueError("dispatch directory does not exist")
    paths = sorted(directory.glob("*.json"))[:limit]
    if not paths:
        return []
    project_map = project_map or {}
    inferred_project = Path(project).resolve() if project is not None else infer_manifest_project(store)
    entries = []
    for path in paths:
        envelope = json.loads(path.read_text(encoding="utf-8"))
        request = envelope.get("request") if isinstance(envelope, dict) else None
        request_id = request.get("request_id") if isinstance(request, dict) else None
        if not isinstance(request_id, str) or not request_id:
            raise ValueError(f"dispatch file has no request_id: {path.name}")
        selected = project_map.get(request_id, inferred_project)
        if selected is None:
            raise ValueError(f"no project assigned for dispatch request: {request_id}")
        agent_id = f"codex-cli-{request_id}"
        run_root = Path(output_dir).resolve() if output_dir is not None else directory / 'codex-runs'
        run_dir = run_root / request_id / request['attempt_id']
        bind_agent(store, request_id, agent_id, lease_seconds=lease_seconds,
                   host_run_dir=str(run_dir))
        entries.append((path, Path(selected), agent_id))

    def run(entry: tuple[Path, Path, str]) -> dict[str, Any]:
        path, selected, agent_id = entry
        try:
            return run_codex_dispatch(
                store, path, callback_dir, project=selected,
                codex_executable=codex_executable, sandbox=sandbox,
                lease_seconds=lease_seconds, timeout_seconds=timeout_seconds,
                output_dir=output_dir, _bound_agent_id=agent_id)
        except Exception as exc:
            return {"request_id": path.stem, "agent_id": agent_id,
                    "structured": False, "error": repr(exc), "needs_reclaim": True}

    with ThreadPoolExecutor(max_workers=min(max_workers, len(entries)),
                            thread_name_prefix="codex-proof") as executor:
        results = list(executor.map(run, entries))
    return results


__all__ = ["discover_candidate", "discover_candidate_bundle", "infer_manifest_project",
           "run_codex_dispatch", "run_codex_batch"]
