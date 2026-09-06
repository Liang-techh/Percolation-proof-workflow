"""Record the compiled Fin-6/Julia index and block projection adapter."""
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
    assert state.revision == 64 and not state.registry
    side = ROOT / 'examples/routeb_fin6_index_adapter_lean'
    receipt = side / 'FINAL_RECEIPT.md'
    source = side / 'output/run-SU3YmHP0/Fin6IndexAdapter.lean'
    olean = side / 'output/run-SU3YmHP0/Fin6IndexAdapter.olean'
    log = side / 'output/run-SU3YmHP0/terminal.log'
    old_graph = ROOT / 'artifacts/routeb_6dof/block45-obligations-v28.json'
    graph_path = ROOT / 'artifacts/routeb_6dof/block45-obligations-v29.json'
    for path in (receipt, source, olean, log, old_graph):
        assert path.is_file()
    assert not graph_path.exists()
    assert sha(source) == 'e795e93744a18d7c1be84890d4ab04ff41e8f9bf480f11acabe4a3b32684903d'
    assert sha(olean) == 'd04e17a05c56bb58944943d4eb49051840563d97557f427475c11e8bbab820c8'
    log_text = log.read_text(encoding='utf-8')
    receipt_text = receipt.read_text(encoding='utf-8')
    for marker in ('Fin6IndexAdapter_COMPILE_EXIT_CODE=0',
                   'VERIFY_EXIT_CODE=0', 'SOURCE_RESTRICTION_CHECK=PASSED',
                   'FUNCTION_LEVEL_FRAME_BINDING=OPEN', 'propext'):
        assert marker in log_text + receipt_text
    assert 'sorryAx' not in log_text
    assert 'native_decide' not in source.read_text(encoding='utf-8')

    state.event(
        'routeb_b45_1_fin6_index_adapter_compiled',
        receipt=ref(receipt), source=ref(source), olean=ref(olean),
        terminal_log=ref(log), compile_exit=0, verify_exit=0,
        standard_axioms_only=True, source_independent=True,
        fin6_julia_bijection=True, source_order_mapping=True,
        block_mapping=True, function_level_frame_binding=False,
        function_level_mass_binding=False, registry_promoted=False,
        formal_certificate_allowed=False)

    graph = json.loads(old_graph.read_text(encoding='utf-8'))
    graph.update(schema='routeb-proposed-proof-dag-v29',
                 supersedes='block45-obligations-v28.json',
                 active_strategy='close_fin6_source_order_adapter')
    nodes = {node['id']: node for node in graph['nodes']}
    nodes['B45-1_fin6_index_adapter'] = {
        'id': 'B45-1_fin6_index_adapter',
        'status': 'compiled_candidate_comparator_pending',
        'dependencies': ['B45-1_frame_recursion'],
        'source': '../../examples/routeb_fin6_index_adapter_lean/Fin6IndexAdapter.lean',
        'statement': (
            'Kernel-check the Fin 6 to Julia 1-based bijection, source-order '
            'list, and B=(4,5)/D=(1,2,3,6) block projections; keep function-level '
            'DH/frame/mass binding explicitly open.'),
        'verification': {
            'receipt': str(receipt.resolve()), 'run': 'output/run-SU3YmHP0',
            'compile_exit': 0, 'verify_exit': 0,
            'standard_axioms_only': True,
            'source_sha256': sha(source), 'olean_sha256': sha(olean)}}
    identity = nodes['B45-1_mass_functional_identity']
    deps = list(identity.get('dependencies', []))
    if 'B45-1_fin6_index_adapter' not in deps:
        deps.append('B45-1_fin6_index_adapter')
    identity['dependencies'] = deps
    identity.setdefault('compiled_precursors', [])
    if 'B45-1_fin6_index_adapter' not in identity['compiled_precursors']:
        identity['compiled_precursors'].append('B45-1_fin6_index_adapter')
    for obligation in graph['source_binding_obligations']:
        if obligation['id'] == 'B45-1':
            subnodes = obligation.setdefault('subnodes', [])
            if 'B45-1_fin6_index_adapter' not in subnodes:
                subnodes.insert(0, 'B45-1_fin6_index_adapter')
            obligation['fin6_julia_index_adapter'] = 'compiled_candidate_comparator_pending'
            obligation['source_order_specialization'] = 'compiled_candidate'
            obligation['function_level_frame_binding'] = 'open'
            obligation['function_level_mass_binding'] = 'open'
    graph['next_frontier'] = [
        'B45-1 function-level six-step DH frame/axis/origin adapter',
        'B45-1 body COM/Jacobian and link mass contribution',
        'B45-1.c body mass Fourier evaluator for all q',
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
    backup = ROOT / 'artifacts/routeb_storage_checkpoint_20260905/state-before-revision64.json'
    assert not backup.exists()
    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    m4 = next(node for node in state.nodes.values()
              if node.name.startswith('M4.') and node.name != 'M4.correlated_momentum_closure')
    m4.metadata.setdefault('proposed_mathematical_dags', []).append(ref(graph_path))
    m4.metadata['next_mathematical_frontier'] = graph['next_frontier']
    state.event(
        'routeb_b45_1_fin6_index_adapter_checkpoint', proposed_dag=ref(graph_path),
        original_target_unchanged=True, actual_J_proved=False,
        formal_certificate_allowed=False, comparator_accepted=False,
        registry_promotions=0, broad_regression_run=False,
        function_level_binding_open=True)
    store.save(state)
    print(json.dumps(dict(revision=state.revision, nodes=len(state.nodes),
                         graph_nodes=len(nodes), registry=len(state.registry),
                         formal_certificate_allowed=False)))


if __name__ == '__main__':
    main()
