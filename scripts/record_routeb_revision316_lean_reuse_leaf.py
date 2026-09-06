"""Record an abstract, strictly compiled Lean finite-sum reuse leaf."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from record_routeb_port_progress import ROOT, ref
from percolation_workflow.store import StateStore


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    if state.revision != 315 or state.registry:
        raise ValueError("revision-316 recorder requires revision 315 and empty registry")
    side = ROOT / "artifacts/task_routeb_lean_reuse_leaf_current"
    source, report, receipt = (side / n for n in
                               ("RouteBFiniteAggregationLeaf.lean", "REPORT.md", "RECEIPT.json"))
    if not all(p.is_file() for p in (source, report, receipt)):
        raise ValueError("missing Lean reuse leaf evidence")
    check = json.loads(receipt.read_text(encoding="utf-8"))
    if (check.get("status") != "PASS_ABSTRACT_ONLY_NOT_REGISTRY_PROMOTED"
            or check.get("strict_compile", {}).get("command_exit_code") != 0
            or check.get("forbidden_token_scan") != "PASS_NO_SORRY_ADMIT_OR_CUSTOM_AXIOM"
            or check.get("state_registry_guard", {}).get("registry_promoted") is not False):
        raise ValueError("Lean reuse leaf is not a strict abstract-only pass")
    if check.get("lean_toolchain") != "leanprover/lean4:v4.33.1":
        raise ValueError("unexpected Lean toolchain")

    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v269.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v270.json"
    graph = json.loads(old.read_text(encoding="utf-8"))
    record = {
        "kind": "routeb_abstract_lean_reuse_leaf",
        "status": "PASS_ABSTRACT_ONLY_NOT_REGISTRY_PROMOTED",
        "evidence_level": "pinned-lean-zero-sorry-abstract-leaf",
        "candidate": check["candidate"],
        "files": [ref(source), ref(report), ref(receipt)],
        "source_sha256": check["source_sha256"],
        "olean_sha256": check["olean_sha256"],
        "lean_toolchain": check["lean_toolchain"],
        "mathlib_revision": check["mathlib_revision"],
        "strict_compile": True,
        "deployed_source_binding": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph.setdefault("bottleneck_audits", []).append(record)
    graph.setdefault("workflow_hardening", []).append(record)
    graph.setdefault("open_frontier_updates", []).append({
        "node": "B45-1_source_mass_table_exact",
        "status": "abstract_finite_sum_leaf_available_source_premises_open",
        "reason": "pinned Lean verifies finite componentwise sum bounds; Julia/Float64 source premises remain unproved",
        "evidence": ref(receipt),
    })
    graph.update(schema="routeb-proposed-proof-dag-v270", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    checkpoint = ROOT / "artifacts/routeb_storage_checkpoint_20260908/state-before-revision316.json"
    if not checkpoint.exists():
        checkpoint.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, checkpoint)
    graph_sha = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision316_lean_reuse_leaf/v1",
        "graph_sha256": graph_sha, "roots": [], "selected_nodes": [],
        "evidence_sha256": sha(report), "source_sha256": sha(source),
        "receipt_sha256": sha(receipt), "strict_compile": True,
        "abstract_only": True, "deployed_source_binding": False,
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision316_lean_reuse_leaf_recorded",
        proposed_dag=ref(new), proposed_dag_sha256=graph_sha,
        candidate=check["candidate"], strict_compile=True,
        abstract_only=True, deployed_source_binding=False,
        registry_promoted=False, formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name,
                      "registry": len(state.registry),
                      "formal_certificate_allowed": False}))


if __name__ == "__main__":
    main()
