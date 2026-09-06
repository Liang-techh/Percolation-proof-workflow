"""Strict, fail-closed materializer for a Route-B 14-state flowpipe receipt.

This tool never invents numerical evidence.  It accepts a producer receipt,
recomputes source digests, and emits a receipt only after every local and
global obligation passes.
"""
from __future__ import annotations
import argparse, hashlib, json, math
from pathlib import Path

SCHEMA = "routeb-flowpipe-parent-numeric-receipt-v1"
DIM = 14
HASH_KEYS = ("EF", "DN", "DT", "CO", "CU")

class ReceiptError(ValueError): pass

def _finite(x, name):
    if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x):
        raise ReceiptError(f"{name}: finite JSON number required")
    return float(x)

def _interval(v, name):
    if not isinstance(v, list) or len(v) != 2: raise ReceiptError(f"{name}: interval required")
    lo, hi = (_finite(v[0], name+".lo"), _finite(v[1], name+".hi"))
    if lo > hi: raise ReceiptError(f"{name}: lo > hi")
    return lo, hi

def _box(v, name):
    if not isinstance(v, list) or len(v) != DIM: raise ReceiptError(f"{name}: 14D box required")
    return [_interval(x, f"{name}[{i}]") for i, x in enumerate(v)]

def validate(doc, base: Path) -> dict:
    if not isinstance(doc, dict) or doc.get("schema") != SCHEMA or doc.get("status") != "VALIDATED":
        raise ReceiptError("schema/status is not a validated numeric receipt")
    model = doc.get("model")
    expected = {"vector_field_ref":"F_full_X0", "state_dimension":DIM,
                "initial_set_ref":"X0_full", "horizon_ref":"[T_LO,T_HI]",
                "rounding":"outward_ieee754_binary64"}
    if model != expected: raise ReceiptError("model binding or outward rounding declaration mismatch")
    cells = doc.get("cells")
    if not isinstance(cells, list) or not cells: raise ReceiptError("cells are missing")
    previous = None
    for pos, c in enumerate(cells):
        if not isinstance(c, dict) or c.get("index") != pos: raise ReceiptError(f"cell {pos}: contiguous index required")
        t = c.get("time"); lo, hi = _interval([t.get("lo"), t.get("hi")] if isinstance(t,dict) else None, f"cell {pos}.time")
        if previous is not None and lo != previous: raise ReceiptError(f"cell {pos}: time boundary is not exact predecessor boundary")
        previous = hi
        ib, ob = _box(c.get("input_box"), f"cell {pos}.input_box"), _box(c.get("output_box"), f"cell {pos}.output_box")
        if pos and ib != prev_out: raise ReceiptError(f"cell {pos}: input_box is not exact preceding output_box")
        rhs = c.get("rhs")
        if not isinstance(rhs, dict) or rhs.get("dimension") != DIM or not isinstance(rhs.get("components"), list) or len(rhs["components"]) != DIM:
            raise ReceiptError(f"cell {pos}: RHS must contain exactly 14 components")
        _interval([rhs.get("lo"), rhs.get("hi")], f"cell {pos}.rhs")
        for i, q in enumerate(rhs["components"]): _interval(q, f"cell {pos}.rhs.components[{i}]")
        if c.get("outward_ieee754") is not True: raise ReceiptError(f"cell {pos}: outward IEEE754 witness missing")
        lip = c.get("lipschitz"); L = _finite(lip.get("bound"), f"cell {pos}.lipschitz.bound") if isinstance(lip,dict) else -1
        if not isinstance(lip,dict) or lip.get("norm") != "infinity" or L < 0: raise ReceiptError(f"cell {pos}: invalid Lipschitz bound")
        p = c.get("picard")
        if not isinstance(p,dict) or p.get("validated") is not True or not isinstance(p.get("inclusion_witness"),str) or not p["inclusion_witness"].strip(): raise ReceiptError(f"cell {pos}: Picard witness missing")
        h = _finite(p.get("step_width"), f"cell {pos}.picard.step_width"); k = _finite(p.get("contraction_factor"), f"cell {pos}.picard.contraction_factor")
        if h <= 0 or k < 0 or k >= 1 or L*h != k: raise ReceiptError(f"cell {pos}: Picard contraction must equal L*step_width and be < 1")
        prev_out = ob
    tt = doc.get("terminal_transfer")
    if not isinstance(tt,dict) or tt.get("claim") != "flow(X0_full,[T_LO,T_HI]) subseteq P_N_STEPS" or tt.get("validated") is not True or not isinstance(tt.get("witness"),str) or not tt["witness"].strip(): raise ReceiptError("terminal transfer is not validated")
    sh = doc.get("source_hashes")
    if not isinstance(sh,dict): raise ReceiptError("source_hashes missing")
    for key in HASH_KEYS:
        digest = sh.get(key); path = base / f"{key}.source"
        if not isinstance(digest,str) or len(digest)!=64 or any(x not in "0123456789abcdef" for x in digest): raise ReceiptError(f"invalid {key} SHA-256")
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != digest: raise ReceiptError(f"{key}: source hash mismatch or source missing")
    return doc

def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument("receipt", type=Path); ap.add_argument("--source-dir", type=Path, required=True); ap.add_argument("--out", type=Path, required=True)
    a=ap.parse_args()
    try:
        doc=json.loads(a.receipt.read_text(encoding="utf-8")); valid=validate(doc,a.source_dir)
        a.out.parent.mkdir(parents=True,exist_ok=True); a.out.write_text(json.dumps(valid,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        print("FLOWPIPE_NUMERIC_RECEIPT_VALIDATED"); return 0
    except (OSError, ValueError, json.JSONDecodeError) as e:
        print(f"FLOWPIPE_NUMERIC_RECEIPT_FAIL_CLOSED: {e}"); return 1
if __name__ == "__main__": raise SystemExit(main())
