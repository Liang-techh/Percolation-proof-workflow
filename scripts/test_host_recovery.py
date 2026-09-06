"""Exercise abrupt coordinator interruption and host-agent lease recovery.

This is an integration harness for the durable boundary, not a proof fixture:
the child process exits with ``os._exit`` after persisting a bound request.  The
parent then observes the durable reclaim action, closes the timed-out attempt,
and prepares a fresh request for the reopened frontier.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from percolation_workflow.agent_bridge import bind_agent, prepare_requests
from percolation_workflow.host_cycle import run_host_cycle
from percolation_workflow.model import WorkflowState
from percolation_workflow.research import next_actions
from percolation_workflow.store import StateStore


def _child(state_path: Path, request_id: str) -> None:
    store = StateStore(state_path)
    bind_agent(store, request_id, "crash-fixture-agent", lease_seconds=1)
    state = store.load()
    state.event("simulated_coordinator_crash", request_id=request_id,
                note="abrupt os._exit after durable bind")
    store.save(state)
    os._exit(73)


def run(output: Path | None = None) -> dict:
    with tempfile.TemporaryDirectory(prefix="percolation-host-recovery-") as directory:
        root = Path(directory)
        state_path = root / "state.json"
        store = StateStore(state_path)
        state = WorkflowState()
        node_id = state.add_node(
            "goal", "theorem goal : True",
            metadata={"statement_status": "indexed"},
        )
        store.save(state)
        request = prepare_requests(store, limit=1)[0]
        child = subprocess.run(
            [sys.executable, str(Path(__file__).resolve()), "--child",
             str(state_path), request["request_id"]],
            cwd=str(Path(__file__).resolve().parents[1]),
            env={**os.environ, "PYTHONPATH": str(Path(__file__).resolve().parents[1] / "src")},
            capture_output=True,
            text=True,
            check=False,
        )
        if child.returncode != 73:
            raise RuntimeError(f"crash fixture returned {child.returncode}: {child.stderr}")
        after_crash = store.load()
        action_before = next_actions(store)
        if not action_before or action_before[0]["kind"] != "observe_agent":
            raise RuntimeError(f"expected active observation before expiry, got {action_before}")
        time.sleep(1.15)
        action_after = next_actions(store)
        if not action_after or action_after[0]["kind"] != "reclaim_expired_agent":
            raise RuntimeError(f"expected reclaim action after expiry, got {action_after}")
        cycle = run_host_cycle(store)
        if cycle["reclaimed_requests"] != [request["request_id"]] or not cycle["dispatch"]:
            raise RuntimeError(f"host cycle did not reclaim and redispatch: {cycle}")
        recovered = store.load()
        attempt_id = recovered.agent_requests[request["request_id"]]["attempt_id"]
        if recovered.nodes[node_id].status != "in_progress":
            raise RuntimeError("reclaimed node was not reopened and redispatched")
        if recovered.attempts[attempt_id].status != "agent_timeout":
            raise RuntimeError("reclaimed attempt was not marked agent_timeout")
        next_request = cycle["dispatch"][0]
        final = store.load()
        report = {
            "status": "passed",
            "child_exit_code": child.returncode,
            "request_id": request["request_id"],
            "timed_out_attempt_id": attempt_id,
            "next_request_id": next_request["request_id"],
            "node_status": final.nodes[node_id].status,
            "timed_out_attempt_status": final.attempts[attempt_id].status,
            "observed_event": any(e["kind"] == "simulated_coordinator_crash" for e in after_crash.events),
            "next_action_before_expiry": action_before[0]["kind"],
            "next_action_after_expiry": action_after[0]["kind"],
            "cycle_reclaimed_requests": cycle["reclaimed_requests"],
        }
        if output is not None:
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--child", nargs=2, metavar=("STATE", "REQUEST"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.child:
        _child(Path(args.child[0]), args.child[1])
        return 73
    print(json.dumps(run(args.output), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
