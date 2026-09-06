"""Record the improved local P3 enclosure configuration as an open candidate."""
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
    assert state.revision == 164 and not state.registry
    base = ROOT / "artifacts/routeb_agent_p3_next_20260906T085350Z"
    report, summary, replay = (base / name for name in ("REPORT.md", "p3_next_summary.json", "p3_next_summary_replayed.json"))
    for path in (report, summary, replay):
        assert path.is_file(), path
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v118.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v119.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision165.json"
    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    graph["bottleneck_audits"] = graph.get("bottleneck_audits", [])
    graph["bottleneck_audits"].append({
        "kind": "P3_local_meanvalue_zero_centered_candidate",
        "report": {"path": ref(report), "sha256": sha(report)},
        "summary": {"path": ref(summary), "sha256": sha(summary)},
        "replay": {"path": ref(replay), "sha256": sha(replay)},
        "evidence_level": "E1_directed_interval_local_candidate",
        "status": "LOCAL_POSITIVE_GLOBAL_OPEN",
        "configuration": {
            "mass": "meanvalue", "cg": "meanvalue_qdq", "affine_w": True,
            "inverse": "weighted_krawczyk", "split": "zero_centered",
            "radius": "0.005", "safety_factor": "2",
        },
        "h_lo": "5.6715765686215843329542797025",
        "kappa": "0.00429855811027026631830764876743",
        "coverage_complete": False,
        "registry_promoted": False,
    })
    graph.update(schema="routeb-proposed-proof-dag-v119", supersedes="block45-obligations-v118.json")
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
        "schema_version": 1, "algorithm": "routeb_p3_local_enclosure_candidate/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "independent directed BigFloat P3 local enclosure study",
        "report_sha256": sha(report), "summary_sha256": sha(summary),
        "replay_sha256": sha(replay), "coverage_complete": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_p3_local_enclosure_candidate_recorded", report=ref(report), report_sha256=sha(report),
        summary=ref(summary), summary_sha256=sha(summary), replay=ref(replay), replay_sha256=sha(replay),
        status="LOCAL_POSITIVE_GLOBAL_OPEN", configuration={"mass": "meanvalue", "cg": "meanvalue_qdq", "affine_w": True, "inverse": "weighted_krawczyk", "split": "zero_centered", "radius": "0.005", "safety_factor": "2"},
        h_lo="5.6715765686215843329542797025", kappa="0.00429855811027026631830764876743",
        coverage_complete=False, registry_promoted=False, formal_certificate_allowed=False,
        proposed_dag=ref(graph_path), proposed_dag_sha256=digest, broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": graph_path.name, "registry": len(state.registry), "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()
