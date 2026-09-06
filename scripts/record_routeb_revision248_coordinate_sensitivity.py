"""Persist the original-source coordinate sensitivity sidecar."""
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
    assert state.revision == 247 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v201.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v202.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision248.json"
    sidecar = ROOT / "artifacts/task_GBH_remote_coordinate_sensitivity_20260907"
    files = [sidecar / "receipt.json", sidecar / "REPORT.md",
             sidecar / "coordinate_sensitivity_probe.jl"]
    assert old.is_file() and not new.exists() and all(path.is_file() for path in files)
    graph = json.loads(old.read_text(encoding="utf-8"))
    reason = (
        "On the actual original source, a centered half-width q1 probe reduced "
        "rho_hi 26.4169425088... to 13.4971331488..., while q2/q3/q6 showed "
        "weak or no response; all probes remain inverse-unknown and fail-closed."
    )
    audit = {
        "kind": "routeb_original_coordinate_sensitivity_probe",
        "status": "OPEN_FAIL_CLOSED",
        "evidence_level": "original-source-targeted-four-probe",
        "semantic_boundary": reason,
        "sidecar": str(sidecar.resolve()),
        "files": [ref(path) for path in files],
        "registry_promoted": False,
        "formal_certificate_allowed": False,
        "source_binding": {
            "routeB_interval_bounds_sha256": "d51f7c43a1389edb4c4d5e1d6c492a864bcb55229f99e7032a1ec9c9239f99f1",
            "dhport_lib_sha256": "aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936",
        },
        "probe_count": 4,
        "local_priority_signal": "q1",
        "reference_rho_hi": "26.41694250888084041974927848352623931639243099676539544808170709874681681412479",
        "q1_half_rho_hi": "13.49713314881121733587418899152641542220151850058124914428730372935308263307671",
        "q1_half_delta_M_DD_inf_hi": "0.2061445973667288031094413807507720997817489020121323342016138910260193457371763",
    }
    graph.setdefault("bottleneck_audits", []).append(audit)
    graph.setdefault("external_intakes", []).append({
        "kind": audit["kind"], "source": "independent-sidecar:GBH-original-coordinate-sensitivity",
        "sidecar": audit["sidecar"], "files": audit["files"],
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    graph.setdefault("open_frontier_updates", []).append({
        "node": audit["kind"], "status": "open_missing_data", "reason": reason,
        "local_priority_signal": "q1",
    })
    graph.update(schema="routeb-proposed-proof-dag-v202", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision248_coordinate_sensitivity/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "independent-sidecar:GBH-original-coordinate-sensitivity",
        "evidence_sha256": sha(sidecar / "receipt.json"),
        "strict_compile": False, "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision248_coordinate_sensitivity_recorded",
        proposed_dag=ref(new), proposed_dag_sha256=digest,
        audit={"kind": audit["kind"], "status": audit["status"]},
        local_priority_signal="q1", registry_promoted=False,
        formal_certificate_allowed=False, broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()
