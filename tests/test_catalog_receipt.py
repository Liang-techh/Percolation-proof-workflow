import json
from pathlib import Path

import pytest

from percolation_workflow.catalog_receipt import build_catalog_receipt, write_catalog_receipt


CATALOG = Path(__file__).parents[1] / "artifacts" / "anthropic_fermats_intake" / "catalog.json"


def test_catalog_receipt_is_provenance_only():
    receipt = build_catalog_receipt(CATALOG)
    assert receipt["schema_version"] == "external-catalog-receipt-v1"
    assert receipt["source_commit"] == "aa2d8b34692b16c70f699536de0d8e75b9a3e9ef"
    assert receipt["license"] == "Apache-2.0"
    assert receipt["attribution_present"] is True
    assert receipt["registry_promoted"] is False
    assert receipt["formal_certificate_allowed"] is False
    assert receipt["classification_histogram"] == {"1": 4, "2": 4, "3": 8}
    assert receipt["routeb_reuse_set"]


def test_catalog_receipt_write_does_not_change_catalog(tmp_path):
    before = CATALOG.read_bytes()
    output = tmp_path / "receipt.json"
    receipt = write_catalog_receipt(CATALOG, output)
    assert json.loads(output.read_text(encoding="utf-8")) == receipt
    assert CATALOG.read_bytes() == before


def test_malformed_catalog_fails_closed(tmp_path):
    malformed = json.loads(CATALOG.read_text(encoding="utf-8"))
    malformed["commit"] = ""
    path = tmp_path / "bad.json"
    path.write_text(json.dumps(malformed), encoding="utf-8")
    with pytest.raises(ValueError):
        build_catalog_receipt(path)
