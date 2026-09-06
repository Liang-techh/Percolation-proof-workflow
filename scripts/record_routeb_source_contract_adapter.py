"""Record the compiled source origin/axis contract adapter."""
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
    assert state.revision == 72 and not state.registry
    side = ROOT / 'examples/routeb_source_contract_adapter_lean'
    receipt = side / 'FINAL_RECEIPT.md'
    source = side / 'output/run-RSGGTurS/SourceContractAdapter.lean'
    olean = side / 'output/run-RSGGTurS/SourceContractAdapter.olean'
    log = side / 'output/run-RSGGTurS/terminal.log'
    old_graph = ROOT / 'artifacts/routeb_6dof/block45-obligations-v36.json'
    graph_path = ROOT / 'artifacts/routeb_6dof/block45-obligations-v37.json'
    for path in (receipt, source, olean, log, old_graph):
        assert path.is_file()
    assert not graph_path.exists()
    assert sha(source) == '58c0b15b6fceb1064f773acdb9f684dc55a021ac69a030c13e1c8b46f7b9a8dc'
    assert sha(olean) == 'c1908efdfe68c5515623290fdb1808129da75a437d7d163336882282da23d5f4'
    text = log.read_text(encoding='utf-8') + receipt.read_text(encoding='utf-8')
    for marker in ('SourceContractAdapter_COMPILE_EXIT_CODE=0', 'VERIFY_EXIT_CODE=0',
                   'SOURCE_RESTRICTION_CHECK=PASSED',
                   'JULIA_FLOAT64_BINDING=OPEN', 'FULL_MASS_BINDING=OPEN',
                   'propext'):
        assert marker in text
    assert 'sorryAx' not in text

    state.event(
        'routeb_b45_1_source_contract_adapter_compiled',
        receipt=ref(receipt), source=ref(source), olean=ref(olean),
        terminal_log=ref(log), compile_exit=0, verify_exit=0,
        standard_axioms_only=True, source_origin_function_equality=True,
        source_axis_function_equality=True, source_body_mass_lift=True,
        registry_promoted=False, formal_certificate_allowed=False)

    graph = json.loads(old_graph.read_text(encoding='utf-8'))
    graph.update(schema='routeb-proposed-proof-dag-v37',
                 supersedes='block45-obligations-v36.json',
                 active_strategy='source_slot_contract_adapter_before_body_instantiation')
    nodes = {node['id']: node for node in graph['nodes']}
    nodes['B45-1_source_contract_adapter'] = {
        'id': 'B45-1_source_contract_adapter',
        'status': 'compiled_candidate_comparator_pending',
        'dependencies': ['B45-1_frame_slot_accessor',
                         'B45-1_body_contract_core'],
        'source': '../../examples/routeb_source_contract_adapter_lean/SourceContractAdapter.lean',
        'statement': (
            'Kernel-check equality of the source origin/axis functions with the '
            'frame-slot kinematic contract, then lift it to body mass.'),
        'verification': {
            'receipt': str(receipt.resolve()), 'run': 'output/run-RSGGTurS',
            'compile_exit': 0, 'verify_exit': 0,
            'standard_axioms_only': True,
            'source_sha256': sha(source), 'olean_sha256': sha(olean)}}
    identity = nodes['B45-1_mass_functional_identity']
    deps = list(identity.get('dependencies', []))
    if 'B45-1_source_contract_adapter' not in deps:
        deps.append('B45-1_source_contract_adapter')
    identity['dependencies'] = deps
    identity.setdefault('compiled_precursors', [])
    if 'B45-1_source_contract_adapter' not in identity['compiled_precursors']:
        identity['compiled_precursors'].append('B45-1_source_contract_adapter')
    body_node = nodes['B45-1_body_com_jacobian_mass_semantics']
    body_node['source_contract_adapter'] = 'B45-1_source_contract_adapter'
    body_node['adapter_status'] = 'one_body_source_instantiation_open'
    for obligation in graph['source_binding_obligations']:
        if obligation['id'] == 'B45-1':
            subnodes = obligation.setdefault('subnodes', [])
            if 'B45-1_source_contract_adapter' not in subnodes:
                subnodes.insert(3, 'B45-1_source_contract_adapter')
            obligation['source_contract_adapter'] = 'compiled_candidate_comparator_pending'
            obligation['source_origin_axis_function_binding'] = 'compiled_candidate_comparator_pending'
            obligation['body_mass_function_binding'] = 'open'
    graph['next_frontier'] = [
        'B45-1 instantiate one body COM/Jv/Jw over sourceContract and frameContract',
        'B45-1 close block-(4,5) two-body source semantics through contract lift',
        'B45-1 prove six-body mass sum equals source mass evaluator',
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
    backup = ROOT / 'artifacts/routeb_storage_checkpoint_20260905/state-before-revision72.json'
    assert not backup.exists()
    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    m4 = next(node for node in state.nodes.values()
              if node.name.startswith('M4.') and node.name != 'M4.correlated_momentum_closure')
    m4.metadata.setdefault('proposed_mathematical_dags', []).append(ref(graph_path))
    m4.metadata['next_mathematical_frontier'] = graph['next_frontier']
    state.event(
        'routeb_b45_1_source_contract_adapter_checkpoint', proposed_dag=ref(graph_path),
        original_target_unchanged=True, actual_J_proved=False,
        formal_certificate_allowed=False, comparator_accepted=False,
        registry_promotions=0, broad_regression_run=False,
        one_body_instantiation_open=True)
    store.save(state)
    print(json.dumps(dict(revision=state.revision, nodes=len(state.nodes),
                         graph_nodes=len(nodes), registry=len(state.registry),
                         formal_certificate_allowed=False)))


if __name__ == '__main__':
    main()
