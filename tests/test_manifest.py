import json
import tempfile
import unittest
from pathlib import Path

from percolation_workflow.manifest import load_verification_manifest, bind_manifest, initialize_state_from_manifest
from percolation_workflow.model import WorkflowState
from percolation_workflow.store import StateStore


class ManifestTests(unittest.TestCase):
    def test_manifest_can_initialize_a_research_dag_without_target_script(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'contract.json').write_text(json.dumps({'target': 'Root'}), encoding='utf-8')
            manifest_path = root / 'verification-manifest.json'
            manifest_path.write_text(json.dumps({
                'schema_version': 1, 'workspace_root': '.', 'state_path': 'state.json',
                'target': {'root': 'Root', 'contract': 'contract.json'},
                'dependency': {'name': 'Pinned'},
                'nodes': {
                    'Root': {'challenge_module': 'RootChallenge', 'solution_module': 'RootSolution',
                             'source_files': ['RootChallenge.lean', 'RootSolution.lean']},
                    'Leaf': {'challenge_module': 'LeafChallenge', 'solution_module': 'LeafSolution',
                             'source_files': ['LeafChallenge.lean', 'LeafSolution.lean']}},
                'research': {'project': 'manifest-intake', 'root': 'Root', 'nodes': [
                    {'name': 'Root', 'statement': 'theorem Root : True',
                     'proof_sketch': 'close from Leaf'},
                    {'name': 'Leaf', 'statement': 'theorem Leaf : True', 'parent': 'Root'}]}
            }), encoding='utf-8')
            manifest = load_verification_manifest(manifest_path)
            store = StateStore(root / 'state.json')
            state = initialize_state_from_manifest(manifest, store)
            self.assertEqual(state.project, 'manifest-intake')
            root_node = state.nodes[state.root_id]
            leaf_node = state.nodes[next(node_id for node_id, node in state.nodes.items()
                                         if node.name == 'Leaf')]
            self.assertEqual(root_node.metadata['contract']['target'], 'Root')
            self.assertEqual(leaf_node.parent_id, root_node.id)
            self.assertEqual(state.frontier()[0].name, 'Leaf')
            with self.assertRaises(FileExistsError):
                initialize_state_from_manifest(manifest, store)

    def test_local_fkg_manifest_is_portable_and_complete(self):
        manifest = load_verification_manifest(
            Path(__file__).parents[1] / 'examples/local_fkg/verification-manifest.json')
        self.assertEqual(manifest.dependency_name, 'PercolationContinuity')
        self.assertEqual(len(manifest.nodes), 3)
        self.assertEqual(
            manifest.for_node('Percolation.Literature.harris_fkg_local').solution_module,
            'LocalFKGSolutionAgent')

    def test_manifest_rejects_unsafe_source_path(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'manifest.json'
            path.write_text(json.dumps({
                'schema_version': 1,
                'state_path': 'state.json',
                'dependency': {'name': 'Pinned'},
                'nodes': {'goal': {
                    'challenge_module': 'Challenge',
                    'solution_module': 'Solution',
                    'source_files': ['Challenge.lean', '../Solution.lean']}}}),
                encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'unsafe Lean path'):
                load_verification_manifest(path)

    def test_state_binding_rejects_manifest_drift(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            state_path = root / 'state.json'
            state = WorkflowState()
            state.add_node('goal', 'theorem goal : True', metadata={'statement_status': 'indexed'})
            StateStore(state_path).save(state)
            manifest_path = root / 'verification-manifest.json'
            manifest_path.write_text(json.dumps({
                'schema_version': 1,
                'workspace_root': '.',
                'state_path': 'state.json',
                'target': {'root': 'goal'},
                'dependency': {'name': 'Pinned'},
                'nodes': {'goal': {
                    'challenge_module': 'Challenge', 'solution_module': 'Solution',
                    'source_files': ['Challenge.lean', 'Solution.lean']}}}),
                encoding='utf-8')
            manifest = load_verification_manifest(manifest_path)
            bind_manifest(StateStore(state_path), manifest)
            manifest_path.write_text(manifest_path.read_text(encoding='utf-8') + '\n', encoding='utf-8')
            changed = load_verification_manifest(manifest_path)
            with self.assertRaisesRegex(ValueError, 'different verification manifest'):
                bind_manifest(StateStore(state_path), changed)

    def test_manifest_rejects_non_pinned_acceptance_plan(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / 'manifest.json'
            path.write_text(json.dumps({
                'schema_version': 1, 'state_path': 'state.json',
                'dependency': {'name': 'Pinned'},
                'verification': {'acceptance_line': 'custom success'},
                'nodes': {'goal': {'challenge_module': 'Challenge',
                                   'solution_module': 'Solution',
                                   'source_files': ['Challenge.lean', 'Solution.lean']}}}),
                encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'acceptance_line'):
                load_verification_manifest(path)
