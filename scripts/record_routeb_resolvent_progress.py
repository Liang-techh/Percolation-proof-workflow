"""Record same-state coupled reductions, never a nominal-flow substitution."""
import json
from pathlib import Path
import shutil

from record_routeb_port_progress import ROOT,ref,clean_axioms,wsl,LEAN
from percolation_workflow.statements import index_statements
from percolation_workflow.store import StateStore


def main():
    store=StateStore(ROOT/'artifacts/routeb_6dof/state.json')
    state=store.load()
    assert state.revision==42 and len(state.nodes)==38 and not state.registry
    assert state.project=='routeb-6dof-external' and not any(n.status=='in_progress' for n in state.nodes.values())
    side=ROOT/'examples/routeb_coupled_resolvent'
    source=side/'CoupledResolvent.lean'
    run=side/'output/run-HTi4uZSF'
    log=run/'verify.log';out=log.read_text(encoding='utf-8')
    assert 'LEAN_COMPILE_EXIT_CODE=0' in out and 'VERIFY_EXIT_CODE=0' in out and 'sorryAx' not in out
    assert ref(source)['sha256']==ref(run/source.name)['sha256'] and ref(source)['sha256'] in out
    for short in ('acceleration_free_resolvent','total_error_from_coupled_residual'):
        name='RouteBCoupledResolvent.'+short
        assert clean_axioms(name,out)
        decl=next(d for d in index_statements(source) if d.qualified_name==name)
        node=state.add_node(name,decl.source,
            proof_sketch='Subtract actual and same-state nominal force balances; apply the full anisotropic mass dual before taking the block residual cost.',
            metadata={'verification_domain':'lean','source':ref(source),'compile_log':ref(log),
                      'statement_status':'compiled_source_unbound','registry_eligible':False,
                      'comparator_accepted':False,'physical_source_binding':False})
        attempt=state.begin_attempt(node,'coordinator',source_path=str((run/source.name).resolve()))
        state.finish_attempt(attempt,status='compiled',command=[LEAN,'-DwarningAsError=true','--root='+wsl(run),
            '-o',wsl(run/'CoupledResolvent.olean'),wsl(run/source.name)],stdout=out,stderr='',exit_code=0)
    nominal=ROOT/'examples/routeb_coupled_linear_reference/output/run-20260905T192654Z-3dbe159f'
    bounds=side/'output/bounds-20260905T193103Z-725e99c7'
    for audit_run in (nominal,bounds):
        assert 'AUDIT_EXIT_CODE=0' in (audit_run/'terminal.log').read_text(encoding='utf-8')
        manifest=json.loads((audit_run/'before_run.json').read_text(encoding='utf-8'))['inputs']
        for name,e in manifest.items():
            original=e['original_path'] if isinstance(e,dict) else name
            digest=e['sha256'] if isinstance(e,dict) else e
            snapshot=audit_run/'inputs'/(name if isinstance(e,dict) else Path(name).name)
            assert ref(snapshot)['sha256']==digest
            assert ref(Path(original))['sha256']==digest
        state.event('routeb_resolvent_exact_audit',manifest=ref(audit_run/'before_run.json'),
                    log=ref(audit_run/'terminal.log'),exit_code=0,kernel_verified=False,registry_promoted=False)
    reference=json.loads((nominal/'reference.json').read_text(encoding='utf-8'))
    bound_result=json.loads((bounds/'source_bounds.json').read_text(encoding='utf-8'))
    assert reference['status']=='EXACT_COUPLED_NOMINAL_REFERENCE_PASS'
    assert bound_result['status']=='EXACT_ACCELERATION_FREE_SOURCE_COEFFICIENT_AUDIT'
    assert not bound_result['total_R_proved'] and not bound_result['box_invariance_proved']
    report=ROOT/'artifacts/routeb_resolvent_checkpoint_20260905/REPORT.md'
    artifacts=[ref(source),ref(log),ref(side/'DERIVATION.md'),ref(nominal/'reference.json'),
               ref(nominal.parent.parent/'DERIVATION.md'),ref(nominal.parent.parent/'ATTEMPT_HISTORY.md'),
               ref(bounds/'source_bounds.json'),ref(report)]
    gp=ROOT/'artifacts/routeb_6dof/block45-obligations-v7.json'
    assert not gp.exists()
    graph=json.loads((gp.parent/'block45-obligations-v6.json').read_text(encoding='utf-8'))
    graph.update(schema='routeb-proposed-proof-dag-v7',supersedes='block45-obligations-v6.json')
    graph['nodes'].extend([
        dict(id='coupled_nominal_coefficients',status='rational_coefficient_audit_only',dependencies=[],
             statement='Exact full M0/H0/inverse/A/B/e0 maps, including all state/input correlations; no nominal stability assumption.'),
        dict(id='acceleration_free_resolvent',status='compiled_candidate_comparator_pending',dependencies=['rotational_mass_dual'],
             statement='Same-state nominal a0 gives M(a-a0)=r=(M0-M)a0+H0q-G-C+eta and cost(e-e0)<=3/10 Q(r). Source premises remain explicit.'),
        dict(id='coupled_time_dependent_enclosure',status='open',dependencies=['source_semantics','coupled_nominal_coefficients','acceleration_free_resolvent'],
             statement='Bound same-state e0 and nonlinear r along the original full trajectory; static independent-box Q(r) estimate is too coarse, not a disproof. Close continuation/domain and cumulative budgets.')])
    graph['alternatives'].append('Coupled resolvent and momentum formulations retain the same physical goal; neither admits independent nominal-flow residual data as an actual-flow bound.')
    graph['rejected_shortcuts'].append('Use the earlier nominal-trajectory numeric residual integral for same-state e0 along the actual flow')
    nodes={n['id']:n for n in graph['nodes']}
    assert len(nodes)==len(graph['nodes'])
    def visit(k,stack):
        assert k not in stack
        for d in nodes[k]['dependencies']: visit(d,stack|{k})
    for k in nodes: visit(k,set())
    gp.write_text(json.dumps(graph,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    backup=report.parent/'state-before-revision42.json'
    assert not backup.exists()
    shutil.copy2(store.path,backup)
    m4=next(n for n in state.nodes.values() if n.name.startswith('M4.') and n.name!='M4.correlated_momentum_closure')
    m4.metadata.setdefault('proposed_mathematical_dags',[]).append(ref(gp))
    m4.metadata['next_mathematical_frontier']=['time_dependent_correlated_state_enclosure',
        'same_state_e0_and_r_integral_bounds','source_FD_Float64_binding','complete_domain_continuation']
    state.event('routeb_coupled_resolvent_checkpoint',proposed_dag=ref(gp),artifacts=artifacts,
                static_box_bound_too_loose=True,coupled_route_refuted=False,total_R_proved=False,
                formal_certificate_allowed=False,comparator_accepted=False,registry_promotions=0)
    store.save(state)
    print(json.dumps(dict(revision=state.revision,nodes=len(state.nodes),registry=len(state.registry),
                          new_compiled_candidates=2,total_R_proved=False)))


if __name__=='__main__': main()
