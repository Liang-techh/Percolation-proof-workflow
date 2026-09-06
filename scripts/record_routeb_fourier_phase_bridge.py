"""Record the successful Laurent-to-exponential phase bridge."""
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
    assert state.revision == 58 and len(state.nodes) == 64 and not state.registry
    side = ROOT / 'examples/routeb_b45_fourier_normal_form'
    receipt = side / 'FINAL_RECEIPT.md'
    source = side / 'output/run-pFcZfDCg/FourierNormalForm.lean'
    olean = side / 'output/run-pFcZfDCg/FourierNormalForm.olean'
    log = side / 'output/run-pFcZfDCg/terminal.log'
    old_graph = ROOT / 'artifacts/routeb_6dof/block45-obligations-v22.json'
    graph_path = ROOT / 'artifacts/routeb_6dof/block45-obligations-v23.json'
    for path in (receipt, source, olean, log, old_graph):
        assert path.is_file()
    assert not graph_path.exists()
    assert sha(source) == '56ec2f2d29a22942bcb83a3ba98197ae1ce4d607340072b81c013b8d358d3218'
    assert sha(olean) == '49d9dfaf04dae88f70301d697c26548ef65b5dcb3cd750b7a79eb2a7715917f1'
    text = receipt.read_text(encoding='utf-8') + log.read_text(encoding='utf-8')
    for marker in ('Successful run: `output/run-pFcZfDCg`',
                   'fourier_phase_bridge', 'FourierNormalForm_COMPILE_EXIT_CODE=0',
                   'VERIFY_EXIT_CODE=0', 'propext'):
        assert marker in text
    assert 'sorryAx' not in log.read_text(encoding='utf-8')

    state.event(
        'routeb_b45_1_fourier_phase_bridge_compiled',
        receipt=ref(receipt), source=ref(source), olean=ref(olean),
        terminal_log=ref(log), compile_exit=0, verify_exit=0,
        standard_axioms_only=True, exp_trig_bridge=True,
        full_mass_lift=False, physical_source_binding=False,
        registry_promoted=False, formal_certificate_allowed=False)
    graph = json.loads(old_graph.read_text(encoding='utf-8'))
    graph.update(schema='routeb-proposed-proof-dag-v23',
                 supersedes='block45-obligations-v22.json',
                 active_strategy='lift_fourier_phase_bridge_into_mass')
    nodes = {node['id']: node for node in graph['nodes']}
    nodes['B45-1_fourier_phase_bridge'] = {
        'id': 'B45-1_fourier_phase_bridge',
        'status': 'compiled_candidate_comparator_pending',
        'dependencies': ['B45-1_fourier_single_step_normal_form'],
        'source': '../../examples/routeb_b45_fourier_normal_form/FourierNormalForm.lean',
        'statement': (
            'Kernel-check that the Laurent atom z=exp(I*q) yields the expected '
            'cosine/sine values for phases 1, I, and -I.'),
        'verification': {
            'receipt': str(receipt.resolve()), 'run': 'output/run-pFcZfDCg',
            'compile_exit': 0, 'verify_exit': 0, 'standard_axioms_only': True,
            'source_sha256': sha(source), 'olean_sha256': sha(olean)}}
    nodes['B45-1_mass_functional_identity']['dependencies'] = [
        'source_semantics', 'B45-1_fourier_single_step_normal_form',
        'B45-1_fourier_phase_bridge']
    nodes['B45-1_mass_functional_identity']['compiled_precursors'] = [
        'B45-1_fourier_single_step_normal_form', 'B45-1_fourier_phase_bridge']
    nodes['source_semantics']['fourier_normal_form']['exp_trig_bridge'] = 'compiled_candidate'
    nodes['source_semantics']['fourier_normal_form']['phase_receipt'] = str(receipt.resolve())
    nodes['source_semantics']['fourier_normal_form']['full_mass_lift'] = 'open'
    for obligation in graph['source_binding_obligations']:
        if obligation['id'] == 'B45-1':
            if 'B45-1_fourier_phase_bridge' not in obligation['subnodes']:
                obligation['subnodes'].insert(1, 'B45-1_fourier_phase_bridge')
            obligation['phase_bridge'] = 'compiled_candidate_comparator_pending'
    graph['next_frontier'] = [
        'B45-1.2 frame recursion and parent-axis lift',
        'B45-1.c body mass Fourier evaluator for all q',
        'B45-1.g comparator-backed q=0 bridge admission',
        'B45-1.i Float64 enclosure bridge',
        'B45-2 potential and gradient reconstruction',
        'B45-3 H0 and gradient-zero binding',
        'B45-4 Christoffel FD binding',
        'B45-5_residual_domain_bound',
        'positive_supply_eta_physical_projection_and_relative_bound',
        'positive_supply_two_regime_physical_assembly',
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
    backup = ROOT / 'artifacts/routeb_storage_checkpoint_20260905/state-before-revision58.json'
    assert not backup.exists()
    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    m4 = next(node for node in state.nodes.values()
              if node.name.startswith('M4.') and node.name != 'M4.correlated_momentum_closure')
    m4.metadata.setdefault('proposed_mathematical_dags', []).append(ref(graph_path))
    m4.metadata['next_mathematical_frontier'] = graph['next_frontier']
    state.event(
        'routeb_b45_1_phase_bridge_checkpoint', proposed_dag=ref(graph_path),
        original_target_unchanged=True, actual_J_proved=False,
        formal_certificate_allowed=False, comparator_accepted=False,
        registry_promotions=0, broad_regression_run=False)
    store.save(state)
    print(json.dumps(dict(revision=state.revision, nodes=len(state.nodes),
                         graph_nodes=len(nodes), registry=len(state.registry),
                         formal_certificate_allowed=False)))


if __name__ == '__main__':
    main()
