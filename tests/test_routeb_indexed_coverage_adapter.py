import json, subprocess, sys
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "scripts" / "routeb_indexed_coverage_adapter.py"
H = "a" * 64

def doc(records):
    return {"domain_partition": {"base": 33, "coordinates": ["a2","a3","a4","a5"], "address_range": {"min": 0,"max": 32}, "fixed_coordinates": {"a1": 0,"a6": 0}},
            "source_hashes": {"partition": H}, "records": records,
            "et_receipt": {"schema": "routeb-flowpipe-coverage-receipt-v1", "status":"UNVALIDATED"}}

def rec(ix=(1,2,3,4), refs=None, source=H):
    rank = ix[0] + 33*ix[1] + 33**2*ix[2] + 33**3*ix[3]
    return {"leaf_id": "cell16/" + "/".join(f"a{x}={v}" for x,v in zip((2,3,4,5),ix)), "cell_index": list(ix), "rank": rank, "source_hash": source, "adjacency": refs or []}

def run(src, out):
    return subprocess.run([sys.executable, str(SCRIPT), "--input", str(src), "--output", str(out)], capture_output=True, text=True)

def test_sparse_records_adapt_without_enumeration(tmp_path):
    src, out = tmp_path/"in.json", tmp_path/"out.json"
    a, b = rec(), rec((32,32,32,32)); a["adjacency"]=[b["leaf_id"]]
    src.write_text(json.dumps(doc([a,b])))
    r = run(src,out)
    assert r.returncode == 0
    result = json.loads(out.read_text()); assert result["schema"] == "routeb-flowpipe-coverage-receipt-v1"

def test_rank_partition_adjacency_and_hash_fail_closed(tmp_path):
    for change in ("rank", "partition", "adjacency", "hash"):
        value = doc([rec()])
        if change == "rank": value["records"][0]["rank"] += 1
        if change == "partition": value["domain_partition"]["base"] = 34
        if change == "adjacency": value["records"][0]["adjacency"] = ["cell16/a2=9/a3=9/a4=9/a5=9"]
        if change == "hash": value["records"][0]["source_hash"] = "b" * 64
        src, out = tmp_path/f"{change}.json", tmp_path/f"{change}.out"
        src.write_text(json.dumps(value)); assert run(src,out).returncode != 0 and not out.exists()
