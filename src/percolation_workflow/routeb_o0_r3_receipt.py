"""Fail-closed validator for a future physical O0-R3 receipt.

The validator describes the minimum same-key interface identified by the
T-P4-033 review.  It checks exact scalar arithmetic and receipt shape only;
it does not create a physical theorem, prove a source binding, or promote a
registry entry.
"""
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from fractions import Fraction
from typing import Any


O0_R3_RECEIPT_SCHEMA = "routeb.o0_r3.same_key_physical_receipt.v1"
O0_R3_CANONICAL_RECEIPT_SCHEMA = "routeb.o0.canonical_source_metric_schur_receipt.v1"


@dataclass(frozen=True)
class RouteBO0R3ReceiptAudit:
    status: str
    source_key: str | None
    rho_baseline: Fraction | None
    epsilon_port: Fraction | None
    theta: Fraction | None
    remaining_schur_margin: Fraction | None
    added_young_charge: Fraction | None
    leftover_margin: Fraction | None
    errors: tuple[str, ...] = ()
    formal_certificate_allowed: bool = False
    registry_eligible: bool = False


@dataclass(frozen=True)
class RouteBO0R3CanonicalReceiptAudit:
    """Audit result for the nested, content/state-bound O0 receipt contract."""

    status: str
    receipt_id: str | None = None
    source_key: str | None = None
    state_key: str | None = None
    rho_baseline: Fraction | None = None
    epsilon_port: Fraction | None = None
    theta: Fraction | None = None
    remaining_schur_margin: Fraction | None = None
    added_young_charge: Fraction | None = None
    leftover_margin: Fraction | None = None
    missing: tuple[str, ...] = ()
    errors: tuple[str, ...] = ()
    formal_certificate_allowed: bool = False
    registry_eligible: bool = False


def _fraction(value: Any, name: str) -> Fraction:
    if isinstance(value, bool) or isinstance(value, float):
        raise TypeError(f"{name}: exact integer/rational value required")
    if isinstance(value, (int, Fraction)):
        return Fraction(value)
    if isinstance(value, str):
        try:
            return Fraction(value.strip())
        except (ValueError, ZeroDivisionError) as error:
            raise TypeError(f"{name}: malformed exact rational") from error
    raise TypeError(f"{name}: exact integer/rational value required")


def audit_routeb_o0_r3_receipt(receipt: Mapping[str, Any] | None) -> RouteBO0R3ReceiptAudit:
    """Validate a strict same-key O0-R3 physical budget receipt.

    Required proof flags are deliberately boolean and must be explicitly
    ``True``.  Numeric values may be integers, ``Fraction`` instances, or
    rational strings, but never binary floats.  A successful result is still
    only a conditional coordinator input.
    """
    if not isinstance(receipt, Mapping):
        return RouteBO0R3ReceiptAudit(
            status="REJECTED",
            source_key=None,
            rho_baseline=None,
            epsilon_port=None,
            theta=None,
            remaining_schur_margin=None,
            added_young_charge=None,
            leftover_margin=None,
            errors=("receipt_must_be_mapping",),
        )
    required = (
        "source_key", "metric_source_key", "margin_source_key",
        "rho_baseline", "epsilon_port", "theta", "remaining_schur_margin",
        "baseline_bound_proven", "perturbation_bound_proven",
        "metric_lower_bound_proven", "semantic_binding_proven",
        "port_binding_proven", "coverage_complete", "source_artifact_hashes",
    )
    missing = tuple(name for name in required if name not in receipt)
    source_key = receipt.get("source_key")
    source_key = source_key if isinstance(source_key, str) and source_key else None
    if missing:
        return RouteBO0R3ReceiptAudit(
            status="PENDING_REQUIRED_FIELDS",
            source_key=source_key,
            rho_baseline=None,
            epsilon_port=None,
            theta=None,
            remaining_schur_margin=None,
            added_young_charge=None,
            leftover_margin=None,
            errors=tuple(f"missing:{name}" for name in missing),
        )
    errors: list[str] = []
    for name in ("metric_source_key", "margin_source_key"):
        value = receipt.get(name)
        if not isinstance(value, str) or not value:
            errors.append(f"{name}_missing")
        elif source_key is None or value != source_key:
            errors.append(f"{name}_mismatch")
    values: dict[str, Fraction | None] = {}
    for name in ("rho_baseline", "epsilon_port", "theta", "remaining_schur_margin"):
        try:
            values[name] = _fraction(receipt.get(name), name)
        except TypeError as error:
            errors.append(str(error))
            values[name] = None
    for name in ("rho_baseline", "epsilon_port", "remaining_schur_margin"):
        value = values[name]
        if value is not None and value < 0:
            errors.append(f"{name}_negative")
    if values["theta"] is not None and values["theta"] <= 0:
        errors.append("theta_not_positive")
    flag_names = (
        "baseline_bound_proven", "perturbation_bound_proven",
        "metric_lower_bound_proven", "semantic_binding_proven",
        "port_binding_proven", "coverage_complete",
    )
    for name in flag_names:
        if receipt.get(name) is not True:
            errors.append(f"{name}_not_proven")
    hashes = receipt.get("source_artifact_hashes")
    if not isinstance(hashes, Mapping) or not hashes:
        errors.append("source_artifact_hashes_missing")
    if errors:
        malformed_or_inconsistent = any(
            "mismatch" in error
            or "malformed" in error
            or "negative" in error
            or "exact integer/rational value required" in error
            or "malformed exact rational" in error
            for error in errors
        )
        return RouteBO0R3ReceiptAudit(
            status="REJECTED" if malformed_or_inconsistent
            else "PENDING_PROOF_FIELDS",
            source_key=source_key,
            rho_baseline=values["rho_baseline"],
            epsilon_port=values["epsilon_port"],
            theta=values["theta"],
            remaining_schur_margin=values["remaining_schur_margin"],
            added_young_charge=None,
            leftover_margin=None,
            errors=tuple(dict.fromkeys(errors)),
        )
    rho = values["rho_baseline"]
    epsilon = values["epsilon_port"]
    theta = values["theta"]
    margin = values["remaining_schur_margin"]
    assert rho is not None and epsilon is not None and theta is not None and margin is not None
    rho_rounded = rho + epsilon
    charge = (1 + 1 / theta) * (rho_rounded * rho_rounded - rho * rho)
    leftover = margin - charge
    if leftover <= 0:
        return RouteBO0R3ReceiptAudit(
            status="REJECTED",
            source_key=source_key,
            rho_baseline=rho,
            epsilon_port=epsilon,
            theta=theta,
            remaining_schur_margin=margin,
            added_young_charge=charge,
            leftover_margin=leftover,
            errors=("strict_remaining_schur_margin_not_positive",),
        )
    return RouteBO0R3ReceiptAudit(
        status="READY_FOR_COORDINATOR_ADMISSION",
        source_key=source_key,
        rho_baseline=rho,
        epsilon_port=epsilon,
        theta=theta,
        remaining_schur_margin=margin,
        added_young_charge=charge,
        leftover_margin=leftover,
    )


def audit_routeb_o0_r3_canonical_receipt(
    receipt: Mapping[str, Any] | None,
) -> RouteBO0R3CanonicalReceiptAudit:
    """Audit the nested canonical O0-R3 receipt from T-P4-033.

    This is an intake pre-check only.  It never proves the physical identity,
    validates Lean, or promotes a theorem.  Missing theorem receipts are
    pending; malformed or cross-key data is rejected.
    """
    if not isinstance(receipt, Mapping):
        return RouteBO0R3CanonicalReceiptAudit(
            status="REJECTED", errors=("receipt_must_be_mapping",)
        )
    receipt_id = receipt.get("receipt_id") if isinstance(receipt.get("receipt_id"), str) else None
    source_key = receipt.get("source_key") if isinstance(receipt.get("source_key"), str) else None
    state_key = receipt.get("state_key") if isinstance(receipt.get("state_key"), str) else None
    missing: list[str] = []
    errors: list[str] = []
    required = (
        "schema", "status", "receipt_id", "source_key", "state_key", "domain",
        "semantics", "metric", "inverse", "weighted_baseline",
        "weighted_perturbation", "schur_baseline", "physical_binding", "admission",
    )
    for name in required:
        if name not in receipt:
            missing.append(name)
    if receipt.get("schema") != O0_R3_CANONICAL_RECEIPT_SCHEMA:
        errors.append("schema_mismatch") if "schema" in receipt else None
    if receipt.get("status") not in (None, "PENDING"):
        errors.append("receipt_status_must_remain_pending")
    for name, value in (("receipt_id", receipt_id), ("source_key", source_key), ("state_key", state_key)):
        if name in receipt and (value is None or not value):
            missing.append(name)

    sections: dict[str, Mapping[str, Any]] = {}
    for section in required[5:]:
        value = receipt.get(section)
        if not isinstance(value, Mapping):
            if section in receipt:
                errors.append(f"{section}_must_be_mapping")
        else:
            sections[section] = value

    def exact(section: str, name: str, *, allow_null: bool = False) -> Fraction | None:
        label = f"{section}.{name}"
        if section not in sections or name not in sections[section]:
            missing.append(label)
            return None
        value = sections[section].get(name)
        if allow_null and value is None:
            missing.append(label)
            return None
        try:
            return _fraction(value, label)
        except TypeError as error:
            errors.append(str(error))
            return None

    domain = sections.get("domain")
    if domain is not None:
        for name in ("cell_id", "coverage"):
            if not isinstance(domain.get(name), str) or not domain.get(name):
                missing.append(f"domain.{name}")
        if domain.get("axis_order") != ["q1", "q2", "q3", "q4", "q5", "q6"]:
            errors.append("domain.axis_order_mismatch")
        for name in ("q_lo", "q_hi"):
            values = domain.get(name)
            if not isinstance(values, (list, tuple)) or len(values) != 6:
                errors.append(f"domain.{name}_must_have_six_exact_coordinates")
            else:
                for index, value in enumerate(values):
                    try:
                        _fraction(value, f"domain.{name}[{index}]")
                    except TypeError as error:
                        errors.append(str(error))

    semantics = sections.get("semantics")
    if semantics is not None:
        if semantics.get("exact_real_mu") != "1/1000000":
            errors.append("semantics.exact_real_mu_mismatch")
        if semantics.get("deployed_mu_literal") != "1e-6":
            errors.append("semantics.deployed_mu_literal_mismatch")
        for name in ("force_scale", "coefficient_version", "rounding_or_interval_mode"):
            if not isinstance(semantics.get(name), str) or not semantics.get(name):
                missing.append(f"semantics.{name}")

    metric = sections.get("metric")
    if metric is not None:
        for name, expected in (
            ("orientation", "left_output"), ("norm", "induced_2"),
            ("B_up_identity", "B_up = S^T S"),
        ):
            if metric.get(name) != expected:
                errors.append(f"metric.{name}_mismatch")

    inverse = sections.get("inverse")
    if inverse is not None:
        for name in ("matrix", "proof_receipt"):
            if not isinstance(inverse.get(name), str) or not inverse.get(name):
                missing.append(f"inverse.{name}")
        if inverse.get("norm") not in ("induced_2", "induced_infinity"):
            errors.append("inverse.norm_mismatch")

    baseline = sections.get("weighted_baseline")
    perturbation = sections.get("weighted_perturbation")
    schur = sections.get("schur_baseline")
    physical = sections.get("physical_binding")
    for section, names in (
        (baseline, ("map", "statement", "proof_receipt")),
        (perturbation, ("map", "statement", "proof_receipt")),
        (schur, ("lambda", "proof_receipt")),
    ):
        if section is not None:
            for name in names:
                if not isinstance(section.get(name), str) or not section.get(name):
                    missing.append(name)
    if schur is not None and schur.get("same_normalization_as_metric") is not True:
        errors.append("schur_baseline.normalization_mismatch")
    if physical is not None:
        if physical.get("statement") != "R_port a_B = r_B":
            errors.append("physical_binding.statement_mismatch")
        if not isinstance(physical.get("proof_receipt"), str) or not physical.get("proof_receipt"):
            missing.append("physical_binding.proof_receipt")

    rho = exact("weighted_baseline", "rho_r")
    epsilon = exact("weighted_perturbation", "epsilon_R")
    theta = exact("schur_baseline", "theta")
    margin = exact("schur_baseline", "remaining_margin_m_r")
    exact("metric", "beta")
    exact("metric", "s")
    exact("inverse", "K")
    epsilon_a = exact("inverse", "epsilon_A", allow_null=True)
    lambda_value: Fraction | None = None
    if schur is None or "lambda" not in schur:
        missing.append("schur_baseline.lambda")
    else:
        raw_lambda = schur.get("lambda")
        if not isinstance(raw_lambda, str):
            errors.append("schur_baseline.lambda: exact integer/rational value required")
        elif raw_lambda.strip().replace(" ", "") == "1+1/theta":
            if theta is not None and theta > 0:
                lambda_value = 1 + 1 / theta
        else:
            try:
                lambda_value = _fraction(raw_lambda, "schur_baseline.lambda")
            except TypeError as error:
                errors.append(str(error))
    if any(value is not None and value < 0 for value in (rho, epsilon, theta, margin, epsilon_a)):
        errors.append("canonical_exact_value_negative")
    if theta is not None and theta <= 0:
        errors.append("schur_baseline.theta_not_positive")
    if theta is not None and lambda_value is not None and lambda_value != 1 + 1 / theta:
        errors.append("schur_baseline.lambda_mismatch")

    proof_flags = (
        ("metric", "s_positive"), ("metric", "s_sq_le_beta"),
        ("metric", "B_up_ge_beta_I_proved"), ("inverse", "proves_exact_real_bound"),
        ("inverse", "epsilon_A_times_K_lt_one"),
        ("weighted_baseline", "rho_r_nonnegative"),
        ("schur_baseline", "m_r_positive"),
    )
    for section, name in proof_flags:
        if section not in sections or sections[section].get(name) is not True:
            missing.append(f"{section}.{name}")
    admission = sections.get("admission")
    if admission is not None:
        if admission.get("all_source_keys_equal") is not True:
            errors.append("admission.source_keys_not_equal")
        if admission.get("all_state_keys_equal") is not True:
            errors.append("admission.state_keys_not_equal")
        if admission.get("registry_promoted") is True:
            errors.append("registry_boundary_violation")
        if admission.get("formal_certificate_allowed") is True:
            errors.append("formal_gate_boundary_violation")

    if errors:
        return RouteBO0R3CanonicalReceiptAudit(
            status="REJECTED", receipt_id=receipt_id, source_key=source_key,
            state_key=state_key, missing=tuple(dict.fromkeys(missing)),
            errors=tuple(dict.fromkeys(errors)),
        )
    if missing or rho is None or epsilon is None or theta is None or lambda_value is None or margin is None:
        return RouteBO0R3CanonicalReceiptAudit(
            status="PENDING_REQUIRED_FIELDS", receipt_id=receipt_id,
            source_key=source_key, state_key=state_key,
            missing=tuple(dict.fromkeys(missing)),
        )
    charge = (1 + 1 / theta) * ((rho + epsilon) ** 2 - rho ** 2)
    leftover = margin - charge
    if leftover <= 0:
        return RouteBO0R3CanonicalReceiptAudit(
            status="REJECTED", receipt_id=receipt_id, source_key=source_key,
            state_key=state_key, rho_baseline=rho, epsilon_port=epsilon,
            theta=theta, remaining_schur_margin=margin,
            added_young_charge=charge, leftover_margin=leftover,
            errors=("strict_remaining_schur_margin_not_positive",),
        )
    return RouteBO0R3CanonicalReceiptAudit(
        status="READY_FOR_COORDINATOR_ADMISSION", receipt_id=receipt_id,
        source_key=source_key, state_key=state_key, rho_baseline=rho,
        epsilon_port=epsilon, theta=theta, remaining_schur_margin=margin,
        added_young_charge=charge, leftover_margin=leftover,
    )


__all__ = [
    "O0_R3_RECEIPT_SCHEMA",
    "O0_R3_CANONICAL_RECEIPT_SCHEMA",
    "RouteBO0R3ReceiptAudit",
    "RouteBO0R3CanonicalReceiptAudit",
    "audit_routeb_o0_r3_receipt",
    "audit_routeb_o0_r3_canonical_receipt",
]
