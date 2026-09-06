"""Record the exact conditional B45-5 residual decomposition candidate."""
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
    assert state.revision == 90 and not state.registry
    side = ROOT / 'examples/routeb_b45_5_residual_decomposition_lean'
    report = ROOT / 'artifacts/routeb_6dof/B45-5-positive-supply-audit-20260906.md'
    receipt = side / 'FINAL_RECEIPT.md'
    source = side / 'output/run-AeO1JYiI/ResidualDecomposition.lean'
    olean = side / 'output/run-AeO1JYiI/ResidualDecomposition.olean'
    log = side / 'output/run-AeO1JYiI/terminal.log'
    old_graph = ROOT / 'artifacts/routeb_6dof/block45-obligations-v54.json'
    graph_path = ROOT / 'artifacts/routeb_6dof/block45-obligations-v55.json'
    for path in (report, receipt, source, olean, log, old_graph):
        assert path.is_file()
    assert not graph_path.exists()
    assert sha(source) == 'efb2222f53d9fbc6ed18927c94b09a15ccc9f6eba9c3e96e7a9b756c95053d2e'
    assert sha(olean) == '9835982a5ea3899010e9777df5eafefab24a6ebb6d10766d11b1176b23017c0f'
    text = log.read_text(encoding='utf-8') + receipt.read_text(encoding='utf-8')
    for marker in ('ResidualDecomposition_COMPILE_EXIT_CODE=0',
                   'VERIFY_EXIT_CODE=0', 'SOURCE_RESTRICTION_CHECK=PASSED',
                   'propext', 'Classical.choice', 'Quot.sound'):
        assert marker in text
    assert 'sorryAx' not in text

    state.event(
        'routeb_b45_5_residual_decomposition_compiled',
        receipt=ref(receipt), source=ref(source), olean=ref(olean),
        terminal_log=ref(log), compile_exit=0, verify_exit=0,
        standard_axioms_only=True, conditional_source_descriptor=True,
        registry_promoted=False, formal_certificate_allowed=False)

    graph = json.loads(old_graph.read_text(encoding='utf-8'))
    graph.update(schema='routeb-proposed-proof-dag-v55',
                 supersedes='block45-obligations-v54.json',
                 active_strategy='exact_b45_5_residual_decomposition_then_source_binding')
    nodes = {node['id']: node for node in graph['nodes']}
    nodes['B45-5_residual_decomposition_exact_lean'] = {
        'id': 'B45-5_residual_decomposition_exact_lean',
        'status': 'compiled_candidate_comparator_pending',
        'dependencies': [],
        'source': '../../examples/routeb_b45_5_residual_decomposition_lean/ResidualDecomposition.lean',
        'statement': ('Kernel-check the conditional exact decomposition '
                      'l_B=rho_C+rho_G+rho_mgl+rho_kc+rho_mass+rho_remote, '
                      'with rho_kc=(q5/100,q4/200).'),
        'verification': {
            'receipt': str(receipt.resolve()), 'run': 'output/run-AeO1JYiI',
            'compile_exit': 0, 'verify_exit': 0,
            'standard_axioms_only': True,
            'source_sha256': sha(source), 'olean_sha256': sha(olean),
            'source_binding': 'explicit_descriptor_premise',
            'uniform_residual_bound': False}}
    parent = nodes['B45-5_pmi_residual_decomposition']
    parent.setdefault('dependencies', [])
    if 'B45-5_residual_decomposition_exact_lean' not in parent['dependencies']:
        parent['dependencies'].append('B45-5_residual_decomposition_exact_lean')
    parent['exact_lean_candidate'] = 'compiled_candidate_comparator_pending'
    parent['source_binding'] = 'open'
    for obligation in graph['source_binding_obligations']:
        if obligation['id'] == 'B45-5':
            subnodes = obligation.setdefault('subnodes', [])
            if 'B45-5_residual_decomposition_exact_lean' not in subnodes:
                subnodes.insert(0, 'B45-5_residual_decomposition_exact_lean')
            obligation['exact_decomposition_candidate'] = 'compiled_candidate_comparator_pending'
            obligation['source_binding'] = 'open'
    graph['positive_supply_frontier']['equilibrium_floor'] = 'open_exact_next_lemma'
    graph['positive_supply_frontier']['relative_scaling_status'] = (
        'open_absolute_projection_does_not_imply_relative_eta')
    graph['next_frontier'] = [
        'B45-5 bind exact decomposition to B45-1..B45-4 source semantics',
        'B45-5_residual_domain_bound',
        'B45-5_model_replacement_gate',
        'positive_supply prove equilibrium vanishing or exact floor',
        'positive_supply two-regime direct gate',
        'actual mass PSD structural source adapter and eta bounds',
        'B45-1 remaining concrete Fourier/source bindings',
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
    backup = ROOT / 'artifacts/routeb_storage_checkpoint_20260905/state-before-revision90.json'
    assert not backup.exists()
    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    state.event('routeb_b45_5_positive_supply_audit_checkpoint',
                report=ref(report), proposed_dag=ref(graph_path),
                original_target_unchanged=True, actual_J_proved=False,
                formal_certificate_allowed=False, comparator_accepted=False,
                registry_promotions=0, broad_regression_run=False,
                selected_lemma='B45-5_residual_decomposition_exact_lean',
                relative_eta_open=True, equilibrium_floor_open=True,
                actual_mass_psd_source_bound_open=True)
    store.save(state)
    print(json.dumps(dict(revision=state.revision, graph_nodes=len(nodes),
                          registry=len(state.registry),
                          formal_certificate_allowed=False)))


if __name__ == '__main__':
    main()

