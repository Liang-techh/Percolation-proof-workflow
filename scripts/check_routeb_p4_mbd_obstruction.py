"""Check the exact ``M_BD(0)`` projection obstruction from a rational CSV."""
from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from percolation_workflow.routeb_mbd_obstruction import (  # noqa: E402
    audit_routeb_mbd_projection,
)

DEFAULT_SOURCE = (
    ROOT.parent / "6dof_sos_optimized" / "6dof_sos_optimized" /
    "routeB_dense_Mq" / "routeB_fourier_mass_BD_rational.csv"
)


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
    result = audit_routeb_mbd_projection(path.read_text(encoding="utf-8"))
    payload = {
        "status": result.status,
        "matrix_at_zero": [[str(x) for x in row] for row in result.matrix_at_zero],
        "first_column_vector": [str(x) for x in result.first_column_vector],
        "projection_factor": str(result.projection_factor),
        "errors": result.errors,
        "countermodel": "a_D=lambda*e1 with fixed block projection; no finite block-only remote bound",
        "formal_certificate_allowed": result.formal_certificate_allowed,
        "registry_eligible": result.registry_eligible,
        "source": str(path),
    }
    print(json.dumps(payload, indent=2))
    return 0 if result.status == "PROJECTION_OBSTRUCTION_EXACT" else 2


if __name__ == "__main__":
    raise SystemExit(main())
