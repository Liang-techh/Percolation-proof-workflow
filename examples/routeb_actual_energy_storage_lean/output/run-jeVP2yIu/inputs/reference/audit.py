"""Exact six-axis nominal coefficient audit; only Fraction arithmetic.

Execute the preserved copy via verify.py. All reads use pre-run input snapshots;
all generated writes remain in that same attempt directory. No numerical flow.
"""
import csv
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import re

RUN=Path(__file__).resolve().parent
N=6
def zeros(n,m): return [[Q(0) for _ in range(m)] for _ in range(n)]
def eye(n): return [[Q(i==j) for j in range(n)] for i in range(n)]
def transpose(a): return [list(r) for r in zip(*a)]
def mul(a,b):
    assert len(a[0])==len(b)
    return [[sum(x*y for x,y in zip(r,c)) for c in zip(*b)] for r in a]
def add(a,b): return [[x+y for x,y in zip(r,s)] for r,s in zip(a,b)]
def neg(a): return [[-x for x in r] for r in a]
def diag(v): return [[x if i==j else Q(0) for j in range(len(v))] for i,x in enumerate(v)]
def inverse(a):
    n=len(a); z=[r[:]+e for r,e in zip(a,eye(n))]
    for j in range(n):
        pivot=next(i for i in range(j,n) if z[i][j])
        z[j],z[pivot]=z[pivot],z[j]
        d=z[j][j]; z[j]=[x/d for x in z[j]]
        for i in range(n):
            if i!=j:
                d=z[i][j]; z[i]=[x-d*y for x,y in zip(z[i],z[j])]
    assert [r[:n] for r in z]==eye(n)
    return [r[n:] for r in z]
def ldl(a):
    n=len(a); L=eye(n); piv=[]
    for j in range(n):
        d=a[j][j]-sum(L[j][k]**2*piv[k] for k in range(j))
        assert d>0; piv.append(d)
        for i in range(j+1,n):
            L[i][j]=(a[i][j]-sum(L[i][k]*L[j][k]*piv[k] for k in range(j)))/d
    assert mul(mul(L,diag(piv)),transpose(L))==a
    return L,piv
def records(name):
    with (RUN/'inputs'/name).open(newline='',encoding='utf-8') as f: return list(csv.DictReader(f))
def load(records,key):
    out={}
    for r in records:
        nu=tuple(int(r[f'nu{i}']) for i in range(1,7))
        kk=tuple(int(r[i]) for i in key)+nu
        assert kk not in out
        out[kk]=(Q(int(r['real_num']),int(r['real_den'])),Q(int(r['imag_num']),int(r['imag_den'])))
    return out
def vector(source,name):
    raw=re.search(r'(?m)^'+re.escape(name)+r'\s*=\s*\[([^\]]+)\]',source)[1]
    return [Q(s.strip()) for s in raw.split(',')]

def main():
    manifest=json.loads((RUN/'before_run.json').read_text(encoding='utf-8'))
    for name,e in manifest['inputs'].items():
        assert hashlib.sha256((RUN/'inputs'/name).read_bytes()).hexdigest()==e['sha256']
    massrows=records('routeB_fourier_mass_full_rational.csv')
    potrows=records('routeB_fourier_potential_rational.csv')
    assert len(massrows)==610 and len(potrows)==17
    mass=load(massrows,('row','col')); pot=load(potrows,())
    for key,(a,b) in mass.items():
        i,j,*nu=key
        assert mass[(i,j,*[-x for x in nu])]==(a,-b)
        assert mass[(j,i,*nu)]==(a,b)
    for nu,(a,b) in pot.items():
        assert b==0 and pot[tuple(-x for x in nu)]==(a,0)
    julia=(RUN/'inputs/dhport_lib.jl').read_text(encoding='utf-8')
    mu=Q(re.search(r'const MASS_REGULARIZER\s*=\s*([\deE.+-]+)',julia)[1])
    assert mu==Q(1,1000000)
    kp=vector(julia,'Kp'); kd=vector(julia,'Kd'); friction=vector(julia,'b_fr')
    damping=[x+y for x,y in zip(kd,friction)]
    ivals=vector(julia,'I_val'); gw_numer=vector(julia,'gw_coef')
    assert re.search(r'(?m)^gw_coef\s*=.*\]\s*\./\s*I_val',julia)
    G=[(x/i)*i for x,i in zip(gw_numer,ivals)]
    assert kp==list(map(Q,['1','4/5','7/10','3/5','1/2','2/5']))
    assert damping==list(map(Q,['13/10','11/10','19/20','4/5','13/20','1/2']))
    assert G==list(map(Q,['1','1/2','3/10','1/5','1/10','1/20']))
    K=diag(kp); D=diag(damping)
    M=diag([mu]*6); Mi=zeros(6,6)
    for key,(a,b) in mass.items():
        i,j=key[:2]; M[i-1][j-1]+=a; Mi[i-1][j-1]+=b
    assert Mi==zeros(6,6) and M==transpose(M)
    H=zeros(6,6); gradient=[Q(0)]*6
    for nu,(a,b) in pot.items():
        for i in range(6):
            gradient[i]-=nu[i]*b
            for j in range(6): H[i][j]-=nu[i]*nu[j]*a
    assert gradient==[0]*6 and H==transpose(H)
    J=inverse(M)
    assert mul(M,J)==eye(6) and mul(J,M)==eye(6)
    L,pivots=ldl(M)
    S=add(K,H); c=Q(20601,400000)
    assert H[3]==[0]*6 and H[4]==[0,-c,-c,0,-c,0]
    assert S[1][1]<0  # Exact negative stiffness witness e2, no eigenvalue screen.
    accQ=neg(mul(J,S)); accV=neg(mul(J,D)); accW=mul(J,[[x] for x in G])
    force=[[-x for x in S[i]]+[-x for x in D[i]]+[G[i]] for i in range(6)]
    acc=[accQ[i]+accV[i]+accW[i] for i in range(6)]
    assert mul(M,acc)==force  # 6*13 exact polynomial coefficients, all q,v,w.
    A=[zeros(6,6)[i]+eye(6)[i] for i in range(6)]+[accQ[i]+accV[i] for i in range(6)]
    B=[Q(0)]*6+[r[0] for r in accW]
    assert len(A)==12 and all(len(row)==12 for row in A)
    mref=[Q(350003,3000000),Q(200739,4000000)]
    block=[3,4]; remote=[0,1,2,5]
    assert [[M[i][j] for j in block] for i in block]==diag(mref)
    MBD=[[M[i][j] for j in remote] for i in block]
    assert MBD==[[Q(7,60),0,0,Q(1,60)],
                 [Q(-21,80000),Q(41827,800000),Q(8189,160000),0]]
    E=[]
    for m,i in zip(mref,block):
        row=[m*x for x in acc[i]]
        row[i]+=kp[i]; row[6+i]+=damping[i]; row[12]-=G[i]
        E.append(row)
    alt=neg(mul(MBD,[acc[j] for j in remote]))
    for n,i in enumerate(block):
        for j in range(6): alt[n][j]-=H[i][j]
    assert E==alt  # e0=-M0_BD*a0_D-H0_B*q (R=M0_BB).
    # Bind exact source map to the same construction used in linear_direction.py.
    aug=zeros(14,14)
    for i in range(12): aug[i][:12]=A[i][:]; aug[i][12]=B[i]
    aug[12][13]=1
    Eaug=[]
    for m,i in zip(mref,block):
        row=[m*x for x in aug[6+i]]
        row[i]+=kp[i]; row[6+i]+=damping[i]; row[12]-=G[i]
        Eaug.append(row)
    assert Eaug==[r+[Q(0)] for r in E]
    earlier=RUN/'inputs/linear_result.json'
    earlier_comparison='not supplied'
    if earlier.exists():
        previous=json.loads(earlier.read_text(encoding='utf-8'))
        assert [[Q(x) for x in r] for r in previous['mass_zero']]==M
        assert [[Q(x) for x in r] for r in previous['potential_hessian']]==H
        earlier_comparison='EXACT_M0_AND_H0_MATCH'
    weights=[Q(5,8),Q(10,13)]
    cost=mul(mul(transpose(E),diag(weights)),E)
    assert cost==transpose(cost)
    # This factorization, not rounded eigenvalues, proves PSD of the cost Gram.
    names=[f'q{i}' for i in range(1,7)]+[f'v{i}' for i in range(1,7)]+['w']
    support=[{names[j]:str(x) for j,x in enumerate(row) if x} for row in E]
    remote_names=[names[j] for j in remote]+[names[6+j] for j in remote]
    remote_support=[[name for name in remote_names if name in row] for row in support]
    cross=[dict(x=names[i],y=names[j],coefficient=2*cost[i][j])
           for i in range(13) for j in range(i+1,13) if cost[i][j]]
    result=dict(status='EXACT_COUPLED_NOMINAL_REFERENCE_PASS',arithmetic='fractions.Fraction',
        Lean_compiled=False,physical_DH_identification_proved=False,Float64_binding_proved=False,
        nominal_stability_assumed=False,trajectories_or_eigenvalues_computed=False,
        mass_row_count=len(massrows),potential_row_count=len(potrows),mu=mu,
        Kp=kp,D=damping,G=G,M0=M,H0=H,gradient_U0=gradient,stiffness_K_plus_H0=S,
        M0_inverse=J,M0_LDL=dict(L=L,positive_pivots=pivots),
        inverse_left_and_right_entry_checks=72,nominal_balance_coefficient_checks=78,
        residual_identity_coefficient_checks=26,
        negative_stiffness_witness=dict(vector=[0,1,0,0,0,0],quadratic_value=S[1][1]),
        acceleration_q=accQ,acceleration_v=accV,acceleration_w=[r[0] for r in accW],
        A12=A,B12=B,Mref_BB=diag(mref),M0_BD=MBD,
        residual_state_matrix=[r[:12] for r in E],residual_w=[r[12] for r in E],
        residual_all13=E,coordinate_order=names,residual_support=support,
        residual_remote_support=remote_support,weighted_cost_Gram13=cost,
        weighted_cost_metric=weights,nonzero_cost_cross_terms=cross,
        augmented_A14=aug,augmented_E2x14=Eaug,
        earlier_linear_direction_comparison=earlier_comparison,
        input_evidence=manifest['inputs'])
    (RUN/'reference.json').write_text(json.dumps(result,default=str,indent=2)+'\n',encoding='utf-8')
    for name,e in manifest['inputs'].items():
        assert hashlib.sha256((RUN/'inputs'/name).read_bytes()).hexdigest()==e['sha256']
    print(result['status'])
    print('rows mass/potential:',len(massrows),len(potrows))
    print('inverse products: 72; nominal balance: 78; residual identity: 26 exact scalar checks')
    print('LDL positive pivots:',*[str(x) for x in pivots])
    print('H0:',[[str(x) for x in row] for row in H])
    print('negative stiffness witness e2:',S[1][1])
    print('remote residual support:',remote_support)
    print('nonzero residual entries:',[len(row) for row in support],'; cost cross terms:',len(cross))
    print('earlier saved coefficients:',earlier_comparison)

if __name__=='__main__': main()
