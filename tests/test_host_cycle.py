import json
import hashlib
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

from percolation_workflow.host_cycle import run_host_cycle
from percolation_workflow.manifest import load_verification_manifest
from percolation_workflow.model import WorkflowState
from percolation_workflow.store import StateStore


class HostCycleTests(unittest.TestCase):
    def test_formalizable_lane_policy_reaches_host_cycle_dispatch(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            store = StateStore(root / 'state.json')
            state = WorkflowState()
            numeric = state.add_node(
                'numeric', 'theorem numeric : True',
                metadata={'statement_status': 'indexed', 'math_lane': 'numerical_blocker'})
            lean = state.add_node(
                'lean', 'theorem lean : True',
                metadata={'statement_status': 'indexed', 'math_lane': 'lean_adapter'})
            store.save(state)

            result = run_host_cycle(store, math_lane_policy='formalizable')

            self.assertEqual([item['node_id'] for item in result['dispatch']], [lean])
            self.assertEqual(result['dispatch'][0]['scheduler']['math_lane_policy'],
                             'formalizable')
            self.assertNotIn(numeric, [item['node_id'] for item in result['dispatch']])

    def test_cycle_reclaims_dead_compiler_and_dispatches_repair(self):
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
            state.agent_requests['dead-request'] = {
                'request_id': 'dead-request', 'node_id': node_id, 'attempt_id': 'agent-attempt',
                'status': 'checking', 'agent_id': 'agent', 'compile_attempt_id': attempt_id,
                'compile_job': str(job), 'artifact': str(root / 'Candidate.lean')}
            store.save(state)
            (job / 'started.json').write_text(json.dumps({'pid': 424242,
                'attempt_id': attempt_id}), encoding='utf-8')
            with patch('percolation_workflow.agent_bridge._process_alive', return_value=False):
                result = run_host_cycle(store)
            self.assertEqual(result['reclaimed_compilations'], ['dead-request'])
            self.assertEqual(result['dispatch'][0]['work_kind'], 'repair')
            self.assertEqual(store.load().attempts[attempt_id].status, 'compile_error')

    def test_cycle_reclaims_expired_agent_before_dispatching_repair(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            store = StateStore(root / 'state.json')
            state = WorkflowState()
            node_id = state.add_node('goal', 'theorem goal : True',
                                     metadata={'statement_status': 'indexed'})
            store.save(state)
            request = run_host_cycle(store)['dispatch'][0]
            from percolation_workflow.agent_bridge import bind_agent
            bind_agent(store, request['request_id'], 'expiring-agent', lease_seconds=1)
            time.sleep(1.1)
            result = run_host_cycle(store)
            self.assertEqual(result['reclaimed_requests'], [request['request_id']])
            self.assertEqual(len(result['dispatch']), 1)
            self.assertNotEqual(result['dispatch'][0]['request_id'], request['request_id'])
            saved = store.load()
            old_attempt = saved.agent_requests[request['request_id']]['attempt_id']
            self.assertEqual(saved.nodes[node_id].status, 'in_progress')
            self.assertEqual(saved.attempts[old_attempt].status, 'agent_timeout')

    def test_decomposition_callback_persists_ordered_children_once(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            store = StateStore(root / 'state.json')
            state = WorkflowState()
            parent_id = state.add_node('parent', 'theorem parent : True',
                                       metadata={'statement_status': 'indexed'})
            store.save(state)
            request = run_host_cycle(store)['dispatch'][0]
            from percolation_workflow.agent_bridge import bind_agent
            bind_agent(store, request['request_id'], 'planner-agent')
            attempt_id = store.load().agent_requests[request['request_id']]['attempt_id']
            callbacks = root / 'callbacks'
            callbacks.mkdir()
            envelope = {
                'protocol_version': 1, 'kind': 'agent_result',
                'request_id': request['request_id'], 'attempt_id': attempt_id,
                'event_id': 'evt-decomposition', 'agent_id': 'planner-agent',
                'payload': {'status': {'planner-agent': {'completed': 'sketch'}}},
                'decomposition': {'sketch': 'prove parent from first then second', 'children': [
                    {'name': 'first', 'statement': 'theorem first : True', 'proof_sketch': 'trivial'},
                    {'name': 'second', 'statement': 'theorem second : True', 'proof_sketch': 'trivial'}],
                    'comparator_gate': {
                        name: {
                            'source_identity': {
                                'source': f'{name}.lean', 'module': name,
                                'name': f'{name}.{name}',
                                'statement_sha256': hashlib.sha256(
                                    statement.encode()).hexdigest()},
                            'source_statement': statement,
                            'covered_source': [f'{name}.lean'],
                            'target_theorem_identity': {
                                'module': name, 'name': f'{name}.{name}'}}
                        for name, statement in (
                            ('first', 'theorem first : True'),
                            ('second', 'theorem second : True'))
                    }}}
            (callbacks / 'decomposition.json').write_text(json.dumps(envelope), encoding='utf-8')
            first = run_host_cycle(store, callback_dir=callbacks)
            self.assertFalse(first['errors'])
            saved = store.load()
            self.assertEqual(saved.agent_requests[request['request_id']]['status'], 'decomposed')
            proposal = saved.nodes[parent_id].metadata['reduction_proposals'][-1]
            self.assertEqual(len(proposal['children']), 2)
            self.assertEqual(proposal['child_order'], proposal['children'])
            second = run_host_cycle(store, callback_dir=callbacks)
            self.assertFalse(second['errors'])
            self.assertEqual(len(store.load().nodes[parent_id].metadata['reduction_proposals']), 1)

    def test_candidate_callback_starts_coordinator_compile(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            store = StateStore(root / 'state.json')
            state = WorkflowState()
            state.add_node('goal', 'theorem goal : True', metadata={'statement_status': 'indexed'})
            store.save(state)
            request = run_host_cycle(store)['dispatch'][0]
            from percolation_workflow.agent_bridge import bind_agent
            bind_agent(store, request['request_id'], 'agent-1')
            attempt_id = store.load().agent_requests[request['request_id']]['attempt_id']
            callbacks = root / 'callbacks'
            callbacks.mkdir()
            envelope = {
                'protocol_version': 1, 'kind': 'agent_result',
                'request_id': request['request_id'], 'attempt_id': attempt_id,
                'event_id': 'evt-candidate', 'agent_id': 'agent-1',
                'payload': {'status': {'agent-1': {'completed': 'candidate'}}},
                'candidate': {'project': str(root), 'source': str(root / 'Candidate.lean'),
                              'receipt': {'schema_version': 1,
                                          'status': 'compiled_candidate',
                                          'comparator_status': 'accepted',
                                          'registry_status': 'accepted'}}}
            callback = callbacks / 'candidate.json'
            callback.write_text(json.dumps(envelope), encoding='utf-8')
            fake_process = type('Process', (), {'pid': 1234})()
            def fake_start(saved_store, request_id, project, source):
                checkpoint = saved_store.load()
                checkpoint.agent_requests[request_id].update(
                    status='checking', compile_job=str(root / 'job'))
                saved_store.save(checkpoint)
                return fake_process
            with patch('percolation_workflow.host_cycle.start_candidate', side_effect=fake_start) as start:
                result = run_host_cycle(store, callback_dir=callbacks)
            start.assert_called_once_with(store, request['request_id'], str(root), str(root / 'Candidate.lean'))
            self.assertEqual(result['started_compilations'][0]['pid'], 1234)
            saved = store.load()
            self.assertEqual(saved.agent_requests[request['request_id']]['candidate_ingest']['audit_status'],
                             'pending')
            self.assertEqual(saved.agent_requests[request['request_id']]['candidate_ingest']['comparator_status'],
                             'pending')
            self.assertNotIn('candidate_manifest', saved.agent_requests[request['request_id']])
            self.assertEqual(saved.nodes[request['node_id']].metadata.get('evidence_stage') or 'open', 'open')
            self.assertEqual(saved.registry, {})
            claims_before = sum(event['kind'] == 'candidate_receipt_claim_ingested'
                                for event in saved.events)
            run_host_cycle(store, callback_dir=callbacks)
            claims_after = sum(event['kind'] == 'candidate_receipt_claim_ingested'
                               for event in store.load().events)
            self.assertEqual(claims_after, claims_before)

    def test_manifest_is_bound_before_dispatch(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            store = StateStore(root / 'state.json')
            state = WorkflowState()
            state.add_node('goal', 'theorem goal : True', metadata={'statement_status': 'indexed'})
            store.save(state)
            manifest_path = root / 'verification-manifest.json'
            manifest_path.write_text(json.dumps({
                'schema_version': 1, 'workspace_root': '.', 'state_path': 'state.json',
                'target': {'root': 'goal'}, 'dependency': {'name': 'Pinned'},
                'host_protocol': {'name': 'codex-agent-callback', 'version': 1},
                'nodes': {'goal': {'challenge_module': 'Challenge', 'solution_module': 'Solution',
                                   'source_files': ['Challenge.lean', 'Solution.lean']}}}),
                encoding='utf-8')
            manifest = load_verification_manifest(manifest_path)
            result = run_host_cycle(store, manifest=manifest_path)
            self.assertEqual(result['dispatch'][0]['manifest_sha256'], manifest.sha256)
            self.assertEqual(store.load().manifest['sha256'], manifest.sha256)

    def test_cycle_prepares_and_ingests_idempotent_host_callback(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            store = StateStore(root / 'state.json')
            state = WorkflowState()
            state.add_node('goal', 'theorem goal : True', metadata={'statement_status': 'indexed'})
            store.save(state)

            first = run_host_cycle(store)
            request = first['dispatch'][0]
            self.assertEqual(first['next_actions'][0]['kind'], 'dispatch_agent')
            callbacks = root / 'callbacks'
            callbacks.mkdir()
            payload = {'status': {'agent-1': {'completed': 'candidate'}}}
            attempt_id = store.load().agent_requests[request['request_id']]['attempt_id']
            (callbacks / 'result.json').write_text(json.dumps({
                'protocol_version': 1, 'kind': 'agent_result',
                'request_id': request['request_id'], 'attempt_id': attempt_id,
                'event_id': 'evt-1', 'agent_id': 'agent-1', 'payload': payload}),
                encoding='utf-8')
            # The host must bind before returning a callback; this simulates that durable step.
            from percolation_workflow.agent_bridge import bind_agent
            bind_agent(store, request['request_id'], 'agent-1')
            second = run_host_cycle(store, callback_dir=callbacks)
            self.assertEqual(second['accepted_callbacks'], ['result.json'])
            self.assertFalse(second['errors'])
            self.assertEqual(second['next_actions'][0]['kind'], 'compile_candidate')
            self.assertEqual(store.load().agent_requests[request['request_id']]['raw_callback']['event_id'],
                             'evt-1')
            third = run_host_cycle(store, callback_dir=callbacks)
            self.assertEqual(third['accepted_callbacks'], ['result.json'])
            self.assertFalse(third['errors'])
            self.assertEqual(store.load().agent_requests[request['request_id']]['status'], 'reported')
            changed = json.loads((callbacks / 'result.json').read_text(encoding='utf-8'))
            changed['payload'] = {'status': {'agent-1': {'completed': 'different'}}}
            (callbacks / 'result.json').write_text(json.dumps(changed), encoding='utf-8')
            fourth = run_host_cycle(store, callback_dir=callbacks)
            self.assertIn('reused with different', fourth['errors'][0]['error'])

    def test_bad_callback_is_reported_without_state_corruption(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            store = StateStore(root / 'state.json')
            state = WorkflowState()
            state.add_node('goal', 'theorem goal : True', metadata={'statement_status': 'indexed'})
            store.save(state)
            first = run_host_cycle(store)
            callbacks = root / 'callbacks'
            callbacks.mkdir()
            (callbacks / 'bad.json').write_text('{"request_id":"wrong"}', encoding='utf-8')
            result = run_host_cycle(store, callback_dir=callbacks)
            self.assertEqual(len(result['errors']), 1)
            self.assertEqual(store.load().agent_requests[first['dispatch'][0]['request_id']]['status'],
                             'awaiting_dispatch')
