"""Attach the pure M4 cross-branch budget arithmetic child to the DAG."""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from percolation_workflow.store import StateStore


def ref(path: Path) -> dict[str, str]:
    return {"path": str(path.resolve()),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def find(state, name: str):
    for node in state.nodes.values():
        if node.name == name:
            return node
    raise ValueError(f"missing node: {name}")


def main() -> int:
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    parent = find(state, "M4.block45_full_certificate")
    name = "M4.cross_branch_budget_transfer"
    source_artifacts = [ref(path) for path in (
        ROOT / "examples/routeb_m4_cross_branch_budget_lean/CrossBranchBudget.lean",
        ROOT / "examples/routeb_m4_cross_branch_budget_lean/README.md",
        ROOT / "examples/routeb_m4_cross_branch_budget_lean/lean-toolchain",
        ROOT / "examples/routeb_m4_cross_branch_budget_lean/verify.sh",
    )]
    unresolved = [
        "pinned_lean_compile_receipt",
        "zero_sorry_and_allowed_axioms_receipt",
        "P7_integral_tail_charge_binding",
        "P8_ramp_identity_binding",
    ]
    existing = next((n for n in state.nodes.values() if n.name == name), None)
    if existing is not None:
        changed = False
        if existing.parent_id != parent.id:
            existing.parent_id = parent.id
            changed = True
        if existing.id not in parent.dependencies:
            parent.dependencies.append(existing.id)
            changed = True
        if existing.metadata.get("source_artifacts") != source_artifacts:
            existing.metadata["source_artifacts"] = source_artifacts
            changed = True
        if existing.metadata.get("unresolved") != unresolved:
            existing.metadata["unresolved"] = unresolved
            changed = True
        if changed:
            state.event(
                "routeb_m4_cross_branch_budget_provenance_refresh",
                node_id=existing.id, parent_id=parent.id,
                source_artifacts=source_artifacts,
                status="pending_pinned_lean_compile",
                formal_certificate_allowed=False, registry_promoted=False,
            )
            store.save(state)
            print({"status": "provenance_refreshed", "node_id": existing.id,
                   "state_revision": state.revision})
        else:
            print({"status": "already_recorded", "node_id": existing.id,
                   "state_revision": state.revision})
        return 0

    node_id = state.add_node(
        name,
        "The conditional P7 tail charge transfers into the improved M4 "
        "residual budget window by exact rational arithmetic.",
        parent_id=parent.id,
        dependencies=[],
        proof_sketch=(
            "Formalize D_new-D_old=1/10000, the old-gate rho_bar<=16 "
            "corollary, and the general slack form. Keep the P7 integral "
            "estimate and P8 ramp/source bindings as separate obligations."),
        metadata={
            "verification_domain": "lean-pure-arithmetic",
            "statement_status": "pending_pinned_lean_compile",
            "evidence_level": "conditional_arithmetic_child",
            "claim_status": "cross_branch_budget_arithmetic_open",
            "registry_eligible": False,
            "comparator_accepted": False,
            "formal_certificate_allowed": False,
            "preferred_route": True,
            "unresolved": unresolved,
            "source_artifacts": source_artifacts,
        },
    )
    state.event(
        "routeb_m4_cross_branch_budget_child_created",
        node_id=node_id, parent_id=parent.id,
        source_artifacts=source_artifacts,
        status="pending_pinned_lean_compile",
        formal_certificate_allowed=False, registry_promoted=False,
    )
    store.save(state)
    print({"status": "recorded", "node_id": node_id,
           "state_revision": state.revision})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
