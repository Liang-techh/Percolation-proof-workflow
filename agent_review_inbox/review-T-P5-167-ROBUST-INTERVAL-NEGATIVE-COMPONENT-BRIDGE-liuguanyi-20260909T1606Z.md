---
kind: review_result
review_id: review-T-P5-167-robust-interval-negative-component-bridge-liuguanyi-20260909T1606Z
task_id: T-P5-167-ROBUST-INTERVAL-NEGATIVE-COMPONENT-BRIDGE
reviewer: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-09T16:06:00Z
claim_commit: ea0a996d9e0b4f818a14ebb735f97c3e2ae9c5ad
inspected_commit: e4c35b76a0d71e8394ad50a1b49d717206f7b2e9
upstream_reviews:
  - path: agent_review_inbox/review-T-P5-165-NEGATIVE-GRAPH-COMPONENT-FACTORIZATION-kuangmanmozun-20260909T1540Z.md
    commit: f1c26726dcc54201ced3886d51fe0d5f40102ad4
  - path: agent_review_inbox/review-T-P5-159-MONOTONE-SYMBOLIC-FLOOR-BRACKETING-liuguanyi-20260909T1405Z.md
    commit: 1710eb0b113e44bbe7a4d60367e0bcc8f941ccf9
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: preserve_correlated_source_family; build_may_be_negative_graph_from_certified_lower_bounds; factor_robust_copositivity_by_uniform_safe_components; reuse_left_endpoint_partition_across_D_brackets
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: none; exact finite-sum/order algebra and exact rational regression only
exit_code: n/a
---

# T-P5-167 — robust interval negative-component bridge

## 0. Narrow seam and non-overlap

T-P5-165 proves an exact fixed-matrix statement: for a symmetric matrix `M`, copositivity factors over connected components of the graph of strictly negative off-diagonal entries. It explicitly leaves interval/source reification outside the theorem: if an off-diagonal interval straddles zero, one must not split the corresponding vertices from a nominal midpoint sign.

The actual source-facing seam is therefore not another copositivity algorithm. It is the mathematical contract that turns **certified uniform lower bounds** or outward interval endpoints into a safe component partition for an entire correlated matrix family.

This review proves that bridge. It also proves a stronger parameter-interface statement: once cross-component entries are uniformly nonnegative, **correlation across different components may be discarded exactly by taking each component's true parameter marginal image**. Correlation may not, however, be discarded *inside* a component by replacing a correlated family with the Cartesian product of entry intervals; an exact rational counterexample is given below.

This does not overlap T-P5-166, which is already claimed by 红莲魔尊 and studies forest/shared-diagonal PSD certificates inside one negative component. No forest elimination, shared-diagonal budget, provenance/receipt/admission, Lean compile, runtime validation, or registry mutation is performed here.

---

## 1. Robust family setup

Let `Theta` be an arbitrary parameter set and let

`M : Theta -> Sym_N(R)`

be a family of real symmetric matrices. For `x>=0` componentwise, write

`q_theta(x) := x^T M(theta) x`.

Assume the source layer provides certified lower bounds `ell_ij` for every off-diagonal pair:

**(1.1)** `M_ij(theta) >= ell_ij` for every `theta in Theta` and every `i != j`.

No independence of the matrix entries is assumed. The same `theta` may couple every entry.

Define the **may-be-negative graph**

`Gamma_ell = (V,E_ell)`,

with

**(1.2)** `{i,j} in E_ell  <=>  ell_ij < 0`.

Let its connected components be `C_1,...,C_s`.

Because different components have no edge between them,

**(1.3)** `ell_ij >= 0` whenever `i in C_a`, `j in C_b`, `a != b`.

Combining (1.1) and (1.3), every actual source realization satisfies

**(1.4)** `M_ij(theta) >= 0`

for every cross-component pair, uniformly in `theta`.

This one implication is the entire source-to-math bridge.

---

## 2. Main theorem: exact robust factorization from certified lower bounds

### Theorem A — robust may-be-negative component factorization

Under (1.1), the following are equivalent:

**Global robust copositivity**

**(2.1)** for every `theta in Theta` and every `x>=0`,

`x^T M(theta) x >= 0`.

**Componentwise robust copositivity**

**(2.2)** for every component `C_a`, every `theta in Theta`, and every `y>=0` supported on `C_a`,

`y^T M(theta)[C_a] y >= 0`.

### Proof — necessity

Fix `a`, `theta`, and `y>=0` on `C_a`. Extend `y` by zero outside `C_a`. Then the full quadratic form equals the principal-block quadratic form. Hence (2.1) implies (2.2).

### Proof — sufficiency

Fix `theta` and arbitrary `x>=0`. Split by the fixed components of `Gamma_ell`:

**(2.3)**

`x^T M(theta) x
 = sum_a x_Ca^T M(theta)[C_a] x_Ca
   + 2 sum_{a<b} sum_{i in C_a, j in C_b} M_ij(theta) x_i x_j`.

The first sum is nonnegative by (2.2). The second sum is nonnegative by (1.4) and `x_i x_j>=0`. Therefore the full form is nonnegative.

QED.

### Consequence A1 — conservative lower bounds cannot create a false PASS

The lower bounds `ell_ij` need not be sharp. If a certified lower bound is unnecessarily negative, two vertices may be merged into a larger component and the checker does more work. But Theorem A remains exact for that coarser partition.

The dangerous direction is the opposite one: an **uncertified lower bound that is too high** can split two vertices while an actual source realization still has a negative cross entry. Then the proof of (1.4) fails and a false PASS becomes possible.

Hence the typed source contract is not “nominal sign” or “interval midpoint sign”; it is the order statement

`certified_lower_ij <= actual_entry_ij(theta)`

uniformly over the same parameter/domain key.

---

## 3. Parameter marginal theorem: cross-component correlation may be forgotten exactly

The previous theorem still writes every component block with the global parameter `theta`. In actual source code, different blocks often depend on different subsets or projections of the source parameters.

Assume that for each component `C_a` there is a map

`pi_a : Theta -> Theta_a`

and a local family `N_a : Theta_a -> Sym(C_a)` such that

**(3.1)** `M(theta)[C_a] = N_a(pi_a(theta))`.

Define the **true marginal image**

**(3.2)** `Theta_a^im := pi_a(Theta)`.

### Theorem B — exact marginal decoupling across uniformly safe components

Under the cross-component nonnegativity contract (1.4), global robust copositivity is equivalent to

**(3.3)** for every component `a`, every `eta in Theta_a^im`, and every `y>=0`,

`y^T N_a(eta) y >= 0`.

### Proof

By Theorem A, global robustness is equivalent to

`forall a, forall theta in Theta, Copositive(N_a(pi_a(theta)))`.

For fixed `a`, quantifying over all `theta` is exactly the same as quantifying over the image `pi_a(Theta)`. The finite conjunction over components commutes with the universal quantifier. QED.

### Source meaning

Once two components are separated by a uniform nonnegative cross-entry proof, **joint correlation between parameters used only in different components is mathematically irrelevant to robust copositivity**. Each component may be sent to its own exact parameter marginal image without paying a coupling tax.

This is stronger than merely saying “check blocks separately”: it identifies exactly where parameter dependence may be projected away without loss.

The theorem does *not* permit replacing a component's true marginal family by an arbitrary Cartesian product of entry intervals. That enlargement can introduce matrices that the source can never realize.

---

## 4. Exact counterexample: Cartesian interval hull can manufacture a false FAIL

Let the source parameter set consist of two realizations, `Theta={A,B}`.

Define

**(4.1)**

`M(A) =
 [[1, -9/10, 0],
  [-9/10, 1, 1],
  [0, 1, 1]]`,

and

**(4.2)**

`M(B) =
 [[1, 1, 0],
  [1, 1, -9/10],
  [0, -9/10, 1]]`.

Both source realizations are copositive.

For `M(A)`,

`x^T M(A)x
 = [x1^2 + x2^2 - (9/5)x1 x2]
   + x3^2 + 2 x2 x3`.

The `2 x 2` block `[[1,-9/10],[-9/10,1]]` is positive definite because its determinant is `19/100>0`, and the remaining terms are nonnegative on `x>=0`. Hence `M(A)` is copositive. The same argument with indices reversed proves `M(B)` copositive.

However, the entrywise Cartesian interval hull contains the impossible simultaneous realization

**(4.3)**

`H =
 [[1, -9/10, 0],
  [-9/10, 1, -9/10],
  [0, -9/10, 1]]`.

For the exact rational nonnegative witness

`x=(1, 7/5, 1)`,

we obtain

**(4.4)**

`x^T H x
 = 1 + 49/25 + 1
   - 2(9/10)(7/5)
   - 2(9/10)(7/5)
 = 99/25 - 126/25
 = -27/25 < 0`.

Thus the correlated source family is robustly copositive while its independent entrywise interval hull is not.

### Interface rule fixed by the counterexample

- Using interval **lower endpoints only to decide which vertices must remain in the same component** is safe.
- Replacing the source family *inside that component* by all independent choices from those intervals is a separate relaxation and may cause a false FAIL.
- Such a false FAIL is not a mathematical obstruction to the original source family unless the offending interval-hull witness can be reified by one common source parameter/state.

This distinction matters directly for source adapters that mix directed rounding with parameter-dependent DH data.

---

## 5. Specialization to the T-P5-154 floor family

For the additive-floor matrix, T-P5-154/T-P5-165 use

**(5.1)** `M_D(theta)[i,i] = D g_i(theta)`,

**(5.2)** `2 M_D(theta)[i,j]
 = K_ij(theta) + D(g_i(theta)+g_j(theta))`.

Assume source-valid rational lower bounds

**(5.3)** `K_ij(theta) >= k_ij^-`,

**(5.4)** `g_i(theta) >= gamma_i > 0`.

For every `D>=0`, define

**(5.5)**

`L_ij(D) := k_ij^- + D(gamma_i+gamma_j)`.

Then

**(5.6)** `2 M_D(theta)[i,j] >= L_ij(D)`

for every source realization. Therefore the robust may-be-negative graph at floor `D` may be built by the root-free exact test

**(5.7)** `{i,j} is an edge  <=>  L_ij(D) < 0`.

Theorem A then gives an exact robust component factorization for the full correlated family.

No interval midpoint, inverse, square root, eigenvalue, determinant, or source-parameter independence is needed merely to construct the partition.

### Diagonal check

Because `D>=0` and `gamma_i>0`,

`M_D(theta)[i,i] = D g_i(theta) >= D gamma_i >=0`.

Thus singleton components are automatically robustly copositive, exactly as in the exact-data T-P5-165 lane.

---

## 6. Bracket-level theorem: one left-endpoint graph is valid for the entire upward D interval

T-P5-159 uses rational PASS/FAIL bracketing in the scalar floor `D`. T-P5-165 proves candidate-wise negative graphs can only split as `D` increases. With the robust lower packet above, this becomes a useful whole-bracket interface.

Fix `0 <= D_L <= D_U`. Build one graph from the **left endpoint**:

**(6.1)** edge `{i,j}` iff

`k_ij^- + D_L(gamma_i+gamma_j) < 0`.

### Theorem C — left-endpoint component cache

For every `D in [D_L,D_U]`, every actual source negative off-diagonal pair of `M_D(theta)` lies inside one component of the graph (6.1). Equivalently, if two vertices are in distinct left-endpoint components, then

**(6.2)** `M_D(theta)[i,j] >= 0`

for every `theta` and every `D in [D_L,D_U]`.

### Proof

A cross-component pair has

`k_ij^- + D_L(gamma_i+gamma_j) >= 0`.

Because `D>=D_L` and `gamma_i+gamma_j>0`,

`k_ij^- + D(gamma_i+gamma_j)
 >= k_ij^- + D_L(gamma_i+gamma_j)
 >= 0`.

Apply (5.6). QED.

### Consequence C1

During T-P5-159 bisection or signed-witness continuation, the checker may partition once at the current lower endpoint and solve all subsequent candidate floors independently inside those fixed blocks until the lower endpoint itself is raised enough to split them further. Components never need to merge when the lower bracket moves upward.

This is a safe cache theorem for the entire uncertain source family, not merely for a nominal exact matrix.

---

## 7. Outward interval endpoint form

Suppose a directed-rounding producer gives, for each candidate `D`, an outward interval

`2M_D(theta)[i,j] in [lo_ij(D), hi_ij(D)]`

valid for every source realization on the same parameter/domain key.

Then the minimal checker rule is:

- if `lo_ij(D) >= 0`, the pair may be separated;
- if `lo_ij(D) < 0`, the pair must be connected in the may-be-negative graph, even when the midpoint or upper endpoint is positive.

If the producer gives an exact rational lower formula `L_ij(D)` as in (5.5), it is preferable to retain that symbolic lower packet rather than repeatedly classifying rounded midpoints.

A zero lower endpoint is safe for separation because the cross term is then nonnegative, not strictly positive. The graph must therefore use the strict predicate `lower < 0`, matching T-P5-165's exact graph.

---

## 8. Minimal theorem statements for formalization

### Lemma L1 — robust partition closure

For a finite index set partitioned by `block : i -> a`, assume for all `theta`:

1. `M(theta)` symmetric;
2. `block i != block j -> 0 <= M(theta)[i,j]`;
3. every principal block is copositive.

Then `M(theta)` is copositive for every `theta`.

This is finite-sum algebra only.

### Lemma L2 — lower-bound graph soundness

Assume `ell_ij <= M(theta)[i,j]` for all `theta`. If two vertices lie in distinct connected components of the graph `ell_ij<0`, then `0 <= M(theta)[i,j]` for all `theta`.

### Lemma L3 — parameter-image reduction

If `M(theta)[C]=N(pi(theta))`, then

`(forall theta, Copositive(M(theta)[C]))`

iff

`(forall eta in Set.range pi, Copositive(N(eta)))`.

### Lemma L4 — floor-family robust lower edge

From `k^- <= K(theta)`, `gamma_i <= g_i(theta)`, `gamma_j <= g_j(theta)`, and `0<=D`, infer

`k^- + D(gamma_i+gamma_j)
 <= K(theta) + D(g_i(theta)+g_j(theta))`.

All four statements avoid graph algorithms in the theorem core; graph connectivity can remain an external finite combinatorial adapter initially.

---

## 9. Suggested typed source packet

For an actual robust T-P5 floor consumer, bind all fields to one `uncertaintyKey/cellKey/resetKey`:

```text
RobustNegativeComponentPacket:
  candidate_floor_D or bracket_left_D_L
  parameter_family_key
  index_set
  kLower[i,j]          -- certified lower bound for K_ij(theta)
  gLower[i] > 0        -- certified lower bound for g_i(theta)
  lower_bound_scope    -- same source family/domain as the floor theorem
  component_map        -- connected components of lower<0 graph
  local_parameter_map[a] optional
  local_parameter_image_certificate[a] optional
```

Trusted checks need only:

1. the lower-bound inequalities;
2. `gLower[i]>0` and `D>=0`;
3. exact signs of `kLower[i,j] + D(gLower[i]+gLower[j])`;
4. that every cross-component lower expression is nonnegative;
5. component-local copositivity certificates from T-P5-161/158/160/162/164/166 or later lanes.

The component-local checker must preserve the actual correlated parameter semantics unless it explicitly records an additional conservative hull relaxation.

---

## 10. What remains open

This child does **not** prove any actual source lower bounds. The following remain open and must not be silently promoted:

- actual `K_ij(theta)` and `g_i(theta)` reification from the deployed source;
- same-cell / same-uncertainty-key coverage for those bounds;
- outward-rounding correctness if endpoints come from Float64/interval code;
- exact description of each local marginal image `pi_a(Theta)`;
- component-local copositivity when a component is not discharged by an existing mathematical lane;
- the forest/shared-diagonal problem already claimed as T-P5-166;
- P8/M4 flowpipe/domain transport;
- Lean/kernel validation;
- 封不觉 independent validation;
- admission and registry mutation.

`source_binding_proven=false`, `coverage_proven=false`, and `formal_certificate_allowed=false` remain unchanged.

---

## 11. Main mathematical takeaway

The interval seam is cleaner than it first appears:

> Certified lower endpoints are sufficient to determine a **safe global partition**, while the actual correlated source family should remain intact **inside** each component.

This gives an exact robust analogue of T-P5-165 and identifies a precise dependency boundary. Correlations across uniformly nonnegative-separated components can be marginalized away exactly; correlations among entries inside one dangerous component cannot be discarded without an additional relaxation theorem. The exact rational `-27/25` hull counterexample shows why this distinction must be represented in the adapter type rather than left to implementation convention.