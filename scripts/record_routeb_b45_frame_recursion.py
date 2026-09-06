"""Record the narrow B45-1.2 parent-axis/frame recursion leaf."""
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
    assert state.revision == 59 and len(state.nodes) == 64 and not state.registry

    side = ROOT / 'examples/routeb_b45_frame_recursion'
    receipt = side / 'FINAL_RECEIPT.md'
    source = side / 'output/run-k87wlFSd/FrameRecursion.lean'
    olean = side / 'output/run-k87wlFSd/FrameRecursion.olean'
    base_source = side / 'output/run-k87wlFSd/FourierNormalForm.lean'
    base_olean = side / 'output/run-k87wlFSd/FourierNormalForm.olean'
    log = side / 'output/run-k87wlFSd/terminal.log'
    report = ROOT / 'artifacts/routeb_6dof/B45-1-frame-recursion.md'
    old_graph = ROOT / 'artifacts/routeb_6dof/block45-obligations-v23.json'
    graph_path = ROOT / 'artifacts/routeb_6dof/block45-obligations-v24.json'
    for path in (receipt, source, olean, base_source, base_olean, log,
                 report, old_graph):
        assert path.is_file(), path
    assert not graph_path.exists()

    assert sha(source) == (
        '3361f2353b44052e6426e6b41e9f009cf4e5b3c6675a846ab856c1b82616cf10')
    assert sha(olean) == (
        'abf9e99fce858a3cbf94b3bf20238a9f6dcc701370a296676ffc52e0dbd9814b')
    assert sha(base_source) == (
        '56ec2f2d29a22942bcb83a3ba98197ae1ce4d607340072b81c013b8d358d3218')
    assert sha(base_olean) == (
        '49d9dfaf04dae88f70301d697c26548ef65b5dcb3cd750b7a79eb2a7715917f1')

    receipt_text = receipt.read_text(encoding='utf-8')
    log_text = log.read_text(encoding='utf-8')
    report_text = report.read_text(encoding='utf-8')
    for marker in (
        'Status: PASS', 'FrameRecursion_COMPILE_EXIT_CODE=0',
        'FourierNormalForm_COMPILE_EXIT_CODE=0', 'VERIFY_EXIT_CODE=0',
        'prefixFrames_cons', 'terminalFrame_eq_product', 'parent * current',
        'COMPILED_CANDIDATE_COMPARATOR_PENDING'):
        assert marker in receipt_text + log_text + report_text, marker
    assert 'sorryAx' not in log_text
    assert 'FrameRecursion_COMPILE_EXIT_CODE=1' not in log_text

    state.event(
        'routeb_b45_1_frame_recursion_compiled',
        receipt=ref(receipt), source=ref(source), olean=ref(olean),
        base_source=ref(base_source), base_olean=ref(base_olean),
        terminal_log=ref(log), compile_exit=0, verify_exit=0,
        standard_axioms_only=True, no_sorry=True, no_admit=True,
        exact_parent_before_current=True, routeb_constants_reused=True,
        physical_source_binding=False, registry_promoted=False,
        formal_certificate_allowed=False)

    graph = json.loads(old_graph.read_text(encoding='utf-8'))
    graph.update(
        schema='routeb-proposed-proof-dag-v24',
        supersedes='block45-obligations-v23.json',
        active_strategy='lift_exact_frame_recursion_before_mass_functional_binding')
    nodes = {node['id']: node for node in graph['nodes']}
    nodes['B45-1_frame_recursion'] = {
        'id': 'B45-1_frame_recursion',
        'status': 'compiled_candidate_comparator_pending',
        'dependencies': [
            'B45-1_fourier_single_step_normal_form',
            'B45-1_fourier_phase_bridge'],
        'source': '../../examples/routeb_b45_frame_recursion/FrameRecursion.lean',
        'statement': (
            'For a finite list of 4-by-4 complex DH matrices, the parent frame '
            'precedes the current step exactly: prefixFrames parent '
            '(current :: tail) = parent :: prefixFrames (parent * current) tail; '
            'the terminal frame equals parent * the ordered finite product.'),
        'verification': {
            'receipt': str(receipt.resolve()), 'run': 'output/run-k87wlFSd',
            'compile_exit': 0, 'verify_exit': 0,
            'standard_axioms_only': True, 'no_sorry': True, 'no_admit': True,
            'source_sha256': sha(source), 'olean_sha256': sha(olean),
            'base_source_sha256': sha(base_source),
            'base_olean_sha256': sha(base_olean)}}

    mass = nodes['B45-1_mass_functional_identity']
    deps = list(mass.get('dependencies', []))
    if 'B45-1_frame_recursion' not in deps:
        deps.append('B45-1_frame_recursion')
    mass['dependencies'] = deps
    precursors = list(mass.get('compiled_precursors', []))
    if 'B45-1_frame_recursion' not in precursors:
        precursors.append('B45-1_frame_recursion')
    mass['compiled_precursors'] = precursors
    nodes['source_semantics'].setdefault('fourier_normal_form', {})[
        'frame_recursion'] = 'compiled_candidate'
    nodes['source_semantics']['fourier_normal_form'][
        'frame_recursion_receipt'] = str(receipt.resolve())

    for obligation in graph['source_binding_obligations']:
        if obligation['id'] == 'B45-1':
            if 'B45-1_frame_recursion' not in obligation['subnodes']:
                obligation['subnodes'].insert(2, 'B45-1_frame_recursion')
            obligation['frame_recursion'] = 'compiled_candidate_comparator_pending'

    graph['next_frontier'] = [
        'B45-1.c body mass Fourier evaluator for all q',
        'B45-1.g comparator-backed q=0 bridge admission',
        'B45-1.i Float64 enclosure bridge',
        'B45-2 potential and gradient reconstruction',
        'B45-3 H0 and gradient-zero binding',
        'B45-4 Christoffel FD binding',
        'B45-5_residual_domain_bound',
        'positive_supply_eta_physical_projection_and_relative_bound',
        'positive_supply_two_regime_physical_assembly',
        'positive_supply_equilibrium_floor',
        'actual mass PSD and eta bounds',
        'uniform_fixed_identity_scalar_source_gate',
        'all_domain_continuation']
    graph['nodes'] = list(nodes.values())

    def visit(key, stack):
        assert key not in stack, key
        for dep in nodes[key].get('dependencies', []):
            assert dep in nodes, (key, dep)
            visit(dep, stack | {key})

    for key in nodes:
        visit(key, set())

    backup = ROOT / 'artifacts/routeb_storage_checkpoint_20260905/state-before-revision59.json'
    assert not backup.exists()
    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + '\n',
                          encoding='utf-8')
    m4 = next(node for node in state.nodes.values()
              if node.name.startswith('M4.') and
              node.name != 'M4.correlated_momentum_closure')
    m4.metadata.setdefault('proposed_mathematical_dags', []).append(ref(graph_path))
    m4.metadata['next_mathematical_frontier'] = graph['next_frontier']
    state.event(
        'routeb_b45_1_frame_recursion_checkpoint',
        proposed_dag=ref(graph_path), original_target_unchanged=True,
        actual_J_proved=False, formal_certificate_allowed=False,
        comparator_accepted=False, registry_promotions=0,
        broad_regression_run=False, physical_frame_binding_open=True)
    store.save(state)
    print(json.dumps(dict(revision=state.revision, nodes=len(state.nodes),
                         graph_nodes=len(nodes), registry=len(state.registry),
                         formal_certificate_allowed=False)))


if __name__ == '__main__':
    main()
