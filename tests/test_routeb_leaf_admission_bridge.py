import unittest

from examples.routeb_leaf_admission_bridge.bridge import build_advisory_artifact


class RouteBLeafAdmissionBridgeTests(unittest.TestCase):
    def receipt(self):
        return {"compile_exit_code": 0, "module": "RouteB.Leaf", "theorem": "leaf_bound",
                "source_hash": "a" * 64}

    def complete(self):
        return dict(source_binding={"present": True, "evidence_id": "src-1"},
                    coverage={"present": True, "evidence_id": "cov-1"},
                    terminal_transfer={"present": True, "evidence_id": "term-1"},
                    scope=["real-domain"], open_obligations=[])

    def test_complete_leaf_is_advisory_only(self):
        artifact = build_advisory_artifact(self.receipt(), **self.complete())
        self.assertEqual(artifact["status"], "advisory_ready")
        self.assertEqual(artifact["candidate_status"], "compiled_candidate")
        self.assertEqual(artifact["registry_status"], "pending")
        self.assertFalse(artifact["verified"])
        self.assertFalse(artifact["promotion_allowed"])
        self.assertEqual(artifact["dag"]["root"], "RouteB.Leaf.leaf_bound")

    def test_missing_gates_stay_pending(self):
        artifact = build_advisory_artifact(self.receipt(), scope=[], open_obligations=[])
        self.assertEqual(artifact["status"], "pending")
        for gate in ("source_binding", "coverage", "terminal_transfer"):
            self.assertTrue(any(gate in x for x in artifact["reasons"]))

    def test_negative_gate_and_bad_hash_are_rejected(self):
        kwargs = self.complete()
        kwargs["coverage"] = {"present": False, "reason": "not checked"}
        artifact = build_advisory_artifact(dict(self.receipt(), source_hash="not-a-hash"), **kwargs)
        self.assertEqual(artifact["status"], "rejected")
        self.assertFalse(artifact["promotion_allowed"])

    def test_open_obligations_keep_artifact_pending(self):
        kwargs = self.complete()
        kwargs["open_obligations"] = ["float64-source-binding"]
        artifact = build_advisory_artifact(self.receipt(), **kwargs)
        self.assertEqual(artifact["status"], "pending")
        self.assertIn("float64-source-binding", artifact["open_obligations"])


if __name__ == "__main__":
    unittest.main()
