---
kind: review_result
review_id: review-T-P5-037-honglianmozun-20260907T1856
task_id: T-P5-037
agent: 红莲魔尊
source_agent: 红莲魔尊
claimed_at: 2026-09-07T18:51:00-06:00
created_at: 2026-09-07T18:56:00-06:00
inspected_commit: 6c2ce166369319a73e70876020f4a175e08eaa71
inspected_paths:
  - agent_review_inbox/review-T-P5-035-honglianmozun-20260907T1801.md
  - agent_review_inbox/review-T-P5-019-honglianmozun-20260907T0702.md
  - agent_review_inbox/claim-T-P5-036-guyuefangyuan-20260907T1823.md
source_hashes:
  review-T-P5-035: d2bcf4cadc96cda18f2941a742dbd48412661349
  review-T-P5-019: 8f9d3f20992ab1d08a3bf01d6bc6d7bd7a419f41
continuation_of:
  - review-T-P5-035-honglianmozun-20260907T1801
  - review-T-P5-019-honglianmozun-20260907T0702
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_the_joint_Q_minus_one_sixth_sum_square_minus_109_over_200_V_SOS_and_use_the_direct_residual_completion_ledger_as_the_scalar_L2_consumer; keep_T-P5-036_componentwise_anisotropic_lane_disjoint
---

# T-P5-037 — coupled residual completion: a stronger scalar Lyapunov ledger without anisotropic residual budgets

## 0. Result

For the same frozen block-(4,5) storage `V`, dissipation `Q`, state vectors `x=(x4,x5)`, `y=(y4,y5)`, and residual `l` used in `T-P5-019` and `T-P5-035`, define

```text
s := x+y.
```

Instead of first proving a standalone coercivity `Q >= c V` and only afterwards spending half of `Q` to absorb `s^T l`, one can couple the two steps and prove the exact rational joint inequality

```text
Q - (1/6)||s||^2 >= (109/200)V.                        (0.1)
```

This yields the direct completion identity

```text
Q + s^T l + (3/2)||l||^2 - (109/200)V
 = [Q - (1/6)||s||^2 - (109/200)V]
   + (1/6)||s+3l||^2                                   (0.2)
```

and therefore, from the exact moving-frame energy identity `V'=-Q-s^T l`,

```text
V' <= -(109/200)V + (3/2)||l||^2.                      (0.3)
```

This is strictly stronger for the scalar `L2` lane than the separated `T-P5-035` ledger

```text
V' <= -(18797/40000)V + (17/10)||l||^2.                (0.4)
```

For the standard one-trajectory barrier `V*=1/4`, (0.3) gives the exact checker target

```text
1200 L2 < 109,                                          (0.5)
```

so the admissible scalar residual-square budget is

```text
L2 < 109/1200 ~= 0.09083333333.                         (0.6)
```

The previous `T-P5-035` threshold was `18797/272000 ~= 0.06910661765`; the new threshold is larger by the exact factor

```text
(109/1200)/(18797/272000) = 74120/56391
                           ~= 1.31439414.               (0.7)
```

Thus the scalar residual headroom increases by about **31.44%**, with no new source premise.

This child is deliberately disjoint from `T-P5-036`: 古月方源 has already claimed the componentwise anisotropic residual-metric lane.  Here the residual consumer remains the single isotropic scalar `||l||^2`; the improvement comes solely from completing the residual term jointly with the dissipation before collapsing `Q` to `V`.

---

## 1. Frozen exact forms and identity

Use exactly the forms frozen in `T-P5-035`:

```text
M = diag(350003/3000000, 200739/4000000),
D = diag(4/5, 13/20),
K = [[3/4,    -3/400],
     [-3/400, 29/50]],
A = [[0, 1/400],
     [-1/400, 0]].                                      (1.1)
```

For `x=(x4,x5)` and `y=(y4,y5)`,

```text
V
 := (1/2)y^T M y
  + (1/2)x^T K x
  + x^T M y
  + (1/2)x^T D x,                                      (1.2)

Q
 := y^T(D-M)y + x^T K x - y^T A x.                    (1.3)
```

The exact energy identity is unchanged:

```text
V' = -Q - (x+y)^T l.                                   (1.4)
```

Write

```text
S := ||x+y||^2
   = (x4+y4)^2 + (x5+y5)^2.                            (1.5)
```

The new mathematical target is not a stronger bare `Q/V` coercivity constant.  It is the joint Pareto point

```text
(a,lambda) = (1/6,109/200)                              (1.6)
```

for

```text
Q - a S >= lambda V.                                   (1.7)
```

---

## 2. Exact rational SOS certificate for `Q-(1/6)S-(109/200)V`

In coordinate order

```text
z=(x4,x5,y4,y5),
```

the symmetric matrix of

```text
R := Q - (1/6)S - (109/200)V                           (2.1)
```

is

```text
H_R =
[[ 3863/24000,             -873/160000,          -238150327/1200000000,    1/800 ],
 [ -873/160000,             9379/120000,          -1/800,                  -865641653/4800000000 ],
 [ -238150327/1200000000,  -1/800,                 193949491/400000000,      0 ],
 [ 1/800,                  -865641653/4800000000,   0,                       2013471547/4800000000 ]].  (2.2)
```

Choose the positive diagonal scaling

```text
d=(226,2738,100,1178).                                 (2.3)
```

The corresponding exact scaled-diagonal-dominance decomposition is

```text
R =
    (476041/904000000)           x4^2
  + (471636383/6571200000000)    x5^2
  + (127936699/60000000000)      y4^2
  + (96659113/1413600000000)     y5^2

  + (1195137/18080000)
      * (x4 - (113/1369)x5)^2

  + (238150327/2712000000)
      * (x4 - (113/50)y4)^2

  + (589/90400)
      * (x4 + (113/589)y5)^2

  + (1/21904)
      * (x5 - (1369/50)y4)^2

  + (509862933617/6571200000000)
      * (x5 - (1369/589)y5)^2.                         (2.4)
```

Every coefficient in (2.4) is strictly positive.  Expanding the four coordinate squares and five edge squares reproduces every diagonal and every nonzero off-diagonal entry of (2.2) exactly.  Hence

```text
Q - (1/6)||x+y||^2 - (109/200)V >= 0,                  (2.5)
```

which is (0.1).

No eigenvalue, matrix inverse, square root, floating PSD calculation, source table, or solver certificate is used by the proof.

---

## 3. Why the residual completion is especially Lean-friendly

For each coordinate, the Young remainder at `a=1/6` is itself an exact square:

```text
(1/6)s_i^2 + s_i*l_i + (3/2)l_i^2
 = (1/6)(s_i+3l_i)^2.                                  (3.1)
```

Summing the two channels gives

```text
(1/6)||s||^2 + s^T l + (3/2)||l||^2
 = (1/6)||s+3l||^2 >= 0.                               (3.2)
```

Adding (3.2) to (2.5) yields the exact direct SOS consumer

```text
Q + s^T l + (3/2)||l||^2 - (109/200)V >= 0.            (3.3)
```

Thus a formalization need not invoke a generic Cauchy/Young theorem or any square root.  It can expose (2.4), add two squares `(s4+3l4)^2`, `(s5+3l5)^2`, and finish with `ring` plus square nonnegativity.

Using (1.4), (3.3) immediately gives

```text
V' <= -(109/200)V + (3/2)||l||^2.                      (3.4)
```

The constant-residual ultimate coefficient is now

```text
(3/2)/(109/200) = 300/109 ~= 2.75229358,               (3.5)
```

versus `68000/18797 ~= 3.61759855` in `T-P5-035`.  The improvement factor is again `74120/56391`.

---

## 4. Exact nearby obstruction for the same `a=1/6` split

The clean coefficient `109/200=0.545` is close to the actual failure boundary for this fixed residual charge.  One may not round it up to

```text
1091/2000 = 0.5455.                                    (4.1)
```

At the exact rational state

```text
z1=(x4,x5,y4,y5)=(7/100, 1, 3/100, 43/100),            (4.2)
```

exact arithmetic gives

```text
Q(z1) - (1/6)||x+y||^2(z1) - (1091/2000)V(z1)
 = -6687143819/96000000000000
 < 0.                                                   (4.3)
```

Therefore

```text
Q - (1/6)||x+y||^2 >= (1091/2000)V                     (4.4)
```

is rigorously false.

This gives a useful local bracket for the fixed `a=1/6` design:

```text
109/200 is certified,
1091/2000 is false.                                     (4.5)
```

I do **not** claim `109/200` is the exact optimal generalized-eigenvalue constant, nor that `a=1/6` maximizes the entire continuous `(a,lambda)` Pareto frontier.  Its advantage is that it is both substantially stronger downstream and admits the very small rational square completion (3.1).

---

## 5. One-trajectory barrier update

Assume on the same domain

```text
||l||^2 <= L2.                                          (5.1)
```

From (3.4), on the first-exit boundary `V=1/4`,

```text
V' <= -109/800 + (3/2)L2.                              (5.2)
```

Strict inwardness follows from the division-free exact gate

```text
1200 L2 < 109.                                          (5.3)
```

Equivalently,

```text
L2 < 109/1200 ~= 0.09083333333.                        (5.4)
```

Compared with the previous `T-P5-035` gate

```text
272000 L2 < 18797,                                      (5.5)
```

the admissible scalar residual budget is multiplied by

```text
74120/56391 ~= 1.31439414.                              (5.6)
```

No change to the definition or source semantics of `L2` is implied.

---

## 6. Incremental ramp-parameter tube update

The same joint certificate applies to the difference variables of `T-P5-030`.  If the genuine incremental residual contract is

```text
||Dl||^2 <= mu Vd + nu dc^2,
mu >= 0,
nu >= 0,                                                (6.1)
```

then (3.4) gives

```text
Vd'
 <= -(109/200)Vd + (3/2)||Dl||^2
 <= [-(109/200)+(3/2)mu]Vd + (3/2)nu dc^2.             (6.2)
```

For a candidate tube boundary

```text
Vd = Kc dc^2,                                           (6.3)
```

strict inwardness is implied by

```text
(109 - 300 mu) Kc > 300 nu.                            (6.4)
```

For the existing `Kc=1/12`, the checker gate becomes

```text
300 mu + 3600 nu < 109,                                (6.5)
```

or

```text
mu + 12 nu < 109/300 ~= 0.3633333333.                  (6.6)
```

The previous `T-P5-035` threshold was `18797/68000 ~= 0.2764264706`; again the new admissible gain region expands along this scalar direction by the exact factor `74120/56391`.

As before, an absolute residual cap does not imply (6.1); the difference residual must vanish with state/parameter separation in the required sense.

---

## 7. Square-root-free physical-gain slack diagnostic

If the already separated source bridge supplies

```text
mu = U+p,
nu = W+q,
p,q,U,W >= 0,
pq >= UW,                                               (7.1)
```

set

```text
R109 := 109 - 300U - 3600W.                            (7.2)
```

There exist nonnegative `p,q` satisfying `pq>=UW` and the strict new gate

```text
300(U+p) + 3600(W+q) < 109                             (7.3)
```

iff the square-root-free conditions are

```text
R109 > 0,
R109^2 > 4320000 U W.                                  (7.4)
```

because

```text
4*300*3600 = 4320000.                                  (7.5)
```

As in earlier children, a checker may avoid square roots entirely by emitting explicit rational `p,q` and verifying (7.1) and (7.3).

---

## 8. Candidate theorem surface

A minimal source-independent formalization can be split into three algebraic theorems.

First:

```text
block45_Q_minus_one_sixth_sum_sq_minus_109_200_V_sos
```

states the exact equality (2.4).  Its proof should be only `ring`.

Second:

```text
block45_joint_dissipation_residual_coercivity
```

derives

```text
(109/200)V + (1/6)||x+y||^2 <= Q                       (8.1)
```

from the positive square coefficients.

Third:

```text
block45_direct_residual_completion
```

uses the exact identity

```text
(1/6)||s||^2 + s^T l + (3/2)||l||^2
 = (1/6)||s+3l||^2                                     (8.2)
```

to conclude

```text
(109/200)V <= Q + s^T l + (3/2)||l||^2.               (8.3)
```

A neighboring regression theorem should preserve the exact negative value (4.3) for the false `1091/2000` target.

This theorem family is smaller than a generic matrix generalized-eigenvalue API and remains independent of the componentwise anisotropic certificate being developed separately in `T-P5-036`.

---

## 9. Mathematical interpretation

The previous scalar pipeline was sequential:

```text
Q >= cV,
S <= kQ,
Young(S,l),
then discard half of Q.                                (9.1)
```

That ordering loses correlation information because the state directions that make `Q/V` small need not be the same directions that make `S/Q` large.  The new certificate instead asks the single quadratic question

```text
Q - aS >= lambda V                                    (9.2)
```

and only then completes the residual square.  This retains exactly the correlation between storage, dissipation, and the residual coupling direction `s=x+y`.

The choice `a=1/6` is especially useful because its dual residual charge `1/(4a)=3/2` has the exact integer square `(s+3l)^2/6`, while still permitting the strong exact coercivity `lambda=109/200`.

Thus the gain is structural, not a new source estimate and not a numerical optimization claim.

---

## 10. Assumptions, failure boundaries, and non-claims

1. Everything is for the frozen exact block-(4,5) `M,D,K,A` and coordinate convention of `T-P5-035`.
2. `T-P5-037` does not claim the globally optimal `(a,lambda)` Pareto point.  It certifies one simple rational point with a nearby exact failure witness for fixed `a=1/6`.
3. `1091/2000` is false for fixed `a=1/6` by (4.3); do not round the certified `109/200` upward without a new proof.
4. This child remains in the single isotropic `||l||^2` lane.  It does not duplicate or preempt `T-P5-036`'s componentwise anisotropic residual budgets.
5. The incremental tube still requires a genuine difference-residual estimate (6.1); an absolute `L2` envelope cannot replace it.
6. Source residual binding, Float64/solve semantics, P8 domain coverage, ODE continuation/first-exit existence, flowpipe inclusion, provenance, admission, registry promotion, and P5/P8/M4 parent closure remain untouched.
7. No Lean compilation or axiom receipt is claimed here.  The result is an exact-rational mathematical child ready for the separate formalization lane.

## 11. Requested integration action

For the scalar residual consumer, add the joint theorem

```text
Q - (1/6)||x+y||^2 >= (109/200)V
```

and consume it through the exact residual square completion to obtain

```text
V' <= -(109/200)V + (3/2)||l||^2.
```

Then update only the corresponding scalar arithmetic consumers to

```text
single V*=1/4 gate:        1200 L2 < 109,
incremental Kc=1/12 gate:  300 mu + 3600 nu < 109.
```

Keep `T-P5-036` as an independent componentwise anisotropic branch; downstream integration may later compare the scalar joint certificate against the anisotropic certificate and choose the stronger applicable source contract, but neither should be silently substituted for the other.

Keep this review `pending` until normal independent Lean/kernel and coordinator integration gates run.
