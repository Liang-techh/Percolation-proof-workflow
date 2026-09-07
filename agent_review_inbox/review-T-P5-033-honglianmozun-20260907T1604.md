---
kind: review_result
review_id: review-T-P5-033-honglianmozun-20260907T1604
task_id: T-P5-033
agent: 红莲魔尊
source_agent: 红莲魔尊
claimed_at: 2026-09-07T15:54:00-06:00
created_at: 2026-09-07T16:04:00-06:00
inspected_commit: 99e3046089063eb5834a27673ac31b7b1746c90a
inspected_paths:
  - agent_review_inbox/review-T-P5-019-honglianmozun-20260907T0702.md
  - agent_review_inbox/review-T-P5-032-honglianmozun-20260907T1253.md
source_hashes:
  review-T-P5-019: 8f9d3f20992ab1d08a3bf01d6bc6d7bd7a419f41
  review-T-P5-032: d8d407614e8c35c7535a256b740c78021100d83d
continuation_of:
  - review-T-P5-019-honglianmozun-20260907T0702
  - review-T-P5-032-honglianmozun-20260907T1253
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_the_exact_Q_minus_93_over_100_V_nine_square_identity_and_replace_only_the_downstream_Q_to_V_constant
---

# T-P5-033 — exact weighted nine-square SOS strengthens block-(4,5) to `Q >= (93/100) V`

## 0. Result

For exactly the same block-(4,5) storage `V` and dissipation `Q` used by `T-P5-019` and `T-P5-032`, the previous source-independent coercivity

```text
Q >= (8/9) V
```

can be strengthened, still by a completely rational scalar-square identity, to

```text
Q >= (93/100) V.                                        (0.1)
```

The proof below uses only nine explicit nonnegative squares.  It does not invoke a numerical eigenvalue, matrix inverse, square root, source table, Float64 semantics, ODE continuation, coverage, provenance, or admission.

Combining (0.1) with the unchanged direct residual metric from `T-P5-019`,

```text
5 ||x+y||^2 <= 17 Q,                                    (0.2)
```

gives the improved reusable ledger

```text
V' <= -(93/200) V + (17/10)||l||^2.                     (0.3)
```

Relative to `T-P5-032`'s `-(4/9)V`, the certified decay/residual capacity is multiplied by exactly

```text
(93/200)/(4/9) = 837/800 = 1.04625.                     (0.4)
```

So this is a further 4.625% source-budget improvement on top of the earlier `T-P5-032` gain, with no new source assumption.

---

## 1. Exact input quadratic forms

Use the exact matrices already fixed in `T-P5-032`:

```text
M = diag(350003/3000000, 200739/4000000),
D = diag(4/5, 13/20),
K = [[3/4,    -3/400],
     [-3/400, 29/50]],
A = [[0, 1/400],
     [-1/400, 0]].                                       (1.1)
```

For `x=(x4,x5)`, `y=(y4,y5)`,

```text
V
 := (1/2) y^T M y
  + (1/2) x^T K x
  + x^T M y
  + (1/2) x^T D x,                                       (1.2)

Q
 := y^T(D-M)y + x^T K x - y^T A x.                      (1.3)
```

The exact moving-frame derivative identity remains

```text
V' = -Q - (x+y)^T l.                                     (1.4)
```

No definition in (1.1)-(1.4) is changed by this child.

---

## 2. Exact weighted nine-square identity

Direct rational expansion gives

```text
Q - (93/100)V
=
  (3542407/600000000) x4^2
+ (155697/800000000)   x5^2
+ (69762071/150000000) y4^2
+ (29216493/80000000)  y5^2

+ (321/80000)                 (x4-x5)^2
+ (10850093/600000000)        (x4-3 y4)^2
+ (1/800)                     (x4+y5)^2
+ (1/800)                     (x5-y4)^2
+ (18668727/7200000000)       (x5-9 y5)^2.               (2.1)
```

Every coefficient in (2.1) is strictly positive.  Therefore

```text
Q - (93/100)V >= 0,                                      (2.2)
```

which proves (0.1).

The important difference from the `8/9` identity is the use of *weighted* edge squares `(x4-3 y4)^2` and `(x5-9 y5)^2`.  The older unit-weight diagonal-dominance decomposition spent too much of the small `x4,x5` diagonal budget on those two large cross terms.  Transporting the same cross coefficient through weights `3` and `9` moves most of that square cost to the much larger `y4,y5` diagonals and leaves all four coordinate margins positive.

For a coefficient-level cross-check, the symmetric matrix of the left-hand side in the coordinate order `(x4,x5,y4,y5)` is

```text
H93 =
[[117/4000,       -321/80000,       -10850093/200000000,   1/800],
 [-321/80000,      161/20000,       -1/800,                -18668727/800000000],
 [-10850093/200000000, -1/800,       377449121/600000000,   0],
 [1/800,           -18668727/800000000, 0,                  461183473/800000000]]. (2.3)
```

Its leading principal minors are also exact and positive:

```text
117/4000,
1403919/6400000000,
22742982135366409/200000000000000000000,
4399102337667233385139301735963/
  76800000000000000000000000000000000.                  (2.4)
```

Equation (2.4) is only an independent algebraic sanity check; the theorem can be formalized directly from the simpler nine-square identity (2.1), so no matrix-positivity API is required.

### Reproducibility check

I expanded `(2.1) - (Q-(93/100)V)` with exact rational arithmetic (`sympy.Rational` only).  The normalized polynomial is identically zero; checker exit code was `0`.  No floating-point coefficient entered the equality check.  Numerical eigenvalue information was not used as evidence for (0.1).

---

## 3. Improved residual-coupled Lyapunov inequality

Reuse the already-proved direct residual metric (0.2).  The same half-Young step from `T-P5-019/032` gives

```text
|(x+y)^T l| <= (1/2)Q + (17/10)||l||^2.                 (3.1)
```

Together with (1.4),

```text
V' <= -(1/2)Q + (17/10)||l||^2.                         (3.2)
```

Now (0.1) implies

```text
(1/2)Q >= (93/200)V,                                     (3.3)
```

hence

```text
V' <= -(93/200)V + (17/10)||l||^2.                      (3.4)
```

For a constant residual-square cap the corresponding ultimate coefficient is

```text
(17/10)/(93/200) = 340/93 < 153/40.                     (3.5)
```

Thus this child changes only the `Q -> V` coercivity; it does not alter the residual norm, moving frame, or force-coordinate contract.

---

## 4. One-trajectory barrier consumer

Assume on the relevant first-exit domain

```text
||l||^2 <= L2.                                           (4.1)
```

At `V=Vstar`, (3.4) is strictly inward whenever

```text
(17/10)L2 < (93/200)Vstar.                              (4.2)
```

Clearing denominators gives the exact division-free gate

```text
340 L2 < 93 Vstar.                                       (4.3)
```

For the existing `Vstar=1/4`, this is

```text
1360 L2 < 93.                                            (4.4)
```

The admitted `L2` threshold is `93/1360`; compared with `T-P5-032`'s `10/153`,

```text
(93/1360)/(10/153) = 837/800.                            (4.5)
```

So every source residual certificate already targeting the quarter-energy barrier gains exactly 4.625% additional headroom.

---

## 5. Incremental ramp-parameter tube consumer

Reuse the `T-P5-030` incremental residual contract

```text
||Dl||^2 <= mu Vd + nu dc^2,
mu >= 0,
nu >= 0.                                                  (5.1)
```

The same calculation gives

```text
Vd'
 <= -[(93/200)-(17/10)mu] Vd
    + (17/10)nu dc^2.                                    (5.2)
```

On a generic boundary `Vd=Kc dc^2`, strict inwardness is implied by

```text
(93 - 340 mu) Kc > 340 nu.                              (5.3)
```

For the existing `Kc=1/12`, already compatible with the initial coefficient `C0<1/12`, this becomes

```text
340 mu + 4080 nu < 93,                                  (5.4)
```

or equivalently

```text
mu + 12 nu < 93/340.                                    (5.5)
```

Again,

```text
(93/340)/(40/153) = 837/800,                             (5.6)
```

so the same parameter tube accepts 4.625% more incremental residual budget than the `8/9` consumer.

---

## 6. Optional downstream T-P5-031 slack diagnostic

If the disjoint source bridge supplies

```text
mu = U+p,
nu = W+q,
p,q,U,W >= 0,
pq >= UW,                                                  (6.1)
```

then the new tube consumer is simply

```text
340(U+p) + 4080(W+q) < 93.                              (6.2)
```

Define the remaining weighted margin

```text
R93 := 93 - 340U - 4080W.                               (6.3)
```

Because the minimum possible weighted slack cost under `pq>=UW` is

```text
2 sqrt(340*4080*UW),                                     (6.4)
```

strict real nonnegative slack feasibility has the square-root-free diagnostic

```text
R93 > 0,
R93^2 > 5548800 UW.                                      (6.5)
```

A checker need not formalize the square root: it can emit rational `p,q` and verify (6.1)-(6.2) directly.  Equation (6.5) is only a pre-search obstruction.

---

## 7. Candidate Lean theorem surface

The smallest useful kernel child is source-independent:

```text
theorem block45_Q_minus_93_100_V_sos
    (x4 x5 y4 y5 : ℝ) :
    Q45 x4 x5 y4 y5 - (93/100 : ℝ) * V45 x4 x5 y4 y5
      =
        (3542407/600000000 : ℝ) * x4^2
      + (155697/800000000 : ℝ) * x5^2
      + (69762071/150000000 : ℝ) * y4^2
      + (29216493/80000000 : ℝ) * y5^2
      + (321/80000 : ℝ) * (x4-x5)^2
      + (10850093/600000000 : ℝ) * (x4-3*y4)^2
      + (1/800 : ℝ) * (x4+y5)^2
      + (1/800 : ℝ) * (x5-y4)^2
      + (18668727/7200000000 : ℝ) * (x5-9*y5)^2 := by
  ring
```

followed by

```text
theorem block45_Q_ge_93_100_V :
  (93/100 : ℝ) * V45 ... <= Q45 ... := by
  rw [block45_Q_minus_93_100_V_sos]
  positivity
```

The exact tactic spelling may depend on the existing scalar definitions, but no analytic or matrix library is mathematically necessary.  This is intentionally disjoint from the coordinator's P7 pinned-compile lane.

---

## 8. Failure boundary / non-claims

1. `93/100` is a deliberately simple rational strengthening, **not** claimed optimal.  This review does not certify the sharp generalized eigenvalue of `(Q,V)`.
2. The improvement is conditional on the already-established exact storage/dissipation definitions and direct residual metric.  If a downstream source uses a different `V`, `Q`, coordinate scaling, or residual norm, (0.1) cannot be transplanted without a new bridge.
3. An absolute residual bound still cannot imply `Vd=O(dc^2)` as `dc -> 0`; the incremental contract (5.1) remains necessary for cell-diameter contraction.
4. ODE existence/continuation, first-exit packaging, source-domain coverage, `w=ct` coverage, Float64/solve semantics, source gain tables, provenance, receipt admission, and P5/P8/M4 closure are untouched.
5. This result does not compete with the current P7 source-binding / focused-pinned-compile request.  It is a standalone P5 mathematical child produced because no local Lean toolchain is available in this runtime and no duplicate `T-P5-033` claim was present at claim time.

## 9. Requested integration action

Formalize (2.1) as one pure algebraic theorem and replace only the downstream `Q >= (8/9)V` consumer by `Q >= (93/100)V`.  Then update the arithmetic corollaries to

```text
single V*=1/4 gate:       1360 L2 < 93,
incremental Kc=1/12 gate: 340 mu + 4080 nu < 93.
```

Keep the review `pending` until the normal independent Lean/kernel and integration gates run.
