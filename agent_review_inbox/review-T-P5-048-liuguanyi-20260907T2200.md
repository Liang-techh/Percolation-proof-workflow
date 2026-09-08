---
kind: review_result
review_id: review-T-P5-048-liuguanyi-20260907T2200
task_id: T-P5-048
agent: 柳冠一
source_agent: 柳冠一
claimed_at: 2026-09-07T21:59:00-06:00
created_at: 2026-09-07T22:00:00-06:00
claim_commit: 78da39b6f90c8cc4a446dce13e1ee4fb15264d9b
inspected_commit: e62e97c469132f5f9164593e44b4fd2a3f2ba886
inspected_paths:
  - agent_review_inbox/README.md
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/collaboration_board.md
  - agent_review_inbox/review-T-P5-046-guyuefangyuan-20260907T2132.md
  - agent_review_inbox/review-T-P5-047-shared-r-kuangmanmozun-20260907T2148.md
continuation_of:
  - review-T-P5-046-guyuefangyuan-20260907T2132
  - review-T-P5-047-kuangmanmozun-20260907T2148
related_tasks:
  - T-P5-045
  - T-P5-046
  - T-P5-047
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_a_finite-family_shared-r_math_bridge_and_keep_varying-cell_curvatures_explicit; use_curvature_homogenization_before_reusing_same-curvature_candidate_logic; do_not_apply_the_T-P5-047_affine-crossover_rule_directly_across_cells_with_different_curvatures
---

# T-P5-048 — finite-family shared-`r` theorem and curvature-homogenization bridge

## 0. Result

`T-P5-046` gives an exact optimizer for one robust correlated gate

```text
f(r) = A + B*r - d*r^2,       0 <= r <= 1,       d > 0,
```

and `T-P5-047` gives an exact five-candidate rule for **two** such gates when they have the **same curvature** `-d`.

The next interface question is the one needed by a real multi-cell certificate: if a single proof-design parameter `r` must be frozen across finitely many `(cell, consumer)` gates, what is the exact finite-family theorem, and what must be done when the source cells produce different curvatures `d_i`?

There are two clean answers.

1. For a finite family with one common curvature, shared strict feasibility is decided by finitely many rational candidate types: the two endpoints, one vertex for each row, and one pairwise crossover for each pair. All candidate PASS tests admit division-free polynomial forms.
2. For varying curvatures, the same-curvature theorem must **not** be applied directly. A safe bridge is to replace each gate by an explicit lower minorant with one common curvature `D >= d_i`. A pivoted square subtraction

```text
g_i(r) := f_i(r) - (D-d_i)*(r-c_i)^2
```

preserves exact rational arithmetic, gives `g_i(r) <= f_i(r)` globally, and converts every gate to curvature `-D`. The only loss is the visible square tax `(D-d_i)(r-c_i)^2`; there is no hidden interface conservatism.

This is a mathematics/interface child only. It does not establish source interval data, Float64 semantics, cell coverage, first-exit semantics, Lean compilation, comparator equivalence, or admission.

---

## 1. Exact finite-family theorem at common curvature

Let `I` be a finite nonempty index set and assume

```text
d > 0,
f_i(r) := A_i + B_i*r - d*r^2.                         (1.1)
```

We want one shared witness

```text
exists r, 0 <= r <= 1 and forall i, f_i(r) > 0.          (1.2)
```

Define the lower envelope

```text
h(r) := min_i f_i(r)
      = -d*r^2 + min_i (A_i+B_i*r).                     (1.3)
```

Because the second term is the lower envelope of finitely many affine functions, every open region on which one row is strictly active has `h` equal to that row's quadratic; a boundary between active regions is a pairwise affine crossover.

Therefore every maximizer of `h` on `[0,1]` is of one of these types:

```text
(1) r = 0,
(2) r = 1,
(3) r = B_i/(2d) for some active row i,
(4) r = -(A_i-A_j)/(B_i-B_j) for some active pair i,j.  (1.4)
```

Consequently, if any shared strict witness exists, then at least one candidate in (1.4) is itself a shared strict witness. Conversely, any candidate that passes every row is obviously sufficient.

The point for the checker is that the candidate tests can be kept division-free.

---

## 2. Endpoint candidates

The two endpoint predicates are simply

```text
L :<=> forall k, A_k > 0,                                (2.1)
R :<=> forall k, A_k+B_k-d > 0.                          (2.2)
```

No extra assumptions are needed beyond the common `d` used in the family.

---

## 3. Vertex candidate of row `i`

Suppose

```text
0 < B_i < 2d.                                            (3.1)
```

Then

```text
r_i := B_i/(2d)
```

lies in `(0,1)`. For any row `k`, exact substitution gives

```text
4d * f_k(r_i)
 = 4d*A_k + 2*B_k*B_i - B_i^2.                          (3.2)
```

Hence the candidate `r_i` is a shared strict witness iff

```text
forall k,
  4d*A_k + 2*B_k*B_i - B_i^2 > 0.                       (3.3)
```

The checker therefore needs no division to decide the vertex branch; division is needed only after PASS if an explicit rational `r_i` is materialized.

Notice that unlike the two-gate `T-P5-047` predicate, there is no need to encode a separate "active-row" inequality here if the checker evaluates **all rows** at the candidate. If another row is lower, (3.3) checks it directly.

---

## 4. Pairwise crossover candidate of rows `i,j`

Put

```text
c_ij := A_i-A_j,
q_ij := B_i-B_j.                                         (4.1)
```

Under common curvature,

```text
f_i(r)-f_j(r) = c_ij + q_ij*r.                           (4.2)
```

A strict interior crossover exists exactly when

```text
c_ij * (c_ij+q_ij) < 0.                                 (4.3)
```

This implies `q_ij != 0` and gives

```text
r_ij := -c_ij/q_ij in (0,1).                             (4.4)
```

For every row `k`, the value at this crossover satisfies the exact scaled identity

```text
q_ij^2 * f_k(r_ij)
 = q_ij^2*A_k - B_k*c_ij*q_ij - d*c_ij^2.               (4.5)
```

Since `q_ij^2>0`, the pairwise candidate is a shared strict witness iff

```text
forall k,
  q_ij^2*A_k - B_k*c_ij*q_ij - d*c_ij^2 > 0.            (4.6)
```

Again the PASS test is division-free.

This is the finite-family extension of the `T-P5-047` crossover numerator. The only new point is that the candidate generated by rows `i,j` must be checked against **every** row `k`, not merely the generating pair.

---

## 5. Finite exact candidate criterion

Combining the previous sections yields the following mathematical statement.

### Theorem `finite_shared_r_same_curvature`

Assume a finite nonempty family `I`, `d>0`, and

```text
f_i(r)=A_i+B_i*r-d*r^2.
```

Then

```text
exists r in [0,1], forall i, f_i(r)>0
```

iff at least one of the following holds:

```text
L.  forall k, A_k>0;

R.  forall k, A_k+B_k-d>0;

V_i for some i:
    0<B_i<2d,
    forall k,
      4d*A_k + 2*B_k*B_i - B_i^2 > 0;

X_ij for some i != j:
    c_ij*(c_ij+q_ij)<0,
    forall k,
      q_ij^2*A_k - B_k*c_ij*q_ij - d*c_ij^2 > 0.
```                                                     (5.1)

The reverse implication uses the explicit rational witnesses. For the forward implication, maximize the continuous finite lower envelope `h=min_i f_i` on `[0,1]`. At an interior maximizer, either one affine row is active on a neighborhood, in which case the maximizer is its quadratic vertex, or the active affine row changes there, in which case at least two rows cross there. Endpoints give `L/R`. This exhausts the possibilities.

A source checker therefore needs at most

```text
2 + |I| + |I|(|I|-1)/2                                  (5.2)
```

candidate locations, all with exact rational PASS predicates. There is no `r` grid and no square root.

For workflow purposes `I` can be the finite set of `(cell, consumer)` pairs, e.g. quarter-barrier and parameter/incremental gates for every source cell, **provided all rows genuinely have the same curvature**.

---

## 6. Why direct cross-cell reuse of T-P5-047 can be wrong

In the P5 construction inherited from `T-P5-046`, the curvature is

```text
d_i = 4*sL_i*alpha,                                     (6.1)
```

so it can vary with the cell through `sL_i`.

If

```text
f_i(r)=A_i+B_i*r-d_i*r^2,
f_j(r)=A_j+B_j*r-d_j*r^2,
```

then

```text
f_i(r)-f_j(r)
 = (A_i-A_j) + (B_i-B_j)r - (d_i-d_j)r^2.               (6.2)
```

The difference is now quadratic, not affine. The lower envelope may switch branches twice on `[0,1]`, so the one-crossover logic of `T-P5-047` is no longer valid.

An exact regression example is

```text
f1(r) = 3/16 - r^2,          d1=1,
f2(r) = r - 2r^2,           d2=2.                       (6.3)
```

Then

```text
f1(r)-f2(r)
 = r^2-r+3/16
 = (r-1/4)(r-3/4).                                      (6.4)
```

There are **two** interior crossings, `1/4` and `3/4`. Thus any adapter that drops the `d_i` type and feeds these rows into an affine-crossover theorem is mathematically unsound.

This is a typed-interface requirement: the curvature must be part of the gate record, not an implicit global constant unless source construction has proved it common.

---

## 7. Safe curvature homogenization by a common lower minorant

Let the true finite family be

```text
f_i(r)=A_i+B_i*r-d_i*r^2,      d_i>0.                    (7.1)
```

Choose one exact rational

```text
D >= d_i  for all i.                                    (7.2)
```

The simplest common-curvature surrogate is

```text
g_i^0(r):=A_i+B_i*r-D*r^2.                              (7.3)
```

Then

```text
f_i(r)-g_i^0(r)=(D-d_i)r^2 >= 0                         (7.4)
```

for every real `r`. Therefore

```text
g_i^0(r)>0  ==>  f_i(r)>0.                              (7.5)
```

The whole surrogate family has common curvature `-D`, so Section 5 applies exactly.

Among surrogates of the restricted form `A_i+B_i r-D r^2`, the choice

```text
D = max_i d_i                                            (7.6)
```

is pointwise strongest: smaller `D` is not a guaranteed lower minorant for a row attaining the maximum curvature, while larger `D` subtracts extra nonnegative quadratic charge from every row.

---

## 8. Pivoted curvature homogenization: the useful bridge

The unshifted surrogate in (7.3) unnecessarily pays the curvature mismatch at every nonzero `r`. A strictly more flexible exact bridge is available.

For arbitrary rational pivots `c_i`, define

```text
delta_i := D-d_i >= 0,

g_i(r)
 := f_i(r) - delta_i*(r-c_i)^2.                          (8.1)
```

Expanding,

```text
g_i(r)
 = [A_i-delta_i*c_i^2]
   + [B_i+2*delta_i*c_i] r
   - D*r^2.                                              (8.2)
```

Thus every `g_i` again has exactly the common curvature `-D`, but now

```text
f_i(r)-g_i(r)=delta_i*(r-c_i)^2 >= 0.                   (8.3)
```

and, crucially,

```text
g_i(c_i)=f_i(c_i).                                      (8.4)
```

So a source/search layer can select rational pivots near the expected shared witness, while the trusted checker sees only exact rational coefficients and the explicit square-minorant identity.

### Theorem `pivoted_curvature_homogenization`

If `D>=d_i`, then for every real `r,c_i`,

```text
A_i+B_i*r-D*r^2
 + 2(D-d_i)c_i*r
 - (D-d_i)c_i^2
 <= A_i+B_i*r-d_i*r^2.                                  (8.5)
```

The difference is exactly `(D-d_i)(r-c_i)^2`.

This theorem needs only ordered-ring arithmetic plus square nonnegativity.

---

## 9. Quantified loss and completeness relative to a known margin

The pivoted bridge makes its conservatism explicit. Suppose a true shared witness `r_star` has margins

```text
f_i(r_star) >= eta_i > 0.                                (9.1)
```

If the pivots satisfy

```text
(D-d_i)*(r_star-c_i)^2 < eta_i                           (9.2)
```

for every row, then

```text
g_i(r_star)
 = f_i(r_star)-(D-d_i)*(r_star-c_i)^2
 > 0                                                     (9.3)
```

for every row. Hence the common-curvature surrogate family is shared-feasible at the **same** witness.

In particular, if an exact rational candidate `r_star` is already known and one sets

```text
c_i=r_star  for all i,                                   (9.4)
```

then the homogenization has zero loss at that witness, regardless of the spread in `d_i`.

This separates two tasks cleanly:

- **search/optimization** may suggest a rational pivot/witness;
- the **trusted math interface** checks the exact square-minorant identity and the finite common-curvature candidate inequalities.

No floating optimizer result has to be trusted.

---

## 10. Recommended typed contract

A finite-family source-facing record should not merely store `(A,B)`. It should store at least

```text
GateRow :=
  cell_key
  consumer_key
  A : Rat
  B : Rat
  d : Rat
  d_pos : 0 < d                                          (10.1)
```

and the shared-parameter bundle should explicitly distinguish

```text
SameCurvatureBundle(D, rows)
```

from

```text
VaryingCurvatureBundle(rows).                            (10.2)
```

Only the former may call the exact candidate theorem directly. The latter must either:

1. use a future genuine varying-curvature optimizer, or
2. supply `D>=d_i` and pivots `c_i` and pass through `pivoted_curvature_homogenization`.

This prevents a serious adapter bug where per-cell `sL_i` is silently forgotten and the affine crossover theorem is applied outside its hypotheses.

---

## 11. Minimal theorem statements for formalization

The smallest useful Lean/API split is:

```text
same_curvature_vertex_eval_mul
  4*d*f_k(B_i/(2*d))
    = 4*d*A_k + 2*B_k*B_i - B_i^2

same_curvature_cross_eval_mul
  q^2*f_k(-c/q)
    = q^2*A_k - B_k*c*q - d*c^2

finite_shared_r_candidate_sound
  -- explicit endpoint/vertex/crossover witness => all rows positive

finite_shared_r_candidate_complete
  -- finite lower-envelope completeness; may be a later Finset/order theorem

curvature_homogenized_minorant
  D>=d -> A+B*r-D*r^2 <= A+B*r-d*r^2

pivoted_curvature_homogenized_minorant
  D>=d ->
  f(r)-(D-d)*(r-c)^2 <= f(r)

pivoted_curvature_homogenization_margin
  f(r)>=eta and (D-d)*(r-c)^2<eta ->
  f(r)-(D-d)*(r-c)^2>0.                                 (11.1)
```

The two evaluation identities are field identities; the minorant/margin lemmas are ordered-ring/ordered-field arithmetic. The finite completeness theorem is the only part that needs finite-set envelope reasoning.

A practical implementation can formalize **soundness + minorant transport first**. That already permits a checker to emit one explicit rational candidate `r` and prove every row positive. Completeness of the finite candidate enumeration is valuable for declaring a failed search an obstruction, but it should not block safe positive certificates.

---

## 12. Boundaries left open

This review does **not** close any of the following:

- whether a single `r` is semantically required across all P5 cells/consumers;
- concrete source values/enclosures for `A_i,B_i,d_i`;
- proof that `sL_i` and hence `d_i` are state-independent inside a source cell;
- signed Jacobian / bias interval construction from deployed source;
- Float64, finite-difference, controller, solver, or timer semantics;
- first-exit, trajectory, or P8 cell coverage;
- Lean compilation / `#print axioms` / comparator receipt;
- registry admission or P5/P8/M4 closure.

If the final certificate is allowed to choose a different `r` per cell or per consumer, this shared-family constraint should not be imposed at all. If one global `r` is required, then curvature is a first-class typed premise and the homogenization bridge above is the safe route from varying-cell source data to the exact shared-`r` checker.
