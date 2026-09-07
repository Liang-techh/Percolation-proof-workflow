"""Record the independently compiled exact-real trigonometric interval leaf."""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = (ROOT.parent / "6dof_sos_optimized" / "6dof_sos_optimized"
            / "artifacts" / "task_FLT_trig_lean_leaf_20260908")
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
    parent = find(state, "P3.strict_true_dh_bounds")
    name = "P3.trig_endpoint_enclosure_leaf"
    files = [
        ARTIFACT / "FLT_TrigIntervalLeaf.lean",
        ARTIFACT / "AxiomAudit.lean",
        ARTIFACT / "REPORT.md",
        ARTIFACT / "RECEIPT.md",
    ]
    source_artifacts = [ref(path) for path in files if path.is_file()]
    theorem_names = [
        "FLTTrigIntervalLeaf.increasing_endpoint_enclosure",
        "FLTTrigIntervalLeaf.decreasing_endpoint_enclosure",
        "FLTTrigIntervalLeaf.sin_enclosure_of_directed_endpoints",
        "FLTTrigIntervalLeaf.cos_enclosure_of_directed_endpoints",
        "FLTTrigIntervalLeaf.center_radius_enclosure",
    ]
    metadata = {
        "verification_domain": "lean-verified-abstract-external-artifact",
        "statement_status": "lean_verified_abstract_candidate",
        "evidence_level": "independently_compiled_external_artifact",
        "claim_status": "abstract_trigonometric_interval_leaf_open",
        "registry_eligible": False,
        "comparator_accepted": False,
        "formal_certificate_allowed": False,
        "physical_certificate_allowed": False,
        "external_artifact": "task_FLT_trig_lean_leaf_20260908",
        "source_artifacts": source_artifacts,
        "theorem_names": theorem_names,
        "pinned_receipt": {
            "lean_toolchain": "leanprover/lean4:v4.33.0",
            "mathlib_revision": "db584cd6d46c92f209a44c0f1c829460d327499d",
            "compile_status": "passed",
            "axiom_status": "standard_logic_only",
            "placeholder_scan": "passed",
        },
        "frontier_contract": {
            "input": "one-sided exact-real endpoint inequalities",
            "output": "sin/cos pointwise and center-radius enclosure",
            "turning_point_split_required": True,
            "not_proved": [
                "directed_evaluator_or_Julia_binding",
                "IEEE754_or_libm_rounding",
                "DH_expression_binding",
                "partition_coverage",
                "RouteB_certificate",
            ],
        },
        "unresolved": [
            "pinned_coordinator_statement_and_comparator_binding",
            "concrete_directed_endpoint_evaluator",
            "turning_point_cell_partition_coverage",
            "DH_source_and_rounding_binding",
        ],
    }
    existing = next((n for n in state.nodes.values() if n.name == name), None)
    if existing is None:
        node_id = state.add_node(
            name,
            "Exact-real monotonicity and endpoint-to-center-radius enclosure "
            "for sine and cosine on a monotonicity cell.",
            parent_id=parent.id,
            dependencies=[],
            proof_sketch=(
                "Use endpoint certificates and Mathlib monotonicity; require "
                "explicit turning-point partition and keep runtime rounding "
                "as a separate source-binding child."),
            metadata=metadata,
        )
        state.event(
            "routeb_flt_p3_trig_leaf_recorded",
            node_id=node_id,
            parent_id=parent.id,
            theorem_names=theorem_names,
            source_artifacts=source_artifacts,
            status="lean_verified_abstract_candidate",
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
            "routeb_flt_p3_trig_leaf_refresh",
            node_id=existing.id,
            parent_id=parent.id,
            theorem_names=theorem_names,
            source_artifacts=source_artifacts,
            status="lean_verified_abstract_candidate",
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
