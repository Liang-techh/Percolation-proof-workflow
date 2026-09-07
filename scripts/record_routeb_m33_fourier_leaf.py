"""Record the exact M33 source-to-Fourier checker leaf."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = (ROOT.parent / "6dof_sos_optimized" / "6dof_sos_optimized"
            / "artifacts" / "task_routeb_source_fourier_binding_current")
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
    parent = find(state, "P3.strict_true_dh_bounds")
    name = "P3.m33_exact_fourier_source_leaf"
    contract_path = ARTIFACT / "CHECK_RESULT.json"
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    source_files = [
        ARTIFACT / "check_m33_source_fourier_binding.py",
        ARTIFACT / "m33_fourier_witness.csv",
        ARTIFACT / "CHECK_RESULT.json",
        ARTIFACT / "CHECKER_OUTPUT.txt",
        ARTIFACT / "REPORT.md",
        ARTIFACT / "README.md",
    ]
    source_artifacts = [ref(path) for path in source_files if path.is_file()]
    metadata = {
        "verification_domain": "exact-rational-executable-checker",
        "statement_status": "exact_checker_leaf_pending_formalization",
        "evidence_level": "exact_extensional_checker_pass",
        "claim_status": "concrete_m33_exact_formula_open",
        "registry_eligible": False,
        "comparator_accepted": False,
        "formal_certificate_allowed": False,
        "physical_certificate_allowed": False,
        "external_artifact": "task_routeb_source_fourier_binding_current",
        "source_artifacts": source_artifacts,
        "checker_contract": contract,
        "exactization": {
            "decimal_literals": "rational",
            "pi_over_2": "exact quarter turn",
            "coefficient_domain": "Gaussian rationals",
            "entry": "M33",
            "active_joint_angles": [4, 5],
            "support_size": 11,
        },
        "unresolved": [
            "Lean_kernel_formalization_of_the_11_mode_identity",
            "Julia_Float64_AST_and_libm_rounding_binding",
            "all_entry_mass_source_binding",
            "P3_partition_coverage_and_inverse_bounds",
            "coordinator_statement_and_comparator_receipt",
        ],
    }
    existing = next((n for n in state.nodes.values() if n.name == name), None)
    if existing is None:
        node_id = state.add_node(
            name,
            "The canonical exactized DH source entry M33 equals an explicit "
            "11-mode Fourier expression for every real joint configuration.",
            parent_id=parent.id,
            dependencies=[],
            proof_sketch=(
                "Parse the canonical source into a Gaussian-rational Laurent "
                "ring, compare all coefficients with the witness, and retain "
                "the exactization and Float64 gap as separate obligations."),
            metadata=metadata,
        )
        state.event(
            "routeb_m33_exact_fourier_leaf_recorded",
            node_id=node_id,
            parent_id=parent.id,
            source_artifacts=source_artifacts,
            exactization=metadata["exactization"],
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
            "routeb_m33_exact_fourier_leaf_refresh",
            node_id=existing.id,
            parent_id=parent.id,
            source_artifacts=source_artifacts,
            exactization=metadata["exactization"],
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
