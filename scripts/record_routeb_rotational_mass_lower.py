"""Record the exact rotational-prefix mass lower-bound candidate."""
from __future__ import annotations

import csv
import hashlib
from fractions import Fraction
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ROUTE_B = ROOT.parent / "6dof_sos_optimized" / "6dof_sos_optimized"
SOURCE = ROUTE_B / "routeB_dense_Mq"
ROBOT_FINAL = ROUTE_B / "robot_final"
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


def main() -> int:
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    parent = find(state, "P3.strict_true_dh_bounds")
    name = "P3.rotational_prefix_mass_lower_bound"
    csv_path = SOURCE / "routeB_compact_rotational_mass_lower_certificate.csv"
    metrics = read_metrics(csv_path)
    expected = {
        "candidate_mu": "47/5000",
        "regularized_mass_lower": "9401/1000000",
        "prefix_matrix_dimension": "6",
        "rotational_lower_certified": "True",
        "q_dependence": "none",
        "formal_certificate_allowed": "False",
    }
    mismatches = [key for key, value in expected.items()
                  if metrics.get(key) != value]
    if mismatches:
        raise ValueError(f"rotational mass metrics mismatch: {mismatches}")
    minors = [Fraction(item) for item in
              metrics.get("leading_principal_minors", "").split(";")]
    if len(minors) != 6 or any(item <= 0 for item in minors):
        raise ValueError("rotational prefix minors are not strictly positive")
    paths = [
        csv_path,
        SOURCE / "P5_COMPACT_ROTATIONAL_MASS_LOWER_CERTIFICATE_CHECK.md",
        ROBOT_FINAL / "verify_compact_rotational_mass_lower_certificate.py",
        ROBOT_FINAL / "P4_ROTATIONAL_COERCIVITY_CERTIFICATE.md",
    ]
    source_artifacts = [ref(path) for path in paths if path.is_file()]
    metadata = {
        "verification_domain": "exact-rational-structural-source-candidate",
        "statement_status": "exact_checker_candidate_pending_lean_and_source_review",
        "evidence_level": "exact_prefix_gram_checker",
        "claim_status": "uniform_rotational_mass_lower_bound_open",
        "registry_eligible": False,
        "comparator_accepted": False,
        "formal_certificate_allowed": False,
        "physical_certificate_allowed": False,
        "source_artifacts": source_artifacts,
        "metrics": metrics,
        "derived_contract": {
            "candidate_mu": "47/5000",
            "regularized_mass_lower": "9401/1000000",
            "q_dependence": "none",
            "mechanism": "isotropic link inertia plus unit DH-axis prefix map",
            "matrix_dimension": 6,
            "leading_principal_minors_count": 6,
        },
        "unresolved": [
            "Lean_kernel_formalization_of_prefix_Gram_argument",
            "exact_DH_axis_orthogonality_source_binding",
            "Float64_and_libm_rounding_enclosure",
            "translation_mass_and_full_M_source_semantics",
            "P3_domain_and_flowpipe_coverage",
            "coordinator_statement_and_comparator_receipt",
        ],
    }
    existing = next((n for n in state.nodes.values() if n.name == name), None)
    if existing is None:
        node_id = state.add_node(
            name,
            "The recorded isotropic-link rotational prefix Gram gives a "
            "q-independent regularized mass lower bound 9401/1000000.",
            parent_id=parent.id,
            dependencies=[],
            proof_sketch=(
                "Use omega-prefix increments and exact unit-axis semantics to "
                "reduce rotational mass to a rational 6x6 Gram; prove all six "
                "leading principal minors positive and add the diagonal "
                "regularizer. Keep source semantics and Lean lift separate."),
            metadata=metadata,
        )
        state.event(
            "routeb_rotational_mass_lower_candidate_recorded",
            node_id=node_id,
            parent_id=parent.id,
            source_artifacts=source_artifacts,
            regularized_mass_lower="9401/1000000",
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
            "routeb_rotational_mass_lower_candidate_refresh",
            node_id=existing.id,
            parent_id=parent.id,
            source_artifacts=source_artifacts,
            regularized_mass_lower="9401/1000000",
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
