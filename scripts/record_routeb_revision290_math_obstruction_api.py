"""Record the opt-in mathematical obstruction-order API and focused proof."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from record_routeb_port_progress import ROOT, ref
from percolation_workflow.store import StateStore


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    if state.revision != 289 or state.registry:
        raise ValueError("revision-290 recorder requires revision 289 and empty registry")
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v243.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v244.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260908/state-before-revision290.json"
    module = ROOT / "src/percolation_workflow/math_frontier.py"
    test = ROOT / "tests/test_math_frontier_policy.py"
    required = [old, module, test]
    if not all(path.is_file() for path in required):
        raise ValueError("missing math obstruction API evidence")
    source = module.read_text(encoding="utf-8")
    if "rank_math_obstruction_frontier" not in source or "math_bottleneck" not in source:
        raise ValueError("math obstruction API was not found")
    record = {
        "kind": "routeb_math_obstruction_frontier_api",
        "status": "FOCUSED_TEST_PASS_AUDIT_ONLY",
        "evidence_level": "read-only-math-priority-api",
        "files": [ref(module), ref(test)],
        "bottleneck_order": ["coverage", "physical_schur_binding", "interval_sign", "central_fd"],
        "api": "rank_math_obstruction_frontier",
        "ordinary_dispatch_gate_unchanged": True,
        "obstructed_nodes_dispatchable": False,
        "focused_test": "tests/test_math_frontier_policy.py:7 passed",
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph = json.loads(old.read_text(encoding="utf-8"))
    graph.setdefault("workflow_repairs", []).append(record)
    graph.setdefault("bottleneck_audits", []).append(record)
    graph.setdefault("external_intakes", []).append(record)
    graph.setdefault("open_frontier_updates", []).append({
        "node": "routeb_math_obstruction_frontier_api",
        "status": "audit_order_available_dispatch_gate_preserved",
        "reason": "The coordinator can expose coverage-first mathematical bottlenecks without dispatching rank-1/2 obstructed leaves.",
    })
    graph.update(schema="routeb-proposed-proof-dag-v244", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision290_math_obstruction_api/v1",
        "graph_sha256": digest,
        "roots": [],
        "selected_nodes": [],
        "source": str(module),
        "evidence_sha256": sha(module),
        "focused_test_pass": True,
        "audit_only": True,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision290_math_obstruction_api_recorded",
        proposed_dag=ref(new),
        proposed_dag_sha256=digest,
        obstruction_order=record["bottleneck_order"],
        default_dispatch_unchanged=True,
        obstructed_nodes_remain_non_dispatchable=True,
        registry_promoted=False,
        formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name, "registry": len(state.registry)}))


if __name__ == "__main__":
    main()
