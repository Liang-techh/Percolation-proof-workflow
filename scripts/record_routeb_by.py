"""Record the bounded Schur d_N audit without promotion."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from record_routeb_port_progress import ROOT, ref
from percolation_workflow.store import StateStore


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> None:
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    assert state.revision == 195 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v149.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v150.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260906/state-before-revision196.json"
    assert old.is_file() and not new.exists()
    base = ROOT / "artifacts/task_BY_schur_dN_bounded_20260906"
    paths = {n: base / n for n in ("REPORT.md", "ledger.json", "check.py")}
    for p in paths.values():
        assert p.is_file(), p
    graph = json.loads(old.read_text(encoding="utf-8"))
    graph.setdefault("bottleneck_audits", []).append({
        "kind": "routeb_schur_dN_bounded_audit",
        "status": "OPEN_MISSING_DATA",
        "evidence_level": "bounded_rational_refinement_contract",
        "semantic_boundary": "rho_N refinement formula is available but neighbor matrix variation d_N is not numerically witnessed",
        "registry_promoted": False, "formal_certificate_allowed": False,
        "files": {k: {"path": ref(v), "sha256": sha(v)} for k, v in paths.items()},
    })
    graph.setdefault("open_frontier_updates", []).append({
        "node": "RouteBSchur.neighbor_dN",
        "status": "open_missing_data",
        "reason": "need outward-rounded d_N and cell coverage before applying rho_N=||M_DD(0)^-1||inf*d_N<1",
    })
    graph.update(schema="routeb-proposed-proof-dag-v150", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({"schema_version": 1, "algorithm": "routeb_schur_dN_bounded_audit/v1", "graph_sha256": digest, "roots": [], "selected_nodes": [], "source": str(paths["REPORT.md"]), "evidence_sha256": sha(paths["REPORT.md"]), "registry_promoted": False, "formal_certificate_allowed": False})
    state.event("routeb_by_recorded", proposed_dag=ref(new), proposed_dag_sha256=digest, report=ref(paths["REPORT.md"]), report_sha256=sha(paths["REPORT.md"]), registry_promoted=False, formal_certificate_allowed=False, broad_regression_run=False)
    store.save(state)
    print({"revision": state.revision, "graph": new.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()
