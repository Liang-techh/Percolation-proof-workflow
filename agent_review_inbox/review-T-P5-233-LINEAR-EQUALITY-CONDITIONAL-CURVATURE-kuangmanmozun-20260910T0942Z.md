---
kind: review_result
review_id: review-T-P5-233-linear-equality-conditional-curvature-kuangmanmozun-20260910T0942Z
task_id: T-P5-233-LINEAR-EQUALITY-CONDITIONAL-CURVATURE
reviewer: 狂蛮魔尊
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-10T09:42:00Z
claim_commit: 45a0e8db233a743c93faa83d44af5e8ce894003f
inspected_commit: 83602745def87f6b1a14312c59dee86ab68edcc4
upstream_commits:
  - 580ac9aef688269631f738f61bb24b4a7e196625  # T-P5-232 coupled-fiber conditional Schur reduction
  - f91212c7b6b45b35e88e2a71c17b712b363c480d  # T-P5-231 anisotropic kernel-fiber scaling
  - 95fc7a17795dda55ed0f493d5588c573ef84151d  # T-P5-230 ellipsoid trust-region closure
  - 6a10ef29433a4dd050d593d8053383f4ba7fd204  # T-P5-226 higher-corank/range machinery
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_fraction_free_linear_equality_conditional_curvature; add_sharp_loewner_maximality; add_kernel_range_classifier; add_second_schur_exact_gate; preserve_centered_equality_and_relaxation_semantics
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact finite-dimensional rational quadratic algebra only; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-233 — fraction-free conditional curvature from a linear equality coupling

## 0. Verdict and seam

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-232 identified the correct object for a genuinely coupled gauge fiber: the conditional curved cost

`delta_t(z) = inf_u <u-tx,H(u-tx)>`

subject to the actual source relation between the curved coordinate `u` and the nominally flat coordinate `z`. It then showed that a quadratic lower packet

`delta_t(z) >= z^T R_N z`

feeds directly into a second Schur completion.

This child gives an exact, fraction-free producer for that packet when the source relation contains a centered linear equality

**`C (u-tx) = B z`.**

The main result is stronger than a sufficient bound: for `H>0` on the curved subspace and full-row-rank `C`, the induced matrix is the **largest possible quadratic conditional-curvature matrix in Loewner order**. Its kernel is exactly `ker(B)`, its range is exactly `range(B^T)`, and the T-P5-232 second-Schur range gate collapses to one rational linear-algebra test.

No actual P5 source relation, same-cell/tube coverage, deployed Float64 enclosure, Lean receipt, independent validation, registry mutation, admission, or parent closure is claimed.

---

## 1. Setup

Let the curved displacement be

`v := u - t x in R^r`,

and suppose the curved metric satisfies

`H = H^T > 0`.

Let

`C in Q^(m x r)`,

`B in Q^(m x p)`,

with `C` of full row rank `m`.

The exact centered coupling is

**`C v = B z`.**

The quadratic appearing after the first T-P5-232 completion is

`q_t(v,z) = t^2 a + 2 t b^T z - v^T H v`.

All matrices below can be rational when `H,C,B` are rational.

Define

`d := det(H) > 0`,

`J := adj(H)`,

so `H J = J H = d I` and `J=d H^(-1)>0`.

Define the fraction-free constraint Gram matrix

**`S_hat := C J C^T`.**

Because `C` has full row rank and `J>0`,

`S_hat > 0`.

Set

`delta := det(S_hat) > 0`,

`K := adj(S_hat) > 0`,

`G := B^T K B >= 0`,

**`R_hat := d G = d B^T K B >= 0`,**

and

**`Y := J C^T K B`.**

The actual induced curvature is

`R := R_hat / delta`.

The scaled pair `(delta,R_hat)` is preferable for an exact checker because it avoids matrix inverses and square roots entirely.

---

## 2. Exact fraction-free identity

### Theorem A — `linearEquality_fractionFreeConditionalCurvature`

For every `v,z` satisfying

`C v = B z`,

one has the exact identity

**`delta^2 v^T H v`**

**`= (delta v - Y z)^T H (delta v - Y z) + delta z^T R_hat z`.**

Consequently,

**`delta v^T H v >= z^T R_hat z`,**

or equivalently

**`v^T H v >= z^T R z`.**

Equality is attained for every `z` at

**`v_*(z) = Y z / delta`.**

### Proof

First,

`C Y = C J C^T K B = S_hat K B = delta B`.

Hence

`C v_*(z) = B z`,

so the proposed minimizer is feasible.

Also

`H Y = H J C^T K B = d C^T K B`.

Now expand the square:

`(delta v-Yz)^T H(delta v-Yz)`

`= delta^2 v^T H v - 2 delta v^T H Y z + z^T Y^T H Y z`.

Using `C v=Bz`,

`v^T H Y z`

`= d v^T C^T K B z`

`= d z^T B^T K B z`

`= d z^T G z`.

Moreover, because `C Y=delta B`,

`Y^T H Y`

`= d Y^T C^T K B`

`= d delta B^T K B`

`= delta R_hat`.

Therefore the expanded square equals

`delta^2 v^T H v - delta z^T R_hat z`,

which gives the displayed identity. Since `H>0` and `delta>0`, the inequality follows. Equality occurs exactly when `delta v=Yz`. QED.

### Interpretation

The T-P5-232 conditional distance for the equality manifold is therefore known exactly:

**`inf_{Cv=Bz} v^T H v = (1/delta) z^T R_hat z`.**

No optimization remains after the packet `(d,J,S_hat,delta,K,R_hat,Y)` has been checked.

---

## 3. The induced curvature is sharp, not merely sufficient

### Theorem B — `linearEquality_conditionalCurvature_loewnerMaximal`

Let `R_tilde=R_tilde^T` be any matrix such that

`v^T H v >= z^T R_tilde z`

for every pair satisfying `Cv=Bz`.

Then

**`R_tilde <= R_hat/delta`**

in Loewner order.

### Proof

For each `z`, insert the equality-attaining minimizer

`v_*(z)=Yz/delta`.

Theorem A gives

`v_*^T H v_* = (1/delta) z^T R_hat z`.

Hence

`z^T R_tilde z <= (1/delta) z^T R_hat z`

for every `z`, which is exactly the Loewner inequality. QED.

### Consequence

For a source fiber that is exactly the equality manifold, no stronger global quadratic conditional-curvature packet exists. If additional source constraints shrink that manifold, stronger curvature may become possible, but it must use those extra constraints explicitly.

---

## 4. Kernel and range collapse to the coupling matrix

Because `K>0` and `d>0`,

`z^T R_hat z = d (Bz)^T K (Bz)`.

Therefore

**`ker(R_hat) = ker(B)`.**

Since `R_hat` is symmetric,

**`range(R_hat) = ker(R_hat)^perp = range(B^T)`.**

This gives a particularly cheap exact pre-screen for the T-P5-232 second Schur gate:

**`b in range(R_hat)` iff `b in range(B^T)` iff `b orthogonal ker(B)`.**

The checker does not need to construct `R_hat` before deciding whether a genuinely flat forcing component survives.

### Structural meaning

The original nominally flat space is `ker(H_original)` from T-P5-232. The linear equality coupling kills exactly those kernel directions that are seen by `B`; the truly flat residual directions are precisely

**`ker(B)`.**

This is the equality-constrained realization of T-P5-232's statement that the source coupling, not the ambient semidefinite metric alone, decides the true radical.

---

## 5. Exact second-Schur closure

Assume a rational vector `y` satisfies the scaled solve

**`R_hat y = delta b`.**

This is equivalent to

`R y = b`.

### Theorem C — `linearEquality_secondSchur_upper`

For every `v,z` satisfying `Cv=Bz`,

**`q_t(v,z) <= t^2 (a + b^T y)`.**

### Proof

Theorem A gives

`v^T H v >= (1/delta) z^T R_hat z`.

Hence

`q_t(v,z)`

`<= t^2 a + 2t b^T z - (1/delta) z^T R_hat z`.

Using `R_hat y=delta b`,

`2t b^T z - (1/delta) z^T R_hat z`

`= (1/delta) [2t y^T R_hat z - z^T R_hat z]`

`= t^2 b^T y - (1/delta)(z-ty)^T R_hat(z-ty)`

`<= t^2 b^T y`.

QED.

Therefore the exact rational closure gate is

**`R_hat y = delta b` and `a + b^T y <= 0`.**

No pseudoinverse is needed.

### Exactness on the unrestricted equality manifold

If there are no additional constraints on `z`, the upper bound is attained at

`z=t y`,

`v=Yz/delta`.

Thus

**`sup_{Cv=Bz} q_t(v,z) = t^2 (a+b^T y)`**

whenever the range solve exists.

This is an exact second Schur complement, not merely an absorption inequality.

---

## 6. Flat forcing obstruction when the range solve fails

Suppose

`b notin range(B^T)`.

Then there exists

`n in ker(B)`

with

`b^T n != 0`.

On the unrestricted equality manifold choose

`v=0`, `z=s n`.

Because `Bn=0`, the equality `Cv=Bz` is satisfied. Then

`q_t(0,sn)=t^2 a+2ts b^Tn`.

Choosing the sign and magnitude of `s` gives

**`sup q_t = +infinity`**

for every fixed `t>0`.

This is a true mathematical FAIL for the unrestricted equality manifold.

However, if the actual source additionally bounds `z`, the same range failure is **not** a global FAIL: it routes back to the T-P5-229/T-P5-231 support-radius/exponent branch on the surviving flat subspace `ker(B)`.

This distinction is essential.

---

## 7. Rational regression example

Take

`H = diag(2,1)`,

`C = [1 1]`,

`B = [1 2]`.

Then

`d=2`,

`J=diag(1,2)`,

`S_hat = 3`,

`delta=3`,

`K=1`.

Hence

`R_hat = 2 [[1,2],[2,4]]`,

and

`R = (2/3) [[1,2],[2,4]]`.

The coupling is

`v_1+v_2=z_1+2z_2`.

The exact minimizing curved displacement is

`v_* = ((z_1+2z_2)/3, 2(z_1+2z_2)/3)`,

and indeed

`2v_1^2+v_2^2 >= (2/3)(z_1+2z_2)^2`

with equality at `v_*`.

The true radical is

`ker(B)=span((-2,1))`.

For

`b=(1,2)`

one may choose

`y=(3/2,0)`,

because

`R_hat y = 3 b = delta b`.

Then

`b^T y=3/2`.

If `a=-3/2`, the unrestricted equality manifold has exact worst value zero for every `t`.

This gives a small all-rational PASS/sharpness regression.

---

## 8. Counterexample: the centering cannot be dropped

The equality must be written for the displacement from the same Schur center used in the completed square.

Take the scalar case

`H=C=B=1`,

but let the actual relation be

**`v = z - t`**

rather than the centered relation `v=z`.

Consider

`q_t(v,z) = -t^2 + 2tz - v^2`.

If one incorrectly erases the affine offset and applies the centered formula `v=z`, the predicted worst value is

`sup_z (-t^2+2tz-z^2)=0`.

That would look safe.

But under the actual relation `v=z-t`,

`q_t = -z^2+4tz-2t^2`,

whose maximum occurs at `z=2t` and equals

**`2t^2 > 0`.**

Thus forgetting the offset can create a **false PASS**.

Correct routing: either prove the source equality is centered at the same `tx`, or explicitly re-center the affine relation and rederive the base/cross coefficients before applying this packet.

---

## 9. Counterexample: full-row-rank is a packet condition, not a mathematical necessity

Take

`H=I_2`,

`C=[[1,0],[0,0]]`,

`B=[[1],[0]]`.

The equality is simply

`v_1=z`.

Its exact conditional cost is

`inf (v_1^2+v_2^2)=z^2`.

However

`S_hat=C C^T=diag(1,0)`

has determinant zero, so the determinant/adjugate packet above cannot be used.

Therefore

**`delta=0` must route to row-rank compression / higher-corank machinery, not to mathematical FAIL and not to zero curvature.**

A producer may first delete dependent equality rows or provide a rational full-row-rank basis for the row space, then apply Theorem A.

---

## 10. Counterexample: an equality packet cannot be consumed on a relaxed outer relation

Take scalar

`H=C=B=1`.

For the exact equality `v=z`, the induced curvature is `z^2`.

Now replace the source statement by the relaxed relation

`|v-z| <= 1`.

The pair

`z=1`, `v=0`

is admissible, but

`v^2=0 < 1=z^2`.

Hence the equality-derived lower bound fails on the relaxation.

This matters because conditional-curvature lower bounds are PASS-oriented evidence. A producer must establish

**`F_actual subset { (v,z) : Cv=Bz }`**

before consuming this packet. An outer approximation that relaxes the equality is insufficient.

Conversely, any additional constraints that only shrink the exact equality manifold preserve the lower bound automatically.

---

## 11. Suggested exact checker packet

For a same-key source cell/tube, a minimal rational packet can be:

1. `H=H^T>0` on the curved coordinates;
2. exact centered equality `Cv=Bz`;
3. rank certificate `rank(C)=m`;
4. `d=det(H)`, `J=adj(H)` with `HJ=dI`;
5. `S_hat=CJC^T`, `delta=det(S_hat)>0`, `K=adj(S_hat)` with `S_hat K=delta I`;
6. `R_hat=d B^T K B`;
7. optional `Y=J C^T K B` for equality reconstruction;
8. second-Schur solve `R_hat y=delta b`;
9. scalar reserve `a+b^Ty<=0`.

The first seven certify the **sharp conditional curvature**. Items 8-9 certify the quadratic Lyapunov closure.

A cheap dispatcher may test `b in range(B^T)` before constructing the full packet. If that fails and the source bounds the residual `ker(B)` coordinate, route to support/exponent closure rather than declaring FAIL.

---

## 12. Lean-facing theorem decomposition

Suggested finite-dimensional leaves:

1. `linearEquality_fractionFree_identity`
   - hypotheses `H^T=H`, `H>0`, `rank C=m`, `Cv=Bz`;
   - exact identity with `adj`/`det` and the scaled square.

2. `linearEquality_conditionalCurvature_lower`
   - derive `delta * v^T H v >= z^T R_hat z`.

3. `linearEquality_conditionalCurvature_attained`
   - prove `CY=delta B` and equality at `v=Yz/delta`.

4. `linearEquality_conditionalCurvature_loewnerMaximal`
   - any other universal quadratic lower packet is bounded by `R_hat/delta`.

5. `linearEquality_inducedKernel_eq`
   - with `K>0`, prove `ker(R_hat)=ker(B)`.

6. `linearEquality_inducedRange_eq`
   - conclude `range(R_hat)=range(B^T)`.

7. `linearEquality_secondSchur_upper`
   - hypotheses `R_hat y=delta b`; conclude `q_t<=t^2(a+b^Ty)`.

8. `linearEquality_flatRangeFailure_unbounded`
   - unrestricted `z`; `b notin range(B^T)` gives an explicit ray with unbounded positive value.

No pseudoinverse theorem is required for this child.

---

## 13. Remaining obligations and next seam

This child does not prove that the actual P5 source satisfies any centered linear equality. Still open:

- same-key source extraction of `C,B,H,x`;
- proof that the equality is exact and centered at the same Schur center;
- dependent-row compression when `C` is rank deficient;
- additional inequalities and exact inner/outer semantics;
- source dilation law and trajectory/cell coverage;
- rational/interval enclosure under deployed Float64 semantics;
- actual second-Schur solve and strict reserve;
- Lean implementation and pinned compile;
- independent validation by 封不觉;
- registry/admission/parent closure.

The next smallest mathematical seam is the **rank-deficient equality packet**: replace the full-row-rank determinant `delta` by a rational row-space basis or maximal-rank principal/compound-minor construction, prove basis invariance of the induced curvature, and preserve a fraction-free certificate without silently deleting inconsistent equality rows.