"""Record the homogeneous frame rotation projection bridge."""
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
    assert state.revision == 82 and not state.registry
    side = ROOT / 'examples/routeb_homogeneous_rotation_projection_lean'
    receipt = side / 'FINAL_RECEIPT.md'
    source = side / 'output/run-O33agpqU/HomogeneousRotationProjection.lean'
    olean = side / 'output/run-O33agpqU/HomogeneousRotationProjection.olean'
    log = side / 'output/run-O33agpqU/terminal.log'
    old_graph = ROOT / 'artifacts/routeb_6dof/block45-obligations-v46.json'
    graph_path = ROOT / 'artifacts/routeb_6dof/block45-obligations-v47.json'
    for path in (receipt, source, olean, log, old_graph):
        assert path.is_file()
    assert not graph_path.exists()
    assert sha(source) == 'a3a6ead7d060729cbcb10ea89122c02fde4c6986474792e369708ff367e8fa8b'
    assert sha(olean) == 'df79c634d37249485ed95efaef8d90b71a8119a5dd401f97efaabe00ffcf1b32'
    text = log.read_text(encoding='utf-8') + receipt.read_text(encoding='utf-8')
    for marker in ('HomogeneousRotationProjection_COMPILE_EXIT_CODE=0', 'VERIFY_EXIT_CODE=0',
                   'SOURCE_RESTRICTION_CHECK=PASSED', 'JULIA_FLOAT64_BINDING=OPEN',
                   'FULL_MASS_BINDING=OPEN', 'propext'):
        assert marker in text
    assert 'sorryAx' not in text
    state.event('routeb_b45_1_homogeneous_rotation_projection_compiled', receipt=ref(receipt),
                source=ref(source), olean=ref(olean), terminal_log=ref(log),
                compile_exit=0, verify_exit=0, standard_axioms_only=True,
                homogeneous_rotation_projection=True, registry_promoted=False,
                formal_certificate_allowed=False)
    graph = json.loads(old_graph.read_text(encoding='utf-8'))
    graph.update(schema='routeb-proposed-proof-dag-v47',
                 supersedes='block45-obligations-v46.json',
                 active_strategy='homogeneous_frame_prefix_to_source_mass')
    nodes = {node['id']: node for node in graph['nodes']}
    nodes['B45-1_homogeneous_rotation_projection'] = {
        'id': 'B45-1_homogeneous_rotation_projection',
        'status': 'compiled_candidate_comparator_pending',
        'dependencies': [],
        'source': '../../examples/routeb_homogeneous_rotation_projection_lean/HomogeneousRotationProjection.lean',
        'statement': 'Kernel-check top-left rotation projection of products of homogeneous 4x4 frames.',
        'verification': {'receipt': str(receipt.resolve()), 'run': 'output/run-O33agpqU',
                         'compile_exit': 0, 'verify_exit': 0,
                         'standard_axioms_only': True,
                         'source_sha256': sha(source), 'olean_sha256': sha(olean)}}
    identity = nodes['B45-1_mass_functional_identity']
    deps = list(identity.get('dependencies', []))
    if 'B45-1_homogeneous_rotation_projection' not in deps:
        deps.append('B45-1_homogeneous_rotation_projection')
    identity['dependencies'] = deps
    identity.setdefault('compiled_precursors', [])
    if 'B45-1_homogeneous_rotation_projection' not in identity['compiled_precursors']:
        identity['compiled_precursors'].append('B45-1_homogeneous_rotation_projection')
    for obligation in graph['source_binding_obligations']:
        if obligation['id'] == 'B45-1':
            subnodes = obligation.setdefault('subnodes', [])
            if 'B45-1_homogeneous_rotation_projection' not in subnodes:
                subnodes.insert(13, 'B45-1_homogeneous_rotation_projection')
            obligation['homogeneous_rotation_projection'] = 'compiled_candidate_comparator_pending'
            obligation['rotated_inertia_binding'] = 'open'
    graph['next_frontier'] = [
        'B45-1 connect Route-B 4x4 frame prefix to cumulative 3x3 rotation prefix',
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
    backup = ROOT / 'artifacts/routeb_storage_checkpoint_20260905/state-before-revision82.json'
    assert not backup.exists()
    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    m4 = next(node for node in state.nodes.values()
              if node.name.startswith('M4.') and node.name != 'M4.correlated_momentum_closure')
    m4.metadata.setdefault('proposed_mathematical_dags', []).append(ref(graph_path))
    m4.metadata['next_mathematical_frontier'] = graph['next_frontier']
    state.event('routeb_b45_1_homogeneous_rotation_projection_checkpoint', proposed_dag=ref(graph_path),
                original_target_unchanged=True, actual_J_proved=False,
                formal_certificate_allowed=False, comparator_accepted=False,
                registry_promotions=0, broad_regression_run=False,
                source_frame_prefix_projection_open=True)
    store.save(state)
    print(json.dumps(dict(revision=state.revision, nodes=len(state.nodes),
                         graph_nodes=len(nodes), registry=len(state.registry),
                         formal_certificate_allowed=False)))


if __name__ == '__main__':
    main()
