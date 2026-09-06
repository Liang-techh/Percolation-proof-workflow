"""Fail-closed validation for adaptive Route-B coverage receipts.

This module validates partition accounting only.  It does not certify interval
arithmetic, DH semantics, residual absorption, or theorem truth.  A complete
coverage claim additionally requires an external dynamics checker and remains
separate from the Lean verified-theorem registry.
"""
from __future__ import annotations

from fractions import Fraction
from typing import Any, Mapping


SCHEMA = "routeb-coverage-receipt-v1"
CANONICAL_SCHEMA = "routeB.interval.coverage_receipt.v1"
DIMENSIONS = 13
UNKNOWN_PREFIXES = ("UNKNOWN", "ERROR")
KNOWN_LEAF_CLASSIFICATIONS = frozenset({
    "BOX_BRACKET_LOWER_NONNEGATIVE",
    "BOX_BRACKET_STRICTLY_NEGATIVE",
    "OUTSIDE_DOMAIN",
    "UNKNOWN_BRACKET",
    "UNKNOWN_DOMAIN_BOUNDARY",
    "UNKNOWN_INVERSE",
    "INVERSE_GUARD_RESOLVED",
    "ERROR_DRIVER_EXCEPTION",
})


class CoverageReceiptError(ValueError):
    """Raised when a coverage receipt cannot be trusted structurally."""


def _fraction(value: Any, field: str) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, (str, int, Fraction)):
        raise CoverageReceiptError(f"{field} must be an exact rational string")
    try:
        return Fraction(value)
    except (TypeError, ValueError, ZeroDivisionError) as exc:
        raise CoverageReceiptError(f"{field} is not an exact rational") from exc


def _vector(node: Mapping[str, Any], key: str) -> tuple[Fraction, ...]:
    values = node.get(key)
    if not isinstance(values, list) or len(values) != DIMENSIONS:
        raise CoverageReceiptError(f"{key} must contain exactly {DIMENSIONS} endpoints")
    result = tuple(_fraction(value, f"{key}[{i}]") for i, value in enumerate(values))
    if any(lo > hi for lo, hi in zip(result, _vector_hi(node, key))):
        raise CoverageReceiptError(f"{key} contains an invalid interval")
    return result


def _vector_hi(node: Mapping[str, Any], key: str) -> tuple[Fraction, ...]:
    # key is box_lo/raw_box_lo; keep the companion lookup explicit so malformed
    # receipts fail with a controlled error rather than a KeyError.
    companion = key[:-2] + "hi" if key.endswith("lo") else None
    values = node.get(companion) if companion else None
    if not isinstance(values, list) or len(values) != DIMENSIONS:
        raise CoverageReceiptError(f"{companion or key} must contain exactly {DIMENSIONS} endpoints")
    return tuple(_fraction(value, f"{companion}[{i}]") for i, value in enumerate(values))


def _box(node: Mapping[str, Any], prefix: str = "") -> tuple[tuple[Fraction, ...], tuple[Fraction, ...]]:
    lo = _vector(node, prefix + "box_lo")
    hi = _vector_hi(node, prefix + "box_lo")
    if any(a > b for a, b in zip(lo, hi)):
        raise CoverageReceiptError(f"{prefix}box has lo > hi")
    return lo, hi


def _ids(values: Any, field: str) -> list[int]:
    if not isinstance(values, list) or any(isinstance(x, bool) or not isinstance(x, int) for x in values):
        raise CoverageReceiptError(f"{field} must be a list of integer ids")
    if len(set(values)) != len(values):
        raise CoverageReceiptError(f"{field} contains duplicate ids")
    return values


def _source_hashes(value: Any) -> None:
    if isinstance(value, Mapping):
        values = list(value.values())
    elif isinstance(value, list):
        if any(not isinstance(item, Mapping) for item in value):
            raise CoverageReceiptError("source_hashes list entries must be objects")
        values = [item.get("sha256") for item in value]
    else:
        raise CoverageReceiptError("source_hashes must be an object or list")
    if isinstance(value, Mapping):
        values = [x.get("sha256") if isinstance(x, Mapping) else x for x in value.values()]
    if not values or any(not isinstance(x, str) or len(x) != 64 or any(c not in "0123456789abcdefABCDEF" for c in x) for x in values):
        raise CoverageReceiptError("source_hashes must contain sha256 values")


def _normalize_canonical(document: Mapping[str, Any]) -> Mapping[str, Any]:
    """Normalize the Julia exporter schema without weakening its fail-closed gates."""
    if document.get("schema") != CANONICAL_SCHEMA:
        return document
    raw_nodes = document.get("nodes")
    if not isinstance(raw_nodes, list) or not raw_nodes:
        raise CoverageReceiptError("canonical receipt nodes must be a nonempty list")
    normalized_nodes: list[dict[str, Any]] = []
    for source in raw_nodes:
        if not isinstance(source, Mapping):
            raise CoverageReceiptError("canonical receipt node is not an object")
        raw_lo, raw_hi = source.get("raw_lo"), source.get("raw_hi")
        effective_lo, effective_hi = source.get("effective_lo"), source.get("effective_hi")
        effective_values = (effective_lo, effective_hi)
        all_effective_null = (isinstance(effective_lo, list)
                              and isinstance(effective_hi, list)
                              and len(effective_lo) == DIMENSIONS
                              and len(effective_hi) == DIMENSIONS
                              and all(x is None for x in effective_lo + effective_hi))
        effective_present = any(value is not None for value in effective_values) and not all_effective_null
        if effective_present:
            if (not isinstance(effective_lo, list) or not isinstance(effective_hi, list)
                    or len(effective_lo) != DIMENSIONS or len(effective_hi) != DIMENSIONS
                    or any(x is None for x in effective_lo + effective_hi)):
                raise CoverageReceiptError("canonical effective box must have 13 rational endpoints")
        use_effective = effective_present
        state = ("discarded" if source.get("discarded") is True else
                 "pending" if source.get("pending") is True else
                 "expanded" if source.get("children") else "leaf")
        normalized_nodes.append({
            "id": source.get("id"), "parent": source.get("parent"),
            "depth": source.get("depth"),
            "box_lo": effective_lo if use_effective else raw_lo,
            "box_hi": effective_hi if use_effective else raw_hi,
            "raw_box_lo": raw_lo, "raw_box_hi": raw_hi,
            "state": state,
            "split_axis_index": source.get("split_index"),
            "cut": source.get("split_cut"),
            "children": source.get("children", []),
            "leaf_classification": (source.get("leaf_classification")
                                     if state == "leaf" else None),
        })
    root = normalized_nodes[0]
    source_hashes = document.get("source_hashes")
    return {
        "schema": SCHEMA,
        "source_hashes": source_hashes,
        "root_box": {"lo": root.get("raw_box_lo"), "hi": root.get("raw_box_hi")},
        "run": {"coordinate_order": document.get("dimension_order", [])},
        "nodes": normalized_nodes,
        "pending_ids": document.get("pending", []),
        "discarded_ids": document.get("discarded", []),
        "summary": {"coverage_complete": document.get("coverage_complete") is True},
    }


def validate_coverage_receipt(document: Mapping[str, Any]) -> dict[str, Any]:
    """Validate a routeb-coverage-receipt-v1 tree and return safe summary data."""
    if not isinstance(document, Mapping):
        raise CoverageReceiptError("receipt must be an object")
    document = _normalize_canonical(document)
    schema = document.get("schema", document.get("schema_version"))
    if schema != SCHEMA:
        raise CoverageReceiptError(f"unsupported schema: {schema!r}")
    run = document.get("run", {})
    if run:
        if not isinstance(run, Mapping):
            raise CoverageReceiptError("run must be an object")
        coordinate_order = run.get("coordinate_order")
        if coordinate_order is not None and (
                not isinstance(coordinate_order, list)
                or len(coordinate_order) != DIMENSIONS):
            raise CoverageReceiptError("run coordinate_order must be a list with 13 entries")
    _source_hashes(document.get("source_hashes"))
    root = document.get("root_box")
    if not isinstance(root, Mapping):
        raise CoverageReceiptError("root_box is missing")
    root_lo = root.get("lo", []); root_hi = root.get("hi", [])
    if not isinstance(root_lo, list) or not isinstance(root_hi, list):
        raise CoverageReceiptError("root_box lo/hi must be lists")
    if len(root_lo) != DIMENSIONS or len(root_hi) != DIMENSIONS:
        raise CoverageReceiptError("root_box must have 13 lo/hi endpoints")
    root_lo_f = tuple(_fraction(x, f"root_box.lo[{i}]") for i, x in enumerate(root_lo))
    root_hi_f = tuple(_fraction(x, f"root_box.hi[{i}]") for i, x in enumerate(root_hi))
    if any(a > b for a, b in zip(root_lo_f, root_hi_f)):
        raise CoverageReceiptError("root_box has lo > hi")

    raw_nodes = document.get("nodes")
    if not isinstance(raw_nodes, list) or not raw_nodes:
        raise CoverageReceiptError("nodes must be a nonempty list")
    nodes: dict[int, Mapping[str, Any]] = {}
    for index, node in enumerate(raw_nodes):
        if not isinstance(node, Mapping):
            raise CoverageReceiptError(f"node {index} is not an object")
        node_id = node.get("id")
        if isinstance(node_id, bool) or not isinstance(node_id, int) or node_id <= 0:
            raise CoverageReceiptError(f"node {index} has invalid id")
        if node_id in nodes:
            raise CoverageReceiptError(f"duplicate node id {node_id}")
        effective_box = _box(node)
        raw_box = _box(node, "raw_")
        if any(effective_box[0][i] < raw_box[0][i] or effective_box[1][i] > raw_box[1][i]
               for i in range(DIMENSIONS)):
            raise CoverageReceiptError(f"node {node_id} effective box escapes raw box")
        parent = node.get("parent")
        if isinstance(parent, bool) or not isinstance(parent, int) or parent < 0:
            raise CoverageReceiptError(f"node {node_id} has invalid parent")
        depth = node.get("depth")
        if isinstance(depth, bool) or not isinstance(depth, int) or depth < 0:
            raise CoverageReceiptError(f"node {node_id} has invalid depth")
        nodes[node_id] = node
    if 1 not in nodes or nodes[1].get("parent") != 0:
        raise CoverageReceiptError("root node id 1 with parent 0 is required")
    if tuple(_fraction(x, "node[1].box_lo") for x in nodes[1]["box_lo"]) != root_lo_f or tuple(_fraction(x, "node[1].box_hi") for x in nodes[1]["box_hi"]) != root_hi_f:
        raise CoverageReceiptError("node 1 does not equal root_box")

    referenced: set[int] = set()
    leaf_ids: set[int] = set()
    for node_id, node in nodes.items():
        state = node.get("state")
        children = _ids(node.get("children", []), f"node {node_id}.children")
        if state == "expanded":
            axis_value = node.get("split_axis_index")
            if (len(children) != 2 or isinstance(axis_value, bool)
                    or not isinstance(axis_value, int) or axis_value not in range(DIMENSIONS)):
                raise CoverageReceiptError(f"expanded node {node_id} must have two children and a valid axis")
            cut = _fraction(node.get("cut"), f"node {node_id}.cut")
            axis = axis_value
            parent_lo, parent_hi = _box(node)
            child_boxes = []
            for child_id in children:
                if child_id not in nodes:
                    raise CoverageReceiptError(f"node {node_id} references missing child {child_id}")
                child = nodes[child_id]
                if child.get("parent") != node_id:
                    raise CoverageReceiptError(f"child {child_id} has wrong parent")
                if child.get("depth") != node.get("depth") + 1:
                    raise CoverageReceiptError(f"child {child_id} has wrong depth")
                child_boxes.append(_box(child))
                referenced.add(child_id)
            left, right = child_boxes
            def orientation_ok(low, high):
                if low[0][axis] != parent_lo[axis] or low[1][axis] != cut:
                    return False
                if high[0][axis] != cut or high[1][axis] != parent_hi[axis]:
                    return False
                return all(i == axis or (
                    low[0][i] == parent_lo[i] and low[1][i] == parent_hi[i] and
                    high[0][i] == parent_lo[i] and high[1][i] == parent_hi[i])
                           for i in range(DIMENSIONS))
            if not (orientation_ok(left, right) or orientation_ok(right, left)):
                raise CoverageReceiptError(f"children of {node_id} do not cover the parent at the cut")
        elif state == "leaf":
            if children:
                raise CoverageReceiptError(f"leaf {node_id} cannot have children")
            if not isinstance(node.get("leaf_classification"), str) or not node["leaf_classification"]:
                raise CoverageReceiptError(f"leaf {node_id} is missing classification")
            leaf_classification = node.get("leaf_classification")
            if leaf_classification not in KNOWN_LEAF_CLASSIFICATIONS:
                raise CoverageReceiptError(f"leaf {node_id} has unknown classification")
            leaf_ids.add(node_id)
        elif state in {"pending", "discarded"}:
            if children:
                raise CoverageReceiptError(f"{state} node {node_id} cannot have children")
            if node.get("leaf_classification") is not None:
                raise CoverageReceiptError(f"{state} node {node_id} cannot have leaf classification")
        else:
            raise CoverageReceiptError(f"node {node_id} has unknown state {state!r}")
    if referenced | {1} != set(nodes):
        raise CoverageReceiptError("node tree is disconnected or has unreferenced nodes")
    pending = set(_ids(document.get("pending_ids", []), "pending_ids"))
    discarded = set(_ids(document.get("discarded_ids", []), "discarded_ids"))
    state_pending = {node_id for node_id, node in nodes.items() if node.get("state") == "pending"}
    state_discarded = {node_id for node_id, node in nodes.items() if node.get("state") == "discarded"}
    if (pending != state_pending or discarded != state_discarded
            or not pending <= set(nodes) or not discarded <= set(nodes) or pending & discarded):
        raise CoverageReceiptError("pending/discarded ids are inconsistent")
    summary = document.get("summary", {})
    if not isinstance(summary, Mapping):
        raise CoverageReceiptError("summary must be an object")
    claim = document.get("claim", summary.get("claim"))
    complete = claim == "dynamics_partition_complete" or summary.get("coverage_complete") is True
    if complete:
        if pending or discarded:
            raise CoverageReceiptError("complete claim cannot contain pending/discarded nodes")
        if any(any(node_id in leaf_ids and node["leaf_classification"].startswith(prefix) for prefix in UNKNOWN_PREFIXES) for node_id, node in nodes.items()):
            raise CoverageReceiptError("complete claim contains unknown/error leaf")
    return {
        "schema": SCHEMA,
        "node_count": len(nodes),
        "leaf_count": len(leaf_ids),
        "pending_count": len(pending),
        "discarded_count": len(discarded),
        "structurally_closed": not pending and not discarded,
        "complete_claim": complete,
    }


__all__ = ["CoverageReceiptError", "SCHEMA", "validate_coverage_receipt"]
