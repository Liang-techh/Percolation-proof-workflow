"""Record the concrete P3 source-binding map as an open obligation ledger."""
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
    if state.revision != 286 or state.registry:
        raise ValueError("revision-287 recorder requires revision 286 and empty registry")
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v240.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v241.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260908/state-before-revision287.json"
    ledger = ROOT / "artifacts/task_FLT_source_binding_map_20260908"
    required = [old, ledger]
    if not all(path.is_file() for path in required):
        raise ValueError("missing source-binding map")
    text = ledger.read_text(encoding="utf-8")
    if "SB-01" not in text or "SB-12" not in text or "h_src" not in text:
        raise ValueError("source-binding ledger is incomplete")
    record = {
        "kind": "routeb_concrete_p3_source_binding_map",
        "status": "FAIL_CLOSED_OBLIGATION_LEDGER_OPEN",
        "evidence_level": "canonical-source-mapped-open-obligations",
        "file": ref(ledger),
        "obligation_ids": [f"SB-{i:02d}" for i in range(1, 13)],
        "mapped_quantities": ["h_src", "h_lo/h_hi", "bound blow/bup", "lB/lv", "midpoint/radius/kappa"],
        "required_backend_facts": ["exact-real sin/cos bridge", "operation-DAG equivalence", "directed absolute rounding", "coverage"],
        "canonical_source_anchor": "routeB_interval_bounds.jl current patched snapshot",
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph = json.loads(old.read_text(encoding="utf-8"))
    graph.setdefault("bottleneck_audits", []).append(record)
    graph.setdefault("external_intakes", []).append(record)
    graph.setdefault("open_frontier_updates", []).append({
        "node": "B45.concrete_source_binding",
        "status": "SB_01_SB_12_open",
        "reason": "The ledger maps abstract error atoms to deployed Julia fields but supplies no theorem admission or numeric certificate.",
    })
    graph.update(schema="routeb-proposed-proof-dag-v241", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision287_source_binding_map/v1",
        "graph_sha256": digest,
        "roots": [],
        "selected_nodes": [],
        "source": str(ledger),
        "evidence_sha256": sha(ledger),
        "obligation_count": 12,
        "physical_binding_open": True,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision287_source_binding_map_recorded",
        proposed_dag=ref(new),
        proposed_dag_sha256=digest,
        concrete_obligation_count=12,
        exact_real_backend_open=True,
        rounding_binding_open=True,
        coverage_closed=False,
        registry_promoted=False,
        formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name, "registry": len(state.registry)}))


if __name__ == "__main__":
    main()
