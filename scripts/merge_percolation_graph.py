from pathlib import Path
import json
from percolation_workflow.graph import merge_reachable_graph
from percolation_workflow.store import StateStore

root = Path(__file__).resolve().parents[1]
store = StateStore(root / 'artifacts/percolation/workflow_state.json')
if not store.path.exists():
    raise FileNotFoundError(store.path)
state = store.load()
ids = merge_reachable_graph(state, root / 'artifacts/percolation/decl_graph.jsonl',
    ['BondPercolation.percolation_continuity', 'BondPercolation.percolation_continuity_Z3'])
store.save(state)
print(json.dumps({'imported_theorems': len(ids), 'nodes': len(state.nodes),
    'dependency_edges': sum(len(n.dependencies) for n in state.nodes.values()),
    'open_leaves': len(state.frontier()), 'registry_entries': len(state.registry)}))
