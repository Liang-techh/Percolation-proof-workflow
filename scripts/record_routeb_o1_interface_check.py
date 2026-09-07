"""Attach the structural O1 interface-check result without promotion."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
CHECK = ROOT / "artifacts/task_routeb_exact_real_coefficient_identity_20260907/INTERFACE_CHECK.json"
sys.path.insert(0, str(ROOT / "src"))

from percolation_workflow.store import StateStore  # noqa: E402


def ref(path: Path) -> dict[str, str]:
    return {"path": str(path.resolve()),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest().upper()}


def find(state, name: str):
    for node in state.nodes.values():
        if node.name == name:
            return node
    raise ValueError(f"missing node: {name}")


def main() -> int:
    if not CHECK.is_file():
        raise FileNotFoundError(CHECK)
    data = json.loads(CHECK.read_text(encoding="utf-8"))
    if data.get("status") != "O1_INTERFACE_PENDING_LEAN_COMPILE":
        raise ValueError(f"unexpected O1 interface status: {data.get('status')!r}")
    if data.get("compile_claim") is not False or data.get("registry_promoted") is not False:
        raise ValueError("interface check crosses the admission boundary")

    state_store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = state_store.load()
    node = find(state, "P4.true_dh_exact_real_coefficient_identity")
    check = {
        "schema_version": 1,
        "status": data["status"],
        "state_revision_checked": data["state_revision"],
        "checks": data["checks"],
        "artifact": ref(CHECK),
        "statement_comparator_status": "pending_compile_and_coordinator_receipt",
        "compile_claim": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    changed = node.metadata.get("o1_interface_check") != check
    node.metadata["o1_interface_check"] = check
    if changed:
        state.event(
            "routeb_o1_interface_check_recorded",
            node_id=node.id,
            check_status=check["status"],
            check_artifact=check["artifact"],
            registry_promoted=False,
            formal_certificate_allowed=False,
        )
        state.validate()
        state_store.save(state)
    print({"status": "recorded" if changed else "already_recorded",
           "node_id": node.id, "check_status": check["status"],
           "state_revision": state.revision})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
