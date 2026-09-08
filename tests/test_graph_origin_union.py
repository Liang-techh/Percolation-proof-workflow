"""Focused synthetic checks for dependency provenance, not theorem validity."""
import copy
import json
import tempfile
import unittest
from pathlib import Path

from percolation_workflow.graph import import_decl_graph, merge_reachable_graph
from percolation_workflow.model import WorkflowState


class GraphOriginUnionTests(unittest.TestCase):
    def project(self, rows, mode, state=None):
        state = WorkflowState() if state is None else state
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'graph.jsonl'
            path.write_text('\n'.join(json.dumps(row) for row in rows), encoding='utf-8')
            if mode == 'merge':
                ids = merge_reachable_graph(state, path, ['root'])
            else:
                ids = import_decl_graph(state, path)
        return state, ids, state.graph_artifacts[-1]

    def test_direct_and_helper_routes_both_contribute(self):
        rows = [
            dict(name='root', kind='theorem', startLine=1,
                 typeDeps=['leaf'], valueDeps=['helper'], attribution_ref='original notice'),
            dict(name='helper', kind='def', valueDeps=['leaf']),
            dict(name='leaf', kind='theorem', startLine=2),
        ]
        for mode in ('merge', 'import'):
            with self.subTest(mode=mode):
                state, ids, artifact = self.project(rows, mode)
                self.assertEqual(artifact['edge_provenance']['root'],
                                 [{'name': 'leaf', 'origins': ['type', 'value']}])
                self.assertEqual(state.nodes[ids['root']].dependencies, [ids['leaf']])
                self.assertEqual(state.nodes[ids['root']].metadata['source']['attribution_ref'],
                                 'original notice')
                self.assertEqual(state.registry, {})
                self.assertTrue(all(node.status == 'open' for node in state.nodes.values()))

    def test_new_origins_at_shared_helper_reach_every_leaf(self):
        rows = [
            dict(name='root', kind='theorem', startLine=1,
                 typeDeps=['join'], valueDeps=['helper']),
            dict(name='helper', kind='def', valueDeps=['join']),
            dict(name='join', kind='def', typeDeps=['type_leaf'], valueDeps=['value_leaf']),
            dict(name='type_leaf', kind='theorem', startLine=2),
            dict(name='value_leaf', kind='theorem', startLine=3),
        ]
        expected = [{'name': name, 'origins': ['type', 'value']}
                    for name in ('type_leaf', 'value_leaf')]
        for mode in ('merge', 'import'):
            for ordered_rows in (rows, list(reversed(rows))):
                with self.subTest(mode=mode, reversed=ordered_rows is not rows):
                    _, _, artifact = self.project(ordered_rows, mode)
                    self.assertEqual(artifact['edge_provenance']['root'], expected)

    def test_helper_cycles_terminate_and_theorem_boundaries_are_preserved(self):
        rows = [
            dict(name='root', kind='theorem', startLine=1, valueDeps=['a']),
            dict(name='a', kind='def', typeDeps=['b']),
            dict(name='b', kind='def', valueDeps=['a', 'leaf']),
            dict(name='leaf', kind='theorem', startLine=2, valueDeps=['grandchild']),
            dict(name='grandchild', kind='theorem', startLine=3),
        ]
        for mode in ('merge', 'import'):
            with self.subTest(mode=mode):
                _, _, artifact = self.project(rows, mode)
                self.assertEqual(artifact['edge_provenance']['root'],
                                 [{'name': 'leaf', 'origins': ['type', 'value']}])
                self.assertEqual(artifact['edge_provenance']['leaf'],
                                 [{'name': 'grandchild', 'origins': ['value']}])

    def test_constructor_origin_applies_only_to_constructor_expansion(self):
        rows = [
            dict(name='root', kind='theorem', startLine=1, typeDeps=['Box']),
            dict(name='Box', kind='inductive', typeDeps=['type_leaf']),
            dict(name='Box.mk', kind='ctor', valueDeps=['ctor_leaf']),
            dict(name='type_leaf', kind='theorem', startLine=2),
            dict(name='ctor_leaf', kind='theorem', startLine=3),
        ]
        for mode in ('merge', 'import'):
            with self.subTest(mode=mode):
                _, _, artifact = self.project(rows, mode)
                self.assertEqual(artifact['edge_provenance']['root'], [
                    {'name': 'ctor_leaf', 'origins': ['constructor', 'type', 'value']},
                    {'name': 'type_leaf', 'origins': ['type']},
                ])

    def test_new_algorithm_appends_evidence_without_rewriting_legacy_record(self):
        rows = [dict(name='root', kind='theorem', startLine=1)]
        for mode, old_version, new_version in (
                ('merge', 'merge_reachable_graph/v1', 'merge_reachable_graph/v2'),
                ('import', 'import_decl_graph/v2', 'import_decl_graph/v3')):
            with self.subTest(mode=mode):
                state, ids, artifact = self.project(rows, mode)
                # Same raw bytes and roots, but evidence from the old algorithm.
                artifact['algorithm'] = old_version
                legacy = copy.deepcopy(artifact)
                _, repeated_ids, current = self.project(rows, mode, state)
                self.assertEqual(current['algorithm'], new_version)
                self.assertEqual(state.graph_artifacts[0], legacy)
                self.assertEqual(len(state.graph_artifacts), 2)
                self.assertEqual(ids, repeated_ids)
                self.project(rows, mode, state)
                self.assertEqual(len(state.graph_artifacts), 2)


if __name__ == '__main__':
    unittest.main()
