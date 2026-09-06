"""Preserve LP; one deterministic repair and exact initial-direction audit.

No second optimization or source collocation. Add p1_4=1/10^6 and c1=1/1000;
use beta=15. Recheck only the saved 70 rows. Separately inspect the returned
coefficients analytically along q2=e, v2=3e/2, c=0 at t=0, with e=1/100.
This directional check can reject a zero-supply candidate; it cannot prove J.
"""
from datetime import datetime,timezone
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import uuid
import csv


def child(run):
    manifest=json.loads((run/'before_run.json').read_text(encoding='utf-8'))
    for name,record in manifest['snapshots'].items():
        assert hashlib.sha256((run/name).read_bytes()).hexdigest()==record['sha256']
    old=json.loads((run/'lp_candidate_evidence.json').read_text(encoding='utf-8'))
    problem=json.loads((run/'lp_problem.json').read_text(encoding='utf-8'))
    ref=json.loads((run/'reference.json').read_text(encoding='utf-8'))
    coeff={name:F(value) for name,value in old['rational_coefficients'].items()}
    coeff['p1_4']=F(1,1000000)
    coeff['c1']=F(1,1000)
    coeff['beta']=F(15)
    xx=[float(coeff[name]) for name in problem['names']]
    residual=[sum(a*x for a,x in zip(row,xx))-b for row,b in zip(problem['A_ub'],problem['b_ub'])]
    A=sum(coeff['a'+str(j)] for j in range(1,9))
    P=[sum(coeff['p'+str(j)+'_'+str(i)] for j in range(1,9)) for i in range(1,7)]
    Hc=sum(coeff['c'+str(j)] for j in range(1,9))
    beta=coeff['beta']
    initial_slacks=[beta-A/2]+[beta-P[i]-(F(7,75)*A if i==3 else 0) for i in range(6)]
    assert min(initial_slacks)>=0 and min(coeff.values())>=0
    budget=F(9,400)*beta+F(3,10000)*A+3*Hc
    assert budget<1
    # Exact same source line M22 is constant, potential T*cos(e)+constant;
    # this restriction was coefficient-checked in the earlier retained audit.
    M22=F(ref['M0'][1][1]);D2=F(ref['D'][1]);S22=F(ref['H0'][1][1])+F(ref['Kp'][1])
    fdot=-sum(j*coeff['a'+str(j)] for j in range(1,9))
    pdot=-sum(j*coeff['p'+str(j)+'_2'] for j in range(1,9))
    ratio=F(3,2);eps=F(1,100)
    quadratic=fdot*M22*ratio**2/2+A*(-ratio*S22-ratio**2*D2)+pdot+2*ratio*P[1]
    T=F(762237,200000)+F(242307,200000)+F(20601,400000)
    assert fdot<0
    # Psi(e)<=e^4/24, multiplying by fdot*T reverses the inequality.
    derivative_lower=quadratic*eps**2+fdot*T*eps**4/24
    radius_squared=(1+ratio**2)*eps**2
    assert radius_squared<F(9,400) and derivative_lower>0
    # Coordinator's predeclared ramp witness: t=1/2,c=1,q=0,v=G/1000.
    # Evaluate actual Christoffel force from the same rational mass CSV.
    M=[[F(x) for x in row] for row in ref['M0']]
    R=[[F(x) for x in row] for row in ref['M0_inverse']]
    G=list(map(F,ref['G']));damping=list(map(F,ref['D']))
    DM=[[[F(0) for k in range(6)] for j in range(6)] for i in range(6)]
    mass_at_zero=[[F(i==j,1000000) for j in range(6)] for i in range(6)]
    with (run/'mass.csv').open(encoding='utf-8-sig',newline='') as handle:
        for row in csv.DictReader(handle):
            i,j=int(row['row'])-1,int(row['col'])-1
            a,b=F(int(row['real_num']),int(row['real_den'])),F(int(row['imag_num']),int(row['imag_den']))
            mass_at_zero[i][j]+=a
            for k in range(6): DM[i][j][k]-=b*int(row['nu'+str(k+1)])
    assert mass_at_zero==M
    gradient=[F(0)]*6
    with (run/'potential.csv').open(encoding='utf-8-sig',newline='') as handle:
        for row in csv.DictReader(handle):
            for i in range(6): gradient[i]-=F(int(row['imag_num']),int(row['imag_den']))*int(row['nu'+str(i+1)])
    assert gradient==[0]*6
    vel=[g/F(1000) for g in G]
    Cforce=[sum((DM[i][j][k]+DM[i][k][j]-DM[j][k][i])*vel[j]*vel[k]/2 for j in range(6) for k in range(6)) for i in range(6)]
    delta=[-sum(R[i][j]*Cforce[j] for j in range(6)) for i in range(6)]
    assert [sum(M[i][j]*delta[j] for j in range(6)) for i in range(6)]==[-c for c in Cforce]
    L=[[F(0) for j in range(6)] for i in range(6)]
    for i,value in enumerate((F(1,3),F(19,117),F(56,585),F(7,165),F(1,45),F(1,90))): L[i][i]=value
    L[1][2]=L[2][1]=F(7,117)
    exact_cost=sum(delta[i]*L[i][j]*delta[j] for i in range(6) for j in range(6))
    oldcoeff={name:F(value) for name,value in old['rational_coefficients'].items()}
    time=F(1,2);tau=1-time
    f=sum(oldcoeff['a'+str(j)]*tau**j for j in range(1,9))
    fprime=-sum(j*oldcoeff['a'+str(j)]*tau**(j-1) for j in range(1,9))
    Wzero=sum(vel[i]*M[i][j]*vel[j] for i in range(6) for j in range(6))/2
    Wzero_dot=-sum(damping[i]*vel[i]**2 for i in range(6))+time*sum(vel[i]*G[i] for i in range(6))
    ramp_Vdot=fprime*Wzero+f*Wzero_dot
    assert exact_cost>=0 and ramp_Vdot>0
    ramp_witness=dict(t=str(time),c='1',w=str(time),q=['0']*6,v=list(map(str,vel)),
        M_equals_M0=True,gradient_U_zero=True,Rpotential_zero=True,
        Christoffel_C=list(map(str,Cforce)),actual_delta=list(map(str,delta)),
        actual_cost=str(exact_cost),actual_cost_display=float(exact_cost),
        fixed_Z_cost_equals_actual_at_M0=True,W0=str(Wzero),W0dot=str(Wzero_dot),
        f=str(f),fprime=str(fprime),original_candidate_Vdot=str(ramp_Vdot),
        original_candidate_Vdot_display=float(ramp_Vdot),
        original_candidate_cost_plus_Vdot=str(exact_cost+ramp_Vdot),
        first_LP_uniform_zero_supply_rejected=True)
    result=dict(status='REPAIRED_FINITE_CANDIDATE_BUT_EXACT_ZERO_SUPPLY_INITIAL_OBSTRUCTION',
        coefficients={k:str(v) for k,v in coeff.items()},
        nonzero_coefficients={k:str(v) for k,v in coeff.items() if v},
        initial_budget=str(budget),initial_budget_display=float(budget),
        remaining_supply_budget=str(1-budget),remaining_supply_budget_display=float(1-budget),
        exact_initial_constraint_slacks=list(map(str,initial_slacks)),
        saved_70_point_max_numerical_violation=max(residual[:70]),
        saved_70_point_slacks=[-v for v in residual[:70]],
        corrected_point_55_slack=-residual[55],
        exact_initial_obstruction=dict(t='0',q2=str(eps),v2=str(ratio*eps),other_coordinates='0; c=w=eta=0',
            original_full12_radius_squared=str(radius_squared),
            Vdot_quadratic_coefficient=str(quadratic),Vdot_quadratic_coefficient_display=float(quadratic),
            Vdot_lower=str(derivative_lower),Vdot_lower_display=float(derivative_lower),
            proof='Vdot = quadratic*e^2 + fdot*T*Psi(e), 0<=Psi(e)<=e^4/24; M22 constant on this source line.',
            implication='Because delta L delta >= 0, zero-supply dissipation fails at an actual allowed initial state under analytic source semantics.'),
        exact_ramp_witness=ramp_witness,
        number_of_new_LP_calls=0,number_of_new_source_collocations=0,
        zero_supply_candidate_rejected=True,entire_W0_family_rejected=False,
        positive_supply_candidate_uniform_gate_proved=False,J1_proved=False,formal_certificate_allowed=False)
    (run/'selected_candidate.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print('Repaired 70 saved rows: maximum numerical violation',max(residual[:70]),flush=True)
    print('Initial budget',budget,float(budget),'remaining',float(1-budget),flush=True)
    print('EXACT initial-direction Vdot lower',derivative_lower,float(derivative_lower),flush=True)
    print('EXACT ramp witness original Vdot',float(ramp_Vdot),'actual source cost',float(exact_cost),flush=True)
    print('The returned coefficients cannot satisfy uniform ZERO-supply dissipation.',flush=True)
    print('Full T=1 actual J<=1 OPEN; positive supply or a redesigned coefficient vector still needed.',flush=True)


def parent():
    root=Path(__file__).resolve().parent
    old=root/'output/lp-20260905T210233Z-e9203653'
    run=root/'output'/('post-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8])
    run.mkdir(parents=True,exist_ok=False)
    sources={'postprocess_lp.py':Path(__file__).resolve(),
             'lp_candidate_evidence.json':old/'lp_candidate_evidence.json',
             'lp_problem.json':old/'lp_problem.json','reference.json':old/'inputs/reference.json',
             'mass.csv':old/'inputs/mass.csv','potential.csv':old/'inputs/potential.csv',
             'source_line_check.json':root/'output/run-20260905T205645Z-63b40a65/candidate_evidence.json'}
    records={}
    for name,path in sources.items():
        shutil.copy2(path,run/name)
        records[name]=dict(original=str(path),sha256=hashlib.sha256((run/name).read_bytes()).hexdigest())
    command=[sys.executable,'-B',str(run/'postprocess_lp.py'),'--child']
    (run/'before_run.json').write_text(json.dumps(dict(created_utc=datetime.now(timezone.utc).isoformat(),command=command,snapshots=records),indent=2)+'\n',encoding='utf-8')
    print('Prospective coefficient postprocessing snapshot:',run,flush=True)
    with (run/'terminal.log').open('w',encoding='utf-8') as log:
        log.write('COMMAND '+json.dumps(command)+'\n');log.flush()
        proc=subprocess.run(command,cwd=run,stdout=log,stderr=subprocess.STDOUT,check=False)
        log.write('\nPOSTPROCESS_EXIT_CODE='+str(proc.returncode)+'\n')
    stable=all(hashlib.sha256((run/name).read_bytes()).hexdigest()==r['sha256'] for name,r in records.items())
    originals={name:hashlib.sha256(Path(r['original']).read_bytes()).hexdigest()==r['sha256'] for name,r in records.items()}
    outputs={name:hashlib.sha256((run/name).read_bytes()).hexdigest() for name in ('selected_candidate.json','terminal.log') if (run/name).exists()}
    (run/'receipt.json').write_text(json.dumps(dict(exit_code=proc.returncode,snapshots_unchanged=stable,originals_unchanged=originals,outputs=outputs,formal_certificate_allowed=False),indent=2)+'\n',encoding='utf-8')
    print((run/'terminal.log').read_text(encoding='utf-8'),flush=True)
    sys.exit(proc.returncode if proc.returncode else (0 if stable else 2))


if __name__=='__main__':
    if '--child' in sys.argv: child(Path(__file__).resolve().parent)
    else: parent()
