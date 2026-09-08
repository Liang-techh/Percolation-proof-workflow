---
kind: review_result
review_id: review-T-P5-047-kuangmanmozun-20260907T2148
task_id: T-P5-047
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
claimed_at: 2026-09-07T21:35:00-06:00
created_at: 2026-09-07T21:48:00-06:00
claim_commit: 99384cd7f2d39325207b7203ac461e0a8fdee502
inspected_commit: 349807ff733f047664136c3f7172666e15d4a2a7
continuation_of:
  - review-T-P5-045-liuguanyi-20260907T2108
  - review-T-P5-046-guyuefangyuan-20260907T2132
related_tasks:
  - T-P5-044
  - T-P5-045
  - T-P5-046
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: if_one_P5_candidate_must_freeze_a_single_Pareto_r_for_both_quarter_and_parameter_gates_use_the_five_candidate_shared_r_checker_below_instead_of_two_independent_optimizers; if_separate_r_witnesses_are_semantically_allowed_do_not_impose_this_extra_constraint
---

# T-P5-047 — exact no-grid shared-`r` optimizer for simultaneous correlated P5 gates

## 0. Result

`T-P5-046` exactly optimizes one correlated robust gate of the form

```text
F(r) = A + B*r - d*r^2,       0 <= r <= 1,       d > 0.
```

It then applies the same one-gate optimizer separately to the quarter barrier and
the `Kc=1/12` parameter/incremental tube.  If the final bundled P5 certificate is
required to freeze **one common Pareto parameter `r`** for both consumers, however,
two separate PASS results are not enough: their positive intervals can be disjoint.

For the two simultaneous margins

```text
f1(r) = A1 + B1*r - d*r^2,
f2(r) = A2 + B2*r - d*r^2,                              (0.1)
```

there is nevertheless an exact square-root-free and grid-free decision rule.
Because the two quadratics have the **same curvature `-d`**, their difference is
affine.  Consequently the lower envelope

```text
h(r) := min(f1(r),f2(r))                                (0.2)
```

has at most one kink.  Its maximum on `[0,1]` is attained at one of only five
types of rational candidates:

```text
r = 0,
r = 1,
r = B1/(2d)  if this is an active interior vertex,
r = B2/(2d)  if this is an active interior vertex,
r = the unique affine crossover of f1 and f2.           (0.3)
```

All five PASS tests can be written **division-free**.  Therefore a checker never
needs a square root, algebraic root object, floating optimizer, or `r` grid.

The resulting criterion is necessary and sufficient.  If it fails, there is no
single `r in [0,1]` satisfying both strict gates under the present affine robust
envelopes.

---

## 1. Generic same-curvature theorem

Assume throughout

```text
d > 0.                                                  (1.1)
```

Put

```text
c := A1-A2,
q := B1-B2.                                             (1.2)
```

Then

```text
f1(r)-f2(r) = c+q*r.                                    (1.3)
```

Define the following five exact-rational PASS predicates.

### L — left endpoint

```text
L :<=> A1 > 0 and A2 > 0.                               (1.4)
```

This is exactly `f1(0)>0` and `f2(0)>0`.

### R — right endpoint

```text
R :<=> A1+B1-d > 0 and A2+B2-d > 0.                    (1.5)
```

This is exactly `f1(1)>0` and `f2(1)>0`.

### V1 — active vertex of the first gate

```text
V1 :<=>
  0 < B1,
  B1 < 2*d,
  4*d*A1 + B1^2 > 0,
  2*d*c + q*B1 <= 0.                                   (1.6)
```

The first two inequalities put

```text
r1 := B1/(2*d)                                          (1.7)
```

strictly inside `(0,1)`.  The third is exactly `f1(r1)>0`, because

```text
4*d*f1(r1) = 4*d*A1+B1^2.                              (1.8)
```

The final inequality is exactly the active-branch condition

```text
f1(r1) <= f2(r1),                                       (1.9)
```

multiplied by the positive denominator `2*d`.

### V2 — active vertex of the second gate

Symmetrically,

```text
V2 :<=>
  0 < B2,
  B2 < 2*d,
  4*d*A2 + B2^2 > 0,
  2*d*c + q*B2 >= 0.                                   (1.10)
```

The last sign is reversed because `f2` is the lower/active branch exactly when
`f1-f2 >= 0`.

### X — strict interior crossover

The affine difference (1.3) has a strict interior zero exactly when

```text
c*(c+q) < 0.                                            (1.11)
```

Indeed this says the endpoint values of `f1-f2` have opposite signs.  In that
case `q != 0` and the unique crossover is

```text
rx := -c/q,          0 < rx < 1.                        (1.12)
```

At this point `f1(rx)=f2(rx)`.  Multiplying its common value by `q^2>0` gives

the exact polynomial numerator

```text
Xnum := A1*q^2 - B1*c*q - d*c^2,                        (1.13)
q^2*f1(rx) = q^2*f2(rx) = Xnum.                         (1.14)
```

Hence define

```text
X :<=> c*(c+q) < 0 and Xnum > 0.                        (1.15)
```

No division is needed to decide this branch.  Division by `q` is needed only
after PASS to materialize the rational witness `rx`.

---

## 2. Exact shared-feasibility criterion

The main theorem is

```text
exists r,
  0 <= r and r <= 1 and
  f1(r) > 0 and f2(r) > 0

iff

L or R or V1 or V2 or X.                                (2.1)
```

This is an exact obstruction theorem, not merely a sufficient shortlist.

### Proof

The reverse implication is immediate from the explicit witnesses

```text
0,
1,
B1/(2d),
B2/(2d),
-c/q.                                                   (2.2)
```

For the forward implication, consider the lower envelope `h=min(f1,f2)`.
Equation (1.3) shows that the identity of the lower branch can change at most
once.  Therefore `[0,1]` is split into at most two closed subintervals, and on
each subinterval `h` is exactly one of the two quadratics.

For either quadratic one has the pure ring identity

```text
4*d*( f_i(B_i/(2d)) - f_i(r) )
  = (2*d*r-B_i)^2 >= 0.                                 (2.3)
```

Thus on a subinterval the maximum occurs either at its interior vertex
`B_i/(2d)` when that vertex belongs to the active branch, or at a subinterval
endpoint.  Every such endpoint is one of `0`, `1`, or the unique crossover.
The corresponding strict positivity tests are precisely `L,R,V1,V2,X`.
This exhausts every possible maximizer of `h`, proving (2.1).

A Lean proof does not need calculus: (2.3), the affine sign split (1.3), and
ordered-field case analysis suffice.

---

## 3. Specialization to the current P5 correlated gates

Use the robust affine quantities from `T-P5-045/T-P5-046`:

```text
D(r)  = D0 + d*r,             d > 0,
Eb(r) = Eb0 + eb*r,
Eg(r) = Eg0 + eg*r.                                    (3.1)
```

The quarter-barrier and parameter/incremental margins are

```text
Fb(r) := (109-r)*D(r) - 800*Eb(r),
Fg(r) := (109-r)*D(r) - 2400*Eg(r).                    (3.2)
```

Expand:

```text
Fb(r) = Ab + Bb*r - d*r^2,
Fg(r) = Ag + Bg*r - d*r^2,                             (3.3)
```

where

```text
Ab = 109*D0 - 800*Eb0,
Bb = 109*d - D0 - 800*eb,

Ag = 109*D0 - 2400*Eg0,
Bg = 109*d - D0 - 2400*eg.                             (3.4)
```

So the generic theorem applies verbatim with the **same** curvature `d`.

There is an additional simplification specific to P5.  Define

```text
H0 := 3*Eg0 - Eb0,
h  := 3*eg  - eb.                                      (3.5)
```

Then the determinant part cancels exactly from the difference:

```text
Fb(r)-Fg(r) = 800*(H0+h*r).                             (3.6)
```

Hence the active bottleneck is decided only by the two robust bias envelopes,
not by `D0` or `d`.

### 3.1 Dominance early exits

Because `H0+h*r` is affine, if

```text
H0 >= 0 and H0+h >= 0,                                 (3.7)
```

then `Fb>=Fg` on all of `[0,1]`.  The parameter gate is globally stronger, so
shared feasibility is exactly the one-gate feasibility of `Fg` from T-P5-046.
Equivalently, this is the robust-envelope condition

```text
Eb(0) <= 3*Eg(0),
Eb(1) <= 3*Eg(1).                                      (3.8)
```

If instead

```text
H0 <= 0 and H0+h <= 0,                                 (3.9)
```

then `Fb<=Fg` everywhere and the quarter gate alone is the bottleneck.

These two endpoint comparisons are enough because the envelope difference is
affine.

### 3.2 Crossing regime

A strict bottleneck switch occurs exactly when

```text
H0*(H0+h) < 0.                                         (3.10)
```

Then

```text
rx = -H0/h in (0,1).                                   (3.11)
```

At the switch, `Eb(rx)=3*Eg(rx)`, so the two charge terms are identical:

```text
800*Eb(rx) = 2400*Eg(rx).                              (3.12)
```

The strict crossover PASS test can be written with no division as

```text
Ab*h^2 - Bb*H0*h - d*H0^2 > 0.                         (3.13)
```

For the quarter vertex, the active-branch condition reduces to

```text
2*d*H0 + h*Bb <= 0,                                    (3.14)
```

and for the parameter vertex to

```text
2*d*H0 + h*Bg >= 0.                                    (3.15)
```

Thus the P5 production checker can use the same five-candidate decision surface
without carrying the generic `800` scale in the crossover arithmetic.

---

## 4. Why separate per-gate optimization is not enough

There is a one-parameter exact family that isolates the issue.  For `eps>0`, set

```text
f1_eps(r) := eps - (r-1/4)^2,
f2_eps(r) := eps - (r-3/4)^2.                           (4.1)
```

Both have curvature `d=1`.  Each gate separately has strict maximum `eps>0`, at
`r=1/4` and `r=3/4` respectively.  Therefore two independent T-P5-046-style
optimizers both return PASS for every `eps>0`.

But their difference is

```text
f1_eps(r)-f2_eps(r) = 1/2-r,                            (4.2)
```

so the unique crossover is `r=1/2`.  Moreover for every real `r`, at least one
of the two distances from `1/4` and `3/4` is at least `1/4`.  Hence

```text
min(f1_eps(r),f2_eps(r)) <= eps-1/16,                   (4.3)
```

with equality at `r=1/2`.  Therefore the exact shared optimum is

```text
max_[0,1] min(f1_eps,f2_eps) = eps-1/16.                (4.4)
```

This gives all three closure regimes in one rational family:

```text
eps = 1/100:
  each gate separately PASSes,
  but the best common margin is -21/400 < 0;
  there is no shared r at all.

eps = 1/16:
  the only common weak point is r=1/2,
  with common margin exactly 0;
  boundary-only, no strict reserve.

eps = 1/10:
  r=1/2 gives common strict margin 3/80 > 0.             (4.5)
```

The last case also shows that the crossover candidate is genuinely necessary.
At the individual vertex `r=1/4`, the second gate equals `-3/20<0`; at
`r=3/4`, the first gate equals `-3/20<0`.  Thus neither individual optimum is a
valid common witness, while the rational crossover is.

So the correct logic is

```text
separate one-gate PASS
  does NOT imply
shared-r PASS.                                          (4.6)
```

---

## 5. Boundary-only and obstruction interpretation

The five-candidate theorem also separates strict success from zero-reserve
contact.  In particular the family (4.1) at `eps=1/16` has a unique crossover
with common value zero.  Any widening that lowers either gate there destroys
shared feasibility immediately.

Therefore if a bundled consumer requires one fixed `r`, equality at the best
candidate must remain **boundary-only**; it cannot be promoted to strict decay.

Conversely, if all five strict candidate predicates fail, then no amount of
refining an `r` grid can repair the current same-curvature affine envelope.  A
successful next move must change the mathematical data: tighten `Eb/Eg`, tighten
the signed determinant envelope, split the source cell, or permit separate proof
parameters if the final semantics actually allow them.

---

## 6. Formalization targets

A small Lean sidecar can be organized around scalar lemmas only:

```text
same_curvature_difference_affine
```

Prove (1.3) by `ring`.

```text
same_curvature_vertex_square
```

Use the denominator-cleared form of (2.3), avoiding division in the core lemma.

```text
active_vertex1_of_polynomial_guard
active_vertex2_of_polynomial_guard
```

Transport (1.6)/(1.10) to the explicit rational vertices.

```text
crossover_inside_of_endpoint_sign_change
crossover_value_scaled
```

Prove (1.11)-(1.14).

```text
shared_positive_iff_five_candidates
```

State (2.1) over a linear ordered field.  The proof is a one-kink interval split;
no matrix API or square root is needed.

```text
p5_correlated_gate_difference
p5_shared_r_dominance_left
p5_shared_r_dominance_right
p5_shared_r_crossover
```

Specialize (3.6)-(3.15).

Regression theorems should include the three exact `eps` values in (4.5).

---

## 7. Scope boundary

This child is mathematically required **only if the final bundled P5 object must
freeze one and the same Pareto parameter `r` for the quarter and parameter gates**.
If the architecture permits the two logically separate consumers to invoke the
underlying Pareto-family theorem with separate `r` witnesses, then imposing a
shared-`r` gate would be an unnecessary strengthening and should not be done.

This review does not resolve that architecture/source-semantics question.  It
only supplies the exact mathematical closure once a shared `r` is required.

It also does not provide deployed source intervals, Float64/controller semantics,
flowpipe/domain coverage, Lean/kernel evidence, P5/P8/M4 closure, or registry
admission.

Status: **pending mathematical child**.