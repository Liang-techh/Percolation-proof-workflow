"""Host-facing phase selection for the persistent research loop.

Uses Codex's existing agent/process tools; does not implement an agent runtime.
Actions are instructions to the single trusted coordinator, not success claims.
"""
from .store import StateStore
from .registry import audit_registry
from .agent_bridge import lease_expired
from .external import EXTERNAL_DOMAIN, external_evidence_staleness, external_diagnostic_is_current
from .model import NodeStatus, status_is_closed


def next_actions(store: StateStore) -> list[dict]:
    if not store.path.is_file():
        raise ValueError('existing research state required')
    state = store.load()
    state.validate()
    forbidden_external = [n for n in state.nodes.values() if n.status == NodeStatus.VERIFIED and
                          n.metadata.get('verification_domain') == EXTERNAL_DOMAIN]
    if forbidden_external:
        return [{'kind': 'revalidate_external_evidence', 'node_id': n.id, 'node_name': n.name,
                 'changed_artifacts': ['external_registry_forbidden'], 'registry_eligible': False}
                for n in forbidden_external]
    if {n.id for n in state.nodes.values() if n.status == 'verified'} != set(state.registry):
        return [{'kind': 'revalidate_registry', 'reason': 'node/registry mismatch'}]
    freshness = audit_registry(state)
    if any(item['status'] != 'current' for item in freshness.values()):
        return [{'kind': 'revalidate_registry', 'evidence': freshness}]
    stale_external = []
    for node in state.nodes.values():
        if node.status == NodeStatus.EVIDENCE_COMPLETE and node.metadata.get('verification_domain') == EXTERNAL_DOMAIN:
            stale = external_evidence_staleness(node)
            if stale:
                stale_external.append({'kind': 'revalidate_external_evidence',
                                       'node_id': node.id, 'node_name': node.name,
                                       'changed_artifacts': stale, 'registry_eligible': False})
    if stale_external:
        # Do not dispatch downstream work alongside a known stale premise.
        return stale_external
    actions = []
    available_frontier = state.frontier()
    primary_external_frontier = any(
        node.metadata.get('verification_domain') == EXTERNAL_DOMAIN and
        not node.metadata.get('conditional', False)
        for node in available_frontier)
    covered = set()
    for request in state.agent_requests.values():
        phase = None
        if request['status'] == 'bound' and lease_expired(request):
            phase = 'reclaim_expired_agent'
        else:
            phase = {'awaiting_dispatch': 'dispatch_agent', 'bound': 'observe_agent',
                     'checking': 'collect_compile'}.get(request['status'])
        if request['status'] == 'reported':
            node = state.nodes[request['node_id']]
            if node.attempts and node.attempts[-1] == request['attempt_id'] and (
                    state.attempts[request['attempt_id']].status == 'candidate_ready'):
                phase = 'compile_candidate'
        if phase:
            covered.add(request['node_id'])
            actions.append({'kind': phase, 'request_id': request['request_id'],
                            'node_id': request['node_id'], 'agent_id': request.get('agent_id')})
    for node in state.nodes.values():
        if node.status == NodeStatus.EVIDENCE_COMPLETE and node.metadata.get(
                'verification_domain') == EXTERNAL_DOMAIN:
            continue
        if node.id in covered or status_is_closed(node.status):
            continue
        if node.metadata.get('repair_exhausted'):
            actions.append({'kind': 'repair_exhausted', 'node_id': node.id,
                            'round': node.metadata.get('repair_exhausted_round'),
                            'max_rounds': node.metadata.get('repair_max_rounds')})
            continue
        if node.status == 'in_progress':
            actions.append({'kind': 'inspect_active_attempt', 'node_id': node.id,
                            'attempt_id': node.attempts[-1]})
            continue
        if node.metadata.get('verification_domain') == EXTERNAL_DOMAIN:
            if node not in available_frontier:
                continue
            if node.metadata.get('conditional', False) and primary_external_frontier:
                # P7 is a fallback route.  Keep it in the DAG, but do not
                # compete with the preferred finite-dimensional frontier.
                continue
            latest = state.attempts[node.attempts[-1]] if node.attempts else None
            if (external_diagnostic_is_current(node) and
                    node.metadata.get('closure_scope', 'mathematical') not in {'engineering', 'audit'}):
                kind = 'decompose_external_obligation'
            elif latest is not None:
                kind = 'repair_external_gate'
            else:
                kind = 'run_external_gate'
            actions.append({
                'kind': kind,
                'node_id': node.id,
                'node_name': node.name,
                'target_root': node.metadata.get('target_root'),
                'command': node.metadata.get('recommended_command', []),
                'evidence_level': node.metadata.get('evidence_level'),
                'claim_status': node.metadata.get('claim_status'),
                'registry_eligible': False,
                'conditional': node.metadata.get('conditional', False),
            })
            continue
        proposals = node.metadata.get('reduction_proposals', [])
        if proposals and proposals[-1]['status'] == 'proposed':
            actions.append({'kind': 'check_sketch', 'node_id': node.id})
            continue
        if node not in state.frontier():
            continue
        if node.metadata.get('statement_status') != 'indexed':
            if not node.metadata.get('proposed_by'):
                actions.append({'kind': 'formalize_target', 'node_id': node.id})
            continue
        if node.metadata.get('proposed_by') and not any(
            p.get('status') == 'sketch_checked' and node.id in p['children']
            for parent in state.nodes.values() for p in parent.metadata.get('reduction_proposals', [])):
            continue
        latest = state.attempts[node.attempts[-1]] if node.attempts else None
        repair_statuses = {'compile_error', 'verification_error', 'provenance_rejected',
                           'verification_rejected', 'agent_error', 'agent_timeout'}
        repair_of = latest if latest and latest.status in repair_statuses else None
        accepted_reduction = next((proposal for proposal in reversed(proposals)
                                   if proposal.get('status') in {'sketch_checked', 'sketch_accepted'}
                                   and proposal.get('reduction_status') == 'accepted'), None)
        work_kind = ('repair_parent_assembly' if accepted_reduction else 'repair') if repair_of else (
            'parent_assembly' if accepted_reduction else 'direct_proof')
        actions.append({'kind': 'verify_candidate' if latest and latest.status == 'compiled'
                        else 'prepare_agent', 'node_id': node.id,
                        'closability': state.frontier_closability(node.id),
                        'work_kind': work_kind,
                        'repair_of_attempt_id': repair_of.id if repair_of else None,
                        'proposal_id': accepted_reduction.get('proposal_id') if accepted_reduction else None})
    # External evidence closure is deliberately not a final theorem signal;
    # only the Lean/comparator registry can trigger final_project_check.
    if state.nodes and all(node.status == 'verified' for node in state.nodes.values()):
        actions.append({'kind': 'final_project_check'})
    return actions
