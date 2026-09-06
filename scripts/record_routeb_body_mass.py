"""Record the compiled body COM/Jacobian mass-semantic leaf."""
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
    assert state.revision == 66 and not state.registry
    side = ROOT / 'examples/routeb_body_mass_lean'
    receipt = side / 'FINAL_RECEIPT.md'
    source = side / 'output/run-vB4nl7Rh/BodyMass.lean'
    olean = side / 'output/run-vB4nl7Rh/BodyMass.olean'
    log = side / 'output/run-vB4nl7Rh/terminal.log'
    old_graph = ROOT / 'artifacts/routeb_6dof/block45-obligations-v30.json'
    graph_path = ROOT / 'artifacts/routeb_6dof/block45-obligations-v31.json'
    for path in (receipt, source, olean, log, old_graph):
        assert path.is_file()
    assert not graph_path.exists()
    assert sha(source) == '65a9cacfc15eea1603ee364148e477b9a2978dd1144f785e705be87d2c201aff'
    assert sha(olean) == 'c437b10ceaaf7287e8caf2269fb7b621155e4607d61734b22991551777a1ca46'
    log_text = log.read_text(encoding='utf-8')
    receipt_text = receipt.read_text(encoding='utf-8')
    for marker in ('BodyMass_COMPILE_EXIT_CODE=0', 'VERIFY_EXIT_CODE=0',
                   'SOURCE_RESTRICTION_CHECK=PASSED',
                   'PHYSICAL_FRAME_BINDING=OPEN', 'FLOAT64_BINDING=OPEN',
                   'propext'):
        assert marker in log_text + receipt_text
    assert 'sorryAx' not in log_text

    state.event(
        'routeb_b45_1_body_com_jacobian_mass_compiled',
        receipt=ref(receipt), source=ref(source), olean=ref(olean),
        terminal_log=ref(log), compile_exit=0, verify_exit=0,
        standard_axioms_only=True, source_independent=True,
        midpoint_com=True, parent_axis=True, jacobian_cutoff=True,
        body_mass_gram_expansion=True, physical_frame_binding=False,
        float64_binding=False, registry_promoted=False,
        formal_certificate_allowed=False)

    graph = json.loads(old_graph.read_text(encoding='utf-8'))
    graph.update(schema='routeb-proposed-proof-dag-v31',
                 supersedes='block45-obligations-v30.json',
                 active_strategy='bind_body_observables_to_frame_chain')
    nodes = {node['id']: node for node in graph['nodes']}
    nodes['B45-1_body_com_jacobian_mass_semantics'] = {
        'id': 'B45-1_body_com_jacobian_mass_semantics',
        'status': 'compiled_candidate_comparator_pending',
        'dependencies': ['B45-1_real_dh_step_bridge', 'B45-1_fin6_index_adapter'],
        'source': '../../examples/routeb_body_mass_lean/BodyMass.lean',
        'statement': (
            'Kernel-check midpoint COM, pre-current parent-axis Jacobians, '
            'ancestor cutoff, inactive-column zeroing, and the body mass Gram '
            'expansion used by the full six-link functional.'),
        'verification': {
            'receipt': str(receipt.resolve()), 'run': 'output/run-vB4nl7Rh',
            'compile_exit': 0, 'verify_exit': 0,
            'standard_axioms_only': True,
            'source_sha256': sha(source), 'olean_sha256': sha(olean)}}
    identity = nodes['B45-1_mass_functional_identity']
    deps = list(identity.get('dependencies', []))
    if 'B45-1_body_com_jacobian_mass_semantics' not in deps:
        deps.append('B45-1_body_com_jacobian_mass_semantics')
    identity['dependencies'] = deps
    identity.setdefault('compiled_precursors', [])
    if 'B45-1_body_com_jacobian_mass_semantics' not in identity['compiled_precursors']:
        identity['compiled_precursors'].append('B45-1_body_com_jacobian_mass_semantics')
    for obligation in graph['source_binding_obligations']:
        if obligation['id'] == 'B45-1':
            subnodes = obligation.setdefault('subnodes', [])
            if 'B45-1_body_com_jacobian_mass_semantics' not in subnodes:
                subnodes.insert(2, 'B45-1_body_com_jacobian_mass_semantics')
            obligation['body_com_jacobian_semantics'] = 'compiled_candidate_comparator_pending'
            obligation['frame_to_origin_axis_binding'] = 'open'
            obligation['body_mass_function_binding'] = 'open'
    graph['next_frontier'] = [
        'B45-1 bind frame-chain origins and pre-current axes to source arrays',
        'B45-1 instantiate COM/Jacobian body semantics for six Route-B links',
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
    backup = ROOT / 'artifacts/routeb_storage_checkpoint_20260905/state-before-revision66.json'
    assert not backup.exists()
    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    m4 = next(node for node in state.nodes.values()
              if node.name.startswith('M4.') and node.name != 'M4.correlated_momentum_closure')
    m4.metadata.setdefault('proposed_mathematical_dags', []).append(ref(graph_path))
    m4.metadata['next_mathematical_frontier'] = graph['next_frontier']
    state.event(
        'routeb_b45_1_body_com_jacobian_mass_checkpoint', proposed_dag=ref(graph_path),
        original_target_unchanged=True, actual_J_proved=False,
        formal_certificate_allowed=False, comparator_accepted=False,
        registry_promotions=0, broad_regression_run=False,
        frame_origin_axis_binding_open=True)
    store.save(state)
    print(json.dumps(dict(revision=state.revision, nodes=len(state.nodes),
                         graph_nodes=len(nodes), registry=len(state.registry),
                         formal_certificate_allowed=False)))


if __name__ == '__main__':
    main()
