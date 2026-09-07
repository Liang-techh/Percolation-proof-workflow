# Route-B P4 canonical `kc` force contract

This is a narrow mathematical/source seam, not a certificate closure.

## Correct two-scale identity

The canonical PMI source contains

```text
kc = 0.05 = 1/20
f1 = ... + kc*q5 + ...
f2 = ... + kc*q4 + ...
```

Therefore the cross contribution in the normalized `f` coordinates is

```text
rho_kc^f(q_B) = (q5/20, q4/20).
```

The canonical PMI code then multiplies `f1` by `I4=1/5` and `f2` by
`I5=1/10` when forming the block force.  Thus the same cross term in force
coordinates is

```text
rho_kc^F(q_B) = diag(1/5,1/10) rho_kc^f(q_B)
              = (q5/100, q4/200).
```

The existing `routeb_b45_5_residual_decomposition_lean` sidecar uses this
force-scale form.  It is a useful algebraic candidate for the canonical force
residual, while its source binding and global domain proof remain open.  The
source-contract checker labels both coordinate systems explicitly and rejects
only an unrecognised scale.

## Deployed DH semantics

The deployed port constructs

```text
tau = -Kp*q - (Kd+b_fr)*dq + G0v + (gw_coef .* I_val)*w
M(q)*a = tau - Cdq - Gq
```

There is no `kc` torque term in that source.  Consequently the PMI `kc` term
must be charged as an additive force residual when comparing the two models;
it cannot be deleted as noise.

The block decomposition also requires the separate remote action
`M_BD(q)*a_D`.  A force residual and an acceleration residual have different
units and may only be converted after an explicitly bound positive mass
operator and its inverse are supplied.

## Gate status

The focused command is:

```text
python scripts/audit_routeb_p4_source_contract.py
```

It can pass the source-text contract while still leaving P4 open.  It does not
prove source equivalence, interval coverage, residual absorption, flowpipe
containment, or Lean kernel validity; those remain separate frontier nodes.
