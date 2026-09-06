"""Persist the conservative sidecar statement-comparator result."""
import json
from pathlib import Path
import shutil

from record_routeb_port_progress import ROOT, ref
from percolation_workflow.store import StateStore


def main():
    store = StateStore(ROOT/'artifacts/routeb_6dof/state.json')
    state = store.load()
    assert state.revision == 50 and len(state.nodes) == 64 and not state.registry
    side = ROOT/'examples/routeb_structural_comparator'
    runs = sorted((side/'output').glob('run-*/result.json'))
    assert runs
    result_path = runs[-1]
    result = json.loads(result_path.read_text(encoding='utf-8'))
    assert result['accepted'] is True
    assert result['comparator_strength'] == 'pre_comparator_only'
    assert result['upstream_comparator'] is False
    assert result['registry_promotion'] is False
    assert all(target['structural_match'] for target in result['targets'])
    state.event('routeb_structural_statement_comparator_finished', result=ref(result_path),
                config=ref(side/'comparator.json'), accepted=True,
                physical_source_binding=False, upstream_comparator=False,
                registry_promoted=False, formal_certificate_allowed=False)
    graph_path = ROOT/'artifacts/routeb_6dof/block45-obligations-v15.json'
    assert not graph_path.exists()
    graph = json.loads((graph_path.parent/'block45-obligations-v14.json').read_text(encoding='utf-8'))
    graph.update(schema='routeb-proposed-proof-dag-v15', supersedes='block45-obligations-v14.json',
                 active_strategy='structurally_compared_sidecars_source_binding_next')
    nodes = {node['id']: node for node in graph['nodes']}
    nodes['origin_quadratic_and_terminal_storage_gate']['status'] = 'structurally_compared_source_unbound'
    nodes['terminal_gate_formalization']['status'] = 'structurally_compared_source_unbound'
    for key in ('origin_quadratic_and_terminal_storage_gate', 'terminal_gate_formalization'):
        nodes[key]['comparator'] = dict(kind='structural_pre_comparator', result=str(result_path.resolve()),
                                        accepted=True, upstream=False, registry_eligible=False)
    nodes['uniform_fixed_identity_scalar_source_gate']['dependencies'] = [
        'fixed_identity_affine_gate', 'origin_quadratic_and_terminal_storage_gate',
        'terminal_gate_formalization', 'correlated_velocity_source_bound']
    graph['next_frontier'] = [
        'bind source Fourier/DH residual floors to terminal hypotheses',
        'prove actual mass PSD and eta bounds on covered source cells',
        'design_a1_positive_or_certified_integrated_supply',
        'uniform_fixed_identity_scalar_source_gate', 'eta_and_AE_source_binding', 'all_domain_continuation']
    graph['rejected_shortcuts'].append(
        'Treat the local structural comparator as the upstream Challenge/Solution comparator or as a physical-source admission.')
    graph['nodes'] = list(nodes.values())
    assert len(nodes) == len(graph['nodes'])
    def visit(key, stack):
        assert key not in stack
        for dep in nodes[key]['dependencies']:
            visit(dep, stack | {key})
    for key in nodes:
        visit(key, set())
    shutil.copy2(store.path, ROOT/'artifacts/routeb_storage_checkpoint_20260905/state-before-revision50.json')
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    m4 = next(node for node in state.nodes.values() if node.name.startswith('M4.') and node.name != 'M4.correlated_momentum_closure')
    m4.metadata.setdefault('proposed_mathematical_dags', []).append(ref(graph_path))
    m4.metadata['next_mathematical_frontier'] = graph['next_frontier']
    state.event('routeb_structural_comparator_checkpoint', proposed_dag=ref(graph_path),
                original_target_unchanged=True, actual_J_proved=False,
                formal_certificate_allowed=False, comparator_accepted=False,
                registry_promotions=0, broad_regression_run=False)
    store.save(state)
    print(json.dumps(dict(revision=state.revision, nodes=len(state.nodes), registry=len(state.registry),
                          structural_comparator=True, upstream_comparator=False,
                          formal_certificate_allowed=False)))


if __name__ == '__main__': main()
