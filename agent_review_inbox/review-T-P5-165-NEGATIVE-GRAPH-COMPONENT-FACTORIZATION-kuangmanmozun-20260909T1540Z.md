---
kind: review_result
review_id: review-T-P5-165-negative-graph-component-factorization-kuangmanmozun-20260909T1540Z
task_id: T-P5-165-NEGATIVE-GRAPH-COMPONENT-FACTORIZATION
reviewer: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-09T15:40:00Z
claim_commit: 1c3b1f261ba7fbb2006ab6c772946eaabf1333d5
inspected_commit: 35e17070f2d8d198c0b6f0c192311b8fe9335456
upstream_reviews:
  - path: agent_review_inbox/review-T-P5-154-UNIFORM-ADDITIVE-SIMPLEX-FLOOR-kuangmanmozun-20260909T1233Z.md
    commit: c9b94c1f931c76c20a0f22e428425a4d659b57bb
  - path: agent_review_inbox/review-T-P5-158-FINITE-SUPPORT-KKT-COPOSITIVITY-DECISION-honglianmozun-20260909T1357Z.md
    commit: fce11e2368dfd33d225a49adfbeb4a880a7c01ae
  - path: agent_review_inbox/review-T-P5-159-MONOTONE-SYMBOLIC-FLOOR-BRACKETING-liuguanyi-20260909T1405Z.md
    commit: 1710eb0b113e44bbe7a4d60367e0bcc8f941ccf9
  - path: agent_review_inbox/review-T-P5-161-Z-MATRIX-COPOSITIVITY-EQUALS-PSD-kuangmanmozun-20260909T1437Z.md
    commit: cf3879b10160fb5964218639570875de8f0e9ff2
  - path: agent_review_inbox/review-T-P5-164-NEGATIVE-STAR-EDGE-DECOMPOSITION-guyuefangyuan-20260909T1521Z.md
    commit: 492a93d2678a4b1d56dae8844299d32de37ab897
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: partition_fixed_D_floor_matrix_by_negative_offdiagonal_components_before_generic_copositivity; localize_all_negative_witness_search_to_one_component; exploit_monotone_component_refinement_during_D_bracketing
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: none; exact finite-sum/order algebra only
exit_code: n/a
---

# T-P5-165 — negative-graph component factorization for mixed-sign copositivity

## 0. Narrow seam and non-overlap

T-P5-154 reduced the uniform additive simplex floor to copositivity of an exact symmetric matrix `M_D`. T-P5-158/160/162 then supplied generic finite-support/KKT machinery; T-P5-161 found the all-nonpositive-offdiagonal Z-matrix corridor where copositivity collapses to PSD; T-P5-164 solved a different scalar sign family in which all bad pair coefficients form one negative star.

The remaining mixed-sign problem can still contain many vertices even when the truly dangerous negative couplings occur in separated regions. Generic support enumeration then wastes effort on supports spanning regions that cannot cooperate negatively.

This child proves an exact factorization valid for **every symmetric matrix at a fixed candidate `D`**:

> build the graph whose edges are exactly the strictly negative off-diagonal entries. Copositivity factors exactly over the connected components of that graph.

This does not re-prove the star theorem and does not replace generic copositivity inside a connected mixed-sign component. It removes all cross-component support combinations before those expensive lanes are invoked.

No source admission, provenance/receipt audit, runtime/Float64 claim, registry mutation, Lean/kernel validation, or independent re-audit is performed.

---

## 1. Abstract setup

Let `M=(m_ij)` be a real symmetric `N x N` matrix. For `x>=0` componentwise, write

`q_M(x) := x^T M x`.

Define the **negative-edge graph**

`Gamma_-(M) = ( {1,...,N}, E_- )`,

with

`{i,j} in E_-  <=>  i != j and m_ij < 0`.

Let its connected components be

`C_1,...,C_s`.

By definition, if `i in C_a`, `j in C_b`, and `a != b`, then

**(1.1)** `m_ij >= 0`.

For a component `C`, let `M[C]` denote the corresponding principal submatrix and `x_C` the coordinate restriction.

---

## 2. Main theorem: exact negative-component factorization

### Theorem A — copositivity factors over negative-edge components

For a real symmetric matrix `M`, the following are equivalent:

1. `M` is copositive:

   **(2.1)** `q_M(x) >= 0` for every `x>=0`.

2. Every negative-edge connected component block is copositive:

   **(2.2)** `q_{M[C_a]}(y) >= 0` for every `a` and every `y>=0` on `C_a`.

### Proof — necessity

Fix one component `C_a` and a nonnegative vector `y` on it. Extend `y` by zero outside `C_a`. Then

`q_M(y_extended)=q_{M[C_a]}(y)`.

Thus global copositivity implies copositivity of every principal component block.

### Proof — sufficiency

Take arbitrary `x>=0`. Split the quadratic form by components:

**(2.3)**

`q_M(x)
 = sum_a q_{M[C_a]}(x_{C_a})
   + 2 sum_{a<b} sum_{i in C_a, j in C_b} m_ij x_i x_j`.

Every first term is nonnegative by (2.2). Every cross-component coefficient is nonnegative by (1.1), while `x_i x_j>=0`. Therefore the complete cross-component sum is also nonnegative. Hence `q_M(x)>=0`.

QED.

### Structural interpretation

Positive off-diagonal couplings can only add nonnegative charge on the nonnegative cone. They can never make two otherwise separated dangerous regions cooperate to create a new negative direction. The only graph edges relevant to *where a negative witness can live* are the strictly negative entries.

This is stronger than a sufficient block bound: because principal restriction gives necessity, it is an exact iff factorization.

---

## 3. Minimal-support witness localization

### Corollary A1 — every failure has a one-component failure witness

If `M` is not copositive, then at least one component block `M[C_a]` is not copositive. Therefore there exists a nonnegative witness `z` supported entirely in one `C_a` such that

**(3.1)** `z^T M z < 0`.

This follows immediately from Theorem A, but it is useful operationally because FAIL evidence never needs coordinates from two distinct negative components.

### Corollary A2 — support-minimal negative witnesses are connected

Suppose `x>=0`, `q_M(x)<0`, and the support of `x` is inclusion-minimal among negative witnesses. Then `supp(x)` lies inside a single connected component of `Gamma_-(M)`.

Proof: if the support meets at least two negative components, write (2.3) on the support. The cross-component part is nonnegative. Since the total is negative, the sum of within-component quadratic terms is negative, so at least one component restriction already has negative quadratic value. That gives a strictly smaller support negative witness, contradiction.

Hence the generic T-P5-158 support lattice can be reduced from all `2^N-1` nonempty supports to supports contained in one negative component:

**(3.2)** at most `sum_a (2^{|C_a|}-1)` supports.

The reduction can be exponential when the negative graph is sparse or disconnected.

---

## 4. Specialization to the T-P5-154 floor matrix

T-P5-154 defines, for `D>=0` and `g_i>0`,

**(4.1)** `M_D[i,i] = D g_i`,

**(4.2)** `2 M_D[i,j] = K_ij + D(g_i+g_j)` for `i != j`.

Therefore the exact negative-edge test at a rational candidate `D` is simply

**(4.3)** `K_ij + D(g_i+g_j) < 0`.

No square root, eigensystem, determinant, inverse, or nonlinear optimization is needed merely to discover the factorization.

### Theorem B — negative components refine monotonically with `D`

Let `0 <= D_1 <= D_2`. Since `g_i+g_j>0`,

`K_ij + D_1(g_i+g_j)
 <= K_ij + D_2(g_i+g_j)`.

Hence

**(4.4)** `E_-(M_{D_2}) subseteq E_-(M_{D_1})`.

So as the floor `D` increases, negative edges can disappear but can never appear. Consequently every connected component at `D_2` is contained in a connected component at `D_1`: the component partition only **refines/splits**, never merges.

### Corollary B1 — finite rational graph events

For a pair with `K_ij>=0`, the pair is never a negative edge for any `D>=0`.

For `K_ij<0`, the conceptual disappearance threshold is

`theta_ij = -K_ij/(g_i+g_j) > 0`.

With rational source data this threshold is rational, but the trusted checker does not need division: it only evaluates the sign in (4.3). There are at most `N(N-1)/2` pair thresholds, so the negative-component partition is constant between finitely many exact rational events and refines when a threshold is crossed.

This gives T-P5-159 bracketing a reusable structural cache: as the lower/upper candidates move upward, previously separated components never have to be merged again.

---

## 5. Exact mixed-sign regression: copositive but indefinite, yet factorization is trivial

The factorization strictly extends the T-P5-161 PSD fast path.

Take the T-P5-154 data

`D=1`,

`g_1=g_2=g_3=g_4=1`,

`K_12=K_34=-4`,

and

`K_13=K_14=K_23=K_24=2`.

Then

**(5.1)**

`M_D =
 [[ 1,-1, 2, 2],
  [-1, 1, 2, 2],
  [ 2, 2, 1,-1],
  [ 2, 2,-1, 1]]`.

The negative-edge graph has exactly two connected components:

`C_1={1,2}`, `C_2={3,4}`.

Each principal block is

`[[1,-1],[-1,1]]`,

with quadratic form `(u-v)^2>=0`; hence each block is PSD and therefore copositive. Theorem A immediately certifies the full `4 x 4` matrix copositive.

Indeed for every `x>=0`,

**(5.2)**

`x^T M_D x
 = (x_1-x_2)^2 + (x_3-x_4)^2
   + 4(x_1+x_2)(x_3+x_4)
 >= 0`.

But `M_D` is **not PSD**. For the signed vector

`v=(1,1,-1,-1)`,

we get

**(5.3)** `v^T M_D v = -16 < 0`.

Therefore T-P5-161 correctly cannot certify this matrix by PSD, while the new negative-component factorization gives an exact copositivity certificate with two tiny blocks. This is a genuine mixed-sign gain, not a restatement of the Z-matrix corridor.

---

## 6. Fail-closed boundary: every proposed split must certify nonnegative cross terms

The factorization is invalid if a negative cross-block coefficient is silently ignored.

Take

`M=[[1,-2],[-2,1]]`.

If one incorrectly split this into two singleton blocks, both singleton diagonals are nonnegative. Nevertheless for `x=(1,1)>=0`,

**(6.1)** `x^T M x = -2 < 0`.

The error is exactly the unaccounted negative cross coefficient `m_12=-2`.

Therefore a checker may split indices into blocks only after proving

**(6.2)** `m_ij>=0`

for every pair placed in distinct blocks. The connected components of the *strictly negative* graph are the canonical finest such split.

### Interval / Float implication

If source reification gives an interval for an off-diagonal entry that straddles zero, e.g. `m_ij in [l,u]` with `l<0<=u`, the edge must be treated as potentially negative for robust certification. A nominal positive or tiny midpoint is not enough to separate the vertices. The current theorem itself is exact-real; directed-rounding or interval-source proof remains an external obligation.

---

## 7. Checker dispatch after factorization

For each fixed exact candidate `D`:

1. Construct the sign graph using (4.3).
2. Compute its connected components `C_a`.
3. Ignore all support combinations crossing components; Theorem A proves they cannot produce the first negative witness.
4. For each component independently:
   - singleton: safe automatically because `D g_i>=0`;
   - if the entire component block is a Z-matrix, use T-P5-161 and exact rational PSD/LDL;
   - if a previously certified low-dimensional/special sign theorem applies, use it locally;
   - otherwise invoke T-P5-158/160/162 only on that component.
5. PASS iff every component passes. FAIL may return the first local nonnegative negative witness, zero-extended to the full index set.

This is exact. It does not replace generic copositivity inside an unresolved connected component, and failure of a local *sufficient* checker must not be promoted to mathematical FAIL unless a genuine negative witness is produced.

### Complexity consequence

If the largest negative component has size `r << N`, the expensive support/KKT layer becomes an `r`-dimensional problem rather than an `N`-dimensional one. In the most favorable case of `N/2` disconnected bad pairs, generic support enumeration drops from roughly `2^N` possibilities to `O(N)` two-vertex checks.

---

## 8. Lean-friendly theorem statements

The graph language can be avoided in the first formalization. A more primitive partition theorem is enough.

### Lemma L1 — nonnegative-cross partition closure

Let a finite index type be partitioned by a block label `b : i -> k`. Let `M` be symmetric. Assume:

1. for `b(i) != b(j)`, `0 <= M_ij`;
2. for every block label `a` and every nonnegative vector `x` supported on that block, `0 <= x^T M x`.

Then for every nonnegative `x`,

`0 <= x^T M x`.

Proof: expand the finite double sum into same-block and distinct-block terms; every distinct-block term is nonnegative.

### Lemma L2 — component witness localization

Under the same assumptions, if a nonnegative `x` has `x^T M x<0`, then some block restriction `x_a` satisfies

`x_a^T M x_a < 0`.

This is the contrapositive engine used to localize FAIL witnesses.

### Lemma L3 — monotone negative-edge disappearance

For `g_i,g_j>0`, `D_1<=D_2`,

`K_ij + D_2(g_i+g_j) < 0`

implies

`K_ij + D_1(g_i+g_j) < 0`.

This scalar lemma is enough to formalize the partition-refinement invariant separately from graph-library details.

These statements use only finite sums, multiplication, order, and symmetry. No analytic or spectral machinery is required.

---

## 9. What this does and does not close

### Mathematical progress

- exact iff factorization of mixed-sign copositivity by negative-edge connected components;
- exact localization of every negative witness to one component;
- exponential support-search reduction when the negative graph is disconnected;
- monotone component refinement along the T-P5-159 floor parameter `D`;
- exact rational mixed-sign regression showing a case that is copositive but indefinite and therefore invisible to the global PSD fast path;
- explicit fail-closed condition for uncertain/unproved cross signs.

### Still open

- actual same-key source values `{g_i,K_ij,D}` and their exact sign table;
- robust interval/directed-rounding proof of signs if source values come from Float64 bounds;
- copositivity of any remaining large connected mixed-sign component;
- actual simplex semantics / coverage / homothetic identity;
- Lean/kernel compilation and independent verification;
- registry/admission and P5/P8/M4 parent closure.

Therefore the correct status is

**`CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding`**.

---

## 10. Recommended next child

Before any generic high-dimensional support enumeration at a candidate floor, source/CSE should emit the exact pair-sign table for

`K_ij + D(g_i+g_j)`.

Run the negative-component split first. If the largest component is already small, existing 2/3/4-vertex or KKT machinery can close it locally. Only a genuinely large connected negative component deserves the full generic copositivity cost.