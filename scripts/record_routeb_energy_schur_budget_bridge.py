"""Record the exact energy-to-Schur budget bridge candidate."""
from __future__ import annotations

import csv
from decimal import Decimal
import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ROUTE_B = ROOT.parent / "6dof_sos_optimized" / "6dof_sos_optimized"
SRC = ROUTE_B / "routeB_dense_Mq"
FINAL = ROUTE_B / "robot_final"
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


def read_metrics(path: Path) -> dict[str, str]:
    with path.open(newline="", encoding="utf-8") as handle:
        return {row["metric"]: row["value"] for row in csv.DictReader(handle)}


def normalize_fraction(value: str) -> str:
    return value.replace("//", "/")


def main() -> int:
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    parent = find(state, "M4.block45_full_certificate")
    name = "M4.energy_to_schur_budget_bridge"
    csv_path = SRC / "routeB_compact_energy_schur_budget_bridge.csv"
    metrics = read_metrics(csv_path)
    expected = {
        "status": "ENERGY_SCHUR_BUDGET_BRIDGE",
        "geometry_threshold_matches_required": "True",
        "geometry_cells_certified": "81",
        "full_2x2_determinant": "0",
        "full_2x2_metric_psd": "True",
        "conditional_terminal_p_bound": "12",
        "conditional_terminal_target_met": "True",
        "scalar_tube_budget_closes": "False",
        "unit_supply_tube_budget_closes": "False",
        "q1_q6_dynamic_coverage": "open",
        "residual_flowpipe_closure": "False",
        "finite_time_terminal_budget_closed": "False",
        "formal_certificate_allowed": "False",
    }
    mismatches = [key for key, value in expected.items()
                  if metrics.get(key) != value]
    if mismatches:
        raise ValueError(f"energy Schur metrics mismatch: {mismatches}")
    if normalize_fraction(metrics["geometry_schur_threshold"]) != normalize_fraction(
            metrics["required_schur_threshold"]):
        raise ValueError("geometry and required Schur thresholds differ")
    if Decimal(metrics["geometry_min_pivot_lower"]) <= 0:
        raise ValueError("geometry minimum pivot is not positive")
    paths = [
        csv_path,
        SRC / "P5_COMPACT_ENERGY_SCHUR_BUDGET_BRIDGE.md",
        SRC / "routeB_compact_energy_schur_budget_bridge.py",
        FINAL / "verify_compact_energy_schur_budget_bridge.py",
    ]
    source_artifacts = [ref(path) for path in paths if path.is_file()]
    metadata = {
        "verification_domain": "exact-rational-conditional-energy-schur-candidate",
        "statement_status": "conditional_terminal_bridge_pending_source_energy_and_flowpipe",
        "evidence_level": "exact_checker_composed_geometry_budget",
        "claim_status": "conditional_m4_terminal_bridge_open",
        "registry_eligible": False,
        "comparator_accepted": False,
        "formal_certificate_allowed": False,
        "physical_certificate_allowed": False,
        "source_artifacts": source_artifacts,
        "metrics": metrics,
        "contract": {
            "geometry_cells": 81,
            "threshold": metrics["required_schur_threshold"],
            "metric_psd": True,
            "conditional_terminal_p_bound": "12",
            "premises_still_required": [
                "energy_inequality",
                "initial_bound",
                "q1_q6_dynamic_coverage",
                "residual_absorption",
                "flowpipe_inclusion",
            ],
        },
        "unresolved": [
            "source_energy_inequality_and_initial_storage_binding",
            "q1_q6_dynamic_and_full_flowpipe_coverage",
            "residual_absorption_and_terminal_transfer_semantics",
            "Lean_kernel_formalization_of_exact_2x2_metric_bridge",
            "coordinator_statement_and_comparator_receipt",
        ],
    }
    existing = next((n for n in state.nodes.values() if n.name == name), None)
    if existing is None:
        node_id = state.add_node(
            name,
            "The exact global mass-geometry Schur threshold composes with "
            "the 2x2 storage/output metric to give the conditional terminal "
            "bound p45 <= 12.",
            parent_id=parent.id,
            dependencies=[],
            proof_sketch=(
                "Check equality of geometry and required thresholds, verify "
                "the exact 2x2 PSD determinant and consume the conditional "
                "energy tube; retain dynamic and residual premises explicitly."),
            metadata=metadata,
        )
        state.event(
            "routeb_energy_schur_budget_bridge_recorded",
            node_id=node_id,
            parent_id=parent.id,
            source_artifacts=source_artifacts,
            threshold=metrics["required_schur_threshold"],
            conditional_terminal_p_bound=12,
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
            "routeb_energy_schur_budget_bridge_refresh",
            node_id=existing.id,
            parent_id=parent.id,
            source_artifacts=source_artifacts,
            threshold=metrics["required_schur_threshold"],
            conditional_terminal_p_bound=12,
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
