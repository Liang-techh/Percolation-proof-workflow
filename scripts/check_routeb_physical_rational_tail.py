"""Check the exact-rational Route-B nominal distal tail seam."""
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
    audit_routeb_physical_rational_tail,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=TARGET)
    args = parser.parse_args()
    paths = [
        args.root / "routeB_physical_rational_descriptor_bridge.csv",
        args.root / "routeB_physical_rational_tail_pmi_scalar_meta.csv",
        args.root / "routeB_physical_rational_tail_pmi_scalar.csv",
    ]
    source_path = args.root / "dhport_lib.jl"
    artifact_bytes = b"".join(path.read_bytes() for path in paths)
    result = audit_routeb_physical_rational_tail(
        *(path.read_text(encoding="utf-8") for path in paths),
        artifact_sha256=hashlib.sha256(artifact_bytes).hexdigest(),
        source_sha256=hashlib.sha256(source_path.read_bytes()).hexdigest(),
    )
    print(json.dumps({
        "status": result.status,
        "artifact_sha256": result.artifact_sha256,
        "source_sha256": result.source_sha256,
        "scalar_terms": result.scalar_terms,
        "scalar_max_total_cs_degree": result.scalar_max_total_cs_degree,
        "errors": result.errors,
        "formal_certificate_allowed": result.formal_certificate_allowed,
        "registry_eligible": result.registry_eligible,
    }, ensure_ascii=False, indent=2))
    return 0 if result.status == "EXACT_RATIONAL_TAIL_CANDIDATE" else 2


if __name__ == "__main__":
    raise SystemExit(main())
