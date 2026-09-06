"""Persist the independent Fourier seam compile blocker."""
import hashlib
import json
import shutil

from record_routeb_port_progress import ROOT, ref
from percolation_workflow.store import StateStore


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    store = StateStore(ROOT / 'artifacts/routeb_6dof/state.json')
    state = store.load()
    assert state.revision == 109 and not state.registry
    old_graph = ROOT / 'artifacts/routeb_6dof/block45-obligations-v65.json'
    graph_path = ROOT / 'artifacts/routeb_6dof/block45-obligations-v66.json'
    receipt = ROOT / 'examples/routeb_b45_source_mass_fourier_bridge_lean/compile_receipt.md'
    source = ROOT / 'examples/routeb_b45_source_mass_fourier_bridge_lean/SourceMassFourierBridge.lean'
    backup = ROOT / 'artifacts/routeb_storage_checkpoint_20260905/state-before-revision110.json'
    for path in (old_graph, graph_path.parent, receipt, source):
        assert path.exists()
    assert not graph_path.exists() and not backup.exists()
    receipt_text = receipt.read_text(encoding='utf-8')
    assert 'Result: failed before elaboration' in receipt_text
    assert 'unknown module prefix' in receipt_text

    graph = json.loads(old_graph.read_text(encoding='utf-8'))
    nodes = {node['id']: node for node in graph['nodes']}
    node_id = 'B45-1_source_mass_fourier_aggregation_seam'
    node = nodes[node_id]
    node['status'] = 'open_compile_blocked'
    node['candidate_evidence']['compile_receipt'] = ref(receipt)
    node['candidate_evidence']['compile_receipt_sha256'] = sha(receipt)
    node['candidate_evidence']['compile_exit'] = 1
    node['candidate_evidence']['olean_snapshot'] = False
    node['failure_boundary'] = 'missing Mathlib.olean in supplied Lean search path before elaboration'
    node['open_bridges'].insert(0, 'create an independent Lake wrapper with pinned Mathlib search path')
    graph['next_frontier'] = [
        'B45-1 create a minimal Lake wrapper for the Fourier aggregation seam',
    ] + [x for x in graph['next_frontier'] if 'pinned receipt' not in x.lower()]
    graph.update(schema='routeb-proposed-proof-dag-v66', supersedes='block45-obligations-v65.json')
    graph['nodes'] = list(nodes.values())
    ids = set(nodes); seen = set(); visiting = set()
    def visit(key):
        if key not in ids or key in visiting:
            raise ValueError('dangling dependency or cycle')
        if key in seen:
            return
        visiting.add(key)
        for dep in nodes[key].get('dependencies', []):
            visit(dep)
        visiting.remove(key); seen.add(key)
    for key in ids:
        visit(key)

    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    state.event(
        'routeb_fourier_aggregation_compile_blocker_recorded',
        source=ref(source), receipt=ref(receipt), receipt_sha256=sha(receipt),
        compile_exit=1, olean_generated=False,
        failure='unknown module prefix Mathlib before elaboration',
        conditional_h_body_preserved=True,
        registry_promotions=0, formal_certificate_allowed=False,
        proposed_dag=ref(graph_path), broad_regression_run=False,
    )
    store.save(state)
    print({'revision': state.revision, 'graph_nodes': len(nodes),
           'registry': len(state.registry), 'formal_certificate_allowed': False})


if __name__ == '__main__':
    main()
