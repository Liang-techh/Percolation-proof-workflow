"""Persist targeted strict-admission/comparator ordering tests."""
import hashlib
import shutil

from record_routeb_port_progress import ROOT
from percolation_workflow.store import StateStore


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    store = StateStore(ROOT / 'artifacts/routeb_6dof/state.json')
    state = store.load()
    assert state.revision == 108 and not state.registry
    test = ROOT / 'tests/test_verification_gate.py'
    backup = ROOT / 'artifacts/routeb_storage_checkpoint_20260905/state-before-revision109.json'
    assert test.is_file() and not backup.exists()
    shutil.copy2(store.path, backup)
    state.event(
        'strict_comparator_seam_targeted_tests',
        implementation_hashes={'tests/test_verification_gate.py': sha(test)},
        command='PYTHONPATH=src python -m pytest -q tests/test_verification_gate.py',
        passed=4,
        strict_failure_short_circuit=True,
        strict_failure_comparator_calls=0,
        strict_failure_registry_promotions=0,
        default_false_path_unchanged=True,
        broad_regression_run=False,
        registry_promotions=0,
        formal_certificate_allowed=False,
    )
    store.save(state)
    print({'revision': state.revision, 'registry': len(state.registry),
           'formal_certificate_allowed': False})


if __name__ == '__main__':
    main()
