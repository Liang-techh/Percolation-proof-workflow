"""Fail-closed checker for a concrete single-box Route-B P8 RHS receipt."""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
from typing import Any


COORDINATE_ORDER = [*(f"q{i}" for i in range(1, 7)),
                    *(f"v{i}" for i in range(1, 7)), "w", "c"]
SCHEMA = "routeb-p8-rhs-endpoint-receipt-v1"
EXPECTED_CANDIDATE_ID = "robot_final/full_dh_probe+dhport_lib"
EXPECTED_BOX_ID = "p8-local-zero-cell-qv-w-1e-2-c-2"
EXPECTED_BOX_LO = ["-0.01"] * 12 + ["-0.01", "-2"]
EXPECTED_BOX_HI = ["0.01"] * 12 + ["0.01", "2"]
EXPECTED_SOURCE_STATE_ORDER = [*(f"q{i}" for i in range(1, 7)),
                               *(f"v{i}" for i in range(1, 7)), "w"]
SOURCE_SPECS = (
    "robot_final/cross_validation/routeB_reachability_full_dh_probe.jl",
    "robot_final/dhport_lib.jl",
)


class ReceiptError(ValueError):
    pass


def _exact(value: Any, field: str, *, allow_null: bool = False) -> Fraction | None:
    if value is None and allow_null:
        return None
    if not isinstance(value, str) or not value.strip():
        raise ReceiptError(f"{field} must be an exact decimal or rational string")
    text = value.strip()
    try:
        if "/" in text:
            numerator, denominator = text.split("/", 1)
            result = Fraction(int(numerator), int(denominator))
        else:
            result = Fraction(text)
    except (ValueError, ZeroDivisionError) as exc:
        raise ReceiptError(f"{field} is not an exact finite number") from exc
    return result


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _require_object(value: Any, field: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ReceiptError(f"{field} must be an object")
    return value


def _check_sources(receipt: dict[str, Any], source_root: Path | None) -> list[dict[str, str]]:
    rows = receipt.get("source_hashes")
    if not isinstance(rows, list) or len(rows) != len(SOURCE_SPECS):
        raise ReceiptError("source_hashes must contain exactly the two declared source files")
    checked = []
    for index, (row, expected_path) in enumerate(zip(rows, SOURCE_SPECS)):
        item = _require_object(row, f"source_hashes[{index}]")
        if item.get("path") != expected_path:
            raise ReceiptError(f"source_hashes[{index}].path drifted from the selected candidate")
        digest = item.get("sha256")
        if not isinstance(digest, str) or len(digest) != 64 or any(
                char not in "0123456789abcdef" for char in digest):
            raise ReceiptError(f"source_hashes[{index}].sha256 must be lowercase SHA-256")
        if source_root is not None:
            path = (source_root / Path(expected_path)).resolve()
            if not path.is_file() or not path.is_relative_to(source_root.resolve()):
                raise ReceiptError(f"declared source is missing or escapes source root: {expected_path}")
            actual = _sha256(path)
            if actual != digest:
                raise ReceiptError(f"source hash mismatch: {expected_path}")
        checked.append({"path": expected_path, "sha256": digest})
    return checked


def _check_vectors(receipt: dict[str, Any]) -> None:
    if receipt.get("coordinate_order") != COORDINATE_ORDER:
        raise ReceiptError("coordinate_order must be exactly q1..q6,v1..v6,w,c")
    if receipt.get("dimension") != 14:
        raise ReceiptError("dimension must be exactly 14")
    box = _require_object(receipt.get("local_box"), "local_box")
    if box.get("id") != EXPECTED_BOX_ID:
        raise ReceiptError("local_box id drifted from the selected single-box scope")
    lo = box.get("lo")
    hi = box.get("hi")
    if not isinstance(lo, list) or not isinstance(hi, list) or len(lo) != 14 or len(hi) != 14:
        raise ReceiptError("local_box lo/hi must contain exactly 14 endpoints")
    if lo != EXPECTED_BOX_LO or hi != EXPECTED_BOX_HI:
        raise ReceiptError("local_box endpoints drifted from the selected single-box scope")
    for index, (low, high) in enumerate(zip(lo, hi)):
        low_f = _exact(low, f"local_box.lo[{index}]")
        high_f = _exact(high, f"local_box.hi[{index}]")
        assert low_f is not None and high_f is not None
        if low_f > high_f:
            raise ReceiptError(f"local_box has lo > hi at coordinate {COORDINATE_ORDER[index]}")


def _check_source_contract(receipt: dict[str, Any]) -> None:
    contract = _require_object(receipt.get("source_contract"), "source_contract")
    if contract.get("julia_state_dimension") != 13:
        raise ReceiptError("source contract must declare Julia full_rhs! dimension 13")
    if contract.get("payload_dimension") != 14:
        raise ReceiptError("source contract must declare lifted payload dimension 14")
    if contract.get("source_function") != "full_rhs!":
        raise ReceiptError("source contract function must be full_rhs!")
    if contract.get("source_state_order") != EXPECTED_SOURCE_STATE_ORDER:
        raise ReceiptError("source contract state order drifted")
    if contract.get("lifted_tail") != {"c": "sidecar parameter; not consumed by full_rhs!"}:
        raise ReceiptError("source contract c-tail binding is not the declared open sidecar")
    if contract.get("source_literal_tail") != {"w_rhs": "0", "c_rhs": "unbound"}:
        raise ReceiptError("source contract tail semantics drifted")
    if contract.get("ramp_binding") != "OPEN":
        raise ReceiptError("ramp binding must remain OPEN")


def _check_coordinate_mapping(receipt: dict[str, Any]) -> None:
    rows = receipt.get("coordinate_mapping")
    if not isinstance(rows, list) or len(rows) != 14:
        raise ReceiptError("coordinate_mapping must contain exactly 14 rows")
    for index, row in enumerate(rows):
        item = _require_object(row, f"coordinate_mapping[{index}]")
        expected_input = (f"u[{index + 1}]" if index < 13 else None)
        expected_output = (f"du[{index + 1}]" if index < 13 else None)
        expected_role = ("q" if index < 6 else "dq" if index < 12 else
                         "w" if index == 12 else "c_sidecar")
        expected_status = "source-text-only" if index < 13 else "OPEN"
        expected = {
            "payload_index_zero_based": index,
            "payload_index_one_based": index + 1,
            "name": COORDINATE_ORDER[index],
            "role": expected_role,
            "julia_full_rhs_input": expected_input,
            "julia_full_rhs_output": expected_output,
            "binding_status": expected_status,
        }
        if item != expected:
            raise ReceiptError(f"coordinate_mapping drift at index {index}")


def _check_intervals(receipt: dict[str, Any], *, allow_pending: bool) -> bool:
    rows = receipt.get("rhs_endpoint_intervals")
    if not isinstance(rows, list) or len(rows) != 14:
        raise ReceiptError("rhs_endpoint_intervals must contain exactly 14 rows")
    complete = True
    for index, row in enumerate(rows):
        item = _require_object(row, f"rhs_endpoint_intervals[{index}]")
        if item.get("coordinate") != COORDINATE_ORDER[index]:
            raise ReceiptError(f"rhs endpoint coordinate drift at index {index}")
        low = _exact(item.get("lower"), f"rhs[{COORDINATE_ORDER[index]}].lower", allow_null=True)
        high = _exact(item.get("upper"), f"rhs[{COORDINATE_ORDER[index]}].upper", allow_null=True)
        if (low is None) != (high is None):
            raise ReceiptError(f"rhs interval must have both endpoints or neither: {COORDINATE_ORDER[index]}")
        if low is None:
            complete = False
        elif low > high:  # type: ignore[operator]
            raise ReceiptError(f"rhs interval has lo > hi: {COORDINATE_ORDER[index]}")
    if not complete and not allow_pending:
        raise ReceiptError("endpoint payload is incomplete; refusing to admit a concrete receipt")
    return complete


def validate(receipt: dict[str, Any], *, source_root: Path | None = None,
             allow_pending: bool = False) -> dict[str, Any]:
    if not isinstance(receipt, dict):
        raise ReceiptError("receipt must be an object")
    if receipt.get("schema") != SCHEMA:
        raise ReceiptError(f"unsupported schema: {receipt.get('schema')!r}")
    if receipt.get("candidate_id") != EXPECTED_CANDIDATE_ID:
        raise ReceiptError("candidate_id drifted from the selected file-level candidate")
    if receipt.get("formal_admission") != "not_theorem" or receipt.get("LEAN_VERIFIED") is not False:
        raise ReceiptError("formal admission must remain not_theorem with LEAN_VERIFIED=false")
    if receipt.get("binding_status") != "source-text-snapshot-only":
        raise ReceiptError("binding_status must remain source-text-snapshot-only")
    _check_vectors(receipt)
    _check_source_contract(receipt)
    _check_coordinate_mapping(receipt)
    sources = _check_sources(receipt, source_root)
    parameters = _require_object(receipt.get("parameters"), "parameters")
    expected_parameters = {
        "horizon_T": "1", "initial_radius": "0.15", "eta_star": "5.6",
        "disturbance_bound": "sqrt(3)", "mass_regularizer": "1e-6",
        "fd_step": "1e-5", "arithmetic": "IEEE-754 Float64 source arithmetic",
    }
    if parameters != expected_parameters:
        raise ReceiptError("parameter metadata drifted from the selected candidate")
    rounding = _require_object(receipt.get("rounding"), "rounding")
    if rounding.get("source_runtime") != "Float64":
        raise ReceiptError("source_runtime must be Float64")
    if rounding.get("endpoint_encoding") != "exact_decimal_or_rational_text_required":
        raise ReceiptError("endpoint encoding must remain exact decimal/rational text")
    if rounding.get("endpoint_rounding") not in {"not_authenticated", "outward"}:
        raise ReceiptError("endpoint rounding must be not_authenticated or outward")
    if rounding.get("direction") not in {"unspecified", "outward"}:
        raise ReceiptError("rounding direction must be unspecified or outward")
    complete = _check_intervals(receipt, allow_pending=allow_pending)
    if complete:
        if receipt.get("receipt_status") != "concrete_endpoint_payload":
            raise ReceiptError("complete intervals require receipt_status=concrete_endpoint_payload")
        if rounding.get("endpoint_rounding") != "outward" or rounding.get("direction") != "outward":
            raise ReceiptError("complete payload requires explicit outward endpoint rounding metadata")
        status = "candidate_payload_only"
    else:
        if receipt.get("receipt_status") != "pending_endpoint_payload":
            raise ReceiptError("incomplete intervals require receipt_status=pending_endpoint_payload")
        status = "pending_endpoint_payload"
    return {
        "schema": "routeb-p8-rhs-endpoint-receipt-report-v1",
        "status": status,
        "coordinate_count": 14,
        "source_count": len(sources),
        "formal_admission": None,
        "binding_conclusion": None,
        "coverage_scope": "one explicit local box only",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("receipt", type=Path)
    parser.add_argument("--source-root", type=Path)
    parser.add_argument("--allow-pending", action="store_true")
    args = parser.parse_args(argv)
    try:
        document = json.loads(args.receipt.read_text(encoding="utf-8"))
        result = validate(document, source_root=args.source_root,
                           allow_pending=args.allow_pending)
    except (OSError, json.JSONDecodeError, ReceiptError) as exc:
        print(json.dumps({
            "schema": "routeb-p8-rhs-endpoint-receipt-report-v1",
            "status": "rejected",
            "formal_admission": None,
            "binding_conclusion": None,
            "error": str(exc),
        }, ensure_ascii=False, indent=2))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
