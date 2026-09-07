"""Audit the finite declared ``lambda=2, theta=1`` witness fold.

This is an exact rational data-contract checker, not a Lean proof.  It folds
the two declared ledger partitions into canonical one-row-per-box witness
sets and keeps source binding, true-DH coverage, comparator, and registry
admission explicitly false.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LEDGER = (ROOT.parent / "6dof_sos_optimized" / "6dof_sos_optimized"
          / "routeB_dense_Mq" / "routeB_compact_combined_schur_partition_ledger.csv")

EXPECTED_BOXES = {"2.7": 256, "5.6": 321}
DECIMAL_TOLERANCE = Fraction(1, 10**15)


def rational(value: str) -> Fraction:
    """Interpret a declared decimal as its exact textual rational."""
    return Fraction(value.strip())


def digest_payload(payload: object) -> str:
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True,
                         separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest().upper()


def canonical_row(row: dict[str, str]) -> dict[str, str]:
    return {key: row[key] for key in (
        "eta", "box_id", "lambda", "theta", "cell_port_pmi_gamma",
        "external_candidate_gamma", "lambda_upper_from_gamma",
        "candidate_margin", "admissible_fixed_lambda",
    )}


def audit(path: Path = LEDGER) -> dict[str, object]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    required = set(canonical_row({key: "" for key in (
        "eta", "box_id", "lambda", "theta", "cell_port_pmi_gamma",
        "external_candidate_gamma", "lambda_upper_from_gamma",
        "candidate_margin", "admissible_fixed_lambda",
    )}))
    if not rows or required - set(rows[0]):
        raise ValueError(f"ledger missing required columns: {sorted(required - set(rows[0]) if rows else required)}")

    partitions: dict[str, dict[str, object]] = {}
    errors: list[str] = []
    for eta, expected in EXPECTED_BOXES.items():
        selected = [row for row in rows
                    if row["eta"] == eta and row["lambda"] == "2.0"
                    and row.get("theta") == "1.0"]
        witnesses = [canonical_row(row) for row in selected]
        witnesses.sort(key=lambda row: int(row["box_id"]))
        box_ids = [row["box_id"] for row in witnesses]
        local_errors: list[str] = []
        if len(witnesses) != expected:
            local_errors.append(f"row_count={len(witnesses)} expected={expected}")
        if len(set(box_ids)) != expected:
            local_errors.append(f"distinct_boxes={len(set(box_ids))} expected={expected}")
        if len(box_ids) != len(set(box_ids)):
            local_errors.append("duplicate_box_id")
        # ``box_id`` is a global ledger label, not the ordinal of this
        # lambda-slice.  A valid finite fold therefore requires uniqueness,
        # not the false assumption that the selected labels are 1..N.
        global_gap = [index for index in range(1, max(map(int, box_ids), default=0) + 1)
                      if str(index) not in set(box_ids)]

        margins: list[Fraction] = []
        floors: list[Fraction] = []
        for row in selected:
            cell = rational(row["cell_port_pmi_gamma"])
            external = rational(row["external_candidate_gamma"])
            upper = rational(row["lambda_upper_from_gamma"])
            margin = rational(row["candidate_margin"])
            margins.append(margin)
            floors.append(Fraction((margin.numerator * 10**12) // margin.denominator, 10**12))
            if row["admissible_fixed_lambda"].strip().lower() != "true":
                local_errors.append(f"box={row['box_id']}:not_admissible")
            if not (cell > 0 and upper > 2 and margin > 0):
                local_errors.append(f"box={row['box_id']}:strict_witness_failed")
            if abs(external - 2 * cell - margin) > DECIMAL_TOLERANCE:
                local_errors.append(f"box={row['box_id']}:margin_relation_outside_tolerance")
            if floors[-1] <= 0:
                local_errors.append(f"box={row['box_id']}:nonpositive_1e-12_floor")

        partition = {
            "eta": eta,
            "lambda": "2.0",
            "theta": "1.0",
            "expected_boxes": expected,
            "row_count": len(witnesses),
            "distinct_boxes": len(set(box_ids)),
            "one_row_per_box": len(box_ids) == len(set(box_ids)),
            "box_id_min": min(map(int, box_ids)) if box_ids else None,
            "box_id_max": max(map(int, box_ids)) if box_ids else None,
            "global_label_gaps_before_max": global_gap,
            "dense_box_ids": False,
            "all_admissible": not any("not_admissible" in error for error in local_errors),
            "strict_upper_and_margin": not any("strict_witness_failed" in error for error in local_errors),
            "margin_relation_within_1e-15": not any("margin_relation" in error for error in local_errors),
            "min_candidate_margin_exact": str(min(margins)) if margins else None,
            "min_conservative_floor_1e-12": str(min(floors)) if floors else None,
            "errors": local_errors,
            "witnesses": witnesses,
        }
        partition["witness_digest"] = digest_payload(witnesses)
        partitions[eta] = partition
        errors.extend(f"eta={eta}:{error}" for error in local_errors)

    folded = [partitions[eta]["witnesses"] for eta in sorted(partitions)]
    all_witnesses = [row for partition in folded for row in partition]
    result = {
        "schema": "routeb.p4.fixed_lambda.uniform_declared_fold.v1",
        "status": "PASS_EXACT_DECLARED_FINITE_FOLD_ONLY" if not errors else "FAIL",
        "ledger": str(path),
        "ledger_sha256": hashlib.sha256(path.read_bytes()).hexdigest().upper(),
        "partitions": partitions,
        "fold": {
            "partition_count": len(partitions),
            "witness_count": len(all_witnesses),
            "witness_digest": digest_payload(all_witnesses),
            "all_partition_rows_pass": not errors,
        },
        "errors": errors,
        "source_binding_proven": False,
        "true_dh_coverage_proven": False,
        "lean_compiled": False,
        "comparator_accepted": False,
        "registry_eligible": False,
        "formal_certificate_allowed": False,
        "proof_boundary": "finite declared ledger rows only; no true-DH/source/coverage claim",
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", type=Path, default=LEDGER)
    parser.add_argument("--write-receipt", type=Path)
    args = parser.parse_args()
    result = audit(args.ledger.resolve(strict=True))
    if args.write_receipt:
        args.write_receipt.parent.mkdir(parents=True, exist_ok=True)
        args.write_receipt.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                                       encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["status"].startswith("PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
