"""Check exact body-3 target coefficients against the frozen trace CSV."""
from __future__ import annotations

import csv
from fractions import Fraction
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "artifacts/task_routeb_body_trace_sink_current/outputs/routeB_fourier_mass_body_trace.csv"
OUT = ROOT / "examples/routeb_b45_source_comparator_lean/O1_BODY_3_TARGET_CHECK.json"


def frac(num: str, den: str) -> Fraction:
    return Fraction(int(num), int(den))


def main() -> None:
    with CSV.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    body3 = [row for row in rows if int(row["body"]) == 3]
    actual: dict[tuple[int, int, tuple[int, ...]], complex] = {}
    for row in body3:
        key = (
            int(row["row"]) - 1,
            int(row["col"]) - 1,
            tuple(int(row[f"nu{k}"]) for k in range(1, 7)),
        )
        actual[key] = complex(
            frac(row["real_num"], row["real_den"]),
            frac(row["imag_num"], row["imag_den"]),
        )

    zero = (0, 0, 0, 0, 0, 0)
    minus_one = (0, -1, 0, 0, 0, 0)
    plus_one = (0, 1, 0, 0, 0, 0)
    minus_two = (0, -2, 0, 0, 0, 0)
    plus_two = (0, 2, 0, 0, 0, 0)
    expected = {
        (0, 0, minus_two): complex(Fraction(-1323, 200000)),
        (0, 0, minus_one): complex(0, Fraction(63, 6250)),
        (0, 0, zero): complex(Fraction(80467, 600000)),
        (0, 0, plus_one): complex(0, Fraction(-63, 6250)),
        (0, 0, plus_two): complex(Fraction(-1323, 200000)),
        (0, 1, minus_one): complex(Fraction(-63, 40000)),
        (0, 1, plus_one): complex(Fraction(-63, 40000)),
        (1, 0, minus_one): complex(Fraction(-63, 40000)),
        (1, 0, plus_one): complex(Fraction(-63, 40000)),
        (1, 1, zero): complex(Fraction(21469, 150000)),
        (1, 2, zero): complex(Fraction(7, 60)),
        (2, 1, zero): complex(Fraction(7, 60)),
        (2, 2, zero): complex(Fraction(7, 60)),
    }
    if actual != expected:
        raise AssertionError(f"body-3 coefficient map mismatch: {actual!r} != {expected!r}")
    receipt = {
        "schema": "routeb.o1.body_3.target_check.v1",
        "status": "PASS_EXACT_BODY3_TARGET_COEFFICIENTS_FAIL_CLOSED",
        "body": 3,
        "zero_based_body": 2,
        "csv_row_count": len(body3),
        "keyed_coefficient_map_matches": True,
        "target_formula": {
            "entry_00": "80467/600000 + (63/3125) sin(q1) - (1323/100000) cos(2*q1)",
            "entry_01_entry_10": "-(63/20000) cos(q1)",
            "entry_11": "21469/150000",
            "entry_12_entry_21_entry_22": "7/60",
            "other_entries": "0",
        },
        "source_expansion_proven": False,
        "trace_fold_proven": False,
        "h_body_3_proven": False,
        "lean_compiled": False,
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    OUT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(receipt)


if __name__ == "__main__":
    main()
