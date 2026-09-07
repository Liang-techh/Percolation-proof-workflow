"""Record the scalar Float64/exact-real seam for DH pi offsets."""
from __future__ import annotations

import hashlib
import json
import math
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


def bits(value: float) -> str:
    return f"0x{struct.unpack('<Q', struct.pack('<d', value))[0]:016x}"


def main() -> int:
    for path in (SOURCE, BOUNDARY):
        if not path.is_file():
            raise FileNotFoundError(path)
    source_text = SOURCE.read_text(encoding="utf-8", errors="replace")
    boundary_text = BOUNDARY.read_text(encoding="utf-8", errors="replace")
    pi_float = math.pi
    half_float = math.pi / 2.0
    pi_float_exact = Fraction.from_float(pi_float)
    half_float_exact = Fraction.from_float(half_float)
    pi_lower, pi_upper = Fraction(333, 106), Fraction(355, 113)
    half_lower, half_upper = Fraction(333, 212), Fraction(355, 226)
    if not (pi_lower < pi_float_exact < pi_upper):
        raise ValueError("Float64 pi is outside the selected rational enclosure")
    if not (half_lower < half_float_exact < half_upper):
        raise ValueError("Float64 pi/2 is outside the selected rational enclosure")
    audit = {
        "schema_version": 1,
        "status": "OPEN_DH_OFFSET_LIBM_ENCLOSURE_REQUIRED",
        "deployed_constants": {
            "pi_literal": "pi",
            "pi_over_two_expression": "pi/2",
            "dh_offsets_observed": ["0", "-pi/2", "pi/2"],
        },
        "float64": {
            "pi_bits_hex": bits(pi_float),
            "pi_exact_dyadic": str(pi_float_exact),
            "pi_over_two_bits_hex": bits(half_float),
            "pi_over_two_exact_dyadic": str(half_float_exact),
        },
        "rational_enclosure": {
            "pi": [str(pi_lower), str(pi_upper)],
            "pi_over_two": [str(half_lower), str(half_upper)],
            "strict_containment_checked": True,
        },
        "source_literal_present": "-pi/2" in source_text and "pi/2" in source_text,
        "boundary_exact_offsets_present": "0, ±π/2" in boundary_text,
        "source_artifacts": [ref(SOURCE), ref(BOUNDARY)],
        "remaining_obligation": (
            "prove the actual sin/cos/libm outputs on every certified angle box and "
            "bind the pi/2 operation schedule; scalar pi containment alone is insufficient"
        ),
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    if not audit["source_literal_present"] or not audit["boundary_exact_offsets_present"]:
        raise ValueError("DH offset source seam is missing")
    store = StateStore(STATE)
    state = store.load()
    node = find(state, "P4.true_dh_float64_evaluator_enclosure")
    changed = node.metadata.get("dh_offset_semantics") != audit
    node.metadata["dh_offset_semantics"] = audit
    unresolved = list(node.metadata.get("unresolved", []))
    marker = "Float64_pi_offset_outward_inclusion"
    if marker not in unresolved:
        unresolved.append(marker)
        node.metadata["unresolved"] = unresolved
        changed = True
    if changed:
        state.event("routeb_dh_offset_semantics_recorded", node_id=node.id,
                    status=audit["status"], registry_promoted=False,
                    formal_certificate_allowed=False)
        state.validate()
        store.save(state)
    print({"status": "recorded" if changed else "already_recorded",
           "audit_status": audit["status"], "pi_over_two_bits_hex": bits(half_float),
           "state_revision": store.load().revision, "formal_certificate_allowed": False,
           "registry_promoted": False})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
