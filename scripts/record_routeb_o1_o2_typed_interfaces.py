"""Record the newest O1/O2 typed interfaces without theorem admission."""
from __future__ import annotations

from hashlib import sha256
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from percolation_workflow.store import StateStore  # noqa: E402


STATE = ROOT / "artifacts/routeb_6dof/state.json"
O1_RECEIPT = ROOT / "examples/routeb_b45_source_comparator_lean/O1_PER_BODY_COMPARATOR_RECEIPT.json"
O2_SCHEMA = ROOT / "artifacts/routeb_theta2_leaf_handoff_20260907/routeb-theta2-external-premises-v1.schema.json"
O2_LEAN = ROOT / "artifacts/routeb_theta2_leaf_handoff_20260907/Theta2ExternalPremisesAdapter.lean"
O2_VALIDATOR = ROOT / "src/percolation_workflow/coverage_receipt.py"
O2_NODE = "P4.true_dh_float64_evaluator_enclosure"
O1_PARENT = "P4.true_dh_exact_real_coefficient_identity"


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest().upper()


def find(state, name: str):
    for node in state.nodes.values():
        if node.name == name:
            return node
    raise ValueError(f"missing node: {name}")


def main() -> None:
    for path in (STATE, O1_RECEIPT, O2_SCHEMA, O2_LEAN, O2_VALIDATOR):
        if not path.is_file():
            raise FileNotFoundError(path)
    store = StateStore(STATE)
    state = store.load()
    o1_parent = find(state, O1_PARENT)
    o2 = find(state, O2_NODE)
    o1_entry = {
        "status": "OPEN_MISSING_FOURIER_BODY_DEFINITION_AND_HBODY",
        "receipt_sha256": digest(O1_RECEIPT),
        "candidate_compile_status": "UNCOMPILED_CANDIDATE",
        "per_body_source_definition_present": True,
        "h_body_typed_premise_only": True,
        "real_cos_sin_lift_minimal_lemma_uncompiled": True,
        "source_binding_proven": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    o2_entry = {
        "status": "EXTERNAL_PREMISE_SCHEMA_READY_REAL_TRIPLE_OPEN",
        "schema_path": str(O2_SCHEMA.resolve()),
        "schema_sha256": digest(O2_SCHEMA),
        "lean_adapter_path": str(O2_LEAN.resolve()),
        "lean_adapter_sha256": digest(O2_LEAN),
        "python_validator_path": str(O2_VALIDATOR.resolve()),
        "python_validator_sha256": digest(O2_VALIDATOR),
        "path_hash_recomputation": True,
        "namespace": "theta2",
        "source_interval_membership_explicit_input": True,
        "coverage_join2_explicit_input": True,
        "real_triple_instance_present": False,
        "lean_adapter_compiled": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    changed = False
    prior = list(o1_parent.metadata.get("o1_per_body_comparator_receipts", []))
    if o1_entry not in prior:
        prior.append(o1_entry)
        o1_parent.metadata["o1_per_body_comparator_receipts"] = prior
        changed = True
    prior = list(o2.metadata.get("o2_external_premise_typed_interfaces", []))
    if o2_entry not in prior:
        prior.append(o2_entry)
        o2.metadata["o2_external_premise_typed_interfaces"] = prior
        changed = True
    if changed:
        state.event(
            "routeb_o1_o2_typed_interfaces_recorded",
            o1_status=o1_entry["status"],
            o1_source_binding_proven=False,
            o2_status=o2_entry["status"],
            o2_real_triple_instance_present=False,
            o2_lean_adapter_compiled=False,
            registry_promoted=False,
            formal_certificate_allowed=False,
        )
        state.validate()
        store.save(state)
    print({"status": "recorded" if changed else "already_recorded", "revision": store.load().revision})


if __name__ == "__main__":
    main()
