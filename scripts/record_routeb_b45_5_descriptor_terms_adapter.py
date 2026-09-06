"""Record the conditional B45-5 descriptor-terms adapter candidate."""
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
    assert state.revision == 94 and not state.registry
    side = ROOT / 'examples/routeb_b45_5_descriptor_terms_adapter_lean'
    receipt = side / 'FINAL_RECEIPT.md'
    source = side / 'output/run-XqI2UV9g/DescriptorTermsAdapter.lean'
    olean = side / 'output/run-XqI2UV9g/DescriptorTermsAdapter.olean'
    log = side / 'output/run-XqI2UV9g/terminal.log'
    old_graph = ROOT / 'artifacts/routeb_6dof/block45-obligations-v55.json'
    graph_path = ROOT / 'artifacts/routeb_6dof/block45-obligations-v56.json'
    for path in (receipt, source, olean, log, old_graph):
        assert path.is_file()
    assert not graph_path.exists()
    assert sha(source) == '1455d987f899102e68346a7d8d074b8aa472d721151b6992d373f005a955750a'
    assert sha(olean) == '4095e24335529b5bb9f8eebfe2f0b784c0ad4c60affe80af1378f2daa2ad61a1'
    text = log.read_text(encoding='utf-8') + receipt.read_text(encoding='utf-8')
    for marker in ('DescriptorTermsAdapter_COMPILE_EXIT_CODE=0',
                   'VERIFY_EXIT_CODE=0', 'SOURCE_RESTRICTION_CHECK=PASSED',
                   'RESIDUAL_BOUND=OPEN', 'FLOAT64_BINDING=OPEN',
                   'SOURCE_COMPARATOR=OPEN', 'propext', 'Classical.choice',
                   'Quot.sound'):
        assert marker in text
    assert 'sorryAx' not in text

    state.event('routeb_b45_5_descriptor_terms_adapter_compiled',
                receipt=ref(receipt), source=ref(source), olean=ref(olean),
                terminal_log=ref(log), compile_exit=0, verify_exit=0,
                standard_axioms_only=True, source_comparator_open=True,
                residual_bound_open=True, registry_promoted=False,
                formal_certificate_allowed=False)

    graph = json.loads(old_graph.read_text(encoding='utf-8'))
    graph.update(schema='routeb-proposed-proof-dag-v56',
                 supersedes='block45-obligations-v55.json',
                 active_strategy='exact_b45_5_residual_decomposition_then_source_binding')
    nodes = {node['id']: node for node in graph['nodes']}
    node_id = 'B45-5_descriptor_terms_adapter'
    nodes[node_id] = {
        'id': node_id,
        'status': 'compiled_candidate_comparator_pending',
        'dependencies': ['B45-5_residual_decomposition_exact_lean'],
        'source': '../../examples/routeb_b45_5_descriptor_terms_adapter_lean/DescriptorTermsAdapter.lean',
        'statement': ('Kernel-check the B45-5 descriptor residual ledger and expose '
                      'the two source-comparator equalities needed for the exact '
                      'six-term residual decomposition.'),
        'verification': {
            'receipt': str(receipt.resolve()), 'run': 'output/run-XqI2UV9g',
            'compile_exit': 0, 'verify_exit': 0,
            'standard_axioms_only': True,
            'source_sha256': sha(source), 'olean_sha256': sha(olean),
            'source_comparator': 'open', 'residual_domain_bound': 'open',
            'float64_binding': 'open'}}
    parent = nodes['B45-5_pmi_residual_decomposition']
    if node_id not in parent.setdefault('dependencies', []):
        parent['dependencies'].append(node_id)
    parent['source_binding'] = 'open_two_source_equalities'
    parent['descriptor_terms_adapter'] = 'compiled_candidate_comparator_pending'
    for obligation in graph['source_binding_obligations']:
        if obligation['id'] == 'B45-5':
            subnodes = obligation.setdefault('subnodes', [])
            if node_id not in subnodes:
                subnodes.insert(1, node_id)
            obligation['descriptor_terms_adapter'] = 'compiled_candidate_comparator_pending'
            obligation['source_comparator_equalities'] = 2
            obligation['residual_domain_bound'] = 'open'
    graph['next_frontier'] = [
        'B45-5 bind sourceBlockForce to expectedSourceForce',
        'B45-5 bind sourceBlockForce to sourceDescriptorRhs',
        'B45-1 bind routeBFrameSlot to homogeneousPrefix using transport lemma',
        'B45-1 sourceBodyMass and concrete mass-table binding',
        'B45-1 bind regularized mass entries to Fourier evaluator and canonical CSV coefficients',
        'B45-1 prove Fourier evaluator equals six-body contract sum',
        'B45-1.i Float64 enclosure bridge',
        'B45-5_residual_domain_bound',
        'positive_supply prove equilibrium vanishing or exact floor',
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
    backup = ROOT / 'artifacts/routeb_storage_checkpoint_20260905/state-before-revision95.json'
    assert not backup.exists()
    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    state.event('routeb_b45_5_descriptor_terms_adapter_checkpoint',
                proposed_dag=ref(graph_path), original_target_unchanged=True,
                source_comparator_open=True, residual_domain_bound_open=True,
                formal_certificate_allowed=False, comparator_accepted=False,
                registry_promotions=0, broad_regression_run=False)
    store.save(state)
    print(json.dumps(dict(revision=state.revision, graph_nodes=len(nodes),
                          registry=len(state.registry), formal_certificate_allowed=False)))


if __name__ == '__main__':
    main()
