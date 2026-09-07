"""Check the exact scalar lambda relations used by the Route-B Schur ledger.

This is a diagnostic contract checker, not a proof admission tool.  It uses
high-precision Decimal reconstruction and reports the quantization error in
the CSV fields; rounded text is not mistaken for an exact rational receipt.
"""
from __future__ import annotations

import csv
from decimal import Decimal, getcontext
from pathlib import Path

getcontext().prec = 80


ROOT = Path(__file__).resolve().parents[1]
LEDGER = (ROOT.parent / "6dof_sos_optimized" / "6dof_sos_optimized" /
          "routeB_dense_Mq" / "routeB_compact_combined_schur_partition_ledger.csv")


def dec(value: str) -> Decimal:
    return Decimal(value.strip())


def audit_ledger() -> dict[str, object]:
    with LEDGER.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    required = {
        "cell_port_pmi_gamma", "external_candidate_gamma", "lambda",
        "lambda_upper_from_gamma", "candidate_margin",
        "admissible_fixed_lambda",
    }
    missing = sorted(required - set(rows[0])) if rows else sorted(required)
    if missing:
        raise ValueError(f"missing columns: {', '.join(missing)}")

    relation_errors = []
    admission_errors = []
    max_upper_error = Decimal(0)
    max_margin_error = Decimal(0)
    upper_tolerance = Decimal("1e-12")
    margin_tolerance = Decimal("1e-15")
    for index, row in enumerate(rows, start=2):
        cell = dec(row["cell_port_pmi_gamma"])
        external = dec(row["external_candidate_gamma"])
        lam = dec(row["lambda"])
        upper = dec(row["lambda_upper_from_gamma"])
        margin = dec(row["candidate_margin"])
        if cell <= 0:
            relation_errors.append((index, "cell_port_pmi_gamma <= 0"))
            continue
        upper_error = abs(upper - external / cell)
        margin_error = abs(margin - (external - lam * cell))
        max_upper_error = max(max_upper_error, upper_error)
        max_margin_error = max(max_margin_error, margin_error)
        if upper_error > upper_tolerance:
            relation_errors.append((index, "lambda_upper_from_gamma"))
        if margin_error > margin_tolerance:
            relation_errors.append((index, "candidate_margin"))
        expected_admissible = lam > 1 and margin > 0
        observed_admissible = row["admissible_fixed_lambda"].strip().lower() == "true"
        if observed_admissible != expected_admissible:
            admission_errors.append((index, observed_admissible, expected_admissible))

    result = {
        "ledger": str(LEDGER),
        "rows": len(rows),
        "relation_errors": len(relation_errors),
        "admission_errors": len(admission_errors),
        "max_upper_abs_error": str(max_upper_error),
        "max_margin_abs_error": str(max_margin_error),
        "upper_tolerance": str(upper_tolerance),
        "margin_tolerance": str(margin_tolerance),
        "status": "PASS" if not relation_errors and not admission_errors else "FAIL",
        "proof_boundary": "diagnostic scalar contract only; no Lean, source, coverage, or registry admission",
    }
    if relation_errors or admission_errors:
        result["relation_examples"] = relation_errors[:5]
        result["admission_examples"] = admission_errors[:5]
    return result


def main() -> int:
    result = audit_ledger()
    print(result)
    relation_errors = result["relation_errors"]
    admission_errors = result["admission_errors"]
    if relation_errors or admission_errors:
        # The examples are already included in the machine-readable result.
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
