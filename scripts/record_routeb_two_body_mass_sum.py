"""Record the compiled block-(4,5) two-body mass-sum leaf."""
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
    assert state.revision == 74 and not state.registry
    side = ROOT / 'examples/routeb_two_body_mass_sum_lean'
    receipt = side / 'FINAL_RECEIPT.md'
    source = side / 'output/run-jYZomeB7/TwoBodyMassSum.lean'
    olean = side / 'output/run-jYZomeB7/TwoBodyMassSum.olean'
    log = side / 'output/run-jYZomeB7/terminal.log'
    old_graph = ROOT / 'artifacts/routeb_6dof/block45-obligations-v38.json'
    graph_path = ROOT / 'artifacts/routeb_6dof/block45-obligations-v39.json'
    for path in (receipt, source, olean, log, old_graph):
        assert path.is_file()
    assert not graph_path.exists()
    assert sha(source) == '22b681e4d7bb0672c223b08973d9e82101161fb7e9556863b50d12d0321b8ba5'
    assert sha(olean) == '79b5a1111a92c75a6da279abbe7041a7a0c9f814dd85bd91543f222a98fb8b1c'
    text = log.read_text(encoding='utf-8') + receipt.read_text(encoding='utf-8')
    for marker in ('TwoBodyMassSum_COMPILE_EXIT_CODE=0', 'VERIFY_EXIT_CODE=0',
                   'SOURCE_RESTRICTION_CHECK=PASSED', 'JULIA_FLOAT64_BINDING=OPEN',
                   'FULL_MASS_BINDING=OPEN', 'propext'):
        assert marker in text
    assert 'sorryAx' not in text
    state.event('routeb_b45_1_two_body_mass_sum_compiled', receipt=ref(receipt),
                source=ref(source), olean=ref(olean), terminal_log=ref(log),
                compile_exit=0, verify_exit=0, standard_axioms_only=True,
                block45_two_body_mass_sum=True, registry_promoted=False,
                formal_certificate_allowed=False)
    graph = json.loads(old_graph.read_text(encoding='utf-8'))
    graph.update(schema='routeb-proposed-proof-dag-v39',
                 supersedes='block45-obligations-v38.json',
                 active_strategy='six_body_lift_over_closed_block45_sum')
    nodes = {node['id']: node for node in graph['nodes']}
    nodes['B45-1_two_body_mass_sum'] = {
        'id': 'B45-1_two_body_mass_sum',
        'status': 'compiled_candidate_comparator_pending',
        'dependencies': ['B45-1_single_body_contract_instantiation'],
        'source': '../../examples/routeb_two_body_mass_sum_lean/TwoBodyMassSum.lean',
        'statement': 'Kernel-check the finite body-3 plus body-4 source/frame mass-sum equality.',
        'verification': {'receipt': str(receipt.resolve()), 'run': 'output/run-jYZomeB7',
                         'compile_exit': 0, 'verify_exit': 0,
                         'standard_axioms_only': True,
                         'source_sha256': sha(source), 'olean_sha256': sha(olean)}}
    identity = nodes['B45-1_mass_functional_identity']
    deps = list(identity.get('dependencies', []))
    if 'B45-1_two_body_mass_sum' not in deps:
        deps.append('B45-1_two_body_mass_sum')
    identity['dependencies'] = deps
    identity.setdefault('compiled_precursors', [])
    if 'B45-1_two_body_mass_sum' not in identity['compiled_precursors']:
        identity['compiled_precursors'].append('B45-1_two_body_mass_sum')
    for obligation in graph['source_binding_obligations']:
        if obligation['id'] == 'B45-1':
            subnodes = obligation.setdefault('subnodes', [])
            if 'B45-1_two_body_mass_sum' not in subnodes:
                subnodes.insert(5, 'B45-1_two_body_mass_sum')
            obligation['two_body_mass_sum'] = 'compiled_candidate_comparator_pending'
            obligation['body_mass_function_binding'] = 'open'
    graph['next_frontier'] = [
        'B45-1 lift block-(4,5) two-body sum to six body contributions',
        'B45-1 prove six-body source mass evaluator equals contract sum',
        'B45-1 body mass Fourier evaluator for all q', 'B45-1.i Float64 enclosure bridge',
        'B45-2 deployed potential and central-FD gradient binding',
        'B45-3 H0 and gradient-zero binding', 'B45-4 Christoffel FD binding',
        'B45-5_residual_domain_bound', 'positive_supply relative scaling and equilibrium floor',
        'actual mass PSD and eta bounds', 'uniform_fixed_identity_scalar_source_gate',
        'all_domain_continuation']
    graph['nodes'] = list(nodes.values())
    def visit(key, stack):
        assert key not in stack
        for dep in nodes[key].get('dependencies', []):
            assert dep in nodes
            visit(dep, stack | {key})
    for key in nodes:
        visit(key, set())
    backup = ROOT / 'artifacts/routeb_storage_checkpoint_20260905/state-before-revision74.json'
    assert not backup.exists()
    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    m4 = next(node for node in state.nodes.values()
              if node.name.startswith('M4.') and node.name != 'M4.correlated_momentum_closure')
    m4.metadata.setdefault('proposed_mathematical_dags', []).append(ref(graph_path))
    m4.metadata['next_mathematical_frontier'] = graph['next_frontier']
    state.event('routeb_b45_1_two_body_mass_sum_checkpoint', proposed_dag=ref(graph_path),
                original_target_unchanged=True, actual_J_proved=False,
                formal_certificate_allowed=False, comparator_accepted=False,
                registry_promotions=0, broad_regression_run=False,
                six_body_lift_open=True)
    store.save(state)
    print(json.dumps(dict(revision=state.revision, nodes=len(state.nodes),
                         graph_nodes=len(nodes), registry=len(state.registry),
                         formal_certificate_allowed=False)))


if __name__ == '__main__':
    main()
