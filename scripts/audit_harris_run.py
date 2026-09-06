"""Read-only acceptance checks for the staged experiment, not the whole long-term goal."""
import json
from pathlib import Path
from percolation_workflow.store import StateStore

root = Path(__file__).resolve().parents[1]
store = StateStore(root / 'artifacts/harris_replay/state.json')
if not store.path.is_file():
    raise FileNotFoundError(store.path)
state = store.load()
state.validate()
names = {'HarrisReplay.harris', 'HarrisReplay.iterated_nonneg', 'HarrisReplay.inner_expansion'}
actual = {n.name for n in state.nodes.values()}
checks = {'expected_nodes': actual == names,
          'all_nodes_verified': all(n.status == 'verified' for n in state.nodes.values()),
          'frontier_empty': not state.frontier(),
          'registry_complete': set(state.registry) == set(state.nodes),
          'baseline_failed': any(a.agent_id == 'coordinator-baseline' and a.exit_code == 1
                                 for a in state.attempts.values()),
          'decomposition_recorded': any(e['kind'] == 'decomposition_proposed' for e in state.events),
          'full_build_passed': any(e['kind'] == 'harris_full_project_build' and e['exit_code'] == 0
                                   for e in state.events)}
acceptance = {'Your solution is okay!', 'nanoda kernel accepts the solution',
              'Lean default kernel accepts the solution'}
checks['every_receipt_has_dual_kernel_acceptance'] = len(state.registry) == 3 and all(
    acceptance <= set(entry.get('verification_receipt', {}).get('comparator_stdout', '').splitlines())
    for entry in state.registry.values())
ordered = [e['node_id'] for e in state.events if e['kind'] == 'node_verified']
parent = next(n for n in state.nodes.values() if n.name == 'HarrisReplay.harris')
checks['children_registered_before_parent'] = parent.id in ordered and all(
    child in ordered and ordered.index(child) < ordered.index(parent.id) for child in parent.dependencies)
print(json.dumps({'checks': checks, 'staged_run_passed': all(checks.values()),
                  'full_workflow_acceptance': 'not established: autonomous orchestration and recovery remain'}, indent=2))
