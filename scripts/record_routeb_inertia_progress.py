"""Preserve mathematical evidence without attributing pre-declaration attempts."""
import json
import re
import shutil

from record_routeb_port_progress import ROOT, ref, clean_axioms, wsl, LEAN
from percolation_workflow.statements import index_statements
from percolation_workflow.store import StateStore


def main():
    store=StateStore(ROOT/'artifacts/routeb_6dof/state.json')
    state=store.load()
    assert state.project=='routeb-6dof-external' and state.revision==40
    assert not state.registry and not any(n.status=='in_progress' for n in state.nodes.values())
    side=ROOT/'examples/routeb_rotational_dual'
    source=side/'RotationalDual.lean'
    sr=ref(source)
    records=[]
    for log in sorted((side/'output').glob('*/verify.log'),key=lambda p:p.stat().st_mtime_ns):
        snap=log.parent/source.name
        out=log.read_text(encoding='utf-8')
        ok='LEAN_COMPILE_EXIT_CODE=0' in out and 'VERIFY_EXIT_CODE=1' not in out
        assert snap.exists()
        terminal_failure=bool(re.search(r'(?:LEAN_COMPILE|VERIFY)_EXIT_CODE=[1-9]',out))
        receipt_path=log.parent/'terminal-receipt.json'
        if not ok and not terminal_failure and receipt_path.exists():
            receipt=json.loads(receipt_path.read_text(encoding='utf-8'))
            assert receipt['kind']=='coordinator_transcription_of_exec_tool_terminal_result'
            assert receipt['exit_code']==1 and receipt['source_sha256']==ref(snap)['sha256']
            assert 'error:' in out and 'sorryAx' in out
            terminal_failure=True
            state.event('routeb_inertia_terminal_receipt',receipt=ref(receipt_path),
                        provenance='retrospective tool-result transcription; failure evidence only')
        assert ok or terminal_failure,str(log)
        declarations={d.qualified_name for d in index_statements(snap)}
        records.append((log,snap,out,ok,declarations))
        # Module failure is preserved even when a later theorem did not exist.
        state.event('routeb_inertia_module_attempt',log=ref(log),snapshot=ref(snap),
                    status='compiled' if ok else 'compile_error',exit_code=0 if ok else 1,
                    theorem_attribution='only declarations present in the snapshot',registry_promoted=False)
    count=0
    for short in ('dh_axes_mass_dual','reference_mismatch_force_only'):
        name='RouteBRotationalDual.'+short
        accepted=[r for r in records if r[3] and ref(r[1])['sha256']==sr['sha256']
                  and sr['sha256'] in r[2] and clean_axioms(name,r[2]) and 'sorryAx' not in r[2]]
        assert accepted,name
        decl=next(d for d in index_statements(source) if d.qualified_name==name)
        node_id=state.add_node(name,decl.source,
            proof_sketch='Actual inertia weights and fixed adjacent-axis products yield an anisotropic mass dual; force balance eliminates acceleration from reference-mass-mismatch cost.',
            metadata={'verification_domain':'lean','source':sr,'compile_log':ref(accepted[-1][0]),
                      'statement_status':'compiled_source_unbound','registry_eligible':False,
                      'comparator_accepted':False,'physical_FK_binding':False,
                      'evidence_level':'lean_compiled_candidate'})
        for log,snap,out,ok,declarations in records:
            if name not in declarations:
                continue
            attempt=state.begin_attempt(node_id,'coordinator',source_path=str(snap.resolve()))
            state.finish_attempt(attempt,status='compiled' if ok else 'compile_error',
                command=[LEAN,'-DwarningAsError=true','--root='+wsl(log.parent),'-o',
                         wsl(log.parent/'RotationalDual.olean'),wsl(snap)],
                stdout=out,stderr='',exit_code=0 if ok else 1)
            count+=1
    checkpoint=ROOT/'artifacts/routeb_inertia_checkpoint_20260905'
    assert (checkpoint/'REPORT.md').exists()
    artifacts=[ref(side/'source_evidence.json'),ref(side/'DERIVATION.md'),
               ref(ROOT/'examples/routeb_inertial_structure/audit_results.json'),
               ref(ROOT/'examples/routeb_inertial_structure/DERIVATION.md'),
               ref(ROOT/'examples/routeb_inertial_structure/ATTEMPT_HISTORY.md'),ref(checkpoint/'REPORT.md')]
    audit=json.loads((ROOT/'examples/routeb_inertial_structure/audit_results.json').read_text(encoding='utf-8'))
    assert audit['status']=='EXACT_MBD_AND_CHRISTOFFEL_IDENTITIES_VERIFIED'
    assert audit['total_point1_budget_proved'] is False
    gp=ROOT/'artifacts/routeb_6dof/block45-obligations-v5.json'
    assert not gp.exists()
    graph=json.loads((gp.parent/'block45-obligations-v4.json').read_text(encoding='utf-8'))
    graph.update(schema='routeb-proposed-proof-dag-v5',supersedes='block45-obligations-v4.json')
    graph['nodes'].extend([
        dict(id='rotational_mass_dual',status='compiled_candidate_comparator_pending',dependencies=[],
             source='../../examples/routeb_rotational_dual/RotationalDual.lean',
             statement='Actual rotational weights and unit/adjacent DH axis premises give exact anisotropic Q and L=Q^-1 bounds, with explicit physical model binding still open.'),
        dict(id='reference_mass_force_budget',status='compiled_candidate_comparator_pending',dependencies=['rotational_mass_dual'],
             source='../../examples/routeb_rotational_dual/RotationalDual.lean',
             statement='Diagonal reference mass mismatch weighted squared cost <=101871/204800000000*Q(f) under actual force balance. Not total residual cost.'),
        dict(id='compact_inertia_transport_binding',status='open',dependencies=['source_semantics'],
             source='../../examples/routeb_inertial_structure/DERIVATION.md',
             statement='Exact Fourier audit of MBD/Christoffel and momentum transport; physical FK, ideal-FD and Float64 binding and cumulative cancellation remain open.')])
    for n in graph['nodes']:
        if n['id']=='nongravity_and_cross_term_budget':
            n['dependencies']+=['reference_mass_force_budget','compact_inertia_transport_binding']
    nodes={n['id']:n for n in graph['nodes']}
    assert len(nodes)==len(graph['nodes'])
    def visit(k,stack):
        assert k not in stack
        for d in nodes[k]['dependencies']: visit(d,stack|{k})
    for k in nodes: visit(k,set())
    gp.write_text(json.dumps(graph,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    backup=checkpoint/'state-before-revision40.json'
    assert not backup.exists()
    shutil.copy2(store.path,backup)
    m4=next(n for n in state.nodes.values() if n.name.startswith('M4.'))
    m4.metadata.setdefault('proposed_mathematical_dags',[]).append(ref(gp))
    m4.metadata['next_mathematical_frontier']=['coupled_momentum_transport_cumulative_budget',
        'full_initial_set_forceMetric_integral_and_total_R','physical_FK_FD_Float64_binding','first_exit_continuation']
    state.event('routeb_inertia_math_checkpoint',proposed_dag=ref(gp),artifacts=artifacts,
                source_coefficient_audit_only=True,total_budget_proved=False,
                formal_certificate_allowed=False,comparator_accepted=False,registry_promotions=0)
    store.save(state)
    print(json.dumps(dict(revision=state.revision,nodes=len(state.nodes),registry=len(state.registry),
                          module_attempts=len(records),declaration_present_attempts=count)))


if __name__=='__main__': main()
