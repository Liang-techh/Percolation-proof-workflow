"""Check exact human body-5 target coefficients against the frozen trace CSV."""
from __future__ import annotations

import csv
from fractions import Fraction
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "artifacts/task_routeb_body_trace_sink_current/outputs/routeB_fourier_mass_body_trace.csv"
OUT = ROOT / "examples/routeb_b45_source_comparator_lean/O1_BODY_5_TARGET_CHECK.json"
ZERO = (0, 0, 0, 0, 0, 0)


def key(a: int, b: int = 0, c: int = 0, d: int = 0) -> tuple[int, ...]:
    return (0, a, b, c, d, 0)


def main() -> None:
    with CSV.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    body5 = [row for row in rows if int(row["body"]) == 5]
    actual: dict[tuple[int, int, tuple[int, ...]], complex] = {}
    for row in body5:
        atom_key = (
            int(row["row"]) - 1,
            int(row["col"]) - 1,
            tuple(int(row[f"nu{k}"]) for k in range(1, 7)),
        )
        actual[atom_key] = complex(
            Fraction(int(row["real_num"]), int(row["real_den"])),
            Fraction(int(row["imag_num"]), int(row["imag_den"])),
        )

    expected: dict[tuple[int, int, tuple[int, ...]], complex] = {}
    expected[(0, 0, ZERO)] = complex(Fraction(1441, 30000))
    expected[(0, 0, key(-2, -2))] = complex(Fraction(-1083, 400000))
    expected[(0, 0, key(-2, -1))] = complex(Fraction(-1197, 200000))
    expected[(0, 0, key(-2, 0))] = complex(Fraction(-1323, 400000))
    expected[(0, 0, key(-1, -1))] = complex(0, Fraction(57, 12500))
    expected[(0, 0, key(-1, 0))] = complex(0, Fraction(63, 12500))
    expected[(0, 0, key(0, -1))] = complex(Fraction(1197, 200000))
    expected[(0, 0, key(0, 1))] = complex(Fraction(1197, 200000))
    expected[(0, 0, key(1, 0))] = complex(0, Fraction(-63, 12500))
    expected[(0, 0, key(1, 1))] = complex(0, Fraction(-57, 12500))
    expected[(0, 0, key(2, 0))] = complex(Fraction(-1323, 400000))
    expected[(0, 0, key(2, 1))] = complex(Fraction(-1197, 200000))
    expected[(0, 0, key(2, 2))] = complex(Fraction(-1083, 400000))

    def add_symmetric(i: int, j: int, atom: tuple[int, ...], coeff: Fraction) -> None:
        expected[(i, j, atom)] = complex(coeff)

    for i, j in ((0, 1), (1, 0)):
        for atom, coeff in (
            (key(-1, -1), Fraction(-57, 40000)),
            (key(-1, 0), Fraction(-63, 40000)),
            (key(1, 0), Fraction(-63, 40000)),
            (key(1, 1), Fraction(-57, 40000)),
        ):
            add_symmetric(i, j, atom, coeff)
    for i, j in ((0, 2), (2, 0)):
        for atom in (key(-1, -1), key(1, 1)):
            add_symmetric(i, j, atom, Fraction(-57, 40000))
    for i, j in ((0, 3), (3, 0)):
        for atom in (key(-1, -1), key(1, 1)):
            add_symmetric(i, j, atom, Fraction(1, 60))
    for i, j in ((0, 4), (4, 0)):
        add_symmetric(i, j, key(-1, -1, -1), Fraction(-1, 120))
        add_symmetric(i, j, key(-1, -1, 1), Fraction(1, 120))
        add_symmetric(i, j, key(1, 1, -1), Fraction(1, 120))
        add_symmetric(i, j, key(1, 1, 1), Fraction(-1, 120))
    for atom, coeff in (
        (key(0, -1), Fraction(1197, 100000)),
        (ZERO, Fraction(8609, 150000)),
        (key(0, 1), Fraction(1197, 100000)),
    ):
        add_symmetric(1, 1, atom, coeff)
    for i, j in ((1, 2), (2, 1)):
        for atom, coeff in (
            (key(0, -1), Fraction(1197, 200000)),
            (ZERO, Fraction(13249, 300000)),
            (key(0, 1), Fraction(1197, 200000)),
        ):
            add_symmetric(i, j, atom, coeff)
    for i, j in ((1, 4), (4, 1), (2, 4), (4, 2)):
        for atom in (key(0, 0, -1), key(0, 0, 1)):
            add_symmetric(i, j, atom, Fraction(1, 60))
    expected[(2, 2, ZERO)] = complex(Fraction(13249, 300000))
    expected[(3, 3, ZERO)] = complex(Fraction(1, 30))
    expected[(4, 4, ZERO)] = complex(Fraction(1, 30))

    if actual != expected:
        only_actual = sorted(set(actual) - set(expected))
        only_expected = sorted(set(expected) - set(actual))
        value_mismatch = sorted(
            (atom_key, actual[atom_key], expected[atom_key])
            for atom_key in set(actual) & set(expected)
            if actual[atom_key] != expected[atom_key]
        )
        raise AssertionError(
            "body-5 coefficient map mismatch: "
            f"actual_only={only_actual!r}, expected_only={only_expected!r}, "
            f"value_mismatch={value_mismatch!r}"
        )
    receipt = {
        "schema": "routeb.o1.body_5.target_check.v1",
        "status": "PASS_EXACT_BODY5_TARGET_COEFFICIENTS_FAIL_CLOSED",
        "body": 5,
        "zero_based_body": 4,
        "csv_row_count": len(body5),
        "keyed_coefficient_map_matches": True,
        "target_formula": {
            "entry_00": "1441/30000 + (63/6250) sin(q1) + (57/6250) sin(q1+q2) - (1323/200000) cos(2q1) + (1197/100000) cos(q2) - (1197/100000) cos(2q1+q2) - (1083/200000) cos(2q1+2q2)",
            "entry_01_entry_10": "-(57/20000) cos(q1+q2) - (63/20000) cos(q1)",
            "entry_02_entry_20": "-(57/20000) cos(q1+q2)",
            "entry_03_entry_30": "(1/30) cos(q1+q2)",
            "entry_04_entry_40": "(1/60)(cos(q1+q2-q3) - cos(q1+q2+q3))",
            "entry_11": "8609/150000 + (1197/50000) cos(q2)",
            "entry_12_entry_21": "13249/300000 + (1197/100000) cos(q2)",
            "entry_14_entry_24_and_transposes": "(1/30) cos(q3)",
            "entry_22": "13249/300000",
            "entry_33_entry_44": "1/30",
            "other_entries": "0",
        },
        "source_expansion_proven": False,
        "trace_fold_proven": False,
        "h_body_5_proven": False,
        "lean_compiled": False,
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    OUT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(receipt)


if __name__ == "__main__":
    main()
