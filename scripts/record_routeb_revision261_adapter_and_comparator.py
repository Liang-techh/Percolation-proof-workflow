"""Persist independent adapter admission audit and comparator transport hardening."""
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
    assert state.revision == 260 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v214.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v215.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision261.json"
    sidecar = ROOT / "artifacts/task_GCJ_adapter_registry_audit_20260907"
    files = [sidecar / "REPORT.md", sidecar / "audit.json", sidecar / "checker.py"]
    assert old.is_file() and not new.exists() and all(path.is_file() for path in files)
    audit_receipt = json.loads((sidecar / "audit.json").read_text(encoding="utf-8"))
    graph = json.loads(old.read_text(encoding="utf-8"))
    adapters = audit_receipt.get("admissible_now", [])
    candidate_only = audit_receipt.get("candidate_only", [])
    adapter_audit = {
        "kind": "independent_adapter_registry_admission_audit",
        "status": audit_receipt.get("result"),
        "evidence_level": "source-and-olean-bound-abstract-adapters",
        "sidecar": str(sidecar.resolve()),
        "files": [ref(path) for path in files],
        "independent_adapter_admissible": adapters,
        "candidate_only": candidate_only,
        "routeb_physical_registry_mutated": False,
        "formal_certificate_allowed": False,
        "registry_promoted": False,
        "semantic_boundary": "Only the independent abstract adapter lane may consume these candidates; no Route-B physical theorem or comparator claim is discharged.",
    }
    comparator_audit = {
        "kind": "decomposition_comparator_context_transport",
        "status": "IMPLEMENTED_FAIL_CLOSED",
        "evidence_level": "focused-host-cycle-test",
        "changed_files": [
            ref(ROOT / "src/percolation_workflow/host_cycle.py"),
            ref(ROOT / "tests/test_host_cycle.py"),
        ],
        "contract": "host callbacks must carry explicit decomposition.comparator_gate context; host_cycle forwards it to propose_decomposition",
        "verification": "19 focused tests passed",
        "bypass": False,
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    graph.setdefault("bottleneck_audits", []).extend([adapter_audit, comparator_audit])
    graph.setdefault("external_intakes", []).append({
        "kind": adapter_audit["kind"],
        "source": "independent-sidecar:GCJ-adapter-registry-audit",
        "sidecar": adapter_audit["sidecar"], "files": adapter_audit["files"],
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    graph.setdefault("workflow_hardening", []).append(comparator_audit)
    graph.setdefault("open_frontier_updates", []).extend([
        {"node": adapter_audit["kind"], "status": "independent_lane_only",
         "reason": adapter_audit["semantic_boundary"]},
        {"node": comparator_audit["kind"], "status": "transport_closed_context_required",
         "reason": comparator_audit["contract"]},
    ])
    graph.update(schema="routeb-proposed-proof-dag-v215", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1, "algorithm": "routeb_revision261_adapter_and_comparator/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "independent-sidecar:GCJ-plus-local-comparator-transport",
        "evidence_sha256": sha(sidecar / "audit.json"), "strict_compile": False,
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    state.event("routeb_revision261_adapter_and_comparator_recorded",
                proposed_dag=ref(new), proposed_dag_sha256=digest,
                independent_adapter_count=len(adapters), candidate_only_count=len(candidate_only),
                routeb_physical_registry_mutated=False, comparator_context_required=True,
                focused_tests_passed=19, registry_promoted=False,
                formal_certificate_allowed=False, broad_regression_run=False)
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name,
                      "independent_adapter_admissible": len(adapters),
                      "candidate_only": len(candidate_only), "registry": len(state.registry)}))


if __name__ == "__main__":
    main()
