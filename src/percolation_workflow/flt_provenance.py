"""Validate the provenance contract for an Anthropic FLT reuse candidate.

This is intentionally an advisory, read-only boundary.  It records the
canonical upstream identity, historical aliases, third-party ownership, and
the minimum P2M behavior that must be reproduced before a candidate can even
enter a pinned Lean/comparator job.  It cannot write workflow state or promote
anything into the verified registry.
"""
from __future__ import annotations

from collections.abc import Mapping
import copy
import json
from pathlib import Path
import re
from typing import Any


SCHEMA_VERSION = "flt-reuse-provenance-v1"
CANONICAL_REPOSITORY = "https://github.com/anthropics/fermats-last-theorem"
SHA256 = re.compile(r"\A[0-9a-f]{64}\Z")
SHA1 = re.compile(r"\A[0-9a-f]{40}\Z")


class FLTProvenanceError(ValueError):
    """The advisory FLT provenance manifest is incomplete or unsafe."""


def _read(value: Mapping[str, Any] | str | Path) -> Mapping[str, Any]:
    if isinstance(value, Mapping):
        return value
    try:
        with Path(value).open(encoding="utf-8") as handle:
            decoded = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise FLTProvenanceError("cannot read FLT provenance manifest") from exc
    if not isinstance(decoded, Mapping):
        raise FLTProvenanceError("FLT provenance manifest must be an object")
    return decoded


def _text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise FLTProvenanceError(f"missing or invalid {field}")
    return value.strip()


def validate_flt_provenance_manifest(
    manifest: Mapping[str, Any] | str | Path,
) -> dict[str, Any]:
    """Return a normalized advisory manifest, without mutating any state.

    The validator deliberately requires the exact P2M behavior and an explicit
    third-party attribution record.  A manifest that passes this function is
    still only eligible for a later pinned compile/comparator job.
    """
    raw = _read(manifest)
    data = copy.deepcopy(dict(raw))
    if data.get("schema_version") != SCHEMA_VERSION:
        raise FLTProvenanceError("unsupported FLT provenance schema")
    if data.get("status") != "pending_review":
        raise FLTProvenanceError("FLT candidate must remain pending_review")
    if data.get("registry_eligible") is not False:
        raise FLTProvenanceError("registry_eligible must be false")

    repository = data.get("repository")
    if not isinstance(repository, Mapping):
        raise FLTProvenanceError("repository provenance must be an object")
    if _text(repository.get("canonical"), "repository.canonical") != CANONICAL_REPOSITORY:
        raise FLTProvenanceError("repository.canonical is not the canonical FLT repository")
    aliases = repository.get("historical_aliases")
    if not isinstance(aliases, list) or not aliases or not all(
        isinstance(alias, str) and alias.strip() for alias in aliases
    ):
        raise FLTProvenanceError("historical repository aliases are required")
    _text(repository.get("commit"), "repository.commit")

    source_files = data.get("source_files")
    if not isinstance(source_files, list) or not source_files:
        raise FLTProvenanceError("source_files must be a nonempty list")
    for index, source in enumerate(source_files):
        if not isinstance(source, Mapping):
            raise FLTProvenanceError(f"source_files[{index}] must be an object")
        _text(source.get("path"), f"source_files[{index}].path")
        digest = _text(source.get("git_blob_sha1"), f"source_files[{index}].git_blob_sha1")
        if not SHA1.fullmatch(digest.lower()):
            raise FLTProvenanceError(f"source_files[{index}] has invalid git blob sha1")
        _text(source.get("ownership"), f"source_files[{index}].ownership")

    p2m = data.get("p2m_contract")
    if not isinstance(p2m, Mapping):
        raise FLTProvenanceError("p2m_contract must be an object")
    required_behavior = (
        "preserve_order",
        "clear_aux_decls_instead_of_revert",
        "universe_generalization_check",
        "comparator_receipt",
    )
    for field in required_behavior:
        if p2m.get(field) is not True:
            raise FLTProvenanceError(f"p2m_contract.{field} must be true")

    candidate = data.get("candidate")
    if not isinstance(candidate, Mapping):
        raise FLTProvenanceError("candidate must be an object")
    _text(candidate.get("path"), "candidate.path")
    digest = _text(candidate.get("sha256"), "candidate.sha256")
    if not SHA256.fullmatch(digest.lower()):
        raise FLTProvenanceError("candidate.sha256 is invalid")
    if candidate.get("classification") not in (1, 2, 3):
        raise FLTProvenanceError("candidate.classification must be 1, 2, or 3")
    if candidate.get("admission_status") != "pending":
        raise FLTProvenanceError("candidate.admission_status must be pending")

    data["advisory_only"] = True
    data["authoritative"] = False
    return data


__all__ = [
    "CANONICAL_REPOSITORY",
    "FLTProvenanceError",
    "SCHEMA_VERSION",
    "validate_flt_provenance_manifest",
]
