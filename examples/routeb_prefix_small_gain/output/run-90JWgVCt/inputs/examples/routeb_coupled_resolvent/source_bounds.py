"""Exact acceleration-free nonlinear-force coefficient audit and envelope.

Uses the complete six-axis coupled nominal acceleration at the same state.
The envelope is conditional on a candidate box, not a flowpipe certificate.
"""
import hashlib
import importlib.util
import json
from fractions import Fraction as Q
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('inertial_algebra',HERE.parent/'routeb_inertial_structure/audit.py')
algebra=importlib.util.module_from_spec(spec);spec.loader.exec_module(algebra)
ZERO=(0,)*6


def transformed(p):
    # q3=s-q2; all transformations occur BEFORE absolute-value bounds.
    out={}
    for nu,c in p.items():
        eta=(nu[0],nu[1]-nu[2],nu[2],nu[3],nu[4],nu[5])
        assert eta not in out
        out[eta]=c
    return out


def real_envelope(p,radii,center_zero=False):
    center=sum(a for a,b in p.values())
    assert sum(b for a,b in p.values())==0
    if center_zero: assert center==0
    # Conjugate-symmetric maps are real. Centering preserves cos cancellation:
    # |cos(theta)-1|<=min(2,theta²/2); |sin(theta)|<=min(1,|theta|).
    variation=sum(abs(a)*min(Q(2),sum(abs(n)*r for n,r in zip(nu,radii))**2/2)+
                  abs(b)*min(Q(1),sum(abs(n)*r for n,r in zip(nu,radii)))
                  for nu,(a,b) in p.items())
    global_cap=sum(abs(a)+abs(b) for a,b in p.values())
    return min(global_cap,abs(center)+variation)


def main():
    run=Path(sys.argv[1]).resolve()
    assert run.parent==HERE/'output' and run.is_dir()
    refpath=Path(sys.argv[2]).resolve()
    ref=json.loads(refpath.read_text(encoding='utf-8'))
    assert ref['status']=='EXACT_COUPLED_NOMINAL_REFERENCE_PASS'
    source=algebra.SRC
    records=algebra.rows('routeB_fourier_mass_full_rational.csv')
    M=[[algebra.load_poly([r for r in records if (int(r['row']),int(r['col']))==(i+1,j+1)])
        for j in range(6)] for i in range(6)]
    M0=[[Q(v) for v in row] for row in ref['M0']]
    mu=Q(ref['mu'])
    for i in range(6): M[i][i]=algebra.add(M[i][i],algebra.const(mu))
    dM=[[algebra.add(algebra.const(M0[i][j]),algebra.scale(M[i][j],-1)) for j in range(6)] for i in range(6)]
    for row in dM:
        for p in row: assert sum(a for a,b in p.values())==sum(b for a,b in p.values())==0
    acc=[[Q(x) for x in ref['acceleration_q'][i]]+[Q(x) for x in ref['acceleration_v'][i]]+
         [Q(ref['acceleration_w'][i])] for i in range(6)]
    # Replace q3=s-q2 and v3=V-v2 in the full nominal map, keeping 13 columns.
    for row in acc:
        row[1]-=row[2];row[7]-=row[8]
    coefficients=[[transformed(algebra.add(*[algebra.scale(dM[i][j],acc[j][l]) for j in range(6)]))
                   for l in range(13)] for i in range(6)]
    potrows=algebra.rows('routeB_fourier_potential_rational.csv')
    U=algebra.load_poly(potrows)
    assert all(b==0 for a,b in U.values())
    H=[[Q(x) for x in row] for row in ref['H0']]
    for i in range(6):
        assert sum(a for a,b in algebra.diff(U,i).values())==0
        for j in range(6):
            assert sum(a for a,b in algebra.diff(algebra.diff(U,i),j).values())==H[i][j]
    # Exact Christoffel velocity polynomial, then combine v2/v3 cancellations.
    sub={0:{0:Q(1)},1:{1:Q(1)},2:{2:Q(1),1:Q(-1)},3:{3:Q(1)},4:{4:Q(1)},5:{5:Q(1)}}
    coriolis=[{} for _ in range(6)]
    for i in range(6):
        for j in range(6):
            for k in range(6):
                p=algebra.scale(algebra.add(algebra.diff(M[i][j],k),algebra.diff(M[i][k],j),
                                           algebra.scale(algebra.diff(M[j][k],i),-1)),Q(1,2))
                for a,ca in sub[j].items():
                    for b,cb in sub[k].items():
                        pair=tuple(sorted((a,b)))
                        coriolis[i][pair]=algebra.add(coriolis[i].get(pair,{}),algebra.scale(p,ca*cb))
        coriolis[i]={pair:transformed(p) for pair,p in coriolis[i].items() if p}
    # This support CONTAINS the original initial ball. Its invariance is OPEN.
    qrad=[Q(2,5),Q(1),Q(6,5),Q(2,5),Q(2,5),Q(2,5)]
    vrad=[Q(3,5),Q(5,2),Q(2),Q(4,5),Q(4,5),Q(2,5)]
    yrad=qrad+vrad+[Q(7,4)] # sqrt(3)<7/4; no input-class restriction.
    ledger=[]
    for i in range(6):
        linear_caps=[real_envelope(p,qrad,center_zero=True) for p in coefficients[i]]
        mass_cap=sum(a*b for a,b in zip(linear_caps,yrad))
        Ccap=sum(real_envelope(p,qrad)*vrad[a]*vrad[b] for (a,b),p in coriolis[i].items())
        # Since all U modes have real coefficients, G-Hq is cubically bounded
        # using |sin(theta)-theta|<=|theta|³/6, valid on all real arguments.
        Gcap=Q(0)
        for nu,(a,b) in U.items():
            n=(nu[0],nu[1]-nu[2],nu[2],nu[3],nu[4],nu[5])
            theta=sum(abs(nj)*r for nj,r in zip(n,qrad))
            Gcap+=abs(a*nu[i])*theta**3/6
        ledger.append(dict(axis=i+1,mass_times_a0=str(mass_cap),C=str(Ccap),gravity_cubic=str(Gcap),
                           r_excluding_eta=str(mass_cap+Ccap+Gcap),mass_linear_coefficients=list(map(str,linear_caps))))
    caps=[Q(row['r_excluding_eta']) for row in ledger]
    # The exact Q cross term is retained in the model; this scalar diagnostic
    # deliberately upper-bounds it only to assess box conservatism.
    diag=[Q(3),Q(8),Q(95,7),Q(165,7),Q(45),Q(90)]
    Qcap=sum(d*r*r for d,r in zip(diag,caps))+10*caps[1]*caps[2]
    inputs=[source/'routeB_fourier_mass_full_rational.csv',source/'routeB_fourier_potential_rational.csv',refpath]
    result=dict(status='EXACT_ACCELERATION_FREE_SOURCE_COEFFICIENT_AUDIT',
        formula='r=(M0-M(q))*a0(q,v,w)+H0*q-G(q)-C(q,v)+eta',
        position_coordinates=['q1','q2','q2+q3','q4','q5','q6'],velocity_coordinates=['v1','v2','v2+v3','v4','v5','v6'],
        q_caps=list(map(str,qrad)),v_caps=list(map(str,vrad)),w_cap='7/4',
        origin_r_and_first_derivatives_zero_without_eta=True,
        reason='Mass differences vanish at zero and multiply zero-equilibrium linear a0; C is quadratic in velocities; gradient zero and Hessian exactly H0; full 13-variable analytic residual has zero linearization.',
        gravity_remainder_cubic=True,component_ledger=ledger,
        box_Q_r_upper_excluding_eta=str(Qcap),box_Q_r_upper_display=float(Qcap),
        entire_initial_ball_contained=True,box_invariance_proved=False,total_R_proved=False,
        physical_FK_FD_Float64_binding=False,Lean_verified=False,
        source_sha256={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs})
    (run/'source_bounds.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(result['status'])
    print('r component envelope (display only):',list(map(float,caps)))
    print('box Q(r) <=',float(Qcap),'without eta; NOT a trajectory integral or acceptance result')


if __name__=='__main__': main()
