# Route-B positive-supply gate (bounded analytical leaf)

This leaf records a finite analytical condition for the concrete `W0` storage
derivative with the fixed matrix choice `Z=I`. It is intentionally bounded:
there is no LP call, trajectory computation, broad regression, registry/state
write, or claim of feasibility or `J <= 1`.

## Exact gate

Put `dM=M0-M(q)`, `r0=dM*a0+H0*q-grad U(q)-C(q,v)`, `r=r0+eta`,
`R=M0^-1`, `h=R*r`, and `e=dM*(I+R*L)*h`. The fixed-`Z=I` scalar source
cost is

```
CR(r0,eta) = h'Lh + 2*(R*L*h)'*dM*h + e'Qe.
```

The exact pointwise positive-supply hypothesis is, on every already-proved
source cell and prefix time `0 <= t <= 1`,

```
CR(r0,eta) + f'*W0
  + f*(-v'(K+H0)q - v'Dv + v'G*w + (14/75)q4*v4 + v'eta)
  + sum_i (p_i'*q_i^2 + 2*p_i*q_i*v_i) + h_c'*c^2
<= b(t).
```

Here `b(t)` is a nonnegative certified supply. A finite exact budget form is
to choose rational `beta_k >= 0` and set
`b(t)=sum_k beta_k*(1-t)^k`; then require

```
V0_upper + sum_k beta_k/(k+1) < 1.
```

This is only the analytical budget gate. It still needs the source-cell,
eta, endpoint, positivity, continuation, and regularity hypotheses listed in
`DERIVATION.md` before it could participate in a theorem about the physical
problem.

## Terminal first-order issue

For `tau=1-t`, `f=a1*tau`, `q=0`, `c=w=0`, `v=rho*(e4+e5)`, and `eta=0`,
the source audit gives a residual cost `E(rho)>0`,
`W0=A(rho)>0`, and `W0dot=-D(rho)`. Thus

```
CR + Vdot = E(rho) - a1*(A(rho) + tau*D(rho)).
```

At the terminal endpoint, zero supply therefore requires the finite exact
condition `a1 >= E(rho)/A(rho)`. With a supply value `b(1)=beta_0`, the
condition becomes `a1 >= (E(rho)-beta_0)/A(rho)` whenever
`beta_0 < E(rho)`. If eta is retained, replace the denominator by
`A(rho)+tau*(D(rho)-rho*(e4+e5)'eta)` and retain `CR(r0,eta)` assembled as
above.

The known candidate has `a1=0`; the exact Fraction audit in `audit.py`
reproduces its positive terminal-neighborhood total. This rejects that
zero-supply candidate only, not the `W0` family or the original target.

The generic coefficient lower-bound lemma is present in
`PositiveSupplyGate.lean` as a prospective Lean source. It was not promoted
to any registry.
