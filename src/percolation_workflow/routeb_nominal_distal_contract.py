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
EXPECTED_GRAM_AUDIT = {
    "status": "PASS",
    "denominator_cap": "1000000000000",
    "exact_bareiss_positive": "true",
    "gram_blocks": "14",
    "max_gram_dimension": "83",
    "formal_certificate_allowed": "false",
    "evidence_level": "rigorous_numerical_tail_subcertificate_candidate",
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


@dataclass(frozen=True)
class RouteBPhysicalRationalGramAudit:
    """Exact rational Gram payload status, below Lean/kernel admission."""

    status: str
    artifact_sha256: str | None
    source_sha256: str | None
    gram_blocks: int
    max_gram_dimension: int
    min_ldl_pivot: Fraction | None
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


def _exact_gram_groups(text: str):
    rows = csv.DictReader(io.StringIO(text))
    required = {"kind", "clique", "constraint", "block", "row", "col", "num", "den"}
    if not rows.fieldnames or not required.issubset(rows.fieldnames):
        return {}, {}, ["gram_payload_header_mismatch"]
    gram = defaultdict(dict)
    equality = defaultdict(list)
    errors: list[str] = []
    for line_no, row in enumerate(rows, start=2):
        try:
            kind = row["kind"]
            key = (row["clique"], row["constraint"], row["block"])
            denominator = int(row["den"])
            numerator = int(row["num"])
            if denominator <= 0:
                errors.append(f"gram_nonpositive_denominator:{line_no}")
            if kind == "gram":
                gram[key][(int(row["row"]) - 1, int(row["col"]) - 1)] = Fraction(
                    numerator, denominator)
            elif kind == "eq_multiplier":
                equality[key].append((int(row["row"]), int(row["col"]),
                                      Fraction(numerator, denominator)))
            else:
                errors.append(f"gram_unknown_kind:{line_no}")
        except (KeyError, TypeError, ValueError, ZeroDivisionError):
            errors.append(f"gram_malformed_row:{line_no}")
    return dict(gram), dict(equality), errors


def _basis_groups(text: str):
    rows = csv.DictReader(io.StringIO(text))
    required = {"kind", "clique", "constraint", "block", "block_row",
                "basis_index", "exponents"}
    if not rows.fieldnames or not required.issubset(rows.fieldnames):
        return {}, ["gram_basis_header_mismatch"]
    groups = defaultdict(list)
    errors: list[str] = []
    for line_no, row in enumerate(rows, start=2):
        try:
            key = (row["clique"], row["constraint"], row["block"])
            exponents = tuple(int(item) for item in row["exponents"].split(";")
                              if item != "")
            if any(power < 0 for power in exponents):
                errors.append(f"gram_basis_negative_exponent:{line_no}")
            groups[(row["kind"], *key)].append(
                (int(row["block_row"]), int(row["basis_index"]), exponents))
        except (KeyError, TypeError, ValueError):
            errors.append(f"gram_basis_malformed_row:{line_no}")
    return dict(groups), errors


def _positive_exact_gram(entries):
    n = max(max(index) for index in entries) + 1
    if len(entries) != n * n:
        return n, None, "gram_matrix_not_dense"
    matrix = [[entries[(i, j)] for j in range(n)] for i in range(n)]
    if any(matrix[i][j] != matrix[j][i]
           for i in range(n) for j in range(n)):
        return n, None, "gram_matrix_not_symmetric"
    lower = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    pivots: list[Fraction] = []
    for i in range(n):
        lower[i][i] = Fraction(1)
        pivot = matrix[i][i] - sum(
            lower[i][k] * lower[i][k] * pivots[k] for k in range(i)
        )
        if pivot <= 0:
            return n, pivot, "gram_matrix_not_positive_definite"
        pivots.append(pivot)
        for j in range(i + 1, n):
            lower[j][i] = (
                matrix[j][i] - sum(
                    lower[j][k] * lower[i][k] * pivots[k] for k in range(i)
                )
            ) / pivot
    return n, min(pivots), None


def audit_routeb_physical_rational_gram(
    audit_csv_text: str,
    gram_csv_text: str,
    basis_csv_text: str,
    *,
    artifact_sha256: str | None = None,
    source_sha256: str | None = None,
) -> RouteBPhysicalRationalGramAudit:
    """Independently check rational Gram shape, symmetry and exact PD blocks."""
    audit = _read_metric_csv(audit_csv_text)
    errors = [
        f"gram_audit_mismatch:{key}"
        for key, expected in EXPECTED_GRAM_AUDIT.items()
        if audit.get(key) != expected
    ]
    gram, equality, gram_errors = _exact_gram_groups(gram_csv_text)
    basis, basis_errors = _basis_groups(basis_csv_text)
    errors.extend(gram_errors)
    errors.extend(basis_errors)
    min_pivot: Fraction | None = None
    dimensions: list[int] = []
    for key, entries in gram.items():
        dimension, pivot, error = _positive_exact_gram(entries)
        dimensions.append(dimension)
        if pivot is not None and (min_pivot is None or pivot < min_pivot):
            min_pivot = pivot
        if error:
            errors.append(f"{error}:{key}")
        basis_key = ("gram", *key)
        records = basis.get(basis_key, [])
        if len(records) != dimension:
            errors.append(f"gram_basis_dimension_mismatch:{key}")
        else:
            rows = sorted(record[0] for record in records)
            indices = [record[1] for record in records]
            if rows != list(range(1, dimension + 1)):
                errors.append(f"gram_basis_row_mismatch:{key}")
            if len(set(indices)) != dimension or any(index < 1 for index in indices):
                errors.append(f"gram_basis_index_mismatch:{key}")
    if len(gram) != 14:
        errors.append("gram_block_count_mismatch")
    if max(dimensions, default=0) != 83:
        errors.append("gram_max_dimension_mismatch")
    if set(equality) != {("1", "1", "0"), ("1", "2", "0"), ("1", "3", "0")}:
        errors.append("equality_multiplier_group_mismatch")
    status = "EXACT_RATIONAL_GRAM_CANDIDATE" if not errors else "OPEN_FAIL_CLOSED"
    return RouteBPhysicalRationalGramAudit(
        status=status,
        artifact_sha256=artifact_sha256,
        source_sha256=source_sha256,
        gram_blocks=len(gram),
        max_gram_dimension=max(dimensions, default=0),
        min_ldl_pivot=min_pivot,
        errors=tuple(errors),
    )


__all__ = [
    "EXPECTED_AUDIT",
    "EXPECTED_INTERFACE",
    "EXPECTED_BRIDGE",
    "EXPECTED_TAIL_META",
    "EXPECTED_GRAM_AUDIT",
    "RouteBNominalDistalBridgeAudit",
    "RouteBPhysicalRationalTailAudit",
    "RouteBPhysicalRationalGramAudit",
    "audit_routeb_nominal_distal_bridge",
    "audit_routeb_physical_rational_tail",
    "audit_routeb_physical_rational_gram",
]
