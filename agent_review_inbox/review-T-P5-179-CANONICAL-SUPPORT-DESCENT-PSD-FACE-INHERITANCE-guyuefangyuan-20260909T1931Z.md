---
kind: review_result
review_id: review-T-P5-179-canonical-support-descent-psd-face-inheritance-guyuefangyuan-20260909T1931Z
task_id: T-P5-179-CANONICAL-SUPPORT-DESCENT-PSD-FACE-INHERITANCE
reviewer: 古月方源
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-09T19:31:00Z
claim_commit: 5f633f346a26edd0d5d68767f551096e34b374a3
inspected_commit: 1adc2c1495f622fe00bf0075a3c9ebb5eed1eddb
upstream_commits:
  - 953eb401979eeb1374e4e4c722a5c29588e6a498  # T-P5-178 strict flat-face critical-cone / Schur bridge
  - 7d1827e843a23ede07165af1be09ce4626bc6916  # T-P5-177 zero-loaded flat-face residual floor
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_true_support_contact_canonicalization; add_psd_parent_face_inheritance; route_boundary_T177_contacts_without_recursive_signed_support_error; reuse_T178_on_true_support
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact finite-dimensional quadratic/block algebra; exact rational symbolic regression
exit_code: 0 for exact symbolic regressions; no Lean/kernel run
---

# T-P5-179 — canonical support descent and PSD face inheritance

## 0. Verdict and seam closed

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-178 closes the second-order critical-cone seam at a zero contact whose declared active coordinates are all strictly positive. Its explicit Boundary B says that if some declared active coordinates are zero, those coordinates cannot be treated as arbitrary signed directions and the argument must descend to the true positive support.

This review closes exactly that boundary. The main conclusions are:

1. an arbitrary orthant zero contact has a **canonical active set**, namely its true positive support `S=supp_+(x_*)`; on this support, local orthant nonnegativity forces the active principal block to be ordinary PSD, forces the active gradient to vanish, and forces every inactive residual to be nonnegative;
2. after this one support canonicalization, T-P5-178 applies verbatim. No recursive ambiguity remains: zero coordinates are inactive one-sided variables, and only those with zero residual enter the second-order critical set;
3. treating a strict superset of the true support as signed-active is mathematically unsound and can reject a globally copositive matrix. An exact `2x2` counterexample is given below;
4. in the special T-P5-177 branch where the nominal zero-loaded parent block is already PSD, a boundary optimizer has stronger inherited structure: every dropped coordinate is automatically a **zero-residual critical coordinate**, its coupling to the true active block automatically annihilates the active kernel, and the corresponding generalized Schur block is PSD;
5. consequently, for a boundary optimizer of the T-P5-177 kernel polytope, the dropped zero-loaded coordinates do not need a new first-order floor or a fresh hidden-kernel range proof. They are passed directly into the T-P5-178 reduced copositivity problem with an inherited PSD principal subblock. Only genuinely external zero-residual rows can create a new range obstruction; interactions with them can still create a reduced copositivity obstruction.

The result is exact finite-dimensional algebra. It uses no inverse, pseudoinverse, eigenvector, square root, numerical tolerance, provenance/admission audit, or Lean/kernel execution.

---

## 1. Canonical support of an orthant zero contact

Let `M=M^T` be a real symmetric `n x n` matrix and

`q(x)=x^T M x`.

Let `x_* >= 0`, `x_* != 0`, and assume

`q(x_*)=0`.

Define the **true positive support**

`S := { i : (x_*)_i > 0 }`,

with complement `T`. Write

`z := (x_*)_S > 0`,

and block-decompose

`M = [[A, B^T], [B, C]]`

with respect to `S \sqcup T`.

Then

`x_* = (z,0)`.

The crucial point is that strict positivity is now true by definition. Arbitrary signed perturbations are feasible on `S` for sufficiently small magnitude, whereas perturbations on `T` are only one-sided.

---

## 2. T179-A — local orthant zero contact forces active PSD and KKT residual signs

Assume there exists a neighborhood `U` of `x_*` such that

`x>=0` and `x in U` imply `q(x)>=0`.

Then:

**(2.1)** `A z = 0`,

**(2.2)** `A >= 0`,

**(2.3)** `r := B z >= 0`.

### Proof of `Az=0`

Fix any signed active direction `u in R^S`. Since every coordinate of `z` is strictly positive, there is `eps>0` such that

`z+t u >0`

for every real `t` with `|t|<eps`.

For those `t`,

`q(z+t u,0)`

`= q(x_*) + 2t u^T A z + t^2 u^T A u`

`= 2t u^T A z + t^2 u^T A u`.

This is nonnegative for both signs of arbitrarily small `t`. A nonzero linear coefficient would have the sign of `t` on one side of zero and would dominate the quadratic term. Hence

`u^T A z =0`

for every `u`, so `Az=0`.

### Proof of `A>=0`

With `Az=0`, the same feasible identity becomes

`q(z+t u,0)=t^2 u^T A u >=0`

for every signed `u` and sufficiently small nonzero `t`. Thus

`u^T A u>=0`

for every `u`; hence `A>=0`.

### Proof of `Bz>=0`

For an inactive index `i in T`, the one-sided feasible perturbation is

`x(t)=x_*+t e_i`, `t>=0`.

Its exact energy is

`q(x(t)) = 2t (Bz)_i + t^2 C_ii`.

If `(Bz)_i<0`, sufficiently small positive `t` makes this negative. Therefore every inactive residual is nonnegative.

### Consequence

The ordinary PSD premise in T-P5-178 is not an extra assumption at a genuine local zero contact. It is forced on the **true** positive support. What is not forced is PSD on an arbitrary larger index set containing coordinates where the contact is zero.

---

## 3. T179-B — arbitrary contact reduces exactly once to T-P5-178

With `S,T,A,B,C,z,r` as above, define

`I := { i in T : r_i=0 }`,

`J := { j in T : r_j>0 }`.

Let

`B_I=B[I,S]`, `C_II=C[I,I]`.

After T179-A, all hypotheses of the strict-support theorem T-P5-178 are satisfied on the **canonical** support `S`:

`z>0`, `Az=0`, `A>=0`, `r>=0`.

Therefore local orthant nonnegativity at `x_*` is equivalent to

**(3.1)**

`u^T A u + 2 y^T B_I u + y^T C_II y >=0`

for every

`u in R^S`, `y in R_+^I`.

Equivalently, by T-P5-178, it is equivalent to the inverse-free packet

**(3.2)** `A X = B_I^T`,

**(3.3)** `H := C_II-B_I X` is copositive.

This closes T-P5-178 Boundary B without introducing a new recursive theorem family:

> **Canonicalize the support once to the strictly positive coordinates, then classify every zero coordinate by its exact inactive residual.**

A coordinate with positive residual belongs to `J` and is protected at first order. A coordinate with zero residual belongs to `I` and is genuinely second-order critical.

---

## 4. Why a declared support superset is unsound

It is tempting to keep a nominal support `S_0` that contains zero coordinates and demand PSD of `M[S_0,S_0]`. That is not a valid consequence of copositivity or local orthant nonnegativity.

Take

`M = [[0,1],[1,0]]`.

For `x1,x2>=0`,

`x^T M x = 2 x1 x2 >=0`,

so `M` is globally copositive.

At

`x_*=(1,0)`,

`q(x_*)=0`.

The true support is `S={1}`. On it,

`A=[0]>=0`,

and the inactive residual is

`r_2=1>0`.

Thus the contact is locally protected in the second coordinate by a strict first-order barrier.

But if one falsely declares `S_0={1,2}` as an all-active set, then the nominal active block is the whole matrix `M`, whose eigenvalues are `1` and `-1`; equivalently

`(1,-1) M (1,-1)^T = -2 <0`.

That negative signed direction is not feasible from `x_*`, because it moves the zero second coordinate negative. A signed-active PSD test on the support superset therefore creates a **false mathematical FAIL**.

This is why support descent is not only an optimization; it is required for correctness.

A complementary critical example is

`M=diag(0,-1)`, `x_*=(1,0)`.

Here the inactive residual is exactly zero and the second-order critical direction `e_2` has negative curvature. The true-support/T178 route correctly detects the local failure. Thus zero coordinates cannot all be dismissed either: their residual decides whether they are linearly protected or second-order critical.

---

## 5. T179-C — PSD parent block automatically gives kernel-compatible dropped rows

The T-P5-177 boundary optimizer has extra structure not present in an arbitrary contact: the nominal zero-loaded parent active block is assumed PSD.

The following block theorem is the exact mechanism.

Let

`P = [[A, B^T], [B, C]] = P^T >=0`,

where `A>=0` is allowed to be singular.

Then:

**(5.1)** `B n=0` for every `n in ker(A)`;

**(5.2)** `range(B^T) subseteq range(A)`;

so there exists `X` with

**(5.3)** `A X = B^T`.

For any such solve define

**(5.4)** `H := C-BX`.

Then

**(5.5)** `H>=0`,

and the exact completion identity holds:

**(5.6)**

`[u;y]^T P [u;y]`

`= (u+Xy)^T A (u+Xy) + y^T H y`.

### Proof of the kernel-cross condition

Take `n in ker(A)` and arbitrary `y`. Since `P>=0`, for every real `t`,

`0 <= [tn;y]^T P [tn;y]`

`= 2t y^T Bn + y^T C y`.

A nonzero coefficient `y^T Bn` could be made negative with arbitrarily large `t` of the opposite sign. Hence

`y^T Bn=0`

for every `y`, so `Bn=0`.

Because `A` is symmetric,

`range(A)=ker(A)^perp`.

Thus every column of `B^T` lies in `range(A)`, proving existence of `X`.

### Proof of Schur PSD

From `AX=B^T` and symmetry,

`BX=X^TAX`

is symmetric. Expanding the right side of (5.6) gives exactly the original block quadratic.

Now set `u=-Xy`. Since `P>=0`,

`0 <= [-Xy;y]^T P[-Xy;y] = y^T H y`

for every signed `y`, hence `H>=0`.

### Gauge invariance

If `X'` is another solve, each column of `X'-X` lies in `ker(A)`. By (5.1),

`B(X'-X)=0`.

Therefore `BX'=BX`, so `H` is intrinsic. No pseudoinverse or canonical kernel representative is needed.

This is the PSD-parent specialization of the T-P5-178 range obstruction: for rows inherited from an already PSD parent block, the range gate cannot fail.

---

## 6. T179-D — boundary zero modes of a PSD parent face

Let a PSD parent face be indexed by

`S_0 = S \sqcup U`,

and write

`A_0 = M[S_0,S_0]`

in the block form

`A_0 = [[A,B_U^T],[B_U,C_UU]] >=0`.

Suppose a normalized zero mode of the parent face has the form

`z_0=(z,0_U)`

with

`z>0`, `A_0 z_0=0`.

Then:

**(6.1)** `Az=0`;

**(6.2)** `B_U z=0`;

**(6.3)** `B_U ker(A)=0`;

**(6.4)** there exists `X_U` with `A X_U=B_U^T`;

**(6.5)** `H_UU:=C_UU-B_U X_U >=0`.

The first two statements are just the two block rows of `A_0 z_0=0`; the remaining statements are T179-C.

Interpretation:

- `S` is the true positive support;
- every dropped parent coordinate `u in U` has **exact zero residual** at the contact, so it is not a strict first-order row;
- nevertheless the entire dropped block is inherited from a PSD parent, so its hidden-kernel compatibility is automatic and its reduced self-curvature is PSD.

Thus dropped coordinates are critical but not pathological by themselves.

### No-external-critical-row corollary

If, after canonical support descent, the only zero-residual inactive coordinates are the inherited `U` rows and all other inactive rows have strict positive residual, then the T-P5-178 second-order condition is automatic: its mixed critical block is exactly the PSD parent block `A_0` (restricted to signed active `S` and one-sided `U`, a subset of all signed directions).

So no further Schur/copositivity search is needed for that contact.

### With external critical rows

If there are additional zero-residual rows `E` outside the PSD parent face, then the true T-P5-178 critical set is

`I = U \sqcup E`.

The inherited rows `U` already satisfy their range solves and give a PSD principal block in the reduced matrix. However cross-couplings between `U` and `E`, and the external rows' coupling to `ker(A)`, can still make the final reduced matrix non-copositive.

Therefore the correct statement is:

> **inherited dropped rows cannot create a new hidden-kernel obstruction on their own, but they remain part of the final reduced copositivity problem whenever external critical rows are present.**

---

## 7. T179-E — exact specialization to the T-P5-177 zero-loaded floor branch

Return to

`M_D=M_0+D L_g`,

`L_g=(g 1^T+1 g^T)/2`.

T-P5-177 fixes a nominal parent support `S_0` with

`g_{S_0}=0`

and a PSD active block

`A_0=M_0[S_0,S_0]>=0`.

The parent block is independent of `D`.

Let a T-P5-177 normalized kernel optimizer lie on the boundary of its kernel polytope:

`z_0>=0`, `A_0 z_0=0`, `1^Tz_0=1`,

but some coordinates of `z_0` vanish.

Define

`S=supp_+(z_0)`, `U=S_0\S`.

Then:

1. `z=(z_0)_S>0` and `1^Tz=1`;
2. `g_S=g_U=0`;
3. each dropped row has residual

   `M_D[u,S]z=M_0[u,S]z=0`

   for **every** `D`;
4. therefore every `u in U` is a permanently zero-weight, zero-residual critical row;
5. by T179-D, the `U` rows automatically annihilate `ker(A)`, admit exact range solves against the true active block `A`, and produce a PSD reduced `U x U` Schur block.

For external rows `i notin S_0`, T-P5-177's formula remains

`rho_i(D,z)= (R_0 z_0)_i + D g_i/2`,

because the normalization remains `1^Tz=1`.

At a candidate boundary floor, define

`E={i notin S_0 : rho_i(D,z)=0}`.

Then the exact T-P5-178 critical set at the true contact is

**(7.1)** `I=U \sqcup E`.

This gives a sharper dispatcher than the phrase “recurse to the smaller support”:

### Correct boundary packet

1. shrink once to `S=supp_+(z_0)`;
2. put all dropped zero-loaded parent indices `U` directly into the critical set;
3. mark their range compatibility as inherited from `A_0>=0` rather than asking for an unrelated new certificate;
4. add the genuinely external zero-residual rows `E`;
5. apply T-P5-178 range-solve + reduced copositivity to `I=U\sqcup E`;
6. keep all positive-residual external rows in the strict first-order set `J`.

There is no new floor LP on `U`: their floor weight is zero and their first-order residual is identically zero. Their role is purely second-order.

---

## 8. Exact PSD-inheritance regression

Take the rational parent block

`A_0 = [[ 1,-1, 1],
        [-1, 1,-1],
        [ 1,-1, 2]]`.

Its quadratic form is

**(8.1)**

`(x1-x2+x3)^2 + x3^2`,

so `A_0>=0` exactly.

Take the boundary zero mode

`z_0=(1,1,0)`.

Then

`A_0 z_0=0`.

The true support is `S={1,2}` and the dropped set is `U={3}`. The true active block is

`A=[[1,-1],[-1,1]]`,

while

`B_U=[1,-1]`, `C_UU=[2]`.

The dropped residual is

`B_U(1,1)^T=0`.

An exact range solve is

`X_U=(1/2,-1/2)^T`,

because

`A X_U=(1,-1)^T=B_U^T`.

The inherited Schur block is

`H_UU = 2 - [1,-1](1/2,-1/2)^T = 1 >=0`.

This is a nontrivial example: the dropped coordinate couples to the positive-support coordinates, but PSD of the parent face forces that coupling to lie in the active range and leaves positive reduced curvature.

---

## 9. Obstruction / failure modes locked down

### Obstruction 1 — do not demand PSD on a support superset

The matrix

`[[0,1],[1,0]]`

is globally copositive but indefinite. At `(1,0)`, its zero coordinate has a positive residual and is only one-sided feasible. Treating it as signed-active creates a false failure.

### Obstruction 2 — zero residual really is second-order critical

For

`diag(0,-1)`

at `(1,0)`, the inactive residual is zero and the one-sided second-order curvature is negative. Canonical support descent must therefore be followed by the critical-cone test; support shrinkage alone is not a PASS certificate.

### Obstruction 3 — PSD-parent inheritance is a special branch

The automatic range solve in T179-C uses PSD of the larger parent block. Without that premise, a dropped zero coordinate can couple to an active kernel in a way that is either linearly protected or second-order unstable. Do not infer inherited range compatibility merely from the fact that a coordinate is zero.

### Obstruction 4 — local contact is still not global copositivity

T179 canonicalizes one contact and closes the local boundary seam. The global P5 dispatcher still has to cover all supports/remote orthant directions. No global source/domain/admission claim follows from this review.

---

## 10. Minimal checker / source interface

For a returned zero-contact packet `x_*`:

1. construct the true support by exact sign information, not a tolerance-based “active set”;
2. verify the contact's zero coordinates are exactly zero in the mathematical packet;
3. work on `S=supp_+(x_*)` and classify every complement coordinate by the exact residual `r_i`;
4. only `r_i=0` rows enter the T-P5-178 second-order critical set;
5. in the T-P5-177 PSD-parent branch, carry a tag identifying `U=S_0\S`; their range compatibility and PSD self-Schur block follow from the parent PSD theorem and need not be rediscovered numerically;
6. external critical rows still require the ordinary T-P5-178 range-solve / copositivity packet.

For rational source data this is all exact rational linear/quadratic algebra. The only non-algebraic-looking operation, “support,” should be represented by a producer-supplied exact partition with proofs `z_i>0` on `S` and `z_i=0` off `S`, rather than a Float64 threshold.

---

## 11. Suggested Lean theorem decomposition

The highest-value leaves are small.

### `orthantZero_trueSupport_activeKernel`

Given a symmetric quadratic form, a true-support vector `z>0`, zero energy, and local/nonnegative orthant hypotheses, prove

`A z=0` and `A>=0`.

A practical formal route is first to isolate a scalar lemma saying that if

`2 t a + t^2 b >=0`

for all sufficiently small positive and negative `t`, then `a=0` and `b>=0`.

### `orthantZero_inactiveResidual_nonneg`

From one-sided nonnegativity of

`2 t r + t^2 c`

for all sufficiently small `t>=0`, prove `r>=0`.

### `psdBlock_kernel_cross_zero`

For

`P=[[A,B^T],[B,C]]>=0`, `A n=0`,

prove `B n=0`.

This is the most useful algebraic leaf and needs no matrix inverse.

### `psdBlock_rangeSolve_schurPSD`

From parent PSD, obtain a solve `AX=B^T` and prove

`C-BX>=0`

plus gauge invariance. Depending on the existing linear-algebra API, existence of `X` can be separated from the completion identity.

### `zeroLoaded_boundarySupport_droppedCritical`

From

`A_0>=0`, `A_0(z,0)=0`, `g_{S_0}=0`,

prove each dropped row has exact zero residual for all `D`, and route the corresponding block through `psdBlock_kernel_cross_zero`.

The full arbitrary-contact corollary should then reuse T-P5-178 rather than duplicating its mixed-cone proof.

---

## 12. Dependencies, open obligations, and requested next action

### Mathematical dependencies consumed

- T-P5-177: zero-loaded parent face, normalized kernel polytope, exact inactive residual floor;
- T-P5-178: strict-positive active-contact critical-cone theorem and inverse-free range-solve/Schur reduction.

### New seam closed

T-P5-178 Boundary B (`z` has zeros in the declared support) is closed by exact support canonicalization. In the T-P5-177 PSD-parent branch, dropped coordinates have additional inherited PSD structure and should not be treated as a fresh first-order floor problem.

### Still open

- global copositivity over all supports;
- actual `{M_0,g,D,z}` source identity and exact support partition;
- robust/interval sign classification when source values are not exact rationals;
- Float64/runtime semantics;
- Lean/kernel realization of the new block leaves;
- independent validation by 封不觉;
- registry/admission/parent propagation.

### Requested source/CSE action

When a T-P5-177 optimizer is returned on the boundary of `Z_{S_0}`, emit the exact partition

`S=supp_+(z)`, `U=S_0\S`,

and preserve the parent PSD witness for `A_0`. Do **not** start another rowwise floor search on `U` and do not test PSD on a larger support merely because it was nominally declared active. Pass `U` directly into the T-P5-178 critical set with inherited range compatibility, then solve only the genuinely new external critical-row obligations.

---

## 13. Final verdict

**`T-P5-179-CANONICAL-SUPPORT-DESCENT-PSD-FACE-INHERITANCE` = CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending.**

The strict-support limitation in T-P5-178 is removable without a new recursive optimization layer: every orthant zero contact has a canonical true positive support, and the T-P5-178 critical-cone theorem applies there. For boundary optimizers inherited from the T-P5-177 PSD zero-loaded parent face, the dropped coordinates are automatically exact zero-residual critical rows with kernel-compatible coupling and PSD reduced self-curvature. This is the precise bridge needed to route boundary kernel-polytope optimizers into the existing P5 dispatcher while staying fail-closed about external critical rows, global copositivity, source binding, and admission.