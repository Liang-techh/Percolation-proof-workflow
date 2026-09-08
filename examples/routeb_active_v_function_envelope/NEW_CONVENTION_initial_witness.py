"""Exact certificate-indexed initial bound, not a runtime or admission receipt.

Reads pinned Route-B files only. No producer imports, numeric optimization,
trig, old obstruction audit, Julia, Lean or file writes. Python -B recommended.
"""
import csv
from fractions import Fraction as Q
from hashlib import sha256
import io
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
ROOT = Path('C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq')
PINS = {
    'routeB_certificate_V.csv': 'cab4a5182981bccbde18ace2d26ece5c0d7b7d3c3cf4a5a7e02e7fcda9b80601',
    'routeB_export_traj.jl': '35ebe806a46273068af1af937c0c0152378d6889024ec5586bf3c7aabd30eccf',
    'routeB_pmi_certificate.jl': '235f4876ed1a3343f6d84f83c0079b4d279886585dc36aeb55b9fc0289177a77',
    'routeB_compact_energy_storage_to_block_audit.py': '80795ef4fcbe0da4fb6d491f040e69196323fc09b01cf5739cb197343ef766b9',
    'routeB_compact_energy_storage_to_block_audit.csv': '8d37219ea1b6189ec84e2eec16aa4fe29e2ee4bd263b946a639fafb7692b2bf1',
    'routeB_compact_block_energy_barrier_audit.py': '62972f8b2049be3351616e25837db722731744f8e3b219d2ddf90fd817026927',
}
ORDER = ['e_qa', 'e_qb', 'e_dqa', 'e_dqb', 'e_t']


def require(condition, message):
    if not condition:
        raise ValueError(message)


def bound(rows, mode):
    polynomial = {}
    for row in rows:
        exps = tuple(Q(row[k]) for k in ORDER)
        require(all(e.denominator == 1 and e >= 0 for e in exps), 'invalid exponent')
        require(sum(exps) <= 4, 'unexpected degree')
        coefficient = Q(row['coeff']) if mode == 'decimal_token_real' else Q.from_float(float(row['coeff']))
        if exps[4] != 0:
            continue  # EXACT substitution t0=0, before polynomial evaluation
        key = tuple(int(e) for e in exps[:4])
        polynomial[key] = polynomial.get(key, Q(0)) + coefficient
    matrix = [[Q(0) for _ in range(4)] for _ in range(4)]
    abs_sums = {1: Q(0), 3: Q(0), 4: Q(0)}
    for exps, c in polynomial.items():
        degree = sum(exps)
        if degree == 2:
            i, j = [i for i, exponent in enumerate(exps) for _ in range(exponent)]
            if i == j:
                matrix[i][i] += c
            else:
                matrix[i][j] += c/2
                matrix[j][i] += c/2
        elif degree:
            abs_sums[degree] += abs(c)
    # Check the exact coefficient-to-symmetric-matrix reconstruction.
    for exps, c in polynomial.items():
        if sum(exps) == 2:
            i, j = [i for i, exponent in enumerate(exps) for _ in range(exponent)]
            require((matrix[i][i] if i == j else 2*matrix[i][j]) == c, 'quadratic mismatch')
    row_upper = [matrix[i][i]+sum(abs(matrix[i][j]) for j in range(4) if j != i) for i in range(4)]
    lam = max([Q(0)] + row_upper)
    r = Q(3, 20)
    constant = polynomial.get((0, 0, 0, 0), Q(0))
    losses = {degree: value*r**degree for degree, value in abs_sums.items()}
    upper = constant + lam*r*r + sum(losses.values())
    require(upper <= Q(-1, 20), 'proposed coarse initial upper not established')
    return {
        't0_polynomial': [{'exponents': list(e), 'coefficient': str(c)} for e,c in sorted(polynomial.items())],
        'quadratic_matrix': [[str(x) for x in row] for row in matrix],
        'quadratic_row_upper': [str(x) for x in row_upper],
        'lambda': str(lam), 'constant': str(constant),
        'nonquadratic_absolute_sums': {str(k): str(v) for k,v in abs_sums.items()},
        'nonquadratic_losses': {str(k): str(v) for k,v in losses.items()},
        'exact_assembled_upper': str(upper), 'coarse_initial_upper': '-1/20',
        'slack_to_coarse_upper': str(Q(-1,20)-upper),
    }


def audit():
    sources = {}
    for name, expected in PINS.items():
        raw = (ROOT/name).read_bytes()
        require(sha256(raw).hexdigest() == expected, 'source drift: '+name)
        sources[name] = raw.decode('utf-8')
    reader = csv.DictReader(io.StringIO(sources['routeB_certificate_V.csv']))
    require(reader.fieldnames == ['coeff']+ORDER, 'wrong coefficient column order')
    rows = list(reader)
    require(len(rows) == 46 and all(None not in r and all(v is not None for v in r.values()) for r in rows), 'malformed table')
    scalar_rows = list(csv.DictReader(io.StringIO(sources['routeB_compact_energy_storage_to_block_audit.csv'])))
    selected = [r for r in scalar_rows if r['metric'] == 'initial_storage_upper']
    require(len(selected) == 1, 'upper selector missing or ambiguous')
    u = Q(selected[0]['value'])
    require(u > 0, 'upper sign')
    # Syntactic file/selector associations, not executed source-read evidence.
    require('V0 = frac(storage["initial_storage_upper"])' in sources['routeB_compact_block_energy_barrier_audit.py'], 'consumer selector drift')
    require('x1, x2, x3, x4, x5 = qv[4], qv[5], dqv[4], dqv[5], tv' in sources['routeB_export_traj.jl'], 'runtime variable map drift')
    return {
        'status': 'pending', 'result': 'EXACT_CERTIFICATE_INDEXED_IDEAL_INITIAL_UPPER',
        'source_sha256': PINS, 'variable_order': ['q4','q5','v4','v5','t'],
        'time0': '0', 'radius_squared': '9/400',
        'X0': 'q4^2+q5^2+v4^2+v5^2<=9/400; all other q/v coordinates zero',
        'upper_selector': {'artifact': 'routeB_compact_energy_storage_to_block_audit.csv', 'metric': 'initial_storage_upper', 'value': str(u)},
        'interpretations': {mode: bound(rows, mode) for mode in ['decimal_token_real', 'python_binary64_decoded_real']},
        'claim': 'For every x in X0, the specified ideal coefficient polynomial at t=0 is <= -1/20 < 0 < selected upper.',
        'historical_producer_function_binding': None, 'same_run_event_binding': None,
        'consumer_function_identity': None, 'runtime_evaluation_observation': None,
        'source_binding_proven': False, 'runtime_initial_bound_proven': False,
        'julia_execution': False, 'lean_lake_execution': False,
        'registry_eligible': False, 'formal_certificate_allowed': False,
    }


if __name__ == '__main__':
    print(json.dumps(audit(), indent=2))
