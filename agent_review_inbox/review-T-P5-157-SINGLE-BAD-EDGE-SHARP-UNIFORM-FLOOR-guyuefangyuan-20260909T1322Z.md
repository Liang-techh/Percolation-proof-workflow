---
kind: review_result
review_id: review-T-P5-157-single-bad-edge-sharp-uniform-floor-guyuefangyuan-20260909T1322Z
task_id: T-P5-157-SINGLE-BAD-EDGE-SHARP-UNIFORM-FLOOR
reviewer: 古月方源
source_agent: 古月方源
created_at: 2026-09-09T13:22:00Z
claim_commit: 5e5509b6f07fd1e33fa16123614eb7f3bf98ff60
inspected_commit: cf1d64b8d3b1a13ad412754e55a69b9c35b6006e
upstream_reviews:
  - path: agent_review_inbox/review-T-P5-153-HOMOTHETIC-SIMPLEX-SLACK-COUPLING-guyuefangyuan-20260909T1223Z.md
    commit: 64a4676b364a81dd196864d7677be2ee587e22c6
  - path: agent_review_inbox/review-T-P5-154-UNIFORM-ADDITIVE-SIMPLEX-FLOOR-kuangmanmozun-20260909T1233Z.md
    commit: c9b94c1f931c76c20a0f22e428425a4d659b57bb
  - path: agent_review_inbox/review-T-P5-155-three-vertex-exact-copositive-floor-honglianmozun-20260909T1310Z.md
    commit: b79e57e78e42aeba644b3e030a7e9a93d81eecf0
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_exact_arbitrary_dimension_single_bad_edge_copositive_reduction; use_two_regime_root_free_gate_for_uniform_floor; treat_midpoint_edge_floor_only_as_lower_bound_when_vertex_scales_differ
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: none; exact ordered-field/quadratic-form algebra only
exit_code: n/a
---

# T-P5-157 — a single negative pair collapses the full simplex floor to one exact edge

## 0. Narrow seam and non-overlap

T-P5-153 gives the exact homothetic simplex defect

`Delta_lambda = sum_{i<j} lambda_i lambda_j K_ij`

and the additive repair gate

`Delta_lambda + D g_lambda >= 0`,

where `g_lambda=sum_i lambda_i g_i` and every `g_i>0`.

T-P5-154 identifies the general full-simplex problem with copositivity of an explicit matrix `M_D`, and shows that edge-by-edge repair is not sufficient in general once several negative pair couplings can cooperate.

T-P5-155 closes the generic `N=3` case by an exact active-set checker.

This child isolates a different exact family that works in **arbitrary simplex dimension**:

> all pair coefficients are nonnegative except one pair `(a,b)`, where `K_ab=-kappa<0`.

For this sign pattern there is no multiway tax. The entire `N`-vertex copositivity problem is exactly equivalent to the two-vertex bad-edge problem. The sharp uniform additive floor therefore has a closed form, while the trusted checker can remain completely root-free and division-free.

No source/admission/provenance audit, receipt work, runtime/Float64 claim, Lean/kernel validation, or registry mutation is performed.

---

## 1. Setup

Let `lambda_i>=0`, `sum_i lambda_i=1`, and `g_i>0`.

Assume one distinguished pair `a != b` satisfies

**(1.1)** `K_ab=-kappa`, with `kappa>0`,

and every other unordered pair satisfies

**(1.2)** `K_ij>=0` for `{i,j}!={a,b}`.

Define

**(1.3)** `g_lambda := sum_i lambda_i g_i`,

**(1.4)** `Delta_lambda := sum_{i<j} lambda_i lambda_j K_ij`.

For a proposed uniform additive floor `D>=0`, T-P5-153/T-P5-154 require

**(1.5)** `F_D(lambda) := Delta_lambda + D g_lambda >=0`

for every simplex weight.

The question is whether all the other vertices can cooperate with the one negative edge and require a larger `D` than the edge itself.

They cannot.

---

## 2. Exact arbitrary-dimensional reduction to the bad edge

### Theorem A — single-bad-edge reduction

Under (1.1)--(1.2), for every `D>=0`, the following are equivalent:

1. `F_D(lambda)>=0` for every `lambda` in the full `N`-vertex simplex;
2. for every `t in [0,1]`,

   **(2.1)**

   `q_D(t) := D[g_a t+g_b(1-t)] - kappa t(1-t) >=0`.

Thus the exact full-simplex uniform floor is the exact floor on edge `(a,b)`.

### Proof — necessity

Restrict the simplex to the bad edge:

`lambda_a=t`, `lambda_b=1-t`, all other `lambda_i=0`.

Then every pair term vanishes except `K_ab lambda_a lambda_b`, and (1.5) becomes exactly (2.1).

### Proof — sufficiency by mass dilution

Take an arbitrary simplex point. Let

`s := lambda_a+lambda_b`.

If `s=0`, the bad term vanishes and every remaining pair term plus `D g_lambda` is nonnegative.

Assume `s>0` and set

`t := lambda_a/s`.

Then `lambda_a=s t`, `lambda_b=s(1-t)`. Because all other pair terms are nonnegative,

`Delta_lambda >= -kappa s^2 t(1-t)`.

Also, because all omitted `g_i` terms are positive,

`g_lambda >= s[g_a t+g_b(1-t)]`.

Hence

`F_D(lambda)`

`>= -kappa s^2 t(1-t)
    + D s[g_a t+g_b(1-t)]`

`= s { D[g_a t+g_b(1-t)]
       - kappa s t(1-t) }`

`>= s { D[g_a t+g_b(1-t)]
       - kappa t(1-t) }`

because `0<s<=1`.

The last brace is `q_D(t)>=0` by hypothesis, so `F_D(lambda)>=0`.

QED.

### Structural interpretation

Mass placed outside the only negative edge is beneficial twice:

- it contributes positive `D g_i lambda_i`;
- it reduces the bad product from `t(1-t)` to `s^2 t(1-t)`.

Therefore an interior multiway minimizer cannot beat the bad edge when the negative-pair graph has only one edge.

This is exactly the sign-pattern regime in which T-P5-154's general copositivity problem collapses to one two-dimensional principal cone.

---

## 3. Equivalent T-P5-154 matrix statement

T-P5-154 defines the homogeneous symmetric matrix `M_D` by

`M_D[i,i]=D g_i`,

`2 M_D[i,j]=K_ij+D(g_i+g_j)`.

For a nonnegative vector `x`, every term involving a good pair is nonnegative, as are all diagonal terms. The only potentially negative cross term is `(a,b)`.

Therefore:

### Corollary A1 — full copositivity iff one principal block is copositive

Under (1.1)--(1.2), `M_D` is copositive iff its `(a,b)` principal block

**(3.1)**

`B_D = [[D g_a, (D(g_a+g_b)-kappa)/2],
        [(D(g_a+g_b)-kappa)/2, D g_b]]`

is copositive on `R_+^2`.

This is stronger than a generic PSD sufficient test: `M_D` itself need not be PSD. The exact nonnegative-orthant question is decided by one `2 x 2` copositive block because every omitted monomial has nonnegative coefficient.

---

## 4. Exact root-free two-regime checker

The edge polynomial can also be written homogeneously. For `x,y>=0`, define

**(4.1)**

`Q_D(x,y)
 = D g_a x^2 + D g_b y^2
   + [D(g_a+g_b)-kappa] x y`.

By normalization `(x,y) -> (t,1-t)`, nonnegativity of `Q_D` on the nonnegative quadrant is equivalent to (2.1).

Define the signed cross deficit

**(4.2)**

`L_D := kappa - D(g_a+g_b)`.

Then

`Q_D = D g_a x^2 + D g_b y^2 - L_D x y`.

### Theorem B — exact division-free gate

Assume `kappa>0`, `g_a>0`, `g_b>0`, `D>=0`. Then the following are equivalent:

1. `q_D(t)>=0` for all `t in [0,1]`;
2. `Q_D(x,y)>=0` for all `x,y>=0`;
3. the following root-free disjunction holds:

   **(4.3)**

   `L_D <= 0`

   **or**

   **(4.4)**

   `L_D^2 <= 4 D^2 g_a g_b`.

There is no square root, matrix inverse, eigenvalue, or division in the trusted gate.

### Proof — easy branch `L_D<=0`

Then the cross coefficient `-L_D` is nonnegative, so every monomial in `Q_D` has nonnegative coefficient for `x,y>=0`.

### Proof — sufficient hard branch

Assume `L_D>0` and (4.4). Put

`A := D g_a x^2 + D g_b y^2`,

`B := L_D x y`.

Both are nonnegative. Exact algebra gives

**(4.5)**

`A^2-B^2`

`= (D g_a x^2-D g_b y^2)^2
   + [4D^2 g_a g_b-L_D^2] x^2 y^2`

`>=0`.

Thus `A>=B`, hence `Q_D=A-B>=0`.

This proof is pure polynomial/order algebra after the sign hypotheses.

### Proof — necessity of the squared gate when `L_D>0`

Suppose instead

`L_D^2 > 4 D^2 g_a g_b`.

If `D=0`, then `Q_D(1,1)=-kappa<0`.

If `D>0`, choose the completely algebraic positive witness

**(4.6)** `x=L_D`, `y=2D g_a`.

Then

**(4.7)**

`Q_D(L_D,2D g_a)
 = D g_a [4D^2 g_a g_b-L_D^2] <0`.

So the quadrant condition fails.

QED.

### Checker form

For exact rational packet data, the trusted consumer only needs to compute

`L = kappa-D*(g_a+g_b)`

and accept if

`L<=0 || L*L <= 4*D*D*g_a*g_b`.

This is much smaller than a generic copositivity or SDP check.

---

## 5. Conceptual sharp floor

The trusted theorem does not need radicals, but the exact mathematical optimum has a simple closed form.

Let

`A=sqrt(g_a)`, `B=sqrt(g_b)`.

The identity

**(5.1)**

`g_a t+g_b(1-t)
 - (A+B)^2 t(1-t)
 = [A t-B(1-t)]^2`

shows

`g_a t+g_b(1-t) >= (A+B)^2 t(1-t)`.

Hence the sharp uniform floor is

**(5.2)**

`D_* = kappa/(sqrt(g_a)+sqrt(g_b))^2`.

Equality occurs at

**(5.3)**

`t_* = sqrt(g_b)/(sqrt(g_a)+sqrt(g_b))`.

Therefore the full `N`-vertex simplex has the same exact optimum, attained on the unique bad edge.

At `D=D_*`, the hard-branch polynomial gate is saturated:

`L_D^2 = 4 D^2 g_a g_b`.

So the root-free gate does not merely give a sufficient rational envelope; it exactly characterizes the sharp threshold.

---

## 6. T-P5-153 midpoint repair is sharp only at equal scales

T-P5-153 records the bad-edge midpoint lower bound

**(6.1)**

`D_mid = kappa/[2(g_a+g_b)]`.

From

`2 sqrt(g_a g_b) <= g_a+g_b`,

we have

`(sqrt(g_a)+sqrt(g_b))^2
 = g_a+g_b+2sqrt(g_a g_b)
 <= 2(g_a+g_b)`.

Therefore

**(6.2)** `D_* >= D_mid`,

with equality iff `g_a=g_b`.

Thus the midpoint witness is a sharp edge obstruction only for equal vertex scales. When the `g` values differ, the worst barycentric point moves away from `1/2`.

### Exact rational regression

Take

`g_a=4`, `g_b=1`, `kappa=9`.

Then

`D_mid = 9/[2(5)] = 9/10`,

whereas

`D_* = 9/(2+1)^2 = 1`.

At the midpoint and `D=9/10`,

`q_D(1/2)=0`.

So the midpoint lower bound appears saturated.

But at the actual worst point `t=1/3`,

`q_{9/10}(1/3)
 = (9/10)*2 - 9*(2/9)
 = 9/5-2
 = -1/5 <0`.

At the true sharp floor `D=1`,

**(6.3)**

`q_1(t)
 = 4t+(1-t)-9t(1-t)
 = (3t-1)^2 >=0`,

with equality exactly at `t=1/3`.

This is a useful regression for any implementation that is tempted to promote midpoint edge checks to exact unequal-scale floors.

---

## 7. No multiway tax, but only under the one-negative-edge hypothesis

The theorem must not be generalized by slogan.

T-P5-154 already provides a three-vertex counterexample with three negative pair couplings where every edge passes but the simplex barycenter fails. That mechanism is impossible here only because there is exactly one negative pair monomial.

If a second negative pair is introduced, even if each negative edge individually has a valid local floor, interactions among supports can matter again. No claim is made here for an arbitrary negative-edge graph.

A natural future mathematical child would classify graph patterns for which edge-local copositivity remains exact. A matching of negative edges is a plausible next tractable family, but it is not proved in this review.

---

## 8. Minimal source-facing packet

To consume this theorem for an actual homothetic uncertainty packet, source/CSE should freeze, under one common source/config/domain key:

1. positive vertex scales `g_i`;
2. exact pair coefficients `K_ij` from the already-signed T-P5-153 slack algebra;
3. one distinguished pair `(a,b)` with a certified `K_ab=-kappa<0`;
4. exact sign certificates `K_ij>=0` for every other pair;
5. a proposed rational uniform floor `D>=0`;
6. the root-free scalar gate

   `L=kappa-D(g_a+g_b)`,

   `L<=0 || L^2<=4D^2 g_a g_b`.

No continuum parameter sweep, interior simplex optimizer, generic copositivity solve, square root, or SDP is needed for this sign pattern.

Necessity as a physical storage obstruction still inherits the same boundary-attainability/domain qualification as T-P5-153/T-P5-154. Sufficiency of the algebraic additive repair does not require that extra attainability premise.

---

## 9. Suggested Lean theorem decomposition

The most valuable trusted leaves are scalar/order algebra first.

### Leaf 1 — hard-branch two-variable quadratic

```lean
theorem twoVar_nonneg_of_crossSquare
    {κ ga gb D x y : ℝ}
    (hκ : 0 < κ) (hga : 0 < ga) (hgb : 0 < gb)
    (hD : 0 ≤ D) (hx : 0 ≤ x) (hy : 0 ≤ y)
    (hL : 0 < κ - D * (ga + gb))
    (hsq : (κ - D * (ga + gb))^2 ≤ 4 * D^2 * ga * gb) :
    0 ≤ D*ga*x^2 + D*gb*y^2
        + (D*(ga+gb)-κ)*x*y := by
  -- ring identity (4.5), positivity, nlinarith/order algebra
```

### Leaf 2 — easy cross-sign branch

```lean
theorem twoVar_nonneg_of_crossNonneg
    {κ ga gb D x y : ℝ}
    (hga : 0 ≤ ga) (hgb : 0 ≤ gb)
    (hD : 0 ≤ D) (hx : 0 ≤ x) (hy : 0 ≤ y)
    (hL : κ ≤ D * (ga + gb)) :
    0 ≤ D*ga*x^2 + D*gb*y^2
        + (D*(ga+gb)-κ)*x*y := by
  positivity
```

### Leaf 3 — exact failure witness

```lean
theorem twoVar_negative_witness_of_crossSquare_fail
    {κ ga gb D : ℝ}
    (hκ : 0 < κ) (hga : 0 < ga) (hgb : 0 < gb)
    (hD : 0 < D)
    (hL : 0 < κ - D * (ga + gb))
    (hfail : 4 * D^2 * ga * gb < (κ - D*(ga+gb))^2) :
    D*ga*(κ-D*(ga+gb))^2
      + D*gb*(2*D*ga)^2
      + (D*(ga+gb)-κ)*(κ-D*(ga+gb))*(2*D*ga) < 0 := by
  ring_nf
  nlinarith
```

### Leaf 4 — simplex reduction

A finite-sum theorem should state that if all `K_ij>=0` except `(a,b)=-κ`, then bad-edge nonnegativity implies `Delta_lambda+D*g_lambda>=0` for every simplex `lambda`. This leaf uses only nonnegative finite sums plus the scalar edge theorem.

### Leaf 5 — optional exact equivalence

Package the two branches as

```lean
singleBadEdge_floor_iff :
  (∀ λ ∈ simplex, 0 ≤ Delta λ + D * g λ)
  ↔
  (let L := κ - D*(ga+gb)
   L ≤ 0 ∨ L^2 ≤ 4*D^2*ga*gb)
```

with the boundary restriction furnishing the reverse direction.

The radical formula (5.2) should remain a corollary/interpretation, not a prerequisite for the trusted checker.

---

## 10. Open obligations and handoff

This review closes only the mathematical sign-pattern reduction. It does **not** prove that an actual source packet has exactly one negative `K_ij`.

The next source-facing step is therefore cheap and decisive:

- compute/freeze the exact `K_ij` table already implied by the T-P5-153 homothetic packet;
- count its strictly negative edges under exact rational signs;
- if exactly one exists, bypass generic T-P5-154 copositivity and consume this theorem;
- if zero exist, T-P5-153 already gives zero additive floor;
- if two or more exist, fail closed back to T-P5-154/T-P5-155 or a later graph-structured child.

Actual source binding, same-key/domain coverage, Float64/interval semantics, controller/FD/P8 integration, Lean/kernel receipt, independent verification by 封不觉, admission, and registry eligibility remain pending.

---

## 11. Status

`CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending`.

New mathematical content:

- arbitrary-dimensional exact reduction from one-negative-edge copositivity to one edge;
- exact two-regime root-free rational gate;
- algebraic strict-failure witness;
- conceptual sharp floor `kappa/(sqrt(g_a)+sqrt(g_b))^2`;
- exact proof that the midpoint lower bound is sharp iff the two cell scales agree;
- rational regression `g_a=4, g_b=1, kappa=9` separating midpoint `9/10` from true sharp floor `1`.
