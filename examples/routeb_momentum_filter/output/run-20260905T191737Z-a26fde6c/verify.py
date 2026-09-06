"""Synchronous attempt capture: snapshots and log exist before each audit.

No async tee or shell pipe: subprocess writes directly to the open log;
the parent waits, then appends and flushes the exit trailer before returning.
"""
from pathlib import Path
from datetime import datetime,timezone
import hashlib
import json
import shutil
import subprocess
import sys
import uuid

SIDE=Path(__file__).resolve().parent
run=SIDE/'output'/('run-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8])
run.mkdir(parents=True,exist_ok=False)
paths=[SIDE/'audit.py',SIDE/'verify.py']
paths += [SIDE/n for n in ('DERIVATION.md','ATTEMPT_HISTORY.md') if (SIDE/n).exists()]
for path in paths: shutil.copy2(path,run/path.name)
source_bounds=SIDE.parent/'routeb_momentum_source_bounds/bounds.json'
if source_bounds.exists(): shutil.copy2(source_bounds,run/'source_bounds.input.json')
manifest={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
if source_bounds.exists(): manifest['source_bounds.input.json']=hashlib.sha256((run/'source_bounds.input.json').read_bytes()).hexdigest()
(run/'before_run.json').write_text(json.dumps(dict(source_snapshots=manifest,python=sys.version),indent=2)+'\n',encoding='utf-8')
print('ATTEMPT_DIRECTORY',run,flush=True)
with (run/'terminal.log').open('w',encoding='utf-8') as log:
    log.write('PRE_RUN_SNAPSHOTS_COMPLETE\n'); log.flush()
    code=1
    try:
        # Execute the saved program, with its source directory supplied through
        # a normal runpy global override handled below, never the mutable draft.
        command=[sys.executable,'-B','-c',
                 'import runpy,sys; d=runpy.run_path(sys.argv[1],run_name="snapshot"); '
                 'd["main"].__globals__["HERE"]=__import__("pathlib").Path(sys.argv[2]); '
                 'sys.argv=[sys.argv[1],sys.argv[3]]; d["main"]()',str(run/'audit.py'),str(SIDE),str(run)]
        code=subprocess.run(command,stdout=log,stderr=subprocess.STDOUT,check=False).returncode
    finally:
        log.write(f'\nAUDIT_EXIT_CODE={code}\n'); log.flush()
print((run/'terminal.log').read_text(encoding='utf-8'),end='')
sys.exit(code)
