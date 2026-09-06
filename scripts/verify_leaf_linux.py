"""Freeze and independently verify one compiled frontier leaf.

The coordinator supplies a portable verification manifest plus the pinned dependency
checkout. The verifier derives each node's challenge, solution and frozen source set
from that manifest, so target-specific theorem/module names do not live in the engine.
"""
import argparse
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
BASE = Path('/home/z5242/.local/share/percolation-workflow')
sys.path.insert(0, str(ROOT / 'src'))

from percolation_workflow.bundles import stage_bundle
from percolation_workflow.manifest import bind_manifest, load_verification_manifest
from percolation_workflow.registry import audit_registry
from percolation_workflow.store import StateStore
from percolation_workflow.verification import verify_and_register


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--manifest', required=True,
                        help='portable verification-manifest.json')
    parser.add_argument('--bundle-root', required=True)
    parser.add_argument('--dependency-project', required=True)
    parser.add_argument('--node', required=True, help='exact theorem name')
    parser.add_argument('--comparator-tools', default=str(BASE / 'verifier-tools'))
    args = parser.parse_args()

    manifest = load_verification_manifest(args.manifest)
    source_project = manifest.path.parent
    state_path = manifest.state_path
    node_manifest = manifest.for_node(args.node)
    store = StateStore(state_path)
    bind_manifest(store, manifest)
    state = store.load()
    matches = [node for node in state.nodes.values() if node.name == args.node]
    if len(matches) != 1:
        raise ValueError('expected one exact theorem in the live DAG')
    node = matches[0]
    if node not in state.frontier() or not node.attempts:
        raise ValueError('selected node is not an open frontier leaf with an attempt')
    if not any(state.attempts[attempt].status in {'candidate_ready', 'compiled'}
               for attempt in node.attempts):
        raise ValueError('selected leaf has no successful agent candidate')
    if any(item['status'] != 'current' for item in audit_registry(state).values()):
        raise ValueError('existing registry needs revalidation before reuse')

    project = stage_bundle(
        source_project, args.bundle_root, node_name=node.name,
        challenge_module=node_manifest.challenge_module,
        solution_module=node_manifest.solution_module,
        source_files=node_manifest.source_files,
        dependency_project=args.dependency_project,
        dependency_name=manifest.dependency_name,
        manifest_identity=manifest.identity_for_state())

    tools = Path(args.comparator_tools).resolve()
    os.environ['PATH'] = '/home/z5242/.elan/toolchains/leanprover--lean4---v4.32.0/bin:' + os.environ['PATH']
    os.environ.update(
        COMPARATOR_LANDRUN=str(tools / 'bin/landrun'),
        COMPARATOR_LEAN4EXPORT=str(tools / 'lean4export/.lake/build/bin/lean4export'),
        COMPARATOR_NANODA=str(tools / 'nanoda/target/release/nanoda_bin'),
        LEAN_ABORT_ON_PANIC='1')
    state.event('leaf_bundle_staged', node_id=node.id, project=str(project),
                source_files=node_manifest.source_files,
                solution_module=node_manifest.solution_module,
                manifest=str(manifest.path))
    store.save(state)
    print(f'Verifying {node.name} in {project}', flush=True)
    accepted = verify_and_register(
        state, node.id, project,
        ['lake', 'env', str(tools / 'comparator/.lake/build/bin/comparator'), 'comparator.json'],
        store=store,
        manifest_identity=manifest.identity_for_state(),
        artifact_aliases=[Path('\\\\wsl.localhost\\Ubuntu') / str(project).lstrip('/')])
    print('registered' if accepted else 'rejected; diagnostics retained', flush=True)
    return 0 if accepted else 1


if __name__ == '__main__':
    raise SystemExit(main())
