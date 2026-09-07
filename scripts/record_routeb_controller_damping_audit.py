"""Record the exact deployed/lifted controller damping audit in the DAG."""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ROUTE_B = ROOT.parent / "6dof_sos_optimized" / "6dof_sos_optimized"
SRC = ROUTE_B / "routeB_dense_Mq"
DEPLOYED_SRC = ROUTE_B / "robot_final"
sys.path.insert(0, str(ROOT / "src"))

from percolation_workflow.routeb_controller_semantics import (  # noqa: E402
    audit_controller_damping_semantics,
)
from percolation_workflow.store import StateStore  # noqa: E402


def ref(path: Path) -> dict[str, str]:
    return {"path": str(path.resolve()),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest().upper()}


def find(state, name: str):
    for node in state.nodes.values():
        if node.name == name:
            return node
    raise ValueError(f"missing node: {name}")


def frac_list(values):
    return [f"{value.numerator}/{value.denominator}" for value in values]


def main() -> int:
    # robot_final is the deployment authority; the dense-source copy is only
    # a source-side mirror and must not silently define deployment semantics.
    deployed = DEPLOYED_SRC / "dhport_lib.jl"
    lifted = SRC / "routeB_fourier_lifted_descriptor_model.jl"
    for path in (deployed, lifted):
        if not path.is_file():
            raise FileNotFoundError(path)
    audit = audit_controller_damping_semantics(
        deployed.read_text(encoding="utf-8", errors="replace"),
        lifted.read_text(encoding="utf-8", errors="replace"),
    )
    payload = {
        "schema_version": 1,
        "status": audit.status,
        "deployed": {
            "Kd": frac_list(audit.deployed_kd or ()),
            "friction": frac_list(audit.deployed_friction or ()),
            "Kd_plus_friction": frac_list(audit.deployed_sum or ()),
        },
        "lifted": {
            "Kd": frac_list(audit.lifted_kd or ()),
            "friction": frac_list(audit.lifted_friction or ()),
            "Kd_plus_friction": frac_list(audit.lifted_sum or ()),
        },
        "mismatched_joint_indices": list(audit.mismatched_indices),
        "deployed_minus_lifted": frac_list(audit.difference or ()),
        "errors": list(audit.errors),
        "source_artifacts": [ref(deployed), ref(lifted)],
        "mathematical_conclusion": (
            "The deployed and lifted torque laws are source-equivalent only if "
            "their exact per-coordinate Kd+friction vectors agree."
        ),
        "required_repair": (
            "select one authoritative damping vector and regenerate/rebind the "
            "other source before any full true-DH source equivalence claim"
        ),
        "formal_certificate_allowed": False,
        "registry_eligible": False,
    }

    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    node = find(state, "P4.true_dh_force_descriptor_semantics")
    changed = False
    if node.metadata.get("controller_damping_semantics") != payload:
        node.metadata["controller_damping_semantics"] = payload
        changed = True
    unresolved = list(node.metadata.get("unresolved", []))
    for item in (
        "controller_damping_vector_source_equivalence",
        "authoritative_controller_parameter_selection",
    ):
        if item not in unresolved:
            unresolved.append(item)
    if unresolved != node.metadata.get("unresolved"):
        node.metadata["unresolved"] = unresolved
        changed = True
    node.metadata["math_bottleneck"] = "source_binding"
    node.metadata["frontier_repair_contract"] = {
        **(node.metadata.get("frontier_repair_contract") or {}),
        "schema_version": 1,
        "next_agent_action": (
            "reconcile exact Kd+friction vectors, select authoritative source, "
            "and return a pinned source/comparator receipt"
        ),
        "preserve_semantic_boundary": (
            "do not silently replace deployed coefficients with lifted coefficients"
        ),
    }
    if changed:
        state.event(
            "routeb_controller_damping_semantics_recorded",
            node_id=node.id,
            audit_status=audit.status,
            mismatched_joint_indices=list(audit.mismatched_indices),
            registry_promoted=False,
            formal_certificate_allowed=False,
        )
        state.validate()
        store.save(state)
    print({"status": "recorded" if changed else "already_recorded",
           "audit_status": audit.status,
           "mismatched_joint_indices": list(audit.mismatched_indices),
           "state_revision": state.revision})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
