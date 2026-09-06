"""Record the narrow physical frame-binding audit without promoting it."""
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
    assert state.revision == 63 and not state.registry
    report = ROOT / 'artifacts/routeb_6dof/B45-1-physical-frame-binding-audit.md'
    old_graph = ROOT / 'artifacts/routeb_6dof/block45-obligations-v27.json'
    graph_path = ROOT / 'artifacts/routeb_6dof/block45-obligations-v28.json'
    assert report.is_file() and old_graph.is_file() and not graph_path.exists()
    assert sha(report) == '2729b67703bbed85acbe26961a5eb2db28098bee371d931a337d176d589497fc'
    text = report.read_text(encoding='utf-8')
    for marker in ('DH rows use', 'OPEN`/`UNKNOWN',
                   'Float64 bridge', 'source binding'):
        assert marker in text

    state.event(
        'routeb_b45_1_physical_frame_binding_audit', report=ref(report),
        report_sha256=sha(report), source_read_only=True,
        template_parameter_phase_consistent=True,
        parent_current_order_consistent=True,
        origin_com_jacobian_text_consistent=True,
        function_level_fin6_binding=False, float64_bridge=False,
        physical_source_binding=False, registry_promoted=False,
        formal_certificate_allowed=False)

    graph = json.loads(old_graph.read_text(encoding='utf-8'))
    graph.update(schema='routeb-proposed-proof-dag-v28',
                 supersedes='block45-obligations-v27.json',
                 active_strategy='close_physical_frame_adapter')
    nodes = {node['id']: node for node in graph['nodes']}
    nodes['B45-1_physical_frame_binding_audit'] = {
        'id': 'B45-1_physical_frame_binding_audit',
        'status': 'source_audit_open',
        'dependencies': ['B45-1_frame_recursion', 'B45-1_fourier_phase_bridge'],
        'source': '../../artifacts/routeb_6dof/B45-1-physical-frame-binding-audit.md',
        'statement': (
            'Audit the deployed Julia/Python DH frame, phase, parent-axis, '
            'origin, COM, and Jacobian conventions against the Lean interface; '
            'text-level consistency is recorded while function-level Fin 6 '
            'binding and Float64 enclosure remain open.'),
        'evidence': {
            'report': str(report.resolve()), 'report_sha256': sha(report),
            'template_parameter_phase_consistent': True,
            'parent_current_order_consistent': True,
            'origin_com_jacobian_text_consistent': True,
            'function_level_fin6_binding': False,
            'float64_bridge': False}}
    for obligation in graph['source_binding_obligations']:
        if obligation['id'] == 'B45-1':
            obligation['physical_frame_binding_audit'] = 'source_audit_open'
            obligation['function_level_fin6_binding'] = 'open'
            obligation['float64_bridge'] = 'open'
            obligation['audit_report'] = str(report.resolve())
    identity = nodes['B45-1_mass_functional_identity']
    identity.setdefault('audit_precursors', [])
    if 'B45-1_physical_frame_binding_audit' not in identity['audit_precursors']:
        identity['audit_precursors'].append('B45-1_physical_frame_binding_audit')
    graph['next_frontier'] = [
        'B45-1 function-level Fin6 frame/axis/index adapter',
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
    backup = ROOT / 'artifacts/routeb_storage_checkpoint_20260905/state-before-revision63.json'
    assert not backup.exists()
    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    m4 = next(node for node in state.nodes.values()
              if node.name.startswith('M4.') and node.name != 'M4.correlated_momentum_closure')
    m4.metadata.setdefault('proposed_mathematical_dags', []).append(ref(graph_path))
    m4.metadata['next_mathematical_frontier'] = graph['next_frontier']
    state.event(
        'routeb_b45_1_physical_frame_binding_checkpoint', proposed_dag=ref(graph_path),
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
