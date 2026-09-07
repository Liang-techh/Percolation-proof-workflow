"""Fail-closed receipt contract for the Route-B residual ``l1`` Lean seam.

The generic theorem in ``examples/routeb_gram_residual_lean`` is useful only
after a remote Lean run binds it to the concrete coefficient residual produced
by the exact Gram reconstruction.  This module validates that narrow handoff
without running Lean and without promoting anything to the verified registry.

The contract intentionally has three outcomes:

* ``pending`` when coordinator-owned pins or bindings are absent;
* ``rejected`` when a supplied value is malformed, inconsistent, or failed;
* ``accepted`` only when the receipt is complete and agrees with every
  authoritative binding supplied by the coordinator.

An accepted receipt is still a compiled candidate.  The parent Route-B theorem
must separately discharge true-DH semantics, coverage, flowpipe, terminal
transfer, comparator, and global CI gates.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import re
from typing import Any, Mapping


RESIDUAL_L1_LEAN_RECEIPT_SCHEMA = "routeb.residual_l1_lean_receipt.v1"
EXPECTED_THEOREMS = (
    "RouteBGramResidual.weighted_residual_l1_bound",
    "RouteBGramResidual.decomposition_nonnegative_of_abs_residual",
)
_SHA256 = re.compile(r"^[0-9a-fA-F]{64}$")
_NONEMPTY = re.compile(r".*\S.*")


@dataclass(frozen=True)
class RouteBResidualL1LeanReceiptAudit:
    """Pure audit result for one remote residual-seam receipt."""

    status: str
    source_sha256: str | None
    coefficient_artifact_sha256: str | None
    theorem_names: tuple[str, ...]
    axioms: dict[str, tuple[str, ...]]
    errors: tuple[str, ...] = ()
    pending: tuple[str, ...] = ()
    formal_certificate_allowed: bool = False
    registry_eligible: bool = False


def _sha(value: Any) -> bool:
    return isinstance(value, str) and bool(_SHA256.fullmatch(value))


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(_NONEMPTY.fullmatch(value))


def _fraction(value: Any) -> Fraction | None:
    if not isinstance(value, str):
        return None
    try:
        result = Fraction(value)
    except (TypeError, ValueError, ZeroDivisionError):
        return None
    return result


def _string_list(value: Any, field: str, errors: list[str]) -> tuple[str, ...] | None:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        errors.append(f"{field}_malformed")
        return None
    if len(value) != len(set(value)):
        errors.append(f"{field}_contains_duplicates")
    return tuple(value)


def _axioms(value: Any, errors: list[str]) -> dict[str, tuple[str, ...]] | None:
    if not isinstance(value, dict) or not value:
        errors.append("axioms_malformed")
        return None
    result: dict[str, tuple[str, ...]] = {}
    for theorem, names in value.items():
        if not isinstance(theorem, str) or not _text(theorem):
            errors.append("axioms_theorem_name_malformed")
            continue
        parsed = _string_list(names, f"axioms:{theorem}", errors)
        if parsed is not None:
            result[theorem] = parsed
    return result


def audit_routeb_residual_l1_lean_receipt(
    receipt: Mapping[str, Any],
    *,
    expected_source_sha256: str | None = None,
    expected_coefficient_artifact_sha256: str | None = None,
    expected_theorem_names: tuple[str, ...] = EXPECTED_THEOREMS,
    expected_lean_toolchain: str | None = None,
    expected_mathlib_commit: str | None = None,
    candidate_receipt: Mapping[str, Any] | None = None,
    allowed_axioms: tuple[str, ...] = ("propext", "Quot.sound", "Classical.choice"),
) -> RouteBResidualL1LeanReceiptAudit:
    """Audit a remote T-P4-018 receipt without performing any side effect.

    The expected hashes and pins are coordinator-owned.  Omitting them keeps
    the result ``pending`` even when the remote receipt is internally complete;
    this prevents an agent from self-authenticating its own source snapshot.
    """
    if not isinstance(receipt, Mapping):
        return RouteBResidualL1LeanReceiptAudit(
            "REJECTED", None, None, (), {}, errors=("receipt_not_mapping",))

    errors: list[str] = []
    pending: list[str] = []
    schema = receipt.get("schema")
    if schema is None:
        pending.append("missing_schema")
    elif schema != RESIDUAL_L1_LEAN_RECEIPT_SCHEMA:
        errors.append("unsupported_schema")

    run_status = receipt.get("compile_status")
    if run_status is None:
        pending.append("missing_compile_status")
    elif run_status != "passed":
        errors.append("compile_status_not_passed")
    exit_code = receipt.get("exit_code")
    if exit_code is None:
        pending.append("missing_exit_code")
    elif type(exit_code) is not int or exit_code != 0:
        errors.append("exit_code_not_zero")
    command = receipt.get("compile_command")
    if command is None:
        pending.append("missing_compile_command")
    elif (not isinstance(command, list) or not command or
          any(not isinstance(part, str) or not _text(part) for part in command)):
        errors.append("compile_command_malformed")

    source = receipt.get("source_sha256")
    coefficient = receipt.get("coefficient_artifact_sha256")
    for field, value in (("source_sha256", source),
                         ("coefficient_artifact_sha256", coefficient)):
        if value is None:
            pending.append(f"missing_{field}")
        elif not _sha(value):
            errors.append(f"{field}_malformed")
    if source is not None and _sha(source):
        if expected_source_sha256 is None:
            pending.append("source_sha256_not_authoritatively_bound")
        elif source.lower() != expected_source_sha256.lower():
            errors.append("source_sha256_mismatch")
    if coefficient is not None and _sha(coefficient):
        if expected_coefficient_artifact_sha256 is None:
            pending.append("coefficient_artifact_sha256_not_authoritatively_bound")
        elif coefficient.lower() != expected_coefficient_artifact_sha256.lower():
            errors.append("coefficient_artifact_sha256_mismatch")

    theorem_names: tuple[str, ...] = ()
    if "theorem_names" not in receipt:
        pending.append("missing_theorem_names")
    else:
        parsed_names = _string_list(receipt.get("theorem_names"), "theorem_names", errors)
        if parsed_names is not None:
            theorem_names = parsed_names
            if parsed_names != tuple(expected_theorem_names):
                errors.append("theorem_names_mismatch")

    parsed_axioms: dict[str, tuple[str, ...]] = {}
    if "axioms" not in receipt:
        pending.append("missing_axioms")
    else:
        parsed = _axioms(receipt.get("axioms"), errors)
        if parsed is not None:
            parsed_axioms = parsed
            if set(parsed) != set(expected_theorem_names):
                errors.append("axiom_theorem_set_mismatch")
            for theorem, names in parsed.items():
                unexpected = sorted(set(names) - set(allowed_axioms))
                if unexpected:
                    errors.append(
                        f"unexpected_axioms:{theorem}:{','.join(unexpected)}")

    for field in ("sorry_free", "admit_free"):
        value = receipt.get(field)
        if value is None:
            pending.append(f"missing_{field}")
        elif value is not True:
            errors.append(f"{field}_not_true")
    forbidden = receipt.get("forbidden_tokens")
    if forbidden is None:
        pending.append("missing_forbidden_tokens_report")
    elif not isinstance(forbidden, list) or any(not isinstance(item, str) for item in forbidden):
        errors.append("forbidden_tokens_report_malformed")
    elif forbidden:
        errors.append("forbidden_tokens_present")

    for field, expected in (("lean_toolchain", expected_lean_toolchain),
                            ("mathlib_commit", expected_mathlib_commit)):
        value = receipt.get(field)
        if value is None:
            pending.append(f"missing_{field}")
        elif not _text(value):
            errors.append(f"{field}_malformed")
        elif expected is None:
            pending.append(f"{field}_not_authoritatively_bound")
        elif value != expected:
            errors.append(f"{field}_mismatch")

    for field in ("coefficient_term_count", "residual_l1", "rational_lower_bound",
                  "scaled_margin", "residual_coefficients_sha256"):
        value = receipt.get(field)
        if value is None:
            pending.append(f"missing_{field}")
            continue
        if field == "coefficient_term_count":
            if type(value) is not int or value <= 0:
                errors.append("coefficient_term_count_malformed")
        elif field == "residual_coefficients_sha256":
            if not _sha(value):
                errors.append("residual_coefficients_sha256_malformed")
        else:
            parsed = _fraction(value)
            if parsed is None:
                errors.append(f"{field}_malformed")
            elif field == "scaled_margin" and parsed <= 0:
                errors.append("scaled_margin_not_positive")

    if candidate_receipt is None:
        pending.append("missing_candidate_reconstruction_receipt")
    elif not isinstance(candidate_receipt, Mapping):
        errors.append("candidate_reconstruction_receipt_malformed")
    else:
        if candidate_receipt.get("status") != "EXACT_RATIONAL_GRAM_RECONSTRUCTION_CANDIDATE":
            errors.append("candidate_reconstruction_not_pass")
        if coefficient is not None and candidate_receipt.get("artifact_sha256") != coefficient:
            errors.append("candidate_artifact_sha256_mismatch")
        for field in ("coefficient_term_count", "residual_l1", "rational_lower_bound",
                      "scaled_margin", "residual_coefficients_sha256"):
            candidate_field = {
                "coefficient_term_count": "residual_term_count",
                "scaled_margin": "certified_scaled_margin",
            }.get(field, field)
            if field in receipt and candidate_field in candidate_receipt:
                if receipt[field] != candidate_receipt[candidate_field]:
                    errors.append(f"candidate_{field}_mismatch")

    status = "REJECTED" if errors else ("PENDING" if pending else "ACCEPTED")
    return RouteBResidualL1LeanReceiptAudit(
        status=status,
        source_sha256=source if _sha(source) else None,
        coefficient_artifact_sha256=coefficient if _sha(coefficient) else None,
        theorem_names=theorem_names,
        axioms=parsed_axioms,
        errors=tuple(dict.fromkeys(errors)),
        pending=tuple(dict.fromkeys(pending)),
    )


__all__ = [
    "EXPECTED_THEOREMS",
    "RESIDUAL_L1_LEAN_RECEIPT_SCHEMA",
    "RouteBResidualL1LeanReceiptAudit",
    "audit_routeb_residual_l1_lean_receipt",
]
