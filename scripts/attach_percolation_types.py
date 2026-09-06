from pathlib import Path
import json
from percolation_workflow.graph import attach_elaborated_types
from percolation_workflow.store import StateStore

root = Path(__file__).resolve().parents[1]
store = StateStore(root / 'artifacts/percolation/workflow_state.json')
if not store.path.exists():
    raise FileNotFoundError(store.path)
state = store.load()
attached = attach_elaborated_types(state, root / 'artifacts/percolation/elaborated_types.jsonl')
store.save(state)
print(json.dumps({'attached': attached,
    'unexpected_axioms': [n.name for n in state.nodes.values() if n.metadata.get('unexpected_axioms')],
    'leaves_with_types': sum('elaborated_type' in n.metadata for n in state.frontier()),
    'registry_entries': len(state.registry)}))
