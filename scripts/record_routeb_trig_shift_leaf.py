"""Attach the exact rational Taylor leaf for the central-FD trig shift."""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ROUTE_B = ROOT.parent / "6dof_sos_optimized" / "6dof_sos_optimized"
SOURCE = ROUTE_B / "routeB_dense_Mq" / "routeB_proofgrade_trig_bounds.csv"
REPORT = ROUTE_B / "routeB_dense_Mq" / "P5_COMPACT_PROOFGRADE_TRIG_BOUNDS.md"
STATE = ROOT / "artifacts/routeb_6dof/state.json"
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
    for path in (SOURCE, REPORT):
        if not path.is_file():
            raise FileNotFoundError(path)
    with SOURCE.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    by_name = {row.get("name"): row for row in rows}
    if set(by_name) != {"sin_h", "cos_h"}:
        raise ValueError("trig leaf must contain exactly sin_h and cos_h")
    for name, row in by_name.items():
        if row.get("order") != "12" or not all(row.get(key) for key in (
            "lower_num", "lower_den", "upper_num", "upper_den", "theorem",
        )):
            raise ValueError(f"malformed exact Taylor row: {name}")
    report_text = REPORT.read_text(encoding="utf-8", errors="replace")
    required_phrases = (
        "uses no floating-point `sin` or `cos`",
        "Angle range reduction",
        "Evidence level: exact rational Taylor leaf",
    )
    if not all(phrase in report_text for phrase in required_phrases):
        raise ValueError("Taylor report does not preserve its evidence boundary")
    audit = {
        "schema_version": 1,
        "status": "EXACT_TAYLOR_SHIFT_LEAF_PRESENT_FLOAT64_BINDING_OPEN",
        "shift": "h=1/100000",
        "rows": rows,
        "source_artifacts": [ref(SOURCE), ref(REPORT)],
        "claims": {
            "exact_rational_taylor_bound_for_sin_h_cos_h": True,
            "floating_point_trig_executed": False,
            "arbitrary_dh_angle_range_reduction": False,
            "float64_libm_binding": False,
            "formal_certificate_allowed": False,
            "registry_promoted": False,
        },
        "remaining_obligation": (
            "bind the exact Taylor constants to the deployed Float64 sin/cos path, "
            "then prove angle-box range reduction and finite-DAG propagation"
        ),
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    store = StateStore(STATE)
    state = store.load()
    node = find(state, "P4.true_dh_float64_evaluator_enclosure")
    changed = node.metadata.get("trig_shift_leaf") != audit
    node.metadata["trig_shift_leaf"] = audit
    unresolved = list(node.metadata.get("unresolved", []))
    marker = "sin_cos_shift_taylor_leaf_float64_binding"
    if marker not in unresolved:
        unresolved.append(marker)
        node.metadata["unresolved"] = unresolved
        changed = True
    if changed:
        state.event("routeb_trig_shift_leaf_recorded", node_id=node.id,
                    status=audit["status"], registry_promoted=False,
                    formal_certificate_allowed=False)
        state.validate()
        store.save(state)
    print({"status": "recorded" if changed else "already_recorded",
           "audit_status": audit["status"], "state_revision": store.load().revision,
           "rows": len(rows), "formal_certificate_allowed": False,
           "registry_promoted": False})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
