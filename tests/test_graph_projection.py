import json
import tempfile
import unittest
from pathlib import Path
from percolation_workflow.graph import merge_reachable_graph, attach_elaborated_types, import_decl_graph
from percolation_workflow.model import WorkflowState


class ProjectionTests(unittest.TestCase):
    def test_axiom_evidence_does_not_promote_or_replace_challenge(self):
        state = WorkflowState()
        node_id = state.add_node('target', 'trusted statement')
        with tempfile.TemporaryDirectory() as directory:
            path = self.graph(directory, [dict(name='target', type='True', axioms=['sorryAx'])])
            self.assertEqual(attach_elaborated_types(state, path), 1)
        self.assertEqual(state.nodes[node_id].statement, 'trusted statement')
        self.assertEqual(state.nodes[node_id].metadata['unexpected_axioms'], ['sorryAx'])
        self.assertEqual(state.registry, {})
        self.assertEqual(state.nodes[node_id].status, 'open')

    def graph(self, directory, rows):
        path = Path(directory) / 'graph.jsonl'
        path.write_text('\n'.join(json.dumps(r) for r in rows), encoding='utf-8')
        return path

    def test_traverse_definitions_and_spanless_helpers_preserve_history(self):
        rows = [
            dict(name='root', kind='theorem', startLine=1, valueDeps=['def']),
            dict(name='def', kind='def', startLine=2, typeDeps=['helper']),
            dict(name='helper', kind='theorem', startLine=0, valueDeps=['leaf']),
            dict(name='leaf', kind='theorem', startLine=3),
            dict(name='unrelated', kind='theorem', startLine=4),
        ]
        state = WorkflowState()
        node_id = state.add_node('root', 'exact original statement')
        attempt_id = state.begin_attempt(node_id, 'original-agent')
        with tempfile.TemporaryDirectory() as directory:
            path = self.graph(directory, rows)
            ids = merge_reachable_graph(state, path, ['root'])
            self.assertEqual(set(ids), {'root', 'leaf'})
            self.assertEqual(ids['root'], node_id)
            self.assertEqual(state.nodes[node_id].statement, 'exact original statement')
            self.assertEqual(state.nodes[node_id].attempts, [attempt_id])
            self.assertIn(attempt_id, state.attempts)
            self.assertEqual(state.nodes[node_id].dependencies, [ids['leaf']])
            self.assertEqual(merge_reachable_graph(state, path, ['root']), ids)
            self.assertEqual(len(state.nodes), 2)
            self.assertEqual(len(state.graph_artifacts), 1)
            artifact = state.graph_artifacts[0]
            self.assertEqual(artifact['roots'], ['root'])
            self.assertEqual(artifact['selected_nodes'], ['leaf', 'root'])
            self.assertEqual(artifact['edge_provenance']['root'][0]['origins'], ['type', 'value'])
            path.write_text(path.read_text(encoding='utf-8') +
                            '\n' + json.dumps(dict(name='later', kind='theorem', startLine=9)),
                            encoding='utf-8')
            merge_reachable_graph(state, path, ['root'])
            self.assertEqual(len(state.graph_artifacts), 2)

    def test_cycle_failure_does_not_partially_mutate_state(self):
        rows = [dict(name='a', kind='theorem', startLine=1, valueDeps=['b']),
                dict(name='b', kind='theorem', startLine=2, valueDeps=['a'])]
        state = WorkflowState()
        state.add_node('existing', 'True')
        before = state.to_dict()
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, 'cycle'):
                merge_reachable_graph(state, self.graph(directory, rows), ['a'])
        self.assertEqual(state.to_dict(), before)

    def test_decl_import_preserves_type_and_value_edges(self):
        rows = [
            dict(name='P.root', kind='theorem', typeDeps=['P.type_leaf'], valueDeps=['P.value_leaf']),
            dict(name='P.type_leaf', kind='opaque'),
            dict(name='P.value_leaf', kind='theorem'),
        ]
        state = WorkflowState()
        with tempfile.TemporaryDirectory() as directory:
            path = self.graph(directory, rows)
            ids = import_decl_graph(state, path, project_prefix='P.')
        self.assertEqual(set(state.nodes[ids['P.root']].dependencies),
                         {ids['P.type_leaf'], ids['P.value_leaf']})
        provenance = {entry['name']: entry['origins']
                      for entry in state.graph_artifacts[0]['edge_provenance']['P.root']}
        self.assertEqual(provenance['P.type_leaf'], ['type'])
        self.assertEqual(provenance['P.value_leaf'], ['value'])

    def test_decl_import_preserves_instance_roots_and_inductive_constructors(self):
        rows = [
            dict(name='P.root', kind='theorem', startLine=1, valueDeps=['P.Box']),
            dict(name='P.Box', kind='inductive', startLine=3),
            dict(name='P.Box.mk', kind='ctor', startLine=4,
                 typeDeps=['P.Box']),
            dict(name='P.instBox', kind='def', startLine=7, isInstance=True,
                 valueDeps=['P.instance_leaf']),
            dict(name='P.instance_leaf', kind='theorem', startLine=8),
            dict(name='P.generated.eq_1', kind='theorem', startLine=0),
        ]
        state = WorkflowState()
        with tempfile.TemporaryDirectory() as directory:
            path = self.graph(directory, rows)
            ids = import_decl_graph(state, path, project_prefix='P.')
        self.assertEqual(set(ids), {'P.root', 'P.instance_leaf'})
        self.assertEqual(state.nodes[ids['P.instance_leaf']].metadata['is_instance'], False)
        artifact = state.graph_artifacts[0]
        self.assertEqual(artifact['algorithm'], 'import_decl_graph/v2')
        self.assertEqual(artifact['instance_roots'], ['P.instBox'])
        self.assertEqual(artifact['constructor_expansions'], ['P.Box.mk'])
        self.assertIn('P.Box', artifact['supporting_declarations'])
        self.assertIn('P.Box.mk', artifact['supporting_declarations'])
        self.assertIn('P.instBox', artifact['supporting_declarations'])
        self.assertIn('P.instance_leaf', artifact['selected_nodes'])
