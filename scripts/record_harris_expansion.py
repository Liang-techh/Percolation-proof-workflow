"""Import the completed child-agent report, explicitly marked as reported evidence."""
from pathlib import Path
from percolation_workflow.store import StateStore

root = Path(__file__).resolve().parents[1]
store = StateStore(root / 'artifacts/harris_replay/state.json')
state = store.load()
event_key = 'expansion-agent-report-v1'
if any(e.get('report_key') == event_key for e in state.events):
    raise SystemExit('Report already recorded')
node = next(n for n in state.nodes.values() if n.name == 'HarrisReplay.inner_expansion')
source = root / 'examples/harris_replay/HarrisReplay/Expansion.lean'
for status, code, excerpt in [
    ('environment_error', 1, "unknown module prefix 'ImportGraph'"),
    ('compile_error', 1, 'integral_add rewrite match failed; agent reported summary'),
    ('passed', 0, ''),
]:
    attempt = state.begin_attempt(node.id, '01a06ff4-bd23-7c52-97b9-f2042b717c40', str(source))
    state.finish_attempt(attempt, status=status, command=['lake', 'env', 'lean', str(source)],
                         stdout=excerpt, stderr='', exit_code=code)
    state.event('agent_report_imported', attempt_id=attempt,
                evidence_origin='completed child-agent report; diagnostics are excerpts',
                cwd=str(root / ('examples/harris_replay' if status == 'environment_error'
                                else 'upstream/formal-math/percolation')))
state.event('agent_report_complete', report_key=event_key)
store.save(state)
print('Recorded reported environment failure, proof repair and successful child compilation.')
