"""Persist source-prefix results and formal first-hit candidates, fail closed.

Only this phase's receipts are inspected. No full regression or registry bypass.
"""
from fractions import Fraction as F
import json
from pathlib import Path
import re
import shutil

from record_routeb_port_progress import ROOT,ref,clean_axioms,wsl,LEAN
from percolation_workflow.statements import index_statements
from percolation_workflow.store import StateStore


def main():
    store=StateStore(ROOT/'artifacts/routeb_6dof/state.json')
    state=store.load()
    assert state.revision==44 and len(state.nodes)==42 and not state.registry
    assert not any(n.status=='in_progress' for n in state.nodes.values())
    side=ROOT/'examples/routeb_prefix_small_gain'
    source=side/'PrefixSmallGain.lean'
    records=[]
    for run in sorted((side/'output').glob('run-*')):
        log=run/'terminal.log';snapshot=run/source.name
        out=log.read_text(encoding='utf-8')
        ok='LEAN_COMPILE_EXIT_CODE=0' in out and 'VERIFY_EXIT_CODE=0' in out
        assert ok or re.search(r'(?:LEAN_COMPILE|VERIFY)_EXIT_CODE=[1-9]',out),run
        assert ref(snapshot)['sha256'] in (run/'before_run.sha256').read_text(encoding='utf-8')
        declarations={d.qualified_name for d in index_statements(snapshot)}
        records.append((run,out,ok,declarations))
        state.event('routeb_prefix_module_attempt',source=ref(snapshot),log=ref(log),
                    exit_code=0 if ok else 1,registry_promoted=False)
    targets=('sqrt_energy_gate','continuousOn_prefix_bootstrap',
             'continuousOn_small_gain_bootstrap','continuousOn_cell_bootstrap')
    for short in targets:
        name='RouteBPrefixSmallGain.'+short
        good=[r for r in records if r[2] and ref(r[0]/source.name)['sha256']==ref(source)['sha256']
              and clean_axioms(name,r[1]) and 'sorryAx' not in r[1]]
        assert good,name
        decl=next(d for d in index_statements(source) if d.qualified_name==name)
        node=state.add_node(name,decl.source,
            proof_sketch='ContinuousOn compact first-hit construction and strict conditional prefix improvement exclude circular energy/domain assumptions. Analytic source/integration premises remain explicit.',
            metadata={'verification_domain':'lean','source':ref(source),
                      'compile_log':ref(good[-1][0]/'terminal.log'),
                      'statement_status':'compiled_source_unbound',
                      'registry_eligible':False,'comparator_accepted':False,
                      'actual_DH_J_proved':False})
        for run,out,ok,declarations in records:
            if name not in declarations: continue
            attempt=state.begin_attempt(node,'01a07329-5b8f-7571-901a-df2166dab73a',
                                        source_path=str((run/source.name).resolve()))
            state.finish_attempt(attempt,status='compiled' if ok else 'compile_error',
                command=[LEAN,'-DwarningAsError=true','--root='+wsl(run),'-o',
                         wsl(run/'PrefixSmallGain.olean'),wsl(run/source.name)],
                stdout=out,stderr='',exit_code=0 if ok else 1)
    prefix=ROOT/'examples/routeb_prefix_budget'
    for run in sorted((prefix/'output').glob('run-*')):
        manifest=json.loads((run/'before_run.json').read_text(encoding='utf-8'))['snapshots']
        assert all(ref(run/name)['sha256']==digest for name,digest in manifest.items())
        assert 'AUDIT_EXIT_CODE=0' in (run/'terminal.log').read_text(encoding='utf-8')
        result=json.loads((run/'results.json').read_text(encoding='utf-8'))
        assert not result['actual_DH_J_proved'] and not result['formal_certificate_allowed']
        previous=F(0)
        for cell in result['strict_prefix_cells']:
            start,end=map(F,cell['time']);barrier=F(cell['strict_barrier'])
            assert F(cell['previous_J_upper'])==previous and previous<barrier<=1
            forcing=F(cell.get('delta_energy_upper',cell.get('Q_r_upper')))
            exact=previous+(end-start)*forcing
            assert exact==F(cell['derived_J_upper'])<barrier
            previous=F(-((-exact.numerator*10**12)//exact.denominator),10**12)
        assert previous==F(result['conditional_J_upper'])
        state.event('routeb_prefix_source_audit',manifest=ref(run/'before_run.json'),
                    source=ref(run/'audit.py'),log=ref(run/'terminal.log'),
                    result=ref(run/'results.json'),conditional_prefix=result['conditional_prefix_horizon'],
                    actual_DH_J_proved=False,kernel_verified=False)
    final=prefix/'output/run-20260905T200854Z-88e7c74d'
    corrected=final/'field_name_correction/results.json'
    original=json.loads((final/'results.json').read_text(encoding='utf-8'))
    result=json.loads(corrected.read_text(encoding='utf-8'))
    amendment=result.pop('receipt_semantics_correction')
    assert amendment['original_sha256']==ref(final/'results.json')['sha256']
    for record in original['fixed_hypothetical_caps']:
        record['delta_energy_integral_upper']=record.pop('Q_r_integral_upper')
    assert result==original, 'field normalization changed mathematics'
    assert 'NORMALIZATION_EXIT_CODE=0' in (corrected.parent/'terminal.log').read_text(encoding='utf-8')
    expected=(final/'audit.py').read_text(encoding='utf-8').replace(
        'Q_r_integral_upper=str(integrated)','delta_energy_integral_upper=str(integrated)').replace(
        'CONDITIONAL_FORCE_BUDGET_UPPER','CONDITIONAL_DELTA_ENERGY_UPPER')
    assert expected==(prefix/'audit.py').read_text(encoding='utf-8'), 'unaudited mathematical edit'
    assert result['conditional_prefix_horizon']=='9/16'
    assert F(result['conditional_J_upper'])==F(26281199249,200000000000)
    assert not result['full_horizon_analytic_budget_closed']
    strategy=ROOT/'examples/routeb_J_strategy'
    algebra=strategy/'output/run-20260905T201432Z-5c2562b5'
    am=json.loads((algebra/'before_run.json').read_text(encoding='utf-8'))
    assert all(ref(Path(item['snapshot']))['sha256']==item['sha256'] for item in am['files'])
    assert 'AUDIT_EXIT_CODE=0' in (algebra/'terminal.log').read_text(encoding='utf-8')
    ar=json.loads((algebra/'audit_results.json').read_text(encoding='utf-8'))
    assert ar['status']=='EXACT_TARGETED_J_ALGEBRA_PASS' and not ar['J_le_1_proved']
    assert F(ar['radial_lower_coefficient_for_abs_t_le_1_over_20'])==F(668495583,3200000000)>0
    assert ar['C_at_zero_v4_equal_v5_coefficient']==['21/25000','0','0','0','0','0']
    state.event('routeb_signed_gravity_and_C_obstruction',manifest=ref(algebra/'before_run.json'),
                result=ref(algebra/'audit_results.json'),log=ref(algebra/'terminal.log'),
                radial_sector_rejected=True,all_cubic_residual_rejected=True,
                original_M4_refuted=False,registry_promoted=False)
    report=ROOT/'artifacts/routeb_prefix_checkpoint_20260905/REPORT.md'
    gp=ROOT/'artifacts/routeb_6dof/block45-obligations-v9.json'
    assert not gp.exists()
    graph=json.loads((gp.parent/'block45-obligations-v8.json').read_text(encoding='utf-8'))
    graph.update(schema='routeb-proposed-proof-dag-v9',supersedes='block45-obligations-v8.json')
    graph['nodes'].extend([
        dict(id='prefix_continuity_bootstrap',status='compiled_candidate_comparator_pending',dependencies=[],
             statement='ContinuousOn, strict start and conditional strict improvement on every pre-exit prefix imply no first hit; integration/source inequalities remain explicit.'),
        dict(id='source_functional_prefix_audit',status='conditional_short_prefix_only',
             dependencies=['coupled_nominal_coefficients','rotational_mass_dual'],
             statement='128 whole-cell rational enclosures and exact source-inverse preconditioning give ideal eta=0 conditional prefix through9/16,J<=26281199249/200000000000. T=1 remains unclosed.'),
        dict(id='signed_gravity_channel_algebra',status='rational_source_identity_only',dependencies=[],
             statement='Three scalar restoring sectors plus a retained twist term. Exact initial-ball witness refutes a globally restoring full gravity residual; origin Coriolis witness refutes an all-cubic residual.'),
        dict(id='finite_inverse_defect_bound',status='analytic_lemma_Lean_and_cells_open',
             dependencies=['rotational_mass_dual'],
             statement='For arbitrary rational P, ||delta||L<=||P r0||L+||(I-MP)r0||Q+||eta||Q; finite algebraic inverse corrections need no convergence assumption. Uniform source cell bounds OPEN.'),
        dict(id='correlated_velocity_source_bound',status='open',dependencies=['coupled_finite_gain_audit','signed_gravity_channel_algebra'],
             statement='Prove actual velocity ellipsoid and preserve mass/Coriolis mixed terms with6x6/7x7 rational positivity gates over the full original input family.'),
        dict(id='signed_energy_gap_certificate',status='open',dependencies=['source_semantics','signed_gravity_channel_algebra'],
             statement='Use signed Sgap derivative v M0 delta-v eta and a7x7 residual multiplier inequality; prove storage/supply bounds at ALL possible prefix endpoints, not justT1.')])
    budget=next(n for n in graph['nodes'] if n['id']=='coupled_J_prefix_budget')
    budget['dependencies'].append('prefix_continuity_bootstrap')
    graph['rejected_shortcuts'].extend([
        'Assume the entire H0q-gradU is a PSD restoring sector: exact counterexample within the original initial ball.',
        'Assume the whole residual is cubic because its linearization vanishes: nonzero quadratic Coriolis witness atq0.',
        'Call min(Q(r),preconditioned_delta_energy) a Q(r) upper bound; it only bounds delta L delta.',
        'Use a terminal-only storage lower bound in a first-exit prefix proof without uniform prefix endpoint control.'])
    graph['alternatives'].append('Unsigned scalar prefix envelope remains unclosed at T1; retain it as partial analytic evidence, not a changed acceptance horizon or physical counterexample.')
    nodes={n['id']:n for n in graph['nodes']}
    assert len(nodes)==len(graph['nodes'])
    def visit(k,stack):
        assert k not in stack
        for d in nodes[k]['dependencies']: visit(d,stack|{k})
    for k in nodes: visit(k,set())
    backup=report.parent/'state-before-revision44.json'
    assert not backup.exists();shutil.copy2(store.path,backup)
    gp.write_text(json.dumps(graph,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    m4=next(n for n in state.nodes.values() if n.name.startswith('M4.') and n.name!='M4.correlated_momentum_closure')
    m4.metadata.setdefault('proposed_mathematical_dags',[]).append(ref(gp))
    m4.metadata['next_mathematical_frontier']=['signed_source_channel_and_mass_C_cancellation',
        'finite_inverse_defect_and_correlated_velocity_certificates',
        'actual_J_prefix_budget_le_one','source_FD_Float64_errors','all_domain_continuation']
    m4.metadata['conditional_analytic_prefix']={'time':'9/16','J_upper':'26281199249/200000000000',
        'eta_zero_assumption':True,'actual_DH_bound':False,'full_horizon_closed':False,'receipt':ref(corrected)}
    state.event('routeb_prefix_mathematical_checkpoint',proposed_dag=ref(gp),report=ref(report),
                corrected_receipt=ref(corrected),normalization=ref(corrected.parent/'before_run.json'),
                source_derivation=ref(prefix/'DERIVATION.md'),strategy=ref(strategy/'REPORT.md'),
                signed_work=ref(strategy/'SIGNED_WORK.md'),first_hit_derivation=ref(side/'DERIVATION.md'),
                original_target_unchanged=True,actual_J_proved=False,
                formal_certificate_allowed=False,registry_promotions=0)
    store.save(state)
    print(json.dumps(dict(revision=state.revision,nodes=len(state.nodes),registry=len(state.registry),
                          conditional_analytic_prefix='9/16',actual_DH_J_proved=False)))


if __name__=='__main__': main()
