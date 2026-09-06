"""Fail-closed structural audit for Route-B residual receipts.

The audit checks that all six residual channels and the implementation-error
channels are keyed to one full-state point.  It is deliberately not a proof
checker: a structurally valid receipt remains external evidence and cannot
enter the theorem registry or formal admission gate.
"""
from __future__ import annotations

from collections.abc import Mapping
from typing import Any


RESIDUAL_CHANNELS = (
    "rho_C", "rho_G", "rho_mgl", "rho_kc", "rho_mass", "rho_remote",
)
REMAINDER_COMPONENTS = ("fd_remainder", "rounding_remainder", "solve_remainder")
IDENTITY_FIELDS = (
    "cell_id", "q_box", "dq_box", "t_box", "w_box", "source_sha256",
    "norm_convention", "outward_rounding_mode",
)

FULL_STATE_KEYS = ("q", "dq", "t", "w", "a", "aB", "aD")
FULL_STATE_OPERATOR_KEYS = ("MBD", "MBD_aD")
FULL_STATE_DESCRIPTOR_KEYS = ("B", "D", "rhs_B", "rhs_D")


def audit_residual_ledger(receipt: Mapping[str, Any]) -> dict[str, Any]:
    """Return a read-only structural verdict for one residual-ledger receipt."""
    errors: list[str] = []
    if not isinstance(receipt, Mapping):
        return {
            "schema_version": 1, "status": "OPEN_FAIL_CLOSED",
            "formal_certificate_allowed": False, "errors": ["receipt_not_mapping"],
        }
    if receipt.get("schema") != "routeb.residual_ledger.v1":
        errors.append("schema_mismatch")
    for field in IDENTITY_FIELDS:
        value = receipt.get(field)
        if not isinstance(value, (str, list, dict)) or not value:
            errors.append(f"missing_identity:{field}")

    channels = receipt.get("channels")
    if not isinstance(channels, Mapping):
        errors.append("channels_not_mapping")
        channels = {}
    for channel in RESIDUAL_CHANNELS:
        record = channels.get(channel)
        if not isinstance(record, Mapping):
            errors.append(f"missing_channel:{channel}")
            continue
        for field in ("source_field", "bound", "status"):
            if field not in record or record[field] in (None, "", []):
                errors.append(f"missing_channel_field:{channel}:{field}")

    remainder = receipt.get("remainder_total")
    if not isinstance(remainder, Mapping):
        errors.append("missing_remainder_total")
    else:
        if remainder.get("charged_once") is not True:
            errors.append("remainder_not_charged_once")
        components = remainder.get("components")
        if components != list(REMAINDER_COMPONENTS):
            errors.append("remainder_components_not_canonical")
        if not remainder.get("bound"):
            errors.append("missing_remainder_bound")

    charged = receipt.get("charged_channels")
    expected = list(RESIDUAL_CHANNELS) + ["remainder_total"]
    if charged != expected:
        errors.append("charged_channels_not_exactly_once")

    return {
        "schema_version": 1,
        "status": "STRUCTURAL_PASS" if not errors else "OPEN_FAIL_CLOSED",
        "formal_certificate_allowed": False,
        "registry_eligible": False,
        "errors": errors,
    }


def audit_full_state_binding(receipt: Mapping[str, Any]) -> dict[str, Any]:
    """Audit the keyed full-state physical-action interface.

    This is intentionally separate from :func:`audit_residual_ledger`: legacy
    residual receipts can remain structurally useful, while a physical Route-B
    receipt must prove that every state/operator/descriptor payload belongs to
    one state key and one source snapshot.  Passing this structural audit is
    never a numerical proof or a registry admission.
    """
    errors: list[str] = []
    if not isinstance(receipt, Mapping):
        errors.append("receipt_not_mapping")
        return {
            "schema_version": 1, "status": "OPEN_FAIL_CLOSED",
            "formal_certificate_allowed": False,
            "registry_eligible": False, "errors": errors,
        }
    if receipt.get("schema") != "routeb.full_state_binding.v1":
        errors.append("schema_mismatch")
    state_key = receipt.get("full_state_key")
    source_snapshot = receipt.get("source_snapshot")
    if not isinstance(state_key, str) or not state_key.strip():
        errors.append("missing_full_state_key")
    if not isinstance(source_snapshot, (str, Mapping)) or not source_snapshot:
        errors.append("missing_source_snapshot")
    if receipt.get("norm_convention") not in {"induced_2", "induced_infinity"}:
        errors.append("unsupported_norm_convention")

    payloads = receipt.get("payloads")
    if not isinstance(payloads, Mapping):
        errors.append("payloads_not_mapping")
        payloads = {}
    for field in FULL_STATE_KEYS + FULL_STATE_OPERATOR_KEYS + FULL_STATE_DESCRIPTOR_KEYS:
        payload = payloads.get(field)
        if not isinstance(payload, Mapping):
            errors.append(f"missing_payload:{field}")
            continue
        if "value" not in payload or payload["value"] in (None, "", []):
            errors.append(f"missing_payload_value:{field}")
        if payload.get("full_state_key") != state_key:
            errors.append(f"payload_key_mismatch:{field}")
        if payload.get("source_snapshot") != source_snapshot:
            errors.append(f"payload_source_mismatch:{field}")
    if receipt.get("action_semantics") != "MBD_times_aD":
        errors.append("remote_action_semantics_not_explicit")
    return {
        "schema_version": 1,
        "status": "STRUCTURAL_PASS" if not errors else "OPEN_FAIL_CLOSED",
        "formal_certificate_allowed": False,
        "registry_eligible": False,
        "errors": errors,
    }


__all__ = [
    "IDENTITY_FIELDS", "REMAINDER_COMPONENTS", "RESIDUAL_CHANNELS",
    "FULL_STATE_KEYS", "FULL_STATE_OPERATOR_KEYS", "FULL_STATE_DESCRIPTOR_KEYS",
    "audit_full_state_binding", "audit_residual_ledger",
]
