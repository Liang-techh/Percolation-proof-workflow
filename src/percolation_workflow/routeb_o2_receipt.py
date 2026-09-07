"""Fail-closed intake for a deployed Route-B O2 runtime receipt.

The receipt describes enough execution provenance for coordinator admission. It
is not a proof, a comparator result, or a registry entry. In particular, a
complete receipt may only become an input to the later Lean/coverage gates.
"""
from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any


RUNTIME_FIELDS = (
    "julia_version", "os_architecture", "blas", "libm",
    "rounding_mode", "fastmath_fma_threading",
)
CONSTANT_FIELDS = ("mu_bits", "h_bits", "two_h_bits", "pi_bits", "pi_over_two_bits")
BOX_FIELDS = ("input_box", "output_enclosure", "dependency_ids")


@dataclass(frozen=True)
class RouteBO2RuntimeReceiptAudit:
    status: str
    missing: tuple[str, ...] = ()
    errors: tuple[str, ...] = ()
    source_sha256: str | None = None
    operation_schedule_hash: str | None = None
    box_count: int = 0
    formal_certificate_allowed: bool = False
    registry_promoted: bool = False


def _missing_mapping_fields(value: Any, fields: Sequence[str], prefix: str) -> list[str]:
    if not isinstance(value, Mapping):
        return [prefix]
    return [f"{prefix}.{field}" for field in fields if not value.get(field)]


def audit_routeb_o2_runtime_receipt(
    receipt: Mapping[str, Any],
    *,
    expected_source_sha256: str,
    expected_operation_schedule_hash: str,
) -> RouteBO2RuntimeReceiptAudit:
    """Audit receipt completeness and binding without admitting O2.

    Hash mismatches and explicit boundary violations are ``REJECTED``. Missing
    evidence is ``PENDING``. Only a structurally complete, hash-bound receipt
    reaches ``READY_FOR_COORDINATOR_ADMISSION``; that status remains below the
    Lean/kernel, comparator, and full coverage gates.
    """
    if not isinstance(receipt, Mapping):
        return RouteBO2RuntimeReceiptAudit("REJECTED", errors=("receipt_not_mapping",))
    missing: list[str] = []
    errors: list[str] = []
    source = receipt.get("source_sha256")
    schedule = receipt.get("operation_schedule_hash")
    if not source:
        missing.append("source_sha256")
    elif str(source).upper() != expected_source_sha256.upper():
        errors.append("source_hash_mismatch")
    if not schedule:
        missing.append("operation_schedule_hash")
    elif str(schedule).upper() != expected_operation_schedule_hash.upper():
        errors.append("operation_schedule_hash_mismatch")
    missing.extend(_missing_mapping_fields(receipt.get("runtime"), RUNTIME_FIELDS, "runtime"))
    missing.extend(_missing_mapping_fields(receipt.get("constants"), CONSTANT_FIELDS, "constants"))
    if not receipt.get("operation_schedule"):
        missing.append("operation_schedule")
    line_hashes = receipt.get("source_line_range_hashes")
    if not isinstance(line_hashes, Mapping):
        missing.append("source_line_range_hashes")
    else:
        for name in ("fk_frames", "mass_matrix", "potential", "arm_MCG", "exact_ddq"):
            if not line_hashes.get(name):
                missing.append(f"source_line_range_hashes.{name}")
    boxes = receipt.get("boxes")
    if not isinstance(boxes, Sequence) or isinstance(boxes, (str, bytes)) or not boxes:
        missing.append("boxes")
        box_count = 0
    else:
        box_count = len(boxes)
        for index, box in enumerate(boxes):
            if not isinstance(box, Mapping):
                errors.append(f"boxes[{index}]_not_mapping")
                continue
            missing.extend(
                f"boxes[{index}].{field}" for field in BOX_FIELDS if not box.get(field)
            )
    coverage = receipt.get("coverage")
    if not isinstance(coverage, Mapping) or coverage.get("all_boxes_covered") is not True:
        missing.append("coverage.all_boxes_covered")
    if receipt.get("finite_non_nan_no_overflow") is not True:
        missing.append("finite_non_nan_no_overflow")
    if receipt.get("registry_promoted") is True:
        errors.append("registry_boundary_violation")
    if receipt.get("formal_certificate_allowed") is True:
        errors.append("formal_gate_boundary_violation")
    if errors:
        status = "REJECTED"
    elif missing:
        status = "PENDING_REQUIRED_FIELDS"
    else:
        status = "READY_FOR_COORDINATOR_ADMISSION"
    return RouteBO2RuntimeReceiptAudit(
        status=status,
        missing=tuple(missing),
        errors=tuple(errors),
        source_sha256=str(source) if source else None,
        operation_schedule_hash=str(schedule) if schedule else None,
        box_count=box_count,
    )


__all__ = ["RouteBO2RuntimeReceiptAudit", "audit_routeb_o2_runtime_receipt"]
