"""Check the isolated exact-rational Route-B P4 ``kc`` budget."""
from __future__ import annotations

import json
from pathlib import Path
from fractions import Fraction
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from percolation_workflow.routeb_kc_budget import derive_routeb_kc_budget  # noqa: E402


def main() -> int:
    result = derive_routeb_kc_budget()
    payload = {
        "status": result.status,
        "normalized_kc": str(result.normalized_kc),
        "force_coefficients": [str(x) for x in result.force_coefficients],
        "q_squared_cap": str(result.q_squared_cap),
        "squared_force_bound": str(result.squared_force_bound),
        "expected_squared_force_bound": "7/18750",
        "formal_certificate_allowed": result.formal_certificate_allowed,
        "registry_eligible": result.registry_eligible,
    }
    print(json.dumps(payload, indent=2))
    return 0 if (
        result.status == "EXACT_ARITHMETIC_CANDIDATE"
        and result.force_coefficients == (Fraction(1, 100), Fraction(1, 200))
        and result.squared_force_bound == Fraction(7, 18750)
    ) else 2


if __name__ == "__main__":
    raise SystemExit(main())
