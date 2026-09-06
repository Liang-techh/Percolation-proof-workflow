"""Check all literal Lean CSV fields and Kp against the read-only source."""
import argparse
import csv
import hashlib
import json
import re
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()
assert args.output.resolve().is_relative_to(HERE)
source = HERE.parents[2] / "6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq"
csv_path = source / "routeB_fourier_potential_rational.csv"
controller_path = source / "dhport_lib.jl"
lean_path = HERE / "PotentialSlice.lean"
with csv_path.open(newline="", encoding="utf-8") as fh:
    reader = csv.DictReader(fh)
    fields = reader.fieldnames
    expected_fields = [f"nu{i}" for i in range(1,7)] + ["real_num","real_den","imag_num","imag_den"]
    assert fields == expected_fields
    expected = [tuple(int(r[f]) for f in fields) for r in reader]
text = lean_path.read_text(encoding="utf-8")
records = re.findall(r"⟨!\[([^\]]+)\],\s*(-?\d+),\s*(\d+),\s*(-?\d+),\s*(\d+)⟩",text)
actual = [tuple(int(v.strip()) for v in freq.split(",")) + tuple(map(int,values))
          for freq,*values in records]
assert len(actual) == len(expected) == 17 and actual == expected
assert len({r[:6] for r in expected}) == 17
assert all(r[7] > 0 and r[8] == 0 and r[9] > 0 for r in expected)
conjugates = {r[:6]:r[6:] for r in expected}
assert all(conjugates[tuple(-x for x in r[:6])] == r[6:] for r in expected)
controller = controller_path.read_text(encoding="utf-8")
kp_csv = re.search(r"\bKp\s*=\s*\[([^\]]+)\]",controller)[1]
kp_lean = re.search(r"def Kp : Fin 6 → ℚ := !\[([^\]]+)\]",text)[1]
source_kp = [Fraction(x.strip()) for x in kp_csv.split(",")]
lean_kp = [Fraction(x.strip()) for x in kp_lean.split(",")]
assert len(lean_kp) == 6 and lean_kp == source_kp
base = HERE.parent / "routeb_dh_power_binding/output/tube-RWfVZNvn"
inputs = [csv_path,controller_path,lean_path,base/"StorageObstruction.lean",base/"StorageObstruction.olean"]
result = dict(status="ALL_17_ROWS_AND_ACTUAL_KP_MATCH_EXACTLY", rows=17,
              csv_fields=fields, original_csv_rows=expected, Kp=list(map(str,lean_kp)),
              both_conjugates_counted_once=True, imaginary_parts_zero=True,
              physical_DH_identification_proved=False,
              sha256={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs})
args.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
print(result["status"])
for path,digest in result["sha256"].items():
    print(digest,path)
