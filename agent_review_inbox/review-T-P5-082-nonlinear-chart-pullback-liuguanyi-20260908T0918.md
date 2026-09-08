---
kind: review_result
review_id: review-T-P5-082-nonlinear-chart-pullback-liuguanyi-20260908T0918
task_id: T-P5-082-NONLINEAR-CHART-PULLBACK
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-08T09:18:00-06:00
claim_commit: b36f7d743f5ae2bee4db946b384a7364b96aeddc
inspected_commits:
  - 8b36d94936707744a1c477696d406bff5bac536e
  - 229302289b459214acfc0adca1c4a4ef5005ae03
  - 91b6d1064d8f63a9ce8374006815cb39e07ccc8a
  - f2769764ff5a9c983114c3de525808be97eb98c7
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: >-
  Use this as the nonlinear-coordinate boundary around T-P5-079/T-P5-081.
  Differential/Riemannian contraction transports exactly through a C2 nonlinear
  chart when the pullback metric and transformed vector field are used. In
  contrast, the finite-step/secant P5 corrector is not exactly conjugate under a
  nonlinear chart; charge the exact chart-curvature remainder through the
  existing additive/correlation-aware defect lane. Do not reuse affine
  similarity constants or same-step conjugacy without this curvature packet.
---

# T-P5-082 — nonlinear chart pullback: exact differential cancellation, finite-step curvature defect

## 0. Result in one line

T-P5-079 and T-P5-081 show that affine coordinate changes are unusually benign:
they preserve the finite secant certificate and the damped corrector exactly.
That statement stops being true for a nonlinear chart.

There is nevertheless an exact invariant core.

Let the physical flow be

`x_dot = -F(t,x)`

in a fixed physical SPD quadratic metric `W`, and let a `C^2` local chart be

`x = T(t,z)`

with invertible Jacobian

`J = D_z T(t,z)`.

Define the transformed vector field `G` by the multiplication-only covariance

**(0.1)** `J G = F(t,T(t,z)) + T_t(t,z)`.

Then `z_dot=-G` is exactly the physical flow written in the nonlinear chart.
Set the pullback metric

**(0.2)** `M(t,z)=J^T W J`.

If `A=D_x F(t,T(t,z))`, then the full nonlinear/time-dependent connection packet
satisfies the exact matrix identity

**(0.3)**
`D_z M[G] + (D_z G)^T M + M D_z G - M_t`
` = J^T (W A + A^T W) J`.

Consequently, if the physical source proves

**(0.4)** `W A + A^T W >= 2 mu W`,

then in the nonlinear chart one gets, with the *same numerical mu*,

**(0.5)**
`D_z M[G] + (D_z G)^T M + M D_z G - M_t >= 2 mu M`.

For an infinitesimal displacement `xi` along `z_dot=-G`,

`Vdiff = xi^T M xi`

therefore obeys

**(0.6)** `d/dt Vdiff <= -2 mu Vdiff`.

No bound on `||D^2 T||`, no condition number of `J`, and no smallness of chart
motion is needed for this *differential* theorem: the nonlinear Hessian and
`T_t` connection terms cancel exactly in the co-moved pullback metric.

But this does **not** preserve the finite P5 secant/corrector theorem. For a fixed
nonlinear chart, if

`J(z) G(z)=F(T(z))`

and one takes a normalized Euler step

`z_E = z-h G(z)`,

then its physical image differs from the physical Euler step by the exact
curvature remainder

**(0.7)**
`r_curv = T(z-hG(z)) - [T(z)-hF(T(z))]`
`       = h ∫_0^1 [J(z)-J(z-thG(z))] G(z) dt`.

Equivalently, for `C^2` charts,

**(0.8)**
`r_curv = h^2 ∫_0^1 (1-t) D^2T(z-thG(z))[G(z),G(z)] dt`.

Thus affine charts are exactly the zero-curvature case `D^2T=0`.

If the source has a bilinear Hessian bound on the whole step segment,

**(0.9)**
`||D^2T(u)[v,v]||_W <= K_T ||v||_Z^2`,

and `||G(z)||_Z^2 <= B_G`, then

**(0.10)**
`||r_curv||_W <= (K_T/2) h^2 B_G`,

hence the division-free squared gate

**(0.11)** `K_T^2 h^4 B_G^2 <= 4 D_curv`

certifies

**(0.12)** `Q_W(r_curv) <= D_curv`.

That `D_curv` is an ordinary additive defect and can be fed directly to
T-P5-078/T-P5-081, or to T-P5-080 when signed correlation with the nominal
corrector is available.

The coefficient `1/2` in (0.10) is sharp even for a one-dimensional rational
quadratic chart.

This review is mathematics/interface only. It does not bind a deployed chart,
source CSE, Float64/FD/controller implementation, physical cell coverage,
P8/ODE trajectory, Lean/kernel receipt, provenance, admission, registry state,
or parent closure.

---

## 1. Exact nonlinear pullback identity

Fix `t,z` and abbreviate

`J = D_z T(t,z)`,

`A = D_x F(t,T(t,z))`,

`M = J^T W J`.

The transformed field is defined by the cleared equality

`J G = F∘T + T_t`.

No inverse needs to appear in the trusted statement. Analytically invertibility
of `J` gives `G=J^{-1}(F∘T+T_t)`, but the source adapter can prove only the
multiplication identity.

Differentiate the covariance in a source direction `xi`:

`D J[xi] G + J D G[xi]`
` = A J xi + D_z T_t[xi]`.

Because `T` is `C^2`, the Hessian is symmetric in its two source directions:

`D J[xi] G = D J[G] xi`.

Also `D_z T_t = J_t`. Hence the operator identity is

**(1.1)**
`D J[G] + J D G = A J + J_t`.

Now differentiate the pullback metric:

**(1.2)**
`D M[G]`
` = (D J[G])^T W J + J^T W D J[G]`,

and

**(1.3)**
`M_t = J_t^T W J + J^T W J_t`.

Add the `DG` terms:

`D M[G] + DG^T M + M DG - M_t`

` = (DJ[G]+JDG-J_t)^T WJ`
`   + J^T W(DJ[G]+JDG-J_t)`.

By (1.1),

`DJ[G]+JDG-J_t = A J`.

Therefore

**Theorem 1.1 — nonlinear connection congruence**

**(1.4)**
`D M[G] + DG^T M + M DG - M_t`
` = J^T(A^T W + W A)J`.

This is an exact identity, not an inequality or perturbative estimate.

### Why no Hessian-size charge appears

`D^2T` entered only through `DJ[G]`, and exactly the same `DJ[G]` appears in the
state-dependent metric derivative `DM[G]`. They cancel after the vector-field
covariance is differentiated. A checker that separately absolute-bounds the
Hessian connection term before forming (1.4) would therefore invent a false
penalty.

This is the nonlinear analogue of T-P5-081's cancellation of `S_dot` against the
co-moving affine metric derivative.

---

## 2. Differential contraction transports with the same rate

Let `xi` be a variational displacement for

`z_dot=-G(t,z)`.

Then

`xi_dot = -DG xi`.

The pullback differential energy is

`Vdiff = xi^T M(t,z) xi`.

Along the transformed flow,

`d/dt M(t,z(t)) = M_t - D M[G]`.

Therefore

`Vdiff_dot`
` = xi^T(M_t-DM[G]-DG^T M-MDG)xi`
` = -xi^T C xi`,

where

`C = DM[G]+DG^T M+MDG-M_t`.

Using Theorem 1.1,

`C = J^T(A^T W+WA)J`.

If the physical derivative packet satisfies

`A^T W+WA >= 2 mu W`,

then by congruence

`C >= 2 mu J^T WJ = 2 mu M`.

Hence

**Theorem 2.1 — nonlinear pullback differential contraction**

**(2.1)** `Vdiff_dot <= -2 mu Vdiff`.

The numerical `mu` is unchanged.

This theorem needs the pullback metric `M(t,z)`. It does **not** say that the
transformed field `G` is strongly monotone with the same `mu` in a fixed
constant normalized metric.

---

## 3. Exact 1D obstruction: finite secant strong monotonicity is not similarity-invariant

Take the physical scalar field

`F(x)=x`, `W=1`.

It has exact strong-monotonicity constant `mu=1`:

`(F(x)-F(y))(x-y)=(x-y)^2`.

Use the nonlinear chart

`T(z)=z+z^3`.

Its Jacobian is

`J(z)=1+3z^2>0`,

so it is a legitimate smooth orientation-preserving chart. The transformed
field satisfying `JG=F∘T` is

`G(z)=(z+z^3)/(1+3z^2)`.

At the exact rational points

`z_1=1`, `z_0=1/2`,

we have

`G(1)=1/2`,

`G(1/2)=5/14`.

Thus

`Delta G = 1/7`, `Delta z=1/2`,

and the scalar secant ratio is

**(3.1)**
`(Delta G Delta z)/(Delta z)^2`
` = Delta G/Delta z`
` = 2/7`.

So the transformed finite-secant inequality cannot retain the physical
constant `mu=1`; on any domain containing these two points, any constant-metric
strong-monotonicity lower bound is at most `2/7`.

Yet Theorem 2.1 still transports the physical differential rate `mu=1` exactly
in the variable pullback metric

`M(z)=J(z)^2`.

This separates two mathematical objects that must not be conflated:

1. affine P5 secant/corrector contraction;
2. nonlinear Riemannian/differential contraction.

The first is not a coordinate tensor under nonlinear reparameterization; the
second is.

---

## 4. Finite-step corrector is not exactly conjugate under nonlinear charts

Keep a fixed nonlinear chart `x=T(z)` and physical explicit corrector

`x_E = x-hF(x)`.

Assume the pointwise covariance

`J(z)G(z)=F(T(z))`.

The naively normalized explicit step is

`z_E=z-hG(z)`.

For an affine chart, T-P5-079 proves

`T(z_E)=x_E`

exactly. For a nonlinear chart this is false in general.

Define

`r_curv = T(z-hG)-T(z)+hJ(z)G`.

Since `JG=F∘T`,

**(4.1)**
`T(z_E)=x_E+r_curv`.

Using the fundamental theorem of calculus along the segment

`gamma(t)=z-thG`,

`T(z-hG)-T(z)`
` = -h ∫_0^1 J(z-thG)G dt`.

Therefore

**Theorem 4.1 — exact first-derivative curvature remainder**

**(4.2)**
`r_curv = h ∫_0^1 [J(z)-J(z-thG)]G dt`.

If `T` is `C^2`, Taylor with integral remainder gives the equivalent identity

**Theorem 4.2 — exact Hessian curvature remainder**

**(4.3)**
`r_curv`
` = h^2 ∫_0^1 (1-t) D^2T(z-thG)[G,G] dt`.

These identities expose precisely what affine similarity was hiding:

`D^2T=0  =>  r_curv=0`.

For a nonlinear chart, the physical and normalized Euler maps differ at order
`h^2`, and the coefficient is a genuine curvature quantity.

---

## 5. Sharp Hessian-to-additive-defect budget

Let `||.||_Z` be the source-coordinate norm used for a chart Hessian packet and
`||v||_W=sqrt(v^T Wv)` the physical metric norm.

Assume the entire segment

`{z-thG(z): 0<=t<=1}`

stays in the chart cell and the source proves

**(5.1)**
`||D^2T(u)[v,v]||_W <= K_T ||v||_Z^2`

for every segment point `u` and relevant `v`.

Then from (4.3),

`||r_curv||_W`
` <= h^2 ∫_0^1 (1-t) K_T ||G||_Z^2 dt`
` = (K_T/2) h^2 ||G||_Z^2`.

Hence if additionally

`||G(z)||_Z^2 <= B_G`,

we obtain

**Theorem 5.1 — curvature defect norm cap**

**(5.2)** `||r_curv||_W <= (K_T/2) h^2 B_G`.

A source/checker that wants no square root or division can propose a rational
`D_curv>=0` and verify only

**(5.3)** `K_T^2 h^4 B_G^2 <= 4 D_curv`.

Then

**(5.4)** `Q_W(r_curv)<=D_curv`.

All trusted arithmetic in (5.3) is multiplication, addition and order.

### Composition with the existing P5 defect lanes

Suppose the exact physical corrector has already been bounded by

`Q_W(a_phys)<=q V`.

The normalized Euler image has the form

`a_phys+r_curv`.

Therefore `D_curv` is exactly an additive-defect packet of the same type used by
T-P5-078/T-P5-081. On a barrier `Vstar`, one may use the existing radical-free
independent-envelope gate with `D=D_curv`.

If the source proves a signed cross term

`<a_phys,r_curv>_W`

or a lower/upper correlation packet, T-P5-080 may consume it instead and avoid
the worst-case triangle geometry.

The curvature defect must be charged **once**. If an evaluator/source mismatch
already measures the same physical difference `T(z-hG)-x_E`, it must not be
charged again under a second label such as "chart motion".

---

## 6. The coefficient 1/2 is sharp

Consider the exact rational one-dimensional chart

`T(z)=z+z^2/2`

on the cell `[-1/2,1/2]`. Its derivative

`J(z)=1+z`

lies in `[1/2,3/2]`, so this is a valid local diffeomorphic chart. Its Hessian is
identically `1`, hence `K_T=1` in the ordinary absolute-value norm.

Take

`z=0`, `h=1`, `G=1/2`.

Then

`z-hG=-1/2`

stays in the cell, and

`T(-1/2)=-3/8`.

The first-order affine prediction is

`T(0)-hJ(0)G = -1/2`.

Therefore the exact curvature remainder is

`r_curv = -3/8 - (-1/2) = 1/8`.

The bound (5.2) gives

`(K_T/2) h^2 G^2 = (1/2)*(1/4)=1/8`.

Equality holds. Thus no uniform coefficient smaller than `1/2` is possible from
a Hessian operator bound alone.

---

## 7. Exact corrector counterexample with the same physical field

The failure of conjugacy is already visible in the same rational polynomial
chart from Section 3.

Take

`F(x)=x`,

`T(z)=z+z^3`,

`z=1`, `h=1`.

Then

`x=T(1)=2`,

`J(1)=4`,

`G(1)=F(2)/4=1/2`.

The physical Euler/corrector step is

`x_E = 2-2 = 0`.

But the normalized Euler step gives

`z_E = 1-1/2 = 1/2`,

whose physical image is

`T(1/2)=5/8`.

Hence

**(7.1)** `r_curv=5/8`.

So even when the physical corrector lands exactly at the root in one step, a
nonlinear-coordinate Euler step with the same `h` need not do so. Reusing
T-P5-079's exact-conjugacy statement outside the affine class can therefore turn
an exact zero-error step into a substantial false residual.

---

## 8. Why a pointwise pullback metric does not repair the finite secant theorem

For two points `z,y`, the physical chord is

`T(z)-T(y)`.

By the segment identity,

`T(z)-T(y)=J_bar(z,y)(z-y)`,

where

`J_bar(z,y)=∫_0^1 J(y+t(z-y))dt`.

Therefore the exact physical chord energy is

`Q_W(T(z)-T(y))`
` = (z-y)^T [J_bar^T W J_bar] (z-y)`.

The exact metric for a finite chord is thus a **two-point mean-Jacobian metric**,
not the pointwise pullback metric `M(z)=J(z)^T WJ(z)`.

Likewise

`F(T(z))-F(T(y))`

is not generally `J_bar(G(z)-G(y))`. Thus the affine three-way identity behind
T-P5-079 has no direct nonlinear analogue with a one-point metric.

This is the structural reason the finite secant constants and one-step corrector
cannot simply be declared coordinate invariant.

---

## 9. Minimal source-to-math typed contract

### Differential/Riemannian lane

For each chart cell, the mathematically sufficient packet is:

1. `T(t,z)` is `C^2` in source coordinates on the cell;
2. `J=D_zT` is full-rank/invertible on the cell;
3. fixed physical SPD weight `W`;
4. cleared transformed-field identity
   `J G = F(t,T)+T_t`;
5. physical Jacobian `A=D_xF(t,T)` and the physical symmetric packet
   `A^T W+WA >= 2 mu W`.

Then the adapter may *derive* `M=J^T WJ` and Theorem 1.1. It does not need a
separate numerical Hessian budget merely to preserve the differential rate.

If differentiating the covariance inside the trusted layer is inconvenient, the
source may instead provide the exact connection identity

`DJ[G]+JDG = AJ+J_t`.

That identity plus `M=J^TWJ` is sufficient for the pure matrix-algebra leaf.

### Finite-step/corrector lane

To consume a nonlinear normalized Euler step, add:

1. same-time covariance `J(z)G(z)=F(T(z))`;
2. segment inclusion `z-thG(z)` stays inside the chart cell for `0<=t<=1`;
3. Hessian bilinear cap `K_T` on that whole segment;
4. squared source-field cap `||G||_Z^2<=B_G`;
5. rational `D_curv` satisfying
   `K_T^2 h^4 B_G^2<=4D_curv`.

Then the only downstream interface is

`Q_W(r_curv)<=D_curv`.

No theorem may silently set `D_curv=0` unless the chart is affine along the
whole step segment or an exact source identity proves the remainder vanishes.

---

## 10. Recommended Lean decomposition

Do not formalize the entire nonlinear flow in one theorem. The clean split is:

1. `pullback_metric_directional_derivative`:
   expand `D(J^T WJ)[g]`;
2. `differentiated_chart_covariance`:
   from `JG=F∘T+T_t`, derive
   `DJ[G]+JDG=AJ+J_t` using Hessian symmetry;
3. `nonlinear_connection_congruence`:
   prove the pure matrix identity
   `DM[G]+DG^TM+MDG-M_t = J^T(A^TW+WA)J`;
4. `pullback_differential_decay`:
   consume a Loewner lower bound and the variational ODE;
5. `nonlinear_euler_curvature_integral`:
   prove (4.2)/(4.3);
6. `curvature_defect_sq_le_of_hessian_cap`:
   consume the segment Hessian and `G` caps and output the multiplication-only
   squared budget.

The first four are differential/Riemannian mathematics. The last two are the
finite-step bridge back to the existing P5 corrector architecture. Keeping them
separate prevents a compiled differential theorem from being misread as a
finite-step secant certificate.

---

## 11. Boundaries that remain open

This review does **not** establish:

- that the deployed P5 SCC actually uses a nonlinear chart;
- an exact source definition/hash for any deployed `T,J,D^2T,G`;
- chart injectivity or image coverage on the physical source domain;
- the rational `K_T` or `B_G` needed for a concrete curvature budget;
- segment inclusion for the actual step size;
- evaluator/FD/controller/Float64 semantics;
- root existence or corrector coverage;
- P8/ODE trajectory transport;
- Lean/kernel compilation or `#print axioms`;
- independent validation by 封不觉;
- comparator/admission/registry or P5/M4 closure.

The main mathematical conclusion is narrower but decisive:

> nonlinear coordinate changes preserve the **differential contraction geometry**
> exactly through the pullback metric, but they do **not** preserve the finite
> secant/corrector packet for free. The missing finite-step price is an exact
> chart-curvature remainder, with sharp leading coefficient `1/2`, and that
> remainder belongs in the existing additive/correlation-aware defect interface.
