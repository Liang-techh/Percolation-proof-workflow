"""Attach the exact terminal remainder-budget gate and its open DH premise."""
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
    assert state.revision == 149 and not state.registry
    report = ROOT / "artifacts/routeb_agent_terminal_budget_next_20260906T081308Z/REPORT.md"
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v103.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v104.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision150.json"
    for path in (report, old_graph):
        assert path.is_file(), path
    assert not graph_path.exists() and not backup.exists()
    text = report.read_text(encoding="utf-8")
    assert "D <= 4483/2000" in text
    assert "CONDITIONAL_EXACT_TERMINAL_GATE = PASS" in text
    assert "DEPLOYED_DH_BINDING = OPEN" in text

    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    nodes = {node["id"]: node for node in graph["nodes"]}
    node_id = "B45-8_terminal_flowpipe_first_exit_interface"
    node = nodes[node_id]
    node.setdefault("verification", {}).setdefault("exact_budget_gates", []).append({
        "report": ref(report), "report_sha256": sha(report),
        "status": "CONDITIONAL_EXACT_TERMINAL_GATE",
        "D_threshold": "4483/2000", "strict_qpoly_margin": True,
        "deployed_D_bound": "open", "registry_eligible": False,
        "formal_certificate_allowed": False,
    })
    node.setdefault("open_bridges", []).append(
        "prove the full deployed-DH trajectory residual integral D <= 4483/2000"
    )
    graph.update(schema="routeb-proposed-proof-dag-v104", supersedes="block45-obligations-v103.json")
    graph["nodes"] = list(nodes.values())
    ids = set(nodes)
    for candidate in nodes.values():
        for dependency in candidate.get("dependencies", []):
            if dependency not in ids:
                raise ValueError(f"dangling dependency: {dependency}")
    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    state.event(
        "routeb_terminal_budget_gate_recorded", node_id=node_id, report=ref(report),
        report_sha256=sha(report), status="CONDITIONAL_EXACT_TERMINAL_GATE",
        D_threshold="4483/2000", strict_qpoly_margin=True, deployed_D_bound="open",
        registry_promoted=False, formal_certificate_allowed=False,
        proposed_dag=ref(graph_path), broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph_nodes": len(nodes),
           "registry": len(state.registry), "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()
