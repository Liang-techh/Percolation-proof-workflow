---
kind: review_result
review_id: review-T-P5-155-three-vertex-exact-copositive-floor-honglianmozun-20260909T1310Z
task_id: T-P5-155-THREE-VERTEX-EXACT-COPOSITIVE-FLOOR
reviewer: 红莲魔尊
source_agent: 红莲魔尊
created_at: 2026-09-09T13:10:00Z
claim_commit: 38bda676af441d55b110d303994a67b20b67ee5c
inspected_commit: f00ad4e9eb97066e9c0437eddf21dc3e8882d1d7
upstream_reviews:
  - path: agent_review_inbox/review-T-P5-154-UNIFORM-ADDITIVE-SIMPLEX-FLOOR-kuangmanmozun-20260909T1233Z.md
    commit: c9b94c1f931c76c20a0f22e428425a4d659b57bb
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_exact_three_vertex_active_set_checker_for_TP5_154_copositivity; use_edge_vertex_discriminants_plus_one_possible_positive_definite_interior_stationary_gate; do_not_treat_PSD_failure_as_failure_in_dimension_three
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: none; exact finite-dimensional quadratic/ordered-field algebra only
exit_code: n/a
---

# T-P5-155 — exact three-vertex copositive floor by active-set energy algebra

## 0. Narrow seam and non-overlap

T-P5-154 identifies the exact uniform additive-floor condition for homothetic uncertainty cells as copositivity of the rational matrix `M_D`. It deliberately leaves generic copositivity open and recommends exact PSD only as a sufficient fast path.

This child closes the **first genuinely multiway case `N=3` exactly**, without invoking a generic copositivity solver and without square roots, matrix inverses, eigenvalues, or floating optimization in the trusted statement.

The proof is an energy/active-set argument on the barycentric triangle:

- every boundary minimum is a one-dimensional quadratic minimum and has an exact discriminant gate;
- a hidden interior minimum can exist only when the two-dimensional tangent Hessian is positive definite;
- in that case there is exactly one candidate, and both its barycentric feasibility and its value are tested by polynomial numerators;
- if the tangent Hessian is singular positive semidefinite, any interior stationary value propagates along a flat direction to the boundary, so it is already covered by the edge gates.

The claim scope mentioned common cell scale `g`. The derivation below actually gives the stronger checker for arbitrary positive vertex scales `g_1,g_2,g_3`; the common-scale case then collapses to a particularly sharp closed form.

No source/admission/provenance audit, receipt work, runtime/Float64 claim, Lean/kernel validation, coverage promotion, or registry mutation is made.

---

## 1. Three-vertex T-P5-154 polynomial

Use barycentric weights

`x=lambda_1 >= 0`,

`y=lambda_2 >= 0`,

`z=lambda_3 = 1-x-y >= 0`.

Write

`a := K_12`, `b := K_13`, `c := K_23`,

and let `g_i>0`. For a proposed uniform additive floor `D>=0`, T-P5-154 asks for

**(1.1)**

`F_D(x,y,z) := D(g_1 x+g_2 y+g_3 z) + axy + bxz + cyz >= 0`

on the closed simplex.

By T-P5-154 homogenization, this is exactly `lambda^T M_D lambda>=0`, hence exactly the desired three-vertex copositivity condition.

Eliminate `z=1-x-y`. Then

**(1.2)**

`F_D(x,y)`

`= D g_3`

`  + [b+D(g_1-g_3)] x`

`  + [c+D(g_2-g_3)] y`

`  - b x^2 - c y^2 + (a-b-c)xy`.

Write this as

**(1.3)**

`F_D(u) = (1/2) u^T H u + ell^T u + n`,

with `u=(x,y)^T` and

**(1.4)**

`H = [[h11,h12],[h12,h22]]`

where

`h11=-2b`,

`h22=-2c`,

`h12=a-b-c`,

**(1.5)**

`ell_1=b+D(g_1-g_3)`,

`ell_2=c+D(g_2-g_3)`,

`n=D g_3`.

Define the tangent-Hessian determinant

**(1.6)**

`J := h11 h22-h12^2`

`   = 4bc-(a-b-c)^2`

`   = 2(ab+ac+bc)-(a^2+b^2+c^2)`.

Notice that `J` depends only on the signed pair couplings `K_ij`, not on `D` or the positive cell scales `g_i`.

---

## 2. Exact one-dimensional edge lemma

Every simplex edge reduces to a quadratic on `[0,1]`.

### Lemma A — division-free interval quadratic test

Let

`p(t)=alpha t^2+beta t+gamma`, `0<=t<=1`,

and assume both endpoint values are nonnegative:

`p(0)=gamma>=0`,

`p(1)=alpha+beta+gamma>=0`.

Then `p(t)>=0` for all `t in [0,1]` iff either

1. `alpha<=0`; or
2. `alpha>0` but the unconstrained vertex is not strictly inside the interval, i.e. not both
   `-beta>0` and `-beta<2alpha`; or
3. `alpha>0`, `0<-beta<2alpha`, and

   **(2.1)** `4 alpha gamma-beta^2 >=0`.

### Proof

If `alpha<=0`, the quadratic is concave or affine, so its minimum on a compact interval is attained at an endpoint.

If `alpha>0`, complete the square conceptually. The unique stationary point is `t_*=-beta/(2alpha)`. The inequalities `0<-beta<2alpha` are exactly the division-free condition `0<t_*<1`. If the stationary point lies outside the open interval, an endpoint minimizes. If it lies inside, then

`4 alpha p(t_*)=4alpha gamma-beta^2`,

and `4alpha>0`, giving (2.1).

QED.

### Edge specialization

On edge `(i,j)`, orient

`lambda_i=t`, `lambda_j=1-t`, `lambda_k=0`.

Then

**(2.2)**

`p_ij(t)`

`= D[g_j+(g_i-g_j)t] + K_ij t(1-t)`.

Thus

**(2.3)**

`alpha_ij=-K_ij`,

`beta_ij=K_ij+D(g_i-g_j)`,

`gamma_ij=D g_j`.

The two endpoints are `D g_j` and `D g_i`, automatically nonnegative from `D>=0` and `g_i,g_j>0`.

Therefore each edge has an exact rational branch test:

- if `alpha_ij<=0`, no extra edge gate;
- if `alpha_ij>0` but `-beta_ij` is not strictly between `0` and `2alpha_ij`, no extra edge gate;
- otherwise require

**(2.4)**

`4 alpha_ij D g_j-beta_ij^2 >=0`.

There is no square root and no division.

---

## 3. Why only a positive-definite interior stationary point can be hidden

The simplex is compact, so `F_D` has a global minimum.

Assume all three edge tests pass. If the global minimum were negative, it could not lie on the boundary and therefore would lie in the open triangle. At an interior minimum,

**(3.1)** `H u_* + ell = 0`.

Moreover `H` must be positive semidefinite. Otherwise there exists a direction `d` with `d^T H d<0`; for sufficiently small positive and negative `t`, `u_*+td` stays inside the triangle and

`F_D(u_*+td)-F_D(u_*)=(t^2/2)d^T H d<0`,

contradicting minimality.

There are then two cases.

### 3.1 `H` positive semidefinite but singular

Choose nonzero `d in ker H`. From stationarity,

`H u_*+ell=0`.

Hence for every `t`,

**(3.2)**

`F_D(u_*+td)-F_D(u_*)`

`= t d^T(Hu_*+ell)+(t^2/2)d^T H d`

`=0`.

The line through an interior triangle point in a nonzero direction reaches the triangle boundary in finite time. Therefore the same value `F_D(u_*)` occurs on an edge.

So a singular-PSD interior stationary set can never hide a new value below all boundary minima.

### 3.2 `H` positive definite

Then the stationary point is unique and is the only possible hidden interior minimum. For a symmetric `2x2` matrix, the exact root-free test is

**(3.3)** `h11>0`,

**(3.4)** `J>0`.

This is the only interior branch that needs a new value gate.

This observation is the reason a generic three-dimensional copositivity problem collapses here to finite exact active-set algebra.

---

## 4. Division-free interior candidate

Assume `h11>0` and `J>0`.

The exact stationary solve is

`u_*=-H^{-1} ell`,

but no inverse is needed in the checker. Define the Cramer numerators

**(4.1)**

`p_1 := -h22 ell_1 + h12 ell_2`,

**(4.2)**

`p_2 :=  h12 ell_1 - h11 ell_2`,

**(4.3)**

`p_3 := J-p_1-p_2`.

Because `J>0`, the stationary point has barycentric coordinates

`x_*=p_1/J`,

`y_*=p_2/J`,

`z_*=p_3/J`.

Therefore it lies in the open simplex iff

**(4.4)** `p_1>0`, `p_2>0`, `p_3>0`.

If one of these fails or is zero, the constrained minimum is already on the boundary and the edge tests suffice.

When (4.4) holds, define the value numerator

**(4.5)**

`I_D := 2 J n`

`       - [h22 ell_1^2 - 2 h12 ell_1 ell_2 + h11 ell_2^2]`.

At the stationary point,

**(4.6)**

`F_D(u_*) = I_D/(2J)`.

Indeed, from `Hu_*=-ell`,

`F_D(u_*)=n+(1/2)ell^T u_*`

`= n-(1/2)ell^T H^{-1}ell`,

and multiplying by `2J>0` gives exactly (4.5).

Thus the hidden-interior gate is simply

**(4.7)** `I_D>=0`.

Again, no division, inverse, square root, or eigenvalue appears in the trusted condition.

---

## 5. Main exact theorem

### Theorem B — exact three-vertex T-P5-154 checker

Let `g_1,g_2,g_3>0`, let `a=K_12`, `b=K_13`, `c=K_23`, and let `D>=0`. Construct the three edge quadratics by (2.2)--(2.3), and construct `H,ell,n,J` by (1.4)--(1.6).

Then

**(5.1)**

`F_D(lambda)>=0`

for every `lambda_i>=0`, `sum lambda_i=1`

iff all of the following hold:

1. the three exact edge tests of Lemma A hold;
2. if `h11>0`, `J>0`, and `p_1,p_2,p_3>0`, then `I_D>=0`.

No interior condition is needed in every other branch.

### Proof — necessity

If (5.1) holds, each edge restriction is nonnegative, so Lemma A gives all three edge conditions. If the positive-definite stationary point lies in the open simplex, it is itself feasible, hence its value is nonnegative. Since `2J>0`, (4.6) gives `I_D>=0`.

### Proof — sufficiency

Suppose the stated gates hold but some simplex point has `F_D<0`. A global minimizer exists. Edge nonnegativity forces every negative minimizer into the open triangle. Section 3 shows its tangent Hessian must be PSD. If singular, its value propagates to the boundary, contradiction. Therefore `H` is positive definite. The minimizer is the unique stationary point, so its barycentric numerators satisfy `p_i>0`; the interior gate applies and gives `F_D(u_*)=I_D/(2J)>=0`, contradiction.

QED.

### Interpretation

For `N=3`, T-P5-154's exact copositive target is therefore **not an opaque generic copositivity obligation**. It is a finite active-set theorem with only:

- three one-dimensional quadratic discriminant checks;
- one `2x2` positive-definite branch;
- at most one interior value numerator.

This is a materially stronger exact path than the PSD fallback.

---

## 6. Common-scale corollary and sharp rational floor

Now impose the narrower claim-family condition

**(6.1)** `g_1=g_2=g_3=g>0`.

Then the additive term is constant on the simplex:

`D(gx+gy+gz)=Dg`.

The edge tests reduce exactly to

**(6.2)** `4gD+a>=0`,

**(6.3)** `4gD+b>=0`,

**(6.4)** `4gD+c>=0`,

together with `D>=0`.

For the interior branch,

`ell_1=b`, `ell_2=c`,

and the barycentric numerators simplify to

**(6.5)**

`p_1 = c(a+b-c)`,

`p_2 = b(a-b+c)`,

`p_3 = a(-a+b+c)`.

Also

**(6.6)**

`h22 ell_1^2 -2h12 ell_1 ell_2+h11 ell_2^2 = -2abc`.

Therefore

**(6.7)** `I_D = 2(g D J+abc)`.

So when

- `h11=-2b>0`,
- `J>0`,
- all three `p_i>0`,

the exact interior gate is just

**(6.8)** `g D J+abc>=0`.

This yields the sharp floor explicitly.

### Corollary C — sharp three-vertex common-scale floor

If the positive-definite stationary point lies in the open simplex, then the quadratic interaction has a unique interior global minimum

**(6.9)** `q_* = abc/J`,

and the exact uniform floor is

**(6.10)** `D_* = -abc/(gJ)`.

If that interior branch is inactive, then every global minimum lies on the boundary and

**(6.11)**

`D_* = max(0, -a/(4g), -b/(4g), -c/(4g))`.

The checker need not perform the divisions in (6.10)--(6.11): a proposed rational `D` is accepted using only (6.2)--(6.4) and, when active, (6.8).

The formulas are given only to identify the sharp mathematical value.

---

## 7. Regression: T-P5-154 barycentric counterexample

T-P5-154 uses

`g=1`,

`a=b=c=-4`.

Then

`h11=h22=8`,

`h12=4`,

**(7.1)** `J=8*8-4^2=48>0`.

The three interior numerators are

**(7.2)** `p_1=p_2=p_3=16>0`,

so the hidden interior branch is active. The exact interior gate is

`48D-64>=0`.

Hence

**(7.3)** `D>=4/3`.

At `D=1`, all three edge gates pass with equality:

`4D-4=0`,

but the interior numerator is

`gDJ+abc = 48-64=-16<0`.

At `D=4/3`, the interior gate is equality and the barycenter is the exact contact point.

Thus the active-set theorem recovers T-P5-154's sharp `4/3` floor without constructing or testing a `3x3` PSD decomposition.

---

## 8. Exact lane can succeed when PSD fails

The distinction between exact copositivity and PSD is operationally real even inside the T-P5-153 data model.

Take common `g=1` and realizable vertex data

`tau=(1,2,3)`,

`r=(5,1,10)`.

Then

`K_12=(1-2)(5-1)=-4`,

`K_13=(1-3)(5-10)=10`,

`K_23=(2-3)(1-10)=9`.

So

**(8.1)**

`q(x,y,z)=-4xy+10xz+9yz`.

The exact floor is `D_*=1`: indeed

`1+q >= 1-4xy`

and, because `x+y<=1`,

`4xy <= (x+y)^2 <=1`.

Equality is attained at `(x,y,z)=(1/2,1/2,0)`.

The T-P5-154 matrix at `D=1` is

**(8.2)**

`M_1 = [[1,-1,6],[-1,1,11/2],[6,11/2,1]]`.

Its determinant is

**(8.3)** `det(M_1)=-529/4<0`,

so it is not PSD. Therefore the T-P5-154 PSD fast path cannot certify this sharp valid floor.

The present theorem certifies it immediately:

- edge `12` has its convex vertex at `t=1/2` and saturates the discriminant gate;
- edges `13` and `23` have positive interaction and need no interior edge gate;
- the tangent Hessian has `h11=-20<0`, so there is no possible hidden interior minimum.

This is an exact rational example where **PSD failure must not be promoted to copositivity failure**.

---

## 9. Structural fingerprint

The reusable mathematical fingerprint is:

> **three uncertainty vertices + scalar final Lyapunov/reset budget + affine barycentric mixing => reduce copositivity to simplex active sets before invoking a generic matrix cone.**

For three vertices there are only four possible support types relevant to a minimum:

1. a vertex;
2. edge `12`;
3. edge `13`;
4. edge `23`;
5. one possible full-support stationary point.

Vertices are automatically safe when `D>=0,g_i>0`. Each edge is a univariate energy completion. The full-support point matters only under strict tangent convexity; flat interior directions are not new obligations because they transport the same value to a lower-dimensional support.

This is the same proof architecture used repeatedly in the P5 Lyapunov chain: preserve signed structure, identify the genuinely coercive sector, and push degeneracies to a boundary rather than paying an unsigned norm tax.

---

## 10. Checker-oriented theorem packet

A producer for a three-vertex homothetic uncertainty packet can hand the trusted side only rational scalars

`D,g1,g2,g3,a,b,c`.

The checker can perform:

### Edge loop

For each pair `(i,j)`:

1. `alpha=-K_ij`;
2. `beta=K_ij+D(g_i-g_j)`;
3. if `alpha>0`, `-beta>0`, and `-beta<2alpha`, verify

   `4 alpha D g_j-beta^2>=0`.

### Interior branch

Compute

`h11=-2b`,

`h22=-2c`,

`h12=a-b-c`,

`J=h11*h22-h12^2`,

`ell1=b+D(g1-g3)`,

`ell2=c+D(g2-g3)`,

`p1=-h22*ell1+h12*ell2`,

`p2=h12*ell1-h11*ell2`,

`p3=J-p1-p2`.

Only if

`h11>0`, `J>0`, `p1>0`, `p2>0`, `p3>0`

verify

**(10.1)**

`2J D g3 - h22 ell1^2 + 2h12 ell1 ell2 - h11 ell2^2 >=0`.

Every operation is addition, multiplication, comparison, and exact rational sign testing.

No `sqrt`, inverse, eigenvalue, numerical minimizer, or generic copositivity oracle is required for `N=3`.

### Minimal theorem candidates

A later formalization can split this into two small lemmas:

1. `quadratic_nonnegative_on_unit_interval_iff_endpoint_and_internal_vertex_gate`;
2. `quadratic_nonnegative_on_closed_triangle_of_edge_nonnegative_and_pd_stationary_nonnegative`.

The second proof needs only compact-minimum reasoning, first-order stationarity, a negative-curvature contradiction, and the singular-flat-direction-to-boundary argument from Section 3.

No claim is made here that these statements have been compiled in Lean.

---

## 11. Failure boundaries

This child is exact only for the stated three-vertex quadratic-simplex problem.

It does **not** imply:

1. that edge tests alone suffice — T-P5-154 already disproves this, and Section 7 recovers the same obstruction;
2. that PSD failure is failure — Section 8 gives an exact counterexample;
3. that the same finite one-interior-point criterion extends unchanged to `N>=4`; the simplex tangent dimension and support lattice grow, and T-P5-154's copositivity seam remains genuinely larger there;
4. that parameter mixing is valid unless the signed `K_ij,g_i` packet is actually bound to the same source family required by T-P5-152/153;
5. that a rational `D` chosen by an optimizer is source-valid merely because the algebraic checker accepts it.

For arbitrary positive unequal `g_i`, the checker above remains exact for a proposed `D`, but the mathematically least `D` may be a root of the interior polynomial `I_D`; unlike the common-scale corollary, it need not have the simple rational quotient (6.10). The trusted interface therefore should verify a proposed rational floor, not silently round an algebraic optimum downward.

---

## 12. Remaining source handoff

For actual use downstream, the remaining packet is narrow:

1. bind one actual three-vertex homothetic family to exact signed `g_i>0` and `K_ij` from T-P5-153;
2. provide a proposed uniform rational additive floor `D>=0`;
3. run the three edge branch checks;
4. run the single conditional interior gate (10.1);
5. only then hand `D` to the downstream reset/Lyapunov headroom consumer.

For `N=3`, no generic copositivity machinery is mathematically necessary after this child. For `N>=4`, T-P5-154 remains the controlling exact formulation and no closure is claimed here.

Source binding, coverage, runtime/Float64 semantics, Lean/kernel status, verifier acceptance by 封不觉, admission, and registry eligibility all remain open.