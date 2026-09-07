"""Check exact human body-4 target coefficients against the frozen trace CSV."""
from __future__ import annotations

import csv
from fractions import Fraction
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "artifacts/task_routeb_body_trace_sink_current/outputs/routeB_fourier_mass_body_trace.csv"
OUT = ROOT / "examples/routeb_b45_source_comparator_lean/O1_BODY_4_TARGET_CHECK.json"


def main() -> None:
    with CSV.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    body4 = [row for row in rows if int(row["body"]) == 4]
    actual: dict[tuple[int, int, tuple[int, ...]], complex] = {}
    for row in body4:
        key = (
            int(row["row"]) - 1,
            int(row["col"]) - 1,
            tuple(int(row[f"nu{k}"]) for k in range(1, 7)),
        )
        actual[key] = complex(
            Fraction(int(row["real_num"]), int(row["real_den"])),
            Fraction(int(row["imag_num"]), int(row["imag_den"])),
        )

    zero = (0, 0, 0, 0, 0, 0)
    expected = {
        (0, 0, (0, -2, -2, 0, 0, 0)): complex(Fraction(-361, 400000)),
        (0, 0, (0, -2, -1, 0, 0, 0)): complex(Fraction(-399, 100000)),
        (0, 0, (0, -2, 0, 0, 0, 0)): complex(Fraction(-441, 100000)),
        (0, 0, (0, -1, -1, 0, 0, 0)): complex(0, Fraction(19, 6250)),
        (0, 0, (0, -1, 0, 0, 0, 0)): complex(0, Fraction(21, 3125)),
        (0, 0, (0, 0, -1, 0, 0, 0)): complex(Fraction(399, 100000)),
        (0, 0, zero): complex(Fraction(48511, 600000)),
        (0, 0, (0, 0, 1, 0, 0, 0)): complex(Fraction(399, 100000)),
        (0, 0, (0, 1, 0, 0, 0, 0)): complex(0, Fraction(-21, 3125)),
        (0, 0, (0, 1, 1, 0, 0, 0)): complex(0, Fraction(-19, 6250)),
        (0, 0, (0, 2, 0, 0, 0, 0)): complex(Fraction(-441, 100000)),
        (0, 0, (0, 2, 1, 0, 0, 0)): complex(Fraction(-399, 100000)),
        (0, 0, (0, 2, 2, 0, 0, 0)): complex(Fraction(-361, 400000)),
    }
    for i, j in ((0, 1), (1, 0)):
        expected[(i, j, (0, -1, -1, 0, 0, 0))] = complex(Fraction(-19, 20000))
        expected[(i, j, (0, -1, 0, 0, 0, 0))] = complex(Fraction(-21, 10000))
        expected[(i, j, (0, 1, 0, 0, 0, 0))] = complex(Fraction(-21, 10000))
        expected[(i, j, (0, 1, 1, 0, 0, 0))] = complex(Fraction(-19, 20000))
    for i, j in ((0, 2), (2, 0)):
        expected[(i, j, (0, -1, -1, 0, 0, 0))] = complex(Fraction(-19, 20000))
        expected[(i, j, (0, 1, 1, 0, 0, 0))] = complex(Fraction(-19, 20000))
    for i, j in ((0, 3), (3, 0)):
        expected[(i, j, (0, -1, -1, 0, 0, 0))] = complex(Fraction(1, 30))
        expected[(i, j, (0, 1, 1, 0, 0, 0))] = complex(Fraction(1, 30))
    for i, j in ((1, 1),):
        expected[(i, j, (0, 0, -1, 0, 0, 0))] = complex(Fraction(399, 50000))
        expected[(i, j, zero)] = complex(Fraction(211, 2400))
        expected[(i, j, (0, 0, 1, 0, 0, 0))] = complex(Fraction(399, 50000))
    for i, j in ((1, 2), (2, 1)):
        expected[(i, j, (0, 0, -1, 0, 0, 0))] = complex(Fraction(399, 100000))
        expected[(i, j, zero)] = complex(Fraction(21083, 300000))
        expected[(i, j, (0, 0, 1, 0, 0, 0))] = complex(Fraction(399, 100000))
    expected[(2, 2, zero)] = complex(Fraction(21083, 300000))
    expected[(3, 3, zero)] = complex(Fraction(1, 15))
    if actual != expected:
        raise AssertionError(f"body-4 coefficient map mismatch: {actual!r} != {expected!r}")
    receipt = {
        "schema": "routeb.o1.body_4.target_check.v1",
        "status": "PASS_EXACT_BODY4_TARGET_COEFFICIENTS_FAIL_CLOSED",
        "body": 4,
        "zero_based_body": 3,
        "csv_row_count": len(body4),
        "keyed_coefficient_map_matches": True,
        "target_formula": {
            "entry_00": "48511/600000 + (42/3125) sin(q1) + (19/3125) sin(q1+q2) - (441/50000) cos(2q1) + (399/50000) cos(q2) - (399/50000) cos(2q1+q2) - (361/200000) cos(2q1+2q2)",
            "entry_01_entry_10": "-(19/10000) cos(q1+q2) - (21/5000) cos(q1)",
            "entry_02_entry_20": "-(19/10000) cos(q1+q2)",
            "entry_03_entry_30": "(1/15) cos(q1+q2)",
            "entry_11": "211/2400 + (399/25000) cos(q2)",
            "entry_12_entry_21": "21083/300000 + (399/50000) cos(q2)",
            "entry_22": "21083/300000",
            "entry_33": "1/15",
            "other_entries": "0",
        },
        "source_expansion_proven": False,
        "trace_fold_proven": False,
        "h_body_4_proven": False,
        "lean_compiled": False,
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    OUT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(receipt)


if __name__ == "__main__":
    main()
