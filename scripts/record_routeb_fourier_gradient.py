"""Record the compiled source-independent Fourier potential gradient leaf."""
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
    assert state.revision == 62 and not state.registry
    side = ROOT / 'examples/routeb_fourier_gradient_lean'
    receipt = side / 'FINAL_RECEIPT.md'
    source = side / 'output/run-weWkW1WN/FourierGradient.lean'
    olean = side / 'output/run-weWkW1WN/FourierGradient.olean'
    log = side / 'output/run-weWkW1WN/terminal.log'
    old_graph = ROOT / 'artifacts/routeb_6dof/block45-obligations-v26.json'
    graph_path = ROOT / 'artifacts/routeb_6dof/block45-obligations-v27.json'
    for path in (receipt, source, olean, log, old_graph):
        assert path.is_file()
    assert not graph_path.exists()
    assert sha(source) == '2bf64904920f1ef6a46cd79d5ba10b14320f60347448bd55becc5c27fe29efeb'
    assert sha(olean) == '5955f79dbaf7667fa1106cf8f93905cf77d18c355c7a53890bfbdf2db5f3ac87'
    log_text = log.read_text(encoding='utf-8')
    receipt_text = receipt.read_text(encoding='utf-8')
    for marker in ('FourierGradient_COMPILE_EXIT_CODE=0',
                   'VERIFY_EXIT_CODE=0', 'SNAPSHOT_HASHES_UNCHANGED=true',
                   'hasDerivAt_fourierPotential_coordinate', 'propext'):
        assert marker in log_text + receipt_text
    assert 'sorryAx' not in log_text and 'sorry' not in source.read_text(encoding='utf-8').lower()

    state.event(
        'routeb_b45_2_fourier_gradient_compiled',
        receipt=ref(receipt), source=ref(source), olean=ref(olean),
        terminal_log=ref(log), compile_exit=0, verify_exit=0,
        standard_axioms_only=True, source_independent=True,
        analytic_gradient=True, finite_difference_binding=False,
        physical_source_binding=False, registry_promoted=False,
        formal_certificate_allowed=False)

    graph = json.loads(old_graph.read_text(encoding='utf-8'))
    graph.update(schema='routeb-proposed-proof-dag-v27',
                 supersedes='block45-obligations-v26.json',
                 active_strategy='compose_fourier_gradient_adapter')
    nodes = {node['id']: node for node in graph['nodes']}
    nodes['B45-2_fourier_gradient_coordinate'] = {
        'id': 'B45-2_fourier_gradient_coordinate',
        'status': 'compiled_candidate_comparator_pending',
        'dependencies': [],
        'source': '../../examples/routeb_fourier_gradient_lean/FourierGradient.lean',
        'statement': (
            'Kernel-check the exact coordinate derivative of a finite Fourier '
            'potential and expose the remaining deployed-potential adapter.'),
        'verification': {
            'receipt': str(receipt.resolve()), 'run': 'output/run-weWkW1WN',
            'compile_exit': 0, 'verify_exit': 0,
            'standard_axioms_only': True,
            'source_sha256': sha(source), 'olean_sha256': sha(olean)}}
    for obligation in graph['source_binding_obligations']:
        if obligation['id'] == 'B45-2':
            subnodes = obligation.setdefault('subnodes', [])
            if 'B45-2_fourier_gradient_coordinate' not in subnodes:
                subnodes.insert(0, 'B45-2_fourier_gradient_coordinate')
            obligation['analytic_gradient'] = 'compiled_candidate_comparator_pending'
            obligation['finite_difference_binding'] = 'open'
            obligation['physical_source_binding'] = 'open'
    graph['next_frontier'] = [
        'B45-1 physical DH frame/axis/index binding',
        'B45-1.c body mass Fourier evaluator for all q',
        'B45-1.g comparator-backed q=0 bridge admission',
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
    backup = ROOT / 'artifacts/routeb_storage_checkpoint_20260905/state-before-revision62.json'
    assert not backup.exists()
    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    m4 = next(node for node in state.nodes.values()
              if node.name.startswith('M4.') and node.name != 'M4.correlated_momentum_closure')
    m4.metadata.setdefault('proposed_mathematical_dags', []).append(ref(graph_path))
    m4.metadata['next_mathematical_frontier'] = graph['next_frontier']
    state.event(
        'routeb_b45_2_fourier_gradient_checkpoint', proposed_dag=ref(graph_path),
        original_target_unchanged=True, actual_J_proved=False,
        formal_certificate_allowed=False, comparator_accepted=False,
        registry_promotions=0, broad_regression_run=False,
        deployed_potential_adapter_open=True)
    store.save(state)
    print(json.dumps(dict(revision=state.revision, nodes=len(state.nodes),
                         graph_nodes=len(nodes), registry=len(state.registry),
                         formal_certificate_allowed=False)))


if __name__ == '__main__':
    main()
