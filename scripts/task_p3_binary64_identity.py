"""Fail-closed identity receipt for an observed binary64 P3 input.

This helper checks representation and contract metadata only.  It deliberately
does not evaluate Taylor series, Julia, libm, or any comparator.
"""
from __future__ import annotations

import argparse
import json
import struct
from fractions import Fraction
from pathlib import Path

SCHEMA = "p3-binary64-identity-receipt-v1"
COORDS = ("q1", "q2", "q3", "q4", "q5", "q6")
DECLARED_LIMITS = {
    "q1": "[-pi,pi]", "q2": "[-pi,pi]", "q3": "[-5pi/6,5pi/6]",
    "q4": "[-pi,pi]", "q5": "[-pi,pi]", "q6": "[-2pi,2pi]",
}

def _hex_bits(value: str) -> int:
    if not isinstance(value, str) or not value.lower().startswith("0x"):
        raise ValueError("binary64 hex must be a 0x-prefixed 16-digit bit pattern")
    bits = int(value, 16)
    if len(value[2:].replace("_", "")) != 16 or not 0 <= bits <= (1 << 64) - 1:
        raise ValueError("binary64 hex must contain exactly 64 bits")
    return bits

def _rational(value: str) -> Fraction:
    if not isinstance(value, str):
        raise ValueError("exact rational must be a string")
    return Fraction(value)

def validate_receipt(receipt: dict) -> dict:
    errors = []
    if receipt.get("schema") != SCHEMA:
        errors.append("schema mismatch")
    if receipt.get("julia_libm_equivalence") != "UNPROVED_AND_NOT_CLAIMED":
        errors.append("explicit Julia/libm equivalence marker is missing or affirmative")
    for field in ("evaluator_hash", "source_hash"):
        value = receipt.get(field)
        if not isinstance(value, str) or len(value) != 64 or any(c not in "0123456789abcdefABCDEF" for c in value):
            errors.append(f"{field} must be a SHA-256 hex digest")
    observed, exact = receipt.get("observed_binary64"), receipt.get("exact_rational_input")
    if not isinstance(observed, dict) or not isinstance(exact, dict):
        errors.append("observed_binary64 and exact_rational_input are required objects")
    else:
        if tuple(observed) != COORDS or tuple(exact) != COORDS:
            errors.append("input order must be exactly q1,q2,q3,q4,q5,q6")
        for q in COORDS:
            try:
                bits = _hex_bits(observed[q])
                if (bits >> 63) == 1 and ((bits >> 52) & 0x7ff) == 0x7ff:
                    errors.append(f"{q}: NaN/infinity is not an input")
                # pack/unpack is the identity under IEEE-754 binary64.
                if struct.unpack(">Q", struct.pack(">d", struct.unpack(">d", struct.pack(">Q", bits))[0]))[0] != bits:
                    errors.append(f"{q}: bit pattern is not binary64")
                _rational(exact[q])
            except (KeyError, ValueError, OverflowError, struct.error) as exc:
                errors.append(f"{q}: {exc}")
        bounds = receipt.get("exact_rational_bounds")
        if not isinstance(bounds, dict) or tuple(bounds) != COORDS:
            errors.append("exact_rational_bounds must contain q1..q6 in order")
        else:
            for q in COORDS:
                try:
                    lo, hi = (_rational(x) for x in bounds[q])
                    x = _rational(exact[q])
                    if lo > hi or not lo <= x <= hi:
                        errors.append(f"{q}: exact rational is outside its inclusive boundary")
                except (KeyError, ValueError, TypeError) as exc:
                    errors.append(f"{q}: invalid boundary ({exc})")
    return {"schema": SCHEMA, "verdict": "PASS" if not errors else "FAIL_CLOSED", "errors": errors,
            "declared_joint_limits": DECLARED_LIMITS,
            "taylor_result_upgrade": "PROHIBITED",
            "julia_libm_equivalence": "UNPROVED_AND_NOT_CLAIMED"}

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("receipt", type=Path)
    args = parser.parse_args()
    result = validate_receipt(json.loads(args.receipt.read_text(encoding="utf-8")))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["verdict"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
