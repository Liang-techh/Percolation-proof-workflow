"""Freeze one compiled live FKG leaf and verify it with the pinned upstream comparator.

Run only after recording the real agent result and coordinator compilation. No hard-coded
verification order; each selected node must be an open frontier leaf.
"""
import argparse
import os
from pathlib import Path
import sys

ROOT = Path('/mnt/c/Users/z5242/Desktop/重构版/工作流')
BASE = Path('/home/z5242/.local/share/percolation-workflow')
UPSTREAM = BASE / 'formal-math-795efb86f191735c5481675763537cfb4ff37e55/percolation'
sys.path.insert(0, str(ROOT / 'src'))
from percolation_workflow.bundles import stage_bundle
from percolation_workflow.store import StateStore
from percolation_workflow.verification import verify_and_register
from percolation_workflow.registry import audit_registry


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--node', required=True, help='exact theorem name')
    parser.add_argument('--solution-module', required=True)
    parser.add_argument('--challenge-module', default='LocalFKGObligations')
    parser.add_argument('--source-file', action='append', required=True,
                        help='explicit relative proof/support Lean file; repeat if needed')
    args = parser.parse_args()
    store = StateStore(ROOT / 'artifacts/local_fkg/state.json')
    state = store.load()
    matches = [n for n in state.nodes.values() if n.name == args.node]
    if len(matches) != 1:
        raise ValueError('expected one exact theorem in the live DAG')
    node = matches[0]
    if node not in state.frontier() or not node.attempts or state.attempts[node.attempts[-1]].status != 'compiled':
        raise ValueError('selected leaf has no coordinator-compiled frontier candidate')
    if any(item['status'] != 'current' for item in audit_registry(state).values()):
        raise ValueError('existing registry needs revalidation before reuse')
    project = stage_bundle(ROOT / 'examples/local_fkg', BASE / 'local-fkg-bundles',
        node_name=node.name, challenge_module=args.challenge_module, solution_module=args.solution_module,
        source_files=['LocalFKGDefinitions.lean', 'LocalFKGObligations.lean', *args.source_file],
        dependency_project=UPSTREAM, dependency_name='PercolationContinuity')
    tools = BASE / 'verifier-tools'
    os.environ['PATH'] = '/home/z5242/.elan/toolchains/leanprover--lean4---v4.32.0/bin:' + os.environ['PATH']
    os.environ.update(COMPARATOR_LANDRUN=str(tools / 'bin/landrun'),
        COMPARATOR_LEAN4EXPORT=str(tools / 'lean4export/.lake/build/bin/lean4export'),
        COMPARATOR_NANODA=str(tools / 'nanoda/target/release/nanoda_bin'), LEAN_ABORT_ON_PANIC='1')
    state.event('leaf_bundle_staged', node_id=node.id, project=str(project),
                source_files=args.source_file, solution_module=args.solution_module)
    store.save(state)
    print(f'Verifying {node.name} in {project}', flush=True)
    accepted = verify_and_register(state, node.id, project,
        ['lake', 'env', str(tools / 'comparator/.lake/build/bin/comparator'), 'comparator.json'], store=store,
        artifact_aliases=[Path('\\\\wsl.localhost\\Ubuntu') / str(project).lstrip('/')])
    print('registered' if accepted else 'rejected; diagnostics retained', flush=True)
    return 0 if accepted else 1


if __name__ == '__main__':
    raise SystemExit(main())
