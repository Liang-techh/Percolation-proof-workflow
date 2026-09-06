"""Add the compiled single-step Fourier normal form to the current DAG."""
import hashlib
import json
import shutil

from record_routeb_port_progress import ROOT, ref
from percolation_workflow.store import StateStore


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    store = StateStore(ROOT / 'artifacts/routeb_6dof/state.json')
    state = store.load()
    assert state.revision == 56 and len(state.nodes) == 64 and not state.registry
    side = ROOT / 'examples/routeb_b45_fourier_normal_form'
    receipt = side / 'FINAL_RECEIPT.md'
    source = side / 'output/run-yFKe4FyW/FourierNormalForm.lean'
    olean = side / 'output/run-yFKe4FyW/FourierNormalForm.olean'
    log = side / 'output/run-yFKe4FyW/terminal.log'
    zero = ROOT / 'examples/routeb_mass_zero_bridge_lean'
    zreceipt = zero / 'FINAL_RECEIPT.md'
    zsource = zero / 'output/run-iIbVmSPE/MassZeroBridge.lean'
    zolean = zero / 'output/run-iIbVmSPE/MassZeroBridge.olean'
    zlog = zero / 'output/run-iIbVmSPE/terminal.log'
    zaudit = zero / 'output/audit-20260905T221316Z/result.json'
    old_graph = ROOT / 'artifacts/routeb_6dof/block45-obligations-v20.json'
    graph_path = ROOT / 'artifacts/routeb_6dof/block45-obligations-v21.json'
    for path in (receipt, source, olean, log, zreceipt, zsource, zolean, zlog,
                 zaudit, old_graph):
        assert path.is_file()
    assert not graph_path.exists()
    assert sha(source) == '5fc6c92f727744a49e8318a951a30748f7a732fd232f31d5ae23a3e9f3a50ca0'
    assert sha(olean) == '81de6730573f9936d64176a17d67d58fa737ce953758836b0211d06a20bbe7fe'
    assert sha(zsource) == '6dcc3103b9a6b9f69ba66fb5649835a28797cd94dce69f6fd53aabe7f839b219'
    assert sha(zolean) == 'ff8a1e54a1516bfb19aafaff2783098fffbbd4b0d405e7c8067e696ce2989bca'
    nt = receipt.read_text(encoding='utf-8') + log.read_text(encoding='utf-8')
    zt = zreceipt.read_text(encoding='utf-8') + zlog.read_text(encoding='utf-8')
    assert 'FourierNormalForm_COMPILE_EXIT_CODE=0' in nt
    assert 'VERIFY_EXIT_CODE=0' in nt and 'standard axioms' in nt
    assert 'output/run-iIbVmSPE' in zt
    assert 'MassZeroBridge_COMPILE_EXIT_CODE=0' in zt
    assert 'VERIFY_EXIT_CODE=0' in zt
    audit = json.loads(zaudit.read_text(encoding='utf-8'))
    assert audit['status'] == 'EXACT_CSV_Q0_PAYLOAD_AUDIT_PASSED'
    assert audit['csv_sha256'] == 'a986a208b62f585c6ca1b9c81b958710d2043e5bf786ddc930a6fa29f7a232b8'
    assert audit['csv_rows'] == 610 and audit['regularized_payload_matches_M0']
    assert not audit['physical_DH_binding'] and not audit['float64_bridge']

    state.event(
        'routeb_b45_1_fourier_normal_form_compiled',
        receipt=ref(receipt), source=ref(source), olean=ref(olean),
        terminal_log=ref(log), compile_exit=0, verify_exit=0,
        standard_axioms_only=True, algebraic_laurent_only=True,
        exp_trig_bridge=False, physical_source_binding=False,
        registry_promoted=False, formal_certificate_allowed=False)
    state.event(
        'routeb_b45_1_q0_bridge_canonical_receipt',
        receipt=ref(zreceipt), source=ref(zsource), olean=ref(zolean),
        terminal_log=ref(zlog), external_audit=ref(zaudit),
        compile_exit=0, verify_exit=0, csv_rows=610, matrix_entries=36,
        exact_rational_payload=True, full_q_function_identity=False,
        physical_source_binding=False, float64_bridge=False,
        registry_promoted=False, formal_certificate_allowed=False,
        supersedes_prior_receipt_references=True)

    graph = json.loads(old_graph.read_text(encoding='utf-8'))
    graph.update(schema='routeb-proposed-proof-dag-v21',
                 supersedes='block45-obligations-v20.json',
                 active_strategy='lift_single_step_fourier_to_full_mass')
    nodes = {node['id']: node for node in graph['nodes']}
    nodes['B45-1_fourier_single_step_normal_form'] = {
        'id': 'B45-1_fourier_single_step_normal_form',
        'status': 'compiled_candidate_comparator_pending',
        'dependencies': [],
        'source': '../../examples/routeb_b45_fourier_normal_form/FourierNormalForm.lean',
        'statement': (
            'Kernel-check the exact Laurent normal form of one Route-B DH step '
            'and the six phase/parameter rows. The identification of Laurent '
            'atoms with exp(I*q) remains open.'),
        'verification': {
            'receipt': str(receipt.resolve()), 'run': 'output/run-yFKe4FyW',
            'compile_exit': 0, 'verify_exit': 0, 'standard_axioms_only': True,
            'source_sha256': sha(source), 'olean_sha256': sha(olean)}}
    nodes['B45-1_mass_functional_identity']['dependencies'] = [
        'source_semantics', 'B45-1_fourier_single_step_normal_form']
    nodes['B45-1_mass_functional_identity']['compiled_precursor'] = (
        'B45-1_fourier_single_step_normal_form')
    nodes['B45-1_zero_point_M0_bridge']['dependencies'] = [
        'B45-1_csv_q0_provenance', 'B45-1_regularizer_kernel_leaf']
    nodes['B45-1_zero_point_M0_bridge']['compiled_leaf'] = 'B45-1_q0_mass_M0_bridge'
    nodes['B45-1_zero_point_M0_bridge']['verification']['run'] = 'output/run-iIbVmSPE'
    nodes['B45-1_zero_point_M0_bridge']['verification']['source_sha256'] = sha(zsource)
    nodes['B45-1_zero_point_M0_bridge']['verification']['olean_sha256'] = sha(zolean)
    nodes['B45-1_zero_point_M0_bridge']['verification']['receipt'] = str(zreceipt.resolve())
    nodes['B45-1_zero_point_M0_bridge']['verification']['terminal_log'] = str(zlog.resolve())
    nodes['source_semantics']['fourier_normal_form'] = {
        'status': 'compiled_candidate', 'source': str(receipt.resolve()),
        'exp_trig_bridge': 'open', 'full_mass_lift': 'open'}
    for obligation in graph['source_binding_obligations']:
        if obligation['id'] == 'B45-1':
            if 'B45-1_fourier_single_step_normal_form' not in obligation['subnodes']:
                obligation['subnodes'].insert(0, 'B45-1_fourier_single_step_normal_form')
            obligation['q0_bridge'] = 'compiled_candidate_comparator_pending'
    graph['next_frontier'] = [
        'B45-1.1 exp/trig bridge for Laurent atoms',
        'B45-1.2 frame recursion and parent-axis lift',
        'B45-1.c body mass Fourier evaluator for all q',
        'B45-1.i Float64 enclosure bridge',
        'B45-2 potential and gradient reconstruction',
        'B45-3 H0 and gradient-zero binding',
        'B45-4 Christoffel FD binding',
        'B45-5_residual_domain_bound',
        'positive_supply_relative_eta_lemma',
        'positive_supply_two_regime_direct_gate',
        'positive_supply_equilibrium_floor',
        'actual mass PSD and eta bounds',
        'uniform_fixed_identity_scalar_source_gate',
        'all_domain_continuation']
    graph['nodes'] = list(nodes.values())

    def visit(key, stack):
        assert key not in stack
        for dep in nodes[key].get('dependencies', []):
            assert dep in nodes
            visit(dep, stack | {key})

    for key in nodes:
        visit(key, set())
    backup = ROOT / 'artifacts/routeb_storage_checkpoint_20260905/state-before-revision56.json'
    assert not backup.exists()
    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    m4 = next(node for node in state.nodes.values()
              if node.name.startswith('M4.') and node.name != 'M4.correlated_momentum_closure')
    m4.metadata.setdefault('proposed_mathematical_dags', []).append(ref(graph_path))
    m4.metadata['next_mathematical_frontier'] = graph['next_frontier']
    state.event(
        'routeb_b45_1_fourier_checkpoint', proposed_dag=ref(graph_path),
        original_target_unchanged=True, actual_J_proved=False,
        formal_certificate_allowed=False, comparator_accepted=False,
        registry_promotions=0, broad_regression_run=False)
    store.save(state)
    print(json.dumps(dict(revision=state.revision, nodes=len(state.nodes),
                         graph_nodes=len(nodes), registry=len(state.registry),
                         formal_certificate_allowed=False)))


if __name__ == '__main__':
    main()
