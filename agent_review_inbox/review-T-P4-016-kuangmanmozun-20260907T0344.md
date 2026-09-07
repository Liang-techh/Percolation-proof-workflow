---
kind: review_result
review_id: review-T-P4-016-kuangmanmozun-20260907T0344
task_id: T-P4-016
source_agent: 狂蛮魔尊
claimed_at: 2026-09-07T03:38:00-06:00
created_at: 2026-09-07T03:44:00-06:00
inspected_commit: 5e812561b497f58bce6c63db7159e8875b014165
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_aggregate_reserve_composition_then_source_bind_total_increment_budgets_without_double_spending
---

# T-P4-016 — aggregate execution-remainder Schur budget without double-spending

## Scope

`T-P4-014` gave the sharp consumer for one already-composed same-coordinate coefficient and one transverse reserve term. `T-P4-015` then gave the source-to-math slice/Lipschitz bridge for one or several execution remainders. The remaining inequality gap is bookkeeping with mathematical content:

> When several execution remainders are routed into the same P4 channel, what is the correct aggregate Schur budget, and when is it invalid to let every term consume the full same-coordinate or transverse allowance independently?

This review answers that question and gives explicit counterexamples to unsafe reserve reuse. No source/IEEE bound, provenance, validation, admission, P4/M4 closure, or final integration is claimed.

Inputs used:

- `review-T-P4-014-kuangmanmozun-20260907T0247.md`;
- `review-T-P4-015-liuguanyi-20260907T0326.md`;
- `review-T-P4-007-liuguanyi-20260907T0212.md` for the execution residual ledger;
- the current block-4 constants already frozen in those reviews.

## 1. Same-coordinate budgets add before Schur absorption

Suppose one P4 scalar residual is decomposed as

```text
r = c*y + sum_i e_i + B,                                     (1)
```

with

```text
|e_i| <= beta_i |y|,    beta_i >= 0.                         (2)
```

Then, without any correlation information,

```text
|c*y + sum_i e_i|
  <= (|c| + sum_i beta_i) |y|.                               (3)
```

Thus the same-coordinate coefficient entering the Schur consumer is

```text
a := |c| + beta_total,
beta_total := sum_i beta_i.                                  (4)
```

The total budget is shared. A bound such as `beta_i <= 6/25` for every term does **not** imply `beta_total <= 6/25`.

The estimate is sharp from the stated information: choose `y>0`, choose the sign of `c*y` positive, and set every `e_i=beta_i*y`.

For the normalized block-4 coefficient `c=1/100`, the previously obtained quarter cap means

```text
beta_total <= 6/25,                                          (5)
```

not `beta_i<=6/25` termwise.

A two-term counterexample makes the failure explicit. If two independent remainders are each granted the full `6/25`, then

```text
a = 1/100 + 6/25 + 6/25 = 49/100,
a^2 = 2401/10000.                                            (6)
```

But block 4 has

```text
p4*d4 = 350003000000001 / 5000000000000000
      ~= 0.0700006,                                          (7)
```

whereas `2401/10000=0.2401`. Therefore the Schur condition fails even before any transverse or additive term is charged.

## 2. Disjoint transverse reserves: the coefficients add, and this is sharp

Now suppose the transverse part is a sum

```text
B = sum_i b_i,                                                (8)
```

and the certificate contains **distinct nonnegative reserve pieces** `H_i` with

```text
b_i^2 <= kappa_i H_i,
kappa_i >= 0,
H_i >= 0.                                                     (9)
```

By Cauchy-Schwarz,

```text
(sum_i |b_i|)^2
 <= (sum_i kappa_i) (sum_i H_i).                             (10)
```

Hence, if

```text
H_total >= sum_i H_i,                                        (11)
```

then

```text
B^2 <= kappa_total H_total,
kappa_total := sum_i kappa_i.                                (12)
```

This coefficient is sharp under only (9)-(11). To see it, take `H_i=kappa_i` and `b_i=kappa_i` with common sign. Then every inequality in (9) is equality and

```text
B^2 / H_total
 = (sum_i kappa_i)^2 / (sum_i kappa_i)
 = sum_i kappa_i.                                            (13)
```

Therefore, when reserve pieces are genuinely disjoint, `sum_i kappa_i` is the correct aggregate transverse cost; there is no generic improvement without correlation/cancellation information.

## 3. Shared-reserve trap: summing kappa_i can be false

A different situation is often hidden in informal bookkeeping: every term is bounded against the **same** reserve `H`:

```text
b_i^2 <= kappa_i H.                                          (14)
```

One may not infer

```text
(sum_i b_i)^2 <= (sum_i kappa_i) H.                          (15)   [FALSE in general]
```

The smallest counterexample is

```text
H=1,
kappa_1=kappa_2=1,
b_1=b_2=1.                                                     (16)
```

Both individual bounds hold exactly, but

```text
(b_1+b_2)^2 = 4 > 2 = (kappa_1+kappa_2) H.                  (17)
```

With a common reserve and no correlation information, the sharp coefficient is instead

```text
kappa_shared = (sum_i sqrt(kappa_i))^2.                      (18)
```

Indeed `|b_i|<=sqrt(kappa_i H)` gives the upper bound, and choosing all `b_i` with the same sign saturates it. Equation (18) is mathematically useful but awkward for exact-rational Lean/source contracts.

Therefore the preferred exact-rational interface is **not** to let several terms independently cite the same `H`. Instead either:

1. split the available positive quadratic reserve into explicit `H_i` pieces and use (9)-(12); or
2. aggregate the physical remainder first and certify one direct bound `B^2<=kappa H`; or
3. retain explicit weighted-allocation variables and prove a division-free Cauchy/Young allocation theorem.

## 4. Coordinate-slope form: aggregate first, dualize once

`T-P4-015` naturally produces transverse slice bounds on a diagonal positive reserve. Let

```text
H(z) = sum_j h_j z_j^2,    h_j>0.                            (19)
```

Suppose execution remainder `i` has a source-certified transverse increment bound

```text
|b_i(z)| <= sum_j gamma_ij |z_j|,
gamma_ij >= 0.                                                (20)
```

Define the aggregate coordinate slopes

```text
Gamma_j := sum_i gamma_ij.                                   (21)
```

Then

```text
|sum_i b_i(z)|
 <= sum_j Gamma_j |z_j|.                                     (22)
```

Weighted Cauchy-Schwarz yields the single dual-reserve coefficient

```text
(sum_i b_i(z))^2 <= kappa_joint H(z),                        (23)

kappa_joint := sum_j Gamma_j^2 / h_j.                        (24)
```

This is the correct source-to-consumer composition when all terms act on the same transverse coordinates. It is generally **not** equal to `sum_i kappa_i`, where `kappa_i=sum_j gamma_ij^2/h_j`, because

```text
Gamma_j^2 = (sum_i gamma_ij)^2                               (25)
```

contains the cross terms that represent simultaneous worst-case alignment.

The coefficient (24) is sharp under only the nonnegative slope information. For the linear extremal family

```text
b_i(z) = sum_j gamma_ij z_j                                 (26)
```

on the positive orthant, choose

```text
z_j proportional to Gamma_j/h_j.                            (27)
```

Then the ratio in (23) reaches `kappa_joint`.

This also shows the right place to exploit cancellation: if the source lane can certify a derivative/increment interval for the **sum** of several semantically compatible execution terms before taking absolute values, it may obtain a smaller `Gamma_j`. Once every term has separately been replaced by an absolute-value slope, that cancellation information has already been lost.

## 5. Full aggregate Schur theorem

Consider

```text
Q = p*x^2 + 2*x*r + d*y^2 + H,                              (28)
```

with

```text
p>0,
d>=0,
H>=0,
|r| <= a|y| + |B|,
B^2 <= kappa H,
a>=0,
kappa>=0.                                                     (29)
```

The sharp `T-P4-014/015` consumer gives

```text
a^2 + d*kappa <= p*d                                        (30)
```

as the information budget guaranteeing `Q>=0`.

Combining Sections 1 and 4, a source-facing sufficient condition for several execution terms is therefore

```text
(|c| + sum_i beta_i)^2
  + d * sum_j (sum_i gamma_ij)^2 / h_j
 <= p*d.                                                      (31)
```

If the transverse reserve is instead split into disjoint pieces `H_i`, replace the second term by

```text
d * sum_i kappa_i.                                           (32)
```

Equations (31)-(32) are the bookkeeping theorem that was missing between the slice bridge and the sharp Schur consumer.

## 6. Concrete block-4 exact budget

For block 4,

```text
p4 = 3/5,
d4 = 116667666666667 / 10^15,
c4 = 1/100.                                                   (33)
```

Let

```text
BETA := sum_i beta_i,
KAPPA := aggregate transverse dual-reserve cost              (34)
```

where `KAPPA` is either the joint coefficient (24) or the valid disjoint-reserve coefficient (12), depending on the actual certificate structure.

The exact closure condition is

```text
(1/100 + BETA)^2 + d4*KAPPA <= p4*d4.                        (35)
```

Clearing denominators gives the Lean/source-friendly form

```text
5000000000000000 * (1/100 + BETA)^2
+ 583338333333335 * KAPPA
<= 350003000000001.                                          (36)
```

If one deliberately spends the entire same-coordinate budget up to `a4=1/4`, so `BETA=6/25`, then the remaining transverse budget is exactly

```text
583338333333335 * KAPPA <= 37503000000001,                  (37)
```

or equivalently

```text
KAPPA <= 37503000000001 / 583338333333335
      ~= 0.06429030608309225.                                (38)
```

This is a **global per-channel** transverse allowance. It is not a per-remainder allowance. Even with genuinely disjoint reserves, two terms each charged at the full right side of (38) would have `KAPPA=2*KAPPA_max` and violate (37).

## 7. A rational reserve-allocation interface

To avoid square roots in Lean and checker outputs, a robust typed interface is:

```text
H_i >= 0,
sum_i H_i <= H,
b_i^2 <= kappa_i H_i,
kappa_i >= 0.                                                 (39)
```

Then expose only

```text
KAPPA = sum_i kappa_i.                                       (40)
```

The finite-sum Cauchy bridge proves

```text
(sum_i b_i)^2 <= KAPPA * H.                                  (41)
```

No matrix inverse or square root is needed. If the source checker instead starts from a common reserve `H`, it should produce an explicit rational allocation `H_i` (often coordinate groups or reserved fractions of the diagonal quadratic) and prove (39), rather than silently reusing `H` in every premise.

For a diagonal coordinate reserve from `T-P4-015`, an even better interface is to bypass artificial `H_i` and emit the aggregate slopes `Gamma_j` plus the single exact rational `KAPPA` in (24).

## 8. Failure boundaries / wrong routes ruled out

The following routes are mathematically invalid without extra hypotheses:

- granting each same-coordinate execution term its own independent `6/25` block-4 allowance;
- granting each transverse execution term the full block-4 `KAPPA_max` and then adding the residuals;
- proving `b_i^2<=kappa_i H` against one shared `H` and replacing the aggregate coefficient by `sum_i kappa_i`;
- separately taking absolute values of all source terms and later claiming cancellation that was not retained by the certified interface.

A correct closure must aggregate budgets before the final Schur step, and the positive quadratic reserve must have an explicit ownership/allocation semantics.

## 9. Lean-friendly theorem package

The first formal child can stay matrix-free.

### A. Two-term/discrete reserve composition

```lean
-- schematic
 theorem two_reserve_cauchy
    (b1 b2 k1 k2 H1 H2 H : Real)
    (hk1 : 0 <= k1) (hk2 : 0 <= k2)
    (hH1 : 0 <= H1) (hH2 : 0 <= H2)
    (hb1 : b1^2 <= k1*H1)
    (hb2 : b2^2 <= k2*H2)
    (hsum : H1 + H2 <= H) :
    (|b1| + |b2|)^2 <= (k1+k2)*H
```

A finite-sum version can follow if needed; the two-term lemma already supports iterative composition.

### B. Shared-reserve counterexample

A tiny theorem/`example` should record the obstruction numerically:

```lean
example :
  ((1:Real)^2 <= 1*1) /\ ((1:Real)^2 <= 1*1) /\
  !(((1:Real)+(1:Real))^2 <= (1+1)*1) := by norm_num
```

### C. Aggregate Schur consumer

Reuse the already-formalized `T-P4-014` theorem after proving

```text
|sum residuals| <= a|y| + |B|
B^2 <= KAPPA*H.
```

The concrete arithmetic corollary should use (36)-(37), not floating decimal constants.

## 10. Remaining blockers

- Source/IEEE lane: classify each `DeltaM/DeltaC/DeltaG/delta_ctrl/solveDefect` increment by same-coordinate slopes and transverse coordinates, or certify the aggregate increment directly.
- Certificate geometry: identify which positive P4 quadratic terms are genuinely distinct reserve pieces and which terms would be double-spending the same `H`.
- Truly additive reference bias remains outside this theorem and still needs cancellation, explicit slack, storage redesign, or the P5 finite-horizon/ultimate-bound route.
- Formalization/validation are separate tasks; this review does not claim Lean compile or axiom status.

## Status

`pending` mathematical child only. It changes no P4/M4 node, registry state, source-binding result, or final conclusion. Awaiting downstream formalization, 封不觉 independent validation if formalized, and 梁智炜 harvest/final integration decision.
