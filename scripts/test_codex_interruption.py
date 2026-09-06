"""Interrupt one real Codex CLI proof process and recover its durable request.

This experiment kills only the Codex child whose PID was written by the adapter's
start marker.  It then lets the coordinator consume the errored callback and
prepare a repair request.  It is recovery evidence, not a proof result.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone
import uuid

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from percolation_workflow.codex_adapter import run_codex_dispatch
from percolation_workflow.host_adapter import FilesystemHostAdapter
from percolation_workflow.host_cycle import run_host_cycle
from percolation_workflow.model import WorkflowState
from percolation_workflow.store import StateStore


DISCLAIMER = "Real Codex process interruption; no proof success is claimed."


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _kill_process(pid: int) -> list[str]:
    if type(pid) is not int or pid <= 0:
        raise ValueError("start marker has an invalid Codex PID")
    if os.name == "nt":
        command = ["taskkill", "/PID", str(pid), "/T", "/F"]
        subprocess.run(command, capture_output=True, text=True, check=False)
        return command
    os.kill(pid, signal.SIGKILL)
    return ["kill", "-9", str(pid)]


def _child(run: Path, codex: str, timeout: int) -> int:
    dispatch_files = sorted((run / "dispatch").glob("*.json"))
    if len(dispatch_files) != 1:
        raise RuntimeError("child expected exactly one dispatch envelope")
    try:
        result = run_codex_dispatch(
            StateStore(run / "state.json"), dispatch_files[0], run / "callback-inbox",
            project=run / "fixture", codex_executable=codex, lease_seconds=120,
            timeout_seconds=timeout, output_dir=run / "codex-runs")
        _write_json(run / "child-result.json", result)
        return 0
    except Exception as exc:
        _write_json(run / "child-error.json", {"error": repr(exc)})
        return 1


def run(codex: str = "codex", *, wait_seconds: int = 45) -> dict:
    if type(wait_seconds) is not int or wait_seconds < 5:
        raise ValueError("wait_seconds must be at least 5")
    run_root = ROOT / "artifacts" / "codex_interruption"
    run = run_root / (datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8])
    fixture = run / "fixture"
    fixture.mkdir(parents=True)
    toolchain = (ROOT / "examples/minimal_lean/lean-toolchain").read_text(encoding="utf-8")
    (fixture / "lean-toolchain").write_text(toolchain, encoding="utf-8")
    (fixture / "lakefile.toml").write_text('name = "codexInterruption"\n', encoding="utf-8")
    (fixture / "Candidate.lean").write_text(
        "theorem goal : True := by trivial\n", encoding="utf-8")

    store = StateStore(run / "state.json")
    state = WorkflowState(project="codex-interruption-experiment")
    node_id = state.add_node("goal", "theorem goal : True",
                             proof_sketch="Interrupt before candidate completion; recover into repair frontier.",
                             metadata={"statement_status": "indexed", "experiment": DISCLAIMER})
    store.save(state)
    envelopes = FilesystemHostAdapter(run, store=store).dispatch(limit=1)
    if len(envelopes) != 1:
        raise RuntimeError("failed to create exactly one durable dispatch")
    request_id = envelopes[0]["request_id"]
    attempt_id = envelopes[0]["attempt_id"]
    child_command = [sys.executable, "-B", str(Path(__file__).resolve()), "--child",
                     str(run), "--codex", codex, "--timeout", str(wait_seconds + 30)]
    child = subprocess.Popen(child_command, cwd=ROOT, stdin=subprocess.DEVNULL,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             text=True, creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
    start_marker = run / "codex-runs" / request_id / attempt_id / "started.json"
    deadline = time.monotonic() + wait_seconds
    while time.monotonic() < deadline and not start_marker.is_file():
        if child.poll() is not None:
            break
        time.sleep(0.05)
    if not start_marker.is_file():
        stdout, stderr = child.communicate(timeout=10)
        report = {"status": "undetermined", "reason": "Codex start marker not observed",
                  "child_exit_code": child.returncode, "child_stdout": stdout,
                  "child_stderr": stderr, "disclaimer": DISCLAIMER, "run_directory": str(run)}
        _write_json(run / "report.json", report)
        return report

    marker = json.loads(start_marker.read_text(encoding="utf-8"))
    kill_command = _kill_process(marker["pid"])
    stdout, stderr = child.communicate(timeout=wait_seconds)
    child_result = json.loads((run / "child-result.json").read_text(encoding="utf-8")) \
        if (run / "child-result.json").is_file() else None
    callback_files = sorted((run / "callback-inbox").glob("*.json"))
    if child.returncode != 0 or child_result is None or len(callback_files) != 1:
        raise RuntimeError(f"interrupted Codex adapter did not finish durably: exit={child.returncode}")
    callback = json.loads(callback_files[0].read_text(encoding="utf-8"))
    cycle = run_host_cycle(store, callback_dir=run / "callback-inbox")
    final = store.load()
    original = final.agent_requests[request_id]
    original_attempt = final.attempts[attempt_id]
    repair_requests = [request for request in final.agent_requests.values()
                       if request.get("repair_of_attempt_id") == attempt_id]
    host_execution = callback.get("payload", {}).get("host_execution", {})
    status = callback.get("payload", {}).get("status", {}).get(callback.get("agent_id"), {})
    report = {
        "status": "passed",
        "disclaimer": DISCLAIMER,
        "run_directory": str(run),
        "request_id": request_id,
        "attempt_id": attempt_id,
        "codex_pid": marker["pid"],
        "kill_command": kill_command,
        "child_exit_code": child.returncode,
        "codex_exit_code": host_execution.get("exit_code"),
        "terminal_event_seen": host_execution.get("terminal_event_seen"),
        "callback_status": status,
        "callback_file": str(callback_files[0]),
        "cycle_errors": cycle["errors"],
        "original_request_status": original.get("status"),
        "original_attempt_status": original_attempt.status,
        "node_status": final.nodes[node_id].status,
        "repair_request_count": len(repair_requests),
        "raw_stdout_path": original.get("raw_callback", {}).get("host_metadata", {}).get("stdout_path"),
        "raw_stderr_path": original.get("raw_callback", {}).get("host_metadata", {}).get("stderr_path"),
        "finished_marker": (start_marker.parent / "finished.json").is_file(),
        "no_proof_claim": True,
    }
    if (host_execution.get("exit_code", 0) == 0 or "errored" not in status or
            cycle["errors"] or original_attempt.status != "agent_error" or
            not repair_requests or final.nodes[node_id].status != "in_progress"):
        report["status"] = "failed"
        _write_json(run / "child-stdout.json", {"stdout": stdout, "stderr": stderr})
        _write_json(run / "report.json", report)
        raise RuntimeError(f"interruption recovery invariant failed: {report}")
    _write_json(run / "report.json", report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--child", type=Path, help=argparse.SUPPRESS)
    parser.add_argument("--codex", default="codex")
    parser.add_argument("--timeout", type=int, default=75)
    parser.add_argument("--wait-seconds", type=int, default=45)
    args = parser.parse_args()
    if args.child:
        return _child(args.child, args.codex, args.timeout)
    try:
        report = run(args.codex, wait_seconds=args.wait_seconds)
    except Exception as exc:
        print(f"failed: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "passed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
