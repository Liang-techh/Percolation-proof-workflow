"""Record the 81-cell block-(4,5) mass-geometry Schur candidate."""
from __future__ import annotations

import csv
import hashlib
from decimal import Decimal
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ROUTE_B = ROOT.parent / "6dof_sos_optimized" / "6dof_sos_optimized"
SRC = ROUTE_B / "routeB_dense_Mq"
FINAL = ROUTE_B / "robot_final"
sys.path.insert(0, str(ROOT / "src"))

from percolation_workflow.store import StateStore


THRESHOLD = "8228439564136788990170047498962311//245393314823307985274304000000000000"


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


def main() -> int:
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    parent = find(state, "P4.residual_schur_pmi")
    name = "P4.block45_global_mass_geometry_schur"
    csv_path = SRC / "routeB_compact_block_schur_global_geometry_interface.csv"
    metrics = read_metrics(csv_path)
    expected = {
        "status": "GLOBAL_GEOMETRY_SCHUR_INTERFACE",
        "active_angles": "q2;q3;q4;q5",
        "inactive_geometry_angles": "q1;q6",
        "domain": "q2:q5 in [-0.15,0.15]^4",
        "coverage_cells": "81",
        "certified_cells": "81",
        "required_block_schur_lower": THRESHOLD,
        "global_geometry_schur_certified": "True",
        "q1_q6_dynamic_coverage": "open",
        "finite_time_terminal_budget_closed": "False",
        "formal_certificate_allowed": "False",
    }
    mismatches = [key for key, value in expected.items()
                  if metrics.get(key) != value]
    if mismatches:
        raise ValueError(f"global geometry metrics mismatch: {mismatches}")
    if Decimal(metrics["minimum_pivot_lower"]) <= 0:
        raise ValueError("minimum pivot lower is not positive")
    paths = [
        csv_path,
        SRC / "P5_COMPACT_BLOCK_SCHUR_GLOBAL_GEOMETRY_INTERFACE.md",
        SRC / "P5_COMPACT_BLOCK_SCHUR_GLOBAL_GEOMETRY_INTERFACE_CHECK.md",
        SRC / "routeB_compact_block_schur_global_geometry_interface.py",
        FINAL / "verify_compact_block_schur_global_geometry_interface.py",
    ]
    source_artifacts = [ref(path) for path in paths if path.is_file()]
    metadata = {
        "verification_domain": "directed-interval-mass-geometry-candidate",
        "statement_status": "exact_threshold_81_cell_candidate_pending_lean_and_source_review",
        "evidence_level": "complete_mean_value_geometry_checker",
        "claim_status": "block45_global_mass_geometry_open",
        "registry_eligible": False,
        "comparator_accepted": False,
        "formal_certificate_allowed": False,
        "physical_certificate_allowed": False,
        "source_artifacts": source_artifacts,
        "metrics": metrics,
        "contract": {
            "domain": "q2:q5 in [-0.15,0.15]^4",
            "cells": 81,
            "statement": "M(q)-c*E45 PSD on every listed cell under recorded mass semantics",
            "threshold": THRESHOLD,
            "minimum_pivot_lower": metrics["minimum_pivot_lower"],
            "inactive_geometry_angles": ["q1", "q6"],
        },
        "unresolved": [
            "exact_DH_mass_source_and_directed_interval_semantics",
            "Lean_kernel_formalization_of_81_cell_ledger_or_certificates",
            "q1_q6_dynamic_and_flowpipe_coverage",
            "residual_absorption_and_terminal_budget_composition",
            "coordinator_statement_and_comparator_receipt",
        ],
    }
    existing = next((n for n in state.nodes.values() if n.name == name), None)
    if existing is None:
        node_id = state.add_node(
            name,
            "The recorded 81-cell mean-value mass ledger certifies the "
            "block-(4,5) Schur threshold on the declared q2:q5 angle box.",
            parent_id=parent.id,
            dependencies=[],
            proof_sketch=(
                "Validate every cell as CERTIFIED_CHOL at the exact terminal "
                "threshold, aggregate the minimum pivot, and keep q1/q6 "
                "dynamic coverage plus residual/flowpipe composition separate."),
            metadata=metadata,
        )
        state.event(
            "routeb_block45_global_geometry_candidate_recorded",
            node_id=node_id,
            parent_id=parent.id,
            source_artifacts=source_artifacts,
            threshold=THRESHOLD,
            coverage_cells=81,
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
            "routeb_block45_global_geometry_candidate_refresh",
            node_id=existing.id,
            parent_id=parent.id,
            source_artifacts=source_artifacts,
            threshold=THRESHOLD,
            coverage_cells=81,
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
