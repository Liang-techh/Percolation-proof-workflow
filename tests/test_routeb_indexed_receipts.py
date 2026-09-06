import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).parents[1] / "scripts" / "record_routeb_indexed_receipts.py"


def row(index=(1, 2, 3, 4), outward=True):
    return {"cell_index": list(index), "source_hash": "a" * 64,
            "geometry": {"q_lo": [0], "q_hi": [1]},
            "rho": {"rho": "1/2"}, "inverse": {"norm": "2"},
            "outward": outward}


def run(src, out):
    return subprocess.run([sys.executable, str(SCRIPT), "--input", str(src), "--output", str(out)],
                          capture_output=True, text=True)


def test_sparse_jsonl_normalizes_without_enumeration(tmp_path):
    src, out = tmp_path / "in.jsonl", tmp_path / "out.jsonl"
    src.write_text(json.dumps(row()) + "\n" + json.dumps(row((32, 32, 32, 32))) + "\n")
    result = run(src, out)
    assert result.returncode == 0
    items = [json.loads(x) for x in out.read_text().splitlines()]
    assert len(items) == 2 and items[0]["rank"] == 1 + 33*2 + 33**2*3 + 33**3*4


@pytest.mark.parametrize("bad", [row((33, 0, 0, 0)), row((0, 0, 0, 0), False)])
def test_rejects_bad_address_or_non_outward(tmp_path, bad):
    src, out = tmp_path / "in.jsonl", tmp_path / "out.jsonl"
    src.write_text(json.dumps(bad))
    assert run(src, out).returncode != 0 and not out.exists()


def test_rejects_missing_duplicate_and_no_input_fail_closed(tmp_path):
    src, out = tmp_path / "in.jsonl", tmp_path / "out.jsonl"
    value = row()
    del value["inverse"]
    src.write_text(json.dumps(value) + "\n" + json.dumps(row()) + "\n")
    assert run(src, out).returncode != 0 and not out.exists()
    src.write_text(json.dumps(row()) + "\n" + json.dumps(row()) + "\n")
    assert run(src, out).returncode != 0 and not out.exists()
    no_input = subprocess.run([sys.executable, str(SCRIPT), "--output", str(out)], capture_output=True)
    assert no_input.returncode != 0
    src.write_text("")
    assert run(src, out).returncode != 0 and not out.exists()
