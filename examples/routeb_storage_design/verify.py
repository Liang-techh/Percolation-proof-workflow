"""Snapshot before the ONE candidate calculation; write only under this leaf."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parent
WORK = ROOT.parent.parent
SOURCE = WORK/'examples/routeb_signed_gap_source/output/run-20260905T203532Z-b2dcff09'
RUN = ROOT/'output'/('run-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8])
RUN.mkdir(parents=True,exist_ok=False)
(RUN/'inputs').mkdir()
paths = {
    'candidate.py': ROOT/'candidate.py', 'verify.py': ROOT/'verify.py', 'PLAN.md': ROOT/'PLAN.md',
    'inputs/state_revision46.json': WORK/'artifacts/routeb_6dof/state.json',
    'inputs/signed_gap_lean_README.md': WORK/'examples/routeb_signed_gap_lean/README.md',
    'inputs/affine_DERIVATION.md': WORK/'examples/routeb_affine_multiplier/DERIVATION.md',
    'inputs/source_REPORT.md': SOURCE/'REPORT.md', 'inputs/source_RESULTS.md': SOURCE/'RESULTS.md',
    'inputs/source_receipt.json': SOURCE/'receipt.json',
    'inputs/audit_results.json': SOURCE/'audit_results.json',
    'inputs/reference.json': SOURCE/'inputs/reference.json',
    'inputs/functionals.json': SOURCE/'functionals.json',
    'inputs/nominal_J_functional_bounds.json': SOURCE/'nominal_J_functional_bounds.json',
    'inputs/mass.csv': SOURCE/'inputs/routeB_fourier_mass_full_rational.csv',
    'inputs/potential.csv': SOURCE/'inputs/routeB_fourier_potential_rational.csv',
}
records = {}
for name, path in paths.items():
    shutil.copy2(path,RUN/name)
    records[name] = dict(original=str(path),sha256=hashlib.sha256((RUN/name).read_bytes()).hexdigest())
state = json.loads((RUN/'inputs/state_revision46.json').read_text(encoding='utf-8'))
if state['revision'] != 46:
    raise RuntimeError('Current state is no longer revision46; candidate not executed')
command = [sys.executable,'-B',str(RUN/'candidate.py')]
(RUN/'before_run.json').write_text(json.dumps(dict(created_utc=datetime.now(timezone.utc).isoformat(),
    command=command,snapshots=records),indent=2)+'\n',encoding='utf-8')
print('Prospective snapshot:',RUN,flush=True)
with (RUN/'terminal.log').open('w',encoding='utf-8') as log:
    log.write('COMMAND '+json.dumps(command)+'\n');log.flush()
    proc = subprocess.run(command,cwd=RUN,stdout=log,stderr=subprocess.STDOUT,check=False)
    log.write('\nCANDIDATE_EXIT_CODE='+str(proc.returncode)+'\n')
stable = all(hashlib.sha256((RUN/name).read_bytes()).hexdigest()==record['sha256'] for name,record in records.items())
original_stable = {name:hashlib.sha256(Path(record['original']).read_bytes()).hexdigest()==record['sha256']
                   for name,record in records.items()}
outputs = {name:hashlib.sha256((RUN/name).read_bytes()).hexdigest()
           for name in ('candidate_evidence.json','terminal.log') if (RUN/name).exists()}
(RUN/'receipt.json').write_text(json.dumps(dict(exit_code=proc.returncode,snapshots_unchanged=stable,
    originals_unchanged=original_stable,outputs=outputs,formal_certificate_allowed=False),indent=2)+'\n',encoding='utf-8')
print((RUN/'terminal.log').read_text(encoding='utf-8'),flush=True)
print('Receipt:',RUN/'receipt.json',flush=True)
sys.exit(proc.returncode if proc.returncode else (0 if stable else 2))
