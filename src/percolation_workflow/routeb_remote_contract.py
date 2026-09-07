"""Fail-closed contract for binding the Route-B remote action ``M_BD a_D``.

The exact projection obstruction shows that a block-only premise cannot bound
the remote action.  This module records the two smallest admissible repair
shapes without pretending that a structurally complete receipt is a proof:

* ``full_state``: the remote acceleration and coupling operator are bounded
  on the same covered full-state domain;
* ``d_row_schur``: a D-row residual, regularized inverse, coupling operator,
  and an explicit elimination identity are all supplied.

Neither mode performs interval arithmetic or Lean verification.  The output
is an input contract for those later gates, and therefore can never promote a
candidate into the theorem registry.
"""
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any


REMOTE_BINDING_SCHEMA = "routeb.remote_binding.v1"
BLOCK_COORDS = (4, 5)
REMOTE_COORDS = (1, 2, 3, 6)
MODES = ("full_state", "d_row_schur")

_COMMON_FIELDS = (
    "full_state_key",
    "source_snapshot",
    "block_coords",
    "remote_coords",
    "norm_convention",
    "action_semantics",
)
_MODE_FIELDS = {
    "full_state": (
        "aD_bound",
        "MBD_operator_bound",
        "remote_action_bound",
        "descriptor_identity",
    ),
    "d_row_schur": (
        "d_row_residual_bound",
        "MDD_regularized_inverse_bound",
        "MBD_operator_bound",
        "schur_elimination_identity",
    ),
}


@dataclass(frozen=True)
class RouteBRemoteBindingAudit:
    """Structural result for one candidate remote-action receipt."""

    status: str
    mode: str | None
    required_fields: tuple[str, ...]
    errors: tuple[str, ...] = ()
    formal_certificate_allowed: bool = False
    registry_eligible: bool = False


def _missing_or_empty(receipt: Mapping[str, Any], field: str) -> bool:
    value = receipt.get(field)
    return value in (None, "", [], {})


def audit_routeb_remote_binding(
    receipt: Mapping[str, Any],
) -> RouteBRemoteBindingAudit:
    """Check that a remote-action receipt has a non-block-only binding.

    This is deliberately a shape check.  A ``STRUCTURAL_PASS`` means only that
    the later exact/source/Lean gates have enough named premises to inspect;
    it does not assert any inequality represented by those premises.
    """
    errors: list[str] = []
    if not isinstance(receipt, Mapping):
        return RouteBRemoteBindingAudit(
            status="OPEN_FAIL_CLOSED",
            mode=None,
            required_fields=(),
            errors=("receipt_not_mapping",),
        )

    if receipt.get("schema") != REMOTE_BINDING_SCHEMA:
        errors.append("schema_mismatch")

    mode = receipt.get("binding_mode")
    if mode not in MODES:
        errors.append("unsupported_binding_mode")
        required_fields: tuple[str, ...] = ()
    else:
        required_fields = _MODE_FIELDS[mode]

    for field in _COMMON_FIELDS:
        if _missing_or_empty(receipt, field):
            errors.append(f"missing_common_field:{field}")

    if tuple(receipt.get("block_coords", ())) != BLOCK_COORDS:
        errors.append("block_coordinate_order_mismatch")
    if tuple(receipt.get("remote_coords", ())) != REMOTE_COORDS:
        errors.append("remote_coordinate_order_mismatch")
    if receipt.get("norm_convention") not in {"induced_2", "induced_infinity"}:
        errors.append("unsupported_norm_convention")
    if receipt.get("action_semantics") != "MBD_times_aD":
        errors.append("remote_action_semantics_not_explicit")

    # This field is intentionally forbidden even when a stronger-looking
    # mode is also present: it is the exact failure mode established by the
    # q=0 projection countermodel.
    if receipt.get("block_only_remote_bound") is not None:
        errors.append("block_only_remote_bound_forbidden")

    for field in required_fields:
        if _missing_or_empty(receipt, field):
            errors.append(f"missing_mode_field:{mode}:{field}")

    status = "STRUCTURAL_PASS" if not errors else "OPEN_FAIL_CLOSED"
    return RouteBRemoteBindingAudit(
        status=status,
        mode=mode if isinstance(mode, str) else None,
        required_fields=required_fields,
        errors=tuple(errors),
    )


__all__ = [
    "BLOCK_COORDS",
    "MODES",
    "REMOTE_BINDING_SCHEMA",
    "REMOTE_COORDS",
    "RouteBRemoteBindingAudit",
    "audit_routeb_remote_binding",
]
