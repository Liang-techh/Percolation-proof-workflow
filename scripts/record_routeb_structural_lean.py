"""Record the structural Lean sidecar and the bounded terminal formalization.

The origin sidecar is a successful pinned compile but has no printed axiom
report; it remains a compiled candidate. The terminal sidecar currently has
only failed attempts and is recorded as an open frontier. Neither can enter
the verified registry through this script.
"""
import hashlib
import json
from pathlib import Path
import shutil

from record_routeb_port_progress import ROOT, ref
from percolation_workflow.store import StateStore


def main():
    store = StateStore(ROOT/'artifacts/routeb_6dof/state.json')
    state = store.load()
    assert state.revision == 48 and len(state.nodes) == 64 and not state.registry
    origin = ROOT/'examples/routeb_origin_quadratic_lean'
    origin_run = origin/'output/run-TIbpu6FN'
    origin_log = origin_run/'terminal.log'
    assert 'OriginQuadratic_COMPILE_EXIT_CODE=0' in origin_log.read_text(encoding='utf-8')
    assert (origin_run/'OriginQuadratic.lean').read_bytes() == (origin/'OriginQuadratic.lean').read_bytes()
    assert hashlib.sha256((origin_run/'OriginQuadratic.olean').read_bytes()).hexdigest() == '42106f99ded794503a116f69f51733decc5882b6bd1b0ba4b631114909c544dd'
    state.event('routeb_origin_quadratic_lean_compiled_candidate', source=ref(origin/'OriginQuadratic.lean'),
                olean=ref(origin_run/'OriginQuadratic.olean'), log=ref(origin_log),
                pinned_lean='4.33.1', mathlib_commit='0df444a360eaa60ab8c11dca51a86af692955474',
                axiom_report_present=False, comparator_accepted=False,
                registry_promoted=False, formal_certificate_allowed=False)
    terminal = ROOT/'examples/routeb_terminal_gate_lean'
    terminal_failed = terminal/'output/run-FELXKx7A/terminal.log'
    assert 'TerminalGate_COMPILE_EXIT_CODE=1' in terminal_failed.read_text(encoding='utf-8')
    state.event('routeb_terminal_gate_lean_open_after_failed_repairs', source=ref(terminal/'TerminalGate.lean'),
                failed_log=ref(terminal_failed), sorryAx_in_failed_output_rejected=True,
                exact_python_gate_remains_active=True, registry_promoted=False,
                formal_certificate_allowed=False)
    graph_path = ROOT/'artifacts/routeb_6dof/block45-obligations-v13.json'
    assert not graph_path.exists()
    graph = json.loads((graph_path.parent/'block45-obligations-v12.json').read_text(encoding='utf-8'))
    graph.update(schema='routeb-proposed-proof-dag-v13', supersedes='block45-obligations-v12.json',
                 active_strategy='formal_origin_gate_then_terminal_supply_design')
    nodes = {node['id']: node for node in graph['nodes']}
    nodes['origin_quadratic_and_terminal_storage_gate']['statement'] = (
        'Formalize the full origin quadratic necessary condition and terminal residual-energy gate. '
        'The exact 2x2 principal obstruction is compiled in OriginQuadratic; the bounded terminal Lean leaf still has failed attempts.')
    nodes['origin_quadratic_and_terminal_storage_gate']['formal_sidecars'] = [
        dict(name='RouteBOriginQuadratic.negSemidefinite_of_originQuadraticLittleO',
             source=str((origin/'OriginQuadratic.lean').resolve()), status='compiled_no_axiom_report'),
        dict(name='RouteBOriginQuadratic.neg_not_quadNonnegative_zero_diagonal_offdiag',
             source=str((origin/'OriginQuadratic.lean').resolve()), status='compiled_no_axiom_report')]
    nodes['origin_quadratic_and_terminal_storage_gate']['evidence'] = [
        str((origin_run/'terminal.log').resolve()), str((origin_run/'OriginQuadratic.olean').resolve())]
    nodes['terminal_gate_formalization'] = dict(
        id='terminal_gate_formalization', status='open', dependencies=['actual_energy_storage_source_derivative'],
        statement='Exact terminal Python obstruction is recorded; Lean bounded interface remains open after two failed snapshots. Need a1-positive/positive-supply theorem with source residual hypotheses.')
    nodes['uniform_fixed_identity_scalar_source_gate']['dependencies'] = [
        'fixed_identity_affine_gate', 'origin_quadratic_and_terminal_storage_gate',
        'terminal_gate_formalization', 'correlated_velocity_source_bound']
    graph['next_frontier'] = [
        'add_axiom_report_and_comparator_for_origin_quadratic_leaf',
        'repair_terminal_gate_formalization_without_sorry',
        'design_a1_positive_or_certified_integrated_supply',
        'uniform_fixed_identity_scalar_source_gate', 'eta_and_AE_source_binding', 'all_domain_continuation']
    graph['rejected_shortcuts'].append(
        'Promote a successful Lean compile without an axiom report, or failed terminal output containing sorryAx, into registry evidence.')
    graph['nodes'] = list(nodes.values())
    assert len(nodes) == len(graph['nodes'])
    def visit(key, stack):
        assert key not in stack
        for dep in nodes[key]['dependencies']:
            visit(dep, stack | {key})
    for key in nodes:
        visit(key, set())
    shutil.copy2(store.path, ROOT/'artifacts/routeb_storage_checkpoint_20260905/state-before-revision48.json')
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    m4 = next(node for node in state.nodes.values() if node.name.startswith('M4.') and node.name != 'M4.correlated_momentum_closure')
    m4.metadata.setdefault('proposed_mathematical_dags', []).append(ref(graph_path))
    m4.metadata['next_mathematical_frontier'] = graph['next_frontier']
    state.event('routeb_structural_lean_checkpoint', proposed_dag=ref(graph_path),
                origin_compile=ref(origin_log), terminal_failed=ref(terminal_failed),
                original_target_unchanged=True, actual_J_proved=False,
                formal_certificate_allowed=False, comparator_accepted=False,
                registry_promotions=0, broad_regression_run=False)
    store.save(state)
    print(json.dumps(dict(revision=state.revision, nodes=len(state.nodes), registry=len(state.registry),
                          origin_compiled=True, terminal_formalization_open=True,
                          formal_certificate_allowed=False)))


if __name__ == '__main__': main()
