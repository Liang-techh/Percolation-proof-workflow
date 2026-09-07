"""Record the short GitHub/Julia execution handoff as pending only."""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "agent_review_inbox/review-T-P4-force-julia-runner-handoff-short-codex-20260907.md"
RUNNER = ROOT / "examples/routeb_b45_5_descriptor_terms_adapter_lean/run_general_state_force_binding.ps1"
VERIFIER = ROOT / "examples/routeb_b45_5_descriptor_terms_adapter_lean/verify_general_state_force_binding.py"
EXPORTER = ROOT / "examples/routeb_b45_5_descriptor_terms_adapter_lean/general_state_force_binding_export.jl"
SOURCE = ROOT.parent / "6dof_sos_optimized" / "6dof_sos_optimized" / "robot_final" / "dhport_lib.jl"
STATE = ROOT / "artifacts/routeb_6dof/state.json"
EXPECTED = {
    "exporter": "5351110E81327EBC059074A2E445A33E00859320BCE37B5B0220BB189F4E46A4",
    "source": "AEBE6DB09B2D943448C5D701631109DBA8F5EEB070CC66593E5DBACA26485936",
}
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
        "JULIA_FOUND=False",
        "PENDING_JULIA_EXECUTION",
        "run_general_state_force_binding.ps1",
        "general-state-export-20260907/",
        "GENERAL_STATE_FORCE_BINDING_INTAKE=PASS_RUNTIME_FLOAT64_SOURCE_BINDING_CANDIDATE",
        "Any missing artifact, hash drift, nonzero exit, schema mismatch",
    ):
        if phrase not in text:
            raise ValueError(f"short force handoff boundary missing: {phrase}")
    actual = {"review": sha(REVIEW), "runner": sha(RUNNER), "verifier": sha(VERIFIER), "exporter": sha(EXPORTER), "source": sha(SOURCE)}
    if actual["exporter"] != EXPECTED["exporter"] or actual["source"] != EXPECTED["source"]:
        raise ValueError(f"frozen force hash drift: {actual}")
    entry = {
        "task_id": "T-P4-KC-COORDINATE-ADAPTER",
        "status": "PENDING_JULIA_EXECUTION",
        "review_sha256": actual["review"],
        "runner_sha256": actual["runner"],
        "verifier_sha256": actual["verifier"],
        "exporter_sha256": actual["exporter"],
        "deployed_source_sha256": actual["source"],
        "required_output_dir": "examples/routeb_b45_5_descriptor_terms_adapter_lean/output/general-state-export-20260907/",
        "julia_found_here": False,
        "runtime_receipt_present": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    store = StateStore(STATE)
    state = store.load()
    node = find(state, "P4.true_dh_force_descriptor_semantics")
    prior = list(node.metadata.get("force_short_handoffs", []))
    changed = entry not in prior
    if changed:
        prior.append(entry)
        node.metadata["force_short_handoffs"] = prior
    desired = {
        "status": entry["status"],
        "review_sha256": actual["review"],
        "runner_sha256": actual["runner"],
        "verifier_sha256": actual["verifier"],
        "exporter_sha256": actual["exporter"],
        "deployed_source_sha256": actual["source"],
        "required_output_dir": entry["required_output_dir"],
        "julia_found_here": False,
        "runtime_receipt_present": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    if node.metadata.get("force_short_handoff") != desired:
        node.metadata["force_short_handoff"] = desired
        changed = True
    if changed:
        state.event(
            "routeb_force_short_julia_handoff_recorded",
            node_id=node.id,
            review_status=entry["status"],
            runtime_receipt_present=False,
            registry_promoted=False,
            formal_certificate_allowed=False,
        )
        state.validate()
        store.save(state)
    print({"status": "recorded" if changed else "already_recorded", "state_revision": store.load().revision, "runtime_receipt_present": False, "registry_promoted": False})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
