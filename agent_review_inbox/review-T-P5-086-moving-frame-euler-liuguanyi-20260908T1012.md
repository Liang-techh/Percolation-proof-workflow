---
kind: review_result
review_id: review-T-P5-086-moving-frame-euler-liuguanyi-20260908T1012
task_id: T-P5-086-MOVING-FRAME-EULER
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-08T10:12:00-06:00
claim_commit: 840da2bf43efd3d37cdccd2c6bff24d788621913
conclusion: PARTIAL
status: pending mathematical/interface child
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
summary: >-
  Exact time-dependent moving-chart bridge for one explicit-Euler step. The
  transformed Euler step is first-order covariant only when the moving-frame
  term T_t is included. Its physical image differs from physical Euler by an
  exact h^2 spacetime-direction curvature remainder. A correlated weighted
  square bound on that directional curvature yields the division-free gate
  h^4 K_C <= 4 D_mov, which can be consumed as an additive/correlation-aware
  defect by the existing P5 corrector lane.
evidence:
  - exact Taylor integral identity along the affine spacetime path
  - weighted Cauchy/Jensen square bound with sharp kernel factor 1/4
  - exact rational obstruction showing omission of T_t creates O(h) error
  - exact cancellation example showing absolute-first curvature bounds can be spurious
risks:
  - deployed chart/source binding is not established
  - spacetime path/tube inclusion is not established
  - no rational source enclosure K_C is supplied here
  - state/time-dependent physical metrics require an additional theorem
  - higher-order integrators are outside this result
next_action: >-
  Bind the deployed chart to the base moving-frame identity, form the whole
  correlated directional second derivative before intervalization, certify a
  same-path weighted-square upper bound K_C, and feed the resulting D_mov into
  the existing additive/correlation-aware defect lane. Formalize the algebraic
  identity and weighted integral bound as separate Lean leaves.
---

# T-P5-086 — moving-frame Euler defect bridge

## 0. Result in one line

T-P5-082 identified the finite-step obstruction for a nonlinear chart at fixed
time. The missing time-dependent statement is not obtained by merely adding a
`T_t` term to a static curvature budget. The correct source-to-math contract is:

1. include `T_t` in the transformed vector field already at **first order**;
2. freeze the base transformed Euler direction `G0`;
3. form the **whole correlated second derivative of `T` along the spacetime
   Euler direction** before absolute/interval enclosure;
4. charge only the resulting `O(h^2)` defect into the existing P5 additive or
   correlation-aware defect lane.

The exact formula is

`r_mov = h^2 ∫_0^1 (1-s) C_T(t+sh,z-shG0;G0) ds`,

where

`C_T(t',z';G0)`
` = T_tt(t',z')`
`   - 2 D_tz T(t',z')[G0]`
`   + D_zz^2 T(t',z')[G0,G0]`.

If a fixed physical weighted quadratic form `Q_W(v)=v^T W v` satisfies

`Q_W(C_T(t+sh,z-shG0;G0)) <= K_C`

for every `s in [0,1]`, then

`Q_W(r_mov) <= h^4 K_C / 4`.

Hence an exact-rational checker may avoid both square roots and division by
checking only

**`h^4 K_C <= 4 D_mov`.**

Then `Q_W(r_mov) <= D_mov` follows.

This is a mathematics/interface child only. It does not establish a deployed
chart, CSE enclosure, Float64/FD/controller semantics, trajectory coverage,
Lean/kernel receipt, independent verification, comparator or admission.

---

## 1. Setup and the mandatory moving-frame covariance

Let

`x = T(t,z)`

be a `C^2` chart on a spacetime tube, with source Jacobian

`J(t,z)=D_z T(t,z)`.

Let the physical ODE be

`x_dot = -F(t,x)`.

We want a transformed field `G` such that

`z_dot = -G(t,z)`

represents the same continuous-time motion. Differentiating the chart gives

`x_dot = T_t(t,z) + J(t,z) z_dot`
`      = T_t(t,z) - J(t,z) G(t,z)`.

Therefore the exact moving-frame relation is

**(1.1)** `T_t - J G = -F(t,T)`,

or equivalently

**(1.2)** `J G = F(t,T) + T_t`.

For the discrete theorem below fix one base point `(t,z)` and abbreviate

`G0 := G(t,z)`.

The trusted interface need not form `J^{-1}`. It is enough to bind the source by
the multiplication identity (1.2) at the base point.

---

## 2. Exact one-step defect identity

Take the normalized explicit-Euler step

**(2.1)** `z_E = z - h G0`

and advance the chart time to `t+h`. Its physical image is

**(2.2)** `x_chart = T(t+h,z-hG0)`.

The physical explicit-Euler step from the same base point is

**(2.3)** `x_E = T(t,z) - h F(t,T(t,z))`.

Define the affine spacetime path

**(2.4)** `gamma(s) = (t+sh, z-shG0)`, `0 <= s <= 1`,

and the vector-valued path

`f(s)=T(gamma(s))`.

Because `G0` is frozen,

`f'(s) = h T_t(gamma(s)) - h D_zT(gamma(s)) G0`.

At the base point, (1.1) gives

**(2.5)** `f'(0) = -h F(t,T(t,z))`.

Differentiating once more gives

**(2.6)**
`f''(s)`
` = h^2 [ T_tt(gamma(s))`
`         - 2 D_tzT(gamma(s))[G0]`
`         + D_zz^2T(gamma(s))[G0,G0] ]`.

Define the correlated directional spacetime curvature

**(2.7)**
`C_T(t',z';G0)`
` := T_tt(t',z')`
`    - 2 D_tzT(t',z')[G0]`
`    + D_zz^2T(t',z')[G0,G0]`.

The second-order Taylor formula with integral remainder is

`f(1)=f(0)+f'(0)+∫_0^1 (1-s)f''(s) ds`.

Using (2.5)-(2.7),

**Theorem 2.1 — exact moving-frame Euler defect**

**(2.8)**
`r_mov := T(t+h,z-hG0)`
`         - [T(t,z)-hF(t,T(t,z))]`
`       = h^2 ∫_0^1 (1-s) C_T(gamma(s);G0) ds`.

This is an equality, not a perturbative heuristic.

### Important source-interface point

Only the **base** identity (1.1) is needed for first-order matching of this
explicit-Euler step. The integral remainder follows from the chart derivatives
along `gamma` with the frozen base vector `G0`. We do **not** need to assert that
`G(t+sh,z-shG0)=G0` along the path.

---

## 3. Weighted squared defect without sqrt

Let `W` be a fixed positive-semidefinite (normally SPD) physical weight and

`Q_W(v)=v^T W v`.

Assume the entire spacetime path lies in the certified chart tube and the source
proves the same-path bound

**(3.1)** `Q_W(C_T(gamma(s);G0)) <= K_C`

for all `s in [0,1]`.

From (2.8), set `C(s)=C_T(gamma(s);G0)`. Weighted Cauchy/Jensen with the positive
kernel `a(s)=1-s` gives

`Q_W(∫_0^1 a(s) C(s) ds)`
` <= (∫_0^1 a(s) ds) (∫_0^1 a(s) Q_W(C(s)) ds)`
` <= (1/2)(K_C/2)`
` = K_C/4`.

Therefore

**Theorem 3.1 — moving-frame squared defect bound**

**(3.2)** `Q_W(r_mov) <= h^4 K_C / 4`.

For an exact-rational checker, introduce a requested additive defect budget
`D_mov >= 0`. It is sufficient to check

**(3.3)** `h^4 K_C <= 4 D_mov`.

Then

**(3.4)** `Q_W(r_mov) <= D_mov`.

No square root, operator norm, matrix inverse, or floating division is required
in this last gate.

If the downstream proof already has a signed/correlated cross-term mechanism,
`r_mov` should be combined there before triangle inequality. Otherwise `D_mov`
is a plain additive squared defect compatible with the existing P5 defect lane.

---

## 4. Why the whole directional curvature must be formed before enclosure

Equation (2.7) contains three terms that can cancel exactly:

`T_tt`, `-2 T_tz[G0]`, and `T_zz[G0,G0]`.

The preferred source order is therefore

`signed chart derivatives`
` -> C_T = T_tt - 2 T_tz[G0] + T_zz[G0,G0]`
` -> Q_W(C_T)`
` -> interval / rational upper enclosure K_C`.

Do not, when avoidable, separately take absolute-value boxes for the three
pieces and only then add them. That operation loses genuine moving-frame
cancellation.

### Exact cancellation example

Take the scalar chart

`T(t,z)=phi(t+z)`

and choose `G0=1`, `F=0`. Where the chart is regular, `T_t=D_zT=phi'`, so the
moving-frame relation `D_zT G0=T_t` holds. Along

`gamma(s)=(t+sh,z-sh)`

the sum `t+z` is constant, hence `T(gamma(s))` is exactly constant and
`r_mov=0`.

For the rational polynomial `phi(q)=q^2`,

`T_tt=2`, `T_tz=2`, `T_zz=2`,

so

**(4.1)** `C_T = 2 - 4 + 2 = 0`.

A componentwise absolute-first fallback would instead charge `2+4+2=8`, even
though the exact discrete chart defect is zero. This is a genuine interface
loss, not merely an aesthetically looser bound.

---

## 5. Obstruction: omitting T_t creates first-order error

A time-dependent chart cannot be treated as a static chart plus a small
second-order correction.

Take the scalar translation

`T(t,z)=z+t`

and physical field

`F=0`.

Then `J=1` and `T_t=1`. The correct moving-frame relation gives

`G=1`.

Hence normalized Euler gives `z_E=z-h`, and after advancing time,

`T(t+h,z-h)=z-h+t+h=T(t,z)`.

The physical Euler step is also exactly `T(t,z)`, so the defect is zero.

If one incorrectly reuses the static rule `JG=F`, then `G=0`; the chart image is

`T(t+h,z)=T(t,z)+h`.

The error is **order h**, not order `h^2`.

Therefore `T_t` is mathematically mandatory in the transformed vector field and
cannot be hidden inside `D_mov` as if it were curvature.

---

## 6. Time-dependent affine charts are not generally exact discrete similarities

Let

`T(t,z)=c(t)+S(t)z`.

Then `D_zz^2T=0`, but the spacetime curvature is generally nonzero:

**(6.1)**
`C_T(t',z';G0)`
` = c''(t') + S''(t') z' - 2 S'(t') G0`.

Thus T-P5-079's exact discrete conjugacy for a **time-independent** affine chart
does not extend automatically to moving affine frames. Exact one-step
conjugacy is recovered when the chart restricted to the spacetime Euler path is
affine in the path parameter, equivalently when

**(6.2)** `C_T(gamma(s);G0)=0`

along the step.

A constant-velocity translation with fixed `S` is one simple zero-curvature
case. A changing scale `S(t)` can generate a nonzero defect even though the
chart is affine in `z`.

---

## 7. Safe fallback if correlated C_T is not available

The preferred packet is the direct square bound (3.1). If source CSE cannot yet
form it, a norm-style fallback is mathematically safe.

Suppose on the full path one has

`||T_tt||_W <= K_tt`,

`||D_tzT[v]||_W <= K_tz ||v||_Z`,

`||D_zz^2T[v,v]||_W <= K_zz ||v||_Z^2`,

and at the base

`||G0||_Z <= B_G`.

Then

**(7.1)**
`||C_T||_W <= K_tt + 2 K_tz B_G + K_zz B_G^2`,

and by integrating the kernel,

**(7.2)**
`||r_mov||_W`
` <= (h^2/2)(K_tt + 2K_tz B_G + K_zz B_G^2)`.

This route is deliberately marked as fallback because it loses all cancellation
between the three chart-derivative terms and usually introduces square-root
quantities if the source begins from squared norms.

---

## 8. Minimal typed mathematical contract

A source adapter need not expose a large geometric API. The minimum useful
packet is:

- base time/state: `t`, `z`;
- rational/nonnegative step `h`;
- chart `T` and frozen base transformed direction `G0`;
- exact base covariance witness
  `T_t(t,z)-D_zT(t,z)G0 = -F(t,T(t,z))`;
- a spacetime path/tube inclusion witness for
  `gamma(s)=(t+sh,z-shG0)`, `s in [0,1]`;
- fixed physical weight `W`;
- correlated curvature-square upper packet
  `Q_W(C_T(gamma(s);G0)) <= K_C`;
- requested squared additive budget `D_mov`;
- scalar gate `h^4 K_C <= 4 D_mov`.

The structural derivatives `T_tt`, `T_tz`, `T_zz` may stay upstream. The trusted
consumer can receive `C_T` or even only its certified weighted-square envelope,
provided the source preserves the same-path and same-`G0` binding.

---

## 9. Minimal theorem statements for formalization

### Theorem A — moving-frame Euler defect identity

Assume `T` is `C^2` on a convex spacetime tube containing `gamma([0,1])`, let
`G0=G(t,z)`, and assume the base identity

`T_t(t,z)-D_zT(t,z)G0=-F(t,T(t,z))`.

Then

`T(t+h,z-hG0)-[T(t,z)-hF(t,T(t,z))]`
` = h^2 ∫_0^1 (1-s)`
`   [T_tt - 2D_tzT[G0] + D_zz^2T[G0,G0]](gamma(s)) ds`.

### Theorem B — weighted square kernel bound

If `Q_W(C(s))<=K_C` for all `s in [0,1]`, then

`Q_W(∫_0^1 (1-s) C(s) ds) <= K_C/4`.

### Corollary C — division-free budget gate

Under Theorems A-B, if

`h^4 K_C <= 4 D_mov`,

then the moving-frame Euler defect has

`Q_W(r_mov)<=D_mov`.

Suggested Lean leaves:

- `moving_frame_euler_defect_identity`
- `weighted_square_integral_triangle_kernel`
- `moving_frame_defect_sq_le`
- `moving_frame_defect_budget_of_mul_le`

The first theorem is calculus/Taylor along one affine path. The second is a
source-independent finite-dimensional weighted integral inequality. Keeping
them separate should avoid mixing source geometry with the trusted scalar
budget algebra.

---

## 10. Dependencies and non-claims

Mathematical dependencies:

- the nonlinear-chart distinction and additive curvature lane identified by
  T-P5-082;
- the existing P5 additive/correlation-aware defect consumers downstream;
- ordinary second-order Taylor integral remainder and weighted Cauchy/Jensen.

This result does **not** prove or claim:

- that the deployed source actually satisfies a particular moving chart;
- that `gamma([0,1])` stays inside the real deployed chart/cell;
- any concrete rational value of `K_C`;
- validity for a state/time-dependent physical metric `W(t,x)`;
- a higher-order Runge-Kutta or multistep analogue;
- Float64, libm, finite-difference, controller, solve or evaluator semantics;
- P8/ODE first-exit or trajectory coverage;
- Lean/kernel closure;
- independent verifier acceptance by 封不觉;
- comparator/admission/registry closure.

Status remains **PARTIAL / pending mathematical-interface child** until those
source and downstream bindings are supplied.
