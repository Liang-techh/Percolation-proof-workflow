"""Real compiler recovery across os._exit; synthetic host response, NOT a live proof agent.

Writes only new runs under artifacts/compile_recovery. No source/test edits, worker
restarts, comparator calls, or registry promotion. Exit 0 = passed, 1 = failed,
2 = undetermined (bounded wait expired). Run with: python -B scripts/test_compile_process_recovery.py
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import traceback
import uuid
from datetime import datetime, timezone

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts" / "compile_recovery"
sys.path.insert(0, str(ROOT / "src"))

from percolation_workflow.agent_bridge import (  # noqa: E402
    bind_agent, collect_candidate, prepare_requests, record_result, start_candidate,
)
from percolation_workflow.model import WorkflowState  # noqa: E402
from percolation_workflow.store import StateStore  # noqa: E402

CRASH_CODE = 73
DISCLAIMER = "Synthetic host-response fixture; NOT a live proof agent or proof-agent result."


class Undetermined(RuntimeError):
    pass


def write(path: Path, value: str) -> None:
    path = path.resolve()
    if not path.is_relative_to(OUTPUT.resolve()):
        raise ValueError(f"output outside experiment directory: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def write_json(path: Path, value: object) -> None:
    write(path, json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def child(case: Path, timeout: float) -> None:
    """Only the child owns the original Popen handle; exit without joining it."""
    require(case.resolve().is_relative_to(OUTPUT.resolve()), "invalid child output path")
    config = load_json(case / "case.json")
    store = StateStore(case / "state.json")
    worker = start_candidate(store, config["request_id"], case / "fixture",
                             case / "fixture" / "Candidate.lean")
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        # The marker establishes that real Lean reached our IO action, NOT liveness.
        # Liveness of the launched worker is checked using its actual Popen handle.
        status = worker.poll()
        if status is not None:
            raise RuntimeError(f"worker exited before crash barrier: {status}")
        if (case / "fixture" / "compiler-entered.json").is_file():
            request = store.load().agent_requests[config["request_id"]]
            require(not (Path(request["compile_job"]) / "result.json").exists(),
                    "receipt unexpectedly completed before coordinator exit")
            observed_status = worker.poll()
            require(observed_status is None, "worker terminated before crash snapshot")
            write_json(case / "child-observation.json", {
                "coordinator_pid": os.getpid(), "worker_pid": worker.pid,
                "worker_poll": observed_status, "liveness_evidence": "Popen.poll()",
                "lean_entered_barrier": True, "receipt_present": False,
                "intended_exit_code": CRASH_CODE, "disclaimer": DISCLAIMER,
            })
            os._exit(CRASH_CODE)
        time.sleep(0.05)
    raise Undetermined("compiler did not reach barrier before bounded child timeout")


def fixture_source(fail: bool) -> str:
    proof = "by recovery_intentionally_invalid_tactic" if fail else "by omega"
    return '''-- Synthetic candidate authored by the recovery experiment, NOT a live proof agent.
#eval do
  IO.FS.withFile "compiler-invocations.jsonl" .append fun h =>
    h.putStrLn "{\\"event\\":\\"real_lean_candidate_execution\\"}"
  IO.FS.writeFile "compiler-entered.json" "{\\"entered\\":true}"
  IO.println "RECOVERY_STDOUT_BEGIN"
  IO.eprintln "RECOVERY_STDERR_BEGIN"
  let mut released := false
  for _ in [:1200] do
    if (← System.FilePath.pathExists "release-compiler") then
      released := true
      break
    IO.sleep 100
  unless released do
    throw (IO.userError "recovery barrier timed out")
  IO.println "RECOVERY_STDOUT_END"
  IO.eprintln "RECOVERY_STDERR_END"

theorem recovery_candidate (n : Nat) : n + 1 ≤ n + 2 := ''' + proof + '''
#check recovery_candidate
'''


def run_case(run: Path, name: str, fail: bool, timeout: float) -> dict:
    case = run / name
    fixture = case / "fixture"
    fixture.mkdir(parents=True)
    toolchain = (ROOT / "examples/minimal_lean/lean-toolchain").read_text(encoding="utf-8")
    write(fixture / "lean-toolchain", toolchain)
    write(fixture / "lakefile.toml", 'name = "compileRecovery"\nversion = "0.1.0"\n')
    write(fixture / "Candidate.lean", fixture_source(fail))
    store = StateStore(case / "state.json")
    state = WorkflowState(project="isolated-real-compile-recovery")
    state.add_node("recovery_candidate", "(n : Nat) : n + 1 ≤ n + 2",
                   proof_sketch="Synthetic experiment: discharge Nat inequality with omega.",
                   metadata={"statement_status": "indexed", "experiment": DISCLAIMER})
    store.save(state)
    request, = prepare_requests(store, limit=1)
    request_id = request["request_id"]
    agent_id = "synthetic-not-live-proof-agent-" + uuid.uuid4().hex
    bind_agent(store, request_id, agent_id)
    response = {"disclaimer": DISCLAIMER, "synthetic": True,
                "status": {agent_id: {"completed": "Synthetic candidate fixture prepared."}}}
    write_json(case / "synthetic-host-response.json", response)
    record_result(store, request_id, agent_id, response)
    write_json(case / "case.json", {"request_id": request_id, "expected_success": not fail,
                                    "disclaimer": DISCLAIMER})
    before = store.load().to_dict()
    write_json(case / "before-crash-state.json", before)

    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    temp = case / "tmp"
    temp.mkdir()
    env.update(TMP=str(temp), TEMP=str(temp), TMPDIR=str(temp))
    command = [sys.executable, "-B", str(Path(__file__).resolve()), "--child", str(case),
               "--timeout", str(timeout)]
    with (case / "coordinator.stdout.log").open("wb") as stdout, \
            (case / "coordinator.stderr.log").open("wb") as stderr:
        coordinator = subprocess.Popen(command, env=env, stdin=subprocess.DEVNULL,
                                       stdout=stdout, stderr=stderr,
                                       creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
        try:
            exit_code = coordinator.wait(timeout=timeout + 10)
        except subprocess.TimeoutExpired:
            write_json(case / "parent-observation.json", {
                "coordinator_pid": coordinator.pid, "exit_code": None,
                "status": "undetermined", "worker_restart_count": 0})
            raise Undetermined("coordinator exit not observed within bounded wait; no restart")
    write_json(case / "parent-observation.json", {
        "parent_pid": os.getpid(), "coordinator_pid": coordinator.pid,
        "exit_code": exit_code, "evidence": "Popen.wait() returned actual process exit code",
        "worker_restart_count": 0, "worker_liveness_after_crash": "not inferred",
    })
    if exit_code == 2:
        raise Undetermined("child timed out waiting for actual Lean execution; inspect child logs")
    require(exit_code == CRASH_CODE, f"child exit was {exit_code}, expected {CRASH_CODE}; see logs")

    # A fresh object reloads the durable checkpoint after the actual process exit.
    resumed = StateStore(case / "state.json")
    checkpoint = resumed.load()
    write_json(case / "after-crash-state.json", checkpoint.to_dict())
    require(checkpoint.registry == {}, "registry must be empty at crash checkpoint")
    require(checkpoint.agent_requests[request_id]["status"] == "checking", "missing checkpoint")
    require(collect_candidate(resumed, request_id) is None,
            "collection before barrier release must report unknown")
    write(fixture / "release-compiler", "Parent observed coordinator exit before releasing real Lean.\n")
    deadline = time.monotonic() + timeout
    result = None
    while time.monotonic() < deadline:
        result = collect_candidate(StateStore(case / "state.json"), request_id)
        if result is not None:
            break
        time.sleep(0.1)
    if result is None:
        raise Undetermined("no receipt within bounded wait; worker state unknown; no automatic restart")

    final = StateStore(case / "state.json").load()
    req = final.agent_requests[request_id]
    job = Path(req["compile_job"])
    receipt = load_json(job / "result.json")
    attempt = final.attempts[req["compile_attempt_id"]]
    compiler_attempts = [a for a in final.attempts.values() if a.agent_id == "compiler-coordinator"]
    invocations = (fixture / "compiler-invocations.jsonl").read_text().splitlines()
    require(len(compiler_attempts) == 1 and len(invocations) == 1, "expected exactly one real compile")
    require(len(list(job.parent.iterdir())) == 1, "unexpected additional compiler job")
    require(len(final.attempts) == 2, "expected one synthetic report plus one compiler attempt")
    require(final.registry == {}, "compile result must not enter registry")
    require(result is (not fail), f"unexpected Lean result: {receipt}")
    require(attempt.status == ("compile_error" if fail else "compiled"), "wrong attempt status")
    require(req["status"] == "checked", "receipt was not collected")
    for field in ("command", "stdout", "stderr", "exit_code"):
        require(getattr(attempt, field) == receipt["result"][field], f"lost diagnostic field {field}")
    diagnostics = attempt.stdout + "\n" + attempt.stderr
    for marker in ("RECOVERY_STDOUT_BEGIN", "RECOVERY_STDOUT_END",
                   "RECOVERY_STDERR_BEGIN", "RECOVERY_STDERR_END"):
        require(marker in diagnostics, f"missing real compiler diagnostic {marker}")
    if fail:
        require("error:" in diagnostics and "unknown tactic" in diagnostics,
                "missing intentional Lean error diagnostic")
    started = load_json(job / "started.json")
    observation = load_json(case / "child-observation.json")
    require(started["pid"] == observation["worker_pid"], "worker identity mismatch")
    require(started["attempt_id"] == attempt.id, "worker attempt mismatch")
    require(observation["coordinator_pid"] == coordinator.pid, "coordinator identity mismatch")
    # Collecting twice must be idempotent: neither a second compile nor a new event.
    saved = (case / "state.json").read_bytes()
    require(collect_candidate(StateStore(case / "state.json"), request_id) is result,
            "repeat collection result changed")
    require((case / "state.json").read_bytes() == saved, "repeat collection mutated state")
    require((fixture / "compiler-invocations.jsonl").read_text().splitlines() == invocations,
            "repeat collection caused another compile")
    write(case / "lean.stdout.log", attempt.stdout)
    write(case / "lean.stderr.log", attempt.stderr)
    summary = {"case": name, "status": "passed", "disclaimer": DISCLAIMER,
               "coordinator_exit_code": exit_code, "worker_pid": started["pid"],
               "compile_exit_code": attempt.exit_code, "compile_status": attempt.status,
               "real_compile_count": len(invocations), "compiler_attempt_count": len(compiler_attempts),
               "registry": final.registry, "diagnostics_match_receipt": True,
               "collection_before_release": None, "repeat_collection_idempotent": True,
               "worker_restart_count": 0, "receipt": str(job / "result.json"),
               "stdout_characters": len(attempt.stdout), "stderr_characters": len(attempt.stderr)}
    write_json(case / "verification.json", summary)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--child", type=Path, help=argparse.SUPPRESS)
    parser.add_argument("--timeout", type=float, default=60.0)
    args = parser.parse_args()
    if not 1 <= args.timeout <= 90:
        parser.error("--timeout must be between 1 and 90 seconds")
    if args.child:
        try:
            child(args.child, args.timeout)
        except Undetermined:
            traceback.print_exc()
            return 2
        return 1
    run = OUTPUT / (datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8])
    run.mkdir(parents=True)
    inputs = [Path(__file__).resolve(), *(ROOT / "src/percolation_workflow" / name for name in
              ("agent_bridge.py", "compile_worker.py", "lean.py", "store.py", "model.py"))]
    hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}
    report = {"status": "running", "disclaimer": DISCLAIMER, "run_directory": str(run),
              "timeout_seconds_per_phase": args.timeout, "input_sha256": hashes, "cases": []}
    write_json(run / "report.json", report)
    print(f"Experiment output: {run}", flush=True)
    code = 0
    try:
        for name, fail in (("success", False), ("compile-error", True)):
            report["cases"].append(run_case(run, name, fail, args.timeout))
            print(f"{name}: passed", flush=True)
        require(all(hashlib.sha256(p.read_bytes()).hexdigest() == hashes[str(p.relative_to(ROOT))]
                    for p in inputs), "experiment implementation changed during execution")
        report["status"] = "passed"
    except Exception as exc:
        code = 2 if isinstance(exc, Undetermined) else 1
        report.update(status="undetermined" if code == 2 else "failed", error=str(exc))
        write(run / "exception.log", traceback.format_exc())
        print(f"{report['status']}: {exc}", flush=True)
    write_json(run / "report.json", report)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
