"""Persist current-pin FLT adapter intake as non-admitting DAG evidence."""
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
    assert state.revision == 279 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v233.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v234.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260908/state-before-revision280.json"
    manifest = ROOT / "artifacts/anthropic_fermats_intake/current_pin_adapter_manifest_20260908.json"
    plan = ROOT / "artifacts/anthropic_fermats_intake/CURRENT_PIN_REUSE_PLAN_20260908.md"
    receipt = ROOT / "artifacts/anthropic_fermats_intake/catalog_receipt_20260907.json"
    assert all(path.is_file() for path in (old, manifest, plan, receipt)) and not new.exists()
    data = json.loads(manifest.read_text(encoding="utf-8"))
    assert data["source_commit"] == "aa2d8b34692b16c70f699536de0d8e75b9a3e9ef"
    assert data["routeb_mathlib_revision"] == "0df444a360eaa60ab8c11dca51a86af692955474"
    assert data["formal_certificate_allowed"] is False and data["registry_promoted"] is False
    for entry in data["entries"]:
        assert entry["registry_promoted"] is False and entry["formal_certificate_allowed"] is False
        for value in entry["evidence_files"]:
            assert (ROOT / entry["evidence_root"] / value).is_file(), (entry["id"], value)
    graph = json.loads(old.read_text(encoding="utf-8"))
    audit = {
        "kind": "anthropic_flt_current_pin_adapter_manifest",
        "status": "CURRENT_PIN_ADAPTER_INTAKE_PASS_NON_ADMISSION",
        "evidence_level": "current-pin-isolated-sidecar-and-provenance-manifest",
        "source": data["repository"], "source_commit": data["source_commit"],
        "source_mathlib_revision": data["source_mathlib_revision"],
        "routeb_mathlib_revision": data["routeb_mathlib_revision"],
        "routeb_lean_toolchain": data["routeb_lean_toolchain"],
        "manifest": {"path": ref(manifest), "sha256": sha(manifest)},
        "reuse_plan": {"path": ref(plan), "sha256": sha(plan)},
        "entries": [{"id": entry["id"], "classification": entry["classification"],
                     "reuse_mode": entry["reuse_mode"], "evidence_root": entry["evidence_root"],
                     "receipt_sha256": entry["receipt_sha256"],
                     "registry_promoted": False, "formal_certificate_allowed": False}
                    for entry in data["entries"]],
        "registry_promoted": False, "formal_certificate_allowed": False,
        "semantic_boundary": data["admission_policy"],
    }
    graph.setdefault("external_intakes", []).append(audit)
    graph.setdefault("bottleneck_audits", []).append(audit)
    graph.setdefault("open_frontier_updates", []).append({
        "node": audit["kind"], "status": "adapter_intake_recorded_not_physical_proof",
        "reason": audit["semantic_boundary"],
    })
    graph.update(schema="routeb-proposed-proof-dag-v234", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1, "algorithm": "routeb_revision280_flt_current_pin_adapters/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": str(manifest), "evidence_sha256": sha(manifest),
        "source_commit": data["source_commit"], "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event("routeb_revision280_flt_current_pin_adapters_recorded",
                proposed_dag=ref(new), proposed_dag_sha256=digest,
                direct_pairing_adapter=True, light_quotient_adapter=True,
                conditional_spectral_adapter=True, direct_calculus_core=True,
                routeb_physical_binding=False, registry_promoted=False,
                formal_certificate_allowed=False, broad_regression_run=False)
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name,
                      "entries": len(data["entries"]), "registry": len(state.registry)}))


if __name__ == "__main__":
    main()
