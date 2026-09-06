"""Exact Fourier audits of concrete Route-B inertial formulas; no trajectories.

Standard library only. All input reads are external; all writes are beside this
script. The optional symbolic inspection is unnecessary for reproduction.
"""
import ast
import csv
import hashlib
import json
import re
from fractions import Fraction as Q
from pathlib import Path

HERE=Path(__file__).resolve().parent
SRC=HERE.parents[2]/"6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq"
ZERO=(0,)*6


def add(*polys):
    out={}
    for p in polys:
        for nu,(a,b) in p.items():
            x,y=out.get(nu,(Q(0),Q(0)))
            out[nu]=(x+a,y+b)
    return {k:v for k,v in out.items() if v!=(0,0)}


def scale(p,c):
    return {k:(a*c,b*c) for k,(a,b) in p.items() if a*c or b*c}


def mul(p,q):
    return add(*[{tuple(x+y for x,y in zip(nu,eta)):(a*c-b*d,a*d+b*c)}
                 for nu,(a,b) in p.items() for eta,(c,d) in q.items()])


def const(c): return {} if c==0 else {ZERO:(Q(c),Q(0))}
def diff(p,k): return {nu:(-b*nu[k],a*nu[k]) for nu,(a,b) in p.items() if nu[k]}


def trig(nu,sine=False):
    other=tuple(-v for v in nu)
    return {nu:(Q(0),Q(-1,2)),other:(Q(0),Q(1,2))} if sine else {
        nu:(Q(1,2),Q(0)),other:(Q(1,2),Q(0))}


def product(*polys):
    p=const(1)
    for q in polys: p=mul(p,q)
    return p


def rows(name):
    with (SRC/name).open(newline="",encoding="utf-8") as fh: return list(csv.DictReader(fh))


def load_poly(records):
    out={}
    for r in records:
        nu=tuple(int(r[f"nu{i}"]) for i in range(1,7))
        assert nu not in out
        out[nu]=(Q(int(r["real_num"]),int(r["real_den"])),
                 Q(int(r["imag_num"]),int(r["imag_den"])))
    return out


def serial(p):
    return [{"nu":nu,"real":str(a),"imag":str(b)} for nu,(a,b) in sorted(p.items())]


def main():
    records=rows("routeB_fourier_mass_full_rational.csv")
    M=[[load_poly([r for r in records if (int(r['row']),int(r['col']))==(i+1,j+1)])
        for j in range(6)] for i in range(6)]
    assert all(M[i][j]==M[j][i] for i in range(6) for j in range(6))
    assert all(nu[0]==nu[5]==0 for row in M for p in row for nu in p)
    for row in M:
        for p in row:
            assert all(p[tuple(-k for k in nu)]==(a,-b) for nu,(a,b) in p.items())
    ns=(0,1,1,0,0,0); nt=(0,1,0,0,0,0); nz=(0,0,1,0,0,0)
    nx=(0,0,0,1,0,0); ny=(0,0,0,0,1,0)
    cs,ss=trig(ns),trig(ns,True); ct,st=trig(nt),trig(nt,True)
    cz,sz=trig(nz),trig(nz,True); cx,sx=trig(nx),trig(nx,True)
    cy,sy=trig(ny),trig(ny,True)
    A0=Q(7,60); m=Q(40147,800000); J=Q(1,60)
    k=Q(147,800000); b=Q(399,400000); d=Q(441,400000)
    j0=Q(21,80000); e0=Q(21,50000); mu=Q(1,1000000)
    A=add(const(A0),scale(mul(sy,sy),k))
    f=add(const(b),scale(cy,k))
    H=add(scale(st,d),const(e0))
    f43=scale(product(sx,sy,f),-1)
    delta42=scale(product(cz,sx,sy),-d)
    f42=add(f43,delta42)
    h53=mul(cx,add(const(m),scale(cy,b)))
    delta52=scale(add(product(cz,cx,cy),scale(mul(sz,sy),-1)),d)
    h52=add(h53,delta52)
    f41=add(mul(A,cs),mul(sy,add(
        mul(cx,add(H,scale(ss,b),scale(mul(ss,cy),k))),scale(mul(cs,sx),j0))))
    h51=add(product(add(const(m),scale(cy,b)),ss,sx),product(H,sx,cy),
             scale(add(mul(ss,sy),scale(product(cs,cx,cy),-1)),j0))
    N=add(mul(cs,cy),scale(product(ss,cx,sy),-1))
    expected={(3,0):f41,(3,1):f42,(3,2):f43,(3,3):A,(3,4):{},(3,5):scale(cy,J),
              (4,0):h51,(4,1):h52,(4,2):h53,(4,3):{},(4,4):const(m),(4,5):{},
              (5,0):scale(N,J),(5,1):scale(mul(sx,sy),J),(5,2):scale(mul(sx,sy),J),
              (5,3):scale(cy,J),(5,4):{},(5,5):const(J)}
    for ij,p in expected.items():
        assert M[ij[0]][ij[1]]==p, ("mass formula mismatch",ij,serial(add(M[ij[0]][ij[1]],scale(p,-1))))
    # Actual regularized spin quasi-momentum, not an uninstantiated identity.
    regularized_row6=[add(p,const(mu) if j==5 else {}) for j,p in enumerate(M[5])]
    regularized_row4=[add(p,const(mu) if j==3 else {}) for j,p in enumerate(M[3])]
    chi=J/(J+mu)
    pi4=[add(p,scale(mul(cy,r),-chi)) for p,r in zip(regularized_row4,regularized_row6)]
    assert pi4[5]=={}
    assert len(records)==610
    # A source-instantiated joint SOS for the small q2/q3 column defect.
    lhs=add(const(d*d),scale(mul(delta42,delta42),-1),scale(mul(delta52,delta52),-1))
    u=add(mul(sz,cy),product(cz,cx,sy)); v=product(cz,sx,cy)
    rhs=scale(add(mul(u,u),mul(v,v)),d*d)
    assert lhs==rhs
    assert Q(10,13)*d*d*8==Q(194481,26000000000)
    stored=rows("routeB_fourier_coriolis_rational.csv")
    coriolis={}
    for i in (3,4,5):
        for j in range(6):
            for ell in range(6):
                p=scale(add(diff(M[i][j],ell),diff(M[i][ell],j),scale(diff(M[j][ell],i),-1)),Q(1,2))
                old=load_poly([r for r in stored if (int(r['row']),int(r['dq_j']),int(r['dq_k']))==(i+1,j+1,ell+1)])
                assert p==old, ("Christoffel source mismatch",i,j,ell)
                coriolis[i,j,ell]=p
    # C_B's complete dependence on v6; no v6^2 term.
    spin4={0:scale(product(ss,sx,sy),-J),1:scale(mul(cx,sy),-J),
           2:scale(mul(cx,sy),-J),3:{},4:scale(sy,-J)}
    spin5={0:scale(add(mul(cs,sy),product(ss,cx,cy)),J),
           1:scale(mul(sx,cy),-J),2:scale(mul(sx,cy),-J),3:scale(sy,J),4:{}}
    for i,spin in ((3,spin4),(4,spin5)):
        assert coriolis[i,5,5]=={}
        for j in range(5): assert scale(coriolis[i,j,5],2)==spin[j]
    # Explicit coefficient identity C_i = (d/dt M_ij)*v_j - (1/2)*v'M_,i*v.
    # Each unordered velocity monomial is checked, including diagonal factors.
    transport={}
    for i in (3,4):
        for j in range(6):
            for ell in range(j,6):
                source=scale(coriolis[i,j,ell],1 if j==ell else 2)
                conv=diff(M[i][j],j) if j==ell else add(diff(M[i][j],ell),diff(M[i][ell],j))
                Ti=scale(diff(M[j][ell],i),Q(1,2) if j==ell else Q(1))
                assert source==add(conv,scale(Ti,-1))
                transport[i,j,ell]=Ti
    # Concrete compact remote-remote scalar entries needed by T4,T5.
    base33=Q(608093,2400000)
    m33=add(const(base33),scale(cy,2*b),scale(product(sx,sx,sy,sy),-k))
    corr23=add(scale(cz,Q(5187,200000)),scale(add(mul(cz,cy),scale(product(sz,cx,sy),-1)),d))
    assert M[2][2]==m33
    assert M[1][2]==add(m33,corr23)
    assert M[1][1]==add(m33,scale(corr23,2),const(Q(54553,200000)))
    # FD C6 has a common sinc multiplier, unlike general C4,C5.
    assert all(abs(n)<=1 for p in M[5] for nu in p for n in nu)
    assert diff(M[5][5],4)=={}
    builder=SRC/"routeB_fourier_rational_probe.py"
    twists=ast.literal_eval(re.search(r"DH_ALPHA\s*=\s*(\[[^\]]+\])",builder.read_text(encoding="utf-8"))[1])
    adjacent=[{0:1,1:0,-1:0}[n] for n in twists[:5]]
    assert adjacent==[0,1,0,0,0]
    julia=(SRC/"dhport_lib.jl").read_text(encoding="utf-8")
    dhtext=re.search(r"(?m)^DH\s*=\s*\[([^\]]+)\]",julia)[1]
    julia_twists=[row.split()[-1] for row in dhtext.split(";")]
    assert julia_twists==["-pi/2","0.0","pi/2","-pi/2","pi/2","0.0"]
    assert re.search(r"const MASS_REGULARIZER\s*=\s*1e-6",julia)
    paths=[SRC/n for n in ("routeB_fourier_mass_full_rational.csv","routeB_fourier_coriolis_rational.csv",
           "routeB_fourier_rational_probe.py","dhport_lib.jl")]
    result=dict(status="EXACT_MBD_AND_CHRISTOFFEL_IDENTITIES_VERIFIED",
                physical_DH_or_Float64_binding_proved=False,total_point1_budget_proved=False,
                full_mass_rows=len(records),mass_formula_entries_checked=len(expected),
                Christoffel_entries_checked=108,block_quadratic_transport_entries_checked=42,
                constants=dict(A0=A0,m=m,J=J,k=k,b=b,d=d,j=j0,e=e0,mu=mu),
                cyclic_coordinates=[1,6],adjacent_axis_cosines=adjacent,
                source_DH_twist_tokens=julia_twists,
                M46="cos(q5)/60 (not constant)",M56="0",regularized_M66=J+mu,
                cyclic_spin_elimination_factor=J/(J+mu),
                column_2_minus_3_joint_squared_bound=d*d,
                column_defect_weighted_cost_bound_per_a2_squared=Q(10,13)*d*d,
                column_defect_weighted_cost_per_Q_conditional_on_main_dual=Q(10,13)*d*d*8,
                M43_absolute_bound=b+k/2,M42_absolute_bound=b+k/2+d,
                M53_absolute_bound=m+b,M52_absolute_bound=m+b+d,
                mass_formulas={f"M{i+1}{j+1}":serial(p) for (i,j),p in expected.items()},
                pi4_velocity_coefficients={f"v{j+1}":serial(p) for j,p in enumerate(pi4)},
                half_kinetic_block_derivative={f"T{i+1}_v{j+1}v{ell+1}":serial(p)
                                              for (i,j,ell),p in transport.items()},
                sha256={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})
    (HERE/"audit_results.json").write_text(json.dumps(result,default=str,indent=2)+"\n",encoding="utf-8")
    # Small exact Christoffel payload for C4,C5, with original ordered indices.
    with (HERE/"block_coriolis_coefficients.csv").open("w",newline="",encoding="utf-8") as fh:
        writer=csv.writer(fh)
        writer.writerow(["row","v_j","v_k",*[f"nu{k}" for k in range(1,7)],"real_num","real_den","imag_num","imag_den"])
        for (i,j,ell),p in coriolis.items():
            if i==5: continue
            for nu,(a,bv) in sorted(p.items()):
                writer.writerow([i+1,j+1,ell+1,*nu,a.numerator,a.denominator,bv.numerator,bv.denominator])
    print(result["status"])
    print("mass entries:",len(expected),"Christoffel entries:",108,"transport coefficients:",42)
    print("adjacent cosines:",adjacent,"spin ratio:",J/(J+mu),"joint column defect bound:",d*d)


if __name__=="__main__": main()
