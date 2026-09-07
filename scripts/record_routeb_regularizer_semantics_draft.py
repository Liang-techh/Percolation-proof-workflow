"""Record the exact Float64-vs-rational regularizer seam for Route-B O0."""
from __future__ import annotations

import hashlib
from fractions import Fraction
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ROUTE_B = ROOT.parent / "6dof_sos_optimized" / "6dof_sos_optimized"
DEPLOYED = ROUTE_B / "robot_final" / "dhport_lib.jl"
ANALYTIC = ROUTE_B / "routeB_dense_Mq" / "routeB_fourier_lifted_descriptor_model.jl"
sys.path.insert(0, str(ROOT / "src"))

from percolation_workflow.store import StateStore  # noqa: E402
from percolation_workflow.routeb_regularizer_semantics import (  # noqa: E402
    FLOAT64_MU_BITS_HEX,
    routeb_regularizer_fact,
)


def ref(path: Path) -> dict[str, str]:
    return {"path": str(path.resolve()),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest().upper()}


def find(state, name: str):
    for node in state.nodes.values():
        if node.name == name:
            return node
    raise ValueError(f"missing node: {name}")


def frac_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def main() -> int:
    for path in (DEPLOYED, ANALYTIC):
        if not path.is_file():
            raise FileNotFoundError(path)
    fact = routeb_regularizer_fact()
    float_mu = fact.mu_float64
    exact_mu = fact.mu_exact_real
    difference = float_mu - exact_mu
    payload = {
        "schema_version": 1,
        "status": "OPEN_ROUNDING_INCLUSION_REQUIRED",
        "deployed_literal": "1e-6",
        "bridge_schema": fact.schema,
        "float64_bits_hex": FLOAT64_MU_BITS_HEX,
        "deployed_float64_exact_value": frac_text(float_mu),
        "analytic_exact_real_value": frac_text(exact_mu),
        "deployed_minus_analytic": frac_text(difference),
        "difference_sign": "negative",
        "outward_interval": [frac_text(item) for item in fact.outward_interval],
        "diagonal_propagation": {
            "matrix_identity": "M_float = M_exact - delta*I under common unregularized-base binding",
            "block_B": [4, 5],
            "block_D": [1, 2, 3, 6],
            "off_diagonal_shift": "0",
            "inverse_and_port": "requires explicit exact-real resolvent premise",
        },
        "source_artifacts": [ref(DEPLOYED), ref(ANALYTIC)],
        "known_fact": "the Float64 literal and exact rational are distinct real numbers",
        "decomposition": [
            {
                "id": "O0.1",
                "name": "literal_representation",
                "status": "FACT_RECORDED",
                "interface": "RouteB.O0.Float64RegularizerLiteral",
            },
            {
                "id": "O0.2",
                "name": "common_base_binding",
                "status": "OPEN",
                "interface": "RouteB.O0.CommonUnregularizedMassBase",
            },
            {
                "id": "O0.3",
                "name": "outward_matrix_inclusion",
                "status": "OPEN",
                "interface": "RouteB.O0.RegularizerMatrixInclusion",
            },
            {
                "id": "O0.4",
                "name": "inverse_port_consumer",
                "status": "OPEN",
                "interface": "RouteB.O0.ResolventPortPerturbation",
            },
        ],
        "exact_consequence": (
            "under a common unregularized base, M_float = M_exact - delta I; "
            "inverse perturbation is a full-matrix resolvent obligation"
        ),
        "remaining_obligation": (
            "prove an outward inclusion for the deployed evaluation, or declare "
            "the exact-real evaluator authoritative and rebind all source claims"
        ),
        "formal_certificate_allowed": False,
        "registry_eligible": False,
    }
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    node = find(state, "P4.true_dh_regularizer_semantics_bridge")
    changed = False
    if node.metadata.get("regularizer_semantics") != payload:
        node.metadata["regularizer_semantics"] = payload
        changed = True
    unresolved = list(node.metadata.get("unresolved", []))
    for item in (
        "IEEE754_outward_inclusion_for_mu",
        "shared_mu_binding_through_MDD_and_R_port",
        "authoritative_evaluator_choice",
    ):
        if item not in unresolved:
            unresolved.append(item)
    if unresolved != node.metadata.get("unresolved"):
        node.metadata["unresolved"] = unresolved
        changed = True
    contract = dict(node.metadata.get("frontier_repair_contract") or {})
    contract["next_agent_action"] = (
        "prove the outward inclusion for Float64 1e-6 versus exact 1/1000000, "
        "then bind the same mu through M_DD and R_port"
    )
    if node.metadata.get("frontier_repair_contract") != contract:
        node.metadata["frontier_repair_contract"] = contract
        changed = True
    if changed:
        state.event(
            "routeb_regularizer_semantics_draft_recorded",
            node_id=node.id,
            status=payload["status"],
            deployed_float64_exact_value=payload["deployed_float64_exact_value"],
            analytic_exact_real_value=payload["analytic_exact_real_value"],
            registry_promoted=False,
            formal_certificate_allowed=False,
        )
        state.validate()
        store.save(state)
    print({"status": "recorded" if changed else "already_recorded",
           "node_id": node.id, "audit_status": payload["status"],
           "deployed_minus_analytic": payload["deployed_minus_analytic"],
           "state_revision": state.revision})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
