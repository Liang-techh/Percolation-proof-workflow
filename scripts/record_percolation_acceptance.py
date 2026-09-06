"""Attach completed upstream acceptance without inventing per-lemma verification receipts."""
import hashlib
import json
from pathlib import Path
from percolation_workflow.store import StateStore

root = Path(__file__).resolve().parents[1]
directory = root / 'artifacts/percolation'
receipt = json.loads((directory / 'linux_acceptance_20260905.json').read_text())
log = (directory / 'linux_comparator_20260905.log').read_bytes()
required = {'nanoda kernel accepts the solution', 'Lean default kernel accepts the solution',
            'Your solution is okay!', 'PASS comparator.json'}
if not required <= set(log.decode().splitlines()):
    raise ValueError('missing final acceptance evidence')
stage = next(s for s in receipt['stages'] if s['stage'] == 'comparator')
if stage['exit_code'] != 0 or stage['status'] != 'passed':
    raise ValueError('comparator stage did not pass')
store = StateStore(directory / 'workflow_state.json')
state = store.load()
digest = hashlib.sha256(log).hexdigest()
if not any(e.get('acceptance_log_sha256') == digest for e in state.events):
    state.event('upstream_submission_accepted', source_commit=receipt['source_commit'],
                acceptance_log_sha256=digest, receipt='linux_acceptance_20260905.json',
                log='linux_comparator_20260905.log',
                scope='upstream Challenge/Solution targets; not autonomous proof discovery')
    store.save(state)
print('Upstream dual-kernel and statement acceptance recorded; per-lemma registry unchanged.')
