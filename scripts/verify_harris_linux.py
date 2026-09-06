"""Verify the staged Harris proof with pinned dual-kernel tools, then close its DAG."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path('/mnt/c/Users/z5242/Desktop/重构版/工作流')
BASE = Path('/home/z5242/.local/share/percolation-workflow')
UPSTREAM = BASE / 'formal-math-795efb86f191735c5481675763537cfb4ff37e55/percolation'
sys.path.insert(0, str(ROOT / 'src'))
from percolation_workflow.verification import verify_and_register
from percolation_workflow.store import StateStore
from percolation_workflow.graph import attach_statement_index
from percolation_workflow.statements import index_statements


def main():
    source = ROOT / 'examples/harris_replay'
    names = ['Challenge.lean', 'Solution.lean', 'HarrisReplay.lean', 'HarrisReplay/Positive.lean',
             'HarrisReplay/Expansion.lean', 'lean-toolchain', 'comparator.json']
    content = {name: (source / name).read_bytes() for name in names}
    digest = hashlib.sha256(b''.join(name.encode() + content[name] for name in sorted(names))).hexdigest()
    project = BASE / ('harris-' + digest[:16])
    marker = project / 'snapshot.json'
    if not project.exists():
        project.mkdir()
        for name, data in content.items():
            dest = project / name
            dest.parent.mkdir(exist_ok=True)
            dest.write_bytes(data)
        config = (source / 'lakefile.toml').read_text().replace(
            '../../upstream/formal-math/percolation/.lake/packages/mathlib',
            str(UPSTREAM / '.lake/packages/mathlib'))
        (project / 'lakefile.toml').write_text(config)
        manifest = json.loads((source / 'lake-manifest.json').read_text())
        for package in manifest['packages']:
            if package['name'] == 'mathlib':
                package['dir'] = str(UPSTREAM / '.lake/packages/mathlib')
        (project / 'lake-manifest.json').write_text(json.dumps(manifest, indent=2))
        (project / '.lake').mkdir()
        (project / '.lake/packages').symlink_to(UPSTREAM / '.lake/packages', target_is_directory=True)
        marker.write_text(json.dumps({'source_digest': digest}))
    if not marker.exists() or json.loads(marker.read_text())['source_digest'] != digest:
        raise ValueError('incomplete snapshot; inspect before retrying')
    for name, data in content.items():
        if (project / name).read_bytes() != data:
            raise ValueError('snapshot source mismatch')
    prefix = '/home/z5242/.elan/toolchains/leanprover--lean4---v4.32.0/bin'
    os.environ['PATH'] = prefix + ':' + os.environ['PATH']
    tools = BASE / 'verifier-tools'
    os.environ.update(COMPARATOR_LANDRUN=str(tools / 'bin/landrun'),
        COMPARATOR_LEAN4EXPORT=str(tools / 'lean4export/.lake/build/bin/lean4export'),
        COMPARATOR_NANODA=str(tools / 'nanoda/target/release/nanoda_bin'), LEAN_ABORT_ON_PANIC='1')
    store = StateStore(ROOT / 'artifacts/harris_replay/state.json')
    if not store.path.exists():
        raise FileNotFoundError(store.path)
    state = store.load()
    attach_statement_index(state, index_statements(project / 'Challenge.lean'))
    state.event('harris_linux_snapshot', path=str(project), digest=digest)
    store.save(state)
    command = ['lake', 'env', str(tools / 'comparator/.lake/build/bin/comparator'), 'comparator.json']
    for name in ['HarrisReplay.iterated_nonneg', 'HarrisReplay.inner_expansion', 'HarrisReplay.harris']:
        node = next(n for n in state.nodes.values() if n.name == name)
        if node.status == 'verified':
            raise ValueError('existing verification requires an explicit reuse/revalidation decision')
        print(f'Verifying {name} in {project}', flush=True)
        if not verify_and_register(state, node.id, project, command, store=store):
            print(f'Failed: {name}; diagnostics retained in {store.path}', flush=True)
            return 1
        print(f'Registered {name}', flush=True)
    result = subprocess.run(['lake', 'build'], cwd=project)
    state.event('harris_full_project_build', exit_code=result.returncode)
    store.save(state)
    return result.returncode


if __name__ == '__main__':
    sys.exit(main())
