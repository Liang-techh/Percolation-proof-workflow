"""Ingest fresh immutable obstruction reviews without promoting evidence."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
O0 = ROOT / "agent_review_inbox/receipt-T-P4-033-O0-R3-same-key-strict-margin-obstruction-20260907.json"
O1 = ROOT / "agent_review_inbox/review-T-P4-033-O1-true-dh-exact-typed-source-export-immutable-codex-20260907.md"
O2 = ROOT / "agent_review_inbox/review-T-P4-036.2-theta2-same-namespace-parent-sibling-obstruction-codex-20260907.md"
O2_INSTANCE = ROOT / "artifacts/routeb_theta2_leaf_handoff_20260907/theta2_leaf_1_coverage_join_obstruction.json"
STATE = ROOT / "artifacts/routeb_6dof/state.json"
sys.path.insert(0, str(ROOT / "src"))
from percolation_workflow.store import StateStore  # noqa: E402


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def find(state, name: str):
    for node in state.nodes.values():
        if node.name == name:
            return node
    raise ValueError(f"missing node: {name}")


def main() -> int:
    for path in (O0, O1, O2, O2_INSTANCE, STATE):
        if not path.is_file():
            raise FileNotFoundError(path)
    o0 = json.loads(O0.read_text(encoding="utf-8"))
    if o0.get("status") != "OPEN_FAIL_CLOSED" or o0.get("schur_margin_consumed") is not False:
        raise ValueError("O0 follow-up is not fail-closed")
    o2i = json.loads(O2_INSTANCE.read_text(encoding="utf-8"))
    if o2i.get("status") != "BLOCKED_AUTHORITY_NOT_ADMISSIBLE":
        raise ValueError("O2 coverage obstruction is not fail-closed")
    o1_text = O1.read_text(encoding="utf-8", errors="replace")
    o2_text = O2.read_text(encoding="utf-8", errors="replace")
    for phrase in (
        "OPEN_SAME_OBJECT_BINDING_TWO_PATHS",
        "M_DD45_at M mu q : Matrix (Fin 4) (Fin 4) ℝ",
        "M_DD_left_inverse_witness` remains `OPEN",
    ):
        if phrase not in o1_text:
            raise ValueError(f"O1 follow-up boundary missing: {phrase}")
    for phrase in (
        "same-namespace canonical 13D parent endpoint: NOT FOUND",
        "same-namespace canonical 13D sibling endpoint: NOT FOUND",
        "concrete CoverageJoin2 premise: NOT FOUND",
        "KEEP ENDPOINT_PROVENANCE_ONLY",
    ):
        if phrase not in o2_text:
            raise ValueError(f"O2 follow-up boundary missing: {phrase}")
    digests = {"o0": sha(O0), "o1": sha(O1), "o2": sha(O2), "o2_instance": sha(O2_INSTANCE)}
    store = StateStore(STATE)
    state = store.load()
    o0node = find(state, "P4.true_dh_regularizer_semantics_bridge")
    o1node = find(state, "P4.true_dh_exact_real_coefficient_identity")
    o2node = find(state, "P4.true_dh_float64_evaluator_enclosure")
    o0entry = {
        "task_id": "T-P4-033-O0-R3",
        "status": "OPEN_FAIL_CLOSED",
        "receipt_sha256": digests["o0"],
        "same_key_receipt_found": False,
        "missing": ["weighted baseline rho_r", "remaining margin m_r", "fixed theta", "strict leftover m_f > 0"],
        "schur_margin_consumed": False,
        "registry_promoted": False,
    }
    o1entry = {
        "task_id": "T-P4-033-O1",
        "status": "OPEN_SAME_OBJECT_BINDING_TWO_PATHS",
        "review_sha256": digests["o1"],
        "source_receipt_present": False,
        "required_binding": "M_DD = M_DD45_at M mu q with exact same source/state/mu/q and D=(1,2,3,6)",
        "registry_promoted": False,
    }
    o2entry = {
        "task_id": "T-P4-036.2",
        "status": "BLOCKED_AUTHORITY_NOT_ADMISSIBLE",
        "review_sha256": digests["o2"],
        "obstruction_sha256": digests["o2_instance"],
        "authority_status": "ENDPOINT_PROVENANCE_ONLY",
        "same_namespace_parent_found": False,
        "same_namespace_sibling_found": False,
        "coverage_join_premise_instantiated": False,
        "global_coverage": False,
        "registry_promoted": False,
    }
    changed = False
    for node, key, entry in (
        (o0node, "o0_strict_leftover_receipts", o0entry),
        (o1node, "o1_typed_source_export_obstructions", o1entry),
        (o2node, "o2_same_namespace_obstructions", o2entry),
    ):
        prior = list(node.metadata.get(key, []))
        if entry not in prior:
            prior.append(entry)
            node.metadata[key] = prior
            changed = True
    if changed:
        state.event(
            "routeb_followup_obstructions_recorded",
            o0_status=o0entry["status"],
            o1_status=o1entry["status"],
            o2_status=o2entry["status"],
            registry_promoted=False,
            formal_certificate_allowed=False,
        )
        state.validate()
        store.save(state)
    print({"status": "recorded" if changed else "already_recorded", "state_revision": store.load().revision, "digests": digests, "registry_promoted": False})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
