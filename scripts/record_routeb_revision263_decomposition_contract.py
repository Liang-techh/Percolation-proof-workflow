"""Persist decomposition comparator transport contract hardening."""
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
    assert state.revision == 262 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v216.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v217.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision263.json"
    source_files = [ROOT / "src/percolation_workflow/agent_bridge.py",
                    ROOT / "src/percolation_workflow/host_cycle.py"]
    assert old.is_file() and not new.exists() and all(path.is_file() for path in source_files)
    graph = json.loads(old.read_text(encoding="utf-8"))
    audit = {
        "kind": "decomposition_comparator_contract_advertised",
        "status": "IMPLEMENTED_FAIL_CLOSED",
        "evidence_level": "focused-agent-bridge-and-host-cycle-tests",
        "changed_files": [ref(path) for path in source_files],
        "request_contract": {
            "required_fields": ["sketch", "children", "comparator_gate"],
            "comparator_gate_fields_per_child": [
                "source_identity", "source_statement", "covered_source",
                "target_theorem_identity"],
            "admission": "fail_closed_before_child_creation",
        },
        "focused_tests": {"command": "tests/test_host_cycle.py tests/test_agent_bridge.py",
                           "passed": 23},
        "bypass": False,
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    graph.setdefault("workflow_hardening", []).append(audit)
    graph.setdefault("open_frontier_updates", []).append({
        "node": audit["kind"], "status": "contract_advertised_and_enforced",
        "reason": "host callback must provide explicit comparator bindings before child creation",
    })
    graph.update(schema="routeb-proposed-proof-dag-v217", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1, "algorithm": "routeb_revision263_decomposition_contract/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "local-agent-bridge-and-host-cycle-hardening",
        "evidence_sha256": sha(source_files[0]), "strict_compile": False,
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    state.event("routeb_revision263_decomposition_contract_recorded",
                proposed_dag=ref(new), proposed_dag_sha256=digest,
                comparator_context_required=True, comparator_contract_advertised=True,
                focused_tests_passed=23, registry_promoted=False,
                formal_certificate_allowed=False, broad_regression_run=False)
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name,
                      "registry": len(state.registry), "formal_certificate_allowed": False}))


if __name__ == "__main__":
    main()
