"""Print the exact conditional Route-B remote acceleration budget."""
from __future__ import annotations

import json

from percolation_workflow.routeb_remote_accel_budget import (
    derive_routeb_remote_acceleration_budget,
)


def main() -> int:
    result = derive_routeb_remote_acceleration_budget()
    print(json.dumps({
        "status": result.status,
        "remote_coordinates": result.remote_coordinates,
        "euclidean_squared_coefficient": str(result.euclidean_squared_coefficient),
        "coordinatewise_reference_coefficient": str(
            result.coordinatewise_reference_coefficient
        ),
        "assumptions": result.assumptions,
        "formal_certificate_allowed": result.formal_certificate_allowed,
        "registry_eligible": result.registry_eligible,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
