---
kind: review_result
review_id: review-T-P5-161-z-matrix-copositivity-equals-psd-kuangmanmozun-20260909T1442Z
task_id: T-P5-161-Z-MATRIX-COPOSITIVITY-EQUALS-PSD
reviewer: 狂蛮魔尊
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-09T14:42:00Z
claim_commit: 0f40285b19ec415fdbdcb43893741da6c63ae10f
inspected_commit: 3fbb1fec1aff70714d16f262451df205b585839a
upstream_commits:
  - c9b94c1f931c76c20a0f22e428425a4d659b57bb  # T-P5-154 uniform additive simplex floor
  - fce11e2368dfd33d225a49adfbeb4a880a7c01ae  # T-P5-158 fixed-floor support/KKT decision
  - 1710eb0b113e44bbe7a4d60367e0bcc8f941ccf9  # T-P5-159 symbolic-floor bracketing
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: use_the_Z_matrix_sign_corridor_as_an_exact_PSD_fast_path_for_fixed_D_and_symbolic_floor_bracketing; keep_generic_support_KKT_outside_the_sign_corridor; require_explicit_cross_nonpositivity_before_treating_PSD_failure_as_physical_floor_failure
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: none; exact finite-dimensional real/rational algebra only
exit_code: n/a
---

# T-P5-161 — symmetric Z-matrix copositivity equals PSD

## 0. Verdict and narrow seam

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-154 reduces a fixed additive simplex floor `D` to copositivity of a symmetric matrix `M_D`. T-P5-158 gives an exact generic finite-support KKT decision, but its worst-case support lattice is combinatorial. T-P5-159 then turns symbolic optimization in `D` into monotone fixed-floor queries.

This child identifies a structural sign regime in which the generic copositivity problem disappears completely:

> For every real symmetric matrix whose off-diagonal entries are nonpositive, copositivity is equivalent to ordinary positive semidefiniteness.

The proof is one line of sign-preserving algebra: replacing `x` by componentwise `|x|` can only decrease the quadratic form. Therefore any signed negative PSD witness automatically yields a nonnegative copositivity witness.

For the T-P5-154 floor matrix this applies whenever

`K_ij + D (g_i+g_j) <= 0`

for every pair. In that corridor, exact rational LDL/PSD checking is not merely a sufficient fast path: it is an exact PASS/FAIL decider. If an entire T-P5-159 rational bracket lies in the corridor, every bisection query may use PSD instead of support enumeration.

This is disjoint from T-P5-160, which is already claimed by 古月方源 for degenerate support kernels/determinant families. No source, provenance, receipt, admission, runtime, or Lean audit is performed here.

---

## 1. General symmetric Z-matrix theorem

Let `M=(m_ij)` be a real symmetric `n x n` matrix. Write

`q_M(x) = x^T M x`.

Call `M` a symmetric **Z-matrix** when

`m_ij <= 0` for every `i != j`.

Call `M` copositive when

`q_M(x) >= 0` for every `x>=0` componentwise.

### Theorem T161-A — `quad_abs_le_of_offdiag_nonpos`

For every symmetric Z-matrix and every real vector `x`,

**`q_M(|x|) <= q_M(x)`.**

Here `|x|` means componentwise absolute value.

### Proof

Expand

`q_M(x) = sum_i m_ii x_i^2 + 2 sum_{i<j} m_ij x_i x_j`.

The diagonal part is unchanged by absolute values. For every pair,

`|x_i| |x_j| = |x_i x_j| >= x_i x_j`.

Since `m_ij<=0`, multiplication reverses the comparison:

`m_ij |x_i| |x_j| <= m_ij x_i x_j`.

Summing all off-diagonal terms gives the result. ∎

### Theorem T161-B — `copositive_iff_psd_of_offdiag_nonpos`

For a real symmetric Z-matrix,

**`M copositive  <=>  M positive semidefinite`.**

### Proof

PSD implies copositive trivially.

Conversely assume copositivity. For arbitrary signed `x`, the vector `|x|` is nonnegative, hence

`0 <= q_M(|x|) <= q_M(x)`

by T161-A. Thus `q_M(x)>=0` for every real `x`, which is exactly PSD. ∎

### Important point

No irreducibility, strict negativity, positive diagonal, invertibility, eigenvector theorem, Perron-Frobenius theorem, or square root is needed. Zero off-diagonal entries and singular PSD endpoints are included automatically.

---

## 2. PSD failure becomes an explicit nonnegative failure witness

The same argument gives a stronger operational statement.

### Theorem T161-C — `signed_psd_counterexample_absifies`

If `M` is symmetric Z and some real vector `x` satisfies

`q_M(x)<0`,

then the physical nonnegative vector

`y=|x|>=0`

satisfies

**`q_M(y) <= q_M(x) < 0`.**

So a PSD counterexample is already enough to produce a copositivity counterexample; no support KKT solve is required.

For rational `M`, if `M` is not PSD then a rational negative witness exists: choose a real negative witness; strict negativity is open under perturbation and `Q^n` is dense in `R^n`. Thus a producer may return exact rational `x`, and the checker only verifies the rational inequality `x^T M x<0`, forms rational `|x|`, and checks the sign gate.

This matters for fail-closed semantics: an implementation merely failing to construct an LDL factorization is not a mathematical FAIL. A valid FAIL packet must still contain an exact negative quadratic witness or another exact PSD-negativity certificate. Once such a witness exists, T161-C converts it to the required nonnegative state.

---

## 3. Specialization to the T-P5-154 floor matrix

Use T-P5-154 notation. For vertices with `g_i>0` and symmetric `K_ij`, define the homogeneous floor matrix by

`M_D[ii] = D g_i`,

`2 M_D[ij] = K_ij + D(g_i+g_j)` for `i!=j`.

Then

`x^T M_D x = Q_0(x) + D L(x)`,

and on simplex vectors this is exactly the uniform-floor expression.

### Theorem T161-D — `valid_floor_iff_psd_in_Z_corridor`

Assume

1. `D>=0`;
2. `g_i>0` for all `i`;
3. for every `i<j`,

   **`K_ij + D(g_i+g_j) <= 0`.**

Then

**`D is a valid uniform simplex floor  <=>  M_D is PSD`.**

### Proof

The pairwise gate makes `M_D` a symmetric Z-matrix. T-P5-154 identifies valid-floor nonnegativity with copositivity of `M_D`. Apply T161-B. ∎

### Consequence

Inside this sign corridor, the exact fixed-floor decision becomes:

- exact PSD PASS -> exact floor PASS;
- exact PSD FAIL witness `x` -> `|x|` is an exact floor FAIL witness.

Therefore T-P5-158's support enumeration is unnecessary in this branch.

---

## 4. A whole rational bracket can stay inside the PSD corridor

For fixed `g_i>0`, each off-diagonal coefficient

`c_ij(D)=K_ij + D(g_i+g_j)`

is increasing in `D`.

### Theorem T161-E — `upper_endpoint_Z_implies_lower_interval_Z`

If `0<=L<=U` and

`K_ij + U(g_i+g_j) <= 0`

for every pair, then the same inequality holds for every `D in [L,U]`.

Hence, if T-P5-159 has a certified floor bracket

`L <= D_* <= U`

and the **upper endpoint** satisfies the Z sign gate, every rational midpoint queried during bracketing also lies in the Z corridor. Every fixed-floor T-P5-158 call may then be replaced by an exact PSD decision.

A particularly clean packet is:

1. rational `U>=0`;
2. exact pairwise gates `K_ij+U(g_i+g_j)<=0`;
3. exact PSD certificate for `M_U`.

Then `U` is valid and `D_*<=U`; moreover the entire search interval `[0,U]` is in the Z corridor, so the sharp floor is exactly the first `D` at which `M_D` becomes PSD.

No generic copositivity oracle is needed anywhere in that interval.

---

## 5. Exact rational checker consequences

Assume rational input data and rational trial `D`.

### PASS lane

After checking the Z sign gate exactly, use any exact rational PSD certificate. A rational `LDL^T`/congruence certificate with nonnegative diagonal pivots is natural because it needs no square roots. Singular zero pivots are allowed when the corresponding exact congruence is valid.

### FAIL lane

Return an exact rational vector `x` with

`x^T M_D x < 0`.

The checker computes `y_i=|x_i|`, verifies `y>=0`, and T161-A yields

`y^T M_D y <= x^T M_D x < 0`.

Normalization to the simplex is mathematically optional because the floor quadratic is homogeneous. If a downstream interface insists on `sum lambda_i=1`, set `s=sum_i y_i>0` and `lambda=y/s`; the checker may instead clear the positive denominator and retain the homogeneous witness.

### Complexity consequence

The analytic obstruction in this branch is polynomial-size linear algebra rather than `2^n-1` support enumeration. This is a mathematical reduction, not a claim about a particular repository implementation's runtime.

---

## 6. Sharp multiway family: PSD recovers the exact full-simplex tax

Take `N>=2`, equal vertex weights

`g_i=g>0`,

and equal adverse pair interactions

`K_ij=-kappa`, `kappa>0`.

Then

`M_D[ii]=Dg`,

`M_D[ij]=Dg-kappa/2` for `i!=j`.

The Z sign gate is

`D <= kappa/(2g)`.

For arbitrary real `x`, let `S=sum_i x_i`. Exact algebra gives

**`x^T M_D x = (kappa/2) sum_i x_i^2 + (Dg-kappa/2) S^2`.**

Define

**`D_* = kappa (N-1)/(2 g N)`.**

At `D=D_*`,

`D_* g-kappa/2 = -kappa/(2N)`,

so

`x^T M_{D_*} x`

`= (kappa/2) [sum_i x_i^2 - S^2/N]`

`>=0`

by `S^2 <= N sum_i x_i^2`.

Thus `M_{D_*}` is PSD. Equality occurs for the all-ones vector.

For `D<D_*`, choose `x=1` (all coordinates one). Then

`x^T M_D x`

`= N [N D g - (N-1)kappa/2]`

`<0`.

Hence `M_D` is not PSD and, since the all-ones vector is already nonnegative, the floor fails.

Therefore the sharp floor is exactly

**`D_* = kappa (N-1)/(2 g N)`.**

Moreover

`D_* < kappa/(2g)`,

and at the sharp point the off-diagonal coefficient is strictly negative:

`-kappa + 2D_*g = -kappa/N < 0`.

So the true multiway floor from T-P5-154 lies strictly inside the Z corridor. The earlier `N`-way tax is not an inherently hard copositivity phenomenon in this sign-symmetric family: one exact PSD check sees it sharply.

This is a useful high-dimensional regression for a future checker.

---

## 7. The sign gate is essential

One must **not** globally replace copositivity by PSD.

Take the rational symmetric matrix

`M = [[1,2],[2,1]]`.

For every `x,y>=0`,

`[x,y] M [x,y]^T = x^2 + 4xy + y^2 >=0`,

so `M` is copositive.

But for the signed vector `(1,-1)`,

`q_M(1,-1)=1-4+1=-2<0`.

Thus `M` is not PSD.

The only reason T161-B works is the off-diagonal nonpositivity that guarantees

`q_M(|x|)<=q_M(x)`.

With positive cross entries, absolute values can increase the quadratic form and a signed negative PSD direction may have no physical nonnegative analogue.

### Hard fail-closed rule

Outside the exact pairwise sign gate

`K_ij+D(g_i+g_j)<=0`,

PSD failure is **not** floor failure. Return to T-P5-155/157/158 copositivity machinery or another justified branch.

---

## 8. A useful partial structural fallback

There is one weaker decomposition that remains sound even when the whole matrix is not Z.

Suppose the vertex set is partitioned into blocks `B_1,...,B_m` such that

1. every diagonal principal block `M[B_a,B_a]` is PSD;
2. every cross-block entry is nonnegative:

   `M_ij>=0` whenever `i in B_a`, `j in B_b`, `a!=b`.

Then `M` is copositive, because for `x>=0`

`x^T M x`

is the sum of nonnegative within-block quadratic forms plus nonnegative cross-block terms.

This is only a **sufficient** decomposition, not an equivalence, and should not be confused with T161-B. It may nevertheless prune a large uncertainty simplex into exact PSD subblocks plus sign-safe positive couplings.

No claim of optimality is made for this fallback.

---

## 9. Minimal formal theorem statements

A Lean-facing implementation can remain division-free.

### T161-L1 — absolute-value domination

For finite index type `ι`, symmetric real matrix `M`, and hypothesis

`forall i j, i != j -> M i j <= 0`,

prove

`quad M (fun i => |x i|) <= quad M x`.

### T161-L2 — Z-copositive iff PSD

Under the same symmetry/sign hypotheses,

`(forall x, (forall i, 0<=x i) -> 0<=quad M x)`

iff

`forall x, 0<=quad M x`.

### T161-L3 — negative witness absification

Under the Z hypotheses,

`quad M x < 0 -> quad M (absVec x) < 0`.

This is immediate from L1 and transitivity.

### T161-L4 — floor specialization

Given T-P5-154's exact identity and pair gates

`K_ij+D*(g_i+g_j)<=0`,

show

`ValidFloor D <-> Matrix.PosSemidef (M D)`.

### T161-L5 — interval sign inheritance

For `D<=U`, `g_i+g_j>0`,

`K_ij+U*(g_i+g_j)<=0`

implies

`K_ij+D*(g_i+g_j)<=0`.

### T161-L6 — equal-family sharp regression

For `N>=2`, `g>0`, `kappa>0`, prove the quadratic identity in Section 6 and the threshold implication using only finite-sum Cauchy and ordered-field algebra.

No determinant, square root, matrix inverse, or eigenvalue API is necessary for the mathematical core.

---

## 10. Failed routes / excluded overclaims

1. **Generic PSD substitution fails.** The positive-off-diagonal `[[1,2],[2,1]]` example is copositive but not PSD.
2. **An LDL program error is not a mathematical counterexample.** FAIL needs exact negative quadratic evidence.
3. **The Z corridor need not contain the sharp floor for arbitrary data.** If a pair coefficient turns positive before global validity, generic copositivity remains necessary.
4. **PSD monotonicity in `D` is not asserted for arbitrary unequal `g_i`.** Although valid floors are monotone on the nonnegative cone by T-P5-159, the affine coefficient matrix in `D` is not automatically PSD on all signed vectors. The safe statement is pointwise equivalence at each `D` inside the Z corridor, plus interval inheritance of the sign gate.
5. **No source equality is inferred from signs.** Actual `g_i,K_ij,D` still require same-key source binding.
6. **No infinite-uncertainty reduction is supplied.** This child remains finite-dimensional after whatever finite simplex/polytope reduction produced T-P5-154.

---

## 11. Next mathematical use

For an actual unresolved T-P5-154 simplex packet, compute the exact rational pair coefficients first.

- If a known valid upper floor `U` also satisfies all Z pair gates at `U`, switch the whole T-P5-159 bracket `[0,U]` to exact PSD/LDL decisions. This can eliminate support enumeration entirely.
- If only some principal support is Z, use PSD on that support as a local exact face decision and retain T-P5-158 only for the remaining mixed-sign supports.
- If the sign gate fails, do not force PSD. Keep the generic copositivity branch.

A useful child for later, if actual source matrices exhibit block sign structure, is to formalize a graph/block decomposition that combines exact Z-PSD components with nonnegative cross-component couplings. That should be driven by real source sparsity rather than invented abstract complexity.

---

## 12. Non-admission boundary

This review proves only a source-independent finite-dimensional inequality theorem. It does **not** establish:

- actual deployed `{g_i,K_ij,D}` values;
- same-cell or uncertainty-simplex semantics;
- physical boundary attainability;
- runtime/Float64 error closure;
- Lean compilation or kernel acceptance;
- independent verification by 封不觉;
- registry/admission eligibility;
- P5/P8/M4 parent closure.

All such gates remain open and fail-closed.
