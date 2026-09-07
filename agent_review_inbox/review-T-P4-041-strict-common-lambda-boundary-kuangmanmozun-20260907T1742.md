---
kind: review_result
review_id: review-T-P4-041-strict-common-lambda-boundary-kuangmanmozun-20260907T1742
task_id: T-P4-041-STRICT-COMMON-LAMBDA-BOUNDARY
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-07T17:42:00-06:00
inspected_commit: cc8d17559adb7e11a7f06710c23673409bbd72b6
inspected_paths:
  - agent_review_inbox/README.md
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/collaboration_board.md
  - agent_review_inbox/review-T-P4-039-common-lambda-kuangmanmozun-20260907T1542.md
  - agent_review_inbox/review-T-P4-040-rational-lambda-guard-kuangmanmozun-20260907T1642.md
related_tasks:
  - T-P4-038
  - T-P4-039
  - T-P4-040-RATIONAL-LAMBDA-GUARD
integration_status: pending
admission_label: pending
proposed_integration_target: P4.combined_schur_common_lambda_strict_boundary
requested_action: distinguish_weak_common_lambda_from_strict_positive_reserve; use_square_free_strict_pair_gate; classify_singleton_boundary_cases_fail_closed; do_not_feed_boundary_only_witness_into_rounding_or_source_widening_consumers
---

# T-P4-041 — strict common-θ/common-λ intersection and boundary-only closure

## 0. Coordinator-targeted question

The collaboration board revision-742 harvest explicitly assigns 狂蛮魔尊 the follow-up:

> strict intersection 与 boundary-only 反例/闭包边界

`T-P4-039` already gives the exact weak feasibility gate for a finite family of Young rows, and `T-P4-040` gives a robust rational interval certificate once an interval with width is supplied.  The missing layer is to distinguish:

1. a merely feasible common point, where some row may be exactly saturated, from
2. a genuinely strict common point carrying positive reserve and therefore admitting a nontrivial implementation/source-widening neighborhood.

This review closes that source-independent mathematical layer.

No source, receipt, coverage, Float64, or registry claim is made.

---

## 1. Setup

For each row `i`, use the T-P4-039 quadratic

```text
q_i(t) := A_i t^2 - G_i t + P_i,
A_i > 0,
P_i >= 0,
G_i > 0,
delta_i := G_i^2 - 4 A_i P_i >= 0.
```

The weak row-feasible interval is

```text
I_i = [l_i,u_i]
```

with

```text
l_i = (G_i-sqrt(delta_i))/(2A_i),
u_i = (G_i+sqrt(delta_i))/(2A_i).
```

Then

```text
q_i(t) <= 0  <=>  t in I_i.
```

If `delta_i>0`, strict feasibility is exactly

```text
q_i(t) < 0  <=>  t in (l_i,u_i).                         (1.1)
```

If `delta_i=0`, the row has exactly one weak witness and no strict witness at all.

For a pair `(i,j)`, retain the square-free quantities from T-P4-039:

```text
C_ij := (G_i A_j - G_j A_i)^2,
U_ij := delta_i A_j^2,
V_ij := delta_j A_i^2.                                   (1.2)
```

All are nonnegative rational polynomials in the row data.

---

## 2. Exact strict pair-overlap gate without square roots

The interiors of two nondegenerate feasible intervals overlap iff

```text
sqrt(C_ij) < sqrt(U_ij) + sqrt(V_ij).                    (2.1)
```

For arbitrary `C,U,V>=0`, the strict analogue of the T-P4-039 square-free lemma is

```text
sqrt(C) < sqrt(U)+sqrt(V)
<=>
C < U+V
OR
(C-U-V)^2 < 4UV.                                         (2.2)
```

### Proof

If `C<U+V`, then

```text
sqrt(C) < sqrt(U+V) <= sqrt(U)+sqrt(V).
```

Otherwise `C>=U+V`.  Then both sides of

```text
C-U-V < 2 sqrt(UV)
```

are nonnegative, so strict squaring is reversible and gives

```text
(C-U-V)^2 < 4UV.
```

The converse reverses the same branches.

Therefore define the exact strict pair predicate

```text
StrictPair(i,j) :=
  C_ij < U_ij+V_ij
  OR
  (C_ij-U_ij-V_ij)^2 < 4 U_ij V_ij.                     (2.3)
```

No root evaluation is needed by the trusted checker.

---

## 3. Exact finite-family strict-feasibility theorem

Let the row family be finite and nonempty.  Under the signs in §1,

```text
exists t>0, forall i, q_i(t) < 0                         (3.1)
```

holds **if and only if**

```text
forall i, delta_i > 0,
forall distinct i,j, StrictPair(i,j).                    (3.2)
```

### Proof

With `delta_i>0`, every strict feasible set is the open interval `(l_i,u_i)`.  A finite family of open intervals has nonempty common intersection iff

```text
L := max_i l_i < U := min_i u_i.                         (3.3)
```

If every pair has positive-width overlap, choose `iL` attaining the maximum lower endpoint and `iU` attaining the minimum upper endpoint.  `StrictPair(iL,iU)` gives

```text
l_iL < u_iU,
```

hence `L<U`.  Any `t in (L,U)` satisfies all rows strictly.  Conversely, one common strict `t` lies in every pair of interiors, so every pair passes (2.3), and every row must have `delta_i>0`.

Thus the T-P4-039 weak `<=` pair gate and this strict `<` pair gate are genuinely different mathematical objects.

---

## 4. Exact boundary-touch polynomial condition

The boundary between strict overlap and disjointness is itself square-free.

For `C,U,V>=0`,

```text
sqrt(C) = sqrt(U)+sqrt(V)                                (4.1)
```

is equivalent to

```text
C >= U+V,
(C-U-V)^2 = 4UV.                                         (4.2)
```

Hence define

```text
BoundaryPair(i,j) :=
  C_ij >= U_ij+V_ij
  AND
  (C_ij-U_ij-V_ij)^2 = 4 U_ij V_ij.                     (4.3)
```

When both rows have `delta>0`, `BoundaryPair(i,j)` means the two closed feasible intervals meet in exactly one endpoint and their interiors are disjoint.

This gives a fail-closed classification:

```text
WeakPair PASS + StrictPair FAIL
<=> BoundaryPair.                                        (4.4)
```

The equality case is therefore not numerical noise; it is the exact mathematical closure boundary.

---

## 5. Finite-family weak-only classification

Assume the finite nonempty family has at least one common weak witness:

```text
exists t>0, forall i, q_i(t) <= 0.                       (5.1)
```

Then there is **no** common strict witness iff at least one of the following holds:

```text
(a) exists i, delta_i = 0;

(b) exists distinct i,j, BoundaryPair(i,j).              (5.2)
```

### Proof

Let `[L,U]` be the full weak intersection.

- If some `delta_i=0`, `I_i` is a singleton, so the full intersection is contained in that singleton.  Under (5.1) it is exactly a singleton; strict feasibility is impossible.
- If a boundary-touching pair exists, its intersection is a singleton.  Again the nonempty full intersection is contained in it, so it is exactly that singleton.
- Conversely suppose weak feasibility holds but strict feasibility fails and all `delta_i>0`.  Then `L=U`.  Let `iL` attain `L` and `iU` attain `U`.  Since both intervals have positive width, `iL != iU`; their pair intersects at exactly the common point, hence satisfies `BoundaryPair(iL,iU)`.

So the only weak-but-not-strict finite cases are precisely zero-discriminant rows or a boundary-touching pair.

---

## 6. Positive reserve is equivalent to strict common feasibility

For a finite nonempty row family, common strict feasibility is equivalent to existence of a **single positive common reserve**:

```text
(exists t>0, forall i, q_i(t)<0)
<=>
(exists t>0, exists m>0, forall i, q_i(t) <= -m).        (6.1)
```

The reverse direction is immediate.  For the forward direction, at a strict witness `t` every number `-q_i(t)` is positive.  Finiteness gives

```text
m := min_i (-q_i(t)) > 0,                                (6.2)
```

and then `q_i(t)<=-m` for all `i`.

This is the downstream closure consequence: a boundary-only common lambda can never support any positive shared Schur/Young reserve, however small.  Any consumer requiring a named positive margin must use the strict gate, not the weak gate.

---

## 7. Sharp rational boundary-only counterexample

Take two rows:

```text
Row 1:
A1=1, P1=2, G1=3, D1=A1+P1+G1=6,
q1(t)=t^2-3t+2=(t-1)(t-2),
delta1=1,
I1=[1,2].

Row 2:
A2=1, P2=6, G2=5, D2=A2+P2+G2=12,
q2(t)=t^2-5t+6=(t-2)(t-3),
delta2=1,
I2=[2,3].                                                (7.1)
```

Both rows are individually strictly feasible.  Their common **weak** feasible set is exactly

```text
I1 intersect I2 = {2}.                                   (7.2)
```

At the only common witness,

```text
q1(2)=0,
q2(2)=0.                                                  (7.3)
```

The square-free pair data are

```text
C=(3-5)^2=4,
U=1,
V=1.                                                      (7.4)
```

Thus the weak T-P4-039 gate passes only through equality:

```text
C>U+V,
(C-U-V)^2 = (4-2)^2 = 4 = 4UV.                           (7.5)
```

The strict gate fails because neither strict branch holds.

So this pair is an exact counterexample to each of the following invalid upgrades:

```text
common weak lambda  => common strict lambda,
common weak lambda  => positive shared reserve,
common weak lambda  => nonzero rounding interval,
common weak lambda  => robustness to coefficient widening.                 (7.6)
```

### Direct lambda form

With `s=lambda-1=1/t`, the two division-free lambda polynomials are

```text
r1(s)=2s^2-3s+1=(2s-1)(s-1),
      feasible s in [1/2,1],

r2(s)=6s^2-5s+1=(3s-1)(2s-1),
      feasible s in [1/3,1/2].                            (7.7)
```

Their only common point is

```text
s=1/2,
lambda=3/2,                                               (7.8)
```

and both rows saturate there.  Therefore this is also an explicit **shared-lambda boundary-only** counterexample, not merely a theta-coordinate artifact.

---

## 8. Boundary instability: exact one-parameter perturbation

The touching example is a true closure boundary.  Keep row 1 fixed and perturb row 2 by a rational parameter `e`:

```text
q2_e(t)
 := (t-(2-e))(t-3)
  = t^2 -(5-e)t + (6-3e).                                (8.1)
```

For `-1<e<1`, row 2 remains nondegenerate with

```text
delta2_e = (1+e)^2 > 0.                                  (8.2)
```

Its interval is

```text
I2_e=[2-e,3].                                             (8.3)
```

Therefore:

```text
e>0  => common interval [2-e,2] has positive width;
e=0  => common interval is the singleton {2};
e<0  => the two rows are disjoint.                        (8.4)
```

The square-free pair algebra sees the same phase transition.  Here

```text
C=(2-e)^2,
U=1,
V=(1+e)^2,
4UV-(C-U-V)^2 = 32 e (1-e).                              (8.5)
```

Thus for `0<e<1` the strict branch is positive, at `e=0` it is exactly zero, and for `e<0` it has the wrong sign.

A completely rational three-point witness is:

```text
e= 1/10: strict overlap;
e= 0:    boundary-only weak overlap;
e=-1/10: no common witness.                              (8.6)
```

For `e=1/10`, choose `t=39/20`.  Then

```text
q1(39/20)   = -19/400,
q2_1/10(39/20) = -21/400.                                (8.7)
```

So the common reserve can be at least `19/400`.  As `e -> 0+`, that reserve collapses to zero.  This is why a boundary-only certificate must never be treated as robust against source uncertainty or implementation rounding.

---

## 9. Interaction with T-P4-040 rational interval guard

`T-P4-040` certifies a chosen rational interval `[a,b]` by endpoint checks.  The present result tells the search/integration layer when such a **nontrivial** interval can exist.

- If the strict gate passes, the common feasible set has positive width.  A rational `0<a<b` subinterval can be chosen inside it and then certified by T-P4-040.
- If only the weak gate passes and the boundary classification (5.2) fires, the common feasible set is a singleton.  There is no `a<b` interval to certify.  Any exact singleton witness may still be useful for a non-strict theorem, but it has zero tolerance to generic coefficient/source widening.

Therefore the safe pipeline is:

```text
weak gate        -> existence / impossibility only;
strict gate      -> positive-reserve eligibility;
T-P4-040 interval-> exact rational robustness certificate.                  (9.1)
```

Do not skip the middle gate when the downstream theorem needs strict margin.

---

## 10. Minimal Lean/checker statements

Suggested source-independent child lemmas:

1. `sqrt_sum_lt_iff_poly`

```text
0<=C -> 0<=U -> 0<=V ->
(sqrt C < sqrt U + sqrt V
 <-> C<U+V \/ (C-U-V)^2 < 4*U*V).
```

2. `sqrt_sum_eq_iff_poly`

```text
0<=C -> 0<=U -> 0<=V ->
(sqrt C = sqrt U + sqrt V
 <-> U+V<=C /\ (C-U-V)^2 = 4*U*V).
```

3. `young_two_rows_common_theta_strict_iff`

Use (2.3) plus `delta_i>0, delta_j>0`.

4. `young_finite_common_theta_strict_of_pairwise`

Finite one-dimensional open-interval Helly/max-lower-min-upper argument.

5. `young_weak_only_boundary_classification`

Under weak common feasibility, prove the dichotomy (5.2).

6. `finite_strict_rows_iff_uniform_positive_reserve`

Finite `min'` argument for (6.1).

7. `touching_rows_weak_not_strict`

Normalize the exact rational counterexample in §7; `norm_num` should discharge all polynomial values.

8. `touching_rows_perturbation_transition`

Optional arithmetic theorem for (8.5), mostly `ring`/`nlinarith`.

The final trusted checker can avoid square roots entirely by exposing (2.3), (4.3), exact row discriminants, and a direct rational candidate check.

---

## 11. Status / non-claims

Admission remains `pending`.

This child proves only the source-independent strict/boundary mathematics requested by 梁智炜.  It does **not** prove:

- any concrete P4 cell coefficients;
- DHProducerBaseBridge/source identity;
- Float64 or true-DH realization;
- coverage;
- Lean/kernel compilation;
- comparator/admission/registry state;
- P4/M4 closure.

The principal integration recommendation is fail-closed: **a weak common-lambda equality witness is not eligible for any consumer that requires positive reserve or nonzero rounding/source-widening tolerance.**
