import json
import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from unittest.mock import patch

from percolation_workflow.agent_bridge import bind_agent, prepare_requests, reclaim_dead_codex
from percolation_workflow.codex_adapter import (_codex_events, _run_codex_process,
                                                 _structured_message, discover_candidate,
                                                 discover_candidate_bundle,
                                                 infer_manifest_project,
                                                 run_codex_batch, run_codex_dispatch)
from percolation_workflow.host_adapter import FilesystemHostAdapter
from percolation_workflow.model import WorkflowState
from percolation_workflow.store import StateStore


class CodexAdapterTests(unittest.TestCase):
    def test_dead_codex_start_marker_is_reclaimed_before_lease_expiry(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            store = StateStore(root / 'state.json')
            state = WorkflowState()
            state.add_node('goal', 'theorem goal : True', metadata={'statement_status': 'indexed'})
            store.save(state)
            request = prepare_requests(store)[0]
            run_dir = root / 'codex-runs' / request['request_id'] / request['attempt_id']
            bind_agent(store, request['request_id'], 'codex-agent', host_run_dir=str(run_dir),
                       lease_seconds=3600)
            run_dir.mkdir(parents=True)
            (run_dir / 'started.json').write_text(json.dumps({
                'schema_version': 1, 'request_id': request['request_id'],
                'attempt_id': request['attempt_id'], 'agent_id': 'codex-agent',
                'pid': 2147483647,
            }), encoding='utf-8')
            self.assertTrue(reclaim_dead_codex(store, request['request_id']))
            recovered = store.load()
            self.assertEqual(recovered.agent_requests[request['request_id']]['status'], 'expired')
            self.assertEqual(recovered.attempts[request['attempt_id']].status, 'agent_timeout')

    def test_manifest_project_is_discovered_only_from_bound_lean_project(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            project = root / 'project'
            project.mkdir()
            manifest = project / 'verification-manifest.json'
            manifest.write_text('{}', encoding='utf-8')
            (project / 'lakefile.toml').write_text('name = "test"\n', encoding='utf-8')
            (project / 'lean-toolchain').write_text('leanprover/lean4:v4.32.0\n', encoding='utf-8')
            store = StateStore(root / 'state.json')
            state = WorkflowState()
            state.manifest = {'path': 'project/verification-manifest.json',
                              'sha256': hashlib.sha256(manifest.read_bytes()).hexdigest()}
            store.save(state)
            self.assertEqual(infer_manifest_project(store), project.resolve())
            state.manifest = {'path': 'project/verification-manifest.json', 'sha256': 'a' * 64}
            store.save(state)
            self.assertIsNone(infer_manifest_project(store))

    def test_batch_binds_serially_and_runs_two_callbacks(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            project = root / 'project'
            project.mkdir()
            for name in ('CandidateA.lean', 'CandidateB.lean'):
                (project / name).write_text('theorem goal : True := by trivial\n', encoding='utf-8')
            store = StateStore(root / 'state.json')
            state = WorkflowState()
            state.add_node('goal-a', 'theorem goal : True', metadata={'statement_status': 'indexed'})
            state.add_node('goal-b', 'theorem goal : True', metadata={'statement_status': 'indexed'})
            store.save(state)
            adapter = FilesystemHostAdapter(root, store=store)
            dispatches = adapter.dispatch()
            self.assertEqual(len(dispatches), 2)
            active = 0
            maximum = 0
            lock = __import__('threading').Lock()
            both_running = threading.Barrier(2, timeout=15)

            def fake_run(command, selected, saved_store, request_id, agent_id, lease_seconds, timeout_seconds, **kwargs):
                nonlocal active, maximum
                with lock:
                    active += 1
                    maximum = max(maximum, active)
                try:
                    source = 'CandidateA.lean' if request_id == dispatches[0]['request_id'] else 'CandidateB.lean'
                    output_path = Path(command[command.index('-o') + 1])
                    output_path.write_text(json.dumps({'candidate': {
                        'project': str(selected), 'source': str(selected / source)},
                        'decomposition': None, 'error': None}), encoding='utf-8')
                    # Require actual overlap without assuming the second worker
                    # completes Windows file/lock setup within 200 milliseconds.
                    both_running.wait()
                    return (0, '{"type":"thread.started","thread_id":"%s"}\n{"type":"turn.completed"}\n' % request_id, '', False, 0)
                finally:
                    with lock:
                        active -= 1

            with patch('percolation_workflow.codex_adapter._run_codex_process', side_effect=fake_run):
                results = run_codex_batch(store, root / 'dispatch', root / 'callbacks',
                                          project=project, max_workers=2)
            self.assertEqual(len(results), 2)
            self.assertTrue(all(item['structured'] for item in results))
            self.assertEqual(maximum, 2)
            self.assertEqual(len(list((root / 'callbacks').glob('*.json'))), 2)

    def test_process_supervisor_renews_lease_before_completion(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)

            class Process:
                returncode = 0

                def __init__(self):
                    self.waits = 0

                def wait(self, timeout=None):
                    self.waits += 1
                    if self.waits == 1:
                        raise subprocess.TimeoutExpired('codex', timeout)
                    return 0

                def communicate(self):
                    return b'out', b'err'

            process = Process()
            store = StateStore(project / 'state.json')
            with patch('percolation_workflow.codex_adapter.subprocess.Popen', return_value=process), \
                 patch('percolation_workflow.codex_adapter.renew_agent') as renew:
                result = _run_codex_process(['codex'], project, store, 'request', 'agent', 3, 10)
            self.assertEqual(result, (0, b'out', b'err', False, 1))
            renew.assert_called_once_with(store, 'request', 'agent', lease_seconds=3)

    def test_process_supervisor_persists_start_and_finish_markers(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            marker_dir = project / 'run'
            marker_dir.mkdir()

            class Process:
                pid = 43210
                returncode = 0
                def wait(self, timeout=None):
                    return 0
                def communicate(self):
                    return b'out', b''

            store = StateStore(project / 'state.json')
            with patch('percolation_workflow.codex_adapter.subprocess.Popen', return_value=Process()):
                result = _run_codex_process(
                    ['codex'], project, store, 'request', 'agent', 30, 10,
                    started_marker=marker_dir / 'started.json',
                    finished_marker=marker_dir / 'finished.json')
            self.assertEqual(result[0], 0)
            started = json.loads((marker_dir / 'started.json').read_text(encoding='utf-8'))
            finished = json.loads((marker_dir / 'finished.json').read_text(encoding='utf-8'))
            self.assertEqual(started['pid'], 43210)
            self.assertEqual(started['request_id'], 'request')
            self.assertEqual(finished['exit_code'], 0)

    def test_process_supervisor_journals_stdout_before_process_finishes(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            transcript = project / 'run' / 'stdout.jsonl'
            stderr = project / 'run' / 'stderr.txt'
            store = StateStore(project / 'state.json')
            result_holder = []

            def run_process():
                result_holder.append(_run_codex_process(
                    [sys.executable, '-c',
                     'import time; print("first", flush=True); time.sleep(3.0); print("second", flush=True)'],
                    project, store, 'request', 'agent', 30, 10,
                    transcript_path=transcript, stderr_path=stderr))

            with patch('percolation_workflow.codex_adapter.renew_agent'):
                worker = threading.Thread(target=run_process)
                worker.start()
                deadline = time.monotonic() + 5
                while (not transcript.is_file() or 'first' not in transcript.read_text(encoding='utf-8')):
                    if time.monotonic() >= deadline:
                        self.fail('stdout journal was not durable before process completion')
                    time.sleep(0.02)
                self.assertTrue(worker.is_alive())
                worker.join(timeout=8)
            self.assertFalse(worker.is_alive())
            self.assertEqual(result_holder[0][0], 0)
            self.assertEqual(transcript.read_text(encoding='utf-8'), 'first\nsecond\n')
            self.assertEqual(stderr.read_text(encoding='utf-8'), '')

    def test_structured_message_accepts_json_fence_and_rejects_prose(self):
        self.assertEqual(_structured_message('```json\n{"candidate": {}}\n```'), {'candidate': {}})
        self.assertIsNone(_structured_message('proof completed, see the file'))
        thread, terminal, events = _codex_events(
            '{"type":"thread.started","thread_id":"t-1"}\n{"type":"turn.completed"}\nnoise')
        self.assertEqual(thread, 't-1')
        self.assertTrue(terminal)
        self.assertEqual(len(events), 2)

    def test_live_cli_run_persists_raw_run_and_callback(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            project = root / 'project'
            project.mkdir()
            (project / 'Candidate.lean').write_text('theorem goal : True := by trivial\n', encoding='utf-8')
            store = StateStore(root / 'state.json')
            state = WorkflowState()
            state.add_node('goal', 'theorem goal : True', metadata={'statement_status': 'indexed'})
            store.save(state)
            request = prepare_requests(store)[0]
            dispatch = FilesystemHostAdapter(root, store=store).persist_dispatch(
                [{'kind': 'dispatch_agent', 'request_id': request['request_id'],
                  'node_id': request['node_id'], 'agent_id': None}],
                {request['request_id']: request})[0]
            dispatch_path = root / 'dispatch' / f"{request['request_id']}.json"
            callback_dir = root / 'callbacks'
            callback_dir.mkdir()
            final = {'candidate': {'project': str(project), 'source': str(project / 'Candidate.lean')}}

            def fake_run(command, project, store, request_id, agent_id, lease_seconds, timeout_seconds, **kwargs):
                output_path = Path(command[command.index('-o') + 1])
                output_path.write_text(json.dumps(final), encoding='utf-8')
                return (0, ('{"type":"thread.started","thread_id":"thread-1"}\n'
                            '{"type":"turn.completed"}\n'), '', False, 0)

            with patch('percolation_workflow.codex_adapter._run_codex_process', side_effect=fake_run):
                result = run_codex_dispatch(store, dispatch_path, callback_dir, project=project)
            self.assertTrue(result['structured'])
            self.assertEqual(result['provider_thread_id'], 'thread-1')
            saved_callback = json.loads(Path(result['callback']).read_text(encoding='utf-8'))
            self.assertEqual(saved_callback['candidate'], final['candidate'])
            self.assertTrue(Path(result['run_dir'], 'stdout.jsonl').is_file())
            self.assertEqual(saved_callback['payload']['host_execution']['stdout_bytes'],
                             len('{"type":"thread.started","thread_id":"thread-1"}\n{"type":"turn.completed"}\n'.encode('utf-8')))
            self.assertEqual(store.load().agent_requests[request['request_id']]['agent_id'], result['agent_id'])

    def test_auto_candidate_source_is_discovered_from_changed_lean_file(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            project = root / 'project'
            project.mkdir()
            source = project / 'Candidate.lean'
            source.write_text('theorem goal : True := by trivial\n', encoding='utf-8')
            store = StateStore(root / 'state.json')
            state = WorkflowState()
            state.add_node('goal', 'theorem goal : True', metadata={'statement_status': 'indexed'})
            store.save(state)
            request = prepare_requests(store)[0]
            dispatch = FilesystemHostAdapter(root, store=store).persist_dispatch(
                [{'kind': 'dispatch_agent', 'request_id': request['request_id'],
                  'node_id': request['node_id'], 'agent_id': None}],
                {request['request_id']: request})[0]
            dispatch_path = root / 'dispatch' / f"{request['request_id']}.json"
            callback_dir = root / 'callbacks'
            callback_dir.mkdir()

            def fake_run(command, selected, saved_store, request_id, agent_id, lease_seconds, timeout_seconds, **kwargs):
                source.write_text('theorem goal : True := by exact True.intro\n', encoding='utf-8')
                Path(command[command.index('-o') + 1]).write_text(json.dumps({
                    'candidate': {'project': str(project), 'source': 'AUTO'},
                    'decomposition': None, 'error': None}), encoding='utf-8')
                return (0, '{"type":"thread.started","thread_id":"thread-auto"}\n'
                           '{"type":"turn.completed"}\n', '', False, 0)

            with patch('percolation_workflow.codex_adapter._run_codex_process', side_effect=fake_run):
                result = run_codex_dispatch(store, dispatch_path, callback_dir, project=project)
            callback = json.loads(Path(result['callback']).read_text(encoding='utf-8'))
            self.assertEqual(Path(callback['candidate']['source']).resolve(), source.resolve())
            self.assertEqual(callback['host_metadata']['candidate_discovery'], 'changed-lean-bundle')

    def test_auto_candidate_source_discovers_conventional_entrypoint_with_support_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            project = root / 'project'
            project.mkdir()
            entrypoint = project / 'Solution.lean'
            helper = project / 'Support.lean'
            entrypoint.write_text('import Support\ntheorem goal : True := by\n  exact support\n', encoding='utf-8')
            helper.write_text('theorem support : True := by trivial\n', encoding='utf-8')
            before = {path.relative_to(project).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
                      for path in (entrypoint, helper)}
            entrypoint.write_text('import Support\ntheorem goal : True := by exact support\n', encoding='utf-8')
            helper.write_text('theorem support : True := by exact True.intro\n', encoding='utf-8')
            bundle = discover_candidate_bundle(project, before)
            self.assertEqual(bundle['entrypoint'].resolve(), entrypoint.resolve())
            self.assertEqual([path.name for path in bundle['sources']], ['Solution.lean', 'Support.lean'])

            store = StateStore(root / 'state.json')
            state = WorkflowState()
            state.add_node('goal', 'theorem goal : True', metadata={'statement_status': 'indexed'})
            store.save(state)
            request = prepare_requests(store)[0]
            dispatch = FilesystemHostAdapter(root, store=store).persist_dispatch(
                [{'kind': 'dispatch_agent', 'request_id': request['request_id'],
                  'node_id': request['node_id'], 'agent_id': None}],
                {request['request_id']: request})[0]
            dispatch_path = root / 'dispatch' / f"{request['request_id']}.json"
            callback_dir = root / 'callbacks'
            callback_dir.mkdir()

            def fake_run(command, selected, saved_store, request_id, agent_id, lease_seconds, timeout_seconds, **kwargs):
                entrypoint.write_text('import Support\ntheorem goal : True := by\n  exact support\n', encoding='utf-8')
                helper.write_text('theorem support : True := by trivial\n', encoding='utf-8')
                Path(command[command.index('-o') + 1]).write_text(json.dumps({
                    'candidate': {'project': str(project), 'source': 'AUTO'},
                    'decomposition': None, 'error': None}), encoding='utf-8')
                return (0, '{"type":"thread.started","thread_id":"thread-bundle"}\n'
                           '{"type":"turn.completed"}\n', '', False, 0)

            with patch('percolation_workflow.codex_adapter._run_codex_process', side_effect=fake_run):
                result = run_codex_dispatch(store, dispatch_path, callback_dir, project=project)
            callback = json.loads(Path(result['callback']).read_text(encoding='utf-8'))
            self.assertEqual(Path(callback['candidate']['source']).resolve(), entrypoint.resolve())
            self.assertEqual([Path(value).name for value in callback['candidate']['sources']],
                             ['Solution.lean', 'Support.lean'])
            self.assertEqual(callback['host_metadata']['candidate_discovery'], 'changed-lean-bundle')

    def test_auto_candidate_discovery_rejects_multiple_changed_sources(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            before = {}
            (project / 'a.lean').write_text('a', encoding='utf-8')
            (project / 'b.lean').write_text('b', encoding='utf-8')
            with self.assertRaises(ValueError):
                discover_candidate(project, before)

    def test_successful_prose_is_agent_error_not_candidate(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            project = root / 'project'
            project.mkdir()
            store = StateStore(root / 'state.json')
            state = WorkflowState()
            state.add_node('goal', 'theorem goal : True', metadata={'statement_status': 'indexed'})
            store.save(state)
            request = prepare_requests(store)[0]
            dispatch = FilesystemHostAdapter(root, store=store).persist_dispatch(
                [{'kind': 'dispatch_agent', 'request_id': request['request_id'],
                  'node_id': request['node_id'], 'agent_id': None}],
                {request['request_id']: request})[0]
            dispatch_path = root / 'dispatch' / f"{request['request_id']}.json"
            callback_dir = root / 'callbacks'
            callback_dir.mkdir()

            def fake_run(command, project, store, request_id, agent_id, lease_seconds, timeout_seconds, **kwargs):
                Path(command[command.index('-o') + 1]).write_text('done', encoding='utf-8')
                return (0, '{"type":"thread.started","thread_id":"thread-2"}\n{"type":"turn.completed"}\n', '', False, 0)

            with patch('percolation_workflow.codex_adapter._run_codex_process', side_effect=fake_run):
                result = run_codex_dispatch(store, dispatch_path, callback_dir, project=project)
            self.assertFalse(result['structured'])
            callback = json.loads(Path(result['callback']).read_text(encoding='utf-8'))
            self.assertIn('errored', callback['payload']['status'][result['agent_id']])


if __name__ == '__main__':
    unittest.main()
