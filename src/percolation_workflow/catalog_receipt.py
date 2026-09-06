"""Build a provenance-only receipt from an external candidate catalog.

The receipt is deliberately separate from ``WorkflowState`` and the verified
theorem registry.  It records what the catalog validator observed; it never
asserts that any external candidate is a theorem or a Route-B proof.
"""
from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
from typing import Any

from .external_catalog import validate_catalog


RECEIPT_SCHEMA = "external-catalog-receipt-v1"


def build_catalog_receipt(path: str | Path) -> dict[str, Any]:
    """Return a deterministic, non-admitting receipt for one catalog file."""
    source = Path(path)
    with source.open(encoding="utf-8") as handle:
        catalog = json.load(handle)
    validation = validate_catalog(catalog)
    candidates = catalog["candidates"]
    return {
        "schema_version": RECEIPT_SCHEMA,
        "source_path": str(source.resolve()),
        "catalog_sha256": validation.provenance_hash,
        "repository": catalog.get("repository"),
        "source_commit": catalog["commit"],
        "license": catalog["license"],
        "attribution_present": all(
            isinstance(candidate.get("attribution_ref"), str)
            and bool(candidate["attribution_ref"].strip())
            for candidate in candidates
        ),
        "lean_toolchain": catalog["lean_toolchain"],
        "mathlib_revision": catalog["mathlib_revision"],
        "classification_histogram": dict(
            sorted((str(key), value) for key, value in Counter(validation.classifications).items())
        ),
        "routeb_reuse_set": list(validation.reuse_set),
        "current_pin_status": validation.current_pin_status,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }


def write_catalog_receipt(path: str | Path, output: str | Path) -> dict[str, Any]:
    """Write only a catalog receipt; no workflow or registry state is touched."""
    receipt = build_catalog_receipt(path)
    destination = Path(output)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return receipt
