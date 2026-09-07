"""Small, fail-closed audit for the exported Route-B M0[4,4] decimal.

This is intentionally a provenance/value audit, not a DH semantics verifier.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import struct
from fractions import Fraction
from pathlib import Path


DEFAULT_ROOT = Path(r"C:\Users\z5242\Desktop\重构版\6dof_sos_optimized\6dof_sos_optimized")
CSV_REL = Path("routeB_dense_Mq") / "routeB_Mq_M0.csv"
SOURCE_REL = Path("routeB_dense_Mq") / "dhport_lib.jl"
ROW = COL = 3  # Julia's M[4,4], represented as zero-based Python indices.
EXPECTED_SPELLING = "0.116667666666667"
EXPECTED_RATIONAL = Fraction(116667666666667, 10**15)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def float_bits(value: float) -> str:
    return struct.pack(">d", value).hex()


def load_cell(path: Path) -> str:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.reader(handle))
    return rows[ROW][COL]


def run(root: Path, output_dir: Path) -> dict:
    csv_path = root / CSV_REL
    source_path = root / SOURCE_REL
    spelling = load_cell(csv_path)
    parsed_float = float(spelling)
    decimal_rational = Fraction(spelling)
    rational_float = float(decimal_rational)
    source_text = source_path.read_text(encoding="utf-8")

    spelling_ok = spelling == EXPECTED_SPELLING and decimal_rational == EXPECTED_RATIONAL
    float_ok = float_bits(parsed_float) == float_bits(rational_float)
    source_contract_markers = {
        "mass_matrix_definition": "function mass_matrix" in source_text,
        "explicit_regularization": "MASS_REGULARIZER" in source_text,
        "regularization_added": "regularization" in source_text and "return M +" in source_text,
    }
    report = {
        "schema": "routeb-p4-decimal-source-binding-audit/v1",
        "status": "PENDING",
        "target": "M0[4,4] (Julia 1-based indexing)",
        "checks": {
            "decimal_spelling_equality": {
                "status": "PASS" if spelling_ok else "FAIL",
                "csv_spelling": spelling,
                "expected_spelling": EXPECTED_SPELLING,
                "exact_rational": f"{decimal_rational.numerator}/{decimal_rational.denominator}",
            },
            "float64_value_equality": {
                "status": "PASS" if float_ok else "FAIL",
                "csv_float": repr(parsed_float),
                "rational_to_float": repr(rational_float),
                "csv_ieee754_bits": float_bits(parsed_float),
                "rational_ieee754_bits": float_bits(rational_float),
            },
            "true_dh_mass_equality": {
                "status": "PENDING",
                "reason": (
                    "The CSV snapshot is not an executable proof of the Julia DH mass_matrix "
                    "at q=0. A pinned Float64 execution trace, exact DH/trigonometric model, "
                    "regularization semantics, and a real/Float64 bridge are missing."
                ),
                "source_contract_markers": source_contract_markers,
            },
        },
        "provenance": {
            "external_root": str(root),
            "csv_path": str(CSV_REL),
            "csv_sha256": sha256(csv_path),
            "julia_source_path": str(SOURCE_REL),
            "julia_source_sha256": sha256(source_path),
            "source_role": "canonical numerical DH implementation reference; not imported into Lean",
            "export_role": "routeB_Mq_M0.csv is an exported Float64 snapshot",
        },
        "admission": {
            "p4_source_binding": "PENDING",
            "p4_global_coverage": "OPEN",
            "formal_certificate_allowed": False,
            "verified_registry_mutation": False,
        },
    }
    if not spelling_ok or not float_ok:
        report["status"] = "REJECTED"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "audit_report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    markdown = [
        "# Route-B P4 decimal/source-binding audit",
        "",
        f"Status: **{report['status']}** (true-DH source binding remains pending).",
        "",
        "Target: exported `routeB_Mq_M0.csv[4,4]` (Julia indexing).",
        "",
        "| Layer | Result | Evidence |",
        "|---|---|---|",
        f"| decimal spelling equality | {report['checks']['decimal_spelling_equality']['status']} | `{spelling}` = `{EXPECTED_RATIONAL.numerator}/{EXPECTED_RATIONAL.denominator}` as a decimal spelling |",
        f"| Float64 value equality | {report['checks']['float64_value_equality']['status']} | IEEE-754 bits `{float_bits(parsed_float)}` |",
        "| true-DH mass equality | **PENDING** | no exact DH/Float64 execution-to-real bridge or regularization witness |",
        "",
        "The exact rational leaf proves only the decimal reification. It does not prove that the Julia DH implementation evaluates to this real number, nor that the exported snapshot was generated from the canonical source under the claimed semantics.",
        "",
        f"CSV SHA-256: `{sha256(csv_path)}`",
        f"Julia source SHA-256: `{sha256(source_path)}`",
        "",
        "No external project, persistent state, registry, or P4 admission flag was modified.",
    ]
    (output_dir / "REPORT.md").write_text("\n".join(markdown), encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--external-root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).parent)
    args = parser.parse_args()
    report = run(args.external_root, args.output_dir)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PENDING" else 1


if __name__ == "__main__":
    raise SystemExit(main())
