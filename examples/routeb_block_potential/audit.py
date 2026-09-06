"""Exact 17-row Fourier factorization and block derivatives. No sampling."""
import csv
import hashlib
import json
import re
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parents[2]/"6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq"
ZERO = (0,)*6
C = Q(20601,400000)


def add(*polys):
    out = {}
    for p in polys:
        for nu,(a,b) in p.items():
            x,y = out.get(nu,(Q(0),Q(0)))
            out[nu] = (x+a,y+b)
    return {k:v for k,v in out.items() if v != (0,0)}


def scale(p,c):
    return {k:(a*c,b*c) for k,(a,b) in p.items() if a*c or b*c}


def mul(p,q):
    terms=[]
    for nu,(a,b) in p.items():
        for eta,(c,d) in q.items():
            terms.append({tuple(x+y for x,y in zip(nu,eta)):(a*c-b*d,a*d+b*c)})
    return add(*terms)


def trig(nu, sine=False):
    minus=tuple(-x for x in nu)
    return {nu:(Q(0),Q(-1,2)),minus:(Q(0),Q(1,2))} if sine else {
        nu:(Q(1,2),Q(0)),minus:(Q(1,2),Q(0))}


def diff(p,k):
    return {nu:(-b*nu[k],a*nu[k]) for nu,(a,b) in p.items() if nu[k]}


def block_zero(p):
    return add(*[{tuple(0 if k in (3,4) else n for k,n in enumerate(nu)):(a,b)}
                  for nu,(a,b) in p.items()])


def serial(p):
    return [{"frequency":k,"real":str(a),"imag":str(b)} for k,(a,b) in sorted(p.items())]


def main():
    path=SRC/"routeB_fourier_potential_rational.csv"
    with path.open(newline="",encoding="utf-8") as f:
        records=list(csv.DictReader(f))
    p={}
    for r in records:
        nu=tuple(int(r[f"nu{i}"]) for i in range(1,7))
        assert nu not in p
        p[nu]=(Q(int(r["real_num"]),int(r["real_den"])),
               Q(int(r["imag_num"]),int(r["imag_den"])))
    assert len(records)==len(p)==17 and all(b==0 for a,b in p.values())
    imported_source = HERE.parent/"routeb_potential_slice/output/run-SuGxG04V/PotentialSlice.lean"
    lean_text = imported_source.read_text(encoding="utf-8")
    encoded = re.findall(r"⟨!\[([^\]]+)\],\s*(-?\d+),\s*(\d+),\s*(-?\d+),\s*(\d+)⟩",lean_text)
    encoded_rows = [tuple(int(x.strip()) for x in f.split(","))+tuple(map(int,rest))
                    for f,*rest in encoded]
    fields = [f"nu{i}" for i in range(1,7)]+["real_num","real_den","imag_num","imag_den"]
    assert encoded_rows == [tuple(int(r[k]) for k in fields) for r in records]
    controller_path=SRC/"dhport_lib.jl"
    controller=controller_path.read_text(encoding="utf-8")
    kp=[Q(x.strip()) for x in re.search(r"\bKp\s*=\s*\[([^\]]+)\]",controller)[1].split(",")]
    lean_kp=[Q(x.strip()) for x in re.search(r"def Kp : Fin 6 → ℚ := !\[([^\]]+)\]",lean_text)[1].split(",")]
    assert kp == lean_kp and kp[3:5] == [Q(3,5),Q(1,2)]
    n2=(0,1,0,0,0,0); ns=(0,1,1,0,0,0)
    nx=(0,0,0,1,0,0); ny=(0,0,0,0,1,0)
    cs,ss=trig(ns),trig(ns,True)
    cx,sx=trig(nx),trig(nx,True)
    cy,sy=trig(ny),trig(ny,True)
    block=scale(add(mul(cs,cy),scale(mul(mul(ss,cx),sy),-1)),C)
    candidate=add({ZERO:(Q(10791,4000),Q(0))},
                  scale(trig(n2),Q(762237,200000)),
                  scale(cs,Q(242307,200000)),block)
    assert candidate==p
    dx=scale(mul(mul(ss,sx),sy),C)
    dy=scale(add(scale(mul(cs,sy),-1),scale(mul(mul(ss,cx),cy),-1)),C)
    xx=scale(mul(mul(ss,cx),sy),C)
    xy=scale(mul(mul(ss,sx),cy),C)
    yy=scale(add(scale(mul(cs,cy),-1),mul(mul(ss,cx),sy)),C)
    assert diff(p,3)==dx and diff(p,4)==dy
    assert diff(dx,3)==xx and diff(dx,4)==xy and diff(dy,3)==xy and diff(dy,4)==yy
    assert block_zero(dx)=={} and block_zero(dy)==scale(ss,-C)
    assert block_zero(xx)=={} and block_zero(xy)=={} and block_zero(yy)==scale(cs,-C)
    # Algebraic identities used by the analytic operator-norm derivation.
    # 4/3-(4*r-3*r^2)=3*(r-2/3)^2, coefficient order 0,1,2.
    assert (Q(4,3),Q(-4),Q(3)) == (3*Q(2,3)**2,-6*Q(2,3),Q(3))
    assert Q(7,6)**2 >= Q(4,3)
    L=Q(7,6)*C
    mu=Q(1,2)-L
    assert mu>0
    t=Q(1,100)
    negative=t*t/4-C*t/2  # sin(t)>=t/2 for 0<=t<=1.
    assert 0<t<2*C and negative<0
    result=dict(status="EXACT_FACTOR_AND_BLOCK_DERIVATIVES_MATCH_17_ROWS",
                q_domain="all real q; s=q2+q3, x=q4, y=q5",
                constant=Q(10791,4000),cos_q2=Q(762237,200000),
                cos_s=Q(242307,200000),c=C,
                factor="U=C0+A*cos(q2)+B*cos(s)+c*(cos(s)*cos(y)-sin(s)*cos(x)*sin(y))",
                block_origin_gradient=["0","-c*sin(s)"],
                block_origin_hessian=[["0","0"],["0","-c*cos(s)"]],
                derivative_coefficients=dict(dx=serial(dx),dy=serial(dy),
                                             xx=serial(xx),xy=serial(xy),yy=serial(yy)),
                each_block_hessian_entry_bound=C,
                block_hessian_operator_bound=L,
                sharper_operator_bound="2*c/sqrt(3) (sharp); rational relaxation 7*c/6",
                block_storage_strong_convexity=mu,
                tangent_subtracted_quadratic_coefficient=mu/2,
                centered_storage_uniform_quadratic_lower_bound=False,
                obstruction=dict(q2="pi/2",q3=0,q4=0,q5=t,
                                 centered_storage_upper=negative),
                scalar_alternatives=dict(nonnegative_constant_shift=C*C/(2*mu),
                                         retained_mu_over_four_shift=C*C/mu),
                physical_DH_identification_proved=False,
                imported_17_rows_and_Kp_match=True,
                controller_sha256=hashlib.sha256(controller_path.read_bytes()).hexdigest(),
                imported_lean_sha256=hashlib.sha256(imported_source.read_bytes()).hexdigest(),
                source_sha256=hashlib.sha256(path.read_bytes()).hexdigest())
    (HERE/"audit_results.json").write_text(json.dumps(result,default=str,indent=2)+"\n",encoding="utf-8")
    print(result["status"])
    print("c =",C,"L =",L,"mu =",mu,"mu/2 =",mu/2)
    print("negative witness upper =",negative)
    print("nonnegative shift =",C*C/(2*mu),"quadratic shift =",C*C/mu)
    print("CSV SHA256 =",result["source_sha256"])


if __name__=="__main__":
    main()
