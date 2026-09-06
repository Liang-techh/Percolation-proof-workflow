"""Snapshot source/data before one bounded audit and flush its exit receipt."""
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import uuid

side=Path(__file__).resolve().parent
reference=Path(sys.argv[1]).resolve()
source=side.parents[2]/'6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq'
paths=[side/'source_bounds.py',Path(__file__),side.parent/'routeb_inertial_structure/audit.py',reference,
       source/'routeB_fourier_mass_full_rational.csv',source/'routeB_fourier_potential_rational.csv']
run=side/'output'/('bounds-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8])
(run/'inputs').mkdir(parents=True,exist_ok=False)
hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
for p in paths: shutil.copy2(p,run/'inputs'/p.name)
command=[sys.executable,'-B',str(side/'source_bounds.py'),str(run),str(run/'inputs'/reference.name)]
(run/'before_run.json').write_text(json.dumps(dict(inputs=hashes,command=command),indent=2)+'\n',encoding='utf-8')
print('RUN',run,flush=True)
with (run/'terminal.log').open('w',encoding='utf-8') as log:
    code=1
    try:
        code=subprocess.run(command,stdout=log,stderr=subprocess.STDOUT,check=False).returncode
        if any(hashlib.sha256(Path(p).read_bytes()).hexdigest()!=h for p,h in hashes.items()):
            log.write('INPUT_CHANGED_DURING_AUDIT\n');code=1
    finally:
        log.write(f'\nAUDIT_EXIT_CODE={code}\n');log.flush()
print((run/'terminal.log').read_text(encoding='utf-8'),end='')
sys.exit(code)
