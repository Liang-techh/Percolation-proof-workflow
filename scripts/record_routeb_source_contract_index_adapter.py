"""Record the exact source/body index adapter candidate."""
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
    assert state.revision == 96 and not state.registry
    side = ROOT / 'examples/routeb_source_contract_index_adapter_lean'
    receipt = side / 'FINAL_RECEIPT.md'
    source = side / 'output/run-a7DRfXYo/SourceContractIndexAdapter.lean'
    olean = side / 'output/run-a7DRfXYo/SourceContractIndexAdapter.olean'
    log = side / 'output/run-a7DRfXYo/terminal.log'
    old_graph = ROOT / 'artifacts/routeb_6dof/block45-obligations-v57.json'
    graph_path = ROOT / 'artifacts/routeb_6dof/block45-obligations-v58.json'
    for path in (receipt, source, olean, log, old_graph):
        assert path.is_file()
    assert not graph_path.exists()
    assert sha(source) == '2a18c7b6733af6245f3e5ba6dedd714a9ec7f28fd010122c0258611ce7aac452'
    assert sha(olean) == '50d88296516473e139828678507fda455467b052dd3330e5563f68f4aa41a9da'
    text = log.read_text(encoding='utf-8') + receipt.read_text(encoding='utf-8')
    for marker in ('SourceContractIndexAdapter_COMPILE_EXIT_CODE=0',
                   'SOURCE_RESTRICTION_CHECK=PASSED', 'VERIFY_EXIT_CODE=0',
                   'DH_NUMERIC_EXPANSION=AVOIDED', 'JULIA_FLOAT64_BINDING=OPEN'):
        assert marker in text
    assert 'sorryAx' not in text.lower()
    state.event('routeb_b45_1_source_contract_index_adapter_compiled',
                receipt=ref(receipt), source=ref(source), olean=ref(olean),
                terminal_log=ref(log), compile_exit=0, verify_exit=0,
                standard_axioms_only=True, dh_numeric_expansion=False,
                julia_float64_binding_open=True, registry_promoted=False,
                formal_certificate_allowed=False)
    graph = json.loads(old_graph.read_text(encoding='utf-8'))
    graph.update(schema='routeb-proposed-proof-dag-v58',
                 supersedes='block45-obligations-v57.json',
                 active_strategy='contract_mass_to_regularized_source_mass')
    nodes = {node['id']: node for node in graph['nodes']}
    node_id = 'B45-1_source_contract_index_adapter_exact'
    nodes[node_id] = {
        'id': node_id,
        'status': 'compiled_candidate_comparator_pending',
        'dependencies': ['B45-1_source_contract_adapter', 'B45-1_fin6_index_adapter'],
        'source': '../../examples/routeb_source_contract_index_adapter_lean/SourceContractIndexAdapter.lean',
        'statement': ('Kernel-check exact body-4/body-5 COM endpoints, parent-axis '
                      'slots, active joint columns, and inactive cutoff indices '
                      'for the source contract.'),
        'verification': {
            'receipt': str(receipt.resolve()), 'run': 'output/run-a7DRfXYo',
            'compile_exit': 0, 'verify_exit': 0,
            'standard_axioms_only': True,
            'source_sha256': sha(source), 'olean_sha256': sha(olean),
            'dh_numeric_expansion': False,
            'julia_float64_binding': 'open',
            'source_comparator': 'open'}}
    identity = nodes['B45-1_mass_functional_identity']
    if node_id not in identity.setdefault('dependencies', []):
        identity['dependencies'].append(node_id)
    if node_id not in identity.setdefault('compiled_precursors', []):
        identity['compiled_precursors'].append(node_id)
    for obligation in graph['source_binding_obligations']:
        if obligation['id'] == 'B45-1':
            subnodes = obligation.setdefault('subnodes', [])
            if node_id not in subnodes:
                subnodes.insert(23, node_id)
            obligation['source_contract_index_adapter'] = 'compiled_candidate_comparator_pending'
            obligation['source_body_mass_binding'] = 'open'
    graph['next_frontier'] = [
        'B45-1 sourceBodyMass/sourceContract exact index binding',
        'B45-1 bind routeBFrameSlot to homogeneousPrefix using transport lemma',
        'B45-1 apply source mass-table exact candidate to contract mass sum',
        'B45-1 bind regularized mass entries to Fourier evaluator and canonical CSV coefficients',
        'B45-1 prove Fourier evaluator equals six-body contract sum',
        'B45-1.i Float64 enclosure bridge',
        'B45-5 bind sourceBlockForce to expectedSourceForce',
        'B45-5 bind sourceBlockForce to sourceDescriptorRhs',
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
    backup = ROOT / 'artifacts/routeb_storage_checkpoint_20260905/state-before-revision97.json'
    assert not backup.exists()
    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    state.event('routeb_b45_1_source_contract_index_adapter_checkpoint',
                proposed_dag=ref(graph_path), original_target_unchanged=True,
                source_body_mass_binding_open=True, source_comparator_open=True,
                formal_certificate_allowed=False, comparator_accepted=False,
                registry_promotions=0, broad_regression_run=False)
    store.save(state)
    print(json.dumps(dict(revision=state.revision, graph_nodes=len(nodes),
                          registry=len(state.registry), formal_certificate_allowed=False)))


if __name__ == '__main__':
    main()
