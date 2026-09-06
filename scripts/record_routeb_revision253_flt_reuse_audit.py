"""Persist the Anthropic FLT non-number-theory reuse audit."""
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
    assert state.revision == 252 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v206.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v207.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision253.json"
    sidecar = ROOT / "artifacts/task_GBR_flt_reuse_registry_20260907"
    files = [sidecar / "REPORT.md", sidecar / "catalog.json", sidecar / "checker.py"]
    assert old.is_file() and not new.exists() and all(path.is_file() for path in files)
    catalog = json.loads((sidecar / "catalog.json").read_text(encoding="utf-8"))
    classes = {kind: sum(c.get("classification") == kind for c in catalog["candidates"])
               for kind in ("direct", "leicht", "architecture-only")}
    graph = json.loads(old.read_text(encoding="utf-8"))
    reason = (
        "The FLT snapshot contributes six non-number-theory candidates: three "
        "direct current-pin sidecar patterns and three light adaptations. "
        "The Mathlib pin differs from Route-B, so no source is implicitly admitted."
    )
    audit = {
        "kind": "anthropic_flt_non_number_theory_reuse_audit",
        "status": "PASS_CATALOG_FAIL_CLOSED_ADMISSION",
        "evidence_level": "provenance-and-current-pin-sidecar-catalog",
        "semantic_boundary": reason,
        "sidecar": str(sidecar.resolve()),
        "files": [ref(path) for path in files],
        "source_commit": catalog["source"]["commit"],
        "source_mathlib": catalog["source"]["mathlib_revision"],
        "routeb_mathlib": catalog["routeb_pin"]["mathlib_revision"],
        "classification_counts": classes,
        "pure_number_theory_excluded": True,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph.setdefault("bottleneck_audits", []).append(audit)
    graph.setdefault("external_intakes", []).append({
        "kind": audit["kind"], "source": "anthropic-fermats-last-theorem",
        "sidecar": audit["sidecar"], "files": audit["files"],
        "source_commit": audit["source_commit"],
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    graph.setdefault("open_frontier_updates", []).append({
        "node": audit["kind"], "status": "reuse_catalog_only", "reason": reason,
        "next_gate": "current-pin-recompile-and-explicit-routeb-binding",
    })
    graph.update(schema="routeb-proposed-proof-dag-v207", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision253_flt_reuse_audit/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "external-intake:anthropic-fermats-last-theorem",
        "evidence_sha256": sha(sidecar / "catalog.json"),
        "strict_compile": False, "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision253_flt_reuse_audit_recorded",
        proposed_dag=ref(new), proposed_dag_sha256=digest,
        audit={"kind": audit["kind"], "status": audit["status"]},
        classification_counts=classes, registry_promoted=False,
        formal_certificate_allowed=False, broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new.name,
           "classification_counts": classes, "registry": len(state.registry)})


if __name__ == "__main__":
    main()
