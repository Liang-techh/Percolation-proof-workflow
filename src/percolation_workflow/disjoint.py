"""Pure helpers for the disjoint DO repair-receipt surface.

This module deliberately has no imports from admission, registry, or store
code.  It normalizes and classifies data; it never reads or writes state.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import PurePosixPath
from typing import Any, Mapping


DO_SCHEMA_VERSION = 1
_DO_KEYS = frozenset({"schema_version", "path", "kind", "sha256"})


def normalize_do_path(value: Any) -> str | None:
    """Return a safe, canonical relative POSIX path, or ``None``."""
    if not isinstance(value, str) or not value.strip():
        return None
    path = PurePosixPath(value)
    if (path.is_absolute() or value.startswith(("/", "\\")) or "\\" in value
            or "." in path.parts or ".." in path.parts
            or path == PurePosixPath(".") or not path.name):
        return None
    return path.as_posix()


def canonical_do_schema(value: Any) -> dict[str, Any] | None:
    """Copy a DO mapping after checking its versioned object envelope."""
    if (not isinstance(value, Mapping) or value.get("schema_version") != DO_SCHEMA_VERSION
            or frozenset(value) != _DO_KEYS or value.get("kind") != "repair"):
        return None
    result = dict(value)
    path = normalize_do_path(result.get("path"))
    if path is None:
        return None
    result["path"] = path
    return result


def do_sha256(value: Any) -> str:
    """Hash a JSON-compatible value using the DO canonical encoding."""
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True,
                         separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def classify_manual_review(value: Any) -> str | None:
    """Return the sole blocking manual-review category, if one is present."""
    if not isinstance(value, Mapping):
        return "invalid_schema"
    if value.get("schema_version") != DO_SCHEMA_VERSION:
        return "schema_mismatch"
    if normalize_do_path(value.get("path")) is None:
        return "unsafe_path"
    expected = value.get("sha256")
    if not isinstance(expected, str) or expected != do_sha256(
            {key: item for key, item in value.items() if key != "sha256"}):
        return "hash_mismatch"
    if frozenset(value) != _DO_KEYS or value.get("kind") != "repair":
        return "invalid_schema"
    return None


def audit_do(value: Any) -> dict[str, Any]:
    """Produce a deterministic, non-persistent DO audit projection."""
    category = classify_manual_review(value)
    schema = canonical_do_schema(value)
    return {"schema_version": DO_SCHEMA_VERSION, "path": schema["path"] if schema else None,
            "sha256": do_sha256(value) if isinstance(value, Mapping) else None,
            "manual_review": category, "ok": category is None}


def build_repair_do(path: Any) -> dict[str, Any]:
    """Build the minimal immutable DO envelope used by the repair-loop event."""
    raw = {"schema_version": DO_SCHEMA_VERSION, "path": path, "kind": "repair"}
    return {**raw, "sha256": do_sha256(raw)} if normalize_do_path(path) is not None else raw
