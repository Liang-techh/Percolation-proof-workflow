"""Snapshot BEFORE audit; each invocation retains its own code, inputs and failure log."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import uuid


def main():
    side = Path(__file__).resolve().parent
    root = side.parents[1]
    source = root.parent / '6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq'
    run = side / 'output' / ('run-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-' + uuid.uuid4().hex[:8])
    (run / 'inputs').mkdir(parents=True, exist_ok=False)
    paths = {p.name: p for p in side.iterdir() if p.is_file()}
    external = {
        'inertial_audit.py': root / 'examples/routeb_inertial_structure/audit.py',
        'gain_audit.py': root / 'examples/routeb_coupled_finite_gain/audit.py',
        'coupled_audit.py': root / 'examples/routeb_coupled_linear_reference/audit.py',
        'coupled_DERIVATION.md': root / 'examples/routeb_coupled_linear_reference/DERIVATION.md',
        'reference.json': root / 'examples/routeb_coupled_linear_reference/output/run-20260905T192654Z-3dbe159f/reference.json',
        'prefix_audit.py': root / 'examples/routeb_prefix_budget/audit.py',
        'prefix_DERIVATION.md': root / 'examples/routeb_prefix_budget/DERIVATION.md',
        'prefix_results.json': root / 'examples/routeb_prefix_budget/output/run-20260905T200854Z-88e7c74d/field_name_correction/results.json',
        'SIGNED_WORK.md': root / 'examples/routeb_J_strategy/SIGNED_WORK.md',
        'strategy_REPORT.md': root / 'examples/routeb_J_strategy/REPORT.md',
    }
    for name in ('routeB_fourier_mass_full_rational.csv', 'routeB_fourier_coriolis_rational.csv',
                 'routeB_fourier_potential_rational.csv', 'dhport_lib.jl', 'routeB_fourier_rational_probe.py'):
        external[name] = source / name
    paths.update({'inputs/' + name: path for name, path in external.items()})
    manifest = {}
    for name, path in paths.items():
        shutil.copy2(path, run / name)
        manifest[name] = dict(original=str(path), sha256=hashlib.sha256((run/name).read_bytes()).hexdigest())
    before = dict(created_utc=datetime.now(timezone.utc).isoformat(), snapshots=manifest,
                  execution=[sys.executable, '-B', str(run/'audit.py')],
                  policy='All audit reads use snapshots. All writes stay in this attempt. Failed attempts retained.')
    (run/'before_run.json').write_text(json.dumps(before, indent=2)+'\n', encoding='utf-8')
    print('RUN', run, flush=True)
    code = 1
    try:
        with (run/'terminal.log').open('w', encoding='utf-8') as log:
            try:
                env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
                code = subprocess.run(before['execution'], cwd=run, env=env, stdout=log,
                                      stderr=subprocess.STDOUT, check=False).returncode
            finally:
                log.write(f'\nAUDIT_EXIT_CODE={code}\n')
    finally:
        unchanged = {name: hashlib.sha256((run/name).read_bytes()).hexdigest() == entry['sha256']
                     for name, entry in manifest.items()}
        outputs = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in run.iterdir()
                   if p.is_file() and p.name not in manifest and p.name != 'receipt.json'}
        receipt = dict(exit_code=code, input_and_code_unchanged=unchanged, output_sha256=outputs,
                       finished_utc=datetime.now(timezone.utc).isoformat())
        (run/'receipt.json').write_text(json.dumps(receipt, indent=2)+'\n', encoding='utf-8')
    print((run/'terminal.log').read_text(encoding='utf-8'), end='')
    if not all(unchanged.values()): raise RuntimeError('snapshot changed during execution')
    return code


if __name__ == '__main__': sys.exit(main())
