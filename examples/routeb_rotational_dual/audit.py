"""Exact small parameter/dual-metric audit; not a physical Lean binding."""
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path
import re

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parents[2]/'6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq/dhport_lib.jl'


def main():
    source=SOURCE.read_text(encoding='utf-8')
    match=re.search(r'^I_val\s*=\s*\[([^\]]+)\]',source,re.M)
    inertia=[F(s.strip()) for s in match[1].split(',')]
    weights=[x/3 for x in inertia]
    assert weights==[F(1,3),F(1,5),F(7,60),F(1,15),F(1,30),F(1,60)]
    dh=re.search(r'^DH\s*=\s*\[([^\]]+)\]',source,re.M)[1]
    alpha=[row.split()[-1] for row in dh.split(';') if row.strip()]
    assert alpha==['-pi/2','0.0','pi/2','-pi/2','pi/2','0.0']
    assert 'const MASS_REGULARIZER = 1e-6' in source
    assert 'Jw\' * (Ri * Ii * Ri\') * Jw' in source
    # Under exact-real DH rotation semantics these are adjacent-axis products.
    adjacent=[F(0),F(1),F(0),F(0),F(0)]
    Q=[[F(0) for _ in range(6)] for _ in range(6)]
    for i,w in enumerate(weights):
        Q[i][i]+=1/w
        if i<5:
            Q[i+1][i+1]+=1/w
            Q[i][i+1]=Q[i+1][i]=-adjacent[i]/w
    L=[[F(0) for _ in range(6)] for _ in range(6)]
    for i,c in enumerate([F(1,3),F(19,117),F(56,585),F(7,165),F(1,45),F(1,90)]): L[i][i]=c
    L[1][2]=L[2][1]=F(7,117)
    assert all(sum(Q[i][k]*L[k][j] for k in range(6))==int(i==j) for i in range(6) for j in range(6))
    mismatch=F(5,8)*F(147,800000)**2*F(165,7)
    assert mismatch==F(101871,204800000000)
    result=dict(status='EXACT_PARAMETERS_AND_DUAL_METRIC_IDENTITY',
        source=str(SOURCE),source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        weights=list(map(str,weights)),DH_alpha=alpha,adjacent_axis_dot=list(map(str,adjacent)),
        inverse_upper_Q=[[str(x) for x in row] for row in Q],
        mass_lower_L=[[str(x) for x in row] for row in L],
        exact_QL_identity=True,unregularized_scalar_lower='1/90',regularized_scalar_lower='100009/9000000',
        prior_scalar_lower='9401/1000000',mass_mismatch_cost_factor=str(mismatch),
        full_physical_FK_Lean_binding=False,float64_axis_and_rotation_error_enclosed=False,
        total_residual_budget_proved=False)
    (HERE/'source_evidence.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print('EXACT_DUAL_METRIC_AUDIT_OK; total_residual_budget_proved=false')


if __name__=='__main__': main()
