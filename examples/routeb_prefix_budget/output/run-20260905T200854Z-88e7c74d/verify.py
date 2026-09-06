"""Immutable snapshots, snapshot execution and synchronous terminal receipt."""
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import uuid

side=Path(__file__).resolve().parent
root=side.parents[1]
source=root.parent/'6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq'
reference=side.parent/'routeb_coupled_linear_reference/output/run-20260905T192654Z-3dbe159f/reference.json'
run=side/'output'/('run-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8])
(run/'inputs').mkdir(parents=True,exist_ok=False)
paths={
    'audit.py':side/'audit.py','verify.py':Path(__file__),
    'inputs/gain_audit.py':side.parent/'routeb_coupled_finite_gain/audit.py',
    'inputs/inertial_audit.py':side.parent/'routeb_inertial_structure/audit.py',
    'inputs/reference.json':reference,
    'inputs/routeB_fourier_mass_full_rational.csv':source/'routeB_fourier_mass_full_rational.csv',
    'inputs/routeB_fourier_potential_rational.csv':source/'routeB_fourier_potential_rational.csv'}
for name,path in paths.items(): shutil.copy2(path,run/name)
manifest={name:hashlib.sha256((run/name).read_bytes()).hexdigest() for name in paths}
(run/'before_run.json').write_text(json.dumps(dict(snapshots=manifest,originals={k:str(v) for k,v in paths.items()}),indent=2)+'\n',encoding='utf-8')
print('RUN',run,flush=True)
with (run/'terminal.log').open('w',encoding='utf-8') as log:
    code=1
    try: code=subprocess.run([sys.executable,'-B',str(run/'audit.py'),str(run)],stdout=log,stderr=subprocess.STDOUT,check=False).returncode
    finally: log.write(f'\nAUDIT_EXIT_CODE={code}\n');log.flush()
print((run/'terminal.log').read_text(encoding='utf-8'),end='')
sys.exit(code)
