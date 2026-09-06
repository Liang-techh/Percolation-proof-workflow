"""A durable compiler process: writes diagnostics independently of the coordinator.

This worker never edits research state or registers a theorem. Its private job directory
is coordinator-owned; the receipt is a recovery mechanism, not a security boundary.
"""
import json
import os
from pathlib import Path
import sys
from dataclasses import asdict
from .lean import run_lean


def main():
    directory = Path(sys.argv[1]).resolve()
    job = json.loads((directory / 'job.json').read_text(encoding='utf-8'))
    # Exclusive creation prevents accidental relaunch of the same job. A marker is
    # never used as evidence that the process is still alive or has terminated.
    with (directory / 'started.json').open('x', encoding='utf-8') as output:
        json.dump({'pid': os.getpid(), 'attempt_id': job['attempt_id']}, output)
    commands = job.get('commands') or [job['command']]
    if (not isinstance(commands, list) or not commands or
            any(not isinstance(command, list) for command in commands)):
        raise ValueError('compiler job has malformed command list')
    steps = []
    for command in commands:
        step = run_lean(job['project'], command)
        steps.append(asdict(step))
        if not step.ok:
            break
    result = steps[-1]
    # The public result remains the entrypoint command for backward-compatible
    # coordinator identity checks; ``steps`` records every supporting module
    # compiled before it, with raw diagnostics for repair.
    result['command'] = job['command']
    result['stdout'] = '\n'.join(step['stdout'] for step in steps)
    result['stderr'] = '\n'.join(step['stderr'] for step in steps)
    result['ok'] = all(step['ok'] for step in steps)
    result['exit_code'] = 0 if result['ok'] else next(
        step['exit_code'] for step in steps if not step['ok'])
    receipt = {'attempt_id': job['attempt_id'], 'request_id': job['request_id'],
               'result': result, 'steps': steps}
    temporary = directory / 'result.tmp'
    temporary.write_text(json.dumps(receipt, ensure_ascii=False), encoding='utf-8')
    temporary.replace(directory / 'result.json')


if __name__ == '__main__':
    main()
