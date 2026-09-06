"""Replay the pinned formal-math acceptance script in an isolated Linux source tree."""
import json
import os
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

COMMIT = '795efb86f191735c5481675763537cfb4ff37e55'
BASE = Path('/home/z5242/.local/share/percolation-workflow')
REPO = Path('/mnt/c/Users/z5242/Desktop/重构版/工作流/upstream/formal-math')
DEST = BASE / ('formal-math-' + COMMIT)


def main():
    install = json.loads((BASE / 'tools/installation.json').read_text())
    env = dict(os.environ)
    env.update(CARGO_HOME=install['cargo_home'], RUSTUP_HOME=install['rustup_home'],
               TOOLS_DIR=str(BASE / 'verifier-tools'))
    env['PATH'] = ':'.join([install['go_bin'], install['bin'], install['cargo_home'] + '/bin',
                            '/home/z5242/.elan/bin', env['PATH']])
    marker = DEST / 'source-commit.txt'
    if not DEST.exists():
        DEST.mkdir(parents=True)
        archive = subprocess.Popen(['git', '-c', f'safe.directory={REPO}', '-C', str(REPO),
            'archive', COMMIT, 'percolation', '.github/scripts/comparator-check.sh'], stdout=subprocess.PIPE)
        unpack = subprocess.run(['tar', '-x', '-C', str(DEST)], stdin=archive.stdout)
        archive.stdout.close()
        if archive.wait() or unpack.returncode:
            raise RuntimeError('Source archive failed; inspect incomplete destination before retrying')
        marker.write_text(COMMIT + '\n')
    if not marker.exists() or marker.read_text().strip() != COMMIT:
        raise RuntimeError('Refusing to use an unrecognized or incomplete source tree')
    logs = BASE / 'acceptance-logs'
    logs.mkdir(exist_ok=True)
    run_id = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    receipt = {'source_commit': COMMIT, 'source_directory': str(DEST), 'stages': []}
    for stage, command in [
        ('cache', ['lake', 'exe', 'cache', 'get']),
        ('comparator', ['bash', '../.github/scripts/comparator-check.sh']),
    ]:
        log = logs / f'{run_id}-{stage}.log'
        entry = {'stage': stage, 'command': command, 'log': str(log),
                 'started_at': datetime.now(timezone.utc).isoformat(), 'status': 'running'}
        receipt['stages'].append(entry)
        receipt_path = logs / f'{run_id}.json'
        receipt_path.write_text(json.dumps(receipt, indent=2) + '\n')
        print(f'STAGE {stage}; log {log}', flush=True)
        with log.open('w') as out:
            process = subprocess.Popen(command, cwd=DEST / 'percolation', env=env,
                stdout=out, stderr=subprocess.STDOUT)
            entry['pid'] = process.pid
            receipt_path.write_text(json.dumps(receipt, indent=2) + '\n')
            code = process.wait()
        entry.update(exit_code=code, status='passed' if code == 0 else 'failed',
                     finished_at=datetime.now(timezone.utc).isoformat())
        receipt_path.write_text(json.dumps(receipt, indent=2) + '\n')
        print(f'STAGE {stage} exit {code}; receipt {receipt_path}', flush=True)
        if code:
            print(log.read_text(errors='replace')[-6000:], flush=True)
            return code
    return 0


if __name__ == '__main__':
    sys.exit(main())
