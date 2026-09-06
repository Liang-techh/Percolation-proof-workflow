"""Record the compiled block-(4,5) single-body contract specialization."""
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
    assert state.revision == 73 and not state.registry
    side = ROOT / 'examples/routeb_single_body_contract_instantiation_lean'
    receipt = side / 'FINAL_RECEIPT.md'
    source = side / 'output/run-XSWyT6w1/SingleBodyContractInstantiation.lean'
    olean = side / 'output/run-XSWyT6w1/SingleBodyContractInstantiation.olean'
    log = side / 'output/run-XSWyT6w1/terminal.log'
    old_graph = ROOT / 'artifacts/routeb_6dof/block45-obligations-v37.json'
    graph_path = ROOT / 'artifacts/routeb_6dof/block45-obligations-v38.json'
    for path in (receipt, source, olean, log, old_graph):
        assert path.is_file()
    assert not graph_path.exists()
    assert sha(source) == '3d38adef4396a5db0b01c3b85102b29c2c4f2f1bf9e8b3cc2e12ea31877b7f95'
    assert sha(olean) == 'e14eb735fa0bf9f9aef78928fe696bd2bcd08d0856468c801277fdd2c8dcb609'
    text = log.read_text(encoding='utf-8') + receipt.read_text(encoding='utf-8')
    for marker in ('SingleBodyContractInstantiation_COMPILE_EXIT_CODE=0',
                   'VERIFY_EXIT_CODE=0', 'SOURCE_RESTRICTION_CHECK=PASSED',
                   'JULIA_FLOAT64_BINDING=OPEN', 'FULL_MASS_BINDING=OPEN',
                   'propext'):
        assert marker in text
    assert 'sorryAx' not in text

    state.event(
        'routeb_b45_1_single_body_contract_instantiated',
        receipt=ref(receipt), source=ref(source), olean=ref(olean),
        terminal_log=ref(log), compile_exit=0, verify_exit=0,
        standard_axioms_only=True, block45_link4_cutoff=True,
        block45_link5_active=True, body3_mass_lift=True, body4_mass_lift=True,
        registry_promoted=False, formal_certificate_allowed=False)

    graph = json.loads(old_graph.read_text(encoding='utf-8'))
    graph.update(schema='routeb-proposed-proof-dag-v38',
                 supersedes='block45-obligations-v37.json',
                 active_strategy='two_body_mass_sum_over_closed_single_body_leaves')
    nodes = {node['id']: node for node in graph['nodes']}
    nodes['B45-1_single_body_contract_instantiation'] = {
        'id': 'B45-1_single_body_contract_instantiation',
        'status': 'compiled_candidate_comparator_pending',
        'dependencies': ['B45-1_source_contract_adapter'],
        'source': '../../examples/routeb_single_body_contract_instantiation_lean/SingleBodyContractInstantiation.lean',
        'statement': (
            'Kernel-check the block-(4,5) body-3 and body-4 cutoffs and lift '
            'source/frame contract equality to each body mass separately.'),
        'verification': {
            'receipt': str(receipt.resolve()), 'run': 'output/run-XSWyT6w1',
            'compile_exit': 0, 'verify_exit': 0,
            'standard_axioms_only': True,
            'source_sha256': sha(source), 'olean_sha256': sha(olean)}}
    identity = nodes['B45-1_mass_functional_identity']
    deps = list(identity.get('dependencies', []))
    if 'B45-1_single_body_contract_instantiation' not in deps:
        deps.append('B45-1_single_body_contract_instantiation')
    identity['dependencies'] = deps
    identity.setdefault('compiled_precursors', [])
    if 'B45-1_single_body_contract_instantiation' not in identity['compiled_precursors']:
        identity['compiled_precursors'].append('B45-1_single_body_contract_instantiation')
    for obligation in graph['source_binding_obligations']:
        if obligation['id'] == 'B45-1':
            subnodes = obligation.setdefault('subnodes', [])
            if 'B45-1_single_body_contract_instantiation' not in subnodes:
                subnodes.insert(4, 'B45-1_single_body_contract_instantiation')
            obligation['single_body_contract_instantiation'] = 'compiled_candidate_comparator_pending'
            obligation['body_mass_function_binding'] = 'open'
    graph['next_frontier'] = [
        'B45-1 combine body-3 and body-4 source/frame mass contributions',
        'B45-1 close block-(4,5) two-body source semantics',
        'B45-1 lift two-body result to six body contributions',
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
    backup = ROOT / 'artifacts/routeb_storage_checkpoint_20260905/state-before-revision73.json'
    assert not backup.exists()
    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    m4 = next(node for node in state.nodes.values()
              if node.name.startswith('M4.') and node.name != 'M4.correlated_momentum_closure')
    m4.metadata.setdefault('proposed_mathematical_dags', []).append(ref(graph_path))
    m4.metadata['next_mathematical_frontier'] = graph['next_frontier']
    state.event(
        'routeb_b45_1_single_body_contract_checkpoint', proposed_dag=ref(graph_path),
        original_target_unchanged=True, actual_J_proved=False,
        formal_certificate_allowed=False, comparator_accepted=False,
        registry_promotions=0, broad_regression_run=False,
        two_body_mass_sum_open=True)
    store.save(state)
    print(json.dumps(dict(revision=state.revision, nodes=len(state.nodes),
                         graph_nodes=len(nodes), registry=len(state.registry),
                         formal_certificate_allowed=False)))


if __name__ == '__main__':
    main()
