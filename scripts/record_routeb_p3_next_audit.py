"""Record the independent P3 directed-interval audit as an open leaf."""
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
    assert state.revision == 162 and not state.registry
    base = ROOT / "artifacts/routeb_agent_p3_next_20260906T085340Z"
    report, replay, replay_csv = (base / name for name in ("REPORT.md", "replay_summary.json", "replay_summary.csv"))
    for path in (report, replay, replay_csv):
        assert path.is_file(), path
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v116.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v117.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision163.json"
    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    graph["bottleneck_audits"] = graph.get("bottleneck_audits", [])
    graph["bottleneck_audits"].append({
        "kind": "P3_directed_interval_replay",
        "report": {"path": ref(report), "sha256": sha(report)},
        "replay": {"path": ref(replay), "sha256": sha(replay)},
        "replay_csv": {"path": ref(replay_csv), "sha256": sha(replay_csv)},
        "evidence_level": "directed_interval_numeric_candidate",
        "status": "LOCAL_POSITIVE_GLOBAL_OPEN",
        "global_kappa": "5030.7000334738",
        "local_positive_radii": ["0.005", "0.01", "0.015"],
        "coverage_complete": False,
        "registry_promoted": False,
    })
    graph.update(schema="routeb-proposed-proof-dag-v117", supersedes="block45-obligations-v116.json")
    ids = {node["id"] for node in graph["nodes"]}
    for node in graph["nodes"]:
        for dependency in node.get("dependencies", []):
            if dependency not in ids:
                raise ValueError(f"dangling dependency: {dependency}")
    if not backup.exists():
        shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    digest = sha(graph_path)
    state.graph_artifacts.append({
        "schema_version": 1, "algorithm": "routeb_p3_next_audit/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "independent directed interval P3 replay",
        "report_sha256": sha(report), "replay_sha256": sha(replay),
        "coverage_complete": False, "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_p3_next_audit_recorded", report=ref(report), report_sha256=sha(report),
        replay=ref(replay), replay_sha256=sha(replay), replay_csv=ref(replay_csv),
        replay_csv_sha256=sha(replay_csv), status="LOCAL_POSITIVE_GLOBAL_OPEN",
        global_kappa="5030.7000334738", local_positive_radii=["0.005", "0.01", "0.015"],
        coverage_complete=False, registry_promoted=False, formal_certificate_allowed=False,
        proposed_dag=ref(graph_path), proposed_dag_sha256=digest, broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": graph_path.name, "registry": len(state.registry), "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()
