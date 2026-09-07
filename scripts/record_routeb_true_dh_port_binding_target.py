"""Record the missing true-DH source-to-port binding theorem target."""
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
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    parent = find(state, "P4.residual_schur_pmi")
    port = find(state, "P4.residual_port_frobenius_bound")
    nominal = find(state, "P4.nominal_distal_descriptor_bridge")
    name = "P4.true_dh_port_source_binding"
    source_paths = (
        SRC / "dhport_lib.jl",
        SRC / "routeB_pmi_certificate.jl",
        SRC / "routeB_compact_nominal_descriptor_interface.csv",
        SRC / "routeB_compact_dh_nominal_distal_bridge_audit.csv",
        ROOT / "src/percolation_workflow/routeb_source_contract.py",
        ROOT / "scripts/record_routeb_p4_source_binding_receipt.py",
    )
    for path in source_paths:
        if not path.is_file():
            raise FileNotFoundError(path)

    metadata = {
        "verification_domain": "lean",
        "research_stage": "P4",
        "math_lane": "source_semantics",
        "math_bottleneck": "source_binding",
        "statement_status": "formalization_target",
        "claim_status": "true_dh_port_source_binding_open",
        "evidence_level": "typed-source-semantics-target",
        "registry_eligible": False,
        "comparator_accepted": False,
        "formal_certificate_allowed": False,
        "source_artifacts": [ref(path) for path in source_paths],
        "source_provenance": {
            "origin": "coordinator-created typed source-binding target; no external theorem copied",
            "upstream_inspiration": "Route-B DH port source contract and nominal distal bridge",
            "attribution_required": True,
        },
        "mathematical_contract": {
            "premises": [
                "M_mu(q) a = tau(q,dq,w) - C_fd(q,dq)dq - G_fd(q)",
                "the deployed force residual uses the explicit force-scale kc correction",
                "the nominal descriptor bridge uses M_mu,DD*v+DeltaM_DB*a_B=0 and r_B-M_BD*v=0",
                "R is the same typed residual map consumed by the port Frobenius bound",
            ],
            "conclusion": "R a_B = r_B = (M_mu(q) a)_B on the declared descriptor/source domain",
            "required_coordinate_scale": "force coordinates q5/100 and q4/200; normalized f coordinates must not be silently substituted",
            "required_remote_term": "M_BD(q)*a_D remains explicit in the block projection",
            "regularization": "M_mu=M+1/1000000 I and central-FD h=1/100000 must be shared by source and adapter",
            "non_implications": [
                "source text audit is not a Lean proof",
                "nominal bridge identities do not prove coefficient-level R binding",
                "port Frobenius budget does not prove source equality",
                "the target does not close interval coverage or residual absorption",
            ],
        },
        "frontier_repair_contract": {
            "schema_version": 1,
            "next_agent_action": "construct the smallest typed adapter that identifies the deployed DH force row, descriptor block projection, and port map R on one common real domain",
            "inputs": [port.name, nominal.name],
            "required_receipts": [
                "source contract audit",
                "pinned Lean source/adapter compile",
                "statement comparator identity",
            ],
            "acceptance_conditions": [
                "exact force-scale equality is stated, not inferred from normalized f notation",
                "the same regularizer and FD semantics occur on both sides",
                "M_BD*a_D is retained rather than replaced by a surrogate difference term",
                "zero sorry/admit and allowed-axiom receipt are explicit",
            ],
            "promotion_blocked_until": [
                "pinned_lean_compile_receipt",
                "coefficient_level_true_dh_binding",
                "full_domain_coverage",
                "residual_absorption",
            ],
        },
        "unresolved": [
            "coefficient_level_R_aB_equals_rB_identity",
            "Float64_to_exact_real_source_adapter",
            "common_domain_and_angle_graph_binding",
            "residual_absorption_and_flowpipe_consumption",
            "pinned_lean_and_statement_comparator_receipt",
        ],
    }

    existing = next((node for node in state.nodes.values() if node.name == name), None)
    if existing is None:
        node_id = state.add_node(
            name,
            "On the declared regularized true-DH source domain, prove the typed equality "
            "R a_B = r_B = (M_mu(q) a)_B while retaining the explicit M_BD(q)a_D block term.",
            parent_id=parent.id,
            proof_sketch=(
                "Bind the deployed force/descriptor source to one exact real interface, "
                "project the common descriptor equation to block B, and identify the "
                "same residual map R used by the port bound. Keep force-vs-normalized "
                "coordinates, regularization, FD semantics, and remote acceleration "
                "as explicit premises; do not infer them from a numerical receipt."),
            metadata=metadata,
        )
        state.event(
            "routeb_true_dh_port_source_binding_target_added",
            node_id=node_id,
            parent_id=parent.id,
            source_artifacts=metadata["source_artifacts"],
            required_upstream=[port.id, nominal.id],
            registry_promoted=False,
            formal_certificate_allowed=False,
        )
        store.save(state)
        print({"status": "recorded", "node_id": node_id,
               "state_revision": state.revision})
        return 0

    changed = False
    if existing.parent_id != parent.id:
        existing.parent_id = parent.id
        if existing.id not in parent.dependencies:
            parent.dependencies.append(existing.id)
        changed = True
    for key, value in metadata.items():
        if existing.metadata.get(key) != value:
            existing.metadata[key] = value
            changed = True
    if changed:
        state.event(
            "routeb_true_dh_port_source_binding_target_refresh",
            node_id=existing.id,
            parent_id=parent.id,
            source_artifacts=metadata["source_artifacts"],
            registry_promoted=False,
            formal_certificate_allowed=False,
        )
        store.save(state)
        print({"status": "refreshed", "node_id": existing.id,
               "state_revision": state.revision})
    else:
        print({"status": "already_recorded", "node_id": existing.id,
               "state_revision": state.revision})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
