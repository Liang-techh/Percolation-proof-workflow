"""Persist strict Lean admission hardening and optional integration."""
import hashlib
import shutil

from record_routeb_port_progress import ROOT
from percolation_workflow.store import StateStore


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    store = StateStore(ROOT / 'artifacts/routeb_6dof/state.json')
    state = store.load()
    assert state.revision == 101 and not state.registry
    files = [ROOT / 'src/percolation_workflow/strict_admission.py',
             ROOT / 'src/percolation_workflow/verification.py',
             ROOT / 'src/percolation_workflow/controller.py',
             ROOT / 'tests/test_strict_admission.py']
    backup = ROOT / 'artifacts/routeb_storage_checkpoint_20260905/state-before-revision102.json'
    assert all(path.is_file() for path in files) and not backup.exists()
    shutil.copy2(store.path, backup)
    state.event('strict_lean_admission_hardening',
                implementation_hashes={str(path.relative_to(ROOT)).replace('\\', '/'): sha(path)
                                       for path in files},
                parser_supports_real_lean_axiom_reports=True,
                generated_audit_imports_solution_module=True,
                challenge_placeholders_excluded=True,
                optional_config_gate='strict_admission',
                reduction_default_unchanged=True,
                registry_promotions=0, formal_certificate_allowed=False)
    store.save(state)
    print({'revision': state.revision, 'registry': len(state.registry),
           'formal_certificate_allowed': False})


if __name__ == '__main__':
    main()
