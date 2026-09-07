"""Ingest an O0 exact-bounds obstruction receipt, fail-closed."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "agent_review_inbox/receipt-T-P4-033-O0-exact-K-Br-Cf-same-key-obstruction-20260907.json"
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
    for path in (RECEIPT, STATE):
        if not path.is_file():
            raise FileNotFoundError(path)
    payload = json.loads(RECEIPT.read_text(encoding="utf-8"))
    required = {
        "schema": "routeb-o0-exact-k-br-cf-same-key-obstruction-v2",
        "task": "T-P4-033",
        "status": "OBSTRUCTION_NO_AUTHORITATIVE_SAME_KEY_TUPLE",
    }
    for key, expected in required.items():
        if payload.get(key) != expected:
            raise ValueError(f"O0 receipt field {key!r} is not {expected!r}")
    admission = payload.get("admission", {})
    if any(admission.get(key) is not False for key in (
        "formal_certificate_allowed", "registry_eligible", "ledger_consumed", "schur_margin_consumed"
    )):
        raise ValueError("O0 obstruction receipt is not fail-closed")
    tuple_payload = payload.get("tuple", {})
    if tuple_payload.get("K", {}).get("authoritative_exact_real_receipt") is not False:
        raise ValueError("O0 receipt unexpectedly admits K")
    for field in ("Br", "Cf"):
        item = tuple_payload.get(field, {})
        if item.get("value_exact_rational") is not None or not item.get("missing"):
            raise ValueError(f"O0 receipt unexpectedly admits {field}")
    if payload.get("key_contract", {}).get("same_key_tuple_found") is not False:
        raise ValueError("O0 receipt unexpectedly found a same-key tuple")

    review_entry = {
        "schema_version": 1,
        "task_id": payload["task"],
        "source_agent": "codex-inbox",
        "review_status": payload["status"],
        "receipt_artifact": {"path": str(RECEIPT.resolve()), "sha256": sha(RECEIPT)},
        "observed_state_revision": payload.get("observed_state_revision"),
        "missing_same_key_fields": payload.get("exact_missing_fields", []),
        "constructive_bound_search": payload.get("constructive_bound_search", {}),
        "formal_certificate_allowed": False,
        "registry_promoted": False,
        "admission_status": "obstruction_pending_exact_keyed_bounds",
    }
    store = StateStore(STATE)
    state = store.load()
    node = find(state, "P4.true_dh_regularizer_semantics_bridge")
    prior = list(node.metadata.get("o0_exact_bounds_receipts", []))
    changed = review_entry not in prior
    if changed:
        prior.append(review_entry)
        node.metadata["o0_exact_bounds_receipts"] = prior
    desired = {
        "status": payload["status"],
        "receipt_sha256": review_entry["receipt_artifact"]["sha256"],
        "observed_state_revision": payload.get("observed_state_revision"),
        "same_key_tuple_found": False,
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    if node.metadata.get("o0_exact_bounds_receipt_intake") != desired:
        node.metadata["o0_exact_bounds_receipt_intake"] = desired
        changed = True
    if changed:
        state.event(
            "routeb_o0_exact_bounds_receipt_ingested",
            node_id=node.id,
            review_status=payload["status"],
            admission_status="obstruction_pending_exact_keyed_bounds",
            registry_promoted=False,
            formal_certificate_allowed=False,
        )
        state.validate()
        store.save(state)
    print({
        "status": "recorded" if changed else "already_recorded",
        "review_status": payload["status"],
        "state_revision": store.load().revision,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
