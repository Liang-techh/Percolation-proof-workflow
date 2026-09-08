"""Read-only exact-rational audit of a uniform raw-Vfull lower envelope.

No Julia, Lean, numerical trig, runtime observations or file writes.
CLI success is arithmetic checking only; admission always remains pending.
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
    'routeB_analytic_mass_full_cs_polynomial.csv': '1a1db0b737abac58afae06e95766d2da91c12425fe1be388364f1dca7db59451',
    'routeB_analytic_gravity_cs_polynomial.csv': '2760489cba6dc2f2d25ac8f33fa5a25e430bb92040c022004d1ef949d3e09c5d',
    'routeB_compact_energy_storage_to_block_audit.csv': '8d37219ea1b6189ec84e2eec16aa4fe29e2ee4bd263b946a639fafb7692b2bf1',
    'routeB_compact_energy_storage_to_block_audit.py': '80795ef4fcbe0da4fb6d491f040e69196323fc09b01cf5739cb197343ef766b9',
    'routeB_compact_dh_full_energy_supply_split_audit.jl': 'd6d9bd3131d73fddf946f8652458b04c628f76471d497b2a52a49f0335b30632',
    'routeB_compact_dh_gain_descriptor_regeneration_audit.jl': '04b764434601dd0c11b2a6554156fd4d948cf742dbf33472b960e0d54e8235c9',
    'routeB_fourier_lifted_descriptor_model.jl': '0fcf733144b3d7b1b08f328fe4ad24477057c56976f0ef53633c450d8fc4729d',
}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def read_pinned(root):
    out = {}
    for name, digest in PINS.items():
        raw = (root / name).read_bytes()
        require(sha256(raw).hexdigest() == digest, 'source drift: ' + name)
        out[name] = raw.decode('utf-8')
    return out


def terms(text):
    for row in csv.DictReader(io.StringIO(text)):
        exps = tuple(int(row['e' + str(i)]) for i in range(1, 13))
        require(all(e >= 0 for e in exps), 'non-polynomial exponent')
        yield row, exps, Q(int(row['num']), int(row['den']))


def audit(root=ROOT):
    src = read_pinned(root)
    # Exact source tokens locate the value convention; they are not runtime proof.
    require('Vfull_DH = Kfull_DH + Ugrav_DH + Uctrl_DH' in src['routeB_compact_dh_full_energy_supply_split_audit.jl'], 'raw value assignment')
    require('sum(g0[i] * q[i] for i in 1:6)' in src['routeB_compact_dh_full_energy_supply_split_audit.jl'], 'linear compensation')
    require('M[i, i] += Q(1, 1_000_000)' in src['routeB_fourier_lifted_descriptor_model.jl'], 'regularizer source')
    require('INITIAL_RADIUS = Q(3, 20)' in src['routeB_compact_energy_storage_to_block_audit.py'], 'radius source')
    regen = src['routeB_compact_dh_gain_descriptor_regeneration_audit.jl']
    for token in ('A0_grav_DH = Q(762237, 200000)', 'Agrav_DH = Q(242307, 200000)', 'Bgrav_DH = Q(20601, 400000)'):
        require(token in regen, 'potential coefficient source')
    # On X0, q1,q2,q3,q6=0; only q4,q5 trig factors remain.
    polys = {(i, j): {} for i in (4, 5) for j in (4, 5)}
    for row, exps, coefficient in terms(src['routeB_analytic_mass_full_cs_polynomial.csv']):
        ij = int(row['row']), int(row['col'])
        if ij not in polys or any(exps[2*j-1] for j in (1, 2, 3, 6)):
            continue
        key = exps[6:10]
        polys[ij][key] = polys[ij].get(key, Q(0)) + coefficient
    mu = Q(1, 1000000)
    for i in (4, 5):
        polys[i, i][(0, 0, 0, 0)] = polys[i, i].get((0, 0, 0, 0), Q(0)) + mu
    entry_abs = {ij: sum(map(abs, poly.values()), Q(0)) for ij, poly in polys.items()}
    # max(row norm, column norm) bounds the Euclidean operator norm; no SPD assumption.
    m = max([sum(entry_abs[i, j] for j in (4, 5)) for i in (4, 5)] +
            [sum(entry_abs[i, j] for i in (4, 5)) for j in (4, 5)])
    g = [Q(0) for _ in range(6)]
    for row, exps, coefficient in terms(src['routeB_analytic_gravity_cs_polynomial.csv']):
        if not any(exps[1::2]):
            g[int(row['row'])-1] += coefficient
    # The source defines g0 by this analytic substitution; no FD-zero claim.
    r = Q(3, 20)
    a0, a, b = Q(762237, 200000), Q(242307, 200000), Q(20601, 400000)
    require(b > 0 and m >= 0, 'signs for envelope')
    potential_lower = a0 + a + b*(1-r*r/2)
    kinetic_loss = m*r*r/2
    linear_loss = r*(abs(g[3])+abs(g[4]))
    lower = potential_lower-kinetic_loss-linear_loss
    rows = list(csv.DictReader(io.StringIO(src['routeB_compact_energy_storage_to_block_audit.csv'])))
    selected = [row['value'] for row in rows if row['metric'] == 'initial_storage_upper']
    require(len(selected) == 1, 'unique initial scalar')
    upper = Q(selected[0].replace('//', '/'))
    require(lower > upper, 'no strict uniform obstruction certified by this envelope')
    return {
        'status': 'pending', 'result': 'UNIFORM_RAW_IDEAL_EXPRESSION_LOWER_EXCEEDS_RECORDED_UPPER',
        'target': 'raw Vfull_DH; fixed pinned analytic configuration; no cross term',
        'domain': 'q/v outside joints4,5 zero; q4^2+q5^2+v4^2+v5^2 <= (3/20)^2; physical trig lift',
        'source_sha256': PINS, 'regularizer': str(mu), 'radius': str(r),
        'mass_entry_absolute_envelopes': {str(ij): str(v) for ij, v in entry_abs.items()},
        'mass_operator_upper': str(m), 'analytic_g0': list(map(str, g)),
        'potential_lower': str(potential_lower), 'kinetic_absolute_loss': str(kinetic_loss),
        'linear_absolute_loss': str(linear_loss), 'uniform_W_lower': str(lower),
        'recorded_initial_upper': str(upper), 'strict_separation': str(lower-upper),
        'uniform_claim': 'For every x in X0, W_K(embed_K(x)) >= uniform_W_lower > recorded_initial_upper, conditional on the stated ideal-expression/source binding.',
        'arithmetic_checks_pass': True, 'lean_julia_run': False,
        'source_binding_proven': False, 'runtime_observation': None,
        'registry_eligible': False, 'formal_certificate_allowed': False,
    }


if __name__ == '__main__':
    print(json.dumps(audit(), indent=2, ensure_ascii=False))
