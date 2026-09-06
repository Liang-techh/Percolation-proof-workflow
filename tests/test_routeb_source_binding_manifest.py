import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

PATH = Path(__file__).parents[1] / "scripts" / "routeb_source_binding_manifest.py"
spec = importlib.util.spec_from_file_location("routeb_manifest", PATH)
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)


class RouteBSourceManifestTests(unittest.TestCase):
    def fixture(self):
        root = Path(tempfile.mkdtemp()); (root / "a.jl").write_bytes(b"source\n")
        sha = hashlib.sha256(b"source\n").hexdigest()
        meta = {"domain": {"kind": "full_state_ball", "radius": "3/20"},
                "normalization": {"state": "q1..q6,v1..v6,w,c", "time": "T=1"},
                "fd": {"step": "1e-5", "regularizer": "1e-6"}, "float64_marker": True}
        base = {"state_order": mod.STATE_ORDER, "sources": [{"path": "a.jl", "sha256": sha}], **meta}
        return root, base, dict(base)

    def test_accepts_exact_contract(self):
        root, m, r = self.fixture(); self.assertEqual(mod.validate(m, r, source_root=root)["status"], "passed")

    def test_rejects_order_hash_metadata_and_marker(self):
        for field, value in (("state_order", list(reversed(mod.STATE_ORDER))), ("float64_marker", False),
                             ("domain", {"wrong": 1})):
            root, m, r = self.fixture(); r[field] = value
            with self.assertRaises(mod.ValidationError): mod.validate(m, r, source_root=root)
        root, m, r = self.fixture(); m["sources"][0]["sha256"] = "0" * 64
        with self.assertRaises(mod.ValidationError): mod.validate(m, r, source_root=root)

    def test_does_not_return_binding_conclusion(self):
        root, m, r = self.fixture(); self.assertIsNone(mod.validate(m, r, source_root=root)["binding_conclusion"])


if __name__ == "__main__": unittest.main()
