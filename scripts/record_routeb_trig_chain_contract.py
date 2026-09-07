"""Attach the P3 DH exact-real trig-chain contract to the O2 frontier.

This recorder deliberately treats the external CSV as conditional exact-real
evidence.  It does not promote a theorem, bind Julia Float64/libm calls, or
change either the formal-certificate gate or the verified registry.
"""
from __future__ import annotations

import csv
import hashlib
import json
from fractions import Fraction
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ROUTE_B = ROOT.parent / "6dof_sos_optimized" / "6dof_sos_optimized"
REPORT = ROUTE_B / "routeB_dense_Mq" / "P3_DH_TRIG_CHAIN_CONTRACT.md"
SOURCE = ROUTE_B / "routeB_dense_Mq" / "routeB_p3_dh_trig_chain_contract.csv"
STATE = ROOT / "artifacts/routeb_6dof/state.json"
sys.path.insert(0, str(ROOT / "src"))

from percolation_workflow.store import StateStore  # noqa: E402


REQUIRED_COLUMNS = {
    "link", "atom", "phase_k", "q_lower_num", "q_lower_den",
    "q_upper_num", "q_upper_den", "center_sin_num", "center_sin_den",
    "center_cos_num", "center_cos_den", "reduced_lower_num",
    "reduced_lower_den", "reduced_upper_num", "reduced_upper_den",
    "sin_lower_num", "sin_lower_den", "sin_upper_num", "sin_upper_den",
    "cos_lower_num", "cos_lower_den", "cos_upper_num", "cos_upper_den",
}


def ref(path: Path) -> dict[str, str]:
    return {"path": str(path.resolve()),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest().upper()}


def find(state, name: str):
    for node in state.nodes.values():
        if node.name == name:
            return node
    raise ValueError(f"missing node: {name}")


def rational(row: dict[str, str], prefix: str) -> Fraction:
    return Fraction(int(row[f"{prefix}_num"]), int(row[f"{prefix}_den"]))


def main() -> int:
    for path in (REPORT, SOURCE):
        if not path.is_file():
            raise FileNotFoundError(path)

    report_text = REPORT.read_text(encoding="utf-8", errors="replace")
    required_phrases = (
        "interpreted over `ℝ`",
        "rational `pi` enclosure",
        "order-12 Taylor leaf",
        "does not prove Julia's `Float64`",
        "EXACT_REAL_CONTRACT_PLUS_CONDITIONAL_FLOAT64_BINDING_REQUIRED",
    )
    if not all(phrase in report_text for phrase in required_phrases):
        raise ValueError("P3 report does not preserve its evidence boundary")

    with SOURCE.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    if len(rows) != 12 or not rows:
        raise ValueError(f"expected 12 P3 rows, got {len(rows)}")
    if set(rows[0]) != REQUIRED_COLUMNS:
        raise ValueError("P3 CSV schema changed or is incomplete")
    if sorted({row["link"] for row in rows}) != [str(i) for i in range(1, 7)]:
        raise ValueError("P3 CSV must cover links 1..6")
    if {row["atom"] for row in rows} != {"theta", "alpha"}:
        raise ValueError("P3 CSV must contain theta and alpha rows")

    # Re-check the cheap exact invariants that distinguish this artifact from
    # an untyped numeric table.  Every endpoint and center entry is a rational,
    # and the local q box is exactly [-3/20, 3/20].
    endpoint_prefixes = (
        "q_lower", "q_upper", "reduced_lower", "reduced_upper",
        "sin_lower", "sin_upper", "cos_lower", "cos_upper",
    )
    for row in rows:
        for prefix in endpoint_prefixes:
            rational(row, prefix)
        rational(row, "center_sin")
        rational(row, "center_cos")
        expected_box = (Fraction(-3, 20), Fraction(3, 20))
        if row["atom"] == "alpha":
            # alpha is a fixed DH constant; its q column is the degenerate
            # zero input used by the external contract.
            expected_box = (Fraction(0), Fraction(0))
        if rational(row, "q_lower") != expected_box[0]:
            raise ValueError("unexpected lower q bound")
        if rational(row, "q_upper") != expected_box[1]:
            raise ValueError("unexpected upper q bound")
        if rational(row, "sin_lower") > rational(row, "sin_upper"):
            raise ValueError("sin interval is reversed")
        if rational(row, "cos_lower") > rational(row, "cos_upper"):
            raise ValueError("cos interval is reversed")

    audit = {
        "schema_version": 1,
        "status": "EXACT_REAL_DH_TRIG_CHAIN_CONTRACT_FLOAT64_BINDING_OPEN",
        "coverage": {
            "links": 6,
            "rows": len(rows),
            "atoms": ["theta", "alpha"],
            "input_partition": {
                "theta": "q_i in [-3/20, 3/20]",
                "alpha": "singleton q=0 (fixed DH offset)",
            },
            "endpoint_encoding": "integer numerator/denominator pairs",
        },
        "source_artifacts": [ref(REPORT), ref(SOURCE)],
        "claims": {
            "exact_real_phase_and_center_bookkeeping": True,
            "conditional_exact_real_interval_rows": True,
            "order_12_taylor_leaf_reused": True,
            "float64_pi_and_argument_rounding_bound": False,
            "float64_sin_cos_libm_bound": False,
            "finite_operation_propagation": False,
            "formal_certificate_allowed": False,
            "registry_promoted": False,
        },
        "remaining_obligations": [
            "bind Float64 pi/2 and argument formation to each certified angle box",
            "prove the deployed Float64/libm sin and cos enclosure",
            "propagate all finite operations through the DH evaluator",
            "compose per-box coverage with the O2 evaluator and residual leaves",
        ],
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }

    artifact_refs = [ref(REPORT), ref(SOURCE)]
    binding = {
        "schema_version": 1,
        "task_id": "T-P4-036",
        "target_node": "P4.true_dh_float64_evaluator_enclosure",
        "status": "OPEN_P3_CONDITIONAL_INPUT_ONLY",
        "input_contract": {
            "metadata_key": "trig_chain_contract",
            "contract_id": "routeb-p3-trig-dh-chain-contract/v1",
            "required_status": audit["status"],
            "artifact_hashes": [item["sha256"] for item in artifact_refs],
        },
        "leaves": [
            {"id": "T-P4-036.1", "kind": "pi_over_two_and_angle_formation_rounding", "status": "OPEN"},
            {"id": "T-P4-036.2", "kind": "argument_range_reduction", "status": "OPEN"},
            {"id": "T-P4-036.3", "kind": "float64_libm_sin_cos_enclosure", "status": "OPEN"},
            {"id": "T-P4-036.4", "kind": "finite_dh_operation_propagation", "status": "OPEN"},
        ],
        "composition_gate": {
            "required_leaf_ids": [f"T-P4-036.{i}" for i in range(1, 5)],
            "all_required": True,
            "per_box_coverage_required": True,
            "status": "OPEN",
        },
        "source_binding": {
            "angle_formulas": {
                "theta": "q[ii] + DH[ii,1]",
                "alpha": "DH[ii,4]",
            },
            "theta_phase_k_by_link": [0, -1, 1, 0, 0, 0],
            "alpha_phase_k_by_link": [-1, 0, 1, -1, 1, 0],
            "open_obligation_counts": {
                "angle_formation_inclusion": 12,
                "range_reduction_inclusion": 12,
                "libm_sin_cos_enclosure": 12,
                "finite_link_dag_propagation": 6,
            },
            "interface_targets": [
                "RouteB.P3.DHThetaPhaseContract",
                "RouteB.P3.DHAlphaPhaseContract",
                "RouteB.P3.ExactRealTrigRangeReductionLeaf",
                "RouteB.P3.Float64AngleFormationInclusion",
                "RouteB.P3.Float64LibmSinCosEnclosure",
                "RouteB.P3.DHLinkFiniteDAGEnclosure",
                "RouteB.P3.DHChainFloat64EvaluatorEnclosure",
            ],
        },
        "interface_layers": [
            {
                "id": "A_exact_real_interval_range_reduction",
                "status": "INTERFACE_DRAFT__UNCOMPILED",
                "theorems": [
                    "RouteB.P3.ExactRealTrigRangeReductionLeaf",
                    "RouteB.P3.ExactSinCosCellSound",
                ],
                "uses_machine_float": False,
            },
            {
                "id": "B_float64_argument_binding",
                "status": "OPEN",
                "theorems": ["RouteB.P3.Float64AngleFormationInclusion"],
                "requires": ["runtime/source pin", "binary64 decode", "addition-rounding bound"],
            },
            {
                "id": "C_libm_enclosure",
                "status": "OPEN",
                "theorems": ["RouteB.P3.Float64LibmSinCosEnclosure"],
                "requires": ["pinned runtime/libm", "finite/non-NaN assumptions", "actual call trace"],
            },
            {
                "id": "D_finite_dh_propagation",
                "status": "OPEN",
                "theorems": [
                    "RouteB.P3.DHLinkFiniteDAGEnclosure",
                    "RouteB.P3.DHChainFloat64EvaluatorEnclosure",
                ],
                "requires": ["layers B/C", "operation schedule", "per-box coverage"],
            },
        ],
        "formal_certificate_allowed": False,
        "registry_eligible": False,
        "registry_promoted": False,
    }

    store = StateStore(STATE)
    state = store.load()
    node = find(state, "P4.true_dh_float64_evaluator_enclosure")
    changed = node.metadata.get("trig_chain_contract") != audit
    node.metadata["trig_chain_contract"] = audit
    if node.metadata.get("o2_trig_binding") != binding:
        node.metadata["o2_trig_binding"] = binding
        changed = True
    unresolved = list(node.metadata.get("unresolved", []))
    for marker in (
        "dh_trig_chain_float64_argument_binding",
        "dh_trig_chain_libm_enclosure",
    ):
        if marker not in unresolved:
            unresolved.append(marker)
            changed = True
    node.metadata["unresolved"] = unresolved
    if changed:
        state.event(
            "routeb_p3_trig_chain_contract_recorded",
            node_id=node.id,
            status=audit["status"],
            rows=len(rows),
            registry_promoted=False,
            formal_certificate_allowed=False,
        )
        state.validate()
        store.save(state)
    print({
        "status": "recorded" if changed else "already_recorded",
        "audit_status": audit["status"],
        "rows": len(rows),
        "state_revision": store.load().revision,
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
