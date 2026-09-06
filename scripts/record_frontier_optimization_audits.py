"""Record the next independent frontier audits as non-admitting evidence."""
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
    assert state.revision == 219 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v173.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v174.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision220.json"
    specs = [
        (
            "task_FT_partition_certificate_bottleneck_20260907",
            "obligations.json",
            ["REPORT.md", "obligations.json", "provenance.md"],
            "partition_certificate",
            "complete indexed partition and cellwise margin receipt remains open; minimum partition is 33^4",
        ),
        (
            "task_FU_scheduler_bottleneck_20260907",
            "design.json",
            ["REPORT.md", "design.json", "provenance.md"],
            "reduction_closure_batch",
            "compiled children lack an optional batch closure handoff; proposed optimization is design-only",
        ),
        (
            "task_FV_flt_finite_dimensional_scan_20260907",
            "candidates.json",
            ["REPORT.md", "candidates.json", "checker.py"],
            "flt_finite_dimensional_scan",
            "8 finite-dimensional and inner-product candidates are classified with pin provenance; no Route-B theorem is admitted",
        ),
    ]
    assert old.is_file() and not new.exists()
    graph = json.loads(old.read_text(encoding="utf-8"))
    audits = []
    for dirname, json_name, names, node, reason in specs:
        sidecar = ROOT / "artifacts" / dirname
        files = [sidecar / name for name in names]
        assert all(path.is_file() for path in files)
        payload = json.loads((sidecar / json_name).read_text(encoding="utf-8"))
        if isinstance(payload, dict):
            items = payload.get("obligations", payload.get("candidates", payload.get("leaves", [])))
        else:
            items = []
        audit = {
            "kind": f"routeb_{node}_audit",
            "status": "OPEN_FAIL_CLOSED",
            "evidence_level": "independent_sidecar_audit",
            "semantic_boundary": reason,
            "sidecar": str(sidecar.resolve()),
            "payload_sha256": sha(sidecar / json_name),
            "item_count": len(items) if isinstance(items, list) else None,
            "files": [ref(path) for path in files],
            "registry_promoted": False,
            "formal_certificate_allowed": False,
        }
        audits.append(audit)
        graph.setdefault("external_intakes", []).append(
            {
                "kind": audit["kind"],
                "source": "local-routeb-frontier-optimization-audit",
                "sidecar": audit["sidecar"],
                "payload_sha256": audit["payload_sha256"],
                "item_count": audit["item_count"],
                "files": audit["files"],
                "registry_promoted": False,
                "formal_certificate_allowed": False,
            }
        )
        graph.setdefault("bottleneck_audits", []).append(audit)
        graph.setdefault("open_frontier_updates", []).append(
            {"node": audit["kind"], "status": "open_fail_closed", "reason": reason}
        )
    graph.update(schema="routeb-proposed-proof-dag-v174", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)

    digest = sha(new)
    state.graph_artifacts.append(
        {
            "schema_version": 1,
            "algorithm": "routeb_frontier_optimization_audits/v1",
            "graph_sha256": digest,
            "roots": [],
            "selected_nodes": [],
            "source": "independent-sidecars:FT,FU,FV",
            "evidence_sha256": sha(ROOT / "artifacts/task_FT_partition_certificate_bottleneck_20260907/obligations.json"),
            "registry_promoted": False,
            "formal_certificate_allowed": False,
        }
    )
    state.event(
        "routeb_frontier_optimization_audits_recorded",
        proposed_dag=ref(new),
        proposed_dag_sha256=digest,
        audits=[
            {"kind": audit["kind"], "status": audit["status"], "item_count": audit["item_count"]}
            for audit in audits
        ],
        registry_promoted=False,
        formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new.name, "audits": len(audits), "registry": len(state.registry)})


if __name__ == "__main__":
    main()
