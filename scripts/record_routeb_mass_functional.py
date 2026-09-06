"""Record the compiled source-independent mass-functional composition leaf."""
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
    assert state.revision == 61 and len(state.nodes) == 64 and not state.registry
    side = ROOT / 'examples/routeb_mass_functional_lean'
    receipt = side / 'FINAL_RECEIPT.md'
    source = side / 'output/run-pVaCVj2p/MassFunctional.lean'
    olean = side / 'output/run-pVaCVj2p/MassFunctional.olean'
    log = side / 'output/run-pVaCVj2p/terminal.log'
    old_graph = ROOT / 'artifacts/routeb_6dof/block45-obligations-v25.json'
    graph_path = ROOT / 'artifacts/routeb_6dof/block45-obligations-v26.json'
    for path in (receipt, source, olean, log, old_graph):
        assert path.is_file()
    assert not graph_path.exists()
    assert sha(source) == 'e9b90d46b70e5cfad1cd03a1da34b6fbc369751a791fd40a867424921e8ac63a'
    assert sha(olean) == '946cdcb566546bff92524869673abfeb627587217979995b41fddb0d1cc3ef8d'
    log_text = log.read_text(encoding='utf-8')
    receipt_text = receipt.read_text(encoding='utf-8')
    for marker in ('MassFunctional_COMPILE_EXIT_CODE=0',
                   'VERIFY_EXIT_CODE=0', 'SNAPSHOT_HASHES_UNCHANGED=true',
                   'ideal_mass_eq_fourier_of_linkwise', 'propext'):
        assert marker in log_text + receipt_text
    assert 'sorryAx' not in log_text and 'admit' not in source.read_text(encoding='utf-8').lower()

    state.event(
        'routeb_b45_1_mass_functional_composition_compiled',
        receipt=ref(receipt), source=ref(source), olean=ref(olean),
        terminal_log=ref(log), compile_exit=0, verify_exit=0,
        standard_axioms_only=True, source_independent=True,
        full_mass_lift=False, physical_source_binding=False,
        registry_promoted=False, formal_certificate_allowed=False)

    graph = json.loads(old_graph.read_text(encoding='utf-8'))
    graph.update(schema='routeb-proposed-proof-dag-v26',
                 supersedes='block45-obligations-v25.json',
                 active_strategy='compose_linkwise_mass_functional')
    nodes = {node['id']: node for node in graph['nodes']}
    nodes['B45-1_mass_functional_composition'] = {
        'id': 'B45-1_mass_functional_composition',
        'status': 'compiled_candidate_comparator_pending',
        'dependencies': [],
        'source': '../../examples/routeb_mass_functional_lean/MassFunctional.lean',
        'statement': (
            'Kernel-check that pointwise equality of six link masses, '
            'translational/rotational Jacobians, and inertia weights implies '
            'equality of the complete ideal mass functional, including the '
            'finite link sum and exact diagonal regularizer.'),
        'verification': {
            'receipt': str(receipt.resolve()), 'run': 'output/run-pVaCVj2p',
            'compile_exit': 0, 'verify_exit': 0,
            'standard_axioms_only': True,
            'source_sha256': sha(source), 'olean_sha256': sha(olean)}}
    identity = nodes['B45-1_mass_functional_identity']
    deps = list(identity.get('dependencies', []))
    if 'B45-1_mass_functional_composition' not in deps:
        deps.append('B45-1_mass_functional_composition')
    identity['dependencies'] = deps
    precursors = list(identity.get('compiled_precursors', []))
    if 'B45-1_mass_functional_composition' not in precursors:
        precursors.append('B45-1_mass_functional_composition')
    identity['compiled_precursors'] = precursors
    graph['next_frontier'] = [
        'B45-1.2 frame recursion and parent-axis lift',
        'B45-1.c body mass Fourier evaluator for all q',
        'B45-1.g comparator-backed q=0 bridge admission',
        'B45-1.i Float64 enclosure bridge',
        'B45-2 potential and gradient reconstruction',
        'B45-3 H0 and gradient-zero binding',
        'B45-4 Christoffel FD binding',
        'B45-5_residual_domain_bound',
        'positive_supply_eta_physical_projection_and_relative_bound',
        'positive_supply_two_regime_physical_assembly',
        'positive_supply_equilibrium_floor',
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
    backup = ROOT / 'artifacts/routeb_storage_checkpoint_20260905/state-before-revision61.json'
    assert not backup.exists()
    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    m4 = next(node for node in state.nodes.values()
              if node.name.startswith('M4.') and node.name != 'M4.correlated_momentum_closure')
    m4.metadata.setdefault('proposed_mathematical_dags', []).append(ref(graph_path))
    m4.metadata['next_mathematical_frontier'] = graph['next_frontier']
    state.event(
        'routeb_b45_1_mass_functional_checkpoint', proposed_dag=ref(graph_path),
        original_target_unchanged=True, actual_J_proved=False,
        formal_certificate_allowed=False, comparator_accepted=False,
        registry_promotions=0, broad_regression_run=False,
        linkwise_source_adapter_open=True)
    store.save(state)
    print(json.dumps(dict(revision=state.revision, nodes=len(state.nodes),
                         graph_nodes=len(nodes), registry=len(state.registry),
                         formal_certificate_allowed=False)))


if __name__ == '__main__':
    main()
