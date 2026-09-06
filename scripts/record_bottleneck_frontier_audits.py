"""Append independent mathematical bottleneck audits to the open frontier."""
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
    assert state.revision == 218 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v172.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v173.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision219.json"
    specs = [
        (
            "task_FQ_true_dh_schur_bottleneck_20260907",
            "obligations.json",
            ["REPORT.md", "obligations.json", "provenance.md"],
            "true_dh_schur",
            "OPEN_FAIL_CLOSED",
            "true-DH physical Schur bridge remains open; symbolic obligations and missing assumptions are recorded",
        ),
        (
            "task_FR_residual_coverage_bottleneck_20260907",
            "obligations.json",
            ["REPORT.md", "obligations.json", "provenance.json", "evidence.md"],
            "residual_coverage",
            "OPEN_FAIL_CLOSED",
            "18 residual-absorption and partition-coverage obligations are recorded without global closure",
        ),
        (
            "task_FS_terminal_flowpipe_bottleneck_20260907",
            "theorem_leaves.json",
            ["REPORT.md", "theorem_leaves.json", "provenance.md", "evidence.md"],
            "terminal_flowpipe",
            "OPEN_FAIL_CLOSED",
            "terminal-transfer and flowpipe frontier FP0-FP6 remains open; numerical evidence is not promoted",
        ),
    ]
    assert old.is_file() and not new.exists()
    graph = json.loads(old.read_text(encoding="utf-8"))
    audits = []
    for dirname, json_name, names, node, status, reason in specs:
        sidecar = ROOT / "artifacts" / dirname
        files = [sidecar / name for name in names]
        assert all(path.is_file() for path in files)
        payload = json.loads((sidecar / json_name).read_text(encoding="utf-8"))
        audit = {
            "kind": f"routeb_{node}_bottleneck_audit",
            "status": status,
            "evidence_level": "independent_sidecar_mathematical_audit",
            "semantic_boundary": reason,
            "sidecar": str(sidecar.resolve()),
            "payload_sha256": sha(sidecar / json_name),
            "payload_summary": {
                "top_level_keys": sorted(payload),
                "obligation_count": len(payload.get("obligations", [])) if isinstance(payload, dict) else None,
                "leaf_count": len(payload.get("leaves", [])) if isinstance(payload, dict) else None,
            },
            "files": [ref(path) for path in files],
            "registry_promoted": False,
            "formal_certificate_allowed": False,
        }
        audits.append(audit)
        graph.setdefault("external_intakes", []).append(
            {
                "kind": audit["kind"],
                "source": "local-routeb-bottleneck-audit",
                "sidecar": audit["sidecar"],
                "payload_sha256": audit["payload_sha256"],
                "files": audit["files"],
                "registry_promoted": False,
                "formal_certificate_allowed": False,
            }
        )
        graph.setdefault("bottleneck_audits", []).append(audit)
        graph.setdefault("open_frontier_updates", []).append(
            {"node": audit["kind"], "status": "open_fail_closed", "reason": reason}
        )
    graph.update(schema="routeb-proposed-proof-dag-v173", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)

    digest = sha(new)
    state.graph_artifacts.append(
        {
            "schema_version": 1,
            "algorithm": "routeb_bottleneck_frontier_audits/v1",
            "graph_sha256": digest,
            "roots": [],
            "selected_nodes": [],
            "source": "independent-sidecars:FQ,FR,FS",
            "evidence_sha256": sha(ROOT / "artifacts/task_FR_residual_coverage_bottleneck_20260907/obligations.json"),
            "registry_promoted": False,
            "formal_certificate_allowed": False,
        }
    )
    state.event(
        "routeb_bottleneck_frontier_audits_recorded",
        proposed_dag=ref(new),
        proposed_dag_sha256=digest,
        audits=[
            {"kind": audit["kind"], "status": audit["status"], "payload_sha256": audit["payload_sha256"]}
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
