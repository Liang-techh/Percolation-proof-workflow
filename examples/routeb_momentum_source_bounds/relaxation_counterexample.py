"""Rational enclosure of a continuous-input relaxed FILTER counterexample.

This is NOT a trajectory of the original six-axis DH system. It tests whether
discarding all correlation and derivative information in sigma is sound enough
to prove the desired outputs. No floating arithmetic enters the enclosure.
"""
from fractions import Fraction as Q
from math import factorial
from pathlib import Path
import hashlib
import json

HERE=Path(__file__).resolve().parent
N=4
GRID=10**40


def eye(): return [[Q(int(i==j)) for j in range(N)] for i in range(N)]
def mul(A,B): return [[sum(A[i][k]*B[k][j] for k in range(N)) for j in range(N)] for i in range(N)]
def add(A,B): return [[A[i][j]+B[i][j] for j in range(N)] for i in range(N)]
def scale(A,c): return [[v*c for v in row] for row in A]
def norm(A): return max(sum(abs(v) for v in row) for row in A)
def action(A,x): return [sum(a*b for a,b in zip(row,x)) for row in A]
def upward(x): return Q(-((-x.numerator*GRID)//x.denominator),GRID)
def round_matrix(A):
    P=[[Q(v.numerator*GRID//v.denominator,GRID) for v in row] for row in A]
    return P,norm(add(A,scale(P,-1)))


def exponential_enclosure(A,t):
    B=scale(A,t)
    squarings=0
    while norm(B)>Q(1,2):
        B=scale(B,Q(1,2));squarings+=1
    degree=24
    term=eye();P=eye()
    for k in range(1,degree+1):
        term=scale(mul(term,B),Q(1,k));P=add(P,term)
    a=norm(B)
    # Sum of omitted matrix powers in induced infinity norm: first omitted
    # term times a geometric tail <=2 since a<=1/2 and factorials increase.
    error=2*a**(degree+1)/factorial(degree+1)
    P,rounding=round_matrix(P)
    error=upward(error+rounding)
    for _ in range(squarings):
        error=2*norm(P)*error+error**2
        P=mul(P,P)
        P,rounding=round_matrix(P)
        error=upward(error+rounding)
    return P,error,dict(degree=degree,scaling_squarings=squarings,scaled_norm=str(a),
                      matrix_error_upper=str(error))


def main():
    m=Q(200739,4000000);k=Q(1,2);d=Q(13,20)
    # Strictly below the source-bound ledger's sigma5 cap; not physical input.
    S=Q(59,500)
    cap=Q(json.loads((HERE/'bounds.json').read_text(encoding='utf-8'))['sigma_caps'][1])
    assert S<cap
    intervals=[(Q(1,100),-100*S),(Q(98,100),Q(0)),(Q(1,100),200*S)]
    y=[Q(0),Q(0),Q(0),Q(1)] # q5,p5,sigma5,constant
    radius=Q(0);receipts=[]
    for duration,slope in intervals:
        A=[[Q(0),1/m,-1/m,Q(0)],[-k,-d/m,d/m,Q(0)],
           [Q(0),Q(0),Q(0),slope],[Q(0)]*4]
        P,err,receipt=exponential_enclosure(A,duration)
        radius=upward(norm(P)*radius+err*(max(map(abs,y))+radius))
        exact_sigma=y[2]+duration*slope
        y=action(P,y)
        y[2]=exact_sigma;y[3]=Q(1)
        receipt.update(duration=str(duration),sigma_slope=str(slope),state_error_radius=str(radius))
        receipts.append(receipt)
    # Sigma is exactly a piecewise-linear prescribed input with endpoint S.
    assert y[2]==S and y[3]==1
    q=y[0];v=(y[1]-S)/m
    vr=radius/m
    assert q-radius>0 and v+vr<0
    qmin=q-radius;vabsmin=-(v+vr)
    terminal_lower=3*qmin*qmin+2*vabsmin*vabsmin
    domain_lower=Q(3,2)*qmin*qmin+Q(4,5)*vabsmin*vabsmin
    assert terminal_lower>12 and domain_lower>Q(28,5)
    # Use concise rational outward endpoint bounds for the readable claim.
    assert Q(0)<q-radius and q+radius<Q(1,10)
    assert Q(-5)<v-vr and v+vr<Q(-4)
    result=dict(status='RATIONAL_TAYLOR_ENCLOSED_RELAXED_FILTER_COUNTEREXAMPLE',
        actual_DH_trajectory=False,Lean_verified=False,
        original_theorem_refuted=False,
        model='qdot=(p-sigma)/m; pdot=-k*q-(d/m)*p+(d/m)*sigma; axis5; w=h=0',
        m=str(m),k=str(k),d=str(d),sigma_cap=str(S),source_conditional_sigma_cap=str(cap),
        initial_q_p_sigma=['0','0','0'],initial_v='0',sigma_continuous=True,
        sigma_description='Linear 0 to -S on [0,.01], constant -S on [.01,.99], linear -S to +S on [.99,1]',
        terminal_q_enclosure=['0','1/10'],terminal_v_enclosure=['-5','-4'],
        terminal_quantity_lower='32',domain_quantity_lower='64/5',
        exact_terminal_lower=str(terminal_lower),exact_domain_lower=str(domain_lower),
        segment_receipts=receipts,
        missing_physical_constraint='sigma must equal the DH inertial coupling along the same full-six-axis trajectory; the artificial ramp need not satisfy that identity or the candidate velocity box',
        tail_argument='For ||B||<=1/2, omitted exponential series <=2||B||^(n+1)/(n+1)!; propagate induced-infinity-norm errors under squaring and matrix-vector multiplication; explicitly charge matrix rounding on 10^-40 rational grid and round scalar error bounds upward',
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (HERE/'relaxation_counterexample.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print('RELAXED_FILTER_ONLY: exact endpoint q in (0,1/10), v in (-5,-4)')
    print('qterminal>32>12; p-domain>64/5>28/5; original DH theorem NOT refuted')


if __name__=='__main__': main()
