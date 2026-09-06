"""Fail-closed capture boundary for an external Route-B flowpipe calculator.

This is an input contract, not a numerical interval evaluator.  It deliberately
does not coerce JSON numbers or point samples into intervals.  A producer must
send decimal endpoint strings plus an explicit outward-rounding witness and a
source artifact reference for every interval-bearing field.
"""
from __future__ import annotations

import argparse, hashlib, json, math, re
from pathlib import Path

DIM = 14
SCHEMA = "routeb-flowpipe-numeric-capture-v1"
DECIMAL = re.compile(r"^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?$")

class CaptureError(ValueError):
    pass

def _decimal(value, name):
    if not isinstance(value, str) or not DECIMAL.fullmatch(value):
        raise CaptureError(f"{name}: decimal endpoint string required (JSON numbers rejected)")
    x = float(value)
    if not math.isfinite(x):
        raise CaptureError(f"{name}: finite endpoint required")
    return x

def interval(value, name):
    if not isinstance(value, dict) or set(value) != {"lo", "hi", "rounding", "source_ref"}:
        raise CaptureError(f"{name}: explicit interval object required")
    lo, hi = _decimal(value["lo"], name+".lo"), _decimal(value["hi"], name+".hi")
    if lo > hi:
        raise CaptureError(f"{name}: lo > hi")
    if value["rounding"] != "outward_ieee754_binary64":
        raise CaptureError(f"{name}: outward IEEE754 witness required")
    if not isinstance(value["source_ref"], str) or not value["source_ref"].strip():
        raise CaptureError(f"{name}: producer source_ref required")

def box(value, name):
    if not isinstance(value, list) or len(value) != DIM:
        raise CaptureError(f"{name}: exactly 14 explicit intervals required")
    for i, item in enumerate(value):
        interval(item, f"{name}[{i}]")

def validate(doc, source_dir: Path):
    if not isinstance(doc, dict) or doc.get("schema") != SCHEMA:
        raise CaptureError("schema mismatch")
    if doc.get("status") != "VALIDATED":
        raise CaptureError("capture status must be VALIDATED")
    if doc.get("model") != {"vector_field_ref":"F_full_X0", "state_dimension":14,
                             "initial_set_ref":"X0_full", "horizon_ref":"[T_LO,T_HI]"}:
        raise CaptureError("model binding mismatch")
    cells = doc.get("cells")
    if not isinstance(cells, list) or not cells:
        raise CaptureError("cells missing")
    previous = None
    for pos, cell in enumerate(cells):
        if cell.get("index") != pos:
            raise CaptureError(f"cell {pos}: contiguous index required")
        t = cell.get("time")
        if not isinstance(t, dict): raise CaptureError(f"cell {pos}: time missing")
        interval(t, f"cell {pos}.time")
        if previous is not None and t["lo"] != previous:
            raise CaptureError(f"cell {pos}: time boundary is not exact producer value")
        previous = t["hi"]
        box(cell.get("input_box"), f"cell {pos}.input_box")
        box(cell.get("output_box"), f"cell {pos}.output_box")
        rhs = cell.get("rhs")
        if not isinstance(rhs, list) or len(rhs) != DIM:
            raise CaptureError(f"cell {pos}.rhs: exactly 14 explicit intervals required")
        for i, item in enumerate(rhs): interval(item, f"cell {pos}.rhs[{i}]")
        lip = cell.get("lipschitz")
        if not isinstance(lip, dict) or lip.get("norm") != "infinity":
            raise CaptureError(f"cell {pos}: infinity-norm Lipschitz record required")
        interval(lip.get("bound"), f"cell {pos}.lipschitz.bound")
        picard = cell.get("picard")
        if not isinstance(picard, dict) or picard.get("validated") is not True:
            raise CaptureError(f"cell {pos}: validated Picard witness required")
        interval(picard.get("step_width"), f"cell {pos}.picard.step_width")
        interval(picard.get("contraction_factor"), f"cell {pos}.picard.contraction_factor")
        for key in ("inclusion_witness", "source_ref"):
            if not isinstance(picard.get(key), str) or not picard[key].strip():
                raise CaptureError(f"cell {pos}.picard.{key}: required")
    terminal = doc.get("terminal_witness")
    if not isinstance(terminal, dict) or terminal.get("validated") is not True:
        raise CaptureError("validated terminal witness required")
    for key in ("witness_ref", "source_ref"):
        if not isinstance(terminal.get(key), str) or not terminal[key].strip():
            raise CaptureError(f"terminal_witness.{key}: required")
    hashes = doc.get("source_hashes")
    if not isinstance(hashes, dict) or set(hashes) != {"EF","DN","DT","CO","CU"}:
        raise CaptureError("exact EF/DN/DT/CO/CU source hashes required")
    for key, digest in hashes.items():
        if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise CaptureError(f"{key}: SHA-256 required")
        path = source_dir / f"{key}.source"
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise CaptureError(f"{key}: source hash mismatch or source missing")
    return doc

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("capture", type=Path); ap.add_argument("--source-dir", type=Path, required=True)
    args = ap.parse_args()
    try:
        validate(json.loads(args.capture.read_text(encoding="utf-8")), args.source_dir)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"FLOWPIPE_CAPTURE_FAIL_CLOSED: {exc}"); return 1
    print("FLOWPIPE_CAPTURE_ACCEPTED_SHAPE"); return 0

if __name__ == "__main__": raise SystemExit(main())
