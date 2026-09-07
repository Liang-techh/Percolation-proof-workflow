"""Record local O1 intake and O2 namespace hardening without promotion."""
from __future__ import annotations

from pathlib import Path
import sys
import hashlib

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from percolation_workflow.store import StateStore  # noqa: E402


STATE = ROOT / "artifacts" / "routeb_6dof" / "state.json"
O1_RECEIPT = ROOT / "artifacts" / "task_routeb_o1_true_dh_exact_typed_mdd_source_v2_20260907" / "RECEIPT.json"


def find(state, name: str):
    for node in state.nodes.values():
        if node.name == name:
            return node
    raise ValueError(f"missing node: {name}")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def main() -> None:
    store = StateStore(STATE)
    state = store.load()
    if not O1_RECEIPT.is_file():
        raise FileNotFoundError(O1_RECEIPT)
    o1 = find(state, "P4.true_dh_exact_real_coefficient_identity")
    o2 = find(state, "P4.true_dh_float64_evaluator_enclosure")
    o1_entry = {
        "status": "CONDITIONAL_TYPED_SOURCE_INTAKE_VALIDATOR",
        "schema": "routeb.o1.true_dh_exact_typed_mdd_source.v2",
        "validator": "src/percolation_workflow/routeb_o1_source_receipt.py",
        "source_binding_required": True,
        "source_binding_paths": ["h_source_mass", "h_aggregate_and_h_body"],
        "mu_exact": "1/1000000",
        "registry_promoted": False,
        "formal_certificate_allowed": False,
        "receipt_path": str(O1_RECEIPT.resolve()),
        "receipt_sha256": sha256(O1_RECEIPT),
        "source_binding_proven": False,
        "artifact_binding_validator": "src/percolation_workflow/routeb_o1_source_receipt.py",
        "hash_only_metadata_pending": True,
    }
    o2_entry = {
        "status": "FAIL_CLOSED_THETA2_NAMESPACE_GATE",
        "validator": "src/percolation_workflow/coverage_receipt.py",
        "schema": "routeb-theta2-canonical-coverage-v1",
        "namespace": "theta2",
        "q2_anchor": {"lo": "-3/20", "hi": "3/20"},
        "parent_q2_subset_required": True,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    changed = False
    for node, key, entry in ((o1, "o1_source_receipt_validator", o1_entry),
                             (o2, "o2_theta2_namespace_gate", o2_entry)):
        if node.metadata.get(key) != entry:
            node.metadata[key] = entry
            changed = True
    if changed:
        state.event(
            "routeb_o1_intake_o2_namespace_hardening",
            o1_schema=o1_entry["schema"],
            o1_binding_required=True,
            o2_schema=o2_entry["schema"],
            o2_theta2_q2_anchor=o2_entry["q2_anchor"],
            registry_promoted=False,
            formal_certificate_allowed=False,
        )
        state.validate()
        store.save(state)
    print({"status": "recorded" if changed else "already_recorded", "revision": store.load().revision})


if __name__ == "__main__":
    main()
