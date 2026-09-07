"""Record the narrow Route-B P4 source-to-port binding seam.

This recorder joins two already fail-closed audits:

* the canonical Julia source contract for the deployed force/descriptor
  semantics; and
* the exact-rational nominal distal bridge interface.

It deliberately records a *conditional interface receipt* only.  In
particular, ``R_port*a_B = r_B`` is still an open theorem/adapter obligation, so
this script never promotes a node, a registry entry, or the global gate.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ROUTE_B = ROOT.parent / "6dof_sos_optimized" / "6dof_sos_optimized"
SRC = ROUTE_B / "routeB_dense_Mq"
DEPLOYED_SRC = ROUTE_B / "robot_final"
sys.path.insert(0, str(ROOT / "src"))

from percolation_workflow.routeb_nominal_distal_contract import (  # noqa: E402
    audit_routeb_nominal_distal_bridge,
)
from percolation_workflow.routeb_source_contract import (  # noqa: E402
    audit_routeb_p4_source_contract,
)
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
    pmi = SRC / "routeB_pmi_certificate.jl"
    # robot_final is the deployment source of truth; routeB_dense_Mq contains
    # research mirrors and must not silently define the deployed contract.
    dh = DEPLOYED_SRC / "dhport_lib.jl"
    bridge_audit = SRC / "routeB_compact_dh_nominal_distal_bridge_audit.csv"
    bridge_interface = SRC / "routeB_compact_nominal_descriptor_interface.csv"
    nominal_doc = SRC / "P5_COMPACT_NOMINAL_DESCRIPTOR_INTERFACE.md"
    bridge_doc = SRC / "P5_COMPACT_DH_NOMINAL_DISTAL_BRIDGE_AUDIT.md"
    module = ROOT / "src/percolation_workflow/routeb_source_contract.py"
    nominal_module = ROOT / "src/percolation_workflow/routeb_nominal_distal_contract.py"
    required = (pmi, dh, bridge_audit, bridge_interface, nominal_doc,
                bridge_doc, module, nominal_module)
    for path in required:
        if not path.is_file():
            raise FileNotFoundError(path)

    pmi_text = pmi.read_text(encoding="utf-8", errors="replace")
    dh_text = dh.read_text(encoding="utf-8", errors="replace")
    source_result = audit_routeb_p4_source_contract(pmi_text, dh_text)
    strict_source_checks = {
        "mass_regularizer_literal": "const MASS_REGULARIZER = 1e-6" in dh_text,
        "fd_step_literal": "const CG_FINITE_DIFF_STEP = 1e-5" in dh_text,
        "mass_regularizer_is_parameterized": (
            "mass_regularization::Real = MASS_REGULARIZER" in dh_text
            and "regularization = mass_regularization" in dh_text
        ),
        "fd_step_is_parameterized": (
            "fd_step::Real = CG_FINITE_DIFF_STEP" in dh_text
            and "fd_step = fd_step" in dh_text
        ),
    }

    audit_text = bridge_audit.read_text(encoding="utf-8")
    interface_text = bridge_interface.read_text(encoding="utf-8")
    bridge_result = audit_routeb_nominal_distal_bridge(
        audit_text,
        interface_text,
        artifact_sha256=hashlib.sha256(
            bridge_audit.read_bytes() + bridge_interface.read_bytes()
        ).hexdigest().upper(),
        source_sha256=next(
            (line.split(",", 1)[1] for line in audit_text.splitlines()
             if line.startswith("controller_source_sha256,")),
            None,
        ),
    )
    if source_result.errors:
        raise ValueError(f"source contract rejected: {source_result.errors}")
    if not all(strict_source_checks.values()):
        raise ValueError(f"strict source semantics rejected: {strict_source_checks}")
    if bridge_result.errors:
        raise ValueError(f"nominal bridge rejected: {bridge_result.errors}")

    source_artifacts = [ref(path) for path in required]
    binding = {
        "status": "SOURCE_AND_NOMINAL_BRIDGE_PASS_BINDING_OPEN",
        "source_contract_status": source_result.status,
        "nominal_bridge_status": bridge_result.status,
        "strict_source_checks": strict_source_checks,
        "force_coordinate_kc": list(source_result.expected_force_rho_kc),
        "normalized_coordinate_kc": list(source_result.expected_rho_kc),
        "deployed_descriptor_semantics": (
            "M_mu(q) a = tau(q,dq,w) - C_fd(q,dq) dq - G_fd(q)"
        ),
        "actual_port_quantity": "r_B = (M_mu(q) a)_B",
        "required_remote_term": source_result.remote_term_required,
        "normalized_port_binding_target": "R_port a_B = r_B",
        "nominal_bridge_equations": [
            "M_mu,DD(q)*v + (M_DB(q)-M0_DB)*a_B = 0",
            "r_B - M_BD(q)*v = 0",
        ],
        "regularizer": "mu=1/1000000 in every mass and descriptor term",
        "finite_difference_semantics": "central FD with h=1/100000 for C/G",
        "required_semantic_separation": [
            "the PMI kc term is normalized f-scale, while the deployed force residual uses q5/100,q4/200",
            "the port provider gives a squared Frobenius budget, not a proof of source equality",
            "source text pass does not prove Float64-to-real equality or DH coefficient coverage",
        ],
        "open_binding_obligations": [
            "prove or compile the typed equality R_port*a_B=r_B on the declared descriptor domain",
            "bind the same regularized M_mu and force coordinate scale in the Lean adapter",
            "connect the source equality to the coefficient-level residual absorption theorem",
        ],
        "formal_certificate_allowed": False,
        "registry_eligible": False,
    }

    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    port = find(state, "P4.residual_port_frobenius_bound")
    metadata = port.metadata
    changed = False
    for key, value in {
        "source_binding_receipt": binding,
        "source_binding_artifacts": source_artifacts,
        "source_binding_status": binding["status"],
    }.items():
        if metadata.get(key) != value:
            metadata[key] = value
            changed = True

    unresolved = list(metadata.get("unresolved", []))
    unresolved = [
        "typed_source_binding_R_port_aB_equals_rB"
        if item == "typed_source_binding_R_aB_equals_rB" else item
        for item in unresolved
    ]
    unresolved = list(dict.fromkeys(unresolved))
    for item in (
        "typed_source_binding_R_port_aB_equals_rB",
        "regularized_force_scale_binding",
        "source_to_coefficient_residual_absorption",
    ):
        if item not in unresolved:
            unresolved.append(item)
    if unresolved != metadata.get("unresolved"):
        metadata["unresolved"] = unresolved
        changed = True

    if changed:
        state.event(
            "routeb_p4_source_binding_receipt_recorded",
            node_id=port.id,
            source_binding_status=binding["status"],
            source_contract_status=source_result.status,
            nominal_bridge_status=bridge_result.status,
            source_artifacts=source_artifacts,
            registry_promoted=False,
            formal_certificate_allowed=False,
        )
        store.save(state)
        print({"status": "recorded", "node_id": port.id,
               "state_revision": state.revision,
               "source_binding_status": binding["status"]})
    else:
        print({"status": "already_recorded", "node_id": port.id,
               "state_revision": state.revision,
               "source_binding_status": binding["status"]})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
