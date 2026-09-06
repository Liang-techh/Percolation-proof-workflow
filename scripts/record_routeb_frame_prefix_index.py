"""Record the compiled generic finite frame-prefix index leaf."""
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
    assert state.revision == 68 and not state.registry
    side = ROOT / 'examples/routeb_frame_prefix_index_lean'
    receipt = side / 'FINAL_RECEIPT.md'
    source = side / 'output/run-lVHyO9Lp/FramePrefixIndex.lean'
    olean = side / 'output/run-lVHyO9Lp/FramePrefixIndex.olean'
    log = side / 'output/run-lVHyO9Lp/terminal.log'
    old_graph = ROOT / 'artifacts/routeb_6dof/block45-obligations-v32.json'
    graph_path = ROOT / 'artifacts/routeb_6dof/block45-obligations-v33.json'
    for path in (receipt, source, olean, log, old_graph):
        assert path.is_file()
    assert not graph_path.exists()
    assert sha(source) == '6a834b585e14286bf2ba1042493955c065b8a1ba2dd82b5b942a09ce9c2181a5'
    assert sha(olean) == '60eaab045dd51a99d497949fa07a3172574dbb3a8789573a054ddf17cef1ca26'
    text = log.read_text(encoding='utf-8') + receipt.read_text(encoding='utf-8')
    for marker in ('FramePrefixIndex_COMPILE_EXIT_CODE=0', 'VERIFY_EXIT_CODE=0',
                   'SOURCE_RESTRICTION_CHECK=PASSED',
                   'JULIA_FLOAT64_BINDING=OPEN', 'FULL_MASS_BINDING=OPEN',
                   'propext'):
        assert marker in text
    assert 'sorryAx' not in text

    state.event(
        'routeb_b45_1_frame_prefix_index_compiled',
        receipt=ref(receipt), source=ref(source), olean=ref(olean),
        terminal_log=ref(log), compile_exit=0, verify_exit=0,
        standard_axioms_only=True, source_independent=True,
        generic_fin6_prefix=True, source_parent_times_current=True,
        seven_frame_expansion=True, physical_frame_binding=False,
        float64_binding=False, registry_promoted=False,
        formal_certificate_allowed=False)

    graph = json.loads(old_graph.read_text(encoding='utf-8'))
    graph.update(schema='routeb-proposed-proof-dag-v33',
                 supersedes='block45-obligations-v32.json',
                 active_strategy='use_generic_prefix_for_single_body_instantiation')
    nodes = {node['id']: node for node in graph['nodes']}
    nodes['B45-1_frame_prefix_index'] = {
        'id': 'B45-1_frame_prefix_index',
        'status': 'compiled_candidate_comparator_pending',
        'dependencies': ['B45-1_frame_origin_axis_semantics',
                         'B45-1_real_dh_step_bridge',
                         'B45-1_fin6_index_adapter'],
        'source': '../../examples/routeb_frame_prefix_index_lean/FramePrefixIndex.lean',
        'statement': (
            'Kernel-check a generic six-step source frame recursion expanded '
            'to an explicit seven-frame prefix while preserving parent*current '
            'order, without unfolding DH matrix entries.'),
        'verification': {
            'receipt': str(receipt.resolve()), 'run': 'output/run-lVHyO9Lp',
            'compile_exit': 0, 'verify_exit': 0,
            'standard_axioms_only': True,
            'source_sha256': sha(source), 'olean_sha256': sha(olean)}}
    identity = nodes['B45-1_mass_functional_identity']
    deps = list(identity.get('dependencies', []))
    if 'B45-1_frame_prefix_index' not in deps:
        deps.append('B45-1_frame_prefix_index')
    identity['dependencies'] = deps
    identity.setdefault('compiled_precursors', [])
    if 'B45-1_frame_prefix_index' not in identity['compiled_precursors']:
        identity['compiled_precursors'].append('B45-1_frame_prefix_index')
    for obligation in graph['source_binding_obligations']:
        if obligation['id'] == 'B45-1':
            subnodes = obligation.setdefault('subnodes', [])
            if 'B45-1_frame_prefix_index' not in subnodes:
                subnodes.insert(3, 'B45-1_frame_prefix_index')
            obligation['frame_prefix_index'] = 'compiled_candidate_comparator_pending'
            obligation['frame_to_origin_axis_binding'] = 'compiled_candidate_comparator_pending'
            obligation['body_mass_function_binding'] = 'open'
    graph['next_frontier'] = [
        'B45-1 prove one fixed-body frame-prefix index to body COM/Jacobian interface',
        'B45-1 instantiate all six body contributions without matrix-entry unfolding',
        'B45-1 body mass Fourier evaluator for all q',
        'B45-1.i Float64 enclosure bridge',
        'B45-2 deployed potential and central-FD gradient binding',
        'B45-3 H0 and gradient-zero binding',
        'B45-4 Christoffel FD binding',
        'B45-5_residual_domain_bound',
        'positive_supply relative scaling and equilibrium floor',
        'actual mass PSD and eta bounds',
        'uniform_fixed_identity_scalar_source_gate',
        'all_domain_continuation']
    graph['nodes'] = list(nodes.values())

    def visit(key, stack):
        assert key not in stack
        for dep in nodes[key].get('dependencies', []):
            assert dep in nodes
            visit(dep, stack | {key})

    for key in nodes:
        visit(key, set())
    backup = ROOT / 'artifacts/routeb_storage_checkpoint_20260905/state-before-revision68.json'
    assert not backup.exists()
    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    m4 = next(node for node in state.nodes.values()
              if node.name.startswith('M4.') and node.name != 'M4.correlated_momentum_closure')
    m4.metadata.setdefault('proposed_mathematical_dags', []).append(ref(graph_path))
    m4.metadata['next_mathematical_frontier'] = graph['next_frontier']
    state.event(
        'routeb_b45_1_frame_prefix_index_checkpoint', proposed_dag=ref(graph_path),
        original_target_unchanged=True, actual_J_proved=False,
        formal_certificate_allowed=False, comparator_accepted=False,
        registry_promotions=0, broad_regression_run=False,
        single_body_instantiation_open=True)
    store.save(state)
    print(json.dumps(dict(revision=state.revision, nodes=len(state.nodes),
                         graph_nodes=len(nodes), registry=len(state.registry),
                         formal_certificate_allowed=False)))


if __name__ == '__main__':
    main()
