"""Structural validator for a certificate-indexed initial-value contract.

This module checks identity and event-chain shape only.  It deliberately does
not infer a polynomial inequality from a manifest, and a structurally
consistent contract remains pending until an exact finite checker, source
binding, and the normal admission gates provide their own receipts.
"""
from __future__ import annotations

from collections.abc import Mapping
from fractions import Fraction
import copy
import json
from pathlib import Path
import re
from typing import Any


SCHEMA_VERSION = "routeb-initial-binding-contract-v1"
SHA256 = re.compile(r"\A[0-9a-f]{64}\Z")
RATIONAL = re.compile(r"\A[+-]?[0-9]+(?:/[1-9][0-9]*)?\Z")
VARIABLE_ORDER = ("q4", "q5", "v4", "v5", "t")


class InitialBindingContractError(ValueError):
    """The finite initial-binding contract is malformed or inconsistent."""


def _read(value: Mapping[str, Any] | str | Path) -> Mapping[str, Any]:
    if isinstance(value, Mapping):
        return value
    try:
        with Path(value).open(encoding="utf-8") as handle:
            decoded = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise InitialBindingContractError("cannot read initial-binding contract") from exc
    if not isinstance(decoded, Mapping):
        raise InitialBindingContractError("initial-binding contract must be an object")
    return decoded


def _text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise InitialBindingContractError(f"missing or invalid {field}")
    return value.strip()


def _hash(value: Any, field: str) -> str:
    result = _text(value, field).lower()
    if not SHA256.fullmatch(result):
        raise InitialBindingContractError(f"{field} must be a SHA-256 digest")
    return result


def _rational(value: Any, field: str) -> str:
    result = _text(value, field)
    if not RATIONAL.fullmatch(result):
        raise InitialBindingContractError(f"{field} must be a canonical rational token")
    try:
        Fraction(result)
    except (ValueError, ZeroDivisionError) as exc:
        raise InitialBindingContractError(f"{field} is not a rational") from exc
    return result


def _hash_map(value: Any, field: str) -> dict[str, str]:
    if not isinstance(value, Mapping) or not value:
        raise InitialBindingContractError(f"{field} must be a nonempty object")
    return {str(key): _hash(item, f"{field}.{key}") for key, item in value.items()}


def validate_initial_binding_contract(
    contract: Mapping[str, Any] | str | Path,
) -> dict[str, Any]:
    """Validate structural bindings and return an explicitly pending result."""
    data = copy.deepcopy(dict(_read(contract)))
    if data.get("schema_version") != SCHEMA_VERSION:
        raise InitialBindingContractError("unsupported initial-binding schema")
    if data.get("registry_eligible") is not False:
        raise InitialBindingContractError("registry_eligible must be false")
    if data.get("formal_certificate_allowed") is not False:
        raise InitialBindingContractError("formal_certificate_allowed must be false")

    function = data.get("function")
    if not isinstance(function, Mapping):
        raise InitialBindingContractError("function must be an object")
    certificate_hash = _hash(function.get("certificate_sha256"), "function.certificate_sha256")
    interpretation = _text(function.get("coefficient_interpretation"),
                            "function.coefficient_interpretation")
    if interpretation not in {"literal_decimal", "decoded_binary64"}:
        raise InitialBindingContractError("function.coefficient_interpretation is unsupported")
    order = function.get("variable_order")
    if order != list(VARIABLE_ORDER):
        raise InitialBindingContractError("function.variable_order must be q4,q5,v4,v5,t")
    if function.get("t0") not in (0, "0"):
        raise InitialBindingContractError("function.t0 must be zero")

    domain = data.get("domain")
    if not isinstance(domain, Mapping):
        raise InitialBindingContractError("domain must be an object")
    _text(domain.get("x0_key"), "domain.x0_key")
    _text(domain.get("constraint"), "domain.constraint")
    if domain.get("remote_coordinates_zero") is not True:
        raise InitialBindingContractError("domain.remote_coordinates_zero must be true")

    upper = data.get("upper")
    if not isinstance(upper, Mapping):
        raise InitialBindingContractError("upper must be an object")
    upper_hash = _hash(upper.get("artifact_sha256"), "upper.artifact_sha256")
    _text(upper.get("metric_selector"), "upper.metric_selector")
    upper_value = _rational(upper.get("value"), "upper.value")
    if upper.get("unique_row_count") != 1:
        raise InitialBindingContractError("upper.unique_row_count must be one")

    witness = data.get("initial_witness")
    if not isinstance(witness, Mapping):
        raise InitialBindingContractError("initial_witness must be an object")
    _text(witness.get("representation"), "initial_witness.representation")
    _hash(witness.get("artifact_sha256"), "initial_witness.artifact_sha256")
    basis = witness.get("monomial_basis")
    if not isinstance(basis, list) or not basis or not all(
        isinstance(item, str) and item.strip() for item in basis
    ):
        raise InitialBindingContractError("initial_witness.monomial_basis must be nonempty")
    if witness.get("exact_coefficient_identity_checked") is not True:
        raise InitialBindingContractError(
            "initial_witness.exact_coefficient_identity_checked must be true"
        )
    if witness.get("psd_factorization_checked") is not True:
        raise InitialBindingContractError(
            "initial_witness.psd_factorization_checked must be true"
        )

    producer = data.get("producer_event")
    consumer = data.get("consumer_event")
    if not isinstance(producer, Mapping) or not isinstance(consumer, Mapping):
        raise InitialBindingContractError("producer_event and consumer_event are required")
    producer_id = _text(producer.get("event_id"), "producer_event.event_id")
    consumer_id = _text(consumer.get("event_id"), "consumer_event.event_id")
    producer_outputs = _hash_map(producer.get("output_hashes"), "producer_event.output_hashes")
    consumer_inputs = _hash_map(consumer.get("input_hashes"), "consumer_event.input_hashes")
    if consumer.get("producer_event_ref") != producer_id:
        raise InitialBindingContractError("consumer_event.producer_event_ref does not match producer")
    if consumer_inputs != producer_outputs:
        raise InitialBindingContractError("consumer input hashes do not equal producer outputs")
    _text(consumer.get("function_key"), "consumer_event.function_key")
    _text(producer.get("execution_record"), "producer_event.execution_record")

    finite = data.get("finite_checker_receipt")
    finite_ready = isinstance(finite, Mapping) and finite.get("status") == "exact_checker_passed"
    pending_reasons = []
    if not finite_ready:
        pending_reasons.append("missing_exact_finite_checker_receipt")
    if producer.get("execution_status") != "completed":
        pending_reasons.append("producer_execution_not_authenticated")
    if consumer.get("execution_status") != "completed":
        pending_reasons.append("consumer_execution_not_authenticated")

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PENDING",
        "structural_consistency": True,
        "pending_reasons": pending_reasons,
        "function": {
            "certificate_sha256": certificate_hash,
            "coefficient_interpretation": interpretation,
            "variable_order": list(VARIABLE_ORDER),
            "t0": 0,
        },
        "upper": {"artifact_sha256": upper_hash, "value": upper_value},
        "producer_event_id": producer_id,
        "consumer_event_id": consumer_id,
        "finite_checker_receipt_present": finite_ready,
        "registry_eligible": False,
        "formal_certificate_allowed": False,
    }


__all__ = [
    "InitialBindingContractError",
    "SCHEMA_VERSION",
    "validate_initial_binding_contract",
]
