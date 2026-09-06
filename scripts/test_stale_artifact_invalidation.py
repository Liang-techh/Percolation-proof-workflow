"""Exercise source-drift detection and dependency invalidation on a fresh Lean run.

The fixture deliberately uses the small public Lean example and a synthetic
trusted comparator line.  It is a freshness/invalidation experiment, not a
claim that the fixture is a research proof: the fixture still contains the
expected ``sorry`` placeholders.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
import shutil
import sys
import tempfile
import uuid

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from percolation_workflow.model import NodeStatus, WorkflowState
from percolation_workflow.registry import audit_registry, invalidate_dependents
from percolation_workflow.statements import index_statements
from percolation_workflow.store import StateStore
from percolation_workflow.verification import source_snapshot, verify_and_register


DISCLAIMER = (
    "Fresh source-drift and registry invalidation experiment; the minimal fixture contains "
    "sorry placeholders and no research-proof success is claimed."
)


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run(output: Path | None = None) -> dict:
    run_dir = ROOT / "artifacts" / "stale_artifact_invalidation" / (
        datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]
    )
    with tempfile.TemporaryDirectory(prefix="percolation-stale-artifact-") as directory:
        project = Path(directory) / "minimal_lean"
        source = ROOT / "examples" / "minimal_lean"
        shutil.copytree(
            source,
            project,
            ignore=shutil.ignore_patterns(".lake", "*.olean", "*.ilean", "*.hash", "*.trace"),
        )
        comparator = json.loads((project / "comparator.json").read_text(encoding="utf-8"))
        comparator["enable_nanoda"] = True
        (project / "comparator.json").write_text(
            json.dumps(comparator, indent=2) + "\n", encoding="utf-8"
        )

        declaration = next(
            record for record in index_statements(project / "Challenge.lean")
            if record.qualified_name == "Minimal.main"
        )
        state_path = Path(directory) / "state.json"
        store = StateStore(state_path)
        state = WorkflowState(project="stale-artifact-invalidation")
        node_id = state.add_node(
            "Minimal.main",
            declaration.source,
            proof_sketch="Register once, mutate a source, audit, then reopen the stale node.",
            metadata={"statement_status": "indexed"},
        )
        store.save(state)
        comparator_command = [
            sys.executable,
            "-c",
            "print('Your solution is okay!')",
        ]
        registered = verify_and_register(
            store.load(),
            node_id,
            project,
            comparator_command,
            store=store,
        )
        if not registered:
            raise RuntimeError("fresh verification did not register the fixture")
        before = store.load()
        original_hashes = before.registry[node_id]["verification_receipt"]["source_hashes"]
        (project / "Solution.lean").write_text(
            (project / "Solution.lean").read_text(encoding="utf-8")
            + "\n-- deliberate post-registration source drift\n",
            encoding="utf-8",
        )
        current_hashes = source_snapshot(project)
        audit = audit_registry(store.load())
        if audit[node_id]["status"] != "stale":
            raise RuntimeError(f"source drift was not classified as stale: {audit}")
        invalidated = invalidate_dependents(
            store.load(), [node_id], reason="deliberate Solution.lean source drift", store=store
        )
        final = store.load()
        report = {
            "status": "passed",
            "disclaimer": DISCLAIMER,
            "run_directory": str(run_dir),
            "project_fixture": str(project),
            "node_id": node_id,
            "registered_before_drift": registered,
            "source_hash_changed": original_hashes != current_hashes,
            "audit_status_after_drift": audit[node_id]["status"],
            "audit_reason_after_drift": audit[node_id]["reason"],
            "invalidated_nodes": sorted(invalidated),
            "final_node_status": final.nodes[node_id].status,
            "final_registry": final.registry,
            "previous_verification_count": len(
                final.nodes[node_id].metadata.get("previous_verifications", [])
            ),
            "frontier_contains_node": node_id in {item.id for item in final.frontier()},
        }
        if not (
            report["source_hash_changed"]
            and report["audit_status_after_drift"] == "stale"
            and report["final_node_status"] == NodeStatus.OPEN
            and not report["final_registry"]
            and report["previous_verification_count"] == 1
            and report["frontier_contains_node"]
        ):
            report["status"] = "failed"
            _write_json(run_dir / "report.json", report)
            raise RuntimeError(f"stale-artifact invariant failed: {report}")
        _write_json(run_dir / "report.json", report)
        if output is not None:
            _write_json(output, report)
        return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        report = run(args.output)
    except Exception as exc:
        print(f"failed: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "passed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
