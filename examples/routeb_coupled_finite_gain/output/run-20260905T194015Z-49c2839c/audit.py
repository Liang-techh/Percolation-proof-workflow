"""Exact-rational finite-horizon coupled nominal and correction-gain bounds.

Whole time cells, full initial ball, entire ramp family. Not an actual DH
flowpipe: the coupled nonlinear residual integral remains a separate premise.
"""
from fractions import Fraction as F
from math import factorial,isqrt
from pathlib import Path
import hashlib
import json
import sys

DIM=14
GRID=10**40
SQGRID=10**20
CELLS=128
DEGREE=12


def zeros(r,c): return [[F(0) for _ in range(c)] for _ in range(r)]
def eye(n): return [[F(int(i==j)) for j in range(n)] for i in range(n)]
def fmul(A,B):
    cols=list(zip(*B))
    return [[sum(a*b for a,b in zip(row,col)) for col in cols] for row in A]
def fscale(A,x): return [[a*x for a in row] for row in A]
def fadd(A,B): return [[a+b for a,b in zip(row,col)] for row,col in zip(A,B)]
def norm(A): return max(sum(abs(a) for a in row) for row in A)
def ceil(x): return -((-x.numerator)//x.denominator)
def grid(A):
    P=[[a.numerator*GRID//a.denominator for a in row] for row in A]
    err=max(sum(abs(a-F(p,GRID)) for a,p in zip(row,ps)) for row,ps in zip(A,P))
    return P,ceil(err*GRID)
def imul(A,B):
    cols=list(zip(*B))
    return [[sum(a*b for a,b in zip(row,col))//GRID for col in cols] for row in A]
def product(A,ea,B,eb):
    P=imul(A,B)
    error=(norm(A)*eb+norm(B)*ea+ea*eb+GRID-1)//GRID+len(B[0])
    return P,error
def sqrtup(x):
    assert x>=0
    n=isqrt(x.numerator*SQGRID*SQGRID//x.denominator)
    return F(n+1,SQGRID)


def step_exponential(A,h):
    B=fscale(A,h);squarings=0
    while norm(B)>F(1,2): B=fscale(B,F(1,2));squarings+=1
    P=eye(DIM);term=eye(DIM)
    degree=28
    for n in range(1,degree+1):
        term=fscale(fmul(term,B),F(1,n));P=fadd(P,term)
    tail=2*norm(B)**(degree+1)/factorial(degree+1)
    P,error=grid(P);error+=ceil(tail*GRID)
    for _ in range(squarings): P,error=product(P,error,P,error)
    return P,error,dict(taylor_degree=degree,scalings=squarings,operator_error=str(F(error,GRID)))


def maxsquare(lo,hi): return max(lo*lo,hi*hi)
def signal_cost(interval,rows,weights):
    # Frobenius dominates the induced operator norm, preserving a SINGLE
    # 12-dimensional radius for all selected outputs, not one radius per row.
    f2=sum(w*sum(maxsquare(*interval[i][j]) for j in range(12)) for i,w in zip(rows,weights))/GRID**2
    b2=sum(w*maxsquare(*interval[i][13]) for i,w in zip(rows,weights))/GRID**2
    return (F(3,20)*sqrtup(f2)+sqrtup(F(3))*sqrtup(b2))**2


def kernel_squared(interval):
    diagonal=[F(3),F(8),F(95,7),F(165,7),F(45),F(90)]
    result=F(0)
    for row,w in zip((12,13),(F(5,8),F(10,13))):
        z=interval[row][6:12]
        cross_min=min(a*b for a in z[1] for b in z[2])
        upper=sum(d*maxsquare(*ab) for d,ab in zip(diagonal,z))-10*cross_min
        assert upper>=0
        result+=w*upper/GRID**2
    return result


def main():
    run=Path(sys.argv[1]).resolve()
    reference=run/'inputs/reference.json'
    data=json.loads(reference.read_text(encoding='utf-8'))
    assert data['status']=='EXACT_COUPLED_NOMINAL_REFERENCE_PASS'
    A=[[F(v) for v in row] for row in data['augmented_A14']]
    C=eye(DIM)[:12]+[[F(v) for v in row] for row in data['augmented_E2x14']]
    h=F(1,CELLS)
    E,ee,exp_receipt=step_exponential(A,h)
    series=[];power=C
    for n in range(DEGREE+1):
        series.append(grid(power))
        if n<DEGREE: power=fscale(fmul(power,A),h/F(n+1))
    a=norm(A)*h
    assert a<F(DEGREE+2)
    # Ratio after the first omitted term <=a/(degree+2); geometric tail.
    tail=a**(DEGREE+1)/factorial(DEGREE+1)/(1-a/F(DEGREE+2))
    cnorm=[sum(abs(v) for v in row) for row in C]
    P,ep=grid(eye(DIM))
    nominal_integral=F(0);dynamic_gain=F(0);pmax=F(0)
    states=[F(0)]*12;receipts=[]
    for cell in range(CELLS):
        polys=[product(T,e,P,ep) for T,e in series]
        common_error=sum(e for T,e in polys)
        interval=[]
        for i in range(14):
            error=common_error+ceil(cnorm[i]*tail*(norm(P)+ep))
            row=[]
            for j in range(14):
                base=polys[0][0][i][j]
                low=base+sum(min(0,T[i][j]) for T,e in polys[1:])-error
                high=base+sum(max(0,T[i][j]) for T,e in polys[1:])+error
                row.append((low,high))
            interval.append(row)
        ncost=signal_cost(interval,(12,13),(F(5,8),F(10,13)))
        kgain=sqrtup(kernel_squared(interval))
        pb=signal_cost(interval,(3,4,9,10),(F(3,2),F(3,2),F(4,5),F(4,5)))
        nominal_integral+=h*ncost;dynamic_gain+=h*kgain;pmax=max(pmax,pb)
        for i in range(12):
            states[i]=max(states[i],sqrtup(signal_cost(interval,(i,),(F(1),))))
        receipts.append(dict(time=[str(cell*h),str((cell+1)*h)],
                             nominal_cost_sup=str(ncost),kernel_norm_sup=str(kgain),
                             nominal_p_sup=str(pb),transition_error=str(F(ep,GRID))))
        P,ep=product(E,ee,P,ep)
    # Exact T=1 transition enclosure, with no entire-cell interpolation loss.
    CP,ec=product(series[0][0],series[0][1],P,ep)
    endpoint=[[(v-ec,v+ec) for v in row] for row in CP]
    terminal=signal_cost(endpoint,(3,4,9,10),(F(3),F(3),F(2),F(2)))
    m4=F(350003,3000000);m5=F(200739,4000000)
    direct_squared=max(F(5,8)*m4*m4*F(165,7),F(10,13)*m5*m5*45)
    direct=sqrtup(direct_squared);gain=direct+dynamic_gain
    # User-facing rational caps are rounded UP; candidate budget gates use
    # those caps, never display floats or an unenclosed nominal trajectory.
    Ncap=F(ceil(nominal_integral*10**6),10**6)
    Hcap=F(ceil(gain*10**6),10**6)
    gates=[]
    for denominator in (10,20,25,40,50,100,200,500,1000,2000,10000):
        J=F(1,denominator)
        upper=(sqrtup(Ncap)+Hcap*sqrtup(J))**2
        gates.append(dict(J=str(J),actual_cost_upper=str(upper),sufficient_for_R_le_point1=upper<=F(1,10)))
    result=dict(status='RATIONAL_FULL_TIME_COUPLED_GAIN_ENCLOSURE',
        actual_DH_flowpipe_proved=False,nonlinear_J_bound_proved=False,Lean_verified=False,
        input='all full12 initial norm<=3/20; w(t)=c*t,c^2<=3,T=1',
        nominal_model_stability_assumed=False,time_cells=CELLS,local_degree=DEGREE,
        fixed_grid=GRID,step_exponential=exp_receipt,local_tail=str(tail),
        nominal_integrated_cost_upper=str(nominal_integral),N_rational_cap=str(Ncap),
        correction_direct_norm_upper=str(direct),correction_dynamic_L1_upper=str(dynamic_gain),
        correction_gain_H_upper=str(gain),H_rational_cap=str(Hcap),
        nominal_all_time_p_upper=str(pmax),nominal_terminal_q_upper=str(terminal),
        nominal_state_absolute_caps=list(map(str,states)),candidate_J_gates=gates,
        gain_meaning='R_actual^(1/2)<=sqrt(N)+H sqrt(J), J=integral delta^T L delta<=integral Q(r); variation-of-constants and finite-horizon convolution inequalities are explicit analytical premises, not new Lean theorems here',
        Q_metric='diag(3,8,95/7,165/7,45,90),Q23=Q32=-5; L=Q^-1',
        matrix_error_method='Induced-infinity operator error, rational grid rounding charged under every product; complete time cells covered by local Taylor interval powers and geometric matrix tail',
        reference_sha256=hashlib.sha256(reference.read_bytes()).hexdigest(),cells=receipts)
    (run/'results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(result['status'])
    print('N<=',Ncap,'H<=',Hcap,'nominal P<=',float(pmax),'nominal Qterminal<=',float(terminal))
    print('nominal state caps display',list(map(float,states)))
    print('sufficient hypothetical J gates:',[g['J'] for g in gates if g['sufficient_for_R_le_point1']])
    print('ACTUAL_NONLINEAR_J_NOT_PROVED')


if __name__=='__main__': main()
