"""Read-only validation for installing proposed theorem children into a DAG.

The migrator deliberately returns a plan and an audit report instead of a
WorkflowState.  Callers can inspect the plan, but there is no save/write path
to the workflow checkpoint or theorem registry.
"""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any

from .model import NodeStatus


class DryRunError(ValueError):
    """A proposal is malformed or cannot be safely attached to this snapshot."""


def _check(name: str, passed: bool, detail: str, checks: list[dict[str, Any]]) -> None:
    checks.append({"name": name, "status": "pass" if passed else "fail", "detail": detail})


def _acyclic(edges: dict[str, list[str]]) -> tuple[bool, list[str]]:
    visiting: set[str] = set()
    visited: set[str] = set()
    trail: list[str] = []

    def visit(node: str) -> bool:
        if node in visiting:
            trail.append(node)
            return False
        if node in visited:
            return True
        visiting.add(node)
        for child in edges.get(node, []):
            if not visit(child):
                trail.append(node)
                return False
        visiting.remove(node)
        visited.add(node)
        return True

    for node in edges:
        if node not in visited and not visit(node):
            return False, list(reversed(trail))
    return True, []


def dry_run_migrate(state_path: str | Path, proposal_path: str | Path) -> dict[str, Any]:
    """Validate a proposed child patch against an exact state byte snapshot.

    The returned ``plan`` is an in-memory, non-persisted view of the edges that
    would be added.  The input files are opened read-only and never replaced.
    """
    state_path, proposal_path = Path(state_path), Path(proposal_path)
    state_bytes = state_path.read_bytes()
    state = json.loads(state_bytes.decode("utf-8"))
    proposal = json.loads(proposal_path.read_text(encoding="utf-8"))
    checks: list[dict[str, Any]] = []
    failures: list[str] = []

    def require(name: str, condition: bool, detail: str) -> None:
        _check(name, condition, detail, checks)
        if not condition:
            failures.append(name)

    require("schema", proposal.get("schema") == "routeb-entry-dag-proposed-patch-v1",
            "recognized proposal schema")
    require("mutation_guard", proposal.get("mode") == "proposal_only" and
            proposal.get("state_mutation") is False,
            "proposal declares proposal_only and state_mutation=false")
    snapshot = proposal.get("snapshot", {})
    actual_hash = hashlib.sha256(state_bytes).hexdigest()
    require("snapshot_revision", snapshot.get("revision") == state.get("revision"),
            f"proposal={snapshot.get('revision')!r}, state={state.get('revision')!r}")
    require("snapshot_root", snapshot.get("root_id") == state.get("root_id"),
            "proposal root matches state root")
    require("snapshot_hash", snapshot.get("state_sha256") == actual_hash,
            f"proposal={snapshot.get('state_sha256')!r}, actual={actual_hash}")

    existing = state.get("nodes", {})
    proposed = proposal.get("nodes", [])
    ids = [node.get("id") for node in proposed if isinstance(node, dict)]
    names = [node.get("name") for node in proposed if isinstance(node, dict)]
    layers = [node.get("metadata", {}).get("entry_contract_layer")
              for node in proposed if isinstance(node, dict)]
    require("unique_proposed_ids", len(ids) == len(set(ids)), "no duplicate proposed IDs")
    require("no_id_overwrite", not (set(existing) & set(ids)), "no proposed ID exists in state")
    existing_names = {node.get("name") for node in existing.values()}
    require("unique_names", len(names) == len(set(names)) and not (set(names) & existing_names),
            "no duplicate or existing theorem names")
    require("complete_layers", set(layers) == {f"L{i}" for i in range(7)} and len(layers) == 7,
            "exactly one proposed child for each L0-L6")

    all_ids = set(existing) | set(ids)
    edges = {node_id: [] for node_id in all_ids}
    parent_edges: list[dict[str, str]] = []
    for node in proposed:
        if not isinstance(node, dict):
            failures.append("node_shape")
            continue
        node_id = node.get("id")
        metadata = node.get("metadata")
        deps = node.get("dependencies")
        parent = node.get("parent_id")
        good_shape = (isinstance(node_id, str) and isinstance(metadata, dict) and
                      isinstance(deps, list) and len(deps) == len(set(deps)))
        require(f"node_shape:{node_id}", good_shape, "ID, metadata, and unique dependency list")
        if not good_shape:
            continue
        require(f"parent:{node_id}", parent in existing,
                "parent is an existing node; installation cannot invent/reparent the spine")
        require(f"dependencies:{node_id}", all(dep in all_ids and dep != node_id for dep in deps),
                "all dependencies resolve in the combined graph and no self-edge")
        require(f"open:{node_id}", node.get("status") == NodeStatus.OPEN.value,
                "proposed children enter only as open nodes")
        require(f"registry_fail_closed:{node_id}", metadata.get("registry_eligible") is False,
                "proposed child is not registry eligible")
        require(f"evidence_level:{node_id}", isinstance(metadata.get("evidence_level"), str) and
                bool(metadata["evidence_level"].strip()),
                "evidence level is explicitly labelled; registry eligibility remains separate")
        require(f"no_receipt:{node_id}", not node.get("verified_artifact") and
                not node.get("attempts"), "proposal carries no verification/attempt state")
        if parent in existing:
            parent_edges.append({"child_id": node_id, "parent_id": parent})
            edges[parent].append(node_id)
        for dep in deps:
            if dep in edges:
                edges[dep].append(node_id)

    acyclic, cycle = _acyclic(edges)
    require("combined_acyclic", acyclic, "combined prerequisite-to-dependent graph is acyclic" +
            (f": {' -> '.join(cycle)}" if cycle else ""))

    parent_ids = sorted({edge["parent_id"] for edge in parent_edges})
    parent_report = []
    for parent_id in parent_ids:
        parent = existing[parent_id]
        status = parent.get("status")
        in_registry = parent_id in state.get("registry", {})
        can_attach = status != NodeStatus.VERIFIED.value and not in_registry
        require(f"parent_open:{parent_id}", can_attach,
                "parent is not verified and has no registry receipt")
        parent_report.append({"parent_id": parent_id, "name": parent.get("name"),
                              "status_before": status,
                              "registry_before": in_registry,
                              "closure_gate": "blocked_by_open_proposed_children"})

    # This is the only simulated mutation: a deep copy used solely to expose
    # the prospective edge delta.  It is never saved and never returned as state.
    simulated = copy.deepcopy(existing)
    for edge in parent_edges:
        deps = simulated[edge["parent_id"]].setdefault("dependencies", [])
        if edge["child_id"] not in deps:
            deps.append(edge["child_id"])
    plan = {"add_nodes": proposed, "add_parent_edges": parent_edges,
            "parent_closure": parent_report, "registry_delta": {"add": [], "remove": []}}
    state_unchanged = hashlib.sha256(state_path.read_bytes()).hexdigest() == actual_hash
    require("state_read_only", state_unchanged, "state bytes unchanged after dry-run")
    require("registry_unchanged", plan["registry_delta"] == {"add": [], "remove": []},
            "registry has no simulated additions or removals")
    return {
        "schema": "theorem-dag-dry-run-migration-report-v1",
        "mode": "dry_run",
        "safe_to_install": not failures,
        "input": {"state_path": str(state_path), "proposal_path": str(proposal_path),
                   "state_revision": state.get("revision"), "state_sha256": actual_hash,
                   "proposal_sha256": hashlib.sha256(proposal_path.read_bytes()).hexdigest()},
        "checks": checks,
        "failures": failures,
        "plan": plan,
        "invariants": {"state_mutated": False, "registry_mutated": False,
                        "existing_node_count": len(existing),
                        "proposed_node_count": len(proposed),
                        "simulated_node_count": len(simulated) + len(proposed)},
    }
