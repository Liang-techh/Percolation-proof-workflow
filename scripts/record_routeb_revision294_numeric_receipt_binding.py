"""Record the cross-artifact numeric receipt binding checker."""
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
    if state.revision != 293 or state.registry:
        raise ValueError("revision-294 recorder requires revision 293 and empty registry")
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v247.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v248.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260908/state-before-revision294.json"
    side = ROOT / "artifacts/task_FLT_operator_binding_20260908"
    required = [old, side / "bind_numeric_receipt.py", side / "numeric_binding_receipt.json", side / "extraction.out", side / "exact_rational_replay_20260906.out", side / "receipt.json"]
    if not all(path.is_file() for path in required):
        raise ValueError("missing numeric receipt binding evidence")
    binding = json.loads((side / "numeric_binding_receipt.json").read_text(encoding="utf-8"))
    if binding.get("status") != "PASS_ARTIFACTS_BOUND_SINGLE_CELL_SOURCE_SEMANTICS_OPEN" or binding.get("failure_count") != 0:
        raise ValueError("numeric receipt binding did not pass fail-closed checks")
    record = {
        "kind": "routeb_numeric_receipt_cross_artifact_binding",
        "status": binding["status"],
        "evidence_level": "source-hash-plus-julia-extraction-plus-fraction-replay-plus-contract-binding",
        "files": [ref(side / name) for name in ("bind_numeric_receipt.py", "numeric_binding_receipt.json", "extraction.out", "exact_rational_replay_20260906.out", "receipt.json")],
        "cell": binding["cell"],
        "failure_count": binding["failure_count"],
        "source_interval_semantics_formalized": binding["source_interval_semantics_formalized"],
        "domain_coverage_complete": binding["domain_coverage_complete"],
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph = json.loads(old.read_text(encoding="utf-8"))
    graph.setdefault("bottleneck_audits", []).append(record)
    graph.setdefault("external_intakes", []).append(record)
    graph.setdefault("open_frontier_updates", []).append({
        "node": "B45.numeric_receipt_binding",
        "status": "cross_artifact_binding_pass_source_semantics_open",
        "reason": "The one-cell outputs are mutually bound and source-hashed, but this does not prove the physical interval evaluator or coverage.",
    })
    graph.update(schema="routeb-proposed-proof-dag-v248", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision294_numeric_receipt_binding/v1",
        "graph_sha256": digest,
        "roots": [],
        "selected_nodes": [],
        "source": str(side),
        "evidence_sha256": sha(side / "numeric_binding_receipt.json"),
        "cross_artifact_binding": True,
        "single_cell_only": True,
        "source_semantics_open": True,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision294_numeric_receipt_binding_recorded",
        proposed_dag=ref(new),
        proposed_dag_sha256=digest,
        cross_artifact_binding=True,
        canonical_source_hash_bound=True,
        julia_extraction_bound=True,
        exact_rational_replay_bound=True,
        single_cell_only=True,
        source_interval_semantics=False,
        domain_coverage_complete=False,
        registry_promoted=False,
        formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name, "registry": len(state.registry)}))


if __name__ == "__main__":
    main()
