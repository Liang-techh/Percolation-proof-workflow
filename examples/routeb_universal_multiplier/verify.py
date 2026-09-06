"""Prospective snapshot execution; never overwrite a prior receipt."""
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import uuid

side=Path(__file__).resolve().parent
run=side/'output'/('run-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8])
(run/'inputs').mkdir(parents=True,exist_ok=False)
files={'audit.py':side/'audit.py','verify.py':Path(__file__),
       'inputs/reference.json':side.parent/'routeb_coupled_linear_reference/output/run-20260905T192654Z-3dbe159f/reference.json',
       'inputs/affine_derivation.md':side.parent/'routeb_affine_multiplier/DERIVATION.md'}
for name,path in files.items(): shutil.copy2(path,run/name)
snapshots={name:hashlib.sha256((run/name).read_bytes()).hexdigest() for name in files}
(run/'before_run.json').write_text(json.dumps(dict(snapshots=snapshots,originals={k:str(v) for k,v in files.items()}),indent=2)+'\n',encoding='utf-8')
print('RUN',run,flush=True)
with (run/'terminal.log').open('x',encoding='utf-8') as log:
    code=1
    try: code=subprocess.run([sys.executable,'-B',str(run/'audit.py'),str(run)],stdout=log,stderr=subprocess.STDOUT,check=False).returncode
    finally: log.write(f'\nAUDIT_EXIT_CODE={code}\n');log.flush()
print((run/'terminal.log').read_text(encoding='utf-8'),end='')
sys.exit(code)
