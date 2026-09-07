"""Check the exact body-2 target coefficients against the frozen trace CSV."""
from __future__ import annotations

import csv
from fractions import Fraction
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "artifacts/task_routeb_body_trace_sink_current/outputs/routeB_fourier_mass_body_trace.csv"
OUT = ROOT / "examples/routeb_b45_source_comparator_lean/O1_BODY_2_TARGET_CHECK.json"


def rational(num: str, den: str) -> Fraction:
    return Fraction(int(num), int(den))


def main() -> None:
    with CSV.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    body2 = [row for row in rows if int(row["body"]) == 2]
    actual: dict[tuple[int, int, tuple[int, ...]], Fraction] = {}
    for row in body2:
        key = (
            int(row["row"]) - 1,
            int(row["col"]) - 1,
            tuple(int(row[f"nu{k}"]) for k in range(1, 7)),
        )
        actual[key] = rational(row["real_num"], row["real_den"])
        if int(row["imag_num"]) != 0:
            actual[key] += rational(row["imag_num"], row["imag_den"]) * 1j

    expected = {
        (0, 0, (0, 0, 0, 0, 0, 0)): Fraction(20953, 100000),
        (0, 0, (0, -1, 0, 0, 0, 0)): 1j * Fraction(21, 3125),
        (0, 0, (0, 1, 0, 0, 0, 0)): 1j * Fraction(-21, 3125),
        (0, 0, (0, -2, 0, 0, 0, 0)): Fraction(-441, 200000),
        (0, 0, (0, 2, 0, 0, 0, 0)): Fraction(-441, 200000),
        (1, 1, (0, 0, 0, 0, 0, 0)): Fraction(10441, 50000),
    }
    if actual != expected:
        raise AssertionError(f"body-2 coefficient map mismatch: {actual!r} != {expected!r}")
    receipt = {
        "schema": "routeb.o1.body_2.target_check.v1",
        "status": "PASS_EXACT_BODY2_TARGET_COEFFICIENTS_FAIL_CLOSED",
        "body": 2,
        "csv_row_count": len(body2),
        "keyed_coefficient_map_matches": True,
        "target_formula": {
            "entry_00": "20953/100000 + (42/3125) sin(q2) - (441/100000) cos(2*q2)",
            "entry_11": "10441/50000",
            "other_entries": "0",
        },
        "source_expansion_proven": False,
        "trace_fold_proven": False,
        "h_body_2_proven": False,
        "lean_compiled": False,
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    OUT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(receipt)


if __name__ == "__main__":
    main()
