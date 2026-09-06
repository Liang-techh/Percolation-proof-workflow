"""Persist the trusted new target before any live solver dispatch."""
from pathlib import Path
import hashlib
import json
from percolation_workflow.model import WorkflowState
from percolation_workflow.store import StateStore
from percolation_workflow.statements import index_statements

root = Path(__file__).resolve().parents[1]
project = root / 'examples/local_fkg'
store = StateStore(root / 'artifacts/local_fkg/state.json')
if store.path.exists():
    raise SystemExit('existing research state retained; use CLI to resume')
record, = index_statements(project / 'LocalFKGChallenge.lean')
state = WorkflowState(project='local-fkg-live')
state.add_node(record.qualified_name, record.source, metadata={
    'statement_status': 'indexed', 'challenge_module': 'LocalFKGChallenge',
    'challenge_source_sha256': hashlib.sha256((project / 'LocalFKGChallenge.lean').read_bytes()).hexdigest(),
    'contract': json.loads((project / 'research-contract.json').read_text()),
    'environment_status': 'dependency preparation in progress; statement not yet compiled'})
state.event('trusted_target_intake', source_file=record.source_file,
            provenance='upstream statement only; original target proof not read')
store.save(state)
print(state.root_id)
