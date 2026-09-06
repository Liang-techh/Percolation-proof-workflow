"""Persist the compiled B45-5 full-state/descriptor repair interface."""
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
    assert state.revision == 110 and not state.registry
    base = ROOT / 'artifacts/routeb_b45_5_minimal_interface_20260906'
    source = base / 'B45MinimalInterface.lean'
    olean = base / 'output/run-oy6FPaEW/B45MinimalInterface.olean'
    audit = base / 'B45-5-minimal-interface-audit.md'
    old_graph = ROOT / 'artifacts/routeb_6dof/block45-obligations-v66.json'
    graph_path = ROOT / 'artifacts/routeb_6dof/block45-obligations-v67.json'
    backup = ROOT / 'artifacts/routeb_storage_checkpoint_20260905/state-before-revision111.json'
    for path in (source, olean, audit, old_graph):
        assert path.is_file()
    assert not graph_path.exists() and not backup.exists()
    log = (base / 'output/run-oy6FPaEW/terminal.log').read_text(encoding='utf-8')
    assert 'B45MinimalInterface_COMPILE_EXIT_CODE=0' in log
    assert 'VERIFY_EXIT_CODE=0' in log
    assert 'SOURCE_RESTRICTION_CHECK=PASSED' in log

    graph = json.loads(old_graph.read_text(encoding='utf-8'))
    nodes = {node['id']: node for node in graph['nodes']}
    node_id = 'B45-5_minimal_fullstate_descriptor_interface'
    assert node_id not in nodes
    nodes[node_id] = {
        'id': node_id,
        'status': 'compiled_candidate_comparator_pending',
        'dependencies': ['B45-5_residual_decomposition_exact_lean',
                         'B45-5_descriptor_terms_adapter'],
        'source': '../../artifacts/routeb_b45_5_minimal_interface_20260906/B45MinimalInterface.lean',
        'statement': (
            'Kernel-check the minimum repair interface after the PMI projection '
            'obstruction: full-state enclosures, one explicit FD remainder budget, '
            'and descriptor/Schur equations with a bounded remote term.'
        ),
        'verification': {
            'audit': ref(audit),
            'source': ref(source),
            'olean': ref(olean),
            'source_sha256': sha(source),
            'olean_sha256': sha(olean),
            'compile_exit': 0,
            'verify_exit': 0,
            'standard_axioms_only': True,
            'source_restriction': 'passed',
            'registry_promoted': False,
        },
        'closed_subclaims': [
            'exact M_BD a_D unbounded projection family',
            'nonzero remote-velocity quadratic obstruction shape',
            'full-state bound fields are explicit premises',
            'FD truncation/rounding/solve error is one remainder budget',
            'descriptor block equations and bounded Schur remote term',
        ],
        'open_bridges': [
            'bind actual source C/G/FD outputs',
            'prove strict Schur bound from full DH mass and dynamics',
            'connect first-exit and terminal-transfer arguments',
        ],
    }
    gate = nodes['B45-5_model_replacement_gate']
    gate.setdefault('compiled_precursors', []).append(node_id)
    gate['minimum_repair_interface'] = node_id
    bound = nodes['B45-5_residual_domain_bound']
    bound['repair_interface'] = node_id
    bound['current_domain_status'] = 'obstructed_without_interface'
    graph['next_frontier'] = [
        'B45-5 instantiate DescriptorSchurInterface with actual full DH C/G/FD',
        'B45-5 prove strict Schur remote bound over covered domain',
        'B45-5 connect descriptor interface to first-exit and terminal transfer',
    ] + [x for x in graph['next_frontier'] if 'descriptor' not in x.lower() or 'schur' not in x.lower()]
    graph.update(schema='routeb-proposed-proof-dag-v67', supersedes='block45-obligations-v66.json')
    graph['nodes'] = list(nodes.values())
    ids = set(nodes); seen = set(); visiting = set()
    def visit(key):
        if key not in ids or key in visiting:
            raise ValueError('dangling dependency or cycle')
        if key in seen:
            return
        visiting.add(key)
        for dep in nodes[key].get('dependencies', []):
            visit(dep)
        visiting.remove(key); seen.add(key)
    for key in ids:
        visit(key)

    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    state.event(
        'routeb_b45_5_minimal_interface_recorded',
        source=ref(source), olean=ref(olean), audit=ref(audit),
        source_sha256=sha(source), olean_sha256=sha(olean),
        compile_exit=0, verify_exit=0, standard_axioms_only=True,
        current_pmi_domain_obstruction_preserved=True,
        descriptor_schur_minimum_route=True,
        actual_source_binding_open=True,
        registry_promotions=0, formal_certificate_allowed=False,
        proposed_dag=ref(graph_path), broad_regression_run=False,
    )
    store.save(state)
    print({'revision': state.revision, 'graph_nodes': len(nodes),
           'registry': len(state.registry), 'formal_certificate_allowed': False})


if __name__ == '__main__':
    main()
