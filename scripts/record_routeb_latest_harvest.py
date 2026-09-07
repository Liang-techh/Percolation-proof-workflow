"""Integrate the latest O0/O2 reviews without closing mathematical nodes."""
from __future__ import annotations

from hashlib import sha256
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from percolation_workflow.store import StateStore  # noqa: E402


STATE = ROOT / "artifacts/routeb_6dof/state.json"
O0_RECEIPT = ROOT / "agent_review_inbox/receipt-T-P4-033-O0-same-key-baseline-bias-search-obstruction-20260907.json"
O0_REVIEW = ROOT / "agent_review_inbox/review-T-P4-033-O0-same-key-baseline-bias-search-20260907.md"
O2_REVIEW = ROOT / "agent_review_inbox/review-T-P4-036.2-theta2-exporter-namespace-hash-binding-codex-20260907.md"
BRANCH = ROOT.parent / "6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq/routeB_interval_branch_bound.jl"


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest().upper()


def find(state, name: str):
    for node in state.nodes.values():
        if node.name == name:
            return node
    raise ValueError(f"missing node: {name}")


def main() -> None:
    for path in (STATE, O0_RECEIPT, O0_REVIEW, O2_REVIEW, BRANCH):
        if not path.is_file():
            raise FileNotFoundError(path)
    store = StateStore(STATE)
    state = store.load()
    o0 = find(state, "P4.true_dh_exact_real_coefficient_identity")
    o2 = find(state, "P4.true_dh_float64_evaluator_enclosure")
    o0_entry = {
        "status": "OBSTRUCTION",
        "disposition": "NO_STRICT_SCHUR_CONSUMABLE_SAME_KEY_BASELINE_OR_AFFINE_BIAS_RECEIPT",
        "receipt_sha256": digest(O0_RECEIPT),
        "review_sha256": digest(O0_REVIEW),
        "rejected_global_lower_as_L_base": "1/1000000",
        "same_key_L_base": False,
        "same_key_physical_residual": False,
        "schur_margin_consumed": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    o2_entry = {
        "status": "EXPORTER_NAMESPACE_AND_HASH_FILE_BOUND_REAL_TRIPLE_OPEN",
        "review_sha256": digest(O2_REVIEW),
        "branch_source_sha256": digest(BRANCH),
        "theta2_namespace_anchor": {"coordinate": "q2", "lo": "-3/20", "hi": "3/20"},
        "hash_file_binding": True,
        "real_triple_receipt_present": False,
        "external_premises_present": False,
        "global_coverage": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    changed = False
    for node, key, entry in (
        (o0, "o0_same_key_baseline_bias_search", o0_entry),
        (o2, "o2_namespace_hash_binding_reviews", o2_entry),
    ):
        prior = list(node.metadata.get(key, []))
        if entry not in prior:
            prior.append(entry)
            node.metadata[key] = prior
            changed = True
    if changed:
        state.event(
            "routeb_latest_o0_o2_harvest",
            o0_status=o0_entry["status"],
            o0_schur_margin_consumed=False,
            o2_status=o2_entry["status"],
            o2_real_triple_receipt_present=False,
            registry_promoted=False,
            formal_certificate_allowed=False,
        )
        state.validate()
        store.save(state)
    print({"status": "recorded" if changed else "already_recorded", "revision": store.load().revision})


if __name__ == "__main__":
    main()
