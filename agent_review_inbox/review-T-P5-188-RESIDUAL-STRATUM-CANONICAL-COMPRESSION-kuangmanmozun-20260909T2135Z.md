---
kind: review_result
review_id: review-T-P5-188-residual-stratum-canonical-compression-kuangmanmozun-20260909T2135Z
task_id: T-P5-188-RESIDUAL-STRATUM-CANONICAL-COMPRESSION
reviewer: 狂蛮魔尊
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-09T21:35:00Z
claim_commit: 8342c27184544424bf7c97a9ef207fef97db30a7
inspected_commit: 99e8191d8e78124b64e2ae88ba8febd120ddd052
upstream_commits:
  - 1b4d00d6d3c2cbcbf3c1eadc4d7a3e729b7d808e  # T-P5-187 residual uniqueness / kernel gauge
  - 4c6c4ab0ae84f7e397975e6de14e8167efcd6bfa  # T-P5-186 singular PSD active fan
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_zero_residual_stratum_exact_minimizer_characterization; add_psd_principal_kernel_lift; prune_fixed_direction_face_duplicates
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact finite-dimensional convex quadratic/KKT algebra
exit_code: no Lean/kernel run
---

# T-P5-188 — residual-stratum canonical compression

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-187 proves that for one fixed external direction all orthant KKT minimizers of the same PSD quadratic have the same residual and differ only by `ker(P)`. This review sharpens that statement into an exact description of the *entire* minimizer set.

Once one exact KKT packet `(y,r)` is known, let

`I := {i : r_i = 0}` and `J := {j : r_j > 0}`.

Then every minimizer is obtained by setting the `J` coordinates to zero and solving just one principal linear system on `I`:

`P_II x_I = -b_I`, `x_I >= 0`.

Conversely **every** nonnegative solution of that reduced system is a global orthant minimizer. No additional cross-row test is needed: PSD forces every kernel vector of the active principal block, when lifted by zeros, into the full kernel of `P`, so the `J` residual is automatically unchanged.

Thus, for a fixed external direction, overlapping active-face representatives are not separate mathematical objects. They are simply different points of one canonical affine slice on the zero-residual stratum. This can prune duplicate face packets after T-P5-185/186/187.

This does **not** claim that `I` equals the support of every minimizer, nor that one residual stratum is valid for an entire external cone. Source binding, cone/domain coverage, runtime semantics, Lean/kernel verification, independent validation, admission and registry eligibility remain open.

---

## 1. Setup

Let `P=P^T >= 0` and define

`f(x) = x^T P x + 2 b^T x`, for `x>=0`.

Assume one KKT minimizer `y>=0` is known, with

`r := P y + b >= 0`,

`y^T r = 0`.

Because `P>=0`, `f` is convex, so these KKT conditions are sufficient for global optimality.

T-P5-187 gives the additional fact that every other KKT minimizer has the same residual `r`.

Define the exact residual partition

`I = {i : r_i=0}`,

`J = {j : r_j>0}`.

Since `r>=0`, these sets partition all coordinates.

---

## 2. PSD principal-kernel lifting lemma

### Lemma T188-A

Let `S` be a coordinate subset. Let `d` be supported in `S`, and suppose

`P_SS d_S = 0`.

Then

`P d = 0`.

### Proof

Because `d` is zero off `S`,

`d^T P d = d_S^T P_SS d_S = 0`.

For a symmetric PSD matrix, zero quadratic energy implies kernel membership: `d^T P d=0 => P d=0`. Hence the lifted vector is in `ker(P)`. QED.

### Equivalent cross-row statement

In particular,

`P_SS d_S=0 => P_{S^c,S} d_S=0`.

So a principal-block kernel direction cannot secretly change the residual on omitted coordinates. This is exactly the cross-row fact needed below.

No inverse or pseudoinverse is involved.

---

## 3. Exact minimizer-set theorem

### Theorem T188-B — zero-residual affine slice

Under the setup above, the complete set of global minimizers of `f` over the nonnegative orthant is exactly

`M = { z : z_J=0, z_I>=0, P_II z_I = -b_I }`.

### Necessity

Let `z` be any minimizer. By T-P5-187 its KKT residual is the same vector `r`.

For every `j in J`, `r_j>0`. Complementarity gives

`z_j r_j=0`,

therefore `z_j=0`. Hence `z_J=0`.

On `I`, residual equality gives

`0 = r_I = (Pz+b)_I = P_II z_I + b_I`,

so

`P_II z_I = -b_I`.

Also `z_I>=0`. Thus every minimizer lies in `M`.

### Sufficiency

Conversely let `z` satisfy

`z_J=0`, `z_I>=0`, `P_II z_I=-b_I`.

The reference minimizer `y` also has `y_J=0` because `r_J>0`, and it obeys

`P_II y_I=-b_I`.

Set `d=z-y`. Then `d` is supported in `I` and

`P_II d_I=0`.

By T188-A,

`P d=0`.

Therefore

`Pz+b = Py+b = r >=0`.

On `I`, `r_I=0`; on `J`, `z_J=0`. Hence

`z^T r=0`.

So `z` satisfies the KKT conditions and, because `P>=0`, is a global minimizer. QED.

---

## 4. Affine kernel form and uniqueness criterion

Fix any one solution `y_I` of the reduced system. Then

`{x_I : P_II x_I=-b_I} = y_I + ker(P_II)`.

Hence

**`M = { (y_I+k,0_J) : k in ker(P_II), y_I+k>=0 }`.**

By T188-A every lifted `(k,0_J)` lies in `ker(P)`. Therefore the kernel gauge found in T-P5-187 is not merely necessary: it gives the complete freedom after the residual partition is fixed.

Immediate corollaries:

1. If `P_II` is positive definite, the orthant minimizer is unique.
2. If `P_II` is singular, all nonuniqueness is exactly the intersection of one affine kernel space with the orthant.
3. The reduced energy is automatically identical on this whole set because `Pk=0`.
4. Coordinates in `J` are forced zero in every minimizer.
5. Coordinates in `I` are only *eligible* to be active; some may still be zero in every feasible point of the affine slice. Thus `I` must not be mislabeled as the support.

---

## 5. Exact checker compression

For a fixed external direction, a producer that already has one exact KKT packet can canonicalize all face data as follows.

1. Verify `P=P^T>=0`.
2. Verify `y>=0` and exact `r=Py+b>=0`.
3. Verify complementarity `y^T r=0` (or coordinatewise `y_i r_i=0`).
4. Partition by exact signs into `I={r_i=0}` and `J={r_i>0}`.
5. Store only the reduced affine system `P_II x=-b_I, x>=0` plus the canonical residual `r_J`.

Any additional active-face representative for the same external direction is duplicate mathematical information. To check a proposed representative `x`, it is enough to verify

`x_J=0`, `x_I>=0`, `P_II x_I=-b_I`.

The full cross residual then agrees automatically by T188-A.

This is especially useful in singular seams where many active supports overlap: the checker need not separately compare every pair of transports once they are known to correspond to the same fixed `(P,b)` and residual stratum.

---

## 6. Fail-closed boundary: PSD is essential

The principal-kernel lifting lemma is false without PSD.

Take

`P = [[0,1],[1,0]]`.

For `S={1}`, the principal block is `[0]`, so every scalar `d_1` lies in `ker(P_SS)`. But for `d=(1,0)`,

`P d = (0,1) != 0`.

There is an even stronger optimization regression. Let

`b=(0,1)`.

On the nonnegative orthant,

`f(x_1,x_2)=2 x_2(x_1+1) >=0`.

Thus every point `(t,0)`, `t>=0`, is a global minimizer. Yet the residuals are

`P(t,0)+b = (0,t+1)`,

which depend on `t`. Hence residual uniqueness and cross-row invariance both fail although the quadratic is still nonnegative on the orthant. Ordinary copositivity of `P` is not enough; the full PSD hypothesis is material.

Therefore if `P>=0` in the ordinary PSD sense has not been established, this child is **not applicable**. Failure of the PSD gate is not by itself a proof that the parent copositivity claim fails.

---

## 7. Formalizable theorem statements

Suggested finite-dimensional statements:

- `psd_principalKernel_lift`:
  for symmetric PSD `P`, a vector supported on `S` whose `S` principal action is zero lies in `ker(P)`.

- `orthantMinimizers_eq_zeroResidualSlice`:
  given one KKT point `y` of a PSD quadratic, with residual `r`, all minimizers are exactly the nonnegative solutions of `P_II x=-b_I` on `I={r=0}`, extended by zero on `J={r>0}`.

- `orthantMinimizer_unique_of_zeroResidualPrincipal_posDef`:
  if the zero-residual principal block is positive definite, the minimizer is unique.

- `orthantMinimizer_kernelGauge_complete`:
  every two minimizers differ by a full-kernel vector supported on `I`, and every orthant-feasible such kernel displacement remains a minimizer.

All proofs use only finite sums, PSD quadratic facts, exact order/complementarity, and linear algebra. No square roots, eigenvectors, inverses or pseudoinverses are mathematically necessary.

---

## 8. What remains open

This child does not provide:

- a source-bound `(P,b)` packet;
- proof that an external cone stays in one residual sign stratum;
- coverage of all external directions;
- Float64/interval sign semantics near `r_i=0`;
- Lean/kernel compilation;
- independent verification by 封不觉;
- admission/registry or P5/P8/M4 parent closure.

The next useful mathematical child, if needed, is **residual-stratum stability under varying external direction**: derive exact inequalities that certify a cone on which `r_J(e)>0` and `r_I(e)=0` remain valid, so the canonical reduced affine system can replace a collection of face packets on an entire polyhedral cone rather than only pointwise.