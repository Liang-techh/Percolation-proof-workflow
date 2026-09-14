---
kind: review_result
task_id: T-P5-157
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_utc: 2026-09-09T13:32:00Z
parent_context:
  - T-P5-154
  - T-P5-155
related_nonoverlap:
  - T-P5-156
---

# T-P5-157 — FOUR-VERTEX-FACE-KKT-COPOSITIVITY-CLOSURE

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

For a fixed candidate additive floor `D`, T-P5-154 reduces the full simplex obligation to copositivity of one exact rational symmetric matrix `M_D`. T-P5-155 supplies an exact three-vertex face checker. This child closes the next smallest dimension:

> **For a 4×4 symmetric rational matrix, once all four 3×3 principal faces are certified copositive, the only remaining failure mode is an interior KKT point. That failure mode is exact rational linear feasibility.**

Thus fixed-`D`, four-vertex copositivity needs no quartic root formula, square root, inverse, spectral decomposition, or nonlinear optimization in the trusted statement.

This does **not** optimize over `D`, does not bind actual source data, and does not replace T-P5-156's separate weighted-slack/refinement sufficient lane.

---

## 1. Setup

Let

`M ∈ Q^{4×4}`, `M = M^T`,

and let

`Δ_4 := { λ ∈ R^4 : λ_i >= 0, 1^T λ = 1 }`.

Define

`q(λ) := λ^T M λ`.

Copositivity of `M` is equivalent, by positive homogeneity, to

`q(λ) >= 0` for every `λ ∈ Δ_4`.

For each `i`, let `M_hat_i` denote the 3×3 principal matrix obtained by deleting row and column `i`.

Assume as input certificates that every `M_hat_i` is copositive. Under T-P5-155 this is an exact three-vertex obligation.

---

## 2. Main theorem: face-safe 4-simplex failure is exactly interior KKT failure

### Theorem T157-A — `face_copositive_and_no_negative_interior_kkt_iff_copositive`

Assume all four principal faces `M_hat_i` are copositive. Then the following are equivalent:

1. `M` is **not** copositive.
2. There exist `λ ∈ R^4` and `α ∈ R` such that

   `λ_i > 0` for every `i`,

   `1^T λ = 1`,

   `M λ = α 1`,

   `α < 0`.

Moreover, for every such witness,

`q(λ) = α`.

### Proof

**(2 ⇒ 1).** Multiply `Mλ=α1` on the left by `λ^T`:

`q(λ) = λ^T M λ = α λ^T1 = α < 0`.

Since `λ ∈ Δ_4`, copositivity fails.

**(1 ⇒ 2).** Because `Δ_4` is compact and `q` is continuous, choose a global minimizer `λ_* ∈ Δ_4`. Non-copositivity gives

`q(λ_*) < 0`.

If `λ_*` lay on the boundary, at least one coordinate would vanish. Then `λ_*` would belong to a 3-vertex principal face; copositivity of that face would imply `q(λ_*) >= 0`, contradiction. Hence

`λ_{*,i} > 0` for every `i`.

Therefore no inequality constraint is active at the minimizer. The equality-constrained first-order condition for `1^T λ=1` gives some scalar `β` with

`2Mλ_* = β1`.

Put `α=β/2`. Then `Mλ_*=α1`. Multiplying by `λ_*^T` gives `α=q(λ_*)<0`. ∎

### Consequence

After the four face certificates have passed, **there are no hidden edge/vertex/nonstationary failure modes left**. Any negative point forces a negative interior stationary point.

---

## 3. Exact rationality of the interior witness

The KKT equations are linear:

`Mλ - α1 = 0`,

`1^T λ = 1`.

Equivalently,

```text
[ M   -1 ] [ λ ] = [ 0 ]
[ 1^T  0 ] [ α ]   [ 1 ] .
```

All coefficients are rational when `M` is rational.

### Lemma T157-B — `strict_real_kkt_witness_implies_rational_kkt_witness`

If the bordered system has a real solution satisfying

`λ_i>0` for all `i` and `α<0`,

then it has a rational solution satisfying the same strict inequalities.

### Proof

Exact Gaussian elimination over `Q` expresses the real solution set, when nonempty, as

`z = z_0 + Vt`,

where `z_0` and a basis matrix `V` may be chosen rational. The strict sign constraints define a relatively open subset of this rational affine space. Rational parameter vectors are dense in `R^k`; therefore any nonempty relatively open sign-feasible subset contains a rational parameter vector, hence a rational `(λ,α)` witness. ∎

So the negative-interior branch never needs an irrational witness in the trusted packet.

---

## 4. A fully closed exact-rational feasibility gate

Strict inequalities can be converted to one rational LP with a margin variable `t`:

maximize `t` subject to

`Mλ = α1`,

`1^T λ = 1`,

`λ_i >= t` for `i=1,...,4`,

`-α >= t`.

Call its optimum `t_*`.

### Theorem T157-C — `four_vertex_failure_iff_positive_kkt_margin`

Under the four face-copositivity assumptions,

`M` is not copositive **iff** `t_* > 0`.

Proof is immediate from Theorem T157-A: a strict KKT witness has positive minimum margin, and `t>0` forces all required strict signs.

Because `Σ_i λ_i=1`, every feasible `t` satisfies `t<=1/4`, so the maximization is bounded above. With rational data, exact rational LP arithmetic can provide:

- a rational primal witness with `t>0` for decisive **FAIL**; or
- an exact dual/Farkas certificate that `t<=0` for **PASS** after all faces have passed.

This is useful for formalization because the trusted core can be reduced to linear equalities/inequalities plus the already-existing 3-face copositivity theorems.

---

## 5. Nonsingular fast path

If `M` is nonsingular, solve exactly

`M y = 1`,

and put

`s := 1^T y`.

Every interior KKT solution must satisfy

`λ = y/s`, `α = 1/s`,

provided `s != 0`.

Under the face-copositivity assumptions, a negative interior witness exists **iff every component of `y` is strictly negative**.

Indeed:

- if `y_i<0` for all `i`, then `s<0`, so `λ_i=y_i/s>0` and `α=1/s<0`;
- conversely, if `λ>0` and `α<0`, then `y=λ/α` has every component negative.

### Important boundary

This is only a **fast path**. If `M` is singular, or if one tries to reason through a pseudoinverse/arbitrary solve, return to the bordered exact system. The trusted theorem does not require matrix inversion.

---

## 6. Sharp counterexample: every 3-face passes, full 4-simplex fails

Take the rational symmetric matrix with

`M_ii = 5/2`,

`M_ij = -1` for `i != j`.

Every 3×3 principal face has quadratic form

`q_face(x) = (7/2) Σ_i x_i^2 - (Σ_i x_i)^2`.

By `(Σ_i x_i)^2 <= 3 Σ_i x_i^2`,

`q_face(x) >= (1/2) Σ_i x_i^2 >= 0`.

Hence every 3-face is actually PSD, therefore copositive.

But at the full-simplex barycenter

`λ = (1/4,1/4,1/4,1/4)`,

the row sum is

`5/2 - 3 = -1/2`,

so

`Mλ = (-1/8)1`,

and

`q(λ) = -1/8 < 0`.

Thus **checking all four facets alone is insufficient**. The missing object is precisely the interior KKT witness from Theorem T157-A.

This example is also an exact rational regression fixture for the checker.

---

## 7. Sharp endpoint: the sign test must use `α<0`, not `α<=0`

Take

`M_ii = 3`,

`M_ij = -1` for `i != j`.

On the simplex,

`q(λ) = 4 Σ_i λ_i^2 - 1`.

Cauchy gives

`4 Σ_i λ_i^2 >= (Σ_i λ_i)^2 = 1`,

so `q(λ)>=0`: the matrix is copositive.

At the barycenter,

`Mλ=0`, hence `α=0`, and `q(λ)=0`.

Therefore a checker that treats `α<=0` as a failure witness would reject a valid sharp boundary case. The decisive sign is strictly

`α < 0`.

Equivalently, the LP margin must be strictly positive; `t_*=0` is not a FAIL witness.

---

## 8. Formalizable theorem statements

A Lean-style mathematical interface can be kept small.

### `face_copositive_and_no_negative_interior_kkt_iff_copositive`

Inputs:

- `M : Matrix (Fin 4) (Fin 4) Q` with `M.transpose = M`;
- copositivity of each principal 3-face.

Statement:

```text
Copositive M <->
  ¬ ∃ λ α,
      (∀ i, 0 < λ i) ∧
      (sum λ = 1) ∧
      (M *ᵥ λ = α • 1) ∧
      α < 0.
```

### `negative_interior_kkt_has_rational_witness`

For rational `M`, real strict feasibility of the bordered KKT system implies rational strict feasibility.

### `invertible_four_vertex_interior_failure_iff_solve_one_strictly_negative`

Under face copositivity and exact solve `My=1`, if `M` is invertible:

```text
¬ Copositive M <-> ∀ i, y_i < 0.
```

The bordered theorem should remain primary; this specialization is optional optimization.

---

## 9. How this plugs into the T-P5-154 floor matrix

For a fixed candidate floor `D`, construct the exact rational symmetric `M_D` from T-P5-154.

For a four-vertex uncertainty simplex:

1. extract its four 3×3 principal matrices;
2. run the T-P5-155 exact three-vertex copositivity checker on each face;
3. if any face fails, preserve its lower-dimensional exact counterexample;
4. if all faces pass, solve the bordered KKT margin LP above;
5. if `t_*>0`, return the exact rational interior negative witness;
6. if `t_*<=0` by exact certificate, fixed-`D` full-simplex copositivity passes.

This is an **exact fixed-`D` four-vertex lane**. It is complementary to T-P5-156: weighted-slack/refinement structure may certify large problems cheaply, while the present child gives a dimension-4 exact fallback when the actual uncertainty simplex has four vertices.

---

## 10. Fail-closed boundaries

1. **Facet PASS is not full PASS.** Section 6 is a strict rational counterexample.
2. **PSD failure is not copositivity failure.** The trusted object remains copositivity; PSD is only an optional sufficient fast path.
3. **The KKT witness must have `λ_i>0` for all i and `α<0`.** Boundary stationary points are already handled by faces; `α=0` is a valid sharp endpoint.
4. **Do not divide by `s=1^Ty` in the singular/degenerate branch.** Use the bordered exact system.
5. **No pseudoinverse semantics are needed or admitted.** Exact rational linear elimination/LP is enough.
6. **This child fixes `D`.** Finding the globally minimal `D` as `M_D` varies is a separate parametric problem.
7. **Scope is intentionally N=4.** Recursive face/KKT decomposition can be generalized, but complexity grows and no claim of an efficient general copositivity algorithm is made here.
8. Actual `{g_i,K_ij,D}` source binding, same-key/simplex semantics, Float64/runtime reification, Lean/kernel proof, independent verification by 封不觉, registry/admission, and P5 parent closure remain open.

---

## 11. Next child suggested by the mathematics

If the actual unresolved simplex has exactly four vertices, the next concrete source-side step is to emit `M_D` at the candidate `D`, run four exact T-P5-155 face checks, then form the bordered KKT system and return either:

- a rational `(λ,α)` with `λ>0, α<0` as a decisive insufficient-floor counterexample; or
- an exact rational LP/Farkas certificate that no such interior witness exists.

If the actual simplex has more than four vertices, do **not** blindly enumerate a general copositivity recursion before checking whether T-P5-156's weighted-slack/refinement structure reduces it more cheaply.
