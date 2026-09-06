"""Record the B45-1 mass-binding decomposition without promoting it."""
import json
from pathlib import Path

from record_routeb_port_progress import ROOT, ref
from percolation_workflow.store import StateStore


def main():
    store = StateStore(ROOT / 'artifacts/routeb_6dof/state.json')
    state = store.load()
    assert state.revision == 52 and len(state.nodes) == 64 and not state.registry
    report = ROOT / 'artifacts/routeb_6dof/B45-1-mass-plan.md'
    graph_path = ROOT / 'artifacts/routeb_6dof/block45-obligations-v17.json'
    old_graph_path = ROOT / 'artifacts/routeb_6dof/block45-obligations-v16.json'
    assert report.is_file() and old_graph_path.is_file() and not graph_path.exists()
    text = report.read_text(encoding='utf-8')
    for marker in (
        'B45-1 质量矩阵绑定审计',
        'q=0', 'Lean `M0`',
        'B45-1.0', 'B45-1.9', 'Float64 bridge',
        'exact-real source contract'):
        assert marker in text

    state.event(
        'routeb_b45_1_mass_plan',
        report=ref(report), status='decomposed_open',
        zero_point_reconstruction=True, full_ideal_function_identity=False,
        float64_rounding_bridge=False, registry_promoted=False,
        formal_certificate_allowed=False)

    graph = json.loads(old_graph_path.read_text(encoding='utf-8'))
    graph.update(
        schema='routeb-proposed-proof-dag-v17',
        supersedes='block45-obligations-v16.json',
        active_strategy='decompose_mass_semantics_before_psd')
    nodes = {node['id']: node for node in graph['nodes']}
    nodes['B45-1_mass_functional_identity'] = {
        'id': 'B45-1_mass_functional_identity',
        'status': 'open',
        'dependencies': ['source_semantics'],
        'statement': (
            'Prove the ideal real DH link/Jacobian mass formula equals the '
            'finite Fourier mass evaluator for every q, with exact index, '
            'parent-axis, midpoint COM, isotropic I_val/3, and coefficient '
            'normalization contracts.'),
        'decomposition': ['B45-1.a constants/index contract',
                          'B45-1.b DH frame/Jacobian normal form',
                          'B45-1.c ideal base mass = Fourier evaluator',
                          'B45-1.d CSV completeness/normalization'],
        'plan_report': str(report.resolve())}
    nodes['B45-1_regularized_mass_adapter'] = {
        'id': 'B45-1_regularized_mass_adapter',
        'status': 'open',
        'dependencies': ['B45-1_mass_functional_identity'],
        'statement': (
            'Prove regularizedMass(q)=FourierMass(q)+(1/1000000) I6 '
            'as an ideal-real adapter, separating the base CSV from the '
            'diagonal regularizer.'),
        'decomposition': ['B45-1.e exact diagonal regularizer',
                          'B45-1.f ideal regularized mass identity'],
        'plan_report': str(report.resolve())}
    nodes['B45-1_zero_point_M0_bridge'] = {
        'id': 'B45-1_zero_point_M0_bridge',
        'status': 'external_exact_candidate_open_lean',
        'dependencies': ['B45-1_regularized_mass_adapter'],
        'statement': (
            'Instantiate q=0 and prove the 36-entry rational identity '
            'regularizedMass(0)=M0; existing CSV audit is evidence, not '
            'a registry theorem.'),
        'evidence': ['CSV FourierMass(0)+1e-6 I=M0 exact audit'],
        'plan_report': str(report.resolve())}
    nodes['B45-1_float64_enclosure_bridge'] = {
        'id': 'B45-1_float64_enclosure_bridge',
        'status': 'open',
        'dependencies': ['B45-1_regularized_mass_adapter'],
        'statement': (
            'Prove a domain-specific operator-norm enclosure between deployed '
            'Julia Float64 mass and ideal-real regularized mass, including '
            'rounding semantics; do not infer it from the ideal identity.'),
        'plan_report': str(report.resolve())}
    source = nodes['source_semantics']
    source['mass_binding_plan'] = {
        'report': str(report.resolve()),
        'status': 'decomposed_open',
        'ideal_function_identity': 'open',
        'zero_point_M0_bridge': 'exact_external_candidate_open_lean',
        'float64_bridge': 'open'}
    for obligation in graph['source_binding_obligations']:
        if obligation['id'] == 'B45-1':
            obligation['status'] = 'decomposed_open'
            obligation['subnodes'] = [
                'B45-1_mass_functional_identity',
                'B45-1_regularized_mass_adapter',
                'B45-1_zero_point_M0_bridge',
                'B45-1_float64_enclosure_bridge']
            obligation['report'] = str(report.resolve())
    graph['next_frontier'] = [
        'B45-1.a constants/index contract',
        'B45-1.b DH frame/Jacobian normal form',
        'B45-1.c ideal base mass = Fourier evaluator',
        'B45-1.d CSV completeness/normalization',
        'B45-1.e/f regularized mass adapter',
        'B45-1.g q=0 M0 bridge in Lean',
        'B45-1.i Float64 enclosure bridge',
        'B45-2 potential and gradient reconstruction',
        'B45-3 H0 and gradient-zero binding',
        'B45-4 Christoffel FD binding',
        'B45-5 repair PMI/actual block equation mismatch',
        'actual mass PSD and eta bounds',
        'positive_supply_gate uniform feasibility and coefficient/J search',
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
    backup = ROOT / 'artifacts/routeb_storage_checkpoint_20260905/state-before-revision52.json'
    assert not backup.exists()
    import shutil
    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    m4 = next(node for node in state.nodes.values()
              if node.name.startswith('M4.') and node.name != 'M4.correlated_momentum_closure')
    m4.metadata.setdefault('proposed_mathematical_dags', []).append(ref(graph_path))
    m4.metadata['next_mathematical_frontier'] = graph['next_frontier']
    state.event(
        'routeb_b45_1_mass_plan_checkpoint',
        proposed_dag=ref(graph_path), original_target_unchanged=True,
        zero_point_reconstruction_only=True, actual_J_proved=False,
        formal_certificate_allowed=False, comparator_accepted=False,
        registry_promotions=0, broad_regression_run=False)
    store.save(state)
    print(json.dumps(dict(revision=state.revision, nodes=len(state.nodes),
                         graph_nodes=len(nodes), B45_1_subnodes=4,
                         registry=len(state.registry),
                         formal_certificate_allowed=False)))


if __name__ == '__main__':
    main()
