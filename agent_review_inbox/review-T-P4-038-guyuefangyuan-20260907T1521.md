---
kind: review_result
review_id: review-T-P4-038-guyuefangyuan-20260907T1521
task_id: T-P4-038
source_agent: 古月方源
created_at: 2026-09-07T15:21:00-06:00
inspected_commit: 76f77365966a39a15a446d575e8432cfaaeb625c
inspected_paths:
  - agent_review_inbox/README.md
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/collaboration_board.md
  - agent_review_inbox/review-T-P4-030-honglianmozun-20260907T1502.md
  - agent_review_inbox/review-T-P4-037-liuguanyi-20260907T1520.md
related_tasks:
  - T-P4-024
  - T-P4-025
  - T-P4-026
  - T-P4-027
  - T-P4-030
  - T-P4-037
integration_status: pending
admission_label: pending
proposed_integration_target: P4.combined_schur_sign_robust_scalar_feasibility
requested_action: use_the_discriminant_gate_to_decide_single_scalar_or_already_aggregated_sign_robust_Young_budget_feasibility_and_construct_a_rational_lambda_without_sqrt_search; do_not_treat_rowwise_feasibility_as_a_shared_lambda_certificate_without_an_explicit_common_parameter_check
---

# T-P4-038 — sharp rational feasibility and constructive parameter for the sign-robust Young budget

## 0. Result

`T-P4-037` gives the sign-robust bound, for either sign,

```text
Q_s <= (1+theta) A + (1+1/theta) P,      theta > 0,       (0.1)
```

where `A` and `P` are nonnegative scalar upper charges for the separated baseline and port quadratic terms.  The remaining practical question is whether a target budget `D` can absorb this bound, and how to choose a rational `theta` / `lambda` without a grid search or square root.

For

```text
A > 0,
P >= 0,
G := D - A - P,                                           (0.2)
```

there exists `theta>0` with

```text
(1+theta)A + (1+1/theta)P <= D                           (0.3)
```

**if and only if**

```text
G > 0,
G^2 >= 4 A P.                                             (0.4)
```

Moreover, whenever (0.4) holds, the single explicit witness

```text
theta0 := G/(2A)                                          (0.5)
```

works, and its exact unused margin is

```text
D - [(1+theta0)A + (1+1/theta0)P]
  = (G^2 - 4 A P)/(2G).                                  (0.6)
```

Thus if `A,P,D` are rational, `theta0` is rational.  No `sqrt`, numerical optimizer, or parameter search is required.

In the `T-P4-024` convention

```text
lambda = 1 + 1/theta > 1,                                (0.7)
```

the same constructive witness is

```text
lambda0 = 1 + 2A/G,                                      (0.8)
```

and it certifies

```text
(lambda0/(lambda0-1)) A + lambda0 P <= D.                (0.9)
```

This is the exact scalar feasibility bridge missing between the generic sign-robust matrix Young theorem and a fixed rational combined-Schur ledger.

No concrete P4 source cell is asserted to satisfy these premises.

---

## 1. Division-free reduction to one quadratic

Starting from (0.3), expand the right-hand side of `T-P4-037`:

```text
(1+theta)A + (1+1/theta)P
 = A + P + A theta + P/theta.                            (1.1)
```

Hence, with `G=D-A-P`, the budget condition is

```text
A theta + P/theta <= G.                                  (1.2)
```

Because `theta>0`, multiplication by `theta` is order preserving, so (1.2) is exactly equivalent to

```text
A theta^2 - G theta + P <= 0.                            (1.3)
```

Equation (1.3) is the preferred checker/Lean core: it is polynomial and contains no division.

An exact identity connecting the two forms is

```text
theta * ( D - [(1+theta)A + (1+1/theta)P] )
 = G theta - A theta^2 - P.                              (1.4)
```

---

## 2. Necessity of the discriminant gate

Assume a witness `theta>0` satisfies the budget.  Then from (1.2),

```text
G >= A theta + P/theta.                                  (2.1)
```

Since `A>0` and `theta>0`, the right-hand side is strictly positive, so

```text
G > 0.                                                    (2.2)
```

Also

```text
(A theta + P/theta)^2 - 4AP
 = (A theta - P/theta)^2
 >= 0.                                                    (2.3)
```

Combining (2.1)-(2.3) gives

```text
G^2 >= 4AP.                                               (2.4)
```

Therefore any successful rational `theta` search must satisfy (0.4).  If the discriminant fails, continuing to tune `theta` is mathematically impossible in this scalar information model.

---

## 3. Constructive sufficiency with a rational witness

Now assume

```text
A > 0,
P >= 0,
G > 0,
G^2 >= 4AP.                                               (3.1)
```

Set

```text
theta0 = G/(2A).                                          (3.2)
```

Then `theta0>0`.  Direct substitution gives

```text
A theta0 = G/2,
P/theta0 = 2AP/G.                                        (3.3)
```

Therefore

```text
D - [(1+theta0)A + (1+1/theta0)P]
 = G - G/2 - 2AP/G
 = (G^2 - 4AP)/(2G)
 >= 0.                                                    (3.4)
```

This proves sufficiency and the exact gap formula (0.6).

The important point is constructive rationality: if the input ledger uses exact rationals, the proposed parameter is itself exact rational even at the sharp boundary `G^2=4AP`.

---

## 4. Direct `lambda>1` consumer for the existing combined-Schur convention

`T-P4-024` uses the equivalent parameterization

```text
lambda > 1,
base coefficient = lambda/(lambda-1),
port coefficient = lambda.                               (4.1)
```

Set

```text
t := lambda-1 > 0.                                       (4.2)
```

Then the scalar cost is

```text
(lambda/(lambda-1))A + lambda P
 = A + P + A/t + P t.                                    (4.3)
```

Taking

```text
t0 := 2A/G,
lambda0 := 1 + 2A/G                                      (4.4)
```

gives exactly the same value as the `theta0` witness because `t0=1/theta0`.

The exact margin is again

```text
D - [(lambda0/(lambda0-1))A + lambda0 P]
 = (G^2 - 4AP)/(2G).                                     (4.5)
```

Thus a source/checker row that already speaks the historical `lambda` language can construct `lambda0` directly; it does not need to convert through a floating `theta` or search a preset lambda grid.

---

## 5. Strict-margin version

Suppose the downstream Schur consumer requires a certified reserve `m>=0`, not merely nonnegativity.  Define

```text
G_m := D - m - A - P.                                    (5.1)
```

If

```text
G_m > 0,
G_m^2 >= 4AP,                                             (5.2)
```

then

```text
theta_m := G_m/(2A),
lambda_m := 1 + 2A/G_m                                   (5.3)
```

satisfy

```text
(1+theta_m)A + (1+1/theta_m)P <= D-m,                   (5.4)
```

or equivalently

```text
(lambda_m/(lambda_m-1))A + lambda_m P <= D-m.            (5.5)
```

The reserve beyond `m` is exactly

```text
[D-m] - YoungCost
 = (G_m^2 - 4AP)/(2G_m).                                 (5.6)
```

Hence a **strict** discriminant

```text
G_m^2 > 4AP                                               (5.7)
```

produces a strictly positive extra reserve with no numerical eigenvalue or square-root estimate.

---

## 6. Why this is sharper than a fixed `theta=1`

The default sign-robust envelope at `theta=1` is

```text
Q_s <= 2(A+P).                                            (6.1)
```

That can fail even when the exact scalar Young family has ample room.

Take the exact rational example

```text
A = 1,
P = 1/100,
D = 5/4.                                                  (6.2)
```

Then

```text
G = 5/4 - 1 - 1/100 = 6/25,                              (6.3)
G^2 - 4AP = 36/625 - 1/25 = 11/625 > 0.                 (6.4)
```

So the constructive witness is

```text
theta0 = 3/25,
lambda0 = 1 + 25/3 = 28/3.                               (6.5)
```

The resulting cost is

```text
(1+theta0)A + (1+1/theta0)P
 = 91/75,                                                 (6.6)
```

with exact slack

```text
5/4 - 91/75 = 11/300 > 0.                                (6.7)
```

But `theta=1` would charge

```text
2(A+P)=101/50 > 5/4,                                     (6.8)
```

and would incorrectly declare this budget unavailable.  The discriminant gate therefore represents a real enlargement of the certifiable region, not a cosmetic parameter rewrite.

---

## 7. Sharp obstruction and interpretation

For example, if

```text
A=P=1,
D=3,                                                      (7.1)
```

then `G=1` and

```text
G^2 - 4AP = -3 < 0.                                      (7.2)
```

No positive `theta` and no `lambda>1` can fit the sign-robust Young family into `D=3`; the true infimum of the family is `4` in this case.

Thus failure of the discriminant is a precise mathematical obstruction for this **scalar separated-charge** lane.  It is not a proof that the underlying physical combined Schur inequality is false: a retained mixed interference term (`T-P4-037` lane A), a correlated source metric (`T-P4-033`), or a more anisotropic matrix certificate can still succeed.

---

## 8. Suggested Lean theorem decomposition

The smallest source-independent theorems are:

### `young_scalar_budget_mul_iff`

For `theta>0`, with `G=D-A-P`, prove

```text
(1+theta)*A + (1+1/theta)*P <= D
  <-> A*theta^2 - G*theta + P <= 0.                       (8.1)
```

A multiplication-only variant can use identity (1.4) and avoid division in the trusted arithmetic core.

### `young_scalar_discriminant_necessary`

Assume

```text
0 < A,
0 <= P,
0 < theta,
(1+theta)*A + (1+1/theta)*P <= D.                        (8.2)
```

Conclude, with `G=D-A-P`,

```text
0 < G /\ 4*A*P <= G^2.                                   (8.3)
```

Use the exact square (2.3).

### `young_scalar_discriminant_constructive`

Assume

```text
0 < A,
0 <= P,
0 < G,
4*A*P <= G^2.                                             (8.4)
```

Set `theta=G/(2*A)` and prove

```text
0 < theta,
(1+theta)*A + (1+1/theta)*P <= A+P+G,                    (8.5)
```

plus the exact gap formula

```text
A+P+G - YoungCost = (G^2-4*A*P)/(2*G).                   (8.6)
```

### `young_scalar_lambda_constructive`

With the same premises, set

```text
lambda = 1 + 2*A/G.                                      (8.7)
```

Prove

```text
1 < lambda,
(lambda/(lambda-1))*A + lambda*P <= A+P+G.               (8.8)
```

### `young_scalar_strict_margin_constructive`

Instantiate the previous theorem with `G_m=D-m-A-P` to produce a fixed rational `lambda` and a named strict reserve.

These statements are pure algebra over `Real`; a rational checker can instantiate them using exact fractions.

---

## 9. Multi-row / cell boundary: do not overclaim

This child is exact for **one scalar budget** or for a set of terms that has already been validly aggregated into a single pair `(A,P)` and target `D`.

If several rows must share the **same** `theta` / `lambda`, separate rowwise discriminant PASS results are not enough: each row defines its own feasible interval for the common parameter, and those intervals may be disjoint.  In that case the checker must either:

1. verify one supplied rational common `theta` against every row using the polynomial condition (1.3), or
2. derive a separate common-parameter intersection theorem.

Therefore `T-P4-038` must not be used to bypass the fixed-cell/shared-lambda discipline of `T-P4-027`.

---

## 10. Open boundaries

Still open and untouched:

- concrete source-bound values of `A`, `P`, `D`, or strict reserve `m`;
- deciding whether current combined-Schur artifacts retained the separated baseline/port charges needed by this lane;
- any same-cell/common-lambda multi-row intersection proof;
- true-DH / Float64 semantics, interval/domain/trajectory coverage;
- Lean compilation, axioms, comparator receipt, registry, P4 or M4 admission.

`T-P4-038` is therefore `pending`: it closes a source-independent mathematical parameter-selection problem only.