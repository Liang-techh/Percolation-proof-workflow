import json
from pathlib import Path
import pytest
from percolation_workflow.external_catalog import CatalogValidationError, validate_catalog, validate_catalog_file

CATALOG = Path(__file__).parents[1] / "artifacts" / "anthropic_fermats_intake" / "catalog.json"

def test_anthropic_catalog_is_read_only_and_classified():
    before = CATALOG.read_bytes()
    result = validate_catalog_file(CATALOG)
    assert CATALOG.read_bytes() == before
    assert set(result.classifications) == {1, 2, 3}
    assert len(result.provenance_hash) == 64
    assert result.current_pin_status == "declared"
    assert result.reuse_set

def test_classification_is_strictly_one_two_or_three():
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    catalog["candidates"][0]["classification"] = 4
    with pytest.raises(CatalogValidationError, match="classification"):
        validate_catalog(catalog)

def test_pure_number_theory_is_not_routeb_reuse():
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    candidate = dict(catalog["candidates"][0])
    candidate.update(path="Theorems/number_theory.lean", kind="pure number-theory lemma", classification=1)
    catalog["candidates"] = [candidate]
    assert validate_catalog(catalog).reuse_set == ()

@pytest.mark.parametrize("field", ["commit", "license", "lean_toolchain", "mathlib_revision"])
def test_source_and_current_pin_metadata_are_required(field):
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    del catalog[field]
    with pytest.raises(CatalogValidationError):
        validate_catalog(catalog)
