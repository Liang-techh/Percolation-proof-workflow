"""Replay the existing Harris reduction with children as assumptions, not new discovery."""
from pathlib import Path
import sys
from percolation_workflow.model import WorkflowState
from percolation_workflow.store import StateStore
from percolation_workflow.statements import index_statements
from percolation_workflow.decomposition import ChildGoal, propose_decomposition
from percolation_workflow.sketch import check_sketch

ROOT = Path(__file__).resolve().parents[1]
project = ROOT / 'examples/harris_sketch'
store = StateStore(ROOT / 'artifacts/harris_sketch/state.json')
records = {r.qualified_name: r.source for r in index_statements(project / 'Challenge.lean')}
if store.path.exists():
    state = store.load()
    parent = state.root_id
    if state.project != 'harris-sketch-replay' or state.nodes[parent].statement != records['HarrisReplay.harris']:
        raise SystemExit('Existing state is not this experiment')
else:
    state = WorkflowState(project='harris-sketch-replay')
    parent = state.add_node('HarrisReplay.harris', records['HarrisReplay.harris'])
    propose_decomposition(state, parent, 'Expand the double integral; monotonicity makes it nonnegative.',
        [ChildGoal(n, records[n]) for n in ('HarrisReplay.iterated_nonneg', 'HarrisReplay.inner_expansion')],
        agent_id='coordinator-replay-of-existing-decomposition', store=store)
# The parent declaration was read from the trusted Challenge above; retain that
# binding explicitly so the frontier scheduler can later close the parent.
state.nodes[parent].metadata['statement_status'] = 'indexed'
store.save(state)
accepted = check_sketch(store, parent, project, challenge_module='Challenge',
                        reduction_module='Reduction', reduction_name='harris_reduction')
print('sketch_checked' if accepted else 'sketch_rejected')
sys.exit(0 if accepted else 1)
