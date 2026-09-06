"""Prospective snapshot and synchronous receipt for the one bounded LP."""
from datetime import datetime,timezone
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import uuid

ROOT=Path(__file__).resolve().parent
WORK=ROOT.parent.parent
SOURCE=WORK/'examples/routeb_signed_gap_source/output/run-20260905T203532Z-b2dcff09'
RUN=ROOT/'output'/('lp-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8])
(RUN/'inputs').mkdir(parents=True,exist_ok=False)
paths={'lp_candidate.py':ROOT/'lp_candidate.py','verify_lp.py':ROOT/'verify_lp.py','LP_PLAN.md':ROOT/'LP_PLAN.md',
       'inputs/state_revision46.json':WORK/'artifacts/routeb_6dof/state.json',
       'inputs/reference.json':SOURCE/'inputs/reference.json',
       'inputs/mass.csv':SOURCE/'inputs/routeB_fourier_mass_full_rational.csv',
       'inputs/potential.csv':SOURCE/'inputs/routeB_fourier_potential_rational.csv',
       'inputs/functionals.json':SOURCE/'functionals.json',
       'inputs/nominal_J_functional_bounds.json':SOURCE/'nominal_J_functional_bounds.json',
       'inputs/audit_results.json':SOURCE/'audit_results.json','inputs/source_REPORT.md':SOURCE/'REPORT.md',
       'inputs/source_RESULTS.md':SOURCE/'RESULTS.md'}
paths['inputs/exact_witness.json']=ROOT/'output/post-20260905T210708Z-19f7d8ba/selected_candidate.json'
records={}
for name,path in paths.items():
    shutil.copy2(path,RUN/name)
    records[name]=dict(original=str(path),sha256=hashlib.sha256((RUN/name).read_bytes()).hexdigest())
if json.loads((RUN/'inputs/state_revision46.json').read_text(encoding='utf-8'))['revision']!=46:
    raise RuntimeError('Revision changed; LP not executed')
command=[sys.executable,'-B',str(RUN/'lp_candidate.py')]
(RUN/'before_run.json').write_text(json.dumps(dict(created_utc=datetime.now(timezone.utc).isoformat(),command=command,snapshots=records),indent=2)+'\n',encoding='utf-8')
print('Prospective LP snapshot:',RUN,flush=True)
with (RUN/'terminal.log').open('w',encoding='utf-8') as log:
    log.write('COMMAND '+json.dumps(command)+'\n');log.flush()
    proc=subprocess.run(command,cwd=RUN,stdout=log,stderr=subprocess.STDOUT,check=False)
    log.write('\nLP_SCREEN_EXIT_CODE='+str(proc.returncode)+'\n')
stable=all(hashlib.sha256((RUN/name).read_bytes()).hexdigest()==r['sha256'] for name,r in records.items())
originals={name:hashlib.sha256(Path(r['original']).read_bytes()).hexdigest()==r['sha256'] for name,r in records.items()}
outputs={name:hashlib.sha256((RUN/name).read_bytes()).hexdigest() for name in ('terminal.log','lp_problem.json','lp_candidate_evidence.json') if (RUN/name).exists()}
(RUN/'receipt.json').write_text(json.dumps(dict(exit_code=proc.returncode,snapshots_unchanged=stable,originals_unchanged=originals,outputs=outputs,formal_certificate_allowed=False),indent=2)+'\n',encoding='utf-8')
print((RUN/'terminal.log').read_text(encoding='utf-8'),flush=True)
sys.exit(proc.returncode if proc.returncode else (0 if stable else 2))
