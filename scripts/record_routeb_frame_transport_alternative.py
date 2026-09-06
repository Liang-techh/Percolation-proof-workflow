"""Record a clean independent proof candidate for the existing frame seam."""
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
    assert state.revision == 123 and not state.registry
    base = ROOT / "artifacts/routeb_agent_frame_transport_20260906T070654Z"
    source = base / "AgentFrameTransport.lean"
    olean = base / "AgentFrameTransport.olean"
    receipt = base / "RECEIPT.md"
    log = base / "terminal.log"
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v77.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v78.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision124.json"
    for path in (source, olean, receipt, log, old_graph):
        assert path.is_file(), path
    assert not graph_path.exists() and not backup.exists()
    source_text = source.read_text(encoding="utf-8")
    receipt_text = receipt.read_text(encoding="utf-8")
    log_text = log.read_text(encoding="utf-8")
    assert "AGENT_FRAME_TRANSPORT_COMPILE_EXIT_CODE=0" in receipt_text
    assert "no `sorryAx`" in receipt_text
    assert "AGENT_FRAME_TRANSPORT_COMPILE_EXIT_CODE=0" in log_text
    assert "sorry" not in source_text.lower()

    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    nodes = {node["id"]: node for node in graph["nodes"]}
    node_id = "B45-1_pure_prefix_transport_shadow_leaf"
    assert node_id in nodes
    node = nodes[node_id]
    node.setdefault("verification", {}).setdefault("alternate_candidates", []).append({
        "source": ref(source), "olean": ref(olean), "receipt": ref(receipt),
        "log": ref(log), "source_sha256": sha(source), "olean_sha256": sha(olean),
        "receipt_sha256": sha(receipt), "log_sha256": sha(log),
        "compile_exit": 0, "standard_axioms_only": True, "sorry_ax": 0,
        "registry_promoted": False,
        "semantic_boundary": "pure Fin7 transport only; concrete DH accessor binding remains open",
    })
    node.setdefault("open_bridges", []).append(
        "alternate pure transport candidate still requires concrete accessor comparator"
    )
    graph.update(schema="routeb-proposed-proof-dag-v78", supersedes="block45-obligations-v77.json")
    graph["nodes"] = list(nodes.values())
    ids = set(nodes)
    for candidate in nodes.values():
        for dep in candidate.get("dependencies", []):
            if dep not in ids:
                raise ValueError(f"dangling dependency: {dep}")

    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    state.event(
        "routeb_frame_transport_alternative_recorded",
        node_id=node_id, source=ref(source), olean=ref(olean), receipt=ref(receipt),
        source_sha256=sha(source), olean_sha256=sha(olean), receipt_sha256=sha(receipt),
        compile_exit=0, sorry_ax=0, registry_promoted=False,
        concrete_accessor_binding_open=True, formal_certificate_allowed=False,
        proposed_dag=ref(graph_path), broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph_nodes": len(nodes),
           "registry": len(state.registry), "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()
