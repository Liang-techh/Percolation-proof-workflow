"""Record the P3 source-binding interface and concrete obligation ledger."""
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
    if state.revision != 284 or state.registry:
        raise ValueError("revision-285 recorder requires revision 284 and empty registry")
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v238.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v239.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260908/state-before-revision285.json"
    p3 = Path(r"C:\Users\z5242\Desktop\重构版\6dof_sos_optimized\6dof_sos_optimized\artifacts\task_FLT_p3_source_binding_20260908")
    audit = ROOT / "artifacts/task_FLT_source_binding_audit_20260908"
    required = [
        old, p3 / "FLT_P3_SourceBinding.lean", p3 / "AUDIT.md", p3 / "OBLIGATIONS.csv", p3 / "contract.json", p3 / "VERIFICATION.md",
        audit / "REPORT.md", audit / "OBLIGATIONS.csv", audit / "contract.json",
    ]
    if not all(path.is_file() for path in required):
        raise ValueError("missing P3 source-binding evidence")
    p3_contract = json.loads((p3 / "contract.json").read_text(encoding="utf-8"))
    audit_contract = json.loads((audit / "contract.json").read_text(encoding="utf-8"))
    if p3_contract.get("formal_certificate_allowed") is not False or p3_contract.get("physical_certificate_allowed") is not False:
        raise ValueError("P3 contract is not fail-closed")

    p3_record = {
        "kind": "routeb_p3_exact_real_source_binding_leaf",
        "status": "LEAN_VERIFIED_ABSTRACT_SOURCE_BINDING_INTERFACE",
        "evidence_level": "current-pin-strict-compile-abstract-interface",
        "files": [ref(p3 / name) for name in ("FLT_P3_SourceBinding.lean", "AUDIT.md", "OBLIGATIONS.csv", "contract.json", "VERIFICATION.md")],
        "proved": [
            "derivative-hull to central-FD secant bridge",
            "payload + rounding + derivative error composition",
            "each error source counted exactly once",
        ],
        "open_obligations": [
            "six-joint concrete DH derivative hull",
            "Julia operation-DAG exact-real equivalence",
            "sin/cos and Float64 absolute outward rounding",
            "shifted-domain and partition coverage",
        ],
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    audit_record = {
        "kind": "routeb_p3_concrete_source_binding_obligation_ledger",
        "status": audit_contract.get("status", "FAIL_CLOSED_OPEN"),
        "evidence_level": "canonical-source-audit-no-physical-admission",
        "files": [ref(audit / name) for name in ("REPORT.md", "OBLIGATIONS.csv", "contract.json")],
        "canonical_source_sha256": audit_contract.get("canonical_source_sha256"),
        "obligation_ids": [f"FLT-RB-SB-O{i}" for i in range(1, 11)],
        "bottlenecks": ["exact-real sin/cos bridge", "h_src endpoint semantics", "midpoint/radius/kappa outward rounding", "source/operation-DAG binding"],
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph = json.loads(old.read_text(encoding="utf-8"))
    for record in (p3_record, audit_record):
        graph.setdefault("bottleneck_audits", []).append(record)
        graph.setdefault("external_intakes", []).append(record)
    graph.setdefault("open_frontier_updates", []).extend([
        {"node": "B45.p3_source_binding", "status": "abstract_interface_closed_concrete_frontier_open", "reason": p3_record["open_obligations"]},
        {"node": "B45.concrete_operation_dag", "status": "O1_O10_open", "reason": audit_record["bottlenecks"]},
    ])
    graph.update(schema="routeb-proposed-proof-dag-v239", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision285_p3_source_binding/v1",
        "graph_sha256": digest,
        "roots": [],
        "selected_nodes": [],
        "source": "abstract P3 leaf + canonical concrete obligation ledger",
        "evidence_sha256": sha(p3 / "contract.json"),
        "obligation_count": 10,
        "physical_binding_open": True,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision285_p3_source_binding_recorded",
        proposed_dag=ref(new),
        proposed_dag_sha256=digest,
        abstract_source_binding_leaf=True,
        concrete_obligation_count=10,
        exact_real_dh_binding=False,
        float64_outward_rounding=False,
        coverage_closed=False,
        registry_promoted=False,
        formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name, "registry": len(state.registry)}))


if __name__ == "__main__":
    main()
