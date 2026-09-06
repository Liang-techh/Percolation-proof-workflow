"""Copied synchronous capture pattern; immutable inputs before each audit."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib
import json
import shutil
import subprocess
import sys
import uuid

SIDE=Path(__file__).resolve().parent
SOURCE=SIDE.parents[2]/'6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq'
run=SIDE/'output'/('run-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8])
(run/'inputs').mkdir(parents=True,exist_ok=False)
local=[SIDE/'audit.py',SIDE/'verify.py']
local += [SIDE/n for n in ('DERIVATION.md','ATTEMPT_HISTORY.md') if (SIDE/n).exists()]
for p in local: shutil.copy2(p,run/p.name)
inputs={name:SOURCE/name for name in ('routeB_fourier_mass_full_rational.csv',
    'routeB_fourier_potential_rational.csv','dhport_lib.jl','routeB_fourier_rational_probe.py')}
inputs['linear_direction.py']=SIDE.parent/'routeb_residual_budget_screen/linear_direction.py'
previous=SIDE.parent/'routeb_residual_budget_screen/linear_output/result.json'
if previous.exists(): inputs['linear_result.json']=previous
evidence={}
for name,p in inputs.items():
    shutil.copy2(p,run/'inputs'/name)
    evidence[name]=dict(original_path=str(p),sha256=hashlib.sha256((run/'inputs'/name).read_bytes()).hexdigest())
manifest=dict(python=sys.version,inputs=evidence,
              local_snapshots={p.name:hashlib.sha256((run/p.name).read_bytes()).hexdigest() for p in local})
(run/'before_run.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print('ATTEMPT_DIRECTORY',run,flush=True)
with (run/'terminal.log').open('w',encoding='utf-8') as log:
    log.write('PRE_RUN_SNAPSHOTS_COMPLETE\n'); log.flush()
    code=1
    try:
        code=subprocess.run([sys.executable,'-B',str(run/'audit.py')],stdout=log,
                            stderr=subprocess.STDOUT,check=False).returncode
    finally:
        log.write(f'\nAUDIT_EXIT_CODE={code}\n'); log.flush()
print((run/'terminal.log').read_text(encoding='utf-8'),end='')
sys.exit(code)
