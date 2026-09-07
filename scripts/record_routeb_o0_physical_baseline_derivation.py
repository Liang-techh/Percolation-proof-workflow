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
REVIEW = ROOT / "agent_review_inbox/review-T-P4-033-O0-exact-physical-baseline-derivation-20260907.md"


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest().upper()


def find(state, name: str):
    for node in state.nodes.values():
        if node.name == name:
            return node
    raise ValueError(f"missing node: {name}")


def main() -> None:
    for path in (STATE, RECEIPT, REVIEW):
        if not path.is_file():
            raise FileNotFoundError(path)
    store = StateStore(STATE)
    state = store.load()
    node = find(state, "P4.true_dh_exact_real_coefficient_identity")
    entry = {
        "status": "CONDITIONAL_EXACT_SAME_KEY_BASELINE_DERIVATION",
        "receipt_path": str(RECEIPT.resolve()),
        "receipt_sha256": digest(RECEIPT),
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
    changed = entry not in prior
    if changed:
        prior.append(entry)
        node.metadata["o0_physical_baseline_derivations"] = prior
        node.metadata["o0_physical_baseline_derivation"] = entry
        state.event(
            "routeb_o0_physical_baseline_derivation",
            status=entry["status"],
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
