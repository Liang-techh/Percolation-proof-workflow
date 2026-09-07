from __future__ import annotations

import pytest
import hashlib

from percolation_workflow.coverage_receipt import (
    CoverageReceiptError,
    validate_canonical_coverage_triple,
    validate_coverage_receipt,
    validate_theta2_external_premises,
)


H = "a" * 64


def _node(node_id, parent, lo, hi, state, *, children=None, axis=None, cut=None, classification=None):
    return {
        "id": node_id,
        "parent": parent,
        "depth": 0 if node_id == 1 else 1,
        "box_lo": list(lo),
        "box_hi": list(hi),
        "raw_box_lo": list(lo),
        "raw_box_hi": list(hi),
        "state": state,
        "split_axis_index": axis,
        "cut": cut,
        "children": list(children or []),
        "leaf_classification": classification,
    }


def valid_receipt():
    root_lo = ["-1"] * 13
    root_hi = ["1"] * 13
    left_hi = root_hi.copy(); left_hi[0] = "0"
    right_lo = root_lo.copy(); right_lo[0] = "0"
    return {
        "schema": "routeb-coverage-receipt-v1",
        "source_hashes": {"driver": H},
        "root_box": {"lo": root_lo, "hi": root_hi},
        "nodes": [
            _node(1, 0, root_lo, root_hi, "expanded", children=[2, 3], axis=0, cut="0"),
            _node(2, 1, root_lo, left_hi, "leaf", classification="BOX_BRACKET_LOWER_NONNEGATIVE"),
            _node(3, 1, right_lo, root_hi, "leaf", classification="UNKNOWN_BRACKET"),
        ],
        "pending_ids": [],
        "discarded_ids": [],
        "claim": "geometry_only",
    }


def test_valid_tree_receipt_is_structurally_closed():
    summary = validate_coverage_receipt(valid_receipt())
    assert summary == {
        "schema": "routeb-coverage-receipt-v1",
        "node_count": 3,
        "leaf_count": 2,
        "pending_count": 0,
        "discarded_count": 0,
        "structurally_closed": True,
        "complete_claim": False,
    }


@pytest.mark.parametrize("mutation", ["cut", "missing_child", "complete_pending", "raw_shape"])
def test_receipt_fail_closed(mutation):
    doc = valid_receipt()
    if mutation == "cut":
        doc["nodes"][1]["box_hi"][0] = "1/2"
    elif mutation == "missing_child":
        doc["nodes"][0]["children"] = [2, 99]
    elif mutation == "complete_pending":
        doc["claim"] = "dynamics_partition_complete"
        doc["pending_ids"] = [3]
    else:
        doc["nodes"][2]["raw_box_hi"] = ["1"] * 12
    with pytest.raises(CoverageReceiptError):
        validate_coverage_receipt(doc)


@pytest.mark.parametrize("coordinate_order", ["q1", tuple(f"q{i}" for i in range(13))])
def test_run_coordinate_order_must_be_a_json_list(coordinate_order):
    doc = valid_receipt()
    doc["run"] = {"coordinate_order": coordinate_order}
    with pytest.raises(CoverageReceiptError, match="coordinate_order"):
        validate_coverage_receipt(doc)


def test_run_must_be_an_object():
    doc = valid_receipt()
    doc["run"] = "not-an-object"
    with pytest.raises(CoverageReceiptError, match="run must be an object"):
        validate_coverage_receipt(doc)


def test_pending_state_and_pending_ids_must_match_before_complete_claim():
    doc = valid_receipt()
    doc["nodes"][2]["state"] = "pending"
    doc["nodes"][2]["leaf_classification"] = None
    doc["nodes"][1]["leaf_classification"] = "BOX_BRACKET_LOWER_NONNEGATIVE"
    doc["claim"] = "dynamics_partition_complete"
    with pytest.raises(CoverageReceiptError, match="pending/discarded ids"):
        validate_coverage_receipt(doc)


def test_complete_claim_rejects_unknown_leaf_classification():
    doc = valid_receipt()
    doc["nodes"][2]["leaf_classification"] = "NOT_CERTIFIED"
    doc["claim"] = "dynamics_partition_complete"
    with pytest.raises(CoverageReceiptError, match="unknown classification"):
        validate_coverage_receipt(doc)


def test_mixed_source_hash_list_is_not_partially_accepted():
    doc = valid_receipt()
    doc["source_hashes"] = [{"sha256": H}, 7]
    with pytest.raises(CoverageReceiptError, match="list entries"):
        validate_coverage_receipt(doc)


def test_effective_box_must_remain_inside_raw_box():
    doc = valid_receipt()
    doc["nodes"][1]["raw_box_lo"][0] = "1/4"
    doc["nodes"][1]["raw_box_hi"][0] = "1/2"
    with pytest.raises(CoverageReceiptError, match="escapes raw box"):
        validate_coverage_receipt(doc)


def test_malformed_summary_is_rejected_as_receipt_error():
    doc = valid_receipt()
    doc["summary"] = "bad"
    with pytest.raises(CoverageReceiptError, match="summary must be an object"):
        validate_coverage_receipt(doc)


def test_canonical_partial_effective_box_is_rejected():
    canonical = {
        "schema": "routeB.interval.coverage_receipt.v1",
        "source_hashes": {"driver": H},
        "dimension_order": [f"x{i}" for i in range(13)],
        "coverage_complete": False,
        "pending": [1],
        "discarded": [],
        "nodes": [{
            "id": 1,
            "parent": 0,
            "depth": 0,
            "raw_lo": ["0"] * 13,
            "raw_hi": ["1"] * 13,
            "effective_lo": ["0"] + [None] * 12,
            "effective_hi": [None] * 13,
            "pending": True,
            "discarded": False,
            "children": [],
        }],
    }
    with pytest.raises(CoverageReceiptError, match="effective box"):
        validate_coverage_receipt(canonical)


def canonical_triple():
    order = ["q1", "q2", "q3", "q4", "q5", "q6",
             "dq1", "dq2", "dq3", "dq4", "dq5", "dq6", "w"]
    lo = ["0"] * 13
    hi = ["1"] * 13
    lo[1] = "-3/20"
    hi[1] = "3/20"
    child_hi = hi.copy(); child_hi[0] = "1/2"
    sibling_lo = lo.copy(); sibling_lo[0] = "1/2"
    return {
        "schema": "routeb-theta2-canonical-coverage-v1",
        "coordinate_order": order,
        "namespace": {
            "name": "theta2",
            "anchor": {"coordinate": "q2", "lo": "-3/20", "hi": "3/20"},
        },
        "source": {
            "receipt_sha256": H,
            "generator_sha256": "b" * 64,
            "interval_source_sha256": "c" * 64,
        },
        "parent": {"id": "p", "box_lo": lo, "box_hi": hi},
        "child": {"id": "c", "parent_id": "p", "box_lo": lo, "box_hi": child_hi},
        "sibling": {"id": "s", "parent_id": "p", "box_lo": sibling_lo, "box_hi": hi},
        "linkage": {"split_axis": "q1", "split_cut": "1/2", "adjacency": "shared_face"},
        "source_interval_membership": {"status": "ACCEPTED", "receipt_sha256": "d" * 64},
        "coverage_join": {"kind": "CoverageJoin2", "premise_receipt_sha256": "e" * 64},
    }


def test_canonical_triple_validates_exact_split_and_keeps_theorem_gates_closed():
    summary = validate_canonical_coverage_triple(canonical_triple())
    assert summary["structural_box_subset"] is True
    assert summary["structural_split_cover"] is True
    assert summary["dynamics_interval_membership_proven"] is False
    assert summary["coverage_join_theorem_proven"] is False
    assert summary["formal_certificate_allowed"] is False


@pytest.mark.parametrize("mutation", ["axis", "linkage", "parent", "membership", "hash"])
def test_canonical_triple_fail_closed(mutation):
    doc = canonical_triple()
    if mutation == "axis":
        doc["linkage"]["split_axis"] = "missing"
    elif mutation == "linkage":
        doc["child"]["parent_id"] = "wrong"
    elif mutation == "parent":
        doc["sibling"]["box_lo"][1] = "-1"
    elif mutation == "membership":
        doc["source_interval_membership"]["status"] = "PENDING"
    else:
        doc["coverage_join"]["premise_receipt_sha256"] = "bad"
    with pytest.raises(CoverageReceiptError):
        validate_canonical_coverage_triple(doc)


def external_premises(tmp_path):
    paths = {}
    for name, content in (("triple.json", "triple\n"),
                          ("membership.json", "membership\n"),
                          ("join.json", "join\n")):
        path = tmp_path / name
        path.write_text(content, encoding="utf-8")
        paths[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    return {
        "schema": "routeb-theta2-external-premises-v1",
        "claim_boundary": (
            "source-bound receipt references only; no dynamics theorem, "
            "Float64/libm claim, or CoverageJoin2 proof"
        ),
        "namespace": {
            "name": "theta2",
            "anchor": {"coordinate": "q2", "lo": "-3/20", "hi": "3/20"},
        },
        "triple_ref": {
            "parent_id": "p", "child_id": "c", "sibling_id": "s",
            "triple_receipt_path": "triple.json",
            "triple_receipt_sha256": paths["triple.json"],
        },
        "source_interval_membership": {
            "status": "ACCEPTED", "receipt_path": "membership.json",
            "receipt_sha256": paths["membership.json"],
        },
        "coverage_join": {
            "kind": "CoverageJoin2", "premise_receipt_path": "join.json",
            "premise_receipt_sha256": paths["join.json"],
        },
    }


def test_theta2_external_premises_binds_files_but_not_theorems(tmp_path):
    summary = validate_theta2_external_premises(external_premises(tmp_path), base_dir=tmp_path)
    assert summary["source_interval_membership_receipt_bound"] is True
    assert summary["coverage_join_premise_receipt_bound"] is True
    assert summary["dynamics_interval_membership_proven"] is False
    assert summary["coverage_join_theorem_proven"] is False
    assert summary["formal_certificate_allowed"] is False


@pytest.mark.parametrize("mutation", ["hash", "extra", "status"])
def test_theta2_external_premises_fail_closed(tmp_path, mutation):
    document = external_premises(tmp_path)
    if mutation == "hash":
        document["coverage_join"]["premise_receipt_sha256"] = "a" * 64
    elif mutation == "extra":
        document["coverage_join"]["proof"] = True
    else:
        document["source_interval_membership"]["status"] = "PENDING"
    with pytest.raises(CoverageReceiptError):
        validate_theta2_external_premises(document, base_dir=tmp_path)
