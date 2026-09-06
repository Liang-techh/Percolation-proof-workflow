"""Consume the completed live decomposition without resetting attempts or the target."""
import json
from pathlib import Path
from percolation_workflow.store import StateStore
from percolation_workflow.statements import index_statements
from percolation_workflow.decomposition import ChildGoal, propose_decomposition
from percolation_workflow.sketch import check_sketch

root = Path(__file__).resolve().parents[1]
project = root / 'examples/local_fkg'
store = StateStore(root / 'artifacts/local_fkg/state.json')
proposal = json.loads((project / 'decomposition.json').read_text(encoding='utf-8'))
state = store.load()
request = state.agent_requests[proposal['request_id']]
if request['status'] not in {'reported', 'decomposed'} or state.attempts[request['attempt_id']].status != 'candidate_ready':
    raise SystemExit('a recorded successful host completion is required')
if proposal['target'] != state.nodes[state.root_id].name:
    raise SystemExit('decomposition target mismatch')
records = {r.qualified_name: r.source for r in index_statements(project / 'LocalFKGObligations.lean')}
if not state.nodes[state.root_id].metadata.get('reduction_proposals'):
    propose_decomposition(state, state.root_id, proposal['parent_sketch'],
        [ChildGoal(child['theorem'], records[child['theorem']], child['mathematical_sketch'])
         for child in proposal['children']], agent_id=request['agent_id'], store=store)
state = store.load()
accepted = state.nodes[state.root_id].metadata['reduction_proposals'][-1]['status'] == 'sketch_checked'
if not accepted:
    accepted = check_sketch(store, state.root_id, project,
        challenge_module='LocalFKGChallenge', reduction_module='LocalFKGReduction',
        reduction_name=proposal['reduction_theorem'], obligation_modules=['LocalFKGObligations'])
state = store.load()
if state.agent_requests[proposal['request_id']]['status'] == 'reported':
    state.agent_requests[proposal['request_id']]['status'] = 'decomposed'
    state.event('decomposition_result_consumed', request_id=proposal['request_id'])
    store.save(state)
print('sketch_checked' if accepted else 'sketch_rejected')
raise SystemExit(0 if accepted else 1)
