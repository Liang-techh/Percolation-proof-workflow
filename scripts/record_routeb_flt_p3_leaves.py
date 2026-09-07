"""Ingest independently compiled FLT-derived P3 calculus leaves.

The artifacts live in the external Route-B workspace and are recorded by
reference only.  This script never promotes them to the verified registry:
they close abstract calculus seams, not concrete DH/rounding/coverage.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ROUTE_B = ROOT.parent / "6dof_sos_optimized" / "6dof_sos_optimized"
ARTIFACT_ROOT = ROUTE_B / "artifacts"
sys.path.insert(0, str(ROOT / "src"))

from percolation_workflow.store import StateStore


def file_ref(path: Path) -> dict[str, str]:
    return {
        "path": str(path.resolve()),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def find(state, name: str):
    for node in state.nodes.values():
        if node.name == name:
            return node
    raise ValueError(f"missing node: {name}")


def load_artifact(name: str) -> tuple[Path, dict, list[dict[str, str]]]:
    root = ARTIFACT_ROOT / name
    contract_path = root / "contract.json"
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    files = [contract_path]
    for candidate in (
        root / next((p.name for p in root.glob("*.lean")), ""),
        root / "AxiomAudit.lean",
        root / "VERIFICATION.md",
        root / "PINNED_ENVIRONMENT.md",
        root / "AUDIT.md",
        root / "README.md",
    ):
        if candidate.is_file() and candidate not in files:
            files.append(candidate)
    return root, contract, [file_ref(path) for path in files]


def ensure_child(state, parent, name: str, statement: str, sketch: str,
                 contract_name: str, source_files: list[dict[str, str]],
                 contract: dict) -> tuple[str, bool]:
    metadata = {
        "verification_domain": "lean-verified-abstract-external-artifact",
        "statement_status": "lean_verified_abstract_candidate",
        "evidence_level": "independently_compiled_external_artifact",
        "claim_status": "abstract_p3_child_open",
        "registry_eligible": False,
        "comparator_accepted": False,
        "formal_certificate_allowed": False,
        "physical_certificate_allowed": False,
        "external_artifact": contract_name,
        "external_artifact_contract": contract,
        "source_artifacts": source_files,
        "provenance_status": "reference_only_no_copy_no_source_mutation",
        "unresolved": [
            "concrete_six_joint_DH_instantiation",
            "operation_DAG_or_rounding_binding",
            "concrete_interval_payload_and_partition_coverage",
            "ODE_flowpipe_and_terminal_transfer",
            "coordinator_statement_identity_and_comparator_receipt",
        ],
    }
    existing = next((n for n in state.nodes.values() if n.name == name), None)
    if existing is None:
        node_id = state.add_node(
            name,
            statement,
            parent_id=parent.id,
            dependencies=[],
            proof_sketch=sketch,
            metadata=metadata,
        )
        state.event(
            "routeb_flt_p3_abstract_leaf_recorded",
            node_id=node_id,
            parent_id=parent.id,
            external_artifact=contract_name,
            theorem_contract=contract.get("theorems", {}),
            source_artifacts=source_files,
            status="lean_verified_abstract_candidate",
            formal_certificate_allowed=False,
            registry_promoted=False,
        )
        return node_id, True

    changed = False
    for key, value in metadata.items():
        if existing.metadata.get(key) != value:
            existing.metadata[key] = value
            changed = True
    if existing.parent_id != parent.id:
        existing.parent_id = parent.id
        changed = True
    return existing.id, changed


def main() -> int:
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    parent = find(state, "P3.strict_true_dh_bounds")
    specs = [
        (
            "task_FLT_routeb_derivative_leaf_20260908",
            "P3.true_dh_derivative_hull_leaf",
            "The exact-real Frechet chain-rule and convex derivative-hull leaf "
            "for a coordinate-changed true-DH map.",
            "Consume the abstract HasFDerivAt composition and convex remainder "
            "bound; keep concrete DH, rounding, and coverage as separate leaves.",
        ),
        (
            "task_FLT_p3_source_binding_20260908",
            "P3.central_fd_derivative_hull_composition",
            "The exact-real central finite-difference to derivative-hull bridge "
            "and three-term rational interval error composition.",
            "Use the convex secant estimate, then add exported-radius, machine "
            "rounding, and derivative-hull terms exactly once.",
        ),
    ]
    results = []
    changed_any = False
    for artifact_name, node_name, statement, sketch in specs:
        _, contract, source_files = load_artifact(artifact_name)
        node_id, changed = ensure_child(
            state, parent, node_name, statement, sketch,
            artifact_name, source_files, contract)
        results.append({"name": node_name, "node_id": node_id,
                        "changed": changed})
        changed_any = changed_any or changed

    if changed_any:
        state.event(
            "routeb_flt_p3_abstract_leaf_catalog_refresh",
            parent_id=parent.id,
            children=[item["node_id"] for item in results],
            status="lean_verified_abstract_candidate",
            formal_certificate_allowed=False,
            registry_promoted=False,
        )
        store.save(state)
    print({"status": "recorded" if changed_any else "already_recorded",
           "children": results, "state_revision": state.revision})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
