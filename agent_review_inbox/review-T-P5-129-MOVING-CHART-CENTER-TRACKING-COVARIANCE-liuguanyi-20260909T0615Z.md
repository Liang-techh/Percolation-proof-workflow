---
kind: review_result
review_id: review-T-P5-129-moving-chart-center-tracking-covariance-liuguanyi-20260909T0615Z
task_id: T-P5-129-MOVING-CHART-CENTER-TRACKING-COVARIANCE
reviewer: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-09T06:15:00Z
claim_commit: af180720427d9be27f9ae78b2762d4a09c3608e7
inspected_commit: adc4cbc2ff740e7a79f536f0707fcde52f844db5
upstream_reviews:
  - path: agent_review_inbox/review-T-P5-120-MOVING-CHART-CONSERVATIVE-POWER-PULLBACK-liuguanyi-20260909T0302Z.md
    commit: 282c801638022fcb40220e1f92f44f3ec0a3993d
  - path: agent_review_inbox/review-T-P5-126-MOVING-CHART-RECENTER-COERCIVITY-liuguanyi-20260909T0518Z.md
    commit: 5777eb0b29cab0c42ee77b072d270efa2ef0a98f
  - path: agent_review_inbox/review-T-P5-127-MOVING-RECENTER-ENVELOPE-TRACKING-guyuefangyuan-20260909T0530Z.md
    commit: 8771585ea270185eaecabbcbef960b0fb2579a87
  - path: agent_review_inbox/review-T-P5-128-ROOT-FREE-ELLIPSOID-SUM-AND-CENTER-TRACKING-kuangmanmozun-20260909T0538Z.md
    commit: 274afb22d19b47aa467684899cdb6017c88c4bd9
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_frame_relative_center_speed_and_fixed_metric_time_slab_then_bind_signed_temporal_frame_mismatch_packet
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: none; finite-dimensional chain-rule, quadratic-form, integral Jensen/Cauchy, and exact order algebra only
exit_code: n/a
---

# T-P5-129 — moving-chart center tracking as a frame-relative metric theorem

## 0. Narrowing after reading the newest inbox

The originally selected seam was the compatibility of T-P5-126 with the new moving-center results. After the claim was recorded, the latest T-P5-127 review was inspected in detail. Its Section 10 already proves the exact center-level chain-rule identities

`Htilde_* = J_*^T H_* J_*`

and

`partial_t grad_z Ftilde(t,z_*) = J_*^T [g_* + H_* T_t(t,z_*)]`,

and it observes that the nonlinear connection term and `J_t^T grad F` vanish at an exact physical critical center.

To avoid duplicating that work, this review **consumes** those identities and proves the next missing mathematical bridge:

1. the correct temporal quantity is the signed **frame-relative mismatch covector**
   `m_* := g_* + H_* tau_*`, with `tau_*:=T_t(t,z_*)`;
2. under the congruence metric `M_*=J_*^T P J_*`, center-speed certification has no Jacobian condition-number loss;
3. the optimal dual constant is exactly invariant for a bijective chart and can be strictly smaller on an immersed tangent subspace;
4. a frame that follows the physical critical center makes the normalized center exactly stationary by signed cancellation;
5. a fixed-metric time-slab corollary gives a root-free finite-time displacement budget which plugs directly into T-P5-128.

This is source-independent mathematics only. It does not claim an actual P5 temporal packet, chart implementation, controller/reference schedule, coverage, Float64 semantics, P8 flowpipe, Lean receipt, independent verification, admission, or registry closure.

---

## 1. Setup and object types

Let physical configuration space be a finite-dimensional real inner-product space, and let `P` be symmetric positive definite. Write

`Q_P(y) := y^T P y`.

Let a time-dependent chart be

`q = T(t,z)`

with spatial Jacobian

`J(t,z) := D_z T(t,z)`

and chart/frame velocity

`tau(t,z) := partial_t T(t,z)`.

Let the scalar potential be `F(t,q)`. Suppose a branch `z_*(t)` is bound to an **actual physical critical center**

`q_*(t) := T(t,z_*(t))`,

`grad_q F(t,q_*(t)) = 0`.

At that center define

`H_* := Hess_q F(t,q_*)`,

`g_* := partial_t grad_q F(t,q_*)`

where `partial_t` is taken at fixed physical `q`, and

`J_* := J(t,z_*)`,

`tau_* := tau(t,z_*)`.

Define the pulled metric

**(1.1)**

`M_* := J_*^T P J_*`,

`Q_M(eta) := eta^T M_* eta = Q_P(J_* eta)`.

If `J_*` is injective on normalized coordinates, then `M_*` is positive definite.

The crucial signed temporal object is

**(1.2) FRAME-RELATIVE MISMATCH**

`m_* := g_* + H_* tau_*`.

By T-P5-127 Section 10, the pulled temporal-gradient covector at the exact critical center is

**(1.3)**

`gtilde_* := partial_t grad_z(F o T)(t,z_*) = J_*^T m_*`.

The two summands in (1.2) must remain signed until after they are combined.

---

## 2. Exact center Hessian: global chart curvature disappears locally

T-P5-126 proves the general nonlinear Hessian identity

`Hess_z(F o T)[eta,eta]`

`= Hess_q F[J eta,J eta]`

`  + <grad_q F, D_z^2 T[eta,eta]>`.

At the physical critical center `grad_q F(t,q_*)=0`. Therefore

**(2.1)**

`Htilde_* = J_*^T H_* J_*`

exactly.

Assume the physical Hessian has the pointwise coercive lower bound

**(2.2)**

`y^T H_* y >= 2 mu Q_P(y)`

for `mu>0`. Then (2.1) gives

**(2.3)**

`eta^T Htilde_* eta >= 2 mu Q_M(eta)`.

So the center-local tracking theorem uses the **same `mu`**, even when the nonlinear chart required a degraded global-cell constant `mu_z` in T-P5-126.

This distinction matters:

- global existence/uniqueness of the recentered point still needs the whole-cell T-P5-126 connection-defect bound;
- once the exact physical critical center is established, the local center-speed equation does not pay that chart-curvature debit again.

---

## 3. Pure algebra leaf: frame-relative center-speed certificate

The calculus layer gives, by differentiating the normalized criticality equation,

**(3.1)**

`Htilde_* z_*dot + gtilde_* = 0`.

Using (1.3) and (2.1), this is

**(3.2)**

`J_*^T H_* J_* z_*dot + J_*^T m_* = 0`.

For the formal/checker core, (3.2) can simply be taken as a typed algebraic premise; no inverse or implicit-function machinery is needed in the algebra leaf.

Assume a nonnegative rational/real constant `G_frame` satisfies the tangent-image dual bound

**(3.3)**

`<m_*, J_* eta>^2 <= G_frame Q_P(J_* eta)`

for every normalized direction `eta`.

Equivalently, using (1.1),

`<J_*^T m_*, eta>^2 <= G_frame Q_M(eta)`.

Put `h=z_*dot`. Taking the inner product of (3.1) with `h`, then using (2.3), gives

`2 mu Q_M(h)`

`<= h^T Htilde_* h`

`= -<gtilde_*,h>`.

Square and apply (3.3):

`4 mu^2 Q_M(h)^2 <= <gtilde_*,h>^2 <= G_frame Q_M(h)`.

If `Q_M(h)=0`, the conclusion is immediate. Otherwise cancel the positive scalar `Q_M(h)`.

Hence:

### Theorem A — frame-relative center-speed bound

Under (2.2), (3.1), and (3.3), with `J_*` injective,

**(3.4)**

`4 mu^2 Q_M(z_*dot) <= G_frame`.

By the kinematic identity

**(3.5)**

`q_*dot = tau_* + J_* z_*dot`,

we have the exact metric identity

**(3.6)**

`Q_M(z_*dot) = Q_P(q_*dot - tau_*)`.

Therefore the same theorem can be written directly in physical variables as

**(3.7) FRAME-RELATIVE PHYSICAL SPEED**

`4 mu^2 Q_P(q_*dot - tau_*) <= G_frame`.

No Jacobian inverse, singular value, condition number, square root, eigenvalue, or matrix square root appears.

---

## 4. Exact dual-constant transport: no condition-number penalty

Define the best full physical dual constant for the signed mismatch `m_*` by the information statement

`<m_*,y>^2 <= G_phys Q_P(y)` for all physical `y`.

Then substituting `y=J_* eta` immediately gives (3.3) with

**(4.1)**

`G_frame <= G_phys`

at the level of optimal constants.

More precisely:

### Theorem B — tangent-restricted dual constant

The optimal normalized constant is exactly

`sup_{eta != 0} <m_*,J_*eta>^2 / Q_P(J_*eta)`,

which is the physical dual norm restricted to `range(J_*)`.

If `J_*` is bijective, `range(J_*)` is the whole physical space, so the optimal normalized and physical constants are **equal**.

Thus a bijective chart carries no condition-number tax when both the covector and metric are transported correctly by

`m -> J^T m`,

`P -> J^T P J`.

If `J_*` is an immersion into a larger physical space, the tangent-restricted constant may be strictly smaller than the full physical one. A producer may therefore certify (3.3) directly on the tangent image instead of paying for irrelevant normal directions.

This is a useful typed distinction: full physical criticality and tangent-only dual control are different obligations.

---

## 5. Exact frame-following cancellation

Suppose the physical critical-center identity from T-P5-127 holds:

**(5.1)**

`H_* q_*dot + g_* = 0`.

If the chart is chosen so that its frame velocity at the center follows that physical center,

**(5.2)**

`tau_* = q_*dot`,

then by (1.2)

`m_* = g_* + H_* tau_*`

`    = g_* + H_* q_*dot`

`    = 0`.

Therefore

`gtilde_*=J_*^T m_*=0`.

Since `Htilde_*` is positive definite on normalized coordinates, (3.1) implies

**(5.3)**

`z_*dot = 0`.

Conversely, the kinematic identity (3.5) shows that `z_*dot=0` implies `q_*dot=tau_*`.

Hence:

### Theorem C — center-following frame equivalence

For an injective chart at an exact physical critical center,

**`z_*dot=0  <->  q_*dot=tau_*`.**

When the physical critical-center equation holds, either side is equivalent to the signed mismatch condition

**`m_*=g_*+H_*tau_*=0`.**

This is not merely a coordinate convenience. It identifies the exact quantity a source adapter should minimize or enclose if the purpose of the moving chart is to reduce recenter motion.

---

## 6. Hard regression: bounding the two frame terms separately invents drift

Take one dimension with

`F(t,q) = (q-t)^2 / 2`.

Then the physical critical center is

`q_*(t)=t`,

and at the center

`H_*=1`,

`g_* = partial_t grad_q F = -1`,

`q_*dot=1`.

Choose the moving chart

`T(t,z)=z+t`.

Then

`J_*=1`,

`tau_*=1`,

and the pulled potential is simply

`Ftilde(t,z)=z^2/2`.

So the normalized critical center is exactly

`z_*(t)=0`,

`z_*dot=0`.

The signed frame mismatch is

**(6.1)**

`m_* = g_* + H_* tau_* = -1+1 = 0`.

If an adapter first replaces `g_*` and `H_*tau_*` by separate absolute envelopes, it sees two nonzero size-1 terms and manufactures a positive center-speed budget despite the exact normalized center being stationary.

Therefore the trusted/source pipeline should form

**`m_*=g_*+H_*tau_*` signed first, then enclose it.**

This is the temporal analogue of the signed cancellation discipline already used for residual cross-multiplication and gyroscopic/conservative work terms elsewhere in P4/P5.

---

## 7. Fixed-metric finite-time displacement without square roots

The pointwise metric `M_*(t)` can vary with time. To obtain a finite-time displacement in one fixed normalized metric, introduce a fixed SPD matrix `M0` and

`Q0(x):=x^T M0 x`.

Assume on a time slab `[t0,t1]`:

1. the same differentiable critical-center branch remains in the certified chart/source cell;
2. `mu>0` is a uniform physical center-Hessian constant;
3. the tangent metric has a uniform lower comparison

   **(7.1)** `M_*(t) >= a M0` with `a>0`;

4. the signed frame-mismatch packet gives

   **(7.2)** `G_frame(t) <= Gbar` with `Gbar>=0`.

Theorem A gives pointwise

`4 mu^2 Q_M(t)(z_*dot) <= Gbar`.

Using (7.1),

**(7.3)**

`4 mu^2 a Q0(z_*dot) <= Gbar`.

Let `h=t1-t0>=0`. Since

`z_*(t1)-z_*(t0) = integral_{t0}^{t1} z_*dot(t) dt`,

quadratic Jensen/Cauchy gives

`Q0(z_*(t1)-z_*(t0))`

`<= h integral_{t0}^{t1} Q0(z_*dot(t)) dt`.

Combining with (7.3) yields the fully root-free slab bound

### Theorem D — fixed-metric frame-relative displacement

**(7.4)**

`4 mu^2 a Q0(z_*(t1)-z_*(t0)) <= h^2 Gbar`.

A sharper integral-budget form is available if the producer supplies

`integral G_frame(t) dt <= Gint`:

**(7.5)**

`4 mu^2 a Q0(z_*(t1)-z_*(t0)) <= h Gint`.

Again the final consumer needs no square root or inverse.

---

## 8. Direct plug into T-P5-128's sharp root-free outer-cell gate

Suppose an outer normalized ellipsoid is centered at `c` and the initial center satisfies

**(8.1)**

`Q0(z_*(t0)-c) <= A`.

From Theorem D define

`S := 4 mu^2 a`,

`G := h^2 Gbar`

(or `G:=h Gint` in the integral version), so that

`S Q0(z_*(t1)-z_*(t0)) <= G`.

T-P5-128 applies directly to

`a_vec := z_*(t0)-c`,

`b_vec := z_*(t1)-z_*(t0)`.

For desired outer radius `R`, define

**(8.2)**

`D := S (R-A) - G`.

The two polynomial checks

**(8.3)** `D >= 0`,

**(8.4)** `D^2 >= 4 S A G`

imply

**(8.5)**

`Q0(z_*(t1)-c) <= R`.

This provides a clean four-layer chain:

`signed physical temporal/frame mismatch`

`-> frame-relative normalized center speed`

`-> fixed-metric finite-time center drift`

`-> sharp root-free outer-cell containment`.

No auxiliary Young parameters `p,q` are needed in the final containment checker.

---

## 9. Rank-deficient charts: exact boundary of the theorem

There are two distinct rank issues which should not be conflated.

### 9.1 Injectivity of `J` on normalized coordinates

For `M_*=J_*^T P J_*` to be positive definite, `J_*` must be injective on normalized coordinates. If `J_* eta=0` for nonzero `eta`, then `Q_M(eta)=0`, and Theorem A cannot control that normalized direction.

### 9.2 Physical criticality from chart criticality

Even if `J_*` is injective as an immersion `R^k -> R^n`, `J_*^T grad F=0` need not imply `grad F=0` when `k<n`. In that case the T-P5-127/T-P5-126 center cancellation cannot be invoked merely from chart criticality.

There are two valid routes:

- independently bind `q_*=T(t,z_*)` as a **physical** critical center (`grad_q F=0`); or
- use a square/full-rank chart for which `ker(J_*^T)=0`, so chart criticality implies physical criticality.

Without one of these, the terms

`<grad F,D^2T[eta,eta]>`

and

`J_t^T grad F`

need not vanish at the chart critical point.

---

## 10. Minimal theorem decomposition for Lean/formal consumption

The clean formal split is:

1. `critical_pullback_hessian_congruence`
   - premise `gradF=0`;
   - conclusion `Htilde = J^T H J` at the center.

2. `frame_temporal_covector_identity`
   - consumes the T-P5-127 calculus identity;
   - `gtilde = J^T (g + H*tau)` at a physical critical center.

3. `frame_relative_center_speed_algebra`
   - pure finite-dimensional algebra;
   - premises `Htilde h + gtilde=0`, `Htilde >= 2mu M`, dual square bound;
   - conclusion `4mu^2 Q_M(h) <= G`.

4. `pullback_metric_relative_velocity_identity`
   - `M=J^T P J`, `qdot=tau+Jh`;
   - conclusion `Q_M(h)=Q_P(qdot-tau)`.

5. `frame_following_center_stationary`
   - signed `g+H*tau=0` plus positive-definite pulled Hessian;
   - conclusion `h=0`.

6. `fixed_metric_center_drift_integral`
   - `M(t)>=a M0`, pointwise speed budget;
   - conclusion `4mu^2 a Q0(delta z)<=h^2 Gbar` or the integral-budget variant.

7. consume T-P5-128 unchanged for outer-cell containment.

Items 3–5 are especially suitable as small algebraic sidecars before any heavy calculus/ODE formalization.

---

## 11. Suggested typed source/interface packet

A minimal actual producer packet for this lane should bind, under one `centerKey/chartKey/potentialKey/timeSlabKey`:

- physical SPD metric `P`;
- physical critical center `q_*(t)` or a square-chart proof that normalized criticality implies it;
- chart center `z_*(t)` with `q_*=T(t,z_*)`;
- `J_* = D_zT(t,z_*)` and frame velocity `tau_*=partial_tT(t,z_*)`;
- physical Hessian `H_*` and temporal gradient `g_*=partial_t grad_q F`;
- the **signed assembled** mismatch `m_*=g_*+H_*tau_*`;
- physical center Hessian coercivity `H_*>=2mu P`;
- tangent-image dual bound for `m_*`, preferably before replacing it by a full-space norm bound;
- for finite-time use, a fixed `M0`, lower comparison `J_*^TPJ_*>=aM0`, and either `Gbar` or an integral budget for `G_frame`;
- same-cell/time-slab coverage for the critical-center branch.

The packet should not separately budget `g_*` and `H_*tau_*` unless it also proves that no useful signed cancellation exists.

---

## 12. What remains open

This result does **not** prove any deployed source identity. In particular, the following remain open:

- actual P5 `F`, `H_*`, `g_*`, `T`, `J_*`, `tau_*`, and center-key binding;
- whether the deployed chart is square/bijective, an immersion with separately proven physical criticality, or something else;
- whole-time-slab persistence of the critical branch inside the same source-valid cell;
- actual rational/interval values of `mu`, `a`, and `G_frame`;
- chart/runtime/Float64/controller/reference semantics;
- FD/reference halo and P8 flowpipe/existence coverage;
- Lean/kernel compilation and `#print axioms` receipt;
- 封不觉 independent verification;
- admission, registry, and formal-certificate gates.

The global nonlinear-chart coercivity theorem from T-P5-126 remains necessary to establish/retain the center in the first place. The present theorem only sharpens the **center-tracking layer after physical criticality is already justified**.

---

## 13. Bottom line

The mathematically correct dynamic chart quantity is not `g_*` and not `H_*tau_*` separately. It is the signed frame mismatch

**`m_* = g_* + H_* tau_*`.**

With congruence metric `M_*=J_*^TPJ_*`, the center-speed theorem is

**`4 mu^2 Q_P(q_*dot-tau_*) = 4 mu^2 Q_M(z_*dot) <= G_frame`.**

Thus a moving chart that follows the physical critical center makes the normalized center stationary exactly, with no condition-number or chart-curvature tax at the center. Over a finite time slab, a fixed lower metric comparison converts this into

**`4 mu^2 a Q0(delta z_*) <= h^2 Gbar`,**

which feeds directly into T-P5-128's sharp polynomial outer-cell gate.

Status remains `CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending` until an actual same-key temporal/frame source packet and all ordinary coverage/formal gates are supplied.
