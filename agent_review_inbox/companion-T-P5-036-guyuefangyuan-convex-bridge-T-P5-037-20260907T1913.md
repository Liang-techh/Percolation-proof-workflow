---
kind: companion_log
task_id: T-P5-036
review_id: review-T-P5-036-guyuefangyuan-20260907T1906
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-07T19:13:00-06:00
related_reviews:
  - review-T-P5-037-honglianmozun-20260907T1856
integration_status: pending
---

# T-P5-036 × T-P5-037 exact Pareto bridge

After `T-P5-036` was claimed, 红莲魔尊 completed the explicitly disjoint scalar child `T-P5-037`, proving

```text
Q >= (109/200)V + (1/6)u4^2 + (1/6)u5^2.              (A)
```

`T-P5-036` proves

```text
Q >= (27/50)V + (101/500)u4^2 + (1/6)u5^2.            (B)
```

These two certificates should not be treated as competitors with a single winner: (A) has slightly more `V` decay, while (B) has much more component-4 residual reserve.  Because both lower-bound the same `Q`, every rational convex combination is automatically valid.

For any rational `r` with `0 <= r <= 1`, multiply (B) by `r`, (A) by `1-r`, and add.  This gives the exact one-parameter Pareto family

```text
Q >= ((109-r)/200) V
     + ((250+53r)/1500) u4^2
     + (1/6) u5^2.                                     (C)
```

No new SOS is needed: (C) is a positive linear combination of two exact rational certificates.

Completing the two residual coordinates gives

```text
V' <= -((109-r)/200)V
      + [375/(250+53r)] l4^2
      + (3/2) l5^2.                                    (D)
```

For same-domain componentwise bounds `l4^2<=E4`, `l5^2<=E5`, a division-free first-exit checker at a general `Vstar` is

```text
75000 E4
 + 300(250+53r) E5
 < (109-r)(250+53r) Vstar.                             (E)
```

At the existing `Vstar=1/4`, multiply by four:

```text
300000 E4
 + 1200(250+53r) E5
 < (109-r)(250+53r).                                   (F)
```

Endpoint checks:

- `r=0` recovers `T-P5-037`: `1200(E4+E5)<109`.
- `r=1` recovers `T-P5-036`: `25000E4+30300E5<2727` after dividing the common factor 12.

Thus source/checker does not need to choose globally between the scalar and anisotropic lanes.  It can retain `E4,E5`, pick any rational `r in [0,1]`, and test (F).  A tiny rational search over `r` is sound and preserves exact arithmetic; there is no need for floating optimization or square roots.

For orientation, the endpoint inward-margin comparison at a general boundary is especially simple.  `T-P5-036` gives more inward margin than `T-P5-037` iff

```text
E4 > (101/5300) Vstar.                                 (G)
```

At `Vstar=1/4`, this threshold is

```text
E4 > 101/21200 ~= 0.00476415.                          (H)
```

So unless the component-4 residual budget is extremely small, the anisotropic endpoint already beats the scalar endpoint; for intermediate source mixtures, the convex family (C)-(F) can be better than both endpoints.

The continuous margin as a function of `r` is concave:

```text
m(r) = ((109-r)/200)Vstar
       - 375 E4/(250+53r)
       - (3/2)E5.
```

An interior real optimizer, when it lies in `[0,1]`, satisfies

```text
(250+53r)^2 = 3975000 * E4 / Vstar.                    (I)
```

Equation (I) is only a mathematical characterization; the trusted checker should simply use a rational `r` witness and verify (E)/(F), avoiding any square-root dependency.

Suggested Lean bridge theorem:

```text
block45_joint_pareto_of_two_certificates
```

with hypotheses `0<=r`, `r<=1`, plus the two already-formalized endpoint inequalities, and conclusion (C).  Downstream arithmetic theorem can consume (E) directly.  This bridge is source-independent and does not alter either agent's ownership: 红莲魔尊 keeps `T-P5-037`; 古月方源 keeps the componentwise `T-P5-036` lane.

Open boundaries remain unchanged: real source `E4,E5`, Float64/FD/solve semantics, same-domain coverage, ODE/first-exit, Lean kernel receipts, and parent admission are still open.
