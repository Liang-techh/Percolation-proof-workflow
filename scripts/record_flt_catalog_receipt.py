"""Persist the external FLT catalog receipt as non-admitting DAG evidence."""
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
    assert state.revision == 215 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v169.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v170.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision216.json"
    receipt = ROOT / "artifacts/anthropic_fermats_intake/catalog_receipt_20260907.json"
    validator = ROOT / "src/percolation_workflow/catalog_receipt.py"
    test = ROOT / "tests/test_catalog_receipt.py"
    assert old.is_file() and not new.exists() and receipt.is_file() and validator.is_file() and test.is_file()

    graph = json.loads(old.read_text(encoding="utf-8"))
    data = json.loads(receipt.read_text(encoding="utf-8"))
    assert data["registry_promoted"] is False and data["formal_certificate_allowed"] is False
    graph.setdefault("external_intakes", []).append(
        {
            "kind": "anthropic_fermats_catalog_receipt",
            "source": data["repository"],
            "commit": data["source_commit"],
            "catalog_sha256": data["catalog_sha256"],
            "receipt": {"path": ref(receipt), "sha256": sha(receipt)},
            "classification_histogram": data["classification_histogram"],
            "routeb_reuse_set": data["routeb_reuse_set"],
            "license": data["license"],
            "attribution_present": data["attribution_present"],
            "registry_promoted": False,
            "formal_certificate_allowed": False,
        }
    )
    audit = {
        "kind": "anthropic_flt_catalog_receipt",
        "status": "RECEIPT_PASS_PROVENANCE_ONLY",
        "evidence_level": "read_only_external_catalog_validation",
        "semantic_boundary": "catalog classification and provenance are validated; no candidate theorem, kernel proof or registry admission is asserted",
        "source_commit": data["source_commit"],
        "registry_promoted": False,
        "formal_certificate_allowed": False,
        "files": {
            "receipt": {"path": ref(receipt), "sha256": sha(receipt)},
            "validator": {"path": ref(validator), "sha256": sha(validator)},
            "test": {"path": ref(test), "sha256": sha(test)},
        },
    }
    graph.setdefault("bottleneck_audits", []).append(audit)
    graph.setdefault("open_frontier_updates", []).append(
        {"node": audit["kind"], "status": "receipt_pass_provenance_only", "reason": audit["semantic_boundary"]}
    )
    graph.update(schema="routeb-proposed-proof-dag-v170", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)

    digest = sha(new)
    state.graph_artifacts.append(
        {
            "schema_version": 1,
            "algorithm": "anthropic_flt_catalog_receipt/v1",
            "graph_sha256": digest,
            "roots": [],
            "selected_nodes": [],
            "source": str(receipt),
            "evidence_sha256": sha(receipt),
            "source_commit": data["source_commit"],
            "catalog_sha256": data["catalog_sha256"],
            "registry_promoted": False,
            "formal_certificate_allowed": False,
        }
    )
    state.event(
        "anthropic_flt_catalog_receipt_recorded",
        proposed_dag=ref(new),
        proposed_dag_sha256=digest,
        receipt=ref(receipt),
        receipt_sha256=sha(receipt),
        source_commit=data["source_commit"],
        registry_promoted=False,
        formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()
