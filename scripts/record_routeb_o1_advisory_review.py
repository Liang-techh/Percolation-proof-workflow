"""Attach an O1 Lean API repair review without claiming compilation."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "agent_review_inbox/review-T-P4-032-codex-20260907.md"
TASK = ROOT / "artifacts/task_routeb_o1_lean_api_audit_20260907"
STATE = ROOT / "artifacts/routeb_6dof/state.json"
sys.path.insert(0, str(ROOT / "src"))

from percolation_workflow.store import StateStore  # noqa: E402


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def ref(path: Path) -> dict[str, str]:
    return {"path": str(path.resolve()), "sha256": sha(path)}


def find(state, name: str):
    for node in state.nodes.values():
        if node.name == name:
            return node
    raise ValueError(f"missing node: {name}")


def main() -> int:
    candidate = TASK / "RouteBO1PortIdentity.lean"
    report = TASK / "REPORT.md"
    receipt = TASK / "RECEIPT.json"
    for path in (REVIEW, candidate, report, receipt):
        if not path.is_file():
            raise FileNotFoundError(path)
    review_text = REVIEW.read_text(encoding="utf-8", errors="replace")
    for phrase in (
        "ADVISORY_REPAIR_REQUIRED__UNCOMPILED",
        "Mathlib.Tactic.Linarith",
        "Matrix.mul_assoc",
        "h_inv_left",
        "not a kernel receipt",
    ):
        if phrase not in review_text:
            raise ValueError(f"O1 review boundary missing: {phrase}")
    receipt_data = json.loads(receipt.read_text(encoding="utf-8"))
    if receipt_data.get("status") != "UNCOMPILED__NON_VERIFIED":
        raise ValueError("O1 source receipt is not uncompiled")
    if b"sorry" in candidate.read_bytes().lower() or b"admit" in candidate.read_bytes().lower():
        raise ValueError("O1 candidate contains forbidden sorry/admit token")

    review = {
        "schema_version": 1,
        "task_id": "T-P4-032",
        "source_agent": "Codex",
        "review_status": "ADVISORY_REPAIR_REQUIRED__UNCOMPILED",
        "review_artifact": ref(REVIEW),
        "candidate_artifacts": [ref(candidate), ref(report), ref(receipt)],
        "repair_actions": [
            "import Mathlib.Tactic.Linarith",
            "normalize hB_left with Matrix.mul_assoc or right-associated product",
            "preserve explicit left inverse M_DD_inv * M_DD = 1",
        ],
        "formal_certificate_allowed": False,
        "registry_promoted": False,
        "admission_status": "pending_pinned_lean_compile",
    }
    store = StateStore(STATE)
    state = store.load()
    node = find(state, "P4.true_dh_exact_real_coefficient_identity")
    reviews = list(node.metadata.get("independent_static_reviews", []))
    changed = review not in reviews
    if changed:
        reviews.append(review)
        node.metadata["independent_static_reviews"] = reviews
    contract = dict(node.metadata.get("frontier_repair_contract") or {})
    repair = list(contract.get("advisory_repairs", []))
    for item in review["repair_actions"]:
        if item not in repair:
            repair.append(item)
    if contract.get("advisory_repairs") != repair:
        contract["advisory_repairs"] = repair
        contract["repair_status"] = "PENDING_PINNED_LEAN_COMPILE"
        node.metadata["frontier_repair_contract"] = contract
        changed = True
    if changed:
        state.event(
            "routeb_o1_advisory_repair_review_recorded",
            node_id=node.id,
            review_status=review["review_status"],
            admission_status=review["admission_status"],
            registry_promoted=False,
            formal_certificate_allowed=False,
        )
        state.validate()
        store.save(state)
    print({
        "status": "recorded" if changed else "already_recorded",
        "review_status": review["review_status"],
        "state_revision": store.load().revision,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
