"""Exercise recovery when a coordinator dies immediately before worker spawn.

The child process writes the durable compile checkpoint and launch intent, then
exits before invoking ``Popen``.  A fresh host-cycle must recover that exact
attempt as a compile error and prepare one repair request.  No worker or proof
result is created by this experiment.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from datetime import datetime, timezone
import uuid

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from percolation_workflow.agent_bridge import bind_agent, prepare_requests, record_result, reclaim_dead_compile, start_candidate
from percolation_workflow.host_cycle import run_host_cycle
from percolation_workflow.model import WorkflowState
from percolation_workflow.store import StateStore


DISCLAIMER = "Real coordinator process interruption before worker spawn; no proof success is claimed."
EXIT_CODE = 73


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _child(run: Path, request_id: str) -> int:
    import percolation_workflow.agent_bridge as bridge

    def crash_before_spawn(*args, **kwargs):
        os._exit(EXIT_CODE)

    bridge.subprocess.Popen = crash_before_spawn
    store = StateStore(run / "state.json")
    start_candidate(store, request_id, run / "fixture", run / "fixture" / "Candidate.lean")
    return 1


def run(*, wait_seconds: int = 30) -> dict:
    run = ROOT / "artifacts" / "coordinator_crash_recovery" / (
        datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8])
    fixture = run / "fixture"
    fixture.mkdir(parents=True)
    (fixture / "lean-toolchain").write_text(
        (ROOT / "examples/minimal_lean/lean-toolchain").read_text(encoding="utf-8"), encoding="utf-8")
    (fixture / "lakefile.toml").write_text('name = "coordinatorCrashRecovery"\n', encoding="utf-8")
    (fixture / "Candidate.lean").write_text('theorem goal : True := by trivial\n', encoding="utf-8")
    store = StateStore(run / "state.json")
    state = WorkflowState(project="coordinator-crash-recovery")
    node_id = state.add_node("goal", "theorem goal : True",
                             proof_sketch="Crash after compile checkpoint and before worker spawn.",
                             metadata={"statement_status": "indexed", "experiment": DISCLAIMER})
    store.save(state)
    request = prepare_requests(store, limit=1)[0]
    request_id = request["request_id"]
    bind_agent(store, request_id, "synthetic-candidate-agent")
    record_result(store, request_id, "synthetic-candidate-agent",
                  {"status": {"synthetic-candidate-agent": {"completed": "candidate prepared"}}})
    child = subprocess.Popen([
        sys.executable, "-B", str(Path(__file__).resolve()), "--child", str(run), request_id],
        cwd=ROOT, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
    child_stdout, child_stderr = child.communicate(timeout=wait_seconds)
    if child.returncode != EXIT_CODE:
        raise RuntimeError(f"coordinator crash fixture returned {child.returncode}: {child_stderr}")
    checkpoint = store.load()
    request_state = checkpoint.agent_requests[request_id]
    job = Path(request_state["compile_job"])
    intent = json.loads((job / "coordinator-intent.json").read_text(encoding="utf-8"))
    if (job / "started.json").exists() or (job / "spawned.json").exists():
        raise RuntimeError("worker marker exists despite pre-spawn crash")
    cycle = run_host_cycle(store)
    final = store.load()
    original_attempt = final.attempts[request_state["compile_attempt_id"]]
    repair = [item for item in final.agent_requests.values()
              if item.get("repair_of_attempt_id") == request_state["compile_attempt_id"]]
    report = {
        "status": "passed",
        "disclaimer": DISCLAIMER,
        "run_directory": str(run),
        "request_id": request_id,
        "crashed_coordinator_pid": intent["coordinator_pid"],
        "child_exit_code": child.returncode,
        "cycle_reclaimed_compilations": cycle["reclaimed_compilations"],
        "cycle_errors": cycle["errors"],
        "compile_attempt_status": original_attempt.status,
        "compile_attempt_exit_code": original_attempt.exit_code,
        "node_status": final.nodes[node_id].status,
        "repair_request_count": len(repair),
        "worker_started_marker": (job / "started.json").exists(),
        "worker_spawned_marker": (job / "spawned.json").exists(),
        "registry": final.registry,
        "child_stdout": child_stdout,
        "child_stderr": child_stderr,
    }
    if (cycle["errors"] or cycle["reclaimed_compilations"] != [request_id] or
            original_attempt.status != "compile_error" or original_attempt.exit_code != 125 or
            final.nodes[node_id].status != "in_progress" or len(repair) != 1 or
            final.registry or report["worker_started_marker"] or report["worker_spawned_marker"]):
        report["status"] = "failed"
        _write_json(run / "report.json", report)
        raise RuntimeError(f"coordinator crash recovery invariant failed: {report}")
    _write_json(run / "report.json", report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--child", nargs=2, metavar=("RUN", "REQUEST"), help=argparse.SUPPRESS)
    parser.add_argument("--wait-seconds", type=int, default=30)
    args = parser.parse_args()
    if args.child:
        return _child(Path(args.child[0]), args.child[1])
    try:
        report = run(wait_seconds=args.wait_seconds)
    except Exception as exc:
        print(f"failed: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "passed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
