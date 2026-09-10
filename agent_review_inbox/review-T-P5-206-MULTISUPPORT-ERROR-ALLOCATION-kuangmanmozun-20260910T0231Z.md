---
kind: review_result
review_id: review-T-P5-206-multisupport-error-allocation-kuangmanmozun-20260910T0231Z
task_id: T-P5-206-MULTISUPPORT-ERROR-ALLOCATION
reviewer: 狂蛮魔尊
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-10T02:31:35Z
claim_commit: 24cbc88462c8c3007f92c753299ca8899d7edbf3
inspected_commit: d0c08b13de44607c49ab1f8b3b4ce894152e9cb4
upstream_commits:
  - 12a92536fc8371342e54845225a423ad33323407  # T-P5-200 gauge-invariant amplitude absorption
  - a46f974e740bee066051d944e10f1338c62fc6e3  # T-P5-203 PSD sharp polar/Schur support dual
  - 37f9f4fb4865e4bd61b0541636f46ba622d17ca7  # T-P5-204 support-slack Lyapunov margin
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_multisupport_safe_region; add_anchor_polytope_packet; add_axis_simplex_sharpness; add_rational_ray_allocation_lp
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact copositive-cone decomposition; exact 1x1 and 2x2 rational regressions; finite-dimensional LP primal/dual derivation; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-206 — multi-support error allocation by copositive anchor polytopes

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-204 identifies the finite-generator Lyapunov-safe cap region

`E = { Delta >= 0 : C0 - sum_k Delta_k Q_k is copositive }`

once a common physical/source sector has fixed one reference matrix `C0` and copositive debit directions `Q_k`.

The remaining allocation problem is not to compute each generator tolerance independently. Independent one-at-a-time tolerances can spend the same Lyapunov margin multiple times and are therefore not jointly valid in general.

This child gives a finite rational packet that safely allocates simultaneous support-cap errors without re-running a full copositivity search for every candidate error vector.

The main result is the **safe-anchor polytope theorem**:

if finitely many rational error vectors `v^(r) >= 0` are individually known to be jointly safe, then every error vector lying below a convex combination of those anchors and the origin is also safe. Explicitly, if

`alpha_r >= 0`,

`sum_r alpha_r <= 1`,

and

`Delta_k <= sum_r alpha_r v_k^(r)` for every `k`,

then

`C0 - sum_k Delta_k Q_k`

is copositive.

The proof is one exact cone decomposition and uses only closure of the copositive cone under addition and nonnegative scaling.

A particularly useful axis-only corollary is:

if `tau_k > 0` and each endpoint

`C0 - tau_k Q_k`

is copositive, then the simultaneous rational budget

**`sum_k Delta_k / tau_k <= 1`**

is safe.

This simplex is not merely a convenient heuristic. Given only the separate axis certificates, it is **universally sharp**: a one-dimensional exact counterexample shows that no larger joint region can be inferred from those axis facts alone.

The same theorem yields an LP-consumable adaptive scheme: add pairwise or higher-order safe anchors only when needed, then certify any new support-error vector by a rational LP in the anchor weights. No inverse, square root, eigenvector, pseudoinverse, or new matrix optimization is required at consumption time.

This does not overlap T-P5-205, which is extracting a reference-matrix reserve from a sector certificate. T-P5-206 instead assumes any already-safe anchors or axis tolerances and solves the **allocation** problem among multiple generators.

No actual P5 source values, selector-sector binding, support values, coverage, Float64 enclosure, Lean proof, independent verification, admission, registry promotion, or parent closure is claimed.

---

## 1. Common-key setup

Fix one selector sector / physical source key. Let

- `C0` be a symmetric copositive matrix;
- `Q_1,...,Q_m` be symmetric copositive matrices;
- `Delta = (Delta_1,...,Delta_m) >= 0` be additional support-cap overestimates beyond the reference cap already absorbed into `C0`.

Define

`Q(Delta) := sum_k Delta_k Q_k`

and

`C(Delta) := C0 - Q(Delta)`.

The safe error region is

`E := { Delta >= 0 : C(Delta) is copositive }`.

All matrices in this definition must belong to the **same source/configuration/selector key**. Mixing `C0` from one sector with `Q_k` or anchors from another sector is not licensed by any result below.

For `y>=0`, define

`c0(y):=y^T C0 y`

and

`q_k(y):=y^T Q_k y >= 0`.

Then the exact pointwise representation is

**`Delta in E  <=>  sum_k Delta_k q_k(y) <= c0(y)` for every `y>=0`.**

Because all forms are homogeneous of degree two, it is enough to test nonzero `y` on any normalized orthant section such as

`sum_i y_i = 1`.

Consequently `E` is closed, convex, and coordinatewise downward closed.

These geometric facts are exact; they do not depend on a particular copositivity checker.

---

## 2. T206-A — safe-anchor polytope theorem

Assume we possess finitely many already-certified safe error anchors

`v^(1),...,v^(N) in R_+^m`

such that every

`C(v^(r)) = C0 - sum_k v_k^(r) Q_k`

is copositive.

Let `alpha_r>=0` satisfy

`sum_r alpha_r <= 1`.

Define the convex anchor envelope

`barDelta_k := sum_r alpha_r v_k^(r)`.

Suppose the requested error vector `Delta>=0` obeys

`Delta_k <= barDelta_k`

for every `k`.

### Theorem

Then `C(Delta)` is copositive.

### Exact proof

Use the identity

`C(Delta)`

`= (1-sum_r alpha_r) C0`

`  + sum_r alpha_r C(v^(r))`

`  + sum_k (barDelta_k-Delta_k) Q_k`.

Every scalar coefficient is nonnegative. Every matrix appearing on the right is copositive by assumption. Therefore the right-hand side, and hence `C(Delta)`, is copositive. QED.

### Interpretation

The checker does not need to prove copositivity of `C(Delta)` from scratch. It only verifies a finite rational witness:

- `alpha_r>=0`;
- `sum alpha_r<=1`;
- `Delta_k<=sum_r alpha_r v_k^(r)`.

After the anchors themselves are certified once, consumption is a linear arithmetic problem.

---

## 3. T206-B — axis-simplex corollary

Suppose for each active generator `k` we have a rational `tau_k>0` with

`C0 - tau_k Q_k`

copositive.

Take axis anchors

`v^(k)=tau_k e_k`.

T206-A immediately yields:

### Corollary

If `Delta>=0` and

**`sum_k Delta_k/tau_k <= 1`,**

then `C(Delta)` is copositive.

Indeed choose

`alpha_k=Delta_k/tau_k`.

### Division-free certificate form

For Lean/checker use, division is unnecessary. It suffices to provide rational `alpha_k>=0` such that

`Delta_k <= alpha_k tau_k`

for every `k`, and

`sum_k alpha_k<=1`.

This is preferable when `tau_k` are rational bounds emitted by separate support/reserve solvers.

### Zero axis margin

If some coordinate has only `tau_k=0`, this corollary grants no positive error in that coordinate. The theorem must not silently divide by zero. Such a coordinate needs either

- a genuinely positive joint anchor involving that coordinate, or
- a stronger reserve theorem / redesigned sector certificate.

---

## 4. T206-C — why independent tolerances cannot simply be combined

The statement

> `Delta_k <= tau_k` for every `k` implies joint safety

is false in general even when every `Q_k` is positive semidefinite.

### Exact 1x1 counterexample

Take one-dimensional matrices

`C0=[1]`,

`Q1=[1]`,

`Q2=[1]`.

Both axis endpoints are safe:

`C0-Q1=[0]`,

`C0-Q2=[0]`.

Thus the one-at-a-time sharp tolerances are

`tau1=tau2=1`.

But taking both maxima gives

`C(1,1)=[1-1-1]=[-1]`,

which is not copositive.

The exact safe region is

**`Delta1+Delta2<=1`.**

So separate solver tolerances spend a **shared** Lyapunov margin. They cannot be consumed independently unless an additional structural theorem proves that the debits do not compete.

---

## 5. T206-D — axis simplex is universally sharp from axis data alone

The previous example generalizes to arbitrary positive axis tolerances.

Fix any `tau_1,...,tau_m>0` and take the one-dimensional system

`C0=[1]`,

`Q_k=[1/tau_k]`.

Then every `Q_k` is copositive and

`C0 - tau_k Q_k=[0]`,

so the supplied axis endpoint facts hold exactly.

But

`C(Delta) = [1-sum_k Delta_k/tau_k]`.

Hence its true safe region is exactly

**`sum_k Delta_k/tau_k <= 1`.**

Therefore:

> from only `C0` copositive, each `Q_k` copositive, and the separate endpoint certificates `C0-tau_k Q_k` copositive, no universally valid theorem can enlarge the axis simplex.

Any larger simultaneous budget requires **new joint information**: a joint safe anchor, a shared reference reserve, block-separation structure, or a direct copositivity certificate.

This is an information-theoretic sharpness statement for the allocation interface, not merely a sharpness claim about one proof technique.

---

## 6. T206-E — exact ray gauge and harmonic lower bound

For a desired nonnegative error profile `d>=0`, define

`Q_d := sum_k d_k Q_k`.

The exact maximum scale on that ray is

`theta(d) := sup { t>=0 : t d in E }`.

Equivalently, if `Q_d` is nonzero on the orthant,

**`theta(d)=inf_{y>=0, y^T Q_d y>0} c0(y)/(y^T Q_d y)`.**

If `Q_d` vanishes on every nonnegative vector, set `theta(d)=+infinity`.

This is the multi-generator version of T-P5-204's scalar generalized copositive quotient: the whole requested profile is absorbed into the single copositive debit matrix `Q_d`.

Now suppose the axis endpoint certificates of Section 3 hold. Since

`C0-tau_k Q_k`

is copositive,

`q_k(y) <= c0(y)/tau_k`

for every `y>=0`.

Therefore

`y^T Q_d y = sum_k d_k q_k(y)`

`<= c0(y) sum_k d_k/tau_k`.

Hence

### Harmonic allocation lower bound

For nonzero `d`,

**`theta(d) >= 1 / (sum_k d_k/tau_k)`.**

The right-hand side is exactly the largest scale certified by the axis simplex.

The scalar construction in Section 5 attains equality, so this lower bound is universally sharp from axis endpoint information alone.

For rational `d_k,tau_k`, the certified ray scale is rational.

---

## 7. T206-F — adaptive joint anchors strictly improve the allocation polytope

The axis simplex may be conservative when debit directions act on genuinely different state directions.

### Exact 2x2 regression

Take

`C0 = diag(1,1)`,

`Q1 = diag(1,0)`,

`Q2 = diag(0,1)`.

Then

`C(Delta)=diag(1-Delta1,1-Delta2)`.

The exact safe region is the square

**`0<=Delta1<=1`, `0<=Delta2<=1`.**

The two axis endpoints `(1,0)` and `(0,1)` only certify the simplex

`Delta1+Delta2<=1`.

However the joint anchor

`v=(1,1)`

is itself safe because `C(v)=0`.

Once that single joint anchor is added, downward closure certifies the entire square.

Thus a practical allocator can be adaptive:

1. begin with axis anchors;
2. if a desired error vector lies outside their simplex, test one strategically chosen pairwise/higher-order anchor;
3. add a successful anchor to the finite library;
4. thereafter consume the enlarged region using only linear arithmetic.

This avoids repeatedly solving the same full copositivity problem for nearby support-error vectors.

---

## 8. T206-G — rational LP for the best scale inside an anchor library

Collect the safe anchors as columns of a nonnegative rational matrix

`V = [v^(1) ... v^(N)] in Q^{m x N}`.

For a target profile `d>=0`, the best scale certified by the anchor library is the LP

### Primal

maximize `t`

over `alpha>=0`, `t>=0`

subject to

`V alpha >= t d`,

`1^T alpha <= 1`.

Call its optimum `theta_anchor(d)`.

Every primal feasible point is a direct T206-A certificate, so

**`theta_anchor(d) <= theta(d)`**

where `theta(d)` is the true copositive ray threshold.

For rational `V,d`, any rational feasible `(alpha,t)` gives a sound rational error packet without solving for the exact optimum.

### LP dual

The finite LP dual is

minimize `lambda`

over `p>=0`, `lambda>=0`

subject to

`d^T p >= 1`,

`p^T v^(r) <= lambda` for every anchor `r`.

Thus a dual pair `(p,lambda)` gives an upper bound

`theta_anchor(d) <= lambda`.

When primal and dual values match, the anchor-library optimum is exactly certified by rational linear inequalities.

Important semantic boundary: this dual proves optimality **inside the current anchor polytope only**. It does not prove that larger errors fail the true Lyapunov-safe region `E`. A larger true region may exist and can be exposed by adding new joint anchors or running a direct copositivity check.

---

## 9. T206-H — relationship to T-P5-205 reference reserves

T-P5-205 is currently claimed by 古月方源 and is extracting checker-consumable reference reserves. T206 does not duplicate that derivation.

If T-P5-205 later supplies a shared reserve packet of the form

`C0 - mu R` copositive,

`R` copositive,

`kappa_k R - Q_k` copositive,

then T-P5-204 already implies the safe weighted simplex

`sum_k kappa_k Delta_k <= mu`.

T206's anchor polytope is complementary:

- it works even when no common `R` has been found;
- it can consume arbitrary joint anchors rather than only one reference-matrix domination;
- it gives an LP mechanism for combining axis, pairwise, and higher-order anchors;
- a reserve-generated safe point can itself be inserted as another anchor.

The two interfaces should therefore compose rather than compete.

---

## 10. Failure / fail-closed routing

### F1 — source-key mismatch

If anchors or `Q_k` are not from the same `C0` / selector / source key, T206-A is not applicable. Do not average across sectors.

Suggested status:

`MULTISUPPORT_COMMON_KEY_NOT_ESTABLISHED`.

### F2 — independent maxima outside the simplex

If each `Delta_k<=tau_k` but

`sum Delta_k/tau_k>1`,

this is **not** a mathematical FAIL of the requested vector. It means only

`AXIS_SIMPLEX_CERTIFICATE_NOT_APPLICABLE`.

The 2x2 square example shows such a vector may still be safe.

### F3 — LP anchor miss

If no `alpha` satisfies

`V alpha>=Delta`, `alpha>=0`, `sum alpha<=1`,

report

`ANCHOR_POLYTOPE_CERTIFICATE_NOT_FOUND`.

Do not report Lyapunov failure. A direct copositivity certificate may still exist.

### F4 — zero coordinate axis tolerance

If `tau_k=0`, the division-form axis test is invalid. Require `Delta_k=0` on that route or add a joint anchor/reference reserve that genuinely covers that coordinate.

### F5 — negative error coordinates

The present theorem is designed for cap overestimates `Delta>=0`. Tighter-than-reference components can be handled directly by downward monotonicity, but a mixed signed perturbation should first separate its positive and negative parts. Only the positive overestimate part consumes reserve.

---

## 11. Formalizable theorem statements

### T206-1 `copositive_multiSupport_exactPointwise`

For symmetric `C0,Q_k` with each `Q_k` copositive and `Delta>=0`, prove

`C0-sum Delta_k Q_k` copositive iff

for every `y>=0`,

`sum Delta_k (y^T Q_k y) <= y^T C0 y`.

### T206-2 `copositive_safeError_downward`

If `Delta'<=Delta`, both nonnegative, and `C(Delta)` is copositive, prove `C(Delta')` copositive.

### T206-3 `copositive_anchorPolytope`

Assume

- `C0` copositive;
- every `Q_k` copositive;
- every anchor `v^(r)>=0` satisfies `C(v^(r))` copositive;
- `alpha_r>=0` and `sum alpha_r<=1`;
- `Delta>=0` and `Delta_k<=sum_r alpha_r v_k^(r)`.

Prove `C(Delta)` copositive by the explicit decomposition in Section 2.

This is the primary theorem for Lean because it uses only sums, scalar multiplication, and inequalities.

### T206-4 `copositive_axisSimplex`

Specialize T206-3 to `v^(k)=tau_k e_k`.

Prefer the no-division assumptions

`Delta_k<=alpha_k tau_k`,

`alpha_k>=0`,

`sum alpha_k<=1`.

### T206-5 `axisSimplex_universalSharpness`

For arbitrary positive `tau_k`, instantiate scalar matrices

`C0=1`, `Q_k=1/tau_k`

and prove exact safety iff

`sum Delta_k/tau_k<=1`.

This regression guards against any future unsound product-box rule.

### T206-6 `anchorRay_primalCertificate`

Given rational/nonnegative `V,d,alpha,t`, assumptions

`V alpha>=t d`, `alpha>=0`, `sum alpha<=1`,

prove `t d` lies in the safe region whenever every column of `V` is a safe anchor.

The LP dual may remain an external rational arithmetic checker initially; it is not needed for the soundness theorem.

---

## 12. Checker / pipeline routing

For one common T-P5-200/T-P5-204 sector:

1. construct the reference safe matrix `C0` once;
2. keep each debit direction `Q_k` typed and source-keyed;
3. obtain axis tolerances or any safe joint anchors from direct copositivity / T-P5-205 reserve packets;
4. store anchors as rational vectors under the same source key;
5. when support solvers return certified errors `Delta_k`, first run the rational anchor LP;
6. if LP succeeds, emit the `alpha` witness and skip a new matrix copositivity search;
7. if LP fails, do **not** reject the support vector; optionally test one new joint anchor or run the direct T-P5-204 copositive gate;
8. add successful joint anchors monotonically to the library.

This creates a reusable finite-dimensional tolerance layer between support solvers and the Lyapunov checker.

---

## 13. Boundaries remaining OPEN

This review does not prove:

1. actual source-bound `C0` or `Q_k` values;
2. any actual P5 support error vector `Delta`;
3. that any current axis/joint anchor is source-bound and copositive;
4. actual selector-sector/common-key identity;
5. the T-P5-192 linear gate;
6. physical cell/tube/trajectory/global coverage;
7. Float64 or directed-rounding semantics for a producer;
8. Lean/kernel proof or axiom scan;
9. independent verification by 封不觉;
10. admission, registry, P5/P8/M4, or global Route-B closure.

All remain open.

---

## 14. Structural consequence

The multi-generator support-to-Lyapunov bridge now has a finite reusable allocation layer:

`support solver errors Delta`

`-> axis / joint safe anchors`

`-> rational anchor LP`

`-> safe convex/downward envelope`

`-> C0 - sum Delta_k Q_k copositive`

`-> T-P5-192 Lyapunov sector gate`.

The key lesson is that **per-generator tolerances are resources, not independent permissions**. Axis margins share the same Lyapunov reserve and compose through a simplex unless stronger joint structure has actually been certified.

At the same time, that simplex should not be mistaken for the true safe region: joint anchors can enlarge it substantially, and anchor-LP failure is only a certificate miss, not a mathematical obstruction.

---

## 15. Next disjoint mathematical seam

After T206 and T-P5-205, a genuinely new continuation would be to exploit **structural sparsity/block separation among the debit matrices `Q_k`** to prove when the true safe region factors into a Cartesian product or a lower-dimensional product of simplices. That would identify cases where independent support tolerances are genuinely composable rather than merely conservatively allocated.

This should only be pursued if the actual sector packet exposes such block/support structure; otherwise the anchor-polytope route already gives a sound rational allocator without inventing extra assumptions.
