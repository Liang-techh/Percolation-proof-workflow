import tempfile
import unittest
import json
import time
from pathlib import Path
from unittest.mock import patch
from percolation_workflow.agent_bridge import (prepare_requests, bind_agent, record_result,
                                             check_candidate, start_candidate, collect_candidate,
                                             retry_candidate,
                                             ingest_compile_log, renew_agent, reclaim_expired_agent,
                                             reclaim_dead_compile)
from percolation_workflow.model import NodeStatus, WorkflowState
from percolation_workflow.store import StateStore
from percolation_workflow.research import next_actions


class BridgeTests(unittest.TestCase):
    def test_prepare_requests_uses_obstruction_aware_dispatch_policy(self):
        with tempfile.TemporaryDirectory() as directory:
            store = StateStore(Path(directory) / 'state.json')
            state = WorkflowState()
            blocked = state.add_node(
                'blocked', 'theorem blocked : True',
                metadata={'statement_status': 'indexed', 'status': 'open_compile_blocked'})
            runnable = state.add_node(
                'runnable', 'theorem runnable : True',
                metadata={'statement_status': 'indexed'})
            store.save(state)

            requests = prepare_requests(store, limit=4)

            self.assertEqual([request['node_id'] for request in requests], [runnable])
            self.assertEqual(requests[0]['scheduler']['obstruction_rank'], 0)
            self.assertNotIn(blocked, [request['node_id'] for request in requests])

    def test_prepare_requests_admits_explicit_formalization_target_leaf(self):
        with tempfile.TemporaryDirectory() as directory:
            store = StateStore(Path(directory) / 'state.json')
            state = WorkflowState()
            node_id = state.add_node(
                'typed-source-leaf', 'theorem typed_source_leaf : True',
                metadata={
                    'statement_status': 'formalization_target',
                    'math_lane': 'source_semantics',
                    'frontier_repair_contract': {'next_agent_action': 'build adapter'},
                })
            store.save(state)

            requests = prepare_requests(store, limit=1)

            self.assertEqual([request['node_id'] for request in requests], [node_id])
            self.assertEqual(requests[0]['frontier_repair_contract']['next_agent_action'],
                             'build adapter')

    def test_prepare_requests_carries_virtual_frontier_as_advisory_context(self):
        with tempfile.TemporaryDirectory() as directory:
            store = StateStore(Path(directory) / 'state.json')
            state = WorkflowState()
            node_id = state.add_node(
                'O2 evaluator', 'theorem o2 : True',
                metadata={
                    'statement_status': 'formalization_target',
                    'math_lane': 'source_semantics',
                    'frontier_repair_contract': {'next_agent_action': 'bind O2'},
                    'o2_trig_binding': {
                        'leaves': [{
                            'id': 'T-P4-036.3',
                            'kind': 'float64_libm_sin_cos_enclosure',
                            'status': 'OPEN',
                        }],
                    },
                })
            before_nodes = len(state.nodes)
            store.save(state)

            request = prepare_requests(store, limit=1)[0]

            self.assertEqual(request['node_id'], node_id)
            self.assertEqual(request['virtual_frontier'][0]['virtual_leaf_id'],
                             'T-P4-036.3')
            self.assertTrue(request['virtual_frontier'][0]['is_virtual'])
            self.assertFalse(request['virtual_frontier'][0]['closure_effect'])
            saved = store.load()
            self.assertEqual(len(saved.nodes), before_nodes)

    def test_prepare_requests_preserves_cross_branch_input_contract(self):
        with tempfile.TemporaryDirectory() as directory:
            store = StateStore(Path(directory) / 'state.json')
            state = WorkflowState()
            input_id = state.add_node('closed-input', 'theorem input : True')
            state.nodes[input_id].status = NodeStatus.VERIFIED
            state.registry[input_id] = {'node_id': input_id, 'artifact': 'input.lean'}
            consumer_id = state.add_node(
                'consumer', 'theorem consumer : True',
                metadata={'statement_status': 'indexed',
                          'required_node_ids': [input_id]})
            store.save(state)

            with patch('percolation_workflow.agent_bridge.audit_registry',
                       return_value={input_id: {'status': 'current'}}):
                requests = prepare_requests(store, limit=4)

            self.assertEqual([request['node_id'] for request in requests], [consumer_id])
            self.assertEqual(requests[0]['required_node_ids'], [input_id])
            self.assertEqual(requests[0]['required_inputs'][input_id]['artifact'], 'input.lean')

    def test_prepare_requests_can_opt_into_formalizable_math_lanes(self):
        with tempfile.TemporaryDirectory() as directory:
            store = StateStore(Path(directory) / 'state.json')
            state = WorkflowState()
            numeric = state.add_node(
                'numeric', 'theorem numeric : True',
                metadata={'statement_status': 'indexed', 'math_lane': 'numerical_blocker'})
            lean = state.add_node(
                'lean', 'theorem lean : True',
                metadata={'statement_status': 'indexed', 'math_lane': 'lean_adapter'})
            store.save(state)

            requests = prepare_requests(store, limit=4, math_lane_policy='formalizable')

            self.assertEqual([request['node_id'] for request in requests], [lean])
            self.assertEqual(requests[0]['scheduler']['math_lane_policy'], 'formalizable')
            self.assertNotIn(numeric, [request['node_id'] for request in requests])

    def test_prepare_requests_deduplicates_explicit_candidate_identity(self):
        with tempfile.TemporaryDirectory() as directory:
            store = StateStore(Path(directory) / 'state.json')
            state = WorkflowState()
            first = state.add_node(
                'first', 'theorem first : True',
                metadata={'statement_status': 'indexed', 'candidate_digest': 'same'})
            second = state.add_node(
                'second', 'theorem second : True',
                metadata={'statement_status': 'indexed', 'candidate_digest': 'same'})
            store.save(state)

            requests = prepare_requests(store, limit=4)

            self.assertEqual(len(requests), 1)
            self.assertIn(requests[0]['node_id'], {first, second})
            self.assertEqual(requests[0]['scheduler']['candidate_identity'], 'same')

    def test_agent_lease_renewal_and_explicit_reclaim_reopens_frontier(self):
        with tempfile.TemporaryDirectory() as directory:
            store = StateStore(Path(directory) / 'state.json')
            state = WorkflowState()
            node_id = state.add_node('goal', 'theorem goal : True',
                                     metadata={'statement_status': 'indexed'})
            store.save(state)
            request_id = prepare_requests(store)[0]['request_id']
            bind_agent(store, request_id, 'lease-agent', lease_seconds=1)
            self.assertEqual(next_actions(store)[0]['kind'], 'observe_agent')
            renew_agent(store, request_id, 'lease-agent', lease_seconds=2)
            self.assertEqual(next_actions(store)[0]['kind'], 'observe_agent')
            time.sleep(2.1)
            self.assertEqual(next_actions(store)[0]['kind'], 'reclaim_expired_agent')
            with self.assertRaisesRegex(ValueError, 'lease has expired'):
                record_result(store, request_id, 'lease-agent',
                              {'status': {'lease-agent': {'completed': 'late callback'}}})
            with self.assertRaisesRegex(ValueError, 'expired'):
                renew_agent(store, request_id, 'lease-agent')
            reclaim_expired_agent(store, request_id)
            saved = store.load()
            self.assertEqual(saved.nodes[node_id].status, 'open')
            self.assertEqual(saved.agent_requests[request_id]['status'], 'expired')
            attempt = saved.attempts[saved.agent_requests[request_id]['attempt_id']]
            self.assertEqual(attempt.status, 'agent_timeout')
            repair = prepare_requests(store)[0]
            self.assertIn('host-agent lease expired', str(repair['diagnostics']))

    def test_live_diagnostics_do_not_finish_agent_or_verify_node(self):
        with tempfile.TemporaryDirectory() as directory:
            store = StateStore(Path(directory) / 'state.json')
            state = WorkflowState()
            node = state.add_node('goal', 'theorem goal : True', metadata={'statement_status': 'indexed'})
            store.save(state)
            request = prepare_requests(store)[0]['request_id']
            bind_agent(store, request, 'fixture-agent')
            path = Path(directory) / 'compile.json'
            report = {'request_id': request, 'command': ['lake', 'env', 'lean', 'Candidate.lean'],
                      'stdout': 'actual diagnostic fixture', 'stderr': '', 'exit_code': 1}
            path.write_text(json.dumps(report), encoding='utf-8')
            ingest_compile_log(store, request, path)
            before = store.path.read_bytes()
            ingest_compile_log(store, request, path)
            self.assertEqual(before, store.path.read_bytes())
            saved = store.load()
            self.assertEqual(saved.nodes[node].status, 'in_progress')
            self.assertEqual(saved.agent_requests[request]['status'], 'bound')
            self.assertEqual(saved.registry, {})
            record_result(store, request, 'fixture-agent', {'status': {'fixture-agent': {'errored': 'fixture exit'}}})
            repair = prepare_requests(store)[0]
            self.assertIn('actual diagnostic fixture', str(repair['diagnostics']))
            with self.assertRaisesRegex(ValueError, 'another request'):
                ingest_compile_log(store, repair['request_id'], path)

    def test_worker_receipt_survives_coordinator_reload(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / 'lean-toolchain').write_bytes(
                (Path(__file__).parents[1] / 'examples/minimal_lean/lean-toolchain').read_bytes())
            (project / 'lakefile.toml').write_text('name = "recoveryTest"\n')
            source = project / 'Candidate.lean'
            support = project / 'Support.lean'
            support_base = project / 'SupportBase.lean'
            support_base.write_text('theorem support_base : True := by trivial\n')
            support.write_text('import SupportBase\ntheorem support : True := by exact support_base\n')
            source.write_text('import Support\ntheorem goal : True := by exact support\n')
            store = StateStore(project / 'state.json')
            state = WorkflowState()
            node = state.add_node('goal', 'theorem goal : True', metadata={'statement_status': 'indexed'})
            store.save(state)
            self.assertEqual(next_actions(store)[0]['kind'], 'prepare_agent')
            request = prepare_requests(store)[0]['request_id']
            self.assertEqual(next_actions(store)[0]['kind'], 'dispatch_agent')
            bind_agent(store, request, 'fixture-agent')
            self.assertEqual(next_actions(store)[0]['kind'], 'observe_agent')
            record_result(store, request, 'fixture-agent',
                          {'status': {'fixture-agent': {'completed': 'candidate'}}})
            self.assertEqual(next_actions(store)[0]['kind'], 'compile_candidate')
            process = start_candidate(store, request, project, source, [source, support, support_base])
            try:
                checkpoint = store.load()
                self.assertEqual(checkpoint.agent_requests[request]['status'], 'checking')
                self.assertEqual([Path(value).name for value in
                                 checkpoint.agent_requests[request]['artifact_sources']],
                                 ['Candidate.lean', 'Support.lean', 'SupportBase.lean'])
                job = json.loads((Path(checkpoint.agent_requests[request]['compile_job']) /
                                  'job.json').read_text(encoding='utf-8'))
                self.assertEqual([Path(value).name for value in job['sources']],
                                 ['Candidate.lean', 'Support.lean', 'SupportBase.lean'])
                self.assertEqual([Path(value).name for value in job['compile_sources']],
                                 ['SupportBase.lean', 'Support.lean', 'Candidate.lean'])
                self.assertEqual(next_actions(store)[0]['kind'], 'collect_compile')
                checkpoint.event('unrelated_callback_during_compilation')
                store.save(checkpoint)
                with self.assertRaises(ValueError):
                    start_candidate(store, request, project, source)
                self.assertEqual(process.wait(timeout=60), 0)
                recovered = StateStore(store.path)
                receipt = Path(checkpoint.agent_requests[request]['compile_job']) / 'result.json'
                raw = receipt.read_text(encoding='utf-8')
                receipt.rename(receipt.with_suffix('.held'))
                self.assertIsNone(collect_candidate(recovered, request))
                wrong = json.loads(raw)
                wrong['attempt_id'] = 'different-execution'
                receipt.write_text(json.dumps(wrong), encoding='utf-8')
                with self.assertRaisesRegex(ValueError, 'another execution'):
                    collect_candidate(recovered, request)
                receipt.write_text(raw, encoding='utf-8')
                self.assertTrue(collect_candidate(recovered, request), raw)
                self.assertTrue(collect_candidate(recovered, request))
                self.assertEqual(next_actions(recovered)[0]['kind'], 'verify_candidate')
                saved = recovered.load()
                self.assertEqual(len(saved.attempts), 2)
                self.assertEqual(saved.nodes[node].metadata['evidence_stage'], 'compiled_candidate')
                self.assertTrue(any(e['kind'] == 'unrelated_callback_during_compilation' for e in saved.events))
                self.assertEqual(saved.registry, {})
            finally:
                if process.poll() is None:
                    process.wait(timeout=60)

    def test_superseded_candidate_cannot_start_compilation(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            store = StateStore(project / 'state.json')
            state = WorkflowState()
            node_id = state.add_node('goal', 'theorem goal : True',
                                     metadata={'statement_status': 'indexed'})
            store.save(state)
            request_id = prepare_requests(store)[0]['request_id']
            bind_agent(store, request_id, 'fixture-agent')
            record_result(store, request_id, 'fixture-agent',
                          {'status': {'fixture-agent': {'completed': 'candidate'}}})
            state = store.load()
            later = state.begin_attempt(node_id, 'later-coordinator')
            state.finish_attempt(later, status='compile_error', command=[],
                                 stdout='', stderr='later error', exit_code=1)
            store.save(state)
            before = store.path.read_bytes()
            with self.assertRaisesRegex(ValueError, 'superseded'):
                check_candidate(store, request_id, project, project / 'Candidate.lean')
            self.assertEqual(store.path.read_bytes(), before)

    def test_real_compiler_error_feeds_next_request(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            version = Path(__file__).parents[1] / 'examples/minimal_lean/lean-toolchain'
            (project / 'lean-toolchain').write_bytes(version.read_bytes())
            (project / 'lakefile.toml').write_text('name = "bridgeTest"\n')
            source = project / 'Candidate.lean'
            source.write_text('theorem goal : True := by\n  unknown_bridge_tactic\n')
            state = WorkflowState()
            node = state.add_node('goal', 'theorem goal : True', metadata={'statement_status': 'indexed'})
            store = StateStore(project / 'state.json')
            store.save(state)
            request = prepare_requests(store)[0]
            bind_agent(store, request['request_id'], 'fixture-agent')
            record_result(store, request['request_id'], 'fixture-agent',
                          {'status': {'fixture-agent': {'completed': 'candidate'}}})
            self.assertEqual(prepare_requests(store), [])
            self.assertFalse(check_candidate(store, request['request_id'], project, source))
            repair_request = prepare_requests(store)[0]
            self.assertIn('unknown tactic', str(repair_request['diagnostics']))
            self.assertIn('Candidate.lean:2:3', str(repair_request['diagnostics']))
            self.assertEqual(repair_request['work_kind'], 'repair')
            self.assertEqual(store.load().attempts[repair_request['repair_of_attempt_id']].status,
                             'compile_error')
            self.assertEqual(repair_request['repair_context']['status'], 'compile_error')
            self.assertEqual(store.load().registry, {})
            with self.assertRaisesRegex(ValueError, 'fresh host agent'):
                bind_agent(store, repair_request['request_id'], 'fixture-agent')

    def test_strict_admission_failure_becomes_durable_repair_request(self):
        with tempfile.TemporaryDirectory() as directory:
            store = StateStore(Path(directory) / 'state.json')
            state = WorkflowState()
            node = state.add_node(
                'goal', 'theorem goal : True',
                metadata={'statement_status': 'indexed'})
            attempt = state.begin_attempt(node, 'verification-coordinator', 'Solution.lean')
            state.finish_attempt(
                attempt, status='strict_admission_rejected', command=['checker'],
                stdout='axiom detected', stderr='strict admission failed', exit_code=1)
            store.save(state)

            requests = prepare_requests(store)

            self.assertEqual(len(requests), 1)
            request = requests[0]
            self.assertEqual(request['work_kind'], 'repair')
            self.assertEqual(request['repair_of_attempt_id'], attempt)
            self.assertEqual(request['repair_context']['status'], 'strict_admission_rejected')
            self.assertIn('strict admission failed', request['repair_context']['stderr'])
            checkpoint = store.load()
            self.assertEqual(checkpoint.attempts[attempt].status, 'strict_admission_rejected')
            self.assertEqual(checkpoint.registry, {})

    def test_bundle_compile_error_repair_reuses_all_sources(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / 'lean-toolchain').write_bytes(
                (Path(__file__).parents[1] / 'examples/minimal_lean/lean-toolchain').read_bytes())
            (project / 'lakefile.toml').write_text('name = "bundleRepairTest"\n')
            support = project / 'Support.lean'
            source = project / 'Candidate.lean'
            support.write_text('theorem support : True := by trivial\n')
            source.write_text('import Support\ntheorem goal : True := by unknown_bundle_tactic\n')
            store = StateStore(project / 'state.json')
            state = WorkflowState()
            node = state.add_node('goal', 'theorem goal : True', metadata={'statement_status': 'indexed'})
            store.save(state)
            request = prepare_requests(store)[0]['request_id']
            bind_agent(store, request, 'bundle-agent')
            record_result(store, request, 'bundle-agent',
                          {'status': {'bundle-agent': {'completed': 'bundle candidate'}}})
            first = start_candidate(store, request, project, source, [source, support])
            self.assertEqual(first.wait(timeout=60), 0)
            self.assertFalse(collect_candidate(store, request))
            failed = store.load()
            self.assertEqual(failed.attempts[failed.agent_requests[request]['compile_attempt_id']].status,
                             'compile_error')
            source.write_text('import Support\ntheorem goal : True := by exact support\n')
            second = retry_candidate(store, request)
            self.assertEqual(second.wait(timeout=60), 0)
            self.assertTrue(collect_candidate(store, request))
            repaired = store.load()
            self.assertEqual([Path(value).name for value in repaired.agent_requests[request]['artifact_sources']],
                             ['Candidate.lean', 'Support.lean'])
            self.assertEqual(repaired.nodes[node].status, 'open')

    def test_dead_compiler_worker_is_reclaimed_without_fabricating_receipt(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            store = StateStore(root / 'state.json')
            state = WorkflowState()
            node_id = state.add_node('goal', 'theorem goal : True',
                                     metadata={'statement_status': 'indexed'})
            attempt_id = state.begin_attempt(node_id, 'compiler-coordinator', str(root / 'Candidate.lean'))
            job = root / 'job'
            job.mkdir()
            state.agent_requests['request'] = {
                'request_id': 'request', 'node_id': node_id, 'attempt_id': 'agent-attempt',
                'status': 'checking', 'agent_id': 'agent', 'compile_attempt_id': attempt_id,
                'compile_job': str(job), 'artifact': str(root / 'Candidate.lean')}
            store.save(state)
            (job / 'started.json').write_text(json.dumps({'pid': 424242,
                'attempt_id': attempt_id}), encoding='utf-8')
            with patch('percolation_workflow.agent_bridge._process_alive', return_value=False):
                self.assertTrue(reclaim_dead_compile(store, 'request'))
            saved = store.load()
            self.assertEqual(saved.agent_requests['request']['status'], 'checked')
            self.assertEqual(saved.attempts[attempt_id].status, 'compile_error')
            self.assertEqual(saved.attempts[attempt_id].exit_code, 125)
            self.assertEqual(saved.nodes[node_id].status, 'open')
            self.assertTrue(any(event['kind'] == 'compiler_worker_reclaimed'
                                for event in saved.events))
            self.assertIsNone(reclaim_dead_compile(store, 'request'))

    def test_dead_coordinator_launch_intent_is_reclaimed_before_worker_spawn(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            store = StateStore(root / 'state.json')
            state = WorkflowState()
            node_id = state.add_node('goal', 'theorem goal : True',
                                     metadata={'statement_status': 'indexed'})
            attempt_id = state.begin_attempt(node_id, 'compiler-coordinator', str(root / 'Candidate.lean'))
            job = root / 'job'
            job.mkdir()
            state.agent_requests['request'] = {
                'request_id': 'request', 'node_id': node_id, 'attempt_id': 'agent-attempt',
                'status': 'checking', 'agent_id': 'agent', 'compile_attempt_id': attempt_id,
                'compile_job': str(job), 'artifact': str(root / 'Candidate.lean'),
                'candidate_project': str(root)}
            store.save(state)
            (job / 'coordinator-intent.json').write_text(json.dumps({
                'schema_version': 1, 'phase': 'launching', 'request_id': 'request',
                'attempt_id': attempt_id, 'coordinator_pid': 424242}), encoding='utf-8')
            with patch('percolation_workflow.agent_bridge._process_alive', return_value=False):
                self.assertTrue(reclaim_dead_compile(store, 'request'))
            saved = store.load()
            self.assertEqual(saved.attempts[attempt_id].status, 'compile_error')
            self.assertIn('before launching compiler worker', saved.attempts[attempt_id].stderr)
            self.assertTrue(any(event['reason'] == 'coordinator exited before launching compiler worker'
                                for event in saved.events if event['kind'] == 'compiler_worker_reclaimed'))

    def test_corrupt_compiler_receipt_becomes_repairable_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            store = StateStore(root / 'state.json')
            state = WorkflowState()
            node_id = state.add_node('goal', 'theorem goal : True',
                                     metadata={'statement_status': 'indexed'})
            attempt_id = state.begin_attempt(node_id, 'compiler-coordinator',
                                             str(root / 'Candidate.lean'))
            job = root / 'job'
            job.mkdir()
            state.agent_requests['request'] = {
                'request_id': 'request', 'node_id': node_id, 'attempt_id': 'agent-attempt',
                'status': 'checking', 'agent_id': 'agent', 'compile_attempt_id': attempt_id,
                'compile_job': str(job), 'artifact': str(root / 'Candidate.lean'),
                'candidate_project': str(root)}
            store.save(state)
            (job / 'result.json').write_text('{not-json', encoding='utf-8')

            self.assertFalse(collect_candidate(store, 'request'))
            saved = store.load()
            self.assertEqual(saved.agent_requests['request']['status'], 'checked')
            self.assertEqual(saved.attempts[attempt_id].status, 'compile_error')
            self.assertEqual(saved.attempts[attempt_id].exit_code, 124)
            self.assertIn('invalid compiler receipt', saved.attempts[attempt_id].stderr)
            self.assertEqual(len(prepare_requests(store)), 1)

    def test_host_repair_round_limit_is_persisted_and_enforced(self):
        with tempfile.TemporaryDirectory() as directory:
            store = StateStore(Path(directory) / 'state.json')
            state = WorkflowState()
            node_id = state.add_node('goal', 'theorem goal : True',
                                     metadata={'statement_status': 'indexed'})
            for index in range(3):
                attempt_id = state.begin_attempt(node_id, f'agent-{index}')
                state.finish_attempt(attempt_id, status='compile_error', command=[],
                                     stdout='', stderr=f'error-{index}', exit_code=1)
            store.save(state)

            self.assertEqual(prepare_requests(store, max_repair_rounds=3), [])
            saved = store.load()
            self.assertTrue(saved.nodes[node_id].metadata['repair_exhausted'])
            self.assertEqual(saved.nodes[node_id].metadata['repair_exhausted_round'], 3)
            self.assertEqual(next_actions(store)[0]['kind'], 'repair_exhausted')

    def test_resume_and_terminal_payload_identity(self):
        with tempfile.TemporaryDirectory() as directory:
            store = StateStore(Path(directory) / 'state.json')
            state = WorkflowState()
            node_id = state.add_node('goal', 'theorem goal : True', metadata={'statement_status': 'indexed'})
            store.save(state)
            request = prepare_requests(store)[0]
            request_id = request['request_id']
            self.assertEqual(prepare_requests(store), [])
            bind_agent(store, request_id, 'host-agent-fixture')
            bind_agent(store, request_id, 'host-agent-fixture')
            with self.assertRaises(ValueError):
                record_result(store, request_id, 'wrong-agent', {})
            with self.assertRaises(ValueError):
                record_result(store, request_id, 'host-agent-fixture', {'status': {}, 'timed_out': True})
            self.assertEqual(store.load().nodes[node_id].status, 'in_progress')
            result = {'status': {'host-agent-fixture': {'completed': 'candidate source ready'}}, 'timed_out': False}
            record_result(store, request_id, 'host-agent-fixture', result)
            record_result(store, request_id, 'host-agent-fixture', result)
            saved = store.load()
            self.assertEqual(saved.agent_requests[request_id]['raw_result'], result)
            self.assertEqual(saved.nodes[node_id].status, 'open')
            self.assertEqual(saved.registry, {})
            self.assertEqual(len(saved.attempts), 1)
