"""Persist the failed source-body-mass bridge attempt as an open frontier."""
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
    assert state.revision == 99 and not state.registry
    source = ROOT / 'examples/routeb_agent_source_mass_binding_lean/AgentSourceMassBinding.lean'
    log = ROOT / 'examples/routeb_agent_source_mass_binding_lean/output/run-v48cuX6f/terminal.log'
    old_graph = ROOT / 'artifacts/routeb_6dof/block45-obligations-v59.json'
    graph_path = ROOT / 'artifacts/routeb_6dof/block45-obligations-v60.json'
    backup = ROOT / 'artifacts/routeb_storage_checkpoint_20260905/state-before-revision100.json'
    for path in (source, log, old_graph):
        assert path.is_file()
    assert not graph_path.exists() and not backup.exists()
    source_digest = sha(source)
    state.event('routeb_b45_1_source_body_mass_bridge_failed',
                source=ref(source), terminal_log=ref(log), source_sha256=source_digest,
                status='stalled_without_olean', compile_exit=None,
                olean_generated=False,
                blocker='missing sourceBodyMass/sourceContract function extensionality',
                registry_promotions=0, formal_certificate_allowed=False)
    graph = json.loads(old_graph.read_text(encoding='utf-8'))
    graph.update(schema='routeb-proposed-proof-dag-v60',
                 supersedes='block45-obligations-v59.json',
                 active_strategy='contract_mass_to_regularized_source_mass')
    nodes = {node['id']: node for node in graph['nodes']}
    node_id = 'B45-1_source_body_mass_extensional_bridge'
    nodes[node_id] = {
        'id': node_id,
        'status': 'open',
        'dependencies': ['B45-1_source_contract_adapter', 'B45-1_source_mass_table_exact'],
        'source': '../../examples/routeb_agent_source_mass_binding_lean/AgentSourceMassBinding.lean',
        'statement': ('Prove the function-level extensional equality between deployed '
                      'sourceBodyMass(q,i,j) and the Lean sourceContract mass/inertia '
                      'sum, including exact body indices and all six link entries.'),
        'attempt_history': [{
            'source_sha256': source_digest,
            'terminal_log': str(log.resolve()),
            'status': 'stalled_without_olean',
            'compile_exit': None,
            'olean_generated': False,
            'repair_attempts': 0}],
        'verification': {
            'source_comparator': 'open',
            'lean_kernel_receipt': 'missing',
            'deployed_source_extensionality': 'open'}}
    parent = nodes['B45-1_mass_functional_identity']
    if node_id not in parent.setdefault('dependencies', []):
        parent['dependencies'].append(node_id)
    if node_id not in parent.setdefault('compiled_precursors', []):
        parent['compiled_precursors'].append(node_id)
    for obligation in graph['source_binding_obligations']:
        if obligation['id'] == 'B45-1':
            subnodes = obligation.setdefault('subnodes', [])
            if node_id not in subnodes:
                subnodes.insert(24, node_id)
            obligation['source_body_mass_extensional_bridge'] = 'open_after_stalled_attempt'
    graph['next_frontier'] = [
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
    state.event('routeb_b45_1_source_body_mass_blocker_checkpoint',
                proposed_dag=ref(graph_path), original_target_unchanged=True,
                source_body_mass_extensionality_open=True,
                formal_certificate_allowed=False, registry_promotions=0,
                broad_regression_run=False)
    store.save(state)
    print({'revision': state.revision, 'graph_nodes': len(nodes),
           'registry': len(state.registry), 'formal_certificate_allowed': False})


if __name__ == '__main__':
    main()
