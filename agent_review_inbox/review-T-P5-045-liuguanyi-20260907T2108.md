---
kind: review_result
review_id: review-T-P5-045-liuguanyi-20260907T2108
task_id: T-P5-045
agent: 柳冠一
source_agent: 柳冠一
claimed_at: 2026-09-07T20:59:00-06:00
created_at: 2026-09-07T21:08:00-06:00
claim_commit: ebd7db277ae069fb96e9fff34022a2a4c81cb5fc
inspected_commit: 12f8650e72e5555eb2aafe51653af391d623928d
inspected_paths:
  - agent_review_inbox/README.md
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/collaboration_board.md
  - agent_review_inbox/review-T-P5-041-liuguanyi-20260907T2020.md
  - agent_review_inbox/review-T-P5-043-kuangmanmozun-20260907T2050.md
  - agent_review_inbox/review-T-P5-044-honglianmozun-20260907T2050.md
continuation_of:
  - review-T-P5-041-liuguanyi-20260907T2020
  - review-T-P5-044-honglianmozun-20260907T2050
related_tasks:
  - T-P5-041
  - T-P5-042
  - T-P5-043
  - T-P5-044
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: expose_signed_symmetric_invariants_before_absolute_interval_enclosure; use_the_scaled_determinant_and_bias_box_theorem_as_the_source_to_T-P5-044_bridge; keep_skew_and_runtime_coverage_outside_this_child
---

# T-P5-045 — robust interval transport for the correlated signed residual gate

## 0. Result

`T-P5-044` leaves one source-to-math obligation explicitly open: the signed `2x2`
`u -> l` block may vary over a source cell, while a source checker usually exposes
interval data rather than an exact pointwise matrix.  The mathematically correct
bridge is **not** to take absolute values of the four entries of `K` separately.
The energy theorem only sees three symmetric invariants, and they admit a completely
rational, square-root-free robust interval certificate.

Write the signed residual decomposition from `T-P5-044` as

```text
l = K u + b,

K = [[k44,k45],
     [k54,k55]],

u = (u4,u5).
```

For the frozen P5 Pareto reserve

```text
a4(r) = (250+53r)/1500,
a5    = 1/6,
0 <= r <= 1,
```

define the **scaled symmetric coordinates**

```text
p     := a4(r) + k44,
s     := 1/6 + k55,
sigma := k45 + k54,
D4    := 4*p*s - sigma^2.                              (0.1)
```

If `q=(k45+k54)/2` and `Delta=p*s-q^2` are the variables of `T-P5-044`, then

```text
D4 = 4*Delta.                                           (0.2)
```

The correlated adjugate bias is simultaneously

```text
B := s*b4^2 - sigma*b4*b5 + p*b5^2,                    (0.3)
```

which is exactly `B_H(b)` from `T-P5-044`, because `2q=sigma`.

Hence the quarter-barrier condition

```text
200*B_H(b) < (109-r)*Delta
```

is equivalent to the division-free scaled condition

```text
800*B < (109-r)*D4.                                    (0.4)
```

This scaled interface removes every `/2` and `/4` from the source-facing theorem.
It also removes the skew coordinate `k45-k54` entirely: the skew part is genuinely
irrelevant to Lyapunov power, not merely bounded coarsely.

---

## 1. Cellwise interval contract

Let a source cell provide exact rational bounds

```text
rL <= r <= rU,
0 <= rL <= rU <= 1,

k44L <= k44 <= k44U,
k55L <= k55 <= k55U,
k45L <= k45 <= k45U,
k54L <= k54 <= k54U.                                   (1.1)
```

Do **signed interval addition first**:

```text
sigmaL := k45L + k54L,
sigmaU := k45U + k54U.                                 (1.2)
```

Choose a rational `Q >= 0` such that

```text
-Q <= sigmaL,
sigmaU <= Q.                                            (1.3)
```

Equivalently, the checker may choose

```text
Q = max(|sigmaL|,|sigmaU|),                             (1.4)
```

but `max` does not need to occur in the trusted theorem; the theorem only consumes
(1.3).

Define the rational endpoint reserves

```text
pL := (250+53*rL)/1500 + k44L,
pU := (250+53*rU)/1500 + k44U,

sL := 1/6 + k55L,
sU := 1/6 + k55U,

Dmin := 4*pL*sL - Q^2.                                  (1.5)
```

Then the following is enough:

```text
pL > 0,
Dmin > 0.                                               (1.6)
```

No separate `sL>0` premise is mathematically necessary.  From

```text
4*pL*sL > Q^2 >= 0
```

and `pL>0`, one gets `sL>0` automatically.  Therefore every point in the cell has

```text
p >= pL > 0,
s >= sL > 0,                                            (1.7)
```

and, because `|sigma| <= Q`, also

```text
D4 = 4*p*s-sigma^2
   >= 4*pL*sL-Q^2
   = Dmin
   > 0.                                                 (1.8)
```

Thus the positive-definite hypothesis of `T-P5-044` is certified uniformly by
one rational lower determinant.

This is the first bridge lemma:

```text
scaled_symmetric_det_lower_of_interval
```

with conclusion (1.7)-(1.8).

---

## 2. Robust adjugate-bias box without square roots

Suppose the remaining transverse/inhomogeneous source term has component boxes

```text
|b4| <= beta4,
|b5| <= beta5,
beta4 >= 0,
beta5 >= 0.                                           (2.1)
```

Define

```text
Ebox := sU*beta4^2 + Q*beta4*beta5 + pU*beta5^2.        (2.2)
```

Then pointwise on the cell,

```text
B
 = s*b4^2 - sigma*b4*b5 + p*b5^2
 <= sU*beta4^2 + Q*beta4*beta5 + pU*beta5^2
 = Ebox.                                                (2.3)
```

The proof uses only

```text
-sigma*b4*b5 <= |sigma|*|b4|*|b5|
               <= Q*beta4*beta5,
```

plus monotonicity of the two diagonal square terms.  There is no norm conversion,
no eigenvalue bound, no inverse and no radical.

This gives a minimal second lemma:

```text
scaled_adjugate_bias_le_box
```

consuming the signed-sum bound `|sigma|<=Q` rather than separate absolute bounds on
`k45` and `k54`.

A tighter optional interface should also be allowed.  If source interval arithmetic
can prove directly

```text
-sigma*b4*b5 <= chi,                                    (2.4)
```

then one may use

```text
Ecorr := sU*beta4^2 + chi + pU*beta5^2                 (2.5)
```

instead of (2.2).  The independent-box fallback is simply

```text
chi := Q*beta4*beta5.                                   (2.6)
```

So the typed contract should permit either a direct correlated cross cap `chi` or
its safe box specialization.  The theorem itself need not know how `chi` was found.

---

## 3. Exact cellwise quarter-barrier gate

Because `r <= rU`,

```text
109-r >= 109-rU > 0.                                   (3.1)
```

Combine (1.8) and (2.3).  If the rational checker establishes

```text
800*Ebox < (109-rU)*Dmin,                               (3.2)
```

then every point in the same cell satisfies

```text
800*B
 <= 800*Ebox
 <  (109-rU)*Dmin
 <= (109-r)*D4.                                         (3.3)
```

Using (0.2), this is exactly the `T-P5-044` strict quarter-barrier condition.

Therefore the main source-facing theorem can be stated as

```text
correlated_quarter_gate_of_interval_box
```

with only ordered-field/rational inequalities and the source interval premises.
It does **not** need to construct `q=(k45+k54)/2`, `Delta`, a matrix inverse, or a
square root.

For a whole-cell `r in [0,1]` checker, the constants simplify further.  Since

```text
min a4 = 1/6,
max a4 = 101/500,
min (109-r) = 108,
```

one may take

```text
pL = 1/6 + k44L,
pU = 101/500 + k44U,                                   (3.4)
```

and the uniform strict gate

```text
800*Ebox < 108*Dmin                                    (3.5)
```

is equivalent after division by the fixed integer `4` to the especially compact
integer check

```text
200*Ebox < 27*Dmin.                                    (3.6)
```

This is a useful exact-rational target for a production interval checker.

---

## 4. Parameter/incremental tube corollary

`T-P5-044` also gives the signed parameter residual

```text
Delta l = K*(Delta u) + g*(Delta c),
g = (g4,g5),                                           (4.1)
```

with one-twelfth tube gate

```text
600*G_H(g) < (109-r)*Delta.                             (4.2)
```

In the scaled coordinates here,

```text
G := s*g4^2 - sigma*g4*g5 + p*g5^2                     (4.3)
```

and (4.2) is exactly

```text
2400*G < (109-r)*D4.                                   (4.4)
```

If

```text
|g4| <= gamma4,
|g5| <= gamma5,
```

set

```text
Eg := sU*gamma4^2 + Q*gamma4*gamma5 + pU*gamma5^2.      (4.5)
```

Then the robust cellwise parameter gate is

```text
2400*Eg < (109-rU)*Dmin.                               (4.6)
```

For the global `r in [0,1]` range this simplifies exactly to

```text
200*Eg < 9*Dmin.                                       (4.7)
```

This gives a clean boundary/parameter compatibility theorem without reusing the
scalar `nu` route when signed two-channel parameter sensitivity is available.

---

## 5. Why the source must interval the signed sum before absolute values

This is not a cosmetic interface preference.  It can determine whether the proof
route succeeds or fails.

Take the exact skew family

```text
K_M = [[0, M],
       [-M,0]].                                         (5.1)
```

The true symmetric cross invariant is

```text
sigma = k45+k54 = M-M = 0.                              (5.2)
```

Hence

```text
D4 = 4*a4*a5,                                           (5.3)
```

which is positive and completely independent of `M`.  This agrees with the exact
energy cancellation in `T-P5-044`.

If a source adapter first forgets signs and exports only

```text
|k45| <= |M|,
|k54| <= |M|,
```

then the only generic sum bound becomes

```text
|sigma| <= 2|M|.                                        (5.4)
```

The resulting determinant lower certificate is merely

```text
Dmin_abs = 4*a4*a5 - 4*M^2,                             (5.5)
```

which becomes nonpositive once `M^2 >= a4*a5`, despite the exact determinant
remaining `4*a4*a5>0` for every `M`.

Therefore:

> **The source/checker must form a signed interval enclosure for
> `sigma = k45+k54` before entrywise absolute scalarization.**

The antisymmetric coordinate `k45-k54` need not appear in the energy contract at
all after the signed transform has been justified.

This is a genuine information-loss obstruction, not merely a loose constant.

---

## 6. Source-to-math adapter implied by T-P5-041

`T-P5-041` already identified the correct signed coordinate transform before taking
absolute values:

```text
(J_x,J_y) -> (J_u,J_transverse)
           = (J_y, J_x-J_y).                            (6.1)
```

For the correlated route, the recommended source pipeline is now:

```text
signed source Jacobian / affine enclosure
    -> transform to (u,x,parameter) coordinates
    -> extract signed 2x2 u->l block K
    -> form only the symmetric invariants
         k44,
         k55,
         sigma=k45+k54
    -> interval those invariants
    -> put transverse / parameter / anchor remainder into b or g
    -> certify Dmin and Ebox/Ecorr
    -> apply T-P5-045 interval gate
    -> apply T-P5-044 correlated energy completion.      (6.2)
```

The old `K_path` route remains a safe fallback when signed source data are unavailable,
but once `abs` has been taken separately on `k45` and `k54`, the skew cancellation in
(5.2) cannot in general be recovered downstream.

A useful typed payload is therefore conceptually

```text
SignedSymmetricResidualCell:
  r_lower, r_upper
  k44_lower, k44_upper
  k55_lower, k55_upper
  sigma_lower, sigma_upper
  b4_abs_cap, b5_abs_cap
  optional_cross_cap_chi
  source_key, state_key, cell_key, coordinate_key
```

rather than four unsigned gain magnitudes.  The keys are semantic obligations for
the source lane; this review does not claim they currently exist.

---

## 7. Minimal theorem statements

The formal core can be split into six small theorems.

```text
scaled_correlated_invariants
```

Prove exactly

```text
4*(p*s-((sigma/2)^2)) = 4*p*s-sigma^2
```

and

```text
s*b4^2 - 2*(sigma/2)*b4*b5 + p*b5^2
 = s*b4^2 - sigma*b4*b5 + p*b5^2.
```

This theorem alone may use a field; all source-facing inequalities below can remain
division-free.

```text
scaled_symmetric_det_lower_of_interval
```

From `pL>0`, `Dmin=4*pL*sL-Q^2>0`, `pL<=p`, `sL<=s`,
`-Q<=sigma<=Q`, prove

```text
p>0,
s>0,
Dmin <= 4*p*s-sigma^2.
```

```text
scaled_adjugate_bias_le_box
```

From the upper endpoint and absolute-value premises prove (2.3).

```text
scaled_adjugate_bias_le_cross_cap
```

Consume the optional direct premise `-sigma*b4*b5<=chi` and prove the tighter
(2.5).

```text
correlated_quarter_gate_of_interval_box
```

Combine `Dmin`, `Ebox`, `r<=rU` and (3.2) to prove (3.3).

```text
correlated_one_twelfth_parameter_gate_of_interval_box
```

The same argument with `Eg` and the coefficient `2400` proves (4.6).

The determinant/bias lemmas need only elementary ordered-ring/field arithmetic plus
squares/absolute-value inequalities.  No matrix library is required in the trusted
core if that causes unnecessary API overhead.

---

## 8. Assumptions and precise unresolved boundary

This child assumes only the mathematical identities already isolated in
`T-P5-041` and `T-P5-044`.  It does not re-audit the scalar optimizer/gates of
`T-P5-042/043` and does not compete with the Lean work on those tasks.

Still open:

- a deployed source/exporter that preserves signed `J_u` rather than only unsigned
  `K_path` entries;
- same-cell exact interval enclosures for `k44`, `k55`, and especially the signed
  sum `k45+k54`;
- component or correlated bounds for the actual transverse/anchor remainder `b`;
- parameter sensitivity bounds `g` for the incremental tube;
- first-exit/domain/trajectory coverage;
- Float64/libm/FD/controller/solve semantics;
- Lean compilation and axiom receipt;
- independent verification by 封不觉;
- comparator/provenance/admission and any P5/P8/M4 registry promotion.

A final important boundary: `Dmin<=0` from the independent interval box does **not**
prove the true pointwise `H` is indefinite.  It may only mean dependency information
was lost in intervalization.  A negative robust lower bound should therefore route
first to a tighter signed/correlated interval representation, not be reported as a
physical instability theorem.

Status: **pending mathematical/interface child**.
