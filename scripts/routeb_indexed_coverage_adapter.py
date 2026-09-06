"""Fail-closed adapter from sparse indexed receipts to the ET coverage schema.

The adapter only validates and copies supplied records.  In particular it never
enumerates the 33^4 address space and never creates a missing witness.
"""
from __future__ import annotations

import argparse, hashlib, json, os, re, tempfile
from pathlib import Path
from typing import Any

BASE = 33
COORDS = ("a2", "a3", "a4", "a5")
HASH = re.compile(r"^[0-9a-f]{64}$")
ET = "routeb-flowpipe-coverage-receipt-v1"

class AdapterError(ValueError): pass

def _load(path: Path) -> dict[str, Any]:
    try: data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e: raise AdapterError(f"cannot read input: {e}") from e
    if not isinstance(data, dict) or not isinstance(data.get("records"), list):
        raise AdapterError("input must be an object with sparse records[]")
    return data

def _rank(ix: Any) -> int:
    if isinstance(ix, dict):
        try: ix = [ix[k] for k in COORDS]
        except KeyError as e: raise AdapterError("cell_index requires a2,a3,a4,a5") from e
    if not isinstance(ix, list) or len(ix) != 4 or any(isinstance(x, bool) or not isinstance(x, int) or not 0 <= x < BASE for x in ix):
        raise AdapterError("cell_index coordinates must be integers in [0,32]")
    return sum(x * BASE**i for i, x in enumerate(ix))

def validate(doc: dict[str, Any]) -> dict[str, Any]:
    p = doc.get("domain_partition")
    if not isinstance(p, dict) or p.get("base") != BASE or tuple(p.get("coordinates", ())) != COORDS:
        raise AdapterError("domain partition metadata is not the cell16 33^4 partition")
    if p.get("address_range") != {"min": 0, "max": 32}:
        raise AdapterError("invalid domain address range")
    fixed = p.get("fixed_coordinates")
    if fixed not in (None, {"a1": 0, "a6": 0}): raise AdapterError("fixed coordinate metadata mismatch")
    sh = doc.get("source_hashes")
    if not isinstance(sh, dict) or not sh or any(not isinstance(v, str) or not HASH.fullmatch(v) for v in sh.values()):
        raise AdapterError("source_hashes must contain lowercase sha256 values")
    declared = sh.get("partition") or doc.get("source_hash")
    if not isinstance(declared, str) or not HASH.fullmatch(declared): raise AdapterError("partition source hash missing")
    records = doc["records"]
    if not records: raise AdapterError("sparse records[] is empty")
    ids, ranks = set(), set()
    for n, r in enumerate(records, 1):
        if not isinstance(r, dict): raise AdapterError(f"record {n} is not an object")
        leaf = r.get("leaf_id"); ix = r.get("cell_index")
        if not isinstance(leaf, str) or not leaf.startswith("cell16/"): raise AdapterError(f"record {n}: invalid leaf_id")
        rank = _rank(ix)
        if r.get("rank") != rank: raise AdapterError(f"record {n}: rank mismatch")
        if leaf in ids or rank in ranks: raise AdapterError(f"record {n}: duplicate cell")
        if r.get("source_hash") != declared: raise AdapterError(f"record {n}: source hash mismatch")
        ids.add(leaf); ranks.add(rank)
    for n, r in enumerate(records, 1):
        for key in ("adjacency", "adjacency_refs", "neighbors"):
            refs = r.get(key, [])
            if not isinstance(refs, list) or any(x not in ids or x == r["leaf_id"] for x in refs):
                raise AdapterError(f"record {n}: invalid adjacency reference")
    et = doc.get("et_receipt")
    if not isinstance(et, dict) or et.get("schema") != ET:
        raise AdapterError("missing ET receipt with exact schema id")
    return {"schema": ET, "status": et.get("status"), "model": et.get("model"),
            "partition": et.get("partition"), "coverage": et.get("coverage"),
            "first_exit": et.get("first_exit"), "terminal_transfer": et.get("terminal_transfer"),
            "source_hashes": et.get("source_hashes")}

def adapt(source: Path, output: Path) -> dict[str, Any]:
    result = validate(_load(source))
    output.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=output.name + ".", dir=output.parent, text=True)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f: json.dump(result, f, ensure_ascii=False, sort_keys=True, indent=2); f.write("\n")
        os.replace(tmp, output)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)
    return result

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__); ap.add_argument("--input", required=True, type=Path); ap.add_argument("--output", required=True, type=Path)
    try: result = adapt(ap.parse_args().input, ap.parse_args().output)
    except AdapterError as e: ap.error(str(e))
    print(json.dumps({"status": "adapted", "schema": ET}))
    return 0
if __name__ == "__main__": raise SystemExit(main())
