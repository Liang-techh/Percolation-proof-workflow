import json
from pathlib import Path
import shutil
import tempfile
import unittest

from percolation_workflow.upload_plan import (build_upload_plan, compare_elaborated_types,
                                               generate_definition_module, generate_skeleton,
                                               generate_solution_module, generate_theorem_stub,
                                               join_stage_facts, load_jsonl,
                                               ordered_upload_actions, proof_stub,
                                               rewrite_imports, rewrite_reference_ranges,
                                               skeleton_subtract)
from percolation_workflow.uploader import Prove2MeTransport, UploadLedger
from percolation_workflow.lean import run_lean


FIXTURE = Path(__file__).resolve().parents[1] / 'upstream' / 'prove2me_workspace' / 'examples' / 'upload_full_project'


class UploadPlanTests(unittest.TestCase):
    def test_public_sum_squares_fixture_joins_and_classifies_by_exact_facts(self):
        graph = load_jsonl(FIXTURE / 'expected' / 'decl_graph.jsonl')
        sketch = {
            'SumSquares.Defs': load_jsonl(FIXTURE / 'expected' / 'sketch_info.Defs.jsonl'),
            'SumSquares.Lemmas': load_jsonl(FIXTURE / 'expected' / 'sketch_info.Lemmas.jsonl'),
            'SumSquares.Main': load_jsonl(FIXTURE / 'expected' / 'sketch_info.Main.jsonl'),
        }
        plan = build_upload_plan(graph, sketch, ['SumSquares.six_sumSq'],
                                 force_nodes=['SumSquares.sumSq_succ'],
                                 source_root=FIXTURE / 'SumSquares')
        by_name = {row['name']: row for row in plan['nodes']}
        self.assertEqual(by_name['SumSquares.six_sumSq']['destination'], 'theorem_node')
        self.assertEqual(by_name['SumSquares.sumSq_succ']['destination'], 'theorem_node')
        self.assertEqual(by_name['_private.SumSquares.Main.0.SumSquares.six_mul_succ']['destination'],
                         'inline_helper')
        self.assertIn('SumSquares.sumSq.match_1', plan['spanless_dropped'])
        self.assertIn('SumSquares.Defs', plan['definition_modules'])
        self.assertEqual(plan['definition_modules']['SumSquares.Defs']['source_path'],
                         'SumSquares/Defs.lean')
        self.assertRegex(plan['definition_modules']['SumSquares.Defs']['source_digest'], r'^[0-9a-f]{64}$')

    def test_join_uses_containment_for_wrapped_and_anonymous_declarations(self):
        graph = [{
            'name': 'P.wrapped', 'userName': 'P.wrapped', 'module': 'P.Main',
            'kind': 'theorem', 'isPrivate': False, 'startLine': 3, 'endLine': 5,
            'typeDeps': [], 'valueDeps': [],
        }, {
            'name': 'P.inst', 'userName': 'P.inst', 'module': 'P.Main',
            'kind': 'def', 'isPrivate': False, 'startLine': 8, 'endLine': 8,
            'typeDeps': [], 'valueDeps': [],
        }]
        facts = {'P.Main': [{
            'kind': 'decl', 'nameText': 'wrapped',
            'declStart': {'line': 2, 'col': 0, 'offset': 10},
            'declEnd': {'line': 6, 'col': 1, 'offset': 60},
            'valStart': {'line': 4, 'col': 15, 'offset': 42},
            'valKind': 'simple', 'docstring': None, 'privateTok': None,
        }, {
            'kind': 'decl', 'nameText': None,
            'declStart': {'line': 7, 'col': 0, 'offset': 61},
            'declEnd': {'line': 9, 'col': 1, 'offset': 90},
            'valStart': {'line': 8, 'col': 10, 'offset': 75},
            'valKind': 'simple', 'docstring': None, 'privateTok': None,
        }]}
        joined = join_stage_facts(graph, facts)
        self.assertEqual(joined['P.wrapped']['decl_start']['line'], 2)
        self.assertEqual(joined['P.wrapped']['val_start']['offset'], 42)
        self.assertIsNone(joined['P.inst']['source_fact']['nameText'])

    def test_proof_cut_is_byte_offset_and_subtraction_is_right_to_left(self):
        source = 'α := 1\n\ntheorem goal : True := by\n  trivial\n'
        raw = source.encode('utf-8')
        cut = raw.index(b':=', len('α := 1\n\n'.encode('utf-8')))
        fact = {'val_start': {'offset': cut, 'line': 3, 'col': 18}}
        self.assertEqual(proof_stub(source, fact), 'α := 1\n\ntheorem goal : True := by sorry')
        first = 'def a : Nat := 1\n'
        second = 'theorem b : True := by trivial\n'
        combined = first + second
        a = {'decl_start': {'offset': 0}, 'decl_end': {'offset': len(first.encode())}}
        b_start = len(first.encode())
        b = {'decl_start': {'offset': b_start},
             'decl_end': {'offset': len(combined.encode())}}
        self.assertEqual(skeleton_subtract(combined, [a]), second)
        self.assertEqual(skeleton_subtract(combined, [b]), first)

    def test_reference_renames_use_stage_two_ranges_and_preserve_qualification(self):
        source = 'theorem old (x : Nat) : old x = old x := by\n  exact rfl\n'
        references = [
            {'const': 'P.old', 'start': {'offset': 8}, 'end': {'offset': 11}},
            {'const': 'P.old', 'start': {'offset': 24}, 'end': {'offset': 27}},
            {'const': 'P.old', 'start': {'offset': 32}, 'end': {'offset': 35}},
        ]
        self.assertEqual(
            rewrite_reference_ranges(source, references, {'P.old': 'P.renamed'}),
            'theorem renamed (x : Nat) : renamed x = renamed x := by\n  exact rfl\n')
        qualified = 'P.old x\n'
        self.assertEqual(
            rewrite_reference_ranges(qualified, [{'const': 'P.old',
                                                  'start': {'offset': 0}, 'end': {'offset': 5}}],
                                       {'P.old': 'Q.new'}),
            'Q.new x\n')

    def test_generate_skeleton_cuts_selected_theorem_and_rewrites_only_import_lines(self):
        graph = load_jsonl(FIXTURE / 'expected' / 'decl_graph.jsonl')
        facts = join_stage_facts(
            [row for row in graph if row['module'] == 'SumSquares.Main'],
            {'SumSquares.Main': load_jsonl(FIXTURE / 'expected' / 'sketch_info.Main.jsonl')})
        source = (FIXTURE / 'SumSquares' / 'SumSquares' / 'Main.lean').read_text(encoding='utf-8')
        skeleton = generate_skeleton(source, facts,
                                     ['_private.SumSquares.Main.0.SumSquares.six_mul_succ',
                                      'SumSquares.six_sumSq'],
                                     stub_names=['SumSquares.six_sumSq'])
        self.assertIn('private theorem six_mul_succ', skeleton)
        self.assertIn('theorem six_sumSq', skeleton)
        self.assertIn('theorem six_sumSq (n : ℕ) :', skeleton)
        self.assertIn(':= by sorry', skeleton)
        rewritten = rewrite_imports(source, {'SumSquares.Lemmas': [
            'Definitions.Def_SumSquares_Defs', 'Theorems.Thm_SumSquares_sumSq_succ']},
            extra_imports=['Mathlib.Tactic'])
        self.assertIn('import Definitions.Def_SumSquares_Defs\n', rewritten)
        self.assertIn('import Theorems.Thm_SumSquares_sumSq_succ\n', rewritten)
        self.assertNotIn('import SumSquares.Lemmas', rewritten)
        self.assertIn('private theorem six_mul_succ', rewritten)

    def test_platform_generators_use_exact_spans_for_fixture_tree(self):
        graph = load_jsonl(FIXTURE / 'expected' / 'decl_graph.jsonl')
        sketch = {
            'SumSquares.Defs': load_jsonl(FIXTURE / 'expected' / 'sketch_info.Defs.jsonl'),
            'SumSquares.Lemmas': load_jsonl(FIXTURE / 'expected' / 'sketch_info.Lemmas.jsonl'),
            'SumSquares.Main': load_jsonl(FIXTURE / 'expected' / 'sketch_info.Main.jsonl'),
        }
        joined = join_stage_facts([row for row in graph if row['startLine'] != 0], sketch)
        defs_source = (FIXTURE / 'SumSquares' / 'SumSquares' / 'Defs.lean').read_text(encoding='utf-8')
        defs = generate_definition_module(
            defs_source,
            {name: fact for name, fact in joined.items() if fact['module'] == 'SumSquares.Defs'},
            [name for name, fact in joined.items()
             if fact['module'] == 'SumSquares.Defs' and
             next(row for row in graph if row['name'] == name)['kind'] not in {'theorem', 'opaque'}])
        self.assertIn('def sumSq', defs)
        self.assertIn('instance : SumBudget ℕ', defs)
        lemmas_source = (FIXTURE / 'SumSquares' / 'SumSquares' / 'Lemmas.lean').read_text(encoding='utf-8')
        lemma_facts = {name: fact for name, fact in joined.items() if fact['module'] == 'SumSquares.Lemmas'}
        stub = generate_theorem_stub(lemmas_source, lemma_facts, 'SumSquares.sumSq_succ')
        self.assertNotIn('Unfolding lemma', stub)
        self.assertIn(':= by sorry', stub)
        main_source = (FIXTURE / 'SumSquares' / 'SumSquares' / 'Main.lean').read_text(encoding='utf-8')
        main_facts = {name: fact for name, fact in joined.items() if fact['module'] == 'SumSquares.Main'}
        solution = generate_solution_module(
            main_source, main_facts, 'SumSquares.six_sumSq',
            ['_private.SumSquares.Main.0.SumSquares.six_mul_succ'],
            namespace_prefix='SumSquares')
        self.assertIn('private theorem six_mul_succ', solution)
        self.assertIn('open SumSquares in\ntheorem solution', solution)
        self.assertNotIn('/-- Six times', solution)
        sum_solution = generate_solution_module(
            lemmas_source, lemma_facts, 'SumSquares.sumSq_succ', namespace_prefix='SumSquares')
        self.assertIn('open SumSquares in\ntheorem solution', sum_solution)
        self.assertNotIn('namespace SumSquares', sum_solution)

    def test_solution_generator_hoists_active_section_binders(self):
        source = ('namespace Demo\nsection\nvariable {α : Type} (x : α)\n'
                  'theorem target : x = x := by rfl\nend\nend Demo\n')
        raw = source.encode('utf-8')
        target_start = raw.index(b'theorem target')
        name_start = raw.index(b'target', target_start)
        facts = {'Demo.target': {
            'decl_start': {'offset': target_start},
            'decl_end': {'offset': len(raw)},
            'val_start': {'offset': raw.index(b':= by', target_start)},
            'references': [{'const': 'Demo.target',
                            'start': {'offset': name_start},
                            'end': {'offset': name_start + len(b'target')}}],
        }}
        solution = generate_solution_module(source, facts, 'Demo.target', namespace_prefix='Demo')
        self.assertIn('open Demo\nvariable {α : Type} (x : α)\nopen Demo in\n', solution)
        self.assertIn('theorem solution : x = x := by rfl', solution)
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            shutil.copyfile(Path(__file__).parents[1] / 'examples/minimal_lean/lean-toolchain',
                            project / 'lean-toolchain')
            (project / 'lakefile.toml').write_text('name = "sectionHoistTest"\n', encoding='utf-8')
            generated = project / 'Solution.lean'
            generated.write_text(solution, encoding='utf-8')
            result = run_lean(project, ['lake', 'env', 'lean', '-R', str(project), '-o',
                                        str(project / 'Solution.olean'), str(generated)])
            self.assertTrue(result.ok, result.stdout + result.stderr)

    def test_ambiguous_containment_fails_closed(self):
        graph = [{'name': 'P.x', 'userName': 'P.x', 'module': 'P.Main', 'kind': 'theorem',
                  'isPrivate': False, 'startLine': 3, 'endLine': 3, 'typeDeps': [], 'valueDeps': []}]
        fact = {'kind': 'decl', 'nameText': 'x',
                'declStart': {'line': 1, 'col': 0, 'offset': 0},
                'declEnd': {'line': 5, 'col': 0, 'offset': 20},
                'valStart': {'line': 3, 'col': 5, 'offset': 10},
                'docstring': None, 'privateTok': None}
        with self.assertRaises(ValueError):
            join_stage_facts(graph, {'P.Main': [fact, dict(fact)]})

    def test_elaborated_type_diff_only_allows_universe_display_renaming(self):
        original = [{'name': 'P.goal', 'type': '(α : Type u_1) → α = α'},
                    {'name': 'P.other', 'type': '(β : Type u_2) → β = β'}]
        staged = [{'name': 'P.goal', 'type': '(α : Type u_9) → α = α'},
                  {'name': 'P.other', 'type': '(β : Type u_4) → β = Nat'}]
        report = compare_elaborated_types(original, staged)
        self.assertFalse(report['ok'])
        self.assertEqual([item['name'] for item in report['mismatches']], ['P.other'])
        self.assertTrue(compare_elaborated_types(original[:1], staged[:1])['ok'])
        self.assertFalse(compare_elaborated_types(original[:1], staged,
                                                  rename_map={'P.goal': 'P.renamed'})['ok'])

    def test_ordered_actions_are_definitions_then_theorems_then_solutions(self):
        plan = {'schema_version': 1, 'nodes': [
            {'name': 'root', 'module': 'Main', 'destination': 'theorem_node',
             'dependencies': ['leaf']},
            {'name': 'leaf', 'module': 'Lemmas', 'destination': 'theorem_node',
             'dependencies': []},
            {'name': 'Def', 'module': 'Defs', 'destination': 'definition_material',
             'dependencies': []},
        ]}
        actions = ordered_upload_actions(plan, definition_imports={'Defs': []})
        self.assertEqual([item['kind'] for item in actions], [
            'submit_definition', 'submit_theorem', 'submit_theorem',
            'verify_solution', 'verify_solution'])
        self.assertEqual([item.get('name') for item in actions[1:3]], ['leaf', 'root'])
        self.assertEqual([item.get('name') for item in actions[3:]], ['leaf', 'root'])
        cyclic = dict(plan)
        cyclic['nodes'] = [{'name': 'A', 'module': 'A', 'destination': 'definition_material'},
                           {'name': 'B', 'module': 'B', 'destination': 'definition_material'}]
        with self.assertRaises(ValueError):
            ordered_upload_actions(cyclic, definition_imports={'A': ['B'], 'B': ['A']})

    def test_upload_ledger_records_before_and_after_and_reuses_theorem_ids(self):
        actions = [
            {'key': 'theorem:leaf', 'kind': 'submit_theorem', 'name': 'leaf', 'depends_on': []},
            {'key': 'solution:leaf', 'kind': 'verify_solution', 'name': 'leaf',
             'depends_on': ['theorem:leaf']},
        ]
        class Transport:
            def __init__(self):
                self.calls = []
            def execute(self, action, *, operation_key, context):
                self.calls.append((operation_key, dict(context)))
                if action['kind'] == 'submit_theorem':
                    return {'theorem_id': 'T-leaf', 'status': 'PUBLISHED'}
                return {'submission_id': 'S-leaf', 'status': 'Proved',
                        'theorem_id': context['theorem:leaf']['theorem_id']}
        with tempfile.TemporaryDirectory() as directory:
            ledger_path = Path(directory) / 'upload-ledger.json'
            transport = Transport()
            result = UploadLedger(ledger_path).run(actions, transport)
            self.assertEqual(result['status'], 'complete')
            self.assertEqual(transport.calls[1][1]['theorem:leaf']['theorem_id'], 'T-leaf')
            before = len(transport.calls)
            result2 = UploadLedger(ledger_path).run(actions, transport)
            self.assertEqual(result2['status'], 'complete')
            self.assertEqual(len(transport.calls), before)

    def test_upload_ledger_resumes_in_flight_with_same_operation_key(self):
        actions = [{'key': 'definition:Defs', 'kind': 'submit_definition',
                    'module': 'Defs', 'depends_on': []}]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'ledger.json'
            ledger = UploadLedger(path)
            ledger.prepare(actions)
            ledger.data['actions']['definition:Defs']['status'] = 'in_flight'
            ledger.save()
            calls = []
            class Transport:
                def execute(self, action, *, operation_key, context):
                    calls.append(operation_key)
                    return {'job_id': 'J1', 'status': 'PUBLISHED'}
            UploadLedger(path).run(actions, Transport())
            self.assertEqual(calls, ['definition:Defs'])

    def test_prove2me_transport_submits_polls_and_passes_theorem_id_to_verify(self):
        class Response:
            def __init__(self, status, value):
                self.status = status
                self._raw = json.dumps(value).encode('utf-8')
            def getcode(self):
                return self.status
            def read(self):
                return self._raw
            def close(self):
                pass

        calls = []
        def opener(request, timeout):
            calls.append(request)
            path = request.full_url.split('?', 1)[0]
            if path.endswith('/submit-problem'):
                self.assertEqual(request.get_header('Authorization'), 'Bearer token')
                self.assertEqual(request.get_header('Idempotency-key'), 'theorem:P.t')
                return Response(202, {'jobs': [{'job_id': 'J1', 'name': 'P.t'}], 'errors': []})
            if path.endswith('/publish-jobs/J1'):
                return Response(200, {'status': 'PUBLISHED', 'theorem_id': 'T1',
                                      'theorem_name': 'P.t'})
            if path.endswith('/verify') and request.get_method() == 'POST':
                body = request.data
                self.assertIn(b'name="theorem_id"', body)
                self.assertIn(b'\r\nT1\r\n', body)
                self.assertEqual(request.get_header('Idempotency-key'), 'solution:P.t')
                return Response(202, {'submission_id': 'S1', 'status': 'PENDING'})
            if path.endswith('/verify') and request.get_method() == 'GET':
                return Response(200, {'submission_id': 'S1', 'status': 'ACCEPTED',
                                      'theorem_id': 'T1'})
            self.fail(f'unexpected request: {request.full_url}')

        actions = [
            {'key': 'theorem:P.t', 'kind': 'submit_theorem', 'name': 'P.t',
             'payload': {'theorem_name': 'P.t', 'formal_statement':
                         'theorem P.t : True := by sorry'}, 'depends_on': []},
            {'key': 'solution:P.t', 'kind': 'verify_solution', 'name': 'P.t',
             'solution': 'theorem solution : True := by trivial',
             'depends_on': ['theorem:P.t']},
        ]
        with tempfile.TemporaryDirectory() as directory:
            transport = Prove2MeTransport(
                access_token='token', opener=opener,
                operation_store=Path(directory) / 'remote-operations.json',
                poll_interval_seconds=0, sleep=lambda _: None)
            result = UploadLedger(Path(directory) / 'ledger.json').run(actions, transport)
            self.assertEqual(result['status'], 'complete')
            self.assertEqual(len(calls), 4)

    def test_prove2me_transport_resumes_a_published_job_without_resubmitting(self):
        class Response:
            def __init__(self, status, value):
                self.status = status
                self._raw = json.dumps(value).encode('utf-8')
            def getcode(self):
                return self.status
            def read(self):
                return self._raw
            def close(self):
                pass

        first_calls = []
        def first_opener(request, timeout):
            first_calls.append(request)
            if request.get_method() == 'POST':
                return Response(202, {'jobs': [{'job_id': 'J2', 'name': 'P.t'}]})
            raise OSError('not used')

        action = {'key': 'theorem:P.t', 'kind': 'submit_theorem', 'name': 'P.t',
                  'payload': {'theorem_name': 'P.t', 'formal_statement':
                              'theorem P.t : True := by sorry'}, 'depends_on': []}
        with tempfile.TemporaryDirectory() as directory:
            operation_store = Path(directory) / 'remote-operations.json'
            ledger_path = Path(directory) / 'ledger.json'
            first = Prove2MeTransport(access_token='token', opener=first_opener,
                                       operation_store=operation_store,
                                       poll_interval_seconds=0, sleep=lambda _: None)
            with self.assertRaises(Exception):
                UploadLedger(ledger_path).run([action], first)
            second_calls = []
            def second_opener(request, timeout):
                second_calls.append(request)
                self.assertEqual(request.get_method(), 'GET')
                return Response(200, {'status': 'PUBLISHED', 'theorem_id': 'T2',
                                      'theorem_name': 'P.t'})
            second = Prove2MeTransport(access_token='token', opener=second_opener,
                                       operation_store=operation_store,
                                       poll_interval_seconds=0, sleep=lambda _: None)
            result = UploadLedger(ledger_path).run([action], second)
            self.assertEqual(result['status'], 'complete')
            self.assertEqual(len(first_calls), 2)
            self.assertEqual(len(second_calls), 1)


if __name__ == '__main__':
    unittest.main()
