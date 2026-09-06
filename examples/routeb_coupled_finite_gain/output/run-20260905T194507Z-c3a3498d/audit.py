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
    def bilinear(x,y):
        lo=hi=F(0)
        terms=[(diagonal[j],x[j],y[j]) for j in range(6)]
        terms += [(F(-5),x[1],y[2]),(F(-5),x[2],y[1])]
        for weight,a,b in terms:
            values=[weight*u*v for u in a for v in b]
            lo+=min(values);hi+=max(values)
        return lo/GRID**2,hi/GRID**2
    x=interval[12][6:12];y=interval[13][6:12]
    xlo,xhi=bilinear(x,x);zlo,zhi=bilinear(y,y);vlo,vhi=bilinear(x,y)
    xlo=max(F(0),xlo)*F(5,8);xhi*=F(5,8)
    zlo=max(F(0),zlo)*F(10,13);zhi*=F(10,13)
    difference=max(abs(xlo-zhi),abs(xhi-zlo))
    off=max(abs(vlo),abs(vhi))
    # Exact 2x2 spectral formula; squared offdiagonal weight is rational.
    return (xhi+zhi+sqrtup(difference**2+4*F(5,8)*F(10,13)*off**2))/2


def positive_definite_integer(A):
    """Fraction-free Sylvester test. Only positive pivots discharge this gate."""
    B=[row[:] for row in A];previous=1;pivots=[]
    for k in range(len(B)):
        pivot=B[k][k]
        if pivot<=0: return False,pivots
        pivots.append(pivot)
        for i in range(k+1,len(B)):
            for j in range(k+1,len(B)):
                numerator=pivot*B[i][j]-B[i][k]*B[k][j]
                assert numerator%previous==0
                B[i][j]=numerator//previous
        previous=pivot
    return True,pivots


def integrated_nominal_bound(glow,ghigh):
    denominator=2*104*GRID**2*CELLS
    midpoint=[[glow[i][j]+ghigh[i][j] for j in range(13)] for i in range(13)]
    error=max(sum(ghigh[i][j]-glow[i][j] for j in range(12)) for i in range(12))
    def gate(lam):
        A=[[(lam.numerator*denominator if i==j else 0)-
            (midpoint[i][j]+(error if i==j else 0))*lam.denominator
            for j in range(12)] for i in range(12)]
        return positive_definite_integer(A)
    hi=F(max(sum(abs(v) for v in row[:12]) for row in midpoint[:12])+error+1,denominator)
    assert gate(hi)[0]
    lo=F(0)
    for _ in range(18):
        mid=(lo+hi)/2
        if gate(mid)[0]: hi=mid
        else: lo=mid
    lam=F(ceil(hi*10**9),10**9)
    ok,pivots=gate(lam);assert ok
    # Full initial ball and one constant ramp coefficient, AFTER integration.
    b2=sum(F(max(abs(glow[i][12]),abs(ghigh[i][12]))*2,denominator)**2 for i in range(12))
    d=F(2*ghigh[12][12],denominator)
    bound=F(9,400)*lam+F(3,10)*sqrtup(F(3))*sqrtup(b2)+3*d
    return bound,dict(initial_Gram_lambda_upper=str(lam),Gram_midpoint_denominator=str(denominator),
                      Gram_midpoint_numerators=midpoint,initial_Gram_operator_error=str(F(error,denominator)),
                      positive_integer_Sylvester_pivots=list(map(str,pivots)),
                      initial_input_cross_norm_upper=str(sqrtup(b2)),input_Gram_upper=str(d))


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
    glow=[[0]*13 for _ in range(13)];ghigh=[[0]*13 for _ in range(13)]
    active=list(range(12))+[13]
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
        for i,ii in enumerate(active):
            for j,jj in enumerate(active):
                for row,weight in ((12,65),(13,80)):
                    vals=[a*b for a in interval[row][ii] for b in interval[row][jj]]
                    glow[i][j]+=weight*min(vals);ghigh[i][j]+=weight*max(vals)
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
    integrated,gram_receipt=integrated_nominal_bound(glow,ghigh)
    Ncap=F(ceil(min(nominal_integral,integrated)*10**6),10**6)
    Hcap=F(ceil(gain*10**6),10**6)
    gates=[]
    for denominator in (10,12,15,16,20,25,40,50,100,200,500,1000,2000,10000):
        J=F(1,denominator)
        upper=(sqrtup(Ncap)+Hcap*sqrtup(J))**2
        gates.append(dict(J=str(J),actual_cost_upper=str(upper),sufficient_for_R_le_point1=upper<=F(1,10)))
    result=dict(status='RATIONAL_FULL_TIME_COUPLED_GAIN_ENCLOSURE',
        actual_DH_flowpipe_proved=False,nonlinear_J_bound_proved=False,Lean_verified=False,
        input='all full12 initial norm<=3/20; w(t)=c*t,c^2<=3,T=1',
        nominal_model_stability_assumed=False,time_cells=CELLS,local_degree=DEGREE,
        fixed_grid=GRID,step_exponential=exp_receipt,local_tail=str(tail),
        nominal_integrated_cost_upper=str(integrated),pointwise_Frobenius_integral_upper=str(nominal_integral),
        integrated_Gram_receipt=gram_receipt,N_rational_cap=str(Ncap),
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
