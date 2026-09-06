"""Persist strict-admission runtime hardening after targeted verification."""
import hashlib
import shutil

from record_routeb_port_progress import ROOT
from percolation_workflow.store import StateStore


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    store = StateStore(ROOT / 'artifacts/routeb_6dof/state.json')
    state = store.load()
    assert state.revision == 103 and not state.registry
    files = [
        ROOT / 'src/percolation_workflow/strict_admission.py',
        ROOT / 'src/percolation_workflow/verification.py',
        ROOT / 'src/percolation_workflow/controller.py',
        ROOT / 'tests/test_strict_admission.py',
        ROOT / 'tests/test_strict_admission_real.py',
    ]
    backup = ROOT / 'artifacts/routeb_storage_checkpoint_20260905/state-before-revision104.json'
    assert all(path.is_file() for path in files)
    assert not backup.exists()
    shutil.copy2(store.path, backup)
    state.event(
        'strict_admission_runtime_hardening',
        implementation_hashes={str(path.relative_to(ROOT)).replace('\\', '/'): sha(path)
                               for path in files},
        targeted_tests={'command': 'PYTHONPATH=src python -m pytest -q '
                                  'tests/test_strict_admission.py tests/test_strict_admission_real.py',
                        'passed': 6, 'broad_regression_run': False},
        real_fixture={'clean_lake_solution_import': True,
                      'challenge_placeholders_excluded': True,
                      'temporary_audit_file_removed': True},
        real_example={'project': 'examples/minimal_lean',
                      'theorem': 'Minimal.main_verified',
                      'accepted': True,
                      'axioms': ['propext', 'Quot.sound']},
        solution_module_precompiled=True,
        manifest_hash_captured_before_build=True,
        no_axioms_output_supported=True,
        optional_config_gate='strict_admission',
        reduction_default_unchanged=True,
        registry_promotions=0,
        formal_certificate_allowed=False,
    )
    store.save(state)
    print({'revision': state.revision, 'registry': len(state.registry),
           'formal_certificate_allowed': False})


if __name__ == '__main__':
    main()
