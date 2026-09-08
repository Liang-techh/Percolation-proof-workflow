import json
from pathlib import Path

import pytest

from percolation_workflow.flt_provenance import (
    FLTProvenanceError,
    validate_flt_provenance_manifest,
)


ROOT = Path(__file__).parents[1]
MANIFEST = ROOT / "examples" / "anthropic_flt_reusable_lean" / "PROVENANCE_CORRECTION_20260908.json"


def test_flt_provenance_manifest_is_advisory_and_pin_complete():
    result = validate_flt_provenance_manifest(MANIFEST)
    assert result["advisory_only"] is True
    assert result["authoritative"] is False
    assert result["repository"]["canonical"].endswith("anthropics/fermats-last-theorem")
    assert result["p2m_contract"]["clear_aux_decls_instead_of_revert"] is True
    assert result["p2m_contract"]["universe_generalization_check"] is True
    assert any(source["ownership"].startswith("third-party")
               for source in result["source_files"])


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("registry_eligible", True),
        ("status", "accepted"),
    ],
)
def test_flt_provenance_rejects_authority_or_status_drift(field, value):
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    data[field] = value
    with pytest.raises(FLTProvenanceError):
        validate_flt_provenance_manifest(data)


def test_flt_provenance_requires_universe_generalization_check():
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    data["p2m_contract"]["universe_generalization_check"] = False
    with pytest.raises(FLTProvenanceError, match="universe_generalization_check"):
        validate_flt_provenance_manifest(data)
