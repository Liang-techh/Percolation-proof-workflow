"""Prospective snapshot runner for the single terminal gate audit."""
from datetime import datetime, timezone
import hashlib,json,shutil,subprocess,sys,uuid
from pathlib import Path
side=Path(__file__).resolve().parent; work=side.parent.parent
candidate=work/'examples/routeb_storage_design/output/lp-20260905T210840Z-ac3429b0'
run=side/'output'/('run-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8])
(run/'inputs').mkdir(parents=True,exist_ok=False)
paths={'audit.py':side/'audit.py','verify.py':Path(__file__),'PLAN.md':side/'PLAN.md',
       'inputs/candidate.json':candidate/'lp_candidate_evidence.json',
       'inputs/candidate_receipt.json':candidate/'receipt.json',
       'inputs/reference.json':candidate/'inputs/reference.json',
       'inputs/mass.csv':candidate/'inputs/mass.csv',
       'inputs/derivation.md':work/'examples/routeb_storage_design/DERIVATION.md'}
for name,path in paths.items(): shutil.copy2(path,run/name)
snapshots={name:hashlib.sha256((run/name).read_bytes()).hexdigest() for name in paths}
(run/'before_run.json').write_text(json.dumps({'snapshots':snapshots,'originals':{k:str(v) for k,v in paths.items()}},indent=2)+'\n',encoding='utf-8')
with (run/'terminal.log').open('w',encoding='utf-8') as log:
    log.write('COMMAND '+json.dumps([sys.executable,'-B',str(run/'audit.py'),str(run)])+'\n')
    code=subprocess.run([sys.executable,'-B',str(run/'audit.py'),str(run)],stdout=log,stderr=subprocess.STDOUT,check=False).returncode
    log.write(f'\nAUDIT_EXIT_CODE={code}\n')
print('RUN',run)
print((run/'terminal.log').read_text(encoding='utf-8'))
sys.exit(code)
