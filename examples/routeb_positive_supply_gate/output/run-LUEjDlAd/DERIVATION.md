# Bounded derivation: positive supply and the terminal `a1` gate

## Scope and status

This is a source-unbound analytical sidecar for the concrete storage

```
W0dot = -v'(K+H0)q - v'Dv + v'G w + (14/75) q4 v4 + v'eta.
```

It uses the fixed-`Z=I` finite quadratic gate already derived in the local
work. No LP, trajectory, scan, broad regression, state edit, or registry edit
is part of this leaf. No feasibility statement and no `J <= 1` statement is
made.

## 1. Fixed-`Z=I` source cost, with eta counted once

Let

```
dM = M0 - M(q)
r0 = dM*a0 + H0*q - grad U(q) - C(q,v)
r  = r0 + eta
R  = M0^-1
h  = R*r
z  = (R*L - I)*h
e  = dM*(2*h+z) = dM*(I+R*L)*h.
```

Under the source mass order `M(q) >= L > 0`, the lower block for `Z=I` is
`2M-L >= L`. The finite completion therefore gives the scalar sufficient
condition

```
delta'Ldelta <= CR(r0,eta),

CR(r0,eta) = h'Lh + 2*(R*L*h)'*dM*h + e'Qe.
```

The definition must be evaluated with `r=r0+eta` before taking any interval
or absolute-value bound. In particular, the cross terms between `r0` and
`eta` are part of the same quadratic cost; eta is not an additional copy of
the residual. The derivative also contains the single explicit work term
`f*v'eta`.

## 2. Concrete storage derivative

Use `tau=1-t` and finite positive powers

```
f(t)   = sum_j a_j*tau^j
p_i(t) = sum_j p_ij*tau^j
h_c(t) = sum_j c_j*tau^j.
```

For
`V=f*W0 + sum_i p_i*q_i^2 + h_c*c^2`, with `c'=0`, the source-derived
product rule is

```
Vdot = f'*W0
     + f*(-v'(K+H0)q - v'Dv + v'G*w + (14/75)q4*v4 + v'eta)
     + sum_i (p_i'*q_i^2 + 2*p_i*q_i*v_i)
     + h_c'*c^2.
```

Consequently, a finite exact positive-supply gate is the following hypothesis
on every state/source point in the proved prefix cell:

```
CR(r0,eta) + Vdot <= b(t).
```

Choose a rational polynomial supply
`b(t)=sum_{k=0}^m beta_k*(1-t)^k` with `beta_k>=0`. Its exact coefficient
budget is

```
V0_upper + sum_{k=0}^m beta_k/(k+1) < 1.                 (B)
```

Equation (B) is the requested finite budget condition. It is a prospective
arithmetic condition, not an integrated dynamical conclusion. To use it in a
full proof one would still need the fundamental-theorem-of-calculus bridge,
`V>=0`/terminal endpoint bounds, and a continuation/first-exit argument.

## 3. First-order terminal calculation

Take the source-cell slice

```
q=0, c=0, w=0, v=rho*u, u=e4+e5.
```

For the known source witness, `M=M0`, and the Christoffel residual is

```
C = (21/25000)*rho^2*e1.
```

With `eta=0`, define the exact residual cost

```
E(rho) = ((21/25000)^2 * rho^4) * (e1' R L R e1),
```

and

```
A(rho) = W0 = (rho^2/2)*(u'M0u),
D(rho) = rho^2*(u'Du), so W0dot = -D(rho).
```

For the first-order mode `f=a1*tau`, all position and ramp-square terms
vanish on this slice, and the exact gate expression is

```
E(rho) - a1*A(rho) - a1*tau*D(rho)
= E(rho) - a1*(A(rho)+tau*D(rho)).                 (T)
```

Thus, if a nonnegative supply polynomial has value `b(t)` at this point, the
finite exact terminal hypothesis is

```
E(rho) - a1*(A(rho)+tau*D(rho)) <= b(t).             (T_b)
```

Whenever the denominator is positive and `b(t)<E(rho)`, (T_b) implies

```
a1 >= (E(rho)-b(t))/(A(rho)+tau*D(rho)).             (A1)
```

At `tau=0`, (A1) reduces to `a1 >= (E(rho)-beta_0)/A(rho)`. In particular,
zero supply (`beta_0=0`) requires `a1 >= E(rho)/A(rho)>0`. The term `a1` is
therefore not optional if the terminal source neighborhood has a positive
residual floor and the supply is zero there.

If eta is not zero, retain it exactly by replacing (T) with

```
CR(r0,eta) - a1*A(rho)
 + a1*tau*(-D(rho) + rho*u'eta) <= b(t),             (T_eta)
```

or equivalently use denominator
`A(rho)+tau*(D(rho)-rho*u'eta)`, provided that denominator is certified
positive. This is the explicit eta hypothesis needed by a Lean verification;
an absolute eta bound alone is not silently substituted for it.

## 4. Exact known-candidate audit

At `rho=1/20`, `tau=1/100`, the known candidate has `a1=0` and
`f=a8*tau^8`, where
`a8=6995146470641/1000000000000`. The exact source witness gives

```
E = 7954729780571525062950308308715457359162746863876688481 /
    2139693685849290060237084157997244412955032963896020129690764194800
W0 = 2002229/9600000000
W0dot = -29/8000.
```

The audit computes `E + f'*W0 + f*W0dot > 0` exactly. Hence the fixed scalar
gate with `b=0` fails for that candidate at this static source point. The
point is used only as a known candidate obstruction; it is not asserted to be
terminally reachable. The audit also computes the positive endpoint floor
`E/W0`; it does not search for a coefficient or claim that any positive
supply budget is uniformly certifiable.

## 5. Remaining hypotheses / blocker

The derivation is not a completed theorem because the following premises are
still external or unproved in this leaf:

1. uniform exact source binding for `M,U,C`, their derivatives, and the
   implementation/FD/rounding/solve defects;
2. a proved source-cell enclosure for `CR(r0,eta)`, including all eta cross
   terms and the explicit `v'eta` work term;
3. `M(q)>=L>0` and the domain/first-exit continuation argument;
4. the initial `V0_upper`, positivity of `V` on the covered prefix, and the
   terminal endpoint comparison;
5. regularity and FTC hypotheses needed to turn (B) and the pointwise gate
   into an actual accumulated correction bound.

`PositiveSupplyGate.lean` records only the generic finite algebraic inequality
behind (A1) and the coefficient-budget arithmetic. It is prospective source
code; no registry admission or theorem-level feasibility claim follows.
