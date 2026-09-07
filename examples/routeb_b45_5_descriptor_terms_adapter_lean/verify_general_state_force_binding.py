"""Intake gate for a fresh general-state force-binding export.

This verifier consumes artifacts produced by
``general_state_force_binding_export.jl``.  It never runs Julia and never
promotes a result to a theorem or deployed-tau equivalence.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import math
import re
import sys
from pathlib import Path


EXPECTED_EXPORTER_SHA = "5351110e81327ebc059074a2e445a33e00859320bce37b5b0220bb189f4e46a4"
EXPECTED_SOURCE_SHA = "aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936"
TOL = 1e-12

EXPECTED_HEADER = [
    "sample", "q4", "q5", "dq4", "dq5", "w",
    "CdqB4", "CdqB5", "GqB4", "GqB5", "G0B4", "G0B5",
    "tauB4", "tauB5", "rhsB4", "rhsB5",
    "sourceBlockForce4", "sourceBlockForce5", "aB4", "aB5",
    "aD1", "aD2", "aD3", "aD6",
    "MqBB11", "MqBB12", "MqBB21", "MqBB22",
    "MqBD41", "MqBD42", "MqBD43", "MqBD46",
    "MqBD51", "MqBD52", "MqBD53", "MqBD56",
    "sourceDescriptorRhs4", "sourceDescriptorRhs5",
    "E1_4", "E1_5", "E2_4", "E2_5",
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fail(message: str) -> "NoReturn":
    raise SystemExit(f"REJECTED: {message}")


def main() -> int:
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--export-dir", type=Path, default=here / "output" / "general-state-export-20260907")
    parser.add_argument("--exporter", type=Path, default=here / "general_state_force_binding_export.jl")
    parser.add_argument(
        "--source",
        type=Path,
        default=here.parents[2] / "6dof_sos_optimized" / "6dof_sos_optimized" / "robot_final" / "dhport_lib.jl",
    )
    parser.add_argument("--stdout", type=Path, required=True)
    parser.add_argument("--stderr", type=Path, required=True)
    parser.add_argument("--exit-code", type=Path, required=True)
    args = parser.parse_args()

    for path in (args.exporter, args.source):
        if not path.is_file():
            fail(f"missing input {path}")
    for path in (args.stdout, args.stderr, args.exit_code):
        if not path.is_file():
            fail(f"missing process receipt {path}")

    exporter_sha = digest(args.exporter)
    source_sha = digest(args.source)
    if exporter_sha != EXPECTED_EXPORTER_SHA:
        fail(f"exporter hash drift: {exporter_sha}")
    if source_sha != EXPECTED_SOURCE_SHA:
        fail(f"deployed source hash drift: {source_sha}")

    try:
        exit_code = int(args.exit_code.read_text(encoding="utf-8").strip())
    except ValueError:
        fail("exit-code receipt is not a single integer")
    if exit_code != 0:
        fail(f"Julia process exit code is {exit_code}")

    stdout = args.stdout.read_text(encoding="utf-8")
    if "GENERAL_STATE_FORCE_BINDING_EXPORT_STATUS=PASS_RUNTIME_FLOAT64" not in stdout:
        fail("stdout lacks PASS_RUNTIME_FLOAT64 exporter status")
    for token in ("SOURCE_SHA256=" + source_sha, "EXPORTER_SHA256=" + exporter_sha, "MAX_E1=", "MAX_E2="):
        if token not in stdout:
            fail(f"stdout lacks {token}")

    csv_path = args.export_dir / "force_binding_states.csv"
    receipt_path = args.export_dir / "FORCE_BINDING_RECEIPT.md"
    if not csv_path.is_file() or not receipt_path.is_file():
        fail("exporter CSV or receipt is missing")

    with csv_path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames != EXPECTED_HEADER:
            fail("CSV header/schema/order mismatch")
        rows = list(reader)
    if len(rows) != 16:
        fail(f"expected 16 rows, found {len(rows)}")

    numeric_fields = [field for field in EXPECTED_HEADER if field != "sample"]
    max_e1 = 0.0
    max_e2 = 0.0
    for expected_sample, row in enumerate(rows, start=1):
        if row.get("sample") != str(expected_sample):
            fail(f"sample order mismatch at row {expected_sample}")
        values: dict[str, float] = {}
        for field in numeric_fields:
            try:
                value = float(row[field])
            except (KeyError, TypeError, ValueError):
                fail(f"non-numeric field {field} at row {expected_sample}")
            if not math.isfinite(value):
                fail(f"non-finite field {field} at row {expected_sample}")
            values[field] = value
        max_e1 = max(max_e1, abs(values["E1_4"]), abs(values["E1_5"]))
        max_e2 = max(max_e2, abs(values["E2_4"]), abs(values["E2_5"]))
    if max_e1 > TOL or max_e2 > TOL:
        fail(f"residual gate failed: max_E1={max_e1}, max_E2={max_e2}")

    receipt = receipt_path.read_text(encoding="utf-8")
    for token in (f"source_sha256: `{source_sha}`", f"exporter_sha256: `{exporter_sha}`", "status: `PASS_RUNTIME_FLOAT64`"):
        if token not in receipt:
            fail(f"generated receipt lacks {token}")

    print("GENERAL_STATE_FORCE_BINDING_INTAKE=PASS_RUNTIME_FLOAT64_SOURCE_BINDING_CANDIDATE")
    print(f"SOURCE_SHA256={source_sha}")
    print(f"EXPORTER_SHA256={exporter_sha}")
    print(f"CSV_SHA256={digest(csv_path)}")
    print(f"RUNTIME_RECEIPT_SHA256={digest(receipt_path)}")
    print(f"STDOUT_SHA256={digest(args.stdout)}")
    print(f"STDERR_SHA256={digest(args.stderr)}")
    print(f"MAX_E1={max_e1}")
    print(f"MAX_E2={max_e2}")
    print("DEPLOYED_TAU_EQUIVALENCE=NOT_CLAIMED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
