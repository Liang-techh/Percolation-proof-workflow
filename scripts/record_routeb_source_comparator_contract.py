"""Attach the machine-readable source contract to the proposed Route-B DAG."""
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
    assert state.revision == 104 and not state.registry
    contract_json = ROOT / 'artifacts/routeb_6dof/source_comparator_contract_v61.json'
    contract_md = ROOT / 'artifacts/routeb_6dof/source_comparator_contract_v61.md'
    old_graph = ROOT / 'artifacts/routeb_6dof/block45-obligations-v61.json'
    graph_path = ROOT / 'artifacts/routeb_6dof/block45-obligations-v62.json'
    backup = ROOT / 'artifacts/routeb_storage_checkpoint_20260905/state-before-revision105.json'
    assert contract_json.is_file() and contract_md.is_file() and old_graph.is_file()
    assert not graph_path.exists() and not backup.exists()
    contract = json.loads(contract_json.read_text(encoding='utf-8'))
    assert contract['schema'] == 'routeb-source-comparator-contract-v1'
    assert contract['registry_eligible'] is False
    assert contract['formal_certificate_allowed'] is False
    assert contract['dimensions']['q']['scope'] == 'all six coordinates'
    assert contract['dimensions']['dq']['scope'] == 'all six velocities'
    assert contract['dimensions']['w']['scope'].startswith('one scalar')
    assert contract['numerical_semantics']['regularization_mu'] == '1/1000000'
    assert contract['numerical_semantics']['finite_difference_h'] == '1/100000'

    graph = json.loads(old_graph.read_text(encoding='utf-8'))
    nodes = {node['id']: node for node in graph['nodes']}
    node_id = 'B45-1_deployed_dh_source_comparator_contract'
    assert node_id not in nodes
    nodes[node_id] = {
        'id': node_id,
        'status': 'source_audit_open',
        'dependencies': [
            'B45-1_fin6_index_adapter',
            'B45-1_body_com_jacobian_mass_semantics',
            'B45-1_regularized_mass_adapter',
        ],
        'source': '../../artifacts/routeb_6dof/source_comparator_contract_v61.json',
        'statement': (
            'Fix the deployed dhport_lib.jl source semantics for the full six-axis '
            'q,dq,w inputs, DH/index/COM/parent-axis rules, regularization, and '
            'central finite differences; keep the Julia Float64 extensional bridge open.'
        ),
        'verification': {
            'json': ref(contract_json),
            'markdown': ref(contract_md),
            'json_sha256': sha(contract_json),
            'markdown_sha256': sha(contract_md),
            'authoritative_source_sha256': contract['provenance']['authoritative_source_sha256'],
            'superseded_dag_sha256': contract['provenance']['dag_sha256'],
            'status': 'audit_only',
            'registry_eligible': False,
            'formal_certificate_allowed': False,
        },
        'open_bridges': [
            'function-level DH/frame/COM/Jacobian extensionality',
            'Float64-to-real enclosure or exact execution semantics',
            'source finite-difference binding for C_times_dq and G',
        ],
    }
    source = nodes['source_semantics']
    source['source_comparator_contract'] = {
        'node': node_id,
        'status': 'audit_only',
        'json': ref(contract_json),
        'json_sha256': sha(contract_json),
    }
    obligation = next(item for item in graph['source_binding_obligations'] if item['id'] == 'B45-1')
    obligation.setdefault('subnodes', []).append(node_id)
    obligation['source_comparator_contract'] = 'audit_only'
    obligation['full_state_input_semantics'] = 'fixed_in_contract'
    obligation['deployed_julia_float64_binding'] = 'open'
    obligation['finite_difference_source_binding'] = 'open'
    graph['next_frontier'] = [
        'B45-1 prove the exact-real contract functions match the deployed source functions',
        'B45-1 bind Float64 mass_matrix and central finite differences with an enclosure',
    ] + [item for item in graph['next_frontier'] if item not in {
        'B45-1 bind minimal source loop to deployed mass_matrix semantics',
        'B45-1 sourceBodyMass/sourceContract exact index binding',
    }]
    graph.update(schema='routeb-proposed-proof-dag-v62', supersedes='block45-obligations-v61.json')
    graph['nodes'] = list(nodes.values())
    ids = set(nodes)
    visiting, seen = set(), set()
    def visit(key):
        if key not in ids or key in visiting:
            raise ValueError('dangling dependency or cycle')
        if key in seen:
            return
        visiting.add(key)
        for dep in nodes[key].get('dependencies', []):
            visit(dep)
        visiting.remove(key)
        seen.add(key)
    for key in ids:
        visit(key)

    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    state.event(
        'routeb_source_comparator_contract_attached',
        contract_json=ref(contract_json),
        contract_markdown=ref(contract_md),
        proposed_dag=ref(graph_path),
        contract_sha256=sha(contract_json),
        authoritative_source_sha256=contract['provenance']['authoritative_source_sha256'],
        full_q_dq_w=True,
        regularization='1/1000000',
        finite_difference_h='1/100000',
        deployed_float64_binding_open=True,
        registry_promotions=0,
        formal_certificate_allowed=False,
    )
    store.save(state)
    print({'revision': state.revision, 'graph_nodes': len(nodes),
           'registry': len(state.registry), 'formal_certificate_allowed': False})


if __name__ == '__main__':
    main()
