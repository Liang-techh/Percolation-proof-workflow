---
kind: review_result
review_id: review-T-P5-249-rectangular-affine-image-slemma-kuangmanmozun-20260910T1336Z
task_id: T-P5-249-RECTANGULAR-AFFINE-IMAGE-SLEMMA
reviewer: 狂蛮魔尊
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-10T13:36:00Z
claim_commit: 733621dc2ac02cb87baba0a0ec00520179d32bec
inspected_commit: 5ccb74d88233672e4756368de70b9fe79a6833a4
upstream_commits:
  - a25de2d6e01b16133af9dc40d46efcfef6731ef8  # T-P5-247 affine GL(n) chart covariance
  - f01ba94dd82e9c4d1749f010e1a5fa6f1a6a1d8f  # T-P5-248 nonlinear-chart defect reserve, disjoint branch
  - f4457fd93d95b1ed58c5ec4f3fbb995a2f73fb9a  # T-P5-246 joint shifted source-target S-lemma
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_affine_image_source_completion; add_rectangular_image_slemma; add_lossless_equality_multiplier_lift; add_scalar_normal_penalty_range_gate; add_effective_radius_fraction_free_classifier; preserve_empty_point_rankdeficient_and_source_binding_boundaries
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact quadratic completion; one-constraint S-lemma on full-column-rank image coordinates; block-congruence/equality-multiplier algebra; generalized Schur complement; exact rational counterexamples; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-249 — Rectangular affine-image S-lemma and exact equality-multiplier lifting

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-247 closes the bijective `GL(n)` chart case and explicitly leaves the non-surjective image branch separate. T-P5-248 is concurrently about nonlinear chart defects. This child closes the smallest disjoint linear-image seam:

`y = P z + h`, with `P in R^{n x m}`, `rank(P)=m<=n`.

The main conclusions are:

1. a physical ellipsoid restricted to the affine image has an exact lower-dimensional ellipsoid description, including the case where the ambient ellipsoid center is not on the image;
2. safety of a quadratic target on that image is losslessly characterized by a one-constraint S-lemma in `z` whenever the effective image radius is positive;
3. the pulled-back PSD certificate is equivalent to an **ambient PSD certificate with unrestricted linear equality multipliers**;
4. replacing the equality multiplier by a single scalar penalty `tau C^T C` is not lossless at semidefinite contact. Its exact obstruction is the usual Schur range condition;
5. therefore failure of a scalar normal penalty must never be reported as failure of image-restricted safety.

No actual P5 image/source packet, tube/cell coverage, Float64 semantics, Lean/kernel receipt, independent validation, admission, registry mutation, or P5/P8/M4 parent closure is claimed.

---

# Part I — exact source restriction to a rectangular affine image

## 1. Data

Let

`P in R^{n x m}`, `rank(P)=m`,

`h,c in R^n`, `M=M^T>0`, `R>=0`.

The physical affine image is

`A = { y : y=Pz+h for some z in R^m }`,

and the ambient source ellipsoid is

`E = { y : (y-c)^T M (y-c) <= R }`.

Set

`d := c-h`,

`K := P^T M P`,

`b := P^T M d`.

Because `P` has full column rank and `M>0`,

**`K>0`.**

Define

`k := K^{-1} b`,

and

`delta := d^T M d - b^T K^{-1} b`.

Then direct completion of squares gives

**Theorem 1 — `affineImage_sourceCompletion`.**

For every `z`,

`(Pz-d)^T M (Pz-d)`

`= (z-k)^T K (z-k) + delta`.

Moreover

**`delta >= 0`**, because it is the minimum over `z` of the nonnegative quadratic `(Pz-d)^T M(Pz-d)`.

Thus the image intersection is governed by the **effective radius**

`R_eff := R-delta`.

Exactly:

`y=Pz+h in E`

iff

`(z-k)^T K(z-k) <= R_eff`.

This strictly generalizes the center-compatible branch in T-P5-247. If `c=Pk+h`, then `d=Pk`, `b=Kk`, `delta=0`, so `R_eff=R`.

---

## 2. Fraction-free radius classifier

For rational data, the branch `R_eff >,=,< 0` can be decided without constructing a floating inverse.

Let

`kap := det(K) > 0`,

`J := adj(K)`.

Then `K^{-1}=J/kap`, and define

`delta_hat := kap*d^T M d - b^T J b`,

`R_hat := kap*R-delta_hat`

`       = kap*(R-d^T M d)+b^T J b`.

Since

`delta = delta_hat/kap`,

`R_eff = R_hat/kap`,

and `kap>0`, we have the exact sign equivalence

**`sign(R_eff)=sign(R_hat)`.**

Also `delta_hat>=0`.

This gives a clean rational dispatcher:

- `R_hat<0`: image/source intersection empty;
- `R_hat=0`: one image point;
- `R_hat>0`: positive-radius image ellipsoid and strict Slater in image coordinates.

An empty image intersection may make an implication vacuous, but it is **not** domain coverage evidence.

---

# Part II — target pullback and exact image S-lemma

## 3. Quadratic target

Let

`q(y)=A+2 l^T y+y^T G y`, `G=G^T`.

Under `y=Pz+h`, define

`G_z := P^T G P`,

`l_z := P^T(l+Gh)`,

`A_z := A+2l^Th+h^TGh`.

Then

`q(Pz+h)=A_z+2l_z^Tz+z^TG_z z`.

Recenter at the image-source center `k` by `w=z-k`. Define

`l_k := l_z+G_z k`,

`A_k := A_z+2l_z^T k+k^TG_z k`.

Hence

`q(P(k+w)+h)=A_k+2l_k^T w+w^TG_z w`.

---

## 4. Positive-radius branch

Assume `R_eff>0`. The reduced source is

`w^T K w <= R_eff`, with `K>0`,

so `w=0` is a strict Slater point.

For `mu>=0`, define

`S_img(mu) :=`

`[[ mu K-G_z,      -l_k ],`

` [ -l_k^T,  -A_k-mu R_eff ]]`.

Then the ordinary one-constraint lossless S-lemma gives:

**Theorem 2 — `quadraticSafety_onAffineImage_iff`.**

If `R_eff>0`, the following are equivalent:

1. `q(y)<=0` for every `y in A intersect E`;
2. there exists `mu>=0` such that `S_img(mu)>=0`.

This is exact image safety. No ambient unsafe direction is tested.

### Degenerate branches

If `R_eff=0`, then `A intersect E` is the single point

`y_* = Pk+h`,

and the exact test is simply

**`q(y_*)<=0`.**

The strict-Slater S-lemma branch must not be invoked.

If `R_eff<0`, the intersection is empty. A checker may record vacuous image safety, but a physical coverage consumer must reject the packet unless emptiness is intended.

---

# Part III — relation to the ambient S-lemma block

## 5. Rectangular augmented chart

Define the ambient shifted-source S-lemma block

`S_y(mu) :=`

`[[ mu M-G,                 -l-mu M c ],`

` [ (-l-mu M c)^T, -A-mu R+mu c^T M c ]]`.

Let

`H := [[P,h],[0,1]]`,

an `(n+1) x (m+1)` full-column-rank matrix.

For every `mu`, direct substitution gives the rectangular congruence

**`H^T S_y(mu) H = S_z(mu)`,**

where `S_z(mu)` is the unrecentered `z`-coordinate block. The translation `z=k+w` is invertible, so

`S_z(mu)>=0 <=> S_img(mu)>=0`.

Unlike T-P5-247, `H` is not invertible. Therefore

`S_y(mu)>=0 => H^T S_y(mu)H>=0`

but the converse generally fails. That failure is correct: `S_y` tests directions outside the physical image.

---

## 6. Exact counterexample: image safe, ambient unsafe

Take

`n=2`, `m=1`, `P=e1`, `h=c=0`, `M=I_2`, `R=1`,

and

`q(y1,y2) = -1/4 + y2^2`.

On the image `y2=0`,

`q=-1/4<0`

for every `|y1|<=1`, so image safety is strict.

The reduced block at `mu=1/8` is

`S_img(1/8)=diag(1/8,1/8)>0`.

But the ambient block is

`S_y(mu)=diag(mu, mu-1, 1/4-mu)`.

Ambient PSD would require simultaneously

`mu>=1` and `mu<=1/4`,

which is impossible.

Therefore a non-surjective chart must not require ambient PSD without equality multipliers.

---

# Part IV — lossless ambient lifting with equality multipliers

## 7. Affine image as homogeneous linear equalities

Choose a full-row-rank matrix `Aeq in R^{r x n}`, `r=n-m`, such that

`ker(Aeq)=range(P)`.

The affine image `y=Pz+h` is equivalent to

`Aeq(y-h)=0`.

In augmented coordinates `xi=[y;1]`, define

`C := [Aeq, -Aeq h]`.

Then

`C H=0`,

and dimension counting gives

**`ker(C)=range(H)`.**

---

## 8. Projection/equality-multiplier lemma

Let `S=S^T in R^{N x N}`, let `C in R^{r x N}` have full row rank, and let columns of `H` form a basis of `ker(C)`.

Then:

**Theorem 3 — `restrictedPSD_iff_freeEqualityMultiplier`.**

The following are equivalent:

1. `H^T S H >= 0`;
2. there exists `Y in R^{r x N}` such that

   **`S + C^T Y + Y^T C >= 0`.**

### Constructive proof

Choose a right inverse `R_C` with `C R_C=I_r` and set

`T=[H,R_C]`.

Then `T` is invertible and

`C T=[0,I_r]`.

Write

`T^T S T = [[K0,B],[B^T,D]]`.

The restriction hypothesis is precisely `K0>=0`.

Let

`Y' := [-B^T, -D/2]`.

Since `T` is invertible, choose `Y` with `Y T=Y'`. Then

`T^T(S+C^TY+Y^TC)T`

`= [[K0,B],[B^T,D]]`

`  + [[0,-B],[-B^T,-D]]`

`= [[K0,0],[0,0]] >=0`.

The converse is immediate because `C H=0`.

Thus unrestricted linear equality multipliers are **lossless even at semidefinite contact**.

For rational `S,C,H`, a rational pivot right inverse and rational `T^{-1}` give a rational `Y`; no spectral decomposition is mathematically required.

---

## 9. Image S-lemma as an ambient certificate

Apply Theorem 3 to `S=S_y(mu)` and the affine-image constraint matrix `C`.

For `R_eff>0`, Theorem 2 becomes:

**Theorem 4 — `affineImageSafety_ambientEqualityCertificate_iff`.**

`q<=0` on `A intersect E`

iff there exist `mu>=0` and a free equality multiplier matrix `Y` such that

**`S_y(mu)+C^TY+Y^TC >=0`.**

This is the exact ambient representation of the rectangular-image S-lemma.

It cleanly separates:

- source inequality multiplier: the scalar `mu>=0`;
- affine-image equalities: unrestricted linear multiplier `Y`.

Do not force the equality part into an additional nonnegative S-procedure scalar.

---

# Part V — why a single scalar normal penalty is not lossless

## 10. Scalar penalty branch

A tempting restricted ansatz is

`S + tau C^T C >=0`, `tau>=0`.

In the same coordinates `T=[H,R_C]`, since `CT=[0,I]`, write again

`T^T S T=[[K0,B],[B^T,D]]`.

Then

`T^T(S+tau C^TC)T`

`=[[K0,B],[B^T,D+tau I]]`.

The generalized Schur complement gives the exact classifier:

**Theorem 5 — `scalarNormalPenalty_exists_iff`.**

Assume `K0>=0`. A finite scalar `tau` exists iff

**`range(B) subset range(K0)`.**

Equivalently,

`ker(K0) subset ker(B^T)`.

When this range condition holds, choose any `X` solving

`K0 X=B`.

Then a given `tau` works iff

**`D+tau I-B^T X >=0`.**

The matrix `B^T X` is symmetric and independent of the chosen solution modulo the nullspace.

If `K0>0`, the range gate is automatic and

`X=K0^{-1}B`.

The sharp threshold is

**`tau_min = max(0, lambda_max(B^T K0^{-1}B-D))`.**

Thus strict restricted PSD guarantees some scalar normal penalty, but semidefinite restricted PSD does not.

---

## 11. Sharp semidefinite counterexample

Take the abstract homogeneous packet

`S=[[0,1],[1,0]]`,

`C=[0,1]`,

so `ker(C)=span(e1)`.

The restriction is

`e1^T S e1=0`,

hence image/subspace PSD holds.

But for every scalar `tau`,

`S+tau C^TC=[[0,1],[1,tau]]`

has determinant

**`-1`**, hence is never PSD.

The range obstruction is exact: `K0=0`, `B=1`, so `range(B)` is not contained in `range(K0)`.

By contrast the free equality multiplier

`Y=[-1,0]`

gives

`S+C^TY+Y^TC=0`.

Therefore:

**failure of the scalar penalty is not failure of the image theorem.**

Suggested fail-closed label:

`SCALAR_NORMAL_PENALTY_RANGE_OBSTRUCTION__FREE_EQUALITY_MULTIPLIER_STILL_AVAILABLE`.

---

# Part VI — useful exact regressions and corollaries

## 12. Center not on the image

Let

`P=(1,0)^T`, `h=0`, `M=diag(2,3)`,

`c=(1/2,1/3)^T`, `R=1`.

Then

`K=2`, `b=1`, `k=1/2`,

`d^TMd=5/6`,

and

`delta=5/6-1/2=1/3`.

Hence

**`R_eff=2/3`.**

Directly on the image `y=(z,0)`,

`(y-c)^TM(y-c)=2(z-1/2)^2+1/3`,

so the source condition is exactly

`2(z-1/2)^2<=2/3`.

For the fraction-free classifier, `kap=2`, `J=1`, and

`R_hat=kap R_eff=4/3>0`.

This confirms that an off-image ambient center consumes source radius by the exact squared `M`-distance to the image.

---

## 13. Strict-image branch can use scalar penalty

If a chosen `mu` yields

`H^T S_y(mu)H >0`,

then `K0>0`, hence the scalar penalty range gate is automatic. A sufficiently large `tau C^TC` produces an ambient PSD packet.

So the practical distinction appears exactly at image contact/degeneracy:

- strict image certificate: scalar penalty is complete;
- semidefinite image certificate: scalar penalty needs the range gate;
- free equality multiplier: complete in both cases.

This is the same structural phenomenon seen in earlier Schur/kernel children: cross terms against a zero-energy tangent direction cannot be repaired by adding curvature only in the normal block.

---

# Part VII — formalization-friendly theorem leaves

## 14. Suggested theorem statements

1. `affineImage_source_completion`
   - hypotheses: `M>0`, `rank P=m`;
   - conclusion: exact completion and `delta>=0`.

2. `affineImage_effectiveRadius_adjugate`
   - `kap=det(P^TMP)>0`, `J=adj(...)`;
   - `kap*R_eff = kap*(R-d^TMd)+b^T J b`;
   - exact sign branch.

3. `quadraticTarget_rectangularPullback`
   - exact formulas for `A_z,l_z,G_z`.

4. `affineImage_slemma_iff`
   - positive effective radius;
   - image safety iff reduced PSD block for some `mu>=0`.

5. `restrictedPSD_iff_freeEqualityMultiplier`
   - finite-dimensional symmetric matrix statement independent of P5.

6. `affineImage_slemma_ambientEquality_iff`
   - combine 4 and 5 with augmented affine constraints.

7. `scalarNormalPenalty_exists_iff_range`
   - generalized Schur complement with `K0>=0`.

8. `scalarNormalPenalty_strict_threshold`
   - `K0>0`, threshold `lambda_max(B^TK0^{-1}B-D)`.

9. `scalarPenaltyFailure_notRestrictedFailure`
   - small exact regression/counterexample.

Recommended order: formalize the pure linear-algebra equality-multiplier theorem first; source/coverage adapters remain outside.

---

# Part VIII — boundaries

## 15. Rank-deficient P

If `rank(P)<m`, then `P^TMP` is singular. The source pullback is a cylinder/gauge problem, not the full-column-rank image theorem above. One must quotient the parameter nullspace or use the earlier gauge/fiber machinery.

Suggested label:

`CHART_PARAMETERIZATION_NOT_INJECTIVE__QUOTIENT_GAUGE_REQUIRED`.

## 16. Equality packet must be exact

The free-multiplier lift assumes exact affine equalities `C[y;1]=0`. If the physical graph only satisfies `||C[y;1]||<=eta`, the equality term no longer vanishes and must be charged as a genuine defect. Do not reuse the exact image theorem for a thick tube.

## 17. Empty image/source intersection

`R_eff<0` proves only that the declared image misses the declared source ellipsoid. It must not be converted into trajectory/domain coverage or physical PASS.

## 18. Ambient PSD remains stronger

If an ambient certificate exists, it is reusable beyond the image. The equality-multiplier certificate proves only the intended image-restricted statement. Downstream consumers must preserve that domain tag.

---

# Part IX — structural fingerprint and next seam

## 19. Fingerprint

`full-column-rank rectangular affine embedding`

`-> exact M-orthogonal source projection`

`-> effective image radius`

`-> reduced one-constraint S-lemma`

`-> rectangular certificate restriction`

`-> lossless free equality-multiplier lift`

`-> scalar normal penalty only after Schur range gate`.

This is an **image/equality mechanism**, distinct from T-P5-248's nonlinear-defect mechanism and from rank-deficient quotient/gauge transport.

## 20. Next genuinely distinct mathematical seam

The smallest remaining extension is a **thick affine-image tube**:

`||C[y;1]||_W <= eta`

instead of exact `C[y;1]=0`.

The free equality multiplier is then no longer free because its term does not vanish. A useful next child would optimize the equality multiplier against the tube norm and the existing metric-relative certificate reserve, deriving an exact Schur/support-function debit rather than replacing the tube by a coarse Euclidean ball.

That seam should remain separate from T-P5-248 unless an actual source packet couples the nonlinear chart defect and the normal-tube error.

---

## 21. Non-claims

This review does not establish:

- an actual deployed rectangular P5 chart;
- source identity of `P,h,c,M,R`;
- an actual affine-image equality packet `C`;
- tube/cell/trajectory/FD-halo coverage;
- Float64/interval semantics;
- a Lean/kernel receipt;
- independent verification by 封不觉;
- admission/registry eligibility;
- P5/P8/M4 parent closure.

Status remains **CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding**.
