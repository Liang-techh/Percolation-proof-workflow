"""Persist a meaningful rejected relaxation; do not close the physical goal."""
import json
import shutil
from fractions import Fraction as Q

from record_routeb_math_progress import ROOT,ref
from percolation_workflow.store import StateStore


def main():
    store=StateStore(ROOT/'artifacts/routeb_6dof/state.json')
    state=store.load()
    assert state.revision==41 and len(state.nodes)==37 and not state.registry
    assert state.project=='routeb-6dof-external' and not any(n.status=='in_progress' for n in state.nodes.values())
    side=ROOT/'examples/routeb_momentum_source_bounds'
    filter_side=ROOT/'examples/routeb_momentum_filter'
    source=json.loads((side/'bounds.json').read_text(encoding='utf-8'))
    witness=json.loads((side/'relaxation_counterexample.json').read_text(encoding='utf-8'))
    assert source['box_invariance_proved'] is False and source['Lean_verified'] is False
    assert witness['actual_DH_trajectory'] is False and witness['original_theorem_refuted'] is False
    assert Q(witness['sigma_cap'])<Q(source['sigma_caps'][1])
    assert Q(witness['exact_terminal_lower'])>12 and Q(witness['exact_domain_lower'])>Q(28,5)
    assert source['script_sha256']==ref(side/'bounds.py')['sha256']
    assert witness['script_sha256']==ref(side/'relaxation_counterexample.py')['sha256']
    accepted=[]
    for run in sorted((filter_side/'output').glob('run-*')):
        log=run/'terminal.log'
        out=log.read_text(encoding='utf-8')
        assert 'AUDIT_EXIT_CODE=' in out
        manifest=json.loads((run/'before_run.json').read_text(encoding='utf-8'))['source_snapshots']
        assert all(ref(run/name)['sha256']==h for name,h in manifest.items())
        success='AUDIT_EXIT_CODE=0' in out
        state.event('routeb_filter_audit_attempt',log=ref(log),source_manifest=ref(run/'before_run.json'),
                    exit_code=0 if success else 1,kernel_verified=False,registry_promoted=False)
        current_source=(filter_side/'audit.py').read_text(encoding='utf-8')
        snapshot_source=(run/'audit.py').read_text(encoding='utf-8')
        source_matches=manifest['audit.py']==ref(filter_side/'audit.py')['sha256']
        obsolete='certifies_P_lt_45=pb<45,certifies_P_lt_5_6=pb<Q(28,5),'
        corrected='certifies_P_lt_5_6=pb<Q(28,5),'
        label_only=(snapshot_source.count(obsolete)==1 and
                    snapshot_source.replace(obsolete,corrected)==current_source)
        if success and (source_matches or label_only):
            result=json.loads((run/'results.json').read_text(encoding='utf-8'))
            if any(c['name']=='actual_source_caps_eta_zero' for c in result['cases']):
                accepted.append(run)
                if label_only:
                    state.event('routeb_filter_label_only_revision',audited_snapshot=ref(run/'audit.py'),
                                current_script=ref(filter_side/'audit.py'),
                                exact_edit='remove obsolete P<45 output field only; P<5.6 and Q<12 calculations unchanged',
                                current_label_revision_rerun=False,kernel_admission_allowed=False)
    assert accepted,'No complete source-bound final filter audit'
    report=ROOT/'artifacts/routeb_filter_checkpoint_20260905/REPORT.md'
    artifacts=[ref(report),ref(side/'bounds.json'),ref(side/'relaxation_counterexample.json'),
               ref(side/'DERIVATION.md'),ref(filter_side/'DERIVATION.md'),
               ref(filter_side/'ATTEMPT_HISTORY.md'),ref(accepted[-1]/'results.json')]
    artifacts += [ref(p) for p in sorted((side/'history').glob('*'))]
    node=state.add_node('M4.correlated_momentum_closure',
        'Retain the actual joint six-axis p/sigma dynamics and prove the original block output bounds; amplitude caps alone admit a nonphysical relaxed-filter counterexample.',
        proof_sketch='Preserve V=v2+v3 and cyclic momentum relations, or prove sufficient temporal/cumulative error bounds; full original initial set and ramp family are unchanged.',
        metadata={'verification_domain':'mathematical_diagnostic','statement_status':'open_research_obligation',
                  'registry_eligible':False,'formal_certificate_allowed':False,'artifacts':artifacts})
    gp=ROOT/'artifacts/routeb_6dof/block45-obligations-v6.json'
    assert not gp.exists()
    graph=json.loads((gp.parent/'block45-obligations-v5.json').read_text(encoding='utf-8'))
    graph.update(schema='routeb-proposed-proof-dag-v6',supersedes='block45-obligations-v5.json')
    graph['nodes'].extend([
        dict(id='momentum_source_cap_audit',status='conditional_rational_audit_only',dependencies=['compact_inertia_transport_binding'],
             statement='Exact sigma/T bounds after preserving V, on a candidate support whose invariance remains OPEN.'),
        dict(id='amplitude_only_filter_relaxation',status='rejected_by_rational_auxiliary_counterexample',dependencies=[],
             statement='At the current caps, the relaxed continuous-sigma filter violates P5.6 and terminal Q12. This is NOT an original DH counterexample.'),
        dict(id='correlated_momentum_closure',status='open',dependencies=['source_semantics','compact_inertia_transport_binding'],
             statement='Keep p/sigma physical correlations or establish temporal/cumulative control. Do not rely solely on current amplitude caps.')])
    graph['alternatives'].append('Amplitude-only filter relaxation is rejected; correlated momentum closure remains a possible route to the unchanged physical outputs, not an additional root prerequisite.')
    graph['rejected_shortcuts'].append('Current sigma/h amplitude caps alone imply original output or candidate-box invariance')
    nodes={n['id']:n for n in graph['nodes']}
    assert len(nodes)==len(graph['nodes'])
    def visit(k,stack):
        assert k not in stack
        for d in nodes[k]['dependencies']: visit(d,stack|{k})
    for k in nodes: visit(k,set())
    gp.write_text(json.dumps(graph,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    backup=report.parent/'state-before-revision41.json'
    assert not backup.exists()
    shutil.copy2(store.path,backup)
    m4=next(n for n in state.nodes.values() if n.name.startswith('M4.') and n.id!=node)
    m4.metadata.setdefault('proposed_mathematical_dags',[]).append(ref(gp))
    m4.metadata['next_mathematical_frontier']=['coupled_p_sigma_full_state_dynamics',
        'actual_temporal_or_total_residual_integral_budget','source_FD_Float64_binding','full_domain_continuation']
    state.event('routeb_filter_relaxation_checkpoint',node_id=node,proposed_dag=ref(gp),artifacts=artifacts,
                original_target_refuted=False,auxiliary_amplitude_only_route_rejected=True,
                total_R_proved=False,formal_certificate_allowed=False,registry_promotions=0)
    store.save(state)
    print(json.dumps(dict(revision=state.revision,nodes=len(state.nodes),registry=len(state.registry),
                          positive_physical_certificate=False,relaxation_rejected=True)))


if __name__=='__main__': main()
