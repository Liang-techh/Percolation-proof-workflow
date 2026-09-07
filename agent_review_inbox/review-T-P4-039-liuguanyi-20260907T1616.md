---
kind: review_result
review_id: review-T-P4-039-liuguanyi-20260907T1616
task_id: T-P4-039
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-07T16:16:00-06:00
inspected_commit: ee85de08d92bdac4492a5722989c954b8d4ac0f9
inspected_paths:
  - agent_review_inbox/README.md
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/collaboration_board.md
  - agent_review_inbox/review-T-P4-037-liuguanyi-20260907T1520.md
  - agent_review_inbox/review-T-P4-038-guyuefangyuan-20260907T1521.md
  - agent_review_inbox/review-T-P4-038-juyangxianzun-20260907T1558.md
related_tasks:
  - T-P4-024
  - T-P4-027
  - T-P4-037
  - T-P4-038
integration_status: pending
admission_label: pending
proposed_integration_target: P4.combined_schur_shared_parameter_rational_intersection
requested_action: formalize the completed-square radius certificate and common rational inner-interval theorem; use it only after same-cell row charges A_i/P_i/D_i are bound; do not infer source coverage or P4 admission
---

# T-P4-039 — common rational `theta` / `lambda` for several sign-robust Young rows

## 0. Result

`T-P4-037` and `T-P4-038` close the separated sign-robust Young algebra for one row:

```text
Young_i(theta) := (1+theta) A_i + (1+1/theta) P_i,
theta > 0,
G_i := D_i - A_i - P_i,

Young_i(theta) <= D_i
  <-> p_i(theta) := A_i theta^2 - G_i theta + P_i <= 0.   (0.1)
```

The remaining `T-P4-027`-style issue is that several rows in one source cell must consume the **same** `theta`, equivalently the same historical

```text
lambda = 1 + 1/theta > 1.                                (0.2)
```

Separate rowwise discriminant PASS results do not solve this intersection problem.

This child gives an exact-rational, square-root-free common-parameter certificate.  For every row let

```text
Delta_i := G_i^2 - 4 A_i P_i.                            (0.3)
```

Choose a rational radius `s_i >= 0` satisfying

```text
s_i^2 <= Delta_i.                                         (0.4)
```

Define the rational inner interval

```text
L_i := (G_i - s_i)/(2 A_i),
U_i := (G_i + s_i)/(2 A_i),                               (0.5)
```

under `A_i>0`, `G_i>0`, `P_i>=0`.

Then **every** `theta in [L_i,U_i]` is feasible for row `i`.  Hence, for finitely many rows, if

```text
L := max_i L_i,
U := min_i U_i,
L <= U,                                                    (0.6)
```

then the single exact-rational witness

```text
theta_common := (L+U)/2 > 0,
lambda_common := 1 + 1/theta_common                       (0.7)
```

simultaneously certifies all rows.

No square root, floating optimizer, or rowwise parameter mismatch appears in the trusted check.  The checker may construct `(s_i,L,U,theta_common)` externally and the Lean core only needs polynomial/rational inequalities.

Moreover, if `L<U`, the constructed witness lies strictly inside every inner interval and therefore produces a strictly positive common reserve row by row.

This certificate family is **complete for strict common feasibility in the existential sense**: if there is a real `theta_* > 0` for which every row has strict budget slack, then there exist rational radii `s_i` and a rational common `theta` satisfying the certificate above.  Thus exact-rational shared-parameter checking loses no strictly feasible cell merely because the true quadratic endpoints contain irrational square roots.

No concrete P4 row/cell values are asserted here.

---

## 1. Completed-square identity behind the bridge

For one row write

```text
p(theta) := A theta^2 - G theta + P,
Delta := G^2 - 4 A P.                                    (1.1)
```

The exact identity is

```text
4 A p(theta)
  = (2 A theta - G)^2 - Delta.                            (1.2)
```

This is the useful multi-row form of the single-row discriminant calculation: instead of solving for the two roots with `sqrt(Delta)`, one can certify that `theta` lies in a rational inner tube around the quadratic center.

If

```text
A > 0,
s >= 0,
s^2 <= Delta,
(2 A theta - G)^2 <= s^2,                                (1.3)
```

then (1.2) gives

```text
4 A p(theta) <= 0,
```

hence

```text
p(theta) <= 0.                                            (1.4)
```

Together with `theta>0` and the exact `T-P4-038` multiplication identity, this is exactly the Young budget.

The strongest checker-facing point is that (1.3) is **division free**.  Even the interval endpoints in (0.5) need not be part of the trusted arithmetic core; they are only a convenient rational construction of a common witness.

---

## 2. Rational inner interval theorem

Assume

```text
A > 0,
G > 0,
P >= 0,
s >= 0,
s^2 <= Delta = G^2 - 4 A P.                             (2.1)
```

Because `P>=0`,

```text
Delta <= G^2.                                             (2.2)
```

Together with `s>=0`, `G>0`, and `s^2<=Delta`, this implies `s<=G`; therefore

```text
0 <= (G-s)/(2A) <= (G+s)/(2A),                            (2.3)
```

and the upper endpoint is strictly positive.

Now let

```text
(G-s)/(2A) <= theta <= (G+s)/(2A).                        (2.4)
```

Multiplying by `2A>0` gives

```text
-s <= 2A theta - G <= s,                                  (2.5)
```

hence

```text
(2A theta-G)^2 <= s^2 <= Delta.                           (2.6)
```

Using (1.2), `p(theta)<=0`.  If `theta>0`, then

```text
(1+theta)A + (1+1/theta)P <= A+P+G = D.                  (2.7)
```

Thus `[L_i,U_i]` really is a certified **inner** feasible interval.  If `s^2=Delta`, it is the full exact quadratic feasible interval, but the theorem never needs to form `sqrt(Delta)`.

---

## 3. Finite common-parameter intersection

Let `I` be a finite nonempty row set.  For each `i in I` assume the premises of section 2 and define exact-rational `L_i,U_i`.

Set

```text
L := max_i L_i,
U := min_i U_i.                                           (3.1)
```

If

```text
L <= U,                                                    (3.2)
```

then every `theta` in `[L,U]` belongs to every row's certified inner interval.  Because every `U_i>0`, also `U>0`; from `0<=L<=U`, the midpoint

```text
theta_c := (L+U)/2                                        (3.3)
```

is positive.  Since all inputs are rational, `theta_c` is rational.

For every row,

```text
Young_i(theta_c) <= D_i.                                  (3.4)
```

The historical fixed-`lambda` consumer can therefore take the **single** rational value

```text
lambda_c := 1 + 1/theta_c > 1.                            (3.5)
```

This is exactly the shared-cell discipline that separate `T-P4-038` row witnesses did not provide.

A checker can avoid `max`/`min` APIs entirely by accepting rational `L,U,theta_c` together with the finite inequalities

```text
L_i <= L <= theta_c <= U <= U_i                           (3.6)
```

for every row.  The mathematical content remains the same.

---

## 4. Exact reserve formula

The completed-square identity also gives the unused row budget without any optimization argument.

`T-P4-038` gives

```text
theta * (D - Young(theta)) = -p(theta).                   (4.1)
```

Combining with (1.2), for `A>0` and `theta>0`,

```text
D - Young(theta)
 = [Delta - (2A theta-G)^2] / (4 A theta).                (4.2)
```

Therefore a strict radius condition

```text
(2A theta-G)^2 < Delta                                    (4.3)
```

produces an explicit positive reserve.

In particular, if the global inner intersection is strict,

```text
L < U,                                                     (4.4)
```

then `theta_c=(L+U)/2` lies strictly between every `L_i` and `U_i`.  Hence

```text
(2 A_i theta_c-G_i)^2 < s_i^2 <= Delta_i,                 (4.5)
```

so every row gets a strictly positive reserve by (4.2).

A prescribed downstream reserve `m_i>=0` is handled without changing the theorem: replace

```text
D_i  by  D_i - m_i,
G_i  by  G_i^m := D_i - m_i - A_i - P_i                  (4.6)
```

before building `Delta_i`, `s_i`, and the common interval.  Then the same common `theta_c` proves `Young_i(theta_c) <= D_i-m_i` for all rows.

---

## 5. Why rowwise `T-P4-038` PASS is not enough

Take two exact-rational rows:

```text
row 1: A1=1, P1=2,  D1=6,   so G1=3,
row 2: A2=1, P2=12, D2=20,  so G2=7.                     (5.1)
```

Their quadratic conditions are

```text
p1(theta)=theta^2-3theta+2 <= 0  <-> theta in [1,2],
p2(theta)=theta^2-7theta+12 <= 0 <-> theta in [3,4].      (5.2)
```

Each row separately has

```text
Delta1=Delta2=1 >= 0                                      (5.3)
```

and therefore individually passes `T-P4-038`.  But the feasible intervals are disjoint, so **no shared positive theta exists**.

This is an exact counterexample to any integration rule of the form

```text
forall row, rowwise_discriminant_PASS
=> shared_lambda_PASS.                                    (5.4)
```

A common-parameter certificate is genuinely additional mathematics.

---

## 6. The radius intersection is stronger than merely trying row centers

A tempting finite strategy is to try only the `T-P4-038` constructive center of each row,

```text
theta_i^0 = G_i/(2A_i).                                   (6.1)
```

That strategy is not complete even for a simple rational overlap.

Take

```text
row 1: A1=1, P1=2,     D1=6,
       feasible interval [1,2], center 3/2;

row 2: A2=1, P2=77/16, D2=165/16,
       G2=9/2,
       feasible interval [7/4,11/4], center 9/4.          (6.2)
```

Both discriminants are exactly `1`.  The first center `3/2` is outside row 2; the second center `9/4` is outside row 1.  Thus trying only row centers finds no shared parameter.

But choose exact rational radii

```text
s1=s2=1.                                                  (6.3)
```

Then the rational inner intervals are the full intervals above, with

```text
L=7/4,
U=2,
theta_c=(L+U)/2=15/8,
lambda_c=1+8/15=23/15.                                   (6.4)
```

At `theta_c=15/8`, both rows have exactly

```text
p1(theta_c)=p2(theta_c)=-7/64,                            (6.5)
```

and, using (4.1), both Young budgets retain the exact reserve

```text
D_i - Young_i(theta_c) = 7/120 > 0.                       (6.6)
```

So the radius-intersection construction certifies a shared rational parameter in a case where every row-center candidate fails.

---

## 7. Completeness for strict common feasibility

The radius certificate is intentionally an **inner** approximation when `s_i^2<Delta_i`, so a fixed coarse choice of `s_i` can miss a feasible overlap.  However, it does not create a fundamental exact-rational obstruction when the common cell has strict slack.

Assume finitely many rational rows and suppose there exists a real

```text
theta_* > 0                                               (7.1)
```

such that

```text
p_i(theta_*) < 0                                          (7.2)
```

for every row.  By (1.2),

```text
|2A_i theta_* - G_i|^2 < Delta_i.                         (7.3)
```

Hence

```text
|2A_i theta_* - G_i| < sqrt(Delta_i).                     (7.4)
```

By density of the rationals, for each finite row choose a rational `s_i` strictly between these two positive bounds.  Then

```text
s_i^2 < Delta_i                                           (7.5)
```

and `theta_*` lies strictly inside the rational interval `[L_i,U_i]`.  Because the row set is finite,

```text
max_i L_i < theta_* < min_i U_i.                          (7.6)
```

Thus `L<U`, and the rational midpoint `(L+U)/2` is a strict common witness.

So, for finite scalar rows, a rational-radius certificate exists whenever the shared Young budget is strictly feasible over `Real`.  Irrational quadratic endpoints therefore do **not** force a floating or algebraic-number parameter into the trusted P4 interface.

Boundary-only feasibility is deliberately not upgraded by this argument; if the intersection has zero width, the checker must provide an exact common witness/certificate for that boundary case rather than invoke strict-density reasoning.

---

## 8. Minimal theorem statements for Lean

The first formalization should remain pure algebra and finite-order reasoning; no source/P8 API is needed.

### `young_completed_square_identity`

```text
4*A*(A*theta^2-G*theta+P)
  = (2*A*theta-G)^2 - (G^2-4*A*P).                        (8.1)
```

### `young_feasible_of_rational_radius`

Assume

```text
0 < A,
0 < theta,
0 <= s,
s^2 <= G^2-4*A*P,
(2*A*theta-G)^2 <= s^2.                                  (8.2)
```

Conclude

```text
A*theta^2-G*theta+P <= 0.                                 (8.3)
```

Then compose with the already compiled `young_scalar_budget_mul_iff` from `T-P4-038`.

### `young_inner_interval_feasible`

Under `A>0,G>0,P>=0,s>=0,s^2<=Delta`, prove every positive `theta` between `(G-s)/(2A)` and `(G+s)/(2A)` satisfies the row budget.

### `young_common_parameter_of_inner_bounds`

For a finite nonempty row index type, consume one **shared** `theta>0` and the per-row inner-bound hypotheses, then conclude every row budget.  A second constructor theorem may define `theta=(L+U)/2` from supplied rational common bounds `L<=U`.

### `young_reserve_completed_square`

Prove the exact reserve identity (4.2), preferably first in multiplied/division-free form:

```text
4*A*theta*(D-Young(theta))
 = Delta-(2*A*theta-G)^2.                                 (8.4)
```

The density/completeness theorem in section 7 is mathematically useful but should be a later optional theorem; it is not needed by the trusted exact checker and should not delay the four algebraic lemmas above.

---

## 9. Typed integration contract

For one fixed source cell, the scalar combined-Schur lane may now emit:

```text
rows = [(A_i,P_i,D_i)]
common_theta : Rat
optional_radius_i : Rat
```

with the trusted finite checks

```text
A_i > 0,
common_theta > 0,
(2A_i common_theta-G_i)^2 <= s_i^2,
s_i^2 <= G_i^2-4A_iP_i                                  (9.1)
```

or, even more minimally after construction, simply the already compiled polynomial row checks

```text
A_i*common_theta^2-G_i*common_theta+P_i <= 0.             (9.2)
```

The new mathematics explains how to construct and justify the **same rational parameter** across rows; it does not authorize different `theta_i` values to be silently folded into one cell.

If different source cells use different common parameters, a higher-level piecewise certificate must keep the cell tag attached.  A fixed-cell theorem cannot erase that dependency unless the downstream theorem explicitly quantifies the parameter per cell.

---

## 10. Open boundaries

Still open and not claimed here:

- concrete same-cell P4 `A_i,P_i,D_i` source bindings;
- whether current combined-Schur artifacts retain the separated baseline/port charges needed by `T-P4-037`;
- matrix/anisotropic lanes that should bypass scalar Young rather than be scalarized prematurely;
- true-DH / Float64 evaluator semantics;
- source-cell identity, interval/trajectory/flowpipe coverage;
- Lean compilation / `#print axioms` / independent verifier receipt for this new child;
- P4/M4 registry or final admission.

`T-P4-039` is therefore a **pending mathematical/interface child** only.  It closes the source-independent common-rational-parameter construction for finitely many scalar Young rows, including an exact strict-reserve formula and a proof that rational certificates are complete whenever the common scalar budget has strict real slack.
