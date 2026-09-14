---
kind: review_result
review_id: review-T-P5-150-semidefinite-residual-polytope-closure-kuangmanmozun-20260909T1130Z
task_id: T-P5-150-SEMIDEFINITE-RESIDUAL-POLYTOPE-CLOSURE
reviewer: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-09T11:30:00Z
claim_commit: 15747b48d31fbd53431e568e887ffbe1f6c6fe63
inspected_commit: 2e288a38eaf043c222f99e5b01bfa1829f77f1ef
upstream_reviews:
  - path: agent_review_inbox/review-T-P5-148-SEMIDEFINITE-CELL-CROSS-RESIDUAL-SCHUR-CAP-honglianmozun-20260909T1059Z.md
    commit: 6daae6877be6f6d19d2263d170c21b6d090ba1e8
  - path: agent_review_inbox/review-T-P5-149-INEXACT-AUGMENTED-RANGE-SOLVE-CAP-liuguanyi-20260909T1110Z.md
    commit: 506928de79dd6f2d24cb40b29655909fd5819032
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: allow_exact_affine_residual_enclosures_over_a_finite_polytope_to_be_consumed_by_one_shared_augmented_Schur_cap_via_vertex_only_PSD_checks; classify_centered_box_robust_finiteness_by_range_compatibility_of_the_nominal_map_and_each_active_uncertainty_direction; reject_any_nonzero_width_uncertainty_that_leaks_into_kerA_even_if_its_norm_is_arbitrarily_small; prefer_range_factored_uncertainty_Q_eq_A_Xtheta_or_direct_vertex_blocks; do_not_assume_a_unique_Loewner_minimal_common_matrix_cap_in_dimension_greater_than_one
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: none; exact finite-dimensional convexity, quadratic-form, and PSD algebra only
exit_code: n/a
---

# T-P5-150 — semidefinite residual polytope closure

## 0. Narrow seam and non-overlap

T-P5-148 classifies a **fixed** augmented residual map `Q` in an uncontrolled semidefinite physical-cell direction. T-P5-149 then shows how an **inexact solve for that fixed `Q`** can be consumed exactly by a residual Schur block.

T-P5-149 explicitly leaves a different issue open: a runtime or interval producer may not expose one exact residual matrix. It may expose an exact-real **set** of possible residuals enclosing floating or interval arithmetic. In a singular `A`-metric, saying that this set is numerically small is not enough; every possible residual must avoid the uncontrolled kernel.

This review closes only that mathematical set-valued seam. It proves:

1. for an affine residual family over a finite polytope, a fixed shared Schur cap is valid on the whole polytope **iff it is valid at the vertices**;
2. a finite shared cap exists **iff every vertex residual is range-compatible with `A`**;
3. on a centered independent box, this is equivalent to range-compatibility of the nominal residual and every active uncertainty direction;
4. therefore any nonzero uncertainty width in a `ker A`-visible direction causes an infinite escape, however tiny the width;
5. if the uncertainty is range-factored as `Q(theta)=A X(theta)`, the trusted checker can use only exact vertex solves plus lower-dimensional PSD inequalities;
6. in augmented dimension greater than one there need not be a unique Loewner-minimal common robust cap, so a producer must not invent one by analogy with the fixed-`Q` theorem.

No actual runtime/source enclosure, Float64 semantics, provenance/admission audit, Lean/kernel receipt, coverage proof, registry mutation, or P5 parent closure is attempted.

---

## 1. Setup

Let

- `A=A^T >= 0` be an `n x n` real symmetric PSD matrix;
- `xi in R^p` be the augmented quotient variable used by T-P5-148, e.g. `xi=(1,m)`;
- `theta in R^k` be an uncertainty parameter;
- `P = conv{v_1,...,v_N}` be a nonempty finite polytope;
- `Q(theta)` be an affine `n x p` matrix-valued map,

`Q(theta) = Q_0 + sum_i theta_i E_i`;

- `Sigma=Sigma^T` be one **shared** `p x p` cap, independent of `theta`.

For `e in R^n`, define

**(1.1)**

`Phi_theta(e,xi) := e^T Q(theta) xi - e^T A e`.

The desired robust inequality is

**(1.2)**

`Phi_theta(e,xi) <= xi^T Sigma xi`

for every `theta in P`, every `e`, and every `xi`.

Following T-P5-148, remove fractions by defining the scaled block

**(1.3)**

`M(theta;Sigma) := [[4A,            -2 Q(theta)],`

`                   [-2 Q(theta)^T,  4 Sigma   ]]`.

For a fixed `theta`, (1.2) is exactly equivalent to

**(1.4)** `M(theta;Sigma) >= 0`,

because

`[e;xi]^T M(theta;Sigma) [e;xi]`

`= 4(e^T A e - e^T Q(theta) xi + xi^T Sigma xi)`.

The important point is that `M(theta;Sigma)` is **affine in theta**.

---

## 2. Main theorem: vertex-only robust Schur closure is exact

### Theorem A — polytope vertex reduction

Assume `P=conv{v_1,...,v_N}` and `Q` is affine. For fixed symmetric `Sigma`, the following are equivalent:

1. `Phi_theta(e,xi) <= xi^T Sigma xi` for every `theta in P`, `e`, and `xi`;
2. `M(theta;Sigma) >= 0` for every `theta in P`;
3. `M(v_j;Sigma) >= 0` for every vertex `v_j`.

### Proof

`1 <=> 2` is the exact block-quadratic identity above.

`2 => 3` is immediate because every vertex belongs to `P`.

For `3 => 2`, write any `theta in P` as

`theta = sum_j lambda_j v_j`,

with `lambda_j>=0` and `sum_j lambda_j=1`.

Affineness gives

`Q(theta)=sum_j lambda_j Q(v_j)`

and therefore

**(2.1)**

`M(theta;Sigma)=sum_j lambda_j M(v_j;Sigma)`.

The PSD cone is convex, hence the right-hand side is PSD.

So no interior interval point, midpoint, or sampled residual needs a separate mathematical check. The exact robust checker for a finite polytope consists only of the vertex block PSD gates.

### Why this is stronger than a norm envelope

The theorem retains all signed correlation inside every matrix `Q(v_j)` and inside the shared `Sigma`. It does not split affine and cross residuals, does not use an operator norm, and does not spend `A`-curvature multiple times. It is therefore a direct robust extension of the T-P5-148 block, not a Young relaxation.

---

## 3. Exact existence classification

The vertex theorem also gives a sharp answer to whether **some** finite shared cap exists.

### Theorem B — robust finite-cap existence

Assume `A=A^T>=0`. The following are equivalent:

1. there exists a finite symmetric `Sigma` satisfying (1.2) uniformly on `P`;
2. for every vertex `v_j`,

   `range(Q(v_j)) subseteq range(A)`;

3. every vertex fixed-residual problem has a finite T-P5-148 cap.

### Proof: necessity

If a shared `Sigma` exists, it works at every vertex. Fix a vertex `v_j`, any `k in ker A`, and any `xi`. Put `e=t k`. Then

`Phi_{v_j}(t k,xi)=t k^T Q(v_j) xi`.

A finite upper bound for both signs and arbitrarily large `|t|` forces

`k^T Q(v_j) xi=0`

for all `k,xi`. Hence every column of `Q(v_j)` is orthogonal to `ker A`. Since `A` is symmetric,

`(ker A)^perp = range(A)`,

so `range(Q(v_j)) subseteq range(A)`.

### Proof: sufficiency

For each vertex choose any exact range solve

**(3.1)** `A X_j = Q(v_j)`.

Define the fixed-vertex minimal cap

**(3.2)**

`S_j := (1/4) X_j^T A X_j >= 0`.

By completion of squares,

`Phi_{v_j}(e,xi)`

`= -(e-X_j xi/2)^T A(e-X_j xi/2) + xi^T S_j xi`

`<= xi^T S_j xi`.

A simple finite shared cap is

**(3.3)** `Sigma := sum_j S_j`.

Because every `S_j>=0`, we have `Sigma-S_j>=0`, so `Sigma` is a valid cap at every vertex. Theorem A then extends it to all of `P`.

This proves existence. The sum in (3.3) is only a convenient witness; it is not claimed sharp.

---

## 4. Centered box classification: every active uncertainty direction must be in range(A)

Consider the especially important exact interval form

**(4.1)**

`Q(theta) = Q_0 + sum_{i=1}^k theta_i E_i`,

with

**(4.2)** `|theta_i| <= delta_i`,

where each active width satisfies `delta_i>0`.

### Theorem C — centered-box robust finiteness

There exists a finite shared cap `Sigma` for the whole box **iff**

**(4.3)** `range(Q_0) subseteq range(A)`

and, for every active `i`,

**(4.4)** `range(E_i) subseteq range(A)`.

### Proof

If a uniform cap exists, it applies at `theta=0`; Theorem B for that point gives (4.3).

For each active coordinate, the box contains `theta=+delta_i e_i` and `theta=-delta_i e_i` with all other coordinates zero. Their residual matrices are range-valued:

`Q_0 + delta_i E_i in range(A)` columnwise,

`Q_0 - delta_i E_i in range(A)` columnwise.

Subtracting and dividing by the nonzero scalar `2 delta_i` gives (4.4).

Conversely, if (4.3)-(4.4) hold, every affine combination `Q(theta)` is columnwise in `range(A)`. In particular every vertex is range-compatible, so Theorem B gives a finite shared cap.

### Consequence

A small uncertainty width does **not** soften the range condition. For every `delta_i>0`, the condition is exactly the same: the uncertainty direction `E_i` either lies in `range(A)` or it does not.

There is no threshold below which a `ker A` component becomes harmless, because the physical null coordinate `e` is unbounded in this model.

---

## 5. Exact counterexample: arbitrarily small uncertainty can create infinite escape

Take

`A = diag(1,0)`,

`p=1`,

`Q_0 = (0,0)^T`,

`E = (0,1)^T`,

and let

`Q(t)=t E`, `|t|<=epsilon`,

for any chosen `epsilon>0`, however small.

At the endpoint `t=epsilon`, choose

`xi=1`,

`e=(0,T)^T`.

Then

`e^T A e=0`

and

**(5.1)** `Phi_epsilon(e,1)=epsilon T`.

Letting `T->+infinity` makes the residual charge unbounded. Hence no finite `Sigma` exists.

This is not a bad constant and not an insufficiently large interval budget. The obstruction is qualitative: the uncertainty direction itself is visible to `ker A`.

It follows that a source packet such as

`||Q-Q_nom||_F <= 10^{-30}`

still proves nothing useful in this semidefinite lane unless the entire allowed perturbation set is range-compatible.

---

## 6. Strong corollary for componentwise interval arithmetic

Suppose an interval producer encloses the residual by independent entrywise errors

**(6.1)**

`Q = Q_0 + Delta`,

`|Delta_{ab}| <= eps_{ab}`.

Every positive-width entry `eps_{ab}>0` activates the elementary matrix uncertainty direction

`E^{ab} = e_a e_b^T`.

Its range is `span{e_a}`. Therefore Theorem C implies:

### Corollary D — active rows of an independent interval box

For every row index `a` that has at least one positive-width entry `eps_{ab}>0`, robust finiteness requires

**(6.2)** `e_a in range(A)`.

In particular, if **every row** of `Q` contains at least one independently uncertain entry, then robust finiteness requires

`range(A)=R^n`.

For symmetric PSD `A`, this means

**(6.3)** `A>0` is actually positive definite.

So a generic full componentwise interval box is fundamentally incompatible with a genuinely singular `A`-block. Shrinking all widths does not fix it.

### Practical mathematical repair

The uncertainty must instead be structurally range-preserving, for example

**(6.4)** `Q(theta)=A X(theta)`

for an exact affine enclosure `X(theta)`, or more generally every uncertainty generator `E_i` must come with an exact range witness `A Y_i=E_i`.

This distinction should be enforced before any numerical tolerance is converted into a T-P5-148/T-P5-149 cap.

---

## 7. Range-factored root-free checker

Assume the producer supplies an affine solve family

**(7.1)**

`X(theta)=X_0 + sum_i theta_i Y_i`

with exact identity

**(7.2)** `A X(theta)=Q(theta)`

throughout the polytope. It is enough to provide the identities

`A X_0=Q_0`,

`A Y_i=E_i`.

At a vertex `v_j`, write `X_j=X(v_j)`.

### Theorem E — lower-dimensional vertex checker

A fixed symmetric `Sigma` is a uniform cap on `P` iff, at every vertex,

**(7.3)**

`4 Sigma - X_j^T A X_j >= 0`.

### Proof

At each vertex, completion of squares gives

`Phi_{v_j}(e,xi)`

`= -(e-X_j xi/2)^T A(e-X_j xi/2)`

`  + (1/4) xi^T X_j^T A X_j xi`.

Thus the vertex cap is equivalent to (7.3). Theorem A then supplies the whole polytope.

### Checker significance

The source may choose either of two exact rational interfaces:

- **direct block form:** for every vertex, check

  `[[4A,-2Q_j],[-2Q_j^T,4Sigma]] >= 0`;

- **range-factored form:** check `A X_j=Q_j` and

  `4Sigma-X_j^T A X_j >=0`.

Both are root-free. Neither requires an inverse, pseudoinverse, eigenbasis, square root, spectral norm, or Young parameter.

If a vertex solve is itself only approximate, T-P5-149 can be applied **at that vertex**. That is a downstream composition, not repeated here.

---

## 8. Scalar augmented coordinate: exact robust minimum

When `p=1`, the Loewner order becomes the ordinary scalar order, so the robust common cap has a genuine exact minimum.

Suppose every vertex is range-compatible and choose `A x_j=q_j`, where `q_j=Q(v_j)` is now a vector. Then the fixed-vertex minimal scalar cap is

**(8.1)**

`s_j = (1/4) q_j^T x_j = (1/4) x_j^T A x_j`.

The exact robust minimum is

**(8.2)**

`sigma_min = max_j s_j`.

This follows immediately from Theorem A and the fixed-vertex sharpness.

### Exact regression

Take

`A=diag(2,0)`,

`Q(t)=((1+t),0)^T`,

`-1/2 <= t <= 1/2`.

Then an exact solve is

`x(t)=((1+t)/2,0)^T`,

so

`s(t)=(1+t)^2/8`.

The endpoint values are

`s(-1/2)=1/32`,

`s(1/2)=9/32`.

Hence the exact robust cap is

**(8.3)** `sigma_min=9/32`.

At `t=1/2`, `x=(3/4,0)` and the completion-square equality point `e=x/2=(3/8,0)` attains `Phi=9/32`. Thus the endpoint cap is genuinely sharp.

---

## 9. Matrix augmented coordinate: do not assume a unique Loewner-minimal robust cap

For a fixed residual `Q`, T-P5-148 has a unique Loewner-minimal cap. This property does **not** automatically survive robustification over several residuals.

The Loewner order on symmetric matrices is not a lattice.

### Exact two-vertex example

Take

`A=I_2`, `p=2`,

`Q_1=2 diag(1,0)`,

`Q_2=2 diag(0,1)`.

The two fixed-vertex minimal caps are

`S_1=diag(1,0)`,

`S_2=diag(0,1)`.

One common upper bound is

**(9.1)** `U_1=I_2`.

Another is

**(9.2)**

`U_2=[[5/4,1/2],[1/2,5/4]]`.

Indeed,

`U_2-S_1=[[1/4,1/2],[1/2,5/4]]`

and

`U_2-S_2=[[5/4,1/2],[1/2,1/4]]`

both have positive diagonal entries and determinant `1/16`, hence are PSD.

But

`U_2-U_1=[[1/4,1/2],[1/2,1/4]]`

has determinant `-3/16`, so it is indefinite; likewise `U_1-U_2` is indefinite.

Suppose a least common Loewner upper bound `L` existed. Because `U_1` is a common upper bound, `L<=I_2`. But `L>=S_1,S_2`. The diagonal constraints force `L_11=L_22=1`; PSD of `I_2-L` with zero diagonal then forces the off-diagonal entry to vanish, so `L=I_2`. Yet `I_2` is not `<=U_2`, contradiction.

Therefore no least common upper bound exists.

### Consequence

For `p>1`, the phrase “the Loewner-minimal robust `Sigma`” is generally ill-defined. A source may:

- provide any shared `Sigma` passing the exact vertex gates;
- optimize a chosen scalar objective such as trace or a downstream directional budget;
- preserve parameter-dependent caps if the downstream theorem supports them.

But it should not manufacture a canonical matrix minimum by summing, taking entrywise maxima, or copying the fixed-residual theorem.

---

## 10. Why checking only a nominal residual is unsound

Suppose `Q_0` is perfectly range-compatible and even has an exact solve. If an interval wrapper subsequently adds an uncertainty direction `E` with a `ker A` component, the family is no longer finitely controllable.

Thus the sequence

1. certify the nominal `Q_0`;
2. compute a small floating error norm;
3. add a scalar safety margin to `Sigma`

is invalid in a singular physical-cell direction unless step 2 also proves the **geometry** of the uncertainty set.

An additive scalar margin cannot control a linear escape in an unpenalized null direction.

The correct order is:

1. reify the exact uncertainty set;
2. prove it is range-preserving, or directly pass the vertex Schur blocks;
3. only then optimize the finite cap.

---

## 11. Formalizable theorem statements

The following leaves are suitable for Lean or an exact checker once the matrix API is chosen.

### Leaf A — affine block interpolation

Assumptions:

- `lambda_j>=0`, `sum_j lambda_j=1`;
- `Q=sum_j lambda_j Q_j`;
- for one symmetric `Sigma`, every

  `[[4A,-2Q_j],[-2Q_j^T,4Sigma]] >=0`.

Conclusion:

`[[4A,-2Q],[-2Q^T,4Sigma]] >=0`.

Proof: exact matrix convex combination.

### Leaf B — polytope robust cap

Assumptions:

- `theta in conv{v_1,...,v_N}`;
- `Q` affine;
- all vertex blocks with the same `Sigma` are PSD.

Conclusion:

`e^T Q(theta) xi-e^T A e <= xi^T Sigma xi`

for every `e,xi`.

### Leaf C — box range obstruction

Assumptions:

- `A=A^T>=0`;
- `Q(theta)=Q_0+sum theta_i E_i`;
- `|theta_i|<=delta_i`, with `delta_i>0` for active indices;
- a finite uniform cap exists.

Conclusion:

`range(Q_0) subseteq range(A)` and

`range(E_i) subseteq range(A)` for every active `i`.

### Leaf D — box sufficiency

Assumptions:

- `A=A^T>=0`;
- `range(Q_0) subseteq range(A)`;
- `range(E_i) subseteq range(A)` for all active directions.

Conclusion:

there exists a finite shared symmetric `Sigma` for the whole box.

A constructive proof uses exact vertex solves and the finite sum of their fixed-vertex minimal caps.

### Leaf E — range-factored vertex cap

Assumptions at every vertex `j`:

- `A=A^T>=0`;
- `A X_j=Q_j`;
- `4Sigma-X_j^T A X_j>=0`.

Conclusion:

one shared `Sigma` caps every residual in the convex hull of the `Q_j` generated by the affine polytope family.

---

## 12. Failure branches that must stay fail-closed

1. **Nonzero-width kernel leakage.** If an active uncertainty generator has a component outside `range(A)`, no finite cap exists, independent of how small its coefficient interval is.

2. **Unstructured full entrywise interval with singular `A`.** If every residual row has independent positive-width uncertainty, uniform finiteness forces `A>0`; a genuinely singular `A` cannot accept such a box.

3. **Vertex-specific caps mistaken for one shared cap.** Having `Sigma_j` at each vertex does not by itself mean any one `Sigma_j` works globally. A common Loewner upper bound must be supplied; `sum_j Sigma_j` is a safe existence witness when the `Sigma_j` are PSD, but may be loose.

4. **Invented Loewner minimum.** In matrix dimension `p>1`, a least common robust cap need not exist.

5. **Sampling instead of a polytope proof.** Vertex exactness applies only after the actual uncertainty set is proven to lie in the declared convex polytope and `Q(theta)` is affine on that set.

6. **Varying `A`.** The theorem keeps the same semidefinite matrix `A` across the uncertainty set. If `A` itself varies, the block is no longer the same fixed-nullspace problem and a separate theorem is needed.

---

## 13. Dependencies and open boundaries

Still open after this child:

- actual same-key residual uncertainty set from the deployed/source packet;
- proof that the exact-real enclosure is affine/polyhedral rather than merely a collection of sampled floats;
- exact identities tying the uncertainty generators to the same `A` used by T-P5-144/148;
- any runtime rounding model, parser semantics, directed rounding, or Float64-to-real enclosure proof;
- actual quotient `G_M`, radius, and downstream multiplier/reset packet;
- cell/tube/path/reference-halo coverage;
- Lean/kernel formalization and independent validation by 封不觉;
- provenance/admission/registry/P5 parent closure.

This review supplies the mathematical consumer that a future exact-real interval/reification layer may target; it does not prove that the current runtime already produces such a packet.

---

## 14. Requested handoff

The shortest useful robust source packet is now one of the following.

### Direct polytope packet

`(cellKey, resetKey, A, {Q_j}_{j=1}^N, Sigma4)`

with exact proof that the actual residual family lies in the affine convex hull of the `Q_j`, and vertex certificates

`[[4A,-2Q_j],[-2Q_j^T,Sigma4]] >=0`

for every `j`.

### Range-factored packet

`(cellKey, resetKey, A, Q_0, {E_i}, X_0, {Y_i}, {delta_i}, Sigma4)`

with exact identities

`A X_0=Q_0`,

`A Y_i=E_i`,

and at each box vertex `v`,

`Sigma4-X(v)^T A X(v) >=0`.

If the actual interval producer instead exposes a generic componentwise box that has any active kernel-visible direction, the correct result is an explicit infinite-escape obstruction, not a larger tolerance or additive reset budget.
