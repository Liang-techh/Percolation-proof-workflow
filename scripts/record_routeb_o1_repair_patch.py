"""Record the local O1 API repair as pending remote Lean compilation."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "agent_review_inbox/review-T-P4-032-repair-20260907.md"
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
    for path in (REVIEW, candidate):
        if not path.is_file():
            raise FileNotFoundError(path)
    text = REVIEW.read_text(encoding="utf-8", errors="replace")
    for phrase in ("Mathlib.Tactic.Linarith", "Matrix.mul_assoc", "PENDING_LEAN_COMPILE"):
        if phrase not in text:
            raise ValueError(f"repair receipt missing: {phrase}")
    if "import Mathlib.Tactic.Linarith" not in candidate.read_text(encoding="utf-8"):
        raise ValueError("candidate is missing explicit Linarith import")
    if b"sorry" in candidate.read_bytes().lower() or b"admit" in candidate.read_bytes().lower():
        raise ValueError("candidate contains forbidden sorry/admit token")
    repair = {
        "schema_version": 1,
        "task_id": "T-P4-032",
        "status": "REPAIR_PATCHED__PENDING_LEAN_COMPILE",
        "review_artifact": ref(REVIEW),
        "candidate_artifact": ref(candidate),
        "actions": [
            "explicit Mathlib.Tactic.Linarith import",
            "Matrix.mul_assoc normalization in hB_left",
            "preserve explicit left inverse premise",
        ],
        "lean_compiled": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    store = StateStore(STATE)
    state = store.load()
    node = find(state, "P4.true_dh_exact_real_coefficient_identity")
    prior = list(node.metadata.get("repair_attempts", []))
    changed = repair not in prior
    if changed:
        prior.append(repair)
        node.metadata["repair_attempts"] = prior
    contract = dict(node.metadata.get("frontier_repair_contract") or {})
    contract["latest_candidate"] = repair["candidate_artifact"]
    contract["repair_status"] = repair["status"]
    contract["lean_compile_claim"] = False
    if node.metadata.get("frontier_repair_contract") != contract:
        node.metadata["frontier_repair_contract"] = contract
        changed = True
    if changed:
        state.event(
            "routeb_o1_repair_patch_recorded",
            node_id=node.id,
            repair_status=repair["status"],
            registry_promoted=False,
            formal_certificate_allowed=False,
        )
        state.validate()
        store.save(state)
    print({
        "status": "recorded" if changed else "already_recorded",
        "repair_status": repair["status"],
        "candidate_sha256": repair["candidate_artifact"]["sha256"],
        "state_revision": store.load().revision,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
