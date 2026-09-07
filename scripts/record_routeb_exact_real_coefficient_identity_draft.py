"""Attach the uncompiled O1 theorem interface to its frontier node."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
TASK = ROOT / "artifacts/task_routeb_exact_real_coefficient_identity_20260907"
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
    report = TASK / "REPORT.md"
    receipt = TASK / "RECEIPT.json"
    for path in (report, receipt):
        if not path.is_file():
            raise FileNotFoundError(path)
    receipt_data = json.loads(receipt.read_text(encoding="utf-8"))
    if receipt_data.get("status") != "INTERFACE_DRAFT__UNCOMPILED":
        raise ValueError("O1 draft is not explicitly uncompiled")
    interface = {
        "schema_version": 1,
        "status": receipt_data["status"],
        "theorem": receipt_data["theorem"],
        "definition": receipt_data["definition"],
        "assumptions": receipt_data["assumptions"],
        "dimension_audit": receipt_data["dimension_audit"],
        "decomposition": [
            {
                "id": "O1.1",
                "name": "eliminate_D_velocity",
                "status": "INTERFACE_DRAFT__UNCOMPILED",
                "interface": "RouteB.O1.BlockEquations",
            },
            {
                "id": "O1.2",
                "name": "apply_explicit_left_inverse",
                "status": "INTERFACE_DRAFT__UNCOMPILED",
                "interface": "RouteB.O1.LeftInverseMulVec",
            },
            {
                "id": "O1.3",
                "name": "assemble_port_product",
                "status": "INTERFACE_DRAFT__UNCOMPILED",
                "interface": "RouteB.O1.PortCoefficientIdentity",
            },
            {
                "id": "O1.4",
                "name": "bind_true_dh_source_blocks",
                "status": "OPEN",
                "interface": "RouteB.O1.TrueDHBlockExtraction",
            },
        ],
        "report": ref(report),
        "receipt": ref(receipt),
        "compile_claim": False,
        "source_binding": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }

    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    node = find(state, "P4.true_dh_exact_real_coefficient_identity")
    changed = False
    if node.metadata.get("o1_interface_draft") != interface:
        node.metadata["o1_interface_draft"] = interface
        changed = True
    unresolved = list(node.metadata.get("unresolved", []))
    for item in (
        "uncompiled_exact_real_interface",
        "typed_block_extraction_binding",
        "M_DD_left_inverse_witness",
        "Matrix_mulVec_orientation_and_associativity",
    ):
        if item not in unresolved:
            unresolved.append(item)
    if unresolved != node.metadata.get("unresolved"):
        node.metadata["unresolved"] = unresolved
        changed = True
    contract = dict(node.metadata.get("frontier_repair_contract") or {})
    contract.update({
        "schema_version": 1,
        "next_agent_action": (
            "compile the exact-real O1 theorem against the current pin, then return "
            "zero-sorry, allowed-axiom, statement-comparator, and source-binding receipts"
        ),
        "preserve_semantic_boundary": (
            "keep the left-inverse algebra separate from block extraction, Float64 "
            "enclosure, norms, coverage, and physical source binding"
        ),
    })
    if node.metadata.get("frontier_repair_contract") != contract:
        node.metadata["frontier_repair_contract"] = contract
        changed = True
    if changed:
        state.event(
            "routeb_o1_exact_real_coefficient_identity_draft_recorded",
            node_id=node.id,
            draft_status=interface["status"],
            report=interface["report"],
            receipt=interface["receipt"],
            registry_promoted=False,
            formal_certificate_allowed=False,
        )
        state.validate()
        store.save(state)
    print({"status": "recorded" if changed else "already_recorded",
           "node_id": node.id, "draft_status": interface["status"],
           "state_revision": state.revision})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
