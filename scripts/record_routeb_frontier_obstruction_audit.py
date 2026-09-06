"""Record strict obstruction audits without promoting any theorem candidate."""
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
    assert state.revision == 98 and not state.registry
    positive = ROOT / 'artifacts/routeb_6dof/B45-5-positive-supply-audit-20260906.md'
    mismatch = ROOT / 'artifacts/routeb_6dof/B45-5-mismatch-plan.md'
    old_graph = ROOT / 'artifacts/routeb_6dof/block45-obligations-v58.json'
    graph_path = ROOT / 'artifacts/routeb_6dof/block45-obligations-v59.json'
    backup = ROOT / 'artifacts/routeb_storage_checkpoint_20260905/state-before-revision99.json'
    for path in (positive, mismatch, old_graph):
        assert path.is_file()
    assert not graph_path.exists() and not backup.exists()
    state.event('routeb_frontier_obstruction_audit',
                positive_supply_audit=ref(positive),
                residual_mismatch_plan=ref(mismatch),
                positive_supply_sha256=sha(positive),
                residual_mismatch_sha256=sha(mismatch),
                relative_eta_absolute_bound_obstructed=True,
                residual_domain_bound_obstructed_by_unbounded_remote_acceleration=True,
                registry_promotions=0, formal_certificate_allowed=False)
    graph = json.loads(old_graph.read_text(encoding='utf-8'))
    graph.update(schema='routeb-proposed-proof-dag-v59',
                 supersedes='block45-obligations-v58.json',
                 active_strategy='contract_mass_to_regularized_source_mass')
    nodes = {node['id']: node for node in graph['nodes']}
    nodes['positive_supply_relative_eta_lemma']['obstruction_audit'] = {
        'status': 'blocked_under_current_absolute_error_assumptions',
        'source': str(positive.resolve()),
        'required_alternatives': ['eta_at_equilibrium_zero',
                                  'state_relative_error',
                                  'direct_gate_with_equilibrium_floor']}
    nodes['positive_supply_equilibrium_floor']['obstruction_audit'] = {
        'status': 'open_exact_next_lemma',
        'source': str(positive.resolve()),
        'necessary_cost_if_eta_nonzero': 'eta^T RLR eta'}
    nodes['B45-5_residual_domain_bound']['obstruction_audit'] = {
        'status': 'blocked_without_global_acceleration_and_mass_enclosures',
        'source': str(mismatch.resolve()),
        'missing_bounds': ['M_BB-D0', 'M_BD', 'a_B', 'a_D', 'FD_remainder']}
    graph['next_frontier'] = [
        'B45-1 sourceBodyMass/sourceContract exact index binding',
        'B45-1 bind routeBFrameSlot to homogeneousPrefix using transport lemma',
        'B45-1 apply source mass-table exact candidate to contract mass sum',
        'B45-1 bind regularized mass entries to Fourier evaluator and canonical CSV coefficients',
        'B45-1 prove Fourier evaluator equals six-body contract sum',
        'B45-1.i Float64 enclosure bridge',
        'B45-5 obtain global enclosures for M_BB-D0, M_BD, a_B, a_D and FD remainder',
        'B45-5 bind sourceBlockForce to expectedSourceForce',
        'B45-5 bind sourceBlockForce to sourceDescriptorRhs',
        'positive_supply prove eta(0)=0 or exact equilibrium floor',
        'positive_supply prove state-relative eta scaling or commit direct-gate branch',
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
    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    state.event('routeb_frontier_obstruction_checkpoint',
                proposed_dag=ref(graph_path), original_target_unchanged=True,
                residual_domain_bound_open=True, relative_eta_route_open=True,
                formal_certificate_allowed=False, registry_promotions=0,
                broad_regression_run=False)
    store.save(state)
    print({'revision': state.revision, 'graph_nodes': len(nodes),
           'registry': len(state.registry), 'formal_certificate_allowed': False})


if __name__ == '__main__':
    main()
