"""Persist the sign audit, frontier experiments, Lean refresh, and host bridge."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from record_routeb_port_progress import ROOT, ref
from percolation_workflow.store import StateStore


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    assert state.revision == 275 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v229.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v230.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision276.json"
    names = {
        "grid": ROOT / "artifacts/task_GCV_meanvalue_q2q3_grid_20260907",
        "coverage": ROOT / "artifacts/task_GCX_meanvalue_coverage_frontier_20260907",
        "soundness": ROOT / "artifacts/task_GCW_meanvalue_soundness_20260907",
        "lean": ROOT / "artifacts/task_GDA_lean_fullstate_schur_refresh_20260907",
        "bridge": ROOT / "artifacts/task_GDB_repair_registry_gap_20260907",
        "dag": ROOT / "artifacts/task_GDC_theorem_dag_decomposition_20260907",
    }
    required = [old, names["grid"] / "receipt.json", names["coverage"] / "receipt.json",
                names["soundness"] / "receipt.json", names["soundness"] / "report.md",
                names["lean"] / "receipt.json", names["lean"] / "FullStateSchurRefresh.lean",
                names["lean"] / "compile_strict.log", names["lean"] / "checker.py",
                names["bridge"] / "receipt.json", names["bridge"] / "report.md",
                names["dag"] / "receipt.json", names["dag"] / "report.md"]
    assert all(path.is_file() for path in required) and not new.exists()
    grid, coverage, soundness, lean, bridge, dag = [
        load(names[key] / "receipt.json") for key in ("grid", "coverage", "soundness", "lean", "bridge", "dag")
    ]
    graph = load(old)

    sign = {
        "kind": "routeb_h_sign_normalization_required",
        "status": "SOURCE_SUCCESS_DIRECTION_IS_NONNEGATIVE",
        "source_definition": "h_src = bound - ||l_B||^2; h_lo = bound_lo - l2_hi",
        "success_direction": "h_lo > 0 implies h_src > 0 and ||l_B||^2 < bound",
        "negative_target_rewrite": "h_neg = ||l_B||^2 - bound = -h_src; prove h_neg < 0",
        "literal_source_h_B_lt_zero_is_success": False,
        "evidence": [ref(names["soundness"] / "report.md"), ref(names["dag"] / "report.md")],
        "registry_promoted": False, "formal_certificate_allowed": False,
        "semantic_boundary": "Historical negative-h labels remain retained as candidate/obstruction evidence; comparator must use the explicit sign map.",
    }
    graph.setdefault("bottleneck_audits", []).append(sign)
    graph.setdefault("external_intakes", []).append({
        "kind": sign["kind"], "source": "audit:GCW-GDC-sign-normalization",
        "sidecar": str(names["soundness"].resolve()), "files": sign["evidence"],
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    graph.setdefault("open_frontier_updates", []).append({
        "node": sign["kind"], "status": "sign_map_required_before_admission",
        "reason": sign["semantic_boundary"],
    })

    entries = [
        {"kind": "routeb_meanvalue_fd_q2q3_grid_no_strict_negative", "receipt": grid,
         "side": names["grid"], "files": [names["grid"] / "receipt.json"],
         "reason": "16 q2/q3 combinations remain BOX_BRACKET_LOWER_NONNEGATIVE; no strict negative source h interval."},
        {"kind": "routeb_meanvalue_coverage_frontier_no_propagatable_region", "receipt": coverage,
         "side": names["coverage"], "files": [names["coverage"] / "receipt.json", names["coverage"] / "probe.jl"],
         "reason": "12 core/adjacent targeted cells have positive source h lower bounds; no propagation witness."},
        {"kind": "routeb_meanvalue_block45_soundness_open", "receipt": soundness,
         "side": names["soundness"], "files": [names["soundness"] / "report.md", names["soundness"] / "receipt.json"],
         "reason": "Exact-real central-FD math is conditional; outward interval and Float64/analytic-DH bridges remain open."},
        {"kind": "independent_formal_adapter_fullstate_schur_refresh", "receipt": lean,
         "side": names["lean"], "files": [names["lean"] / "receipt.json", names["lean"] / "FullStateSchurRefresh.lean", names["lean"] / "compile_strict.log", names["lean"] / "checker.py"],
         "reason": "Six current-pin declarations compile with zero nonstandard axioms; admission is independent lane only."},
        {"kind": "host_cycle_compiled_candidate_registry_cascade_gap", "receipt": bridge,
         "side": names["bridge"], "files": [names["bridge"] / "report.md", names["bridge"] / "receipt.json"],
         "reason": "Coordinator post-compile verify/register/cascade edge was absent; minimal fail-closed bridge added in host_cycle."},
        {"kind": "routeb_theorem_dag_38_node_sign_and_frontier_audit", "receipt": dag,
         "side": names["dag"], "files": [names["dag"] / "report.md", names["dag"] / "receipt.json"],
         "reason": "38-node decomposition identifies sign normalization, source soundness, physical Schur, coverage, flowpipe and terminal transfer leaves."},
    ]
    for entry in entries:
        graph.setdefault("bottleneck_audits", []).append({
            "kind": entry["kind"], "status": entry["receipt"].get("status"),
            "evidence_level": "targeted-sidecar-audit", "sidecar": str(entry["side"].resolve()),
            "files": [ref(path) for path in entry["files"]],
            "receipt_sha256": sha(entry["side"] / "receipt.json"),
            "registry_promoted": False, "formal_certificate_allowed": False,
            "semantic_boundary": entry["reason"],
        })
        graph.setdefault("external_intakes", []).append({
            "kind": entry["kind"], "source": "targeted-sidecar", "sidecar": str(entry["side"].resolve()),
            "files": [ref(path) for path in entry["files"]],
            "registry_promoted": False, "formal_certificate_allowed": False,
        })
        graph.setdefault("open_frontier_updates", []).append({
            "node": entry["kind"], "status": "retained_fail_closed", "reason": entry["reason"]
        })
    graph.update(schema="routeb-proposed-proof-dag-v230", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1, "algorithm": "routeb_revision276_sign_frontier_host_bridge/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "sidecars:GCV-GCX-GCW-GDA-GDB-GDC",
        "evidence_sha256": sha(names["dag"] / "receipt.json"),
        "workflow_patch": "host_cycle coordinator promotion bridge",
        "strict_compile": True, "registry_promoted": False, "formal_certificate_allowed": False,
    })
    state.event("routeb_revision276_sign_frontier_host_bridge_recorded",
                proposed_dag=ref(new), proposed_dag_sha256=digest,
                sign_normalization_required=True, meanvalue_grid_closed=False,
                coverage_closed=False, independent_adapter_only=True,
                host_candidate_cascade_bridge=True, registry_promoted=False,
                formal_certificate_allowed=False, broad_regression_run=False)
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name, "registry": len(state.registry)}))


if __name__ == "__main__":
    main()
