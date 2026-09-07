"""Record the exact O1 port-identity decomposition without admitting O1.

The review may report a compiled temporary probe, but it is not the canonical
candidate receipt.  This intake only preserves the reusable linear-algebra
chain and its missing source/projected premises.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "agent_review_inbox/review-T-P4-033-O1-next-codex.md"
CANDIDATE = ROOT / "artifacts/task_routeb_o1_lean_api_audit_20260907/RouteBO1PortIdentity.lean"
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
    for path in (REVIEW, CANDIDATE, STATE):
        if not path.is_file():
            raise FileNotFoundError(path)
    text = REVIEW.read_text(encoding="utf-8", errors="replace")
    for phrase in (
        "eliminate_D", "schur_port_action", "routeB_port_identity",
        "临时 probe", "不是 canonical verification", "h_inv_left",
        "true-DH block extraction receipt", "exact-real projected balance receipt",
    ):
        if phrase not in text:
            raise ValueError(f"O1 exact identity boundary missing: {phrase}")
    candidate_bytes = CANDIDATE.read_bytes().lower()
    if b"sorry" in candidate_bytes or b"admit" in candidate_bytes:
        raise ValueError("O1 candidate contains forbidden sorry/admit token")

    review = {
        "schema_version": 1,
        "task_id": "T-P4-033-O1-next",
        "source_agent": "Codex",
        "review_status": "EXACT_LINEAR_ALGEBRA_CHAIN_CONDITIONALLY_COMPILED",
        "review_artifact": ref(REVIEW),
        "candidate_artifact": ref(CANDIDATE),
        "chain": ["eliminate_D", "schur_port_action", "routeB_port_identity"],
        "reusable_interface": {
            "B": "Fin 2",
            "D": "Fin 4",
            "R_port": "-(M_BD * M_DD_inv * DeltaM_DB)",
            "premise": "M_DD_inv * M_DD = 1",
        },
        "missing_premises": [
            "determinant-to-left-inverse exact adapter",
            "true-DH block extraction and source hash binding",
            "exact projected h_D and h_B balance receipts",
            "same-(mu,q) inverse witness",
            "canonical pinned Lean/comparator receipt",
        ],
        "temporary_probe": {
            "reported_exit_code": 0,
            "reported_zero_sorry": True,
            "reported_no_axiom": True,
            "canonical_receipt_present": False,
        },
        "formal_certificate_allowed": False,
        "registry_promoted": False,
        "admission_status": "pending_canonical_pinned_lean_receipt_and_projected_premises",
    }
    store = StateStore(STATE)
    state = store.load()
    node = find(state, "P4.true_dh_exact_real_coefficient_identity")
    reviews = list(node.metadata.get("independent_static_reviews", []))
    changed = review not in reviews
    if changed:
        reviews.append(review)
        node.metadata["independent_static_reviews"] = reviews
    desired = {
        "status": "CONDITIONALLY_COMPILED_CHAIN_OPEN_PREMISES",
        "chain": review["chain"],
        "candidate_artifact": review["candidate_artifact"],
        "missing_premises": review["missing_premises"],
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    if node.metadata.get("exact_port_identity_chain") != desired:
        node.metadata["exact_port_identity_chain"] = desired
        changed = True
    if changed:
        state.event(
            "routeb_o1_exact_identity_review_recorded",
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
