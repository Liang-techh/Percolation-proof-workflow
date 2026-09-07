"""Check the exact scalar lambda relations used by the Route-B Schur ledger.

This is a diagnostic contract checker, not a proof admission tool.  It uses
high-precision Decimal reconstruction and reports the quantization error in
the CSV fields; rounded text is not mistaken for an exact rational receipt.
"""
from __future__ import annotations

import csv
from collections import defaultdict
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path

getcontext().prec = 80


ROOT = Path(__file__).resolve().parents[1]
LEDGER = (ROOT.parent / "6dof_sos_optimized" / "6dof_sos_optimized" /
          "routeB_dense_Mq" / "routeB_compact_combined_schur_partition_ledger.csv")


def dec(value: str) -> Decimal:
    return Decimal(value.strip())


def fraction(value: str) -> Fraction:
    """Treat a declared decimal field as its exact quantized rational text."""
    return Fraction(value.strip())


def conservative_floor(value: Fraction, digits: int = 12) -> Fraction:
    """Return a decimal-grid lower bound, never larger than ``value``."""
    scale = 10 ** digits
    return Fraction((value.numerator * scale) // value.denominator, scale)


def audit_ledger() -> dict[str, object]:
    with LEDGER.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    required = {
        "cell_port_pmi_gamma", "external_candidate_gamma", "lambda",
        "lambda_upper_from_gamma", "candidate_margin",
        "admissible_fixed_lambda", "lambda_lower_strict", "eta", "box_id",
    }
    missing = sorted(required - set(rows[0])) if rows else sorted(required)
    if missing:
        raise ValueError(f"missing columns: {', '.join(missing)}")

    relation_errors = []
    admission_errors = []
    max_upper_error = Decimal(0)
    max_margin_error = Decimal(0)
    by_eta: dict[str, dict[str, object]] = defaultdict(
        lambda: {"rows": 0, "admissible": 0, "rejected": 0,
                 "min_lambda_upper": None, "first_rejected": None})
    upper_tolerance = Decimal("1e-12")
    margin_tolerance = Decimal("1e-15")
    for index, row in enumerate(rows, start=2):
        cell = dec(row["cell_port_pmi_gamma"])
        external = dec(row["external_candidate_gamma"])
        lam = dec(row["lambda"])
        upper = dec(row["lambda_upper_from_gamma"])
        margin = dec(row["candidate_margin"])
        eta_stats = by_eta[row["eta"]]
        eta_stats["rows"] += 1
        if row["lambda_lower_strict"].strip() != "1.0":
            relation_errors.append((index, "lambda_lower_strict"))
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
        if observed_admissible:
            eta_stats["admissible"] += 1
        else:
            eta_stats["rejected"] += 1
            if eta_stats["first_rejected"] is None:
                eta_stats["first_rejected"] = {
                    "row": index,
                    "box_id": row["box_id"],
                    "theta": row.get("theta"),
                    "lambda": row["lambda"],
                    "lambda_upper": row["lambda_upper_from_gamma"],
                    "candidate_margin": row["candidate_margin"],
                }
        current_min = eta_stats["min_lambda_upper"]
        if current_min is None or upper < current_min:
            eta_stats["min_lambda_upper"] = upper
        if observed_admissible != expected_admissible:
            admission_errors.append((index, observed_admissible, expected_admissible))

    for stats in by_eta.values():
        if stats["min_lambda_upper"] is not None:
            stats["min_lambda_upper"] = str(stats["min_lambda_upper"])

    # A useful repair candidate is a single fixed rational lambda reused for
    # every row of one declared eta partition.  This is still only a ledger
    # witness: it says nothing about cells absent from the artifact or about
    # the true-DH/source and Lean gates.
    uniform_lambda_witnesses: dict[str, dict[str, object]] = {}
    for eta in sorted(by_eta):
        eta_rows = [row for row in rows if row["eta"] == eta]
        for lambda_text in ("2.0", "1.5", "1.25"):
            selected = [row for row in eta_rows if row["lambda"] == lambda_text]
            margins = [dec(row["candidate_margin"]) for row in selected]
            exact_margins = [fraction(row["candidate_margin"]) for row in selected]
            key = f"eta={eta},lambda={lambda_text}"
            uniform_lambda_witnesses[key] = {
                "row_count": len(selected),
                "distinct_boxes": len({row["box_id"] for row in selected}),
                "all_admissible": bool(selected) and all(
                    row["admissible_fixed_lambda"].strip().lower() == "true"
                    for row in selected
                ),
                "min_candidate_margin": str(min(margins)) if margins else None,
                "min_candidate_margin_exact": (
                    str(min(exact_margins)) if exact_margins else None
                ),
                "conservative_margin_lower_bound_1e-12": (
                    str(conservative_floor(min(exact_margins)))
                    if exact_margins else None
                ),
                "proof_boundary": "declared ledger rows only; not global coverage",
            }

    result = {
        "ledger": str(LEDGER),
        "rows": len(rows),
        "relation_errors": len(relation_errors),
        "admission_errors": len(admission_errors),
        "max_upper_abs_error": str(max_upper_error),
        "max_margin_abs_error": str(max_margin_error),
        "upper_tolerance": str(upper_tolerance),
        "margin_tolerance": str(margin_tolerance),
        "per_eta": dict(sorted(by_eta.items())),
        "uniform_lambda_witnesses": uniform_lambda_witnesses,
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
