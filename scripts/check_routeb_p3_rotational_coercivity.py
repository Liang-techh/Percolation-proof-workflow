"""Check the source shape for the P3 rotational block-coercivity target.

The checker is deliberately symbolic/source-level.  It does not sample q,
diagonalize Float64 matrices, or claim that the exact-real rotation argument
has already been bound to the implementation.
"""
from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT.parent / "6dof_sos_optimized" / "6dof_sos_optimized" / "routeB_dense_Mq" / "dhport_lib.jl"


def audit_source(text: str) -> dict[str, object]:
    required = {
        "rotational_identity": "Jw[:, jj] = z[:, jj]",
        "isotropic_link_inertia": "Ii = (I_val[ii] / 3)",
        "rotational_mass_term": "Jw' * (Ri * Ii * Ri') * Jw",
        "joint4_twist": "0.0 0.19 0.0 -pi/2",
        "explicit_regularizer": "M + Float64(regularization) .* Matrix{Float64}(I, 6, 6)",
    }
    errors = [name for name, fragment in required.items() if fragment not in text]
    match = re.search(r"I_val\s*=\s*\[([^]]+)\]", text)
    inertia = []
    if match:
        inertia = [Fraction(token.strip()) for token in match.group(1).split(",")]
    expected = [Fraction(1, 5), Fraction(1, 10), Fraction(1, 20)]
    if len(inertia) < 6 or inertia[3:6] != expected:
        errors.append("link_4_5_6_inertia_constants_not_bound")
    return {
        "status": "SOURCE_SHAPE_PASS" if not errors else "OPEN_FAIL_CLOSED",
        "errors": errors,
        "unregularized_block_lower_bound": [["7/60", "0"], ["0", "1/20"]],
        "regularized_block_lower_bound": [["7/60+1/1000000", "0"], ["0", "1/20+1/1000000"]],
        "unregularized_inverse_norm_upper": "20",
        "regularized_inverse_norm_upper": "20000000/1000001",
        "exact_real_rotation_binding_required": True,
        "formal_certificate_allowed": False,
        "registry_eligible": False,
    }


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SOURCE
    if not path.is_file():
        print(json.dumps({
            "status": "OPEN_FAIL_CLOSED",
            "errors": ["missing_source", str(path)],
            "formal_certificate_allowed": False,
            "registry_eligible": False,
        }, indent=2))
        return 2
    result = audit_source(path.read_text(encoding="utf-8", errors="replace"))
    result["source"] = str(path)
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "SOURCE_SHAPE_PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
