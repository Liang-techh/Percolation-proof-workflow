---
kind: review_result
review_id: review-T-P5-239-rankone-twocap-fiber-secular-liuguanyi-20260910T1059Z
task_id: T-P5-239-RANKONE-TWOCAP-FIBER-SECULAR
reviewer: 柳冠一
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-10T10:59:00Z
claim_commit: 1aebf9fb52a300b0eec3cb0e7bfc9c4590167bb8
inspected_commit: ca8af5e8ecd5576e5b58b729b29e58cbe69aebf7
upstream_commits:
  - bb04e60d4718744aeb58d390ace3b5742f53fa5e  # T-P5-238 dominant-cap single-S-lemma closure
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_rankone_two_cap_fiber_theorem; add_piecewise_switch_contract; add_transverse_trust_region_secular_packet; add_two_centered_caps_homogeneous_exact_sprocedure; add_exact_affine_target_counterexample; keep_generic_affine_rankone_branch_unresolved_without_fiber_or_primal_certificate
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact finite-dimensional algebra, trust-region KKT/secular reduction, elementary SDP rank-reduction argument, and exact rational counterexample; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-239 — Rank-one two-cap fiber/secular bridge and the exact affine-target obstruction

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-238 leaves the first genuinely active noncommuting branch: after whitening one coercive centered source cap, suppose a second centered cap differs from a scalar multiple of the first by rank one. This child gives the exact source geometry and then separates two target regimes which must not be conflated:

1. for a **homogeneous quadratic debit**, two centered caps already admit a lossless two-multiplier PSD certificate (the rank-one source hypothesis is not even needed);
2. for a **general affine-quadratic debit with a linear term**, rank-one source interaction does **not** restore losslessness. An exact rational 2D counterexample is given below.

What rank-one interaction does give in the affine case is an exact one-coordinate fiber decomposition. Each fiber is one ordinary Euclidean trust-region problem, hence has a one-scalar secular/KKT description. This is an exact bridge, but it is not equivalent to one global constant two-multiplier S-procedure.

No actual P5 source matrix, tube identity, trajectory coverage, Float64 enclosure, Lean receipt, independent validation, admission, registry mutation, or parent closure is claimed.

---

# Part I — exact rank-one source geometry after whitening

## 1. Normal form

Let the first source cap have already been whitened and radius-normalized:

`E1 = { z in R^n : ||z||^2 <= 1 }`.

Assume the second normalized centered cap has

`A2 = a I + b u u^T`,

where

- `||u||=1`;
- `a>0`;
- `a+b>0`.

Thus

`E2 = { z : a ||z||^2 + b (u^T z)^2 <= 1 }`.

This is exactly the case in which the second cap differs from the scalar multiple `a I` by rank one.

Decompose uniquely

`z = s u + w`, with `u^T w = 0`.

Then

`||z||^2 = s^2 + ||w||^2`,

and the two source inequalities are

`||w||^2 <= r1^2(s) := 1-s^2`,

`||w||^2 <= r2^2(s) := [1-(a+b)s^2]/a`.

Hence the intersection is exactly

**`E1 intersect E2 = { s u+w : u^T w=0, ||w||^2 <= R^2(s) }`,**

where

**`R^2(s)=min(r1^2(s),r2^2(s))`**

on the scalar interval where both right sides are nonnegative.

### Theorem A — `rankOneTwoCap_exactFiber`

The formula above is an iff, not an outer relaxation. It uses only orthogonal decomposition along the one rank-changing direction `u`.

## 2. Exact switch law

The difference of the two transverse radius squares is

`r2^2(s)-r1^2(s) = [1-a-b s^2]/a`.

Therefore, in the genuinely active crossing regime

`(a-1)(a+b-1)<0`,

there is one switch in `s^2` at

**`s_*^2 = (1-a)/b`.**

No matrix eigenproblem remains after whitening: the complete source interaction is one scalar switch plus an orthogonal ball fiber.

For example, if `a<1<a+b` (the axial direction is tighter in the second cap), then

- `E1` controls the transverse radius for `|s| <= s_*`;
- `E2` controls it for `|s| >= s_*` until the axial endpoint.

If `a>1>a+b`, the active pieces reverse.

Dominant cases are exactly the non-crossing Loewner cases already routed to T-P5-238 and should not be re-solved here.

---

# Part II — arbitrary quadratic debit becomes a one-coordinate family of trust regions

## 3. Target block decomposition

Let

`q(z)=q0 + 2 h^T z + z^T H z`,

with symmetric `H` and arbitrary `h`.

Relative to `R u direct-sum u^perp`, write

`h = eta u + d`, with `d perpendicular u`,

and

`H = [[gamma, c^T],[c,G]]`,

where `G` acts on `u^perp`.

Then on `z=s u+w`,

`q(s,w) = q0 + 2 eta s + gamma s^2`

`           + 2 (d+s c)^T w + w^T G w`.

Define

`ell(s):=d+s c`.

For each feasible scalar `s`, the exact fiber maximum is

`Phi(s) = q0+2 eta s+gamma s^2`

`       + sup_{||w||^2 <= R^2(s)} [w^T G w + 2 ell(s)^T w]`.

Thus

**`q<=0 on E1 intersect E2` iff `Phi(s)<=0` for every feasible s.**

This is the exact source-to-Lyapunov bridge produced by the rank-one interaction.

## 4. One-scalar trust-region dual on each fiber

For a fixed `s`, put `r^2=R^2(s)`, `ell=ell(s)`. The ordinary trust-region S-lemma gives

`sup_{||w||^2<=r^2} (w^T G w+2 ell^T w)`

`= inf_{lambda>=0, lambda I-G >=0}`

`  [lambda r^2 + ell^T (lambda I-G)^dagger ell]`,

with the usual range condition `ell in range(lambda I-G)` at a singular endpoint.

In the regular boundary branch `lambda I-G>0`, the maximizing fiber point is

`w=(lambda I-G)^(-1) ell`,

and an active boundary satisfies the secular equation

`|| (lambda I-G)^(-1) ell ||^2 = r^2`.

For exact rational checking, write

`K(lambda)=lambda I-G`, `D(lambda)=det K(lambda)`, `J(lambda)=adj K(lambda)`.

Whenever `D(lambda) != 0`, the boundary equation is fraction-free:

**`ell^T J(lambda)^T J(lambda) ell - r^2 D(lambda)^2 = 0`.**

Since `G` is symmetric, `J^T=J`.

The packet must still check

- `lambda>=0`;
- `K(lambda)>=0` (strictly positive in the regular branch);
- the correct active source branch for `R^2(s)`;
- scalar feasibility of `s`.

At `D(lambda)=0`, do not divide: retain the range/kernel hard-case branch exactly as in the earlier singular-Schur machinery.

### Consequence

Rank-one source interaction really does reduce the arbitrary affine-quadratic problem to a **one-dimensional outer coordinate `s` plus a one-scalar trust-region multiplier on each fiber**. It does **not** in general collapse both scalars to one global constant multiplier.

---

# Part III — a positive exact subcase: homogeneous target, two centered caps

## 5. Lossless theorem

There is an important stronger fact which prevents over-attributing power to the rank-one assumption.

Let `A1>0`, `A2>=0` be centered source matrices and consider the homogeneous target

`z^T H z <= B`

on

`z^T A1 z <= 1`, `z^T A2 z <= 1`.

### Theorem B — `twoCenteredCaps_homogeneous_sprocedure_lossless`

The implication above holds iff there exist `lambda1,lambda2>=0` such that

**`lambda1 A1 + lambda2 A2 - H >=0`,**

and

**`lambda1+lambda2 <= B`.**

So for a homogeneous quadratic target the ordinary two-multiplier certificate is lossless for **any two centered caps**, not merely for a rank-one pair.

## 6. Elementary rank-reduction proof

Lift only the homogeneous second moment `X=zz^T`. The SDP relaxation is

maximize `tr(HX)`

subject to

`X>=0`,

`tr(A1 X)<=1`,

`tr(A2 X)<=1`.

Because `A1>0`, the feasible set is compact; a sufficiently small `epsilon I` is strictly feasible, so primal/dual SDP strong duality holds.

It remains to show the relaxation has a rank-one optimum. Take an extreme feasible `X` of rank `r`. If `r>=2`, symmetric perturbations supported on `range(X)` have dimension

`r(r+1)/2 >=3`.

At most two scalar inequalities are active. Hence there exists a nonzero supported symmetric perturbation annihilating every active trace constraint. For sufficiently small plus/minus perturbations, PSD is preserved and every inactive inequality remains strict. This writes `X` as a nontrivial midpoint of two feasible matrices, contradicting extremality.

Therefore every nonzero extreme optimum has rank one; the zero optimum is trivial. Thus the SDP value equals the original QCQP value. Its dual is exactly the two-multiplier condition above.

### Structural meaning

The affine linear term is not cosmetic. Adding a first moment requires the augmented moment matrix `[[X,x],[x^T,1]]`; the fixed bottom-right equality adds another affine constraint, allowing rank-two extreme SDP points. That is precisely where the lossless two-multiplier argument can fail.

---

# Part IV — exact rational counterexample for an affine target

## 7. Rank-one pair

Work in `R^2` with coordinates `(x,y)`.

Take

`E1: x^2+y^2 <=1`,

`E2: (17/9)x^2 + (1/2)y^2 <=1`.

The second matrix is

`A2 = (1/2) I + (25/18) e1 e1^T`,

so it differs from the scalar multiple `(1/2)I` by **rank one**.

Neither cap dominates the other because the relative eigenvalues are `17/9>1` and `1/2<1`.

The exact switch is

`a=1/2`, `b=25/18`, hence

`s_*^2=(1-a)/b=9/25`,

so `|x|=3/5`.

## 8. Safe affine-quadratic target

Define

`q(x,y) = -4xy + (74/15)x + (18/5)y - 98/25`.

Let

`p=(3/5,4/5)`.

Then

`p in boundary(E1) intersect boundary(E2)`

and

`q(p)=0`.

We now prove **exactly** that `q<=0` on `E1 intersect E2`.

### Step 1 — monotonicity in `y`

From `E2`,

`|x| <= 3/sqrt(17) < 3/4`.

The coefficient of `y` in `q` is

`c(x)=18/5-4x > 18/5-3 = 3/5 >0`.

Hence, for fixed feasible `x`, `q` is strictly increasing in `y`. It is enough to check the upper fiber boundary.

Also set

`R(x)=98/25-(74/15)x`.

Since `x<3/4`,

`R(x)>98/25-37/10 = 11/50>0`.

Thus the desired boundary inequality can be squared without changing direction.

### Step 2 — central branch `|x|<=3/5`

Here the unit circle is active:

`y_max=sqrt(1-x^2)`.

We need

`c(x)sqrt(1-x^2) <= R(x)`.

The exact squared difference factors as

`R(x)^2-c(x)^2(1-x^2)`

`= [8(5x-3)/5625] P1(x)`,

where

`P1(x)=2250x^3-2700x^2+1375x-564`.

Its derivative is

`P1'(x)=25(270x^2-216x+55)`.

The quadratic in parentheses has negative discriminant

`216^2-4*270*55 = -12744 <0`

and positive leading coefficient, so `P1'>0` on `R`.

Moreover

`P1(3/5)=-225<0`.

Therefore `P1(x)<0` for every `x<=3/5`. On `|x|<=3/5`, also `5x-3<=0`, hence the squared difference is nonnegative. Equality occurs at `x=3/5`.

### Step 3 — positive outer branch `3/5<=x<=3/sqrt(17)`

Here the second ellipse is active:

`y_max=sqrt(2-(34/9)x^2)`.

The exact squared difference is

`R(x)^2-c(x)^2[2-(34/9)x^2]`

`= [4(5x-3)/5625] P2(x)`,

where

`P2(x)=17000x^3-20400x^2-625x+4947`.

Now

`P2'(x)=25(2040x^2-1632x-25)`.

On `[3/5,3/4]`, the quadratic derivative factor is convex and is negative at both endpoints:

`2040(3/5)^2-1632(3/5)-25 = -1349/5 <0`,

`2040(3/4)^2-1632(3/4)-25 = -203/2 <0`.

Hence `P2` decreases there. Since `3/sqrt(17)<3/4`,

`P2(x) > P2(3/4)=1401/8>0`

throughout the positive outer branch. Also `5x-3>=0`, so the squared difference is nonnegative.

### Step 4 — negative outer branch `-3/sqrt(17)<=x<=-3/5`

Here again the second ellipse is active. For `x<0`,

`2040x^2-1632x-25>0`

on this interval, so `P2` is increasing. Since

`P2(-3/5)=-5694<0`,

we have `P2(x)<0` on the whole negative outer branch. There `5x-3<0`, hence the same squared difference is nonnegative.

Combining the three branches proves

**`q(x,y)<=0` for every `(x,y) in E1 intersect E2`, with equality at `p`.**

This is an exact rational proof; no sampling is used.

## 9. No constant two-multiplier S-procedure certificate exists

Write the source inequalities as

`g1=x^2+y^2-1 <=0`,

`g2=(17/9)x^2+(1/2)y^2-1 <=0`.

Suppose, for contradiction, that there exist `lambda1,lambda2>=0` such that

`r := lambda1 g1 + lambda2 g2 - q`

is globally nonnegative.

At `p`, both source constraints and the target are zero, so

`r(p)=0`.

A globally nonnegative quadratic attaining zero at an interior point of ambient `R^2` must have zero gradient there. Therefore

`lambda1 grad g1(p)+lambda2 grad g2(p)=grad q(p)`.

The exact vectors are

`grad g1(p)=(6/5,8/5)`,

`grad g2(p)=(34/15,4/5)`,

`grad q(p)=(26/15,6/5)`.

The first two vectors are linearly independent (determinant `-4/3`), so the multipliers are uniquely forced:

**`lambda1=lambda2=1/2`.**

The quadratic matrix of `r` is then

`K = (1/2)I + (1/2)A2 - Hq`,

where

`Hq=[[0,-2],[-2,0]]`.

Hence

`K=[[13/9,2],[2,3/4]]`.

But

**`det K = 13/12-4 = -35/12 <0`.**

So `K` is indefinite, impossible for a globally nonnegative quadratic with a zero. Contradiction.

Therefore the exact safe implication has **no** constant two-multiplier quadratic S-procedure certificate.

### Theorem C — `rankOneTwoCap_affineTarget_notLossless`

The data above are a fully rational counterexample showing:

> Even when one centered source matrix differs from a scalar multiple of the other by rank one, the standard constant two-multiplier S-procedure is not lossless for an arbitrary affine-quadratic target.

This closes the yes/no part of the seam left by T-P5-238.

---

# Part V — exact dispatcher and formalization boundary

## 10. Recommended mathematical routing

For two common-centered caps:

- if one cap Loewner-dominates the other, use T-P5-238: exact single-cap collapse and ordinary one-constraint S-lemma;
- else, if the target is homogeneous quadratic, use Theorem B: exact two-multiplier PSD certificate (rank-one source structure not required);
- else, if after whitening the second cap is scalar-plus-rank-one, use Theorem A plus the piecewise fiber/trust-region reduction; a constant two-multiplier miss is **inconclusive**, not FAIL;
- a true mathematical FAIL requires a primal feasible source witness with positive target debit, or another exact impossibility theorem specific to the source packet.

## 11. Fraction-free fiber packet

A rational implementation can avoid square roots in the trusted core by storing branch data as radius squares:

`r1sq(s)=1-s^2`,

`r2sq(s)=[1-(a+b)s^2]/a`,

plus the sign condition deciding the minimum. For a fixed rational/algebraic `s` and regular secular root `lambda`, use

`D=det(lambda I-G)`, `J=adj(lambda I-G)`,

and check

`ell^T J^2 ell = r^2 D^2`,

with exact PSD/sign/range conditions. Algebraic `s` or `lambda` requires root isolation or certified intervals; a decimal optimizer is not an exact witness.

## 12. Suggested theorem leaves

1. `rankOneTwoCap_exactFiber`
2. `rankOneTwoCap_switchSq`
3. `fiberTrustRegion_slemma_exact`
4. `fiberTrustRegion_fractionFree_secular`
5. `twoCenteredCaps_homogeneous_rankOneExtreme`
6. `twoCenteredCaps_homogeneous_sprocedure_lossless`
7. `rankOneAffineCounterexample_sourceSafe`
8. `rankOneAffineCounterexample_noTwoMultiplierCertificate`

The counterexample leaves are especially useful as regression guards against an unsafe dispatcher upgrade.

---

# Part VI — remaining obligations

## 13. Still open

This child does not establish:

- that the actual P5 source packet has exactly two common-centered caps;
- an actual whitening / quotient map and its same-key source identity;
- that an actual second cap is scalar-plus-rank-one after whitening;
- exact source radii/matrices rather than outer or interval surrogates;
- a concrete source-bound fiber interval or same-tube trajectory coverage;
- a deployed target block `(q0,h,H)`;
- a proof of the univariate outer inequality `Phi(s)<=0` for deployed data;
- Float64/interval semantics;
- Lean/kernel implementation;
- independent validation by 封不觉;
- admission / registry / P5-P8-M4 parent closure.

## 14. Next smallest mathematical seam

The next useful child should be source-facing rather than another generic multiplier variant:

**transport an actual physical quadratic cap pair through the existing equality quotient and whitening map, and prove an exact test for `A2-aI` having rank one in quotient coordinates without constructing floating eigenvectors.**

For rational data this can be expressed by vanishing 2x2 minors of `A2-aI` together with one nonzero entry/minor and exact positivity/crossing checks. If the actual source pair fails rank one, the correct result is an explicit structural obstruction and the dispatcher stays on the generic noncommuting branch.
