"""Attach the fresh Julia execution handoff and verifier to the force gate."""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "agent_review_inbox/review-T-P4-fresh-export-execution-handoff-codex-20260907.md"
CHECKER = ROOT / "examples/routeb_b45_5_descriptor_terms_adapter_lean/verify_general_state_force_binding.py"
EXPORTER = ROOT / "examples/routeb_b45_5_descriptor_terms_adapter_lean/general_state_force_binding_export.jl"
SOURCE = ROOT.parent / "6dof_sos_optimized" / "6dof_sos_optimized" / "robot_final" / "dhport_lib.jl"
STATE = ROOT / "artifacts/routeb_6dof/state.json"
EXPECTED_EXPORTER = "5351110E81327EBC059074A2E445A33E00859320BCE37B5B0220BB189F4E46A4"
EXPECTED_SOURCE = "AEBE6DB09B2D943448C5D701631109DBA8F5EEB070CC66593E5DBACA26485936"
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
    for path in (REVIEW, CHECKER, EXPORTER, SOURCE, STATE):
        if not path.is_file():
            raise FileNotFoundError(path)
    text = REVIEW.read_text(encoding="utf-8", errors="replace")
    for phrase in (
        "JULIA_EXECUTION = NOT RUN",
        "PENDING_JULIA_EXECUTION",
        "GENERAL_STATE_FORCE_BINDING_INTAKE=PASS_RUNTIME_FLOAT64_SOURCE_BINDING_CANDIDATE",
        "DEPLOYED_TAU_EQUIVALENCE = NOT_CLAIMED",
        "MAIN_STATE_MUTATION = false",
    ):
        if phrase not in text:
            raise ValueError(f"force execution handoff boundary missing: {phrase}")
    exporter_sha = sha(EXPORTER)
    source_sha = sha(SOURCE)
    if exporter_sha != EXPECTED_EXPORTER or source_sha != EXPECTED_SOURCE:
        raise ValueError("frozen force execution input hash drift")
    entry = {
        "schema_version": 1,
        "task_id": "T-P4-KC-COORDINATE-ADAPTER",
        "source_agent": "codex-inbox",
        "review_status": "PENDING_JULIA_EXECUTION",
        "review_artifact": {"path": str(REVIEW.resolve()), "sha256": sha(REVIEW)},
        "checker": {"path": str(CHECKER.resolve()), "sha256": sha(CHECKER)},
        "exporter_sha256": exporter_sha,
        "deployed_source_sha256": source_sha,
        "required_outputs": [
            "force_binding_states.csv", "FORCE_BINDING_RECEIPT.md",
            "worker.stdout.txt", "worker.stderr.txt", "worker.exit-code.txt",
        ],
        "runtime_gate": {
            "process_exit_code": 0,
            "rows": 16,
            "max_E1": "<=1e-12",
            "max_E2": "<=1e-12",
        },
        "deployed_tau_equivalence": "NOT_CLAIMED",
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    store = StateStore(STATE)
    state = store.load()
    node = find(state, "P4.true_dh_force_descriptor_semantics")
    prior = list(node.metadata.get("force_execution_handoffs", []))
    changed = entry not in prior
    if changed:
        prior.append(entry)
        node.metadata["force_execution_handoffs"] = prior
    desired = {
        "status": entry["review_status"],
        "review_sha256": entry["review_artifact"]["sha256"],
        "checker_sha256": entry["checker"]["sha256"],
        "exporter_sha256": exporter_sha,
        "deployed_source_sha256": source_sha,
        "required_outputs": entry["required_outputs"],
        "runtime_gate": entry["runtime_gate"],
        "runtime_receipt_present": False,
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    if node.metadata.get("force_execution_handoff") != desired:
        node.metadata["force_execution_handoff"] = desired
        changed = True
    if changed:
        state.event(
            "routeb_force_execution_handoff_recorded",
            node_id=node.id,
            review_status=entry["review_status"],
            runtime_receipt_present=False,
            checker_hash_bound=True,
            registry_promoted=False,
            formal_certificate_allowed=False,
        )
        state.validate()
        store.save(state)
    print({
        "status": "recorded" if changed else "already_recorded",
        "review_status": entry["review_status"],
        "state_revision": store.load().revision,
        "checker_sha256": entry["checker"]["sha256"],
        "runtime_receipt_present": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
