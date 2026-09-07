"""Fail-closed source contract for the deployed Route-B P4 force seam.

This module does not prove the dynamics.  It checks a small, high-value
semantic boundary before any Lean sidecar or numerical receipt consumes it:

* the canonical PMI source uses ``kc = 0.05 = 1/20`` in force coordinates;
* the deployed DH port has no matching ``kc`` torque term and solves
  ``M(q) a = tau - C dq - G``;
* the omitted PMI term is therefore ``(q5/20, q4/20)`` at force scale;
* the block split still requires an explicit ``M_BD(q) a_D`` binding.

An old adapter with a different scale is reported as stale, never silently
rewritten.  Passing this structural contract is evidence about source text,
not a theorem, source-equivalence proof, or registry admission.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import re


@dataclass(frozen=True)
class RouteBP4SourceContract:
    status: str
    kc: Fraction | None
    expected_rho_kc: tuple[str, str]
    observed_adapter_rho_kc: tuple[str, str] | None
    remote_term_required: str
    force_acceleration_separated: bool
    errors: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
    formal_certificate_allowed: bool = False
    registry_eligible: bool = False


_KC = re.compile(r"(?m)^\s*kc\s*=\s*([0-9]+(?:\.[0-9]+)?)\s*$")


def _normalise(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _adapter_rho(text: str) -> tuple[str, str] | None:
    """Recognise only the two historical/canonical exact shapes."""
    normal = _normalise(text)
    if "q.2 / 20" in normal and "q.1 / 20" in normal:
        return ("q5/20", "q4/20")
    if "q.2 / 100" in normal and "q.1 / 200" in normal:
        return ("q5/100", "q4/200")
    return None


def audit_routeb_p4_source_contract(
    pmi_source: str,
    dh_source: str,
    adapter_source: str | None = None,
) -> RouteBP4SourceContract:
    """Audit the narrow canonical P4 force/descriptor source seam.

    ``adapter_source`` is optional so a source scan can pass before a new
    sidecar exists.  If supplied, a mismatching historical adapter is a hard
    rejection rather than a warning.
    """
    errors: list[str] = []
    warnings: list[str] = []
    kc: Fraction | None = None
    match = _KC.search(pmi_source)
    if match is None:
        errors.append("missing_pmi_kc_literal")
    else:
        kc = Fraction(match.group(1))
        if kc != Fraction(1, 20):
            errors.append(f"unexpected_pmi_kc:{kc}")

    pmi = _normalise(pmi_source)
    if "f1 = -a[ja] * qa - c[ja] * dqa + kc * qb + gw[ja] * w" not in pmi:
        errors.append("pmi_f1_cross_term_not_bound")
    if "f2 = -a[jb] * qb - c[jb] * dqb + kc * qa + gw[jb] * w" not in pmi:
        errors.append("pmi_f2_cross_term_not_bound")

    dh = _normalise(dh_source)
    expected_tau = "tau = -Kp .* q - (Kd + b_fr) .* dq + G0v + (gw_coef .* I_val) .* w"
    if expected_tau not in dh:
        errors.append("deployed_tau_formula_not_bound")
    if "Mq \\ (tau - Cdq - Gq)" not in dh:
        errors.append("deployed_descriptor_solve_not_bound")
    if re.search(r"\bkc\b", dh):
        errors.append("deployed_dh_source_contains_unexpected_kc")

    observed = _adapter_rho(adapter_source) if adapter_source is not None else None
    if adapter_source is not None and observed != ("q5/20", "q4/20"):
        errors.append("adapter_kc_scale_mismatch")
    if adapter_source is None:
        warnings.append("no_adapter_source_supplied")

    status = "SOURCE_CONTRACT_PASS"
    if errors:
        status = "OPEN_FAIL_CLOSED"
    elif adapter_source is not None and observed == ("q5/20", "q4/20"):
        status = "SOURCE_AND_ADAPTER_SCALE_PASS"

    return RouteBP4SourceContract(
        status=status,
        kc=kc,
        expected_rho_kc=("q5/20", "q4/20"),
        observed_adapter_rho_kc=observed,
        remote_term_required="M_BD(q) * a_D",
        force_acceleration_separated=True,
        errors=tuple(errors),
        warnings=tuple(warnings),
    )


__all__ = ["RouteBP4SourceContract", "audit_routeb_p4_source_contract"]
