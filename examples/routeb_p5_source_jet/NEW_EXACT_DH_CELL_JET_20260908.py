"""Read-only exact polynomial jet extraction; not source/kernel admission.

Uses only the Python standard library. No external writes, Float64, eval,
Julia execution, inverse construction, or fabricated metric/residual fields.
Default stdout is a compact receipt; --emit includes exact coefficient tables.
Exit 2 means the complete P5 source packet remains missing, not arithmetic failure.
"""
import argparse
import csv
import hashlib
import json
import re
from fractions import Fraction as Q
from pathlib import Path

FILES = {
    'routeB_dense_Mq/routeB_compact_dh_gain_descriptor_regeneration_audit.jl': '04B764434601DD0C11B2A6554156FD4D948CF742DBF33472B960E0D54E8235C9',
    'routeB_dense_Mq/routeB_fourier_lifted_descriptor_model.jl': '0FCF733144B3D7B1B08F328FE4AD24477057C56976F0EF53633C450D8FC4729D',
    'routeB_dense_Mq/routeB_analytic_mass_full_cs_polynomial.csv': '1A1DB0B737ABAC58AFAE06E95766D2DA91C12425FE1BE388364F1DCA7DB59451',
    'routeB_dense_Mq/routeB_analytic_gravity_cs_polynomial.csv': '2760489CBA6DC2F2D25AC8F33FA5A25E430BB92040C022004D1EF949D3E09C5D',
    'routeB_dense_Mq/routeB_analytic_coriolis_cs_polynomial.csv': 'CDC587AFD26B2AB5498C5917E8C620E7C9AADA8B2F5B4128C88DF14E78B4E4BB',
    'robot_formal_v1/interval_bounds/half_active_vanis2_domain_probe.json': '28710E24C1528F98B3E0B54B388836824B11E6DE8E19491737B6C85BF6FF2D1E',
}
N = 25  # q1..q6, v1..v6, w, c1,s1,...,c6,s6
ZERO = (0,) * N


def add(*polys):
    out = {}
    for poly in polys:
        for ex, coeff in poly.items():
            out[ex] = out.get(ex, Q(0)) + coeff
    return {ex: c for ex, c in out.items() if c}


def scale(poly, coeff):
    return {ex: c * coeff for ex, c in poly.items() if c * coeff}


def times_var(poly, index):
    out = {}
    for ex, c in poly.items():
        e = list(ex)
        e[index] += 1
        out[tuple(e)] = c
    return out


def partial(poly, index):
    out = {}
    for ex, c in poly.items():
        if ex[index]:
            e = list(ex)
            e[index] -= 1
            out[tuple(e)] = c * ex[index]
    return out


def physical_derivative(poly, index):
    # Pullback to c_i=cos(q_i), s_i=sin(q_i), not independent lift partials.
    if index >= 6:
        return partial(poly, index)
    ci, si = 13 + 2 * index, 14 + 2 * index
    return add(partial(poly, index), scale(times_var(partial(poly, ci), si), -1),
               times_var(partial(poly, si), ci))


def load_rows(root, name):
    with (root / 'routeB_dense_Mq' / name).open(newline='', encoding='utf-8-sig') as f:
        for row in csv.DictReader(f):
            ex = [0] * 13 + [int(row['e' + str(i)]) for i in range(1, 13)]
            if min(ex) < 0:
                raise ValueError('negative exponent')
            yield row, {tuple(ex): Q(int(row['num']), int(row['den']))}


def gain_vector(source, name):
    match = re.search(r'const ' + name + r' = Q\[([^\]]+)\]', source)
    if not match:
        raise ValueError('missing actual gain definition: ' + name)
    body = match.group(1)
    tokens = re.findall(r'Q\(\s*(-?\d+)\s*(?:,\s*(\d+)\s*)?\)', body)
    if re.sub(r'Q\(\s*-?\d+\s*(?:,\s*\d+\s*)?\)|[\s,]', '', body):
        raise ValueError('unsupported gain syntax')
    result = [Q(int(n), int(d or 1)) for n, d in tokens]
    if len(result) != 6:
        raise ValueError('gain dimension')
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('source_root', type=Path)
    ap.add_argument('--emit', action='store_true')
    args = ap.parse_args()
    root = args.source_root.resolve()
    for rel, expected in FILES.items():
        if hashlib.sha256((root / rel).read_bytes()).hexdigest().upper() != expected:
            raise ValueError('INPUT_HASH_MISMATCH: ' + rel)
    domain = json.loads((root / list(FILES)[-1]).read_text())
    for rel, digest in domain['source_hashes'].items():
        if FILES.get(rel, '').lower() != digest.lower():
            raise ValueError('CELL_SOURCE_HASH_MISMATCH: ' + rel)
    source = (root / list(FILES)[0]).read_text()
    kp, damping, gw = (gain_vector(source, n) for n in ('Kp_DH', 'd_DH', 'GwI_DH'))
    M = [[{} for _ in range(6)] for _ in range(6)]
    gravity, coriolis = [{} for _ in range(6)], [{} for _ in range(6)]
    for row, p in load_rows(root, 'routeB_analytic_mass_full_cs_polynomial.csv'):
        i, j = int(row['row']) - 1, int(row['col']) - 1
        M[i][j] = add(M[i][j], p)
    for i in range(6):
        M[i][i] = add(M[i][i], {ZERO: Q(1, 1000000)})
    for row, p in load_rows(root, 'routeB_analytic_gravity_cs_polynomial.csv'):
        i = int(row['row']) - 1
        gravity[i] = add(gravity[i], p)
    for row, p in load_rows(root, 'routeB_analytic_coriolis_cs_polynomial.csv'):
        i = int(row['row']) - 1
        p = times_var(times_var(p, 5 + int(row['dq_j'])), 5 + int(row['dq_k']))
        coriolis[i] = add(coriolis[i], p)
    # q=0 implies c=1,s=0, exactly as the imported g0 definition.
    g0 = [sum((c for ex, c in p.items() if all(ex[j] == 0 for j in range(14, 25, 2))), Q(0))
          for p in gravity]
    R = [add(scale(times_var({ZERO: Q(1)}, i), -kp[i]),
             scale(times_var({ZERO: Q(1)}, 6+i), -damping[i]),
             scale(times_var({ZERO: Q(1)}, 12), gw[i]), {ZERO: g0[i]},
             scale(coriolis[i], -1), scale(gravity[i], -1)) for i in range(6)]
    jets = {}
    for i in range(6):
        jets[f'R[{i}]'] = R[i]
        for k in range(13):
            jets[f'DR[{i},{k}]'] = physical_derivative(R[i], k)
        for j in range(6):
            jets[f'M[{i},{j}]'] = M[i][j]
            for k in range(6):
                jets[f'DM[{i},{j},{k}]'] = physical_derivative(M[i][j], k)
    encoded = {key: [[list(ex), str(c.numerator), str(c.denominator)]
                     for ex, c in sorted(poly.items())] for key, poly in sorted(jets.items())}
    digest = hashlib.sha256(json.dumps(encoded, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    report = dict(status='EXACT_JET_EXTRACTION_ONLY_PENDING', source_files=FILES,
                  cell=list(FILES)[-1], domain_scope=domain['scope'],
                  variables=[f'q{i}' for i in range(1, 7)] + [f'v{i}' for i in range(1, 7)] + ['w'] +
                            [s + str(i) for i in range(1, 7) for s in ('c', 's')],
                  polynomial_count=len(jets), term_count=sum(map(len, jets.values())),
                  coefficient_tables_sha256=digest,
                  conditional_contract={
                      'state': 'x=(q,v), input w separate; direction h=(h_q,h_v,h_w)',
                      'acceleration': 'alpha: M(q)*alpha=R(q,v,w)',
                      'directional_mass': 'DM[h_q]=sum_k DM[:,:,k]*h_q[k]',
                      'directional_rhs': 'DR[h]=sum_k DR[:,k]*h[k]',
                      'acceleration_jet': 'M*Dalpha[h]=DR[h]-DM[h_q]*alpha',
                      'vector_field_jet': 'f=(v,alpha); Df[h]=(h_v,Dalpha[h]); P5 F=-f if b=0 is separately justified',
                      'regularity_guard': 'invertible M and differentiable source on an open neighborhood of the same cell',
                      'metric_jet': 'W(t,x), Wt, DW[h] require separately bound actual metric; no default W',
                      'base_split': 'f_actual=-F+b; Db=D(f_actual)+DF; extra e excludes Db*xi',
                  },
                  missing=['same-cell acceleration solution and differentiability',
                           'Da solution of differentiated descriptor', 'actual W,Wt,DW carrier binding',
                           'actual/nominal b,Db and additional variational e',
                           'input-law/time and whole-tube coverage', 'source semantic certification'],
                  source_binding_proven=False, formal_certificate_allowed=False, admission='pending')
    if args.emit:
        report['coefficient_tables'] = encoded
    print(json.dumps(report, sort_keys=True, indent=2))
    return 2


if __name__ == '__main__':
    raise SystemExit(main())
