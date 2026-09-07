"""Record the non-runtime force runner handoff and its fail-closed disposition."""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "agent_review_inbox/review-T-P4-force-exporter-runner-codex-20260907.md"
RUNNER = ROOT / "examples/routeb_b45_5_descriptor_terms_adapter_lean/run_general_state_force_binding.ps1"
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
    for path in (REVIEW, RUNNER, STATE):
        if not path.is_file():
            raise FileNotFoundError(path)
    text = REVIEW.read_text(encoding="utf-8", errors="replace")
    for phrase in (
        "JULIA_EXECUTION = NOT RUN HERE",
        "PENDING_JULIA_EXECUTION",
        "FRESH_CSV = NOT GENERATED HERE",
        "MAIN_STATE_MUTATION = false",
        "verify_general_state_force_binding.py",
    ):
        if phrase not in text:
            raise ValueError(f"force runner review boundary missing: {phrase}")
    entry = {
        "schema_version": 1,
        "task_id": "T-P4-KC-COORDINATE-ADAPTER",
        "source_agent": "codex-inbox",
        "review_status": "PENDING_JULIA_EXECUTION",
        "review_artifact": {"path": str(REVIEW.resolve()), "sha256": sha(REVIEW)},
        "runner": {"path": str(RUNNER.resolve()), "sha256": sha(RUNNER)},
        "fresh_output_required": True,
        "overwrite_existing_output_forbidden": True,
        "julia_executed_here": False,
        "fresh_csv_present": False,
        "fresh_receipt_present": False,
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    store = StateStore(STATE)
    state = store.load()
    node = find(state, "P4.true_dh_force_descriptor_semantics")
    prior = list(node.metadata.get("force_runner_reviews", []))
    changed = entry not in prior
    if changed:
        prior.append(entry)
        node.metadata["force_runner_reviews"] = prior
    desired = {
        "status": entry["review_status"],
        "review_sha256": entry["review_artifact"]["sha256"],
        "runner_sha256": entry["runner"]["sha256"],
        "fresh_output_required": True,
        "overwrite_existing_output_forbidden": True,
        "julia_executed_here": False,
        "fresh_csv_present": False,
        "fresh_receipt_present": False,
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    if node.metadata.get("force_runner_review") != desired:
        node.metadata["force_runner_review"] = desired
        changed = True
    if changed:
        state.event(
            "routeb_force_runner_review_recorded",
            node_id=node.id,
            review_status=entry["review_status"],
            fresh_receipt_present=False,
            overwrite_existing_output_forbidden=True,
            registry_promoted=False,
            formal_certificate_allowed=False,
        )
        state.validate()
        store.save(state)
    print({
        "status": "recorded" if changed else "already_recorded",
        "review_status": entry["review_status"],
        "state_revision": store.load().revision,
        "runner_sha256": entry["runner"]["sha256"],
        "fresh_receipt_present": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
