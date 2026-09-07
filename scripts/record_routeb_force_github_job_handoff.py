"""Record the copyable GitHub Actions force-runtime handoff as pending."""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "agent_review_inbox/review-T-P4-force-github-job-handoff-short-codex-20260907.md"
RUNNER = ROOT / "examples/routeb_b45_5_descriptor_terms_adapter_lean/run_general_state_force_binding.ps1"
VERIFIER = ROOT / "examples/routeb_b45_5_descriptor_terms_adapter_lean/verify_general_state_force_binding.py"
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
    for path in (REVIEW, RUNNER, VERIFIER, EXPORTER, SOURCE, STATE):
        if not path.is_file():
            raise FileNotFoundError(path)
    text = REVIEW.read_text(encoding="utf-8", errors="replace")
    for phrase in (
        "PENDING_RUNTIME_JULIA",
        "DEPLOYED_SOURCE_REPOSITORY",
        "DEPLOYED_SOURCE_REF",
        "workflow_dispatch",
        "julia-actions/setup-julia@v2",
        "run_general_state_force_binding.ps1",
        "actions/upload-artifact@v4",
    ):
        if phrase not in text:
            raise ValueError(f"GitHub force handoff boundary missing: {phrase}")
    actual = {"review": sha(REVIEW), "runner": sha(RUNNER), "verifier": sha(VERIFIER), "exporter": sha(EXPORTER), "source": sha(SOURCE)}
    if actual["exporter"] != EXPECTED_EXPORTER or actual["source"] != EXPECTED_SOURCE:
        raise ValueError(f"frozen force hash drift: {actual}")
    entry = {
        "task_id": "T-P4-KC-COORDINATE-ADAPTER",
        "status": "PENDING_RUNTIME_JULIA",
        "review_sha256": actual["review"],
        "runner_sha256": actual["runner"],
        "verifier_sha256": actual["verifier"],
        "exporter_sha256": actual["exporter"],
        "deployed_source_sha256": actual["source"],
        "workflow_dispatch": True,
        "required_repository_variables": ["DEPLOYED_SOURCE_REPOSITORY", "DEPLOYED_SOURCE_REF"],
        "julia_version": "1.10",
        "required_rows": 16,
        "required_output_dir": "workflow/examples/routeb_b45_5_descriptor_terms_adapter_lean/output/general-state-export-20260907/",
        "runtime_receipt_present": False,
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    store = StateStore(STATE)
    state = store.load()
    node = find(state, "P4.true_dh_force_descriptor_semantics")
    prior = list(node.metadata.get("force_github_job_handoffs", []))
    changed = entry not in prior
    if changed:
        prior.append(entry)
        node.metadata["force_github_job_handoffs"] = prior
    desired = {
        "status": entry["status"],
        "review_sha256": actual["review"],
        "runner_sha256": actual["runner"],
        "verifier_sha256": actual["verifier"],
        "exporter_sha256": actual["exporter"],
        "deployed_source_sha256": actual["source"],
        "workflow_dispatch": True,
        "required_repository_variables": entry["required_repository_variables"],
        "julia_version": "1.10",
        "required_rows": 16,
        "runtime_receipt_present": False,
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    if node.metadata.get("force_github_job_handoff") != desired:
        node.metadata["force_github_job_handoff"] = desired
        changed = True
    if changed:
        state.event(
            "routeb_force_github_job_handoff_recorded",
            node_id=node.id,
            review_status=entry["status"],
            runtime_receipt_present=False,
            formal_certificate_allowed=False,
            registry_promoted=False,
        )
        state.validate()
        store.save(state)
    print({"status": "recorded" if changed else "already_recorded", "state_revision": store.load().revision, "runtime_receipt_present": False, "registry_promoted": False})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
