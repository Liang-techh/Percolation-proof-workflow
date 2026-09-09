---
kind: review_result
review_id: review-T-P5-158-finite-support-kkt-copositivity-decision-honglianmozun-20260909T1400Z
task_id: T-P5-158-FINITE-SUPPORT-KKT-COPOSITIVITY-DECISION
reviewer: 红莲魔尊
agent: 红莲魔尊
source_agent: 红莲魔尊
created_at: 2026-09-09T14:00:00Z
claim_commit: 59482d8a9ecea220a8803ad0e49926e8a6123771
inspected_commit: 314769cb5a0c946e8da2f56caed001189914616e
upstream_commits:
  - c9b94c1f931c76c20a0f22e428425a4d659b57bb  # T-P5-154 uniform additive simplex floor
  - b79e57e78e42aeba644b3e030a7e9a93d81eecf0  # T-P5-155 exact three-vertex checker
  - f304662c5b3e3fc0224e9ba99934aa336ab18639  # T-P5-157 four-vertex face/KKT closure
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: use_support_lattice_KKT_as_exact_fixed_floor_copositivity_fallback_after_low_dimensional_fast_paths; enumerate_only_uncertified_supports; keep_symbolic_D_optimization_and_source_binding_separate
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: none; exact finite-dimensional real/rational algebra only
exit_code: n/a
---

# T-P5-158 — finite-support KKT copositivity decision

## 0. Verdict and narrow seam

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-154 reduced a fixed additive robust-reset floor to copositivity of an exact rational symmetric matrix. T-P5-155 gave a closed-form exact checker for three vertices. T-P5-157 then showed that, for four vertices whose three-vertex faces are already safe, only one full-support KKT branch remains.

The remaining mathematical seam is the generic finite number of uncertainty vertices. The smallest useful result is not another sufficient PSD surrogate. It is the exact support structure of a negative copositive witness.

This child proves:

> For any finite rational symmetric matrix, non-copositivity is equivalent to the existence of a nonempty principal support on which a strictly positive simplex vector solves one bordered linear KKT system at a strictly negative level.

Consequently, **fixed-floor copositivity in arbitrary finite dimension can be decided by finitely many exact rational linear feasibility problems**. No square root, eigenvalue computation, matrix inverse, nonlinear optimizer, or generic copositivity oracle is required in the trusted mathematical statement.

The price is combinatorial rather than analytic: in the worst case one may inspect `2^n-1` nonempty supports. Low-dimensional face certificates and sparsity can prune that lattice heavily.

This result does **not** optimize a symbolic floor parameter `D`, does not bind an actual source matrix, and does not claim computational efficiency for large `n`.

---

## 1. Setup

Let

`M in Q^(n x n)`, `M=M^T`, `n>=1`.

For a real vector `x>=0`, define

`q_M(x)=x^T M x`.

`M` is copositive iff

`q_M(x)>=0` for every `x>=0`.

By quadratic homogeneity, it is enough to test the simplex

`Delta_n = {lambda in R^n : lambda_i>=0, 1^T lambda=1}`.

Indeed every nonzero `x>=0` can be written as

`x = s lambda`, `s=1^T x>0`, `lambda=x/s in Delta_n`,

and

`q_M(x)=s^2 q_M(lambda)`.

For a nonempty index set `S subseteq {1,...,n}`, let `M_SS` denote the corresponding principal submatrix and let `1_S` be its all-ones vector.

---

## 2. Main theorem: every failure is a finite-support negative KKT witness

### Theorem T158-A — `noncopositive_iff_negative_support_kkt`

The following are equivalent.

1. `M` is not copositive.
2. There exist a nonempty support `S`, a vector `lambda_S in R^S`, and a scalar `alpha in R` such that

   `lambda_S > 0` componentwise,

   `1_S^T lambda_S = 1`,

   `M_SS lambda_S = alpha 1_S`,

   `alpha < 0`.

For every witness in (2), extending `lambda_S` by zero outside `S` gives a physical simplex counterexample and

**`lambda^T M lambda = alpha < 0`.**

### Proof: support witness implies failure

Extend `lambda_S` to `lambda in Delta_n` by setting all coordinates outside `S` to zero. Then

`lambda^T M lambda`

`= lambda_S^T M_SS lambda_S`

`= lambda_S^T (alpha 1_S)`

`= alpha (1_S^T lambda_S)`

`= alpha < 0`.

Hence `M` is not copositive.

### Proof: failure implies support witness

Assume `M` is not copositive. After simplex normalization there is some `lambda in Delta_n` with `q_M(lambda)<0`.

Because `Delta_n` is compact and `q_M` is continuous, choose a global minimizer `lambda_*` on `Delta_n`. Then

`q_M(lambda_*)<0`.

Let

`S = {i : lambda_{*,i}>0}`.

`S` is nonempty and `lambda_{*,S}` lies in the relative interior of the face `Delta_S`.

Take any tangent vector `v in R^S` with

`1_S^T v=0`.

Since every coordinate of `lambda_{*,S}` is strictly positive, for sufficiently small positive and negative `epsilon`,

`lambda_{*,S}+epsilon v`

remains in `Delta_S`. Therefore the derivative of the quadratic at `epsilon=0` must vanish:

`0 = d/d epsilon q_M(lambda_*+epsilon v)|_(epsilon=0)`

`= 2 v^T M_SS lambda_{*,S}`.

Thus `M_SS lambda_{*,S}` is orthogonal to every vector with zero coordinate sum. The orthogonal complement of that tangent space is `span{1_S}`. Hence there exists `alpha` such that

`M_SS lambda_{*,S}=alpha 1_S`.

Multiplying on the left by `lambda_{*,S}^T` gives

`alpha`

`= alpha 1_S^T lambda_{*,S}`

`= lambda_{*,S}^T M_SS lambda_{*,S}`

`= q_M(lambda_*)`

`<0`.

This is the required support witness. ∎

### Important structural point

No inactive-coordinate KKT inequality is needed in the certificate.

For proving that a chosen point is a global optimizer, inactive gradients matter. Here they do not: once a support system produces a positive `lambda_S` with `alpha<0`, that vector itself is already a negative feasible state. Conversely, a true failure supplies at least one support through the global-minimum argument.

This substantially simplifies the trusted packet.

---

## 3. Minimal negative support and recursive face localization

Among all supports admitting a negative witness, choose one of minimum cardinality, call it `S_min`.

### Corollary T158-B — `minimal_bad_support_has_safe_proper_faces`

For every proper nonempty subset `T proper_subset S_min`, the principal matrix `M_TT` is copositive.

Otherwise `M_TT` would itself admit a negative simplex point, and Theorem T158-A applied to that smaller matrix would produce a negative witness on a support strictly contained in `S_min`, contradiction.

Therefore every failure has a **minimal bad principal face** with two properties:

1. every proper principal face is copositive;
2. the bad face itself has a strictly positive full-support KKT witness.

This is the dimension-independent form of the mechanism used in T-P5-157.

### Corollary T158-C — `face_safe_reduces_to_full_support_kkt`

If every proper principal submatrix of `M` is already certified copositive, then `M` is non-copositive iff there exist

`lambda>0`, `1^T lambda=1`, `M lambda=alpha 1`, `alpha<0`.

So an exact checker may proceed recursively through the support lattice and only solve the full-support bordered system after all proper faces have passed.

---

## 4. Rational witness theorem

The previous theorem is over real variables. For the repository's exact-rational checker architecture, the crucial additional fact is that irrational witnesses are unnecessary when `M` is rational.

Fix a support `S`. The stationarity equations are the rational linear system

`M_SS lambda_S - alpha 1_S = 0`,

`1_S^T lambda_S = 1`.

Equivalently,

```text
[ M_SS   -1_S ] [lambda_S] = [0]
[ 1_S^T    0   ] [ alpha  ]   [1].
```

### Theorem T158-D — `real_strict_support_witness_implies_rational_witness`

If the bordered system has a real solution with

`lambda_S>0`, `alpha<0`,

then it has a rational solution with the same strict signs.

### Proof

Perform Gaussian elimination over `Q`.

If the solution is unique, its coordinates are rational immediately.

If the solution set has positive dimension, rational row reduction expresses it as

`z = z_0 + V t`,

where `z_0` and the columns of `V` are rational and `t` is a real free-parameter vector.

The conditions `lambda_i>0` and `alpha<0` define a relatively open subset of this affine solution space. By assumption that open subset is nonempty. Rational parameter vectors are dense in the real parameter space, so it contains a rational `t`. The corresponding `z` is rational and retains all strict signs. ∎

### Consequence

For rational `M`, **every non-copositivity failure has an exact rational negative support witness.**

This is stronger than merely saying the matrix can be numerically falsified.

---

## 5. Exact rational LP-margin gate for one support

For each nonempty support `S`, introduce a margin variable `t` and solve the rational linear program

maximize `t` subject to

`M_SS lambda_S = alpha 1_S`,

`1_S^T lambda_S = 1`,

`lambda_{S,i} >= t` for every `i in S`,

`-alpha >= t`.

Call the optimum `t_S^*`; if the equality system is infeasible, set `t_S^*=-infinity` by convention.

Because the coordinates sum to one,

`t <= 1/|S|`,

so the objective is bounded above whenever the system is feasible.

### Theorem T158-E — `support_failure_iff_positive_margin`

A support `S` carries a negative KKT witness iff

**`t_S^*>0`.**

Proof:

- a strict witness has positive minimum margin

  `min(min_i lambda_i, -alpha)>0`,

  so some feasible `t>0` exists;
- any feasible `t>0` forces `lambda_i>0` and `alpha<0`, hence gives a support witness.

Since all coefficients are rational, a positive branch has a rational primal witness. A non-positive branch can be certified by exact rational LP dual/Farkas data.

---

## 6. Finite exact decision theorem

### Theorem T158-F — `finite_support_decision_for_rational_copositivity`

For rational symmetric `M`,

**`M` is copositive iff for every nonempty support `S`, the support-margin LP is either infeasible or has `t_S^*<=0`.**

Equivalently,

**`M` is non-copositive iff at least one nonempty support has `t_S^*>0`.**

This is a finite exact decision procedure with at most

`2^n-1`

support branches.

Each branch uses only rational linear equalities and inequalities.

### Trusted arithmetic requirements

A checker needs only:

1. extraction of a principal rational matrix `M_SS`;
2. exact rational linear-system / LP feasibility;
3. exact rational sign comparisons;
4. for FAIL, the direct identity

   `lambda_S^T M_SS lambda_S = alpha < 0`;
5. for PASS, exact infeasibility or `t<=0` dual certificates for all support branches not already discharged by stronger face certificates.

No general-purpose numerical copositivity solver is mathematically necessary.

---

## 7. Why `t=0` is a boundary signal, not a failure witness

A frequent implementation error would be to accept a support solution with some zero coordinate as if it were a full-support witness.

If `t_S^*=0`, the support branch has not produced the strict certificate required by Theorem T158-A. Any candidate with a zero coordinate belongs to a proper face and should be delegated to that smaller support.

This is exactly why the support lattice is the correct object:

- strict positive margin means **this support itself fails**;
- zero margin means **look at a proper face**;
- all proper faces safe plus no strict full-support witness means **this face is safe**.

Thus no epsilon convention is needed.

---

## 8. Nonsingular fast path on any support

If `M_SS` is nonsingular, solve exactly

`M_SS y = 1_S`.

Let

`s=1_S^T y`.

Every full-support stationary solution on that face must satisfy

`lambda_S=y/s`,

`alpha=1/s`,

when `s!=0`.

Under already-certified proper faces, a negative full-support witness exists iff

**every component of `y` is strictly negative.**

Indeed, if `y<0`, then `s<0`, hence `lambda=y/s>0` and `alpha=1/s<0`. Conversely a negative KKT witness obeys

`y=lambda/alpha`,

so every component of `y` is negative.

This generalizes the nonsingular fast path in T-P5-157. Singular principal blocks must return to the bordered rational system; no pseudoinverse convention is needed.

---

## 9. Exact five-vertex example: every proper face passes, full simplex fails

The four-vertex phenomenon from T-P5-157 is not dimension-specific.

Take `n=5` and the rational symmetric matrix

`M_ii = 7/2`,

`M_ij = -1` for `i!=j`.

On a support of cardinality `k`, with simplex weights summing to one,

`q(lambda)`

`= (9/2) sum_i lambda_i^2 - (sum_i lambda_i)^2`

`= (9/2) sum_i lambda_i^2 - 1`.

By Cauchy,

`sum_i lambda_i^2 >= 1/k`.

Hence the minimum on a `k`-vertex face is

`(9/2)(1/k)-1`.

For every proper face, `k<=4`, so

`q >= 9/8 - 1 = 1/8 > 0`.

Thus **every proper principal face is strictly copositive**.

But at the five-vertex barycenter

`lambda=(1/5,1/5,1/5,1/5,1/5)`,

one has

`q(lambda)=9/10-1=-1/10`.

Moreover every row satisfies

`(M lambda)_i = (7/2)(1/5)-4(1/5) = -1/10`,

so

`M lambda = (-1/10) 1`.

This is exactly the full-support KKT witness predicted by T158-C.

Therefore checking all lower-dimensional faces is insufficient unless the final full-support branch is also checked.

---

## 10. Exact PASS example where PSD would falsely reject

Let

```text
M = [1 2]
    [2 1].
```

`M` is not PSD: `(1,-1)` is a negative-eigenvalue direction.

But for every `x>=0`,

`x^T M x = x_1^2 + 4 x_1 x_2 + x_2^2 >=0`.

So `M` is copositive.

The support checker sees:

- `S={1}`: stationary value `alpha=1>0`;
- `S={2}`: stationary value `alpha=1>0`;
- `S={1,2}`: `lambda=(1/2,1/2)` and `alpha=3/2>0`.

No support has positive failure margin.

Thus the support/KKT route is genuinely a copositivity checker, not a disguised PSD test. It retains precisely the nonnegative-orthant geometry that T-P5-154 was designed to preserve.

---

## 11. Exact FAIL example localized to a two-vertex support

Let

```text
M = [ 1 -2]
    [-2  1].
```

The singleton faces pass, but on `S={1,2}`,

`lambda=(1/2,1/2)` gives

`M lambda = (-1/2) 1`,

so `alpha=-1/2` and

`lambda^T M lambda=-1/2`.

The support margin may take

`t=min(1/2,1/2)=1/2>0`.

This is an exact rational FAIL witness with no spectral computation.

---

## 12. Relationship to T-P5-154 / T-P5-155 / T-P5-157

### T-P5-154

For a **fixed rational candidate floor `D`**, T-P5-154 constructs an exact rational symmetric matrix `M_D` whose copositivity is the robust simplex obligation.

T-P5-158 can now serve as the generic finite-dimensional exact fallback:

`fixed D -> build M_D -> enumerate uncertified supports -> rational KKT-margin checks`.

The earlier PSD gate remains a useful fast sufficient path, but PSD failure is no longer a mathematical dead end.

### T-P5-155

For three vertices, the analytic edge/interior formulas in T-P5-155 are much cheaper than generic support enumeration. They should remain the preferred specialized fast path.

T-P5-158 explains why that finite active-set analysis is complete: every negative minimum lives on some support face and is stationary relative to that face.

### T-P5-157

T-P5-157 is recovered exactly by setting `n=4` and taking the four three-vertex principal faces as already certified. T158-C then leaves only the full support `S={1,2,3,4}` and its bordered KKT system.

So the hierarchy is now:

1. use closed-form low-dimensional face checkers when available;
2. reuse certified proper faces;
3. solve only the remaining full-support bordered branch;
4. in the worst case, enumerate the finite support lattice.

---

## 13. Structural fingerprint for the Lyapunov/reset pipeline

The reusable structural rule is:

> **Quadratic robust failure on a finite simplex localizes to a minimal active uncertainty support, and that support exposes a strictly negative relative-interior KKT equality.**

This suggests a fail-closed checker architecture:

- preserve the signed quadratic matrix until after uncertainty geometry is fixed;
- avoid replacing copositivity by PSD unless using it only as a fast sufficient gate;
- cache principal-face certificates;
- when a face fails, return the smallest support with a rational negative KKT witness;
- when a face passes only after all proper faces pass, its only new obligation is the full-support bordered system.

For energy/Lyapunov diagnostics this is useful because a failure witness identifies **which uncertainty vertices must mix simultaneously** to consume the reset budget. It is more informative than a generic negative eigenvector, which may leave the physical simplex entirely.

---

## 14. Candidate theorem statements

### Candidate theorem 1 — support witness completeness

`noncopositive M`

iff there exist nonempty `S`, `lambda_S>0`, `alpha<0` with

`sum lambda_S=1`

and

`M_SS lambda_S = alpha 1_S`.

### Candidate theorem 2 — face-pruned full-support criterion

If every proper principal submatrix of `M` is copositive, then

`M` copositive

iff there do **not** exist `lambda>0`, `alpha<0` satisfying

`sum lambda=1`, `M lambda=alpha 1`.

### Candidate theorem 3 — rational witness

For rational symmetric `M`, every real strict support witness can be replaced by a rational strict support witness.

### Candidate theorem 4 — LP margin criterion

For fixed support `S`, strict failure is equivalent to positivity of the exact rational margin LP optimum.

These statements are intentionally independent of source/runtime details.

---

## 15. Failure boundaries / what this child does not close

1. **Symbolic optimization over `D` is not closed.** For each fixed rational `D`, `M_D` is rational and the checker is exact. If `D` itself is a variable inside `M_D`, the joint KKT equations may become bilinear in `(D,lambda)`; this theorem does not pretend that is an LP.
2. **The worst-case support count is exponential.** This is an exact mathematical fallback, not a polynomial-time complexity claim.
3. **Infinite uncertainty sets are not covered directly.** They first require a finite exact polytope/simplex reduction or another compactness/structure theorem.
4. **Source equality remains external.** An exact checker for a rational matrix does not prove that the matrix equals the deployed Lyapunov/reset packet.
5. **Domain/cell coverage remains external.** The simplex matrix can be correct while the underlying physical state cell is wrong.
6. **No Lean/kernel validation was run.** This is a candidate mathematical theorem package only.
7. **No admission or registry mutation is justified.**

---

## 16. Recommended next handoff

For any actual fixed-floor robust-reset packet with finitely many uncertainty vertices:

1. bind the exact rational `M_D` to the same source/state-cell key;
2. run any cheap PSD or low-dimensional face fast paths first;
3. retain cached copositive principal faces;
4. for each remaining support, emit either
   - a rational strict KKT witness `(S,lambda,alpha)` with `alpha<0`, or
   - an exact LP dual/Farkas certificate excluding positive margin;
5. treat the support witness as a diagnostic: it identifies the exact subset of uncertainty vertices responsible for a reset-floor failure.

Current status remains **pending** until source binding, physical coverage, and the repository's independent verification gates are supplied.