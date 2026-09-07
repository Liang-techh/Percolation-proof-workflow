"""Ingest the force source-binding contract with explicit stale-hash handling."""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ROUTE = ROOT.parent / "6dof_sos_optimized" / "6dof_sos_optimized" / "robot_final"
REVIEW = ROOT / "agent_review_inbox/review-T-P4-force-source-binding-contract-codex-20260907.md"
STATE = ROOT / "artifacts/routeb_6dof/state.json"
ARTIFACTS = {
    "deployed_dhport": ROUTE / "dhport_lib.jl",
    "interface_script": ROUTE / "routeB_descriptor_residual_interface.jl",
    "interface_csv": ROUTE / "routeB_descriptor_residual_interface.csv",
    "verifier": ROUTE / "verify_descriptor_interface.py",
    "m0_table": ROUTE / "routeB_Mq_M0.csv",
}
EXPECTED = {
    "deployed_dhport": "AEBE6DB09B2D943448C5D701631109DBA8F5EEB070CC66593E5DBACA26485936",
    "interface_script": "D3D21705E5E904A080E4B86DC4C380788D2323C155570A8E7B40D62B11BB0A24",
    "interface_csv": "ED10D0335DEBACD670A26871CAD9CE51FC871CB86F6AE956125AEAE3DEE00E24",
    "verifier": "47E1C02EA4ADDD64EB8C11F3DBBDF7B414288A55E8AA625494C365FC9B3FCBB0",
    "m0_table": "28D98AD71D1D6C2CBE830872CAD9077F2F7B4E2D932794217EB68868FD2E2B40",
}
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
    if not REVIEW.is_file() or not STATE.is_file():
        raise FileNotFoundError(REVIEW if not REVIEW.is_file() else STATE)
    if any(not path.is_file() for path in ARTIFACTS.values()):
        raise FileNotFoundError("one or more source-binding artifacts are absent")
    text = REVIEW.read_text(encoding="utf-8", errors="replace")
    for phrase in (
        "sourceBlockForce = expectedSourceForce q v w t",
        "sourceBlockForce = sourceDescriptorRhs t",
        "AUDITABLE_STATE_CONTRACT_PASS",
        "OPEN_PENDING_B_ROW_EXPORT_AND_FLOAT64_BRIDGE",
        "OPEN_PENDING_ACTUAL_MQ_BB_BD_EXPORT",
        "deployed `tau` equivalence: `NOT CLAIMED`",
        "registry/state mutation: `false`",
    ):
        if phrase not in text:
            raise ValueError(f"force source contract boundary missing: {phrase}")
    actual = {name: sha(path) for name, path in ARTIFACTS.items()}
    matched = {name: actual[name] == EXPECTED[name] for name in ARTIFACTS}
    status = (
        "AUDITABLE_ZERO_STATE_CONTRACT_PASS_GENERAL_SOURCE_BINDING_OPEN"
        if all(matched.values())
        else "AUDITABLE_ZERO_STATE_CONTRACT_PASS_ARTIFACT_HASH_DRIFT_GENERAL_OPEN"
    )
    entry = {
        "schema_version": 1,
        "task_id": "T-P4-KC-COORDINATE-ADAPTER",
        "source_agent": "codex-inbox",
        "review_status": status,
        "review_artifact": ref(REVIEW),
        "artifact_hashes_expected": EXPECTED,
        "artifact_hashes_actual": actual,
        "artifact_hash_matches": matched,
        "zero_state_witness": "AUDITABLE_STATE_CONTRACT_PASS",
        "general_source_force_binding": "OPEN",
        "general_descriptor_binding": "OPEN",
        "deployed_tau_equivalence": "NOT_CLAIMED",
        "float64_to_real": "OPEN",
        "formal_certificate_allowed": False,
        "registry_promoted": False,
        "admission_status": "source_contract_only_pending_general_state_export",
    }
    store = StateStore(STATE)
    state = store.load()
    node = find(state, "P4.true_dh_force_descriptor_semantics")
    prior = list(node.metadata.get("source_binding_contract_reviews", []))
    changed = entry not in prior
    if changed:
        prior.append(entry)
        node.metadata["source_binding_contract_reviews"] = prior
    desired = {
        "status": status,
        "review_sha256": entry["review_artifact"]["sha256"],
        "artifact_hash_matches": matched,
        "zero_state_witness": "AUDITABLE_STATE_CONTRACT_PASS",
        "general_source_force_binding": "OPEN",
        "general_descriptor_binding": "OPEN",
        "deployed_tau_equivalence": "NOT_CLAIMED",
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    if node.metadata.get("source_binding_contract") != desired:
        node.metadata["source_binding_contract"] = desired
        changed = True
    if changed:
        state.event(
            "routeb_force_source_binding_contract_recorded",
            node_id=node.id,
            review_status=status,
            zero_state_witness="AUDITABLE_STATE_CONTRACT_PASS",
            artifact_hash_binding="PASS" if all(matched.values()) else "OPEN_STALE_HASH",
            general_source_binding="OPEN",
            registry_promoted=False,
            formal_certificate_allowed=False,
        )
        state.validate()
        store.save(state)
    print({
        "status": "recorded" if changed else "already_recorded",
        "review_status": status,
        "artifact_hash_matches": matched,
        "state_revision": store.load().revision,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
