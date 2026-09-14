---
kind: review_result
review_id: review-T-P5-100-base-storage-collar-math-honglianmozun-20260908T2102Z
task_id: T-P5-100-BASE-STORAGE-COLLAR-MATH
source_agent: 红莲魔尊
created_at: 2026-09-08T21:02:00Z
claim_commit: e9a858d734fd05171858942f38bd2263219e788f
inspected_commit: 668fff02f7306867160cd9b893646c5ad6c2de3b
status: CONDITIONAL_PASS
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize the ledger-to-collar and lifted-base-storage identities, then bind a real base-storage/source-tube packet without reusing variational semantics by name
commands: none_math_derivation_only
lean_compile_status: not_run
source_binding_proven: false
registry_eligible: false
formal_certificate_allowed: false
---

# T-P5-100 — base-storage collar mathematics and the legal defect bridge

## 0. Result

T-P5-096 already proves that a two-level **base-state** storage collar closes the whole flowed path-sheet premise once one has, on the outer collar,

`nu * Udot <= -nu^2 * U + E`,

`nu > 0`, `E <= nu^2 * R_in`, and `R_in < R_out`.

The missing mathematical interface is how an existing energy/residual ledger may legally produce that inequality without silently reusing the variational storage `xi^T W xi` as a base-state storage.

This review gives three exact pieces:

1. a **ledger-to-collar compiler** for ordinary Lyapunov/mechanical energy inequalities;
2. the only clean way to reuse a moving-metric variational packet as a base-state storage: introduce an explicit state-to-tangent lift and pay its exact lift defect;
3. an **affine storage-normalization covariance law** showing exactly how additive anchor/shift conventions modify the collar additive term. Keeping `E` unchanged after shifting the storage is mathematically wrong.

All instance gates can be checked with addition, multiplication, squaring and order. No inverse, eigenvalue, square root or exponential is required in the trusted certificate.

This is source-independent exact-real mathematics. It does not claim deployed DH/Float64/FD/controller/solve semantics, a P8 flowpipe, source-tube coverage, Lean compilation, or admission.

---

## 1. Typed semantic separation

Use two distinct object types conceptually:

`BaseStorage U : (t,x) -> R`

and

`VariationalStorage V : (t,x,xi) -> R`.

A collar packet is valid only for the first type. It must identify the actual base flow `x' = f(t,x)` and the derivative

`L_f U = partial_t U + D_x U[f]`.

The variational energy

`V(t,x,xi) = xi^T W(t,x) xi`

is not, by itself, a base-state domain function. Setting `xi=0` gives `V=0` at every base point, including points outside any intended source tube. Therefore the following is forbidden without a separate theorem:

`variational_barrier <= R  ==>  base_state_in_source_tube`.

A legal bridge must provide an explicit lift `zeta(t,x)` and define a genuine base storage by

**(1.1)** `U_zeta(t,x) := zeta(t,x)^T W(t,x) zeta(t,x)`.

It must then also prove how `zeta` evolves along the actual base flow. Section 4 gives the exact defect created by that lift.

---

## 2. Main ledger-to-collar compiler

Assume on the outer source-valid collar `U <= R_out` an actual base-state energy ledger of the form

**(2.1)** `Udot <= -c U - D + P`,

where `D >= 0` is a dissipation channel. Suppose the complete perturbation/uncertainty power has already been assembled with signs preserved and satisfies

**(2.2)** `P <= alpha U + theta D + beta`.

Assume

**(2.3)** `c > alpha`,

**(2.4)** `theta <= 1`.

Define

`nu := c-alpha > 0`.

Then direct substitution gives

`Udot`
` <= -(c-alpha)U -(1-theta)D + beta`
` <= -nu U + beta`.

Multiplying by the positive `nu` gives

**(2.5)** `nu Udot <= -nu^2 U + nu beta`.

Thus T-P5-096 Route B may consume

**(2.6)** `E_collar := nu beta`.

The collar gate becomes

**(2.7)** `beta <= nu R_in`,

because multiplying (2.7) by `nu>0` yields

`nu beta <= nu^2 R_in`.

Therefore the complete division-free instance gate is simply

**(2.8)**

`c > alpha`,

`theta <= 1`,

`R_in < R_out`,

`beta <= (c-alpha) R_in`.

No quotient `beta/(c-alpha)` needs to be constructed.

### Candidate theorem statement

`base_storage_collar_of_energy_ledger`

Inputs:

- `Udot <= -c*U - D + P`,
- `0 <= D`,
- `P <= alpha*U + theta*D + beta`,
- `alpha < c`, `theta <= 1`,
- `beta <= (c-alpha)*Rin`,
- `Rin < Rout`.

Output on the outer collar:

`(c-alpha)*Udot <= -(c-alpha)^2*U + (c-alpha)*beta`,

with the T-P5-096 inner-level gate already discharged.

This is the minimal mathematical compiler from an ordinary energy ledger to the collar theorem.

---

## 3. Finite-channel composition and how existing residual leaves fit

Suppose instead there are finitely many signed perturbation channels `P_j` with

`P_j <= alpha_j U + theta_j D + beta_j`.

Let

`alpha = sum alpha_j`,

`theta = sum theta_j`,

`beta = sum beta_j`.

Then summation gives (2.2) exactly, so the only global gates are

**(3.1)** `sum alpha_j < c`,

**(3.2)** `sum theta_j <= 1`,

**(3.3)** `sum beta_j <= (c-sum alpha_j) R_in`.

This prevents a common bookkeeping error: one does not need to allocate an independent full unit of dissipation to every defect channel. Only the **sum** of dissipation fractions must stay below one.

This interface also cleanly consumes earlier energy-side residual leaves:

- a signed force/residual absorption result of the form `P_j <= lambda_j D + kappa_j` enters with `alpha_j=0`, `theta_j=lambda_j`, `beta_j=kappa_j`;
- a relative base-state perturbation `P_j <= a_j U` enters with `alpha_j=a_j`, `theta_j=0`, `beta_j=0`;
- an exact nonlinear cancellation, such as a same-source mechanical skew/Christoffel identity, enters as `P_j=0` and should be cancelled **before** any norm enclosure.

The typed order is therefore:

`signed energy identity -> exact cancellations -> relative/dissipative/additive channel bounds -> aggregate alpha/theta/beta -> collar gate`.

Taking absolute values before the signed energy object is formed can only lose information and may create a false collar failure.

---

## 4. Legal variational-to-base bridge: an explicit lift and its exact defect

There is one reusable route from T-P5-090/091/093-type moving-metric contraction into a genuine base storage, but it requires an explicit lift.

Let the actual base dynamics be

**(4.1)** `xdot = -F(t,x) + b(t,x)`.

Write

`A = D_x F`,

`B = D_x b`.

Let `W(t,x)` be symmetric, and let `zeta(t,x)` be a chosen state-dependent tangent vector. Define the base storage

**(4.2)** `U := zeta^T W zeta`.

Along the actual base flow define the **lift defect**

**(4.3)**

`e_lift := d/dt zeta(t,x(t)) - (-A+B) zeta`

`       = partial_t zeta + D_x zeta[-F+b] + A zeta - B zeta`.

Define the nominal contraction tensor

**(4.4)**

`C0 := A^T W + W A - (W_t - D_x W[F])`,

and the base-flow Lie defect tensor

**(4.5)**

`S_b := D_x W[b] + B^T W + W B`.

A direct differentiation, with no inequality, gives the exact identity

**(4.6) LIFTED BASE-STORAGE IDENTITY**

`Udot = - zeta^T C0 zeta + zeta^T S_b zeta + 2 zeta^T W e_lift`.

### Derivation

Because

`zeta_dot = (-A+B)zeta + e_lift`

and

`W_dot = W_t - D_xW[F] + D_xW[b]`,

we have

`Udot`
`= 2 zeta^T W zeta_dot + zeta^T W_dot zeta`
`= -zeta^T(A^T W+WA)zeta`
`  +zeta^T(B^T W+WB)zeta`
`  +2 zeta^T W e_lift`
`  +zeta^T(W_t-DW[F]+DW[b])zeta`,

which is exactly (4.6).

This identity is the required semantic bridge. It shows precisely where the T-P5-093 Lie-defect term and the T-P5-091 variational-defect term belong when the quadratic form is repurposed as a **base-state** storage through a lift.

Crucially, `B zeta` is already part of the actual tangent generator and `B^T W+WB` is already inside `S_b`. It must not be charged again inside `e_lift`.

---

## 5. Lifted robust collar theorem

Assume on the same outer collar:

**(5.1)** nominal contraction

`zeta^T C0 zeta >= 2 mu U`;

**(5.2)** signed base-flow Lie defect

`zeta^T S_b zeta <= 2 rho_b U`;

split the lift defect as

`e_lift = r + d`,

with

**(5.3)** signed/relative lift defect power

`zeta^T W r <= rho_r U`;

**(5.4)** additive lift-defect metric budget

`d^T W d <= Ebar`.

Define

**(5.5)** `nu := mu-rho_b-rho_r` and assume `nu>0`.

From (4.6),

`Udot <= -2 nu U + 2 zeta^T W d`.

PSD of `W` gives the exact completion

`(nu zeta-d)^T W (nu zeta-d) >= 0`,

hence

`2 nu zeta^T W d <= nu^2 U + d^T W d <= nu^2 U + Ebar`.

Multiplying the differential inequality by `nu` therefore yields

**(5.6)**

`nu Udot <= -nu^2 U + Ebar`.

This is exactly the scalar hypothesis required by T-P5-096 Route B. Therefore, if

**(5.7)** `Ebar <= nu^2 R_in`,

and `R_in<R_out`, with the outer sublevel contained in the certified source/contraction tube, the inner base-storage level is forward invariant and may be used for whole path-sheet coverage.

### Why this is stronger than saying “use the variational energy as U”

The theorem identifies two extra source obligations that the variational theorem does not provide automatically:

1. the lift `zeta(t,x)` must be a real state-dependent object whose outer sublevel controls base-state location;
2. its exact evolution defect `e_lift` must be certified.

Without these, T-P5-091/093 remain tangent-space statements and cannot close P5-096 Route B.

---

## 6. Exact nonlinear obstruction to the zero-defect shortcut

The lift defect is not a formality. Even the obvious choice `zeta=x` has a nonzero defect for a nonlinear vector field.

Take the scalar system

`xdot = -F(x)`,

`F(x)=x+x^3`,

with `W=1` and `b=0`.

Choose `zeta(x)=x`, so the candidate base storage is `U=x^2`.

Then

`A=F'(x)=1+3x^2`.

The actual lift derivative is

`zeta_dot = xdot = -x-x^3`,

whereas the variational generator would give

`-A zeta = -x-3x^3`.

Therefore

**(6.1)** `e_lift = 2x^3`.

The actual storage derivative is

`Udot = -2x^2-2x^4`.

If one illegally set `e_lift=0`, the variational formula would predict

`Udot = -2(1+3x^2)x^2 = -2x^2-6x^4`,

which differs by exactly

`2 zeta e_lift = 4x^4`.

Thus a base displacement cannot be treated as a variational vector merely because both live in the same coordinate space. The missing nonlinear secant/Taylor remainder is exactly a lift defect and must be paid or handled by a path-energy theorem such as T-P5-094.

This gives a precise fail-closed rule:

**No state-to-tangent lift theorem + no lift-defect bound => no legal variational-to-base collar reuse.**

---

## 7. Affine storage normalization covariance

This is directly relevant whenever multiple candidate storages differ by scale or additive anchor conventions.

Assume a base storage `U` already satisfies

**(7.1)** `nu Udot <= -nu^2 U + E`.

Let

**(7.2)** `U_tilde := a U + k`, with constant `a>0` and constant shift `k`.

Then `U_tilde_dot=a Udot`, so multiplying (7.1) by `a` gives

`nu U_tilde_dot`
` <= -a nu^2 U + a E`
` = -nu^2 U_tilde + (aE + nu^2 k)`.

Therefore the transformed additive term is exactly

**(7.3)** `E_tilde = a E + nu^2 k`.

The corresponding levels must transform as

**(7.4)**

`R_in_tilde = a R_in + k`,

`R_out_tilde = a R_out + k`.

Then the collar gate is exactly covariant:

`E_tilde <= nu^2 R_in_tilde`

iff

`aE + nu^2 k <= a nu^2 R_in + nu^2 k`

iff, because `a>0`,

**(7.5)** `E <= nu^2 R_in`.

Likewise

`R_out_tilde-R_in_tilde = a(R_out-R_in)>0`.

So an affine storage re-normalization is mathematically harmless **only when storage, levels and additive collar term are transported together**.

### Exact obstruction if the additive term is not shifted

Take the ideal homogeneous inequality

`nu Udot <= -nu^2 U`

and set `U_tilde=U+k` with `k>0`.

If one keeps `E=0` unchanged, at any point with `U=0` and `Udot=0` the claimed shifted inequality would require

`0 <= -nu^2 k`,

which is false.

The correct transformed inequality contains `E_tilde=nu^2 k`.

Therefore a constant energy shift cannot be ignored merely because derivatives of `U` and `U+k` are equal. This is the collar-level version of the active-V normalization obstruction: derivative identities do not determine value-level barrier semantics.

A typed implementation should consequently distinguish

- `defect_norm_budget`, which may be an actual norm square, from
- `collar_additive_budget`, which after a storage shift also contains the deterministic normalization term `nu^2 k`.

They are not interchangeable semantic fields even if they enter the same scalar inequality.

---

## 8. Mechanical/Lyapunov specialization

For a deployed mechanical storage, a common ledger has the form

`Udot <= -cU - D + P_rel + P_force + beta0`.

Suppose

`P_rel <= alpha U`,

and a force-residual absorption theorem gives

`P_force <= lambda D + kappa`.

Then Section 2 applies with

`theta=lambda`,

`beta=beta0+kappa`,

and the collar is certified by

**(8.1)**

`alpha < c`,

`lambda <= 1`,

`beta0+kappa <= (c-alpha) R_in`.

This is exactly where signed residual boxes, dual quadratic forms, Schur allocations or mechanical cancellation leaves should feed the base-storage collar. No variational interpretation is needed.

If the same-source mechanical Christoffel identity cancels a geometric term exactly, that term contributes zero to `P_force`; separately charging both the metric material derivative and the Christoffel mismatch would double count the same geometry.

---

## 9. Failure boundaries / exact obstructions

The new bridge must fail closed in the following cases.

1. **Variational/base semantic mismatch.** `xi^T W xi` alone gives no base-state tube. A lift `zeta(t,x)` plus source-tube sublevel inclusion is required.
2. **Unpaid lift defect.** Even `zeta=x` has `e_lift!=0` for generic nonlinear dynamics; Section 6 is an exact counterexample.
3. **No positive remaining decay.** If aggregate `alpha>=c`, the ledger alone yields no positive `nu`; a collar might still be provable from other structure, but not from this compiler.
4. **Too much dissipation allocation.** If aggregate `theta>1`, one cannot discard the `D` channel. Closure would require a separate lower bound relating `D` to `U` or a redesigned allocation.
5. **Additive budget exceeds the level reserve.** If `beta>(c-alpha)R_in`, the present data do not prove invariance. This is a certificate failure, not automatically a dynamical counterexample.
6. **Outer-level inclusion missing.** Even a perfect scalar inequality does not prove the source evaluator, derivative bounds or contraction tensor are valid there; `U<=R_out -> sourceTube` is an independent premise.
7. **Storage normalization changed without budget/level transport.** Keeping the same `E` after `U -> aU+k` is unsound; the exact transformed term is `aE+nu^2k`.
8. **Time-dependent shift.** If `k=k(t)`, an additional `nu*k'(t)` contribution appears after multiplying the derivative inequality. The constant-shift theorem above must not be reused unchanged.

---

## 10. Candidate formal theorem leaves

Minimal theorem decomposition suggested for a later Lean lane:

1. `base_storage_collar_of_energy_ledger`
   - pure ordered-ring algebra from (2.1)-(2.8).
2. `base_storage_collar_of_finite_channels`
   - finite-sum aggregation of `alpha/theta/beta` channels.
3. `lifted_base_storage_exact_identity`
   - exact ring/finite-dimensional bilinear identity (4.6), with all derivative/source hypotheses explicit.
4. `lifted_base_storage_robust_collar`
   - consumes nominal contraction, signed Lie defect, relative lift defect and additive metric budget to produce (5.6)-(5.7).
5. `affine_storage_normalization_covariant`
   - exact identities (7.3)-(7.5).
6. `nonlinear_identity_lift_defect_regression`
   - scalar `F=x+x^3`, `zeta=x`, proving `e_lift=2x^3` and the resulting `4x^4` derivative mismatch.

These leaves should remain source-independent until a real packet identifies:

`U_base`, `actualFlow`, `sourceTube`, `R_in`, `R_out`, the signed energy ledger, and—if the variational lift route is used—`W,F,b,zeta,e_lift` on the **same** outer collar.

---

## 11. Integration recommendation

T-P5-096 should not ask downstream source owners to directly provide the already-compressed symbol `E` if their natural data are an energy ledger. The cleaner typed handoff is:

`BaseEnergyLedger(c,D,P)`

`+ DefectAllocation(alpha,theta,beta)`

`+ StorageConvention(scale,shift,levels)`

`+ OuterSublevelSourceInclusion`

which this child compiles into the T-P5-096 scalar collar packet.

If a moving-metric variational theorem is reused, insert the explicit `StateTangentLift(zeta,e_lift)` layer first. This prevents the two exact errors isolated above: treating nonlinear base displacement as a zero-defect variational vector, and treating additive storage normalization as invisible because the derivative is unchanged.

Status remains `pending`: the mathematics is complete at the exact-real interface level, but no actual Route-B base storage/source-tube packet has been bound in this review.
