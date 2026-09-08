---
kind: review_result
review_id: review-T-P5-043-kuangmanmozun-20260907T2050
task_id: T-P5-043
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
claimed_at: 2026-09-07T20:30:00-06:00
created_at: 2026-09-07T20:50:00-06:00
claim_commit: ad17a318017005896e1a5df44b9f996e778b36a1
inspected_commit: 79a6b3b6061fa6cef969c85aef05a7f6c512ff70
inspected_paths:
  - agent_review_inbox/README.md
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/collaboration_board.md
  - agent_review_inbox/review-T-P5-041-liuguanyi-20260907T2020.md
  - agent_review_inbox/review-T-P5-042-guyuefangyuan-20260907T2041.md
  - agent_review_inbox/companion-T-P5-042-guyuefangyuan-20260907T2044.md
source_hashes:
  review-T-P5-041: a85bd01d469fe8d925db9d1331d861cfd6a854ab
  review-T-P5-042: 5f9bb0a204b6594740d3c67dce22c8d3f7282bf8
  companion-T-P5-042: 1871a3bd1d9e67832a16906ac5ea360f141109a8
continuation_of:
  - review-T-P5-041-liuguanyi-20260907T2020
  - review-T-P5-042-guyuefangyuan-20260907T2041
related_tasks:
  - T-P5-039
  - T-P5-040
  - T-P5-041
  - T-P5-042
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_or_checkerize_the_four_branch_direct_feasibility_gate_before_any_ell_or_rho_search; on_exact_FAIL_route_to_tighter_signed_or_correlated_source_bounds_instead_of_retuning_scalar_mixed_parameters
---

# T-P5-043 — exact radical-free **two-channel** centered-residual feasibility / obstruction gate

## 0. Result

T-P5-042 solves the one-channel tradeoff

```text
g_i(rho)
 := [ (R_i-rho)^2/m_i + C_i ] / (a_i-rho),

0 <= rho <= R_i,
rho < a_i,
a_i>0, m_i>0, R_i>=0, C_i>=0,                         (0.1)
```

and the centered P5 decay condition is

```text
g_4(rho4) + g_5(rho5) < L,                              (0.2)
```

where in the current Pareto family

```text
L = 2*c = (109-r)/100.                                  (0.3)
```

T-P5-042 already removes a `rho` grid once rational per-channel budgets
`ell4,ell5` are proposed.  The remaining question is more basic:

> **Before searching either `ell_i` or `rho_i`, is (0.2) mathematically
> feasible at all inside the independent two-channel mixed model?**

This review gives a complete exact answer.  Define, for each channel,

```text
d_i := a_i - R_i,
D_i := d_i^2 + m_i*C_i,
N_i := R_i^2 + m_i*C_i,
P_i := m_i*a_i > 0,
B_i := m_i*C_i - R_i*(2*a_i-R_i).                       (0.4)
```

Classify the channel as

```text
E_i  (endpoint-optimal) : B_i >= 0,
I_i  (interior/limit)   : B_i < 0.                      (0.5)
```

Then **exactly one** of the following four rational/polynomial gates decides
whether there exist admissible `rho4,rho5` satisfying (0.2).

### E/E gate

If `E_4` and `E_5`, feasibility is equivalent to

```text
N4*P5 + N5*P4 < L*P4*P5.                               (0.6)
```

### I/E gate

If `I_4` and `E_5`, define

```text
T4 := 2*P5*d4 + m4*(L*P5-N5).                           (0.7)
```

Then feasibility is equivalent to the two strict polynomial conditions

```text
T4 > 0,
4*P5^2*D4 < T4^2.                                       (0.8)
```

### E/I gate

If `E_4` and `I_5`, define

```text
T5 := 2*P4*d5 + m5*(L*P4-N4).                           (0.9)
```

Then feasibility is equivalent to

```text
T5 > 0,
4*P4^2*D5 < T5^2.                                      (0.10)
```

### I/I gate

If `I_4` and `I_5`, define

```text
T := L*m4*m5 + 2*m5*d4 + 2*m4*d5,                      (0.11)

S := T^2 - 4*m5^2*D4 - 4*m4^2*D5.                     (0.12)
```

Then feasibility is equivalent to

```text
T > 0,
S > 0,
S^2 > 64*m4^2*m5^2*D4*D5.                              (0.13)
```

There are **no square roots, divisions, eigenvalues, optimizers, grids, or
auxiliary `ell_i` variables in these final gates**.  With rational source rows
and rational `r`, every check is exact rational arithmetic; after denominators
are cleared it is purely polynomial.

Most importantly, this is an **obstruction gate**, not just another sufficient
bound:

```text
branch gate FAIL
  ==> no choice of rho4,rho5 can satisfy the centered scalar model (0.2).
```

Therefore an exact FAIL means that further `rho` tuning or `ell` search is
mathematically useless.  The next route must improve the source row / energy
reserve or leave the independent scalar-channel model, e.g. preserve more
signed Jacobian cancellation, use a correlated two-channel quadratic form, an
SPN/copositive split, or partition the source domain.

---

## 1. One-channel infimum in the two regimes

T-P5-042 proves that `rho=0` is globally optimal exactly when

```text
m*C >= R*(2*a-R).                                       (1.1)
```

Hence in the endpoint regime `E_i`,

```text
inf g_i = g_i(0)
        = (R_i^2+m_i*C_i)/(m_i*a_i)
        = N_i/P_i,                                      (1.2)
```

and the infimum is attained.

In the strict opposite regime `I_i`, T-P5-042 gives

```text
inf g_i
 = (2/m_i)*(sqrt(D_i)-d_i).                             (1.3)
```

If `D_i>0`, the minimizer is attained at

```text
rho_i* = a_i - sqrt(D_i).                               (1.4)
```

The only non-attained case is

```text
R_i=a_i,
C_i=0,
D_i=0.                                                  (1.5)
```

Then

```text
g_i(rho) = (a_i-rho)/m_i > 0,
inf g_i = 0,                                            (1.6)
```

as `rho -> a_i^-`.

This boundary does **not** break a strict feasibility theorem.  For independent
channels,

```text
exists rho4,rho5 : g4(rho4)+g5(rho5)<L

iff

inf g4 + inf g5 < L.                                    (1.7)
```

The forward direction is immediate.  In the reverse direction, attained
minima may be used directly; each degenerate channel (1.5) can be made
arbitrarily close to its zero infimum.  A positive strict gap in (1.7) pays
for that approximation.

Thus it is enough to eliminate the radicals in the sum of the two exact
infima.

---

## 2. Two elementary radical-elimination lemmas

### 2.1 One radical

For `X>=0`,

```text
sqrt(X) < T
```

is equivalent to

```text
T > 0,
X < T^2.                                                (2.1)
```

The sign condition is essential; squaring alone is unsound.

### 2.2 Sum of two radicals

Let

```text
A>0, B>0, X>=0, Y>=0,
S0 := T^2-A^2*X-B^2*Y.                                  (2.2)
```

Then

```text
A*sqrt(X) + B*sqrt(Y) < T                               (2.3)
```

is equivalent to

```text
T > 0,
S0 > 0,
S0^2 > 4*A^2*B^2*X*Y.                                  (2.4)
```

Proof: (2.3) first gives `T>0`.  Squaring once gives

```text
2*A*B*sqrt(X*Y) < S0,                                   (2.5)
```

so `S0>0`; squaring (2.5), now with both sides nonnegative, gives the last
condition in (2.4).  Conversely, the two sign conditions make the second
squaring reversible, hence

```text
(A*sqrt(X)+B*sqrt(Y))^2 < T^2,
```

and positivity of `T` recovers (2.3).

These two lemmas are the only algebra needed below.

---

## 3. Derivation of the four direct gates

### 3.1 E/E

Use (1.2) in both channels:

```text
N4/P4 + N5/P5 < L.                                      (3.1)
```

Since `P4,P5>0`, clearing denominators gives exactly (0.6).

### 3.2 I/E

Channel 4 contributes (1.3), channel 5 contributes `N5/P5`.  The target is

```text
(2/m4)*(sqrt(D4)-d4) + N5/P5 < L.                       (3.2)
```

Multiply by the positive `m4*P5` and rearrange:

```text
2*P5*sqrt(D4) <
  2*P5*d4 + m4*(L*P5-N5)
 = T4.                                                  (3.3)
```

Apply the one-radical lemma with `X=D4` and right side `T4/(2P5)`, or simply
square the already scaled form (3.3).  This gives exactly (0.8).

No extra check such as `L-N5/P5>0` is required: if the endpoint channel has
already consumed the entire target, (0.8) automatically fails.

### 3.3 E/I

This is symmetric and gives (0.9)-(0.10).

### 3.4 I/I

Use (1.3) twice:

```text
(2/m4)*(sqrt(D4)-d4)
+ (2/m5)*(sqrt(D5)-d5)
< L.                                                     (3.4)
```

Multiply by the positive `m4*m5` and move the rational shifts to the right:

```text
2*m5*sqrt(D4) + 2*m4*sqrt(D5) < T,                      (3.5)
```

where `T` is (0.11).  Apply the two-radical lemma with

```text
A=2*m5,
B=2*m4,
X=D4,
Y=D5.                                                   (3.6)
```

Its first post-square residual is exactly `S` from (0.12), and

```text
4*A^2*B^2*X*Y
 = 64*m4^2*m5^2*D4*D5.                                 (3.7)
```

Thus (0.13) is necessary and sufficient.

---

## 4. Why all three I/I sign/cross gates are necessary

It is unsafe to keep only the final squared polynomial.  Three exact examples
separate the roles.

### 4.1 Omitting `T>0` gives a false PASS

Take the generic radical problem

```text
A=B=1,
X=Y=1,
T=-3.                                                   (4.1)
```

Then

```text
S0 = 9-1-1 = 7 > 0,
S0^2 = 49 > 4,                                          (4.2)
```

but

```text
sqrt(1)+sqrt(1)=2 < -3                                  (4.3)
```

is impossible.  So the final square cannot encode the sign of the original
right side.

### 4.2 Omitting `S0>0` also gives a false PASS

Take

```text
A=B=1,
X=100,
Y=1,
T=1.                                                    (4.4)
```

Then `T>0`, but

```text
S0 = 1-100-1 = -100,
S0^2 = 10000 > 400 = 4*X*Y.                            (4.5)
```

The final squared inequality passes while the original statement

```text
10+1 < 1                                                (4.6)
```

is false.  The first-square residual must be explicitly positive.

### 4.3 Replacing the final strict `>` by `>=` admits boundary-only decay

Take

```text
A=B=1,
X=Y=1,
T=2.                                                    (4.7)
```

Then

```text
S0=2,
S0^2=4=4*X*Y,                                          (4.8)
```

and the radical sum is exactly `2`, not strictly below it.  Equality carries
zero decay reserve and must remain FAIL for the strict centered consumer.

Therefore all three signs in (0.13) are semantic, not checker decoration.

---

## 5. Exact rational I/I regression with a rational `rho` witness

Take two identical abstract channels

```text
a4=a5=1,
m4=m5=1,
R4=R5=1/2,
C4=C5=1/100,
L=1/20.                                                 (5.1)
```

Each channel is genuinely interior because

```text
B_i
 = 1/100 - (1/2)*(3/2)
 = -37/50 < 0.                                          (5.2)
```

Also

```text
d_i = 1/2,
D_i = 1/4+1/100 = 13/50.                                (5.3)
```

The direct I/I quantities are

```text
T = 1/20 + 1 + 1 = 41/20 > 0,                          (5.4)

S
 = (41/20)^2 - 8*(13/50)
 = 849/400 > 0.                                         (5.5)
```

The final cross margin is

```text
S^2 - 64*D4*D5
 = 28577/160000 > 0.                                    (5.6)
```

so the radical-free gate certifies strict feasibility.

A concrete rational witness, not needed by the gate but useful as a regression,
is

```text
rho4=rho5=49/100.                                       (5.7)
```

For each channel,

```text
g_i(49/100)
 = [ (1/100)^2 + 1/100 ] / (51/100)
 = 101/5100.                                            (5.8)
```

Hence

```text
g4+g5
 = 101/2550
 < 1/20,

1/20 - 101/2550
 = 53/5100 > 0.                                         (5.9)
```

So the direct gate is not merely detecting an irrational optimizer: it can
certify an open region containing exact rational `rho` witnesses.

---

## 6. Exact boundary-only I/I regression

Take instead

```text
a4=a5=m4=m5=1,
R4=R5=1/2,
C4=C5=11/100,
L=2/5.                                                  (6.1)
```

Now

```text
d_i=1/2,
D_i=1/4+11/100=9/25,
sqrt(D_i)=3/5,                                          (6.2)
```

and each channel remains interior because

```text
11/100 - 3/4 = -16/25 < 0.                              (6.3)
```

The exact channel infimum is

```text
inf g_i = 2*(3/5-1/2)=1/5,                              (6.4)
```

so the two-channel infimum is exactly `2/5=L`: there is no strict decay
margin.

The polynomial gate sees the same boundary without using the square root:

```text
T = 12/5,
S = 72/25,

S^2
 = 5184/625
 = 64*(9/25)^2.                                         (6.5)
```

Thus the last condition in (0.13) is equality, not strict `>`, and the gate
correctly returns **boundary-only FAIL**.

This is useful for interval/source widening: an equality certificate has zero
robustness and must not be promoted to a strict-decay witness.

---

## 7. Relationship to T-P5-042 rational budget constructors

This review does **not** replace the constructive `ell -> rho` interface from
T-P5-042.  It should sit immediately before it:

```text
real transformed source row
        |
        v
compute exact (a_i,m_i,R_i,C_i)
        |
        v
T-P5-043 direct four-branch feasibility gate
        |
        +-- FAIL --> exact scalar-model obstruction; tighten source / change model
        |
        `-- PASS --> search only for a rational open witness
                     (ell4,ell5), then use T-P5-042
                     vertex/endpoint constructors to emit rational rho_i
```

Why this is complete: a PASS says the sum of exact infima is strictly below
`L`.  Therefore there is an open positive margin.  Rational `ell_i` can be
chosen just above the infima with total still below `L`; equivalently, a dyadic
outward search using the T-P5-042 exact branch tests must eventually terminate.
No optimizer grid is needed, and a failed finite search can no longer be
confused with mathematical infeasibility because T-P5-043 decides that first.

Conversely, if T-P5-043 FAILs, **no** rational or irrational choices of
`ell_i/rho_i` can save the independent centered two-channel model.  Continuing
to tune those parameters is wasted work.

---

## 8. Recommended formal/checker surface

A small Lean/checker decomposition is enough.

### `sqrt_lt_iff_sq_with_sign`

For `X>=0`, prove

```text
sqrt X < T <-> 0<T and X<T^2.
```

If avoiding `Real.sqrt` entirely in the final theorem, use this only as an
internal proof lemma and expose the polynomial side.

### `weighted_two_sqrt_lt_iff_poly`

For `A,B>0`, `X,Y>=0`, define `S0=T^2-A^2*X-B^2*Y` and prove

```text
A*sqrt X + B*sqrt Y < T
<->
0<T and 0<S0 and 4*A^2*B^2*X*Y < S0^2.
```

### `channel_endpoint_or_interior_inf`

Package the T-P5-042 one-channel classification using

```text
B=m*C-R*(2*a-R).
```

The output should distinguish the attained endpoint branch from the
interior/degenerate-infimum branch.

### `two_channel_mixed_feasible_EE`
### `two_channel_mixed_feasible_IE`
### `two_channel_mixed_feasible_EI`
### `two_channel_mixed_feasible_II`

Expose exactly (0.6), (0.8), (0.10), and (0.13).  A checker can branch only on
the signs of `B4,B5` and then evaluate rational polynomials.

### `two_channel_mixed_direct_obstruction`

Corollary: failure of the active branch gate implies

```text
forall rho4 rho5,
  admissible rho4 -> admissible rho5 ->
  L <= g4(rho4)+g5(rho5).
```

This is the high-value theorem for routing failed source rows.

### regression theorems

Keep Sections 5 and 6 as exact arithmetic regressions, plus the three false
squaring examples from Section 4.  They guard precisely the sign conditions
most likely to be lost in a later checker refactor.

---

## 9. Assumptions and remaining boundary

This child assumes the T-P5-041/T-P5-042 independent channel abstraction is
already valid:

```text
a_i>0,
m_i>0,
R_i>=0,
C_i>=0,
```

with the centered residual represented by the corresponding `g_i`.

It does **not** prove or re-audit:

- the deployed signed Jacobian / `K_path` source row;
- that a state-independent anchor/FD/controller/solve bias is centered (it is
  not, in general; such terms remain additive);
- Julia/Float64 or true-DH semantics;
- flowpipe/domain coverage or ODE continuation;
- Lean compilation / `#print axioms` / source provenance;
- P5/P8/M4 closure or registry admission.

The direct gate is exact **only for the independent scalar two-channel mixed
model**.  A FAIL is not a physical impossibility theorem; it is a precise
certificate that this particular scalarization cannot close.  The mathematically
appropriate next escalation is then a tighter signed source enclosure,
correlated two-channel quadratic absorption, SPN/copositive structure, or a
domain partition — not more scalar `rho` tuning.

**Status: pending mathematical child — 待封不觉独立验证 / 待梁智炜最终整合。**
