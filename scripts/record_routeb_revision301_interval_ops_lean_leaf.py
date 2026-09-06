"""Resume the interval-operations Lean leaf after revisions 299-300."""
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
    if state.revision != 300 or state.registry:
        raise ValueError("revision-301 recorder requires revision 300 and empty registry")
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v254.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v255.json"
    side = ROOT / "artifacts/task_FLT_interval_ops_lean_leaf_20260908"
    lean, olean, receipt, report = (side / n for n in ("FLTIntervalOps.lean", "FLTIntervalOps.olean", "RECEIPT.md", "REPORT.md"))
    if not all(p.is_file() for p in (old, lean, olean, receipt, report)):
        raise ValueError("missing interval-ops Lean leaf")
    source_sha = "a169444c91d0e14008e5abd6e7a9ec80845e91322100edd5f9d3b4f01de6e593"
    olean_sha = "2fa66f548b124d8d34e8a65f552d53b39f4e1df6209f2a48649fbbe55e470aaf"
    if sha(lean) != source_sha or sha(olean) != olean_sha:
        raise ValueError("interval-ops Lean hashes do not match receipt")
    text = receipt.read_text(encoding="utf-8")
    if "Strict compile: exit code `0`" not in text or "no `sorry`, no `admit`, no custom `axiom`" not in text:
        raise ValueError("strict interval-ops receipt markers missing")
    record = {
        "kind": "routeb_abstract_interval_operations_lean_leaf",
        "status": "LEAN_VERIFIED_ABSTRACT_REAL_INTERVAL_OPERATIONS_SOURCE_BINDING_OPEN",
        "evidence_level": "strict-lean-compile-plus-abstract-receipt",
        "files": [ref(lean), ref(olean), ref(receipt), ref(report)],
        "lean_toolchain": "leanprover/lean4:v4.33.1",
        "mathlib_revision": "0df444a360eaa60ab8c11dca51a86af692955474",
        "source_sha256": source_sha,
        "olean_sha256": olean_sha,
        "strict_compile": True,
        "custom_axioms": False,
        "concrete_julia_binding": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph = json.loads(old.read_text(encoding="utf-8"))
    graph.setdefault("bottleneck_audits", []).append(record)
    graph.setdefault("external_intakes", []).append(record)
    graph.setdefault("open_frontier_updates", []).append({
        "node": "B45.rounding",
        "status": "abstract_interval_ops_verified",
        "reason": "Exact-real interval arithmetic and square interfaces compile in Lean; concrete Julia rounding/source semantics remain open.",
    })
    graph.update(schema="routeb-proposed-proof-dag-v255", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260908/state-before-revision301.json"
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision301_interval_ops_lean_leaf/v1",
        "graph_sha256": digest,
        "roots": [],
        "selected_nodes": [],
        "source": str(side),
        "evidence_sha256": sha(receipt),
        "strict_compile": True,
        "abstract_only": True,
        "concrete_julia_binding": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision301_interval_ops_lean_leaf_recorded",
        proposed_dag=ref(new),
        proposed_dag_sha256=digest,
        strict_compile=True,
        abstract_only=True,
        concrete_julia_binding=False,
        registry_promoted=False,
        formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name, "registry": len(state.registry)}))


if __name__ == "__main__":
    main()
