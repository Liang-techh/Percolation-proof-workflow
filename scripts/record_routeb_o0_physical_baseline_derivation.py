"""Record the O0 exact baseline derivation as a conditional child artifact."""
from __future__ import annotations

from hashlib import sha256
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from percolation_workflow.store import StateStore  # noqa: E402


STATE = ROOT / "artifacts/routeb_6dof/state.json"
RECEIPT = ROOT / "artifacts/routeb_6dof/o0_physical_baseline_derivation_20260907.json"
CHECK = ROOT / "artifacts/routeb_6dof/o0_physical_baseline_derivation_20260907.check.json"
REVIEW = ROOT / "agent_review_inbox/review-T-P4-033-O0-exact-physical-baseline-derivation-20260907.md"
LEDGER_RECEIPT = ROOT / "agent_review_inbox/receipt-T-P4-033-O0-physical-baseline-binding-ledger-20260907.json"
LEDGER_REVIEW = ROOT / "agent_review_inbox/review-T-P4-033-O0-physical-baseline-binding-ledger-20260907.md"


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest().upper()


def find(state, name: str):
    for node in state.nodes.values():
        if node.name == name:
            return node
    return None


def find_required(state, name: str):
    node = find(state, name)
    if node is None:
        raise ValueError(f"missing node: {name}")
    return node


def main() -> None:
    for path in (STATE, RECEIPT, CHECK, REVIEW, LEDGER_RECEIPT, LEDGER_REVIEW):
        if not path.is_file():
            raise FileNotFoundError(path)
    store = StateStore(STATE)
    state = store.load()
    node = find_required(state, "P4.true_dh_exact_real_coefficient_identity")
    residual_parent = find_required(
        state, "P4.true_dh_residual_map_coefficient_binding"
    )
    baseline_leaf = find(state, "P4.O0.physical_baseline_factor")
    leaf_added = False
    if baseline_leaf is None:
        baseline_leaf_id = state.add_node(
            "P4.O0.physical_baseline_factor",
            "Under the exact same source/state key, derive a physical baseline factor L_base from the M_BB mass lower bound and A_up metric upper bound.",
            parent_id=residual_parent.id,
            proof_sketch=(
                "Use the exact M_BB center and all-q enclosure, symmetry, and "
                "the weighted A_up comparison to derive L_base; keep every "
                "source/energy/residual binding premise explicit."
            ),
            metadata={
                "verification_domain": "external-research",
                "research_stage": "P4",
                "statement_status": "conditional_exact_baseline_derivation",
                "frontier_kind": "O0_physical_coercivity",
                "registry_eligible": False,
                "comparator_accepted": False,
                "source_binding_proven": False,
                "formal_certificate_allowed": False,
            },
        )
        baseline_leaf = state.nodes[baseline_leaf_id]
        leaf_added = True
    entry = {
        "status": "CONDITIONAL_EXACT_SAME_KEY_BASELINE_DERIVATION",
        "receipt_path": str(RECEIPT.resolve()),
        "receipt_sha256": digest(RECEIPT),
        "checker_path": str(CHECK.resolve()),
        "checker_sha256": digest(CHECK),
        "checker_status": "PASS_CONDITIONAL_FAIL_CLOSED",
        "binding_ledger_sha256": digest(LEDGER_RECEIPT),
        "binding_ledger_review_sha256": digest(LEDGER_REVIEW),
        "binding_ledger_status": "OBSTRUCTION_SAME_KEY_PHYSICAL_BINDINGS_INCOMPLETE",
        "review_sha256": digest(REVIEW),
        "L_base": "120442959/280443400",
        "mass_lower": "40147653/800000000",
        "metric_upper": "1402217/12000000",
        "baseline_bound_proven": False,
        "physical_energy_identity_proven": False,
        "physical_residual_binding_proven": False,
        "schur_margin_consumed": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    prior = list(node.metadata.get("o0_physical_baseline_derivations", []))
    changed = entry not in prior or leaf_added
    if changed:
        prior.append(entry)
        node.metadata["o0_physical_baseline_derivations"] = prior
        node.metadata["o0_physical_baseline_derivation"] = entry
        baseline_leaf.metadata["conditional_derivation_receipt"] = entry
        state.event(
            "routeb_o0_physical_baseline_derivation",
            status=entry["status"],
            baseline_leaf_id=baseline_leaf.id,
            L_base=entry["L_base"],
            baseline_bound_proven=False,
            physical_energy_identity_proven=False,
            schur_margin_consumed=False,
            registry_promoted=False,
            formal_certificate_allowed=False,
        )
        state.validate()
        store.save(state)
    print({"status": "recorded" if changed else "already_recorded", "revision": store.load().revision})


if __name__ == "__main__":
    main()
