"""Record the FLT generic-module scan and provenance validator results."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from record_routeb_port_progress import ROOT, ref
from percolation_workflow.store import StateStore


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ev(*names: str) -> dict[str, Path]:
    result: dict[str, Path] = {}
    for name in names:
        path = ROOT / name
        assert path.is_file(), path
        result[name] = path
    return result


def main() -> None:
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    assert state.revision == 213 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v167.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v168.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision214.json"
    assert old.is_file() and not new.exists()

    audits = [
        (
            "anthropic_flt_calculus_scan",
            "SCAN_COMPLETE_NO_DIRECT_REUSE",
            "8 calculus/derivation candidates found: 6 light-adaptation and 2 architecture-only; no direct Route-B flowpipe theorem",
            ev(
                "artifacts/task_FL_flt_calculus_scan_20260907/REPORT.md",
                "artifacts/task_FL_flt_calculus_scan_20260907/candidates.json",
                "artifacts/task_FL_flt_calculus_scan_20260907/checker.py",
            ),
        ),
        (
            "anthropic_flt_topology_scan",
            "CE_REUSE_APPROVED_EXTRA_TRANSPORT_CANDIDATES",
            "7 topology/quotient candidates classified; CE quotient continuous-linear adapter is current-pin compiled, while additional lifts remain hypothesis-bound",
            ev(
                "artifacts/task_FM_flt_topology_scan_20260907/REPORT.md",
                "artifacts/task_FM_flt_topology_scan_20260907/candidates.json",
                "artifacts/task_FM_flt_topology_scan_20260907/checker.py",
            ),
        ),
        (
            "anthropic_flt_linear_transport_scan",
            "SCAN_COMPLETE_SIDEcar_DEDUPLICATED",
            "8 spectral/linear/transport candidates classified and deduplicated; registry/admission mutation excluded",
            ev(
                "artifacts/task_FN_flt_linear_transport_scan_20260907/REPORT.md",
                "artifacts/task_FN_flt_linear_transport_scan_20260907/candidates.json",
                "artifacts/task_FN_flt_linear_transport_scan_20260907/checker.py",
            ),
        ),
        (
            "anthropic_flt_registry_obstruction_architecture",
            "ARCHITECTURE_ONLY_NON_VERIFIED",
            "FLT theorem/solution split, declaration graph, sketch split and obstruction history map cleanly to ProofNode metadata but do not prove theorems",
            ev(
                "artifacts/task_FO_flt_registry_obstruction_architecture_20260907/REPORT.md",
                "artifacts/task_FO_flt_registry_obstruction_architecture_20260907/mapping.json",
                "artifacts/task_FO_flt_registry_obstruction_architecture_20260907/checker.py",
            ),
        ),
        (
            "anthropic_flt_external_catalog_validator",
            "TOOL_READY_PROVENANCE_HASHED_ROUTEB_FILTER",
            "classification 1/2/3, commit/path/license/attribution/current-pin and pure-number-theory exclusion are mechanically checked without registry mutation",
            ev(
                "src/percolation_workflow/external_catalog.py",
                "tests/test_external_catalog.py",
                "docs/external-catalog-README.md",
            ),
        ),
        (
            "anthropic_flt_snapshot_provenance",
            "PROVENANCE_PINNED_APACHE2_NON_VERIFIED",
            "snapshot commit, Lean/Mathlib pins, license, NOTICE and attribution are recorded; source reuse remains subject to current-pin recompilation",
            ev(
                "artifacts/anthropic_fermats_intake/catalog.json",
                "artifacts/anthropic_fermats_last_theorem/ATTRIBUTION.md",
                "artifacts/anthropic_fermats_last_theorem/NOTICE",
                "artifacts/anthropic_fermats_last_theorem/formalization.yaml",
            ),
        ),
    ]

    graph = json.loads(old.read_text(encoding="utf-8"))
    graph.setdefault("external_intakes", []).append(
        {
            "kind": "anthropic_fermats_generic_module_scan",
            "source": "https://github.com/anthropics/fermats-last-theorem",
            "commit": "aa2d8b34692b16c70f699536de0d8e75b9a3e9ef",
            "mathlib_revision": "db584cd6d46c92f209a44c0f1c829460d327499d",
            "license": "Apache-2.0",
            "catalog": {"path": ref(ROOT / "artifacts/anthropic_fermats_intake/catalog.json"), "sha256": sha(ROOT / "artifacts/anthropic_fermats_intake/catalog.json")},
            "registry_promoted": False,
            "formal_certificate_allowed": False,
        }
    )
    for kind, status, reason, evidence in audits:
        graph.setdefault("bottleneck_audits", []).append(
            {
                "kind": kind,
                "status": status,
                "evidence_level": "external_scan_or_provenance_validator",
                "semantic_boundary": reason,
                "source_commit": "aa2d8b34692b16c70f699536de0d8e75b9a3e9ef",
                "registry_promoted": False,
                "formal_certificate_allowed": False,
                "files": {
                    key: {"path": ref(path), "sha256": sha(path)}
                    for key, path in evidence.items()
                },
            }
        )
        graph.setdefault("open_frontier_updates", []).append(
            {"node": kind, "status": status.lower(), "reason": reason}
        )

    graph.update(schema="routeb-proposed-proof-dag-v168", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)

    digest = sha(new)
    for kind, _status, _reason, evidence in audits:
        first = next(iter(evidence.values()))
        state.graph_artifacts.append(
            {
                "schema_version": 1,
                "algorithm": kind + "/v1",
                "graph_sha256": digest,
                "roots": [],
                "selected_nodes": [],
                "source": str(first),
                "evidence_sha256": sha(first),
                "source_commit": "aa2d8b34692b16c70f699536de0d8e75b9a3e9ef",
                "registry_promoted": False,
                "formal_certificate_allowed": False,
            }
        )
    state.event(
        "anthropic_flt_scan_catalog_recorded",
        proposed_dag=ref(new),
        proposed_dag_sha256=digest,
        audits=[item[0] for item in audits],
        source_commit="aa2d8b34692b16c70f699536de0d8e75b9a3e9ef",
        registry_promoted=False,
        formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()
