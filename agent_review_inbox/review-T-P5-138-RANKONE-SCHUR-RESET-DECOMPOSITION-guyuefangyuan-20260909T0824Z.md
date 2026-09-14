---
kind: review_result
review_id: review-T-P5-138-rankone-schur-reset-decomposition-guyuefangyuan-20260909T0824Z
task_id: T-P5-138-RANKONE-SCHUR-RESET-DECOMPOSITION
reviewer: 古月方源
source_agent: 古月方源
created_at: 2026-09-09T08:24:00Z
claim_commit: a07844ba307fc38b731796fea11da59f6e42c329
inspected_commit: f4212a7463a782d219e0ee2dbcbba06f4c04b8b5
upstream_reviews:
  - path: agent_review_inbox/review-T-P5-137-ELLIPSOIDAL-KNOT-RESET-MULTIPLIER-honglianmozun-20260909T0811Z.md
    commit: f4212a7463a782d219e0ee2dbcbba06f4c04b8b5
  - path: agent_review_inbox/review-T-P5-136-TANGENT-TO-PHYSICAL-COERCIVITY-BRIDGE-liuguanyi-20260909T0801Z.md
    commit: 865615dd454c608b79a4fc3eb2f6fcef32c508bf
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: for_fixed_multiplier_expose_shifted_curvature_and_rank_one_domination_keep_augmented_LMI_for_joint_search_and_reject_singular_boundary_when_reset_covector_sees_nullspace
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: none; exact quadratic-form / rank-one PSD algebra only
exit_code: n/a
---

# T-P5-138 — rank-one Schur decomposition of the ellipsoidal knot-reset multiplier

## 0. Narrow seam and non-overlap

T-P5-137 gives the exact sufficient reset certificate

`M(tau,E) = [[H + tau G, -b/2],[-b^T/2, E-C-tau R]] >= 0`

for the physical ellipsoid `x^T G x <= R` and the signed reset envelope

`W_+ - kappa W_- <= b^T x - x^T H x + C`.

That is already the correct one-constraint S-procedure geometry. This child does **not** redo that theorem, does not scalarize back to `(A,B,R)`, and does not search an actual source packet. It isolates one remaining algebraic seam:

> for a fixed multiplier `tau`, what exactly does the augmented `(n+1)x(n+1)` PSD condition say in the original `n`-dimensional physical space?

The answer is an exact rank-one domination theorem. It is useful for three reasons:

1. it gives an inverse-free / square-root-free same-dimensional checker interface;
2. it exposes the precise nullspace obstruction when the shifted curvature is singular;
3. it shows when a source-provided dual quadratic bound can be consumed without constructing an augmented matrix factorization.

No actual source binding, same-cell coverage, controller/Float64 semantics, P8 flowpipe, Lean/kernel receipt, independent verification, admission, or registry promotion is claimed.

---

## 1. Abstract block and shifted curvature

Let `K` be a symmetric quadratic-form matrix, `b` a column covector/vector, and `e` a scalar. Define

`B(K,b,e) := [[K, -b/2],[-b^T/2, e]]`.

For `x` in the physical state space and scalar `t`, its quadratic form is

**(1.1)**

`Q_B(x,t) = x^T K x - t b^T x + e t^2`.

Define the rank-one residual matrix

**(1.2)**

`S(K,b,e) := 4 e K - b b^T`.

The whole result is about the exact relation between `B >= 0` and `S >= 0`.

---

## 2. Main theorem: block PSD iff curvature PSD plus rank-one domination

### Theorem A — rank-one Schur decomposition

For symmetric `K`,

**(2.1)**

`B(K,b,e) >= 0`

if and only if all three conditions hold:

**(2.2)** `K >= 0`,

**(2.3)** `e >= 0`,

**(2.4)** `4 e K - b b^T >= 0`.

Equivalently, (2.4) says pointwise

**(2.5)**

`(b^T x)^2 <= 4 e (x^T K x)`

for every `x`.

This is the singular-safe Schur complement. No inverse of `K` is required.

### 2.1 Forward direction

Assume `B>=0`.

The principal `K` block is PSD, hence `K>=0`. The bottom-right principal scalar is nonnegative, hence `e>=0`.

Now fix any `x`. Apply the Cauchy inequality for the PSD bilinear form induced by `B` to the two augmented vectors

`u=(x,0)`, `v=(0,1)`.

Then

`<u,v>_B = -b^T x/2`,

`<u,u>_B = x^T K x`,

`<v,v>_B = e`.

Therefore

`(b^T x)^2/4 <= e (x^T K x)`,

which is exactly (2.5). Hence `4eK-bb^T>=0`.

This forward implication can also be proved by restricting `B` to the two-dimensional span of `(x,0)` and `(0,1)` and using nonnegativity of the resulting `2x2` Gram determinant.

### 2.2 Reverse direction without inverse or square root

Assume (2.2)-(2.5). Fix arbitrary `x,t`, and write

`q := x^T K x >= 0`,

`p := b^T x`,

`c := e t^2 >= 0`,

`s := t p`.

From (2.5),

`s^2 = t^2 p^2 <= 4 q e t^2 = 4 q c`.

We need to show

`q - s + c >= 0`.

If `s<=0`, this is immediate from `q,c>=0`.

If `s>0`, observe the exact identity

**(2.6)**

`(q+c)^2 - s^2 = (q-c)^2 + (4qc-s^2) >= 0`.

Both `q+c` and `s` are nonnegative, hence `(q+c)^2>=s^2` implies `q+c>=s`. Thus

`q-s+c>=0`.

Since `x,t` were arbitrary, `B>=0`.

The reverse proof is therefore entirely polynomial/order algebra: addition, multiplication, squaring, and case split on the sign of one scalar. No inverse, square root, eigenvalue, or generalized inverse appears.

---

## 3. Direct specialization to T-P5-137

For the T-P5-137 reset packet, fix `tau` and set

**(3.1)**

`K_tau := H + tau G`,

**(3.2)**

`e_tau,E := E - C - tau R`.

Then the T-P5-137 augmented matrix is exactly

`B(K_tau,b,e_tau,E)`.

Hence its PSD gate is equivalent to the same-dimensional conditions

**(3.3)** `K_tau >= 0`,

**(3.4)** `e_tau,E >= 0`,

**(3.5)** `4 e_tau,E K_tau - b b^T >= 0`.

### Theorem B — ellipsoid reset from rank-one domination

Assume:

- `tau>=0`;
- `x^T G x<=R`;
- `W_+-kappa W_- <= b^T x-x^T H x+C`;
- (3.3)-(3.5).

Then

**(3.6)** `W_+ <= kappa W_- + E`.

### Direct proof

From Theorem A with `t=1`,

`x^T K_tau x - b^T x + e_tau,E >= 0`.

Expand:

`x^T H x - b^T x + E-C`

` = [x^T K_tau x - b^T x + e_tau,E]`

`   - tau (x^T G x-R)`.

The first bracket is nonnegative. Since `tau>=0` and `x^T G x-R<=0`, the second contribution `-tau(x^T Gx-R)` is also nonnegative. Thus

`x^T H x - b^T x + E-C >=0`,

or

`b^T x-x^T Hx+C <= E`.

Insert the reset envelope to obtain (3.6).

This is exactly the T-P5-137 consumer with the augmented PSD condition decomposed.

---

## 4. Source-facing dual-cap corollary

A source producer may already know a quadratic dual bound in the shifted metric rather than a block factorization.

Suppose a scalar `Bdual>=0` satisfies

**(4.1)**

`Bdual K_tau - b b^T >= 0`,

or equivalently

`(b^T x)^2 <= Bdual (x^T K_tau x)`

for every `x`.

If also

**(4.2)** `Bdual <= 4 e_tau,E`,

then

`4 e_tau,E K_tau - b b^T`

` = (4e_tau,E-Bdual)K_tau + (Bdual K_tau-bb^T) >=0`.

Therefore Theorem B applies.

### Corollary C — dual cap to reset

For fixed `tau`, a checker may consume the four exact gates

`tau>=0`,

`K_tau>=0`,

`e_tau,E>=0`,

`Bdual<=4e_tau,E`,

plus the source-side PSD witness `Bdual K_tau-bb^T>=0`.

This is useful when the producer naturally emits a dual-norm matrix certificate. It avoids computing `K_tau^-1` and avoids adding an augmented dimension.

The constant `4` is sharp. In one dimension with `K=1`, `b=2`, `e=1`,

`4eK-b^2 = 4-4 =0`,

so equality is attained.

---

## 5. Exact nullspace obstruction

The rank-one form makes the singular case completely transparent.

### Theorem D — nullspace obstruction

Assume `K>=0`. If there exists a nonzero direction `v` such that

**(5.1)** `K v = 0`,

but

**(5.2)** `b^T v != 0`,

then for every finite real `e`,

**(5.3)** `4eK-bb^T` is not PSD.

Indeed,

`v^T(4eK-bb^T)v`

` = 4e v^T K v - (b^T v)^2`

` = -(b^T v)^2 <0`.

Consequently `B(K,b,e)` cannot be PSD for any finite `e`.

In finite-dimensional real inner-product space with symmetric `K`, this is exactly the range compatibility condition

**(5.4)** `b in range(K)`

because `range(K)=ker(K)^perp`.

The important practical point is that **positive definiteness of `K` is not necessary**. What is necessary at a singular direction is that `b` annihilate that direction.

### Singular but feasible exact example

Take

`K = diag(0,1)`,

`b=(0,2)`,

`e=1`.

Then

`4eK-bb^T = 0` identically.

Hence the augmented block is PSD even though `K` is singular. The zero-curvature direction is harmless because the reset covector has no component there.

This example is important for theorem design: replacing `K>=0` by `K>0` would be sound but unnecessarily strong and would reject exact boundary certificates that are genuinely valid.

---

## 6. Singular multiplier boundary can be structurally impossible

T-P5-137 notes that boundary multipliers can be delicate. The rank-one decomposition distinguishes two different issues:

1. **arithmetic/rational boundary difficulty**: a real feasible multiplier may not have a convenient rational representation;
2. **geometric singular-boundary obstruction**: even an exact real boundary multiplier is impossible if `b` sees the nullspace of `K_tau`.

The second is intrinsic and cannot be repaired by increasing the reset floor `E` while holding that singular `tau` fixed.

### Exact one-dimensional saturation

Take

`G=1`, `H=-1`, `b=1`, `R=1`, `C=0`.

The physical reset envelope is

`phi(x)=x+x^2`

on `|x|<=1`; its true maximum is `2`, attained at `x=1`.

For the multiplier certificate,

`K_tau = tau-1`,

`e_tau,E = E-tau`.

At the minimal curvature shift `tau=1`,

`K_tau=0`

but `b=1` does not annihilate its nullspace. Theorem D therefore says:

**no finite `E` can certify the reset at `tau=1`.**

For `tau>1`, Theorem A reduces to

`E-tau>=0`,

`4(E-tau)(tau-1)>=1`.

Put `s=tau-1>0`. Then

`E >= 1+s+1/(4s)`.

The exact square identity

`(2s-1)^2 >=0`

implies

`s+1/(4s)>=1`.

Hence every certificate has

`E>=2`.

Equality is attained at

`tau=3/2`, `e=1/2`, `E=2`,

where

`4 e K_tau = 4*(1/2)*(1/2)=1=b^2`.

Thus the exact physical optimum is recovered, but the optimal multiplier must move strictly inside the curvature-PSD region. The singular boundary `tau=1` is genuinely infeasible for every finite floor.

This is a useful counterexample-guided rule for future searches: if a candidate multiplier is sitting on a singular `K_tau` and the source covector has nonzero projection on its nullspace, do not spend time increasing `E`; move `tau`, change the reset geometry, or exploit an additional signed cancellation.

---

## 7. Monotonicity for fixed multiplier

For a fixed `tau`, `K_tau` is fixed and increasing `E` increases only

`e_tau,E = E-C-tau R`.

If `E_0` is feasible and `E>=E_0`, then

`4 e_tau,E K_tau-bb^T`

` = [4 e_tau,E0 K_tau-bb^T]`

`   + 4(E-E_0)K_tau >=0`,

and `e_tau,E>=e_tau,E0>=0`.

Therefore feasibility is monotone in `E` at fixed `tau`.

This supports a fail-closed rational checker: once a rational floor is certified for a fixed rational `tau`, any larger rational floor is automatically certified without a new matrix search.

---

## 8. Important search warning: do not destroy the affine LMI structure

The rank-one decomposition is exact for **verification** at fixed `(tau,E)`, but it should not automatically replace the T-P5-137 augmented LMI during joint parameter search.

The augmented matrix

`[[H+tau G,-b/2],[-b^T/2,E-C-tau R]]`

is affine in the decision variables `(tau,E)`.

By contrast,

`4(E-C-tau R)(H+tau G)-bb^T`

contains products such as `E*tau` and `tau^2` when both parameters are varied. So the decomposed gate can turn a convex affine-LMI search into a nonlinear polynomial search even though the feasible set is mathematically identical.

Recommended division of labor:

- **search/design layer:** keep the T-P5-137 augmented LMI;
- **exact checker / source consumer:** after `tau,E` are frozen, optionally use `K>=0`, `e>=0`, `4eK-bb^T>=0` or the dual-cap corollary;
- **obstruction analysis:** use the nullspace theorem immediately at singular `K`.

This avoids trading away the strongest computational structure while still exposing the exact mathematics to the trusted checker.

---

## 9. Minimal Lean theorem decomposition

The first Lean leaves should avoid matrix inverses and, if desired, even avoid block-matrix APIs.

### 9.1 `quadratic_block_nonneg_of_rankone_domination`

Scalar/quadratic-form statement:

Assume for all `x`

`0 <= q x`,

and scalars `e>=0`,

`(p x)^2 <= 4*e*q x`.

Then for all `x,t`,

**(9.1)**

`0 <= q x - t*p x + e*t^2`.

Proof: the case split and square identity (2.6). This is the smallest source-independent leaf and should be mostly `nlinarith` plus a sign split.

### 9.2 `rankone_domination_impossible_on_null`

Assume

`q v=0`, `p v !=0`.

Then no finite `e` can satisfy

`(p v)^2 <= 4*e*q v`.

This is a one-line exact obstruction and does not need matrix APIs.

### 9.3 `dual_cap_promotes_rankone_domination`

Assume

`p^2 <= B*q`,

`0<=q`,

`B<=4e`.

Then

`p^2<=4e*q`.

Again pure scalar order algebra.

### 9.4 `ellipsoid_reset_of_rankone_domination`

Assume the T-P5-137 reset envelope, cell inequality, `tau>=0`, shifted-curvature nonnegativity and pointwise rank-one domination. Conclude

`W_+<=kappa W_-+E`.

This theorem can be formalized before a full finite-matrix PSD equivalence.

### 9.5 Optional matrix theorem `block_psd_iff_rankone_psd`

After the scalar leaves are stable, add the finite-dimensional matrix equivalence

`[[K,-b/2],[-b^T/2,e]] >=0`

iff

`K>=0 ∧ e>=0 ∧ 4eK-bb^T>=0`.

The forward direction can use the PSD Cauchy/Gram determinant API; the reverse direction can reuse 9.1.

### 9.6 Regression theorem `singular_boundary_floor_two`

For the exact one-dimensional fixture in section 6, prove:

- `tau=1` cannot satisfy the rank-one gate for any finite `E`;
- every `tau>1` certificate has `E>=2`;
- `tau=3/2,E=2` satisfies the gate.

This is a useful exact regression for both nullspace handling and branch-safe arithmetic.

---

## 10. Source-facing packet recommendation

If an actual knot producer can preserve the full signed geometry from T-P5-137, the smallest fixed-parameter checker packet is now:

- same physical/reference key;
- `G,H,b,C,R`;
- frozen rational `tau,E`;
- `K=H+tau G` identity;
- `e=E-C-tau R` identity;
- exact PSD witness for `K`;
- exact PSD witness for `4eK-bb^T` (or a dual-cap witness `Bdual K-bb^T>=0` plus `Bdual<=4e`);
- same-cell coverage and complete reset-term accounting.

If `K` is singular, the producer should additionally expose a nullspace/range witness or let the rank-one PSD test fail directly. It must not silently replace singular `K` by a nearby positive-definite matrix unless the corresponding perturbation is charged in the reset envelope.

If joint `(tau,E)` optimization is still needed, preserve the original augmented affine LMI for the search and only emit the decomposed packet after parameters are frozen.

---

## 11. Failure boundaries and nonclaims

### 11.1 Rank-one PSD does not create source geometry

The theorem only consumes `K,b,e`. It does not prove that a deployed reset event has the T-P5-137 signed envelope or that `G,H,b,C,R` belong to one source/configuration.

### 11.2 `K>=0` alone is insufficient

A large scalar reset floor cannot repair a covector component along `ker K`. Theorem D is an exact obstruction.

### 11.3 `K>0` is unnecessarily strong

The singular aligned example shows valid certificates can live on a PSD boundary. The correct condition is rank-one domination, not blanket positive definiteness.

### 11.4 Dual projections are not automatically a dual-matrix certificate

A few measured projections of `b` do not establish `Bdual K-bb^T>=0` in the full physical space. The source packet must certify the complete covector/metric relation on the declared domain.

### 11.5 Search and checker roles differ

The decomposed rank-one gate is exact but nonlinear in `(tau,E)` if both vary. Do not replace the affine augmented LMI in an optimizer unless that tradeoff is deliberate.

### 11.6 No parent closure

This child does not establish actual source binding, chart/physical identity, runtime/Float64 semantics, P8 coverage, dwell/headroom values, Lean compilation, independent verification, admission, registry eligibility, or M4/P5 parent closure.

---

## 12. Result

`T-P5-138-RANKONE-SCHUR-RESET-DECOMPOSITION` is a **CONDITIONAL_PASS_MATHEMATICAL_CHILD**.

New mathematical content relative to T-P5-137:

1. exact singular-safe equivalence
   `[[K,-b/2],[-b^T/2,e]]>=0`
   iff
   `K>=0`, `e>=0`, `4eK-bb^T>=0`;
2. direct source dual-cap consumer `Bdual K-bb^T>=0`, `Bdual<=4e`;
3. exact nullspace obstruction `Kv=0`, `b^Tv!=0` => no finite reset floor at that fixed multiplier;
4. exact singular-feasible counterexample showing `K>0` would be too strong;
5. exact one-dimensional reset fixture where the singular boundary multiplier is impossible for every `E`, while the interior multiplier `tau=3/2` recovers the sharp physical floor `E=2`;
6. a search/checker separation rule: preserve the augmented affine LMI for joint design, use the rank-one decomposition after parameter freezing or for obstruction analysis.

The next useful source step is not another generic Schur proof. It is to preserve an actual same-key signed knot packet `(G,H,b,C,R)` and either emit a frozen `(tau,E)` with exact `K`/rank-one PSD witnesses or keep the augmented LMI candidate until source and cell coverage are bound.