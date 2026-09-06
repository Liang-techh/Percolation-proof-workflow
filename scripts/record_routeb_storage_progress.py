"""Append the fixed-Z / actual-energy checkpoint, without registry admission.

Only hashes, exact literal reference entries, executed compiler markers and
new evidence receipts are inspected. No old tests, solvers or builds run.
"""
from fractions import Fraction as F
import json
from pathlib import Path
import re
import shutil

from record_routeb_port_progress import ROOT, ref, clean_axioms, wsl, LEAN
from record_routeb_signed_progress import sha_manifest
from percolation_workflow.statements import index_statements
from percolation_workflow.store import StateStore


def json_manifest(run):
    data = json.loads((run/'before_run.json').read_text(encoding='utf-8'))
    for name, record in data['snapshots'].items():
        digest = record['sha256'] if isinstance(record, dict) else record
        assert ref(run/name)['sha256'] == digest, (run, name)
    receipt_path = run/'receipt.json'
    if receipt_path.exists():
        receipt = json.loads(receipt_path.read_text(encoding='utf-8'))
        assert receipt['exit_code'] == 0 and receipt['snapshots_unchanged']
        for name, digest in receipt['outputs'].items():
            assert ref(run/name)['sha256'] == digest, (run, name)
    return data


def main():
    store = StateStore(ROOT/'artifacts/routeb_6dof/state.json')
    state = store.load()
    assert state.revision == 46 and len(state.nodes) == 53 and not state.registry
    assert not any(n.status == 'in_progress' for n in state.nodes.values())
    report = ROOT/'artifacts/routeb_storage_checkpoint_20260905/REPORT.md'
    assert report.is_file()
    universal = ROOT/'examples/routeb_universal_multiplier_lean'
    energy = ROOT/'examples/routeb_actual_energy_storage_lean'
    derivative_side = ROOT/'examples/routeb_actual_storage_derivative'
    records = {}
    for side, modules in ((universal, ('UniversalMultiplier',)),
                          (energy, ('ReferenceMass', 'ActualStorage')),
                          (derivative_side, ('ActualStorageDerivative',))):
        for run in sorted((side/'output').glob('run-*')):
            sha_manifest(run)
            log = run/'terminal.log'
            text = log.read_text(encoding='utf-8')
            overall = re.search(r'(?m)^VERIFY_EXIT_CODE=(\d+)$', text)
            assert overall, run
            executed = []
            for module in modules:
                marker = re.search(r'(?m)^'+module+r'_COMPILE_EXIT_CODE=(\d+)$', text)
                if marker is None:
                    continue  # A snapshot does not establish compiler execution.
                snapshot = run/(module+'.lean')
                names = {d.qualified_name for d in index_statements(snapshot)}
                code = int(marker[1])
                records.setdefault(module, []).append((run, text, code, names, int(overall[1])))
                executed.append(dict(module=module, exit_code=code))
                state.event('routeb_storage_module_attempt', module=module,
                            source=ref(snapshot), log=ref(log), exit_code=code,
                            registry_promoted=False)
            assert executed, run
            state.event('routeb_storage_execution_scope', run=str(run.resolve()),
                        executed_modules=executed, nonexecuted_modules_not_counted=True,
                        overall_exit_code=int(overall[1]))
    specs = [
        (universal, 'UniversalMultiplier', 'RouteBUniversalMultiplier.D_dominates_L', '01a07355-a2ff-7cb0-ab7b-ce2f6926972f'),
        (universal, 'UniversalMultiplier', 'RouteBUniversalMultiplier.CONSTRUCTIVELOSSLESS', '01a07355-a2ff-7cb0-ab7b-ce2f6926972f'),
        (universal, 'UniversalMultiplier', 'RouteBUniversalMultiplier.frozen_affine_dual_bound', '01a07355-a2ff-7cb0-ab7b-ce2f6926972f'),
        (energy, 'ReferenceMass', 'RouteBActualEnergyStorage.M0_le_identity', '01a0735d-d889-7d60-9c3a-0443c054b62f'),
        (energy, 'ActualStorage', 'RouteBActualEnergyStorage.W0_nonneg', '01a0735d-d889-7d60-9c3a-0443c054b62f'),
        (energy, 'ActualStorage', 'RouteBActualEnergyStorage.W0_initial_upper', '01a0735d-d889-7d60-9c3a-0443c054b62f'),
        (energy, 'ActualStorage', 'RouteBActualEnergyStorage.synthesisV_nonneg_on_P', '01a0735d-d889-7d60-9c3a-0443c054b62f'),
        (energy, 'ActualStorage', 'RouteBActualEnergyStorage.synthesisV_terminal', '01a0735d-d889-7d60-9c3a-0443c054b62f'),
        (energy, 'ActualStorage', 'RouteBActualEnergyStorage.synthesisV_initial_upper', '01a0735d-d889-7d60-9c3a-0443c054b62f'),
    ]
    specs.extend((derivative_side, 'ActualStorageDerivative', name, '01a07355-a2ff-7cb0-ab7b-ce2f6926972f')
                 for name in ('RouteBActualStorageDerivative.hasDerivAt_W0_from_source',
                              'RouteBActualStorageDerivative.hasDerivAt_storageV_from_source'))
    for side, module, name, agent in specs:
        source = side/(module+'.lean')
        # A later module's failure does not invalidate an already completed
        # zero-exit kernel compilation. Check this theorem's own axiom report.
        good = [r for r in records[module] if r[2] == 0 and
                ref(r[0]/source.name)['sha256'] == ref(source)['sha256'] and
                clean_axioms(name, r[1]) and (r[0]/(module+'.olean')).is_file()]
        assert good, name
        declaration = next(d for d in index_statements(source) if d.qualified_name == name)
        node = state.add_node(name, declaration.source,
            proof_sketch='Fixed identity affine multiplier and frozen-center SOS, or concrete actual-energy nonnegative storage with exact reference coefficients, full initial ball and explicit source hypotheses.',
            metadata={'verification_domain': 'lean', 'statement_status': 'compiled_source_unbound',
                      'source': ref(source), 'compile_log': ref(good[-1][0]/'terminal.log'),
                      'registry_eligible': False, 'comparator_accepted': False,
                      'physical_certificate': False})
        for run, text, code, names, overall in records[module]:
            if name not in names:
                continue
            attempt = state.begin_attempt(node, agent, source_path=str((run/source.name).resolve()))
            state.finish_attempt(attempt, status='compiled' if code == 0 else 'compile_error',
                command=[LEAN, '-DwarningAsError=true', '--root='+wsl(run), '-o',
                         wsl(run/(module+'.olean')), wsl(run/source.name)],
                stdout=text, stderr='', exit_code=code)

    # Directly match every literal matrix entry to the frozen exact reference.
    reference_path = ROOT/'examples/routeb_coupled_linear_reference/output/run-20260905T192654Z-3dbe159f/reference.json'
    reference = json.loads(reference_path.read_text(encoding='utf-8'))
    mass_source = energy/'ReferenceMass.lean'
    text = mass_source.read_text(encoding='utf-8')
    for matrix in ('M0', 'H0'):
        body = text.split('def '+matrix+' : Mat 6 := ![', 1)[1].split('\n\n', 1)[0]
        rows = re.findall(r'!\[([^\[\]]+)\]', body)
        parsed = [[F(x.strip()) for x in row.split(',')] for row in rows]
        assert parsed == [[F(x) for x in row] for row in reference[matrix]], matrix
    state.event('routeb_actual_energy_literal_reference', source=ref(mass_source),
                reference=ref(reference_path), exact_entries_checked=72,
                physical_DH_identification_proved=False, registry_promoted=False)

    algebra = ROOT/'examples/routeb_universal_multiplier/output/run-20260905T205229Z-e12aa6da'
    json_manifest(algebra)
    assert ref(algebra/'audit.py')['sha256'] == ref(algebra.parent.parent/'audit.py')['sha256']
    assert 'AUDIT_EXIT_CODE=0' in (algebra/'terminal.log').read_text(encoding='utf-8')
    result = json.loads((algebra/'results.json').read_text(encoding='utf-8'))
    assert result['frozen_center_congruence_entry_checks'] == 49
    assert result['pointwise_lossless_congruence_entry_checks'] == 49
    assert not result['actual_DH_J_proved'] and not result['formal_certificate_allowed']
    state.event('routeb_fixed_identity_exact_audit', result=ref(algebra/'results.json'),
                manifest=ref(algebra/'before_run.json'), registry_promoted=False)
    obstruction = ROOT/'examples/routeb_storage_origin_gate/output/run-20260905T211357Z-f7fae1f0'
    json_manifest(obstruction)
    assert ref(obstruction/'audit.py')['sha256'] == ref(obstruction.parent.parent/'audit.py')['sha256']
    assert 'AUDIT_EXIT_CODE=0' in (obstruction/'terminal.log').read_text(encoding='utf-8')
    negative = json.loads((obstruction/'results.json').read_text(encoding='utf-8'))
    assert negative['uniform_zero_supply_candidate_rejected']
    assert F(negative['Vdot']) > 0 and F(negative['initial_norm_squared']) < F(9,400)
    assert not negative['physical_target_refuted'] and not negative['formal_certificate_allowed']
    state.event('routeb_exact_zero_supply_candidate_rejection', result=ref(obstruction/'results.json'),
                manifest=ref(obstruction/'before_run.json'), log=ref(obstruction/'terminal.log'),
                candidate_run='lp-20260905T210840Z-ac3429b0',
                entire_storage_family_rejected=False, registry_promoted=False)
    design = ROOT/'examples/routeb_storage_design'
    evidence = []
    for run in sorted((design/'output').iterdir()):
        if not run.is_dir() or not (run/'before_run.json').exists():
            continue
        json_manifest(run)
        receipt = json.loads((run/'receipt.json').read_text(encoding='utf-8'))
        paths = [run/name for name in receipt['outputs'] if name.endswith('.json') and name!='lp_problem.json']
        evidence.extend(ref(p) for p in paths)
        state.event('routeb_storage_candidate_attempt', manifest=ref(run/'before_run.json'),
                    receipt=ref(run/'receipt.json'), results=[ref(p) for p in paths],
                    numerical_or_exact_candidate_only=True, uniform_gate_proved=False,
                    registry_promoted=False)
    selected_path = design/'output/lp-20260905T210840Z-ac3429b0/lp_candidate_evidence.json'
    selected = json.loads(selected_path.read_text(encoding='utf-8'))
    coefficients = {k: F(v) for k,v in selected['rational_coefficients'].items()}
    count = selected['degree']
    total_f = sum(coefficients[f'a{j}'] for j in range(1,count+1))
    total_c = sum(coefficients[f'c{j}'] for j in range(1,count+1))
    beta = coefficients['beta']
    assert min(coefficients.values()) >= 0 and beta >= total_f/2
    for i in range(1,7):
        position = sum(coefficients[f'p{j}_{i}'] for j in range(1,count+1))
        assert beta >= position+(F(7,75)*total_f if i==4 else 0)
    budget = F(9,400)*beta+F(3,10000)*total_f+3*total_c
    assert budget == F(835965494010387,2500000000000000)
    assert not selected['J1_proved'] and not selected['uniform_gate_proved']
    state.event('routeb_rejected_candidate_conditional_initial_budget', candidate=ref(selected_path),
                exact_beta_constraints_checked=True, conditional_initial_storage_upper=str(budget),
                zero_supply_candidate_rejected=True, actual_J_upper_proved=False)

    gp = ROOT/'artifacts/routeb_6dof/block45-obligations-v11.json'
    assert not gp.exists()
    graph = json.loads((gp.parent/'block45-obligations-v10.json').read_text(encoding='utf-8'))
    graph.update(schema='routeb-proposed-proof-dag-v11', supersedes='block45-obligations-v10.json',
                 active_strategy='fixed_identity_multiplier_actual_energy_storage')
    graph['nodes'].extend([
        dict(id='fixed_identity_affine_gate', status='compiled_candidate_comparator_pending',
             dependencies=['affine_multiplier_dissipation'],
             statement='Z=I has D=2M-L>=L under source mass order; pointwise losslessness and noncontractive frozen-center scalar sufficient gate are derived from finite sums.'),
        dict(id='concrete_actual_energy_storage', status='compiled_candidate_comparator_pending',
             dependencies=['global_fourier_gravity_floor','signed_gap_source_derivative'],
             statement='W0=kineticM0-Sgap+7q4^2/75 is nonnegative on q4^2<=56/15 with actual mass PSD and literal-source identities; actual M0<=I is proved by exact DSOS.'),
        dict(id='decaying_storage_prefix_initial_terminal', status='compiled_candidate_comparator_pending',
             dependencies=['concrete_actual_energy_storage'],
             statement='Nonnegative positive powers of1-t give prefix-nonnegative V, V(1)=0 and a full12-ball initial budget; source initialSgap lower bound is explicit.'),
        dict(id='actual_energy_storage_source_derivative', status='compiled_candidate_comparator_pending',
             dependencies=['concrete_actual_energy_storage','signed_gap_source_derivative'],
             statement='Source-level kinetic/Christoffel chain rules cancel M0delta exactly in W0dot; actual storageV product/finite-sum derivative is composed without a final-rate assumption.'),
        dict(id='storage_collocation_and_ramp_repair', status='zero_supply_candidates_refuted',
             dependencies=['fixed_identity_affine_gate','concrete_actual_energy_storage'],
             statement='Exactly two bounded LP searches; first candidate refuted by exact ramp/initial witnesses, second by an exact allowed q6/v6 initial state. Candidate initial budgets are not J bounds.'),
        dict(id='origin_quadratic_and_terminal_storage_gate', status='open',
             dependencies=['actual_energy_storage_source_derivative'],
             statement='Enforce the full13x13 origin quadratic necessary condition over time and terminal residual-energy coverage (a1>0 or positive supply), before more nonlinear collocation.'),
        dict(id='uniform_fixed_identity_scalar_source_gate', status='open',
             dependencies=['fixed_identity_affine_gate','origin_quadratic_and_terminal_storage_gate','correlated_velocity_source_bound'],
             statement='Prove the chosen storage derivative plus signed frozen-center source cost<=supply throughout actual covered cells, including ramp-driven small velocities and eta.')])
    uniform = next(n for n in graph['nodes'] if n['id']=='uniform_affine_matrix_certificate')
    uniform['dependencies'] = ['signed_augmented_storage_assembly','uniform_fixed_identity_scalar_source_gate']
    uniform['statement'] = 'Use the fixed-Z scalar route as the active sufficient construction; full affine multiplier alternatives remain available.'
    budget = next(n for n in graph['nodes'] if n['id']=='uniform_signed_storage_supply_budget')
    budget['dependencies'] = ['uniform_affine_matrix_certificate','decaying_storage_prefix_initial_terminal']
    budget['statement'] = 'Close strict all-prefix budget with explicit initialSgap/source bounds, actual-domain continuation and ramp/eta supply; nonnegative storage avoids a generic signed endpoint lower enclosure.'
    graph['alternatives'].append('Earlier general signed-storage, homogeneous-multiplier and unsigned-prefix routes retained; the current nonnegative storage family is a sufficient ansatz, not a restriction of the original theorem.')
    graph['rejected_shortcuts'].extend([
        'Treat frozen h=M0^-1 r as actual delta away from M=M0.',
        'Treat a finite LP objective below1 or solverOPTIMAL as the uniform dissipation certificate.',
        'Forget ramp-reserve constraints at nonzero small velocities because zero-state ramp points have zero residual.',
        'Use q4-domain positivity as a whole-trajectory assumption instead of a strict pre-exit continuation premise.'])
    nodes = {n['id']: n for n in graph['nodes']}
    assert len(nodes) == len(graph['nodes'])
    def visit(key, stack):
        assert key not in stack
        for dep in nodes[key]['dependencies']:
            visit(dep, stack | {key})
    for key in nodes:
        visit(key, set())
    backup = report.parent/'state-before-revision46.json'
    assert not backup.exists()
    shutil.copy2(store.path, backup)
    gp.write_text(json.dumps(graph, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    m4 = next(n for n in state.nodes.values() if n.name.startswith('M4.') and n.name!='M4.correlated_momentum_closure')
    m4.metadata.setdefault('proposed_mathematical_dags', []).append(ref(gp))
    m4.metadata['next_mathematical_frontier'] = [
        'origin_13x13_quadratic_and_terminal_a1_or_supply_gate', 'uniform_actual_energy_storage_scalar_source_gate',
        'strict_full_initial_ball_and_all_prefix_budget', 'eta_and_AE_source_binding', 'all_domain_continuation']
    state.event('routeb_actual_energy_mathematical_checkpoint', report=ref(report), proposed_dag=ref(gp),
                universal_lean_receipt=ref(universal/'FINAL_RECEIPT.md'),
                actual_energy_lean_receipt=ref(energy/'FINAL_RECEIPT.md'),
                derivative_lean_receipt=ref(derivative_side/'FINAL_RECEIPT.md'),
                second_candidate_exact_rejection=ref(obstruction/'results.json'),
                candidates=evidence, original_target_unchanged=True, actual_J_proved=False,
                formal_certificate_allowed=False, comparator_accepted=False, registry_promotions=0,
                broad_regression_run=False)
    store.save(state)
    print(json.dumps(dict(revision=state.revision, nodes=len(state.nodes), registry=len(state.registry),
                          exact_literal_entries_checked=72, formal_certificate_allowed=False)))


if __name__ == '__main__':
    main()
