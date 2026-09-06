"""Persist the isolated frame transport leaf and its import-cost boundary."""
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
    assert state.revision == 106 and not state.registry
    base = ROOT / 'artifacts/routeb_frame_slot_homogeneous_prefix_minimal_20260906'
    source = base / 'PurePrefixTransport.lean'
    olean = base / 'pure-run-LScan9nR/PurePrefixTransport.olean'
    result = base / 'RESULT.md'
    old_graph = ROOT / 'artifacts/routeb_6dof/block45-obligations-v63.json'
    graph_path = ROOT / 'artifacts/routeb_6dof/block45-obligations-v64.json'
    backup = ROOT / 'artifacts/routeb_storage_checkpoint_20260905/state-before-revision107.json'
    for path in (source, olean, result, old_graph):
        assert path.is_file()
    assert not graph_path.exists() and not backup.exists()
    assert 'PURE_VERIFY_EXIT_CODE=0' in result.read_text(encoding='utf-8')

    graph = json.loads(old_graph.read_text(encoding='utf-8'))
    nodes = {node['id']: node for node in graph['nodes']}
    node_id = 'B45-1_pure_prefix_transport_shadow_leaf'
    assert node_id not in nodes
    nodes[node_id] = {
        'id': node_id,
        'status': 'compiled_candidate_comparator_pending',
        'dependencies': ['B45-1_homogeneous_prefix_projection'],
        'source': '../../artifacts/routeb_frame_slot_homogeneous_prefix_minimal_20260906/PurePrefixTransport.lean',
        'statement': (
            'Kernel-check the finite Fin 7 prefix transport from pointwise step '
            'homogeneity to homogeneousPrefix, without importing the concrete '
            'Route-B frame accessor.'
        ),
        'verification': {
            'result': ref(result),
            'run': 'pure-run-LScan9nR',
            'compile_exit': 0,
            'verify_exit': 0,
            'standard_axioms_only': True,
            'source_sha256': sha(source),
            'olean_sha256': sha(olean),
            'source_comparator': 'open',
            'concrete_accessor_binding': 'open_import_cost',
        },
        'open_bridges': [
            'bind routeBStepFunction to the pointwise homogeneous step theorem',
            'make FrameSlotAccessor/Projection import tractable under resource budget',
        ],
    }
    projection = nodes['B45-1_homogeneous_prefix_projection']
    projection.setdefault('compiled_precursors', []).append(node_id)
    obligation = next(item for item in graph['source_binding_obligations'] if item['id'] == 'B45-1')
    obligation.setdefault('subnodes', []).append(node_id)
    obligation['source_frame_prefix_binding'] = 'pure_transport_compiled_concrete_import_open'
    graph['next_frontier'] = [
        'B45-1 refactor FrameSlotAccessor/Projection imports into a low-cost adapter',
        'B45-1 instantiate pure prefix transport with routeBStepFunction',
    ] + [x for x in graph['next_frontier'] if 'frame' not in x.lower() or 'transport' not in x.lower()]
    graph.update(schema='routeb-proposed-proof-dag-v64', supersedes='block45-obligations-v63.json')
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
        'routeb_frame_transport_shadow_leaf_recorded',
        result=ref(result), source=ref(source), olean=ref(olean),
        source_sha256=sha(source), olean_sha256=sha(olean),
        compile_exit=0, verify_exit=0, standard_axioms_only=True,
        concrete_accessor_import_blocked=True,
        concrete_accessor_timeout_s=180,
        registry_promotions=0, formal_certificate_allowed=False,
        proposed_dag=ref(graph_path),
    )
    store.save(state)
    print({'revision': state.revision, 'graph_nodes': len(nodes),
           'registry': len(state.registry), 'formal_certificate_allowed': False})


if __name__ == '__main__':
    main()
