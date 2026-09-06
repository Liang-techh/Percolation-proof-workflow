"""Persist the next RHS, receipt, and terminal-attachment frontier audits."""
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
    assert state.revision == 225 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v179.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v180.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision226.json"
    specs = [
        ("task_GY_rhs_binding_contract_20260907", ["REPORT.md", "fields.json", "provenance.md"], "rhs_binding_contract", "OPEN_FAIL_CLOSED", "Float64, finite-difference, and Julia solve exact-real enclosures remain unresolved."),
        ("task_GAA_partition_validator_probe_20260907", ["REPORT.md", "fixture.json", "validate.py", "provenance.md"], "partition_validator_probe", "CURRENT_PIN_VALIDATOR_PASS_NON_COVERAGE", "One synthetic partition receipt validates deterministically; coverage_complete remains false and no 33^4 enumeration occurred."),
        ("task_GAB_terminal_parent_attachment_20260907", ["REPORT.md", "attachment.json", "provenance.md"], "terminal_parent_attachment", "OPEN_FAIL_CLOSED", "GB conditional terminal theorem is mapped to M4 parent/child gates without bypassing comparator or registry."),
    ]
    assert old.is_file() and not new.exists()
    graph = json.loads(old.read_text(encoding="utf-8"))
    audits = []
    for dirname, names, node, status, reason in specs:
        sidecar = ROOT / "artifacts" / dirname
        files = [sidecar / name for name in names]
        assert all(path.is_file() for path in files)
        audit = {
            "kind": f"routeb_{node}_audit", "status": status,
            "evidence_level": "independent_sidecar_frontier_audit",
            "semantic_boundary": reason, "sidecar": str(sidecar.resolve()),
            "files": [ref(path) for path in files],
            "registry_promoted": False, "formal_certificate_allowed": False,
        }
        audits.append(audit)
        graph.setdefault("bottleneck_audits", []).append(audit)
        graph.setdefault("external_intakes", []).append({
            "kind": audit["kind"], "source": "local-routeb-gy-gaa-gab-frontier",
            "sidecar": audit["sidecar"], "files": audit["files"],
            "registry_promoted": False, "formal_certificate_allowed": False,
        })
        graph.setdefault("open_frontier_updates", []).append({
            "node": audit["kind"], "status": status.lower(), "reason": reason,
        })
    graph.update(schema="routeb-proposed-proof-dag-v180", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1, "algorithm": "routeb_gy_gaa_gab_frontier/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "independent-sidecars:GY,GAA,GAB",
        "evidence_sha256": sha(ROOT / "artifacts/task_GY_rhs_binding_contract_20260907/fields.json"),
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_gy_gaa_gab_frontier_recorded", proposed_dag=ref(new),
        proposed_dag_sha256=digest,
        audits=[{"kind": x["kind"], "status": x["status"]} for x in audits],
        registry_promoted=False, formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new.name, "audits": len(audits), "registry": len(state.registry)})


if __name__ == "__main__":
    main()
