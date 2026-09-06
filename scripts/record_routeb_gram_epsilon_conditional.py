"""Record the conditional exact rational remainder interface for P6 blocks 3/4."""
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
    assert state.revision == 154 and not state.registry
    base = ROOT / "artifacts/routeb_agent_gram_epsilon_next_20260906_021102"
    report = base / "REPORT.md"
    lean_source = base / "GramEpsilonInterface.lean"
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v108.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v109.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision155.json"
    for path in (report, lean_source, old_graph):
        assert path.is_file(), path
    assert not graph_path.exists() and not backup.exists()
    text = report.read_text(encoding="utf-8")
    for marker in ("E_3(B)", "E_4(B)", "DECLARED_FORMAL_DOMAIN_ATTACHED_TO_P6_BLOCK34: missing"):
        assert marker in text
    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    nodes = {node["id"]: node for node in graph["nodes"]}
    node_id = "B45-P6_exact_gram_identity_obstruction"
    node = nodes[node_id]
    node.setdefault("verification", {}).setdefault("conditional_remainder_interfaces", []).append({
        "report": ref(report), "lean_source": ref(lean_source),
        "report_sha256": sha(report), "lean_source_sha256": sha(lean_source),
        "domain_id": "P6_block34_box_v1",
        "variables": ["qa", "qb", "dqa", "dqb", "t", "w"],
        "upper_abs": ["2", "2", "3", "3", "1", "2"],
        "blocks": [3, 4], "mismatch_terms": {"3": 28, "4": 28},
        "epsilon": {
            "3": "395592317681666891515041483/5000000000000000000000000000000000",
            "4": "1977774742347034261262942763/25000000000000000000000000000000000",
        },
        "lean_status": "COMPILED_IN_NON_AUTHORITATIVE_MATHLIB_CHECKOUT",
        "status": "CONDITIONAL_RATIONAL_BOX_REMAINDER_ONLY",
        "domain_attached": False, "source_bound": False,
        "registry_eligible": False, "formal_certificate_allowed": False,
    })
    node.setdefault("open_bridges", []).extend([
        "prove P6 block 3/4 domain membership from authoritative trajectory/tube semantics",
        "replace constant remainder with an exact polynomial remainder or margin absorption proof",
        "compile the instantiated coefficient table under the current pinned Route-B Mathlib environment",
    ])
    graph.update(schema="routeb-proposed-proof-dag-v109", supersedes="block45-obligations-v108.json")
    graph["nodes"] = list(nodes.values())
    ids = set(nodes)
    for candidate in nodes.values():
        for dependency in candidate.get("dependencies", []):
            if dependency not in ids:
                raise ValueError(f"dangling dependency: {dependency}")
    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    state.event(
        "routeb_gram_epsilon_conditional_recorded", node_id=node_id,
        report=ref(report), lean_source=ref(lean_source),
        report_sha256=sha(report), lean_source_sha256=sha(lean_source),
        domain_id="P6_block34_box_v1", variables=["qa", "qb", "dqa", "dqb", "t", "w"],
        upper_abs=["2", "2", "3", "3", "1", "2"], blocks=[3, 4],
        mismatch_terms={"3": 28, "4": 28},
        epsilon_3="395592317681666891515041483/5000000000000000000000000000000000",
        epsilon_4="1977774742347034261262942763/25000000000000000000000000000000000",
        lean_status="COMPILED_IN_NON_AUTHORITATIVE_MATHLIB_CHECKOUT",
        status="CONDITIONAL_RATIONAL_BOX_REMAINDER_ONLY", domain_attached=False,
        source_bound=False, registry_promoted=False, formal_certificate_allowed=False,
        proposed_dag=ref(graph_path), broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph_nodes": len(nodes),
           "registry": len(state.registry), "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()
