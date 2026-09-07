---
kind: review_result
review_id: review-T-P5-034-honglianmozun-20260907T1701
task_id: T-P5-034
agent: 红莲魔尊
source_agent: 红莲魔尊
claimed_at: 2026-09-07T16:54:00-06:00
created_at: 2026-09-07T17:01:00-06:00
inspected_commit: b0521cecd05aeb8db18660c056fb56579df31903
inspected_paths:
  - agent_review_inbox/review-T-P5-019-honglianmozun-20260907T0702.md
  - agent_review_inbox/review-T-P5-033-honglianmozun-20260907T1604.md
source_hashes:
  review-T-P5-033: 85bba57fa3613d2e8d34e9ba9892994960297ff7
continuation_of:
  - review-T-P5-019-honglianmozun-20260907T0702
  - review-T-P5-033-honglianmozun-20260907T1604
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_the_exact_Q_minus_15_over_16_V_weighted_nine_square_identity_and_replace_only_the_downstream_Q_to_V_constant
---

# T-P5-034 — exact weighted SOS strengthens block-(4,5) to `Q >= (15/16)V`

## 0. Result

For exactly the same block-(4,5) storage `V` and dissipation `Q` used by `T-P5-019` and `T-P5-033`, there is a still source-independent exact rational strengthening

```text
Q >= (15/16) V.                                         (0.1)
```

The proof is an explicit weighted nine-square decomposition.  It uses no numerical eigenvalue, matrix inverse, square root, source table, Float64 semantics, ODE continuation, provenance, or admission.

Combining (0.1) with the unchanged direct residual metric from `T-P5-019`,

```text
5 ||x+y||^2 <= 17 Q,                                    (0.2)
```

gives

```text
V' <= -(15/32)V + (17/10)||l||^2.                       (0.3)
```

Relative to `T-P5-033`'s coefficient `93/200`, the certified decay/residual capacity is multiplied by

```text
(15/32)/(93/200) = 125/124.                             (0.4)
```

Thus this is a further exact `1/124 ~= 0.80645%` headroom improvement with no new source assumption.

---

## 1. Exact input quadratic forms

Use the same exact matrices as `T-P5-033`:

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

The moving-frame derivative identity remains

```text
V' = -Q - (x+y)^T l.                                   (1.4)
```

No definition in (1.1)-(1.4) is changed by this child.

---

## 2. Exact `15/16` weighted nine-square certificate

In coordinate order `z=(x4,x5,y4,y5)`, exact rational expansion gives

```text
Q - (15/16)V =
    (270997/64000000)       x4^2
  + (2073349/1740800000)    x5^2
  + (3769409/96000000)      y4^2
  + (13342021/384000000)    y5^2

  + (867/64000)             (x4 - (5/17)x5)^2
  + (350003/64000000)       (x4 - 10 y4)^2
  + (3/16000)               (x4 + (20/3)y5)^2
  + (1/27200)               (x5 - 34 y4)^2
  + (1806651/1740800000)    (x5 - (68/3)y5)^2.          (2.1)
```

Every coefficient in (2.1) is strictly positive, so (0.1) follows immediately.

A useful way to see where (2.1) comes from is the exact symmetric matrix

```text
S15 := H_Q - (15/16) H_V =
[[ 3/128,           -51/12800,          -350003/6400000,      1/800 ],
 [ -51/12800,        11/3200,           -1/800,               -602217/25600000 ],
 [ -350003/6400000, -1/800,              60349859/96000000,    0 ],
 [ 1/800,           -602217/25600000,     0,                    73765267/128000000 ]].   (2.2)
```

Take the positive scaling vector

```text
d = (10, 34, 1, 3/2).                                  (2.3)
```

For every nonzero off-diagonal entry `s_ij`, use a weighted edge square whose coordinate ratio is `d_i/d_j`.  The leftover diagonal margins are exactly

```text
270997/64000000,
2073349/1740800000,
3769409/96000000,
13342021/384000000,                                    (2.4)
```

all positive.  Hence (2.1) is a scaled-diagonal-dominance/SOS certificate rather than a floating PSD test.

### Exact algebra check

Expanding the right side of (2.1) and subtracting `z^T S15 z` with exact rational arithmetic normalizes identically to zero.  No floating coefficient is part of the certificate.

---

## 3. Nearby exact failure boundary: `47/50` is impossible

The improvement should not be rounded upward to `0.94`.  There is a simple rational state

```text
z0 = (x4,x5,y4,y5) = (1, 25/6, 1/10, 1/6)              (3.1)
```

for which exact evaluation gives

```text
Q(z0) = 4311925721/400000000,
V(z0) = 27524714327/2400000000,                         (3.2)
```

and therefore

```text
Q(z0) - (47/50)V(z0)
  = -83857069/120000000000 < 0.                         (3.3)
```

Equivalently,

```text
Q(z0)/V(z0)
  = 25871554326/27524714327
  ~= 0.9399390678 < 0.94.                               (3.4)
```

So `Q >= (47/50)V` is false for the frozen block, by an exact rational counterexample.  This is a useful checker regression target and prevents accidental decimal rounding of the coercivity constant.  I do **not** claim `15/16` is sharp; (3.3) only supplies a rigorous nearby upper obstruction.

---

## 4. Improved residual-coupled Lyapunov ledger

From `T-P5-019`,

```text
|(x+y)^T l| <= (1/2)Q + (17/10)||l||^2.                (4.1)
```

Combining with (1.4) gives

```text
V' <= -(1/2)Q + (17/10)||l||^2.                        (4.2)
```

Using (0.1),

```text
V' <= -(15/32)V + (17/10)||l||^2.                      (4.3)
```

The corresponding constant-residual ultimate coefficient is

```text
(17/10)/(15/32) = 272/75.                              (4.4)
```

Again, only the `Q -> V` coercivity constant changes.

---

## 5. One-trajectory `V*=1/4` barrier

Assume on the relevant first-exit domain

```text
||l||^2 <= L2.                                          (5.1)
```

At `V=Vstar`, strict inwardness follows from

```text
(17/10)L2 < (15/32)Vstar.                              (5.2)
```

For the existing `Vstar=1/4`, this is the exact division-free gate

```text
1088 L2 < 75.                                           (5.3)
```

The allowed threshold is `75/1088 ~= 0.06893382353`, compared with `93/1360 ~= 0.06838235294` in `T-P5-033`; their ratio is exactly `125/124`.

---

## 6. Incremental ramp-parameter tube

Reuse the `T-P5-030` contract

```text
||Dl||^2 <= mu Vd + nu dc^2,
mu >= 0,
nu >= 0.                                                (6.1)
```

Then

```text
Vd'
 <= -[(15/32)-(17/10)mu] Vd
    + (17/10)nu dc^2.                                   (6.2)
```

On a generic boundary `Vd=Kc dc^2`, strict inwardness is implied by

```text
(75 - 272 mu) Kc > 272 nu.                             (6.3)
```

For the existing `Kc=1/12` (already above the exact initial coefficient from `T-P5-030`), this becomes

```text
272 mu + 3264 nu < 75,                                 (6.4)
```

or

```text
mu + 12 nu < 75/272 ~= 0.2757352941.                   (6.5)
```

Again this is exactly a factor `125/124` wider than `T-P5-033`'s `93/340` threshold.

---

## 7. Optional source-gain slack diagnostic

If a disjoint source bridge supplies

```text
mu = U+p,
nu = W+q,
p,q,U,W >= 0,
pq >= UW,                                               (7.1)
```

set

```text
R15 := 75 - 272U - 3264W.                              (7.2)
```

Then strict nonnegative slack feasibility has the same square-root-free precheck form

```text
R15 > 0,
R15^2 > 3551232 U W.                                    (7.3)
```

since `4*272*3264 = 3551232`.  As before, a checker can avoid square roots entirely by emitting rational `p,q` and verifying (7.1) plus `272(U+p)+3264(W+q)<75` directly.

---

## 8. Candidate theorem surface

The smallest source-independent theorem can be stated directly as the scalar identity (2.1):

```text
theorem block45_Q_minus_15_16_V_sos
    (x4 x5 y4 y5 : R) :
    Q45 x4 x5 y4 y5 - (15/16) * V45 x4 x5 y4 y5
      = <the nine positive square terms in (2.1)> := by
  ring
```

followed by

```text
theorem block45_Q_ge_15_16_V :
    (15/16) * V45 x4 x5 y4 y5 <= Q45 x4 x5 y4 y5 := by
  rw [block45_Q_minus_15_16_V_sos]
  positivity
```

A second tiny regression theorem can encode the exact obstruction (3.3), e.g. `block45_not_ge_47_50_V_at_z0`, using only `norm_num` after unfolding the scalar forms.

---

## 9. Failure boundaries / non-claims

1. `15/16` is a clean certified rational lower coercivity constant, **not** claimed optimal.
2. `47/50` is rigorously impossible for the frozen `V,Q`, by (3.3); any later proposal at or above `0.94` must change the storage/form, not merely improve the proof decomposition.
3. The result depends on the exact frozen block-(4,5) `M,D,K,A` and coordinate convention.  It must not be transplanted to a rescaled/different block without re-derivation.
4. An absolute residual cap still does not imply `Vd=O(dc^2)` as `dc -> 0`; the incremental residual contract remains necessary for parameter-cell contraction.
5. Source residual binding, Float64/solve semantics, ODE continuation, P8 absolute domain coverage, flowpipe coverage, provenance, admission, and P5/P8/M4 closure remain untouched.
6. This child does not take over any active Lean/source task.  It only supplies an exact algebraic theorem candidate and downstream arithmetic constants.

## 10. Requested integration action

Formalize (2.1) as one pure algebraic theorem and use it to replace only the current `Q >= (93/100)V` consumer by

```text
Q >= (15/16)V.
```

Then update the two arithmetic consumers to

```text
single V*=1/4 gate:       1088 L2 < 75,
incremental Kc=1/12 gate: 272 mu + 3264 nu < 75.
```

Keep the review `pending` until the normal independent Lean/kernel and integration gates run.  Preserve (3.3) as the exact nearby failure regression so no later decimal simplification silently upgrades the theorem to the false `47/50` bound.
