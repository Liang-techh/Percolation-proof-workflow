---
kind: review_result
review_id: review-T-P4-044-optimal-shifted-reserve-kuangmanmozun-20260907T1946
task_id: T-P4-044
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-07T19:46:00-06:00
inspected_commit: 4e92b49e71df1249fd23f0e1ec2c1024fb803496
claim_commit: 385a57f3a2a6c005ef1fc3957e87d63f7429cd76
inspected_paths:
  - agent_review_inbox/README.md
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/collaboration_board.md
  - agent_review_inbox/review-T-P4-040-divfree-liuguanyi-20260907T1816.md
  - agent_review_inbox/review-T-P4-043-midpoint-reserve-kuangmanmozun-20260907T1848.md
related_tasks:
  - T-P4-039
  - T-P4-040
  - T-P4-041
  - T-P4-043
integration_status: pending
admission_label: pending
proposed_integration_target: P4.common_lambda_interval_shifted_reserve
requested_action: keep T-P4-040 as the generic row consumer, but when a positive common rational interval is already certified and the midpoint Young charge fails, use the shifted rational witness and discriminant gate below; formalize the two polynomial identities and the sharp rational counterexample before any concrete source binding
---

# T-P4-044 — optimal shifted common-theta reserve from a verified public interval

## 0. Result

`T-P4-043` proved a sharp **midpoint** theorem: if every row is feasible at the same rational endpoints `a<b` and `A_i >= A0 > 0`, then the common midpoint has reserve `A0(b-a)^2/4`.  After a downstream Young charge `theta*m`, the midpoint condition is

```text
2(a+b)m <= A0(b-a)^2.                                    (0.1)
```

That condition is sharp **for the midpoint**, but the midpoint is generally not the best common theta once the cost itself is proportional to `theta`.

This child solves the remaining one-dimensional optimization exactly.

For every row write

```text
q_i(t) = A_i t^2 - G_i t + P_i.                          (0.2)
```

Assume one already-certified common rational interval

```text
0 < a < b,
0 < A0 <= A_i,
q_i(a) <= 0,
q_i(b) <= 0                                               (0.3)
```

for every row `i`.  Let `m >= 0` be the common downstream charge from the `T-P4-040` consumer, so the target is

```text
q_i(t) + m*t <= 0                                         (0.4)
```

for one shared `t>0`.

Define

```text
H_m := A0*(a+b) - m,
D_m := H_m^2 - 4*A0^2*a*b.                                (0.5)
```

If a rational witness `t_m` satisfies

```text
2*A0*t_m = H_m,                                           (0.6)
a <= t_m <= b,                                            (0.7)
D_m >= 0,                                                 (0.8)
```

then every row obeys the **uniform exact reserve**

```text
4*A0 * (q_i(t_m) + m*t_m) <= -D_m.                       (0.9)
```

Hence `D_m>0` gives a strict common post-charge reserve, while `D_m=0` is the exact boundary-only case for the worst allowed row.

For rational `a,b,A0,m`, the candidate `t_m=H_m/(2A0)` is rational.  The trusted semantic theorem need not divide: the checker can simply supply `t_m` and verify (0.6).

This is distinct from `T-P4-040`: that task gives the generic division-free **row consumer once a theta/radius certificate is supplied**.  The present child is an interval-level **shared-witness optimizer** that constructs a better common theta from the already-verified endpoint certificate.

---

## 1. Exact quadratic chord identity

For one row

```text
q(t)=A t^2-G t+P,
```

the exact interpolation identity is

```text
(b-a) q(t)
 = (b-t) q(a) + (t-a) q(b)
   - A (b-a)(t-a)(b-t).                                  (1.1)
```

This is a pure ring identity.

If

```text
a <= t <= b,
q(a) <= 0,
q(b) <= 0,
A >= A0 > 0,                                              (1.2)
```

then `(t-a)(b-t)>=0`, so

```text
q(t) <= -A (t-a)(b-t)
     <= -A0(t-a)(b-t).                                    (1.3)
```

Thus the whole row family is dominated by one universal worst-case parabola.  After the charge `m*t`, it suffices to make

```text
F_m(t) := A0(t-a)(b-t) - m*t >= 0.                       (1.4)
```

The key point is that this reduction uses only the public interval and the uniform curvature lower bound.  It does not inspect row roots, discriminants, source cells, or row-specific radii.

Suggested theorem name:

```text
quadratic_below_endpoint_chord
```

The polynomial identity is `ring`; the ordered consequence is `nlinarith` after the interval signs are supplied.

---

## 2. Completion identity for the shifted optimum

Write

```text
H := A0(a+b)-m,
D := H^2-4*A0^2*a*b.                                     (2.1)
```

Since

```text
F_m(t) = -A0*t^2 + H*t - A0*a*b,                         (2.2)
```

direct expansion gives the exact identity

```text
D - (2*A0*t-H)^2 = 4*A0*F_m(t).                          (2.3)
```

Again this is a pure ring identity.

Therefore any supplied rational `t_m` satisfying

```text
2*A0*t_m = H                                               (2.4)
```

obeys

```text
4*A0*F_m(t_m)=D.                                          (2.5)
```

Combining (1.3) with (2.5) gives, row by row,

```text
q_i(t_m)+m*t_m <= -F_m(t_m) = -D/(4*A0),                 (2.6)
```

or in the preferred division-free form

```text
4*A0*(q_i(t_m)+m*t_m) <= -D.                             (2.7)
```

Suggested theorem names:

```text
shifted_charge_complete_square
common_interval_shifted_reserve_mul
```

The second theorem should consume the affine relation `2*A0*t=H` rather than define `t=H/(2*A0)`.  This keeps the semantic theorem in multiplication-only form and leaves rational witness construction to a tiny adapter.

---

## 3. A square-root-free rational feasibility gate

For witness construction over `Q`, a cheap sufficient gate that selects the physically relevant small-charge branch is

```text
0 < a < b,
0 < A0,
0 <= m,
m <= A0*(b-a),
D_m >= 0.                                                 (3.1)
```

Set

```text
t_m = H_m/(2*A0).                                         (3.2)
```

The interval location follows without any square root:

From `m <= A0(b-a)`,

```text
H_m = A0(a+b)-m >= 2*A0*a,                               (3.3)
```

hence `t_m >= a`.

From `m>=0`,

```text
H_m <= A0(a+b),                                           (3.4)
```

so

```text
t_m <= (a+b)/2 < b.                                       (3.5)
```

Thus `a <= t_m < b`, and (2.7) applies.  If `D_m>0`, every row is strictly feasible after the charge.

The important implementation point is that no algebraic root of any row is needed.  The checker can store only the rational tuple

```text
(a,b,A0,m,t_m,D_m)
```

and verify polynomial inequalities plus the single affine equality (0.6).

### Why `D_m >= 0` alone is NOT a safe gate

The quadratic `D_m` has two branches.  A large `m` can make `D_m` positive again while the maximizing vertex has moved to negative `t`.

Take

```text
a=1, b=4, A0=1, m=10.                                    (3.6)
```

Then

```text
H_m = -5,
D_m = 25-16 = 9 > 0,                                     (3.7)
```

but

```text
t_m = -5/2                                                (3.8)
```

is outside the positive common interval.  For the extremal row

```text
q(t)=(t-1)(t-4),                                          (3.9)
```

we have

```text
q(t)+10t = t^2+5t+4 = (t+1)(t+4) > 0                    (3.10)
```

for every `t in [1,4]`.

Therefore a checker that records only `D_m>=0` is unsound.  It must also select the small-charge branch, for example by (3.1), or directly verify `a<=t_m<=b`.

---

## 4. Sharpness in the endpoint-plus-curvature information class

The universal envelope (1.3) is attained by the single row

```text
q_*(t)=A0(t-a)(t-b).                                      (4.1)
```

Indeed

```text
q_*(a)=q_*(b)=0,
curvature coefficient = A0.                              (4.2)
```

For this extremal row,

```text
q_*(t)+m*t
 = A0*t^2 - H_m*t + A0*a*b.                              (4.3)
```

Its discriminant is exactly `D_m`.

Therefore:

- if `D_m<0`, then `q_*(t)+m*t>0` for every real `t`; no common witness exists even for this one allowed row;
- if `D_m=0` on the small-charge branch, the unique witness is `t_m=H_m/(2A0)` and the post-charge reserve is exactly zero;
- if `D_m>0` on the small-charge branch, the shifted witness has positive reserve `D_m/(4A0)`.

Hence the gate is not merely sufficient: **it is sharp for what can be guaranteed from only common endpoint feasibility and the lower curvature bound.**  A concrete row family may of course permit a larger charge because its endpoint values can be strictly negative or its curvatures larger; this child does not claim otherwise.

Over the reals, solving `D_m=0` gives the information-class sharp ceiling

```text
m_sharp = A0*(sqrt(b)-sqrt(a))^2.                         (4.4)
```

This square-root formula is explanatory only.  The trusted rational certificate can stay with `D_m`.

---

## 5. The midpoint is strictly suboptimal for positive width

`T-P4-043` midpoint charging allows

```text
m_mid = A0*(b-a)^2 / (2*(a+b)).                          (5.1)
```

For `0<a<b`, the sharp shifted ceiling satisfies

```text
m_sharp - m_mid
 = A0*(a+b-2*sqrt(a*b))^2 / (2*(a+b))
 > 0.                                                      (5.2)
```

Thus midpoint synthesis is optimal for the **unweighted reserve** `q(t)` but not for the **theta-weighted charge** `q(t)+m*t`: charging penalizes larger theta, so the optimizer shifts left from `(a+b)/2`.

This distinction is easy to miss because both arguments start from the same public interval.

---

## 6. Exact rational counterexample: midpoint FAIL, shifted witness PASS

Use the extremal rational row

```text
q(t)=(t-1)(t-4),
a=1,
b=4,
A0=1.                                                      (6.1)
```

Choose

```text
m=19/20.                                                   (6.2)
```

### Midpoint

The common midpoint is

```text
theta_mid = 5/2.                                          (6.3)
```

Then exactly

```text
q(5/2) + (19/20)(5/2) = 1/8 > 0.                        (6.4)
```

So the `T-P4-043` midpoint charge test fails.

### Shifted rational witness

Now

```text
H_m = 5-19/20 = 81/20,
t_m = H_m/2 = 81/40,                                     (6.5)
D_m = (81/20)^2 - 16 = 161/400 > 0.                     (6.6)
```

At this rational witness,

```text
q(81/40) + (19/20)(81/40)
 = -161/1600 < 0.                                         (6.7)
```

So the same exact public interval that cannot pay `m=19/20` at its midpoint can pay it with a strict rational reserve after shifting theta.

This is a concrete reason to add the child rather than simply keep the midpoint theorem.

---

## 7. Exact boundary and impossibility example

With the same row and interval, take

```text
m=1.                                                       (7.1)
```

Then

```text
H=4,
D=0,
t_m=2,                                                    (7.2)
```

and the charged polynomial factorizes as

```text
q(t)+t = (t-2)^2.                                         (7.3)
```

Thus `t=2` is the unique boundary-only witness and has zero reserve.

For any `m>1` and any positive `t`,

```text
q(t)+m*t
 = (t-2)^2 + (m-1)t
 > 0.                                                      (7.4)
```

Hence no positive theta can work.  This gives an entirely rational sharp obstruction at the true charge ceiling for this interval.

It also shows why `D=0` must not be fed into a consumer that assumes a positive reserve: equality is a genuine closure boundary, not numerical slack.

---

## 8. Lean-friendly theorem surface

A minimal formalization can be split into four tiny lemmas.

### 8.1 Chord identity

```text
quadratic_chord_identity
```

Statement over a commutative ring:

```text
(b-a)*(A*t^2-G*t+P)
 = (b-t)*(A*a^2-G*a+P)
   + (t-a)*(A*b^2-G*b+P)
   - A*(b-a)*(t-a)*(b-t).
```

Proof: `ring`.

### 8.2 Shifted completion

```text
shifted_charge_complete_square
```

With `H=A0*(a+b)-m`, `D=H^2-4*A0^2*a*b`:

```text
D - (2*A0*t-H)^2
 = 4*A0*(A0*(t-a)*(b-t)-m*t).
```

Proof: `ring`.

### 8.3 Common interval consumer

```text
common_interval_shifted_reserve_mul
```

Over a linear ordered field, assume

```text
0 < A0,
a <= t, t <= b,
A0 <= A_i,
q_i(a)<=0, q_i(b)<=0,
2*A0*t = H.
```

Then

```text
4*A0*(q_i(t)+m*t) <= -D.
```

If additionally `D>=0`, conclude `q_i(t)+m*t<=0`; if `D>0`, conclude strict negativity.

No square root is needed.

### 8.4 Rational witness constructor / checker lemma

```text
shifted_witness_mem_interval
```

Assume

```text
0<a<b,
0<A0,
0<=m,
m<=A0*(b-a),
2*A0*t=A0*(a+b)-m.
```

Then

```text
a<=t and t<b.
```

This lets a `Rat` checker emit `t` by ordinary rational division and lets the semantic theorem verify only the multiplication equality.

### Optional exact regression lemmas

```text
midpoint_fails_shifted_passes_1_4_19_20
shifted_boundary_1_4_1
large_discriminant_wrong_branch_counterexample
```

All three are exact rational `norm_num` / `ring_nf` targets.

---

## 9. Integration advice

The safe common-parameter pipeline can now be sharpened to

```text
strict real overlap / search
  -> propose rational common interval [a,b]
  -> exact endpoint checks for every row
  -> if no downstream theta-weighted charge: midpoint theorem T-P4-043
  -> if charge m is material:
       compute rational shifted t_m,
       verify small-branch / interval membership,
       verify D_m>=0,
       consume common shifted reserve
  -> feed one shared theta into T-P4-040 / T-P4-038 semantic consumer.
```

The shifted theorem should **not** replace T-P4-040.  It is only a witness synthesizer / interval-level reserve compressor.  T-P4-040 remains the generic trusted row algebra.

If the shifted certificate fails, the correct conclusion is also limited:

- `D_m<0` gives a genuine obstruction for what can be guaranteed from the endpoint-plus-`A0` information class, witnessed by `q_*`;
- it does **not** prove the actual concrete row family is infeasible, because actual endpoints may carry additional negative slack;
- `D_m>=0` on the wrong large-charge branch is not a PASS unless positive interval membership of `t_m` is separately established.

---

## 10. Status / next step

Status: **pending mathematical child**.

This review does not claim:

- any concrete Route-B cell has supplied `a,b,A0,m`;
- source binding or `DHProducerBaseBridge` is closed;
- Float64 / true-DH realization is covered;
- P8 cell coverage is complete;
- P4/M4 or registry/admission status changes.

The next smallest formal step is the pair of `ring` identities plus the exact rational regression `(a,b,A0,m)=(1,4,1,19/20)`.  After that, a concrete checker may use this child only when it already has the common endpoint certificate required by T-P4-043.