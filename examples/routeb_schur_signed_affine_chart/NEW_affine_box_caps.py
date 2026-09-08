"""Fixed rational 3-by-6 affine box caps; no actual source/Lean admission.

Exact signed dual support functions and a separate convex quadratic vertex cap.
Only a supplied constant chart on a supplied box is checked, not source binding.
"""
from __future__ import annotations
import argparse
import itertools
import json
from fractions import Fraction as Q


def need(ok, why):
    if not ok:
        raise ValueError(why)


def vector(x, n):
    need(type(x) is tuple and len(x) == n, "wrong vector shape")
    need(all(type(t) is Q for t in x), "exact Fraction entries required")


def matrix(x, rows, cols):
    need(type(x) is tuple and len(x) == rows, "wrong matrix shape")
    for row in x:
        vector(row, cols)


def dot(x, y):
    return sum((a*b for a, b in zip(x, y)), Q(0))


def mv(A, x):
    return tuple(dot(row, x) for row in A)


def spd3(H):
    matrix(H, 3, 3)
    need(all(H[i][j] == H[j][i] for i in range(3) for j in range(3)), "metric not symmetric")
    a,b,c = H[0]; _,d,e = H[1]; _,_,f = H[2]
    need(a > 0 and a*d-b*b > 0 and a*(d*f-e*e)-b*(b*f-c*e)+c*(b*e-c*d) > 0,
         "metric not positive definite")


def affine_caps(A, b, H, ell, r0, lo, hi):
    matrix(A, 3, 6); spd3(H)
    for v in (b, ell, r0): vector(v, 3)
    for v in (lo, hi): vector(v, 6)
    need(all(l <= h for l,h in zip(lo,hi)), "reversed box endpoints")

    def projection(v):
        Hv = mv(H, v)
        coeff = tuple(sum((A[i][j]*Hv[i] for i in range(3)), Q(0)) for j in range(6))
        offset = dot(Hv, b)
        lower = offset+sum((min(c*l,c*h) for c,l,h in zip(coeff,lo,hi)), Q(0))
        upper = offset+sum((max(c*l,c*h) for c,l,h in zip(coeff,lo,hi)), Q(0))
        return (lower,upper)

    ucap = projection(ell)
    scap = projection(tuple(ell[i]+r0[i] for i in range(3)))
    dmax = None
    for y in itertools.product(*[(lo[i],hi[i]) for i in range(6)]):
        Ay = mv(A,y)
        defect = tuple(Ay[i]+b[i] for i in range(3))
        value = dot(defect,mv(H,defect))
        dmax = value if dmax is None else max(dmax,value)
    return ucap,scap,dmax


def self_test():
    zero = Q(0)
    H = tuple(tuple(Q(i==j) for j in range(3)) for i in range(3))
    A = tuple(tuple(Q(i==j) for j in range(6)) for i in range(3))
    lo = (Q(-1,4),)*3+(zero,)*3; hi = (Q(1,4),)*3+(zero,)*3
    ell=(Q(1),zero,zero); r0=(zero,Q(1),zero); b=(Q(-2),zero,zero)
    u,s,D = affine_caps(A,b,H,ell,r0,lo,hi)
    need(u == (Q(-9,4),Q(-7,4)), "signed u/offset lost")
    need(s == (Q(-5,2),Q(-3,2)), "signed s/offset lost")
    need(D == Q(83,16), "independent quadratic cap incorrect")
    # The two dual directions miss a third direction: both vanish, D does not.
    Aorth = tuple(tuple(Q(i==2 and j==2) for j in range(6)) for i in range(3))
    lorth=(zero,zero,Q(-1),zero,zero,zero); horth=(zero,zero,Q(1),zero,zero,zero)
    u0,s0,D0=affine_caps(Aorth,(zero,)*3,H,ell,r0,lorth,horth)
    need(u0 == (zero,zero) and s0 == (zero,zero) and D0 == 1, "dual-only obstruction lost")
    wrong_offset=affine_caps(A,(zero,)*3,H,ell,r0,lo,hi)
    need(wrong_offset[0] != u and wrong_offset[2] != D, "offset is material")
    for test in [lambda: affine_caps(A,(2.0,zero,zero),H,ell,r0,lo,hi),
                 lambda: affine_caps(A,b,H,ell,r0,hi,lo),
                 lambda: affine_caps(A,b,((Q(-1),zero,zero),H[1],H[2]),ell,r0,lo,hi)]:
        try: test()
        except ValueError: pass
        else: raise RuntimeError("invalid input accepted")
    return {"result":"pass", "u_interval":list(map(str,u)),"s_interval":list(map(str,s)),
            "D_cap":str(D),"vertices_per_box":64,"dual_zero_D_positive":True,
            "source_bound":False,"runtime_verified":False,"lean_executed":False,
            "registry_eligible":False,"scope":"fixed_synthetic_rational_affine_box"}


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test",action="store_true",required=True)
    parser.parse_args()
    print(json.dumps(self_test(),indent=2))
