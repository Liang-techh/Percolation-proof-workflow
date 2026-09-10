---
kind: review_result
review_id: review-T-P5-235-equality-ellipsoid-rankfree-kkt-commutation-liuguanyi-20260910T1001Z
task_id: T-P5-235-EQUALITY-ELLIPSOID-RANKFREE-KKT-COMMUTATION
reviewer: 柳冠一
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-10T10:01:00Z
claim_commit: f9329277f55d27fb0a6892605bcea923e8374adb
inspected_commit: 1c074f03d5855488ce9b5f96cea437c0d5481973
upstream_commits:
  - 69e1214a25f1e14137fb606bb6025b33ae187dd3  # T-P5-234 rank-deficient equality quotient dual
  - 4b309ccdccf423d949421138b2b980e071fb2f49  # T-P5-233 linear-equality conditional curvature
  - 580ac9aef688269631f738f61bb24b4a7e196625  # T-P5-232 coupled-fiber conditional Schur reduction
  - 95fc7a17795dda55ed0f493d5588c573ef84151d  # T-P5-230 ellipsoid trust-region S-lemma closure
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_rankfree_equality_ellipsoid_psd_certificate; add_fixed_lambda_quotient_lift_commutation; add_fraction_free_active_kkt_packet; add_strict_margin_rationalization_boundary
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact finite-dimensional convex quadratic / KKT / adjugate algebra only; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-235 — equality + ellipsoid rank-free KKT commutation bridge

## 0. Verdict and seam

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-234 closed the rank-deficient centered equality problem and left one explicit next seam: intersect the exact equality manifold with a genuine bounded quadratic source fiber, but do so without first constructing a nullspace basis. T-P5-230 already gives the exact one-multiplier trust-region certificate when there is no equality.

This child proves that the two mechanisms combine without loss. For a homogeneous centered equality and a positive-definite ellipsoid, safety of a concave quadratic debit on

`A y = 0`, `y^T P y <= T^2`

is equivalent to one PSD block with **one equality multiplier vector and one nonnegative trust-region multiplier**. No row-rank assumption on `A` is required. Moreover, for every fixed trust multiplier `lambda`, quotienting by `ker(A)` and lifting with an equality multiplier are exactly equivalent. Thus equality reduction and trust-region dualization commute at the theorem level, not merely numerically.

For the active branch `lambda>0`, the packet admits a completely rational fraction-free form using `det`/`adj`; the only remaining scalar gate is one polynomial/rational inequality. A sharp active optimum is recognized by two exact equations: an equality-stationarity equation and the ellipsoid-boundary equation.

No actual P5 source equality, source ellipsoid, same-cell/tube coverage, Float64 enclosure, Lean/kernel receipt, independent validation, admission, registry mutation, or parent closure is claimed.

---

## 1. General joint-variable setup

Let

`y in R^n`,

`A in Q^(m x n)` with arbitrary row rank,

`H=H^T >= 0`,

`P=P^T > 0`,

`T>0`,

and define the concave quadratic debit

**`q(y) := q0 + 2 g^T y - y^T H y`.**

The actual bounded equality fiber is

**`F := { y : A y = 0, y^T P y <= T^2 }`.**

The desired Lyapunov sign is

`q(y) <= 0` for every `y in F`.

The T-P5-232/233/234 specialization is obtained by taking

`y=(v,z)`,

`A=[C,-B]`,

`H=diag(H_v,0)`,

`g=(0,t b)`,

`q0=t^2 a`,

with the same centered displacement `v=u-tx`. The joint ellipsoid may encode a true source tube in `(v,z)` coordinates. The theorem below deliberately keeps the source map abstract.

---

## 2. Exact rank-free equality + ellipsoid PSD certificate

For `lambda>=0` and `nu in R^m`, define

`K_lambda := H + lambda P`,

`c_lambda := -q0 - lambda T^2`,

and the symmetric homogenized block

**`M(lambda,nu) := [[K_lambda, A^T nu - g], [(A^T nu-g)^T, c_lambda]]`.**

### Theorem A — `equalityEllipsoid_safe_iff_rankFreePSDMultiplier`

Under the setup above, the following are equivalent.

1. `q(y)<=0` for every `y` satisfying `Ay=0` and `y^TPy<=T^2`.
2. There exist `lambda>=0` and `nu` such that

**`M(lambda,nu) >= 0`.**

No rank assumption on `A` is needed.

### Proof: sufficiency

For every `y`,

`[y;1]^T M(lambda,nu) [y;1]`

`= y^T H y - 2 g^T y - q0`

`  + lambda (y^T P y - T^2)`

`  + 2 nu^T A y`

`= -q(y) + lambda (y^T P y-T^2) + 2 nu^T Ay`.

On `F`, the equality term vanishes and the ellipsoid term is nonpositive. If the block is PSD, the left side is nonnegative, hence

`-q(y) >= lambda (T^2-y^TPy) >= 0`.

Therefore `q(y)<=0` on all of `F`.

### Proof: necessity

Minimize the convex quadratic

`f(y):=-q(y)=y^THy-2g^Ty-q0`

subject to `Ay=0` and `y^TPy-T^2<=0`.

Because `P>0` and `T>0`, the feasible set is nonempty and compact, and `y=0` is a strict Slater point for the inequality while satisfying the homogeneous equality. Hence the convex quadratic program has an attained optimum and strong Lagrange duality with dual attainment.

If `q<=0` on `F`, the primal minimum of `f` is nonnegative. Therefore some optimal `lambda>=0,nu` has globally nonnegative Lagrangian

`L(y)=f(y)+lambda(y^TPy-T^2)+2nu^TAy`.

A quadratic polynomial is globally nonnegative iff its homogenized symmetric matrix is PSD. That matrix is exactly `M(lambda,nu)`. QED.

### Interpretation

This is the equality-constrained version of the T-P5-230 S-lemma/trust-region packet. The equality multiplier does not require a row-space basis, pseudoinverse, or deletion of dependent rows; inconsistent dependent-row information is retained automatically because `Ay=0` is never compressed away.

---

## 3. Fixed-`lambda` quotient/lift commutation theorem

The previous proof uses convex duality globally. There is also a direct algebraic theorem explaining exactly why the equality multiplier and the trust multiplier commute.

Let `N` be any full-column matrix whose image is exactly `ker(A)`. Define

`H_N := N^T H N`,

`P_N := N^T P N > 0`,

`g_N := N^T g`,

and for fixed `lambda>=0`,

`K_N(lambda) := H_N + lambda P_N = N^T K_lambda N`.

The quotient homogenized block is

**`M_N(lambda) := [[K_N(lambda), -g_N],[-g_N^T,c_lambda]]`.**

### Theorem B — `fixedLambda_quotientPSD_iff_equalityMultiplierLift`

For every fixed `lambda>=0`,

**`M_N(lambda)>=0`**

if and only if there exists `nu` such that

**`M(lambda,nu)>=0`.**

This statement is independent of the chosen basis `N` of `ker(A)`.

### Proof

The reverse implication is immediate by restricting the full quadratic to `y=N xi`, because `AN=0`.

For the forward implication, `M_N(lambda)>=0` says the quadratic

`F_N(xi)=xi^T K_N xi-2g_N^Txi+c_lambda`

is nonnegative for all `xi`. Hence its minimum is attained at some `xi_*` satisfying

`K_N xi_*=g_N`.

Set `y_*=N xi_*`. Then

`N^T(K_lambda y_*-g)=0`.

Since `im(N)=ker(A)`, finite-dimensional orthogonality gives

`K_lambda y_*-g in range(A^T)`.

Choose `nu` so that

`K_lambda y_*-g + A^T nu=0`,

or equivalently

`g-A^Tnu=K_lambda y_*`.

Now

`[y;1]^T M(lambda,nu)[y;1]`

`= y^TK_lambda y -2 y_*^T K_lambda y + c_lambda`

`= (y-y_*)^T K_lambda (y-y_*)`

`  + c_lambda-y_*^T K_lambda y_*`.

The first term is nonnegative because `K_lambda>=0`. The scalar second term is exactly the minimum of `F_N`, hence is nonnegative by `M_N(lambda)>=0`. Therefore the full block is PSD. QED.

### Consequence — exact commutation

Restriction and trust loading commute identically:

**`N^T(H+lambda P)N = N^THN + lambda N^TPN`.**

Theorem B then says the quotient PSD certificate can always be lifted back to a rank-free equality-multiplier certificate at the same `lambda`. Therefore the two execution orders are mathematically identical:

1. quotient `Ay=0`, then apply T-P5-230 in quotient coordinates; or
2. add the trust-region multiplier first, then eliminate the equality by a multiplier `nu`.

No full-rank row assumption and no explicit quotient basis are required by the second route.

---

## 4. Active branch: exact fraction-free rational packet

The main implementation advantage appears when `lambda>0`. Since `P>0`,

**`K := H+lambda P > 0`.**

For rational `lambda`, all of `K` is rational. Define

`d := det(K) > 0`,

`J := adj(K)`,

so

`KJ=JK=dI`, `J>0`.

For a candidate equality multiplier `nu`, set

**`r := g-A^Tnu`.**

Then

`M(lambda,nu)=[[K,-r],[-r^T,c_lambda]]`.

### Theorem C — `activeLambda_fractionFreePSDGate`

For `lambda>0`,

`M(lambda,nu)>=0`

if and only if

**`d*c_lambda - r^T J r >= 0`.**

Equivalently, in the original debit sign convention,

**`d*(q0+lambda T^2) + r^T J r <= 0`.**

### Proof

Because `K>0`, the Schur complement is exact:

`M>=0 <-> c_lambda-r^TK^{-1}r>=0`.

Substitute `K^{-1}=J/d` and multiply by the positive `d`. QED.

### Trusted-checker content

A rational packet needs only:

1. rational `lambda>0,nu`;
2. exact `K=H+lambda P`;
3. `d=det(K)>0`, `J=adj(K)`, `KJ=dI`;
4. `r=g-A^Tnu`;
5. the scalar sign `d(q0+lambda T^2)+r^TJr<=0`.

No inverse or square root is needed in the trusted layer.

---

## 5. Best equality multiplier at a fixed active `lambda`

For fixed `lambda>0`, not every `nu` is equally useful. The best one is characterized by a rank-free normal equation.

### Theorem D — `activeLambda_equalityMultiplierNormalEquation`

Let `r=g-A^Tnu`. The equality multiplier is optimal for this fixed `lambda` exactly when

**`A J r = 0`.**

Equivalently,

**`(A J A^T) nu = A J g`.**

This system is always consistent, even if `A` is rank deficient.

### Proof of consistency

Since `J>0`,

`range(AJA^T)=range(A)`.

The right side `AJg` lies in `range(A)`, so the system is consistent. With rational data, a rational solution exists by exact linear algebra.

### Optimality identity

Assume `AJr=0` and replace `nu` by `nu+eta`. Then

`r_eta=r-A^Teta`.

The cross term vanishes:

`eta^T A J r=0`.

Hence

**`r_eta^T J r_eta = r^T J r + eta^T A J A^T eta >= r^T J r`.**

Thus the normal-equation multiplier minimizes the Schur surcharge and maximizes the certified margin at fixed `lambda`.

This is the rank-free equality analogue of orthogonal projection, but it uses only a PSD Gram equation and never constructs `ker(A)` explicitly.

---

## 6. Exact active KKT packet and sharp worst-case value

Assume `lambda>0`, choose `nu` satisfying `AJr=0`, and define the scaled candidate maximizer

**`y_* := J r / d`.**

Then

`Ay_*=0`

by the normal equation, and

`Ky_*=r`.

For every equality-feasible `y`,

`g^Ty=r^Ty`.

A direct completion gives

`q(y)`

`= q0 + lambda T^2 + 2r^Ty-y^TKy`

`  - lambda(T^2-y^TPy)`

`<= q0 + lambda T^2 + r^T K^{-1}r`

`= q0 + lambda T^2 + (r^TJr)/d`.

### Theorem E — `activeKKT_exactWorstCase`

If in addition the exact active-boundary equation holds,

**`(Jr)^T P (Jr) = d^2 T^2`,**

then `y_*` lies on the ellipsoid boundary and attains the upper bound. Therefore

**`sup_{Ay=0, y^TPy<=T^2} q(y)`**

**`= q0 + lambda T^2 + (r^T J r)/d`.**

Consequently the exact sharp safety gate is

**`d(q0+lambda T^2)+r^TJr <= 0`.**

No root extraction or quotient basis is needed to verify a supplied active KKT packet.

### Complementarity dispatcher

The combined problem has two clean branches.

- **Inactive trust region (`lambda=0`)**: the equality-only optimum lies inside the ellipsoid. Route directly to the T-P5-234 rank-free equality packet.
- **Active trust region (`lambda>0`)**: use Theorem E with the exact boundary equation.

This avoids forcing `det(H)>0` at `lambda=0`; the possibly singular equality-only branch remains exactly where T-P5-234 already has the correct range/kernel machinery.

---

## 7. Scalar dual after equality elimination, without a quotient basis

For every `lambda>0`, let `nu_lambda` solve

`A J_lambda (g-A^Tnu_lambda)=0`,

where

`J_lambda=adj(H+lambda P)`,

`d_lambda=det(H+lambda P)`.

Define

**`Phi(lambda) := q0 + lambda T^2 + (r_lambda^T J_lambda r_lambda)/d_lambda`.**

Then

**`Theta := sup_F q = inf_{lambda>=0} Phi(lambda)`,**

with the `lambda=0` endpoint interpreted by the T-P5-234 equality-only branch.

This is exactly the T-P5-230 scalar trust-region dual after quotienting by `Ay=0`, but written entirely in ambient coordinates. The equality normal equation computes the quotient metric projection implicitly.

For an active optimum, the derivative/envelope condition is precisely

`y_lambda^T P y_lambda = T^2`,

which is the fraction-free boundary equation in Theorem E.

Thus the equality multiplier `nu` and the trust multiplier `lambda` do not compete for different semantics: `nu` performs the metric projection at fixed `lambda`, while `lambda` tunes the trust curvature after that projection. Because the restriction identity in Section 3 is exact, either order yields the same scalar dual.

---

## 8. When the commutation statement is valid, and when it is not

The exact commutation theorem depends on three semantic conditions.

### 8.1 The equality must be exact and homogeneous in the same centered variables

`Ay=0` must describe the same centered displacement used in `q` and the ellipsoid. If the source relation is affine, `Ay=h`, one must first choose a feasible anchor and re-center **all three objects**: objective, equality, and ellipsoid. Re-centering only the equality changes linear and constant terms in the ellipsoid and invalidates the simple packet above.

### 8.2 The trust region must be the actual consumed quadratic set

Replacing the true source fiber by an outer ellipsoid preserves PASS soundness, because proving `q<=0` on a superset is safe. But failure of the outer ellipsoid certificate is not a source-level FAIL unless an actual source witness inside the true fiber is produced.

### 8.3 A relaxed equality tube is not an exact equality

If the source only gives `||Ay||<=eps`, then the term `2nu^TAy` no longer vanishes. The exact equality certificate cannot be consumed unchanged. A tube needs its own support/Young/S-lemma penalty. Treating a relaxed tube as `Ay=0` can create a false PASS.

These are typed source-interface boundaries, not numerical details.

---

## 9. Rationality and the sharp-boundary obstruction

For rational `H,P,A,g,q0,T^2` and a **rational active multiplier** `lambda>0`, every object in Theorems C-E is rational, including a solution of the rank-deficient normal equation. Hence the active packet is exactly replayable over rationals.

However, the optimal `lambda_*` of the trust-region problem need not be rational even for rational input. Therefore:

- if the final safety margin is **strictly negative**, continuity gives an open neighborhood of successful multipliers; a nearby rational `lambda` can be used, and the exact rational packet remains available;
- if the problem is exactly sharp with zero reserve and its unique optimizer is irrational, a purely rational exact-active packet may not exist. That boundary needs an algebraic-number/root-isolation or interval-certified multiplier representation rather than silently rounding `lambda_*`.

This is the same strict-margin versus sharp-root distinction already encountered elsewhere in the P5 chain. A decimal optimizer must not be promoted to an exact theorem at zero reserve.

---

## 10. Exact rational regression: neither equality-only nor ellipsoid-only is enough

Take

`y=(y1,y2)`,

`A=[1,-1]`, so `y1=y2`,

`H=diag(1,0)`,

`P=I`,

`T^2=1/2`,

`g=(0,1)`,

`q0=-3/4`.

Thus

`q(y)=-3/4+2y2-y1^2`.

On the equality manifold write `y1=y2=s`. The ellipsoid becomes

`2s^2<=1/2`, hence `|s|<=1/2`, and

`q=-3/4+2s-s^2`.

Its exact maximum is at `s=1/2` and equals zero. So the combined constraint is **sharp safe**.

### Equality-only fails

Without the ellipsoid, the equality-only maximum occurs at `s=1` and equals

`-3/4+2-1=1/4>0`.

### Ellipsoid-only fails

Without the equality, taking `y1=0` and positive `y2` near the ellipsoid boundary gives a strictly positive debit. Thus neither individual constraint proves safety; the intersection is essential.

### Exact active packet

Choose

`lambda=1/2`,

`nu=-3/4`.

Then

`K=H+lambda P=diag(3/2,1/2)`,

`d=det(K)=3/4`,

`J=adj(K)=diag(1/2,3/2)`,

`r=g-A^Tnu=(3/4,1/4)`.

The equality normal equation is exact:

`A J r = (1,-1) dot (3/8,3/8)=0`.

The reconstructed maximizer is

`y_*=Jr/d=(1/2,1/2)`.

The active boundary equation is exact:

`(Jr)^T P(Jr)=9/32=d^2 T^2`.

Finally,

`d(q0+lambda T^2)+r^TJr`

`= (3/4)(-3/4+1/4)+3/8`

`= -3/8+3/8=0`.

Hence the fraction-free packet certifies the sharp combined result with no inverse and no irrational constant.

---

## 11. Minimal theorem statements for formalization

Suggested finite-dimensional leaves:

1. `equalityEllipsoid_multiplier_sufficient`
   - direct quadratic identity from `M(lambda,nu)>=0`.

2. `fixedLambda_quotientPSD_iff_equalityMultiplierLift`
   - purely linear-algebraic proof; no optimization library required.

3. `equalityEllipsoid_safe_iff_rankFreePSDMultiplier`
   - can be obtained by composing the quotient theorem with the existing T-P5-230 exact ellipsoid theorem, avoiding formal convex-duality machinery if desired.

4. `activeLambda_fractionFreePSDGate`
   - `K>0`, `KJ=dI`, `d>0` implies block PSD iff scalar adjugate gate.

5. `activeLambda_equalityMultiplierNormalEquation`
   - `AJr=0` and exact optimality identity under `nu -> nu+eta`.

6. `activeKKT_exactWorstCase`
   - consume `AJr=0` and `(Jr)^TP(Jr)=d^2T^2`; conclude exact supremum and fraction-free sign gate.

7. `strictMargin_rationalMultiplierNeighborhood`
   - optional analysis lemma: strict negative reserve is open in `lambda`, allowing rationalization of an irrational optimizer.

Formalization should keep actual source binding, ellipsoid coverage, floating-point semantics, and admission entirely outside these algebraic leaves.

---

## 12. Remaining obligations and next seam

Still open:

- extraction of an actual same-key centered equality `Ay=0` from the P5 source/tangent/fiber equations;
- extraction of an actual bounded quadratic source fiber `y^TPy<=T^2` on the same coordinates and same cell/tube;
- proof that the equality and ellipsoid are exact, inner, or outer models with the correct PASS/FAIL semantics;
- interval/Float64 enclosure for `H,P,A,g,q0,T^2`;
- concrete strict reserve or a certified algebraic active multiplier at a sharp boundary;
- trajectory/cell/tube/global coverage;
- Lean implementation and pinned compile;
- independent validation by 封不觉;
- admission / registry / parent closure.

The next smallest mathematical seam is now **source-side quadratic-fiber transport through a non-injective coordinate map**: given a physical ellipsoid or energy sublevel in state coordinates and a possibly redundant lifted `(v,z)` representation, derive the exact pulled quadratic constraint and characterize when the pullback is positive definite only on the equality quotient. That theorem would remove the unnecessarily strong ambient assumption `P>0` while preserving the rank-free KKT packet via quotient coercivity, and would connect this branch directly to the source-to-math adapter layer rather than producing another abstract optimizer variant.
