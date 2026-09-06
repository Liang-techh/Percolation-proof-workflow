"""Concrete fixed-Z multiplier ansatz and noncontractive scalar source gate.

Exact symbolic coefficient identities, not numerical trajectories or a claim
that a storage/supply certificate has been found.
"""
import hashlib
import json
from pathlib import Path
import sys
import sympy as sp


def main():
    run=Path(sys.argv[1]).resolve();inputs=run/'inputs'
    data=json.loads((inputs/'reference.json').read_text(encoding='utf-8'))
    assert data['status']=='EXACT_COUPLED_NOMINAL_REFERENCE_PASS'
    M0=sp.Matrix([[sp.Rational(x) for x in row] for row in data['M0']])
    R=sp.Matrix([[sp.Rational(x) for x in row] for row in data['M0_inverse']])
    assert M0==M0.T and R==R.T and M0*R==R*M0==sp.eye(6)
    Q=sp.diag(3,8,sp.Rational(95,7),sp.Rational(165,7),45,90)
    Q[1,2]=Q[2,1]=-5
    L=sp.diag(sp.Rational(1,3),sp.Rational(19,117),sp.Rational(56,585),
              sp.Rational(7,165),sp.Rational(1,45),sp.Rational(1,90))
    L[1,2]=L[2,1]=sp.Rational(7,117)
    assert L*Q==Q*L==sp.eye(6)
    T=sp.eye(6);T[1,2]=sp.Rational(7,19)
    W=sp.diag(sp.Rational(1,3),sp.Rational(19,117),sp.Rational(7,95),
              sp.Rational(7,165),sp.Rational(1,45),sp.Rational(1,90))
    assert T.T*W*T==L and all(W[i,i]>0 for i in range(6))
    names={(i,j):sp.Symbol(f'dM{i}{j}') for i in range(6) for j in range(i,6)}
    dM=sp.Matrix(6,6,lambda i,j:names[min(i,j),max(i,j)])
    M=M0-dM;D=2*M-L
    h=sp.Matrix(sp.symbols('h0:6'));z=sp.Matrix(sp.symbols('z0:6'))
    # The independent h,z coordinates parametrize every r,g bijectively.
    r=M0*h;g=M0*z-L*h+r
    assert R*r==h
    assert all(sp.expand(x)==0 for x in z-(R*g+(R*L*R-R)*r))
    b,d=sp.symbols('b d')
    top=b-d-2*(z.T*r)[0]
    u=g+r-M*z
    H=sp.zeros(7,7);H[0,0]=top;H[0,1:7]=-u.T;H[1:7,0]=-u;H[1:7,1:7]=D
    change=sp.eye(7);change[1:7,0]=h
    e=dM*(2*h+z)
    mhat=b-d-2*(g.T*h)[0]-(h.T*L*h)[0]-2*((z+h).T*dM*h)[0]
    K=sp.zeros(7,7);K[0,0]=mhat;K[0,1:7]=-e.T;K[1:7,0]=-e;K[1:7,1:7]=D
    discrepancies=list(change.T*H*change-K)
    assert all(sp.expand(x)==0 for x in discrepancies)
    assert D-L==2*(M-L)
    # The next identity uses arbitrary e, rather than expanding the large
    # source-dependent square. Substitution is justified by the preceding
    # exact coefficient identity; no smallness hypothesis is introduced.
    ee=sp.Matrix(sp.symbols('e0:6'));y=sp.Matrix(sp.symbols('y0:6'))
    s,margin=sp.symbols('s margin')
    left=s*s*margin-2*s*(ee.T*y)[0]+(y.T*D*y)[0]
    shifted=y-s*Q*ee
    right=(y.T*(D-L)*y)[0]+(shifted.T*L*shifted)[0]+s*s*(margin-(ee.T*Q*ee)[0])
    assert sp.expand(left-right)==0
    # Fixed Z=I is pointwise lossless if z solves Mz=g-r+Ldelta.
    # This identity is coefficient-wise in a generic symmetric M as well.
    delta=sp.Matrix(sp.symbols('delta0:6'));zz=sp.Matrix(sp.symbols('optimal_z0:6'))
    rr=M*delta;gg=M*zz+rr-L*delta
    a=b-d-2*(zz.T*rr)[0];uu=gg+rr-M*zz
    true_margin=b-d-2*(gg.T*delta)[0]-(delta.T*L*delta)[0]
    lossless=sp.zeros(7,7);lossless[0,0]=a;lossless[0,1:7]=-uu.T
    lossless[1:7,0]=-uu;lossless[1:7,1:7]=D
    congruence=sp.eye(7);congruence[1:7,0]=-delta
    expanded=congruence.T*sp.diag(true_margin,D)*congruence
    assert all(sp.expand(x)==0 for x in lossless-expanded)
    def matrix_strings(A): return [[str(x) for x in row] for row in A.tolist()]
    result=dict(status='EXACT_FIXED_IDENTITY_MULTIPLIER_AND_SCALAR_GATE_PASS',
        free_symmetric_mass_defect_entries=21,free_center_and_affine_coordinates=12,
        frozen_center_congruence_entry_checks=49,metric_SOS_identity_checks=1,
        pointwise_lossless_congruence_entry_checks=49,
        bijective_force_storage_parameterization=True,source_M0_inverse_checked=True,
        exact_L_square_completion=True,exact_Q_inverse=True,
        ansatz=dict(Z=matrix_strings(sp.eye(6)),h_force_matrix=matrix_strings(R),
                    z_gradient_matrix=matrix_strings(R),z_force_matrix=matrix_strings(R*L*R-R),
                    formula='h=Rr; z=Rg+(RLR-R)r; R=M0^-1; r includes eta once'),
        bottom='D=2M-L; D-L=2(M-L)>=0 under the existing mass lower-bound premise',
        defect='e=dM(2h+z)',
        scalar_gate='b >= d+2g.h+h^T L h+2(z+h)^T dM h+e^T Q e',
        exact_at_M0=True,contraction_factor_required=False,
        pointwise_optimal_z='M^-1 g-delta+M^-1 L delta, delta=M^-1 r',
        scalar_gate_uniformly_verified=False,storage_P_k_selected=False,
        actual_DH_J_proved=False,physical_FD_Float64_binding=False,
        Lean_verified=False,formal_certificate_allowed=False,
        numerical_solver_or_trajectory_run=False,sympy_version=sp.__version__,
        warning='Constructs multipliers from a still-unselected storage derivative g,d. The uniform scalar gate, source domain, eta and all-prefix supply/storage budget remain OPEN.',
        inputs={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs.iterdir() if p.is_file()})
    (run/'results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(result['status'])
    print('EXACT_CONGRUENCE_CHECKS=49+49 METRIC_SOS_CHECKS=1')
    print('Z=I; GLOBAL_BOTTOM_PREMISE=M>=L; NO_EPSILON_ASSUMPTION')
    print('STORAGE_AND_UNIFORM_SCALAR_BUDGET_STILL_OPEN')


if __name__=='__main__': main()
