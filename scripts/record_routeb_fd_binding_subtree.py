"""Persist the exact-real/Float64 central-FD theorem decomposition."""
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
    assert state.revision == 111 and not state.registry
    old_graph = ROOT / 'artifacts/routeb_6dof/block45-obligations-v67.json'
    graph_path = ROOT / 'artifacts/routeb_6dof/block45-obligations-v68.json'
    report = ROOT / 'artifacts/routeb_6dof/B45-2-central-fd-source-binding-subtree.md'
    backup = ROOT / 'artifacts/routeb_storage_checkpoint_20260905/state-before-revision112.json'
    assert old_graph.is_file() and report.is_file()
    assert not graph_path.exists() and not backup.exists()
    report_text = report.read_text(encoding='utf-8')
    for marker in ('FD-0', 'FD-5', 'FD-6', 'FD-10', 'OPEN/UNKNOWN'):
        assert marker in report_text

    graph = json.loads(old_graph.read_text(encoding='utf-8'))
    nodes = {node['id']: node for node in graph['nodes']}
    node_id = 'B45-source_central_fd_binding_subtree'
    assert node_id not in nodes
    nodes[node_id] = {
        'id': node_id,
        'status': 'decomposed_open',
        'dependencies': [
            'B45-1_deployed_dh_source_comparator_contract',
            'B45-1_source_body_mass_extensional_probe',
            'B45-5_minimal_fullstate_descriptor_interface',
        ],
        'source': '../../artifacts/routeb_6dof/B45-2-central-fd-source-binding-subtree.md',
        'statement': (
            'Decompose central finite-difference source binding into exact-real '
            'FD-0..FD-5 leaves and Float64/rounding FD-6..FD-10 leaves for full '
            'q,dq dimensions, C*dq, G, and the regularized mass calls.'
        ),
        'verification': {
            'report': ref(report),
            'report_sha256': sha(report),
            'status': 'audit_only',
            'compiled': False,
            'registry_eligible': False,
            'formal_certificate_allowed': False,
        },
        'exact_real_leaves': ['FD-0', 'FD-1', 'FD-2', 'FD-3', 'FD-4', 'FD-5'],
        'float64_bridge_leaves': ['FD-6', 'FD-7', 'FD-8', 'FD-9', 'FD-10'],
        'open_bridges': [
            'deployed Julia C*dq source binding',
            'deployed Julia G source binding',
            'IEEE-754 operation and trigonometric enclosure',
            'analytic derivative/remainder bounds',
        ],
    }
    source = nodes['source_semantics']
    source['central_fd_binding_subtree'] = {
        'node': node_id, 'status': 'decomposed_open',
        'report': ref(report), 'report_sha256': sha(report),
    }
    for parent_id in ('B45-5_residual_domain_bound', 'B45-5_model_replacement_gate'):
        nodes[parent_id].setdefault('open_precursors', []).append(node_id)
    graph['next_frontier'] = [
        'B45 FD-0..FD-4 exact-real source loop adapters',
        'B45 FD-5 analytic central-difference remainder bounds',
        'B45 FD-6..FD-10 Float64 operation/FD/contraction enclosures',
    ] + [x for x in graph['next_frontier'] if 'C/G/FD' not in x]
    graph.update(schema='routeb-proposed-proof-dag-v68', supersedes='block45-obligations-v67.json')
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
        'routeb_central_fd_binding_subtree_recorded',
        report=ref(report), report_sha256=sha(report),
        exact_real_leaves=['FD-0', 'FD-1', 'FD-2', 'FD-3', 'FD-4', 'FD-5'],
        float64_bridge_leaves=['FD-6', 'FD-7', 'FD-8', 'FD-9', 'FD-10'],
        deployed_source_binding_open=True, registry_promotions=0,
        formal_certificate_allowed=False, proposed_dag=ref(graph_path),
        broad_regression_run=False,
    )
    store.save(state)
    print({'revision': state.revision, 'graph_nodes': len(nodes),
           'registry': len(state.registry), 'formal_certificate_allowed': False})


if __name__ == '__main__':
    main()
