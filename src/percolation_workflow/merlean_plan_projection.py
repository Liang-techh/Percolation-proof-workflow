"""Pure-Python, read-only projection compatible with MerLean plan-store views.

This module deliberately does not implement a store.  ``WorkflowState`` remains
the authority for scheduling, evidence, and registry admission; the records
here are deterministic export views for dashboards, inspection, and interop.
"""
from __future__ import annotations

import json
import hashlib
from collections import defaultdict, deque
from pathlib import Path
from typing import Any, Iterable

from .model import EvidenceStage, NodeStatus, ProofNode, WorkflowState


SCHEMA_VERSION = 1
UPSTREAM = {
    "project": "MerLean",
    "repository": "https://github.com/MerLeanProver/MerLean",
    "adapted_paths": ["src/plan_store/store.py", "src/plan_store/lean_sync.py"],
    "license_note": "See upstream repository NOTICE; no upstream code is copied here.",
}


def _status(node: ProofNode, state: WorkflowState) -> tuple[str, str]:
    """Return conservative external status and explicit admission status."""
    stage = state.evidence_stage(node.id).value
    admitted = (node.status == NodeStatus.VERIFIED and node.id in state.registry and
                stage in {EvidenceStage.LEAN_VERIFIED.value, EvidenceStage.GLOBAL_CLOSED.value})
    if admitted:
        return "completed", "verified"
    if stage == EvidenceStage.COMPILED_CANDIDATE.value:
        return "pending", "compiled_candidate"
    if node.status == NodeStatus.IN_PROGRESS:
        return "in_progress", "pending"
    return "pending", "pending"


def _graph(state: WorkflowState) -> tuple[dict[str, set[str]], dict[str, set[str]]]:
    nodes = {
        node_id: set(node.dependencies) |
        set(node.metadata.get("required_node_ids", []))
        for node_id, node in state.nodes.items()
    }
    for node_id, deps in nodes.items():
        unknown = deps - nodes.keys()
        if unknown:
            raise ValueError(f"node {node_id} has unknown dependencies: {sorted(unknown)}")
    reverse = {node_id: set() for node_id in nodes}
    for parent, deps in nodes.items():
        for child in deps:
            reverse[child].add(parent)
    return nodes, reverse


def topo_order(state: WorkflowState) -> list[str]:
    """Return prerequisite-first deterministic order; reject cycles."""
    deps, reverse = _graph(state)
    indegree = {node_id: len(children) for node_id, children in deps.items()}
    ready = deque(sorted(node_id for node_id, count in indegree.items() if count == 0))
    result: list[str] = []
    while ready:
        node_id = ready.popleft()
        result.append(node_id)
        for parent in sorted(reverse[node_id]):
            indegree[parent] -= 1
            if indegree[parent] == 0:
                ready.append(parent)
        ready = deque(sorted(ready))
    if len(result) != len(deps):
        raise ValueError(f"workflow graph contains a cycle: {cycles(state)}")
    return result


def levels(state: WorkflowState) -> dict[str, int]:
    """Assign leaves level 0 and parents one above their deepest prerequisite."""
    return _levels(state)


def _levels(state: WorkflowState) -> dict[str, int]:
    deps, _ = _graph(state)
    result: dict[str, int] = {}
    for node_id in topo_order(state):
        result[node_id] = max((result[child] + 1 for child in sorted(deps[node_id])), default=0)
    return result


def forward_cone(state: WorkflowState, node_id: str) -> list[str]:
    """Return deterministic downstream dependents of ``node_id`` (excluding it)."""
    _, reverse = _graph(state)
    if node_id not in reverse:
        raise KeyError(node_id)
    seen: set[str] = set()
    queue = deque(sorted(reverse[node_id]))
    while queue:
        current = queue.popleft()
        if current in seen:
            continue
        seen.add(current)
        queue.extend(sorted(reverse[current]))
    return sorted(seen)


def cycles(state: WorkflowState) -> list[list[str]]:
    """Return deterministic cycle components, without mutating or validating state."""
    deps, _ = _graph(state)
    index = 0
    stack: list[str] = []
    on_stack: set[str] = set()
    indices: dict[str, int] = {}
    low: dict[str, int] = {}
    components: list[list[str]] = []

    def visit(node_id: str) -> None:
        nonlocal index
        indices[node_id] = low[node_id] = index
        index += 1
        stack.append(node_id); on_stack.add(node_id)
        for child in sorted(deps[node_id]):
            if child not in indices:
                visit(child); low[node_id] = min(low[node_id], low[child])
            elif child in on_stack:
                low[node_id] = min(low[node_id], indices[child])
        if low[node_id] == indices[node_id]:
            component: list[str] = []
            while True:
                item = stack.pop(); on_stack.remove(item); component.append(item)
                if item == node_id: break
            if len(component) > 1 or node_id in deps[node_id]:
                components.append(sorted(component))

    for node_id in sorted(deps):
        if node_id not in indices: visit(node_id)
    return sorted(components)


def project(state: WorkflowState, *, provenance: dict[str, Any] | None = None) -> dict[str, Any]:
    """Build formal nodes plus excluded Note/Summary records from a snapshot."""
    order = topo_order(state)
    node_levels = _levels(state)
    formal: list[dict[str, Any]] = []
    notes: list[dict[str, Any]] = []
    for position, node_id in enumerate(order):
        node = state.nodes[node_id]
        external_status, admission = _status(node, state)
        stage = state.evidence_stage(node_id).value
        metadata = dict(node.metadata)
        node_provenance = metadata.pop("provenance", None)
        required_node_ids = metadata.get("required_node_ids", [])
        required_input_registry_refs = {}
        for required_id in sorted(required_node_ids):
            required_node = state.nodes[required_id]
            entry = state.registry.get(required_id)
            required_input_registry_refs[required_id] = {
                "name": required_node.name,
                "statement_sha256": hashlib.sha256(
                    required_node.statement.encode("utf-8")).hexdigest(),
                "status": "verified_registry" if entry is not None else "missing",
                "artifact": entry.get("artifact") if isinstance(entry, dict) else None,
            }
        formal.append({
            "statement_id": node.id, "type": "Theorem", "name": node.name,
            "content": node.statement, "dependencies": sorted(node.dependencies),
            "required_node_ids": sorted(required_node_ids),
            "required_input_registry_refs": required_input_registry_refs,
            "dependents": forward_cone(state, node.id), "proof": node.verified_artifact,
            "proof_sketch": node.proof_sketch, "lean_path": metadata.get("lean_path"),
            "hierarchy_level": node_levels[node.id], "order": position,
            "workflow_status": node.status.value, "evidence_stage": stage,
            "status": external_status, "admission_status": admission,
            "attempts": list(node.attempts), "metadata": metadata,
        })
        if node.proof_sketch:
            notes.append({"statement_id": node.id, "type": "Note", "content": node.proof_sketch,
                          "excluded_from_graph": True, "source": "WorkflowState.proof_sketch"})
        if node_provenance is not None:
            notes.append({"statement_id": node.id, "type": "Note", "content": node_provenance,
                          "excluded_from_graph": True, "source": "WorkflowState.metadata.provenance"})
    notes.append({"statement_id": state.root_id, "type": "Summary",
                  "content": {"project": state.project, "root_id": state.root_id,
                              "revision": state.revision, "frontier": [n.id for n in state.frontier()]},
                  "excluded_from_graph": True, "source": "WorkflowState"})
    return {"schema_version": SCHEMA_VERSION, "project": state.project,
            "revision": state.revision, "root_id": state.root_id,
            "statements": formal, "notes": notes,
            "provenance": {**UPSTREAM, **(provenance or {})}}


def export_views(state: WorkflowState, directory: str | Path, *, provenance: dict[str, Any] | None = None) -> dict[str, Path]:
    """Write disjoint deterministic MerLean-style derived JSON views."""
    view = project(state, provenance=provenance)
    target = Path(directory); target.mkdir(parents=True, exist_ok=True)
    statements = {"schema_version": SCHEMA_VERSION, "project": view["project"],
                  "statements": view["statements"], "provenance": view["provenance"]}
    progress = {"schema_version": SCHEMA_VERSION, "project": view["project"],
                "revision": view["revision"], "root_id": view["root_id"],
                "statements": [{"statement_id": row["statement_id"], "status": row["status"],
                                "workflow_status": row["workflow_status"],
                                "evidence_stage": row["evidence_stage"],
                                "admission_status": row["admission_status"]} for row in view["statements"]]}
    analytics = {"schema_version": SCHEMA_VERSION, "project": view["project"],
                 "node_count": len(view["statements"]), "note_count": len(view["notes"]),
                 "topo_order": [row["statement_id"] for row in view["statements"]],
                 "levels": {row["statement_id"]: row["hierarchy_level"] for row in view["statements"]},
                 "frontier": [n.id for n in state.frontier()], "cycles": cycles(state),
                 "provenance": view["provenance"]}
    payloads = {"statements.json": statements, "progress.json": progress, "analytics.json": analytics}
    paths: dict[str, Path] = {}
    for filename, payload in payloads.items():
        path = target / filename
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        paths[filename] = path
    return paths
