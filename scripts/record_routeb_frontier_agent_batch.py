"""Persist the independently verified frontier results without promotion."""
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
    assert state.revision == 105 and not state.registry
    old_graph = ROOT / 'artifacts/routeb_6dof/block45-obligations-v62.json'
    graph_path = ROOT / 'artifacts/routeb_6dof/block45-obligations-v63.json'
    backup = ROOT / 'artifacts/routeb_storage_checkpoint_20260905/state-before-revision106.json'
    positive_source = ROOT / 'examples/routeb_positive_supply_frontier_lean/Frontier.lean'
    positive_olean = ROOT / 'examples/routeb_positive_supply_frontier_lean/output/run-1dUPvw7e/Frontier.olean'
    positive_receipt = ROOT / 'examples/routeb_positive_supply_frontier_lean/FINAL_RECEIPT.md'
    residual_audit = ROOT / 'artifacts/routeb_6dof/B45-5-pmi-domain-frontier-audit-20260906.md'
    fourier_source = ROOT / 'examples/routeb_b45_source_mass_fourier_bridge_lean/SourceMassFourierBridge.lean'
    fourier_readme = ROOT / 'examples/routeb_b45_source_mass_fourier_bridge_lean/README.md'
    for path in (old_graph, positive_source, positive_olean, positive_receipt,
                 residual_audit, fourier_source, fourier_readme):
        assert path.is_file()
    assert not graph_path.exists() and not backup.exists()

    graph = json.loads(old_graph.read_text(encoding='utf-8'))
    nodes = {node['id']: node for node in graph['nodes']}

    positive_id = 'positive_supply_two_regime_frontier_algebraic'
    assert positive_id not in nodes
    nodes[positive_id] = {
        'id': positive_id,
        'status': 'compiled_candidate_comparator_pending',
        'dependencies': ['positive_supply_gate', 'positive_supply_relative_eta_kernel_leaf'],
        'source': '../../examples/routeb_positive_supply_frontier_lean/Frontier.lean',
        'statement': (
            'Kernel-check the two-regime terminal denominator: eta=0 is positive '
            'for rho>0, relative eta with kappa<A+D is positive, and the threshold '
            'kappa>=A+D has an exact nonpositive witness; equilibrium floor is budgeted '
            'without dividing at rho=0.'
        ),
        'verification': {
            'receipt': ref(positive_receipt),
            'run': 'output/run-1dUPvw7e',
            'compile_exit': 0,
            'verify_exit': 0,
            'standard_axioms_only': True,
            'source_sha256': sha(positive_source),
            'olean_sha256': sha(positive_olean),
            'source_comparator': 'open',
            'physical_eta_binding': 'open',
            'registry_promoted': False,
        },
        'open_bridges': [
            'bind eta to the physical projected source defect',
            'prove eta(0)=0 or state-relative scaling',
            'close direct gate and equilibrium floor over the admitted source domain',
        ],
    }
    direct_gate = nodes['positive_supply_two_regime_direct_gate']
    direct_gate.setdefault('compiled_precursors', []).append(positive_id)
    frontier = graph['positive_supply_frontier']
    frontier['two_regime_algebraic_leaf'] = positive_id
    frontier['status'] = 'open_two_regime_eta_frontier'
    frontier['physical_binding'] = 'open'

    residual_id = 'B45-5_pmi_domain_feasibility_audit'
    assert residual_id not in nodes
    nodes[residual_id] = {
        'id': residual_id,
        'status': 'source_audit_open',
        'dependencies': ['B45-5_residual_domain_bound'],
        'source': '../../artifacts/routeb_6dof/B45-5-pmi-domain-frontier-audit-20260906.md',
        'statement': (
            'Audit whether the current PMI block domain can uniformly bound '
            'rho_remote=M_BD a_D and the full C(q,dq)dq/G residual.'
        ),
        'verification': {
            'report': ref(residual_audit),
            'report_sha256': sha(residual_audit),
            'status': 'obstructed_current_domain',
            'registry_eligible': False,
            'formal_certificate_allowed': False,
        },
        'counterexample': {
            'fixed_block_state': 'q4=q5=dq4=dq5=t=w=0',
            'remote_acceleration_family': 'a_D=lambda*e1',
            'zero_configuration_cross_block': '(7/60,-21/80000)',
            'conclusion': 'norm(M_BD*a_D) is unbounded as lambda tends to infinity',
        },
        'minimal_repairs': [
            'full q,dq,input,acceleration enclosures',
            'descriptor/Schur equation M(q)a=r with explicit M_BD a_D bound',
        ],
    }
    residual_bound = nodes['B45-5_residual_domain_bound']
    residual_bound['current_domain_status'] = 'refuted_by_unbounded_remote_acceleration_family'
    residual_bound['repair_node'] = residual_id

    fourier_id = 'B45-1_source_mass_fourier_aggregation_seam'
    assert fourier_id not in nodes
    nodes[fourier_id] = {
        'id': fourier_id,
        'status': 'open_unverified_candidate',
        'dependencies': ['B45-1_source_mass_table_exact', 'B45-1_regularizer_kernel_leaf'],
        'source': '../../examples/routeb_b45_source_mass_fourier_bridge_lean/SourceMassFourierBridge.lean',
        'statement': (
            'Abstract exact-real aggregation seam: a per-body source/Fourier '
            'comparator implies the full six-body regularized mass identity.'
        ),
        'candidate_evidence': {
            'source_sha256': sha(fourier_source),
            'readme_sha256': sha(fourier_readme),
            'compiled_receipt': False,
            'olean_snapshot': False,
        },
        'open_bridges': [
            'missing pinned compile receipt/olean snapshot',
            'per-body DH/Jacobian/Fourier comparator premise',
            'full 610-row aggregate CSV binding',
            'Julia Float64 to exact-real bridge',
        ],
        'semantic_warning': '17-row table is potential Fourier data, not a mass-table slice',
    }
    mass_identity = nodes['B45-1_mass_functional_identity']
    mass_identity.setdefault('open_precursors', []).append(fourier_id)

    graph['next_frontier'] = [
        'B45-1 sourceBodyMass function-level DH/COM/Jacobian extensional bridge',
        'B45-1 obtain a pinned receipt for the abstract Fourier aggregation seam',
        'B45-1 prove per-body or aggregate 610-row mass comparator',
        'B45-5 replace current PMI domain or add full descriptor/Schur acceleration bounds',
        'positive_supply bind eta(0)=0 or state-relative scaling to physical source',
    ] + [x for x in graph['next_frontier'] if x not in {
        'B45-1 bind minimal source loop to deployed mass_matrix semantics',
        'B45-1 sourceBodyMass/sourceContract exact index binding',
    }]
    graph.update(schema='routeb-proposed-proof-dag-v63', supersedes='block45-obligations-v62.json')
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
        'routeb_frontier_agent_batch_recorded',
        positive_supply_leaf={
            'node': positive_id,
            'receipt': ref(positive_receipt),
            'source_sha256': sha(positive_source),
            'olean_sha256': sha(positive_olean),
            'compile_exit': 0,
            'verify_exit': 0,
            'physical_binding_open': True,
        },
        residual_domain_audit={
            'node': residual_id,
            'report': ref(residual_audit),
            'report_sha256': sha(residual_audit),
            'current_domain_obstructed': True,
        },
        fourier_aggregation_candidate={
            'node': fourier_id,
            'source': ref(fourier_source),
            'source_sha256': sha(fourier_source),
            'compiled_receipt_present': False,
        },
        proposed_dag=ref(graph_path),
        registry_promotions=0,
        formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print({'revision': state.revision, 'graph_nodes': len(nodes),
           'registry': len(state.registry), 'formal_certificate_allowed': False})


if __name__ == '__main__':
    main()
