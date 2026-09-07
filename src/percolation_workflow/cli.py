from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from .store import StateStore
from .registry import audit_registry
from .controller import verify_frontier, verify_manifest_frontier
from .manifest import load_verification_manifest, initialize_state_from_manifest
from .sketch import check_sketch
from .decomposition import ChildGoal, propose_decomposition
from .research import next_actions
from .agent_bridge import (prepare_requests, bind_agent, record_result, check_candidate,
                           collect_candidate, ingest_compile_log, retry_candidate,
                           renew_agent, reclaim_expired_agent)
from .host_cycle import run_host_cycle
from .host_adapter import FilesystemHostAdapter
from .codex_adapter import infer_manifest_project, run_codex_dispatch, run_codex_batch
from .external import initialize_routeb_intake, run_external_gate, refresh_routeb_tracking
from .repair_classification import dry_run_repair_integration
from .merlean_plan_projection import export_views as export_merlean_plan_views


def main() -> int | None:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["status", "audit-registry", "verify-frontier", "verify-manifest",
                                            "init-manifest", "propose-decomposition",
                                            "init-routeb-external", "refresh-routeb-external", "run-external-gate",
                                            "prepare-agents", "dry-run-repair", "pending-agents", "bind-agent", "renew-agent", "reclaim-agent", "record-agent", "compile-agent", "retry-compile-agent", "collect-compile", "check-sketch", "next-actions", "ingest-agent-log", "persist-callback", "run-codex-agent", "run-codex-agents", "host-cycle", "export-plan-store"])
    parser.add_argument("state")
    parser.add_argument('--project')
    parser.add_argument('--comparator-executable')
    parser.add_argument('--node-projects', help='trusted JSON mapping of every node ID to its isolated verification project')
    parser.add_argument('--max-steps', type=int, default=100)
    parser.add_argument('--max-repair-rounds', type=int, default=3)
    parser.add_argument('--limit', type=int, default=4)
    parser.add_argument('--math-lane-policy', choices=['ordinary', 'formalizable'],
                        default='ordinary')
    parser.add_argument('--lease-seconds', type=int, default=3600)
    parser.add_argument('--request-id')
    parser.add_argument('--agent-id')
    parser.add_argument('--result-file')
    parser.add_argument('--source')
    parser.add_argument('--parent-id')
    parser.add_argument('--challenge-module', default='Challenge')
    parser.add_argument('--reduction-module', default='Reduction')
    parser.add_argument('--reduction-name')
    parser.add_argument('--obligation-module', action='append', default=[])
    parser.add_argument('--callback-dir', help='directory of host callback envelopes')
    parser.add_argument('--dispatch-file', help='durable agent_dispatch envelope for run-codex-agent')
    parser.add_argument('--dispatch-dir', help='directory of durable agent_dispatch envelopes for run-codex-agents')
    parser.add_argument('--project-map', help='JSON mapping request_id to assigned project for run-codex-agents')
    parser.add_argument('--max-workers', type=int, default=2)
    parser.add_argument('--codex-executable', default='codex')
    parser.add_argument('--sandbox', default='workspace-write')
    parser.add_argument('--timeout-seconds', type=int)
    parser.add_argument('--output-dir', help='durable raw Codex run directory')
    parser.add_argument('--manifest', help='portable verification manifest')
    parser.add_argument('--sketch', help='proof sketch for propose-decomposition')
    parser.add_argument('--children-file', help='JSON array of child theorem objects')
    parser.add_argument('--dependency-project', help='pinned dependency checkout for verify-manifest')
    parser.add_argument('--bundle-root', help='content-addressed bundle cache; defaults to manifest verification.bundle_root')
    parser.add_argument('--comparator-tools', help='upstream comparator tool directory for verify-manifest')
    parser.add_argument('--target-root', help='external research project root for intake/gates')
    parser.add_argument('--node-name', help='external DAG node name for run-external-gate')
    parser.add_argument('--gate-command', action='append', help='one token of an external gate command; repeat for argv')
    args = parser.parse_args()
    store = StateStore(args.state)
    if args.command == 'init-manifest':
        if not args.manifest:
            parser.error('init-manifest requires --manifest')
        manifest = load_verification_manifest(args.manifest)
        if store.path.resolve() != manifest.state_path.resolve():
            parser.error('init-manifest state must match manifest state_path')
        state = initialize_state_from_manifest(manifest, store)
        print(json.dumps({'state': str(store.path), 'root_id': state.root_id,
                          'nodes': len(state.nodes), 'frontier': [n.name for n in state.frontier()]},
                         ensure_ascii=False, indent=2))
        return
    if args.command == 'init-routeb-external':
        if not args.target_root:
            parser.error('init-routeb-external requires --target-root')
        state = initialize_routeb_intake(args.target_root, store)
        print(json.dumps({'state': str(store.path), 'root_id': state.root_id,
                          'nodes': len(state.nodes),
                          'frontier': [n.name for n in state.frontier()],
                          'registry': len(state.registry),
                          'verification_domain': 'external-research'},
                         ensure_ascii=False, indent=2))
        return
    if args.command == 'propose-decomposition':
        if not args.parent_id or not args.agent_id or not args.sketch or not args.children_file:
            parser.error('propose-decomposition requires --parent-id, --agent-id, --sketch and --children-file')
        raw_children = json.loads(Path(args.children_file).read_text(encoding='utf-8'))
        if not isinstance(raw_children, list):
            parser.error('children-file must contain a JSON array')
        children = []
        for child in raw_children:
            if not isinstance(child, dict) or not isinstance(child.get('name'), str) \
                    or not isinstance(child.get('statement'), str):
                parser.error('each child requires name and statement')
            children.append(ChildGoal(child['name'], child['statement'], child.get('proof_sketch', '')))
        state = store.load()
        child_ids = propose_decomposition(state, args.parent_id, args.sketch, children,
                                          agent_id=args.agent_id, store=store)
        print(json.dumps({'child_ids': child_ids}, ensure_ascii=False, indent=2))
        return
    if not store.path.is_file():
        parser.error('research state does not exist')
    if args.command == 'refresh-routeb-external':
        print(json.dumps(refresh_routeb_tracking(store), ensure_ascii=False, indent=2))
        return
    if args.command == 'run-external-gate':
        if not args.node_name:
            parser.error('run-external-gate requires --node-name')
        result = run_external_gate(store, args.node_name,
                                    command=args.gate_command or None,
                                    cwd=args.target_root, agent_id=args.agent_id or 'external-coordinator',
                                    timeout_seconds=args.timeout_seconds)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result['status'] == 'evidence_complete' else 1
    if args.command == 'ingest-agent-log':
        if not args.request_id or not args.result_file:
            parser.error('ingest-agent-log requires request-id and result-file')
        ingest_compile_log(store, args.request_id, args.result_file)
        return
    if args.command == 'next-actions':
        print(json.dumps(next_actions(store), ensure_ascii=False, indent=2))
        return
    if args.command == 'host-cycle':
        comparator_command = None
        if args.comparator_executable:
            comparator_command = ['lake', 'env', args.comparator_executable, 'comparator.json']
        trusted_project_map = None
        if args.project_map:
            trusted_project_map = json.loads(Path(args.project_map).read_text(encoding='utf-8'))
            if not isinstance(trusted_project_map, dict):
                parser.error('project-map must contain a JSON object')
        print(json.dumps(run_host_cycle(store, callback_dir=args.callback_dir, limit=args.limit,
                                        manifest=args.manifest,
                                        math_lane_policy=args.math_lane_policy,
                                        comparator_command=comparator_command,
                                        trusted_project_map=trusted_project_map),
                         ensure_ascii=False, indent=2))
        return
    if args.command == 'persist-callback':
        if not args.result_file or not args.callback_dir:
            parser.error('persist-callback requires result-file and callback-dir')
        callback_path = Path(args.result_file)
        envelope = json.loads(callback_path.read_text(encoding='utf-8'))
        adapter = FilesystemHostAdapter(Path(args.callback_dir).resolve().parent,
                                        store=store, callback_inbox=args.callback_dir)
        print(adapter.write_callback(envelope))
        return
    if args.command == 'run-codex-agent':
        if not args.dispatch_file or not args.callback_dir or not args.project:
            parser.error('run-codex-agent requires --dispatch-file, --callback-dir and --project')
        result = run_codex_dispatch(
            store, args.dispatch_file, args.callback_dir, project=args.project,
            codex_executable=args.codex_executable, sandbox=args.sandbox,
            lease_seconds=args.lease_seconds, timeout_seconds=args.timeout_seconds,
            output_dir=args.output_dir)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result['exit_code'] == 0 and result['structured'] else 1
    if args.command == 'run-codex-agents':
        if not args.dispatch_dir or not args.callback_dir:
            parser.error('run-codex-agents requires --dispatch-dir and --callback-dir')
        project_map = None
        if args.project_map:
            project_map = json.loads(Path(args.project_map).read_text(encoding='utf-8'))
            if not isinstance(project_map, dict):
                parser.error('project-map must contain a JSON object')
        inferred_project = None
        if args.project is None and not project_map:
            inferred_project = infer_manifest_project(store)
            if inferred_project is None:
                parser.error('run-codex-agents requires --project, --project-map, or a bound manifest project')
        results = run_codex_batch(
            store, args.dispatch_dir, args.callback_dir, project=args.project or inferred_project,
            project_map=project_map, limit=args.limit, max_workers=args.max_workers,
            codex_executable=args.codex_executable, sandbox=args.sandbox,
            lease_seconds=args.lease_seconds, timeout_seconds=args.timeout_seconds,
            output_dir=args.output_dir)
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return 0 if all(item.get('exit_code') == 0 and item.get('structured') for item in results) else 1
    if args.command == 'check-sketch':
        if not args.project or not args.parent_id or not args.reduction_name:
            parser.error('check-sketch requires project, parent-id and reduction-name')
        accepted = check_sketch(store, args.parent_id, args.project,
            challenge_module=args.challenge_module, reduction_module=args.reduction_module,
            reduction_name=args.reduction_name, obligation_modules=args.obligation_module)
        print('sketch_checked' if accepted else 'sketch_rejected')
        return 0 if accepted else 1
    if args.command == 'collect-compile':
        if not args.request_id:
            parser.error('collect-compile requires request-id')
        result = collect_candidate(store, args.request_id)
        print('awaiting_receipt' if result is None else ('compiled' if result else 'needs_repair'))
        return 2 if result is None else (0 if result else 1)
    if args.command == 'compile-agent':
        if not args.request_id or not args.project or not args.source:
            parser.error('compile-agent requires request-id, project and source')
        accepted = check_candidate(store, args.request_id, args.project, args.source)
        print('compiled' if accepted else 'needs_repair')
        return 0 if accepted else 1
    if args.command == 'retry-compile-agent':
        if not args.request_id:
            parser.error('retry-compile-agent requires request-id')
        process = retry_candidate(store, args.request_id, args.project, args.source)
        print(json.dumps({'pid': process.pid, 'request_id': args.request_id}, ensure_ascii=False))
        return
    if args.command == 'prepare-agents':
        print(json.dumps(prepare_requests(store, limit=args.limit,
                                          math_lane_policy=args.math_lane_policy),
                         ensure_ascii=False, indent=2))
        return
    if args.command == 'dry-run-repair':
        print(json.dumps(dry_run_repair_integration(
            store.load(), max_repair_rounds=args.max_repair_rounds), ensure_ascii=False, indent=2))
        return
    if args.command in {'bind-agent', 'record-agent'}:
        if not args.request_id or not args.agent_id:
            parser.error('request-id and agent-id required')
        if args.command == 'bind-agent':
            bind_agent(store, args.request_id, args.agent_id, lease_seconds=args.lease_seconds)
        else:
            if not args.result_file:
                parser.error('record-agent requires the raw terminal tool result file')
            record_result(store, args.request_id, args.agent_id,
                          json.loads(Path(args.result_file).read_text(encoding='utf-8')))
        return
    if args.command == 'renew-agent':
        if not args.request_id or not args.agent_id:
            parser.error('renew-agent requires request-id and agent-id')
        renew_agent(store, args.request_id, args.agent_id, lease_seconds=args.lease_seconds)
        return
    if args.command == 'reclaim-agent':
        if not args.request_id:
            parser.error('reclaim-agent requires request-id')
        reclaim_expired_agent(store, args.request_id)
        return
    if args.command == 'verify-frontier':
        if not args.project or not args.comparator_executable:
            parser.error('verify-frontier requires --project and --comparator-executable')
        outcome = verify_frontier(store, args.project,
            ['lake', 'env', args.comparator_executable, 'comparator.json'], max_steps=args.max_steps,
            node_projects=json.loads(Path(args.node_projects).read_text(encoding='utf-8'))
                if args.node_projects else None)
        print(outcome)
        return 0 if outcome == 'verified' else 1
    if args.command == 'verify-manifest':
        if not args.manifest or not args.dependency_project:
            parser.error('verify-manifest requires --manifest and --dependency-project')
        manifest = load_verification_manifest(args.manifest)
        bundle_value = args.bundle_root or manifest.verification.get('bundle_root')
        if not isinstance(bundle_value, str) or not bundle_value.strip():
            parser.error('verify-manifest requires --bundle-root or verification.bundle_root')
        bundle_root = Path(bundle_value)
        if not bundle_root.is_absolute():
            bundle_root = manifest.path.parent / bundle_root
        if args.comparator_executable:
            comparator_command = ['lake', 'env', args.comparator_executable, 'comparator.json']
        elif args.comparator_tools:
            tools = Path(args.comparator_tools)
            comparator_command = ['lake', 'env', str(tools / 'comparator/.lake/build/bin/comparator'),
                                  'comparator.json']
        else:
            parser.error('verify-manifest requires --comparator-executable or --comparator-tools')
        outcome = verify_manifest_frontier(
            store, manifest.path, args.dependency_project, bundle_root,
            comparator_command, max_steps=args.max_steps)
        print(outcome)
        return 0 if outcome == 'verified' else 1
    state = store.load()
    if args.command == 'export-plan-store':
        if not args.output_dir:
            parser.error('export-plan-store requires --output-dir')
        paths = export_merlean_plan_views(state, args.output_dir)
        print(json.dumps({name: str(path) for name, path in paths.items()},
                         ensure_ascii=False, indent=2))
        return
    if args.command == 'pending-agents':
        print(json.dumps([r for r in state.agent_requests.values()
                          if r['status'] in {'awaiting_dispatch', 'bound', 'checking'}],
                         ensure_ascii=False, indent=2))
        return
    if args.command == 'audit-registry':
        print(json.dumps(audit_registry(state), indent=2))
        return
    print(f"project={state.project} nodes={len(state.nodes)} registry={len(state.registry)}")
    for node in state.nodes.values():
        print(f"{node.status.value:12} {node.name} ({node.id})")
    print("frontier=" + ",".join(n.name for n in state.frontier()))


if __name__ == "__main__":
    raise SystemExit(main())
