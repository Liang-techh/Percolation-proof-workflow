"""Check a Route-B remote-action contract JSON without admitting it."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from percolation_workflow.routeb_remote_contract import audit_routeb_remote_binding


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("receipt", type=Path)
    args = parser.parse_args()
    result = audit_routeb_remote_binding(
        json.loads(args.receipt.read_text(encoding="utf-8"))
    )
    print(json.dumps({
        "status": result.status,
        "binding_mode": result.mode,
        "required_fields": result.required_fields,
        "errors": result.errors,
        "formal_certificate_allowed": result.formal_certificate_allowed,
        "registry_eligible": result.registry_eligible,
    }, ensure_ascii=False, indent=2))
    return 0 if result.status == "STRUCTURAL_PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
