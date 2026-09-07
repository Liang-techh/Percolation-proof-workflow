"""Recompute the O0 conditional baseline ratio and preserve a small receipt."""
from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from fractions import Fraction
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from percolation_workflow.routeb_regularizer_semantics import (  # noqa: E402
    derive_routeb_physical_baseline_factor,
)


INPUT = ROOT / "artifacts/routeb_6dof/o0_physical_baseline_derivation_20260907.json"
OUTPUT = ROOT / "artifacts/routeb_6dof/o0_physical_baseline_derivation_20260907.check.json"


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest().upper()


def main() -> None:
    document = json.loads(INPUT.read_text(encoding="utf-8"))
    result = derive_routeb_physical_baseline_factor(
        Fraction(document["mass_block_derivation"]["mass_lower"]),
        Fraction(document["metric_upper"]),
        source_key=document["source_key"],
        theta=1,
        rho_rounded=0,
    )
    expected = Fraction(document["L_base"])
    if result.L_base != expected:
        raise AssertionError(f"L_base mismatch: {result.L_base} != {expected}")
    if result.status != "CONDITIONAL_EXACT_PHYSICAL_BASELINE":
        raise AssertionError(f"unexpected status: {result.status}")
    if result.baseline_bound_proven or result.schur_margin_consumed:
        raise AssertionError("conditional derivation crossed a closed gate")
    receipt = {
        "schema": "routeb.o0.physical_baseline_derivation.check.v1",
        "status": "PASS_CONDITIONAL_FAIL_CLOSED",
        "input_sha256": digest(INPUT),
        "mass_lower": str(result.mass_lower),
        "metric_upper": str(result.metric_upper),
        "L_base": str(result.L_base),
        "strict_margin_at_theta_1_rho_0": str(result.strict_margin),
        "baseline_bound_proven": result.baseline_bound_proven,
        "schur_margin_consumed": result.schur_margin_consumed,
        "formal_certificate_allowed": result.formal_certificate_allowed,
        "registry_promoted": result.registry_eligible,
    }
    OUTPUT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(receipt)


if __name__ == "__main__":
    main()
