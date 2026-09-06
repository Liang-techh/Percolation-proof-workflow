"""Persist direct original-output proof route; never require an optional R gate."""
import json
from pathlib import Path
import re
import shutil

from record_routeb_port_progress import ROOT,ref,clean_axioms,wsl,LEAN
from percolation_workflow.statements import index_statements
from percolation_workflow.store import StateStore


def main():
    store=StateStore(ROOT/'artifacts/routeb_6dof/state.json');state=store.load()
    assert state.revision==43 and len(state.nodes)==40 and not state.registry
    assert not any(n.status=='in_progress' for n in state.nodes.values())
    side=ROOT/'examples/routeb_coupled_gain_bridge';source=side/'GainBridge.lean'
    records=[]
    for run in sorted((side/'output').glob('run-*')):
        log=run/'terminal.log';out=log.read_text(encoding='utf-8');snapshot=run/source.name
        ok='LEAN_COMPILE_EXIT_CODE=0' in out and 'VERIFY_EXIT_CODE=0' in out
        assert ok or re.search(r'(?:LEAN_COMPILE|VERIFY)_EXIT_CODE=[1-9]',out)
        assert ref(snapshot)['sha256'] in (run/'before_run.sha256').read_text(encoding='utf-8')
        declarations={d.qualified_name for d in index_statements(snapshot)}
        records.append((run,out,ok,declarations))
        state.event('routeb_gain_module_attempt',source=ref(snapshot),log=ref(log),
                    exit_code=0 if ok else 1,registry_promoted=False)
    for short in ('final_reference_cost_under_J_cap','original_outputs_under_J_one'):
        name='RouteBCoupledGainBridge.'+short
        good=[r for r in records if r[2] and ref(r[0]/source.name)['sha256']==ref(source)['sha256']
              and clean_axioms(name,r[1]) and 'sorryAx' not in r[1]]
        assert good,name
        decl=next(d for d in index_statements(source) if d.qualified_name==name)
        node=state.add_node(name,decl.source,proof_sketch='Scalar admission from explicit coupled finite-horizon gain premises; direct original-output route uses J<=1, optional residual route uses J<=1/20.',
            metadata={'verification_domain':'lean','source':ref(source),'compile_log':ref(good[-1][0]/'terminal.log'),
                      'statement_status':'compiled_source_unbound','registry_eligible':False,'comparator_accepted':False})
        for run,out,ok,declarations in records:
            if name not in declarations: continue
            attempt=state.begin_attempt(node,'01a07293-ab66-7160-8adc-1e554c8d3db3',source_path=str((run/source.name).resolve()))
            state.finish_attempt(attempt,status='compiled' if ok else 'compile_error',
                command=[LEAN,'-DwarningAsError=true','--root='+wsl(run),'-o',wsl(run/'GainBridge.olean'),wsl(run/source.name)],
                stdout=out,stderr='',exit_code=0 if ok else 1)
    gain=ROOT/'examples/routeb_coupled_finite_gain'
    for run in sorted((gain/'output').glob('run-*')):
        assert 'AUDIT_EXIT_CODE=0' in (run/'terminal.log').read_text(encoding='utf-8')
        manifest=json.loads((run/'before_run.json').read_text(encoding='utf-8'))['snapshots']
        assert all(ref(run/name)['sha256']==h for name,h in manifest.items())
        state.event('routeb_gain_interval_audit',manifest=ref(run/'before_run.json'),
                    log=ref(run/'terminal.log'),result=ref(run/'results.json'),kernel_verified=False)
    final=gain/'output/run-20260905T194943Z-9ad8ada4'
    assert ref(final/'audit.py')['sha256']==ref(gain/'audit.py')['sha256']
    result=json.loads((final/'results.json').read_text(encoding='utf-8'))
    assert not result['nonlinear_J_bound_proved'] and not result['actual_DH_flowpipe_proved']
    assert any(g['J']=='1' and g['sufficient_for_original_outputs'] for g in result['direct_output_J_gates'])
    report=ROOT/'artifacts/routeb_gain_checkpoint_20260905/REPORT.md'
    artifacts=[ref(report),ref(gain/'DERIVATION.md'),ref(final/'results.json'),ref(side/'DERIVATION.md'),
               ref(side/'ATTEMPT_HISTORY.md'),ref(gain/'stored_path_diagnostic.py'),
               ref(gain/'output/run-20260905T194015Z-49c2839c/stored_path_diagnostic.json')]
    gp=ROOT/'artifacts/routeb_6dof/block45-obligations-v8.json';assert not gp.exists()
    graph=json.loads((gp.parent/'block45-obligations-v7.json').read_text(encoding='utf-8'))
    graph.update(schema='routeb-proposed-proof-dag-v8',supersedes='block45-obligations-v7.json',
                 active_strategy='full_coupled_direct_original_outputs_from_J_le_one')
    old_root=next(n for n in graph['nodes'] if n['id']=='M4')
    legacy=dict(old_root);legacy['id']='legacy_residual_cost_route'
    legacy['statement']='Optional historical route to the same physical outputs using R<=1/10; not an extra prerequisite of the direct-output strategy.'
    graph['nodes'].append(legacy)
    graph['nodes'].extend([
        dict(id='coupled_finite_gain_audit',status='rational_full_time_enclosure_only',dependencies=['coupled_nominal_coefficients'],statement='Full initial ball/ramp/time interval gives NP,NT,KP²,KT². Matrix enclosure is not Lean-admitted.'),
        dict(id='coupled_variation_bridge',status='open',dependencies=['source_semantics','coupled_finite_gain_audit','curve_regularity'],statement='Bind same-state actual/nominal variation of constants and L2-to-pointwise gains to the formal physical model, with identical initial state/input.'),
        dict(id='direct_output_scalar_gate',status='compiled_candidate_comparator_pending',dependencies=[],statement='Explicit scalar gain premises and J<=1 imply original P<28/5 and terminal Q<12.'),
        dict(id='coupled_J_prefix_budget',status='open',dependencies=['source_semantics','acceleration_free_resolvent','coupled_time_dependent_enclosure'],statement='On every pre-exit prefix prove integral delta L delta<=1, or sufficient integral Q(r)<=1, including actual implementation defects.'),
        dict(id='direct_output_prefix_assembly',status='open',dependencies=['coupled_variation_bridge','direct_output_scalar_gate','coupled_J_prefix_budget'],statement='Assemble original outputs on every prefix without presupposing global source-domain coverage.'),
        dict(id='coupled_domain_continuation',status='open',dependencies=['direct_output_prefix_assembly','remote_state_and_joint_domain'],statement='Close all source-domain premises, complete-state continuation and T=1 under the original initial/input contract.')])
    old_root['dependencies']=['direct_output_prefix_assembly','coupled_domain_continuation']
    graph['alternatives'].append('legacy_residual_cost_route is optional; R<=1/10 was a chosen intermediary, not part of the original P5.6/Q12 acceptance target.')
    nodes={n['id']:n for n in graph['nodes']};assert len(nodes)==len(graph['nodes'])
    def visit(k,stack):
        assert k not in stack
        for d in nodes[k]['dependencies']: visit(d,stack|{k})
    for k in nodes: visit(k,set())
    gp.write_text(json.dumps(graph,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    backup=report.parent/'state-before-revision43.json';assert not backup.exists();shutil.copy2(store.path,backup)
    m4=next(n for n in state.nodes.values() if n.name.startswith('M4.') and n.name!='M4.correlated_momentum_closure')
    m4.metadata.setdefault('proposed_mathematical_dags',[]).append(ref(gp))
    m4.metadata['next_mathematical_frontier']=['actual_J_prefix_budget_le_one',
        'coupled_variation_and_gain_formal_binding','source_FD_Float64_errors','all_domain_continuation']
    state.event('routeb_direct_output_gain_checkpoint',proposed_dag=ref(gp),artifacts=artifacts,
                original_target_unchanged=True,intermediate_R_gate_optional=True,
                nonlinear_J_proved=False,formal_certificate_allowed=False,registry_promotions=0)
    store.save(state)
    print(json.dumps(dict(revision=state.revision,nodes=len(state.nodes),registry=len(state.registry),
                          direct_route_J_cap=1,actual_J_proved=False)))


if __name__=='__main__': main()
