"""Persist the bounded, read-only source-binding audit as open obligations."""
import csv
import hashlib
import json
from pathlib import Path
import shutil

from record_routeb_port_progress import ROOT, ref
from percolation_workflow.store import StateStore


def main():
    store = StateStore(ROOT/'artifacts/routeb_6dof/state.json')
    state = store.load()
    assert state.revision == 51 and len(state.nodes) == 64 and not state.registry
    side = ROOT/'examples/routeb_source_binding_audit'
    report = side/'REPORT.md'
    manifest = side/'SHA256SUMS.csv'
    assert report.is_file() and manifest.is_file()
    for row in csv.DictReader(manifest.open(encoding='utf-8')):
        path = side/row['path'].replace('\\', '/')
        assert path.is_file() and path.stat().st_size == int(row['bytes'])
        assert hashlib.sha256(path.read_bytes()).hexdigest() == row['sha256']
    text = report.read_text(encoding='utf-8')
    assert 'B45-1' in text and 'B45-5' in text and 'kc=0.05' in text
    assert 'OPEN / MISMATCH FLAG' in text
    supply = ROOT/'examples/routeb_positive_supply_gate'
    supply_receipt = supply/'FINAL_RECEIPT.md'
    supply_log = supply/'output/run-IL9p8Cz4/terminal.log'
    supply_lean = supply/'output/run-IL9p8Cz4/PositiveSupplyGate.lean'
    supply_olean = supply/'output/run-IL9p8Cz4/PositiveSupplyGate.olean'
    assert supply_receipt.is_file() and supply_log.is_file()
    assert supply_lean.is_file() and supply_olean.is_file()
    supply_text = supply_receipt.read_text(encoding='utf-8')
    supply_log_text = supply_log.read_text(encoding='utf-8')
    assert 'Status: PASS' in supply_text
    assert 'PositiveSupplyGate_COMPILE_EXIT_CODE=0; VERIFY_EXIT_CODE=0' in supply_text
    assert 'EXACT_A1_POSITIVE_SUPPLY_AUDIT_PASS' in supply_log_text
    assert 'NO_FEASIBILITY_OR_J1_CLAIM' in supply_log_text
    assert hashlib.sha256(supply_lean.read_bytes()).hexdigest() == (
        'f5002568a092ffad7ed1c6a42fa4ec6ce4544bf9d4eb0001b59a73eca334d3f4')
    assert hashlib.sha256(supply_olean.read_bytes()).hexdigest() == (
        'c47591997657ca175c1377d65450df35cfbe7955d03173f92534fd6e3eb33627')
    state.event(
        'routeb_b45_source_binding_audit',
        report=ref(report), manifest=ref(manifest), exact_snapshot_files=14,
        source_text_facts=True, functional_DH_binding=False,
        PMI_kc_mismatch=True, status='open_obligations',
        registry_promoted=False, formal_certificate_allowed=False)
    state.event(
        'routeb_positive_supply_gate_lean',
        receipt=ref(supply_receipt), source=ref(supply_lean),
        olean=ref(supply_olean), terminal_log=ref(supply_log),
        compile_exit=0, verify_exit=0, standard_axioms_only=True,
        exact_a1_floor_display='1.782507279003281e-08',
        uniform_feasibility=False, J_proved=False,
        registry_promoted=False, formal_certificate_allowed=False)
    graph_path = ROOT/'artifacts/routeb_6dof/block45-obligations-v16.json'
    assert not graph_path.exists()
    graph = json.loads(
        (graph_path.parent/'block45-obligations-v15.json').read_text(encoding='utf-8'))
    graph.update(
        schema='routeb-proposed-proof-dag-v16',
        supersedes='block45-obligations-v15.json',
        active_strategy='source_binding_before_physical_certificate')
    nodes = {node['id']: node for node in graph['nodes']}
    nodes['source_semantics']['statement'] = (
        'Bind the deployed DH/FD/Float64 source to the Lean Fourier/mass/potential '
        'objects, including index maps, regularization, finite differences, eta '
        'and trajectory semantics. B45-1..B45-4 remain open.')
    nodes['source_semantics']['binding_audit'] = dict(
        report=str(report.resolve()), status='open',
        exact_snapshot_manifest=str(manifest.resolve()))
    nodes['positive_supply_gate'] = dict(
        id='positive_supply_gate', status='compiled_candidate_comparator_pending',
        dependencies=['actual_energy_storage_source_derivative',
                      'fixed_identity_affine_gate'],
        source='../../examples/routeb_positive_supply_gate/PositiveSupplyGate.lean',
        statement=(
            'Generic eta-aware first-order terminal lower bound and nonnegative '
            'polynomial coefficient budget. The exact audit gives a positive '
            'candidate first-order floor, but uniform physical feasibility and '
            'J<=1 remain open.'),
        verification=dict(receipt=str(supply_receipt.resolve()),
                          run='output/run-IL9p8Cz4', standard_axioms_only=True,
                          compile_exit=0, verify_exit=0,
                          source_sha256='f5002568a092ffad7ed1c6a42fa4ec6ce4544bf9d4eb0001b59a73eca334d3f4',
                          olean_sha256='c47591997657ca175c1377d65450df35cfbe7955d03173f92534fd6e3eb33627'))
    nodes['origin_quadratic_and_terminal_storage_gate']['dependencies'] = [
        'actual_energy_storage_source_derivative', 'source_semantics',
        'positive_supply_gate']
    nodes['uniform_fixed_identity_scalar_source_gate']['dependencies'] = [
        'fixed_identity_affine_gate',
        'origin_quadratic_and_terminal_storage_gate',
        'terminal_gate_formalization',
        'correlated_velocity_source_bound',
        'source_semantics']
    graph['source_binding_obligations'] = [
        dict(id='B45-1', status='open',
             statement='Functional full mass reconstruction M_FD(q)=FourierMass(q)+1e-6 I with DH transform/index/COM/inertia bindings.'),
        dict(id='B45-2', status='open',
             statement='Functional potential reconstruction and finite-difference gradient binding.'),
        dict(id='B45-3', status='open',
             statement='DH meaning of H0 and gradient at zero.'),
        dict(id='B45-4', status='open',
             statement='Source finite-difference Christoffel tensor binding to the Lean contraction.'),
        dict(id='B45-5', status='open_mismatch',
             statement='PMI block model has kc=0.05 cross terms absent from actual tau; prove an explicit residual decomposition or replace the model.')]
    graph['next_frontier'] = [
        'B45-1 functional mass reconstruction',
        'B45-2 potential and gradient reconstruction',
        'B45-3 H0 and gradient-zero binding',
        'B45-4 Christoffel FD binding',
        'B45-5 repair PMI/actual block equation mismatch',
        'actual mass PSD and eta bounds',
        'positive_supply_gate uniform feasibility and coefficient/J search',
        'uniform_fixed_identity_scalar_source_gate',
        'all_domain_continuation']
    graph['rejected_shortcuts'].append(
        'Use the PMI kc=0.05 block model as the actual DH equation without an explicit residual decomposition.')
    graph['nodes'] = list(nodes.values())
    assert len(nodes) == len(graph['nodes'])

    def visit(key, stack):
        assert key not in stack
        for dep in nodes[key]['dependencies']:
            visit(dep, stack | {key})

    for key in nodes:
        visit(key, set())
    shutil.copy2(
        store.path,
        ROOT/'artifacts/routeb_storage_checkpoint_20260905/state-before-revision51.json')
    graph_path.write_text(
        json.dumps(graph, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    m4 = next(node for node in state.nodes.values()
              if node.name.startswith('M4.')
              and node.name != 'M4.correlated_momentum_closure')
    m4.metadata.setdefault('proposed_mathematical_dags', []).append(ref(graph_path))
    m4.metadata['next_mathematical_frontier'] = graph['next_frontier']
    state.event(
        'routeb_source_binding_checkpoint',
        proposed_dag=ref(graph_path), original_target_unchanged=True,
        actual_J_proved=False, formal_certificate_allowed=False,
        comparator_accepted=False, registry_promotions=0,
        broad_regression_run=False)
    store.save(state)
    print(json.dumps(dict(
        revision=state.revision, nodes=len(state.nodes), registry=len(state.registry),
        B45_obligations=5, PMI_kc_mismatch=True,
        formal_certificate_allowed=False)))


if __name__ == '__main__':
    main()
