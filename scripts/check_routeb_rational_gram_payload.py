"""Check the exact-rational Gram payload behind the Route-B tail PMI candidate."""
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
    audit_routeb_physical_rational_gram,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=TARGET)
    args = parser.parse_args()
    audit = args.root / "routeB_tail_pmi_scalar_gram_rational_audit.csv"
    gram = args.root / "routeB_tail_pmi_scalar_gram_rational.csv"
    basis = args.root / "routeB_tail_pmi_scalar_gram_basis.csv"
    source = args.root / "dhport_lib.jl"
    artifact_bytes = b"".join(path.read_bytes() for path in (audit, gram, basis))
    result = audit_routeb_physical_rational_gram(
        audit.read_text(encoding="utf-8"),
        gram.read_text(encoding="utf-8"),
        basis.read_text(encoding="utf-8"),
        artifact_sha256=hashlib.sha256(artifact_bytes).hexdigest(),
        source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
    )
    print(json.dumps({
        "status": result.status,
        "artifact_sha256": result.artifact_sha256,
        "source_sha256": result.source_sha256,
        "gram_blocks": result.gram_blocks,
        "max_gram_dimension": result.max_gram_dimension,
        "min_ldl_pivot": (str(result.min_ldl_pivot)
                           if result.min_ldl_pivot is not None else None),
        "errors": result.errors,
        "formal_certificate_allowed": result.formal_certificate_allowed,
        "registry_eligible": result.registry_eligible,
    }, ensure_ascii=False, indent=2))
    return 0 if result.status == "EXACT_RATIONAL_GRAM_CANDIDATE" else 2


if __name__ == "__main__":
    raise SystemExit(main())
