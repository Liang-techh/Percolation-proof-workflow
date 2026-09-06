# B45-5 exact residual decomposition candidate

This sidecar formalizes the narrow algebraic seam identified by the B45-5
audit.  It keeps the PMI block as a nominal force and treats the actual source
descriptor equation as an explicit hypothesis.

For the block `(4,5)`, the exact PMI cross residual is

```text
rho_kc = (q5/100, q4/200).
```

The theorem proves only the identity

```text
l_B = rho_C + rho_G + rho_mgl + rho_kc + rho_mass + rho_remote.
```

It does not prove that any residual is small, does not bind Julia/Float64
semantics, and does not close the global PMI/first-exit certificate.

