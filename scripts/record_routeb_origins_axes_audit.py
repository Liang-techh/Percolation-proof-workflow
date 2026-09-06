"""Persist the read-only deployed origins/parent-axis source audit."""
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
    assert state.revision == 117 and not state.registry
    audit = ROOT / "artifacts/routeb_b45_source_body_mass_bridge_audit_20260906.md"
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v72.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v73.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision118.json"
    for path in (audit, old_graph):
        assert path.is_file(), path
    assert not graph_path.exists() and not backup.exists()
    text = audit.read_text(encoding="utf-8")
    for marker in ("structural semantics", "parent axis", "midpoint", "jj <= ii",
                   "Float64", "Exact extensionality premises"):
        assert marker in text
    assert "No numerical samples are used as evidence" in text

    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    nodes = {node["id"]: node for node in graph["nodes"]}
    node_id = "B45-1_deployed_origins_axes_source_audit"
    assert node_id not in nodes
    nodes[node_id] = {
        "id": node_id,
        "status": "source_audit_open",
        "dependencies": [
            "B45-1_source_body_mass_extensional_probe",
            "B45-1_frame_recursion",
            "B45-1_fin6_index_adapter",
        ],
        "source": "../../artifacts/routeb_b45_source_body_mass_bridge_audit_20260906.md",
        "statement": (
            "Audit the structural correspondence of deployed Julia/Python and "
            "exact-real source-body mass semantics: seven frame slots, "
            "parent-before-current axis, midpoint COM, jj<=ii cutoff, and I_val/3."
        ),
        "verification": {
            "audit": ref(audit), "audit_sha256": sha(audit),
            "status": "audit_only", "compiled": False,
            "registry_eligible": False, "comparator_accepted": False,
            "main_state_modified": False, "original_project_modified": False,
        },
        "closed_subclaims": [
            "seven frame-slot structural layout",
            "parent-axis read before current transform",
            "post-step origin and midpoint COM layout",
            "jj<=ii active-column cutoff",
            "isotropic I_val/3 structural term",
        ],
        "open_bridges": [
            "Julia Float64 sin/cos and matrix-product exact semantics",
            "regularizer convention and exact-real alignment",
            "formal source-to-Lean frame/origin/axis extensionality theorem",
            "body and six-body mass comparator",
        ],
        "semantic_boundary": "read-only structural audit; not a theorem or numerical certificate",
    }
    bridge = nodes["B45-1_source_body_mass_extensional_bridge"]
    bridge.setdefault("audit_precursors", []).append(node_id)
    bridge["deployed_origins_axes_status"] = "structural_audit_open"
    graph["next_frontier"] = [
        "B45-1 formalize deployed origins == sourceContract origins",
        "B45-1 formalize deployed parent axes == sourceContract axes",
        "B45-1 bind Float64 trigonometric/matrix semantics and regularizer",
    ] + [x for x in graph["next_frontier"] if "deployed Julia origins" not in x and "deployed Julia parent axes" not in x]
    graph.update(schema="routeb-proposed-proof-dag-v73", supersedes="block45-obligations-v72.json")
    graph["nodes"] = list(nodes.values())

    ids = set(nodes)
    seen = set()
    visiting = set()
    def visit(key):
        if key not in ids or key in visiting:
            raise ValueError("dangling dependency or cycle")
        if key in seen:
            return
        visiting.add(key)
        for dep in nodes[key].get("dependencies", []):
            visit(dep)
        visiting.remove(key)
        seen.add(key)
    for key in ids:
        visit(key)

    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    state.event(
        "routeb_origins_axes_source_audit_recorded",
        audit=ref(audit), audit_sha256=sha(audit),
        structural_match=True, exact_extensionality_proved=False,
        float64_semantics_open=True, regularizer_alignment_open=True,
        comparator_accepted=False, registry_promoted=False,
        formal_certificate_allowed=False, proposed_dag=ref(graph_path),
        broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph_nodes": len(nodes),
           "registry": len(state.registry), "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()
