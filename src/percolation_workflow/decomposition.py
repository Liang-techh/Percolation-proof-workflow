"""Persistent, agent-proposed reductions with checked child-to-parent cascades."""
from dataclasses import dataclass
import copy
import uuid
from .model import WorkflowState, NodeStatus
from .store import StateStore
from .comparator_gate import check_statement_comparator_gate


@dataclass(frozen=True)
class ChildGoal:
    name: str
    statement: str
    proof_sketch: str = ''


def propose_decomposition(state: WorkflowState, parent_id: str, sketch: str,
                          children: list[ChildGoal], *, agent_id: str,
                          store: StateStore | None = None,
                          comparator_gate: dict[str, dict] | None = None) -> list[str]:
    """Add child obligations transactionally while retaining earlier attempts/reductions.

    Existing theorem names are reused only on exact statement agreement. A proposal
    does not certify that the children imply the parent. After the proposal's
    reduction audit is accepted and every child is registry-verified,
    ``close_verified_reductions`` may close the parent; the final root comparator
    remains mandatory.
    """
    if not sketch.strip() or not children:
        raise ValueError('a decomposition needs a sketch and child obligations')
    if any(not child.name.strip() or not child.statement.strip() for child in children):
        raise ValueError('child names and statements must be nonempty')
    # Child creation is an admission boundary, not merely graph bookkeeping.
    # A missing coordinator-owned comparator context must therefore fail closed;
    # otherwise the optional argument silently bypasses the comparator gate.
    if comparator_gate is None:
        raise ValueError('comparator gate context is required before child admission')
    if len({child.name for child in children}) != len(children):
        raise ValueError('duplicate child goals')
    candidate = copy.deepcopy(state)
    parent = candidate.nodes[parent_id]
    if parent.status != NodeStatus.OPEN:
        raise ValueError('finish the current attempt before proposing a reduction')
    by_name = {node.name: node.id for node in candidate.nodes.values()}
    if len(by_name) != len(candidate.nodes):
        raise ValueError('ambiguous existing theorem names')
    child_ids = []
    for child in children:
        context = comparator_gate.get(child.name)
        if not isinstance(context, dict):
            raise ValueError(f'missing comparator gate context: {child.name}')
        gate = check_statement_comparator_gate(
            source_identity=context.get('source_identity'),
            source_statement=context.get('source_statement'),
            candidate_statement=child.statement,
            covered_source=context.get('covered_source'),
            target_theorem_identity=context.get('target_theorem_identity'))
        if not gate:
            raise ValueError('comparator gate rejected child: ' + '; '.join(gate.reasons))
        child_id = by_name.get(child.name)
        if child_id is not None:
            if candidate.nodes[child_id].statement != child.statement:
                raise ValueError(f'existing theorem has a different statement: {child.name}')
        else:
            child_id = candidate.add_node(child.name, child.statement,
                parent_id=parent_id, proof_sketch=child.proof_sketch,
                metadata={'statement_status': 'proposed', 'proposed_by': agent_id})
            by_name[child.name] = child_id
        if child_id not in parent.dependencies:
            parent.dependencies.append(child_id)
        child_ids.append(child_id)
    parent.proof_sketch = sketch
    proposal_id = uuid.uuid4().hex
    parent.metadata.setdefault('reduction_proposals', []).append({
        'proposal_id': proposal_id,
        'submission_id': None,
        'agent_id': agent_id,
        'sketch': sketch,
        'children': child_ids,
        'child_order': list(child_ids),
        'imports': [{'node_id': child_id, 'kind': 'theorem', 'ordinal': ordinal}
                    for ordinal, child_id in enumerate(child_ids)],
        'environment': None,
        'visibility': 'local',
        'status': 'proposed',
    })
    candidate.validate()
    for request in candidate.agent_requests.values():
        if request['node_id'] == parent_id and request['status'] == 'reported':
            request['status'] = 'decomposed'
    candidate.event('decomposition_proposed', parent_id=parent_id, children=child_ids,
                    agent_id=agent_id, sketch=sketch)
    if store:
        store.save(candidate)
        state.revision = candidate.revision
    state.nodes, state.events = candidate.nodes, candidate.events
    state.agent_requests = candidate.agent_requests
    return child_ids
