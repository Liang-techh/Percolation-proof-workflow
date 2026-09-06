"""Persist the append-only attempt-history hardening checkpoint."""
import hashlib
import shutil

from record_routeb_port_progress import ROOT, ref
from percolation_workflow.store import StateStore


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    store = StateStore(ROOT / 'artifacts/routeb_6dof/state.json')
    state = store.load()
    assert state.revision == 97 and not state.registry
    model = ROOT / 'src/percolation_workflow/model.py'
    test = ROOT / 'tests/test_attempt_history_replay.py'
    backup = ROOT / 'artifacts/routeb_storage_checkpoint_20260905/state-before-revision98.json'
    assert model.is_file() and test.is_file() and not backup.exists()
    shutil.copy2(store.path, backup)
    state.event('attempt_history_replay_hardening',
                schema_version=1, model_sha256=sha(model),
                test_sha256=sha(test), append_only=True,
                bounded_output_summary=4096, legacy_reconstruction=True,
                fail_closed_validation=True, registry_promotions=0,
                formal_certificate_allowed=False)
    store.save(state)
    print({'revision': state.revision, 'attempts': len(state.attempts),
           'history': len(state.attempt_history), 'registry': len(state.registry),
           'formal_certificate_allowed': False})


if __name__ == '__main__':
    main()
