"""Targeted rational algebra for the J strategy; no integration or trajectories.

Reads existing source data; prints a receipt. Does not write any files.
Run: python -B examples/routeb_J_strategy/algebra_audit.py
"""
import importlib.util
import hashlib
import json
import argparse
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--inputs', type=Path)
args = parser.parse_args()
input_dir = args.inputs.resolve() if args.inputs else None
algebra_path = (input_dir / 'inertial_algebra.py' if input_dir else
                HERE.parent / 'routeb_inertial_structure/audit.py')
ref_path = (input_dir / 'reference.json' if input_dir else
            HERE.parent / 'routeb_coupled_linear_reference/output/'
            'run-20260905T192654Z-3dbe159f/reference.json')
spec = importlib.util.spec_from_file_location(
    "inertial_algebra", algebra_path)
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)
if input_dir:
    a.SRC = input_dir
ref = json.loads(ref_path.read_text())


def mm(x, y):
    return [[sum(u*v for u, v in zip(row, col)) for col in zip(*y)] for row in x]


def tr(x):
    return list(map(list, zip(*x)))


def at_zero(p):
    assert sum(z[1] for z in p.values()) == 0
    return sum((z[0] for z in p.values()), F(0))


ns = (0, 1, 1, 0, 0, 0)
nu = (0, 1, 0, 0, 0, 0)
nx = (0, 0, 0, 1, 0, 0)
ny = (0, 0, 0, 0, 1, 0)
np = tuple(i+j for i, j in zip(ns, ny))
A, B, C = F(762237, 200000), F(242307, 200000), F(20601, 400000)
P = a.product(a.trig(ns, True), a.add(a.const(1), a.scale(a.trig(nx), -1)),
              a.trig(ny, True))
U = a.load_poly(a.rows("routeB_fourier_potential_rational.csv"))
new_U = a.add(a.const(F(10791, 4000)), a.scale(a.trig(nu), A),
              a.scale(a.trig(ns), B), a.scale(a.trig(np), C), a.scale(P, C))
assert U == new_U
for i in range(6):
    assert a.diff(U, i) == a.diff(new_U, i)

# Radial gravity sector obstruction at q=t*d, d=(0,0,1,2,-1,0).
# q dot (H0 q - grad U) = k4*t^4 + O(t^6).
d = (0, 0, 1, 2, -1, 0)
k4 = -sum(re * sum(v*x for v, x in zip(freq, d))**4 / 6
          for freq, (re, im) in U.items())
tail6 = sum(abs(re) * abs(sum(v*x for v, x in zip(freq, d)))**6 / 120
            for freq, (re, im) in U.items())
assert k4 == (48*C-B)/6 and k4 > 0
# |t|<=1/20 fits the original full12 initial ball with v=0.
assert F(6, 400) <= F(9, 400)
radial_lower = k4-tail6/F(400)
assert radial_lower > 0

records = a.rows("routeB_fourier_mass_full_rational.csv")
M = [[a.load_poly([r for r in records if (int(r['row']), int(r['col'])) == (i+1,j+1)])
      for j in range(6)] for i in range(6)]
M0 = [[F(z) for z in row] for row in ref['M0']]
assert all(at_zero(M[i][j]) + (F(ref['mu']) if i == j else 0) == M0[i][j]
           for i in range(6) for j in range(6))
assert all(at_zero(a.diff(a.diff(U, i), j)) == F(ref['H0'][i][j])
           for i in range(6) for j in range(6))
# Exact coefficient of v4*v5 in C(0,v).
C45 = [at_zero(a.add(a.diff(M[i][3], 4), a.diff(M[i][4], 3),
                     a.scale(a.diff(M[3][4], i), -1))) for i in range(6)]
assert C45[0] == F(21, 25000)
C44 = [at_zero(a.add(a.diff(M[i][3], 3),
                     a.scale(a.diff(M[3][3], i), F(-1, 2)))) for i in range(6)]
C55 = [at_zero(a.add(a.diff(M[i][4], 4),
                     a.scale(a.diff(M[4][4], i), F(-1, 2)))) for i in range(6)]
C_equal = [u+v+w for u, v, w in zip(C44, C45, C55)]
assert C_equal[0] != 0

L = [[F(0) for j in range(6)] for i in range(6)]
for i, x in enumerate([F(1,3), F(19,117), F(56,585), F(7,165), F(1,45), F(1,90)]):
    L[i][i] = x
L[1][2] = L[2][1] = F(7,117)
Q = [[F(0) for j in range(6)] for i in range(6)]
for i, x in enumerate([F(3), F(8), F(95,7), F(165,7), F(45), F(90)]):
    Q[i][i] = x
Q[1][2] = Q[2][1] = F(-5)
I = [[F(i == j) for j in range(6)] for i in range(6)]
assert mm(L,Q) == I
Mi = [[F(z) for z in row] for row in ref['M0_inverse']]
assert mm(Mi, M0) == mm(M0, Mi) == I
W0 = mm(mm(Mi, L), Mi)
# Five fixed gravity channels: e2, e2+e3, e2+e3+e5, e4, e5.
N = tr([nu, ns, np, nx, ny])
gram = mm(mm(tr(N), W0), N)
coarse = mm(mm(tr(N), Q), N)
T = [row[:] for row in I]
T[2][1] = F(1)
adapted_Q = mm(mm(T, Q), tr(T))
summary = {
    'status': 'EXACT_TARGETED_J_ALGEBRA_PASS',
    'potential_fourier_identity': True,
    'radial_obstruction_direction': d,
    'radial_k4': k4,
    'radial_absolute_t6_remainder_cap': tail6,
    'radial_lower_coefficient_for_abs_t_le_1_over_20': radial_lower,
    'radial_obstruction_scope': 'global radial gravity sector only; not a counterexample to M4 or J<=1',
    'full12_initial_ball_witness': {'q': 't*(0,0,1,2,-1,0)', 'v': '0',
        'abs_t_upper': '1/20', 'q_norm_squared': '6*t^2',
        'q_norm_squared_upper': '3/200', 'initial_ball_squared_radius': '9/400'},
    'C_at_zero_v4_v5_coefficient': C45,
    'C_at_zero_v4_equal_v5_coefficient': C_equal,
    'gravity_channel_Gram_M0_inverse_L_M0_inverse': gram,
    'gravity_channel_Gram_Q': coarse,
    'gravity_channel_Gram_source_inverse_display': [[float(z) for z in row] for row in gram],
    'Q_in_q1_u_s_x_y_q6_coordinates': adapted_Q,
    'channel_squares_origin_vs_coarse_display': [
        {'source_inverse': float(gram[i][i]), 'Q': float(coarse[i][i]),
         'ratio': float(gram[i][i]/coarse[i][i])} for i in range(5)],
    'trajectory_or_eigenvalue_sweep': False,
    'J_le_1_proved': False,
    'physical_FD_Float64_binding': False,
    'source_sha256': {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in [
        a.SRC / 'routeB_fourier_mass_full_rational.csv',
        a.SRC / 'routeB_fourier_potential_rational.csv',
        ref_path, algebra_path]},
}
print(json.dumps(summary, default=str, indent=2))
