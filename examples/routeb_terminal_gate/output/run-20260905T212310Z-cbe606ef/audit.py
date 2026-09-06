"""Exact terminal-neighborhood obstruction; no solver or trajectory."""
import csv, hashlib, json, sys
from fractions import Fraction as F
from pathlib import Path

def main():
    run=Path(sys.argv[1]).resolve()
    manifest=json.loads((run/'before_run.json').read_text(encoding='utf-8'))
    for name,digest in manifest['snapshots'].items():
        assert hashlib.sha256((run/name).read_bytes()).hexdigest()==digest
    ref=json.loads((run/'inputs/reference.json').read_text(encoding='utf-8'))
    cand=json.loads((run/'inputs/candidate.json').read_text(encoding='utf-8'))
    coef={k:F(v) for k,v in cand['rational_coefficients'].items()}
    assert coef['a1']==0 and all(coef[f'a{j}']==0 for j in range(1,8))
    assert all(coef[f'p{j}_{i}']==0 for j in range(1,9) for i in range(1,7))
    assert all(coef[f'c{j}']==0 for j in range(1,9) if j != 4)
    a8=coef['a8']; rho=F(1,20); tau=F(1,100)
    M=[[F(x) for x in row] for row in ref['M0']]
    R=[[F(x) for x in row] for row in ref['M0_inverse']]
    D=list(map(F,ref['D'])); v=[0,0,0,rho,rho,0]
    DM=[[[F(0) for _ in range(6)] for _ in range(6)] for _ in range(6)]
    with (run/'inputs/mass.csv').open(encoding='utf-8-sig',newline='') as h:
        for row in csv.DictReader(h):
            i,j=int(row['row'])-1,int(row['col'])-1
            im=F(int(row['imag_num']),int(row['imag_den']))
            for k in range(6): DM[i][j][k]-=im*int(row['nu'+str(k+1)])
    C=[sum((DM[i][j][k]+DM[i][k][j]-DM[j][k][i])*v[j]*v[k]/2
           for j in range(6) for k in range(6)) for i in range(6)]
    assert C==[F(21,10000000),F(0),F(0),F(0),F(0),F(0)]
    delta=[-sum(R[i][j]*C[j] for j in range(6)) for i in range(6)]
    L=[[F(0) for _ in range(6)] for _ in range(6)]
    for i,x in enumerate([F(1,3),F(19,117),F(56,585),F(7,165),F(1,45),F(1,90)]): L[i][i]=x
    L[1][2]=L[2][1]=F(7,117)
    E=sum(delta[i]*L[i][j]*delta[j] for i in range(6) for j in range(6))
    W0=sum(v[i]*M[i][j]*v[j] for i in range(6) for j in range(6))/2
    Wdot=-sum(D[i]*v[i]*v[i] for i in range(6))
    f=a8*tau**8; fp=-8*a8*tau**7
    Vdot=fp*W0+f*Wdot
    assert E>0 and E+Vdot>0 and tau>0
    result=dict(status='EXACT_TERMINAL_NEIGHBORHOOD_ZERO_SUPPLY_REJECTED',
        candidate='lp-20260905T210840Z-ac3429b0', t='99/100', tau=str(tau),
        q=['0']*6, v=list(map(str,v)), rho=str(rho), C=list(map(str,C)),
        delta=list(map(str,delta)), residual_cost=str(E), residual_cost_display=float(E),
        W0=str(W0), W0dot=str(Wdot), a8=str(a8), f=str(f), fprime=str(fp),
        Vdot=str(Vdot), Vdot_display=float(Vdot), total=str(E+Vdot),
        total_display=float(E+Vdot), a1='0',
        implication='At this source state the affine scalar gate has b=0 and requires cost+Vdot<=0; exact total is positive.',
        candidate_rejected=True, entire_storage_family_rejected=False,
        physical_target_refuted=False, J1_proved=False, Lean_verified=False,
        formal_certificate_allowed=False, solver_calls=0, trajectory_solves=0,
        fixed_test_points=1)
    (run/'results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(result['status'])
    print('EXACT_COST_PLUS_VDOT='+str(E+Vdot)+' DISPLAY='+str(float(E+Vdot)))
    print('a1=0 terminal candidate rejected; original T=1 goal OPEN')

if __name__=='__main__': main()
