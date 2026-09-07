# B45-5 exact residual decomposition candidate

This sidecar formalizes the narrow algebraic seam identified by the B45-5
audit.  It keeps the PMI block as a nominal force and treats the actual source
descriptor equation as an explicit hypothesis.

Historical-snapshot warning: this sidecar defines an older normalized toy
`pmiForce`, so its exact cross term is

```text
rho_kc = (q5/100, q4/200).

It is not the current canonical deployed PMI source.  The current
`routeB_pmi_certificate.jl` has `kc=0.05=1/20` and therefore its force-scale
cross term is `(q5/20,q4/20)`.  The old sidecar is retained for provenance and
history, but must be rejected by the source-contract checker when presented as
the current adapter.  A corrected adapter must also bind the remote term
`M_BD(q) a_D`; neither term is an acceleration residual by renaming.
```

The theorem proves only the identity

```text
l_B = rho_C + rho_G + rho_mgl + rho_kc + rho_mass + rho_remote.
```

It does not prove that any residual is small, does not bind Julia/Float64
semantics, and does not close the global PMI/first-exit certificate.
