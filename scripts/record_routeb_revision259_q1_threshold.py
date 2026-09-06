"""Persist the q1-only local Neumann threshold crossing."""
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
    assert state.revision == 258 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v212.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v213.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision259.json"
    sidecar = ROOT / "artifacts/task_GCC_q1_deeper_refinement_20260907"
    files = [sidecar / "REPORT.md", sidecar / "receipt.json", sidecar / "probe.jl"]
    assert old.is_file() and not new.exists() and all(path.is_file() for path in files)
    receipt = json.loads((sidecar / "receipt.json").read_text(encoding="utf-8"))
    graph = json.loads(old.read_text(encoding="utf-8"))
    reason = (
        "q1-only original-source refinement crosses the local Neumann threshold "
        "at 1/64 (rho_hi=0.8068458978...), while 1/32 remains above one; this "
        "closes only the contracted cell guard and not coverage or M4."
    )
    audit = {
        "kind": "routeb_original_q1_local_neumann_threshold",
        "status": receipt["status"],
        "evidence_level": "original-source-two-targeted-probes",
        "semantic_boundary": reason,
        "sidecar": str(sidecar.resolve()),
        "files": [ref(path) for path in files],
        "source_sha256": receipt["source_hash"],
        "cell": receipt["cell"],
        "metric": receipt["metric"],
        "probe_count": receipt["probe_count"],
        "threshold_crossing": {
            "depth": 6, "width_fraction": "1/64",
            "rho_hi": "0.8068458977980264943060861593371242",
            "delta_M_DD_inf_hi": "0.01197131419943879121975104978050677",
            "guard_status": "CERTIFIED_NEUMANN_RHO_LT_ONE",
        },
        "coverage_complete": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph.setdefault("bottleneck_audits", []).append(audit)
    graph.setdefault("external_intakes", []).append({
        "kind": audit["kind"], "source": "independent-sidecar:GCC-q1-deeper-refinement",
        "sidecar": audit["sidecar"], "files": audit["files"],
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    graph.setdefault("open_frontier_updates", []).append({
        "node": audit["kind"], "status": "local_guard_closed_global_open", "reason": reason,
    })
    graph.update(schema="routeb-proposed-proof-dag-v213", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision259_q1_threshold/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "independent-sidecar:GCC-q1-deeper-refinement",
        "evidence_sha256": sha(sidecar / "receipt.json"),
        "strict_compile": False, "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision259_q1_threshold_recorded",
        proposed_dag=ref(new), proposed_dag_sha256=digest,
        audit={"kind": audit["kind"], "status": audit["status"]},
        local_guard_closed=True, global_coverage_closed=False,
        registry_promoted=False, formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()
