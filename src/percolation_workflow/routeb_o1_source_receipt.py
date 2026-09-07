"""Fail-closed intake for the O1 exact typed source export contract."""
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from fractions import Fraction
from typing import Any


O1_SOURCE_RECEIPT_SCHEMA = "routeb.o1.true_dh_exact_typed_mdd_source.v2"
O1_BLOCK_ORDER = (1, 2, 3, 6)
O1_DIDX = (0, 1, 2, 5)
O1_BIDX = (3, 4)


@dataclass(frozen=True)
class RouteBO1SourceReceiptAudit:
    status: str
    source_key: str | None = None
    state_key: str | None = None
    mu_exact: Fraction | None = None
    source_binding_proven: bool = False
    source_binding_path: str | None = None
    missing: tuple[str, ...] = ()
    errors: tuple[str, ...] = ()
    comparator_status: str = "pending"
    formal_certificate_allowed: bool = False
    registry_eligible: bool = False


def _exact(value: Any, field: str) -> Fraction:
    if isinstance(value, bool) or isinstance(value, float):
        raise TypeError(f"{field}: exact integer/rational value required")
    try:
        return Fraction(value)
    except (TypeError, ValueError, ZeroDivisionError) as exc:
        raise TypeError(f"{field}: malformed exact rational") from exc


def _hash(value: Any, field: str) -> None:
    if (not isinstance(value, str) or len(value) != 64
            or any(c not in "0123456789abcdefABCDEF" for c in value)):
        raise ValueError(f"{field}: sha256 hex string required")


def _nonempty_string(value: Any, field: str, missing: list[str], errors: list[str]) -> None:
    if value is None:
        missing.append(field)
    elif not isinstance(value, str) or not value.strip():
        errors.append(f"{field}_must_be_nonempty_string")


def audit_routeb_o1_source_receipt(
    receipt: Mapping[str, Any] | None,
) -> RouteBO1SourceReceiptAudit:
    """Validate the O1 typed export shape without granting theorem admission.

    A source-binding theorem and a generated Lean file are necessary but not
    sufficient for ``VERIFIED``: pinned compilation, comparator, axiom and
    project-level gates remain separate downstream checks.
    """
    if not isinstance(receipt, Mapping):
        return RouteBO1SourceReceiptAudit(status="REJECTED", errors=("receipt_must_be_mapping",))
    missing: list[str] = []
    errors: list[str] = []
    if receipt.get("schema") != O1_SOURCE_RECEIPT_SCHEMA:
        errors.append("schema_mismatch")
    source_key = receipt.get("source_key") if isinstance(receipt.get("source_key"), str) else None
    state_key = receipt.get("state_key") if isinstance(receipt.get("state_key"), str) else None
    _nonempty_string(receipt.get("source_key"), "source_key", missing, errors)
    _nonempty_string(receipt.get("state_key"), "state_key", missing, errors)
    if receipt.get("mu_exact") is None:
        missing.append("mu_exact")
        mu = None
    else:
        try:
            mu = _exact(receipt.get("mu_exact"), "mu_exact")
        except TypeError as exc:
            errors.append(str(exc)); mu = None
        if mu is not None and mu != Fraction(1, 1_000_000):
            errors.append("mu_exact_mismatch")
    required_strings = (
        "matrix_type", "evaluator_definition", "regularization",
        "projection_type", "projection_term", "binding_theorem",
        "lean_file_hash", "coefficient_payload_hash", "deployed_source_hash",
    )
    for field in required_strings:
        if field not in receipt:
            missing.append(field)
        elif field.endswith("_hash"):
            try:
                _hash(receipt.get(field), field)
            except ValueError as exc:
                errors.append(str(exc))
        else:
            _nonempty_string(receipt.get(field), field, missing, errors)
    if receipt.get("matrix_type") != "Matrix (Fin 6) (Fin 6) ℝ":
        errors.append("matrix_type_mismatch")
    if receipt.get("projection_type") != "Matrix (Fin 4) (Fin 4) ℝ":
        errors.append("projection_type_mismatch")
    if not isinstance(receipt.get("projection_term"), str) or "M_DD45_at" not in receipt.get("projection_term", ""):
        errors.append("projection_term_mismatch")
    if receipt.get("binding_theorem") != "h_MDD_def":
        errors.append("binding_theorem_mismatch")
    if receipt.get("regularization") != "M_authoritative = M_fourier + mu * I":
        errors.append("regularization_mismatch")
    for field, expected in (
        ("block_order_one_based", list(O1_BLOCK_ORDER)),
        ("didx_zero_based", list(O1_DIDX)),
        ("bidx_zero_based", list(O1_BIDX)),
    ):
        if field not in receipt:
            missing.append(field)
        elif receipt.get(field) != expected:
            errors.append(f"{field}_mismatch")
    q_domain = receipt.get("q_domain")
    if q_domain is None:
        missing.append("q_domain")
    elif not isinstance(q_domain, (str, Mapping)):
        errors.append("q_domain_must_be_exact_point_cell_or_mapping")
    source_path = receipt.get("source_binding_theorem")
    if source_path is None:
        missing.append("source_binding_theorem")
    elif source_path not in ("h_source_mass", "h_aggregate_and_h_body", "h_aggregate,h_body"):
        errors.append("source_binding_theorem_path_mismatch")
    source_proven = receipt.get("source_binding_proven") is True
    if errors:
        return RouteBO1SourceReceiptAudit(
            status="REJECTED", source_key=source_key, state_key=state_key,
            mu_exact=mu, source_binding_proven=source_proven,
            source_binding_path=source_path if isinstance(source_path, str) else None,
            missing=tuple(dict.fromkeys(missing)), errors=tuple(dict.fromkeys(errors)),
        )
    if missing:
        return RouteBO1SourceReceiptAudit(
            status="PENDING_REQUIRED_FIELDS", source_key=source_key, state_key=state_key,
            mu_exact=mu, source_binding_proven=source_proven,
            source_binding_path=source_path, missing=tuple(dict.fromkeys(missing)),
        )
    if not source_proven:
        return RouteBO1SourceReceiptAudit(
            status="CONDITIONAL_TYPED_SOURCE_EXPORT", source_key=source_key,
            state_key=state_key, mu_exact=mu, source_binding_path=source_path,
            errors=("source_binding_theorem_not_proven",),
        )
    return RouteBO1SourceReceiptAudit(
        status="READY_FOR_TYPED_SOURCE_INTAKE", source_key=source_key,
        state_key=state_key, mu_exact=mu, source_binding_proven=True,
        source_binding_path=source_path, comparator_status="pending",
    )


__all__ = [
    "O1_SOURCE_RECEIPT_SCHEMA", "O1_BLOCK_ORDER", "O1_DIDX", "O1_BIDX",
    "RouteBO1SourceReceiptAudit", "audit_routeb_o1_source_receipt",
]
