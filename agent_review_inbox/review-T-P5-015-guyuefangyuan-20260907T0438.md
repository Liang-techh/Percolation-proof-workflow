---
kind: review_result
review_id: review-T-P5-015-guyuefangyuan-20260907T0438
task_id: T-P5-015
source_agent: 古月方源
claimed_at: 2026-09-07T04:24:00-06:00
created_at: 2026-09-07T04:38:00-06:00
inspected_commit: 34fe9d01737dfd969662099326efbfb7e20f0396
inspected_paths:
  - agent_review_inbox/review-T-P5-013-honglianmozun-20260907T0358.md
  - agent_review_inbox/review-T-P5-014-liuguanyi-20260907T0417.md
  - agent_review_inbox/review-T-P5-011-sumengchen-20260907T0221.md
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize generic damping-split certificate and the rational two-thirds corollary; let source/checker choose a rational split after binding Q,E,Rbar,T,g0
---

# T-P5-015 — optimized damping split for the finite-horizon cubic + weighted-dual barrier

## Scope

This is a mathematical child of the P5 finite-horizon barrier in `T-P5-013` and the weighted-dual source interface in `T-P5-014`.  It does **not** redo the cubic estimate, weighted Cauchy inequality, source binding, IEEE error accounting, provenance, or admission.

The only question is: once the available damping margin `g0` must be split as

```text
g0 = g_C + g_R,
```

how should one allocate damping between

- `g_C`: absorption of the cubic C-FD power term, and
- `g_R`: completion-of-squares payment for the weighted-dual remainder,

so that the finite-horizon first-exit barrier is as permissive as possible?

The fixed `50/50` split used in `T-P5-013` is convenient but not optimal.  A clean rational `2/3 : 1/3` split **strictly dominates it on every nonnegative instance that the 50/50 split can certify**, and it is exactly optimal when the initial/ramp energy load is zero.

## 1. Starting ledger

Use the notation already established by `T-P5-011`/`T-P5-013`:

```text
Zdot <= -g0 A + P_C + <r,v> + h_ramp,
P_C^2 <= Lambda A^3,
A <= K Z,
R_D(r) <= Rbar,
h_ramp <= Hbar.
```

Write

```text
Q := Lambda K >= 0,
E := Z0 + T Hbar.
```

For the nondegenerate case considered below assume

```text
Q > 0,  g0 > 0,  T >= 0,  Rbar >= 0,  E >= 0.
```

Split with a scalar `alpha`:

```text
0 < alpha < 1,
g_C = alpha g0,
g_R = (1-alpha) g0.
```

The cubic barrier may be taken at its largest value allowed by the scalar cubic information,

```text
Zstar = alpha^2 g0^2 / Q,
```

because `Q Zstar = g_C^2`.

The weighted-dual completion from `T-P5-013` gives

```text
-g_R A + <r,v> <= Rbar/(4 g_R).
```

Hence the first-exit headroom condition becomes

```text
E + T Rbar/[4(1-alpha)g0] < alpha^2 g0^2/Q.          (1)
```

This is the exact scalar optimization problem induced by the existing P5 information.

## 2. Dimensionless reduction

Define

```text
e   := Q E / g0^2,
rho := Q T Rbar / (4 g0^3).
```

Since `1-alpha>0`, (1) is equivalent to

```text
rho < H_e(alpha),
H_e(alpha) := (1-alpha)(alpha^2-e).                  (2)
```

Equivalently, without any division at all,

```text
4 Q (1-alpha) g0 E + Q T Rbar
  < 4 alpha^2 (1-alpha) g0^3.                        (3)
```

Equation (3) is the recommended checker/Lean-facing certificate.  The split parameter may be any rational number in `(0,1)`; no square root or calculus has to appear in the final proof object.

## 3. Exact optimal split

First, if `e >= 1`, no split can work: for every `0<alpha<1`, one has `alpha^2<1<=e`, hence `H_e(alpha)<=0`, while `rho>=0`.

Now assume `0 <= e < 1`.  Differentiating only to locate the optimizer gives

```text
H_e'(alpha) = e + 2 alpha - 3 alpha^2.
```

The unique critical point in the useful interval is

```text
alpha_* = [1 + sqrt(1+3e)]/3,
```

and it lies in `[2/3,1)`.

There is also a calculus-free algebraic proof of optimality that is better suited to later formalization.  At a stationary witness `s` satisfying

```text
e = 3 s^2 - 2 s,
```

one has the exact polynomial identity

```text
H_e(s) - H_e(alpha)
  = (alpha-s)^2 (2s + alpha - 1).                    (4)
```

For `s>=2/3` and `alpha>=0`, the right-hand side is nonnegative.  Thus `s=alpha_*` is the global maximizer on `[0,1]`, without needing a second-derivative argument.

At the optimum, using `e=3s^2-2s`,

```text
H_e(alpha_*) = 2 alpha_* (1-alpha_*)^2.              (5)
```

Therefore, for `0<=e<1`, the strict scalar split is feasible iff

```text
rho < 2 alpha_* (1-alpha_*)^2.                       (6)
```

Equality is the sharp boundary for this particular scalar split-ledger architecture: at equality the best split only saturates the first-exit budget, so it cannot prove the strict headroom required by the current barrier argument.

### Formalization note

The exact optimizer formula is useful analytically, but there is no reason to put `sqrt` into the checker.  Given rational `e`, a checker can choose a rational `alpha` near `alpha_*` and prove the polynomial certificate (3).  Soundness depends only on that rational certificate, not on numerical optimization.

## 4. A universal rational improvement: `2/3 : 1/3`

Take

```text
alpha = 2/3,
g_C = 2 g0/3,
g_R = g0/3.
```

Then

```text
H_e(2/3) = 4/27 - e/3,
```

so the normalized certificate is

```text
9 e + 27 rho < 4.                                    (7)
```

In original variables this clears to

```text
36 Q g0 E + 27 Q T Rbar < 16 g0^3.                  (8)
```

No division is present in (8).

For the current C-FD specialization from `T-P5-011`,

```text
Q = Lambda K = 13 S_F / 72000000000000000,
```

(8) reduces, after dividing a common factor `9`, to the exact integer certificate

```text
52 S_F g0 E + 39 S_F T Rbar
  < 128000000000000000 g0^3.                         (9)
```

For the current target `T=1` and `E=Z0+Hbar`, this is simply

```text
52 S_F g0 (Z0+Hbar) + 39 S_F Rbar
  < 128000000000000000 g0^3.                         (10)
```

This is a direct replacement candidate for the more conservative 50/50 source-facing inequality in `T-P5-013`.

## 5. `2/3` strictly dominates the existing `1/2` split

For the existing half split,

```text
H_e(1/2) = 1/8 - e/2.
```

The exact difference is

```text
H_e(2/3) - H_e(1/2)
  = 5/216 + e/6
  = (5 + 36e)/216 > 0                                (11)
```

for every `e>=0`.

Consequently, whenever the 50/50 split can certify a nonnegative instance, the 2/3 split certifies it with strictly more slack.  This is not merely a special-regime improvement.

In cleared original variables the 50/50 condition is

```text
4 Q g0 E + 2 Q T Rbar < g0^3.                        (12)
```

Under `Q,E,T,Rbar>=0` and `g0>0`, (12) implies (8).  A Lean proof can be done by `nlinarith` after introducing the nonnegative products, or by transporting (11).

### Concrete rational counterexample to “50/50 is enough/optimal”

Take the normalized values

```text
e = 0,
rho = 7/50.
```

Then

```text
7/50 > 1/8,
```

so the 50/50 split fails, but

```text
7/50 < 4/27,
```

so the 2/3 split succeeds.  This gives an exact rational witness that the older split rejects a case admitted by the new one.

Two useful endpoint comparisons are:

- pure remainder load `E=0`: 50/50 allows `Q T Rbar/g0^3 < 1/2`, whereas 2/3 allows `<16/27`, an `32/27` (~18.5%) larger remainder budget; and
- pure baseline/ramp load `Rbar=0`: 50/50 requires `e<1/4`, whereas 2/3 allows `e<4/9`.

For `E=0`, `alpha=2/3` is in fact the exact optimizer from (5), so no other fixed split can improve the pure-remainder threshold.

## 6. Degenerate branches

### `Q=0`

If `Q=Lambda K=0`, then the cubic square estimate forces the cubic contribution to vanish in the corresponding exact-real branch.  There is no reason to reserve damping for `g_C`; all available damping may be assigned to the weighted-dual remainder.  This branch should stay separate from formulas containing division by `Q`.

### `Rbar=0` (or `T=0`)

There is no additive weighted-dual rate to pay.  The formal split can take `g_R=0` if the downstream theorem permits it; otherwise one can choose rational `alpha<1` arbitrarily close to `1`.  The sharp scalar energy condition approaches

```text
e < 1,
```

which is much less restrictive than either fixed 1/2 or 2/3 split.

## 7. Suggested Lean theorem decomposition

The first theorem should be purely algebraic and generic.

```text
theorem damping_split_certificate
  (Q g0 E T Rbar alpha : R)
  (hQ : 0 < Q) (hg : 0 < g0)
  (hE : 0 <= E) (hT : 0 <= T) (hR : 0 <= Rbar)
  (ha0 : 0 < alpha) (ha1 : alpha < 1)
  (hcert :
    4*Q*(1-alpha)*g0*E + Q*T*Rbar
      < 4*alpha^2*(1-alpha)*g0^3) :
  E + T*(Rbar / (4*((1-alpha)*g0)))
    < alpha^2*g0^2/Q
```

The exact conclusion can instead be packaged into the `g_C/g_R/Zstar/B_R` premises expected by the existing finite-horizon barrier theorem.

Second, add the rational specialization:

```text
theorem two_thirds_split_certificate ...
  (hcert : 36*Q*g0*E + 27*Q*T*Rbar < 16*g0^3) :
  <the P5-013 split premises with g_C=2*g0/3, g_R=g0/3>
```

Third, formalize the dominance lemma:

```text
theorem two_thirds_dominates_half ...
  (hhalf : 4*Q*g0*E + 2*Q*T*Rbar < g0^3) :
  36*Q*g0*E + 27*Q*T*Rbar < 16*g0^3
```

with the same nonnegativity assumptions.

Optional, source-independent optimizer support can be kept as the polynomial identity

```text
theorem split_objective_stationary_identity
  (e s alpha : R)
  (hs : e = 3*s^2 - 2*s) :
  (1-s)*(s^2-e) - (1-alpha)*(alpha^2-e)
    = (alpha-s)^2*(2*s+alpha-1)
```

proved by `ring`.  This gives the exact optimizer comparison without importing calculus.

Finally, for the current C-FD constant, formalize the rational reduction (9) by `norm_num`/`ring_nf` rather than carrying decimal approximations.

## 8. Dependencies and remaining blockers

This result consumes, but does not replace:

- `T-P5-011`: cubic energy barrier and `Q=Lambda K`;
- `T-P5-013`: weighted-dual/ramp finite-horizon first-exit ledger;
- `T-P5-014`: conversion of source/runtime remainder information into `Rbar`.

Still open after this child:

1. actual source/checker computation and binding of `S_F`, hence `Q`;
2. actual `Z0` and same-domain ramp-work cap `Hbar`;
3. actual weighted-dual cap `Rbar`, including runtime/solve/controller remainder composition;
4. any execution-level IEEE/solve semantics not already included in `Rbar`;
5. ODE/coverage assumptions needed by the first-exit theorem;
6. independent validation and final integration.

The optimization should happen **after** `Q,E,Rbar,T,g0` are bound: a small rational search over `alpha` can approximate the exact optimum, while certificate (3) keeps the proof object entirely rational and square-root free.

## Status

`pending` mathematical result.  No P5/P8/M4 state, registry, provenance, or final conclusion was modified.  Await formalization/independent validation and 梁智炜 integration.
