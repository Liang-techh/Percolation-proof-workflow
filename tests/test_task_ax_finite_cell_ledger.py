import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).parents[1]
ART = ROOT / "artifacts" / "task_AX_finite_cell_ledger_v2"
spec = importlib.util.spec_from_file_location("ax_checker", ART / "check_finite_cell_ledger.py")
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


def load():
    return json.loads((ART / "finite_cell_ledger_v2.json").read_text(encoding="utf-8"))


def test_open_skeleton_is_admissible_but_not_flowpipe():
    data = load()
    assert checker.errors(data, ART) == []
    assert data["status"] == "OPEN"
    assert data["policy"]["no_flowpipe_generated"] is True


def test_matched_face_requires_positive_receipt_and_exact_edge():
    data = load()
    data["initial_cover"]["box_ids"] = ["x0"]
    data["cells"] = [
        {"id": "c0", "initial_box_id": "x0", "time_box": {"lo": "0", "hi": "1/10"},
         "exit_faces": [{"id": "f0", "classification": "matched_successor", "successor_id": "c1",
                         "positive_step": True, "continuation_receipt": "r0"}]},
        {"id": "c1", "initial_box_id": "x0", "time_box": {"lo": "1/10", "hi": "1/5"}, "exit_faces": []},
    ]
    data["continuation_receipts"] = [{"id": "r0", "status": "MISSING", "from_cell": "c0",
        "exit_face_id": "f0", "to_cell": "c1", "from_time": "1/10", "to_time": "1/10",
        "delta_t": {"lo": "0", "hi": "1/10"},
        "proof_artifact": None}]
    data["exit_face_accounting"]["edges"] = [{"from_cell": "c0", "face_id": "f0", "to_cell": "c1"}]
    assert any("strictly positive delta_t" in e for e in checker.errors(data, ART))
