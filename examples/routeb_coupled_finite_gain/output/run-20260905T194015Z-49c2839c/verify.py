"""Snapshot before computation; synchronous complete terminal receipt."""
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import uuid

side=Path(__file__).resolve().parent
ref=Path(sys.argv[1]).resolve()
run=side/'output'/('run-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8])
(run/'inputs').mkdir(parents=True,exist_ok=False)
for path in (side/'audit.py',Path(__file__)): shutil.copy2(path,run/path.name)
shutil.copy2(ref,run/'inputs/reference.json')
manifest={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (run/'audit.py',run/'verify.py')}
manifest['inputs/reference.json']=hashlib.sha256((run/'inputs/reference.json').read_bytes()).hexdigest()
(run/'before_run.json').write_text(json.dumps(dict(snapshots=manifest,original_reference=str(ref)),indent=2)+'\n',encoding='utf-8')
print('RUN',run,flush=True)
with (run/'terminal.log').open('w',encoding='utf-8') as log:
    code=1
    try: code=subprocess.run([sys.executable,'-B',str(run/'audit.py'),str(run)],stdout=log,stderr=subprocess.STDOUT,check=False).returncode
    finally: log.write(f'\nAUDIT_EXIT_CODE={code}\n');log.flush()
print((run/'terminal.log').read_text(encoding='utf-8'),end='')
sys.exit(code)
