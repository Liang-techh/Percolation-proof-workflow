"""Fail-closed, read-only validation for external theorem candidate catalogs."""
from __future__ import annotations
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

_REQUIRED_ROOT = ("commit", "license", "lean_toolchain", "mathlib_revision")
_NUMBER_THEORY_MARKERS = ("number-theor", "number_theor", "fermat", "prime", "divisib")

class CatalogValidationError(ValueError):
    """The external catalog is malformed or unsafe to classify."""

@dataclass(frozen=True)
class CatalogValidation:
    classifications: tuple[int, ...]
    reuse_set: tuple[str, ...]
    provenance_hash: str
    current_pin_status: str

def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())

def _is_pure_number_theory(candidate: Mapping[str, Any]) -> bool:
    text = " ".join(str(candidate.get(k, "")) for k in ("path", "kind", "rationale", "current_routeb_use")).lower()
    return any(marker in text for marker in _NUMBER_THEORY_MARKERS)

def validate_catalog(catalog: Mapping[str, Any]) -> CatalogValidation:
    """Validate decoded JSON and return derived facts without mutating it."""
    if not isinstance(catalog, Mapping):
        raise CatalogValidationError("catalog must be an object")
    missing = [key for key in _REQUIRED_ROOT if not _nonempty(catalog.get(key))]
    if missing:
        raise CatalogValidationError("missing source/pin metadata: " + ", ".join(missing))
    candidates = catalog.get("candidates")
    if not isinstance(candidates, list):
        raise CatalogValidationError("candidates must be a list")
    classifications: list[int] = []
    reuse: list[str] = []
    for index, candidate in enumerate(candidates):
        if not isinstance(candidate, Mapping):
            raise CatalogValidationError(f"candidate {index} must be an object")
        for key in ("path", "attribution_ref"):
            if not _nonempty(candidate.get(key)):
                raise CatalogValidationError(f"candidate {index} missing {key}")
        classification = candidate.get("classification")
        if type(classification) is not int or classification not in (1, 2, 3):
            raise CatalogValidationError(f"candidate {index} classification must be 1, 2, or 3")
        classifications.append(classification)
        if not _is_pure_number_theory(candidate) and classification in (1, 2):
            reuse.append(candidate["path"])
    canonical = json.dumps(catalog, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return CatalogValidation(tuple(classifications), tuple(reuse), hashlib.sha256(canonical).hexdigest(), "declared")

def validate_catalog_file(path: str | Path) -> CatalogValidation:
    """Read and validate one JSON catalog without writing project state."""
    with Path(path).open(encoding="utf-8") as handle:
        return validate_catalog(json.load(handle))
