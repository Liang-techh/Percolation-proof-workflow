"""Strict, standalone validator for the B45-5 residual-closure receipt.

This module is intentionally not wired into admission or the registry.  It
only validates a supplied JSON receipt and, when requested, its source hash.
No defaults, numerical completion, or rounding is performed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any

SCHEMA = "routeb-b45-5-residual-closure-receipt-v1"
REQUIRED = (
    "schema", "descriptor_dimensions", "spectral_gap", "coupling_norms",
    "regularizer", "residual_source", "outward_rounding", "domain_coverage",
)
PLACEHOLDERS = {"", "tbd", "todo", "pending", "unknown", "placeholder", "n/a", "na"}


class ReceiptValidationError(ValueError):
    """Raised when a receipt cannot establish every closure obligation."""


def _required(obj: dict[str, Any], keys: tuple[str, ...], where: str) -> None:
    missing = [key for key in keys if key not in obj]
    if missing:
        raise ReceiptValidationError(f"{where}: missing fields: {', '.join(missing)}")


def _number(value: Any, where: str, *, positive: bool = False) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ReceiptValidationError(f"{where}: finite numeric value required")
    result = float(value)
    if not math.isfinite(result) or (positive and result <= 0):
        raise ReceiptValidationError(f"{where}: invalid numeric value")
    return result


def _text(value: Any, where: str) -> str:
    if not isinstance(value, str) or value.strip().lower() in PLACEHOLDERS:
        raise ReceiptValidationError(f"{where}: non-placeholder text required")
    return value


def validate_receipt(receipt: Any, *, source_root: Path | None = None) -> dict[str, Any]:
    if not isinstance(receipt, dict):
        raise ReceiptValidationError("receipt must be an object")
    _required(receipt, REQUIRED, "receipt")
    if receipt["schema"] != SCHEMA:
        raise ReceiptValidationError("receipt.schema: unsupported schema")

    dimensions = receipt["descriptor_dimensions"]
    if not isinstance(dimensions, dict):
        raise ReceiptValidationError("descriptor_dimensions: object required")
    _required(dimensions, ("rows", "cols"), "descriptor_dimensions")
    for key in ("rows", "cols"):
        value = dimensions[key]
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            raise ReceiptValidationError(f"descriptor_dimensions.{key}: positive integer required")

    gap = receipt["spectral_gap"]
    if not isinstance(gap, dict):
        raise ReceiptValidationError("spectral_gap: object required")
    _required(gap, ("A", "mu"), "spectral_gap")
    A, mu = _number(gap["A"], "spectral_gap.A", positive=True), _number(gap["mu"], "spectral_gap.mu", positive=True)
    if not A > mu:
        raise ReceiptValidationError("spectral_gap: A must be strictly greater than mu")

    norms = receipt["coupling_norms"]
    if not isinstance(norms, dict) or not norms:
        raise ReceiptValidationError("coupling_norms: non-empty object required")
    for name, value in norms.items():
        _text(name, "coupling_norms key")
        _number(value, f"coupling_norms.{name}")
        if value < 0:
            raise ReceiptValidationError(f"coupling_norms.{name}: must be non-negative")

    regularizer = receipt["regularizer"]
    if not isinstance(regularizer, dict):
        raise ReceiptValidationError("regularizer: object required")
    _required(regularizer, ("rho",), "regularizer")
    _number(regularizer["rho"], "regularizer.rho", positive=True)

    source = receipt["residual_source"]
    if not isinstance(source, dict):
        raise ReceiptValidationError("residual_source: object required")
    _required(source, ("path", "sha256"), "residual_source")
    path_text, expected = _text(source["path"], "residual_source.path"), _text(source["sha256"], "residual_source.sha256")
    if len(expected) != 64 or any(c not in "0123456789abcdefABCDEF" for c in expected):
        raise ReceiptValidationError("residual_source.sha256: SHA-256 hex required")
    if source_root is not None:
        path = Path(path_text)
        if not path.is_absolute():
            path = source_root / path
        if not path.is_file():
            raise ReceiptValidationError("residual_source.path: source does not exist")
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual.lower() != expected.lower():
            raise ReceiptValidationError("residual_source: SHA-256 mismatch")

    outward = receipt["outward_rounding"]
    if outward is not True:
        raise ReceiptValidationError("outward_rounding: literal true required")

    coverage = receipt["domain_coverage"]
    if not isinstance(coverage, dict):
        raise ReceiptValidationError("domain_coverage: object required")
    _required(coverage, ("complete", "domain_id"), "domain_coverage")
    if coverage["complete"] is not True:
        raise ReceiptValidationError("domain_coverage.complete: literal true required")
    _text(coverage["domain_id"], "domain_coverage.domain_id")
    return {"status": "valid", "schema": SCHEMA}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--source-root", type=Path)
    args = parser.parse_args()
    try:
        receipt = json.loads(args.input.read_text(encoding="utf-8"))
        result = validate_receipt(receipt, source_root=args.source_root or args.input.parent)
    except (OSError, json.JSONDecodeError, ReceiptValidationError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
