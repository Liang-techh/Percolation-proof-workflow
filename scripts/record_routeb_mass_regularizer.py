"""Record the compiled exact mass-regularizer leaf in the proposed DAG."""
import hashlib
import json
import shutil

from record_routeb_port_progress import ROOT, ref
from percolation_workflow.store import StateStore


def main():
    store = StateStore(ROOT / 'artifacts/routeb_6dof/state.json')
    state = store.load()
    assert state.revision == 54 and len(state.nodes) == 64 and not state.registry
    side = ROOT / 'examples/routeb_mass_regularizer_lean'
    receipt = side / 'FINAL_RECEIPT.md'
    run = side / 'output/run-8qHz1Tiv'
    source = run / 'MassRegularizer.lean'
    olean = run / 'MassRegularizer.olean'
    log = run / 'terminal.log'
    old_graph = ROOT / 'artifacts/routeb_6dof/block45-obligations-v18.json'
    graph_path = ROOT / 'artifacts/routeb_6dof/block45-obligations-v19.json'
    assert receipt.is_file() and source.is_file() and olean.is_file() and log.is_file()
    assert old_graph.is_file() and not graph_path.exists()
    assert hashlib.sha256(source.read_bytes()).hexdigest() == (
        'cd8dafa426a77d867e541f6855b71e58157d383bbbfa214a2712235bf851528b')
    assert hashlib.sha256(olean.read_bytes()).hexdigest() == (
        'f3b2566f78df4e9a4bbdbba7a7f58319c6c4b5315fe57e87a80cb343af18667a')
    rt = receipt.read_text(encoding='utf-8')
    lt = log.read_text(encoding='utf-8')
    for marker in ('Status: PASS', 'MassRegularizer_COMPILE_EXIT_CODE=0',
                   'VERIFY_EXIT_CODE=0', 'propext', 'Float64 bridge'):
        assert marker in (rt + lt)

    state.event(
        'routeb_mass_regularizer_leaf_compiled',
        receipt=ref(receipt), source=ref(source), olean=ref(olean),
        terminal_log=ref(log), compile_exit=0, verify_exit=0,
        standard_axioms_only=True, source_unbound=True,
        registry_promoted=False, formal_certificate_allowed=False)
    graph = json.loads(old_graph.read_text(encoding='utf-8'))
    graph.update(
        schema='routeb-proposed-proof-dag-v19',
        supersedes='block45-obligations-v18.json',
        active_strategy='compiled_regularizer_leaf_before_mass_functional_binding')
    nodes = {node['id']: node for node in graph['nodes']}
    nodes['B45-1_regularizer_kernel_leaf'] = {
        'id': 'B45-1_regularizer_kernel_leaf',
        'status': 'compiled_candidate_comparator_pending',
        'dependencies': [],
        'source': '../../examples/routeb_mass_regularizer_lean/MassRegularizer.lean',
        'statement': (
            'Kernel-check exact entrywise semantics of the real rational '
            '(1/1000000) diagonal regularizer and its composition with an '
            'explicit unregularized-mass/Fourier equality premise.'),
        'verification': {
            'receipt': str(receipt.resolve()), 'run': 'output/run-8qHz1Tiv',
            'compile_exit': 0, 'verify_exit': 0, 'standard_axioms_only': True,
            'source_sha256': 'cd8dafa426a77d867e541f6855b71e58157d383bbbfa214a2712235bf851528b',
            'olean_sha256': 'f3b2566f78df4e9a4bbdbba7a7f58319c6c4b5315fe57e87a80cb343af18667a'}}
    nodes['B45-1_regularized_mass_adapter']['dependencies'] = [
        'B45-1_mass_functional_identity', 'B45-1_regularizer_kernel_leaf']
    nodes['B45-1_regularized_mass_adapter']['kernel_leaf'] = (
        'B45-1_regularizer_kernel_leaf')
    for obligation in graph['source_binding_obligations']:
        if obligation['id'] == 'B45-1':
            obligation['subnodes'].insert(2, 'B45-1_regularizer_kernel_leaf')
            obligation['regularizer_leaf'] = 'compiled_candidate_comparator_pending'
    graph['next_frontier'] = [
        'B45-1.c ideal base mass = Fourier evaluator',
        'B45-1.g q=0 M0 bridge in Lean',
        'B45-1.i Float64 enclosure bridge',
        'B45-2 potential and gradient reconstruction',
        'B45-3 H0 and gradient-zero binding',
        'B45-4 Christoffel FD binding',
        'B45-5_pmi_residual_decomposition',
        'B45-5_residual_domain_bound',
        'B45-5_model_replacement_gate',
        'positive_supply_relative_eta_lemma',
        'positive_supply_two_regime_direct_gate',
        'positive_supply_equilibrium_floor',
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
    backup = ROOT / 'artifacts/routeb_storage_checkpoint_20260905/state-before-revision54.json'
    assert not backup.exists()
    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    m4 = next(node for node in state.nodes.values()
              if node.name.startswith('M4.') and node.name != 'M4.correlated_momentum_closure')
    m4.metadata.setdefault('proposed_mathematical_dags', []).append(ref(graph_path))
    m4.metadata['next_mathematical_frontier'] = graph['next_frontier']
    state.event(
        'routeb_mass_regularizer_checkpoint', proposed_dag=ref(graph_path),
        original_target_unchanged=True, actual_J_proved=False,
        formal_certificate_allowed=False, comparator_accepted=False,
        registry_promotions=0, broad_regression_run=False)
    store.save(state)
    print(json.dumps(dict(revision=state.revision, nodes=len(state.nodes),
                         graph_nodes=len(nodes), registry=len(state.registry),
                         formal_certificate_allowed=False)))


if __name__ == '__main__':
    main()
