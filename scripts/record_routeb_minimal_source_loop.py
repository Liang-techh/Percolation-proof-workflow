"""Record the repaired low-dependency source-loop Lean candidate."""
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
    assert state.revision == 102 and not state.registry
    side = ROOT / 'examples/routeb_agent_minimal_source_loop_lean'
    receipt = side / 'FINAL_RECEIPT.md'
    source = side / 'output/run-GKVqBwZa/RouteBMinimalSourceLoop.lean'
    olean = side / 'output/run-GKVqBwZa/RouteBMinimalSourceLoop.olean'
    log = side / 'output/run-GKVqBwZa/terminal.log'
    old_graph = ROOT / 'artifacts/routeb_6dof/block45-obligations-v60.json'
    graph_path = ROOT / 'artifacts/routeb_6dof/block45-obligations-v61.json'
    backup = ROOT / 'artifacts/routeb_storage_checkpoint_20260905/state-before-revision103.json'
    for path in (receipt, source, olean, log, old_graph):
        assert path.is_file()
    assert not graph_path.exists() and not backup.exists()
    assert sha(source) == '82a8d0d7c7e6ea7ab8867d4c1113cdff23b146b441a9c08442a9b187594480d6'
    assert sha(olean) == 'adaab00bbd19f242df0d147c59f06620c8ef55ed401266cadc8e521fc7f3a5c2'
    receipt_text = receipt.read_text(encoding='utf-8')
    for marker in ('COMPILE_EXIT_CODE=0', 'SOURCE_RESTRICTION_CHECK=PASSED',
                   'MAIN_DAG_STATE_UNCHANGED=true', 'Quot.sound'):
        assert marker in receipt_text
    assert not any(token in source.read_text(encoding='utf-8')
                   for token in ('sorry', 'admit', 'axiom '))
    state.event('routeb_b45_1_minimal_source_loop_compiled',
                receipt=ref(receipt), source=ref(source), olean=ref(olean),
                terminal_log=ref(log), compile_exit=0, verify_exit=0,
                standard_axioms_only=True, source_comparator='open',
                deployed_julia_binding='open', registry_promoted=False,
                formal_certificate_allowed=False)
    graph = json.loads(old_graph.read_text(encoding='utf-8'))
    graph.update(schema='routeb-proposed-proof-dag-v61',
                 supersedes='block45-obligations-v60.json',
                 active_strategy='contract_mass_to_regularized_source_mass')
    nodes = {node['id']: node for node in graph['nodes']}
    node_id = 'B45-1_minimal_source_loop_mass_sum'
    nodes[node_id] = {
        'id': node_id,
        'status': 'compiled_candidate_comparator_pending',
        'dependencies': [],
        'source': '../../examples/routeb_agent_minimal_source_loop_lean/RouteBMinimalSourceLoop.lean',
        'statement': ('Kernel-check the finite six-body Julia-style mass loop, '
                      'cutoff gating, and rotated-isotropic link accumulation '
                      'against a generic massFromLinks definition.'),
        'verification': {
            'receipt': str(receipt.resolve()), 'run': 'output/run-GKVqBwZa',
            'compile_exit': 0, 'verify_exit': 0,
            'standard_axioms_only': True,
            'source_sha256': sha(source), 'olean_sha256': sha(olean),
            'source_comparator': 'open', 'deployed_julia_binding': 'open'}}
    identity = nodes['B45-1_mass_functional_identity']
    if node_id not in identity.setdefault('compiled_precursors', []):
        identity['compiled_precursors'].append(node_id)
    for obligation in graph['source_binding_obligations']:
        if obligation['id'] == 'B45-1':
            subnodes = obligation.setdefault('subnodes', [])
            if node_id not in subnodes:
                subnodes.insert(25, node_id)
            obligation['minimal_source_loop'] = 'compiled_candidate_comparator_pending'
    graph['next_frontier'] = [
        'B45-1 bind minimal source loop to deployed mass_matrix semantics',
        'B45-1 sourceBodyMass/sourceContract exact index binding',
        'B45-1 sourceBodyMass/sourceContract function extensional bridge',
        'B45-1 bind routeBFrameSlot to homogeneousPrefix using transport lemma',
        'B45-1 apply source mass-table exact candidate to contract mass sum',
        'B45-1 bind regularized mass entries to Fourier evaluator and canonical CSV coefficients',
        'B45-1 prove Fourier evaluator equals six-body contract sum',
        'B45-1.i Float64 enclosure bridge',
        'B45-5 obtain global enclosures for M_BB-D0, M_BD, a_B, a_D and FD remainder',
        'B45-5 bind sourceBlockForce to expectedSourceForce',
        'B45-5 bind sourceBlockForce to sourceDescriptorRhs',
        'positive_supply prove eta(0)=0 or exact equilibrium floor',
        'positive_supply prove state-relative eta scaling or commit direct-gate branch',
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
    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    state.event('routeb_b45_1_minimal_source_loop_checkpoint',
                proposed_dag=ref(graph_path), original_target_unchanged=True,
                deployed_source_binding_open=True, source_comparator_open=True,
                formal_certificate_allowed=False, registry_promotions=0,
                broad_regression_run=False)
    store.save(state)
    print({'revision': state.revision, 'graph_nodes': len(nodes),
           'registry': len(state.registry), 'formal_certificate_allowed': False})


if __name__ == '__main__':
    main()
