---
kind: review_result
review_id: review-T-P5-035-guyuefangyuan-20260907T1728
task_id: T-P5-035
agent: 古月方源
source_agent: 古月方源
claimed_at: 2026-09-07T17:20:00-06:00
created_at: 2026-09-07T17:28:00-06:00
inspected_commit: 205fb1a54112cbbf19424a3a61500780b2ba0159
continuation_of:
  - review-T-P5-019-honglianmozun-20260907T0702
  - review-T-P5-034-honglianmozun-20260907T1701
related_reviews:
  - review-T-P5-031-guyuefangyuan-20260907T1224
  - review-T-P5-034-guyuefangyuan-20260907T1629
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_joint_Q_V_sum_metric_SOS_and_use_the_joint_residual_consumer_before_any_further_separate_constant_optimization
---

# T-P5-035 — joint `Q/V/residual-direction` certificate: `Q >= 27/50 V + 1/6 S`

## 0. Main result

For exactly the same frozen block-(4,5) storage `V`, dissipation `Q`, and residual direction used in `T-P5-019` and the newer `T-P5-034`, define

```text
S := ||x+y||^2
   = (x4+y4)^2 + (x5+y5)^2.
```

Instead of separately proving a strong coercivity bound `Q >= kV` and a separate residual metric `S <= C Q`, one can retain both pieces of `Q` simultaneously.  The exact rational joint inequality is

```text
Q >= (27/50) V + (1/6) S.                              (0.1)
```

This has a much larger downstream effect than another tiny improvement of the already-near-sharp `Q/V` constant.  With the exact derivative

```text
V' = -Q - (x+y)^T l,                                   (0.2)
```

and `||l||^2 <= L2`, the elementary square

```text
0 <= ||(x+y) - 3l||^2
```

gives

```text
|(x+y)^T l| <= (1/6)S + (3/2)L2.                       (0.3)
```

Combining (0.1)-(0.3) cancels the residual-direction reserve exactly:

```text
V' <= -(27/50)V + (3/2)L2.                             (0.4)
```

Hence the sharp checker-facing ratio delivered by this particular joint certificate is

```text
L2 < (9/25) V                                          (0.5)
```

at a barrier.  For the existing `Vstar=1/4`, this is simply

```text
100 L2 < 9.                                            (0.6)
```

For the existing incremental `Kc=1/12` tube with

```text
||Dl||^2 <= mu Vd + nu dc^2,
```

the new strict boundary gate is

```text
25 mu + 300 nu < 9.                                    (0.7)
```

Equivalently `mu + 12 nu < 9/25`.

The previous best separated consumer from `T-P5-034` had threshold

```text
mu + 12 nu < 75/272.
```

The new admissible threshold is larger by the exact factor

```text
(9/25)/(75/272) = 816/625 = 1.3056.                    (0.8)
```

So the improvement is **30.56%** with no new physical/source assumption.

---

## 1. Frozen quadratic forms

Use the same exact matrices as `T-P5-034`:

```text
M = diag(350003/3000000, 200739/4000000),
D = diag(4/5, 13/20),
K = [[3/4,    -3/400],
     [-3/400, 29/50]],
A = [[0, 1/400],
     [-1/400, 0]].
```

For `x=(x4,x5)` and `y=(y4,y5)`,

```text
V
 := (1/2)y^T M y
  + (1/2)x^T K x
  + x^T M y
  + (1/2)x^T D x,

Q
 := y^T(D-M)y + x^T K x - y^T A x,

S
 := (x4+y4)^2 + (x5+y5)^2.                             (1.1)
```

The derivative identity remains exactly

```text
V' = -Q - (x+y)^T l.                                   (1.2)
```

No source definition, coordinate convention, storage, or dynamics is changed by this child.

---

## 2. Exact nine-square proof of the joint lower bound

Set

```text
R := Q - (27/50)V - (1/6)S.                            (2.1)
```

Direct exact-rational expansion gives the following identity:

```text
R =
    (2964919/675000000)      x4^2
  + (856633/1350000000)      x5^2
  + (6647747/1200000000)     y4^2
  + (66610033/4800000000)    y5^2

  + (73/160000)              (12*x4 - x5)^2
  + (59450081/10800000000)   (4*x4 - 9*y4)^2
  + (1/38400)                (16*x4 + 3*y5)^2
  + (1/21600)                (x5 - 27*y4)^2
  + (216259859/43200000000)  (4*x5 - 9*y5)^2.          (2.2)
```

Every coefficient in (2.2) is strictly positive.  Therefore `R >= 0`, proving (0.1).

For an independent structural check, in coordinate order

```text
z = (x4,x5,y4,y5)
```

the symmetric matrix of `R` is

```text
[[ 989/6000,           -219/40000,          -59450081/300000000,        1/800 ],
 [ -219/40000,          2437/30000,         -1/800,                    -216259859/1200000000 ],
 [ -59450081/300000000,-1/800,               145549619/300000000,       0 ],
 [ 1/800,              -216259859/1200000000, 0,                         503518441/1200000000 ]].  (2.3)
```

The rational scaling vector

```text
d = (9/4, 27, 1, 12)                                  (2.4)
```

makes (2.3) strictly scaled diagonally dominant.  The four exact leftover diagonal margins after charging the five off-diagonal edge squares are

```text
2964919/675000000,
856633/1350000000,
6647747/1200000000,
66610033/4800000000,                                   (2.5)
```

which are precisely the first four coefficients of (2.2).  Thus (2.2) is not a floating PSD observation; it is an explicit rational SDD/SOS certificate.

---

## 3. Why the joint certificate beats the separated constants

`T-P5-034` separately supplies

```text
Q >= (15/16)V,                                         (3.1)
```

while `T-P5-019` separately supplies

```text
S <= (17/5)Q.                                          (3.2)
```

Using the standard half-`Q` Young split gives

```text
V' <= -(15/32)V + (17/10)L2,                           (3.3)
```

so the barrier ratio is

```text
(15/32)/(17/10) = 75/272 ~= 0.275735.                  (3.4)
```

The problem is not that either (3.1) or (3.2) is poor in isolation.  Both are already close to their separate optima.  The loss comes from demanding that the *same copy of `Q`* independently pay the full `V` coercivity and the full residual-direction metric, and then splitting it 50/50.

The joint certificate (0.1) allocates `Q` directly as

```text
Q = [at least (27/50)V] + [at least (1/6)S] + SOS slack.
```

That is the correct resource-allocation object for the derivative, because the residual work consumes `S`, not an abstract second copy of `Q`.

---

## 4. Exact residual absorption and ISS ledger

Let

```text
s := x+y.
```

For any residual `l`, Cauchy plus the elementary Young square gives

```text
s^T l <= |s^T l|
      <= (1/6)||s||^2 + (3/2)||l||^2.                 (4.1)
```

A division-free proof is obtained from

```text
0 <= ||s - 3l||^2
   = ||s||^2 - 6 s^T l + 9||l||^2.                   (4.2)
```

Therefore, if `||l||^2 <= L2`, then from (1.2) and (0.1),

```text
V'
 <= -Q + (1/6)S + (3/2)L2
 <= -(27/50)V + (3/2)L2.                              (4.3)
```

The corresponding constant-input ultimate coefficient is

```text
(3/2)/(27/50) = 25/9.                                  (4.4)
```

For comparison, the separated `T-P5-034` coefficient is `272/75`.  Their ratio is

```text
(25/9)/(272/75) = 625/816,                             (4.5)
```

so the ultimate residual floor coefficient is reduced by about 23.4%, equivalently the admissible barrier residual grows by the reciprocal factor `816/625`.

---

## 5. Direct product certificate and near-optimality obstruction

The joint quadratic bound also implies a clean quartic product bound.  Since `V>=0` and `S>=0`,

```text
Q >= (27/50)V + (1/6)S >= 0.
```

Using

```text
((27/50)V + (1/6)S)^2 - (9/25)V*S
  = ((27/50)V - (1/6)S)^2 >= 0,                       (5.1)
```

we obtain

```text
Q^2 >= (9/25) V S.                                    (5.2)
```

This explains the barrier ratio `9/25` directly: if `||l||^2 < (9/25)V`, then Cauchy gives residual work strictly smaller than `Q` at any nontrivial boundary point.

There is also a simple exact rational obstruction showing that further optimization of this *same frozen `V,Q,S` product route* has little room.  At

```text
z0 = (x4,x5,y4,y5) = (1/15, 1, 1/33, 7/16),           (5.3)
```

exact evaluation gives

```text
Q(z0) = 2334313183591/3345408000000,
V(z0) = 7192542100063/11151360000000,
S(z0) = 14467561/6969600.                              (5.4)
```

and

```text
91*V(z0)*S(z0) - 250*Q(z0)^2
 = 5314476251522753619407
   / 44767018745856000000000
 > 0.                                                   (5.5)
```

Hence the universal claim

```text
Q^2 >= (91/250) V S                                    (5.6)
```

is false.  If `k_joint^*` denotes the best universal product constant for these exact frozen forms, then

```text
9/25 <= k_joint^* < 91/250.                            (5.7)
```

The ratio between the obstruction and the certified value is only

```text
(91/250)/(9/25) = 91/90.                               (5.8)
```

Thus the present `9/25` certificate is within less than `1/90 ~= 1.11%` of this explicit upper obstruction.  This is a strong reason not to spend the next main mathematical lane shaving this constant; source residual bounds and same-domain coverage dominate the remaining uncertainty.

---

## 6. One-trajectory barrier

At a first-exit boundary `V=Vstar`, (4.3) is strictly inward whenever

```text
(3/2)L2 < (27/50)Vstar,
```

i.e.

```text
25 L2 < 9 Vstar.                                       (6.1)
```

For the existing quarter barrier `Vstar=1/4`, this reduces to

```text
100 L2 < 9.                                            (6.2)
```

The previous separated gate was

```text
1088 L2 < 75.                                          (6.3)
```

The new residual allowance is larger by exactly `816/625`.

As before, (6.2) is only a differential/barrier consumer.  It does not create the same-domain source bound `L2`, a nominal-domain margin, ODE continuation, or P8 coverage.

---

## 7. Incremental parameter tube

Reuse the source-facing incremental contract

```text
||Dl||^2 <= mu Vd + nu dc^2,
mu >= 0,
nu >= 0.                                               (7.1)
```

Applying (4.3) to the difference dynamics gives

```text
Vd'
 <= -[(27/50) - (3/2)mu] Vd
    + (3/2)nu dc^2.                                    (7.2)
```

On a boundary

```text
Vd = Kc dc^2,
```

strict inwardness is implied by

```text
(27 - 75 mu) Kc > 75 nu.                              (7.3)
```

For the existing `Kc=1/12`, this is

```text
25 mu + 300 nu < 9,                                   (7.4)
```

or equivalently

```text
mu + 12 nu < 9/25.                                    (7.5)
```

Compared with the latest separated gate

```text
272 mu + 3264 nu < 75,
```

the same linear combination `mu+12nu` is allowed to be larger by exactly `816/625`.

---

## 8. Updated source-gain discriminant for `T-P5-031`

If a future source bridge supplies the same nonnegative decomposition

```text
mu = U+p,
nu = W+q,
U,W,p,q >= 0,
p*q >= U*W,                                            (8.1)
```

then define

```text
R35 := 9 - 25U - 300W.                                 (8.2)
```

There exist nonnegative real slacks `p,q` with

```text
p*q >= U*W,
25p + 300q < R35                                       (8.3)
```

iff the strict scalar feasibility conditions hold:

```text
R35 > 0,
R35^2 > 30000 U W.                                     (8.4)
```

Necessity follows from

```text
(25p + 300q)^2 >= 4*25*300*p*q >= 30000 U W.
```

For sufficiency one may choose the usual balanced real slacks, but a checker need not introduce square roots: it can search rational `p,q` and verify (8.1) together with `25(U+p)+300(W+q)<9` directly.  Thus (8.4) is a fail-fast diagnostic, not a new trusted transcendental operation.

---

## 9. Lean-friendly theorem decomposition

The strongest minimal formalization is source-independent scalar algebra; no matrix eigensolver is needed.

Suggested atoms:

```lean
theorem block45_joint_Q_minus_V_S_sos
    (x4 x5 y4 y5 : R) :
    Q45 x4 x5 y4 y5
      - (27/50) * V45 x4 x5 y4 y5
      - (1/6) * ((x4+y4)^2 + (x5+y5)^2)
      = <the nine positive square terms in (2.2)> := by
  ring
```

```lean
theorem block45_joint_Q_lower
    (x4 x5 y4 y5 : R) :
    (27/50) * V45 x4 x5 y4 y5
      + (1/6) * ((x4+y4)^2 + (x5+y5)^2)
      <= Q45 x4 x5 y4 y5 := by
  rw [block45_joint_Q_minus_V_S_sos]
  positivity
```

```lean
theorem joint_residual_young
    (s4 s5 l4 l5 : R) :
    s4*l4 + s5*l5
      <= (1/6)*(s4^2+s5^2) + (3/2)*(l4^2+l5^2) := by
  nlinarith [sq_nonneg (s4-3*l4), sq_nonneg (s5-3*l5)]
```

```lean
theorem block45_joint_iss
    (hDeriv : dV <= -Q + work)
    (hQ : (27/50)*V + (1/6)*S <= Q)
    (hWork : work <= (1/6)*S + (3/2)*L2) :
    dV <= -(27/50)*V + (3/2)*L2 := by
  linarith
```

Then expose exact arithmetic corollaries

```text
100 L2 < 9,
25 mu + 300 nu < 9,
R35 > 0 and R35^2 > 30000 U W.
```

A separate regression theorem should encode (5.5), e.g.

```text
block45_joint_not_ge_91_250_at_z0
```

using exact rational `norm_num` after unfolding `V45,Q45,S45`.

---

## 10. Dependencies and non-claims

This child depends only on the already-frozen exact block-(4,5) forms and derivative identity from the P5 hypocoercive lane.  It does **not** supply or claim:

1. source residual/Jacobian bounds `L2`, `U`, `W`, `mu`, or `nu`;
2. Julia/Float64/libm/FD/linear-solve semantics;
3. true-DH equality or deployed controller equality;
4. nominal or actual P8 flowpipe coverage;
5. ODE existence/continuation or first-exit formalization;
6. provenance/receipt/admission/registry promotion;
7. full 6-DOF P5/M4 closure.

The result is source-independent mathematics only and must remain `pending` until the normal independent Lean/kernel and coordinator integration gates run.

## 11. Recommended next action

Formalize the nine-square identity (2.2) and the two-line residual Young consumer (4.1).  Downstream P5/P8 code should prefer the joint gate

```text
25 mu + 300 nu < 9
```

over further separate optimization of `Q >= kV` and `S <= C Q`.

After this child, the highest-value mathematics is no longer another global frozen-block constant: it is obtaining a genuine same-domain source incremental/anchor residual bound and checking it against the new joint gate.  The exact obstruction (5.5) shows that the same `V,Q,S` joint constant itself has less than ~1.11% remaining room before an explicit rational counterexample.
