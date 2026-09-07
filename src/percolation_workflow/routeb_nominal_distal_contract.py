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
from collections import defaultdict
from fractions import Fraction


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
EXPECTED_BRIDGE = {
    "block_B": "4,5",
    "D_coordinates": "1,2,3,6",
    "r_hat": "0,1,-6377/6250,0",
    "rho_num": "10616159325566083327957",
    "rho_den": "39062500000000000000000",
    "orthogonality_entries": "3",
    "retained_polynomial_terms": "46",
    "retained_max_total_cs_degree": "5",
    "full_MBB_12": "153080849893419/50000000000000000000000000000000",
    "full_MBB_21": "153080849893419/50000000000000000000000000000000",
    "evidence_level": "algebraic_subcertificate",
}
EXPECTED_TAIL_META = {
    "pmi_dimension": "3",
    "schur_scalar_dimension": "1",
    "scalar_terms": "27",
    "scalar_max_total_cs_degree": "6",
    "rho": "10616159325566083327957/39062500000000000000000",
    "delta_sq": "1/160000",
    "active_variables": "c3;s3;c4;s4;c5;s5",
    "energy_accounting": "tail_only_no_double_count",
    "evidence_level": "algebraic_sos_input_candidate",
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


@dataclass(frozen=True)
class RouteBPhysicalRationalTailAudit:
    """Exact-rational tail seam status, still below theorem admission."""

    status: str
    artifact_sha256: str | None
    source_sha256: str | None
    scalar_terms: int
    scalar_max_total_cs_degree: int
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


def _read_exact_scalar_polynomial(text: str) -> tuple[dict[tuple[int, ...], Fraction], list[str]]:
    rows = csv.DictReader(io.StringIO(text))
    required = {"row", "col", "num", "den", *(f"e{k}" for k in range(1, 13))}
    if not rows.fieldnames or not required.issubset(rows.fieldnames):
        return {}, ["scalar_polynomial_header_mismatch"]
    polynomial: defaultdict[tuple[int, ...], Fraction] = defaultdict(Fraction)
    errors: list[str] = []
    for line_no, row in enumerate(rows, start=2):
        try:
            if row.get("row") != "1" or row.get("col") != "1":
                errors.append(f"scalar_polynomial_coordinate_mismatch:{line_no}")
            monomial = tuple(int(row[f"e{k}"]) for k in range(1, 13))
            if any(power < 0 for power in monomial):
                errors.append(f"scalar_polynomial_negative_exponent:{line_no}")
            denominator = int(row["den"])
            numerator = int(row["num"])
            if denominator <= 0:
                errors.append(f"scalar_polynomial_nonpositive_denominator:{line_no}")
            polynomial[monomial] += Fraction(numerator, denominator)
        except (KeyError, TypeError, ValueError, ZeroDivisionError):
            errors.append(f"scalar_polynomial_malformed_row:{line_no}")
    return ({monomial: value for monomial, value in polynomial.items() if value}, errors)


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


def audit_routeb_physical_rational_tail(
    bridge_csv_text: str,
    tail_meta_csv_text: str,
    scalar_csv_text: str,
    *,
    artifact_sha256: str | None = None,
    source_sha256: str | None = None,
) -> RouteBPhysicalRationalTailAudit:
    """Check the exact rational tail seam without asserting global positivity."""
    bridge = _read_metric_csv(bridge_csv_text)
    meta = _read_metric_csv(tail_meta_csv_text)
    errors = [
        f"bridge_mismatch:{key}"
        for key, expected in EXPECTED_BRIDGE.items()
        if bridge.get(key) != expected
    ]
    errors.extend(
        f"tail_meta_mismatch:{key}"
        for key, expected in EXPECTED_TAIL_META.items()
        if meta.get(key) != expected
    )
    polynomial, polynomial_errors = _read_exact_scalar_polynomial(scalar_csv_text)
    errors.extend(polynomial_errors)
    terms = len(polynomial)
    degree = max((sum(monomial) for monomial in polynomial), default=0)
    if terms != 27:
        errors.append("scalar_polynomial_term_count_mismatch")
    if degree != 6:
        errors.append("scalar_polynomial_degree_mismatch")
    if any(any(power != 0 for power in monomial[:4] + monomial[10:])
           for monomial in polynomial):
        errors.append("scalar_polynomial_active_variable_mismatch")
    status = "EXACT_RATIONAL_TAIL_CANDIDATE" if not errors else "OPEN_FAIL_CLOSED"
    return RouteBPhysicalRationalTailAudit(
        status=status,
        artifact_sha256=artifact_sha256,
        source_sha256=source_sha256,
        scalar_terms=terms,
        scalar_max_total_cs_degree=degree,
        errors=tuple(errors),
    )


__all__ = [
    "EXPECTED_AUDIT",
    "EXPECTED_INTERFACE",
    "EXPECTED_BRIDGE",
    "EXPECTED_TAIL_META",
    "RouteBNominalDistalBridgeAudit",
    "RouteBPhysicalRationalTailAudit",
    "audit_routeb_nominal_distal_bridge",
    "audit_routeb_physical_rational_tail",
]
