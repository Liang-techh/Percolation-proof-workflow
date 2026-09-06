"""Check the immutable target in the already-built pinned upstream environment."""
from pathlib import Path
import hashlib
from percolation_workflow.lean import run_lean
from percolation_workflow.store import StateStore

root = Path(__file__).resolve().parents[1]
source = root / 'examples/local_fkg/LocalFKGChallenge.lean'
store = StateStore(root / 'artifacts/local_fkg/state.json')
before = hashlib.sha256(source.read_bytes()).hexdigest()
state = store.load()
if before != state.nodes[state.root_id].metadata['challenge_source_sha256']:
    raise SystemExit('trusted target source changed')
result = run_lean(root / 'upstream/formal-math/percolation', ['lake', 'env', 'lean', str(source)])
state = store.load()
unchanged = before == hashlib.sha256(source.read_bytes()).hexdigest()
state.event('target_elaboration_checked', command=result.command, stdout=result.stdout,
    stderr=result.stderr, exit_code=result.exit_code, source_unchanged=unchanged,
    environment=str(root / 'upstream/formal-math/percolation'),
    scope='target placeholder elaboration, not a proof or registry admission')
state.nodes[state.root_id].metadata['environment_status'] = (
    'target elaborated in pinned upstream environment' if result.ok and unchanged else 'target check failed')
store.save(state)
print(result.stdout)
print(result.stderr)
raise SystemExit(0 if result.ok and unchanged else 1)
