---
kind: review_result
review_id: review-T-P5-248-nonlinear-chart-defect-quadratic-reserve-guyuefangyuan-20260910T1322Z
task_id: T-P5-248-NONLINEAR-CHART-DEFECT-QUADRATIC-RESERVE
reviewer: 古月方源
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-10T13:22:00Z
claim_commit: 52d387764953dcd99b09dfd1d1fad2a61f3cec4b
inspected_commit: cc3c1f109dbd8c56b63bb584ad4763be831da8bc
upstream_commits:
  - a25de2d6e01b16133af9dc40d46efcfef6731ef8  # T-P5-247 affine GL(n) chart covariance
  - f4457fd93d95b1ed58c5ec4f3fbb995a2f73fb9a  # T-P5-246 joint shifted source-target S-lemma
  - e8ba5dc69b700621893313a4202255a98267ebef  # T-P5-243 strict-margin coefficient-error budget
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_nonlinear_chart_defect_identity; add_relative_defect_cone_lmi; add_gradient_obstruction_dispatch; add_second_order_remainder_reserve_transfer; add_source_inclusion_cone_lmi; add_radial_jacobian_to_remainder_adapter; preserve_graph_vs_cone_and_source_coverage_boundaries
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact quadratic expansion; homogeneous one-constraint S-lemma; block-PSD algebra; rational 1D regressions; radial fundamental-theorem estimate; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-248 — Nonlinear chart defect: exact cone-LMI absorption, sharp gradient obstruction, and second-order recovery

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-247 proves that every exact invertible affine chart is mathematically free: source quadratic, target quadratic, S-lemma block, and metric-relative reserve move by congruence. The next distinct seam is therefore not another affine coefficient budget, but what happens when the actual chart has a nonlinear remainder.

This child studies

`y = c + P x + r(x)`,  `det(P) != 0`,

with the affine center already matched to the physical source center `c`. It gives four concrete results.

1. The pulled target defect is exactly

   `Delta_q(x,r) = 2 a0^T r + 2 x^T P^T G r + r^T G r`,

   where `a0=l+Gc` is the physical target gradient divided by two at the chart center.

2. If the producer only knows a first-order relative graph relaxation

   `r^T W r <= kappa^2 x^T M x`,

   then a finite **quadratic** debit `Delta_q <= rho x^T M x` on the whole relaxed cone is possible only if `a0=0`. In the `a0=0` branch, the optimal cone-relaxed statement is exactly a single homogeneous S-lemma LMI.

3. If `a0 != 0`, this is not a physical FAIL. It is a sharp obstruction to the first-order cone relaxation: the linear term in `r` scales like `t`, while a quadratic reserve scales like `t^2`. Graph-specific cancellation, a vertical constant reserve, or a genuinely second-order chart remainder can still close the problem.

4. For a second-order remainder `r^T W r <= beta^2 (x^T M x)^2`, the center-gradient term becomes quadratic-order and admits a fully algebraic reserve charge. A radial Jacobian condition with `Dr(0)=0` implies exactly this second-order remainder scaling.

A separate cone-LMI controls **physical source inclusion**. Target-debit absorption and source coverage are therefore not conflated.

No actual deployed nonlinear chart, same-cell/tube packet, derivative enclosure, Float64 semantics, Lean receipt, independent verification, registry mutation, or P5/P8/M4 closure is claimed.

---

# Part I — exact nonlinear pullback defect

## 1. Physical quadratic and centered affine chart

Let

`q(y) = A + 2 l^T y + y^T G y`,  `G=G^T`.

Let the physical source ellipsoid be

`E_y = { y : (y-c)^T M_y (y-c) <= R_y }`,  `M_y>0`.

Let the chart be

`phi(x) = c + P x + r(x)`,

where `P` is invertible. The exact affine reference is

`phi0(x)=c+Px`.

Define the pulled source metric

`M := P^T M_y P > 0`,

and the center target gradient

`a0 := l + G c`.

## 2. Exact defect identity

Since

`q(y+r)-q(y) = 2(l+Gy)^T r + r^T G r`,

with `y=c+Px`, we obtain

**Theorem 1 — `quadraticPullback_nonlinearDefect`.**

For every `x,r`,

`q(c+Px+r) - q(c+Px)`

`= 2 a0^T r + 2 x^T P^T G r + r^T G r`.

This is the correct packet to charge after the exact affine part has already been normalized by T-P5-247. In particular, `P` itself is not an error coefficient.

---

# Part II — first-order relative defect cone

## 3. Relative graph relaxation

Let `W=W^T>0` and `kappa>=0`. Suppose the actual graph is enclosed by

`r(x)^T W r(x) <= kappa^2 s(x)`,

where

`s(x):=x^T M x`.

For the algebraic theorem, enlarge the graph to the homogeneous cone

`C_kappa := {(x,r): r^TWr <= kappa^2 x^TMx}`.

This relaxation is deliberate: it makes the checker finite-dimensional and exact, but it may be conservative relative to the actual graph `r=r(x)`.

### `kappa=0`

Because `W>0`, `kappa=0` forces `r=0`. Then the nonlinear defect vanishes exactly. The nontrivial branch below assumes `kappa>0`.

---

## 4. Sharp center-gradient obstruction

Assume `kappa>0` and `a0 != 0`.

Claim: there is **no finite scalar `rho`** such that

`Delta_q(x,r) <= rho x^TMx`

for every `(x,r) in C_kappa`.

### Proof

Choose any nonzero `r0` with `a0^T r0>0`; for example `r0=a0`. Since `M>0`, choose some nonzero `x0` and scale it, if necessary, so that

`r0^TWr0 <= kappa^2 x0^TMx0`.

Thus `(x0,r0)` lies in the cone. Because the cone is homogeneous, `(t x0,t r0)` also lies in it for every `t>0`.

The nonlinear defect is

`Delta_q(t x0,t r0)`

`= 2t a0^T r0`

`  + t^2 [2 x0^T P^T G r0 + r0^T G r0]`.

The proposed reserve is

`rho (t x0)^T M (t x0) = rho t^2 x0^TMx0`.

Divide by `t>0` and let `t -> 0+`. The left side tends to the strictly positive number `2a0^Tr0`, while the right side tends to zero. Contradiction.

Therefore:

**Theorem 2 — `relativeChartDefect_nonzeroCenterGradient_noQuadraticConeBudget`.**

For `kappa>0`, a finite homogeneous quadratic reserve on the full relative-defect cone requires

**`a0=0`.**

### Exact meaning of the obstruction

This is **not** a claim that the physical nonlinear chart is unsafe. It says only that the relaxation `r^TWr<=kappa^2 s`, which forgets the direction of `r(x)`, cannot preserve a reserve that vanishes quadratically at the chart center when `a0!=0`.

Safe dispatches remain:

- use a positive vertical/constant reserve such as T-P5-243;
- retain graph-specific directional cancellation instead of replacing the graph by the cone;
- or prove that `r` is second-order, treated in Part IV.

---

# Part III — exact homogeneous LMI when `a0=0`

## 5. Target-defect LMI

Assume `a0=0`, `kappa>0`, and choose `rho>=0`.

Then the desired implication is

`r^TWr <= kappa^2 x^TMx`

`=> 2x^T P^T G r + r^T G r <= rho x^TMx`.

The cone constraint has a strict point: take `r=0` and any `x!=0`. Hence the one-constraint homogeneous S-lemma is lossless.

For a multiplier `tau>=0`, subtract `tau` times the cone slack from the desired nonnegative quadratic:

`rho x^TMx - 2x^TP^TGr - r^TGr`

`- tau(kappa^2 x^TMx-r^TWr)`.

Its block matrix in `(x,r)` is

**`T_target(rho,tau) :=`**

`[[ (rho-tau*kappa^2) M,   -P^T G ],`

` [ -G P,                  tau W-G ]]`.

Therefore:

**Theorem 3 — `relativeChartDefect_quadraticBudget_iff_LMI`.**

Under `M>0`, `W>0`, `kappa>0`, `G=G^T`, and `a0=0`, the following are equivalent:

1. `Delta_q(x,r) <= rho x^TMx` for every `(x,r) in C_kappa`;
2. there exists `tau>=0` such that `T_target(rho,tau)>=0`.

The forward implication is the lossless homogeneous S-lemma; the reverse implication is direct expansion and needs no optimizer.

### Checker boundary

For a rational packet, a producer may submit rational `rho,tau`. The checker only verifies one symmetric PSD matrix. No square root, inverse, pseudoinverse, floating eigenvector, or chart Jacobian inversion is required.

The exact existence of a rational `tau` at a singular sharp boundary is a separate formalization detail; soundness never depends on the converse if the producer supplies a valid rational multiplier.

---

## 6. One-dimensional exact regression

Take

`M=W=P=1`, `G=1`, `a0=0`, `kappa=1/2`.

Then

`Delta_q=2xr+r^2`,  `|r|<=|x|/2`.

The exact worst-case ratio is

`Delta_q/x^2 = 2*(1/2)+(1/2)^2 = 5/4`.

At `rho=5/4`, choose `tau=3`. Then

`T_target = [[1/2,-1],[-1,2]] >=0`

with determinant zero. Thus the LMI reaches the exact sharp cone boundary.

---

# Part IV — second-order remainder restores quadratic absorption

## 7. Second-order graph packet

Assume instead that on a bounded chart domain

`s=x^TMx <= R_x`

we have the stronger remainder bound

**`r^TWr <= beta^2 s^2`**,  `beta>=0`.

This is the natural remainder scaling when `P` is the true first derivative of a `C^1`/`C^{1,1}` chart at the center.

Let `sigma>=0` satisfy the inverse-free dual-gradient matrix inequality

**`sigma W - a0 a0^T >=0`.**

Then for every `r`,

`(a0^T r)^2 <= sigma r^TWr`.

Hence on the second-order graph packet,

`|a0^T r|^2 <= sigma beta^2 s^2`.

Choose `c0>=0` satisfying the square-only scalar gate

**`c0^2 >= 4 sigma beta^2`.**

Then

**`2 a0^T r <= c0 s`.**

No square root is required by the checker.

---

## 8. Reduce the remaining terms to the first-order cone

Choose any `kappa>=0` satisfying

**`beta^2 R_x <= kappa^2`.**

Since `s<=R_x`,

`r^TWr <= beta^2 s^2 <= beta^2 R_x s <= kappa^2 s`.

Thus the bilinear/Hessian portion

`2x^TP^TGr+r^TGr`

may be charged by Theorem 3 whenever a producer supplies `rho,tau` with

`T_target(rho,tau)>=0`.

Combining with the center-gradient budget gives

**`Delta_q(x,r) <= (c0+rho) s`.**

Therefore:

**Theorem 4 — `secondOrderChartDefect_quadraticReserveTransfer`.**

Suppose on `s<=R_x` the affine-reference target already satisfies

`q(c+Px) <= -epsilon s`,

with `epsilon>=0`. If

- `r^TWr <= beta^2 s^2`;
- `sigma W-a0a0^T>=0`;
- `c0>=0`, `c0^2>=4 sigma beta^2`;
- `beta^2 R_x<=kappa^2`;
- some `rho,tau>=0` satisfy `T_target(rho,tau)>=0`;
- and `c0+rho<=epsilon`;

then

**`q(c+Px+r(x)) <= 0`**

throughout the same chart domain.

This is the requested recovery mechanism: a nonzero center gradient is fatal only for a first-order direction-forgetting cone. Once the chart remainder is genuinely second-order, the gradient contribution itself becomes quadratic and can consume finite reserve.

---

## 9. Radial Jacobian route to the second-order packet

Let `r(0)=0` and `Dr(0)=0`. Assume the chart domain is star-shaped about zero and, along every radial segment, the derivative obeys the metric operator inequality

**`Dr(x)^T W Dr(x) <= L^2 (x^TMx) M`.**

For fixed `x`, set `gamma(t)=r(tx)`. Then

`gamma'(t)=Dr(tx)x`.

The matrix inequality gives

`||gamma'(t)||_W <= L t (x^TMx)`.

By the fundamental theorem of calculus and the triangle inequality,

`||r(x)||_W`

`<= integral_0^1 L t (x^TMx) dt`

`= (L/2) x^TMx`.

Therefore

**`r(x)^TWr(x) <= (L^2/4)(x^TMx)^2`.**

So one may take `beta=L/2`.

This derivative-to-remainder leaf is analytically separate from the finite-dimensional LMI checker: source/interval machinery may certify the Jacobian inequality, while the downstream target theorem consumes only the resulting scalar `beta` packet.

A weaker uniform derivative inequality

`Dr(x)^T W Dr(x) <= kappa^2 M`

with only `r(0)=0` similarly yields the first-order relative packet

`r(x)^TWr(x) <= kappa^2 x^TMx`.

---

# Part V — source-domain inclusion is a separate exact LMI

## 10. Why target absorption is not coverage

Even if the target defect is small, the nonlinear chart may move a point outside the physical source ellipsoid. This must be checked separately.

The affine pullback source energy is

`s=x^T M x`,  `M=P^T M_y P`.

The nonlinear image source energy is

`(Px+r)^T M_y(Px+r)`.

Assume the first-order cone packet

`r^TWr <= kappa^2 s`,  `kappa>0`.

For a desired expansion factor `chi>=0`, ask whether

`(Px+r)^T M_y(Px+r) <= chi s`

for every pair in the cone.

By the same homogeneous S-lemma, this is equivalent to existence of `tau_s>=0` with

**`T_source(chi,tau_s) :=`**

`[[ (chi-1-tau_s*kappa^2) M,   -P^T M_y ],`

` [ -M_y P,                     tau_s W-M_y ]] >=0`.

Therefore:

**Theorem 5 — `relativeChartDefect_sourceExpansion_iff_LMI`.**

Under `M_y>0`, `W>0`, `P` invertible and `kappa>0`, the nonlinear source expansion factor `chi` is certified exactly on the relaxed cone by the above PSD block.

Consequently, if the chart domain is restricted to

`x^TMx <= R_y/chi`

for some `chi>0` satisfying this gate, then every nonlinear image lies inside the physical ellipsoid `E_y`.

### Matched-metric regression

If `P=I` and `W=M_y=M`, the exact factor is

`chi=(1+kappa)^2`.

For `kappa=1/2`, take `chi=9/4`, `tau_s=3`. Then the scalar 2x2 factor is again

`[[1/2,-1],[-1,2]]>=0`.

Thus the LMI recovers the exact triangle-inequality factor but does so in a form that generalizes to anisotropic `P,W,M_y` without a matrix square root.

---

# Part VI — dispatcher and counterexamples

## 11. Dispatcher

A safe nonlinear-chart consumer should branch as follows.

**Exact affine remainder:** `r=0`. Use T-P5-247; zero chart cost.

**First-order relative remainder, center gradient zero:** use `T_target(rho,tau)>=0` and spend the resulting `rho` against a quadratic reserve.

**First-order relative remainder, center gradient nonzero:** do not manufacture a quadratic budget from a direction-forgetting cone. Use either a constant/vertical reserve, retain graph direction, or improve the source theorem to a second-order remainder.

**Second-order remainder:** use the dual-gradient square gate plus the homogeneous LMI for the remaining bilinear/Hessian terms.

**Any branch that needs physical ellipsoid coverage:** additionally check `T_source(chi,tau_s)>=0` or a stronger exact source-specific inclusion theorem. Target safety and source inclusion are distinct obligations.

---

## 12. Regression: first-order gradient obstruction is real

In one dimension take `P=M=W=1`, `G=0`, `a0=1`, `kappa=1`.

The cone contains `r=x>0`. The chart target defect is

`Delta_q=2r=2x`.

No finite `rho` can satisfy `2x<=rho x^2` for all sufficiently small positive `x`.

A checker that applies Young's inequality with a fixed additive constant can hide this scaling mismatch, but then it has switched from a quadratic reserve to a **vertical** reserve. The two budget types must remain typed separately.

---

## 13. Regression: first-order defect can consume a finite quadratic reserve when `a0=0`

Take `P=M=W=1`, `G=-2`, `a0=0`, `kappa=1/2`.

For the affine target `q_aff(x)=-2x^2`, the nonlinear defect is

`Delta_q=-4xr-2r^2`.

Over `|r|<=|x|/2`, the maximum occurs at `r=-x/2` and equals

`(3/2)x^2`.

The exact LMI uses `rho=3/2`, `tau=2`:

`T_target=[[1,2],[2,4]]>=0`.

Hence the original reserve `2x^2` leaves a strict residual reserve `(1/2)x^2` after the worst allowed first-order chart defect.

---

## 14. Regression: second-order remainder defeats the linear-scaling obstruction

Take one dimension with `W=M=1`, `a0=1`, and impose

`r^2 <= x^4`.

Then `beta=1`, `sigma=1`, and the square gate permits `c0=2`. Indeed

`2a0 r <= 2|r| <= 2x^2`.

The same nonzero center gradient that made the first-order cone impossible now costs a finite quadratic debit because the chart remainder vanishes to second order.

---

# Part VII — Lean decomposition

## 15. Suggested theorem leaves

The first Lean pass should avoid differential calculus and formalize only exact finite-dimensional algebra.

Suggested leaves:

- `quadraticPullback_nonlinearDefect`
- `relativeChartDefect_nonzeroCenterGradient_noQuadraticConeBudget`
- `relativeChartDefect_LMI_sound`
- `relativeChartDefect_quadraticBudget_iff_LMI` (converse only if a suitable homogeneous S-lemma is already available)
- `dualGradient_psd_imp_inner_sq_le`
- `secondOrderRemainder_gradient_budget`
- `secondOrderRemainder_to_relative_on_ball`
- `secondOrderChartDefect_quadraticReserveTransfer`
- `relativeChartDefect_sourceExpansion_LMI_sound`
- `relativeChartDefect_sourceExpansion_iff_LMI` (again, converse may be staged)

The radial calculus adapters can be separate later leaves:

- `uniformJacobianMetricBound_imp_relativeRemainder`
- `radialJacobianLinearGrowth_imp_secondOrderRemainder`.

A producer-first checker needs only the sound PSD directions; formalizing the lossless S-lemma converse is useful for completeness but is not required for certificate soundness.

---

# Part VIII — unresolved boundaries

## 16. What is still open

This child does **not** prove that the real P5 source adapter has a nonlinear chart packet. In particular, it does not provide:

- a same-key deployed `P,c,r,Dr,M_y,W`;
- proof that `P` is the exact center Jacobian of the runtime/source chart;
- a bound on `Dr` or on the second derivative/Lipschitz constant;
- star-shaped radial-segment coverage of the actual tube/cell;
- exact relation between decoded Float64 chart code and mathematical `r`;
- a source-domain `chi` packet for the real source ellipsoid;
- a target reserve `epsilon` on the same physical cell;
- Lean/kernel compilation;
- independent verification by 封不觉;
- admission or registry eligibility.

Failure of either cone-LMI is **not** physical failure. It means only that the chosen direction-forgetting conic relaxation is too coarse. The next fallback is graph-specific sector/cross-correlation information, not provenance work and not automatic theorem rejection.

## 17. Recommended next seam

The mathematically distinct next question is **graph-specific sector transport** for the case where the cone-LMI fails but the source can certify directional information such as

`r(x)=B(x)x`,

with a symmetric/sector enclosure on `B(x)` or an exact orthogonality/cancellation relation with `a0+GPx`.

Such a theorem could be strictly less conservative than the cone relaxation and would be justified only if a real source packet exposes directional Jacobian/sector data. Otherwise the correct next action is source binding for `(r,Dr)` rather than inventing another optimizer.

Status remains **CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding**.