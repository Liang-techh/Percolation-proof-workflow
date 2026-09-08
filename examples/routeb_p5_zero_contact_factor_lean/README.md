# T-P5-056 zero-contact factor Lean sidecar

Agent: 巨阳仙尊

This portable sidecar formalizes the source-independent trusted core proposed by
狂蛮魔尊 in `T-P5-056`: exact repeated-root/factor certificates for degree-2
and degree-3 branch-free remainder polynomials, plus separate one-sided endpoint
factor consumers.

The kernel-facing interface deliberately treats a rational root as an untrusted
*witness*: Lean verifies only division-free coefficient identities and sign
conditions.  No gcd/root-finding/CAS procedure is trusted.  The quadratic branch
proves an exact `a*(t-r)^2` factor; the cubic branch proves
`(t-r)^2*(a*t+b+2*a*r)` and reduces the remaining sign check to the two affine
endpoint values.  Endpoint zeros are kept separate through `t*Q(t)` and
`(1-t)*Q(t)` identities, so a valid simple endpoint root is not incorrectly
forced to have even multiplicity.

Regression theorems freeze the `r=1/3` square that stalls pure dyadic Bernstein
controls, the simple-root polynomial `(t-1/3)(t-2/3)` that is negative at
`1/2`, and the valid simple endpoint root `P(t)=t`.  A final typed seam feeds a
certified quadratic `Rtr` packet and cubic `Rdet` packet into an already-proved
two-remainder consumer.

This sidecar does **not** formalize rational-root discovery, the global
certificate-level completeness theorem from `T-P5-056-C`, deployed source
coefficient binding, Float64/FD/controller semantics, P8 ODE/domain coverage,
P5/M4 closure, or registry admission.  In particular, a non-strict zero-contact
PASS is not a positive-reserve or strict-decay certificate.

Run with:

```bash
CI_PORTABLE=1 bash examples/routeb_p5_zero_contact_factor_lean/verify.sh
```

The verifier uses the repository-pinned `examples/local_fkg` Lake environment
and requires `lake` and `lean` on `PATH`; it contains no machine-specific path.
