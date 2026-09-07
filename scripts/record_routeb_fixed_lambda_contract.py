"""Record the per-cell fixed-lambda admissibility contract for Route-B PMI."""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from check_routeb_fixed_lambda_ledger import audit_ledger
from percolation_workflow.store import StateStore


def find(state, name: str):
    for node in state.nodes.values():
        if node.name == name:
            return node
    raise ValueError(f"missing node: {name}")


def main() -> int:
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    parent = find(state, "P4.combined_schur_port_energy_adapter")
    name = "P4.fixed_cell_lambda_admissibility"
    diagnostic = ROOT / "scripts/check_routeb_fixed_lambda_ledger.py"
    audit = audit_ledger()
    if audit["status"] != "PASS":
        raise ValueError(f"fixed-lambda diagnostic failed: {audit}")
    diagnostic_receipt = {
        "checker": str(diagnostic),
        "checker_sha256": hashlib.sha256(diagnostic.read_bytes()).hexdigest(),
        "status": "diagnostic_pass_decimal_quantized",
        "rows": audit["rows"],
        "per_eta": audit["per_eta"],
        "uniform_lambda_witnesses": audit["uniform_lambda_witnesses"],
        "max_upper_abs_error": audit["max_upper_abs_error"],
        "max_margin_abs_error": audit["max_margin_abs_error"],
        "upper_tolerance": audit["upper_tolerance"],
        "margin_tolerance": audit["margin_tolerance"],
        "registry_promoted": False,
        "formal_certificate_allowed": False,
        "proof_boundary": "diagnostic scalar contract only; no Lean, source, coverage, or registry admission",
    }
    uniform_two = {
        key: value for key, value in audit["uniform_lambda_witnesses"].items()
        if key.endswith(",lambda=2.0")
    }
    uniform_pmi_instantiation = {
        "lambda": "2",
        "theta": "1",
        "lower_right_block": "(1/2) I_2",
        "port_charge": "2*rho*A_up",
        "declared_partition_witnesses": uniform_two,
        "boundary": "finite declared ledger rows only; no true-DH coverage claim",
    }
    metadata = {
        "verification_domain": "lean",
        "research_stage": "P4",
        "statement_status": "formalization_target",
        "claim_status": "fixed_cell_lambda_contract_open",
        "evidence_level": "typed-parameter-domain-target",
        "registry_eligible": False,
        "comparator_accepted": False,
        "formal_certificate_allowed": False,
        "source_provenance": {
            "origin": "new Route-B parameter-domain target; no upstream code copied",
            "upstream_inspiration": "Route-B P5_COMPACT_COMBINED_SCHUR_INTERFACE.md",
            "attribution_required": True,
        },
        "mathematical_contract": {
            "premises": [
                "theta > 0 and lambda = 1 + 1/theta",
                "lambda is fixed for the cell and rational, not state-dependent",
                "the cell ledger supplies an exact strict upper admissibility bound lambda_upper_k",
            ],
            "conclusion": "accept only 1 < lambda_k < lambda_upper_k and a nonnegative exact Schur margin for every consumed cell",
            "pmi_binding": "the same fixed lambda_k is used in the affine PMI and its Schur complement; changing lambda with state invalidates the affine certificate",
            "ledger_formula": "when gamma_cell_k > 0, lambda_upper_k = gamma_external_k / gamma_cell_k and candidate_margin_k = gamma_external_k - lambda_k*gamma_cell_k; strict admissibility is 1 < lambda_k < lambda_upper_k",
            "ledger_guard": "candidate rows with admissible_fixed_lambda=false are rejected even if another row has positive candidate_margin",
            "repair_candidate": "lambda=2 (theta=1) is a fixed rational witness for every declared row in both eta partitions when the ledger marks those rows admissible; this remains a candidate over the declared artifact only",
            "uniform_pmi_instantiation": uniform_pmi_instantiation,
            "ledger_reconciliation": "do not mix aggregate routeB_compact_port_frobenius_ledger lambda bounds with per-cell combined_schur_partition_ledger bounds until their metric and PMI semantics are proven equivalent",
            "diagnostic_receipt": diagnostic_receipt,
            "not_a_coverage_proof": True,
            "not_a_residual_decomposition": True,
        },
        "frontier_repair_contract": {
            "schema_version": 1,
            "obstruction": "some declared eta=5.6 rows reject the historical lambda=5 or lambda=3 candidate",
            "preferred_repair": "reuse fixed rational lambda=2 (theta=1) on each declared row and recompute the Schur margin",
            "witness_receipt_key": "uniform_lambda_witnesses[eta=*,lambda=2.0]",
            "acceptance_conditions": [
                "every selected declared row is marked admissible_fixed_lambda=true",
                "the exact quantized margin and a conservative positive rational lower bound are recorded",
                "lambda remains fixed per cell and is not state-dependent",
                "rejected historical rows remain immutable obstruction evidence",
            ],
            "next_missing_theorem": "lift the finite ledger witness to true-DH interval/source coverage",
            "promotion_blocked_until": [
                "source_binding_R_port_aB_equals_rB",
                "coefficient_level_residual_absorption",
                "complete_domain_coverage",
                "pinned_lean_comparator_receipt",
            ],
        },
        "unresolved": [
            "exact Lean statement for strict rational interval membership",
            "typed connection from lambda_upper_k to the pinned cell ledger",
            "all-cell witness/coverage receipt",
            "reconciliation of aggregate and per-cell lambda admissibility ledgers",
        ],
    }
    existing = next((node for node in state.nodes.values() if node.name == name), None)
    if existing is None:
        node_id = state.add_node(
            name,
            "For each Route-B cell, a fixed rational lambda_k must satisfy "
            "1<lambda_k<lambda_upper_k and the exact Schur margin must be "
            "nonnegative before the affine PMI may consume it.",
            parent_id=parent.id,
            proof_sketch=(
                "Formalize the strict parameter-domain side condition and keep "
                "the per-cell witness separate from all-cell coverage. Reject "
                "state-dependent lambda and any ledger row marked inadmissible."),
            metadata=metadata,
        )
        state.event(
            "routeb_fixed_cell_lambda_contract_added",
            node_id=node_id,
            parent_id=parent.id,
            registry_promoted=False,
            formal_certificate_allowed=False,
        )
        store.save(state)
        print({"status": "recorded", "node_id": node_id, "state_revision": state.revision})
        return 0
    changed = False
    if existing.parent_id != parent.id:
        existing.parent_id = parent.id
        changed = True
    for key, value in metadata.items():
        if existing.metadata.get(key) != value:
            existing.metadata[key] = value
            changed = True
    if changed:
        state.event(
            "routeb_fixed_cell_lambda_contract_refresh",
            node_id=existing.id,
            parent_id=parent.id,
            registry_promoted=False,
            formal_certificate_allowed=False,
        )
        store.save(state)
        print({"status": "refreshed", "node_id": existing.id, "state_revision": state.revision})
    else:
        print({"status": "already_recorded", "node_id": existing.id, "state_revision": state.revision})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
