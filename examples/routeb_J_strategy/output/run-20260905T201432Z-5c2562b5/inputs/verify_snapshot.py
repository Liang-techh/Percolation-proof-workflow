"""One immutable snapshot run of the targeted algebra audit; own directory only."""
import datetime as dt
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import uuid

HERE = Path(__file__).resolve().parent
def stamp():
    return dt.datetime.now(dt.timezone.utc).isoformat()
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

tag = dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
run = HERE / 'output' / ('run-' + tag + '-' + uuid.uuid4().hex[:8])
inputs = run / 'inputs'
inputs.mkdir(parents=True, exist_ok=False)
source = HERE.parents[2] / '6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq'
files = {
    'algebra_audit.py': HERE / 'algebra_audit.py',
    'verify_snapshot.py': HERE / 'verify_snapshot.py',
    'REPORT.md': HERE / 'REPORT.md',
    'SIGNED_WORK.md': HERE / 'SIGNED_WORK.md',
    'inertial_algebra.py': HERE.parent / 'routeb_inertial_structure/audit.py',
    'reference.json': HERE.parent / 'routeb_coupled_linear_reference/output/'
        'run-20260905T192654Z-3dbe159f/reference.json',
    'routeB_fourier_mass_full_rational.csv': source / 'routeB_fourier_mass_full_rational.csv',
    'routeB_fourier_potential_rational.csv': source / 'routeB_fourier_potential_rational.csv',
    'prefix_results.input.json': HERE.parent / 'routeb_prefix_budget/output/'
        'run-20260905T200606Z-34dbb987/results.json',
}
hashes = []
for name, path in files.items():
    original_hash = sha(path)
    target = inputs / name
    shutil.copy2(path, target)
    assert sha(target) == original_hash == sha(path)
    hashes.append({'original': str(path), 'snapshot': str(target), 'sha256': original_hash})
command = [sys.executable, '-B', str(inputs / 'algebra_audit.py'), '--inputs', str(inputs)]
before = {
    'recorded_at_utc': stamp(), 'command': command, 'cwd': str(HERE),
    'files': hashes,
    'prior_execution_notice': 'RETROSPECTIVE: development executions already occurred without immutable snapshots or terminal.log receipts. This file does not reconstruct or certify those executions. The following execution is a new prospective snapshot run.',
    'scope': 'Targeted exact algebra, not a trajectory run or J/M4 certificate.',
}
(run / 'before_run.json').write_text(json.dumps(before, indent=2) + '\n', encoding='utf-8')
stdout = []
with (run / 'terminal.log').open('x', encoding='utf-8') as log:
    log.write('START_UTC=' + stamp() + '\n')
    log.write('BEFORE_RUN_SHA256=' + sha(run / 'before_run.json') + '\n')
    log.flush()
    child = subprocess.Popen(command, cwd=HERE, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, text=True, encoding='utf-8')
    for line in child.stdout:
        stdout.append(line)
        log.write(line)
        log.flush()
    code = child.wait()
    log.write('AUDIT_EXIT_CODE=' + str(code) + '\nEND_UTC=' + stamp() + '\n')
    log.flush()
if code == 0:
    result = json.loads(''.join(stdout))
    assert result['status'] == 'EXACT_TARGETED_J_ALGEBRA_PASS'
    (run / 'audit_results.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
unchanged = all(sha(Path(item['original'])) == item['sha256'] and
                sha(Path(item['snapshot'])) == item['sha256'] for item in hashes)
receipt = {'completed_at_utc': stamp(), 'exit_code': code,
    'before_run_sha256': sha(run / 'before_run.json'),
    'terminal_log_sha256': sha(run / 'terminal.log'),
    'originals_and_snapshots_unchanged': unchanged,
    'result_sha256': sha(run / 'audit_results.json') if code == 0 else None}
(run / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'run': str(run), **receipt}, indent=2))
sys.exit(code if code else (0 if unchanged else 2))
