---
kind: review_result
task_id: T-P4-FORCE-SOURCE-CHILD
source_agent: codex-local
created_at: 2026-09-07
integration_status: pending
---

# True-DH force/source bottleneck: independent q4/q5 child and minimal contract repair

## Scope

This review is restricted to the q4/q5 force-coordinate seam between the
canonical deployed DH source and the lifted nominal source. It does not rerun
the old mismatch audit, does not inspect broad P4 coverage, and does not
modify workflow state, registry, or either external source tree.

## New source-level finding

The current force-scale checker tests only for literal source strings
`q5/100` and `q4/200`. That test is too syntactic for the canonical lifted
implementation: the coefficients are constructed compositionally as
`Ival[4] * Q(1,20) * q[5]` and `Ival[5] * Q(1,20) * q[4]`. Therefore the current
status `FORCE_SCALE_TERMS_UNSUPPORTED_IN_CURRENT_CANONICAL_SOURCES` is a
checker false negative for the coordinate-normalization child; it is not
evidence that the force-scale identity itself is unavailable.

This does not establish direct equality with deployed `tau`. It isolates a
smaller source-bound algebraic fact that can be admitted independently.

## Canonical anchors

1. Deployed source: `robot_final/dhport_lib.jl`, SHA-256
   `AEBE6DB09B2D943448C5D701631109DBA8F5EEB070CC66593E5DBACA26485936`.
   The parameter vectors are at lines 12--18; the deployed controller equation
   is at lines 102--109. The source uses

   ```text
   tau = -Kp*q - (Kd+b_fr)*dq + G0v + (gw_coef .* I_val)*w.
   ```

   In particular, `tau` is not the source of the q4/q5 cross coefficient.

2. Lifted source: `routeB_dense_Mq/routeB_fourier_lifted_descriptor_model.jl`,
   SHA-256
   `0FCF733144B3D7B1B08F328FE4AD24477057C56976F0EF53633C450D8FC4729D`.
   The exact rational parameter rows are at lines 150--155; the nominal rows
   and force assembly are at lines 160--166:

   ```text
   f4 = ... + Q(1,20) * q[5]
   f5 = ... + Q(1,20) * q[4]
   l4_expr = Ival[4] * f4 - ...
   l5_expr = Ival[5] * f5 - ...
   ```

   Thus `Ival[4]=1/5`, `Ival[5]=1/10`, and `kc=1/20` are all source-local
   exact rational facts.

3. Target coordinate contract: `docs/routeb-p4-kc-force-contract.md` and the
   `source_binding_receipt` in `artifacts/routeb_6dof/state.json` require the
   force coordinates `(q5/100,q4/200)` while retaining the normalized
   coordinates `(q5/20,q4/20)` as a separate scale.

## Independently closeable child

Proposed child:

```text
P4.force_scale_adapter_q45
```

Define the normalized block coordinate and the force coordinate by

```text
B = (4,5),
q_B = (q4,q5)^T,
J = [[0,1],[1,0]],
D_B = diag(I4,I5) = diag(1/5,1/10),
kc = 1/20.
```

Then the normalized lifted cross term is

```text
rho_kc^f(q_B) = kc J q_B
               = (q5/20, q4/20)^T,
```

and the force-scale adapter is

```text
ForceScale45(f_B) := D_B f_B.
```

The child theorem is the exact identity

```text
D_B rho_kc^f(q_B)
  = kc D_B J q_B
  = (q5/100, q4/200)^T.
```

The proof only consumes the three rational equalities

```text
(1/5)(1/20) = 1/100,
(1/10)(1/20) = 1/200,
J(q4,q5)^T = (q5,q4)^T.
```

It does not consume `M_BD`, `M_DD`, `a_D`, central-FD semantics, Float64
enclosure, domain coverage, or the physical descriptor equality. Consequently
it is the smallest candidate child that can close without changing the
physical model.

## Exact force-row form to which the child binds

Multiplying the two lifted nominal rows by their inertias gives

```text
F_lift,4 = -3/4 q4 - 1/2 dq4 + 1/5 w + q5/100,
F_lift,5 = -29/50 q5 - 13/20 dq5 + 1/10 w + q4/200.
```

The adapter binds only the final cross summand in these rows. The remaining
terms stay in their original source coordinates. In particular, the adapter
must not rewrite `f_B` into deployed `tau_DH,B`, and it must not erase the
nominal-vs-deployed residual.

## Minimal source-contract repair

Replace the current literal-presence test with a two-channel contract:

```text
force_scale_derivation:
  status: PRESENT_COMPOSITIONAL
  normalized_term: kc * J * q_B
  kc: 1/20
  inertia_map: diag(1/5,1/10)
  force_term: (q5/100,q4/200)
  derivation: inertia_map * normalized_term

deployed_tau:
  direct_kc_term: ABSENT
  authority: robot_final/dhport_lib.jl:102-109

binding_boundary:
  force_scale_adapter_closed: pending_typed_child
  lifted_equals_deployed_tau: false
```

The checker should accept either of the following source witnesses, provided
they are tied to the lifted-source hash:

```text
Ival[4] * Q(1,20) * q[5] = Q(1,100) * q[5]
Ival[5] * Q(1,20) * q[4] = Q(1,200) * q[4]
```

It should separately preserve the negative fact that the deployed controller
source has no direct `kc` term. This avoids both failure modes: rejecting a
valid compositional coordinate adapter because its simplified coefficient is
not printed, or silently promoting the adapter to a true-DH controller
equivalence theorem.

## Next theorem after the child

Once `P4.force_scale_adapter_q45` is admitted, the next source-bound theorem
should be the conditional block residual identity

```text
l_B := D_B f_B - D0 a_B,
r_DH,B := (tau_DH - Cdq - Gq)_B,

l_B = (D_B f_B - r_DH,B)
      + (M_BB(q)-D0)a_B
      + M_BD(q)a_D,
```

with the first bracket expanded using the already source-bound
`(q5/100,q4/200)` term. This is the correct handoff to residual absorption;
the q4/q5 adapter itself does not require any new physical-model assumption.

## Status

```text
child = P4.force_scale_adapter_q45
classification = exact_compositional_source_algebra
status = INTERFACE_DRAFT__UNCOMPILED
direct_true_DH_tau_equivalence = NOT_CLAIMED
formal_certificate_allowed = false
registry_promoted = false
```

