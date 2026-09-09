---
kind: review_result
review_id: review-T-P5-164-negative-star-edge-decomposition-guyuefangyuan-20260909T1521Z
task_id: T-P5-164-NEGATIVE-STAR-EDGE-DECOMPOSITION
reviewer: 古月方源
source_agent: 古月方源
created_at: 2026-09-09T15:21:00Z
claim_commit: 3ad5526ea2d2ca6cbc124a35812fc3453a13c9f2
inspected_commit: 49030923232cf2c3c24c78bf49983eb81538f472
upstream_reviews:
  - path: agent_review_inbox/review-T-P5-153-HOMOTHETIC-SIMPLEX-SLACK-COUPLING-guyuefangyuan-20260909T1223Z.md
    commit: 64a4676b364a81dd196864d7677be2ee587e22c6
  - path: agent_review_inbox/review-T-P5-154-UNIFORM-ADDITIVE-SIMPLEX-FLOOR-kuangmanmozun-20260909T1233Z.md
    commit: c9b94c1f931c76c20a0f22e428425a4d659b57bb
  - path: agent_review_inbox/review-T-P5-157-SINGLE-BAD-EDGE-SHARP-UNIFORM-FLOOR-guyuefangyuan-20260909T1322Z.md
    commit: 4a42f46d6ce6b73b5a72b936e435b22ada5c5e25
  - path: agent_review_inbox/review-T-P5-158-FINITE-SUPPORT-KKT-COPOSITIVITY-DECISION-honglianmozun-20260909T1357Z.md
    commit: 8b3b4098f6c7e7bc2cdfa62dc9749f6d37736661
  - path: agent_review_inbox/review-T-P5-160-DEGENERATE-SUPPORT-KERNEL-BRANCH-guyuefangyuan-20260909T1432Z.md
    commit: 7024791953977bb79404d788d3d1246a20a37a57
  - path: agent_review_inbox/review-T-P5-162-TANGENT-PD-AFFINE-SUPPORT-CONTINUATION-honglianmozun-20260909T1502Z.md
    commit: 4cdafba95db0d3cfee9c29ace026e77eea8f88f1
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: detect_negative_edge_star_before_generic_copositivity; reduce_uniform_floor_to_finite_hub_leaf_gates; use_triangle_obstruction_to_fail_closed_outside_star_pattern
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: none; exact ordered-field and finite-sum algebra only
exit_code: n/a
---

# T-P5-164 — negative-star edge decomposition: exact arbitrary-dimensional floor from finitely many 2-vertex gates

## 0. Narrow seam and non-overlap

T-P5-153 gives the homothetic-simplex additive-floor problem in the scalar form

`F_D(lambda) := D g_lambda + Delta_lambda`,

where

`g_lambda = sum_i lambda_i g_i`,

`Delta_lambda = sum_{i<j} K_ij lambda_i lambda_j`,

with `lambda_i>=0`, `sum_i lambda_i=1`, and `g_i>0`.

T-P5-154 turns the fully general problem into copositivity of an explicit matrix. T-P5-157 proved that if there is only one negative pair coefficient, the entire simplex floor is exactly the floor of that one edge. T-P5-158/160/162 then develop generic support, singular-kernel, and tangent-PD machinery when several bad couplings can interact.

This child isolates the next exact graph family in arbitrary dimension:

> every negative pair coefficient is incident to one common hub vertex, while all leaf-leaf pair coefficients are nonnegative.

For this **negative-star** sign pattern, there is again no genuine multiway interior tax. The global continuum problem is exactly equivalent to finitely many hub/leaf two-vertex edge problems.

This is a mathematical reduction only. No source admission, provenance/receipt audit, Float64/runtime claim, registry mutation, Lean/kernel validation, or independent re-audit is performed.

---

## 1. Setup

Fix a distinguished hub vertex `0`. Let the other vertices be indexed by a finite leaf set `I`.

Assume

`lambda_0 >= 0`, `lambda_i >= 0`,

`lambda_0 + sum_{i in I} lambda_i = 1`,

and

`g_0 > 0`, `g_i > 0`.

For every leaf `i`, write the hub/leaf pair coefficient as

**(1.1)** `K_0i = -a_i`, with `a_i >= 0`.

The genuinely bad leaves are exactly those with `a_i>0`.

Assume every leaf/leaf pair is good:

**(1.2)** `K_ij >= 0` for all distinct `i,j in I`.

Define

**(1.3)**

`F_D(lambda)
 = D [g_0 lambda_0 + sum_i g_i lambda_i]
   - lambda_0 sum_i a_i lambda_i
   + sum_{i<j, i,j in I} K_ij lambda_i lambda_j`.

The source-facing question is:

> for a proposed rational `D>=0`, is `F_D(lambda)>=0` for every simplex point?

---

## 2. Main theorem: a negative star is exactly the intersection of its bad-edge gates

### Theorem A — negative-star reduction

Under (1.1)--(1.2), for every `D>=0`, the following are equivalent.

**Global condition**

**(2.1)** `F_D(lambda)>=0` for every simplex point `lambda`.

**Finite edge family**

For every leaf `i` and every `t in [0,1]`,

**(2.2)**

`E_i(D,t)
 := D [g_0 t + g_i(1-t)] - a_i t(1-t) >= 0`.

Hence the full `|I|+1` vertex simplex is safe exactly when every hub/leaf edge is safe.

### Proof — necessity

Fix a leaf `i` and restrict the simplex to the edge `{0,i}`:

`lambda_0=t`,

`lambda_i=1-t`,

all other coordinates zero.

Every leaf/leaf term vanishes and (1.3) becomes exactly (2.2). Therefore global nonnegativity implies every edge gate.

### Proof — sufficiency

Take an arbitrary simplex point and put

**(2.3)** `y := lambda_0`,

**(2.4)** `s := sum_i lambda_i = 1-y`.

If `s=0`, then `y=1`, the negative hub/leaf contribution vanishes, and

`F_D(lambda)=D g_0>=0`.

Assume now `s>0`.

For every leaf `i`, the pair `(y,s)` is itself a valid two-vertex simplex point because

`y>=0`, `s>=0`, `y+s=1`.

Therefore the edge hypothesis (2.2), evaluated at `t=y`, gives

**(2.5)**

`a_i y s <= D(g_0 y + g_i s)`.

Multiply (2.5) by the nonnegative weight `lambda_i` and sum over `i`:

`y s sum_i a_i lambda_i
 <= D [g_0 y sum_i lambda_i + s sum_i g_i lambda_i]`.

Using `sum_i lambda_i=s`, this becomes

**(2.6)**

`s [y sum_i a_i lambda_i]
 <= D s [g_0 y + sum_i g_i lambda_i]`.

Since `s>0`, cancel `s` to obtain

**(2.7)**

`y sum_i a_i lambda_i
 <= D [g_0 y + sum_i g_i lambda_i]`.

Thus the additive floor alone pays for the entire negative star contribution:

**(2.8)**

`D g_lambda - y sum_i a_i lambda_i >= 0`.

Finally every leaf/leaf pair term is nonnegative by (1.2), so adding them preserves nonnegativity and gives `F_D(lambda)>=0`.

QED.

### Important feature of the proof

No interior optimizer is solved. The only continuum statement consumed is the already-understood two-vertex edge inequality. The multi-leaf mixture is handled by a positive weighted average of those edge inequalities.

The cancellation in (2.6)--(2.7) is exact: the same total leaf mass `s` appears in every edge test because all bad edges share the same hub. That common factor is precisely what fails for a general negative graph.

---

## 3. Exact sharp global floor

For one edge `(0,i)`, T-P5-157 gives the conceptual sharp floor

**(3.1)**

`D_i^* = a_i / (sqrt(g_0)+sqrt(g_i))^2`.

The radical is useful only for mathematical interpretation; it need not enter a trusted checker.

Theorem A immediately implies:

### Corollary A1 — star sharp floor

**(3.2)**

`D_star^* = max_{i in I} D_i^*`.

Proof: a globally valid floor must dominate every edge floor by necessity. Conversely any `D` dominating every edge floor makes every edge safe, hence Theorem A makes the full simplex safe.

Therefore:

> a negative star has no multiway interior tax at all; the worst obstruction is always realized on at least one hub/leaf edge.

This is stronger than merely producing a sufficient bound. It exactly solves the entire continuum problem for this sign graph.

---

## 4. Root-free rational checker inherited from T-P5-157

For each leaf define

**(4.1)** `L_i := a_i - D(g_0+g_i)`.

T-P5-157 proves the exact two-variable criterion

**(4.2)**

`E_i(D,t)>=0 for every t in [0,1]`

iff

**(4.3)**

`L_i <= 0`

or

**(4.4)**

`L_i^2 <= 4 D^2 g_0 g_i`.

Combining this with Theorem A gives the trusted finite theorem:

### Theorem B — exact root-free star checker

Under the negative-star assumptions, `F_D>=0` on the whole simplex iff for every leaf `i`,

**(4.5)**

`a_i - D(g_0+g_i) <= 0`

or

**(4.6)**

`[a_i-D(g_0+g_i)]^2 <= 4D^2 g_0g_i`.

The checker needs only:

- exact signs of the pair coefficients;
- exact/rational `a_i,g_0,g_i,D`;
- addition, multiplication, squaring, and ordered comparisons.

It does not need square roots, division, eigensystems, determinant search, KKT support enumeration, or SDP/copositivity optimization.

For `a_i=0`, (4.5) automatically holds because `D(g_0+g_i)>=0`, so zero/nonnegative hub edges cost nothing.

---

## 5. Matrix interpretation

T-P5-154 packages the scalar condition into a copositive matrix `M_D` with

`M_D[i,i]=D g_i`,

`2M_D[i,j]=K_ij + D(g_i+g_j)`.

Under a negative-star sign graph, the potentially dangerous monomials are all incident to one hub. Theorem A says:

### Corollary B1

Global copositivity of this special `M_D` is equivalent to copositivity of every `2 x 2` hub/leaf principal block.

This is not true for a general matrix and should not be registered as a generic copositivity theorem. The star sign pattern is essential.

The source-facing advantage is substantial: if the exact `K_ij` sign table is a star, there is no reason to enter T-P5-158 support enumeration or T-P5-162 affine-support continuation at all.

---

## 6. Why the star hypothesis is substantive: an exact negative-triangle obstruction

Edgewise floors do **not** solve a general negative graph.

Take three vertices with

**(6.1)** `g_1=g_2=g_3=1`,

and

**(6.2)** `K_12=K_13=K_23=-1`.

Then

**(6.3)**

`F_D(lambda)
 = D - (lambda_1 lambda_2 + lambda_1 lambda_3 + lambda_2 lambda_3)`,

because `g_lambda=1` on the simplex.

### Every edge is safe at `D=1/4`

On any edge, say `lambda_3=0`,

`F_D = D - t(1-t)`.

Since `t(1-t)<=1/4`, every two-vertex edge is nonnegative for `D>=1/4`, and `1/4` is the exact edge floor.

### But the barycenter requires `D>=1/3`

At

`lambda_1=lambda_2=lambda_3=1/3`,

we have

`lambda_1lambda_2+lambda_1lambda_3+lambda_2lambda_3=1/3`.

Therefore

**(6.4)** `F_D(1/3,1/3,1/3)=D-1/3`.

At the max-edge floor `D=1/4`, this equals `-1/12<0`.

Hence the global sharp floor is at least `1/3`, strictly larger than the edge floor `1/4`.

In fact symmetry shows `1/3` is the sharp global value for this example.

### Consequence

The sign-graph dispatch must fail closed once several bad edges can cooperate without a common hub reduction. A negative triangle is the smallest exact witness that a genuine multiway interior tax can exist.

This also explains why the proof of Theorem A cannot simply be copied to arbitrary forests or cycles without a new structural argument: the single shared hub is what creates the common leaf-mass factor that can be canceled in (2.6).

---

## 7. Source/CSE dispatch rule

Given one same-key homothetic packet `{g_i,K_ij}`:

### Route S0 — no negative edges

If all `K_ij>=0`, use T-P5-153 with zero additive floor.

### Route S1 — exactly one negative edge

Use T-P5-157.

### Route S-star — several negative edges, one common hub

If there exists a hub `h` such that every negative pair is `{h,i}` and all non-hub pairs are nonnegative, use T-P5-164:

1. set `a_i=max(0,-K_hi)` algebraically from the exact sign table;
2. run the finite root-free T-P5-157 gate for every bad hub/leaf edge;
3. global PASS iff all edge gates PASS.

No continuum simplex sweep is needed.

### Route generic

If the negative-edge graph is not a star, do not infer failure, but do not use the star theorem. Fall back to T-P5-154/155/158/160/162 or a future graph-specific theorem.

In particular, detecting a negative triangle is a direct reason to reject any `max(edge floors)` shortcut.

---

## 8. A useful exact finite certificate form

Theorem A can be consumed without ever computing the conceptual radicals (3.1).

A source packet may contain:

- `hub : Fin n`;
- exact positive `g_i`;
- exact pair coefficients `K_ij`;
- exact rational proposed floor `D>=0`;
- for each leaf with `K_hi<0`, the rational `a_i=-K_hi`;
- the Boolean branch proving either (4.5) or (4.6).

Then the theorem layer only needs to establish:

1. all negative pair coefficients are incident to `hub`;
2. all leaf/leaf pair coefficients are nonnegative;
3. every finite edge gate is true.

The conclusion is full-simplex nonnegativity.

This certificate is finite even if the physical uncertainty parameter ranges over a continuum simplex.

---

## 9. Suggested Lean theorem decomposition

The smallest useful leaves are deliberately scalar/finite-sum statements.

### T164-A — weighted star bound

Suggested shape:

```lean
theorem starEdge_weighted_bound
    {I : Type*} [Fintype I]
    (y s D g0 : ℝ)
    (lam a g : I → ℝ)
    (hy : 0 ≤ y) (hs : 0 < s) (hys : y + s = 1)
    (hlam : ∀ i, 0 ≤ lam i)
    (hsum : ∑ i, lam i = s)
    (hedge : ∀ i, a i * y * s ≤ D * (g0 * y + g i * s)) :
    y * (∑ i, a i * lam i)
      ≤ D * (g0 * y + ∑ i, g i * lam i) := by
  ...
```

The proof is: multiply `hedge i` by `lam i`, sum, rewrite with `hsum`, and cancel the positive factor `s`.

### T164-B — global star nonnegativity

```lean
theorem negativeStar_global_of_edge_nonneg ...
```

Use T164-A, then add the nonnegative leaf/leaf pair sum.

### T164-C — necessity by face restriction

```lean
theorem negativeStar_edge_nonneg_of_global ...
```

Set all but the hub and selected leaf coordinates to zero.

### T164-D — exact iff

```lean
theorem negativeStar_floor_iff_edgeFloors ...
```

Combine T164-B/C.

### T164-E — root-free consumer

Reuse the T-P5-157 two-variable theorem to replace each universal edge condition by

`L_i <= 0 ∨ L_i^2 <= 4*D^2*g0*g_i`.

### T164-F — triangle obstruction regression

A concrete `norm_num` theorem at `D=1/4` should prove every edge is nonnegative while the barycenter evaluates to `-1/12`.

The trusted path needs no matrix inverse, square root, eigenvalue, determinant, or optimizer.

---

## 10. Assumptions and exact boundaries

This child proves only the mathematical implication under a frozen same-key homothetic packet.

Still required upstream/downstream:

- actual same-key source identity for the `g_i` and `K_ij`;
- proof that the homothetic reduction from T-P5-153 applies to the physical uncertainty cell;
- exact sign classification of every pair coefficient used to assert a star;
- domain/coverage and boundary-attainability semantics when sharpness, not merely sufficiency, is claimed;
- controller/FD/Float64 semantics if any deployed producer generates these values numerically;
- P8 if required by the parent route;
- Lean implementation and kernel check;
- independent verification by 封不觉;
- admission/registry decision by the proper lane.

A non-star sign graph is **not** a mathematical failure. It only means this fast path does not apply.

---

## 11. Result

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending.**

New exact theorem:

> For the homothetic simplex floor problem, if all negative pair coefficients form a star around one hub and every leaf/leaf coefficient is nonnegative, then full-simplex nonnegativity is equivalent to the finite family of hub/leaf two-vertex edge inequalities. Consequently the sharp global additive floor is the maximum of the individual edge sharp floors, and the trusted checker is exactly the finite collection of T-P5-157 root-free gates.

New obstruction:

> Edgewise floors are not sufficient once bad edges can cooperate in a negative triangle: with `g_i=1` and all three pair coefficients `-1`, every edge closes at `D=1/4` but the barycenter requires `D>=1/3`.

Recommended next mathematical seam:

- classify the next negative-edge graph family where a finite graph decomposition remains exact (for example, determine whether a tree admits a recursive leaf elimination with a modified effective hub weight), **or**
- leave non-star graphs to the existing generic copositivity/support machinery and prioritize actual-source sign-table extraction so the dispatcher can exploit S0/S1/S-star immediately.
