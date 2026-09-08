---
kind: review_result
review_id: review-T-P5-084-nonlinear-chart-secants-kuangmanmozun-20260908T0953
task_id: T-P5-084-NONLINEAR-CHART-SECANT-GEOMETRY
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-08T09:53:00-06:00
claim_commit: 52c5e62a3f387f82f69977da42275309f88d3a8a
inspected_commits:
  - 72f430f93517ccf4bf5da5e26b29c83c56ef5e7b
  - 11118d96c8df11a4861d1955d19a16825441c9ce
  - 52c5e62a3f387f82f69977da42275309f88d3a8a
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: >-
  Insert after T-P5-082/T-P5-083 as the nonlinear-chart global secant/inverse
  geometry boundary. Pointwise Jacobian invertibility, determinant positivity,
  or a uniform smallest-singular-value bound do not by themselves certify
  global injectivity or a co-Lipschitz inverse. Use either the strong-monotone
  Jacobian gate or the near-affine Jacobian-tube gate below. The latter also
  gives an exact image-ball reserve and a division-free transfer gate for a
  fixed normalized z-barrier. Keep the finite-displacement secant metric distinct
  from the tangent pullback metric of T-P5-082.
---

# T-P5-084 — nonlinear chart secant geometry: global inverse reserve, image-ball gate, and a false local-Jacobian shortcut

## 0. Result in one line

T-P5-082 establishes exact *differential* pullback contraction for a nonlinear
chart and an explicit finite-step curvature defect. T-P5-083 closes the domain
of the Euler segment used by that curvature estimate. A different global
geometry question remains:

> when does the nonlinear chart itself have a single-valued, quantitatively
> controlled inverse on the whole certified cell?

A pointwise lower bound on `sigma_min(DT)` is **not enough**. Even an everywhere
orientation-preserving local diffeomorphism with `sigma_min(DT) >= 1` on a
convex rectangle can wrap around and identify two distant source points.

Two source-friendly sufficient gates are proved here.

### Gate A — strong monotone Jacobian

For a fixed SPD metric `H`, if on a convex cell `Omega`

**(0.1)** `v^T (H DT(u) + DT(u)^T H) v >= 2 mu v^T H v`

for every `u in Omega`, every `v`, with `mu>0`, then

**(0.2)**
`<T(z)-T(w), z-w>_H >= mu ||z-w||_H^2`,

hence

**(0.3)** `||T(z)-T(w)||_H >= mu ||z-w||_H`.

So `T` is injective and its inverse on `T(Omega)` is `1/mu`-Lipschitz.

This gate is robust but orientation-specific; it is sufficient, not necessary.

### Gate B — near-affine Jacobian tube

Choose a fixed invertible reference matrix `A`. Suppose on the convex cell

**(0.4)** `||A v||_H >= m ||v||_H`, `m>0`,

and

**(0.5)** `||(DT(u)-A)v||_H <= eps ||v||_H`

for every `u,v`, with

**(0.6)** `0 <= eps < m`.

Then for every `z,w in Omega`,

**(0.7)**
`||T(z)-T(w)||_H >= (m-eps) ||z-w||_H`.

Thus the exact global inverse reserve is at least `m-eps`, without any
pointwise determinant or local inverse theorem.

The threshold is sharp under this information: in one dimension,
`T(z)=(m-eps)z` attains equality.

Even better, if the closed `H`-ball `B_H(z0,r)` lies in the source cell, then

**(0.8)**
`B_H(T(z0),(m-eps)r) subset T(B_H(z0,r))`.

So the same reserve also certifies a concrete *image-coverage ball*.
For a requested target radius `rho`, the checker can use the division-free gate

**(0.9)** `rho + eps*r <= m*r`.

Strict `<` gives interior reserve.

Finally, if physical finite-displacement energy contracts by `q` and the chart
has secant constants `mu,L`, then a fixed normalized source-coordinate barrier
contracts whenever

**(0.10)** `q L^2 < mu^2`.

No square root or division is required in the trusted gate.

This is mathematics/interface only. It does not bind a deployed chart, source
CSE, concrete rational Jacobian tube, Float64/controller/FD implementation,
P8/ODE coverage, Lean/kernel receipt, provenance, admission, registry state, or
parent closure.

---

## 1. Exact secant factorization on a convex cell

Let `Omega subset R^n` be convex and let `T : Omega -> R^n` be `C^1` on a
neighborhood of every segment under consideration.

For `z,w in Omega`, write

`d = z-w`,

and define the secant operator

**(1.1)**
`S(z,w) = integral_0^1 DT(w+t d) dt`.

The vector fundamental theorem of calculus gives the exact identity

**Theorem 1.1 — nonlinear secant factorization**

**(1.2)** `T(z)-T(w) = S(z,w) (z-w)`.

Everything about global inverse geometry is therefore a statement about the
*average Jacobian along a segment*, not merely each pointwise Jacobian.

This distinction is the source of the obstruction below.

---

## 2. Counterexample: uniform pointwise Jacobian invertibility does not imply global injectivity

Consider the convex rectangle

`Omega = [0,1] x [0,2*pi]`

and

**(2.1)**
`T(x,y) = (e^x cos y, e^x sin y)`.

Its Jacobian is

`DT(x,y) = e^x [[cos y, -sin y], [sin y, cos y]]`.

Therefore

**(2.2)** `DT^T DT = e^(2x) I`,

so on all of `Omega`

**(2.3)** `sigma_min(DT) = e^x >= 1`.

Also

**(2.4)** `det DT = e^(2x) > 0`.

Thus every point has a uniformly invertible, orientation-preserving Jacobian.
Nevertheless

**(2.5)** `T(0,0)=T(0,2*pi)=(1,0)`.

Hence `T` is not injective.

For the secant displacement `d=(0,2*pi)`, (1.2) gives

`S((0,2*pi),(0,0)) d = 0`.

So an average of uniformly invertible matrices can be singular on the relevant
secant direction. The invalid shortcut is therefore:

`DT(u)^T DT(u) >= mu^2 I for all u`

`NOT=>`

`||T(z)-T(w)|| >= mu ||z-w||`.

The same example also kills the stronger-looking shortcut

`det DT>0 + sigma_min(DT)>=mu >0 => global chart inverse`.

A local inverse theorem cannot repair this global wrapping defect.

---

## 3. Gate A: symmetric-Jacobian coercivity gives a global secant reserve

Let `H` be fixed SPD and define

`<a,b>_H = a^T H b`,

`||a||_H^2 = a^T H a`.

Assume for every `u in Omega` and every vector `v`,

**(3.1)**
`v^T [H DT(u) + DT(u)^T H] v >= 2 mu v^T H v`,

with `mu>0`.

Take `z,w in Omega`, `d=z-w`. By (1.2),

`<T(z)-T(w),d>_H`

` = integral_0^1 d^T H DT(w+t d)d dt`.

The scalar

`d^T H DT d`

is equal to

`(1/2) d^T(H DT + DT^T H)d`.

Therefore (3.1) gives

**(3.2)**
`<T(z)-T(w),d>_H >= mu ||d||_H^2`.

Weighted Cauchy-Schwarz gives

`<T(z)-T(w),d>_H`
` <= ||T(z)-T(w)||_H ||d||_H`.

For `d != 0`, cancel `||d||_H` to obtain

**Theorem 3.1 — strong-monotone Jacobian implies global co-Lipschitz chart**

**(3.3)**
`||T(z)-T(w)||_H >= mu ||z-w||_H`.

Consequences:

- `T` is injective on `Omega`;
- for `x1,x2 in T(Omega)`,
  `||T^{-1}(x1)-T^{-1}(x2)||_H <= mu^{-1}||x1-x2||_H`;
- any two certified source points cannot collapse under the chart;
- the co-Lipschitz reserve is global on the full convex cell, not merely local.

If one also has

**(3.4)** `DT(u)^T H DT(u) <= L^2 H`,

then segment integration gives

**(3.5)** `||T(z)-T(w)||_H <= L ||z-w||_H`.

Thus the chart is quantitatively bi-Lipschitz with constants `(mu,L)`.

### 3.1 This gate is sufficient, not necessary

Take a fixed ninety-degree rotation `T(z)=R z`. It is a global isometry and has
perfect inverse reserve `1`, but

`R+R^T=0`.

Hence (3.1) cannot hold with positive `mu` in the Euclidean metric. Refusing
such a chart merely because the symmetric part is not positive would be too
conservative.

This motivates Gate B.

---

## 4. Gate B: a near-affine Jacobian tube survives arbitrary fixed orientation

Fix an invertible reference linear map `A`. Assume

**(4.1)** `||A v||_H >= m ||v||_H`

for all `v`, with `m>0`, and

**(4.2)** `||(DT(u)-A)v||_H <= eps ||v||_H`

for all `u in Omega`, all `v`, with `0<=eps<m`.

Write

`E(u)=DT(u)-A`.

The exact secant operator is

`S=A+Ebar`,

where

`Ebar = integral_0^1 E(w+t d) dt`.

For each fixed `d`, triangle/Jensen integration gives

**(4.3)** `||Ebar d||_H <= eps ||d||_H`.

Therefore

`||T(z)-T(w)||_H`
` = ||A d + Ebar d||_H`
` >= ||A d||_H - ||Ebar d||_H`
` >= (m-eps)||d||_H`.

So:

**Theorem 4.1 — near-affine global secant gate**

If (4.1)--(4.2) hold on a convex cell and `eps<m`, then

**(4.4)**
`||T(z)-T(w)||_H >= (m-eps)||z-w||_H`

for all `z,w` in that cell.

This is orientation-agnostic because `A` can itself be a rotation, shear, or
other source-provided reference chart.

A fully squared source packet may state

**(4.5)** `A^T H A >= m^2 H`,

**(4.6)** `(DT(u)-A)^T H (DT(u)-A) <= eps^2 H`,

plus the rational scalar gate `0<=eps<m`.

The final inverse certificate can then retain the rational reserve

**(4.7)** `mu_sec = m-eps > 0`.

No determinant and no eigenvalue computation is needed by the consumer once
(4.5)--(4.6) are source-certified.

### 4.1 Sharpness under this envelope

In one dimension let

`A=m`,

`T(z)=(m-eps)z`.

Then `DT-A=-eps`, so the Jacobian-tube bound is attained and

`|T(z)-T(w)|=(m-eps)|z-w|`.

Thus no universal reserve larger than `m-eps` can be deduced from only
(4.1)--(4.2).

---

## 5. Image coverage: the same near-affine gate gives a certified physical ball

Co-Lipschitz injectivity alone only controls points already known to lie in the
image. For a chart adapter, one also wants a concrete physical region known to
be covered by the chart.

Let the closed source ball

`B_H(z0,r)={z: ||z-z0||_H <= r}`

lie in the source cell, and assume Gate B on this ball.

Define the nonlinear remainder relative to `A`:

**(5.1)**
`R(z)=T(z)-T(z0)-A(z-z0)`.

From (4.2), for `z,w` in the ball,

**(5.2)** `||R(z)-R(w)||_H <= eps ||z-w||_H`.

Let a target `y` satisfy

**(5.3)** `||y-T(z0)||_H <= (m-eps)r`.

Since (4.1) implies

`||A^{-1}u||_H <= m^{-1}||u||_H`,

consider

**(5.4)**
`Phi(z)=z0+A^{-1}[y-T(z0)-R(z)]`.

For `z in B_H(z0,r)`,

`||Phi(z)-z0||_H`
` <= m^{-1}[(m-eps)r+eps r]`
` = r`.

So `Phi` maps the closed ball to itself. Also

**(5.5)**
`||Phi(z)-Phi(w)||_H <= (eps/m)||z-w||_H`.

Because `eps/m<1`, Banach's fixed-point theorem gives a unique fixed point in
the ball. The fixed-point equation is exactly `T(z)=y`.

Therefore:

**Theorem 5.1 — near-affine image-ball coverage**

**(5.6)**
`B_H(T(z0),(m-eps)r) subset T(B_H(z0,r))`.

For a requested target radius `rho>=0`, a trusted checker need only establish

**(5.7)** `rho + eps*r <= m*r`.

This is division-free. A strict reserve is

**(5.8)** `R_img = m*r - eps*r - rho > 0`.

### 5.1 Sharpness

Again take one-dimensional `T(z)=(m-eps)z` on `[-r,r]`. Its image is exactly

`[-(m-eps)r,(m-eps)r]`.

Thus the radius `(m-eps)r` is sharp under the near-affine packet.

### 5.2 What is and is not closed

This theorem certifies a physical image ball around a chosen chart center when
a source ball is available. It does **not** claim arbitrary non-ball source
cells map onto any prescribed physical polygon/box. Such shape-specific image
coverage remains a separate geometric obligation.

---

## 6. Finite-displacement energy uses a secant metric, not the tangent pullback metric

T-P5-082's exact differential contraction naturally uses the tangent pullback
metric

`M_tan(z)=DT(z)^T H DT(z)`.

For a finite displacement from a reference `z*`, the exact physical quadratic
energy is instead

**(6.1)**
`V_phys(z)=||T(z)-T(z*)||_H^2`.

By the secant factorization,

`T(z)-T(z*)=S_*(z)(z-z*)`,

where

`S_*(z)=integral_0^1 DT(z*+t(z-z*))dt`.

Hence

**(6.2)**
`V_phys(z)=(z-z*)^T S_*^T H S_* (z-z*)`.

The finite-displacement metric is therefore the **secant metric**

**(6.3)** `M_sec(z)=S_*(z)^T H S_*(z)`,

not `M_tan(z)`.

They agree for affine charts and generally differ for nonlinear charts.

### Exact one-dimensional regression

Take

`T(z)=z+a z^2`, `z*=0`.

Then

`S_*(z)=1+a z`,

while

`DT(z)=1+2a z`.

Thus

**(6.4)** `V_phys(z)=z^2(1+a z)^2`,

whereas the tangent quadratic surrogate is

**(6.5)** `V_tan(z)=z^2(1+2a z)^2`.

Except at `a z=0`, these are not equal. A finite P5 barrier must not silently
replace one by the other.

This also explains why the local Jacobian singular-value lower bound can fail
globally: it controls every tangent metric while the secant matrix can still
lose rank through orientation cancellation.

---

## 7. Transfer of physical contraction to a fixed normalized z-barrier

Assume on the certified chart cell the secant geometry satisfies

**(7.1)**
`mu ||z-z*||_H <= ||T(z)-T(z*)||_H <= L ||z-z*||_H`,

with `mu>0`.

Suppose a physical finite-step theorem gives

**(7.2)**
`V_phys(z_plus) <= q V_phys(z)`, `q>=0`.

Then

`mu^2 ||z_plus-z*||_H^2`
` <= V_phys(z_plus)`
` <= q V_phys(z)`
` <= q L^2 ||z-z*||_H^2`.

Therefore

**Theorem 7.1 — fixed normalized barrier transfer**

**(7.3)**
`mu^2 ||z_plus-z*||_H^2 <= q L^2 ||z-z*||_H^2`.

A strict contraction of the same fixed `z`-quadratic barrier is certified by

**(7.4)** `q L^2 < mu^2`.

Equality is boundary-only. The trusted gate is polynomial/rational and needs no
square root or division.

The conceptual distinction is important:

- if the consumer uses the exact physical/secant energy `V_phys`, chart
  distortion costs nothing beyond whatever physical theorem already proves;
- if it insists on a fixed coordinate quadratic `||z-z*||_H^2`, it must pay the
  chart distortion ratio through (7.4).

For Gate A one may take the lower constant `mu` from (3.1). For Gate B one may
take

`mu=m-eps`.

An upper constant can come from a source bound

`DT^T H DT <= L^2 H`

or, in the near-affine lane, from

`||A v||_H <= M||v||_H`

and `||DT-A||<=eps`, giving `L<=M+eps`.

---

## 8. Failure branches and checker semantics

### FAIL/OBSTRUCTION 1 — pointwise determinant or smallest singular value only

If the only source data are

`det DT != 0`

or even

`DT^T H DT >= mu^2 H`,

there is no valid global-injectivity conclusion. The exponential-polar example
is an exact counterexample.

Correct status: `NOT_CERTIFIED_GLOBAL_CHART` unless a separate topology/injective
source theorem is supplied.

### FAIL/OBSTRUCTION 2 — averaging singular-value lower bounds

It is invalid to say each `DT(u)` has `sigma_min>=mu`, therefore its segment
average `S(z,w)` does too. Singular values are not lower-convex under matrix
averaging; rotating Jacobians can cancel.

### NOT_APPLICABLE, not mathematical FAIL — symmetric coercivity absent

Failure of Gate A does not prove the chart is bad. A rotation is the simplest
counterexample. Try Gate B with a nontrivial reference `A`, or supply an exact
secant/injectivity theorem.

### FAIL/OBSTRUCTION 3 — tangent metric substituted for finite secant energy

For nonlinear `T`, `DT(z)^T H DT(z)` is a differential metric. It cannot be used
as an exact finite-displacement physical energy without an additional comparison
theorem. The quadratic chart regression in section 6 must remain in tests.

### FAIL/OBSTRUCTION 4 — image coverage inferred from injectivity alone

Injectivity/co-Lipschitz controls the inverse on the image, but does not identify
what the image contains. Use Theorem 5.1 for a near-affine ball, or provide a
separate shape-specific image theorem.

---

## 9. Minimal theorem statements for formalization

Suggested small leaves:

1. `nonlinear_secant_factorization_convex`

   On a convex segment, prove
   `T z - T w = (integral t, DT(w+t(z-w))) (z-w)`.

2. `strong_monotone_jacobian_secant`

   From
   `v^T(H*DT+DT^T*H)v >= 2*mu*v^T H v`
   derive
   `<Tz-Tw,z-w>_H >= mu*Q_H(z-w)`.

3. `strong_monotone_chart_colipschitz`

   Add SPD Cauchy-Schwarz and derive
   `Q_H(Tz-Tw) >= mu^2 Q_H(z-w)`.

4. `near_affine_jacobian_secant`

   From a fixed `A`, lower reserve `m`, perturbation `eps<m`, derive
   `Q_H(Tz-Tw) >= (m-eps)^2 Q_H(z-w)`.

5. `near_affine_image_ball`

   Banach self-map proof for
   `rho+eps*r <= m*r`.

6. `secant_energy_identity`

   `Q_H(Tz-Tz*) = Q_{S_*^T H S_*}(z-z*)`.

7. `fixed_chart_barrier_transfer_sq_gate`

   From lower/upper secant bounds and physical contraction, derive the cleared
   condition `q*L^2 < mu^2` for strict fixed-coordinate contraction.

8. regressions:

   - `exp_polar_uniform_jacobian_not_injective`;
   - `rotation_not_strong_monotone_but_isometry`;
   - `quadratic_chart_tangent_ne_secant`;
   - one-dimensional sharpness for `m-eps` and image radius.

For an early Lean slice, Gate A can be proved first without matrix singular
values. Gate B can then use an abstract normed linear-map packet, leaving source
matrix inequalities as adapter obligations.

---

## 10. Recommended downstream routing

For a nonlinear chart consumer:

1. Use T-P5-082 for differential pullback and finite-step curvature defect.
2. Use T-P5-083 to prove the whole Euler segment stays where the Hessian packet
   is valid.
3. Separately certify global chart geometry:
   - prefer Gate A if a signed symmetric-Jacobian coercivity theorem is natural;
   - otherwise use Gate B around a fixed reference affine chart `A`.
4. If physical target coverage is needed and Gate B is available, use the exact
   ball reserve `rho+eps*r <= m*r`.
5. Keep finite physical energy in the secant metric. Only convert to a fixed
   normalized quadratic barrier through `q L^2 < mu^2`.

Do not let a local Jacobian determinant/singular-value certificate silently
stand in for steps 3--4.

---

## 11. Status boundary

This child is **pending mathematical child** only.

It does not establish:

- any deployed nonlinear chart or its exact source definition/hash;
- any concrete `H,A,m,eps,L,r,rho` packet;
- chart coverage for a non-ball physical target;
- Float64/controller/FD semantics;
- P8/ODE trajectory coverage;
- Lean/kernel compilation or receipt;
- provenance, admission, registry state, P5/M4 closure, or parent closure.

The mathematical contribution is the exact separation:

**local tangent invertibility is not global secant invertibility; global chart
closure requires a no-cancellation mechanism.**

Strong monotonicity supplies one such mechanism. A uniformly small Jacobian tube
around a fixed invertible affine orientation supplies another, and additionally
gives a sharp, division-free image-ball reserve.