"""Exact affine multiplier algebra and a source-instantiated point witness.

No trajectory, SDP, sampling or spectral numerics. This does NOT establish a
uniform storage or J<=1. The witness refutes only homogeneous-certificate
completeness, not the physical target.
"""
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import sympy as sp


def main():
    run=Path(sys.argv[1]).resolve();inputs=run/'inputs'
    spec=importlib.util.spec_from_file_location('source_algebra',inputs/'inertial_audit.py')
    alg=importlib.util.module_from_spec(spec);spec.loader.exec_module(alg)
    alg.SRC=inputs
    ref=json.loads((inputs/'reference.json').read_text(encoding='utf-8'))
    assert ref['status']=='EXACT_COUPLED_NOMINAL_REFERENCE_PASS'
    def matrix(key): return sp.Matrix([[sp.Rational(x) for x in row] for row in ref[key]])
    M0,R=matrix('M0'),matrix('M0_inverse')
    assert M0==M0.T and R==R.T and R*M0==M0*R==sp.eye(6)
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

    # Check coefficient identities in 21 independent symmetric mass-defect
    # entries and all six g,r entries, rather than checking numerical samples.
    DD={(i,j):sp.Symbol(f'dM{i}{j}') for i in range(6) for j in range(i,6)}
    dM=sp.Matrix(6,6,lambda i,j:DD[min(i,j),max(i,j)])
    M=M0-dM
    g=sp.Matrix(sp.symbols('g0:6'));r=sp.Matrix(sp.symbols('r0:6'))
    b,d=sp.symbols('b d')
    Z=R*L;z=R*g
    bottom=Z.T*M+M*Z-L
    cross=-(g+Z.T*r-M*z)
    top=b-d-2*(z.T*r)[0]
    expected_bottom=L-L*R*dM-dM*R*L
    expected_cross=-(L*R*r+dM*R*g)
    expected_top=b-d-2*(g.T*R*r)[0]
    discrepancies=list(bottom-expected_bottom)+list(cross-expected_cross)+[top-expected_top]
    assert all(sp.expand(x)==0 for x in discrepancies)

    # Source point: q=0, v=(e4+e5)/20, w=0, eta=0. Entire initial ball is
    # unchanged; this ONE exact point is only a formulation counterexample.
    rows=alg.rows('routeB_fourier_mass_full_rational.csv')
    mass=[[alg.load_poly([rr for rr in rows if (int(rr['row']),int(rr['col']))==(i+1,j+1)])
           for j in range(6)] for i in range(6)]
    def origin(poly):
        assert sum(im for re,im in poly.values())==0
        return sum((re for re,im in poly.values()),F(0))
    assert all(sp.Rational(origin(mass[i][j]))+(sp.Rational(ref['mu']) if i==j else 0)==M0[i,j]
               for i in range(6) for j in range(6))
    v=sp.Matrix([0,0,0,sp.Rational(1,20),sp.Rational(1,20),0])
    C=[]
    for i in range(6):
        value=sp.Rational(0)
        for j in range(6):
            for k in range(6):
                poly=alg.scale(alg.add(alg.diff(mass[i][j],k),alg.diff(mass[i][k],j),
                       alg.scale(alg.diff(mass[j][k],i),-1)),F(1,2))
                value+=sp.Rational(origin(poly))*v[j]*v[k]
        C.append(value)
    C=sp.Matrix(C)
    assert C==sp.Matrix([sp.Rational(21,10000000),0,0,0,0,0])
    U=alg.load_poly(alg.rows('routeB_fourier_potential_rational.csv'))
    assert all(origin(alg.diff(U,i))==0 for i in range(6))
    D=sp.diag(*map(sp.Rational,ref['D']))
    a0=-R*D*v;a=R*(-D*v-C)
    delta=a-a0;force=-C
    assert M0*delta==force
    assert (v.T*v)[0]==sp.Rational(1,200)<sp.Rational(9,400)
    energy=(delta.T*L*delta)[0]
    assert energy>0
    # A local storage derivative jet, NOT a constructed global storage:
    # Vdot=d+2g'delta=-energy, so Jdensity+Vdot=0<budget.
    gg=-L*delta;dd=energy;bb=energy/2
    zz=R*gg;ZZ=R*L
    top0=bb-dd-2*(zz.T*force)[0]
    cross0=-(gg+ZZ.T*force-M0*zz)
    bot0=ZZ.T*M0+M0*ZZ-L
    block=sp.zeros(7,7);block[0,0]=top0
    block[1:7,0]=cross0;block[0,1:7]=cross0.T;block[1:7,1:7]=bot0
    margin=bb-dd-2*(gg.T*delta)[0]-energy
    assert margin==energy/2>0
    congruence=sp.eye(7);congruence[1:7,0]=-delta
    diagonal=sp.diag(margin,L)
    assert block==congruence.T*diagonal*congruence
    assert bb-dd==-energy/2<0  # every homogeneous Z has this negative corner.
    assert energy+dd+2*(gg.T*delta)[0]==0
    def sm(A): return [[str(x) for x in row] for row in A.tolist()]
    result=dict(status='EXACT_AFFINE_RESIDUAL_MULTIPLIER_AUDIT_PASS',
        coefficient_identities=len(discrepancies),free_mass_defect_coordinates=21,
        all_six_force_and_storage_gradient_coordinates=True,
        exact_M0_inverse=True,exact_L_positive_square_completion=True,
        affine_matrix='[[b-d-2z.r, -(g+Z^T r-Mz)^T],[-(g+Z^T r-Mz),Z^T M+MZ-L]]',
        frozen_inverse_formula=dict(Z='R L',z='R g',top='b-d-2g^T R r',
            cross='-(L R r+dM R g)',bottom='L-L R dM-dM R L',R='M0^-1'),
        witness=dict(q=['0']*6,v=list(map(str,v)),w='0',eta='0',
            initial_norm_squared='1/200',original_ball_squared_radius='9/400',
            exact_C=list(map(str,C)),exact_delta=list(map(str,delta)),
            delta_L_delta=str(energy),g=list(map(str,gg)),d=str(dd),b=str(bb),
            actual_density_plus_derivative='0',strict_supply_margin=str(margin),
            homogeneous_top_left=str(bb-dd),homogeneous_every_Z_impossible=True,
            affine_matrix=sm(block),congruence=sm(congruence),
            positive_diagonal_block=sm(diagonal),affine_strictly_positive=True,
            global_storage_constructed=False,scope='Source-instantiated local descriptor and freely chosen storage jet only; not an actual J integral certificate.'),
        actual_DH_J_proved=False,uniform_source_cell_certificate=False,
        physical_FD_Float64_binding=False,Lean_verified=False,
        formal_certificate_allowed=False,sympy_version=sp.__version__,
        trajectory_or_solver_run=False,
        input_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs.iterdir() if p.is_file()})
    (run/'results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(result['status'])
    print('COEFFICIENT_IDENTITIES',len(discrepancies))
    print('SOURCE_INITIAL_NORM_SQUARED=1/200')
    print('HOMOGENEOUS_TOP_LEFT_NEGATIVE=true AFFINE_CONGRUENCE_POSITIVE=true')
    print('NO_UNIFORM_STORAGE_OR_J_CERTIFICATE')


if __name__=='__main__': main()
