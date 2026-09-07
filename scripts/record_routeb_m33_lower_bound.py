"""Record the exact algebraic lower-bound child for the M33 Fourier leaf."""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = (ROOT.parent / "6dof_sos_optimized" / "6dof_sos_optimized"
            / "artifacts" / "task_routeb_source_fourier_binding_current")
SIDEcar = ROOT / "examples/routeb_m33_exact_lower_lean"
sys.path.insert(0, str(ROOT / "src"))

from percolation_workflow.store import StateStore


def ref(path: Path) -> dict[str, str]:
    return {"path": str(path.resolve()),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest().upper()}


def find(state, name: str):
    for node in state.nodes.values():
        if node.name == name:
            return node
    raise ValueError(f"missing node: {name}")


def main() -> int:
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    parent = find(state, "P3.m33_exact_fourier_source_leaf")
    name = "P3.m33_exact_lower_bound"
    paths = [
        SIDEcar / "M33LowerBound.lean",
        SIDEcar / "README.md",
        SIDEcar / "check_exact_lower.py",
        SIDEcar / "lean-toolchain",
        SIDEcar / "verify.sh",
        ARTIFACT / "CHECK_RESULT.json",
        ARTIFACT / "m33_fourier_witness.csv",
    ]
    source_artifacts = [ref(path) for path in paths if path.is_file()]
    metadata = {
        "verification_domain": "lean-exact-algebraic-candidate",
        "statement_status": "pending_pinned_lean_compile",
        "evidence_level": "source_bound_exact_algebraic_sidecar_uncompiled",
        "claim_status": "m33_global_lower_bound_open",
        "registry_eligible": False,
        "comparator_accepted": False,
        "formal_certificate_allowed": False,
        "physical_certificate_allowed": False,
        "theorem_names": ["RouteBM33ExactLower.m33_lower_bound"],
        "source_artifacts": source_artifacts,
        "upstream_source_leaf": {
            "node": parent.name,
            "canonical_source_sha256":
                "AEBE6DB09B2D943448C5D701631109DBA8F5EEB070CC66593E5DBACA26485936",
            "exact_formula_support": 11,
        },
        "bound": "3016537/12000000",
        "frontier_contract": {
            "substitution": [
                "u=cos(q5) in [-1,1]",
                "x=cos(2*q4) in [-1,1]",
                "cos(2*q5)=2*u^2-1",
            ],
            "output": "M33 >= 3016537/12000000",
        },
        "unresolved": [
            "pinned_lean_compile_and_axiom_receipt",
            "coordinator_statement_identity_and_comparator_binding",
            "upstream_checker_to_lean_formula_binding",
            "Float64_rounding_and_all_entry_mass_binding",
            "P3_partition_coverage_and_inverse_bounds",
        ],
    }
    existing = next((n for n in state.nodes.values() if n.name == name), None)
    if existing is None:
        node_id = state.add_node(
            name,
            "The exact M33 Fourier expression has the global rational lower "
            "bound 3016537/12000000 on the cosine box.",
            parent_id=parent.id,
            dependencies=[],
            proof_sketch=(
                "Factor the difference from the endpoint lower bound as "
                "(u+1)*(B-2C*(1-u)*(1-x)); bound the two box factors by 2 "
                "and close the remaining rational inequality."),
            metadata=metadata,
        )
        state.event(
            "routeb_m33_exact_lower_bound_recorded",
            node_id=node_id,
            parent_id=parent.id,
            source_artifacts=source_artifacts,
            bound=metadata["bound"],
            status=metadata["statement_status"],
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
            "routeb_m33_exact_lower_bound_refresh",
            node_id=existing.id,
            parent_id=parent.id,
            source_artifacts=source_artifacts,
            bound=metadata["bound"],
            status=metadata["statement_status"],
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
