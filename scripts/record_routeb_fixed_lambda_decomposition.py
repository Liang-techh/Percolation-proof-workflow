"""Decompose the fixed-lambda witness into independent proof obligations.

The decomposition is a planning/formalization target.  It does not consume
the diagnostic receipt as a theorem and deliberately keeps every child open
until a pinned Lean/comparator receipt is supplied.
"""
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from percolation_workflow.store import StateStore  # noqa: E402


def find(state, name: str):
    for node in state.nodes.values():
        if node.name == name:
            return node
    raise ValueError(f"missing node: {name}")


CHILDREN = (
    (
        "P4.fixed_lambda_decimal_quantization",
        "Treat every declared decimal ledger field as its exact quantized rational and prove the 1e-12 floor is no larger than the recorded candidate margin.",
        "Parse positive decimal numerators and denominators, preserve their textual provenance, and prove the conservative floor inequality in exact rational arithmetic; do not infer an unrecorded real source value.",
    ),
    (
        "P4.fixed_lambda_upper_ratio_identity",
        "For positive gamma_cell, prove lambda_upper=gamma_external/gamma_cell and candidate_margin=gamma_external-lambda*gamma_cell, with strict lambda admissibility equivalent to 1<lambda<lambda_upper.",
        "Use field-level rational arithmetic and the positivity premise to cross-multiply only by a positive denominator; retain the aggregate/per-cell metric distinction.",
    ),
    (
        "P4.fixed_lambda_two_row_admissibility",
        "For every declared row selected with fixed rational lambda=2 and theta=1, prove 1<lambda<lambda_upper and the recorded conservative Schur margin is positive.",
        "Instantiate the scalar contract at lambda=2, replay the exact quantized row witness, and preserve negative lambda=5/3 rows as separate obstruction evidence.",
    ),
    (
        "P4.fixed_lambda_uniform_declared_row_fold",
        "Fold the finite declared ledger rows for eta=2.7 and eta=5.6 into a uniform lambda=2 witness, without claiming coverage outside the ledger artifact.",
        "Combine the row-level witnesses with finite-set membership and distinct-box accounting; expose the exact finite witness set and leave true-DH interval coverage as an independent premise.",
    ),
)


def main() -> int:
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    parent = find(state, "P4.fixed_cell_lambda_admissibility")
    existing_by_name = {node.name: node for node in state.nodes.values()}
    child_ids: list[str] = []
    changed = False
    for name, statement, sketch in CHILDREN:
        child = existing_by_name.get(name)
        if child is None:
            child_id = state.add_node(
                name,
                statement,
                parent_id=parent.id,
                proof_sketch=sketch,
                metadata={
                    "verification_domain": "lean",
                    "statement_status": "formalization_target",
                    "claim_status": "fixed_lambda_decomposition_child_open",
                    "evidence_level": "typed-proof-obligation",
                    "registry_eligible": False,
                    "comparator_accepted": False,
                    "formal_certificate_allowed": False,
                    "source_provenance": {
                        "origin": "coordinator-created decomposition of the Route-B fixed-lambda contract",
                        "upstream_inspiration": "Route-B fixed-cell combined-Schur ledger",
                        "attribution_required": True,
                    },
                    "decomposition_role": "fixed_lambda_witness",
                    "unresolved": [
                        "pinned_lean_compile_receipt",
                        "zero_sorry_and_allowed_axioms_receipt",
                        "statement_comparator_receipt",
                    ],
                },
            )
            child = state.nodes[child_id]
            existing_by_name[name] = child
            changed = True
        else:
            if child.statement != statement:
                raise ValueError(f"existing child statement mismatch: {name}")
            if child.parent_id != parent.id:
                raise ValueError(f"existing child has unexpected parent: {name}")
        if child.id not in parent.dependencies:
            parent.dependencies.append(child.id)
            changed = True
        child_ids.append(child.id)

    decomposition = {
        "schema_version": 1,
        "status": "open_children_pending_pinned_receipts",
        "children": child_ids,
        "child_order": child_ids,
        "closure_rule": "fixed_cell_lambda_admissibility closes only after every child is VERIFIED and comparator-accepted",
        "finite_witness_boundary": "declared ledger rows only; no true-DH/domain coverage claim",
    }
    if parent.metadata.get("decomposition_contract") != decomposition:
        parent.metadata["decomposition_contract"] = decomposition
        changed = True
    parent.proof_sketch = (
        "Decompose the fixed rational parameter contract into exact decimal-to-rational "
        "quantization, positive-denominator ratio identity, lambda=2 row admissibility, "
        "and a finite declared-row fold. Keep all source, true-DH, coverage, residual, "
        "Lean, and comparator obligations independent."
    )
    if changed:
        state.event(
            "routeb_fixed_lambda_decomposition_recorded",
            parent_id=parent.id,
            children=child_ids,
            closure_rule=decomposition["closure_rule"],
            registry_promoted=False,
            formal_certificate_allowed=False,
        )
        state.validate()
        store.save(state)
        print({"status": "recorded", "parent_id": parent.id,
               "children": child_ids, "state_revision": state.revision})
    else:
        print({"status": "already_recorded", "parent_id": parent.id,
               "children": child_ids, "state_revision": state.revision})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
