"""Exact cyclic-axis obstruction to the second zero-supply candidate."""
import csv
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import sys


def main():
    run = Path(sys.argv[1]).resolve()
    manifest = json.loads((run/'before_run.json').read_text(encoding='utf-8'))
    for name, digest in manifest['snapshots'].items():
        assert hashlib.sha256((run/name).read_bytes()).hexdigest() == digest
    candidate = json.loads((run/'inputs/candidate.json').read_text(encoding='utf-8'))
    reference = json.loads((run/'inputs/reference.json').read_text(encoding='utf-8'))
    coefficients = {k: F(v) for k, v in candidate['rational_coefficients'].items()}
    degree = candidate['degree']
    assert all(coefficients[f'p{j}_6'] == 0 for j in range(1, degree+1))
    f = sum(coefficients[f'a{j}'] for j in range(1, degree+1))
    fp = -sum(j*coefficients[f'a{j}'] for j in range(1, degree+1))
    assert f > 0
    m66 = F(reference['M0'][5][5])
    h66 = F(reference['H0'][5][5])
    k6, d6 = F(reference['Kp'][5]), F(reference['D'][5])
    assert h66 == 0

    def restricted(name, mass):
        grouped = {}
        with (run/'inputs'/name).open(encoding='utf-8-sig', newline='') as handle:
            for row in csv.DictReader(handle):
                if mass and (row['row'] != '6' or row['col'] != '6'):
                    continue
                n = int(row['nu6'])
                a, b = grouped.get(n, (F(0), F(0)))
                grouped[n] = (a+F(int(row['real_num']), int(row['real_den'])),
                              b+F(int(row['imag_num']), int(row['imag_den'])))
        return {n: ab for n, ab in grouped.items() if ab != (0, 0)}

    mass = restricted('mass.csv', True)
    potential = restricted('potential.csv', False)
    assert mass == {0: (m66-F(1, 1000000), F(0))}
    assert potential == {0: (F(3108789, 400000), F(0))}
    q6, v6 = F(1, 100), F(-1, 400)
    radius_sq = q6*q6+v6*v6
    assert radius_sq < F(9, 400)
    W0 = m66*v6*v6/2
    W0dot = -(k6+h66)*q6*v6-d6*v6*v6
    Vdot = fp*W0+f*W0dot
    assert Vdot > 0
    qq = F(0)
    qv = -f*(k6+h66)/2
    vv = fp*m66/2-f*d6
    determinant = qq*vv-qv*qv
    assert determinant < 0
    assert qq*q6*q6+2*qv*q6*v6+vv*v6*v6 == Vdot
    result = dict(
        status='EXACT_SECOND_CANDIDATE_ZERO_SUPPLY_REJECTED_AT_ALLOWED_INITIAL_STATE',
        candidate_run='lp-20260905T210840Z-ac3429b0',
        t='0', c='0', w='0', eta='0, analytic semantics only',
        q=['0']*5+[str(q6)], v=['0']*5+[str(v6)],
        initial_norm_squared=str(radius_sq), original_initial_ball_squared='9/400',
        original_block_P='0', original_terminal_Q_at_test_state='0',
        exact_restricted_mass66_constant=str(m66),
        exact_restricted_potential_constant='3108789/400000',
        restricted_remainder='0', f=str(f), fprime=str(fp),
        W0=str(W0), W0dot=str(W0dot), Vdot=str(Vdot), Vdot_display=float(Vdot),
        local_quadratic_block=[[str(qq), str(qv)], [str(qv), str(vv)]],
        local_quadratic_determinant=str(determinant),
        local_negative_semidefinite_impossible=True,
        derivation='Vdot=fprime*W0+f*W0dot; other storage terms vanish at q6,v6,c0. W0dot uses the signed-gap actual-force identity and eta0. Since L>=0, energy_cost+Vdot>0.',
        uniform_zero_supply_candidate_rejected=True,
        entire_storage_family_rejected=False, physical_target_refuted=False,
        positive_supply_alternative_rejected=False, physical_source_binding=False,
        Lean_verified=False, J1_proved=False, formal_certificate_allowed=False,
        solver_calls=0, trajectory_solves=0, prospectively_fixed_test_points=1)
    (run/'results.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(result['status'])
    print('EXACT_VDOT='+str(Vdot)+' DISPLAY='+str(float(Vdot)))
    print('INITIAL_NORM_SQUARED='+str(radius_sq)+' <9/400')
    print('ZERO_SUPPLY_CANDIDATE_REJECTED; ORIGINAL_T1_GOAL_OPEN')


if __name__ == '__main__':
    main()
