---
kind: review_result
review_id: review-T-P5-142-robust-inexact-multiplier-bracket-guyuefangyuan-20260909T0931Z
task_id: T-P5-142-ROBUST-INEXACT-MULTIPLIER-BRACKET
reviewer: 古月方源
source_agent: 古月方源
created_at: 2026-09-09T09:31:00Z
claim_commit: 7b2cad5239705fa3ff6291f69cce935866e94d15
inspected_commit: 73c0244929135c9a9ce676490a47c1338ce1dc19
upstream_reviews:
  - path: agent_review_inbox/review-T-P5-139-RANGE-SOLVE-SCHUR-RESET-kuangmanmozun-20260909T0834Z.md
    commit: f0198916eb5fe1783cbeb9055031c9d9bd0dc954
  - path: agent_review_inbox/review-T-P5-140-MULTIPLIER-SECANT-OPTIMIZATION-honglianmozun-20260909T0908Z.md
    commit: 6d4275c964d8f3481f87e8546d7bec8b020651c0
  - path: agent_review_inbox/review-T-P5-141-INEXACT-RANGE-SOLVE-RESIDUAL-BRIDGE-liuguanyi-20260909T0912Z.md
    commit: 138a9ecb30323619bcac1b6b2b39c4d56435e100
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: use_the_intrinsic_floor_interval_and_asymmetric_two_point_sign_gates_to_drive_rational_multiplier_search; for_a_three_point_bracket_sharpen_the_middle_residual_cap_first; do_not_use_approximate_G_norm_as_a_stationarity_surrogate_near_singular_shifted_curvature_without_an_explicit_metric_bridge
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: none; exact finite-dimensional quadratic-form and ordered-field algebra only
exit_code: n/a
---

# T-P5-142 — robust multiplier bracketing from inexact range solves

## 0. Narrow seam and non-overlap

T-P5-139 identifies the exact fixed-multiplier Schur floor from an exact range solve. T-P5-140 then proves exact secant identities, discrete convexity, stationary optimality, and rational multiplier bracketing. T-P5-141 closes a different seam: an **inexact** range solve

`r = b - K y`

can still certify the same augmented PSD/reset statement if it carries a same-metric residual cap

`sigma K - r r^T >= 0`

and pays the corrected scalar floor.

T-P5-141 correctly leaves one point fail-closed: a conservative residual floor must not be treated as the exact sharp floor when optimizing the multiplier.

This child closes that narrow mathematical seam without pretending the approximate solve is exact. The main observation is:

> the residual cap encloses the **true intrinsic sharp floor** in a one-sided interval, and these one-sided intervals are enough to recover certified secant signs and a global rational optimizer bracket.

A useful consequence is unexpectedly asymmetric: to prove that the true floor decreases from a left candidate to a right candidate, only the **right** residual-energy cap enters; to prove that it increases, only the **left** cap enters. Therefore a three-point bracket around a middle multiplier consumes only the middle residual-cap size.

This review does not redo the augmented-PSD proof of T-P5-141, the exact secant proof of T-P5-140, source binding, solver/Float64 semantics, provenance/admission, Lean compilation, P8 coverage, or parent closure.

---

## 1. Setup and the hidden exact correction

Fix a range-feasible shifted curvature

`K = H + tau G`,

where `K` is symmetric PSD. Let the producer supply

`y`,

`r := b - K y`,

`sigma >= 0`,

with

**(1.1)** `sigma K - r r^T >= 0`.

T-P5-141 proves that (1.1) annihilates every null direction of `K`, hence in finite dimension

**(1.2)** `r in range(K)`.

Therefore there exists at least one correction vector `z` satisfying

**(1.3)** `K z = r`.

Then

**(1.4)** `u := y + z`

is an exact range solve:

`K u = K y + r = b`.

Define the intrinsic residual energy

**(1.5)** `rho := r^T z`.

Because `Kz=r`,

`rho = z^T K z >= 0`.

Moreover T-P5-141's residual-cap argument gives

**(1.6)** `rho <= sigma`.

Indeed, evaluate (1.1) on `z`:

`0 <= sigma z^T K z - (r^T z)^2`

`   = rho (sigma-rho)`.

Since `rho>=0`, this gives `rho<=sigma`. As in T-P5-139/T-P5-141, `rho` is independent of the chosen correction solution because two corrections differ by a null vector of `K`.

The key point is that the trusted consumer need not compute `z` or `rho`; it only uses

**(1.7)** `0 <= rho <= sigma`.

---

## 2. Exact true-floor decomposition

Let

**(2.1)** `A := b^T y + r^T y`.

Let `q := b^T u` be the intrinsic exact range-solve scalar associated with the true sharp fixed-multiplier floor.

### Theorem A — exact residual-energy decomposition of the sharp scalar

One has

**(2.2)** `q = A + rho`.

### Proof

Using `u=y+z` and `b=Ky+r`,

`q = b^T(y+z)`

`  = b^T y + b^T z`

`  = b^T y + (Ky+r)^T z`

`  = b^T y + y^T K z + r^T z`

`  = b^T y + r^T y + rho`

`  = A+rho`.

No inverse or pseudoinverse occurs.

For the T-P5-139/T-P5-140 sharp fixed-multiplier reset floor

**(2.3)** `E_tau := C + tau R + q/4`,

Theorem A and `0<=rho<=sigma` immediately give the exact interval

**(2.4)**

`A <= 4(E_tau-C-tau R) <= A+sigma`.

This is the main interface of this child.

The upper endpoint is exactly the conservative scalar used by T-P5-141:

`A+sigma = b^T y+r^T y+sigma`.

The lower endpoint is new and matters for optimization: the true sharp floor cannot fall below the signed quantity `A`.

If `sigma=rho` is the intrinsic residual energy, both sides collapse to equality and one recovers the exact T-P5-139 floor even though the producer initially supplied only an inexact vector `y`.

---

## 3. Budget trichotomy for one approximate candidate

Let a downstream layer allow reset headroom `J`. Define the scaled available Schur floor

**(3.1)** `S_J := 4(J-C-tau R)`.

From (2.4) there are three exact cases.

### Theorem B — accept / reject / unresolved split

1. If

   **(3.2)** `S_J < A`,

   then `J < E_tau`: this multiplier is mathematically impossible for that budget.

2. If

   **(3.3)** `A+sigma <= S_J`,

   then `E_tau <= J`, and this is exactly the T-P5-141 sufficient residual-cap gate.

3. If

   **(3.4)** `A <= S_J < A+sigma`,

   then the scalar residual-cap interface alone does not decide the true sharp floor. The correct action is to sharpen the residual energy, supply an exact correction solve, or change multiplier; it is not sound to promote the conservative endpoint to an exact optimum statement.

This distinction is useful operationally: the same approximate solve can produce a **hard rejection** before an exact correction is computed, because the lower endpoint `A` is already intrinsic-safe.

---

## 4. Two approximate multipliers: intrinsic cross-metric interval

Now take two range-feasible multipliers

`tau_0 < tau_1`,

and set

`d := tau_1-tau_0 > 0`.

For each endpoint let

`K_i = H+tau_i G`,

`r_i=b-K_i y_i`,

`A_i=b^T y_i+r_i^T y_i`,

and let `rho_i` be the intrinsic residual energy satisfying

`0<=rho_i<=sigma_i`.

Let `u_i` denote any exact corrected solve `K_i u_i=b`, and define the canonical exact cross metric

**(4.1)** `c_01 := u_0^T G u_1`.

T-P5-140 proves the exact range-solve secant identity

**(4.2)** `d c_01 = q_0-q_1`.

Using Theorem A,

`q_i=A_i+rho_i`,

so

**(4.3)**

`d c_01 = A_0-A_1 + rho_0-rho_1`.

Because `0<=rho_i<=sigma_i`, this yields the singular-safe interval

**(4.4)**

`A_0-A_1-sigma_1`

` <= d c_01`

` <= A_0-A_1+sigma_0`.

This is important: we enclosed the **exact canonical T-P5-140 cross metric** without bounding the approximate vectors in the `G` metric and without reconstructing either correction vector.

The interval remains valid at a singular feasible boundary because it is derived from the intrinsic exact floor scalars rather than from a noncanonical same-point norm.

---

## 5. Two-point robust floor-order gates

T-P5-140 also gives

**(5.1)** `4(E_1-E_0) = d(4R-c_01)`.

Combining with (4.3), define

**(5.2)**

`D_01 := 4 d R + A_1-A_0`.

Then the **true** sharp-floor difference satisfies the exact decomposition

**(5.3)**

`4(E_1-E_0) = D_01 + rho_1-rho_0`.

Hence

**(5.4)**

`D_01-sigma_0`

` <= 4(E_1-E_0)`

` <= D_01+sigma_1`.

This gives two fail-closed sign gates.

### Theorem C1 — certified descent

If

**(5.5)** `D_01+sigma_1 < 0`,

then

**(5.6)** `E_1 < E_0`.

Equivalently, without introducing `D_01`,

**(5.7)**

`A_0-A_1-sigma_1 > 4 d R`.

Notice that `sigma_0` does **not** enter this gate. Uncertainty in `rho_0` can only increase the old exact scalar `q_0`, which helps prove that moving right decreased the floor.

### Theorem C2 — certified ascent

If

**(5.8)** `D_01-sigma_0 > 0`,

then

**(5.9)** `E_1 > E_0`.

Equivalently,

**(5.10)**

`A_0-A_1+sigma_0 < 4 d R`.

Now `sigma_1` does not enter. Uncertainty in the new residual energy can only increase `q_1`, which helps the new point; to prove the new floor is still worse, only the old endpoint's upper correction matters.

The weak versions with `<=` / `>=` are immediate.

This directional asymmetry is the first main new consequence beyond T-P5-141.

---

## 6. Three-point global bracket using only the middle cap size

Take three range-feasible multipliers

`tau_0 < tau_1 < tau_2`,

with

`d_01=tau_1-tau_0`,

`d_12=tau_2-tau_1`.

Suppose each approximate packet is range-compatible as above. Numerically, assume only the middle residual cap `sigma_1` is sharpened enough to satisfy

**left descent gate**

**(6.1)**

`A_0-A_1-sigma_1 > 4 d_01 R`,

and

**right ascent gate**

**(6.2)**

`A_1-A_2+sigma_1 < 4 d_12 R`.

By Theorem C,

**(6.3)** `E_1<E_0`,

and

**(6.4)** `E_1<E_2`.

T-P5-140 proves that the true sharp floor is discretely convex on the range-feasible multiplier ray.

### Theorem D — robust three-point optimizer bracket

Under (6.1)-(6.2), every feasible multiplier `tau<tau_0` satisfies

**(6.5)** `E_tau>E_0>E_1`,

and every feasible multiplier `tau>tau_2` satisfies

**(6.6)** `E_tau>E_2>E_1`.

Therefore every feasible point with floor no larger than `E_1` lies inside

**(6.7)** `[tau_0,tau_2]`.

In particular, any global minimizer, if attained, lies in `[tau_0,tau_2]`.

### Proof on the left

Take any feasible `tau<tau_0`. Apply T-P5-140 discrete convexity to the triple

`tau < tau_0 < tau_1`.

Its division-free slope inequality is

`(tau_1-tau_0)(E_0-E_tau)`

` <= (tau_0-tau)(E_1-E_0)`.

The right side is strictly negative because `tau_0-tau>0` and `E_1-E_0<0`. Therefore

`E_0-E_tau<0`,

hence `E_tau>E_0>E_1`.

### Proof on the right

For any feasible `tau>tau_2`, apply discrete convexity to

`tau_1<tau_2<tau`:

`(tau-tau_2)(E_2-E_1)`

` <= (tau_2-tau_1)(E_tau-E_2)`.

The left side is strictly positive, so `E_tau-E_2>0`, proving (6.6).

### Middle-cap principle

The remarkable point is that the **sizes** of `sigma_0` and `sigma_2` do not enter (6.1)-(6.2). The outer packets still need range compatibility, but their residual-energy uncertainty has the favorable sign in the relevant comparison. Only the middle cap must be numerically tight.

Thus for a rational search algorithm, once three candidates are available, the best place to spend solve precision is the middle candidate rather than uniformly tightening every solve.

---

## 7. A root-free rational search rule

For rational source matrices/data and rational candidate multipliers, all consumed quantities can remain rational:

- `A_i=b^T y_i+r_i^T y_i`;
- `sigma_i`;
- `4(tau_j-tau_i)R`;
- the two sign reserves

  `Ldec := A_i-A_j-sigma_j-4(tau_j-tau_i)R`,

  `Linc := 4(tau_j-tau_i)R-(A_i-A_j+sigma_i)`.

A checker may use:

- `Ldec>0` to certify the exact floor decreased;
- `Linc>0` to certify the exact floor increased;
- both around a middle candidate to certify a global bracket by Theorem D.

No inverse, pseudoinverse, square root, determinant, eigenvalue, derivative, or numerical optimizer is required in the trusted search certificate.

If a pair is unresolved, one should sharpen only the cap whose sign actually matters:

- for attempted descent `i -> j`, sharpen `sigma_j`;
- for attempted ascent `i -> j`, sharpen `sigma_i`.

This is strictly more targeted than comparing two fully conservative T-P5-141 floors `A_i+sigma_i` and `A_j+sigma_j` symmetrically.

---

## 8. Why approximate same-point `G` norms are dangerous near singularity

A tempting shortcut is to reuse T-P5-140's stationarity test

`u_tau^T G u_tau ? 4R`

by simply replacing the exact solve `u_tau` with the approximate producer vector `y_tau`.

That is unsound even when the residual dual cap `sigma` is arbitrarily small.

### Counterexample — small `K`-residual energy, order-one `G` correction

In one dimension let

`G=1`,

`K=epsilon>0`,

`y=0`,

`b=epsilon`,

so

`r=b-Ky=epsilon`.

Take

`sigma=epsilon`.

Then the residual cap is exact:

`sigma K-r^2 = epsilon^2-epsilon^2 = 0`.

As `epsilon -> 0`, the certified residual energy `sigma` tends to zero.

But the exact correction is

`z=1`,

because `Kz=epsilon=r`, and therefore the exact solve is

`u=1`.

Thus

`G(y)=0`,

while

`G(u)=1`.

So no universal implication of the form

`small sigma => y is close to u in the G metric`

can hold without an additional comparison between `G` and `K`.

This is precisely why Sections 4-7 use the intrinsic scalar floor/cross-secant route: it remains stable as `K` approaches a singular feasible boundary.

---

## 9. Optional safe bridge back to the stationarity norm

Sometimes a producer may genuinely want the T-P5-140 same-point stationarity threshold. There is a safe additional interface, but it must be explicit.

Assume in addition that for some rational `lambda>=0`,

**(9.1)** `lambda K-G >= 0`.

Let `z` be the exact residual correction `Kz=r`. Then

`z^T G z <= lambda z^T K z`

`           = lambda rho`

`           <= lambda sigma`.

Hence

**(9.2)** `Q_G(z) <= lambda sigma`.

Let

`s := Q_G(y)`.

Choose rational `delta` with

`0<=delta<=1`

and

**(9.3)** `lambda sigma <= delta^2 s`.

Then `Q_G(z)<=delta^2 Q_G(y)`. Applying the root-free quadratic secant/tangent sandwich already established in T-P5-134 to

`u=y+z`

gives

**(9.4)**

`(1-delta)^2 s <= Q_G(u) <= (1+delta)^2 s`.

Therefore:

- if

  **(9.5)** `(1+delta)^2 s <= 4R`,

  then the exact solve satisfies `Q_G(u)<=4R`, and T-P5-140 proves no larger feasible multiplier can improve this point;

- if

  **(9.6)** `(1-delta)^2 s >= 4R`,

  then `Q_G(u)>=4R`, and the symmetric secant argument proves no smaller feasible multiplier can improve this point.

Two candidates satisfying the opposite inequalities give a two-point stationarity bracket.

### Important singular boundary

If `G>0` and `K` is singular, a full-space inequality `lambda K-G>=0` is impossible for finite `lambda`: take nonzero `v in ker K`, then

`v^T(lambda K-G)v = -v^T G v < 0`.

So (9.1) is naturally an interior positive-definite adapter. Near a singular lower boundary, use the intrinsic cross-floor method of Sections 4-7 or provide a range-restricted metric bridge; do not invent a finite full-space `lambda`.

---

## 10. Exact rational regression

Reuse the one-dimensional family from T-P5-140:

`G=1`,

`H=1`,

`b=4`,

`R=1`,

`C=0`.

The exact sharp floor is

`E_tau = tau + 4/(1+tau)`,

with global optimum at `tau=1`.

Use deliberately inexact rational solves.

### At `tau_0=0`

`K_0=1`, choose `y_0=3`.

Then

`r_0=4-1*3=1`,

choose the sharp cap `sigma_0=1`,

and

`A_0=4*3+1*3=15`.

The true exact scalar is `q_0=16`, which indeed lies in `[15,16]`.

### At `tau_1=1`

`K_1=2`, choose `y_1=3/2`.

Then

`r_1=4-2*(3/2)=1`,

`sigma_1=1/2`, because

`sigma_1 K_1-r_1^2 = 1-1=0`,

and

`A_1=4*(3/2)+1*(3/2)=15/2`.

The exact scalar is `q_1=8`, lying in `[15/2,8]`.

### At `tau_2=2`

`K_2=3`, choose `y_2=1`.

Then

`r_2=1`,

`sigma_2=1/3`,

`A_2=4+1=5`,

while the exact scalar is `q_2=16/3`.

### Left descent gate

Here `d_01=1`, and

`A_0-A_1-sigma_1`

` = 15-15/2-1/2`

` = 7`

` > 4 = 4d_01R`.

Hence the true floor strictly decreases:

`E_1<E_0`.

Indeed `E_0=4` and `E_1=3`.

### Right ascent gate

Here `d_12=1`, and

`A_1-A_2+sigma_1`

` = 15/2-5+1/2`

` = 3`

` < 4 = 4d_12R`.

Hence

`E_2>E_1`.

Indeed `E_2=10/3>3`.

Therefore Theorem D certifies that every global minimizer lies in

`[0,2]`

using approximate solves, and the two numerical sign gates consume only the middle cap `sigma_1=1/2`.

This regression also shows that the method is not merely an acceptance bound for one LMI: it recovers true multiplier-search information lost by naively treating conservative floors as exact.

---

## 11. Suggested Lean theorem split

The highest-value source-independent Lean leaves are small.

### L1 — `sharpFloor_eq_approxBase_add_residualEnergy`

Inputs:

- symmetric `K`;
- `r=b-Ky`;
- `Kz=r`;
- `u=y+z`;
- `Ku=b`.

Conclusion:

`b dot u = (b dot y + r dot y) + r dot z`.

This is ring algebra plus symmetry.

### L2 — `residualEnergy_interval_of_dualCap`

Inputs:

- `K>=0`;
- `Kz=r`;
- `sigma>=0`;
- `sigma K-r r^T>=0`.

Conclusion:

`0 <= r dot z <= sigma`.

The proof is exactly Section 1.

### L3 — `sharpFloor_interval_of_inexactSolve`

Compose L1/L2 and the scaled floor equality to conclude

`A <= 4(E-C-tau R) <= A+sigma`.

### L4 — `inexactFloor_difference_interval`

Pure scalar theorem:

if `0<=rho_i<=sigma_i` and

`Delta=D+rho_1-rho_0`,

then

`D-sigma_0 <= Delta <= D+sigma_1`.

This is likely a few lines of `linarith`/ordered-ring reasoning and is the best immediate checker leaf.

### L5 — `inexactFloor_descent` / `inexactFloor_ascent`

From L4 derive the strict sign gates (5.5) and (5.8).

### L6 — `threePoint_bracket_of_discreteConvex`

Abstract away all matrix data. Inputs:

- `tau_0<tau_1<tau_2`;
- `E_1<E_0` and `E_1<E_2`;
- the T-P5-140 discrete-convex secant inequality for arbitrary feasible triples.

Conclusion:

all feasible `tau<tau_0` have `E_tau>E_0`, and all feasible `tau>tau_2` have `E_tau>E_2`.

### L7 — optional `residual_to_stationarity_metric`

Inputs:

- `Kz=r`;
- residual-energy upper bound `r dot z<=sigma`;
- `lambda K-G>=0`.

Conclusion:

`Q_G(z)<=lambda sigma`.

Then reuse T-P5-134's quadratic sandwich rather than reproving it.

No matrix inverse API is needed in these trusted statements.

---

## 12. Source/checker packet suggested by this child

For each rational multiplier candidate retain, under the same reset/cell/reference key:

1. `tau`, `K=H+tau G`, and PSD witness for `K`;
2. approximate `y`;
3. exact signed residual identity `r=b-Ky`;
4. `sigma>=0` and exact same-metric cap `sigma K-r r^T>=0`;
5. exact scalar `A=b^T y+r^T y`;
6. for search, compare `A` and only the directionally relevant residual cap using Sections 5-7;
7. only if using the optional same-point stationarity route, additionally supply the explicit `G`-to-`K` metric bridge (or a correctly typed range-restricted substitute).

A generic solver tolerance, Euclidean residual norm, or approximate `y^TGy` is not a substitute for this packet.

---

## 13. Fail-closed boundaries

1. The interval theorem assumes the T-P5-141 same-metric residual cap, not merely a norm report.
2. `r` must remain the exact signed residual of the same `K,b,y`.
3. The range-compatibility consequence is finite-dimensional and depends on symmetry/PSD; do not transplant it to an arbitrary operator without the corresponding closed-range theorem.
4. `A` is signed. Replacing `r^T y` by an absolute-value bound is a separate conservative adapter and may destroy the asymmetric search advantage.
5. The two-point sign gates certify the **true sharp S-procedure floor** only under the exact upstream quadratic reset model and same source key; they do not certify that the deployed reset source equals that model.
6. T-P5-140 discrete convexity is consumed only after exact range feasibility is recovered mathematically; an arbitrary approximate solve with a nullspace residual component remains rejected.
7. Small `sigma` does not imply small correction in the physical `G` metric near singular `K`; Section 8 is a hard counterexample.
8. The optional full-space bridge `lambda K-G>=0` cannot hold at singular `K` when `G>0`; use the cross-floor route there.
9. A bracket localizes the true multiplier optimum. It does not prove the optimum fits the downstream dwell/headroom budget, nor does it close the actual source/coverage/controller/P8 obligations.
10. No Lean/kernel receipt, independent verification by 封不觉, admission, or registry promotion is claimed here.

---

## 14. Result

The multiplier-search seam left open by T-P5-141 is now closed at the mathematical interface level without upgrading a conservative solve into an exact one.

For every approximate same-metric residual packet,

**`A := b^T y+r^T y`**

satisfies

**`A <= 4(E_tau-C-tau R) <= A+sigma`**

for the **true intrinsic sharp fixed-multiplier floor**.

For two candidates `tau_0<tau_1`, this yields the exact sign-safe interval

**`D_01-sigma_0 <= 4(E_1-E_0) <= D_01+sigma_1`**,

where

`D_01=4(tau_1-tau_0)R+A_1-A_0`.

Thus descent only needs the right cap, ascent only the left cap. For three candidates, the two gates

**`A_0-A_1-sigma_1 > 4(tau_1-tau_0)R`**

and

**`A_1-A_2+sigma_1 < 4(tau_2-tau_1)R`**

combine with T-P5-140 discrete convexity to place every global minimizer inside `[tau_0,tau_2]`; only the middle residual-cap size is numerically consumed.

The near-singular counterexample also shows why this intrinsic floor/cross-secant route is preferable to treating an approximate same-point `G` norm as a stationarity witness.

Current status remains `CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending` until actual same-key source packets, coverage, runtime semantics, Lean/kernel validation, independent verification, and admission gates are supplied.
