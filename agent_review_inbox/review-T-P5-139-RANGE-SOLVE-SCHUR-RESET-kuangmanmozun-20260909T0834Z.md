---
kind: review_result
review_id: review-T-P5-139-range-solve-schur-reset-kuangmanmozun-20260909T0834Z
task_id: T-P5-139-RANGE-SOLVE-SCHUR-RESET
reviewer: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-09T08:34:00Z
claim_commit: bd6da17a29757a78f6376180efb31aaefa66ecc2
inspected_commit: 725f76e5bd27c658e59183961d762b9b719d7716
upstream_reviews:
  - path: agent_review_inbox/review-T-P5-137-ELLIPSOIDAL-KNOT-RESET-MULTIPLIER-honglianmozun-20260909T0811Z.md
    commit: f4212a7463a782d219e0ee2dbcbba06f4c04b8b5
  - path: agent_review_inbox/review-T-P5-138-RANKONE-SCHUR-RESET-DECOMPOSITION-guyuefangyuan-20260909T0824Z.md
    commit: 2a86f55903249300cd2bde81f678f1e34f7493f1
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: for_each_fixed_tau_prefer_psd_shifted_curvature_plus_exact_range_solve_and_one_scalar_floor_gate; keep_augmented_LMI_for_joint_search; reject_only_fixed_tau_when_b_not_in_range_K
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: none; exact quadratic-form completion and rational arithmetic only
exit_code: n/a
---

# T-P5-139 — exact range-solve reduction of the fixed-multiplier Schur reset gate

## 0. Narrow seam and non-overlap

T-P5-137 gives the lossless one-constraint ellipsoidal reset certificate

`M(tau,E) = [[H+tau G, -b/2],[-b^T/2, E-C-tau R]] >= 0`,

and T-P5-138 decomposes a fixed `(tau,E)` check into

`K_tau := H+tau G >= 0`,

`e := E-C-tau R >= 0`,

`4 e K_tau - b b^T >= 0`.

The remaining checker cost is still an `n x n` rank-one PSD test. This child removes that test when the producer can provide one exact linear solve in the shifted curvature metric.

It does **not** redo the S-procedure, source binding, actual reference extraction, provenance, Lean compilation, admission, registry promotion, or flowpipe/coverage work.

The key new observation is an exact completion identity. For a symmetric PSD matrix `K`, if a vector `y` satisfies

`K y = b`,

then the entire augmented Schur block is controlled by the single scalar `b^T y`.

---

## 1. Exact completion identity

Let `K` be symmetric, let `b,y,x` be real finite-dimensional vectors, and let `e,t` be real scalars. Assume

**(1.1)** `K y = b`.

Set

`q := b^T y`.

By symmetry and (1.1),

`q = y^T K y`.

Then for every `x,t`,

**(1.2)**

`4 [ x^T K x - t b^T x + e t^2 ]`

` = (2x-t y)^T K (2x-t y) + t^2 (4e-q)`.

### Proof

Expand the right-hand side:

`(2x-t y)^T K (2x-t y)`

` = 4 x^T K x - 4t y^T K x + t^2 y^T K y`

` = 4 x^T K x - 4t b^T x + t^2 q`.

Adding `t^2(4e-q)` gives exactly

`4 x^T K x - 4t b^T x + 4e t^2`.

No inverse, square root, pseudoinverse, eigenvalue, Cauchy tuning parameter, or division is used.

---

## 2. Main sufficient theorem: PSD + exact solve + one scalar gate

### Theorem A — range-solve block nonnegativity

Assume:

1. `K` is symmetric PSD;
2. `K y = b`;
3. `4e - b^T y >= 0`.

Then for every `x,t`,

**(2.1)**

`x^T K x - t b^T x + e t^2 >= 0`.

Equivalently,

**(2.2)**

`[[K,-b/2],[-b^T/2,e]] >= 0`.

### Proof

In (1.2), the first term is nonnegative because `K>=0`; the second is nonnegative because `t^2>=0` and `4e-b^T y>=0`. Hence the left side is nonnegative.

The scalar gate automatically implies `e>=0`: since

`b^T y = y^T K y >=0`,

we have `4e>=b^T y>=0`.

So a separate bottom-right nonnegativity gate is unnecessary once the solve and PSD hypotheses are present.

---

## 3. Sharp necessity at a supplied solve

The scalar floor in Theorem A is not merely sufficient.

### Theorem B — floor necessity

Assume `K y=b` and the augmented block is PSD. Then

**(3.1)** `b^T y <= 4e`.

### Proof by one test vector

Evaluate the augmented quadratic form at `(x,t)=(y,2)`:

`y^T K y - 2 b^T y + 4e`

` = q - 2q + 4e`

` = 4e-q`.

PSD therefore forces `4e-q>=0`.

Thus, for any fixed exact solution `y`, the smallest admissible scalar is exactly

**(3.2)** `e_min = (b^T y)/4`.

The root-free checker need not divide by four; it can retain the exact gate

**(3.3)** `4e - b^T y >=0`.

If a proposed floor violates (3.3), the single explicit witness `(y,2)` already rejects the augmented PSD claim.

---

## 4. Singular-safe exactness and solution-value invariance

A singular `K` is not a problem if `b` lies in its range.

Suppose

`K y=b`, `K y'=b`.

Then `v:=y-y'` satisfies `K v=0`. By symmetry,

`b^T v = (K y)^T v = y^T K v =0`.

Hence

**(4.1)** `b^T y = b^T y'`.

So the scalar

**(4.2)** `q_K(b) := b^T y  for any solution K y=b`

is well-defined even when the solution is nonunique.

Moreover

`q_K(b)=y^T K y>=0`.

Therefore the fixed-`K` minimal Schur floor is intrinsic; it does not depend on which exact solution the producer returns.

This is the singular-safe analogue of `b^T K^{-1} b`, but it never introduces an inverse or pseudoinverse into the trusted statement.

---

## 5. Finite-dimensional equivalence

For a symmetric matrix `K` in finite-dimensional real space, the augmented block is PSD if and only if

**(5.1)** `K>=0`,

**(5.2)** there exists `y` with `K y=b`,

**(5.3)** `b^T y <= 4e`.

The reverse implication is Theorem A.

For the forward implication, PSD gives `K>=0`. If `v in ker K`, test the augmented quadratic at `(x,t)=(s v,1)`:

`e - s b^T v >=0` for every real `s`.

This is possible only if `b^T v=0`. Hence `b` annihilates `ker K`. For symmetric finite-dimensional `K`,

`range(K)=ker(K)^perp`,

so `b in range(K)` and some `y` solving `K y=b` exists. Theorem B then gives (5.3).

This isolates the exact singular obstruction:

> a fixed multiplier can fail for every finite reset floor solely because the reset covector has a component along the nullspace of the shifted curvature.

That is a failure of the **fixed multiplier**, not automatically a failure of the bounded physical reset problem; changing `tau` can move `K_tau` away from the incompatible singular boundary.

---

## 6. Direct specialization to the ellipsoidal knot reset

For T-P5-137/138 define

`K_tau := H + tau G`,

`e_tau,E := E-C-tau R`.

### Theorem C — range-solve ellipsoidal reset gate

Assume:

1. `tau>=0`;
2. `K_tau>=0`;
3. an exact vector `y_tau` satisfies `K_tau y_tau=b`;
4. the scalar floor gate

**(6.1)**

`4(E-C-tau R) - b^T y_tau >=0`.

Then the T-P5-137 block PSD condition holds, hence on every physical state with

`x^T G x<=R`,

**(6.2)**

`W_+(x) <= kappa W_-(x) + E`.

For a fixed multiplier `tau`, the exact minimal block-certificate floor is therefore characterized by

**(6.3)**

`4(E_min-C-tau R) = b^T y_tau`.

The checker can stay division-free and consume (6.1) directly.

### Dwell/headroom form

If the downstream hybrid layer gives a maximum admissible knot charge `J`, simply replace `E` by `J`:

**(6.4)**

`4(J-C-tau R) - b^T y_tau >=0`.

This removes an augmented matrix and also removes the T-P5-138 rank-one PSD matrix from the fixed-`tau` consumer.

---

## 7. Relation to the T-P5-138 dual-cap corollary

T-P5-138 allows a source-side dual cap `Bdual` satisfying

`Bdual K - b b^T >=0`.

When `K y=b`, the intrinsic scalar

`q=b^T y`

is the sharp dual constant in the `K` metric.

Indeed, PSD Cauchy for the semidefinite form induced by `K` gives

`(b^T x)^2 = (y^T K x)^2 <= (y^T K y)(x^T K x)`

` = q (x^T K x)`.

Hence

**(7.1)** `q K - b b^T >=0`.

Conversely, if some `Bdual K-bb^T>=0`, evaluate at `x=y`:

`Bdual q-q^2 = q(Bdual-q)>=0`.

If `q>0`, this forces `Bdual>=q`. If `q=0`, PSD plus `K y=b` implies `b=0`, and the sharp dual constant is `0`.

Thus the exact solve does not merely produce a valid `Bdual`; it produces the **smallest possible one**. The T-P5-138 condition `Bdual<=4e` then collapses to the single sharp gate `q<=4e`.

---

## 8. Exact rational consequence

Suppose a fixed `tau` has already been chosen rationally and `K_tau,b,C,R,E` are rational.

If the producer supplies a rational solution of

`K_tau y_tau=b`,

then every remaining quantity in Theorem C is rational:

- `b^T y_tau`;
- `4(E-C-tau R)-b^T y_tau`;
- the matrix entries of `K_tau`.

Therefore the trusted packet can consist of:

1. an exact rational PSD witness for `K_tau`;
2. exact rational row equalities `K_tau y_tau=b`;
3. one exact rational scalar inequality (6.1).

No inverse, square root, algebraic number, pseudoinverse, augmented LDL, or rank-one PSD decomposition is needed.

For a rational linear system, if consistency is established, ordinary exact Gaussian elimination can choose a rational solution. The remaining rational-boundary caveat from T-P5-137 concerns the search for the multiplier `tau` itself, not the fixed-`tau` linear solve or the corresponding optimal floor.

---

## 9. Sharp singular-compatible example

Take the two-dimensional physical cell

`G=I`, `R=1`,

and reset packet

`H=diag(-1,1)`, `b=(0,3)`, `C=0`.

Choose the multiplier

`tau=1`.

Then

`K_tau=H+G=diag(0,2)`,

which is singular PSD.

The reset covector is compatible with the nullspace. Solve

`K_tau y=b`.

One rational solution is

`y=(0,3/2)`.

Therefore

`q=b^T y=9/2`.

The sharp fixed-`tau` scalar gate is

`4(E-1)-9/2>=0`,

so

**(9.1)** `E>=17/8`.

At `E=17/8` the gate is exact equality.

This is not merely a multiplier artifact. The physical reset envelope is

`3 x2 + x1^2 - x2^2`

on

`x1^2+x2^2<=1`.

For fixed `x2`, maximizing in `x1` uses `x1^2=1-x2^2`, giving

`1+3x2-2x2^2`.

Its maximum occurs at `x2=3/4`, with value

`1 + 9/4 - 18/16 = 17/8`.

Hence the singular-compatible range-solve certificate recovers the **true physical optimum exactly**.

This is a concrete reason not to strengthen `K_tau>=0` to positive definiteness.

---

## 10. Singular-incompatible counterexample

Keep

`K=diag(0,2)`,

but take

`b=(1,0)`.

There is no solution to `K y=b` because `b` points directly into the nullspace direction.

For any finite `e`, evaluate the augmented quadratic at

`x=(s,0)`, `t=1`:

`x^T Kx - b^T x + e = e-s`.

Choosing `s>e` makes this negative. Therefore no finite floor can make that fixed block PSD.

This is a decisive obstruction and should be checked before spending search effort on increasing `E` at the same singular multiplier.

Again, it rejects only that fixed `tau`; it does not by itself reject the bounded-cell reset statement, because a different multiplier may restore compatible/positive shifted curvature.

---

## 11. Minimal Lean-facing theorem split

A very small formalization can avoid range, inverse, and block-matrix APIs initially.

### L1 — `quadratic_block_nonneg_of_psd_solve_floor`

Inputs:

- symmetric PSD quadratic form `K`;
- `K y=b`;
- `b dot y <= 4e`.

Conclusion for all `x,t`:

`0 <= x^T K x - t*(b dot x) + e*t^2`.

Proof target is the exact identity

`4*lhs = Q_K(2x-t y) + t^2*(4e-b dot y)`.

### L2 — `solve_floor_necessary_of_block_nonneg`

Inputs:

- `K y=b`;
- block quadratic nonnegative for all `x,t`.

Conclusion:

`b dot y <= 4e`.

Proof: specialize to `x=y,t=2`.

### L3 — `solve_energy_unique`

Inputs:

`K y=b`, `K y'=b`, `K` symmetric.

Conclusion:

`b dot y=b dot y'`.

This is the singular-solution invariance needed to make the scalar floor well-defined.

### L4 — optional finite-dimensional range equivalence

After the three algebraic leaves compile, one may add the range theorem

`block PSD <-> K PSD and exists y, K y=b and b dot y<=4e`,

using `range(K)=ker(K)^perp` for symmetric finite-dimensional maps.

The trusted reset consumer does not need L4 if the source packet explicitly supplies `y`.

---

## 12. Fail-closed boundaries

This child does **not** permit any of the following shortcuts:

- dropping the exact equality `K_tau y_tau=b` and treating an approximate solve as exact;
- using a Euclidean solve when the actual shifted curvature is a different matrix object;
- treating a singular-incompatible fixed `tau` as a proof that the bounded physical reset is impossible;
- turning a rational candidate `tau` into a source-bound multiplier without same-cell `G,H,b,C,R` identity;
- replacing an actual-source/coverage packet by this source-independent theorem;
- promoting a mathematical child to Lean/kernel, registry, P5, P8, or M4 closure.

If an approximate solve is all that is available, its residual must be retained as a new signed/additive term and budgeted separately; it cannot be silently absorbed into (6.1).

---

## 13. Recommended next packet

For each frozen candidate multiplier `tau`, the smallest high-value producer packet is now:

1. exact same-key `K_tau=H+tau G`;
2. exact PSD witness for `K_tau`;
3. exact rational vector `y_tau` with `K_tau y_tau=b`;
4. exact scalar `q_tau=b^T y_tau`;
5. available dwell/reset floor `J` or `E`;
6. scalar reserve `4(E-C-tau R)-q_tau` (or the `J` version).

If item 3 is inconsistent, expose a nullspace witness and move `tau` rather than increasing the floor. If the scalar reserve is negative, the supplied `(y_tau,2)` gives an immediate exact rejection witness for that fixed multiplier. If it is nonnegative, no rank-one PSD matrix or augmented Schur factorization is needed at verification time.

Current status remains `CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending`. No actual source, same-cell coverage, Float64/controller semantics, P8 flowpipe, Lean/kernel receipt, independent verification, admission, registry, or P5/M4 parent closure is upgraded.
