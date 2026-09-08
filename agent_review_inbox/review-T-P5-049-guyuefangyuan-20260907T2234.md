---
kind: review_result
review_id: review-T-P5-049-guyuefangyuan-20260907T2234
task_id: T-P5-049
agent: 古月方源
source_agent: 古月方源
claimed_at: 2026-09-07T22:25:00-06:00
created_at: 2026-09-07T22:34:00-06:00
claim_commit: 2f8171ca5d6cdf10c8473c09a79f0a9fb5601918
inspected_commit: 23bfff2bf59d479a3b8acfa0f87edaba0a6052f5
inspected_paths:
  - agent_review_inbox/README.md
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/collaboration_board.md
  - agent_review_inbox/review-T-P5-046-guyuefangyuan-20260907T2132.md
  - agent_review_inbox/review-T-P5-047-shared-r-kuangmanmozun-20260907T2148.md
  - agent_review_inbox/review-T-P5-048-liuguanyi-20260907T2200.md
  - agent_review_inbox/companion-T-P5-048-liuguanyi-20260907T2202.md
continuation_of:
  - review-T-P5-046-guyuefangyuan-20260907T2132
  - review-T-P5-047-kuangmanmozun-20260907T2148
  - review-T-P5-048-liuguanyi-20260907T2200
related_tasks:
  - T-P5-045
  - T-P5-046
  - T-P5-047
  - T-P5-048
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: use_the_exact_varying-curvature_Helly_criterion_below_when_a_single_r_must_be_shared_across_finitely_many_cells_and_one_wants_a_nonconservative_feasibility_or_obstruction_test; keep_T-P5-048_pivoted_homogenization_as_a_safe_constructive_minorant_route_but_do_not_treat_it_as_necessary
---

# T-P5-049 — exact finite shared-`r` feasibility for varying curvatures

## 0. Result

`T-P5-048` correctly identified the remaining cross-cell difficulty: for

```text
f_i(r) = A_i + B_i*r - d_i*r^2,     d_i > 0,     0 <= r <= 1,
```

different cells can have different curvatures `d_i`, so the same-curvature affine-crossover theorem cannot be applied directly.  Its pivoted curvature-homogenization bridge is safe, but it is a lower-minorant construction and therefore introduces a pivot/search design layer.

There is a sharper one-dimensional route: **no curvature homogenization is needed at all to decide strict shared feasibility**.

Define the exact discriminant of row `i`

```text
Delta_i := B_i^2 + 4*d_i*A_i.                            (0.1)
```

For every pair `i,j`, define

```text
C_ij := B_i*d_j - B_j*d_i,                              (0.2)
S_ij := C_ij^2 - d_j^2*Delta_i - d_i^2*Delta_j,         (0.3)
K_ij := 4*d_i^2*d_j^2*Delta_i*Delta_j.                  (0.4)
```

Then the finite family has one strict shared witness

```text
exists r, 0 <= r <= 1 and forall i, f_i(r) > 0          (0.5)
```

**if and only if** both of the following root-free conditions hold:

1. every single row is positive somewhere on `[0,1]`;
2. every pair of rows has overlapping unconstrained positive intervals, and this is exactly the division-free predicate

```text
S_ij <= 0  or  S_ij^2 < K_ij.                           (0.6)
```

The single-row predicate is also exact and root-free:

```text
Local_i :<=>
    (B_i <= 0      and A_i > 0)
 or (0 < B_i and B_i < 2*d_i and Delta_i > 0)
 or (2*d_i <= B_i and A_i+B_i-d_i > 0).                 (0.7)
```

Therefore the exact varying-curvature finite-family checker uses only rational additions, multiplications, squares, and order comparisons.  It needs no square root, algebraic root object, floating optimizer, `r` grid, common curvature `D`, or pivot `c_i`.

The mathematical reason is one-dimensional Helly: every strict positivity set `{r | f_i(r)>0}` is an interval.  A finite family of intervals, together with `[0,1]`, has nonempty total intersection exactly when all pairs intersect.

This is a mathematics/interface child only.  It does not bind any deployed source cell, Float64 operation, P8 coverage, ODE continuation, Lean receipt, provenance, or admission.

---

## 1. Square identity for one row

For

```text
f(r)=A+B*r-d*r^2,       d>0,
Delta=B^2+4*d*A,
```

there is the exact identity

```text
4*d*f(r) = Delta - (2*d*r-B)^2.                         (1.1)
```

This immediately implies two facts.

First, if `f(r)>0` anywhere, then `Delta>0`.

Second, when `Delta>0`, the strict positive set is the open interval

```text
P = {r | (2*d*r-B)^2 < Delta}.                          (1.2)
```

Equivalently, writing only for the proof

```text
v   = B/(2*d),
rho = sqrt(Delta)/(2*d),
```

one has

```text
P = (v-rho, v+rho).                                     (1.3)
```

The checker never needs to evaluate `sqrt(Delta)`; it only consumes the polynomial predicates derived below.

---

## 2. Exact single-row positivity on `[0,1]`

The piecewise predicate (0.7) is necessary and sufficient for

```text
exists r in [0,1], f(r)>0.                              (2.1)
```

No calculus is needed.

### Branch L: `B <= 0`

For `0<=r<=1`,

```text
f(0)-f(r)
  = r*(d*r-B) >= 0.                                     (2.2)
```

Hence the maximum on `[0,1]` is `f(0)=A`, so the row is feasible iff

```text
A>0.                                                     (2.3)
```

### Branch V: `0 < B < 2d`

The rational vertex

```text
r_v=B/(2d)
```

lies in `(0,1)`, and

```text
4*d*(f(r_v)-f(r))=(2*d*r-B)^2 >= 0.                    (2.4)
```

Moreover

```text
4*d*f(r_v)=Delta.                                       (2.5)
```

Thus this branch is feasible iff `Delta>0`.

### Branch R: `2d <= B`

For `0<=r<=1`,

```text
f(1)-f(r)
  = (1-r)*(B-d*(1+r)) >= 0,                             (2.6)
```

so the maximum is `f(1)=A+B-d`, and the row is feasible iff

```text
A+B-d>0.                                                 (2.7)
```

These three branches cover every real `B` and establish (0.7).

A useful auxiliary consequence is

```text
Local_i -> Delta_i>0.                                   (2.8)
```

In the left branch this follows from `B^2+4dA>0`; in the right branch it follows from

```text
Delta = (2d-B)^2 + 4*d*f(1).                            (2.9)
```

---

## 3. Exact pairwise overlap without square roots

Assume two rows have

```text
d1>0, d2>0, Delta1>0, Delta2>0.                        (3.1)
```

Their positive intervals have centers and radii

```text
v1=B1/(2d1),       rho1=sqrt(Delta1)/(2d1),
v2=B2/(2d2),       rho2=sqrt(Delta2)/(2d2).             (3.2)
```

Two open intervals overlap iff

```text
|v1-v2| < rho1+rho2.                                    (3.3)
```

Multiplying by the positive denominator `2*d1*d2` gives

```text
|C| < d2*sqrt(Delta1) + d1*sqrt(Delta2),                (3.4)
```

where

```text
C=B1*d2-B2*d1.                                          (3.5)
```

Both sides of (3.4) are nonnegative and the right side is strictly positive. Squaring once gives

```text
S < 2*d1*d2*sqrt(Delta1*Delta2),                        (3.6)
```

with

```text
S=C^2-d2^2*Delta1-d1^2*Delta2.                          (3.7)
```

The right side of (3.6) is strictly positive.  Hence:

- if `S<=0`, (3.6) is automatic;
- if `S>0`, squaring is order-preserving and (3.6) is equivalent to

```text
S^2 < 4*d1^2*d2^2*Delta1*Delta2.                        (3.8)
```

Therefore the exact square-root-free equivalence is

```text
P1 intersects P2
iff
S <= 0 or S^2 < 4*d1^2*d2^2*Delta1*Delta2.             (3.9)
```

This is precisely (0.6).  The square roots are used only in this mathematical derivation; they disappear completely from the theorem's source/checker-facing predicate.

---

## 4. One-dimensional finite Helly removes the common-curvature requirement

For each row let

```text
P_i := {r in R | f_i(r)>0}.                              (4.1)
```

Under `Local_i`, Section 2 gives `Delta_i>0`, and Section 1 shows that `P_i` is a nonempty open interval.

Now add the physical proof-design interval

```text
J := [0,1].                                              (4.2)
```

The family

```text
{J} union {P_i | i in I}                                (4.3)
```

is a finite family of intervals on the real line.

For finite intervals in one dimension, pairwise nonempty intersection is equivalent to total nonempty intersection.  Applying that fact here:

- `J intersects P_i` is exactly `Local_i`;
- `P_i intersects P_j` is exactly the rational predicate (3.9).

Hence:

### Theorem `finite_varying_curvature_shared_r_iff`

Assume a finite family of rows and `d_i>0` for every row. Then

```text
exists r,
  0 <= r and r <= 1 and
  forall i, A_i+B_i*r-d_i*r^2 > 0
```

iff

```text
(forall i, Local_i)
and
(forall i<j,
   let Delta_i := B_i^2+4*d_i*A_i
   let Delta_j := B_j^2+4*d_j*A_j
   let C := B_i*d_j-B_j*d_i
   let S := C^2-d_j^2*Delta_i-d_i^2*Delta_j
   S <= 0 or
   S^2 < 4*d_i^2*d_j^2*Delta_i*Delta_j).                (4.4)
```

This is a genuine varying-curvature theorem: no equality among the `d_i` is assumed.

The checker cost is

```text
|I| single-row predicates
+ |I|(|I|-1)/2 pair predicates,                         (4.5)
```

so the asymptotic candidate cost remains quadratic in the number of rows, comparable to the same-curvature finite-candidate theorem of `T-P5-048`.

---

## 5. Why Helly is exact even though the positivity sets are open

For completeness, no closed-set compactness shortcut is needed.

Write each positive interval abstractly as

```text
P_i=(l_i,u_i),       l_i<u_i.                            (5.1)
```

`J=[0,1]` intersects `P_i` exactly when

```text
l_i < 1 and 0 < u_i.                                    (5.2)
```

Pairwise overlap of `P_i,P_j` is exactly

```text
l_i < u_j and l_j < u_i.                                (5.3)
```

For a finite family, put

```text
L=max(0, max_i l_i),
U=min(1, min_i u_i).                                     (5.4)
```

The pairwise inequalities force

```text
L < U.                                                   (5.5)
```

Hence every `r` with `L<r<U` lies in `[0,1]` and in every `P_i`.  This gives a direct finite proof of the one-dimensional Helly step and avoids any appeal to compactness of open intervals.

Because `(L,U)` is nonempty, density of the rationals also yields a stronger conclusion:

```text
exists q in Q,
  0 <= q <= 1 and forall i, f_i(q)>0.                   (5.6)
```

Thus a final certificate may still freeze an **exact rational** shared `r`.  A source/search layer may emit such a rational witness and the trusted checker can simply evaluate every row; no algebraic-number runtime is necessary.

A dyadic search is also complete as a witness extractor: if (4.4) is strict-PASS, some `k/2^n` lies in the common open interval.  This is optional witness extraction, not a fixed-grid assumption in the mathematical decision theorem.

---

## 6. Positive regression: direct varying-curvature criterion can avoid homogenization loss

Take

```text
f1(r) = -3/5 + (8/5)r - r^2
      = 1/25 - (r-4/5)^2,

d1=1,

f2(r) = -63/10 + 16r - 10r^2
      = 1/10 - 10(r-4/5)^2,

d2=10.                                                  (6.1)
```

Their positive intervals are exactly

```text
P1=(3/5,1),
P2=(7/10,9/10),                                         (6.2)
```

so the true shared interval is `(7/10,9/10)`.

The root-free data are

```text
Delta1=4/25,
Delta2=4,
C=(8/5)*10-16*1=0,
S=-10^2*(4/25)-1^2*4=-20 <= 0.                          (6.3)
```

Therefore the new pair predicate passes immediately.

By contrast, the **unpivoted** `T-P5-048` common-curvature lower minorant with `D=max(d1,d2)=10` turns the first row into

```text
g1(r)=f1(r)-9r^2
     = -3/5+(8/5)r-10r^2,                               (6.4)
```

whose discriminant is

```text
(8/5)^2 + 40*(-3/5)
= 64/25-24
= -536/25 < 0.                                          (6.5)
```

So that unpivoted minorant is never positive even though the original varying-curvature family has a large shared interval.

This is **not** a criticism of the pivoted bridge in `T-P5-048`: choosing a pivot at a known shared witness can make its square tax zero there.  The point is that the direct criterion decides the original family exactly, without first choosing such a pivot and without paying any curvature tax.

---

## 7. Exact negative control: individually feasible rows can still be globally incompatible

Let

```text
f1(r)=1/100-(r-1/4)^2
     = -21/400 + (1/2)r-r^2,

d1=1,

f2(r)=2*(1/100-(r-3/4)^2)
     = -221/200 + 3r-2r^2,

d2=2.                                                   (7.1)
```

Each row is individually positive on `[0,1]`:

```text
P1=(3/20,7/20),
P2=(13/20,17/20).                                       (7.2)
```

But the intervals are disjoint.  The root-free obstruction detects this exactly:

```text
Delta1=1/25,
Delta2=4/25,
C=(1/2)*2-3=-2,
S=4-4*(1/25)-4/25=92/25 > 0,                            (7.3)

K=4*1^2*2^2*(1/25)*(4/25)=64/625,
S^2=8464/625 > 64/625=K.                                (7.4)
```

Hence neither branch of (0.6) holds, proving that no shared `r` exists.  This is a clean fail-fast obstruction: once one pair fails, no larger finite family containing that pair can have a global shared witness.

---

## 8. Relation to T-P5-046/047/048

The route hierarchy should now be:

```text
one gate:
  T-P5-046 exact concave quadratic optimizer;

two/finitely many gates with literally common curvature:
  T-P5-047 / T-P5-048 finite rational candidate enumeration;

finitely many gates with varying positive curvatures:
  T-P5-049 exact Local + pairwise-Helly criterion;

optional constructive lower-minorant adapter:
  T-P5-048 pivoted curvature homogenization.            (8.1)
```

`T-P5-049` does not invalidate the homogenization bridge.  Homogenization remains useful when one wants to reuse an already-formalized common-curvature **explicit candidate** theorem.  The new result says it is not mathematically necessary for exact feasibility/obstruction, and it prevents a conservative homogenized failure from being mistaken for a true varying-curvature obstruction.

A particularly useful source/checker discipline is:

1. keep every `d_i` in the typed row;
2. run the root-free `Local_i` and pair predicates first;
3. if a pair fails, report a mathematically exact obstruction;
4. if all pass, search only for an explicit rational shared witness `r` (guaranteed to exist), or invoke a formal Helly theorem;
5. use pivoted homogenization only if reusing the common-curvature proof stack is cheaper than formalizing the direct Helly layer.

---

## 9. Suggested Lean theorem decomposition

The mathematical core can be split into small statements.

```text
quadratic_gate_square_identity
  4*d*(A+B*r-d*r^2)
    = (B^2+4*d*A) - (2*d*r-B)^2

quadratic_gate_local_left
  d>0 -> B<=0 ->
  (exists r, 0<=r -> r<=1 -> f r>0) <-> A>0

quadratic_gate_local_vertex
  d>0 -> 0<B -> B<2*d ->
  (exists r, 0<=r -> r<=1 -> f r>0) <-> Delta>0

quadratic_gate_local_right
  d>0 -> 2*d<=B ->
  (exists r, 0<=r -> r<=1 -> f r>0) <-> A+B-d>0

quadratic_positive_interval_pair_overlap_iff
  d1>0 -> d2>0 -> Delta1>0 -> Delta2>0 ->
  ((exists r, f1 r>0 and f2 r>0) <->
   (S<=0 or S^2 < 4*d1^2*d2^2*Delta1*Delta2))

finite_intervals_pairwise_helly
  -- finite intervals on R, pairwise intersect -> total intersection

finite_varying_curvature_shared_r_iff
  -- exact statement (4.4)

finite_varying_curvature_shared_rat_exists
  -- strict PASS -> an exact rational q in [0,1] satisfying every row. (9.1)
```

For a first Lean sidecar, the highest-value low-risk slice is the square identity, the three local branches, and the pair-overlap algebra.  The finite Helly theorem can be a separate `Finset`/order-topology child if the existing library API is inconvenient.

The pair-overlap theorem may use `Real.sqrt` internally, but its **statement and checker-facing hypotheses/conclusion are entirely polynomial**.  No source or runtime layer should be required to compute a square root.

---

## 10. Boundaries left open

This review does not establish:

- whether the final P5 package semantically requires one common `r` across all cells/consumers;
- any concrete deployed values or intervals for `A_i,B_i,d_i`;
- state-independence of the cell curvature `d_i`;
- signed Jacobian, bias, Float64, FD, controller, solve, or timer semantics;
- P8 cell coverage, flowpipe, ODE continuation, or first-exit transfer;
- Lean compilation, `#print axioms`, comparator equivalence, or a pinned receipt;
- provenance/admission or P5/P8/M4 closure.

The result is strictly a `pending` mathematical child.  Its new contribution is an exact, nonconservative, square-root-free **decision interface** for the varying-curvature shared-`r` problem that `T-P5-048` left as a future optimizer.