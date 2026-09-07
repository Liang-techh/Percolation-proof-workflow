"""Map a verified Lean leaf receipt to a theorem-DAG advisory artifact.

This module is intentionally a projection only. It does not import the
workflow registry, mutate state, or turn a compiled candidate into a verified
node. Missing authoritative evidence is ``pending``; malformed or negative
evidence is ``rejected``.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Mapping, Sequence
from typing import Any

_SHA256 = re.compile(r"^[0-9a-f]{64}$")


def _sha256(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True,
                         separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _hash(value: Any) -> bool:
    return isinstance(value, str) and bool(_SHA256.fullmatch(value))


def _strings(value: Any, field: str, errors: list[str]) -> None:
    if not isinstance(value, list) or any(not _nonempty(item) for item in value):
        errors.append(f"{field} must be a list of nonempty strings")
    elif len(value) != len(set(value)):
        errors.append(f"{field} contains duplicate entries")


def _gate(value: Any, field: str, errors: list[str]) -> None:
    if not isinstance(value, Mapping):
        errors.append(f"{field} must be an object")
        return
    present = value.get("present", value.get("accepted"))
    if not isinstance(present, bool):
        errors.append(f"{field}.present must be boolean")
    if "evidence_id" in value and not _nonempty(value["evidence_id"]):
        errors.append(f"{field}.evidence_id must be nonempty")


def validate_leaf_inputs(receipt: Mapping[str, Any], *, source_binding: Any = None,
                         coverage: Any = None, terminal_transfer: Any = None) -> tuple[str, ...]:
    """Return malformed-input errors; absence is handled as pending by the builder."""
    if not isinstance(receipt, Mapping):
        return ("compile receipt must be an object",)
    errors: list[str] = []
    if receipt.get("compile_exit_code") != 0:
        errors.append("compile_exit_code must be zero")
    if not _nonempty(receipt.get("module")) or not _nonempty(receipt.get("theorem")):
        errors.append("module and theorem are required")
    if "source_hash" in receipt and not _hash(receipt["source_hash"]):
        errors.append("source_hash must be a lowercase SHA-256")
    for name, value in (("source_binding", source_binding), ("coverage", coverage),
                        ("terminal_transfer", terminal_transfer)):
        if value is not None:
            _gate(value, name, errors)
    return tuple(errors)


def build_advisory_artifact(
    receipt: Mapping[str, Any], *, source_binding: Any = None,
    coverage: Any = None, terminal_transfer: Any = None,
    scope: Sequence[str] | None = None,
    open_obligations: Sequence[str] | None = None,
    parent_id: str | None = None,
) -> dict[str, Any]:
    """Build a theorem-DAG advisory artifact without registry promotion.

    A missing gate is pending; an explicit ``present: false`` gate is rejected.
    Even ``advisory_ready`` has ``registry_status=pending`` and
    ``promotion_allowed=false``.
    """
    if not isinstance(receipt, Mapping):
        return _rejected(("compile receipt must be an object",), receipt)
    errors = list(validate_leaf_inputs(receipt, source_binding=source_binding,
                                       coverage=coverage,
                                       terminal_transfer=terminal_transfer))
    pending: list[str] = []
    if "source_hash" not in receipt:
        pending.append("missing source_hash")
    for name, value in (("source_binding", source_binding), ("coverage", coverage),
                        ("terminal_transfer", terminal_transfer)):
        if value is None:
            pending.append(f"missing {name} evidence")
        elif isinstance(value, Mapping) and value.get("present", value.get("accepted")) is False:
            errors.append(f"{name} evidence is explicitly negative")
    normalized_scope = (list(scope) if scope is not None
                        and not isinstance(scope, (str, bytes)) else None)
    if scope is None:
        pending.append("missing scope")
    elif normalized_scope is None:
        errors.append("scope must be a list of nonempty strings")
    else:
        _strings(normalized_scope, "scope", errors)
    normalized_open = (list(open_obligations) if open_obligations is not None
                       and not isinstance(open_obligations, (str, bytes)) else None)
    if open_obligations is None:
        pending.append("missing open_obligations")
    elif normalized_open is None:
        errors.append("open_obligations must be a list of nonempty strings")
    else:
        _strings(normalized_open, "open_obligations", errors)
        if normalized_open:
            pending.append("open obligations remain")
    if errors:
        return _rejected(tuple(dict.fromkeys(errors)), receipt)
    if pending:
        return _artifact("pending", tuple(dict.fromkeys(pending)), receipt,
                         source_binding, coverage, terminal_transfer,
                         normalized_scope, normalized_open, parent_id)
    return _artifact("advisory_ready", (), receipt, source_binding, coverage,
                     terminal_transfer, normalized_scope, normalized_open, parent_id)


def _rejected(reasons: tuple[str, ...], receipt: Any) -> dict[str, Any]:
    return {"schema_version": 1, "status": "rejected", "reasons": list(reasons),
            "receipt": dict(receipt) if isinstance(receipt, Mapping) else None,
            "registry_status": "pending", "verified": False,
            "promotion_allowed": False}


def _artifact(status: str, reasons: tuple[str, ...], receipt: Mapping[str, Any],
              source_binding: Any, coverage: Any, terminal_transfer: Any,
              scope: list[str] | None, open_obligations: list[str] | None,
              parent_id: str | None) -> dict[str, Any]:
    node_id = f"{receipt['module']}.{receipt['theorem']}"
    node = {"node_id": node_id, "parent_id": parent_id,
            "child_ids": [], "dependency_ids": []}
    return {"schema_version": 1, "status": status, "reasons": list(reasons),
            "candidate_status": "compiled_candidate", "registry_status": "pending",
            "verified": False, "promotion_allowed": False,
            "statement_identity": {"module": receipt["module"], "theorem": receipt["theorem"]},
            "compile_receipt": dict(receipt), "source_hash": receipt.get("source_hash"),
            "scope": scope, "open_obligations": open_obligations,
            "gates": {"source_binding": source_binding, "coverage": coverage,
                      "terminal_transfer": terminal_transfer},
            "dag": {"nodes": [node], "root": node_id},
            "artifact_sha256": _sha256({"node": node, "source_hash": receipt.get("source_hash"),
                                         "scope": scope, "open_obligations": open_obligations})}
