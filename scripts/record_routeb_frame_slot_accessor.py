"""Record the compiled source frame/origin/axis slot bridge."""
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
    assert state.revision == 70 and not state.registry
    side = ROOT / 'examples/routeb_frame_slot_accessor_lean'
    receipt = side / 'FINAL_RECEIPT.md'
    source = side / 'output/run-4RJoHvpZ/FrameSlotAccessor.lean'
    olean = side / 'output/run-4RJoHvpZ/FrameSlotAccessor.olean'
    log = side / 'output/run-4RJoHvpZ/terminal.log'
    old_graph = ROOT / 'artifacts/routeb_6dof/block45-obligations-v34.json'
    graph_path = ROOT / 'artifacts/routeb_6dof/block45-obligations-v35.json'
    for path in (receipt, source, olean, log, old_graph):
        assert path.is_file()
    assert not graph_path.exists()
    assert sha(source) == 'f497bd1f45fae4dd385f4d0f46df79252c92e5cd027b29d5dc55011f91525c31'
    assert sha(olean) == '89be6d796b4564c3d84778eb7649772313403bb998184fb1ae028bb177e93af9'
    text = log.read_text(encoding='utf-8') + receipt.read_text(encoding='utf-8')
    for marker in ('FrameSlotAccessor_COMPILE_EXIT_CODE=0', 'VERIFY_EXIT_CODE=0',
                   'SOURCE_RESTRICTION_CHECK=PASSED',
                   'JULIA_FLOAT64_BINDING=OPEN', 'FULL_MASS_BINDING=OPEN',
                   'propext'):
        assert marker in text
    assert 'sorryAx' not in text

    state.event(
        'routeb_b45_1_frame_slot_accessor_compiled',
        receipt=ref(receipt), source=ref(source), olean=ref(olean),
        terminal_log=ref(log), compile_exit=0, verify_exit=0,
        standard_axioms_only=True, source_independent=True,
        source_frame_getD_bridge=True, source_origin_slot_bridge=True,
        source_axis_slot_bridge=True, physical_frame_binding=False,
        float64_binding=False, registry_promoted=False,
        formal_certificate_allowed=False)

    graph = json.loads(old_graph.read_text(encoding='utf-8'))
    graph.update(schema='routeb-proposed-proof-dag-v35',
                 supersedes='block45-obligations-v34.json',
                 active_strategy='single_body_adapter_over_core_and_slots')
    nodes = {node['id']: node for node in graph['nodes']}
    nodes['B45-1_frame_slot_accessor'] = {
        'id': 'B45-1_frame_slot_accessor',
        'status': 'compiled_candidate_comparator_pending',
        'dependencies': ['B45-1_frame_prefix_index',
                         'B45-1_frame_origin_axis_semantics',
                         'B45-1_fin6_index_adapter'],
        'source': '../../examples/routeb_frame_slot_accessor_lean/FrameSlotAccessor.lean',
        'statement': (
            'Kernel-check the fixed Fin-7 frame accessor against the source '
            'List.getD slots and lift the equality to source origin and axis arrays.'),
        'verification': {
            'receipt': str(receipt.resolve()), 'run': 'output/run-4RJoHvpZ',
            'compile_exit': 0, 'verify_exit': 0,
            'standard_axioms_only': True,
            'source_sha256': sha(source), 'olean_sha256': sha(olean)}}
    identity = nodes['B45-1_mass_functional_identity']
    deps = list(identity.get('dependencies', []))
    if 'B45-1_frame_slot_accessor' not in deps:
        deps.append('B45-1_frame_slot_accessor')
    identity['dependencies'] = deps
    identity.setdefault('compiled_precursors', [])
    if 'B45-1_frame_slot_accessor' not in identity['compiled_precursors']:
        identity['compiled_precursors'].append('B45-1_frame_slot_accessor')
    for obligation in graph['source_binding_obligations']:
        if obligation['id'] == 'B45-1':
            subnodes = obligation.setdefault('subnodes', [])
            if 'B45-1_frame_slot_accessor' not in subnodes:
                subnodes.insert(4, 'B45-1_frame_slot_accessor')
            obligation['source_frame_slot_binding'] = 'compiled_candidate_comparator_pending'
            obligation['source_origin_axis_slot_binding'] = 'compiled_candidate_comparator_pending'
            obligation['body_mass_function_binding'] = 'open'
    graph['next_frontier'] = [
        'B45-1 one-body adapter: core body COM/Jacobian over source origin/axis slots',
        'B45-1 block-(4,5) second-body adapter over the same slots',
        'B45-1 lift two-body source semantics to six body contributions',
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
    backup = ROOT / 'artifacts/routeb_storage_checkpoint_20260905/state-before-revision70.json'
    assert not backup.exists()
    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    m4 = next(node for node in state.nodes.values()
              if node.name.startswith('M4.') and node.name != 'M4.correlated_momentum_closure')
    m4.metadata.setdefault('proposed_mathematical_dags', []).append(ref(graph_path))
    m4.metadata['next_mathematical_frontier'] = graph['next_frontier']
    state.event(
        'routeb_b45_1_frame_slot_accessor_checkpoint', proposed_dag=ref(graph_path),
        original_target_unchanged=True, actual_J_proved=False,
        formal_certificate_allowed=False, comparator_accepted=False,
        registry_promotions=0, broad_regression_run=False,
        single_body_source_adapter_open=True)
    store.save(state)
    print(json.dumps(dict(revision=state.revision, nodes=len(state.nodes),
                         graph_nodes=len(nodes), registry=len(state.registry),
                         formal_certificate_allowed=False)))


if __name__ == '__main__':
    main()
