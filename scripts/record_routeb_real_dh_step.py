"""Record the compiled ideal-real six-step DH bridge."""
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
    assert state.revision == 65 and not state.registry
    side = ROOT / 'examples/routeb_real_dh_step_lean'
    receipt = side / 'FINAL_RECEIPT.md'
    source = side / 'output/run-nAZVlwhR/RealDHStep.lean'
    olean = side / 'output/run-nAZVlwhR/RealDHStep.olean'
    log = side / 'output/run-nAZVlwhR/terminal.log'
    old_graph = ROOT / 'artifacts/routeb_6dof/block45-obligations-v29.json'
    graph_path = ROOT / 'artifacts/routeb_6dof/block45-obligations-v30.json'
    for path in (receipt, source, olean, log, old_graph):
        assert path.is_file()
    assert not graph_path.exists()
    assert sha(source) == '9c04da5b9627ee749c53009733006934f95b2d33265e46ca59d0725aa453786a'
    assert sha(olean) == '16c705c9907e302e4351d9ad47923d5c115b83bd9707bdd3b0c7fd3068a0411b'
    log_text = log.read_text(encoding='utf-8')
    receipt_text = receipt.read_text(encoding='utf-8')
    for marker in ('RealDHStep_COMPILE_EXIT_CODE=0', 'VERIFY_EXIT_CODE=0',
                   'SOURCE_RESTRICTION_CHECK=PASSED',
                   'JULIA_FLOAT64_BINDING=OPEN', 'FULL_MASS_BINDING=OPEN',
                   'propext'):
        assert marker in log_text + receipt_text
    assert 'sorryAx' not in log_text

    state.event(
        'routeb_b45_1_real_dh_step_bridge_compiled',
        receipt=ref(receipt), source=ref(source), olean=ref(olean),
        terminal_log=ref(log), compile_exit=0, verify_exit=0,
        standard_axioms_only=True, ideal_real_bridge=True,
        six_step_specialization=True, julia_float64_binding=False,
        full_mass_binding=False, registry_promoted=False,
        formal_certificate_allowed=False)

    graph = json.loads(old_graph.read_text(encoding='utf-8'))
    graph.update(schema='routeb-proposed-proof-dag-v30',
                 supersedes='block45-obligations-v29.json',
                 active_strategy='lift_real_dh_step_to_frame_and_mass')
    nodes = {node['id']: node for node in graph['nodes']}
    nodes['B45-1_real_dh_step_bridge'] = {
        'id': 'B45-1_real_dh_step_bridge',
        'status': 'compiled_candidate_comparator_pending',
        'dependencies': ['B45-1_fourier_phase_bridge', 'B45-1_fin6_index_adapter'],
        'source': '../../examples/routeb_real_dh_step_lean/RealDHStep.lean',
        'statement': (
            'Kernel-check the six ideal-real Route-B DH step matrices entrywise: '
            'each complex Fourier step equals the complex coercion of its explicit '
            'real trigonometric step matrix.'),
        'verification': {
            'receipt': str(receipt.resolve()), 'run': 'output/run-nAZVlwhR',
            'compile_exit': 0, 'verify_exit': 0,
            'standard_axioms_only': True,
            'source_sha256': sha(source), 'olean_sha256': sha(olean)}}
    identity = nodes['B45-1_mass_functional_identity']
    deps = list(identity.get('dependencies', []))
    if 'B45-1_real_dh_step_bridge' not in deps:
        deps.append('B45-1_real_dh_step_bridge')
    identity['dependencies'] = deps
    identity.setdefault('compiled_precursors', [])
    if 'B45-1_real_dh_step_bridge' not in identity['compiled_precursors']:
        identity['compiled_precursors'].append('B45-1_real_dh_step_bridge')
    for obligation in graph['source_binding_obligations']:
        if obligation['id'] == 'B45-1':
            subnodes = obligation.setdefault('subnodes', [])
            if 'B45-1_real_dh_step_bridge' not in subnodes:
                subnodes.insert(1, 'B45-1_real_dh_step_bridge')
            obligation['ideal_real_step_bridge'] = 'compiled_candidate_comparator_pending'
            obligation['julia_float64_binding'] = 'open'
            obligation['full_mass_binding'] = 'open'
    graph['next_frontier'] = [
        'B45-1 source frame recursion with explicit origins and parent axes',
        'B45-1 COM midpoint and cross-product Jacobian columns',
        'B45-1 body mass Fourier evaluator for all q',
        'B45-1.i Float64 enclosure bridge',
        'B45-2 deployed potential and central-FD gradient binding',
        'B45-3 H0 and gradient-zero binding',
        'B45-4 Christoffel FD binding',
        'B45-5_residual_domain_bound',
        'positive_supply relative scaling and equilibrium floor',
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
    backup = ROOT / 'artifacts/routeb_storage_checkpoint_20260905/state-before-revision65.json'
    assert not backup.exists()
    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    m4 = next(node for node in state.nodes.values()
              if node.name.startswith('M4.') and node.name != 'M4.correlated_momentum_closure')
    m4.metadata.setdefault('proposed_mathematical_dags', []).append(ref(graph_path))
    m4.metadata['next_mathematical_frontier'] = graph['next_frontier']
    state.event(
        'routeb_b45_1_real_dh_step_bridge_checkpoint', proposed_dag=ref(graph_path),
        original_target_unchanged=True, actual_J_proved=False,
        formal_certificate_allowed=False, comparator_accepted=False,
        registry_promotions=0, broad_regression_run=False,
        source_frame_origin_adapter_open=True)
    store.save(state)
    print(json.dumps(dict(revision=state.revision, nodes=len(state.nodes),
                         graph_nodes=len(nodes), registry=len(state.registry),
                         formal_certificate_allowed=False)))


if __name__ == '__main__':
    main()
