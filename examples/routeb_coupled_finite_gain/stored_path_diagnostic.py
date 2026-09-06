"""E1 postprocess of ONE retained path; no trajectory solve or proof claim.

Analytic Fourier forces, not bitwise original Julia FD execution. Trapezoidal
integrals of sampled diagnostics are un-enclosed and only steer proof effort.
"""
import csv
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import sys
import numpy as np


def main():
    run=Path(sys.argv[1]).resolve()
    reference=json.loads((run/'inputs/reference.json').read_text(encoding='utf-8'))
    side=Path(__file__).resolve().parent
    src=side.parents[2]/'6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq'
    path=side.parent/'routeb_residual_budget_screen/output/run-20260905-124428-858595669005400/linear_direction.csv'
    with path.open(newline='',encoding='utf-8') as f: rows=list(csv.DictReader(f))
    def read(name):
        with (src/name).open(newline='',encoding='utf-8') as f: return list(csv.DictReader(f))
    mass=read('routeB_fourier_mass_full_rational.csv');potential=read('routeB_fourier_potential_rational.csv')
    modes=np.array([[int(r[f'nu{i}']) for i in range(1,7)] for r in mass])
    coeff=np.array([complex(float(F(int(r['real_num']),int(r['real_den']))),float(F(int(r['imag_num']),int(r['imag_den'])))) for r in mass])
    index=np.array([(int(r['row'])-1)*6+int(r['col'])-1 for r in mass])
    pmodes=np.array([[int(r[f'nu{i}']) for i in range(1,7)] for r in potential])
    pcoeff=np.array([float(F(int(r['real_num']),int(r['real_den']))) for r in potential])
    def matrix(key): return np.array([[float(F(x)) for x in row] for row in reference[key]])
    M0=matrix('M0');H0=matrix('H0');Aq=matrix('acceleration_q');Av=matrix('acceleration_v')
    Aw=np.array([float(F(x)) for x in reference['acceleration_w']])
    K=np.array([float(F(x)) for x in reference['Kp']]);D=np.array([float(F(x)) for x in reference['D']]);Ginput=np.array([float(F(x)) for x in reference['G']])
    Q=np.diag([3,8,95/7,165/7,45,90]);Q[1,2]=Q[2,1]=-5
    L=np.linalg.inv(Q)
    weight=np.array([5/8,10/13]);mref=np.diag(M0)[3:5]
    times=[];values=[];max_identity_error=0
    for row in rows:
        t=float(row['t']);q=np.array([float(row[f'q{i}']) for i in range(1,7)])
        v=np.array([float(row[f'v{i}']) for i in range(1,7)]);w=1.7*t
        mc=coeff*np.exp(1j*(modes@q))
        M=np.bincount(index,weights=mc.real,minlength=36).reshape(6,6)+np.eye(6)*1e-6
        dM=np.stack([np.bincount(index,weights=(1j*modes[:,k]*mc).real,minlength=36).reshape(6,6) for k in range(6)],axis=2)
        C=np.einsum('ijk,j,k->i',dM,v,v)-.5*np.einsum('jki,j,k->i',dM,v,v)
        G=((1j*pcoeff*np.exp(1j*(pmodes@q)))[:,None]*pmodes).sum(axis=0).real
        a=np.linalg.solve(M,-K*q-D*v+Ginput*w-C-G)
        a0=Aq@q+Av@v+Aw*w
        r=(M0-M)@a0+H0@q-G-C;delta=a-a0
        max_identity_error=max(max_identity_error,float(np.max(abs(M@delta-r))))
        load=K[3:5]*q[3:5]+D[3:5]*v[3:5]-Ginput[3:5]*w
        e=mref*a[3:5]+load;e0=mref*a0[3:5]+load
        times.append(t);values.append([float(delta@L@delta),float(r@Q@r),float(weight@(e*e)),float(weight@(e0*e0))])
    integrals=np.trapezoid(values,x=times,axis=0)
    result=dict(evidence='E1_STORED_PATH_ANALYTIC_FLOAT64_DIAGNOSTIC',
        no_new_trajectory_integrated=True,bitwise_Julia_FD=False,interval_or_Lean_verified=False,
        path=str(path),path_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),c=1.7,
        samples=len(times),sampled_trapezoid_integrals=dict(zip(['delta_L_delta','r_Q_r','actual_e_cost','same_state_e0_cost'],map(float,integrals))),
        max_force_identity_roundoff=max_identity_error,
        warning='Does not prove or refute any integral bound. Distinguishes the small actual correction energy from its potentially loose Q(r) upper estimate; same-state e0 is NOT the isolated nominal solution.')
    (run/'stored_path_diagnostic.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result['sampled_trapezoid_integrals']))
    print('UNENCLOSED_DIAGNOSTIC_ONLY')


if __name__=='__main__': main()
