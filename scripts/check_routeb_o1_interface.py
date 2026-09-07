"""Check the coordinator-owned O1 interface before a Lean compile receipt.

This is a structural statement/source gate.  It deliberately returns a
pending result when the interface is sound but uncompiled; it is not a proof
checker and cannot promote a registry entry.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "artifacts/routeb_6dof/state.json"
RECEIPT = ROOT / "artifacts/task_routeb_exact_real_coefficient_identity_20260907/RECEIPT.json"
OUT = ROOT / "artifacts/task_routeb_exact_real_coefficient_identity_20260907/INTERFACE_CHECK.json"


def find_node(state: dict, name: str) -> dict:
    for node in state.get("nodes", {}).values():
        if node.get("name") == name:
            return node
    raise ValueError(f"missing node: {name}")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def main() -> int:
    state = json.loads(STATE.read_text(encoding="utf-8"))
    draft = json.loads(RECEIPT.read_text(encoding="utf-8"))
    node = find_node(state, "P4.true_dh_exact_real_coefficient_identity")
    statement = node.get("statement", "")
    definition = draft.get("definition", "")
    assumptions = draft.get("assumptions", {})
    matrices = assumptions.get("matrices", {})
    equations = assumptions.get("equations", [])
    checks = {
        "node_statement_uses_R_port": "R_port*a_B=r_B" in statement,
        "node_statement_has_negative_port_formula": "R_port=-M_BD*M_DD^(-1)*(M_DB-M0_DB)" in statement,
        "draft_definition_has_negative_port_formula": "R_port = -(M_BD * M_DD_inv * DeltaM_DB)" == definition,
        "column_vector_action": draft.get("dimension_audit", {}).get("column_action") == "Matrix.mulVec",
        "product_order": draft.get("dimension_audit", {}).get("product_order") == "(B×D)(D×D)(D×B)=B×B",
        "left_inverse_present": assumptions.get("minimal_inverse_obligation") == "M_DD_inv * M_DD = 1",
        "D_balance_present": "M_DD.mulVec v + DeltaM_DB.mulVec a_B = 0" in equations,
        "B_balance_present": "r_B - M_BD.mulVec v = 0" in equations,
        "matrix_shapes_present": set(matrices) == {"M_DD", "M_DD_inv", "DeltaM_DB", "M_BD"},
        "uncompiled_boundary_explicit": draft.get("verification", {}).get("compile_claim") is False,
        "registry_boundary_explicit": draft.get("verification", {}).get("registry_promotion") is False,
    }
    ok = all(checks.values())
    result = {
        "schema_version": 1,
        "status": "O1_INTERFACE_PENDING_LEAN_COMPILE" if ok else "O1_INTERFACE_REJECTED",
        "node": node["name"],
        "node_id": next(node_id for node_id, value in state["nodes"].items() if value is node),
        "state_revision": state.get("revision"),
        "checks": checks,
        "source_receipt": {"path": str(RECEIPT.resolve()), "sha256": sha(RECEIPT)},
        "compile_claim": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(result)
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
