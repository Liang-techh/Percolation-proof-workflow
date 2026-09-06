"""Fail-closed, provenance-only reuse projection for external FLT candidates.

This module deliberately sits outside :mod:`registry` and ``WorkflowState``.
It verifies that an externally discovered candidate still names the exact
source bytes recorded by its intake metadata, then returns a small advisory
projection.  It has no writer and cannot promote a candidate into any
authoritative workflow state.
"""
from __future__ import annotations

from collections.abc import Mapping, Sequence
import hashlib
import json
from pathlib import Path
import re
from typing import Any


SCHEMA_VERSION = "anthropic-advisory-reuse-v1"

_REQUIRED_PROVENANCE = (
    "repository",
    "commit",
    "license",
    "lean_toolchain",
    "mathlib_revision",
)
_CANDIDATE_METADATA = (
    "kind",
    "classification",
    "reuse_mode",
    "rationale",
    "current_routeb_use",
)
_FORBIDDEN_KEYS = frozenset(
    {
        "verified_registry",
        "registry",
        "registry_promoted",
        "dependencies",
        "closure",
        "formal_certificate_allowed",
        "authoritative",
        "advisory_only",
    }
)
_SHA256 = re.compile(r"\A[0-9a-f]{64}\Z")


class AdvisoryReuseError(ValueError):
    """The intake or one of its source bindings is unsafe to project."""


def _nonempty_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _reject_authority_fields(value: Any, location: str = "catalog") -> None:
    """Reject authority-bearing input instead of silently dropping it."""
    if isinstance(value, Mapping):
        for key, child in value.items():
            if key in _FORBIDDEN_KEYS:
                raise AdvisoryReuseError(
                    f"{location} contains forbidden authority field: {key}"
                )
            _reject_authority_fields(child, f"{location}.{key}")
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        for index, child in enumerate(value):
            _reject_authority_fields(child, f"{location}[{index}]")


def _read_catalog(catalog: Mapping[str, Any] | str | Path) -> Mapping[str, Any]:
    if isinstance(catalog, Mapping):
        return catalog
    path = Path(catalog)
    try:
        with path.open(encoding="utf-8") as handle:
            decoded = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise AdvisoryReuseError(f"cannot read advisory intake catalog: {path}") from exc
    if not isinstance(decoded, Mapping):
        raise AdvisoryReuseError("advisory intake catalog must be an object")
    return decoded


def _canonical_sha256(value: Mapping[str, Any]) -> str:
    try:
        encoded = json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise AdvisoryReuseError("advisory intake catalog is not JSON-compatible") from exc
    return hashlib.sha256(encoded).hexdigest()


def _required_provenance(catalog: Mapping[str, Any]) -> dict[str, str]:
    missing = [key for key in _REQUIRED_PROVENANCE if not _nonempty_text(catalog.get(key))]
    if missing:
        raise AdvisoryReuseError("missing provenance: " + ", ".join(missing))
    return {key: catalog[key].strip() for key in _REQUIRED_PROVENANCE}


def _aliased_text(
    candidate: Mapping[str, Any], primary: str, alias: str, location: str
) -> str:
    primary_value = candidate.get(primary)
    alias_value = candidate.get(alias)
    if primary_value is not None and alias_value is not None and primary_value != alias_value:
        raise AdvisoryReuseError(f"{location} has conflicting {primary}/{alias}")
    value = primary_value if primary_value is not None else alias_value
    if not _nonempty_text(value):
        raise AdvisoryReuseError(f"{location} missing {primary}")
    return value.strip()


def _bound_source(
    candidate: Mapping[str, Any], source_root: Path, index: int
) -> dict[str, Any]:
    location = f"candidate {index}"
    relative_name = _aliased_text(candidate, "path", "source_path", location)
    expected_hash = _aliased_text(candidate, "sha256", "source_sha256", location)
    if not _SHA256.fullmatch(expected_hash):
        raise AdvisoryReuseError(f"{location} has invalid sha256")

    relative = Path(relative_name)
    if relative.is_absolute() or "\x00" in relative_name or ".." in relative.parts:
        raise AdvisoryReuseError(f"{location} source path must stay inside source_root")
    try:
        resolved = (source_root / relative).resolve()
    except (OSError, RuntimeError, ValueError) as exc:
        raise AdvisoryReuseError(
            f"{location} source path cannot be resolved: {relative_name}"
        ) from exc
    try:
        inside_root = resolved.is_relative_to(source_root)
    except ValueError:
        inside_root = False
    if not inside_root:
        raise AdvisoryReuseError(f"{location} source path escapes source_root")
    if not resolved.is_file():
        raise AdvisoryReuseError(f"{location} source is missing: {relative_name}")
    try:
        actual_hash = hashlib.sha256(resolved.read_bytes()).hexdigest()
    except OSError as exc:
        raise AdvisoryReuseError(f"{location} source cannot be read: {relative_name}") from exc
    if actual_hash != expected_hash.lower():
        raise AdvisoryReuseError(f"{location} source is stale: sha256 mismatch")

    attribution = candidate.get("attribution_ref")
    if not _nonempty_text(attribution):
        raise AdvisoryReuseError(f"{location} missing attribution_ref")

    projected: dict[str, Any] = {
        "path": resolved.relative_to(source_root).as_posix(),
        "sha256": expected_hash.lower(),
        "attribution_ref": attribution.strip(),
    }
    for key in _CANDIDATE_METADATA:
        if key not in candidate:
            continue
        value = candidate[key]
        if key == "classification":
            if type(value) is not int or value not in (1, 2, 3):
                raise AdvisoryReuseError(f"{location} has invalid classification")
        elif not _nonempty_text(value):
            raise AdvisoryReuseError(f"{location} has invalid {key}")
        projected[key] = value
    return projected


def project_advisory_reuse(
    catalog: Mapping[str, Any] | str | Path, source_root: str | Path
) -> dict[str, Any]:
    """Return a hash-bound advisory projection without mutating workflow state.

    ``catalog`` may be an already decoded intake object or a JSON catalog path.
    Every candidate must provide ``path`` (or ``source_path``), ``sha256`` (or
    ``source_sha256``), and ``attribution_ref``.  The path is resolved below
    ``source_root`` and its current bytes must match the declared SHA-256.

    The returned schema intentionally contains only advisory fields.  In
    particular, no registry, dependency, closure, or certificate-admission
    field is accepted or emitted.  Any missing, stale, malformed, or
    authority-bearing input raises :class:`AdvisoryReuseError`.
    """
    decoded = _read_catalog(catalog)
    _reject_authority_fields(decoded)
    provenance = _required_provenance(decoded)
    candidates = decoded.get("candidates")
    if not isinstance(candidates, list):
        raise AdvisoryReuseError("candidates must be a list")

    try:
        root = Path(source_root).resolve()
        root_is_dir = root.is_dir()
    except (OSError, RuntimeError, TypeError, ValueError) as exc:
        raise AdvisoryReuseError("source_root is invalid") from exc
    if not root_is_dir:
        raise AdvisoryReuseError(f"source_root is missing: {source_root}")

    projected_candidates: list[dict[str, Any]] = []
    seen_paths: set[str] = set()
    for index, candidate in enumerate(candidates):
        if not isinstance(candidate, Mapping):
            raise AdvisoryReuseError(f"candidate {index} must be an object")
        projected = _bound_source(candidate, root, index)
        if projected["path"] in seen_paths:
            raise AdvisoryReuseError(f"duplicate candidate source path: {projected['path']}")
        seen_paths.add(projected["path"])
        projected_candidates.append(projected)

    return {
        "schema_version": SCHEMA_VERSION,
        "advisory_only": True,
        "authoritative": False,
        "catalog_sha256": _canonical_sha256(decoded),
        **provenance,
        "candidates": projected_candidates,
    }


__all__ = ["AdvisoryReuseError", "SCHEMA_VERSION", "project_advisory_reuse"]
