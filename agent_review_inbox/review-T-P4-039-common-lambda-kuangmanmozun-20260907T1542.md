---
kind: review_result
review_id: review-T-P4-039-common-lambda-kuangmanmozun-20260907T1542
task_id: T-P4-039
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-07T15:42:00-06:00
inspected_commit: e18fb7711d60716110c60a1e7b97580f2617a042
inspected_paths:
  - agent_review_inbox/README.md
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/collaboration_board.md
  - agent_review_inbox/review-T-P4-037-liuguanyi-20260907T1520.md
  - agent_review_inbox/review-T-P4-038-guyuefangyuan-20260907T1521.md
related_tasks:
  - T-P4-024
  - T-P4-027
  - T-P4-037
  - T-P4-038
integration_status: pending
admission_label: pending
proposed_integration_target: P4.combined_schur_common_lambda_intersection
requested_action: use_the_pairwise_square_free_interval_gate_for_same_cell_multirow_common_theta_feasibility; rowwise_discriminants_are_not_a_shared_lambda_certificate; for_an_automatic_rational_witness_use_a_direct_candidate_check_or_the_dominating_envelope_corollary
---

# T-P4-039 — exact common-θ/common-λ intersection for multiple Young rows

## 0. Result

`T-P4-038` closes one scalar Young-budget row but explicitly leaves open the same-cell case in which several rows must share one fixed `theta` / `lambda`.  This child gives the missing mathematical intersection layer.

For finitely many rows `i`, write

```text
A_i > 0,
P_i >= 0,
G_i := D_i - A_i - P_i,
q_i(theta) := A_i theta^2 - G_i theta + P_i.              (0.1)
```

By `T-P4-038`, for `theta>0`, the original sign-robust Young budget is equivalent to

```text
q_i(theta) <= 0.                                          (0.2)
```

Define

```text
delta_i := G_i^2 - 4 A_i P_i.                             (0.3)
```

Individual feasibility requires and, under the stated signs, is equivalent to

```text
G_i > 0,
delta_i >= 0.                                             (0.4)
```

For a pair `(i,j)`, define the three entirely rational polynomial quantities

```text
C_ij := (G_i A_j - G_j A_i)^2,
U_ij := delta_i A_j^2,
V_ij := delta_j A_i^2.                                    (0.5)
```

Then the two row-feasible intervals intersect **if and only if**

```text
C_ij <= U_ij + V_ij
OR
(C_ij - U_ij - V_ij)^2 <= 4 U_ij V_ij.                    (0.6)
```

There are no square roots in (0.6).

Because feasible sets of one-dimensional convex quadratics are intervals, a finite family has one common real `theta>0` **if and only if** every row passes (0.4) and every pair passes (0.6).  Thus same-cell/shared-parameter feasibility reduces to `O(n^2)` exact-rational polynomial comparisons.

This also gives a sharp fail-fast obstruction: one failed pair proves that no common `theta`, hence no common `lambda=1+1/theta`, exists in this scalar separated-charge model.  Continuing a shared-lambda grid search after (0.6) fails is mathematically pointless.

For a common **rational** witness, two source-independent routes are provided below:

1. verify any supplied rational `theta0>0` against all `q_i(theta0)<=0`; or
2. use the new coefficientwise dominating-envelope corollary, which constructs one rational witness in closed form without roots or search.

No concrete P4 source row/cell is claimed to satisfy these conditions.

---

## 1. One-row feasible interval

Complete the square:

```text
4 A_i q_i(theta)
 = (2 A_i theta - G_i)^2 - delta_i.                       (1.1)
```

Assume `A_i>0`, `P_i>=0`, `G_i>0`, `delta_i>=0`.  The roots are

```text
theta_i^- = (G_i - sqrt(delta_i))/(2 A_i),
theta_i^+ = (G_i + sqrt(delta_i))/(2 A_i).                (1.2)
```

Since

```text
G_i^2 - delta_i = 4 A_i P_i >= 0,                         (1.3)
```

we have `G_i >= sqrt(delta_i)`, hence

```text
0 <= theta_i^- <= theta_i^+,
theta_i^+ > 0.                                            (1.4)
```

Therefore

```text
q_i(theta) <= 0
<=> theta in I_i := [theta_i^-, theta_i^+].               (1.5)
```

Although (1.2) is useful for the proof, the checker need not evaluate either square root.

---

## 2. Exact pairwise overlap without square roots

Write the center and radius of `I_i` as

```text
c_i := G_i/(2 A_i),
r_i := sqrt(delta_i)/(2 A_i).                              (2.1)
```

Two closed intervals intersect exactly when

```text
|c_i-c_j| <= r_i+r_j.                                     (2.2)
```

Multiply (2.2) by the positive number `2 A_i A_j`.  It becomes

```text
|G_i A_j - G_j A_i|
 <= A_j sqrt(delta_i) + A_i sqrt(delta_j).                (2.3)
```

With (0.5), this is

```text
sqrt(C_ij) <= sqrt(U_ij) + sqrt(V_ij).                    (2.4)
```

Now use the following elementary square-free lemma.

### Lemma: `sqrt_sum_le_iff_poly`

For `C,U,V>=0`,

```text
sqrt(C) <= sqrt(U)+sqrt(V)                                (2.5)
```

if and only if

```text
C <= U+V
OR
(C-U-V)^2 <= 4UV.                                         (2.6)
```

Proof:

- If `C<=U+V`, then

  ```text
  sqrt(C) <= sqrt(U+V) <= sqrt(U)+sqrt(V).
  ```

- If `C>U+V`, both sides of

  ```text
  C-U-V <= 2 sqrt(UV)                                     (2.7)
  ```

  are nonnegative, so squaring is reversible and yields exactly

  ```text
  (C-U-V)^2 <= 4UV.                                       (2.8)
  ```

Conversely, split on `C<=U+V`; the first branch is immediate and the second branch reverses the same two nonnegative squarings.

Combining (2.4)-(2.8) proves the pairwise criterion (0.6).

### Why the disjunction is necessary

It is not safe to square twice without tracking the sign of `C-U-V`.  When `C<U+V`, overlap is already automatic even if the second polynomial inequality happens not to be the convenient branch.  The checker should preserve the exact disjunction or explicitly branch on `C<=U+V`.

---

## 3. Finite-family exactness: one-dimensional Helly

Let the row set be finite and nonempty, with each `I_i` nonempty.  Define

```text
L := max_i theta_i^-,
U := min_i theta_i^+.                                     (3.1)
```

The full family intersects exactly when `L<=U`.

Suppose every pair intersects.  Choose indices `iL,iU` attaining the finite maximum/minimum in (3.1).  Pairwise intersection of `I_iL` and `I_iU` implies

```text
theta_iL^- <= theta_iU^+.                                 (3.2)
```

But the two sides are exactly `L` and `U`; hence `L<=U`.  Therefore

```text
(all pairs intersect) <=> (intersection_i I_i is nonempty).  (3.3)
```

Since each individually feasible interval has a positive upper endpoint, a nonempty full intersection contains a positive feasible point in the present `A_i>0, P_i>=0, G_i>0` setting.  (If `L=0`, then `U>0`, so choose any `0<theta<=U`.)

Consequently, (0.4)+(0.6) is an **exact** common-real-parameter criterion, not merely sufficient.

This is the missing same-cell common-parameter layer mentioned in `T-P4-038` §9.

---

## 4. Sharp counterexample: every row PASS, shared parameter impossible

Take two exact-rational Young rows.

### Row 1

```text
A_1 = 1,
P_1 = 2,
D_1 = 6,
G_1 = D_1-A_1-P_1 = 3,
delta_1 = 3^2 - 4*1*2 = 1.                               (4.1)
```

Thus

```text
q_1(theta) = theta^2 - 3theta + 2
           = (theta-1)(theta-2),                          (4.2)
I_1 = [1,2].
```

`T-P4-038` individually passes, with its rational center witness `theta=3/2`.

### Row 2

```text
A_2 = 1,
P_2 = 12,
D_2 = 20,
G_2 = 7,
delta_2 = 7^2 - 4*12 = 1.                                (4.3)
```

Hence

```text
q_2(theta) = theta^2 - 7theta + 12
           = (theta-3)(theta-4),                          (4.4)
I_2 = [3,4].
```

Again the individual discriminant PASS is strict enough, and the row has rational center witness `theta=7/2`.

But there is no common parameter because `[1,2]` and `[3,4]` are disjoint.

The square-free pair test catches this exactly:

```text
C_12 = (3*1 - 7*1)^2 = 16,
U_12 = 1,
V_12 = 1.                                                 (4.5)
```

Then

```text
16 > 1+1,
(16-1-1)^2 = 196 > 4.                                    (4.6)
```

Both branches of (0.6) fail.

Therefore **rowwise discriminant PASS is not a shared-lambda certificate**.  This is a concrete obstruction, not a bookkeeping preference.

---

## 5. A second counterexample: row-center witnesses do not compose

Even when a common interval exists, simply trying the individual `T-P4-038` center witnesses can miss it.

Take

```text
Row 1:
A_1=1,
P_1=500,
D_1=606,
G_1=105,
delta_1=9025=95^2,
I_1=[5,100],
center c_1=105/2.                                         (5.1)
```

and

```text
Row 2:
A_2=10,
P_2=6,
D_2=77,
G_2=61,
delta_2=3481=59^2,
I_2=[1/10,6],
center c_2=61/20.                                         (5.2)
```

The common interval is

```text
I_1 intersect I_2 = [5,6].                                (5.3)
```

But neither row center lies in the intersection:

```text
105/2 > 6,
61/20 < 5.                                                (5.4)
```

A shared rational witness such as

```text
theta0 = 11/2                                             (5.5)
```

works, with exact residuals

```text
q_1(11/2) = -189/4 < 0,
q_2(11/2) = -27 < 0.                                      (5.6)
```

So a checker may cheaply scan row centers, but failure of that heuristic is **not** an obstruction.  The exact pairwise intersection gate remains the correct mathematical decision layer.

---

## 6. Common rational witness: direct exact checker interface

Once a candidate rational `theta0` is supplied, the trusted condition is extremely small:

```text
0 < theta0,
forall i,  A_i theta0^2 - G_i theta0 + P_i <= 0.          (6.1)
```

No root computation or interval endpoint materialization is needed.

This should be the final checker interface even if an untrusted search procedure proposes `theta0`.  In particular, a numerical optimizer may suggest a nearby rational, but only the exact polynomial checks in (6.1) are trusted.

A useful finite candidate heuristic is to test all rational row centers

```text
c_k = G_k/(2A_k).                                         (6.2)
```

If one center satisfies every row, it is immediately a common rational certificate.  Section 5 shows that this heuristic is incomplete, so failure should fall through to another search rather than be treated as impossibility.

---

## 7. Closed-form common rational witness via a dominating envelope

There is also a fully constructive, no-search sufficient theorem for many rows.

Assume rational numbers

```text
Abar > 0,
Pbar >= 0,
Glow > 0                                                   (7.1)
```

satisfy, for every row `i`,

```text
A_i <= Abar,
P_i <= Pbar,
Glow <= G_i.                                               (7.2)
```

For every `theta>=0`,

```text
q_i(theta)
 = A_i theta^2 - G_i theta + P_i
 <= Abar theta^2 - Glow theta + Pbar
 =: qbar(theta).                                          (7.3)
```

If the single aggregate discriminant gate

```text
Glow^2 >= 4 Abar Pbar                                     (7.4)
```

holds, choose the exact rational

```text
theta_bar := Glow/(2 Abar) > 0.                           (7.5)
```

Then

```text
qbar(theta_bar)
 = Pbar - Glow^2/(4 Abar)
 <= 0,                                                    (7.6)
```

so by (7.3)

```text
forall i, q_i(theta_bar) <= 0.                            (7.7)
```

Thus (7.2)-(7.4) produce a **single rational common theta in closed form**.

A natural exact choice is

```text
Abar = max_i A_i,
Pbar = max_i P_i,
Glow = min_i G_i,                                         (7.8)
```

when these rational extrema are available.  This route can be conservative because the three extrema may come from different rows, but it is exceptionally cheap and completely source-independent.  If it fails, one should fall back to the exact pairwise feasibility gate plus a candidate search; failure of (7.4) alone is not an impossibility proof.

---

## 8. Strict common interval and robust rational synthesis

For a finite family, it is useful to distinguish mere touching from an interval with positive width.

Assume every

```text
delta_i > 0.                                              (8.1)
```

Then each `I_i` has positive radius.  For a pair, positive-length overlap is equivalent to

```text
sqrt(C_ij) < sqrt(U_ij)+sqrt(V_ij).                       (8.2)
```

The exact square-free strict form is

```text
C_ij < U_ij+V_ij
OR
(C_ij-U_ij-V_ij)^2 < 4 U_ij V_ij.                         (8.3)
```

If (8.3) holds for every pair, the same max-lower/min-upper argument gives

```text
L < U.                                                     (8.4)
```

Hence the common feasible set contains a nonempty open interval.  Because rational numbers are dense, it contains a rational `theta0`; that rational can then be trusted solely through (6.1).

This gives a clean separation of roles:

- (0.6) is the exact **real feasibility / impossibility** decision;
- (8.1)+(8.3) gives robust positive-width feasibility and guarantees rational witnesses are available without living on a sharp boundary;
- (6.1) is the final exact certificate for whichever rational witness an untrusted synthesizer returns.

For a boundary-touching case, do not infer a rational witness merely from floating endpoints.  Require a supplied rational candidate and verify (6.1), or use a stronger constructive corollary such as §7.

---

## 9. Direct historical `lambda` form

`T-P4-024` uses

```text
lambda > 1,
theta = 1/(lambda-1).                                     (9.1)
```

Let

```text
s := lambda-1 > 0.                                        (9.2)
```

The row budget

```text
(lambda/(lambda-1)) A_i + lambda P_i <= D_i               (9.3)
```

is equivalent to

```text
A_i/s + P_i s <= G_i.                                     (9.4)
```

Multiplying by `s>0` gives the division-free polynomial

```text
P_i s^2 - G_i s + A_i <= 0.                               (9.5)
```

Thus a common rational `theta` immediately yields

```text
lambda = 1 + 1/theta,                                     (9.6)
```

and conversely a common rational `lambda>1` can be checked without division by evaluating (9.5) at the common `s=lambda-1`.

The `theta` formulation is preferable for the generic intersection theorem because its leading coefficient `A_i` is strictly positive even when `P_i=0`; the direct `s` formulation can become linear when `P_i=0`.

---

## 10. Strict reserve / margin version

If row `i` must retain a named reserve `m_i>=0`, simply replace

```text
G_i = D_i - A_i - P_i                                    (10.1)
```

by

```text
G_i^(m) := D_i - m_i - A_i - P_i.                        (10.2)
```

All formulas above are unchanged after this substitution:

```text
delta_i^(m) = (G_i^(m))^2 - 4 A_i P_i,                   (10.3)
```

followed by the same pairwise `C/U/V` construction.

Therefore a cell requiring one fixed `lambda` across several rows **and** row-specific certified reserves can still use the exact square-free common-parameter gate with no conceptual change.

---

## 11. Suggested Lean/checker theorem decomposition

The smallest source-independent leaves are:

### `young_row_complete_square`

Prove by `ring`:

```text
4*A*(A*t^2-G*t+P)
 = (2*A*t-G)^2 - (G^2-4*A*P).                             (11.1)
```

### `sqrt_sum_le_iff_poly`

For `0<=C,U,V`, prove

```text
sqrt C <= sqrt U + sqrt V
<-> C <= U+V \/ (C-U-V)^2 <= 4*U*V.                       (11.2)
```

If avoiding `sqrt` entirely in the final trusted theorem is desirable, use (11.2) only once to prove an interval-overlap lemma, then expose the polynomial right-hand side as the checker API.

### `young_two_rows_common_theta_iff`

Under

```text
0<A_i, 0<=P_i, 0<G_i, 0<=delta_i,
0<A_j, 0<=P_j, 0<G_j, 0<=delta_j,                          (11.3)
```

define `C,U,V` by (0.5) and prove

```text
(exists t>0, q_i(t)<=0 /\ q_j(t)<=0)
<-> C<=U+V \/ (C-U-V)^2<=4UV.                             (11.4)
```

### `young_finite_common_theta_of_pairwise`

For a finite nonempty index set, prove that if every row interval is nonempty and every pair overlaps, then one common `t>0` satisfies all row quadratics.  This is the one-dimensional max-lower/min-upper argument of §3.

### `young_common_theta_dominating_envelope`

Assume (7.1)-(7.4), set `t=Glow/(2*Abar)`, and conclude

```text
0<t /\ forall i, q_i(t)<=0.                              (11.5)
```

The algebraic core can avoid division by first proving

```text
4*Abar*qbar(Glow/(2*Abar))
 = 4*Abar*Pbar - Glow^2 <= 0.                             (11.6)
```

### `young_common_lambda_of_theta`

Map a certified `theta>0` to `lambda=1+1/theta`, or use the direct polynomial (9.5).

A practical implementation can stop before formalizing the full exact-iff finite-family statement: a checker can use pairwise polynomial rejection plus a supplied rational witness verified by (6.1).  The exact theorem here justifies that this fail-fast rejection is complete for common-real feasibility.

---

## 12. Failure branches and interpretation

The result gives four distinct outcomes that should not be conflated.

1. **An individual discriminant fails.**  That row is impossible in the scalar Young lane, regardless of sharing.
2. **All rows individually pass but one pair fails (0.6).**  No common same-cell `theta/lambda` exists.  This is a genuine shared-parameter obstruction.
3. **All pairwise gates pass but the cheap dominating envelope §7 fails.**  Common real feasibility still holds; use a rational candidate search and exact check (6.1).  The envelope failure is only conservatism.
4. **A candidate rational parameter fails one row.**  Reject that candidate only; unless the exact pairwise gate fails, do not infer impossibility.

If the scalar shared-parameter lane is impossible, the appropriate escape routes remain the same as in `T-P4-037/038`: retain the mixed interference, use the correlated metric from `T-P4-033`, permit a certified finer cell partition with different fixed parameters, or move to a genuinely anisotropic matrix certificate.  Do not hide a failed shared-lambda intersection by assigning row-specific lambdas when the downstream certificate requires one common cell parameter.

---

## 13. Open boundaries

Untouched and still pending:

- concrete P4 values of `(A_i,P_i,D_i)` and how many rows really must share one parameter;
- source equality / true-DH / Float64 semantics;
- interval/domain/trajectory coverage and whether a finer cell partition is permitted;
- Lean compilation and kernel admission;
- comparator/receipt/provenance/registry;
- P4/M4 final closure.

`T-P4-039` is a source-independent mathematical child only.  It closes the common-parameter intersection algebra left open by `T-P4-038`; it does not assert that the current concrete cell ledger passes it.
