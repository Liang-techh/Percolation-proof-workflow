"""Record the B45-5 residual decomposition and supply-frontier obstructions."""
import hashlib
import json
import shutil

from record_routeb_port_progress import ROOT, ref
from percolation_workflow.store import StateStore


def main():
    store = StateStore(ROOT / 'artifacts/routeb_6dof/state.json')
    state = store.load()
    assert state.revision == 53 and len(state.nodes) == 64 and not state.registry
    mismatch = ROOT / 'artifacts/routeb_6dof/B45-5-mismatch-plan.md'
    supply = ROOT / 'artifacts/routeb_6dof/positive-supply-frontier.md'
    old_graph = ROOT / 'artifacts/routeb_6dof/block45-obligations-v17.json'
    graph_path = ROOT / 'artifacts/routeb_6dof/block45-obligations-v18.json'
    assert mismatch.is_file() and supply.is_file() and old_graph.is_file()
    assert not graph_path.exists()
    assert hashlib.sha256(mismatch.read_bytes()).hexdigest() == (
        '5c5e7cc9f382a84ad228d28bf71c9fb46632ef3f79f3bc92869c9c7927d530f9')
    mt = mismatch.read_text(encoding='utf-8')
    st = supply.read_text(encoding='utf-8')
    for marker in ('kc=0.05', 'ρ_kc,B = (q5/100, q4/200)',
                   'l_B = ρ_C + ρ_G + ρ_mgl + ρ_kc + ρ_mass + ρ_remote',
                   'OPEN / mismatch decomposition available'):
        assert marker in mt
    for marker in ('Relative-error lemma', 'Absolute-error obstruction',
                   '36802229/24000000', 'direct gate', 'J<=1'):
        assert marker in st

    state.event(
        'routeb_b45_5_residual_decomposition_audit',
        report=ref(mismatch), status='open_mismatch_decomposition_available',
        rho_kc='(q5/100,q4/200)', pmi_source_matched=False,
        uniform_residual_bound=False, registry_promoted=False,
        formal_certificate_allowed=False)
    state.event(
        'routeb_positive_supply_frontier_audit',
        report=ref(supply), status='open_two_regime_eta_frontier',
        relative_eta_threshold='36802229/24000000',
        absolute_eta_denominator_obstruction=True,
        direct_gate_recommended=True, equilibrium_floor_open=True,
        registry_promoted=False, formal_certificate_allowed=False)

    graph = json.loads(old_graph.read_text(encoding='utf-8'))
    graph.update(
        schema='routeb-proposed-proof-dag-v18',
        supersedes='block45-obligations-v17.json',
        active_strategy='explicit_residual_and_two_regime_supply_gate')
    nodes = {node['id']: node for node in graph['nodes']}
    nodes['B45-5_pmi_residual_decomposition'] = {
        'id': 'B45-5_pmi_residual_decomposition',
        'status': 'open_conditional_algebra',
        'dependencies': ['source_semantics', 'B45-1_mass_functional_identity'],
        'statement': (
            'Using the actual descriptor equation, prove l_B = rho_C + rho_G '
            '+ rho_mgl + rho_kc + rho_mass + rho_remote, with exact '
            'rho_kc=(q5/100,q4/200). Preserve PMI as a nominal model; do not '
            'identify it with DH dynamics.'),
        'report': str(mismatch.resolve()),
        'exact_kc_residual': '(q5/100,q4/200)'}
    nodes['B45-5_residual_domain_bound'] = {
        'id': 'B45-5_residual_domain_bound',
        'status': 'open',
        'dependencies': ['B45-5_pmi_residual_decomposition',
                         'B45-1_float64_enclosure_bridge'],
        'statement': (
            'Bound all C, gravity/mgl, kc, block-mass and remote-acceleration '
            'residual terms on the first-exit certification domain, including '
            'source and Float64 semantics.'),
        'report': str(mismatch.resolve())}
    nodes['B45-5_model_replacement_gate'] = {
        'id': 'B45-5_model_replacement_gate',
        'status': 'open_decision_gate',
        'dependencies': ['B45-5_residual_domain_bound'],
        'statement': (
            'If the explicit PMI residual/Schur bound closes, retain PMI; '
            'otherwise replace the nominal model by a source-definitional '
            'descriptor model. Neither branch is currently closed.'),
        'report': str(mismatch.resolve())}
    nodes['positive_supply_relative_eta_lemma'] = {
        'id': 'positive_supply_relative_eta_lemma',
        'status': 'open',
        'dependencies': ['positive_supply_gate', 'source_semantics'],
        'statement': (
            'Bind eta_u=u dot eta_vec and prove a relative bound '
            '|eta_u|<=kappa rho; then the terminal denominator is uniformly '
            'positive when kappa < 36802229/24000000.'),
        'report': str(supply.resolve())}
    nodes['positive_supply_two_regime_direct_gate'] = {
        'id': 'positive_supply_two_regime_direct_gate',
        'status': 'open',
        'dependencies': ['positive_supply_gate', 'positive_supply_relative_eta_lemma'],
        'statement': (
            'Avoid division near rho=0 by combining a direct quadratic gate and '
            'an explicit equilibrium supply floor with the relative-eta regime.'),
        'report': str(supply.resolve())}
    nodes['positive_supply_equilibrium_floor'] = {
        'id': 'positive_supply_equilibrium_floor',
        'status': 'open',
        'dependencies': ['positive_supply_gate', 'source_semantics'],
        'statement': (
            'Either prove eta(0,0)=0 from source semantics or bound the exact '
            'equilibrium cost eta dot RLR eta over the admitted error set; '
            'the current scalar absolute-eta route is insufficient.'),
        'report': str(supply.resolve())}
    nodes['uniform_fixed_identity_scalar_source_gate']['dependencies'] = [
        'fixed_identity_affine_gate', 'origin_quadratic_and_terminal_storage_gate',
        'terminal_gate_formalization', 'correlated_velocity_source_bound',
        'source_semantics', 'B45-5_model_replacement_gate',
        'positive_supply_two_regime_direct_gate',
        'positive_supply_equilibrium_floor']
    for obligation in graph['source_binding_obligations']:
        if obligation['id'] == 'B45-5':
            obligation['status'] = 'decomposed_open_mismatch'
            obligation['subnodes'] = [
                'B45-5_pmi_residual_decomposition',
                'B45-5_residual_domain_bound',
                'B45-5_model_replacement_gate']
            obligation['report'] = str(mismatch.resolve())
            obligation['exact_residual'] = 'rho_kc=(q5/100,q4/200)'
    graph['positive_supply_frontier'] = {
        'report': str(supply.resolve()),
        'status': 'open_two_regime_eta_frontier',
        'relative_eta_threshold': '36802229/24000000',
        'absolute_eta_obstruction': True,
        'direct_gate': 'required near rho=0',
        'equilibrium_floor': 'open'}
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
    backup = ROOT / 'artifacts/routeb_storage_checkpoint_20260905/state-before-revision53.json'
    assert not backup.exists()
    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    m4 = next(node for node in state.nodes.values()
              if node.name.startswith('M4.') and node.name != 'M4.correlated_momentum_closure')
    m4.metadata.setdefault('proposed_mathematical_dags', []).append(ref(graph_path))
    m4.metadata['next_mathematical_frontier'] = graph['next_frontier']
    state.event(
        'routeb_b45_5_supply_frontier_checkpoint',
        proposed_dag=ref(graph_path), original_target_unchanged=True,
        actual_J_proved=False, formal_certificate_allowed=False,
        comparator_accepted=False, registry_promotions=0,
        broad_regression_run=False)
    store.save(state)
    print(json.dumps(dict(revision=state.revision, nodes=len(state.nodes),
                         graph_nodes=len(nodes), B45_5_subnodes=3,
                         supply_subnodes=3, registry=len(state.registry),
                         formal_certificate_allowed=False)))


if __name__ == '__main__':
    main()
