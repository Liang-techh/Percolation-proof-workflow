"""Record the interval-local P8 endpoint adapter as an open frontier child."""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from percolation_workflow.store import StateStore


def ref(path: Path) -> dict[str, str]:
    return {
        "path": str(path.resolve()),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def find(state, name: str):
    for node in state.nodes.values():
        if node.name == name:
            return node
    raise ValueError(f"missing node: {name}")


def main() -> int:
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    parent = find(state, "P8.independent_reachability")
    name = "P8.interval_local_endpoint_adapter"
    source_artifacts = [
        ref(ROOT / "examples/routeb_p8_ramp_reconstruction_sidecar/P8RampReconstruction.lean"),
        ref(ROOT / "examples/routeb_p8_ramp_reconstruction_sidecar/README.md"),
        ref(ROOT / "examples/routeb_p8_ramp_reconstruction_sidecar/lean-toolchain"),
        ref(ROOT / "examples/routeb_p8_ramp_reconstruction_sidecar/verify.sh"),
    ]
    unresolved = [
        "p8_source_provider_continuity_on_closed_interval",
        "p8_source_provider_derivative_on_open_interval",
        "p8_interval_integral_identity_for_c",
        "p8_flowpipe_coverage_and_terminal_binding",
        "pinned_github_lean_compile_receipt",
    ]
    metadata = {
        "verification_domain": "lean-source-independent-adapter",
        "statement_status": "open_frontier_pending_pinned_lean_compile",
        "evidence_level": "local_source_sidecar_uncompiled",
        "claim_status": "interval_local_adapter_open",
        "registry_eligible": False,
        "comparator_accepted": False,
        "formal_certificate_allowed": False,
        "preferred_route": True,
        "unresolved": unresolved,
        "theorem_names": [
            "RouteBP8RampReconstruction.endpoint_eq_of_zero_derivative_on_interval",
            "RouteBP8RampReconstruction.ramp_endpoint_on_interval",
        ],
        "source_artifacts": source_artifacts,
        "frontier_contract": {
            "domain": "closed_interval_Icc_open_interior_Ioo",
            "required_inputs": [
                "ContinuousOn c Icc(a,b)",
                "HasDerivAt c 0 on Ioo(a,b)",
                "IntervalIntegrable zero and c",
                "HasDerivAt w (c t) on Ioo(a,b)",
                "integral c = c0*(b-a)",
            ],
            "output": "c(b)=c0 and w(b)=w(a)+c0*(b-a)",
            "does_not_prove": [
                "source_binding",
                "ode_existence",
                "flowpipe_coverage",
                "routeb_admission",
            ],
        },
    }
    existing = next((n for n in state.nodes.values() if n.name == name), None)
    if existing is None:
        node_id = state.add_node(
            name,
            "The interval-local P8 calculus adapter transfers the ramp endpoint "
            "from closed-interval continuity, open-interval derivative data, "
            "and explicit integral identities.",
            parent_id=parent.id,
            dependencies=[],
            proof_sketch=(
                "Apply the interval fundamental theorem twice: zero derivative "
                "closes c, then the c-integral identity closes w. Keep source "
                "regularity, flowpipe coverage, and admission separate."),
            metadata=metadata,
        )
        state.event(
            "routeb_p8_interval_local_adapter_created",
            node_id=node_id,
            parent_id=parent.id,
            status=metadata["statement_status"],
            theorem_names=metadata["theorem_names"],
            source_artifacts=source_artifacts,
            formal_certificate_allowed=False,
            registry_promoted=False,
        )
        store.save(state)
        print({"status": "recorded", "node_id": node_id,
               "state_revision": state.revision})
        return 0

    changed = False
    for key, value in metadata.items():
        if existing.metadata.get(key) != value:
            existing.metadata[key] = value
            changed = True
    if existing.parent_id != parent.id:
        existing.parent_id = parent.id
        changed = True
    if changed:
        state.event(
            "routeb_p8_interval_local_adapter_refresh",
            node_id=existing.id,
            parent_id=parent.id,
            status=metadata["statement_status"],
            theorem_names=metadata["theorem_names"],
            source_artifacts=source_artifacts,
            formal_certificate_allowed=False,
            registry_promoted=False,
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
