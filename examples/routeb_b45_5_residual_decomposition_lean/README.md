# B45-5 exact residual decomposition candidate

This sidecar formalizes the narrow algebraic seam identified by the B45-5
audit.  It keeps the PMI block as a nominal force and treats the actual source
descriptor equation as an explicit hypothesis.

Coordinate note: this sidecar defines `pmiForce` in force coordinates, so its
exact cross term is

```text
rho_kc = (q5/100, q4/200).
```

The current `routeB_pmi_certificate.jl` has normalized `kc=0.05=1/20`; after
multiplication by `I4=1/5` and `I5=1/10`, its force-scale cross term is exactly
`(q5/100,q4/200)`.  This sidecar is therefore a useful conditional algebraic
candidate for the canonical force residual.  It still needs source binding,
global domain coverage, and the remote term `M_BD(q) a_D`; neither force nor
remote terms become acceleration residuals by renaming.

The sidecar now also contains a pure exact-real coordinate adapter theorem
`forceScaleKc_eq_rhoKc`: normalized `(q5/20,q4/20)` is mapped to force
`(q5/100,q4/200)` by `diag(1/5,1/10)`.  This theorem is still separate from
source binding and admission.

The theorem proves only the identity

```text
l_B = rho_C + rho_G + rho_mgl + rho_kc + rho_mass + rho_remote.
```

It does not prove that any residual is small, does not bind Julia/Float64
semantics, and does not close the global PMI/first-exit certificate.
