---
kind: review_result
review_id: review-T-P4-017-kuangmanmozun-20260907T0449
task_id: T-P4-017
source_agent: 狂蛮魔尊
claimed_at: 2026-09-07T04:41:00-06:00
created_at: 2026-09-07T04:49:00-06:00
inspected_commit: 0d27aeddcab85203f116f0b373dfe710cde26afa
inspected_paths:
  - docs/routeb-p4-kc-force-contract.md
  - agent_review_inbox/review-T-P4-011-kuangmanmozun-20260907T0046.md
  - agent_review_inbox/review-T-P4-013-kuangmanmozun-20260907T0145.md
  - agent_review_inbox/review-T-P4-014-kuangmanmozun-20260907T0247.md
  - agent_review_inbox/review-T-P4-015-liuguanyi-20260907T0326.md
  - agent_review_inbox/review-T-P4-016-kuangmanmozun-20260907T0344.md
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: keep_generic_Schur_and_slice_lemmas_but_replace_canonical_block4_specializations_by_c_eq_1_over_20_and_beta_total_eq_1_over_5_quarter_headroom
---

# T-P4-017 — canonical-scale repair of the aggregate P4 Schur budget

## Scope

The generic inequality work in `T-P4-013/014/015/016` is useful, but several concrete block-4 specializations instantiate the `kc` coefficient as `c=1/100`. The current canonical source contract instead fixes the generalized-force cross contribution as

```text
rho_kc(q_B) = (q5/20, q4/20).
```

This review performs only the mathematical repair forced by that scale choice. It does not revisit source authentication, IEEE error bounds, validation, admission, or final P4/M4 integration.

The main conclusion is simple but important:

> The scale-free Schur/slice/aggregation lemmas remain correct. Under the current canonical contract, however, every source-facing block-4 budget must use `c=1/20`, not `c=1/100`. Consequently the shared same-`q5` headroom under a total `1/4` envelope is `1/5`, not `6/25`.

The old `6/25` allowance is not merely conservative or differently normalized: when combined with the canonical `1/20` term it produces total coefficient `29/100`, which already violates the sharp block-4 Schur condition even with zero transverse remainder.

## 1. Canonical scale and the generic consumer

For one scalar channel write

```text
r = c y + sum_i e_i + B,
|e_i| <= beta_i |y|,
B^2 <= kappa H,
H >= 0.
```

Define the total same-coordinate slope

```text
beta_total := sum_i beta_i,
a := |c| + beta_total.
```

The generic results of `T-P4-014/015/016` give the sharp source-independent budget

```text
a^2 + d kappa <= p d,                                      (1)
```

with `p>0` and the usual nonnegativity hypotheses. Equivalently,

```text
p x^2 + 2 x r + d y^2 + H >= 0.                            (2)
```

The proof and the reserve-composition rules do not depend on the numerical value of `c`.

Under the current canonical source contract, channel 4 has

```text
c4 = 1/20,
y  = q5,                                                    (3)
```

and channel 5 has the analogous `c5=1/20` with cross coordinate `q4` whenever a compatible scalar Schur consumer is available.

Therefore the correct aggregate coefficient is

```text
a4 = 1/20 + beta_total,                                     (4)
```

not `1/100 + beta_total`.

## 2. Corrected exact block-4 budget

Use the existing block-4 abstract constants

```text
p4 = 3/5,
d4 = 116667666666667 / 10^15.
```

Then

```text
p4 d4 = 350003000000001 / 5000000000000000.                (5)
```

Substituting (4) into (1) gives

```text
(1/20 + beta_total)^2 + d4 kappa
  <= p4 d4.                                                  (6)
```

After clearing the fixed denominator, the exact source/checker-friendly form is

```text
5000000000000000 * (1/20 + beta_total)^2
+ 583338333333335 * kappa
<= 350003000000001.                                         (7)
```

This is the canonical replacement for the `1/100 + BETA` specialization written in `T-P4-016`.

No square root is needed. If `beta_total` and `kappa` are rational, (7) is exact rational arithmetic.

## 3. Correct shared headroom under the existing quarter consumer

If downstream code deliberately keeps the already formalized total coefficient cap

```text
a4 <= 1/4,                                                   (8)
```

then from (4)

```text
beta_total <= 1/4 - 1/20 = 1/5.                             (9)
```

Thus `1/5` is the entire shared allowance for all same-`q5` execution remainders combined. It is not a per-term allowance.

This recovers the canonical-scale result already implicit in `T-P4-011` and repairs the later `6/25` specialization.

At the quarter boundary `beta_total=1/5`, the total coefficient is still exactly `a4=1/4`, so the remaining Schur curvature is

```text
Delta_quarter
 := p4 d4 - (1/4)^2
  = 37503000000001 / 5000000000000000.                     (10)
```

Therefore the total transverse reserve budget at the quarter boundary is unchanged numerically:

```text
583338333333335 * kappa
<= 37503000000001,                                          (11)
```

or

```text
kappa <= 37503000000001 / 583338333333335
      ~= 0.0642903060831.                                   (12)
```

This is a useful distinction: the transverse number in (12) survives only because both the stale and corrected routes are being compared at the same **total** coefficient `a4=1/4`. What changes is how much same-coordinate budget remains after charging the canonical `kc` term.

## 4. Explicit failure of the stale `6/25` same-coordinate allowance

Suppose one incorrectly combines the canonical coefficient with the later stale same-coordinate allowance

```text
c4 = 1/20,
beta_total = 6/25.
```

Then

```text
a4 = 1/20 + 6/25 = 29/100.                                 (13)
```

Its square is

```text
(29/100)^2 = 841/10000 = 0.0841,
```

whereas (5) gives

```text
p4 d4 ~= 0.0700006.
```

Exactly,

```text
p4 d4 - (29/100)^2
 = -70496999999999 / 5000000000000000 < 0.                 (14)
```

Hence no nonnegative transverse reserve budget can repair this coefficient within the same homogeneous Schur architecture: setting the transverse state to zero already fails.

A concrete extremizer removes any ambiguity. Take

```text
y = 1,
e = 6/25,
r = y/20 + e = 29/100,
x = -r/p4 = -29/60,
H = 0.
```

Then

```text
p4*x^2 + 2*x*r + d4*y^2
 = d4 - r^2/p4
 = -70496999999999 / 3000000000000000
 < 0.                                                        (15)
```

Thus the claim “canonical `kc` plus a `6/25` same-coordinate remainder is absorbed by block 4” is mathematically false, not merely unsupported.

## 5. Canonical `kc` alone and the real transverse capacity

With no additional same-coordinate remainder (`beta_total=0`), the canonical `kc` term leaves

```text
Delta_kc
 := p4 d4 - (1/20)^2
  = 337503000000001 / 5000000000000000.                    (16)
```

Hence a transverse quadratic remainder may consume at most

```text
583338333333335 * kappa
<= 337503000000001,                                         (17)
```

that is

```text
kappa
<= 337503000000001 / 583338333333335
~= 0.578571612243.                                          (18)
```

For comparison, using `c=1/100` would report about `0.59914286449`. That larger number is not available under the present canonical source scale.

The exact tradeoff for any `beta_total>=0` is therefore

```text
kappa_max(beta_total)
 = [p4 d4 - (1/20 + beta_total)^2] / d4                     (19)
```

whenever the numerator is nonnegative. Formula (7), rather than the divided form (19), is the preferred proof/checker interface.

## 6. Sharp same-coordinate limit versus the convenient quarter limit

If `kappa=0`, the information-theoretically sharp same-coordinate condition is

```text
(1/20 + beta_total)^2 <= p4 d4.                             (20)
```

Numerically this allows

```text
beta_total <= sqrt(p4 d4) - 1/20
           ~= 0.214576264997.                               (21)
```

The rational quarter consumer uses only

```text
beta_total <= 1/5 = 0.2.                                    (22)
```

So the quarter route is conservative by about `0.0145763` in slope, but it remains comfortably valid. If later source bounds land between `1/5` and the sharp limit, there is no mathematical reason to reject them; one should use the generic sharp theorem rather than forcing the quarter corollary.

For Lean/checker use, avoid the square root and test (20) directly.

## 7. The historical `1/100` total residual target is impossible at canonical scale

The canonical `kc` coefficient is already

```text
1/20 > 1/100.                                                (23)
```

Therefore even with all other remainders identically zero there is no universal envelope

```text
|r_total| <= (1/100)|y|                                     (24)
```

for the canonical channel-4 `kc` term.

This differs qualitatively from the `c=1/100` specialization, where `kc` alone saturated (24). Under the current canonical contract, the old `1/100` total target is simply dead for any nonzero cross coordinate.

## 8. Local-state quadratic cost also returns to the canonical scale

For the canonical vector

```text
rho_kc = (q5/20,q4/20),
```

one has exactly

```text
||rho_kc||^2 = (q4^2+q5^2)/400.                             (25)
```

With

```text
Pstate = (3/2)(q4^2+q5^2) + (4/5)(v4^2+v5^2),
```

this gives

```text
||rho_kc||^2 <= Pstate/600.                                 (26)
```

On `Pstate<=28/5`,

```text
||rho_kc||^2 <= 7/750.                                      (27)
```

Therefore the later `Pstate/15000` / `7/18750` values belong to the differently normalized toy coordinate and are not canonical source-facing bounds under the current contract.

## 9. What remains reusable from T-P4-013/014/015/016

The following mathematics remains valid without change:

1. the generic shifted-residual theorem with arbitrary coefficient `c`;
2. the relative-plus-transverse Schur identity and its sharpness witness;
3. the slice decomposition and increment/Lipschitz bridge;
4. the rule that same-coordinate slopes must be summed before absorption;
5. the warning that independent bounds against one shared transverse reserve cannot simply sum their `kappa_i`;
6. the aggregate-first weighted-dual formula for a genuine shared transverse state.

Only source-facing specializations that hard-code `c=1/100` (or channel-5 `c=1/200`) must not be used as canonical `kc` consumers while `docs/routeb-p4-kc-force-contract.md` remains authoritative.

The already compiled generic Lean theorem from `T-P4-014` therefore does not need to be discarded. A future formalization should instantiate that theorem at `c=1/20` and use a new canonical block-4 corollary rather than rewriting the generic proof.

## 10. Minimal Lean theorem/corollary targets

The mathematical repair can be formalized with very small statements.

```lean
-- Generic source-independent theorem is reused.
-- New canonical arithmetic specialization:
theorem block4_canonical_budget
    (beta kappa : ℝ)
    (hbudget :
      5000000000000000 * (1/20 + beta)^2
      + 583338333333335 * kappa
      <= 350003000000001) :
    (1/20 + beta)^2
      + (116667666666667/1000000000000000 : ℝ) * kappa
      <= (3/5 : ℝ) * (116667666666667/1000000000000000 : ℝ)

-- Quarter headroom at canonical scale.
theorem canonical_quarter_headroom :
  (1/20 : ℝ) + 1/5 = 1/4

-- Concrete obstruction to carrying over 6/25.
theorem canonical_six_twentyfive_failure :
  (3/5 : ℝ) * (-29/60)^2
  + 2 * (-29/60) * (29/100)
  + (116667666666667/1000000000000000 : ℝ)
  < 0

-- Canonical transverse capacity with no other same-coordinate remainder.
theorem canonical_kc_transverse_budget
    (kappa : ℝ)
    (h : 583338333333335*kappa <= 337503000000001) :
    (1/20 : ℝ)^2
      + (116667666666667/1000000000000000 : ℝ)*kappa
      <= (3/5 : ℝ)*(116667666666667/1000000000000000 : ℝ)
```

A stronger source-independent theorem is unnecessary here because the generic theorem already exists; only the canonical specialization needs repair.

## 11. Remaining blockers and next step

This review does not produce any deployed remainder coefficient. The next physical/source tasks remain:

1. bind the `T-P4-007` execution increments to same-coordinate or transverse budgets on the same covered domain;
2. aggregate all same-coordinate coefficients into one `beta_total` and all transverse terms into one non-double-counted `kappa`;
3. test the canonical exact condition (7);
4. keep genuine additive reference bias outside this homogeneous Schur budget unless an independent scalar slack/storage route is provided;
5. keep `T-P4-012` remote `M_BD a_D` on its separate mass-metric route.

Admission remains `pending`. The concrete correction is mathematical: under the current canonical source contract, use `c=1/20`; the quarter same-coordinate headroom is `1/5`, and `6/25` is explicitly impossible for block 4 when added to the canonical `kc` term.