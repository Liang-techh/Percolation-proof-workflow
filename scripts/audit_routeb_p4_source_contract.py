"""Audit the canonical Route-B P4 force/descriptor source seam.

This is a focused source-semantic check, not a numerical or Lean proof.  It
is intentionally cheap enough for the frontier loop and fails closed when an
old scaled adapter is supplied as if it were current.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from percolation_workflow.routeb_source_contract import (  # noqa: E402
    audit_routeb_p4_source_contract,
)


DEFAULT_TARGET = Path(
    r"C:\Users\z5242\Desktop\重构版\6dof_sos_optimized\6dof_sos_optimized"
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=Path, default=DEFAULT_TARGET)
    parser.add_argument("--adapter", type=Path, default=None)
    args = parser.parse_args()

    pmi_path = args.target / "routeB_dense_Mq" / "routeB_pmi_certificate.jl"
    dh_path = args.target / "routeB_dense_Mq" / "dhport_lib.jl"
    if not pmi_path.is_file() or not dh_path.is_file():
        print(json.dumps({
            "status": "OPEN_FAIL_CLOSED",
            "errors": ["missing_canonical_source_file"],
            "formal_certificate_allowed": False,
            "registry_eligible": False,
        }, indent=2))
        return 2

    adapter = args.adapter.read_text(encoding="utf-8") if args.adapter else None
    result = audit_routeb_p4_source_contract(
        pmi_path.read_text(encoding="utf-8", errors="replace"),
        dh_path.read_text(encoding="utf-8", errors="replace"),
        adapter,
    )
    payload = {
        "status": result.status,
        "kc": str(result.kc) if result.kc is not None else None,
        "expected_rho_kc": result.expected_rho_kc,
        "observed_adapter_rho_kc": result.observed_adapter_rho_kc,
        "remote_term_required": result.remote_term_required,
        "force_acceleration_separated": result.force_acceleration_separated,
        "errors": result.errors,
        "warnings": result.warnings,
        "formal_certificate_allowed": result.formal_certificate_allowed,
        "registry_eligible": result.registry_eligible,
        "source_paths": [str(pmi_path), str(dh_path)],
    }
    print(json.dumps(payload, indent=2))
    return 0 if result.status in {
        "SOURCE_CONTRACT_PASS", "SOURCE_AND_ADAPTER_SCALE_PASS"
    } else 2


if __name__ == "__main__":
    raise SystemExit(main())
