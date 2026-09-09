---
kind: review_result
review_id: review-T-P5-144-semidefinite-cell-nullspace-elimination-honglianmozun-20260909T1003Z
task_id: T-P5-144-SEMIDEFINITE-CELL-NULLSPACE-ELIMINATION
reviewer: 红莲魔尊
source_agent: 红莲魔尊
created_at: 2026-09-09T10:03:00Z
claim_commit: 7ba10a40e6bb0ef51905f6ba456e398e3a7b7922
inspected_commit: 205cfc931a924fd6da8ae53f7f1e687337eec4c4
upstream_reviews:
  - path: agent_review_inbox/review-T-P5-137-ELLIPSOIDAL-KNOT-RESET-MULTIPLIER-honglianmozun-20260909T0811Z.md
    commit: f4212a7463a782d219e0ee2dbcbba06f4c04b8b5
  - path: agent_review_inbox/review-T-P5-139-RANGE-SOLVE-SCHUR-RESET-kuangmanmozun-20260909T0834Z.md
    commit: f0198916eb5fe1783cbeb9055031c9d9bd0dc954
  - path: agent_review_inbox/review-T-P5-140-MULTIPLIER-SECANT-OPTIMIZATION-honglianmozun-20260909T0908Z.md
    commit: 6d4275c964d8f3481f87e8546d7bec8b020651c0
  - path: agent_review_inbox/review-T-P5-143-ROOT-FREE-SINGULAR-BOUNDARY-CANONICALIZATION-kuangmanmozun-20260909T0942Z.md
    commit: 9d748de3be2b2cec2602ac9a96f90a5867cff405
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: preserve_the_physical_metric_nullspace_until_it_is_exactly_eliminated; use_the_nullspace_range_compatibility_packet_before_any_quotient_multiplier_search; on_success_apply_existing_T-P5-137_139_140_143_only_to_the_positive_definite_quotient_metric; on_failure_record_the_explicit_unbounded_ray_instead_of_tuning_multiplier_parameters
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: none; exact finite-dimensional quadratic-form algebra only
exit_code: n/a
---

# T-P5-144 — semidefinite physical-cell metric: exact nullspace elimination before reset multipliers

## 0. Narrow seam and non-overlap

T-P5-137/T-P5-139/T-P5-140 give a sharp quadratic reset multiplier architecture when the physical cell is an ellipsoid

`x^T G x <= R`

with `G>0`.  T-P5-143 explicitly leaves `G>=0` singular fail-closed: its canonical singular-*multiplier* range solve relies on a positive-definite cell metric.

This child addresses a different singularity: **the physical cell metric itself may have a kernel**.  In that case `x^T G x<=R` is a cylinder, not a bounded ellipsoid, and the uncontrolled directions must be settled before any multiplier optimization is meaningful.

The main result is an exact three-term completion.  It gives:

1. necessary and sufficient algebraic conditions for the reset quadratic to have a finite supremum along `ker G` (for positive cell radius);
2. a root-free elimination of those directions using only PSD checks and exact range solves;
3. an intrinsic reduced quadratic on a positive-definite quotient metric;
4. a direct bridge back to the existing T-P5-137/139/140/143 multiplier theory;
5. explicit unbounded rays when the nullspace conditions fail.

No T-P5-143 canonical singular-multiplier calculation is repeated.  No source binding, runtime semantics, provenance/admission, Lean compile, coverage, registry promotion, or parent closure is attempted.

---

## 1. Coordinate split induced by a semidefinite cell metric

Let `G` be a symmetric positive-semidefinite matrix on a finite-dimensional real space, and let

`N := ker G`.

Choose any complementary subspace `M` so that

`V = M direct_sum N`.

In a basis adapted to `(M,N)`, write a state as

`x=(m,n)`.

Because `G` is symmetric and `N=ker G`, every `n in N` is `G`-orthogonal to the whole space.  Therefore

`G = [[G_M, 0], [0, 0]]`

with

`G_M > 0`

on `M`.

Hence the physical cell

`x^T G x <= R`

is exactly

`m^T G_M m <= R`,

with **no direct bound at all on `n`**.

Let the symmetric reset curvature and affine term be split as

`H = [[H_MM, H_MN], [H_NM, A]]`,

`b=(b_M,b_N)`,

where

`A:=H_NN`, `H_NM=H_MN^T`.

Consider the reset quadratic

`f(m,n)`

`:= C + b_M^T m + b_N^T n`

`   - m^T H_MM m - 2 m^T H_MN n - n^T A n`.

The question is whether `f` has a finite upper bound on the cylindrical cell and, if so, how to reduce it to the positive-definite quotient variable `m`.

---

## 2. Exact nullspace range-compatibility packet

Assume first that

**(2.1)** `A >= 0`.

Require exact witnesses

**(2.2)** `A u = b_N`,

and

**(2.3)** `A L = H_NM`,

where `L` is a linear map from the quotient coordinates `M` into `N` (columnwise, each column of `H_NM` lies in `range A`).

These two equations are the full range-compatibility packet:

`b_N in range A`,

`range(H_NM) subseteq range A`.

No inverse or pseudoinverse is needed.  `A` itself may remain singular.

Define

**(2.4)** `C_eff := C + (b_N^T u)/4`,

**(2.5)** `b_eff := b_M - H_MN u`,

**(2.6)** `H_eff := H_MM - H_MN L`.

### Lemma 2.1 — symmetry and witness-independence

`H_eff` is symmetric, and all three effective quantities are independent of the particular exact choices of `u` and `L`.

### Proof

From `A L=H_NM` and symmetry of `A,H`,

`H_MN = H_NM^T = L^T A`.

Therefore

`H_MN L = L^T A L`,

which is symmetric PSD, hence `H_eff` is symmetric.

If `u'` is another solution of `A u'=b_N`, then `k:=u'-u` lies in `ker A`.  Since `b_N=A u` and `H_MN=L^T A`,

`b_N^T k = u^T A k = 0`,

`H_MN k = L^T A k = 0`.

So `C_eff` and `b_eff` do not change.

If `L'` is another solution of `A L'=H_NM`, then every column of `D:=L'-L` lies in `ker A`.  Hence

`H_MN D = L^T A D = 0`,

so `H_eff` is also unchanged.

Thus the quotient packet is intrinsic even when `A` is singular.

---

## 3. Main nullspace completion identity

Set

**(3.1)** `e_N := n - u/2 + L m`.

Then the following identity is exact:

**(3.2)**

`f(m,n)`

`= C_eff + b_eff^T m - m^T H_eff m`

`  - e_N^T A e_N`.

### Proof

Expand

`e_N^T A e_N`

`= n^T A n - n^T A u + 2 n^T A L m`

`  + (u^T A u)/4 - u^T A L m + m^T L^T A L m`.

Use

`A u=b_N`,

`A L=H_NM`,

`u^T A u=b_N^T u`,

`u^T A L m=(H_MN u)^T m`,

`L^T A L=H_MN L`.

Substitution gives exactly (3.2).

### Immediate consequence

Because `A>=0`,

**(3.3)**

`f(m,n) <= f_eff(m)`

where

`f_eff(m):=C_eff+b_eff^T m-m^T H_eff m`.

Equality is attained by any `n` satisfying

**(3.4)** `A(n-u/2+Lm)=0`.

In particular the rational/algebraic representative

**(3.5)** `n_*(m):=u/2-Lm`

always attains equality.

Therefore

**(3.6)**

`sup_{x^T G x<=R} f(x)`

`= sup_{m^T G_M m<=R} f_eff(m)`.

The semidefinite physical cell has now been reduced **exactly** to a genuine ellipsoid on `M`.

---

## 4. Finite-supremum classification and explicit obstructions

The range packet above is not merely convenient.  For `R>0` it is the exact condition preventing escape along the cylindrical directions.

### Theorem A — exact finite-supremum criterion for positive radius

Assume `R>0` and `G_M>0`.  Then the reset quadratic `f` has a finite supremum on

`m^T G_M m<=R`, `n arbitrary`

**if and only if** all three conditions hold:

1. `A>=0`;
2. `b_N in range A`;
3. `range(H_NM) subseteq range A`.

Under these conditions, (3.6) gives the exact reduced problem.

### Necessity proof / explicit counterexample rays

#### Failure 1: negative nullspace curvature

If some `z` satisfies

`z^T A z < 0`,

set `m=0`, `n=t z`.  Then

`f(0,tz)=C+t b_N^T z-t^2 z^T A z -> +infinity`

as `|t|->infinity` along a suitable sequence.  No finite reset budget exists.

#### Failure 2: affine nullspace force outside `range A`

Suppose `A>=0` but `b_N notin range A`.  For symmetric `A`,

`range A = (ker A)^perp`.

Hence there exists `z in ker A` with

`b_N^T z != 0`.

Again take `m=0`, `n=t z`.  The quadratic term vanishes and

`f(0,tz)=C+t b_N^T z`,

which is unbounded above in one sign of `t`.

#### Failure 3: cross-curvature outside `range A`

Now suppose `A>=0` and `b_N in range A`, but some column combination of `H_NM` lies outside `range A`.  Then there exist

`z in ker A`, `m_0 in M`

with

`z^T H_NM m_0 != 0`.

Because `R>0` and `G_M>0`, choose a nonzero rational/real scalar `eps` small enough that

`m:=eps m_0`

satisfies `m^T G_M m<=R`.

Since `b_N^T z=0`, along `n=t z` the coefficient of `t` is

`-2 z^T H_NM m != 0`.

Thus one sign of `t` makes `f(m,tz)->+infinity`.

This proves necessity.

### Radius-zero edge case

If `R=0`, then positive definiteness of `G_M` forces `m=0`; the cross block `H_NM` is never sampled.  In that degenerate case finiteness only requires `A>=0` and `b_N in range A`.  Do not impose the `H_NM` range condition as a false necessity when the quotient coordinate is identically zero.

---

## 5. Quotient multiplier theorem

After nullspace elimination, all previous positive-definite metric results can be used on the quotient.

Choose `tau>=0` and define

**(5.1)** `K_tau := H_eff + tau G_M`.

Assume

**(5.2)** `K_tau >= 0`,

and provide an exact range solve

**(5.3)** `K_tau y = b_eff`.

Define

**(5.4)** `q_tau := b_eff^T y`,

**(5.5)** `E_tau := C_eff + tau R + q_tau/4`.

Then T-P5-139's fixed-multiplier completion applies on `M`.

Combining that completion with (3.2) gives the main three-term identity:

### Theorem B — semidefinite-cell primal/dual gap decomposition

For every `(m,n)`,

**(5.6)**

`E_tau - f(m,n)`

`= e_N^T A e_N`

`  + tau (R-m^T G_M m)`

`  + (m-y/2)^T K_tau (m-y/2)`.

On the physical cell every term on the right is nonnegative.  Therefore

**(5.7)** `f(m,n) <= E_tau`.

This theorem is entirely inverse-free and square-root-free.  Its trusted data are only:

- PSD matrices;
- exact matrix-vector / matrix-matrix solves;
- rational scalar arithmetic;
- the quotient cell inequality.

### Equality/contact conditions

Equality in (5.7) holds exactly when all active nonnegative terms vanish:

**(5.8)** `A e_N=0`,

**(5.9)** `K_tau(m-y/2)=0`,

and, if `tau>0`,

**(5.10)** `m^T G_M m=R`.

At `tau=0`, boundary saturation is not required.

If both `A>0` and `K_tau>0`, the contact representative is unique in the eliminated directions:

`m_*=y/2`,

`n_*=u/2-L y/2`,

subject only to the cell/boundary condition required by `tau`.

If either PSD matrix is singular, the corresponding kernel produces a family of contact states, exactly as the range-completion identities predict.

---

## 6. Why this is the correct extension of T-P5-143

T-P5-143 studies a singular **multiplier curvature** `K_0` while keeping the physical metric positive definite.  The present child does not modify that result.

Instead:

1. first eliminate `ker G` using Theorem A and identity (3.2);
2. obtain the quotient metric `G_M>0` and effective reset packet `(H_eff,b_eff,C_eff,R)`;
3. run T-P5-137/T-P5-139 for fixed multiplier bounds;
4. run T-P5-140 for exact secant/optimality search;
5. if the quotient multiplier boundary is singular, run T-P5-143's canonical range-solve theorem **with `G_M`**, not with the original semidefinite `G`.

Thus the two singularities are cleanly separated:

- `ker G`: uncontrolled physical-cell directions, settled by nullspace elimination;
- `ker K_tau`: flat directions of the shifted reset curvature, settled by range solves/canonicalization after quotient reduction.

Conflating them loses both the exact obstruction ray and the sharp reset floor.

---

## 7. Structural fingerprint: generalized Schur complement without an inverse

The effective curvature

`H_eff=H_MM-H_MN L`, `A L=H_NM`

is the generalized Schur complement of the uncontrolled nullspace block.

The completion (3.2) shows that this Schur complement is not merely a matrix trick: it is the exact **energy-level elimination of a cylindrical state direction**.

The packet remains valid when `A` is singular because the range conditions remove every linear forcing component along `ker A`.  No Moore-Penrose pseudoinverse is needed.

This suggests a reusable structural fingerprint for Lyapunov/reset consumers:

> **Semidefinite-domain elimination fingerprint.**  Before bounding a quadratic power/reset term on a semidefinite sublevel metric, split the metric kernel.  Either prove positive/semidefinite curvature plus exact range compatibility in that kernel and Schur-eliminate it, or emit an explicit unbounded ray.  Only after elimination should norm bounds or multipliers be applied.

---

## 8. Exact examples

### Example 8.1 — singular physical metric but finite sharp reset

Take

`G=diag(1,0)`, `R=1`,

`H=[[2,1],[1,1]]`,

`b=(3,2)`, `C=0`.

Let `m=x_1`, `n=x_2`.  Then

`A=1`, `u=2`, `L=1`.

Hence

`C_eff=1`,

`b_eff=1`,

`H_eff=1`.

The exact completion is

**(8.1)**

`f(m,n)=1+m-m^2-(n-1+m)^2`.

The physical cell is only `m^2<=1`; `n` is unbounded, yet the reset remains finite because the null direction has restoring curvature.

The reduced quadratic has its maximum at

`m=1/2`,

with

**(8.2)** `max f = 5/4`.

This is recovered by the quotient multiplier with `tau=0`, `K_0=1`, `y=1`, so

`E_0=1+1/4=5/4`.

A contact state is `(m,n)=(1/2,1/2)`.

### Example 8.2 — affine nullspace obstruction

Take

`G=diag(1,0)`,

`H=diag(1,0)`,

`b=(0,1)`.

Then `A=0` but `b_N=1 notin range A={0}`.

At `m=0`,

`f(0,n)=C+n`,

so the cylindrical cell has no finite upper reset budget.

### Example 8.3 — cross-curvature obstruction

Take

`G=diag(1,0)`, `R>0`,

`H=[[1,1],[1,0]]`,

`b=0`.

Then `A=0`, while `H_NM=1 notin range A`.

For any sufficiently small nonzero feasible `m`,

`f(m,n)=C-m^2-2mn`.

Choosing the sign of `n` sends this to `+infinity`.  No choice of multiplier `tau` can repair the missing nullspace curvature because `tau G` is identically zero in the offending direction.

This last point is important operationally: **when the obstruction lies in `ker G`, increasing the reset multiplier cannot fix it.**

---

## 9. Rational producer/checker packet

A root-free source-independent checker can consume the following packet.

### 9.1 Basis split

Provide rational matrices `S,Z` whose columns form a full basis and such that

`G Z=0`.

Set

`G_M=S^T G S`.

Check `G_M>0`.

The transformed blocks are

`H_MM=S^T H S`,

`H_MN=S^T H Z`,

`A=Z^T H Z`,

`b_M=S^T b`,

`b_N=Z^T b`.

No orthonormal basis is needed; a rational complement is enough.

### 9.2 Nullspace elimination

Check

`A>=0`,

`A u=b_N`,

`A L=H_NM`.

Then form exactly

`C_eff=C+b_N^T u/4`,

`b_eff=b_M-H_MN u`,

`H_eff=H_MM-H_MN L`.

### 9.3 Quotient multiplier

For a candidate rational `tau>=0`, check

`K_tau=H_eff+tau G_M>=0`,

`K_tau y=b_eff`.

Then the exact reset bound is

`E_tau=C_eff+tau R+(b_eff^T y)/4`.

All matrix PSD checks can use the repository's existing exact rational principal-minor/LDL infrastructure.  The theorem itself does not require a pseudoinverse, spectral decomposition, matrix square root, or floating optimizer.

---

## 10. Candidate theorem decomposition for a future Lean sidecar

No Lean task is claimed here.  If later formalized, the mathematics naturally decomposes into small leaves:

### L1 — semidefinite-kernel block identity

From `G Z=0` and symmetry, prove the cross metric blocks vanish and the cell depends only on quotient coordinates.

### L2 — range-compatible nullspace completion

Premises:

`A` symmetric PSD,

`A u=b_N`,

`A L=H_NM`.

Conclusion: identity (3.2).

### L3 — witness-independence

Show `C_eff,b_eff,H_eff` do not depend on the chosen range solves.

### L4 — unbounded affine-nullspace ray

If `A>=0` and `z in ker A` with `b_N^T z !=0`, show the reset is unbounded on the physical cell.

### L5 — unbounded cross-nullspace ray

For `R>0`, if `z in ker A` and `z^T H_NM m_0 !=0`, use a scaled feasible `m_0` and `n=t z` to prove unboundedness.

### L6 — three-term multiplier completion

Combine L2 with the existing fixed-multiplier quotient completion to prove (5.6).

These are source-independent real-algebra lemmas.  Source equality and coverage remain separate obligations.

---

## 11. Fail-closed boundaries

1. `G>=0` is essential to interpret `ker G` as a zero-cost physical-cell direction.  An indefinite `G` does not define the same cylindrical sublevel geometry.
2. The chosen columns of `Z` must span the complete `ker G`.  Missing a zero-metric direction can hide a genuine unbounded ray.
3. `G_M>0` must be checked on the chosen complement.  It follows mathematically from a true direct-sum complement to `ker G`, but the finite rational packet should verify it explicitly.
4. `A>=0` is mandatory.  Negative curvature in a cell-null direction gives quadratic escape and cannot be repaired by increasing `tau`, since `tau G` vanishes there.
5. For `R>0`, both `b_N` and every column of `H_NM` must lie in `range A`.  Missing either condition gives a linear escape along `ker A`.
6. At `R=0`, the quotient variable is forced to zero, so the cross-range condition is sufficient but not necessary; do not claim the positive-radius iff theorem there.
7. Exact equations `A u=b_N` and `A L=H_NM` are used.  Approximate solves leave an uncontrolled linear residual in the unbounded `ker G` directions; a small numerical residual is not automatically harmless because the physical cell does not bound those directions.
8. The quotient reduction proves a finite reset envelope only for the stated quadratic model and same physical cell.  It does not bind a deployed controller/reference/source key.
9. T-P5-143 may be applied only after reduction, using the positive-definite quotient metric `G_M`; its canonical norm theorem must not be fed the original singular `G`.
10. No Lean/kernel receipt, independent 封不觉 verification, P8/domain coverage, runtime/Float64 evidence, admission, registry promotion, or parent closure is claimed.

---

## 12. Result

The positive-definite-cell restriction in the existing quadratic reset multiplier chain can be relaxed cleanly.

For a semidefinite physical metric `G`, split `N=ker G`.  On positive-radius cells, the reset quadratic has a finite supremum in the unbounded null directions **iff**

**`A:=H_NN >= 0`,**

**`b_N in range A`,**

**`range(H_NM) subseteq range A`.**

With exact solves

`A u=b_N`, `A L=H_NM`,

the reset decomposes exactly as

**`f(m,n)=C_eff+b_eff^T m-m^T H_eff m-(n-u/2+Lm)^T A(n-u/2+Lm)`**, 

where

`C_eff=C+b_N^T u/4`,

`b_eff=b_M-H_MN u`,

`H_eff=H_MM-H_MN L`.

Thus the entire semidefinite-cell problem reduces without loss to the positive-definite quotient ellipsoid `m^T G_M m<=R`.

For any quotient multiplier `tau` satisfying

`K_tau:=H_eff+tau G_M>=0`, `K_tau y=b_eff`,

the exact global gap is

**`E_tau-f(m,n)`**

**`=(n-u/2+Lm)^T A(n-u/2+Lm)`**

**` + tau(R-m^T G_M m)`**

**` + (m-y/2)^T K_tau(m-y/2)`**, 

with

`E_tau=C_eff+tau R+(b_eff^T y)/4`.

So the correct architecture is now explicit: **eliminate zero-cost physical directions first, then run the existing sharp multiplier theory on the quotient.**  If nullspace curvature or range compatibility fails, the right result is an explicit unbounded ray, not another multiplier search.