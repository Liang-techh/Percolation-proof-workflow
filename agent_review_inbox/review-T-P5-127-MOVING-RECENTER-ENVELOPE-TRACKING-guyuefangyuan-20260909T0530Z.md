---
kind: review_result
review_id: review-T-P5-127-moving-recenter-envelope-tracking-guyuefangyuan-20260909T0530Z
task_id: T-P5-127-MOVING-RECENTER-ENVELOPE-TRACKING
reviewer: 古月方源
source_agent: 古月方源
created_at: 2026-09-09T05:30:00Z
claim_commit: 367b5ec7d9c884a3e7d2fdc8f4193b91ad9cbb14
inspected_commit: 5777eb0b29cab0c42ee77b072d270efa2ef0a98f
upstream_reviews:
  - path: agent_review_inbox/review-T-P5-124-CENTER-FORCE-MISMATCH-MIXED-COERCIVITY-guyuefangyuan-20260909T0424Z.md
    commit: c0934c14a71d4ee588ea910c018a6a5411520494
  - path: agent_review_inbox/review-T-P5-125-STRONG-CONVEX-RECENTER-EXISTENCE-honglianmozun-20260909T0455Z.md
    commit: 119338bc1d5cc8ab789ce2bc9f55fd656dba3c29
  - path: agent_review_inbox/review-T-P5-126-MOVING-CHART-RECENTER-COERCIVITY-liuguanyi-20260909T0518Z.md
    commit: 5777eb0b29cab0c42ee77b072d270efa2ef0a98f
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_two_time_center_drift_and_potential_gap_envelope_identity_then_bind_same_cell_temporal_gradient_hessian_packet
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: none; finite-dimensional strong-monotonicity, implicit-function, Taylor, and exact quadratic algebra only
exit_code: n/a
---

# T-P5-127 — moving recenter envelope tracking without inverse or double-counted center power

## 0. Bottleneck selected

T-P5-125 proves that on one fixed certified ellipsoidal cell, a strong-Hessian packet plus

`B < 4 mu^2 R`

forces a unique interior critical center. T-P5-126 proves how that frozen-time recenter certificate transports through affine/nonlinear charts, but deliberately leaves open the time-dependent question: if the shaped potential and hence its unique critical center vary with time, how does the center move, how can its motion stay inside the certified tube, and what power term must be paid in a time-dependent recentered storage?

The answer has an important structural split:

1. center motion can be bounded **without writing a Hessian inverse**;
2. a two-time center-displacement theorem is available even without differentiability of the center path;
3. for the exact potential-gap storage `W(t,q)=F(t,q)-F(t,q_*(t))`, the chain rule contains **no separate `q_*dot` debit** because `grad F(t,q_*)=0`;
4. however, explicit time dependence of `F` remains through `partial_t F(t,q)-partial_t F(t,q_*)` and can encode center motion;
5. that temporal power splits into a center-linear term plus a temporal-Hessian term. The center-linear term generically needs an additive floor, while the temporal-Hessian term can be absorbed relatively if a signed same-segment bound is available;
6. the additive floor is sharp and cannot be removed from these premises by a better Young inequality.

This is a mathematical child only. No deployed P5 temporal source packet, controller/reference schedule, chart packet, Float64 semantics, P8 flowpipe, Lean receipt, independent verification, admission, or registry closure is claimed.

---

## 1. Uniform same-cell setup

Let `P` be a fixed symmetric positive-definite matrix and

`Q(x) := x^T P x`.

Let `I` be a time interval and `E` a convex cell on which `F(t,q)` is `C^1` in time and `C^2` in space, with the required mixed derivatives continuous whenever they are used below.

Assume a uniform strong-Hessian lower bound

**(1.1)**

`y^T Hess_q F(t,z) y >= 2 mu Q(y)`

for every `t in I`, `z in E`, and vector `y`, with `mu>0`.

Assume T-P5-125 (or an equivalent existence theorem) supplies for each relevant time a unique interior critical point

**(1.2)**

`q_*(t) in int(E)`,  `grad_q F(t,q_*(t))=0`.

The same-cell hypothesis matters: all segment arguments below must remain inside the cell on which (1.1) and the temporal packets are valid.

---

## 2. Two-time center drift: no differentiability and no inverse needed

Take two times `t0,t1`. Write

`q0 := q_*(t0)`, `q1 := q_*(t1)`, `d := q1-q0`.

Define the gradient change at the old center

**(2.1)**

`g01 := grad F(t1,q0) - grad F(t0,q0)`.

Since `grad F(t0,q0)=0`, this is simply `grad F(t1,q0)`.

Assume a dual quadratic packet

**(2.2)**

`<g01,y>^2 <= G01 Q(y)`

for all vectors `y`, with `G01>=0`.

Strong monotonicity of the `t1` gradient on the segment from `q0` to `q1` gives

`<grad F(t1,q1)-grad F(t1,q0), d> >= 2 mu Q(d)`.

Using `grad F(t1,q1)=0`,

**(2.3)**

`-<g01,d> >= 2 mu Q(d)`.

Square (2.3) and use (2.2):

`4 mu^2 Q(d)^2 <= <g01,d>^2 <= G01 Q(d)`.

If `Q(d)=0`, positive definiteness gives `d=0`. Otherwise cancel the positive scalar `Q(d)`. Thus the final theorem can be stated root-free as

**(2.4) TWO-TIME CENTER DRIFT**

`4 mu^2 Q(q_*(t1)-q_*(t0)) <= G01`.

No Hessian inverse, square root, eigenvalue, or condition number appears.

A useful point is that (2.4) does not need differentiability of `q_*`. It only needs both critical centers, one common strongly-convex cell, and one dual bound on the time-change of the gradient at the old center.

---

## 3. Differential center-speed identity and inverse-free speed bound

Now assume enough smoothness to apply the implicit-function theorem. Since

`H_*(t) := Hess_q F(t,q_*(t)) >= 2 mu P > 0`,

`H_*(t)` is nonsingular. Local `C^1` critical-center branches therefore exist, and uniqueness from strong convexity glues them into the same `q_*(t)` branch on the interval.

Differentiate

`grad_q F(t,q_*(t))=0`.

With

`g_*(t) := partial_t grad_q F(t,q_*(t))`,

we obtain the exact tracking identity

**(3.1)**

`H_*(t) q_*dot(t) + g_*(t) = 0`.

Although the usual explicit formula is `q_*dot=-H_*^{-1}g_*`, the inverse is unnecessary for certification.

Assume

**(3.2)**

`<g_*(t),y>^2 <= G_*(t) Q(y)`.

Put `h=q_*dot`. Taking the inner product of (3.1) with `h` gives

`h^T H_* h = -<g_*,h>`.

By strong convexity,

`2 mu Q(h) <= -<g_*,h>`.

Exactly as in Section 2,

**(3.3) INVERSE-FREE CENTER SPEED**

`4 mu^2 Q(q_*dot(t)) <= G_*(t)`.

This is the differential analogue of (2.4).

---

## 4. Root-free finite-time same-cell tracking gate

Suppose a fixed outer ellipsoid is centered at `c`:

`E_out={q:Q(q-c)<=R_out}`.

At time `t0`, assume

`Q(q_*(t0)-c) <= R_in`.

Suppose Section 2 gives over `[t0,t1]`

`4 mu^2 Q(q_*(t1)-q_*(t0)) <= G01`.

For any positive rational tuning weights `p,q`, the quadratic addition identity gives

**(4.1)**

`p q Q(a+b) <= (p+q)(q Q(a)+p Q(b))`.

Apply it to

`a=q_*(t0)-c`, `b=q_*(t1)-q_*(t0)`.

A completely division-free sufficient same-cell gate is

**(4.2)**

`(p+q)(4 mu^2 q R_in + p G01) <= 4 mu^2 p q R_out`.

Then

`Q(q_*(t1)-c) <= R_out`.

Thus a source packet can track the moving center through a certified collar using only rational additions, multiplications, squares, and comparisons. `p,q` are certificate-tuning knobs, not physical parameters.

If instead a uniform temporal-gradient bound is known on the fixed old center,

`<partial_t grad F(t,q_*(t0)),y>^2 <= Gdot Q(y)`

for `t in[t0,t1]`, then with `h=t1-t0`, scalar integral Cauchy gives

`G01 <= h^2 Gdot`,

so (4.2) may consume `h^2 Gdot` directly.

This still requires the fixed evaluation point and the relevant time strip to stay inside the source-valid cell; it does not manufacture coverage.

---

## 5. Exact potential-gap storage: the moving-center velocity is not a separate power term

Define the exact recentered potential gap

**(5.1)**

`W(t,q) := F(t,q) - F(t,q_*(t))`.

For any differentiable physical trajectory `q(t)`, the chain rule gives

`dW/dt`

`= partial_t F(t,q) + <grad F(t,q),qdot>`

`  - partial_t F(t,q_*) - <grad F(t,q_*),q_*dot>`.

But `grad F(t,q_*)=0`. Hence

**(5.2) ENVELOPE IDENTITY**

`Wdot = <grad F(t,q),qdot>`

`       + [partial_t F(t,q)-partial_t F(t,q_*)]`.

There is **no additional standalone term involving `q_*dot`**.

This corrects an easy bookkeeping mistake: if one differentiates a coordinate difference `x=q-q_*`, a `-q_*dot` term appears in `xdot`; if one simultaneously differentiates the time-dependent recentered potential and then also adds a separate center-motion debit, the same effect can be double-counted. For the exact potential gap, the envelope identity (5.2) is authoritative.

This does **not** mean center motion is free. When the time dependence of `F` is generated by a moving center, it appears inside the explicit-time difference in (5.2). Sections 6–8 quantify that term.

---

## 6. Temporal Taylor split around the exact center

Write

`x := q-q_*(t)`.

Let

`G_t(q) := partial_t F(t,q)`,

`g_*(t) := grad_q G_t(q_*) = partial_t grad_q F(t,q_*)`,

and, when available,

`K_t(z) := Hess_q G_t(z) = partial_t Hess_q F(t,z)`.

Taylor's theorem along the segment `q_*+s x` gives the exact identity

**(6.1)**

`partial_t F(t,q)-partial_t F(t,q_*)`

`= <g_*,x>`

`  + integral_0^1 (1-s) x^T K_t(q_*+s x) x ds`.

This is the useful structural split:

- `<g_*,x>` is the **center-translation / temporal-force term**, first order in displacement;
- the integral is a **temporal-curvature term**, second order in displacement.

The same `g_*` that controls center speed in (3.3) is therefore exactly the linear part of the temporal storage-power defect.

---

## 7. Strong convexity converts displacement energy to storage energy

Since `grad F(t,q_*)=0` and the same segment satisfies (1.1), Taylor's theorem gives

**(7.1)**

`W(t,q) >= mu Q(x)`.

This is the homogeneous coercivity recovered by the recenter branch of T-P5-124/125.

For the temporal-curvature term, suppose a signed same-segment upper packet is available:

**(7.2)**

`x^T K_t(z) x <= 2 ell Q(x)`

for every `z=q_*+s x`, `0<=s<=1`.

Then the integral weight is `1/2`, so

**(7.3)**

`integral_0^1 (1-s) x^T K_t(...)x ds <= ell Q(x)`.

Choose a rational `eta>=0` satisfying the root-free gate

**(7.4)**

`ell <= mu eta`.

Then (7.1) implies

**(7.5)**

`temporal-curvature term <= eta W`.

Thus temporal Hessian variation can be charged purely to the relative rate when its signed upper part is small enough. One should preserve the sign before intervalizing; a negative temporal-Hessian contribution helps and should not be replaced by an absolute value.

---

## 8. Center-linear temporal power requires a mixed relative/additive gate

Assume the center temporal-force dual packet

**(8.1)**

`<g_*,x>^2 <= G0 Q(x)`.

Combining with (7.1) yields, without introducing a square root,

**(8.2)**

`mu <g_*,x>^2 <= G0 W`.

Choose rational `alpha,beta>=0` satisfying

**(8.3)**

`G0 <= 4 mu alpha beta`.

Then

`<g_*,x>^2 <= 4 alpha beta W`

and the square identity

`(alpha W + beta)^2 - 4 alpha beta W = (alpha W-beta)^2 >=0`

implies

**(8.4)**

`<g_*,x> <= alpha W + beta`.

Therefore Sections 6–8 give

**(8.5) TEMPORAL DEFECT GATE**

`partial_t F(t,q)-partial_t F(t,q_*) <= (alpha+eta) W + beta`,

provided

`G0 <= 4 mu alpha beta`,

`ell <= mu eta`.

If the nominal physical dynamics already give

**(8.6)**

`<grad F(t,q),qdot> <= -c W - d D + p_other`,

then the exact moving-center storage obeys

**(8.7)**

`Wdot <= -(c-alpha-eta) W - d D + beta + p_other`.

So the time-dependent recenter consumes relative rate `alpha+eta` and additive budget `beta`, but **does not pay a second independent `q_*dot` term**.

---

## 9. Sharp obstruction: nonzero center speed generically forbids zero-floor homogeneous absorption

The additive floor in Section 8 is not a loose Young artifact.

Take one dimension with `P=1` and

**(9.1)**

`F(t,q)=mu (q-v t)^2`,  `mu>0`, `v!=0`.

Then

`q_*(t)=v t`,

`Hess F=2mu`,

`g_* = partial_t grad F = -2 mu v`,

`G0=4 mu^2 v^2`,

and

`W=mu (q-q_*)^2`.

The temporal-Hessian term vanishes identically. At a physical trajectory with `qdot=0`, writing `x=q-q_*`,

**(9.2)**

`Wdot = -2 mu v x`.

For the sign of `x` opposite to `v`, this is positive and linear in `|x|`, while `W` is quadratic in `|x|`. Hence for every finite `a`, there are arbitrarily small nonzero `x` for which

`Wdot > a W`.

Therefore no theorem of the form

`temporal defect <= alpha W`

can hold uniformly near the moving center when `g_*!=0` from only the present premises.

More strongly, for fixed `alpha>0`, the exact smallest constant `beta` satisfying

`-2 mu v x <= alpha mu x^2 + beta`

for all real `x` is

`beta = mu v^2 / alpha`.

Since `G0=4mu^2v^2`, this is exactly the equality case of

`G0 <= 4 mu alpha beta`.

Thus the scalar gate (8.3) is sharp for the pure moving-center model.

If a deployed controller contains a signed feedforward term that cancels this power, that cancellation should be kept explicitly. Without such extra structure, forcing `beta=0` is mathematically false.

---

## 10. Moving nonlinear chart: critical-center speed has an extra cancellation

Let a time-dependent chart be

`q=T(t,z)`, `J=D_z T`,

and define `Ftilde(t,z)=F(t,T(t,z))`.

At an exact **physical** critical point `q_*=T(t,z_*)`, `grad_q F(t,q_*)=0`. Therefore the connection term in the pulled Hessian vanishes at the center:

**(10.1)**

`Hess_z Ftilde(t,z_*) = J_*^T H_* J_*`.

Likewise

`partial_t grad_z Ftilde`

normally contains a `J_t^T grad F` term, but at the exact critical point that term also vanishes. The remaining identity is

**(10.2)**

`partial_t grad_z Ftilde(t,z_*)`

`= J_*^T [ g_* + H_* T_t(t,z_*) ]`.

Differentiating `grad_z Ftilde(t,z_*(t))=0` gives

`J_*^T H_* J_* z_*dot + J_*^T(g_*+H_* T_t)=0`.

If `J_*^T` has trivial kernel (for example square nonsingular `J_*`), then

**(10.3)**

`H_* [T_t + J_* z_*dot] + g_* = 0`.

But `T_t+J_*z_*dot = q_*dot`, so (10.3) is exactly the physical center-speed identity (3.1).

Thus at an exact physical critical center, the nonlinear-chart second-derivative connection debit from T-P5-126 and the `J_t^T grad F` term both disappear from the **center tracking identity**. They remain relevant away from the center for cellwise coercivity and power transport, but should not be charged twice at the center.

If chart criticality does not imply physical criticality because `ker J^T` is nontrivial, this simplification is unavailable; T-P5-126's kernel condition remains essential.

---

## 11. Minimal theorem statements

### Theorem A — two-time critical-center drift

On one convex cell, if `F1` has gradient strong monotonicity constant `2mu` in metric `Q`, `grad F0(q0)=0`, `grad F1(q1)=0`, and

`<grad F1(q0)-grad F0(q0),y>^2 <= G Q(y)`,

then

`4 mu^2 Q(q1-q0) <= G`.

### Theorem B — inverse-free critical-center speed

If `q_*(t)` is a differentiable critical branch, `Hess F >=2mu P`, and

`<partial_t grad F(t,q_*),y>^2 <= G Q(y)`,

then

`H_* q_*dot + partial_t grad F =0`

and

`4mu^2 Q(q_*dot)<=G`.

### Theorem C — root-free ellipsoid drift closure

If

`Q(q0-c)<=Rin`,

`4mu^2Q(q1-q0)<=G`,

and positive `p,q` satisfy

`(p+q)(4mu^2 q Rin + p G) <= 4mu^2 p q Rout`,

then

`Q(q1-c)<=Rout`.

### Theorem D — exact moving-critical potential-gap derivative

For

`W(t,q)=F(t,q)-F(t,q_*(t))`, `grad F(t,q_*)=0`,

along any differentiable `q(t)`,

`Wdot=<grad F,qdot> + partial_tF(t,q)-partial_tF(t,q_*)`.

No separate `q_*dot` term remains.

### Theorem E — mixed temporal-power absorption

If

`W>=mu Q(x)`,

`<g_*,x>^2<=G0Q(x)`,

`temporalHessianIntegral<=ell Q(x)`,

`G0<=4mu alpha beta`,

`ell<=mu eta`,

then

`partial_tF(t,q)-partial_tF(t,q_*) <= (alpha+eta)W+beta`.

---

## 12. Suggested Lean decomposition

The best source-independent leaves are small:

```text
strong_monotone_critical_center_drift
  -- no IFT and no inverse
  grad0 q0 = 0 -> grad1 q1 = 0
  -> strongMonotone grad1
  -> dual bound on grad1 q0 - grad0 q0
  -> 4*mu^2*Q(q1-q0) <= G

critical_center_speed_identity
  grad F(t,qstar t)=0
  -> derivative chain rule
  -> Hess * qstardot + dtGrad = 0

critical_center_speed_inverse_free
  Hess >= 2*mu*P
  -> dual dtGrad packet
  -> 4*mu^2*Q(qstardot) <= G

quadratic_weighted_add
  p*q*Q(a+b) <= (p+q)*(q*Q(a)+p*Q(b))

potential_gap_moving_center_deriv
  gradF qstar = 0
  -> d/dt [F(t,q)-F(t,qstar)]
     = gradF(q)·qdot + dtF(q)-dtF(qstar)

temporal_taylor_at_critical_center
  dtF(q)-dtF(qstar)
  = <dtGradF(qstar),x>
    + integral (1-s) * x^T dtHessF(qstar+s*x) x

center_linear_temporal_absorption
  W>=mu*Qx
  -> p^2<=G0*Qx
  -> G0<=4*mu*alpha*beta
  -> p<=alpha*W+beta

moving_chart_critical_speed_cancellation
  gradF(qstar)=0
  -> pulled Hessian connection term vanishes at center
  -> J_t^T gradF vanishes at center
  -> physical speed identity under ker(J^T)=0
```

The first, fourth, and center-linear absorption lemmas are essentially quadratic/order algebra. Calculus/IFT leaves can be added after the algebraic consumer is stable.

---

## 13. Source-facing packet

A future actual time-dependent P5 instantiation should freeze under one reference/chart/cell key:

1. shaped scalar potential `F(t,q)` and exact `grad_q F`, `Hess_q F` semantics;
2. one SPD metric `P` and uniform strong-Hessian constant `mu`;
3. a same-cell T-P5-125 center-existence packet for every time slice, or an equivalent direct critical-center witness;
4. temporal gradient `partial_t grad_q F` and its dual energy packet `G0` / two-time `G01`;
5. preferably signed `partial_t Hess_q F` or directly the weighted temporal-curvature integral bound `ell`;
6. inner/outer center-tracking radii and time-strip coverage if the center must stay in one source cell;
7. the nominal dynamic storage ledger `(c,d,p_other)` to consume `alpha+eta` and `beta`;
8. if a moving chart is used, `T,J,T_t`, physical-criticality/no-kernel witness, and the T-P5-126 same-cell chart packet.

Preferred source order is to form the signed temporal scalar power first and intervalize last. In particular, do not separately absolute-bound `q_*dot`, `T_t`, and `partial_tF` if their exact work terms cancel.

---

## 14. Boundaries deliberately left open

This review does not claim:

- that the deployed P5 shaped potential is time dependent in exactly this form;
- that a concrete actual `partial_t grad F` or `partial_t Hess F` packet exists;
- that T-P5-125's root-free center-existence gate holds uniformly over a real reference schedule;
- that the actual moving center stays inside the physical/chart/FD halo;
- that the deployed chart is square, nonsingular, or source-bound to the same `F`;
- that controller feedforward cancels any center-translation power;
- that Float64/runtime evaluation matches these exact-real functions;
- that P8 flowpipe/existence/coverage is closed;
- that any Lean theorem has compiled;
- that 封不觉 has independently verified this child;
- that P5/P8 parent state, formal certificate gate, admission, or registry eligibility has changed.

The main remaining mathematical/source seam is now concrete: either bind `partial_t grad F` / signed temporal-Hessian power on the actual reference tube, or prove that the deployed reference/chart is piecewise constant/affine in a way that makes the corresponding terms vanish on each segment and handles jumps separately.

---

## 15. Final disposition

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending.**

The time-dependent recenter seam can be handled without an explicit Hessian inverse and without double-counting center motion:

- two-time center drift: `4mu^2 Q(delta q_*) <= G01`;
- instantaneous speed: `4mu^2 Q(q_*dot) <= G_*`;
- exact potential-gap storage has no standalone `q_*dot` term;
- temporal power splits into a center-linear term and a temporal-curvature term;
- the center-linear term has the sharp mixed gate `G0<=4mu alpha beta`;
- the temporal-curvature term is relative under `ell<=mu eta`;
- nonlinear chart connection/J_t terms cancel at the exact physical critical center in the speed identity, although they remain relevant away from the center.

The next useful work is an actual same-key temporal source packet or a piecewise-reference specialization, not another generic strong-convexity proof.