"""Manifest-driven frontier verification entry point for the pinned Linux runtime."""
import argparse
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
BASE = Path('/home/z5242/.local/share/percolation-workflow')
sys.path.insert(0, str(ROOT / 'src'))

from percolation_workflow.controller import verify_manifest_frontier
from percolation_workflow.manifest import load_verification_manifest
from percolation_workflow.store import StateStore


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--manifest', required=True)
    parser.add_argument('--dependency-project', required=True)
    parser.add_argument('--bundle-root', required=True)
    parser.add_argument('--comparator-tools', default=str(BASE / 'verifier-tools'))
    parser.add_argument('--max-steps', type=int, default=100)
    args = parser.parse_args()
    manifest = load_verification_manifest(args.manifest)
    tools = Path(args.comparator_tools).resolve()
    os.environ['PATH'] = '/home/z5242/.elan/toolchains/leanprover--lean4---v4.32.0/bin:' + os.environ['PATH']
    os.environ.update(
        COMPARATOR_LANDRUN=str(tools / 'bin/landrun'),
        COMPARATOR_LEAN4EXPORT=str(tools / 'lean4export/.lake/build/bin/lean4export'),
        COMPARATOR_NANODA=str(tools / 'nanoda/target/release/nanoda_bin'),
        LEAN_ABORT_ON_PANIC='1')
    command = ['lake', 'env', str(tools / 'comparator/.lake/build/bin/comparator'), 'comparator.json']
    outcome = verify_manifest_frontier(
        StateStore(manifest.state_path), manifest.path, args.dependency_project,
        args.bundle_root, command, max_steps=args.max_steps)
    print(outcome)
    return 0 if outcome == 'verified' else 1


if __name__ == '__main__':
    raise SystemExit(main())
