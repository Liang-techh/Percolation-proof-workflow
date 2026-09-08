---
kind: review_result
review_id: review-T-P5-040-honglianmozun-20260907T1950
task_id: T-P5-040
agent: 红莲魔尊
source_agent: 红莲魔尊
claimed_at: 2026-09-07T19:50:00-06:00
created_at: 2026-09-07T19:50:00-06:00
inspected_commit: 955af52fd2578b3de83457a78170abc68945c74a
continuation_of:
  - review-T-P5-037-honglianmozun-20260907T1856
  - review-T-P5-036-guyuefangyuan-20260907T1906
  - review-T-P5-039-guyuefangyuan-20260907T1931
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_the_mixed_relative_additive_completion_and_reserve_adjusted_first_exit_gate; keep_source_binding_Lean_receipts_coverage_and_admission_separate
---

# T-P5-040 — sharp mixed relative-plus-additive residual absorption for the block-(4,5) Pareto energy family

## 0. Result

The current P5 energy lane has two exact endpoint certificates and their convex Pareto bridge.  Write

```text
u4 := x4+y4,
u5 := x5+y5,
```

and let `0 <= r <= 1`.  The frozen Pareto family is

```text
Q >= c(r) V + a4(r) u4^2 + a5 u5^2,                   (0.1)
```

with

```text
c(r)  = (109-r)/200,
a4(r) = (250+53r)/1500,
a5    = 1/6.                                           (0.2)
```

The exact moving-frame identity remains

```text
V' = -Q - u4*l4 - u5*l5.                              (0.3)
```

The still-open source interface need not force a false purely-relative model.  Suppose instead that a source-side checker eventually proves, on the same domain,

```text
|l4| <= rho4*|u4| + b4,
|l5| <= rho5*|u5| + b5,                               (0.4)

rho4,rho5,b4,b5 >= 0.
```

Define the remaining quadratic reserves

```text
t4 := a4(r)-rho4,
t5 := a5-rho5.                                         (0.5)
```

If `t4>0` and `t5>0`, then one gets the **sharp channelwise additive-bias charge**

```text
V' <= -c(r)V + b4^2/(4*t4) + b5^2/(4*t5).             (0.6)
```

No auxiliary Young parameter is needed.  The constants `1/(4*t_i)` are optimal for this information: for one channel,

```text
-t*u^2 + b*|u|
 = b^2/(4*t) - t*(|u|-b/(2*t))^2
 <= b^2/(4*t),                                         (0.7)
```

and equality occurs at `|u|=b/(2*t)`.

Thus the additive offset that prevents the older `|l_i| <= rho_i |u_i|` theorem from applying can be charged exactly, while all unused Pareto quadratic reserve is preserved.

---

## 1. Complete derivation

From (0.4),

```text
-u_i*l_i
 <= |u_i|*|l_i|
 <= rho_i*u_i^2 + b_i*|u_i|.                           (1.1)
```

Combining (0.1), (0.3), and (1.1) yields

```text
V'
 <= -cV
    -(a4-rho4)u4^2 + b4|u4|
    -(a5-rho5)u5^2 + b5|u5|.                           (1.2)
```

For `t_i=a_i-rho_i>0`, the exact identity

```text
-t_i*u_i^2 + b_i|u_i|
 = b_i^2/(4*t_i)
   - t_i*(|u_i|-b_i/(2*t_i))^2                         (1.3)
```

proves (0.6).

If a checker has only square budgets

```text
b4^2 <= B4,
b5^2 <= B5,
B4,B5 >= 0,                                            (1.4)
```

then

```text
V' <= -c(r)V + B4/(4*t4) + B5/(4*t5).                 (1.5)
```

This theorem is source-independent: it does not identify what the deployed `l_i`, `rho_i`, or `b_i` are.

---

## 2. Division-free reserve-adjusted first-exit gate

For the existing quarter barrier `V*=1/4`, strict inwardness from (1.5) is exactly implied by

```text
B4/t4 + B5/t5 < c(r).                                  (2.1)
```

Introduce denominator-free reserve variables

```text
A4 := 250 + 53*r - 1500*rho4,
A5 := 1 - 6*rho5.                                      (2.2)
```

Then

```text
t4 = A4/1500,
t5 = A5/6.                                             (2.3)
```

So the positivity premises are simply

```text
A4 > 0,
A5 > 0,                                                (2.4)
```

and (2.1) is equivalent, after multiplication only by positive quantities, to the exact polynomial checker gate

```text
300000*B4*A5 + 1200*B5*A4
  < (109-r)*A4*A5.                                     (2.5)
```

This is the main downstream result of the child.

When `rho4=rho5=0`, one has `A4=250+53r`, `A5=1`, and (2.5) reduces **exactly** to the existing T-P5-039 Pareto gate

```text
300000*B4 + 1200*(250+53r)*B5
  < (109-r)*(250+53r).                                 (2.6)
```

Therefore (2.5) is a conservative extension of the already formalized additive-square consumer, not a competing or incompatible ledger.

---

## 3. Exact failure boundary: why positive reserve is the right interface

The reserve condition in (2.4) is not a cosmetic proof artifact.

For one channel, define

```text
F(u) := -t*u^2 + b*|u|.                                (3.1)
```

Then:

1. If `t>0`, `sup_u F(u)=b^2/(4t)`, attained at `|u|=b/(2t)`.
2. If `t=0` and `b>0`, `F(u)=b|u|` is unbounded above.
3. If `t<0`, `F(u)=|t|u^2+b|u|` is unbounded above even when `b=0`.
4. The degenerate case `t=0,b=0` has zero charge but no remaining quadratic reserve in that channel.

Hence, without an independent bound on `u_i`, there is **no finite source-independent constant bias charge** once `rho_i` exhausts or exceeds `a_i`, except for the trivial zero-bias equality case.

This identifies the exact obstruction to forcing an additive-offset implementation into a purely relative decay theorem: the correct repair is to keep `rho_i<a_i` and pay the sharp bias charge, not to silently drop `b_i`.

---

## 4. Incremental/parameter-tube corollary

The same argument applies to the T-P5-030 difference system.  Suppose a genuine incremental source contract has the mixed form

```text
|Dl4| <= rho4*|Du4| + k4*|dc|,
|Dl5| <= rho5*|Du5| + k5*|dc|,                         (4.1)
```

with

```text
k4^2 <= G4,
k5^2 <= G5.                                            (4.2)
```

Then

```text
Vd' <= -c(r)Vd
       + [G4/(4*t4) + G5/(4*t5)]*dc^2.                 (4.3)
```

For the existing candidate tube

```text
Vd = (1/12)*dc^2,                                      (4.4)
```

strict inwardness follows from the division-free gate

```text
900000*G4*A5 + 3600*G5*A4
  < (109-r)*A4*A5,                                     (4.5)
```

again under `A4>0`, `A5>0`, `0<=r<=1`.

This also isolates a known obstruction in a sharper componentwise form: a fixed additive difference bias that does **not** vanish with `|dc|` cannot yield an `O(dc^2)` parameter-cell tube as `dc -> 0`.  The incremental additive term must scale with state/parameter separation (or be handled by a nonshrinking tube).

---

## 5. Candidate theorem surface

A minimal algebraic formalization can be split into four source-independent lemmas.

```text
mixed_relative_additive_square_completion
```

For `t>0`, prove the exact identity

```text
-t*u^2 + b*abs(u)
 = b^2/(4*t) - t*(abs(u)-b/(2*t))^2.
```

A division-free Lean variant should instead multiply by `4*t` and use only polynomial arithmetic plus `abs_nonneg`.

```text
block45_pareto_mixed_residual_decay
```

Consumes (0.1), (0.3), (0.4), `t4>0`, `t5>0` and proves (0.6).

```text
block45_pareto_bias_first_exit_gate
```

Consumes `A4>0`, `A5>0`, square budgets (1.4), and polynomial gate (2.5), and proves strict inwardness at `V=1/4` without square roots.

```text
block45_pareto_incremental_bias_tube_gate
```

Consumes (4.1)-(4.2) and (4.5), and proves strict inwardness on `Vd=(1/12)dc^2`.

The first-exit and tube gates are intentionally stated with explicit rational witnesses `r,rho4,rho5,B4,B5` (or `G4,G5`) rather than introducing an optimizer.  T-P5-039 already owns the exact Pareto parameter-selection layer for the zero-relative-reserve specialization; this child does not duplicate that work.

---

## 6. Assumptions, dependencies, and non-claims

Mathematical dependencies:

- T-P5-037: exact scalar joint certificate and moving-frame energy identity;
- T-P5-036: anisotropic endpoint certificate;
- the T-P5-036 x T-P5-037 convex bridge: exact Pareto family (0.1);
- T-P5-030 only for the optional incremental corollary.

Required future source premises are explicit: same-domain componentwise values/bounds for `rho4,rho5,b4,b5`, or incremental `k4,k5`, with coordinates matching `u_i=x_i+y_i` / their difference variables.

This review does **not** prove:

- that deployed `forceError`, FD, controller, `solve`, or true-DH residuals satisfy (0.4) or (4.1);
- Float64/source reification;
- ODE existence/continuation or flowpipe coverage;
- any provenance/receipt/admission claim;
- P5/P8/M4 parent closure.

The exact failure boundary in Section 3 must remain visible: additive offsets cannot be discarded merely because a relative-decay theorem is available.

**Status: pending mathematical child — 待封不觉独立验证 / 待梁智炜最终整合。**
