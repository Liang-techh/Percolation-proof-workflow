"""One stdlib-only exact coefficient / endpoint candidate calculation.

Run saved copy through verify.py. No imports from the workspace; no trajectories.
"""
from fractions import Fraction as F
from pathlib import Path
from math import factorial
import csv
import hashlib
import json

RUN = Path(__file__).resolve().parent


def matrix(a):
    return [[F(x) for x in row] for row in a]


def zeros(n, m):
    return [[F(0) for _ in range(m)] for _ in range(n)]


def tr(a):
    return list(map(list, zip(*a)))


def mul(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def add(a, b):
    return [[x+y for x, y in zip(r, s)] for r, s in zip(a, b)]


def scale(a, s):
    return [[s*x for x in r] for r in a]


def diag(xs):
    return [[x if i == j else F(0) for j in range(len(xs))] for i, x in enumerate(xs)]


def inverse(a):
    n = len(a)
    t = [r[:] + [F(i == j) for j in range(n)] for i, r in enumerate(a)]
    for j in range(n):
        p = next(i for i in range(j, n) if t[i][j])
        t[j], t[p] = t[p], t[j]
        pivot = t[j][j]
        t[j] = [v/pivot for v in t[j]]
        for i in range(n):
            if i != j:
                coeff = t[i][j]
                t[i] = [x-coeff*y for x, y in zip(t[i], t[j])]
    return [r[n:] for r in t]


def quad(a, x):
    return sum(x[i]*a[i][j]*x[j] for i in range(len(x)) for j in range(len(x)))


def load(name):
    return json.loads((RUN/'inputs'/name).read_text(encoding='utf-8'))


def restricted_fourier(name, predicate=lambda row: True):
    """Exact coefficients on q=(0,u,0,0,0,0), grouped before enclosure."""
    out = {}
    with (RUN/'inputs'/name).open(encoding='utf-8-sig', newline='') as f:
        for row in csv.DictReader(f):
            if not predicate(row):
                continue
            nu = int(row['nu2'])
            a, b = out.get(nu, (F(0), F(0)))
            out[nu] = (a+F(int(row['real_num']), int(row['real_den'])),
                       b+F(int(row['imag_num']), int(row['imag_den'])))
    return {n: p for n, p in out.items() if p != (0, 0)}


def main():
    before = json.loads((RUN/'before_run.json').read_text(encoding='utf-8'))
    for name, record in before['snapshots'].items():
        assert hashlib.sha256((RUN/name).read_bytes()).hexdigest() == record['sha256']
    ref = load('reference.json')
    audit = load('audit_results.json')
    rows = matrix(load('functionals.json')['rows'])
    supports = load('nominal_J_functional_bounds.json')['cells'][-1]
    M, R, H, A14 = map(matrix, (ref['M0'], ref['M0_inverse'], ref['H0'], ref['augmented_A14']))
    K, D, G = diag(list(map(F, ref['Kp']))), diag(list(map(F, ref['D']))), list(map(F, ref['G']))
    S = add(K, H)
    beta, sigma, radius = F(8, 5), F(1, 64), F(3, 20)
    Q = diag(list(map(F, ('3', '8', '95/7', '165/7', '45', '90'))))
    Q[1][2] = Q[2][1] = F(-5)
    L = inverse(Q)
    assert mul(Q, L) == diag([F(1)]*6) == mul(M, R)
    aa = A14[6:12]
    expected_aa = mul(R, [[-S[i][j] for j in range(6)] +
                          [-D[i][j] for j in range(6)] + [G[i], F(0)] for i in range(6)])
    assert aa == expected_aa
    P = zeros(14, 14)
    for i in range(6):
        for j in range(6):
            P[i][j] = beta*S[i][j]/2
            P[i][6+j] = P[6+j][i] = S[i][j]
            P[6+i][6+j] = D[i][j]+beta*M[i][j]/2
        P[i][12] = P[12][i] = -beta*G[i]/2
        P[i][13] = P[13][i] = G[i]
        P[6+i][12] = P[12][6+i] = -G[i]
    assert P == tr(P)
    gmap = [row[:] for row in P[6:12]]
    for i in range(6):
        for j in range(6):
            gmap[i][6+j] -= beta*M[i][j]/2
    assert gmap == scale(mul(M, aa), F(-1))
    W = add(scale(D, beta), scale(S, F(-2)))
    diagonal_W0 = [F(2,25), F(4,25), F(3,25), F(2,25), F(1,25), F(0)]
    assert W == add(diag(diagonal_W0), scale(H, F(-2)))
    ga, gb, gc = F(762237,200000), F(242307,200000), F(20601,400000)
    def outer(x): return [[a*b for b in x] for a in x]
    e2, e23, e235 = [0,1,0,0,0,0], [0,1,1,0,0,0], [0,1,1,0,1,0]
    assert H == add(add(scale(outer(e2), -ga), scale(outer(e23), -gb)), scale(outer(e235), -gc))
    target = scale(mul(mul(tr(aa), M), aa), F(-2))
    for i in range(6):
        for j in range(6): target[6+i][6+j] -= W[i][j]
        target[i][13] -= beta*G[i]/2
        target[13][i] -= beta*G[i]/2
    assert add(mul(tr(A14), P), mul(P, A14)) == target

    # Entire original initial ball and one ramp parameter, no coordinate box.
    row_bound = max(P[i][i]+sum(abs(P[i][j]) for j in range(12) if j != i) for i in range(12))
    assert sum(g*g for g in G) <= F(6,5)**2 and 3 <= F(7,4)**2
    source_initial_lower = F(audit['initial_ball']['lower'])
    initial_upper_normalized = radius**2*row_bound+2*radius*F(7,4)*F(6,5)-beta*source_initial_lower

    # ONE prospectively fixed endpoint state; no adaptive state search.
    star = [F(0)]*14
    star[1] = star[7] = F(2)
    caps = [F(n)+F(k) for n, k in zip(supports['nominal'], supports['kernel_sqrt'])]
    slacks = [cap-abs(sum(a*b for a, b in zip(row, star))) for cap, row in zip(caps, rows)]
    support_pass = all(s >= 0 for s in slacks)
    restricted_m22 = restricted_fourier('mass.csv', lambda row: row['row'] == row['col'] == '2')
    assert restricted_m22 == {0: (M[1][1]-F(1,1000000), F(0))}
    upoly = restricted_fourier('potential.csv')
    total = ga+gb+gc
    assert upoly == {0: (F(10791,4000),F(0)), -1: (total/2,F(0)), 1: (total/2,F(0))}
    # Taylor-Lagrange |cos(2)-sum_{j=0}^12 (-1)^j 2^(2j)/(2j)!| <= 2^25/25!.
    cos_center = sum(F((-1)**j*2**(2*j), factorial(2*j)) for j in range(13))
    cos_error = F(2**25, factorial(25))
    cos_lo, cos_hi = cos_center-cos_error, cos_center+cos_error
    assert cos_hi < F(-2,5)
    constant = beta*(2*M[1][1]+2*K[1][1])+8*S[1][1]+4*D[1][1]
    vstar_lo, vstar_hi = constant+beta*total*(cos_lo-1), constant+beta*total*(cos_hi-1)
    assert vstar_hi < -36
    # Cross-check via the actual candidate and its signed gap at this state.
    Rpot_lo = total*(2+cos_lo-1)
    assert quad(P, star)+beta*Rpot_lo == vstar_lo
    metric_match = mul(mul(L, R), D)
    skew_witness = next((i,j,metric_match[i][j]-metric_match[j][i])
                        for i in range(6) for j in range(i+1,6)
                        if metric_match[i][j] != metric_match[j][i])
    sgap_hi = F(audit['endpoint_summary']['conditional_J1']['uniform_upper'])
    result = dict(
        status='EXACT_STORAGE_COEFFICIENTS_AND_SINGLE_OUTER_ENDPOINT_CANDIDATE_EVIDENCE',
        original_revision=46, horizon='1', sigma=sigma, k=-beta*sigma,
        Pbar=P, P_selected=scale(P,sigma), W=W, L=L,
        coefficient_checks=dict(full_A14=True, g_minus_M0_a0=True,
                                derivative_all_196_entries=True, W_exact_nonnegative_squares=True),
        initial=dict(Pxx_row_upper=row_bound, normalized_upper=initial_upper_normalized,
                     selected_upper=sigma*initial_upper_normalized,
                     selected_upper_display=float(sigma*initial_upper_normalized)),
        signed_gap_only_endpoint_charge=dict(normalized=beta*(sgap_hi-source_initial_lower),
                                             selected=sigma*beta*(sgap_hi-source_initial_lower)),
        endpoint_test=dict(state=star,time_cell=supports['time'], all97_supports_pass=support_pass,
                           minimum_support_slack=min(slacks),cos2_interval=[cos_lo,cos_hi],
                           Vbar_interval=[vstar_lo,vstar_hi],Vbar_display=[float(vstar_lo),float(vstar_hi)],
                           selected_V_interval=[sigma*vstar_lo,sigma*vstar_hi],
                           selected_V_display=[float(sigma*vstar_lo),float(sigma*vstar_hi)],
                           rejected_scale_class='sigma>=1/36' if support_pass else None,
                           rejection_scope='Nonnegative time-only supply and uniform terminal storage lower bound over this 97-support outer set; not actual reachability or actual J.'),
        metric_matching_obstruction=dict(indices_one_based=[skew_witness[0]+1,skew_witness[1]+1],
                                         L_R_D_minus_transpose_entry=skew_witness[2]),
        full_J1_proved=False, uniform_scalar_gate_proved=False, endpoint_lower_bound_proved=False,
        Lean_verified=False, source_implementation_binding_proved=False,
        trajectories=0, solvers=0, searched_points=0, fixed_test_points=1)
    (RUN/'candidate_evidence.json').write_text(json.dumps(result, default=str, indent=2)+'\n',encoding='utf-8')
    print('Exact full reference/storage coefficient checks: PASS', flush=True)
    print('Initial upper:',result['initial']['selected_upper'],float(sigma*initial_upper_normalized),flush=True)
    print('One fixed endpoint, 97 supports:',support_pass,'minimum slack',min(slacks),flush=True)
    print('Normalized endpoint V interval (display):',result['endpoint_test']['Vbar_display'],flush=True)
    print('Selected endpoint V interval (display):',result['endpoint_test']['selected_V_display'],flush=True)
    print('Scale class rejected:',result['endpoint_test']['rejected_scale_class'],flush=True)
    print('Metric-matched g=-L*a0 skew witness:',skew_witness,flush=True)
    print('Full T=1 actual J<=1: OPEN',flush=True)


if __name__ == '__main__':
    main()
