"""Record the exact binary64 seam for the deployed central-FD step."""
from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
import struct
import sys

ROOT = Path(__file__).resolve().parents[1]
ROUTE_B = ROOT.parent / "6dof_sos_optimized" / "6dof_sos_optimized"
SOURCE = ROUTE_B / "robot_final" / "dhport_lib.jl"
BOUNDARY = ROUTE_B / "routeB_dense_Mq" / "P5_COMPACT_EXACT_REAL_MODEL_BOUNDARY.md"
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
    for path in (SOURCE, BOUNDARY):
        if not path.is_file():
            raise FileNotFoundError(path)
    source_text = SOURCE.read_text(encoding="utf-8", errors="replace")
    boundary_text = BOUNDARY.read_text(encoding="utf-8", errors="replace")
    h_float = 1e-5
    h_float_exact = Fraction.from_float(h_float)
    h_exact = Fraction(1, 100000)
    bits = struct.unpack("<Q", struct.pack("<d", h_float))[0]
    delta = h_float_exact - h_exact
    audit = {
        "schema_version": 1,
        "status": "OPEN_FD_STEP_OUTWARD_INCLUSION_REQUIRED",
        "deployed_literal": "1e-5",
        "deployed_float64_bits_hex": f"0x{bits:016x}",
        "deployed_float64_exact_value": str(h_float_exact),
        "analytic_exact_real_value": str(h_exact),
        "deployed_minus_analytic": str(delta),
        "ordering": "0 < exact_real_value < float64_value" if delta > 0 else "unexpected",
        "outward_interval": [str(h_exact), str(h_float_exact)],
        "source_literal_present": "const CG_FINITE_DIFF_STEP = 1e-5" in source_text,
        "boundary_exact_value_present": "fd_step = h = 1/100000" in boundary_text,
        "source_artifacts": [ref(SOURCE), ref(BOUNDARY)],
        "remaining_obligation": (
            "bind the same h through every mass/potential endpoint and 2h division, "
            "then charge the resulting outward error in C/G enclosure"
        ),
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    if not audit["source_literal_present"] or not audit["boundary_exact_value_present"]:
        raise ValueError("FD-step source seam is missing")
    store = StateStore(STATE)
    state = store.load()
    node = find(state, "P4.true_dh_float64_evaluator_enclosure")
    changed = node.metadata.get("fd_step_semantics") != audit
    node.metadata["fd_step_semantics"] = audit
    unresolved = list(node.metadata.get("unresolved", []))
    marker = "Float64_fd_step_outward_inclusion"
    if marker not in unresolved:
        unresolved.append(marker)
        node.metadata["unresolved"] = unresolved
        changed = True
    if changed:
        state.event("routeb_fd_step_semantics_recorded", node_id=node.id,
                    status=audit["status"], deployed_minus_analytic=str(delta),
                    registry_promoted=False, formal_certificate_allowed=False)
        state.validate()
        store.save(state)
    print({"status": "recorded" if changed else "already_recorded",
           "audit_status": audit["status"], "deployed_minus_analytic": str(delta),
           "state_revision": store.load().revision, "formal_certificate_allowed": False,
           "registry_promoted": False})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
