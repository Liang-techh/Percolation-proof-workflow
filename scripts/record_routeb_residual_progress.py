"""Import source-bound local math evidence; never promote the registry."""
import json
import re
import shutil

from record_routeb_port_progress import ROOT, ref, clean_axioms, wsl, LEAN
from percolation_workflow.statements import index_statements
from percolation_workflow.store import StateStore


def main():
    store = StateStore(ROOT / 'artifacts/routeb_6dof/state.json')
    state = store.load()
    assert state.project == 'routeb-6dof-external' and state.revision == 39
    assert not any(n.status == 'in_progress' for n in state.nodes.values())
    side = ROOT / 'examples/routeb_force_error_decomposition'
    source = side / 'ForceErrorDecomposition.lean'
    sr = ref(source)
    records = []
    for log in sorted((side/'output').glob('*/verify.log'), key=lambda p:p.stat().st_mtime_ns):
        snapshot = log.parent/source.name
        if not snapshot.exists():
            continue
        output = log.read_text(encoding='utf-8')
        success = 'LEAN_COMPILE_EXIT_CODE=0' in output and 'VERIFY_EXIT_CODE=1' not in output
        assert success or re.search(r'(?:LEAN_COMPILE|VERIFY)_EXIT_CODE=[1-9]', output), str(log)
        records.append((log,snapshot,output,success))
    names = ['implemented_reference_force','gravity_weighted_cost_rational']
    attempts = 0
    for name in names:
        theorem = 'RouteBForceErrorDecomposition.'+name
        accepted = [(log,snap) for log,snap,out,ok in records if ok
                    and ref(snap)['sha256']==sr['sha256'] and sr['sha256'] in out
                    and clean_axioms(theorem,out) and 'sorryAx' not in out]
        assert accepted, theorem
        decls = [d for d in index_statements(source) if d.qualified_name==theorem]
        assert len(decls)==1
        node_id = state.add_node(theorem,decls[0].source,
            proof_sketch='Full six-axis residual decomposition; explicit parameter-specific gravity SOS. Physical and cumulative premises remain open.',
            metadata={'verification_domain':'lean','source':sr,'compile_log':ref(accepted[-1][0]),
                      'statement_status':'compiled_source_unbound','registry_eligible':False,
                      'comparator_accepted':False,'evidence_level':'lean_compiled_candidate'})
        for log,snapshot,out,ok in records:
            attempt = state.begin_attempt(node_id,'01a07293-ab66-7160-8adc-1e554c8d3db3',source_path=str(snapshot.resolve()))
            state.finish_attempt(attempt,status='compiled' if ok else 'compile_error',
                command=[LEAN,'-DwarningAsError=true','--root='+wsl(side),'-o',
                         wsl(log.parent/'ForceErrorDecomposition.olean'),wsl(source)],
                stdout=out,stderr='',exit_code=0 if ok else 1)
            state.event('routeb_residual_attempt_imported',node_id=node_id,log=ref(log),
                        snapshot=ref(snapshot),registry_promoted=False)
            attempts += 1
    graph_path=ROOT/'artifacts/routeb_6dof/block45-obligations-v4.json'
    assert not graph_path.exists()
    graph=json.loads((graph_path.parent/'block45-obligations-v3.json').read_text(encoding='utf-8'))
    graph.update(schema='routeb-proposed-proof-dag-v4',supersedes='block45-obligations-v3.json')
    graph['nodes'].extend([
        dict(id='total_error_decomposition',status='compiled_candidate_comparator_pending',dependencies=[],
             source='../../examples/routeb_force_error_decomposition/ForceErrorDecomposition.lean',
             statement='Exact full-six-axis force decomposition and implementation error; old l_total is not the new e.'),
        dict(id='gravity_joint_cost',status='compiled_candidate_comparator_pending',dependencies=[],
             source='../../examples/routeb_force_error_decomposition/ForceErrorDecomposition.lean',
             statement='Explicit analytic gravity weighted squared cost <=424401201/208000000000 for arbitrary angles. Physical/source derivative binding remains open.'),
        dict(id='nongravity_and_cross_term_budget',status='open',dependencies=['source_semantics','total_error_decomposition'],
             statement='Use actual dynamics to bound inertia/coupling/C and runtime residual with correlations; combine with gravity on every pre-exit trajectory.')])
    for node in graph['nodes']:
        if node['id']=='total_error_budget_on_prefix':
            node['dependencies']=['source_semantics','total_error_decomposition','gravity_joint_cost','nongravity_and_cross_term_budget']
    nodes={n['id']:n for n in graph['nodes']}
    def visit(key,stack):
        assert key not in stack
        for dep in nodes[key]['dependencies']:
            visit(dep,stack|{key})
    for key in nodes: visit(key,set())
    graph_path.write_text(json.dumps(graph,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    checkpoint=ROOT/'artifacts/routeb_residual_checkpoint_20260905'
    backup=checkpoint/'state-before-revision39.json'
    assert not backup.exists()
    shutil.copy2(store.path,backup)
    artifacts=[ref(source),ref(side/'source_evidence.json'),ref(side/'DERIVATION.md'),
               ref(checkpoint/'REPORT.md'),ref(ROOT/'examples/routeb_residual_budget_screen/README.md')]
    m4=next(n for n in state.nodes.values() if n.name.startswith('M4.'))
    m4.metadata.setdefault('proposed_mathematical_dags',[]).append(ref(graph_path))
    m4.metadata['next_mathematical_frontier']=['nongravity_and_cross_term_cumulative_bound',
        'full_initial_set_total_error_budget_le_1_over_10','source_and_curve_binding','first_exit_continuation']
    state.event('routeb_residual_math_checkpoint',proposed_dag=ref(graph_path),artifacts=artifacts,
                numerical_screen_evidence='E1_ONLY',distinct_initial_cases=9,
                screened_max_R_approx=0.0100229985895,total_budget_proved=False,
                comparator_accepted=False,formal_certificate_allowed=False,registry_promotions=0)
    assert not state.registry
    store.save(state)
    print(json.dumps(dict(revision=state.revision,new_nodes=2,imported_attempts=attempts,
                          nodes=len(state.nodes),registry=len(state.registry))))


if __name__=='__main__': main()
