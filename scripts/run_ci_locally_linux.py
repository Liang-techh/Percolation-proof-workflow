"""Run the portable CI entry point in a fresh Linux workspace; no hosted Actions claim."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path('/mnt/c/Users/z5242/Desktop/重构版/工作流')
BASE = Path('/home/z5242/.local/share/percolation-workflow')
COMMIT = '795efb86f191735c5481675763537cfb4ff37e55'


def main():
    workspace = Path(tempfile.mkdtemp(prefix='ci-', dir=BASE))
    for folder in ('src', 'tests', 'scripts', 'examples', '.github'):
        shutil.copytree(ROOT / folder, workspace / folder,
                        ignore=shutil.ignore_patterns('.lake', '__pycache__', '*.pyc'))
    for shell in (workspace / 'scripts').glob('*.sh'):
        shell.write_text(shell.read_text())
    upstream = workspace / 'upstream/formal-math'
    upstream.parent.mkdir()
    origin = ROOT / 'upstream/formal-math'
    subprocess.run(['git', '-c', f'safe.directory={origin}', 'clone', '--no-hardlinks',
                    str(origin), str(upstream)], check=True)
    subprocess.run(['git', '-C', str(upstream), 'checkout', '--detach', COMMIT], check=True)
    installation = json.loads((BASE / 'tools/installation.json').read_text())
    env = dict(os.environ, CARGO_HOME=installation['cargo_home'], RUSTUP_HOME=installation['rustup_home'],
               TOOLS_DIR=str(BASE / 'verifier-tools'), RUNNER_TEMP=str(workspace / 'runner-temp'))
    env['PATH'] = ':'.join(['/home/z5242/.elan/bin', installation['go_bin'], installation['bin'],
                            installation['cargo_home'] + '/bin', '/usr/bin', '/bin'])
    (workspace / 'runner-temp').mkdir()
    log = workspace / 'ci.log'
    receipt_path = workspace / 'ci-receipt.json'
    receipt = {'workspace': str(workspace), 'log': str(log), 'command': ['bash', 'scripts/ci_harris.sh'],
               'status': 'running', 'scope': 'local Linux execution of CI script'}
    receipt_path.write_text(json.dumps(receipt, indent=2))
    print(f'CI workspace {workspace}', flush=True)
    with log.open('w') as out:
        process = subprocess.Popen(receipt['command'], cwd=workspace, env=env, stdout=out,
                                   stderr=subprocess.STDOUT)
        receipt['pid'] = process.pid
        receipt_path.write_text(json.dumps(receipt, indent=2))
        code = process.wait()
    receipt.update(exit_code=code, status='passed' if code == 0 else 'failed')
    receipt_path.write_text(json.dumps(receipt, indent=2))
    print(f'CI exit {code}; receipt {receipt_path}', flush=True)
    print(log.read_text(errors='replace')[-5000:], flush=True)
    return code


if __name__ == '__main__':
    raise SystemExit(main())
