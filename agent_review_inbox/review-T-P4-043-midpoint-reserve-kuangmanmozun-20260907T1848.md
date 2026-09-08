---
kind: review_result
review_id: review-T-P4-043-midpoint-reserve-kuangmanmozun-20260907T1848
task_id: T-P4-043
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-07T18:48:00-06:00
inspected_commit: a7127c482f9931b206e2c8e91fe97c0e1fb534e1
inspected_paths:
  - agent_review_inbox/README.md
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/collaboration_board.md
  - agent_review_inbox/review-T-P4-039-common-lambda-kuangmanmozun-20260907T1542.md
  - agent_review_inbox/review-T-P4-040-divfree-liuguanyi-20260907T1816.md
  - agent_review_inbox/review-T-P4-041-strict-boundary-lean-juyangxianzun-20260907T1752.md
  - agent_review_inbox/review-T-P4-042-liuchuanafeng-20260907T1813.md
related_tasks:
  - T-P4-039
  - T-P4-040
  - T-P4-041
  - T-P4-042
integration_status: pending
admission_label: pending
proposed_integration_target: P4.common_lambda_rational_interval_midpoint_reserve
requested_action: if a checker can exhibit one positive-width rational interval whose two endpoints pass every row, use its rational midpoint as the shared theta and charge the exact curvature reserve below; boundary-only width zero must remain non-admissible for any positive-reserve consumer
---

# T-P4-043 — sharp quantitative reserve from a common rational inner interval

## 0. Result

Revision 742 assigns `T-P4-043` to the strict-intersection / boundary-only mathematics lane.  The pairwise weak/strict/boundary classification is already recorded in the earlier strict-boundary child, and the new Lean result kernel-checks the pairwise touching examples.  The remaining useful closure is quantitative:

> once the checker supplies **one common rational interval of positive width** whose two endpoints are feasible for every Young row, the midpoint is automatically a common rational **strict** witness, with an explicit sharp reserve determined only by interval width and curvature.

This avoids square roots, algebraic root materialization, and a trusted finite-family root/Helly implementation.  It also states exactly when midpoint synthesis has no reserve: zero common width, zero uniform curvature, or a downstream reserve charge larger than the sharp width budget.

For one row write

```text
q(t) = A t^2 - G t + P,
A > 0.                                                     (0.1)
```

Let `a < b` be two common rational test points and set

```text
h := b-a > 0,
theta0 := (a+b)/2.                                        (0.2)
```

The central identity is

```text
4 q(theta0)
  = 2 q(a) + 2 q(b) - A (b-a)^2.                         (0.3)
```

Therefore

```text
q(a) <= 0,
q(b) <= 0
------------------------------------------------
q(theta0) <= - A (b-a)^2 / 4 < 0.                        (0.4)
```

The coefficient `1/4` is sharp.

For a finite family with a common curvature lower bound `A_i >= A_min > 0`, the **same** midpoint obeys

```text
forall i,
q_i(theta0) <= - A_min (b-a)^2 / 4.                      (0.5)
```

Thus a positive-width rational inner interval immediately gives a rational common theta and a uniform positive reserve.

---

## 1. Exact midpoint curvature identity

For

```text
q(t)=A t^2-G t+P,
theta0=(a+b)/2,
```

direct expansion gives

```text
4 q(theta0)
 = A(a+b)^2 - 2G(a+b) + 4P.                              (1.1)
```

On the other hand,

```text
2q(a)+2q(b)-A(b-a)^2
 = 2A(a^2+b^2)-2G(a+b)+4P
   -A(a^2-2ab+b^2)
 = A(a+b)^2-2G(a+b)+4P.                                  (1.2)
```

Hence (0.3).

A division-free ordered-ring core can avoid even writing the midpoint:

```text
A*(a+b)^2 - 2*G*(a+b) + 4*P
  = 2*q(a) + 2*q(b) - A*(b-a)^2.                         (1.3)
```

Only the final `Rat`/`Real` adapter defines `theta0=(a+b)/2`.  This matches the division-free philosophy of `T-P4-040` while adding a genuinely new quantitative reserve.

Suggested theorem names:

```text
quadratic_midpoint_scaled_identity
quadratic_midpoint_strict_of_endpoints
```

The identity is `ring`; the inequality is `nlinarith` once `A>0`, `a<b`, and endpoint feasibility are supplied.

---

## 2. Family theorem: rational interval -> rational common strict witness

Let `I` be a finite nonempty row family.  For every `i in I`, define

```text
q_i(t)=A_i t^2-G_i t+P_i.                                (2.1)
```

Assume exact rational data

```text
A_min > 0,
a < b,
forall i, A_min <= A_i,
forall i, q_i(a) <= 0,
forall i, q_i(b) <= 0.                                    (2.2)
```

Then with

```text
theta0=(a+b)/2                                             (2.3)
```

we have for every row

```text
4 q_i(theta0)
 <= -A_i (b-a)^2
 <= -A_min (b-a)^2 < 0.                                  (2.4)
```

Therefore

```text
forall i, q_i(theta0) < 0.                                (2.5)
```

and the common polynomial reserve

```text
sigma := A_min (b-a)^2 / 4                                (2.6)
```

satisfies

```text
sigma > 0,
forall i, q_i(theta0) <= -sigma.                          (2.7)
```

This is stronger than merely knowing that an open common interval exists: it emits a **specific rational witness** and a **specific rational reserve** from endpoint checks only.

### Why this is useful for the trusted checker

A root-based proof of strict overlap may involve irrational endpoints.  The trusted path does not need to store those roots.  An untrusted synthesizer can propose rational `a<b`; the trusted checker only verifies

```text
a < b,
A_min > 0,
A_min <= A_i,
q_i(a) <= 0,
q_i(b) <= 0
```

for every row.  The midpoint theorem then certifies the shared rational theta and strict reserve.

Thus the source-independent decision layers can be separated cleanly:

```text
pairwise strict gate     -> proves a positive-width real intersection exists;
rational interval search -> proposes a,b;
endpoint checker          -> verifies the supplied a,b exactly;
midpoint reserve theorem  -> produces theta0 and sigma;
T-P4-038/040 consumer     -> consumes the one shared theta0.
```

No square root needs to enter the final certificate.

---

## 3. Exact Young-budget reserve after midpoint synthesis

`T-P4-040` expresses a named downstream reserve `m` through

```text
q(theta) + theta*m <= 0.                                  (3.1)
```

Assume additionally

```text
0 <= a,
a < b,
m >= 0.                                                   (3.2)
```

Then `theta0=(a+b)/2>0`.  From (2.4),

```text
4 ( q_i(theta0) + theta0*m )
 <= -A_min(b-a)^2 + 2(a+b)m.                              (3.3)
```

Consequently the completely rational, division-free charge condition

```text
2(a+b)m <= A_min(b-a)^2                                  (3.4)
```

implies for every row

```text
q_i(theta0) + theta0*m <= 0.                              (3.5)
```

If the inequality in (3.4) is strict, every row retains strict post-charge reserve.

More precisely, define the leftover numerator

```text
R := A_min(b-a)^2 - 2(a+b)m.                              (3.6)
```

Then

```text
R >= 0
------------------------------------------------
forall i,
4 * ( -(q_i(theta0)+theta0*m) ) >= R.                    (3.7)
```

So the midpoint interval itself can be used as a reusable **reserve ledger**.  A downstream consumer need not guess a safety factor: it may charge any rational `m` satisfying (3.4), and `R/4` is an exact lower bound on what remains.

Suggested theorem names:

```text
common_midpoint_uniform_reserve
common_midpoint_young_reserve_charge
common_midpoint_young_reserve_leftover
```

---

## 4. Sharpness: the factor `1/4` cannot be improved

Take the extremal row whose two certified endpoints are exactly its roots:

```text
q_*(t) := A (t-a)(t-b),
A>0,
a<b.                                                      (4.1)
```

Then

```text
q_*(a)=q_*(b)=0                                           (4.2)
```

and at the midpoint

```text
q_*(theta0)
 = A((b-a)/2)(-(b-a)/2)
 = -A(b-a)^2/4.                                           (4.3)
```

Thus any theorem using only

```text
A_i >= A_min,
q_i(a)<=0,
q_i(b)<=0
```

cannot replace `1/4` by a larger universal constant.  Equality is attained with `A=A_min`.

The Young-budget threshold (3.4) is sharp for the same reason.  On the extremal row, equality

```text
2(a+b)m = A(b-a)^2                                       (4.4)
```

makes

```text
q_*(theta0)+theta0*m = 0.                                 (4.5)
```

Any larger `m` fails.

### Concrete rational sharpness witness

Choose

```text
A=1,
a=1,
b=3,
q(t)=(t-1)(t-3)=t^2-4t+3.                                (4.6)
```

Then

```text
theta0=2,
q(1)=q(3)=0,
q(2)=-1.                                                  (4.7)
```

The sharp named Young reserve is

```text
m_max = 1/2                                               (4.8)
```

because

```text
q(2)+2*(1/2)=0,                                           (4.9)
```

whereas every `m>1/2` makes the charged inequality positive.  This is an exact rational negative control for any checker that tries to enlarge the reserve coefficient.

---

## 5. Boundary-only and midpoint failure conditions

The midpoint construction is safe only when it is the midpoint of a **single common positive-width interval**.  Three failure modes must stay explicit.

### 5.1 Width zero: boundary-only common feasibility

If `a=b`, (0.3) loses the curvature term.  There is no guaranteed positive reserve.

For example

```text
q(t)=(t-a)^2                                               (5.1)
```

has

```text
q(a)=0                                                     (5.2)
```

but no strict reserve at the only certified point.  This is the interval-level form of the T-P4-041 touching obstruction.

Therefore

```text
common weak point only
```

must never be upgraded to

```text
positive reserve
```

without a separate strict-width witness.

### 5.2 No positive uniform curvature

Positive width alone is insufficient if the family theorem does not carry a positive curvature floor.  The exact counterexample is

```text
q(t) = 0                                                   (5.3)
```

on any `a<b`: both endpoints pass, but the midpoint has zero reserve.

For the actual finite Young family `A_i>0`, one may take

```text
A_min = min_i A_i > 0.                                    (5.4)
```

The theorem should carry this fact explicitly rather than silently relying on finiteness.

### 5.3 Midpoints of rowwise or pairwise intervals do not compose

The theorem requires the **same** `a,b` to pass every row.  It does not justify taking individual row centers, pairwise intersection midpoints, or averaging row witnesses and assuming the result is globally feasible.

The existing exact counterexample with row intervals `[5,100]` and `[1/10,6]` already shows that neither row center lies in the true common interval `[5,6]`.  Likewise, pairwise midpoints in a multi-row family are not a substitute for one globally checked `a,b`.

The trusted final object should therefore bind

```text
cell_id,
common_a,
common_b,
common_theta=(common_a+common_b)/2,
A_min,
endpoint checks for every row.
```

---

## 6. Relation to the current strict-boundary Lean child

The fresh T-P4-041 Lean sidecar successfully kernel-checks the pairwise weak/strict/boundary predicates and the exact touching/perturbation examples, while explicitly leaving the finite-family open-interval Helly layer open.

This `T-P4-043` theorem offers an alternate certificate surface that does **not** need a trusted root-level finite Helly construction once a rational inner interval is supplied:

```text
forall rows, q_i(a)<=0 and q_i(b)<=0
```

plus `a<b` and `A_min>0` is already enough to certify a common strict rational midpoint and quantitative reserve.

The two surfaces are complementary:

- strict pairwise polynomial gate: exact real feasibility / impossibility decision;
- rational interval midpoint gate: constructive rational witness + sharp reserve.

A checker may use the first to decide whether search is worth attempting and the second as the final proof object.

---

## 7. Minimal formalization targets

The smallest useful Lean layer is five source-independent lemmas:

```text
quadratic_midpoint_scaled_identity
quadratic_midpoint_strict_of_endpoints
common_midpoint_uniform_reserve
common_midpoint_young_reserve_leftover
midpoint_reserve_sharp_example
```

Recommended split:

1. prove the scaled identity over a commutative ring with `ring`;
2. prove the one-row inequality over a linear ordered field;
3. lift pointwise over any row type once `A_min<=A_i` and common endpoint checks are supplied;
4. add the named Young reserve via the division-free condition `2(a+b)m <= A_min(b-a)^2`;
5. freeze the rational extremizer `(A,a,b)=(1,1,3)` as a sharpness/negative-control theorem.

No matrix API, square root, eigenvalue, source object, Float64 semantics, P8 coverage, or registry mutation is needed.

---

## 8. Admission boundary

This result is a **pending mathematical child** only.  It does not prove that any concrete Route-B P4 cell currently has a positive-width common rational interval, that actual rows are source-bound, that the realized `theta/lambda` stays inside the certified interval after rounding, or that true-DH/P8 coverage holds.

It also does not overwrite the earlier strict-boundary artifact history.  The current `task_queue.md` names the revision-742 狂蛮魔尊 lane as `T-P4-043`; this review is the correctly routed quantitative continuation and preserves the earlier files immutably.

**Status: pending. 待封不觉独立验证 / 待梁智炜收割与最终整合。**