from percolation_workflow.disjoint import (
    audit_do, build_repair_do, canonical_do_schema, classify_manual_review, do_sha256,
    normalize_do_path,
)


def test_do_helpers_are_deterministic_and_canonical():
    assert normalize_do_path("receipts\\x.json") is None
    assert normalize_do_path("receipts/x.json") == "receipts/x.json"
    raw = {"schema_version": 1, "path": "receipts/x.json", "kind": "repair"}
    value = {**raw, "sha256": do_sha256(raw)}
    assert canonical_do_schema(value)["path"] == "receipts/x.json"
    assert classify_manual_review(value) is None
    assert audit_do(value) == {
        "schema_version": 1, "path": "receipts/x.json",
        "sha256": do_sha256(value), "manual_review": None, "ok": True,
    }


def test_do_manual_review_categories_are_narrow():
    assert classify_manual_review({"schema_version": 2, "path": "x"}) == "schema_mismatch"
    assert classify_manual_review({"schema_version": 1, "path": "../x"}) == "unsafe_path"
    assert classify_manual_review({"schema_version": 1, "path": "x", "sha256": "bad"}) == "hash_mismatch"


def test_repair_do_is_a_valid_disjoint_projection():
    value = build_repair_do("receipts/x.json")
    assert audit_do(value)["ok"] is True
    assert value["kind"] == "repair"


def test_do_envelope_rejects_unknown_fields_fail_closed():
    value = build_repair_do("receipts/x.json")
    value["untrusted"] = "must not be admitted"
    value["sha256"] = do_sha256({key: item for key, item in value.items() if key != "sha256"})
    assert canonical_do_schema(value) is None
    assert classify_manual_review(value) == "invalid_schema"
    assert audit_do(value)["ok"] is False
