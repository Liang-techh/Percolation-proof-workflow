"""Record the force-scale/source projection seam for the true-DH block.

This is deliberately a static source contract.  It distinguishes controller
torque terms from the analytic lifted nominal row and records unsupported
requested coefficients as an obstruction instead of inventing a binding.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
ROUTE_B = ROOT.parent / "6dof_sos_optimized" / "6dof_sos_optimized"
DEPLOYED = ROUTE_B / "robot_final" / "dhport_lib.jl"
LIFTED = ROUTE_B / "routeB_dense_Mq" / "routeB_fourier_lifted_descriptor_model.jl"
NOMINAL = ROUTE_B / "routeB_dense_Mq" / "P5_COMPACT_NOMINAL_DESCRIPTOR_INTERFACE.md"
STATE = ROOT / "artifacts/routeb_6dof/state.json"
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
    for path in (DEPLOYED, LIFTED, NOMINAL):
        if not path.is_file():
            raise FileNotFoundError(path)
    deployed = DEPLOYED.read_text(encoding="utf-8", errors="replace")
    lifted = LIFTED.read_text(encoding="utf-8", errors="replace")
    nominal = NOMINAL.read_text(encoding="utf-8", errors="replace")

    deployed_tau = re.search(r"(?m)^\s*tau\s*=", deployed)
    lifted_tau = re.search(r"(?m)^\s*tau\s*=", lifted)
    required_terms = {
        "q5_over_100": r"q\s*\[?5\]?\s*/\s*100",
        "q4_over_200": r"q\s*\[?4\]?\s*/\s*200",
    }
    deployed_required = {
        name: bool(re.search(pattern, deployed, re.IGNORECASE))
        for name, pattern in required_terms.items()
    }
    lifted_required = {
        name: bool(re.search(pattern, lifted, re.IGNORECASE))
        for name, pattern in required_terms.items()
    }
    nominal_cross_terms = {
        "lifted_q5_cross_term": "Q(1, 20) * q[5]" in lifted,
        "lifted_q4_cross_term": "Q(1, 20) * q[4]" in lifted,
    }
    deployed_controller_semantics = (
        "tau = -Kp .* q - (Kd + b_fr) .* dq + G0v + (gw_coef .* I_val) .* w"
        in deployed
    )
    lifted_controller_semantics = (
        "tau = [-Kp[i] * q[i] - (Kd[i] + Bfr[i]) * dq[i] + g0[i] + GwI[i] * w for i in 1:6]"
        in lifted
    )
    interface_contract_present = all(
        phrase in nominal
        for phrase in (
            "M_DD(q)*v + DeltaM_DB(q)*a_B = 0",
            "r_B - M_BD(q)*v = 0",
        )
    )
    requested_present = all(deployed_required.values()) and all(lifted_required.values())
    status = (
        "FORCE_SCALE_CONTRACT_PRESENT_PENDING_BINDING"
        if requested_present
        else "FORCE_SCALE_TERMS_UNSUPPORTED_IN_CURRENT_CANONICAL_SOURCES"
    )
    audit = {
        "schema_version": 1,
        "status": status,
        "scope": "static selected-source scan; no external source mutation",
        "blocks": {"B": [4, 5], "D": [1, 2, 3, 6]},
        "requested_force_terms": {"q5_over_100": "q5/100", "q4_over_200": "q4/200"},
        "requested_terms_found": {
            "deployed_dhport": deployed_required,
            "lifted_descriptor": lifted_required,
        },
        "controller_tau_source": {
            "deployed_expression_present": deployed_controller_semantics,
            "lifted_expression_present": lifted_controller_semantics,
            "deployed_tau_region_present": deployed_tau is not None,
            "lifted_tau_region_present": lifted_tau is not None,
            "deployed_rows_4_5_semantics": "-Kp_B*q_B-(Kd_B+b_fr_B)*dq_B+G0v_B+GwI_B*w",
            "lifted_rows_4_5_semantics": "-Kp_B*q_B-(Kd_B+Bfr_B)*dq_B+g0_B+GwI_B*w",
        },
        "lifted_nominal_projection": {
            **nominal_cross_terms,
            "observed_cross_coefficient": "1/20" if all(nominal_cross_terms.values()) else None,
            "interpretation": "nominal lifted coupling, not deployed tau coefficient",
        },
        "typed_block_interface_present": interface_contract_present,
        "decomposition": [
            {
                "id": "F0",
                "name": "authoritative_source_selection",
                "status": "OPEN" if not requested_present else "PENDING_BINDING",
                "interface": "RouteB.Force.AuthoritativeSourceKey",
            },
            {
                "id": "F1",
                "name": "controller_tau_semantics",
                "status": "STATIC_FACT_PENDING_AUTHORITY",
                "interface": "RouteB.Force.ControllerTauSemantics",
            },
            {
                "id": "F2",
                "name": "coefficient_normalization",
                "status": "OPEN" if not requested_present else "PENDING_BINDING",
                "interface": "RouteB.Force.CoefficientNormalization",
            },
            {
                "id": "F3",
                "name": "block_projection_B45",
                "status": "OPEN",
                "interface": "RouteB.Force.TrueDHBlockProjection",
            },
            {
                "id": "F4",
                "name": "source_bound_admission",
                "status": "OPEN",
                "interface": "RouteB.Force.SourceBoundAdmission",
            },
        ],
        "source_artifacts": [ref(DEPLOYED), ref(LIFTED), ref(NOMINAL)],
        "resolution": (
            "bind the requested force terms only after an authoritative source/config is identified; "
            "otherwise remove them from the target contract and use the observed source equations"
            if not requested_present
            else "source terms are present but still require typed coefficient binding"
        ),
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }

    store = StateStore(STATE)
    state = store.load()
    node = find(state, "P4.true_dh_force_descriptor_semantics")
    parent = find(state, "P4.true_dh_port_source_binding")
    changed = node.metadata.get("force_scale_contract") != audit
    node.metadata["force_scale_contract"] = audit
    unresolved = list(node.metadata.get("unresolved", []))
    if not requested_present and "requested_force_scale_terms_not_found_in_canonical_sources" not in unresolved:
        unresolved.append("requested_force_scale_terms_not_found_in_canonical_sources")
        changed = True
    if unresolved != node.metadata.get("unresolved"):
        node.metadata["unresolved"] = unresolved
        changed = True
    parent_summary = {
        "status": status,
        "force_descriptor_node": node.name,
        "requested_terms_found": audit["requested_terms_found"],
        "formal_certificate_allowed": False,
    }
    if parent.metadata.get("force_scale_contract") != parent_summary:
        parent.metadata["force_scale_contract"] = parent_summary
        changed = True
    if changed:
        state.event(
            "routeb_force_scale_contract_recorded",
            node_id=node.id,
            parent_id=parent.id,
            status=status,
            requested_terms_found=audit["requested_terms_found"],
            registry_promoted=False,
            formal_certificate_allowed=False,
        )
        state.validate()
        store.save(state)
    print({"status": "recorded" if changed else "already_recorded",
           "audit_status": status, "state_revision": store.load().revision,
           "formal_certificate_allowed": False, "registry_promoted": False})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
