"""Persist exact candidate obstructions and the next structural frontier.

This importer records diagnostics and proposed DAG metadata only. It never
promotes a candidate or a numerical/exact audit into the verified registry.
"""
import hashlib
import json
from pathlib import Path
import shutil

from record_routeb_port_progress import ROOT, ref
from percolation_workflow.store import StateStore


def audit_run(run):
    before = json.loads((run/'before_run.json').read_text(encoding='utf-8'))
    for name, digest in before['snapshots'].items():
        assert ref(run/name)['sha256'] == digest
    log = (run/'terminal.log').read_text(encoding='utf-8', errors='replace')
    assert 'AUDIT_EXIT_CODE=0' in log
    result = run/'results.json'
    assert result.is_file()
    return result


def main():
    store = StateStore(ROOT/'artifacts/routeb_6dof/state.json')
    state = store.load()
    assert state.revision == 47 and len(state.nodes) == 64 and not state.registry
    assert not any(n.status == 'in_progress' for n in state.nodes.values())
    origin = ROOT/'examples/routeb_storage_origin_gate/output/run-20260905T211357Z-f7fae1f0'
    terminal = ROOT/'examples/routeb_terminal_gate/output/run-20260905T212324Z-bf0ed996'
    origin_result = audit_run(origin)
    terminal_result = audit_run(terminal)
    origin_data = json.loads(origin_result.read_text(encoding='utf-8'))
    terminal_data = json.loads(terminal_result.read_text(encoding='utf-8'))
    assert origin_data['uniform_zero_supply_candidate_rejected']
    assert terminal_data['candidate_rejected']
    assert not origin_data['physical_target_refuted'] and not terminal_data['physical_target_refuted']
    assert not origin_data['formal_certificate_allowed'] and not terminal_data['formal_certificate_allowed']
    state.event('routeb_exact_origin_quadratic_obstruction', result=ref(origin_result),
                candidate_run=origin_data['candidate_run'],
                exact_vdot=origin_data['Vdot'], initial_norm_squared=origin_data['initial_norm_squared'],
                source_frequency_restriction=True, candidate_only=True,
                entire_storage_family_rejected=False, registry_promoted=False)
    state.event('routeb_exact_terminal_neighborhood_obstruction', result=ref(terminal_result),
                candidate_run=terminal_data['candidate'], exact_total=terminal_data['total'],
                tau=terminal_data['tau'], a1=terminal_data['a1'], candidate_only=True,
                entire_storage_family_rejected=False, registry_promoted=False)

    graph_path = ROOT/'artifacts/routeb_6dof/block45-obligations-v12.json'
    assert not graph_path.exists()
    graph = json.loads((graph_path.parent/'block45-obligations-v11.json').read_text(encoding='utf-8'))
    graph.update(schema='routeb-proposed-proof-dag-v12', supersedes='block45-obligations-v11.json',
                 active_strategy='structural_origin_and_terminal_gate_before_uniform_source_bound')
    graph['evidence_artifacts'] = [
        dict(kind='exact_candidate_rejection', id='second_zero_supply_origin',
             path=str(origin_result.resolve()), sha256=hashlib.sha256(origin_result.read_bytes()).hexdigest(),
             status='diagnostic_not_theorem'),
        dict(kind='exact_candidate_rejection', id='second_zero_supply_terminal',
             path=str(terminal_result.resolve()), sha256=hashlib.sha256(terminal_result.read_bytes()).hexdigest(),
             status='diagnostic_not_theorem')]
    nodes = {n['id']: n for n in graph['nodes']}
    nodes['origin_quadratic_and_terminal_storage_gate']['statement'] = (
        'Prove/enforce the full13x13 origin quadratic necessary condition over time and the terminal residual-energy gate. '
        'The current second LP is rejected exactly at an allowed q6/v6 initial state and at a fixed terminal-neighborhood state; '
        'a1>0 or certified positive supply remains open.')
    nodes['storage_collocation_and_ramp_repair']['statement'] = (
        'Exactly two bounded LP searches are retained. Both zero-supply candidates are rejected by exact source-level witnesses; '
        'the original target and all other storage families remain open. No third LP is authorized by this checkpoint.')
    nodes['uniform_fixed_identity_scalar_source_gate']['dependencies'] = [
        'fixed_identity_affine_gate', 'origin_quadratic_and_terminal_storage_gate', 'correlated_velocity_source_bound']
    graph['rejected_shortcuts'].append(
        'Run repeated coefficient fitting after exact origin and terminal structural obstructions without first changing the storage ansatz or adding certified supply.')
    graph['next_frontier'] = [
        'formalize_origin_negative_semidefinite_principal_gate',
        'formalize_terminal_first_order_residual_gate',
        'design_a1_positive_or_certified_integrated_supply',
        'uniform_fixed_identity_scalar_source_gate',
        'eta_and_AE_source_binding', 'all_domain_continuation']
    graph['nodes'] = list(nodes.values())
    # DAG integrity: dependencies are identifiers in the same proposed graph.
    assert len(nodes) == len(graph['nodes'])
    def visit(key, stack):
        assert key not in stack
        for dep in nodes[key]['dependencies']:
            visit(dep, stack | {key})
    for key in nodes:
        visit(key, set())
    shutil.copy2(store.path, ROOT/'artifacts/routeb_storage_checkpoint_20260905/state-before-revision47.json')
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    m4 = next(n for n in state.nodes.values() if n.name.startswith('M4.') and n.name != 'M4.correlated_momentum_closure')
    m4.metadata.setdefault('proposed_mathematical_dags', []).append(ref(graph_path))
    m4.metadata['next_mathematical_frontier'] = graph['next_frontier']
    state.event('routeb_structural_gate_checkpoint', proposed_dag=ref(graph_path),
                origin_obstruction=ref(origin_result), terminal_obstruction=ref(terminal_result),
                original_target_unchanged=True, actual_J_proved=False,
                formal_certificate_allowed=False, comparator_accepted=False,
                registry_promotions=0, broad_regression_run=False)
    store.save(state)
    print(json.dumps(dict(revision=state.revision, nodes=len(state.nodes), registry=len(state.registry),
                          formal_certificate_allowed=False, candidate_obstructions=2)))


if __name__ == '__main__':
    main()
