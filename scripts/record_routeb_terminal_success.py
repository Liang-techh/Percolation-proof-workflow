"""Persist the repaired terminal Lean sidecar without theorem admission."""
import json
from pathlib import Path
import shutil

from record_routeb_port_progress import ROOT, ref
from percolation_workflow.store import StateStore


def main():
    store = StateStore(ROOT/'artifacts/routeb_6dof/state.json')
    state = store.load()
    assert state.revision == 49 and len(state.nodes) == 64 and not state.registry
    side = ROOT/'examples/routeb_terminal_gate_lean'
    run = side/'output/run-WLanCOzI'
    log = run/'terminal.log'
    source = run/'TerminalGate.lean'
    olean = run/'TerminalGate.olean'
    assert 'TerminalGate_COMPILE_EXIT_CODE=0' in log.read_text(encoding='utf-8')
    assert 'VERIFY_EXIT_CODE=0' in log.read_text(encoding='utf-8')
    assert source.read_bytes() == (side/'TerminalGate.lean').read_bytes()
    assert ref(olean)['sha256'] == '0113f2184e87c2239b39420b7b9a8818838ac7f054bb029beb66a969323cd182'
    text = log.read_text(encoding='utf-8')
    for name in ('decayPolynomial_nonneg', 'gate_implies_terminal_lower_bound',
                 'fixed_terminal_gate_failure', 'no_uniform_bZero_gate_of_strict_residual'):
        assert f"'RouteBTerminalGate.{name}' depends on axioms:" in text
        start = text.index(f"'RouteBTerminalGate.{name}' depends on axioms:")
        assert 'sorryAx' not in text[start:text.find('\n', start)+1]
    state.event('routeb_terminal_gate_lean_repaired_success', source=ref(source),
                olean=ref(olean), log=ref(log), receipt=ref(side/'FINAL_RECEIPT.md'),
                exported_theorems=4, standard_axioms_only=True,
                source_unbound=True, comparator_accepted=False,
                registry_promoted=False, formal_certificate_allowed=False)
    graph_path = ROOT/'artifacts/routeb_6dof/block45-obligations-v14.json'
    assert not graph_path.exists()
    graph = json.loads((graph_path.parent/'block45-obligations-v13.json').read_text(encoding='utf-8'))
    graph.update(schema='routeb-proposed-proof-dag-v14', supersedes='block45-obligations-v13.json',
                 active_strategy='origin_and_terminal_structural_gates_ready_for_comparator')
    nodes = {node['id']: node for node in graph['nodes']}
    nodes['terminal_gate_formalization']['status'] = 'compiled_candidate_comparator_pending'
    nodes['terminal_gate_formalization']['statement'] = (
        'Pinned Lean now proves the bounded terminal residual gate and its a1=0 failure interface with explicit hypotheses; '
        'the exact source residual floor and physical binding remain open.')
    nodes['terminal_gate_formalization']['formal_sidecar'] = dict(
        source=str((side/'TerminalGate.lean').resolve()), receipt=str((side/'FINAL_RECEIPT.md').resolve()),
        theorem_count=4, standard_axioms_only=True)
    nodes['origin_quadratic_and_terminal_storage_gate']['status'] = 'compiled_candidates_comparator_pending'
    graph['next_frontier'] = [
        'run_statement_comparator_for_origin_and_terminal_sidecars',
        'bind exact source residual floor to terminal_gate hypotheses',
        'design_a1_positive_or_certified_integrated_supply',
        'uniform_fixed_identity_scalar_source_gate', 'eta_and_AE_source_binding', 'all_domain_continuation']
    graph['rejected_shortcuts'].append(
        'Treat the terminal structural interface as the physical terminal transfer; source quartic floor and reachability remain separate.')
    graph['nodes'] = list(nodes.values())
    assert len(nodes) == len(graph['nodes'])
    def visit(key, stack):
        assert key not in stack
        for dep in nodes[key]['dependencies']:
            visit(dep, stack | {key})
    for key in nodes:
        visit(key, set())
    shutil.copy2(store.path, ROOT/'artifacts/routeb_storage_checkpoint_20260905/state-before-revision49.json')
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    m4 = next(node for node in state.nodes.values() if node.name.startswith('M4.') and node.name != 'M4.correlated_momentum_closure')
    m4.metadata.setdefault('proposed_mathematical_dags', []).append(ref(graph_path))
    m4.metadata['next_mathematical_frontier'] = graph['next_frontier']
    state.event('routeb_terminal_structural_checkpoint', proposed_dag=ref(graph_path),
                original_target_unchanged=True, actual_J_proved=False,
                formal_certificate_allowed=False, comparator_accepted=False,
                registry_promotions=0, broad_regression_run=False)
    store.save(state)
    print(json.dumps(dict(revision=state.revision, nodes=len(state.nodes), registry=len(state.registry),
                          terminal_lean_compiled=True, formal_certificate_allowed=False)))


if __name__ == '__main__': main()
