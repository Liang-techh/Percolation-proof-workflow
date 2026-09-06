"""Persist strict FLT-derived analytic leaves as non-admitting advisory DAG evidence.

This recorder deliberately keeps these leaves outside the formal theorem registry:
they expose reusable algebra/calculus interfaces, but do not instantiate the
physical Route-B dynamics, interval source semantics, or certificate gates.
"""
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
    if state.revision != 280 or state.registry:
        raise ValueError("revision-281 recorder requires untouched revision 280 and empty registry")
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v234.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v235.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260908/state-before-revision281.json"
    pairing = ROOT / "artifacts/task_FLT_routeb_pairing_leaf_20260908"
    quotient = ROOT / "artifacts/task_FLT_routeb_quotient_leaf_20260908"
    central_fd = ROOT / "artifacts/task_FLT_central_fd_leaf_20260908"
    # The derivative leaf was intentionally built beside the user project, not
    # copied into this workflow repository. Keep its absolute provenance.
    derivative = Path(
        r"C:\Users\z5242\Desktop\重构版\6dof_sos_optimized\6dof_sos_optimized\artifacts\task_FLT_routeb_derivative_leaf_20260908"
    )
    required = [
        old,
        pairing / "RouteBPairingLeaf.lean", pairing / "receipt.json", pairing / "compile.log",
        quotient / "FLTRouteBQuotientLeaf.lean", quotient / "receipt.json", quotient / "REPORT.md",
        central_fd / "FLTCentralFiniteDifference.lean", central_fd / "REPORT.md",
        derivative / "FLT_RouteB_DerivativeLeaf.lean", derivative / "contract.json", derivative / "VERIFICATION.md",
    ]
    if not all(path.is_file() for path in required):
        raise ValueError("missing leaf evidence")

    leaves = [
        {
            "id": "flt_routeb_pairing_fin6",
            "kind": "analytic_adapter_leaf",
            "status": "CURRENT_PIN_STRICT_COMPILE_PASS_ABSTRACT_ONLY",
            "source": pairing,
            "files": [pairing / "RouteBPairingLeaf.lean", pairing / "receipt.json", pairing / "compile.log"],
            "parent_candidates": ["B45.source_semantics", "B45.local_energy"],
            "obstruction_rank": 3,
            "nonclaims": ["physical pairing positivity", "concrete DH binding", "norm/coverage/SOS/flowpipe"],
        },
        {
            "id": "flt_routeb_quotient_fin6",
            "kind": "analytic_adapter_leaf",
            "status": "CURRENT_PIN_STRICT_COMPILE_PASS_ABSTRACT_ONLY",
            "source": quotient,
            "files": [quotient / "FLTRouteBQuotientLeaf.lean", quotient / "receipt.json", quotient / "REPORT.md"],
            "parent_candidates": ["B45.domain_transport", "B45.source_semantics"],
            "obstruction_rank": 3,
            "nonclaims": ["physical constraint/domain theorem", "DH/dynamics/SOS/flowpipe"],
        },
        {
            "id": "flt_routeb_central_fd_average_derivative",
            "kind": "analytic_adapter_leaf",
            "status": "CURRENT_PIN_STRICT_COMPILE_PASS_ABSTRACT_ONLY",
            "source": central_fd,
            "files": [central_fd / "FLTCentralFiniteDifference.lean", central_fd / "REPORT.md"],
            "parent_candidates": ["B45.central_fd_bridge", "B45.source_semantics"],
            "obstruction_rank": 2,
            "nonclaims": ["interval rounding", "Float64 source binding", "physical DH derivative", "certificate gate"],
        },
        {
            "id": "flt_routeb_true_dh_derivative_hull",
            "kind": "analytic_adapter_leaf",
            "status": "CURRENT_PIN_STRICT_COMPILE_PASS_INTERFACE_ONLY",
            "source": derivative,
            "files": [derivative / "FLT_RouteB_DerivativeLeaf.lean", derivative / "contract.json", derivative / "VERIFICATION.md"],
            "parent_candidates": ["B45.true_dh_source", "B45.central_fd_bridge"],
            "obstruction_rank": 3,
            "nonclaims": ["concrete DH instantiation", "rounding/source binding", "ODE/flowpipe", "P3 parent closure"],
        },
    ]
    for leaf in leaves:
        leaf["source"] = str(leaf["source"].resolve())
        leaf["files"] = [ref(path) for path in leaf["files"]]
        leaf["registry_promoted"] = False
        leaf["formal_certificate_allowed"] = False

    graph = json.loads(old.read_text(encoding="utf-8"))
    overlay = {
        "kind": "flt_current_pin_math_leaf_overlay",
        "status": "RECORDED_NON_ADMISSION",
        "source_commit": "aa2d8b34692b16c70f699536de0d8e75b9a3e9ef",
        "routeb_mathlib_revision": "0df444a360eaa60ab8c11dca51a86af692955474",
        "lean_toolchain": "leanprover/lean4:v4.33.1",
        "leaves": leaves,
        "advisory_reuse_edges": [
            {"from": leaf["id"], "to": parent, "edge_type": "advisory_reuse", "reuse_obstruction_rank": leaf["obstruction_rank"]}
            for leaf in leaves for parent in leaf["parent_candidates"]
        ],
        "dependency_boundary": "advisory edges never enter ProofNode.dependencies or closure eligibility",
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph.setdefault("external_intakes", []).append(overlay)
    graph.setdefault("bottleneck_audits", []).append(overlay)
    graph.setdefault("advisory_reuse_overlays", []).append(overlay)
    graph.setdefault("open_frontier_updates", []).append({
        "node": "flt_current_pin_math_leaf_overlay",
        "status": "math_leaves_recorded_frontier_open",
        "reason": "Generic leaves close analytic sub-obligations only after concrete Route-B hypotheses and comparator checks are supplied.",
        "open_leaves": [leaf["id"] for leaf in leaves],
    })
    graph.update(schema="routeb-proposed-proof-dag-v235", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision281_flt_math_leaves/v1",
        "graph_sha256": digest,
        "roots": [],
        "selected_nodes": [],
        "source": "FLT current-pin strict analytic leaves",
        "evidence_sha256": sha(pairing / "receipt.json"),
        "leaf_count": len(leaves),
        "advisory_edge_count": len(overlay["advisory_reuse_edges"]),
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision281_flt_math_leaves_recorded",
        proposed_dag=ref(new),
        proposed_dag_sha256=digest,
        strict_compile_leaves=len(leaves),
        advisory_reuse_edges=len(overlay["advisory_reuse_edges"]),
        central_fd_identity=True,
        true_dh_concrete_binding=False,
        interval_source_soundness=False,
        registry_promoted=False,
        formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name, "leaves": len(leaves), "registry": len(state.registry)}))


if __name__ == "__main__":
    main()
