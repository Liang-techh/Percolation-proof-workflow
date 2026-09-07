"""Exact arithmetic for an UNBOUND rational pathK/K_cert comparison.

No Lean/Lake, optimization, float conversion, source admission, or filesystem writes.
Input uses canonical rational STRINGS only. See NEW_KPATH_INTERFACE_Comparison_REVIEW.md.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re
import sys

SCHEMA = "T-P5-026-exact-componentwise-comparison-v1"
SCOPE = "source-independent-unbound"
COORDINATES = {"state": ["x4", "x5", "y4", "y5"], "force": ["r4", "r5"]}
MAX_BYTES = 262144
MAX_DIGITS = 64
MAX_DIM = 32
MAX_PATH_TERMS = 2048  # R*m*n, before the fixed 2*4 output slots.
PATH_SOURCE = Path(__file__).resolve().parents[1] / "routeb_p5_piecewise_transport_lean/P5PiecewiseTransport.lean"
PATH_SOURCE_SHA256 = "c445e4110584c5c536f023ad08b2a8c5eccef21fc9b97aa363f24e0a9ae95208"


class Rejected(ValueError):
    def __init__(self, code: str, location: str):
        self.code, self.location = code, location
        super().__init__(f"{code}: {location}")


def need(condition: bool, code: str, location: str) -> None:
    if not condition:
        raise Rejected(code, location)


def boundary() -> dict:
    return {
        "scope": SCOPE,
        "source_binding_verified": False,
        "pathK_lean_binding_verified": False,
        "kernel_verified": False,
        "spn_verified": False,
        "H_matrix_order_proved": False,
        "source_coverage_verified": False,
        "registry_eligible": False,
        "P5_P8_M4_closed": False,
    }


def exact_keys(obj, wanted: set[str], location: str) -> None:
    need(type(obj) is dict and set(obj) == wanted, "object_fields", location)


def rational(value, location: str) -> Fraction:
    need(type(value) is str, "rational_string_required", location)
    need(len(value) <= 2 * MAX_DIGITS + 2, "rational_size", location)
    need(re.fullmatch(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?", value) is not None,
         "rational_syntax", location)
    need(all(len(part.lstrip("-")) <= MAX_DIGITS for part in value.split("/")),
         "rational_size", location)
    result = Fraction(value)
    # Reject +1, -0, 01, 2/4, 1/1, decimals, exponent strings and whitespace.
    need(str(result) == value, "rational_not_canonical", location)
    return result


def matrix(value, rows: int, cols: int, location: str, *, nonnegative=True):
    need(type(value) is list and len(value) == rows, "matrix_shape", location)
    result = []
    for i, row in enumerate(value):
        need(type(row) is list and len(row) == cols, "matrix_shape", f"{location}[{i}]")
        parsed = []
        for j, entry in enumerate(row):
            loc = f"{location}[{i},{j}]"
            q = rational(entry, loc)
            need(not nonnegative or q >= 0, "negative_entry", loc)
            parsed.append(q)
        result.append(parsed)
    return result


def no_duplicates(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, "duplicate_json_key", key)
        result[key] = value
    return result


def forbidden_number(_):
    raise Rejected("json_number_forbidden", "use canonical rational strings")


def parse_bytes(raw: bytes) -> dict:
    need(len(raw) <= MAX_BYTES, "input_size", "input")
    try:
        result = json.loads(raw.decode("utf-8"), object_pairs_hook=no_duplicates,
                            parse_int=forbidden_number, parse_float=forbidden_number,
                            parse_constant=forbidden_number)
    except (UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        raise Rejected("invalid_json", "input") from exc
    need(type(result) is dict, "object_fields", "root")
    return result


def canonical_matrix(value):
    return [[str(q) for q in row] for row in value]


def gain_digest(value) -> str:
    # This is an arithmetic-data fingerprint, NOT authenticated provenance.
    data = {"encoding": "P5-rational-gain-2x4-v1", "coordinates": COORDINATES,
            "gain": canonical_matrix(value)}
    raw = json.dumps(data, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def verify_path_source() -> None:
    need(hashlib.sha256(PATH_SOURCE.read_bytes()).hexdigest() == PATH_SOURCE_SHA256,
         "path_formula_version_changed", "P5PiecewiseTransport.lean")


def _check_payload(payload: dict) -> dict:
    """Verify rational input identities only; no claim that these are source tables."""
    exact_keys(payload, {"schema", "scope", "coordinates", "path", "K_cert"}, "root")
    need(payload["schema"] == SCHEMA, "schema", "root.schema")
    need(payload["scope"] == SCOPE, "scope", "root.scope")
    exact_keys(payload["coordinates"], {"state", "force"}, "coordinates")
    need(payload["coordinates"] == COORDINATES, "coordinate_order", "coordinates")
    path = payload["path"]
    exact_keys(path, {"A", "Hjac", "Scoord", "K_path"}, "path")
    need(type(path["A"]) is list and len(path["A"]) == 2
         and type(path["A"][0]) is list, "matrix_shape", "path.A")
    m = len(path["A"][0])
    need(1 <= m <= MAX_DIM, "dimension_limit", "raw_force_dimension")
    need(type(path["Hjac"]) is list and 1 <= len(path["Hjac"]) <= MAX_DIM,
         "dimension_limit", "segment_count")
    R = len(path["Hjac"])
    first = path["Hjac"][0]
    need(type(first) is list and len(first) == m and type(first[0]) is list,
         "matrix_shape", "path.Hjac[0]")
    n = len(first[0])
    need(1 <= n <= MAX_DIM and R * m * n <= MAX_PATH_TERMS,
         "dimension_limit", "path_terms")
    A = matrix(path["A"], 2, m, "path.A", nonnegative=False)
    H = [matrix(h, m, n, f"path.Hjac[{s}]") for s, h in enumerate(path["Hjac"])]
    need(type(path["Scoord"]) is list and len(path["Scoord"]) == R,
         "matrix_shape", "path.Scoord")
    S = [matrix(v, n, 4, f"path.Scoord[{s}]") for s, v in enumerate(path["Scoord"])]
    K = matrix(path["K_path"], 2, 4, "path.K_path")
    G = matrix(payload["K_cert"], 2, 4, "K_cert")
    # Same explicit order/formula as existing pathK/segmentK, over exact rationals.
    computed = [[sum((abs(A[a][i]) * H[s][i][j] * S[s][j][k]
                     for s in range(R) for i in range(m) for j in range(n)), Fraction(0))
                 for k in range(4)] for a in range(2)]
    entries = []
    for a in range(2):
        for k in range(4):
            loc = f"[{a},{k}]"
            need(K[a][k] == computed[a][k], "pathK_identity_mismatch", loc)
            # Positive denominators: cross difference >= 0 iff K[a,k] <= G[a,k].
            lhs, rhs = K[a][k], G[a][k]
            cross = rhs.numerator * lhs.denominator - lhs.numerator * rhs.denominator
            need(cross >= 0, "componentwise_comparison_failed", loc)
            entries.append({"row": COORDINATES["force"][a], "column": COORDINATES["state"][k],
                            "path": str(lhs), "cert": str(rhs), "slack": str(rhs - lhs),
                            "cross_difference": str(cross)})
    return {
        "status": "unbound_exact_arithmetic_pass",
        "arithmetic_valid": True,
        "path_formula": "sum_s_i_j abs(A[a,i])*Hjac[s,i,j]*Scoord[s,j,k]",
        "path_formula_source_sha256": PATH_SOURCE_SHA256,
        "identity_entries_checked": 8,
        "comparison_entries_checked": 8,
        "entries": entries,
        "K_cert": canonical_matrix(G),
        "K_path_data_sha256": gain_digest(K),
        "K_cert_data_sha256": gain_digest(G),
        **boundary(),
    }


def check_bytes(raw: bytes) -> dict:
    verify_path_source()
    result = _check_payload(parse_bytes(raw))
    verify_path_source()
    result["input_bytes_sha256"] = hashlib.sha256(raw).hexdigest()
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="JSON path, or - for stdin")
    args = parser.parse_args()
    try:
        if args.input == "-":
            raw = sys.stdin.buffer.read(MAX_BYTES + 1)
        else:
            with Path(args.input).open("rb") as stream:
                raw = stream.read(MAX_BYTES + 1)
        result = check_bytes(raw)
    except (Rejected, OSError, ValueError, RecursionError, OverflowError) as exc:
        print(json.dumps({"status": "rejected_or_uncheckable", "arithmetic_valid": False,
                          "code": getattr(exc, "code", "input_or_resource_error"),
                          "location": getattr(exc, "location", str(exc)), **boundary()},
                         ensure_ascii=False, sort_keys=True))
        return 1
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
