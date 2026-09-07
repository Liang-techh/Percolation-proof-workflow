"""Fail-closed intake contract for the Route-B nominal distal bridge.

The deployed research artifact separates a nominal distal acceleration from a
reduced descriptor variable and retains the cross-block port.  This is the
preferred P4 route because it preserves correlation instead of charging a
coarse ``||a_D||`` bound.  The checker below validates only the exact artifact
shape and provenance; it does not prove the polynomial inequalities or source
semantics.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
import io
from typing import Mapping


EXPECTED_AUDIT = {
    "status": "DH_NOMINAL_DISTAL_BRIDGE_AUDIT",
    "mass_regularizer": "1//1000000",
    "full_D_descriptor_rows": "4",
    "nominal_equation_rows": "4",
    "reduced_equation_rows": "4",
    "retained_port_rows": "2",
    "split_identity_exact": "true",
    "nominal_equation_max_degree": "10",
    "reduced_equation_max_degree": "9",
    "port_max_degree": "6",
    "full_DH_rhs_semantics": "true",
    "formal_certificate_allowed": "false",
}
EXPECTED_INTERFACE = {
    "block_B": "4;5",
    "block_D": "1;2;3;6",
    "inverse_substitution": "false",
    "nominal_remote_equation": "M_DD(q)^(-1)*(b_D-M0_DB*a_B)",
    "v_descriptor_equation": "M_DD(q)*v+DeltaM_DB(q)*a_B=0",
    "force_port_equation": "r_B-M_BD(q)*v=0",
}


@dataclass(frozen=True)
class RouteBNominalDistalBridgeAudit:
    status: str
    artifact_sha256: str | None
    source_sha256: str | None
    block_coordinates: tuple[int, ...]
    remote_coordinates: tuple[int, ...]
    errors: tuple[str, ...] = ()
    formal_certificate_allowed: bool = False
    registry_eligible: bool = False


def _read_metric_csv(text: str) -> dict[str, str]:
    rows = csv.DictReader(io.StringIO(text))
    result: dict[str, str] = {}
    if not rows.fieldnames or "value" not in rows.fieldnames:
        return result
    key_column = "metric" if "metric" in rows.fieldnames else "field"
    if key_column not in rows.fieldnames:
        return result
    for row in rows:
        key, value = row.get(key_column), row.get("value")
        if key and value is not None:
            result[key] = value
    return result


def _coordinates(value: str | None) -> tuple[int, ...]:
    if not value:
        return ()
    try:
        return tuple(int(item) for item in value.split(";"))
    except ValueError:
        return ()


def audit_routeb_nominal_distal_bridge(
    audit_csv_text: str,
    interface_csv_text: str,
    *,
    artifact_sha256: str | None = None,
    source_sha256: str | None = None,
) -> RouteBNominalDistalBridgeAudit:
    """Check the two exact CSV contracts without upgrading their evidence."""
    audit = _read_metric_csv(audit_csv_text)
    interface = _read_metric_csv(interface_csv_text)
    errors = [
        f"audit_mismatch:{key}"
        for key, expected in EXPECTED_AUDIT.items()
        if audit.get(key) != expected
    ]
    errors.extend(
        f"interface_mismatch:{key}"
        for key, expected in EXPECTED_INTERFACE.items()
        if interface.get(key) != expected
    )
    block = _coordinates(interface.get("block_B"))
    remote = _coordinates(interface.get("block_D"))
    if block != (4, 5):
        errors.append("block_coordinate_order_mismatch")
    if remote != (1, 2, 3, 6):
        errors.append("remote_coordinate_order_mismatch")
    status = "EXACT_DESCRIPTOR_BRIDGE_CANDIDATE" if not errors else "OPEN_FAIL_CLOSED"
    return RouteBNominalDistalBridgeAudit(
        status=status,
        artifact_sha256=artifact_sha256,
        source_sha256=source_sha256,
        block_coordinates=block,
        remote_coordinates=remote,
        errors=tuple(errors),
    )


__all__ = [
    "EXPECTED_AUDIT",
    "EXPECTED_INTERFACE",
    "RouteBNominalDistalBridgeAudit",
    "audit_routeb_nominal_distal_bridge",
]
