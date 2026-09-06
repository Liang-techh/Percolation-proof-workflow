"""Narrow exact source/Lean-literal audit. No simulation or registry writes."""
import csv
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import re
import sys

run = Path(sys.argv[1]).resolve()
ref = json.loads((run / 'inputs/reference/reference.json').read_text())
source = (run / 'ReferenceMass.lean').read_text()

def literal(name):
    block = source.split('def ' + name + ' : Mat 6 := ![', 1)[1].split('\n\n', 1)[0]
    rows = re.findall(r'!\[([^\]]+)\]', block)
    result = [[Q(x.strip()) for x in row.split(',')] for row in rows]
    assert len(result) == 6 and all(len(row) == 6 for row in result)
    return result

mass = literal('M0')
hessian = literal('H0')
assert mass == [[Q(x) for x in row] for row in ref['M0']]
assert hessian == [[Q(x) for x in row] for row in ref['H0']]
csv_mass = [[Q(i == j, 1000000) for j in range(6)] for i in range(6)]
imag = [[Q(0) for j in range(6)] for i in range(6)]
with (run / 'inputs/reference/routeB_fourier_mass_full_rational.csv').open() as f:
    rows = list(csv.DictReader(f))
assert len(rows) == 610
for r in rows:
    i, j = int(r['row'])-1, int(r['col'])-1
    csv_mass[i][j] += Q(int(r['real_num']), int(r['real_den']))
    imag[i][j] += Q(int(r['imag_num']), int(r['imag_den']))
assert mass == csv_mass and all(x == 0 for row in imag for x in row)
csv_hessian = [[Q(0) for _ in range(6)] for _ in range(6)]
with (run / 'inputs/gravity/routeB_fourier_potential_rational.csv').open() as f:
    potential_rows = list(csv.DictReader(f))
assert len(potential_rows) == 17
for r in potential_rows:
    a = Q(int(r['real_num']), int(r['real_den']))
    assert int(r['imag_num']) == 0
    nu = [int(r[f'nu{i+1}']) for i in range(6)]
    for i in range(6):
        for j in range(6):
            csv_hessian[i][j] -= a*nu[i]*nu[j]
assert hessian == csv_hessian
row_abs = [sum(map(abs, row)) for row in mass]
assert all(x < 1 for x in row_abs)
assert Q(9, 400)/2 + Q(3, 10000) == Q(231, 20000)
assert Q(56, 15)/40 == Q(7, 75)
result = dict(
    status='EXACT_SOURCE_LITERAL_AUDIT_PASSED',
    M0_row_abs_sums=list(map(str, row_abs)),
    I_minus_M0_diagonal_slacks=[str(1-x) for x in row_abs],
    mass_csv_rows=len(rows), potential_csv_rows=len(potential_rows),
    mass_regularizer='1/1000000 (explicit intended-real reference convention)',
    lean_M0_and_H0_equal_reference_and_CSV=True,
    initial_signed_gap_lower_bound='-3/10000: EXPLICIT UNPROVED AUDIT PREMISE',
    physical_DH_Float64_source_identification='UNPROVED',
    reference_sha256=hashlib.sha256((run / 'inputs/reference/reference.json').read_bytes()).hexdigest())
(run / 'source_audit.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2), flush=True)
