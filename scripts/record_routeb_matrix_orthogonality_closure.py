"""Record cumulative rotation orthogonality closure."""
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
    assert state.revision == 80 and not state.registry
    side = ROOT / 'examples/routeb_matrix_orthogonality_closure_lean'
    receipt = side / 'FINAL_RECEIPT.md'
    source = side / 'output/run-w9gDKPMw/MatrixOrthogonalityClosure.lean'
    olean = side / 'output/run-w9gDKPMw/MatrixOrthogonalityClosure.olean'
    log = side / 'output/run-w9gDKPMw/terminal.log'
    old_graph = ROOT / 'artifacts/routeb_6dof/block45-obligations-v44.json'
    graph_path = ROOT / 'artifacts/routeb_6dof/block45-obligations-v45.json'
    for path in (receipt, source, olean, log, old_graph):
        assert path.is_file()
    assert not graph_path.exists()
    assert sha(source) == '4b40d536f6a70cbcf75e7811cb58d2ec658057b22b89bc25598346ff95f7b292'
    assert sha(olean) == '8f48da24ee25652d6d458288af56c6987dde30d6619d40da05915e7e15dcfd86'
    text = log.read_text(encoding='utf-8') + receipt.read_text(encoding='utf-8')
    for marker in ('MatrixOrthogonalityClosure_COMPILE_EXIT_CODE=0', 'VERIFY_EXIT_CODE=0',
                   'SOURCE_RESTRICTION_CHECK=PASSED', 'JULIA_FLOAT64_BINDING=OPEN',
                   'FULL_MASS_BINDING=OPEN', 'propext'):
        assert marker in text
    assert 'sorryAx' not in text
    state.event('routeb_b45_1_matrix_orthogonality_closure_compiled', receipt=ref(receipt),
                source=ref(source), olean=ref(olean), terminal_log=ref(log),
                compile_exit=0, verify_exit=0, standard_axioms_only=True,
                cumulative_frame_rotation_closure=True, registry_promoted=False,
                formal_certificate_allowed=False)
    graph = json.loads(old_graph.read_text(encoding='utf-8'))
    graph.update(schema='routeb-proposed-proof-dag-v45',
                 supersedes='block45-obligations-v44.json',
                 active_strategy='cumulative_frame_rotation_before_rotated_inertia')
    nodes = {node['id']: node for node in graph['nodes']}
    nodes['B45-1_matrix_orthogonality_closure'] = {
        'id': 'B45-1_matrix_orthogonality_closure',
        'status': 'compiled_candidate_comparator_pending',
        'dependencies': [],
        'source': '../../examples/routeb_matrix_orthogonality_closure_lean/MatrixOrthogonalityClosure.lean',
        'statement': 'Kernel-check closure of row-orthogonality under cumulative frame matrix multiplication.',
        'verification': {'receipt': str(receipt.resolve()), 'run': 'output/run-w9gDKPMw',
                         'compile_exit': 0, 'verify_exit': 0,
                         'standard_axioms_only': True,
                         'source_sha256': sha(source), 'olean_sha256': sha(olean)}}
    identity = nodes['B45-1_mass_functional_identity']
    deps = list(identity.get('dependencies', []))
    if 'B45-1_matrix_orthogonality_closure' not in deps:
        deps.append('B45-1_matrix_orthogonality_closure')
    identity['dependencies'] = deps
    identity.setdefault('compiled_precursors', [])
    if 'B45-1_matrix_orthogonality_closure' not in identity['compiled_precursors']:
        identity['compiled_precursors'].append('B45-1_matrix_orthogonality_closure')
    for obligation in graph['source_binding_obligations']:
        if obligation['id'] == 'B45-1':
            subnodes = obligation.setdefault('subnodes', [])
            if 'B45-1_matrix_orthogonality_closure' not in subnodes:
                subnodes.insert(11, 'B45-1_matrix_orthogonality_closure')
            obligation['cumulative_rotation_orthogonality'] = 'compiled_candidate_comparator_pending'
            obligation['rotated_inertia_binding'] = 'open'
    graph['next_frontier'] = [
        'B45-1 lift step rotation orthogonality through six-step frame prefix',
        'B45-1 combine cumulative source rotation orthogonality with isotropic inertia bridge',
        'B45-1 bind rotated isotropic inertia per body to fixed contract inertia',
        'B45-1 bind six-body contract sum to concrete source mass evaluator',
        'B45-1 prove Fourier evaluator equals six-body contract sum',
        'B45-1 include explicit 1e-6 regularizer identity', 'B45-1.i Float64 enclosure bridge',
        'B45-2 deployed potential and central-FD gradient binding', 'B45-3 H0 and gradient-zero binding',
        'B45-4 Christoffel FD binding', 'B45-5_residual_domain_bound',
        'positive_supply relative scaling and equilibrium floor', 'actual mass PSD and eta bounds',
        'uniform_fixed_identity_scalar_source_gate', 'all_domain_continuation']
    graph['nodes'] = list(nodes.values())
    def visit(key, stack):
        assert key not in stack
        for dep in nodes[key].get('dependencies', []):
            assert dep in nodes
            visit(dep, stack | {key})
    for key in nodes:
        visit(key, set())
    backup = ROOT / 'artifacts/routeb_storage_checkpoint_20260905/state-before-revision80.json'
    assert not backup.exists()
    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    m4 = next(node for node in state.nodes.values()
              if node.name.startswith('M4.') and node.name != 'M4.correlated_momentum_closure')
    m4.metadata.setdefault('proposed_mathematical_dags', []).append(ref(graph_path))
    m4.metadata['next_mathematical_frontier'] = graph['next_frontier']
    state.event('routeb_b45_1_matrix_orthogonality_closure_checkpoint', proposed_dag=ref(graph_path),
                original_target_unchanged=True, actual_J_proved=False,
                formal_certificate_allowed=False, comparator_accepted=False,
                registry_promotions=0, broad_regression_run=False,
                cumulative_rotation_lift_open=True)
    store.save(state)
    print(json.dumps(dict(revision=state.revision, nodes=len(state.nodes),
                         graph_nodes=len(nodes), registry=len(state.registry),
                         formal_certificate_allowed=False)))


if __name__ == '__main__':
    main()
