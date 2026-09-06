"""External provenance checker for the narrow B45-1.g Lean payload.

This checker is intentionally outside the kernel.  It reads the frozen CSV,
checks its bytes/hash and 610 records, re-aggregates exact rationals at q=0,
and checks that the Lean source contains the same frozen payload.  Lean then
proves only the finite rational equality in MassZeroBridge.lean.
"""
from __future__ import annotations

import csv
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import re
from datetime import datetime, timezone

SIDE = Path(__file__).resolve().parent
CSV = SIDE.parent / "routeb_source_binding_audit" / "snapshots" / "current_exact" / "routeB_fourier_mass_full_rational.csv"
LEAN = SIDE / "MassZeroBridge.lean"
EXPECTED_SHA256 = "a986a208b62f585c6ca1b9c81b958710d2043e5bf786ddc930a6fa29f7a232b8"

EXPECTED_UNREG = [
    ["4711/6000", "-1481/80000", "-103/16000", "7/60", "-21/80000", "1/60"],
    ["-1481/80000", "1397297/2400000", "677771/2400000", "0", "41827/800000", "0"],
    ["-103/16000", "677771/2400000", "612881/2400000", "0", "8189/160000", "0"],
    ["7/60", "0", "0", "7/60", "0", "1/60"],
    ["-21/80000", "41827/800000", "8189/160000", "0", "40147/800000", "0"],
    ["1/60", "0", "0", "1/60", "0", "1/60"],
]
EXPECTED_M0 = [
    ["2355503/3000000", "-1481/80000", "-103/16000", "7/60", "-21/80000", "1/60"],
    ["-1481/80000", "6986497/12000000", "677771/2400000", "0", "41827/800000", "0"],
    ["-103/16000", "677771/2400000", "3064417/12000000", "0", "8189/160000", "0"],
    ["7/60", "0", "0", "350003/3000000", "0", "1/60"],
    ["-21/80000", "41827/800000", "8189/160000", "0", "200739/4000000", "0"],
    ["1/60", "0", "0", "1/60", "0", "50003/3000000"],
]


def q(text: str) -> Q:
    return Q(text.strip())


def parse_lean_matrix(source: str, name: str) -> list[list[str]]:
    start = source.index(f"def {name} : Mat 6 := ![")
    body = source[start:].split("\n\n", 1)[0].split(":= ![", 1)[1]
    rows = re.findall(r"!\[([^\]]+)\]", body)
    parsed = [[str(q(x)) for x in row.split(",")] for row in rows]
    if len(parsed) != 6 or any(len(row) != 6 for row in parsed):
        raise AssertionError(f"bad frozen {name} matrix shape")
    return parsed


def main() -> None:
    raw = CSV.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    assert digest == EXPECTED_SHA256, (digest, EXPECTED_SHA256)
    with CSV.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 610
    assert set(rows[0]) == {
        "row", "col", "nu1", "nu2", "nu3", "nu4", "nu5", "nu6",
        "real_num", "real_den", "imag_num", "imag_den",
    }
    unreg = [[Q(0) for _ in range(6)] for _ in range(6)]
    imag = [[Q(0) for _ in range(6)] for _ in range(6)]
    seen = set()
    frequency_support = set()
    for row in rows:
        i, j = int(row["row"]) - 1, int(row["col"]) - 1
        assert 0 <= i < 6 and 0 <= j < 6
        seen.add((i, j))
        frequency_support.add(tuple(int(row[f"nu{k}"]) for k in range(1, 7)))
        unreg[i][j] += Q(int(row["real_num"]), int(row["real_den"]))
        imag[i][j] += Q(int(row["imag_num"]), int(row["imag_den"]))
    all_pairs = {(i, j) for i in range(6) for j in range(6)}
    assert seen <= all_pairs
    omitted_pairs = sorted(all_pairs - seen)
    # The exporter omits identically zero matrix entries.  Treat omission as
    # a checked sparse encoding, not as an implicit theorem about file I/O.
    assert all(unreg[i][j] == 0 for i, j in omitted_pairs)
    assert all(x == 0 for row in imag for x in row)
    actual_unreg = [[str(x) for x in row] for row in unreg]
    assert actual_unreg == EXPECTED_UNREG, actual_unreg
    regularized = [
        [str(unreg[i][j] + (Q(1, 1000000) if i == j else Q(0))) for j in range(6)]
        for i in range(6)
    ]
    assert regularized == EXPECTED_M0
    source = LEAN.read_text(encoding="utf-8")
    assert parse_lean_matrix(source, "csvQ0Mass") == EXPECTED_UNREG
    assert parse_lean_matrix(source, "M0") == EXPECTED_M0
    assert "CSV" in source and "file reader" in source

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = SIDE / "output" / f"audit-{stamp}"
    out.mkdir(parents=True, exist_ok=False)
    result = {
        "status": "EXACT_CSV_Q0_PAYLOAD_AUDIT_PASSED",
        "csv_path": str(CSV),
        "csv_sha256": digest,
        "csv_rows": len(rows),
        "matrix_entries": 36,
        "csv_matrix_pairs_present": len(seen),
        "csv_omitted_pairs_are_zero": True,
        "csv_omitted_pairs": [[i + 1, j + 1] for i, j in omitted_pairs],
        "all_imaginary_aggregates_zero": True,
        "frequency_support_cardinality": len(frequency_support),
        "q0_phase_rule": "exp(i * nu dot 0) = 1 for every integer frequency",
        "frozen_payload_matches_csv": True,
        "regularized_payload_matches_M0": True,
        "lean_file_reading": False,
        "physical_DH_binding": False,
        "float64_bridge": False,
    }
    (out / "result.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    (out / "provenance.txt").write_text(
        "CSV_BYTES_HASHED_EXTERNALLY=true\n"
        "LEAN_FILE_READING=false\n"
        "Q0_PAYLOAD_IS_FROZEN=true\n"
        "KERNEL_THEOREM_IS_FINITE_RATIONAL_EQUALITY=true\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2))
    print(f"AUDIT_DIRECTORY={out}")


if __name__ == "__main__":
    main()
