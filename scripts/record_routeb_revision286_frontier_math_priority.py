"""Record a non-admitting math-priority overlay for the open frontier."""
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
    if state.revision != 285 or state.registry:
        raise ValueError("revision-286 recorder requires revision 285 and empty registry")
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v239.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v240.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260908/state-before-revision286.json"
    side = ROOT / "artifacts/task_FLT_frontier_math_priority_20260908"
    required = [old, side / "REPORT.md", side / "receipt.json", side / "check_priority_overlay.py"]
    if not all(path.is_file() for path in required):
        raise ValueError("missing frontier priority evidence")
    receipt = json.loads((side / "receipt.json").read_text(encoding="utf-8"))
    record = {
        "kind": "routeb_math_frontier_priority_overlay",
        "status": receipt.get("status", "FOCUSED_OVERLAY_PASS_NON_DISPATCH"),
        "evidence_level": "focused-scheduler-overlay",
        "files": [ref(side / name) for name in ("REPORT.md", "receipt.json", "check_priority_overlay.py")],
        "priority_order": ["coverage", "physical_schur_binding", "interval_sign", "central_fd"],
        "default_scheduler_unchanged": True,
        "dispatch_eligibility_changed": False,
        "closure_changed": False,
        "dependencies_changed": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph = json.loads(old.read_text(encoding="utf-8"))
    graph.setdefault("workflow_repairs", []).append(record)
    graph.setdefault("bottleneck_audits", []).append(record)
    graph.setdefault("external_intakes", []).append(record)
    graph.setdefault("open_frontier_updates", []).append({
        "node": "routeb_math_frontier_priority",
        "status": "overlay_order_recorded_no_dispatch",
        "reason": "The overlay exposes the mathematical bottleneck order while preserving default scheduler filtering and proof closure semantics.",
    })
    graph.update(schema="routeb-proposed-proof-dag-v240", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision286_frontier_math_priority/v1",
        "graph_sha256": digest,
        "roots": [],
        "selected_nodes": [],
        "source": "focused math frontier priority overlay",
        "evidence_sha256": sha(side / "receipt.json"),
        "overlay_only": True,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision286_frontier_math_priority_recorded",
        proposed_dag=ref(new),
        proposed_dag_sha256=digest,
        priority_order=record["priority_order"],
        default_scheduler_unchanged=True,
        dispatch_eligibility_changed=False,
        registry_promoted=False,
        formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name, "registry": len(state.registry)}))


if __name__ == "__main__":
    main()
