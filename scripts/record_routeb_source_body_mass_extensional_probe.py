"""Persist the conditional source-body-mass extensional probe."""
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
    assert state.revision == 107 and not state.registry
    base = ROOT / 'artifacts/routeb_b45_source_body_mass_extensional_probe_20260906'
    source = base / 'SourceBodyMassExtensionalProbe.lean'
    olean = base / 'SourceBodyMassExtensionalProbe.olean'
    old_graph = ROOT / 'artifacts/routeb_6dof/block45-obligations-v64.json'
    graph_path = ROOT / 'artifacts/routeb_6dof/block45-obligations-v65.json'
    backup = ROOT / 'artifacts/routeb_storage_checkpoint_20260905/state-before-revision108.json'
    for path in (source, olean, old_graph):
        assert path.is_file()
    assert not graph_path.exists() and not backup.exists()
    text = source.read_text(encoding='utf-8')
    for marker in ('source_body_mass_extensional_bridge',
                   'source_body_mass_extensional_bridge_all_bodies',
                   'source_mass_sum_extensional_bridge', '#print axioms'):
        assert marker in text
    assert not any(token in text for token in ('sorry', 'admit', 'axiom '))

    graph = json.loads(old_graph.read_text(encoding='utf-8'))
    nodes = {node['id']: node for node in graph['nodes']}
    node_id = 'B45-1_source_body_mass_extensional_probe'
    assert node_id not in nodes
    nodes[node_id] = {
        'id': node_id,
        'status': 'compiled_candidate_comparator_pending',
        'dependencies': [
            'B45-1_source_contract_adapter',
            'B45-1_body_com_jacobian_mass_semantics',
            'B45-1_source_mass_table_exact',
        ],
        'source': '../../artifacts/routeb_b45_source_body_mass_extensional_probe_20260906/SourceBodyMassExtensionalProbe.lean',
        'statement': (
            'Kernel-check the conditional source-body-mass extensional bridge: '
            'origins/axes equality to sourceContract implies equality of the '
            'Julia-style body loop, all six bodies, and their mass sum.'
        ),
        'verification': {
            'source': ref(source),
            'olean': ref(olean),
            'source_sha256': sha(source),
            'olean_sha256': sha(olean),
            'compile_exit': 0,
            'verify_exit': 0,
            'standard_axioms_only': True,
            'source_restriction': 'passed',
            'registry_promoted': False,
        },
        'closed_subclaims': [
            'midpoint COM',
            'parent-axis cross product',
            'joint <= body cutoff',
            'isotropic inertia scalar I_val/3',
            'single-body, all-body, and summed extensionality',
        ],
        'open_bridges': [
            'prove deployed Julia/DH origins equal sourceContract origins',
            'prove deployed Julia parent axes equal sourceContract axes',
            'Float64 matrix/trigonometric/rounding semantics',
        ],
    }
    bridge = nodes['B45-1_source_body_mass_extensional_bridge']
    bridge.setdefault('compiled_precursors', []).append(node_id)
    bridge['conditional_contract_status'] = 'compiled_under_origins_axes_hypotheses'
    bridge['deployed_float64_status'] = 'open'
    obligation = next(item for item in graph['source_binding_obligations'] if item['id'] == 'B45-1')
    obligation.setdefault('subnodes', []).append(node_id)
    obligation['source_body_mass_binding'] = 'conditional_extensional_probe_compiled'
    obligation['source_body_mass_extensional_bridge'] = 'open_deployed_origins_axes'
    graph['next_frontier'] = [
        'B45-1 prove deployed Julia origins == sourceContract origins',
        'B45-1 prove deployed Julia parent axes == sourceContract axes',
        'B45-1 connect conditional source-body-mass probe to source_contract_adapter',
    ] + [x for x in graph['next_frontier'] if 'sourcebodymass' not in x.lower() and 'mass function-level' not in x.lower()]
    graph.update(schema='routeb-proposed-proof-dag-v65', supersedes='block45-obligations-v64.json')
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
        'routeb_source_body_mass_extensional_probe_recorded',
        source=ref(source), olean=ref(olean),
        source_sha256=sha(source), olean_sha256=sha(olean),
        compile_exit=0, verify_exit=0, standard_axioms_only=True,
        conditional_on_origins_axes=True, deployed_float64_binding_open=True,
        registry_promotions=0, formal_certificate_allowed=False,
        proposed_dag=ref(graph_path),
    )
    store.save(state)
    print({'revision': state.revision, 'graph_nodes': len(nodes),
           'registry': len(state.registry), 'formal_certificate_allowed': False})


if __name__ == '__main__':
    main()
