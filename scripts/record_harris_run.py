"""Persist observations from the coordinator's first live Harris replay run."""
from pathlib import Path
from percolation_workflow.model import WorkflowState
from percolation_workflow.store import StateStore
from percolation_workflow.statements import index_statements
from percolation_workflow.decomposition import ChildGoal, propose_decomposition

root = Path(__file__).resolve().parents[1]
project = root / 'examples/harris_replay'
store = StateStore(root / 'artifacts/harris_replay/state.json')
if store.path.exists():
    raise FileExistsError('Refusing to overwrite Harris research history')
state = WorkflowState(project='harris_replay')
target = index_statements(project / 'Challenge.lean')[0]
parent = state.add_node(target.qualified_name, target.source,
                       metadata={'statement_status': 'indexed'})
attempt = state.begin_attempt(parent, 'coordinator-baseline', str(project / 'Baseline.lean'))
state.finish_attempt(attempt, status='compile_error',
    command=['lake', 'env', 'lean', str(project / 'Baseline.lean')], exit_code=1,
    stdout='aesop: failed to prove the goal after exhaustive search.\nerror: unsolved goals\n'
           '⊢ (∫ (y : Y), φ y ∂ν) * ∫ (y : Y), ψ y ∂ν ≤ ∫ (y : Y), φ y * ψ y ∂ν', stderr='')
state.event('observation_provenance', attempt_id=attempt, exec_session=11268,
            diagnostic_is_excerpt=True, cwd=str(root / 'upstream/formal-math/percolation'))
positive = next(r for r in index_statements(project / 'HarrisReplay/Positive.lean')
                if r.name == 'iterated_nonneg')
expansion = index_statements(project / 'HarrisReplay/Expansion.lean')[0]
children = propose_decomposition(state, parent,
    'Bounded measurability gives three integrability facts. Use monotone-difference positivity '
    'and the independent inner expansion, then expand the outer integral and close the inequality.',
    [ChildGoal(positive.qualified_name, positive.source),
     ChildGoal(expansion.qualified_name, expansion.source)], agent_id='coordinator')
for child_id, agent in zip(children, ['01a06ff4-bc79-7e70-af17-ea72b91a3dc6',
                                     '01a06ff4-bd23-7c52-97b9-f2042b717c40']):
    state.event('codex_agent_dispatched', node_id=child_id, agent_id=agent,
                observation='dispatch occurred before this state import')
for code, diagnostic, cwd in [(1, "unknown module prefix 'ImportGraph'", str(project)),
                              (0, '', str(root / 'upstream/formal-math/percolation'))]:
    child_attempt = state.begin_attempt(children[0], '01a06ff4-bc79-7e70-af17-ea72b91a3dc6',
                                        str(project / 'HarrisReplay/Positive.lean'))
    state.finish_attempt(child_attempt, status='passed' if code == 0 else 'environment_error',
        command=['lake', 'env', 'lean', str(project / 'HarrisReplay/Positive.lean')],
        stdout=diagnostic, stderr='', exit_code=code)
    state.event('agent_report_imported', attempt_id=child_attempt, cwd=cwd,
                evidence_origin='completed Codex child-agent report')
store.save(state)
print(f'Saved {len(state.nodes)} nodes, {len(state.attempts)} observed attempts; registry empty.')
