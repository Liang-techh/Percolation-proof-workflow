---
kind: review_result
review_id: review-GH-MATH-P4-VFULL-DH-ANCHOR-LOCAL-20260908T164337Z
task_id: GH-MATH-P4-VFULL-DH-ANCHOR
source_agent: codex-vfull-anchor-source-lane
created_at: 2026-09-08T16:43:37Z
integration_status: pending
admission_label: pending
status: SYMBOLIC_VALUE_ANCHOR_IDENTIFIED_INITIAL_BOUND_UNBOUND
source_binding_proven: false
initial_bound_binding_proven: false
registry_eligible: false
formal_certificate_allowed: false
generated_numeric_values: false
lean_compile_status: not_run
julia_execution: false
full_regression: false
state_mutation: false
registry_mutation: false
predecessor_review: agent_review_inbox/review-GH-MATH-P4-ACTIVE-INITIAL-BOUND-BINDING-LOCAL-20260908T163551Z.md
predecessor_sha256: a142755e5e7b57eee6eb7d5e599f886077fcb7fd76ae53e13312a6874506608c
requested_action: preserve the raw Vfull value anchor and prove its same-source initial envelope; do not substitute a centered bound
---

# Vfull_DH anchor only: a symbolic source identity, not an admitted initial bound

Only this new review is written. This task fixes Vfull_DH throughout; it does
not repeat candidate selection. No new numeric values, shifts or upper bounds
are evaluated. No producer, Julia, Lean, solver or regression is run.

External E:
`C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq`.

## 1. Explicit value anchor from the inspected assignment

The full-energy source assigns

```text
Vfull_DH(q,v)=Kfull_DH(q,v)+Ugrav_DH(q)
             +(1/2)*sum_i Kp_DH[i]*q_i^2+g0 dot q.
```

Use A0, A and B as abbreviations for the EXISTING source symbols
A0_grav_DH, Agrav_DH, Bgrav_DH, without evaluating their values. On the
physical trigonometric lift at q=0, the source potential formula gives

```text
Ugrav_DH(0)=A0+A+B
Vfull_DH(0,0)=Ugrav_DH(0).
```

This is a direct symbolic substitution into the value expression, not an
inference from its derivative. The kinetic and controller terms vanish at
the origin even before proving g0=0. No source assignment subtracts this
potential anchor from Vfull_DH. These equations are paper source-expression
identities; no kernel or runtime refinement has been verified in this turn.

## 2. Exact restriction to the existing block-only X0

The preceding initial-bound task fixed X0 with only q4,q5,v4,v5 free,
the other coordinates zero. Retain the SAME q/v ordering and physical c/s
lift. Substituting q2=q3=0 in the inspected potential polynomial yields

```text
Ugrav_DH(q)=A0+A+B*cos(q5)
Ugrav_DH(q)-Ugrav_DH(0)=B*(cos(q5)-1).
```

No q4 term survives this restriction; this is not a claim about the full
potential away from X0. Thus the exact candidate-level initial expression is

```text
Vfull_DH(q,v)=Ugrav_DH(0)
 + (1/2)*v_B^T M_BB(q)*v_B
 + B*(cos(q5)-1)
 + (1/2)*(Kp_DH[4]*q4^2+Kp_DH[5]*q5^2)
 + g0[4]*q4+g0[5]*q5,              B-index order=(4,5).
```

Here the symbol B multiplying cosine is the gravity coefficient, whereas
subscript B denotes the joint block; they are distinct. This restricted
identity is the useful value-level anchor for an initial proof. It is not
itself a uniform bound over the block ball and does not certify the existing
initial_storage_upper scalar.

The inspected coefficient B is positive. Accordingly its cosine difference
is nonpositive on real inputs. One may use this fact in a later upper-envelope
proof without computing a new constant, but the raw Ugrav_DH(0) term remains.

## 3. Linear compensation is a separate source premise

The imported Fourier model defines g0 by evaluating analytic gravity at the
origin. The full-energy assignment uses +g0 dot q. Its origin VALUE vanishes
regardless of g0, but its initial-domain contribution does not vanish from
that fact alone: the restricted term is g0[4]*q4+g0[5]*q5.

The existing shift CSV reports g0_exact_zero=true and formal_certificate_allowed=false.
This is a recorded result, not a freshly proved source identity here. To drop
the linear term on X0, the minimal needed exact evidence is g0[4]=g0[5]=0
for the same analytic gravity object (a full-vector zero theorem also works).
Otherwise retain it and supply an actual envelope; no such envelope is invented.

The inspected trigonometric potential itself has zero first derivative at
the origin. Transferring this to g0 requires its gradient/source-gravity
binding; neither the name g0 nor a Hessian upper bound supplies that equality.
Loaded FD-origin gravity is a further distinct object and cannot be replaced
by the analytic zero without refinement. The sign of the linear compensation
must follow the selected source assignment, not be silently changed for an
energy derivative cancellation.

## 4. Regularizer: no origin contribution, nonzero initial kinetic role

The imported mass source loads the analytic mass polynomial and adds its
declared diagonal regularizer once. Kfull_DH uses that resulting M.
At v=0 the entire kinetic value vanishes, so the regularizer changes neither
the displayed origin anchor nor its value proof. On X0, however, it contributes
its kinetic quadratic in v4,v5. A mass upper bound from an unregularized or
differently regularized matrix cannot be copied into this initial proof.

The exact restriction uses M_BB, not a Schur complement: remote velocities
are zero on X0, not minimized/eliminated. The needed upper envelope must bound
that SAME principal block over the allowed initial configurations.

## 5. Minimal missing function-level binding

The existing scalar producer has a quadratic-only formula derived from mass,
Hessian and cross-term envelopes. For THIS raw Vfull_DH its use requires:

1. source-to-expression binding of the initial state/lift and this value
   formula, including the regularized mass and potential anchor;
2. the analytic g0 component identities or retained linear envelope;
3. a valid bound for the restricted mass and other retained terms on X0;
4. an upper-bound statement that includes Ugrav_DH(0), then matches the
   consumer's recorded scalar and threshold, or an explicitly proved
   comparison to an already bound initial storage.

A Hessian bound controls an anchored Taylor remainder, not this raw value.
An origin identity fixes the additive term but does not bound all X0.
Neither fact alone constructs InitialBoundBinding X0 Vfull_DH upper.
No matching full witness was located in the inspected examples interface.

Conclusion: the symbolic value anchor and the exact block-only expression
are explicit; the source-bound initial envelope and scalar/threshold match
remain missing. Keep pending, without selecting another storage or generating
a compensating constant.

## Current byte bindings

Hashes freshly recomputed, filenames relative to E:

| Source/artifact | SHA256 |
|---|---|
| routeB_compact_dh_full_energy_supply_split_audit.jl | d6d9bd3131d73fddf946f8652458b04c628f76471d497b2a52a49f0335b30632 |
| routeB_compact_dh_gain_descriptor_regeneration_audit.jl | 04b764434601dd0c11b2a6554156fd4d948cf742dbf33472b960e0d54e8235c9 |
| routeB_fourier_lifted_descriptor_model.jl | 0fcf733144b3d7b1b08f328fe4ad24477057c56976f0ef53633c450d8fc4729d |
| routeB_compact_dh_storage_shift_audit.csv | 9a357d70638cc37496400da23adc7df8e25d2c012cd5c6d6dd576fb83ee0be3b |

No historical execution, dependency soundness, compiled proof or source
admission is inferred from hashes or existing flags. State/registry untouched.
