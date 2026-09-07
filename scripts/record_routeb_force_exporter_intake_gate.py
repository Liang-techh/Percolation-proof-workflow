"""Record the strict intake gate for the general-state force exporter.

This records a receipt *specification* only.  It never promotes runtime
evidence and never treats the presence of a CSV as a successful source
binding.  A later Julia worker must provide a fresh, hash-bound receipt and
CSV before the runtime candidate status can be considered.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "agent_review_inbox/review-T-P4-force-exporter-intake-gate-codex-20260907.md"
STATE = ROOT / "artifacts/routeb_6dof/state.json"
EXPORTER = ROOT / "examples/routeb_b45_5_descriptor_terms_adapter_lean/general_state_force_binding_export.jl"
DEPLOYED = (
    ROOT.parent
    / "6dof_sos_optimized"
    / "6dof_sos_optimized"
    / "robot_final"
    / "dhport_lib.jl"
)
EXPECTED_EXPORTER = "5351110E81327EBC059074A2E445A33E00859320BCE37B5B0220BB189F4E46A4"
EXPECTED_DEPLOYED = "AEBE6DB09B2D943448C5D701631109DBA8F5EEB070CC66593E5DBACA26485936"
REQUIRED_FIELDS = [
    "q4", "q5", "dq4", "dq5", "w",
    "CdqB4", "CdqB5", "GqB4", "GqB5", "G0B4", "G0B5",
    "tauB4", "tauB5", "rhsB4", "rhsB5",
    "sourceBlockForce4", "sourceBlockForce5",
    "aB4", "aB5", "aD1", "aD2", "aD3", "aD6",
    "MqBB11", "MqBB12", "MqBB21", "MqBB22",
    "MqBD41", "MqBD42", "MqBD43", "MqBD46",
    "MqBD51", "MqBD52", "MqBD53", "MqBD56",
    "sourceDescriptorRhs4", "sourceDescriptorRhs5",
    "E1_4", "E1_5", "E2_4", "E2_5",
]

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
    for path in (REVIEW, STATE, EXPORTER, DEPLOYED):
        if not path.is_file():
            raise FileNotFoundError(path)
    text = REVIEW.read_text(encoding="utf-8", errors="replace")
    required_phrases = (
        "PENDING_JULIA_EXECUTION",
        "PASS_RUNTIME_FLOAT64_SOURCE_BINDING_CANDIDATE",
        "REJECTED_STALE_INPUT",
        "sample_count = 16",
        "B = [4,5]",
        "D = [1,2,3,6]",
        "max(abs(E1_4), abs(E1_5), abs(E2_4), abs(E2_5)) <= 1e-12",
        "deployed `tau` 等价",
        "registry promotion",
    )
    for phrase in required_phrases:
        if phrase not in text:
            raise ValueError(f"force exporter intake gate missing: {phrase}")

    actual_exporter = sha(EXPORTER)
    actual_deployed = sha(DEPLOYED)
    gate_status = "PENDING_JULIA_EXECUTION"
    entry = {
        "schema_version": 1,
        "task_id": "T-P4-KC-COORDINATE-ADAPTER",
        "source_agent": "codex-inbox",
        "review_status": gate_status,
        "review_artifact": ref(REVIEW),
        "exporter": ref(EXPORTER),
        "deployed_source": ref(DEPLOYED),
        "expected_exporter_sha256": EXPECTED_EXPORTER,
        "expected_deployed_sha256": EXPECTED_DEPLOYED,
        "input_hashes_match": {
            "exporter": actual_exporter == EXPECTED_EXPORTER,
            "deployed_source": actual_deployed == EXPECTED_DEPLOYED,
        },
        "required_csv_fields": REQUIRED_FIELDS,
        "seed": 20260907,
        "sample_count": 16,
        "B": [4, 5],
        "D": [1, 2, 3, 6],
        "mass_regularizer": "1e-6",
        "fd_step": "1e-5",
        "residual_threshold": "1e-12",
        "runtime_receipt_required": True,
        "runtime_csv_required": True,
        "general_state_source_binding": "OPEN",
        "deployed_tau_equivalence": "NOT_CLAIMED",
        "float64_to_exact_real": "OPEN",
        "coverage": "OPEN",
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    store = StateStore(STATE)
    state = store.load()
    node = find(state, "P4.true_dh_force_descriptor_semantics")
    prior = list(node.metadata.get("force_exporter_intake_gates", []))
    changed = entry not in prior
    if changed:
        prior.append(entry)
        node.metadata["force_exporter_intake_gates"] = prior
    desired = {
        "status": gate_status,
        "review_sha256": entry["review_artifact"]["sha256"],
        "exporter_sha256": actual_exporter,
        "deployed_source_sha256": actual_deployed,
        "input_hashes_match": entry["input_hashes_match"],
        "sample_count": 16,
        "B": [4, 5],
        "D": [1, 2, 3, 6],
        "residual_threshold": "1e-12",
        "runtime_receipt_required": True,
        "general_state_source_binding": "OPEN",
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    if node.metadata.get("force_exporter_intake_gate") != desired:
        node.metadata["force_exporter_intake_gate"] = desired
        changed = True
    if changed:
        state.event(
            "routeb_force_exporter_intake_gate_recorded",
            node_id=node.id,
            review_status=gate_status,
            exporter_hash_match=actual_exporter == EXPECTED_EXPORTER,
            deployed_source_hash_match=actual_deployed == EXPECTED_DEPLOYED,
            runtime_receipt_required=True,
            general_source_binding="OPEN",
            registry_promoted=False,
            formal_certificate_allowed=False,
        )
        state.validate()
        store.save(state)
    print({
        "status": "recorded" if changed else "already_recorded",
        "review_status": gate_status,
        "exporter_sha256": actual_exporter,
        "deployed_source_sha256": actual_deployed,
        "input_hashes_match": entry["input_hashes_match"],
        "state_revision": store.load().revision,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
