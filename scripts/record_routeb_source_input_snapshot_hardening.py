"""Persist comparator-declared source-input snapshot hardening."""
import hashlib
import shutil

from record_routeb_port_progress import ROOT, ref
from percolation_workflow.store import StateStore


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    store = StateStore(ROOT / 'artifacts/routeb_6dof/state.json')
    state = store.load()
    assert state.revision == 100 and not state.registry
    files = [ROOT / 'src/percolation_workflow/comparator.py',
             ROOT / 'src/percolation_workflow/verification.py',
             ROOT / 'src/percolation_workflow/registry.py',
             ROOT / 'src/percolation_workflow/controller.py',
             ROOT / 'tests/test_declared_source_inputs.py']
    backup = ROOT / 'artifacts/routeb_storage_checkpoint_20260905/state-before-revision101.json'
    assert all(path.is_file() for path in files) and not backup.exists()
    shutil.copy2(store.path, backup)
    state.event('comparator_declared_source_input_snapshot_hardening',
                schema_version=1,
                source_files=['relative_explicit_only', 'no_globs', 'inside_project_only'],
                implementation_hashes={str(path.relative_to(ROOT)).replace('\\', '/'): sha(path)
                                       for path in files},
                registry_freshness_reuses_receipt_inputs=True,
                unsafe_or_missing_inputs_fail_closed=True,
                registry_promotions=0, formal_certificate_allowed=False)
    store.save(state)
    print({'revision': state.revision, 'registry': len(state.registry),
           'formal_certificate_allowed': False})


if __name__ == '__main__':
    main()
