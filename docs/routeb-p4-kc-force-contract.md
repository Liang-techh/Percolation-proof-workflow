# Route-B P4 canonical `kc` force contract

This is a narrow mathematical/source seam, not a certificate closure.

## Correct current-scale identity

The canonical PMI source contains

```text
kc = 0.05 = 1/20
f1 = ... + kc*q5 + ...
f2 = ... + kc*q4 + ...
```

Therefore, in the generalized-force coordinates used by the PMI source, the
cross contribution is

```text
rho_kc(q_B) = (q5/20, q4/20).
```

The older `routeb_b45_5_residual_decomposition_lean` sidecar uses the
different normalized toy definition `(q5/100,q4/200)`.  Its algebra remains a
historical candidate for the definitions written in that file, but it is not a
binding theorem for the current canonical source.  The source-contract checker
rejects that adapter instead of silently changing its coefficients.

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
