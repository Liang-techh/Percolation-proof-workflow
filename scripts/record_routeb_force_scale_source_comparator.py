"""Record the focused force-scale source comparator without promoting a theorem."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "examples/routeb_b45_5_descriptor_terms_adapter_lean/SOURCE_COMPARATOR_RECEIPT_forceScaleKc_20260907.md"
COMPARATOR = ROOT / "examples/routeb_b45_5_descriptor_terms_adapter_lean/source_contract_comparator.py"
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
    for path in (RECEIPT, COMPARATOR, STATE):
        if not path.is_file():
            raise FileNotFoundError(path)
    text = RECEIPT.read_text(encoding="utf-8", errors="replace")
    for phrase in (
        "routeb_b45_5_force_scale_source_contract_v1",
        "Result: `ANCHOR_PASS_DH_EXECUTION_BINDING_OPEN`",
        "Lean statement surface for `forceScaleKc_eq_rhoKc`: `PASS`",
        "`DescriptorTermsAdapter` source-premise surface: `PASS`",
        "source hash binding: `PASS`",
        "deployed_source_binding = OPEN",
        "registry_promotion = false",
    ):
        if phrase not in text:
            raise ValueError(f"force-scale source comparator boundary missing: {phrase}")

    completed = subprocess.run(
        [sys.executable, str(COMPARATOR)],
        cwd=str(ROOT),
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        raise ValueError(f"source comparator rejected: {completed.stdout[-1000:]}{completed.stderr[-1000:]}")
    result = json.loads(completed.stdout)
    if result.get("source_binding_status") != "ANCHOR_PASS_DH_EXECUTION_BINDING_OPEN":
        raise ValueError("unexpected source comparator status")
    if result.get("statement_comparator") != "PASS" or result.get("source_hash_binding") != "PASS":
        raise ValueError("focused source comparator did not pass its declared anchors")

    hash_matches = re.findall(r"[0-9A-Fa-f]{64}", text)
    if not hash_matches:
        raise ValueError("source comparator receipt has no hashes")
    review_entry = {
        "schema_version": 1,
        "task_id": "T-P4-KC-COORDINATE-ADAPTER",
        "source_agent": "codex-local",
        "review_status": "ANCHOR_PASS_DH_EXECUTION_BINDING_OPEN",
        "receipt_artifact": {"path": str(RECEIPT.resolve()), "sha256": sha(RECEIPT)},
        "comparator_artifact": {"path": str(COMPARATOR.resolve()), "sha256": sha(COMPARATOR)},
        "statement_comparator": "PASS",
        "source_anchor_comparator": "PASS",
        "source_binding": "OPEN",
        "deployed_tau_equivalence": "NOT_CLAIMED",
        "derived_force_coefficients": result["derived_force_coefficients"],
        "source_hashes": result["sha256"],
        "unresolved": result["unresolved"],
        "formal_certificate_allowed": False,
        "registry_promoted": False,
        "admission_status": "focused_anchor_receipt_only",
    }
    store = StateStore(STATE)
    state = store.load()
    node = find(state, "P4.true_dh_force_descriptor_semantics")
    prior = list(node.metadata.get("source_comparator_receipts", []))
    changed = review_entry not in prior
    if changed:
        prior.append(review_entry)
        node.metadata["source_comparator_receipts"] = prior
    desired = {
        "status": review_entry["review_status"],
        "receipt_sha256": review_entry["receipt_artifact"]["sha256"],
        "comparator_sha256": review_entry["comparator_artifact"]["sha256"],
        "statement_comparator": "PASS",
        "source_anchor_comparator": "PASS",
        "source_binding": "OPEN",
        "deployed_tau_equivalence": "NOT_CLAIMED",
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    if node.metadata.get("force_scale_source_comparator") != desired:
        node.metadata["force_scale_source_comparator"] = desired
        changed = True
    if changed:
        state.event(
            "routeb_force_scale_source_comparator_recorded",
            node_id=node.id,
            review_status=review_entry["review_status"],
            statement_comparator="PASS",
            source_binding="OPEN",
            registry_promoted=False,
            formal_certificate_allowed=False,
        )
        state.validate()
        store.save(state)
    print({
        "status": "recorded" if changed else "already_recorded",
        "review_status": review_entry["review_status"],
        "state_revision": store.load().revision,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
