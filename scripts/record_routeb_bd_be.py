"""Record BD exact-export and BE Schur-guard sidecars without promotion."""
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
    assert state.revision == 191 and not state.registry
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v145.json"
    new_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v146.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260906/state-before-revision192.json"
    assert old_graph.is_file() and not new_graph.exists()
    bd = ROOT / "artifacts/task_BD_exact_coefficient_gram_validator_20260906"
    be = ROOT / "artifacts/routeb_task_BE_schur_guard_20260906"
    bd_files = {n: bd / n for n in ("validate_exact_export.py", "REPORT.md", "README.md")}
    bd_test = ROOT / "tests/test_routeb_exact_export_validator.py"
    be_files = {n: be / n for n in ("verify_be_guard.py", "README.md", "REPLAY.json")}
    for path in (*bd_files.values(), bd_test, *be_files.values()):
        assert path.is_file(), path
    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    graph.setdefault("bottleneck_audits", []).append({
        "kind": "routeb_exact_coefficient_gram_validator",
        "status": "VALIDATOR_DESIGNED_FAIL_CLOSED",
        "evidence_level": "read_only_exact_witness_validator",
        "semantic_boundary": "validator rejects missing/decimal-only export; no SOS or registry promotion",
        "registry_promoted": False, "formal_certificate_allowed": False,
        "files": {**{k: {"path": ref(v), "sha256": sha(v)} for k, v in bd_files.items()}, "test": {"path": ref(bd_test), "sha256": sha(bd_test)}},
    })
    graph.setdefault("open_frontier_updates", []).append({
        "node": "RouteBP4.exact_coefficient_gram_export",
        "status": "validator_ready_payload_open",
        "reason": "exact reconstruction gate exists, but target export CSV/manifest/Gram witness is absent",
    })
    graph.setdefault("bottleneck_audits", []).append({
        "kind": "routeb_schur_inverse_guard_one_cell",
        "status": "PASS_CONDITIONAL_EXACT_ONE_CELL",
        "evidence_level": "exact_rational_replay",
        "semantic_boundary": "rho<1 only on |q_i|<=1/1000; coverage, source bridge and trajectory remain open",
        "registry_promoted": False, "formal_certificate_allowed": False,
        "files": {k: {"path": ref(v), "sha256": sha(v)} for k, v in be_files.items()},
    })
    graph["open_frontier_updates"].append({
        "node": "RouteBSchur.full_domain_cell_cover",
        "status": "one_cell_guard_parent_open",
        "reason": "Neumann inverse guard is replayed exactly for one cell only; no global cover is admitted",
    })
    graph.update(schema="routeb-proposed-proof-dag-v146", supersedes=old_graph.name)
    new_graph.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new_graph)
    for algorithm, source, extra in (
        ("routeb_exact_coefficient_gram_validator/v1", bd_files["validate_exact_export.py"], {"report_sha256": sha(bd_files["REPORT.md"])}),
        ("routeb_schur_inverse_guard_one_cell/v1", be_files["REPLAY.json"], {"replay_sha256": sha(be_files["REPLAY.json"])}),
    ):
        state.graph_artifacts.append({
            "schema_version": 1, "algorithm": algorithm, "graph_sha256": digest,
            "roots": [], "selected_nodes": [], "source": str(source), **extra,
            "registry_promoted": False, "formal_certificate_allowed": False,
        })
    state.event(
        "routeb_bd_be_recorded", proposed_dag=ref(new_graph), proposed_dag_sha256=digest,
        exact_gram_validator=ref(bd_files["validate_exact_export.py"]),
        exact_gram_report_sha256=sha(bd_files["REPORT.md"]),
        schur_guard_replay=ref(be_files["REPLAY.json"]), schur_guard_replay_sha256=sha(be_files["REPLAY.json"]),
        registry_promoted=False, formal_certificate_allowed=False, broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new_graph.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()
