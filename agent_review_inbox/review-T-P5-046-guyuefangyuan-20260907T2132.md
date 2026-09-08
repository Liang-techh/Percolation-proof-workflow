---
kind: review_result
review_id: review-T-P5-046-guyuefangyuan-20260907T2132
task_id: T-P5-046
agent: 古月方源
source_agent: 古月方源
claimed_at: 2026-09-07T21:23:00-06:00
created_at: 2026-09-07T21:32:00-06:00
claim_commit: ab110a180e77e04ce02398de38fa30bd71740f0a
inspected_commit: 98e26659758694d87344c842b8c98c7d881aaf4c
inspected_paths:
  - agent_review_inbox/README.md
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/collaboration_board.md
  - agent_review_inbox/review-T-P5-044-honglianmozun-20260907T2050.md
  - agent_review_inbox/review-T-P5-045-liuguanyi-20260907T2108.md
  - agent_review_inbox/companion-T-P5-045-liuguanyi-20260907T2111.md
continuation_of:
  - review-T-P5-044-honglianmozun-20260907T2050
  - review-T-P5-045-liuguanyi-20260907T2108
related_tasks:
  - T-P5-039
  - T-P5-044
  - T-P5-045
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_the_exact_piecewise_r_optimizer_above_the_T-P5-045_interval_gate; permit_the_gate_itself_to_certify_positive_definiteness_when_the_robust_bias_envelope_is_nonnegative; do_not_grid_search_r
---

# T-P5-046 — exact Pareto-parameter optimizer for the robust correlated interval gate

## 0. Result

`T-P5-045` gives the correct source-facing robust correlated gate once a single
Pareto reserve parameter `r` has been chosen.  Its point-`r` quarter-barrier
specialization has the form

```text
800 E(r) < (109-r) D(r),                                (0.1)
```

where `D(r)` is the scaled determinant lower bound and `E(r)` is the robust
adjugate-bias upper bound.  The remaining mathematical question is whether the
checker must grid-search `r in [0,1]`.

It does not.  Because only `a4(r)` depends on `r`, both `D` and `E` are affine
in `r`.  Therefore the entire robust gate is one concave quadratic with an
exact rational optimizer and a square-root-free, division-free feasibility
criterion.

The same theorem applies verbatim to the `Kc=1/12` incremental/parameter gate;
only the charge multiplier changes from `800` to `2400`.

A second useful consequence is that one need not require the robust symmetric
block to be positive definite at `r=0`.  If the bias envelope is nonnegative,
**any strict successful gate automatically forces the determinant lower bound
positive at the selected `r`**, and then forces `pL(r)>0`.  Thus `r` itself may
repair an adverse diagonal source gain.

No calculus, eigenvalue, square root, floating optimization, or parameter grid
is needed.

---

## 1. Exact affine reduction of the T-P5-045 cell bounds

Keep one source cell fixed and assume its signed interval data do not depend on
the proof-design parameter `r`.  Put

```text
alpha := 53/1500.                                       (1.1)
```

The T-P5-045 lower/upper diagonal reserves can be written

```text
pL(r) = p0L + alpha*r,
pU(r) = p0U + alpha*r,                                  (1.2)
```

where

```text
p0L = 1/6 + k44L,
p0U = 1/6 + k44U.                                       (1.3)
```

The other signed-symmetric interval data are fixed:

```text
sL = 1/6 + k55L,
sU = 1/6 + k55U,
|sigma| <= Q,
sigma = k45+k54.                                        (1.4)
```

For component bias boxes

```text
|b4| <= beta4,
|b5| <= beta5,
beta4,beta5,Q >= 0,                                     (1.5)
```

T-P5-045 uses

```text
D(r) = 4*sL*pL(r)-Q^2,
E(r) = sU*beta4^2 + Q*beta4*beta5 + pU(r)*beta5^2.      (1.6)
```

Define the exact rational constants

```text
D0 := 4*sL*p0L-Q^2,
d  := 4*sL*alpha = (53/375)*sL,

E0 := sU*beta4^2 + Q*beta4*beta5 + p0U*beta5^2,
e  := alpha*beta5^2.                                    (1.7)
```

Then identically

```text
D(r) = D0+d*r,
E(r) = E0+e*r.                                          (1.8)
```

This is the only structure needed below.

---

## 2. One generic quadratic covers both quarter and parameter gates

Let `m>0` be the charge multiplier and define

```text
F_m(r) := (109-r)*(D0+d*r) - m*(E0+e*r).                (2.1)
```

For the two current consumers:

```text
quarter barrier:       m = 800,
Kc=1/12 parameter tube: m = 2400.                       (2.2)
```

Expand once:

```text
F_m(r) = A_m + B_m*r - d*r^2,                           (2.3)
```

with

```text
A_m := 109*D0 - m*E0,
B_m := 109*d - D0 - m*e.                                (2.4)
```

If `sL>0`, then `d>0`.  Therefore `F_m` is a strictly concave quadratic.

The exact square-completion identity is

```text
4*d*F_m(r)
 = 4*d*A_m + B_m^2 - (2*d*r-B_m)^2.                    (2.5)
```

This is a pure ring identity and should be the main Lean lemma.  It eliminates
calculus and gives the interior optimum immediately.

---

## 3. Exact optimizer on `0 <= r <= 1`

Assume

```text
d > 0.                                                  (3.1)
```

There are exactly three branches.

### 3.1 Left endpoint branch

If

```text
B_m <= 0,                                               (3.2)
```

then for every `r in [0,1]`,

```text
F_m(0)-F_m(r)
 = r*(d*r-B_m)
 >= 0.                                                  (3.3)
```

Hence

```text
r_opt = 0,
F_max = A_m.                                            (3.4)
```

### 3.2 Right endpoint branch

If

```text
B_m >= 2*d,                                             (3.5)
```

then

```text
F_m(1)-F_m(r)
 = (1-r)*(B_m-d*(1+r))
 >= 0                                                   (3.6)
```

for all `r in [0,1]`, because `1+r <= 2`.  Thus

```text
r_opt = 1,
F_max = A_m+B_m-d.                                      (3.7)
```

### 3.3 Interior branch

If

```text
0 < B_m < 2*d,                                          (3.8)
```

then the exact rational point

```text
r_opt := B_m/(2*d)                                      (3.9)
```

lies strictly in `(0,1)`.  From (2.5),

```text
F_max
 = F_m(r_opt)
 = A_m + B_m^2/(4*d).                                  (3.10)
```

The **feasibility test itself need not divide**.  Since `4*d>0`,

```text
F_max > 0
iff
4*d*A_m + B_m^2 > 0.                                   (3.11)
```

So the checker uses only rational additions, multiplications and comparisons to
decide whether the interior branch can close.  Division occurs only after PASS,
to materialize the rational witness `r_opt`.

---

## 4. Necessary-and-sufficient no-grid feasibility criterion

Combining the three branches, for `d>0` one has

```text
exists r, 0 <= r <= 1 and F_m(r)>0                     (4.1)
```

if and only if the corresponding branch condition below holds:

```text
B_m <= 0:
    A_m > 0;

B_m >= 2*d:
    A_m+B_m-d > 0;

0 < B_m < 2*d:
    4*d*A_m+B_m^2 > 0.                                 (4.2)
```

This is exact, not merely sufficient.  Therefore a FAIL of (4.2) is a genuine
obstruction for the entire `r in [0,1]` Pareto family under the current robust
cell envelope.  Further grid refinement of `r` cannot help; the only remaining
options are to tighten the source intervals/bias envelope or move to a stronger
correlated source description.

Conversely, any PASS provides an explicit rational witness `r=0`, `r=1`, or
`r=B_m/(2*d)`.

This is the direct correlated analogue of T-P5-039's scalar `r` optimizer, but
now `D(r)` itself also moves with `r` because the signed residual block modifies
the effective quadratic form.

---

## 5. A successful gate can certify positive definiteness by itself

T-P5-045 states the robust determinant conditions separately.  For optimizer
search it is useful to notice that a successful gate already contains them,
provided the robust bias envelope is nonnegative.

Assume

```text
0 <= r <= 1,
m > 0,
sL > 0,
Q >= 0,
E(r) >= 0,                                              (5.1)
```

and

```text
F_m(r) > 0.                                             (5.2)
```

Then

```text
(109-r)*D(r) > m*E(r) >= 0.                             (5.3)
```

Since `109-r >= 108 > 0`, necessarily

```text
D(r) > 0.                                               (5.4)
```

But

```text
D(r) = 4*sL*pL(r)-Q^2 > 0,                              (5.5)
```

with `sL>0` and `Q^2>=0`; hence also

```text
pL(r) > 0.                                              (5.6)
```

Thus the selected point automatically satisfies the positive-definite interval
premises needed by T-P5-045.

This matters when `D0<=0`: the proof-design reserve `a4(r)` may repair the
symmetric block at some larger `r`.  A checker that insists on `D(0)>0` before
running the optimizer can reject a genuinely feasible cell.

A practical sufficient condition for `E(r)>=0` throughout `[0,1]` is simply

```text
E0 >= 0,
e >= 0,                                                (5.7)
```

because then `E(r)=E0+e*r>=0`.  Here `e=alpha*beta5^2>=0` automatically; only
the recorded robust base envelope `E0>=0` needs to be checked.

---

## 6. Exact determinant-rescue witness

The positivity observation above is not vacuous.  Take the exact point cell

```text
k44 = -53/300,
k55 = 0,
k45 = 0,
k54 = 0,
b = 0.                                                  (6.1)
```

Then

```text
p0 = 1/6-53/300 = -1/100,
s  = 1/6,
Q  = 0,
E(r)=0.                                                 (6.2)
```

Therefore

```text
D0 = -1/150 < 0,                                        (6.3)
```

so a precondition demanding positive definiteness at `r=0` fails.

However at `r=1`,

```text
p(1) = -1/100 + 53/1500 = 19/750 > 0,
D(1) = 4*(1/6)*(19/750) = 19/1125 > 0.                 (6.4)
```

The quarter gate has exact positive margin

```text
F_800(1)
 = 108*(19/1125)
 = 228/125
 > 0.                                                   (6.5)
```

So `r` can genuinely rescue an initially indefinite signed residual block.

---

## 7. Exact interior-success witness with huge skew cancellation

There is also a strict reason not to test only the two endpoint certificates.
Take the exact point cell

```text
k44 = 0,
k55 = 0,
k45 = 100,
k54 = -100,                                             (7.1)
```

so

```text
sigma = k45+k54 = 0,
Q = 0.                                                  (7.2)
```

The residual block has arbitrarily large entrywise magnitude but its skew part
costs zero energy.  Let the remaining bias be exactly

```text
b4 = 5/72,
b5 = 22/75,                                             (7.3)
```

and use the exact point boxes `beta4=5/72`, `beta5=22/75`.

Then

```text
D0 = 1/9,
d  = 53/2250,
E0 = 294409/19440000,
e  = 6413/2109375.                                      (7.4)
```

For the quarter multiplier `m=800`, the quadratic coefficients are

```text
A_800 = -109/24300 < 0,
B_800 = 4093/168750.                                    (7.5)
```

Moreover

```text
0 < B_800 < 2*d,                                       (7.6)
```

so the exact optimizer is

```text
r_opt = B_800/(2*d) = 4093/7950.                        (7.7)
```

Both endpoint gates fail:

```text
F_800(0) = -109/24300 < 0,
F_800(1) = -11501/3037500 < 0.                          (7.8)
```

but the interior gate succeeds with exact positive margin

```text
F_800(r_opt)
 = 14151697/8049375000
 > 0.                                                   (7.9)
```

Thus endpoint-only testing is mathematically incomplete even after the signed
correlated reduction.  The interior rational optimizer strictly enlarges the
certifiable region.

This witness also reinforces the T-P5-045 signed-sum discipline.  If one first
took separate absolute values of the off-diagonal entries, one would replace
the true `Q=|100-100|=0` by the fake `Q_abs=200`, destroying the determinant
bound by roughly `40000` despite the exact skew cancellation.

---

## 8. Parameter/incremental tube specialization

For the `Kc=1/12` incremental tube, T-P5-045's point-`r` scaled gate is

```text
2400*E_g(r) < (109-r)*D(r).                             (8.1)
```

If

```text
E_g(r)=Eg0+eg*r,                                        (8.2)
```

then simply use the same generic formulas with

```text
m = 2400,
A_2400 = 109*D0-2400*Eg0,
B_2400 = 109*d-D0-2400*eg.                              (8.3)
```

The branch test (4.2) and the rational optimizer are unchanged.  Therefore the
existing all-`r` fallback

```text
200*Eg < 9*Dmin                                         (8.4)
```

should remain as a simple uniform sufficient condition, but it is no longer the
only exact-rational option.  A checker with affine `Eg(r)` can use the exact
optimizer above and may certify cells that the worst-`r` uniform fallback loses.

---

## 9. Suggested Lean theorem decomposition

The mathematics can be formalized without matrix APIs.  Minimal scalar targets:

```text
pareto_gate_quadratic_expansion
```

Prove (2.3)-(2.4) by `ring`.

```text
pareto_gate_complete_square
```

Prove (2.5) by `ring`.

```text
pareto_gate_max_left
pareto_gate_max_right
pareto_gate_max_vertex
```

Use (3.3), (3.6), and (2.5); only ordered-ring arithmetic is needed.

```text
pareto_gate_exists_iff_piecewise
```

State the exact three-branch iff (4.2).

```text
positive_robust_gate_implies_det_and_pL_positive
```

From `F_m(r)>0`, `E(r)>=0`, `sL>0`, `m>0`, and `0<=r<=1`, derive
`D(r)>0` and `pL(r)>0`.

```text
robust_correlated_quarter_gate_of_optimal_r
robust_correlated_one_twelfth_gate_of_optimal_r
```

These should be thin consumers that feed the selected rational `r` into the
already separate T-P5-045 interval theorem.  Do not duplicate the signed-sum or
adjugate proof in this child.

Exact regression theorems should preserve both witnesses in Sections 6 and 7.

---

## 10. Boundary / what this does not prove

This result is a source-independent mathematical optimizer only.

It does **not** provide:

- a deployed signed `J_u` / `K` interval table;
- Float64, finite-difference, controller or solve semantics;
- same-cell `beta4/beta5`, `E0`, or parameter-sensitivity bounds;
- P8 flowpipe/domain coverage;
- a Lean compile/axiom/comparator receipt;
- P5/P8/M4 admission.

It also does not authorize taking `r` inside source semantics.  `r` is only a
proof-design parameter selecting one already-valid Pareto energy inequality.
The source cell and its signed interval enclosure remain fixed.

If the exact piecewise test (4.2) fails for a cell, further `r` gridding cannot
repair that same robust envelope.  The correct next step is to improve the
signed source interval/correlation information, not to increase parameter
sampling density.

Status: **pending mathematical child**.
