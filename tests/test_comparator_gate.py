import hashlib
import unittest

from percolation_workflow.comparator_gate import check_statement_comparator_gate


class ComparatorGateTests(unittest.TestCase):
    def context(self, statement="theorem C : True"):
        normalized = " ".join(statement.split())
        return dict(source_identity={"source": "Challenge.lean", "module": "Challenge",
                                     "name": "Challenge.C",
                                     "statement_sha256": hashlib.sha256(normalized.encode()).hexdigest()},
                    source_statement=statement, covered_source=["Challenge.lean"],
                    target_theorem_identity={"module": "Challenge", "name": "Challenge.C"})

    def test_accepts_bound_normalized_covered_target(self):
        self.assertTrue(check_statement_comparator_gate(candidate_statement="theorem C :\n True", **self.context()))

    def test_rejects_each_missing_binding_fail_closed(self):
        context = self.context()
        for key in ("source_identity", "source_statement", "covered_source", "target_theorem_identity"):
            with self.subTest(key=key):
                broken = dict(context, **{key: None})
                self.assertFalse(check_statement_comparator_gate(candidate_statement=context["source_statement"], **broken))

    def test_rejects_target_identity_mismatch(self):
        context = self.context()
        context["target_theorem_identity"] = {"module": "Other", "name": "Challenge.C"}
        self.assertFalse(check_statement_comparator_gate(candidate_statement=context["source_statement"], **context))
