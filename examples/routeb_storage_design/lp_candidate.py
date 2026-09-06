"""Second and final bounded static LP screen. All output is candidate evidence."""
from pathlib import Path
from fractions import Fraction as F
import csv
import hashlib
import json
import numpy as np
import scipy
from scipy.optimize import linprog

RUN = Path(__file__).resolve().parent
INPUTS = RUN/'inputs'
DEGREE = 8


def load(name):
    return json.loads((INPUTS/name).read_text(encoding='utf-8'))


def fm(a):
    return np.array([[float(F(x)) for x in row] for row in a])


def read_fourier(name, mass=False):
    with (INPUTS/name).open(encoding='utf-8-sig',newline='') as f:
        rows = list(csv.DictReader(f))
    nu = np.array([[int(row['nu'+str(i)]) for i in range(1,7)] for row in rows])
    coeff = np.array([float(F(int(r['real_num']),int(r['real_den'])))+
                     1j*float(F(int(r['imag_num']),int(r['imag_den']))) for r in rows])
    if mass:
        ij = np.array([[int(r['row'])-1,int(r['col'])-1] for r in rows])
        return nu,coeff,ij
    return nu,coeff


def main():
    before = json.loads((RUN/'before_run.json').read_text(encoding='utf-8'))
    for name,r in before['snapshots'].items():
        assert hashlib.sha256((RUN/name).read_bytes()).hexdigest() == r['sha256']
    ref = load('reference.json')
    M0,R,H0 = fm(ref['M0']),fm(ref['M0_inverse']),fm(ref['H0'])
    K,D,G = np.array(list(map(lambda x:float(F(x)),ref['Kp']))),np.array(list(map(lambda x:float(F(x)),ref['D']))),np.array(list(map(lambda x:float(F(x)),ref['G'])))
    S = np.diag(K)+H0
    Q = np.diag([3,8,95/7,165/7,45,90]);Q[1,2]=Q[2,1]=-5
    L = np.linalg.inv(Q)
    mn,mc,mij = read_fourier('mass.csv',True)
    un,uc = read_fourier('potential.csv')
    U0 = uc.real.sum()
    functional_rows = fm(load('functionals.json')['rows'])
    supports = load('nominal_J_functional_bounds.json')['cells']
    def caps_at(t):
        cell = supports[min(127,int(t*128))]
        return np.array([float(F(n)+F(k)) for n,k in zip(cell['nominal'],cell['kernel_sqrt'])])
    def source(q,v,w):
        terms = mc*np.exp(1j*(mn@q))
        M = np.eye(6)*1e-6
        np.add.at(M,(mij[:,0],mij[:,1]),terms.real)
        DM = np.zeros((6,6,6))
        for k in range(6): np.add.at(DM[:,:,k],(mij[:,0],mij[:,1]),(1j*mn[:,k]*terms).real)
        up = uc*np.exp(1j*(un@q))
        U = up.real.sum()
        grad = ((1j*up[:,None])*un).real.sum(axis=0)
        C = np.einsum('ijk,j,k->i',DM,v,v)-.5*np.einsum('jki,j,k->i',DM,v,v)
        a0 = R@(-S@q-D*v+G*w)
        dM = M0-M
        r = dM@a0+H0@q-grad-C
        h = R@r
        z = (R@L-np.eye(6))@h
        e = dM@(2*h+z)
        cost = h@L@h+2*(z+h)@dM@h+e@Q@e
        actual_delta = np.linalg.solve(M,r)
        actual_cost = actual_delta@L@actual_delta
        Rp = U-U0-.5*q@H0@q
        W0 = .5*v@M@v+Rp+7/75*q[3]**2
        Wdot = -v@S@q-v@(D*v)+v@G*w+14/75*q[3]*v[3]
        return dict(cost=float(cost),actual_cost=float(actual_cost),W0=float(W0),W0dot=float(Wdot),
                    mass_lower_eig_display=float(np.linalg.eigvalsh(M-L).min()),
                    r=r.tolist(),M=M.tolist(),a0=a0.tolist(),C=C.tolist())
    points=[]
    def add_point(name,t,x,c,shrink=False):
        x=np.array(x,dtype=float)
        factor=1.
        if shrink:
            vals=np.abs(functional_rows[:,:12]@x)
            ratios=np.divide(.9*caps_at(t),vals,out=np.full_like(vals,np.inf),where=vals>0)
            factor=min(1.,float(ratios.min()))
            block=1.5*(x[3]**2+x[4]**2)+.8*(x[9]**2+x[10]**2)
            if block>0: factor=min(factor,np.sqrt(.9*(28/5)/block))
            x=x*factor
        assert abs(c)<=np.sqrt(3)+1e-12
        if t==0: assert x@x<=9/400+1e-12
        assert 1.5*(x[3]**2+x[4]**2)+.8*(x[9]**2+x[10]**2)<=28/5+1e-12
        data=source(x[:6],x[6:],t*c)
        points.append(dict(name=name,t=t,x=x.tolist(),c=c,w=t*c,shrink_factor=factor,**data))
    for i in range(12):
        for sign in (-1,1):
            x=np.zeros(12);x[i]=sign*.15
            add_point('initial_axis_'+str(i)+'_'+str(sign),0.,x,0.)
    for i in (1,3):
        for sign in (-1,1):
            x=np.zeros(12);x[i]=.15/np.sqrt(2);x[i+6]=sign*.15/np.sqrt(2)
            add_point('initial_mixed_'+str(i)+'_'+str(sign),0.,x,sign*np.sqrt(3))
    for t in (.25,.5,.75,1.):
        templates=[]
        for sign in (-1,1):
            x=np.zeros(12);x[1]=2*t;x[7]=sign*2*t
            templates.append(('q2v2_'+str(sign),x,0.))
        x=np.zeros(12);x[2]=2*t;x[8]=2*t;templates.append(('q3v3',x,0.))
        x=np.zeros(12);x[3]=.6*t;x[9]=.6*t;templates.append(('q4v4',x,0.))
        x=np.zeros(12);x[4]=.45*t;x[10]=.6*t;templates.append(('q5v5',x,0.))
        for sign in (-1,1):
            x=np.zeros(12);x[1]=1.5*t;x[2]=-.6*t;x[7]=1.5*t;x[8]=-.6*t
            templates.append(('remote_ramp_'+str(sign),x,sign*np.sqrt(3)))
        x=np.zeros(12);x[0]=.3*t;x[6]=.3*t;x[5]=.2*t;x[11]=.2*t
        templates.append(('cyclic',x,0.))
        for name,x,c in templates: add_point(name+'_'+str(t),t,x,c,True)
    for t in (0.,.25,.5,.75,1.):
        for sign in (-1,1): add_point('zero_state_ramp_'+str(t)+'_'+str(sign),t,np.zeros(12),sign*np.sqrt(3))
    assert len(points)==70
    for t in (.25,.5,.75):
        x=np.zeros(12);x[6:]=G/1000
        add_point('ramp_G_epsilon_'+str(t),t,x,1.)
        if t==.5:
            witness=load('exact_witness.json')['exact_ramp_witness']
            points[-1].update(cost=float(F(witness['actual_cost'])),actual_cost=float(F(witness['actual_cost'])),
                             W0=float(F(witness['W0'])),W0dot=float(F(witness['W0dot'])),
                             exact_witness_imported=True)
    for i in range(6):
        x=np.zeros(12);x[6+i]=.001
        add_point('ramp_axis_epsilon_'+str(i+1),.5,x,1.)
    x=np.zeros(12);x[1]=.01;x[7]=.015
    add_point('initial_exact_direction',0.,x,0.)
    assert len(points)==80
    point_count=len(points)
    names=[name for j in range(1,DEGREE+1) for name in ['a'+str(j)]+['p'+str(j)+'_'+str(i+1) for i in range(6)]+['c'+str(j)]]+['beta']
    lp_rows=[];rhs=[]
    for p in points:
        t=p['t'];tau=1-t;x=np.array(p['x']);q=x[:6];v=x[6:];c=p['c']
        row=np.zeros(65)
        for j in range(1,DEGREE+1):
            power=tau**j;dot=-j*tau**(j-1);offset=(j-1)*8
            row[offset]=dot*p['W0']+power*p['W0dot']
            row[offset+1:offset+7]=dot*q*q+power*2*q*v
            row[offset+7]=dot*c*c
        lp_rows.append(row);rhs.append(-(1+1e-8)*p['cost'])
    objective=np.zeros(65);objective[-1]=9/400
    objective[0:64:8]=3/10000;objective[7:64:8]=3
    row=np.zeros(65);row[0:64:8]=.5;row[-1]=-1
    lp_rows.append(row);rhs.append(0.)
    for i in range(6):
        row=np.zeros(65);row[1+i:64:8]=1;row[-1]=-1
        if i==3: row[0:64:8]=7/75
        lp_rows.append(row);rhs.append(0.)
    AA,bb=np.array(lp_rows),np.array(rhs)
    print('Starting SECOND AND FINAL LP: 65 variables,',len(bb),'inequalities, 80 static source points.',flush=True)
    result=linprog(objective,A_ub=AA,b_ub=bb,bounds=(0,None),method='highs',
                   options={'time_limit':30,'primal_feasibility_tolerance':1e-10,'dual_feasibility_tolerance':1e-10})
    report=dict(status='NUMERICAL_COLLOCATION_ONLY',numpy_version=np.__version__,scipy_version=scipy.__version__,
                solver_status=int(result.status),solver_message=str(result.message),solver_success=bool(result.success),
                point_count=len(points),variables=names,degree=DEGREE,eta='0, analytic candidate only',
                uniform_gate_proved=False,J1_proved=False,formal_certificate_allowed=False,
                no_ODE_solves=True,no_dependency_installs=True,number_of_LP_calls_in_this_run=1,
                total_LP_calls=2,coefficient_inflation_used=False)
    if result.x is not None:
        rational=[F(int(round(max(0.,v)*10**12)),10**12) for v in result.x]
        beta_before=rational[-1]
        asum=sum(rational[j*8] for j in range(8))
        psums=[sum(rational[j*8+1+i] for j in range(8)) for i in range(6)]
        beta_requirements=[asum/2]+[p+(F(7,75)*asum if i==3 else 0) for i,p in enumerate(psums)]
        rational[-1]=max(beta_before,*beta_requirements)
        exact_beta_slacks=[rational[-1]-x for x in beta_requirements]
        assert min(exact_beta_slacks)>=0 and min(rational)>=0
        xx=np.array(list(map(float,rational)))
        residual=AA@xx-bb
        max_violation=float(residual.max())
        report.update(raw_objective=float(result.fun),rational_coefficients=dict(zip(names,map(str,rational))),
                      rational_initial_budget=str(sum(F(3,10000)*rational[j*8]+3*rational[j*8+7] for j in range(8))+F(9,400)*rational[-1]),
                      candidate_budget_display=float(objective@xx),maximum_constraint_violation=max_violation,
                      maximum_source_constraint_violation=float(residual[:point_count].max()),
                      numerical_budget_below_one=bool(objective@xx<1),
                      numerical_constraints_within_1e_minus_8=bool(max_violation<=1e-8),
                      per_point_slack=(-residual[:point_count]).tolist(),
                      beta_before_repair=str(beta_before),beta_after_repair=str(rational[-1]),
                      exact_beta_requirements=list(map(str,beta_requirements)),
                      exact_beta_slacks=list(map(str,exact_beta_slacks)),
                      exact_coefficients_nonnegative=True,
                      lower_bound_marginals=None if result.lower.marginals is None else result.lower.marginals.tolist(),
                      inequality_marginals=None if result.ineqlin.marginals is None else result.ineqlin.marginals.tolist())
        print('Raw candidate LP objective:',result.fun,flush=True)
        print('Rational candidate initial budget:',report['rational_initial_budget'],report['candidate_budget_display'],flush=True)
        print('Exact beta before / after:',beta_before,rational[-1],flush=True)
        print('Maximum numerical constraint violation:',max_violation,flush=True)
        print('Nonzero coefficients:',{name:str(value) for name,value in zip(names,rational) if value},flush=True)
    (RUN/'lp_problem.json').write_text(json.dumps(dict(points=points,names=names,A_ub=AA.tolist(),b_ub=bb.tolist(),objective=objective.tolist()),indent=2)+'\n',encoding='utf-8')
    (RUN/'lp_candidate_evidence.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('Solver status (candidate only):',result.status,result.message,flush=True)
    print('Full T=1 actual J<=1: OPEN',flush=True)


if __name__=='__main__':
    main()
