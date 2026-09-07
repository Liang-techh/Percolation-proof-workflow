"""Audit the exact Route-B nominal distal bridge CSV pair."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
TARGET = (ROOT.parent / "6dof_sos_optimized" / "6dof_sos_optimized" /
          "routeB_dense_Mq")
sys.path.insert(0, str(ROOT / "src"))

from percolation_workflow.routeb_nominal_distal_contract import (
    audit_routeb_nominal_distal_bridge,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=TARGET)
    args = parser.parse_args()
    audit_path = args.root / "routeB_compact_dh_nominal_distal_bridge_audit.csv"
    interface_path = args.root / "routeB_compact_nominal_descriptor_interface.csv"
    audit_text = audit_path.read_text(encoding="utf-8")
    interface_text = interface_path.read_text(encoding="utf-8")
    artifact_bytes = audit_path.read_bytes() + interface_path.read_bytes()
    source_hash = next(
        (line.split(",", 1)[1] for line in audit_text.splitlines()
         if line.startswith("controller_source_sha256,")),
        None,
    )
    result = audit_routeb_nominal_distal_bridge(
        audit_text,
        interface_text,
        artifact_sha256=hashlib.sha256(artifact_bytes).hexdigest(),
        source_sha256=source_hash,
    )
    print(json.dumps({
        "status": result.status,
        "artifact_sha256": result.artifact_sha256,
        "source_sha256": result.source_sha256,
        "block_coordinates": result.block_coordinates,
        "remote_coordinates": result.remote_coordinates,
        "errors": result.errors,
        "formal_certificate_allowed": result.formal_certificate_allowed,
        "registry_eligible": result.registry_eligible,
    }, ensure_ascii=False, indent=2))
    return 0 if result.status == "EXACT_DESCRIPTOR_BRIDGE_CANDIDATE" else 2


if __name__ == "__main__":
    raise SystemExit(main())
