"""Read-only finite algebra obstruction to certificate/energy sameStorage.

Not a Julia execution, initial-bound audit, source theorem or admission gate.
Python binary64 decoding is explicitly not evidence of Julia parse/evaluation.
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
CSV_HASH = 'cab4a5182981bccbde18ace2d26ece5c0d7b7d3c3cf4a5a7e02e7fcda9b80601'
KEYS = ['e_qa', 'e_qb', 'e_dqa', 'e_dqb', 'e_t']


def audit():
    raw = (ROOT / 'routeB_certificate_V.csv').read_bytes()
    if sha256(raw).hexdigest() != CSV_HASH:
        raise ValueError('certificate CSV drift')
    reader = csv.DictReader(io.StringIO(raw.decode('utf-8')))
    if reader.fieldnames != ['coeff'] + KEYS:
        raise ValueError('unexpected CSV header')
    polynomials = {'decimal_token_real': {}, 'python_binary64_decoded_real': {}}
    count = 0
    for row in reader:
        count += 1
        exps = [Q(row[k]) for k in KEYS]
        if any(e.denominator != 1 or e < 0 for e in exps):
            raise ValueError('noninteger or negative exponent')
        decimal = Q(row['coeff'])
        binary = Q.from_float(float(row['coeff']))
        if any(exps[1:]):
            continue  # q5=v4=v5=t=0, q4 remains a variable
        degree = int(exps[0])
        if degree > 4:
            raise ValueError('restricted degree exceeds fourth-difference witness')
        for key, value in [('decimal_token_real', decimal), ('python_binary64_decoded_real', binary)]:
            p = polynomials[key]
            p[degree] = p.get(degree, Q(0)) + value
    # Exact five-node functional on the existing X0 slice, not runtime samples.
    points = [Q(-3,20), Q(-3,40), Q(0), Q(3,40), Q(3,20)]
    weights = [1, -4, 6, -4, 1]
    moments = [sum(w*s**k for w,s in zip(weights,points)) for k in range(5)]
    if moments[:4] != [0]*4 or moments[4] != 24*Q(3,40)**4:
        raise ValueError('incorrect finite-difference functional')
    if not all(s*s <= Q(9,400) for s in points):
        raise ValueError('witness outside X0 slice')
    witnesses = {}
    for interpretation, p in polynomials.items():
        c4 = p.get(4, Q(0))
        functional = sum(c*moments[k] for k,c in p.items())
        if c4 == 0 or functional != 24*Q(3,40)**4*c4 or functional == 0:
            raise ValueError('nonidentity obstruction absent')
        witnesses[interpretation] = {
            'restricted_coefficients': {str(k): str(v) for k,v in sorted(p.items())},
            'fourth_difference': str(functional),
            'cannot_agree_with_any_degree_le_2_polynomial_at_all_five_points': True,
        }
    return {
        'status': 'pending', 'source_binding_proven': False,
        'scope': 'finite exact algebra on pinned certificate; energy slice is an external source premise',
        'certificate_sha256': CSV_HASH, 'row_count': count,
        'slice': 't=0, q4=s, every other q/v coordinate zero',
        'points': [str(s) for s in points], 'weights': weights,
        'moments_degree_0_through_4': [str(m) for m in moments],
        'witnesses': witnesses,
        'consumer_rule': 'Given the same-K energy slice degree <=2, reject its exact sameStorage edge to this certificate; do not reject unrelated initial inequalities.',
        'same_run_initial_upper_binding': None,
        'julia_execution': False, 'lean_lake_execution': False,
        'runtime_evaluation_observation': None, 'registry_eligible': False,
        'formal_certificate_allowed': False,
    }


if __name__ == '__main__':
    print(json.dumps(audit(), indent=2))
