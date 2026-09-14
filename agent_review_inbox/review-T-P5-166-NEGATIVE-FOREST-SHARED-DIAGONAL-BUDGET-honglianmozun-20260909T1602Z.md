---
kind: review_result
review_id: review-T-P5-166-negative-forest-shared-diagonal-budget-honglianmozun-20260909T1602Z
task_id: T-P5-166-NEGATIVE-FOREST-SHARED-DIAGONAL-BUDGET
reviewer: 红莲魔尊
agent: 红莲魔尊
source_agent: 红莲魔尊
created_at: 2026-09-09T16:02:00Z
claim_commit: e4c35b76a0d71e8394ad50a1b49d717206f7b2e9
inspected_commit: ddab1c88212da7be7446c003cbf69fa57d361cf7
upstream_reviews:
  - path: agent_review_inbox/review-T-P5-161-Z-MATRIX-COPOSITIVITY-EQUALS-PSD-kuangmanmozun-20260909T1437Z.md
    commit: cf3879b10160fb5964218639570875de8f0e9ff2
  - path: agent_review_inbox/review-T-P5-164-NEGATIVE-STAR-EDGE-DECOMPOSITION-guyuefangyuan-20260909T1521Z.md
    commit: 492a93d2678a4b1d56dae8844299d32de37ab897
  - path: agent_review_inbox/review-T-P5-165-NEGATIVE-GRAPH-COMPONENT-FACTORIZATION-kuangmanmozun-20260909T1540Z.md
    commit: f1c26726dcc54201ced3886d51fe0d5f40102ad4
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: after_negative_component_factorization_detect_forest_components; try_exact_shared_diagonal_budget_certificate_on_the_negative_skeleton_before_generic_support_KKT; treat_certificate_failure_as_fallback_not_mathematical_failure_when_positive_cross_terms_remain
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: none; exact finite-dimensional ordered-field algebra only
exit_code: n/a
---

# T-P5-166 — negative-forest shared diagonal budget

## 0. Verdict and narrow seam

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-165 proves that, at a fixed candidate floor `D`, copositivity factors exactly over connected components of the graph formed by the strictly negative off-diagonal entries of the exact floor matrix `M_D`. Inside one remaining connected component, however, generic support/KKT can still be expensive.

This child treats the next sparse case:

> the strictly negative graph inside a component is a forest.

The key point is that **checking every negative edge independently is not enough**: two edges sharing a vertex can double-spend the same diagonal Lyapunov budget. The correct local object is a shared diagonal allocation across all incident negative edges.

The result has two layers.

1. For an arbitrary mixed-sign matrix whose negative graph is a forest, a shared-diagonal allocation gives a root-free sufficient copositivity certificate after all nonnegative cross terms are retained as free positive energy.
2. For the associated **negative skeleton** obtained by deleting those nonnegative cross terms, the same certificate is exact: it exists iff the forest-supported Z-matrix is PSD (equivalently copositive by T-P5-161). The exactness proof is a leaf Schur elimination and stays rational for rational input.

This is deliberately not advertised as an exact criterion for the original mixed-sign matrix: positive nonedge couplings can rescue a matrix even when the negative skeleton fails. An exact boundary example is included below.

No source admission, provenance/receipt audit, runtime/Float64 claim, Lean/kernel validation, independent re-audit, or registry mutation is performed.

---

## 1. Fixed-matrix setup and the negative skeleton

Let `M=M^T in R^{n x n}`. Define the strictly negative edge set

`E_- := { {i,j} : i!=j and M_ij<0 }`.

Assume the graph `(V,E_-)` is a forest. Define the **negative skeleton** `N` by

`N_ii := M_ii`,

`N_ij := M_ij` if `{i,j} in E_-`,

`N_ij := 0` otherwise.

Then

`P := M-N`

has zero diagonal and entrywise nonnegative off-diagonal entries. Hence for every `x>=0`,

**(1.1)**

`x^T P x = 2 sum_{i<j, M_ij>=0} M_ij x_i x_j >=0`.

Therefore

**(1.2)** `x^T M x >= x^T N x` for every `x>=0`.

So any copositivity certificate for `N` is automatically a copositivity certificate for `M`.

Because `N` has nonpositive off-diagonal entries, it is a symmetric Z-matrix. T-P5-161 identifies copositivity of `N` with ordinary PSD. The new contribution here is a sparse **forest-local exact PSD decomposition** that does not require a global eigensystem or dense LDL witness.

---

## 2. Direct shared-diagonal edge-block certificate

For every vertex `i`, let `Inc(i)` denote the negative edges incident to `i`.

Suppose we can provide nonnegative numbers

`r_i >=0`,

and, for each negative edge `e={i,j}`, endpoint allocations

`d_{i,e}>=0`, `d_{j,e}>=0`,

such that

**(2.1)** `M_ii = r_i + sum_{e in Inc(i)} d_{i,e}`,

and for every `e={i,j} in E_-`,

**(2.2)** `d_{i,e} d_{j,e} >= M_ij^2`.

### Theorem A — shared-diagonal forest certificate

Under (2.1)--(2.2), `M` is copositive.

In fact the forest assumption is not needed for this forward implication; the allocation certificate is valid on any graph.

### Proof

For `x>=0`, first use (1.2). Then expand `x^T N x` by distributing each diagonal exactly according to (2.1):

`x^T N x`

`= sum_i r_i x_i^2`

`  + sum_{e={i,j} in E_-}`

`      [ d_{i,e} x_i^2 + 2 M_ij x_i x_j + d_{j,e} x_j^2 ]`.

Every scalar residual term is nonnegative. For one edge, the symmetric block

`[[d_{i,e}, M_ij], [M_ij, d_{j,e}]]`

has nonnegative diagonal and determinant

`d_{i,e}d_{j,e}-M_ij^2 >=0`,

hence is PSD. Therefore each bracket is nonnegative for all real `(x_i,x_j)`, not merely on the nonnegative cone. Summing gives

`x^T N x>=0`,

and then `x^T M x>=0` by (1.2). QED.

### Energy interpretation

Each diagonal `M_ii x_i^2` is a finite Lyapunov reserve. A negative coupling edge is allowed to debit only the portions `d_{i,e}x_i^2` and `d_{j,e}x_j^2` explicitly assigned to it. Two incident edges cannot both spend the full vertex diagonal. This is the shared-budget correction missing from naive edgewise tests.

---

## 3. Root-free doubled certificate for the T-P5-154 floor matrix

For the exact floor matrix of T-P5-154,

`M_D[i,i] = D g_i`,

`2 M_D[i,j] = K_ij + D(g_i+g_j)`.

On a negative edge define the positive signed deficit

**(3.1)** `s_ij := -(K_ij + D(g_i+g_j)) >0`.

Then `M_D[i,j]=-s_ij/2`.

Instead of endpoint budgets `d`, use doubled budgets

`a_{i,e}:=2 d_{i,e}`.

The entire certificate becomes division-free:

**vertex budget**

**(3.2)** `sum_{e in Inc(i)} a_{i,e} <= 2 D g_i`,

**edge gate**

**(3.3)** `a_{i,e} a_{j,e} >= s_ij^2`,

with every `a_{i,e}>=0`.

Any unused amount

`2Dg_i - sum_e a_{i,e}`

is simply twice the residual diagonal reserve.

Thus a fixed rational `D`, rational `g_i,K_ij`, and rational endpoint allocations give a checker using only addition, multiplication, squaring, sign tests, and order comparisons. No square roots, inverses, eigenvalues, or continuum optimization are present in the trusted statement.

---

## 4. Exactness for a forest-supported negative skeleton

The forward certificate above is only sufficient for the original mixed-sign `M`, but for the forest skeleton `N` it is exact.

### Theorem B — forest PSD iff shared-diagonal allocation exists

Assume `N=N^T` has off-diagonal support contained in a forest. Then the following are equivalent:

1. `N>=0` in the ordinary PSD sense.
2. There exist nonnegative residuals and endpoint allocations satisfying (2.1)--(2.2) with `M` replaced by `N`.

Moreover, if all entries of `N` are rational, the allocations can be chosen rational.

### Proof: allocation implies PSD

The proof in Section 2 never used `x>=0` once the nonnegative cross remainder was removed. It writes `N` as a sum of PSD two-vertex blocks plus nonnegative diagonal singleton blocks. Hence `N>=0`.

### Proof: PSD forest implies allocation

Proceed by induction on the number of forest edges.

If there are no edges, PSD is equivalent to `N_ii>=0` for every vertex. Set `r_i=N_ii` and there is nothing else to allocate.

Now choose a leaf `ell` with its unique neighbor `p`, and write

`a := N_{ell,ell}`,

`c := N_{ell,p}`.

For a strict negative edge `c!=0`. PSD of the `2 x 2` principal block implies

`a N_pp >= c^2>0`,

so in particular

**(4.1)** `a>0`.

Form the Schur-reduced forest matrix `N'` on `V\{ell}` by leaving every entry unchanged except

**(4.2)** `N'_{pp} := N_{pp} - c^2/a`.

Because `a>0` and `N>=0`, the standard completed-square identity gives, for every vector `y` on the remaining vertices,

`[t;y]^T N [t;y]`

`= a ( t + (c/a)y_p )^2 + y^T N' y`.

Therefore `N'>=0`.

By induction, `N'` has a shared-diagonal allocation. Extend it back to `N` by assigning the leaf edge `e={ell,p}`

**(4.3)** `d_{ell,e}:=a`,

**(4.4)** `d_{p,e}:=c^2/a`.

Set the leaf residual to zero and keep all allocations/residuals from `N'` on the remaining forest. The parent budget is exact because

`N'_{pp}+c^2/a=N_pp`,

and the leaf-edge determinant gate is saturated:

`d_{ell,e}d_{p,e}=c^2=N_{ell,p}^2`.

This completes the induction.

If `N` is rational, every update uses only rational operations on a strictly positive rational pivot `a`, hence every produced allocation is rational. QED.

### Zero-pivot obstruction

At a leaf carrying a nonzero edge, a zero current diagonal pivot is impossible under PSD: the `2 x 2` principal determinant would be `-c^2<0`. Thus leaf elimination fails closed exactly where it should. A final isolated root is allowed to end with zero residual diagonal.

---

## 5. Equivalent exact leaf-elimination checker

The constructive proof gives an alternative sparse checker.

Choose any leaf-elimination order in each tree component. Maintain current diagonal pivots `p_i`, initially `p_i=N_ii`. For a leaf `ell` joined to `p` by edge value `c`:

1. require `p_ell>0` when `c!=0`;
2. replace

   `p_p <- p_p - c^2/p_ell`;
3. delete `ell`.

At the end require every remaining isolated pivot to be nonnegative.

For rational arithmetic, the update can be compared without introducing a square root. If the current parent pivot before update is `b` and `p_ell=a>0`, then

`b-c^2/a >=0`

iff

**(5.1)** `a b - c^2 >=0`.

Repeated exact Fraction arithmetic is therefore enough. The certificate formulation of Section 3 is still preferable for a tiny trusted theorem because it avoids division completely; leaf elimination is an efficient producer for those endpoint budgets.

### Elimination-order invariance

The existence theorem is order-independent: if `N>=0`, every legitimate positive-pivot leaf elimination preserves PSD and eventually succeeds. Different leaf orders may produce different local allocation tables, but all are valid witnesses of the same global PSD fact.

---

## 6. Exact three-node path obstruction: edgewise checks double-spend the center

Consider the forest Z-matrix

**(6.1)**

`N = [[1,   -3/4, 0],`

`     [-3/4, 1,   -3/4],`

`     [0,   -3/4, 1]]`.

Each individual negative-edge principal block is positive definite:

`det [[1,-3/4],[-3/4,1]] = 1-9/16 = 7/16>0`.

So a naive checker that tests the two bad edges separately would declare both edges safe.

But the full tree is not copositive. Take the nonnegative rational vector

`x=(1,3/2,1)`.

Then

`x^T N x`

`= 1 + 9/4 + 1 - 3*(3/2)`

`= 17/4 - 18/4`

**`= -1/4 <0`.**

The shared-budget obstruction is exact. Each leaf has total diagonal budget `1`. To certify an edge of magnitude `3/4`, if the leaf spends at most `1`, the center must spend at least

`(3/4)^2 / 1 = 9/16`.

Two incident edges therefore demand at least

`9/16+9/16=18/16>1`

of center diagonal reserve. The independent edge tests passed only because each of them illegally reused the center's full unit diagonal.

The leaf-elimination calculation says the same thing:

`1 -> center pivot 1-9/16=7/16`,

and the second edge then requires

`(7/16)*1 - 9/16 = -2/16<0`.

This is precisely the minimal multi-edge energy obstruction the new certificate detects.

---

## 7. Boundary: skeleton failure does NOT imply original mixed-sign failure

The positive cross terms deleted in Section 1 can be essential. Therefore failure of the skeleton certificate is a fallback signal, not a mathematical FAIL for the original `M`.

Consider

**(7.1)**

`M = [[1,-1,-1],`

`     [-1,1, 1],`

`     [-1,1, 1]]`.

Its negative-edge graph is the two-edge star centered at vertex 1. The negative skeleton is

`N = [[1,-1,-1],[-1,1,0],[-1,0,1]]`.

For `x=(1,1,1)`,

`x^T N x = -1`,

so the skeleton is not PSD and no shared-diagonal forest allocation can exist.

Nevertheless the original matrix is exactly

**(7.2)** `M = v v^T` with `v=(1,-1,-1)`,

so

**(7.3)** `x^T M x = (x_1-x_2-x_3)^2 >=0`

for every real `x`. It is PSD, hence certainly copositive.

This example is also generated by the T-P5-154 scalar family with

`D=1`, `g_1=g_2=g_3=1`,

`K_12=K_13=-4`, `K_23=0`.

Each bad hub/leaf edge is exactly at the T-P5-164 sharp threshold, and the positive leaf-leaf cross term created by the common additive floor supplies the missing shared energy. Thus T-P5-164 correctly certifies this star while the skeleton fast path rejects its own lower matrix.

**Required fail-closed interpretation:**

- skeleton certificate PASS => original component PASS;
- skeleton certificate FAIL => only "fast path unavailable";
- mathematical FAIL requires an actual nonnegative negative witness for the original component or another exact theorem.

---

## 8. How this plugs into T-P5-165

At a fixed exact `D`:

1. Use T-P5-165 to split `M_D` into connected components of its strictly negative graph.
2. For each component, detect whether that negative graph is a forest.
3. If yes, build the negative skeleton and run either:
   - the division-free shared-budget certificate (3.2)--(3.3), or
   - exact rational leaf elimination to produce those budgets.
4. If the forest skeleton passes, the entire mixed-sign component is copositive immediately.
5. If it fails, do **not** return FAIL. Try stronger structure that uses the positive cross terms:
   - T-P5-164 if the underlying `K_ij` sign graph is a negative star;
   - T-P5-162 if tangent-PD continuation applies;
   - T-P5-158 support/KKT fallback otherwise.
6. For a component whose negative graph contains cycles, this child does not provide exact forest elimination; continue with the existing cycle/generic lanes.

This yields a sparse energy-first decision layer before combinatorial support enumeration.

---

## 9. Candidate Lean-friendly theorem statements

The first formalization need not contain graph theory.

### L1 — two-by-two allocated edge nonnegativity

For reals `a,b>=0`, if `c^2<=a*b`, then for all `x,y`,

`0 <= a*x^2 + 2*c*x*y + b*y^2`.

(The sign of `c` is irrelevant to this local PSD statement.)

### L2 — finite shared-diagonal decomposition

For a finite index type and a finite edge type with endpoint map, assume vertex diagonal equality to residual plus incident allocations and assume L1 on every edge. Then the sparse quadratic is nonnegative for all vectors.

### L3 — nonnegative-cross lift to copositivity

If `N` is nonnegative as a quadratic form and `M-N` has nonnegative entries on every off-diagonal pair used by nonnegative `x`, then `x>=0 -> 0<=x^T M x`.

### L4 — one-leaf Schur identity

For `a>0`,

`a*t^2 + 2*c*t*y + b*y^2`

`= a*(t+(c/a)y)^2 + (b-c^2/a)*y^2`.

A matrix-valued version changes only one parent diagonal and supplies the induction step for forest exactness.

The root-free consumer can stop at L1--L3 and treat leaf elimination as a witness producer rather than part of the trusted proof surface.

---

## 10. What this closes and what remains open

### New mathematical progress

- a shared-diagonal Lyapunov budget certificate that prevents incident negative edges from double-spending one vertex reserve;
- an exact iff theorem for PSD of a forest-supported negative skeleton via edge-local 2x2 blocks plus diagonal residuals;
- a constructive rational leaf-elimination algorithm producing the exact allocation witness;
- a division-free doubled checker specialized to the T-P5-154 floor matrix;
- an exact positive-vector path counterexample proving independent edge checks are insufficient;
- an exact boundary example proving skeleton failure cannot be promoted to mixed-sign copositivity failure;
- a concrete sparse dispatch layer after T-P5-165 and before generic support/KKT enumeration.

### Still open

- actual same-key source values `{g_i,K_ij,D}` and their exact negative graph;
- source/interval proof that the relevant pair signs are exact if coefficients come from Float64 enclosures;
- components with cyclic negative graph where this forest leaf elimination does not apply;
- mixed-sign forest components whose skeleton fails but positive cross terms may still rescue them;
- actual simplex/homothetic source semantics and coverage;
- Lean/kernel compilation and independent verification;
- registry/admission and P5/P8/M4 closure.

The correct status is therefore

**`CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding`.**

---

## 11. Recommended next source-facing artifact

For every T-P5-165 component at the candidate floor, emit:

- the exact negative-edge list;
- exact diagonal `2Dg_i` budgets;
- exact signed edge deficits `s_ij`;
- whether the negative component is a forest;
- if it is a forest, either endpoint allocations `a_{i,e}` satisfying (3.2)--(3.3) or the exact leaf-elimination failure pivot.

This packet is enough to distinguish three cases without generic optimization: certified forest PASS, fast-path-only failure requiring stronger mixed-sign structure, or nonforest component requiring the existing generic lanes.
