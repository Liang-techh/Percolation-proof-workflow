"""Persist FLT-to-Route-B mapping and the reconciled scalar Lean candidate."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from record_routeb_port_progress import ROOT, ref
from percolation_workflow.store import StateStore


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(paths: list[Path]) -> list[Path]:
    assert all(path.is_file() for path in paths), paths
    return paths


def main() -> None:
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    assert state.revision == 254 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v208.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v209.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision255.json"
    gbu = ROOT / "artifacts/task_GBU_lean_scalar_pinned_compile_20260907"
    gbw = ROOT / "artifacts/task_GBW_lean_compile_reconciliation_20260907"
    gbv = ROOT / "artifacts/task_GBV_flt_routeb_mapping_20260907"
    gbu_files = require([gbu / "IntervalNegative.lean", gbu / "IntervalNegative.olean",
                         gbu / "compile.log", gbu / "REPORT.md", gbu / "receipt.json"])
    gbw_files = require([gbw / "REPORT.md", gbw / "checker.py"])
    gbv_files = require([gbv / "REPORT.md", gbv / "mapping.json", gbv / "checker.py"])
    gbu_receipt = json.loads((gbu / "receipt.json").read_text(encoding="utf-8"))
    gbv_mapping = json.loads((gbv / "mapping.json").read_text(encoding="utf-8"))
    graph = json.loads(old.read_text(encoding="utf-8"))
    audits = [
        {
            "kind": "routeb_lean_scalar_interval_negative_candidate",
            "status": "PINNED_COMPILE_PASS_CANDIDATE_ONLY",
            "evidence_level": "pinned-lean-compile-standard-axioms",
            "semantic_boundary": (
                "The pure-real interval-negative lemma compiled at the Route-B "
                "pin with no sorry/admit/custom axiom; it is only an abstract "
                "candidate and has no DH, coverage, or comparator binding."
            ),
            "sidecar": str(gbu.resolve()),
            "files": [ref(path) for path in gbu_files + gbw_files],
            "compile": gbu_receipt["compile"],
            "axioms": gbu_receipt["audit"]["reported_axioms"],
            "registry_promoted": False,
            "formal_certificate_allowed": False,
        },
        {
            "kind": "anthropic_flt_routeb_direct_candidate_mapping",
            "status": "CANDIDATE_MAPPING_FAIL_CLOSED",
            "evidence_level": "static-provenance-mapping",
            "semantic_boundary": (
                "Three FLT direct candidates are mapped to open Route-B leaves "
                "only as conditional interfaces; the mapping does not prove "
                "physical semantics or verified reuse."
            ),
            "sidecar": str(gbv.resolve()),
            "files": [ref(path) for path in gbv_files],
            "mapping_count": len(gbv_mapping["mappings"]),
            "source_commit": "aa2d8b34692b16c70f699536de0d8e75b9a3e9ef",
            "registry_promoted": False,
            "formal_certificate_allowed": False,
        },
    ]
    graph.setdefault("bottleneck_audits", []).extend(audits)
    graph.setdefault("external_intakes", []).extend({
        "kind": audit["kind"],
        "source": "independent-sidecars:GBU-GBW-GBV",
        "sidecar": audit["sidecar"], "files": audit["files"],
        "registry_promoted": False, "formal_certificate_allowed": False,
    } for audit in audits)
    graph.setdefault("open_frontier_updates", []).extend({
        "node": audit["kind"], "status": "candidate_or_mapping_only",
        "reason": audit["semantic_boundary"],
    } for audit in audits)
    graph.update(schema="routeb-proposed-proof-dag-v209", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision255_flt_mapping_and_lean_candidate/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "independent-sidecars:GBU-GBW-GBV",
        "evidence_sha256": {
            "gbu_receipt": sha(gbu / "receipt.json"),
            "gbw_report": sha(gbw / "REPORT.md"),
            "gbv_mapping": sha(gbv / "mapping.json"),
        },
        "strict_compile": True,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision255_flt_mapping_and_lean_candidate_recorded",
        proposed_dag=ref(new), proposed_dag_sha256=digest,
        audits=[{"kind": audit["kind"], "status": audit["status"]} for audit in audits],
        registry_promoted=False, formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()
