"""Source-bound signed checkpoint; record only compiler modules actually run."""
import ast
import csv
from fractions import Fraction as F
import json
from pathlib import Path
import re
import shutil

from record_routeb_port_progress import ROOT,ref,clean_axioms,wsl,LEAN
from percolation_workflow.statements import index_statements
from percolation_workflow.store import StateStore


def sha_manifest(run):
    for line in (run/'before_run.sha256').read_text(encoding='utf-8').splitlines():
        m=re.fullmatch(r'([0-9a-f]{64})\s+(.+)',line)
        assert m,line
        path=m[2]
        assert path.startswith('/mnt/c/')
        local=Path('C:/'+path[len('/mnt/c/'):]).resolve()
        assert local.is_relative_to(run.resolve())
        assert ref(local)['sha256']==m[1],local


def literal_fourier_check(source,csv_path):
    body=source.read_text(encoding='utf-8').split('def realFourierPotential ',1)[1].split('theorem potential_identity ',1)[0]
    pattern=r'^\s*\+?\s*\((-?\d+)\s*/\s*(\d+)\)\s*\*\s*Real\.cos\s+(.+?)\s*--\s*\(([-\d,]+)\)\s*$'
    terms=re.findall(pattern,body,re.M)
    with csv_path.open(newline='',encoding='utf-8') as f: rows=list(csv.DictReader(f))
    assert len(terms)==len(rows)==17
    def vector(expr):
        if isinstance(expr,ast.Expression): return vector(expr.body)
        if isinstance(expr,ast.Name):
            assert expr.id in ('u','s','x','y')
            return tuple(int(expr.id==n) for n in ('u','s','x','y'))
        if isinstance(expr,ast.Constant):
            assert expr.value==0
            return (0,0,0,0)
        if isinstance(expr,ast.UnaryOp) and isinstance(expr.op,ast.USub): return tuple(-v for v in vector(expr.operand))
        if isinstance(expr,ast.BinOp) and isinstance(expr.op,(ast.Add,ast.Sub)):
            sign=1 if isinstance(expr.op,ast.Add) else -1
            return tuple(a+sign*b for a,b in zip(vector(expr.left),vector(expr.right)))
        raise ValueError('not a literal Fourier phase')
    for (num,den,phase,comment),row in zip(terms,rows):
        nu=tuple(int(row['nu'+str(i)]) for i in range(1,7))
        assert nu[0]==nu[5]==0
        assert tuple(map(int,comment.split(',')))==nu
        assert F(num)/F(den)==F(row['real_num'])/F(row['real_den'])
        assert F(row['imag_num'])/F(row['imag_den'])==0
        assert vector(ast.parse(phase.strip(),mode='eval'))==(nu[1]-nu[2],nu[2],nu[3],nu[4])
    return len(rows)


def main():
    store=StateStore(ROOT/'artifacts/routeb_6dof/state.json');state=store.load()
    assert state.revision==45 and len(state.nodes)==46 and not state.registry
    assert not any(n.status=='in_progress' for n in state.nodes.values())
    lean=ROOT/'examples/routeb_signed_gap_lean'
    gravity=ROOT/'examples/routeb_gravity_twist_floor'
    records={}
    for side,modules in ((lean,('SignedGap','ResidualMultiplier','IntegratedBudget')),
                         (gravity,('GravityTwistFloor',))):
        for run in sorted((side/'output').glob('run-*')):
            sha_manifest(run)
            log=run/'terminal.log';text=log.read_text(encoding='utf-8')
            overall=re.search(r'(?m)^VERIFY_EXIT_CODE=(\d+)$',text)
            assert overall,run
            executed=[]
            for module in modules:
                marker=module+'_COMPILE_EXIT_CODE' if side==lean else 'COMPILE_EXIT_CODE'
                match=re.search(r'(?m)^'+marker+r'=(\d+)$',text)
                if match is None:
                    # Snapshot existence does not mean a downstream compiler ran.
                    continue
                code=int(match[1]);snapshot=run/(module+'.lean')
                declarations={d.qualified_name for d in index_statements(snapshot)}
                records.setdefault(module,[]).append((run,text,code,declarations,int(overall[1])))
                executed.append(dict(module=module,exit_code=code))
                state.event('routeb_signed_module_attempt',module=module,source=ref(snapshot),
                            log=ref(log),exit_code=code,registry_promoted=False)
            assert executed,run
            state.event('routeb_signed_attempt_execution_scope',run=str(run.resolve()),
                        executed_modules=executed,nonexecuted_modules_not_counted=True,
                        overall_exit_code=int(overall[1]))
    specs=[
        (lean,'SignedGap','RouteBSignedGap.hasDerivAt_signedGap_from_source','01a0733c-d77f-7c52-bc45-01c76be74ca6'),
        (lean,'ResidualMultiplier','RouteBSignedGap.affine_dissipation_fin6','01a0733c-d77f-7c52-bc45-01c76be74ca6'),
        (lean,'IntegratedBudget','RouteBSignedGap.augmented_affine_dissipation','01a0733c-d77f-7c52-bc45-01c76be74ca6'),
        (lean,'IntegratedBudget','RouteBSignedGap.signed_budget_prefix_bootstrap','01a0733c-d77f-7c52-bc45-01c76be74ca6'),
        (gravity,'GravityTwistFloor','RouteBGravityTwistFloor.psi_ge_sin_fourth','01a07343-3bea-7f03-842f-5343113dbbbd'),
        (gravity,'GravityTwistFloor','RouteBGravityTwistFloor.gravity_twist_floor','01a07343-3bea-7f03-842f-5343113dbbbd'),
        (gravity,'GravityTwistFloor','RouteBGravityTwistFloor.fourier_remainder_floor','01a07343-3bea-7f03-842f-5343113dbbbd')]
    for side,module,name,agent in specs:
        source=side/(module+'.lean')
        good=[r for r in records[module] if r[2]==r[4]==0 and
              ref(r[0]/source.name)['sha256']==ref(source)['sha256'] and clean_axioms(name,r[1]) and 'sorryAx' not in r[1]]
        assert good,name
        decl=next(d for d in index_statements(source) if d.qualified_name==name)
        node=state.add_node(name,decl.source,
            proof_sketch='Real finite-sum derivatives, affine residual cancellation and strict prefix integration, or global quarter-angle gravity floor with literal source Fourier expansion. Physical/source hypotheses remain distinct.',
            metadata={'verification_domain':'lean','statement_status':'compiled_source_unbound',
                      'source':ref(source),'compile_log':ref(good[-1][0]/'terminal.log'),
                      'registry_eligible':False,'comparator_accepted':False,'physical_certificate':False})
        for run,text,code,declarations,overall in records[module]:
            if name not in declarations: continue
            attempt=state.begin_attempt(node,agent,source_path=str((run/source.name).resolve()))
            state.finish_attempt(attempt,status='compiled' if code==0 else 'compile_error',
                command=[LEAN,'-DwarningAsError=true','--root='+wsl(run),'-o',
                         wsl(run/(module+'.olean')),wsl(run/source.name)],
                stdout=text,stderr='',exit_code=code)
    final_gravity=gravity/'output/run-LIFMhESI'
    csv_path=final_gravity/'inputs/routeB_fourier_potential_rational.csv'
    rows_checked=literal_fourier_check(gravity/'GravityTwistFloor.lean',csv_path)
    state.event('routeb_literal_Fourier_source_match',source=ref(gravity/'GravityTwistFloor.lean'),
                csv=ref(csv_path),rows=rows_checked,coefficients_and_actual_phases_checked=True,
                Python_or_DH_identification_proved=False,registry_promoted=False)
    source=ROOT/'examples/routeb_signed_gap_source'
    for run in sorted((source/'output').glob('run-*')):
        manifest=json.loads((run/'before_run.json').read_text(encoding='utf-8'))['snapshots']
        assert all(ref(run/name)['sha256']==item['sha256'] for name,item in manifest.items())
        receipt=json.loads((run/'receipt.json').read_text(encoding='utf-8'))
        assert receipt['exit_code']==0 and all(receipt['input_and_code_unchanged'].values())
        assert all(ref(run/name)['sha256']==digest for name,digest in receipt['output_sha256'].items())
        result=json.loads((run/'audit_results.json').read_text(encoding='utf-8'))
        assert not result['J1_proved'] and not result['Lean_verified']
        state.event('routeb_all6_signed_source_audit',manifest=ref(run/'before_run.json'),
                    result=ref(run/'audit_results.json'),receipt=ref(run/'receipt.json'),
                    kernel_verified=False,registry_promoted=False)
    final_source=source/'output/run-20260905T203532Z-b2dcff09'
    assert ref(source/'audit.py')['sha256']==ref(final_source/'audit.py')['sha256']
    sr=json.loads((final_source/'audit_results.json').read_text(encoding='utf-8'))
    assert sr['christoffel_entries']==216 and sr['cubic_complex_coefficient_checks']==7896
    assert F(sr['endpoint_summary']['existing_strict_prefix']['uniform_upper'])==F(31093066123,10**12)
    affine=ROOT/'examples/routeb_affine_multiplier/output/run-20260905T202634Z-e39dc9a3'
    am=json.loads((affine/'before_run.json').read_text(encoding='utf-8'))['snapshots']
    assert all(ref(affine/name)['sha256']==digest for name,digest in am.items())
    assert ref(affine/'audit.py')['sha256']==ref(affine.parent.parent/'audit.py')['sha256']
    assert 'AUDIT_EXIT_CODE=0' in (affine/'terminal.log').read_text(encoding='utf-8')
    ar=json.loads((affine/'results.json').read_text(encoding='utf-8'))
    assert ar['coefficient_identities']==43 and ar['witness']['homogeneous_every_Z_impossible']
    assert ar['witness']['affine_strictly_positive'] and not ar['witness']['global_storage_constructed']
    assert not ar['actual_DH_J_proved'] and not ar['formal_certificate_allowed']
    state.event('routeb_affine_multiplier_class_audit',manifest=ref(affine/'before_run.json'),
                result=ref(affine/'results.json'),log=ref(affine/'terminal.log'),
                homogeneous_valid_but_incomplete=True,local_jet_not_global_storage=True,
                original_M4_refuted=False,registry_promoted=False)
    report=ROOT/'artifacts/routeb_signed_checkpoint_20260905/REPORT.md'
    gp=ROOT/'artifacts/routeb_6dof/block45-obligations-v10.json';assert not gp.exists()
    graph=json.loads((gp.parent/'block45-obligations-v9.json').read_text(encoding='utf-8'))
    graph.update(schema='routeb-proposed-proof-dag-v10',supersedes='block45-obligations-v9.json',
                 active_strategy='full_coupled_direct_outputs_via_signed_affine_dissipation')
    graph['nodes'].extend([
        dict(id='all6_signed_source_power',status='rational_source_audit_only',dependencies=['coupled_nominal_coefficients'],
             statement='216 Christoffel entries and7896 complex cubic-power coefficients, fullSgap/r0 and signed mass square factors match source tables; physical extraction binding remains open.'),
        dict(id='signed_gap_source_derivative',status='compiled_candidate_comparator_pending',
             dependencies=['all6_signed_source_power','source_semantics','curve_regularity'],
             statement='Source-space chain rules and finite sums prove Sgap derivative v M0 delta-v eta with Christoffel work cancellation, no positive-storage assumption.'),
        dict(id='global_fourier_gravity_floor',status='compiled_candidate_comparator_pending',dependencies=[],
             statement='Literal17-term Fourier potential satisfiesR>=-q4^4/40 globally viaquarter-anglePsi>=sin^4/32; coefficients/phases matchedCSV, physicalDHidentificationstillopen.'),
        dict(id='affine_multiplier_dissipation',status='compiled_candidate_comparator_pending',dependencies=[],
             statement='Full7x7 quadratic form with residual multiplier z+Zdelta impliesdeltaLdelta+Vdot<=b underMdelta=r. Homogeneousz0 subclass validbutnotcomplete.'),
        dict(id='signed_augmented_storage_assembly',status='compiled_candidate_comparator_pending',
             dependencies=['signed_gap_source_derivative','affine_multiplier_dissipation'],
             statement='DifferentiateY P(t)Y+kSgap and assemblefinite-vectoraffinedissipation withactualsame-statefeedback.'),
        dict(id='signed_prefix_integral_bridge',status='compiled_candidate_comparator_pending',
             dependencies=['prefix_continuity_bootstrap'],
             statement='FTC andall-prefixstorage/supplyinequalities plusstrictmargin exclude firsthit. AEadapter andexistencenotassumedproven.'),
        dict(id='signed_endpoint_enclosure',status='conditional_rational_enclosure_only',
             dependencies=['all6_signed_source_power','coupled_finite_gain_audit','global_fourier_gravity_floor'],
             statement='SignedSgap endpointenclosures overcompletecells; through9/16 onexistingidealprefix,through1onlyunderhypotheticalJ1.'),
        dict(id='uniform_affine_matrix_certificate',status='open',
             dependencies=['signed_augmented_storage_assembly','correlated_velocity_source_bound'],
             statement='ConstructcompatibleP,k,z,Z andproveassembled7x7nonnegativeonactualcoveredsourcecells,notonlyalocaljet.'),
        dict(id='uniform_signed_storage_supply_budget',status='open',
             dependencies=['uniform_affine_matrix_certificate','signed_endpoint_enclosure'],
             statement='Proveinitialfullballupper,lowerstorageateverypossibleprefixendpoint,etasupplyandstrictintegralbudgetunderoriginalT1family.')])
    signed=next(n for n in graph['nodes'] if n['id']=='signed_energy_gap_certificate')
    signed['dependencies']=['uniform_affine_matrix_certificate','uniform_signed_storage_supply_budget','signed_prefix_integral_bridge']
    signed['statement']='Assemble actualJ<=1 fromaffine signed dissipation, all-prefix endpoints/supply, source/eta anddomaincoverage. Homogeneousonlyformnotmandatory.'
    budget=next(n for n in graph['nodes'] if n['id']=='coupled_J_prefix_budget')
    budget['dependencies']=['source_semantics','acceleration_free_resolvent','signed_energy_gap_certificate','curve_regularity']
    graph['alternatives'].append('Unsigned source-functional prefix remains retained as partial/alternative evidence, not an extra full-horizon prerequisite of the signed affine route. Homogeneous multiplier remains a valid restricted subclass.')
    graph['rejected_shortcuts'].extend([
        'Restrictresidualmultipliers toZdelta andmistakethisforacompleteclass: sourcepointlocaljetneedsaffinez.',
        'Treatcompiledgapderivative or signedendpointenclosure asaproofthatauniform7x7matrix/supplycertificateexists.',
        'Counta downstreamLeanmoduleasattemptedwhenanearliermodulefailedbeforeitwasinvoked.'])
    nodes={n['id']:n for n in graph['nodes']};assert len(nodes)==len(graph['nodes'])
    def visit(k,stack):
        assert k not in stack
        for d in nodes[k]['dependencies']: visit(d,stack|{k})
    for k in nodes: visit(k,set())
    backup=report.parent/'state-before-revision45.json';assert not backup.exists()
    shutil.copy2(store.path,backup)
    gp.write_text(json.dumps(graph,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    m4=next(n for n in state.nodes.values() if n.name.startswith('M4.') and n.name!='M4.correlated_momentum_closure')
    m4.metadata.setdefault('proposed_mathematical_dags',[]).append(ref(gp))
    m4.metadata['next_mathematical_frontier']=['uniform_affine_signed_7x7_matrix_certificate',
        'compatible_storage_P_k_and_affine_z_Z_selection','all_prefix_storage_supply_budget',
        'eta_and_AE_trajectory_source_binding','all_domain_continuation']
    state.event('routeb_signed_mathematical_checkpoint',proposed_dag=ref(gp),report=ref(report),
                affine_class=ref(affine/'results.json'),signed_source=ref(final_source/'audit_results.json'),
                signed_source_endpoints=ref(final_source/'endpoint_bounds.json'),
                lean_receipt=ref(lean/'FINAL_RECEIPT.md'),gravity_source=ref(gravity/'GravityTwistFloor.lean'),
                original_target_unchanged=True,actual_J_proved=False,formal_certificate_allowed=False,
                comparator_accepted=False,registry_promotions=0)
    store.save(state)
    print(json.dumps(dict(revision=state.revision,nodes=len(state.nodes),registry=len(state.registry),
                          literal_Fourier_rows_checked=rows_checked,actual_DH_J_proved=False)))


if __name__=='__main__': main()
