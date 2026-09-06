import json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).parents[1]
TOOL = ROOT / "scripts" / "routeb_flowpipe_capture_contract.py"

def run(tmp_path, doc):
    p = tmp_path / "capture.json"; p.write_text(json.dumps(doc), encoding="utf-8")
    return subprocess.run([sys.executable, str(TOOL), str(p), "--source-dir", str(tmp_path)], capture_output=True, text=True)

def base():
    return {"schema":"routeb-flowpipe-numeric-capture-v1", "status":"VALIDATED",
            "model":{"vector_field_ref":"F_full_X0","state_dimension":14,"initial_set_ref":"X0_full","horizon_ref":"[T_LO,T_HI]"}}

def test_point_float_is_not_an_interval(tmp_path):
    d = base(); d["cells"] = [{"index":0,"time":[0.0,0.1]}]
    r = run(tmp_path, d)
    assert r.returncode == 1 and "FAIL_CLOSED" in r.stdout

def test_missing_numeric_payload_fails_closed(tmp_path):
    r = run(tmp_path, base())
    assert r.returncode == 1 and "cells missing" in r.stdout
