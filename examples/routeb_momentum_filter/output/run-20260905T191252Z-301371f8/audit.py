"""Bounded exact-rational interval impulse audit. Standard library only.

Run through verify.py: it snapshots sources and opens the terminal log BEFORE
this program runs. No target writes, trajectories, downloads, or Lean claims.
"""
from fractions import Fraction as Q
from math import isqrt
from pathlib import Path
import hashlib
import json
import sys

HERE=Path(__file__).resolve().parent
DEN=10**24
def floor(x): return Q(x.numerator*DEN//x.denominator,DEN)
def ceil(x): return -floor(-x)
class I:
    def __init__(self,a,b=None): self.lo=Q(a); self.hi=Q(a if b is None else b)
    def __add__(self,b):
        b=iv(b); return I(floor(self.lo+b.lo),ceil(self.hi+b.hi))
    __radd__=__add__
    def __neg__(self): return I(-self.hi,-self.lo)
    def __sub__(self,b): return self+-iv(b)
    def __rsub__(self,b): return iv(b)+-self
    def __mul__(self,b):
        b=iv(b); z=[a*c for a in (self.lo,self.hi) for c in (b.lo,b.hi)]
        return I(floor(min(z)),ceil(max(z)))
    __rmul__=__mul__
    def __truediv__(self,b):
        b=iv(b); assert b.lo>0 or b.hi<0
        return self*I(floor(1/b.hi),ceil(1/b.lo))
    def __rtruediv__(self,b): return iv(b)/self
    def absmax(self): return max(abs(self.lo),abs(self.hi))
def iv(x): return x if isinstance(x,I) else I(x)
def sq(x):
    x=iv(x); return I(0 if x.lo<=0<=x.hi else floor(min(x.lo*x.lo,x.hi*x.hi)),ceil(x.absmax()**2))
def sqrtq(x):
    assert x>=0; n=isqrt(x.numerator*DEN*DEN//x.denominator)
    return I(Q(n,DEN),Q(n+1,DEN))
def sqrtiv(x): return I(sqrtq(max(Q(0),x.lo)).lo,sqrtq(max(Q(0),x.hi)).hi)
def exp_scalar(x):
    assert 0<=x<=32
    # Alternating Taylor at x/32 in [0,1]: odd partial sum lower, even upper.
    y=x/32; term=Q(1); total=Q(1)
    for n in range(1,26):
        term*=-y/n; total+=term
        if n==24: upper=total
    z=I(floor(total),ceil(upper))
    for _ in range(5): z=z*z
    return z
def expneg(x):
    x=iv(x); return I(exp_scalar(x.hi).lo,exp_scalar(x.lo).hi)
def out(x):
    x=iv(x); return {"lower":str(x.lo),"upper":str(x.hi),"display_upper":float(x.hi)}

PARAMS=[(Q(350003,3000000),Q(3,5),Q(4,5),Q(1,5)),
        (Q(200739,4000000),Q(1,2),Q(13,20),Q(1,10))]
class Filter:
    def __init__(self,pars):
        self.m,self.k,self.d,self.g=pars
        m,k,d,_=pars; self.a=k/m; self.b=d/m
        delta=d*d-4*m*k; assert delta>0
        root=sqrtq(delta)
        self.alpha=(d-root)/(2*m); self.beta=(d+root)/(2*m)
        assert self.alpha.lo>0
        # Exact sign-bracketing, not floating root selection.
        lo,hi=Q(0),Q(1,2)
        assert self.values(lo)[2].lo>0 and self.values(hi)[2].hi<0
        for _ in range(55):
            mid=(lo+hi)/2; bp=self.values(mid)[2]
            if bp.lo>0: lo=mid
            elif bp.hi<0: hi=mid
            else: raise AssertionError("insufficient precision for peak bracket")
        self.peak=I(lo,hi)
        self.Bmax=self.values(self.peak)[1]
        self.Bpmin=self.values(2*self.peak)[2]
        # Rational Lyapunov matrix for x=(q,p/m), A=[[0,1],[-a,-b]].
        a,b=self.a,self.b
        self.P=[[b/(2*a)+(a+1)/(2*b),1/(2*a)],
                [1/(2*a),(a+1)/(2*a*b)]]
        P=self.P; A=[[Q(0),Q(1)],[-a,-b]]
        for i in range(2):
            for j in range(2):
                z=sum(A[l][i]*P[l][j]+P[i][l]*A[l][j] for l in range(2))
                assert z==(-1 if i==j else 0)
        assert P[0][0]>0 and P[0][0]*P[1][1]-P[0][1]**2>0
    def values(self,t):
        t=iv(t); ea=expneg(self.alpha*t); eb=expneg(self.beta*t)
        gap=self.beta-self.alpha
        B=(ea-eb)/gap
        Bp=(-self.alpha*ea+self.beta*eb)/gap
        A=(self.beta*ea-self.alpha*eb)/gap
        return A,B,Bp
    def kernels(self,t):
        A,B,Bp=self.values(t)
        I0=(1-A)/self.a
        # Cumulative total variations; B' zero at peak and B'' at 2*peak.
        if t<=self.peak.lo: I1=B
        elif t>=self.peak.hi: I1=2*self.Bmax-B
        else: I1=2*self.Bmax
        if t<=2*self.peak.lo: I2=1-Bp
        elif t>=2*self.peak.hi: I2=1+Bp-2*self.Bpmin
        else: I2=1-2*self.Bpmin
        J0=(t-B-self.b*I0)/self.a
        return I0,I1,I2,J0
    def matrix_norm_squared(self,t,wq,wv):
        A,B,Bp=self.values(t)
        # F maps the ACTUAL initial (q0,v0), leaving sigma0 as a separate input.
        X=wq*sq(A)+wv*self.a**2*sq(B)
        Y=wq*A*B-wv*self.a*B*Bp
        Z=wq*sq(B)+wv*sq(Bp)
        return (X+Z+sqrtiv(sq(X-Z)+4*sq(Y)))/2
    def gains(self,t,upper):
        A,B,Bp=self.values(t); I0,I1,I2,J0=self.kernels(upper)
        m=self.m
        # Each tuple multiplies (S0,S,H,|c|). Nonnegative upper coefficients.
        q=[B.absmax()/m,I1.hi/m,I0.hi/m,self.g*J0.hi/m]
        v=[Bp.absmax()/m,(1+I2.hi)/m,I1.hi/m,self.g*I0.hi/m]
        return [[max(Q(0),c) for c in row] for row in (q,v)]

def main():
    output=Path(sys.argv[1]).resolve()
    assert output.parent==HERE/'output' and output.is_dir()
    filters=[Filter(p) for p in PARAMS]
    root3=sqrtq(Q(3)).hi
    # Full 12-dimensional Euclidean ball: the four block entries together
    # have norm <=3/20, not four separately budgeted initial balls.
    radius=Q(3,20)
    cases=[("zero_caps",["0","0"],["0","0"]),
           ("small",["1/100","1/100"],["1/20","1/20"]),
           ("moderate",["3/100","1/50"],["1/10","1/10"]),
           ("larger",["1/20","1/25"],["1/4","1/4"]),
           ("large_sigma",["1/10","1/10"],["1/10","1/10"]),
           ("large_h",["1/100","1/100"],["1","1"])]
    cases=[(name,list(map(Q,s)),list(map(Q,h))) for name,s,h in cases]
    # Exact interval coverage, not trajectory integration or time sampling.
    cells=128
    tube=[]
    for n in range(cells):
        t=I(Q(n,cells),Q(n+1,cells))
        gain=[f.gains(t,t.hi) for f in filters]
        lam=max(f.matrix_norm_squared(t,Q(3,2),Q(4,5)).hi for f in filters)
        tube.append((gain,lam))
    termgain=[f.gains(I(1),Q(1)) for f in filters]
    termlam=max(f.matrix_norm_squared(I(1),Q(3),Q(2)).hi for f in filters)
    def bound(gains,lam,wq,wv,S,H):
        b=[]
        for idx,rows in enumerate(gains):
            u=[S[idx],S[idx],H[idx],root3]  # S0=S; separate gains are exported.
            b.append([sum(c*v for c,v in zip(row,u)) for row in rows])
        inp=sum(wq*q*q+wv*v*v for q,v in b)
        total=sq(radius*sqrtq(lam)+sqrtq(inp))
        return total.hi
    results=[]
    for name,S,H in cases:
        pb=max(bound(ga,la,Q(3,2),Q(4,5),S,H) for ga,la in tube)
        qb=bound(termgain,termlam,Q(3),Q(2),S,H)
        # Cap-only adversary: almost-constant S on (0,1), then switches to -S.
        # sigma(0)=0 and physical initial q=v=0. Continuous transitions approach
        # this value. It is an obstruction for the relaxed filter class only.
        witness=I(0)
        for f,s in zip(filters,S):
            A,B,Bp=f.values(Q(1))
            witness=witness+3*sq(s*B/f.m)+2*sq(s*(2-Bp)/f.m)
        results.append(dict(name=name,S=S,H=H,S0="S (independent conservative initial cap)",
                            P_all_time_upper=pb,Qterminal_upper=qb,
                            certifies_P_lt_45=pb<45,certifies_P_lt_5_6=pb<Q(28,5),
                            certifies_Qterminal_lt_12=qb<12,
                            cap_only_terminal_witness=out(witness),
                            cap_only_terminal_obstruction=witness.lo>12))
    src=HERE.parents[2]/'6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq'
    sources=[src/'dhport_lib.jl',src/'routeB_export_traj.jl',
             HERE.parent/'routeb_inertial_structure/audit_results.json',
             HERE.parent/'routeb_dh_power_binding/ExistingEnergyCore.lean',
             HERE.parent/'routeb_residual_budget_screen/screen.jl']
    payload=dict(status='RATIONAL_INTERVAL_FILTER_AUDIT_PASS',Lean_compiled=False,
        actual_DH_caps_proved=False,total_residualCost_budget_proved=False,
        interval_denominator=DEN,time_cells=cells,initial_full12_radius=radius,
        ramp='w=c*t, c^2<=3, 0<=t<=1',source_sha256={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
        filters=[dict(parameters=p,alpha=out(f.alpha),beta=out(f.beta),peak_time=out(f.peak),
                      Bmax=out(f.Bmax),Bpmin=out(f.Bpmin),lyapunov_P=f.P,
                      terminal_transition=[out(x) for x in f.values(Q(1))],
                      terminal_gains=ga) for f,p,ga in zip(filters,PARAMS,termgain)],
        cases=results,all_time_cells=[dict(gains=g,initial_operator_squared=l) for g,l in tube])
    (output/'results.json').write_text(json.dumps(payload,default=str,indent=2)+'\n',encoding='utf-8')
    for r in results:
        print(r['name'],'P<=',float(r['P_all_time_upper']),'Qterminal<=',float(r['Qterminal_upper']),
              'terminal_cap_only_witness>=',float(Q(r['cap_only_terminal_witness']['lower'])))
    for i,(f,ga) in enumerate(zip(filters,termgain),4):
        print('joint',i,'terminal gains(S0,S,H,|c|):',[[float(x) for x in row] for row in ga])
    print(payload['status'],flush=True)

if __name__=='__main__': main()
