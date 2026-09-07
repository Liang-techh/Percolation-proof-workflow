"""Record the narrowed true-DH source formula audit.

The external Route-B artifacts already expose the residual map

    R_port(q) = -M_BD(q) M_DD(mu,q)^(-1) (M_DB(q) - M0_DB),

and the nominal-distal bridge identifies ``r_B = M_BD v``.  This recorder
checks that the relevant source/interface texts are present and records the
remaining, sharper obligation: an evaluator/enclosure theorem connecting
the Float64 deployment to the exact-real/interval model.  It never promotes
the theorem node or the verified registry.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ROUTE_B = ROOT.parent / "6dof_sos_optimized" / "6dof_sos_optimized"
SRC = ROUTE_B / "routeB_dense_Mq"
sys.path.insert(0, str(ROOT / "src"))

from percolation_workflow.store import StateStore  # noqa: E402


def ref(path: Path) -> dict[str, str]:
    return {
        "path": str(path.resolve()),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest().upper(),
    }


def find(state, name: str):
    for node in state.nodes.values():
        if node.name == name:
            return node
    raise ValueError(f"missing node: {name}")


def main() -> int:
    paths = {
        "deployed_dh": SRC / "dhport_lib.jl",
        "interval_probe": SRC / "routeB_compact_port_bi_partition_probe.jl",
        "analytic_model": SRC / "routeB_fourier_lifted_descriptor_model.jl",
        "nominal_interface": SRC / "P5_COMPACT_NOMINAL_DESCRIPTOR_INTERFACE.md",
        "source_semantics_audit": SRC / "P5_COMPACT_DH_FOURIER_SOURCE_SEMANTICS_AUDIT.md",
        "exact_real_boundary": SRC / "P5_COMPACT_EXACT_REAL_MODEL_BOUNDARY.md",
        "mass_export": SRC / "routeB_analytic_mass_full_cs_polynomial.csv",
    }
    for path in paths.values():
        if not path.is_file():
            raise FileNotFoundError(path)

    text = {key: path.read_text(encoding="utf-8", errors="replace")
            for key, path in paths.items()}
    checks = {
        "deployed_mass_and_fd_are_parameterized": (
            "function mass_matrix" in text["deployed_dh"]
            and "const MASS_REGULARIZER = 1e-6" in text["deployed_dh"]
            and "const CG_FINITE_DIFF_STEP = 1e-5" in text["deployed_dh"]
            and "fd_step::Real = CG_FINITE_DIFF_STEP" in text["deployed_dh"]
        ),
        "interval_probe_declares_blocks": (
            "const DIDX = [1, 2, 3, 6]" in text["interval_probe"]
            and "const BIDX = [4, 5]" in text["interval_probe"]
        ),
        "interval_probe_forms_source_R": (
            "R_gain = [sum(M[BIDX[i], DIDX[k]] * Z[k, j]" in text["interval_probe"]
            and "R = [-R_gain[i, j]" in text["interval_probe"]
            and "Delta[i, j]" in text["interval_probe"]
        ),
        "interval_probe_preserves_remote_term": (
            "r_B = R_port*a_B" in text["interval_probe"]
            and "M_BD" in text["interval_probe"]
        ),
        "analytic_model_uses_same_regularizer": (
            "load_matrix_cs" in text["analytic_model"]
            and "M[i, i] += Q(1, 1_000_000)" in text["analytic_model"]
            and "MDD = M0[D, D]" in text["analytic_model"]
        ),
        "analytic_model_controller_block_is_present": (
            "Kd = Q[4, 5, 3, 1, 2, 3] ./ 5" in text["analytic_model"]
            and "Bfr = Q[1, Q(2, 5), Q(7, 20), Q(3, 10), Q(1, 4), Q(1, 5)]" in text["analytic_model"]
        ),
        "nominal_bridge_equations_present": (
            "M_DD(q)*v + DeltaM_DB(q)*a_B = 0" in text["nominal_interface"]
            and "r_B - M_BD(q)*v = 0" in text["nominal_interface"]
        ),
        "source_semantics_consistency_recorded": (
            "source_semantics_consistent=True" in text["source_semantics_audit"]
        ),
        "float64_enclosure_obligation_explicit": (
            "Float64 evaluation of dhport_lib.jl is contained" in text["exact_real_boundary"]
            and "formal_certificate_allowed=false" in text["exact_real_boundary"]
        ),
    }
    if not all(checks.values()):
        missing = [key for key, ok in checks.items() if not ok]
        raise ValueError(f"source formula audit failed: {missing}")

    audit = {
        "schema_version": 1,
        "status": "SOURCE_FORMULA_PRESENT_CONTROLLER_MISMATCH_AND_FLOAT64_ENCLOSURE_OPEN",
        "formula": "R_port(q)=-M_BD(q)*M_DD(mu,q)^(-1)*(M_DB(q)-M0_DB)",
        "block_order": {"B": [4, 5], "D": [1, 2, 3, 6]},
        "findings": [
            "the interval probe solves M_DD(mu,q)^(-1)*DeltaM_DB(q) and applies the descriptor minus sign",
            "the residual output is R_port=-M_BD(q)*Z; positive R_gain is norm-equivalent only",
            "the nominal bridge retains r_B-M_BD(q)*v=0 and M_DD*v+DeltaM_DB*a_B=0",
            "the analytic c/s model includes the same explicit mu=1/1000000 diagonal regularizer",
            "the source semantics audit records matching DH parameters and h=1/100000 finite differences",
        ],
        "checks": checks,
        "known_semantic_mismatches": [
            {
                "field": "controller_damping_sum",
                "deployed_dhport": ["1.3", "1.1", "0.95", "0.8", "0.65", "0.5"],
                "lifted_descriptor": ["1.8", "1.4", "0.95", "0.5", "0.65", "0.8"],
                "effect": "full lifted descriptor is not yet the deployed controller source",
                "repair": "select one authoritative parameter vector and regenerate/rebind the full descriptor",
            },
        ],
        "remaining_obligations": [
            "resolve the controller damping-vector mismatch before full descriptor source binding",
            "prove the common exact-real domain identity between deployed source and analytic/interval evaluator",
            "prove a roundoff-aware Float64 enclosure for M,C_fd,G_fd,tau and the solved RHS, or make exact-real evaluation authoritative",
            "compile a typed Lean adapter for R*a_B=r_B with the same mu, force coordinates, and remote term",
            "connect the source equality to coefficient-level residual absorption",
        ],
        "non_implications": [
            "source formula presence is not a global interval bound",
            "pointwise or BigFloat regression is not a Float64 enclosure theorem",
            "the port budget and nominal bridge do not promote the registry",
        ],
        "formal_certificate_allowed": False,
        "registry_eligible": False,
    }

    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    parent = find(state, "P4.true_dh_port_source_binding")
    leaf = find(state, "P4.true_dh_residual_map_coefficient_binding")
    artifacts = [ref(path) for path in paths.values()]
    changed = False
    if leaf.metadata.get("source_formula_audit") != audit:
        leaf.metadata["source_formula_audit"] = audit
        changed = True
    if leaf.metadata.get("source_binding_artifacts") != artifacts:
        leaf.metadata["source_binding_artifacts"] = artifacts
        changed = True
    if leaf.metadata.get("math_bottleneck") != "evaluator_enclosure":
        leaf.metadata["math_bottleneck"] = "evaluator_enclosure"
        changed = True
    unresolved = list(leaf.metadata.get("unresolved", []))
    for item in (
        "exact_real_deployed_evaluator_enclosure",
        "float64_roundoff_inclusion_for_R_source",
        "typed_R_aB_equals_rB_adapter",
    ):
        if item not in unresolved:
            unresolved.append(item)
    if unresolved != leaf.metadata.get("unresolved"):
        leaf.metadata["unresolved"] = unresolved
        changed = True

    parent_audit = {
        "status": audit["status"],
        "formula": audit["formula"],
        "leaf": leaf.name,
        "source_semantics_checks": checks,
        "formal_certificate_allowed": False,
    }
    if parent.metadata.get("source_formula_audit") != parent_audit:
        parent.metadata["source_formula_audit"] = parent_audit
        changed = True

    if changed:
        state.event(
            "routeb_true_dh_source_formula_audit_recorded",
            node_id=leaf.id,
            parent_id=parent.id,
            status=audit["status"],
            remaining_obligations=audit["remaining_obligations"],
            registry_promoted=False,
            formal_certificate_allowed=False,
        )
        state.validate()
        store.save(state)
        print({"status": "recorded", "node_id": leaf.id,
               "state_revision": state.revision, "audit_status": audit["status"]})
    else:
        print({"status": "already_recorded", "node_id": leaf.id,
               "state_revision": state.revision, "audit_status": audit["status"]})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
