"""Record the full-contract entry/first-exit ledger as an open obstruction."""
import hashlib
import json
import shutil

from record_routeb_port_progress import ROOT, ref
from percolation_workflow.store import StateStore


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    assert state.revision == 169 and not state.registry
    base = ROOT / "artifacts/routeb_agent_entry_flowpipe_next_20260906T092401Z"
    report, ledger, replay = (base / name for name in ("REPORT.md", "entry_flowpipe_ledger.json", "entry_flowpipe_ledger.py"))
    for path in (report, ledger, replay):
        assert path.is_file(), path
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v123.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v124.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision170.json"
    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    graph["bottleneck_audits"] = graph.get("bottleneck_audits", [])
    graph["bottleneck_audits"].append({
        "kind": "P3_P8_full_contract_entry_first_exit_ledger",
        "report": {"path": ref(report), "sha256": sha(report)},
        "ledger": {"path": ref(ledger), "sha256": sha(ledger)},
        "replay": {"path": ref(replay), "sha256": sha(replay)},
        "status": "ENTRY_NOT_PROVED_FIRST_EXIT_OPEN",
        "evidence_level": "E1_replay_of_recorded_artifacts",
        "initial_member": False,
        "p8_narrow_all_coordinates_disjoint": True,
        "registry_promoted": False,
    })
    graph["open_frontier_updates"] = graph.get("open_frontier_updates", [])
    graph["open_frontier_updates"].append({"node": "B45-P3_full_contract_entry_first_exit", "status": "open", "reason": "need source-bound full 13-state X0+ramp+T1 ledger and non-circular boundary exclusion"})
    graph.update(schema="routeb-proposed-proof-dag-v124", supersedes="block45-obligations-v123.json")
    ids = {node["id"] for node in graph["nodes"]}
    for node in graph["nodes"]:
        for dependency in node.get("dependencies", []):
            if dependency not in ids:
                raise ValueError(f"dangling dependency: {dependency}")
    if not backup.exists():
        shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    digest = sha(graph_path)
    state.graph_artifacts.append({"schema_version": 1, "algorithm": "routeb_entry_flowpipe_ledger/v1", "graph_sha256": digest, "roots": [], "selected_nodes": [], "source": "entry/first-exit ledger replay", "report_sha256": sha(report), "ledger_sha256": sha(ledger), "replay_sha256": sha(replay), "initial_member": False, "formal_certificate_allowed": False})
    state.event("routeb_entry_flowpipe_ledger_recorded", report=ref(report), report_sha256=sha(report), ledger=ref(ledger), ledger_sha256=sha(ledger), replay=ref(replay), replay_sha256=sha(replay), status="ENTRY_NOT_PROVED_FIRST_EXIT_OPEN", initial_member=False, p8_narrow_all_coordinates_disjoint=True, registry_promoted=False, formal_certificate_allowed=False, proposed_dag=ref(graph_path), proposed_dag_sha256=digest, broad_regression_run=False)
    store.save(state)
    print({"revision": state.revision, "graph": graph_path.name, "registry": len(state.registry), "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()
