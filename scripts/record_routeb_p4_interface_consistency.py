"""Persist the P4 interface-consistency lint as non-authoritative state."""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from check_routeb_p4_interface_consistency import audit_state
from percolation_workflow.store import StateStore


def find(state, name: str):
    for node in state.nodes.values():
        if node.name == name:
            return node
    raise ValueError(f"missing node: {name}")


def main() -> int:
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    result = audit_state()
    if result.get("status") != "PASS":
        raise ValueError(f"P4 interface lint failed: {result}")
    checker = ROOT / "scripts/check_routeb_p4_interface_consistency.py"
    receipt = {
        "checker": str(checker),
        "checker_sha256": hashlib.sha256(checker.read_bytes()).hexdigest(),
        "status": "diagnostic_pass",
        "state_revision_checked": result["revision"],
        "checks": result["checks"],
        "registry": result["registry"],
        "registry_promoted": False,
        "formal_certificate_allowed": False,
        "proof_boundary": result["proof_boundary"],
    }
    node = find(state, "P4.combined_schur_port_energy_adapter")
    if node.metadata.get("interface_consistency_receipt") == receipt:
        print({"status": "already_recorded", "state_revision": state.revision})
        return 0
    node.metadata["interface_consistency_receipt"] = receipt
    state.event(
        "routeb_p4_interface_consistency_recorded",
        node_id=node.id,
        receipt=receipt,
        registry_promoted=False,
        formal_certificate_allowed=False,
    )
    store.save(state)
    print({"status": "recorded", "node_id": node.id,
           "state_revision": state.revision})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
