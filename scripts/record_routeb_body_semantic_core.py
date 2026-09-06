"""Record the Mathlib-only body semantic core leaf."""
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
    assert state.revision == 69 and not state.registry
    side = ROOT / 'examples/routeb_body_semantic_core_lean'
    receipt = side / 'FINAL_RECEIPT.md'
    source = side / 'output/run-6vhFP8Zp/BodySemanticCore.lean'
    olean = side / 'output/run-6vhFP8Zp/BodySemanticCore.olean'
    log = side / 'output/run-6vhFP8Zp/terminal.log'
    old_graph = ROOT / 'artifacts/routeb_6dof/block45-obligations-v33.json'
    graph_path = ROOT / 'artifacts/routeb_6dof/block45-obligations-v34.json'
    for path in (receipt, source, olean, log, old_graph):
        assert path.is_file()
    assert not graph_path.exists()
    assert sha(source) == 'fe15f6ca9993f55fc56e6d2c9cca5fa8c7f6e9530b9b900a6f111ed96715149c'
    assert sha(olean) == 'b9e469fd3e40fe1f8ae09686c1cfee813743fe23fbe0979f9564ab4cc84938a3'
    text = log.read_text(encoding='utf-8') + receipt.read_text(encoding='utf-8')
    for marker in ('BodySemanticCore_COMPILE_EXIT_CODE=0', 'VERIFY_EXIT_CODE=0',
                   'SOURCE_RESTRICTION_CHECK=PASSED',
                   'JULIA_FLOAT64_BINDING=OPEN', 'FULL_MASS_BINDING=OPEN',
                   'propext'):
        assert marker in text
    assert 'sorryAx' not in text

    state.event(
        'routeb_b45_1_body_semantic_core_compiled',
        receipt=ref(receipt), source=ref(source), olean=ref(olean),
        terminal_log=ref(log), compile_exit=0, verify_exit=0,
        standard_axioms_only=True, source_independent=True,
        mathlib_only=True, block45_cutoff=True, link_mass_semantics=True,
        registry_promoted=False, formal_certificate_allowed=False)

    graph = json.loads(old_graph.read_text(encoding='utf-8'))
    graph.update(schema='routeb-proposed-proof-dag-v34',
                 supersedes='block45-obligations-v33.json',
                 active_strategy='adapter_over_minimal_body_semantic_core')
    nodes = {node['id']: node for node in graph['nodes']}
    nodes['B45-1_body_semantic_core'] = {
        'id': 'B45-1_body_semantic_core',
        'status': 'compiled_candidate_comparator_pending',
        'dependencies': [],
        'source': '../../examples/routeb_body_semantic_core_lean/BodySemanticCore.lean',
        'statement': (
            'Kernel-check the reusable Mathlib-only body COM/Jacobian/linkMass '
            'core, including the block-(4,5) inactive and active cutoffs, '
            'without importing frame or source modules.'),
        'verification': {
            'receipt': str(receipt.resolve()), 'run': 'output/run-6vhFP8Zp',
            'compile_exit': 0, 'verify_exit': 0,
            'standard_axioms_only': True,
            'source_sha256': sha(source), 'olean_sha256': sha(olean)}}
    body_node = nodes['B45-1_body_com_jacobian_mass_semantics']
    body_node['reusable_core'] = 'B45-1_body_semantic_core'
    body_node['adapter_status'] = 'source_frame_adapter_open'
    identity = nodes['B45-1_mass_functional_identity']
    deps = list(identity.get('dependencies', []))
    if 'B45-1_body_semantic_core' not in deps:
        deps.append('B45-1_body_semantic_core')
    identity['dependencies'] = deps
    identity.setdefault('compiled_precursors', [])
    if 'B45-1_body_semantic_core' not in identity['compiled_precursors']:
        identity['compiled_precursors'].append('B45-1_body_semantic_core')
    for obligation in graph['source_binding_obligations']:
        if obligation['id'] == 'B45-1':
            subnodes = obligation.setdefault('subnodes', [])
            if 'B45-1_body_semantic_core' not in subnodes:
                subnodes.insert(1, 'B45-1_body_semantic_core')
            obligation['body_semantic_core'] = 'compiled_candidate_comparator_pending'
            obligation['body_mass_function_binding'] = 'open'
    graph['next_frontier'] = [
        'B45-1 connect one fixed body to frame-prefix origins/axes over the minimal core',
        'B45-1 instantiate the second block body over the minimal core',
        'B45-1 lift the two-body result to six body contributions',
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
    backup = ROOT / 'artifacts/routeb_storage_checkpoint_20260905/state-before-revision69.json'
    assert not backup.exists()
    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    m4 = next(node for node in state.nodes.values()
              if node.name.startswith('M4.') and node.name != 'M4.correlated_momentum_closure')
    m4.metadata.setdefault('proposed_mathematical_dags', []).append(ref(graph_path))
    m4.metadata['next_mathematical_frontier'] = graph['next_frontier']
    state.event(
        'routeb_b45_1_body_semantic_core_checkpoint', proposed_dag=ref(graph_path),
        original_target_unchanged=True, actual_J_proved=False,
        formal_certificate_allowed=False, comparator_accepted=False,
        registry_promotions=0, broad_regression_run=False,
        frame_adapter_still_open=True)
    store.save(state)
    print(json.dumps(dict(revision=state.revision, nodes=len(state.nodes),
                         graph_nodes=len(nodes), registry=len(state.registry),
                         formal_certificate_allowed=False)))


if __name__ == '__main__':
    main()
