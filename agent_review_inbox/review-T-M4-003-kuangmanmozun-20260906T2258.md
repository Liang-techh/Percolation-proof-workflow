---
kind: review_result
review_id: review-T-M4-003-kuangmanmozun-20260906T2258
task_id: T-M4-003
source_agent: 狂蛮魔尊
claimed_at: 2026-09-06T22:55:00-06:00
created_at: 2026-09-06T22:58:00-06:00
inspected_commit: dbb3e349b8faf62a772651f3745ce8ce9836a567
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_weighted_terminal_split_then_validate
---

# T-M4-003 — weighted terminal quadratic closure and a wider exact residual gate

## Scope

This is a new mathematical child in the M4/C5 terminal-comparison lane. It is
disjoint from the currently claimed `T-M4-002` dependency-cone work and from
P4/P7 source binding. The goal is to identify whether the existing terminal
comparison

```text
Q <= (3/2) L + 3 g D
```

is an intrinsic constant choice or just one Young-inequality split, and whether
a better exact rational split can enlarge the admissible residual budget.

Inspected interfaces:

- `docs/routeb-m4-next-obligations.md`
  - blob `6ca176bd82d3727ceda0d9a3e80e9d999dcc551a`
  - C5 explicitly asks for the new joint inequality before the scalar terminal
    comparator.
- `docs/routeb-block-targets-v2.md`
  - blob `0fe7054f44c3002d782bb3acb51f88ef7021c6a3`
  - preserves the actual terminal target `Q_B(1) < 12`.
- `examples/routeb_terminal_qpoly_comparator_lean/F4DirectQpolyComparator.lean`
  - blob `2d89190182dd7a4a795f8c8e1e930f9f46686bf2`
  - current constants `L`, `g`, `D_gate=4483/2000` and the exact
    `(3/2,3)` scalar comparator.

No provenance, receipt, admission, source-authentication, or kernel-validation
claim is made here.

## 1. Exact weighted split behind the current `(3/2,3)` coefficients

For one scalar coordinate and arbitrary real `a,b,eta`, the identity

```text
eta*(1+eta)*a^2 + (eta+1)*b^2 - eta*(a+b)^2
  = (eta*a-b)^2
```

is exact. Therefore

```text
eta*(a+b)^2
  <= eta*(1+eta)*a^2 + (eta+1)*b^2.                 (1)
```

When `eta>0`, division by `eta` gives

```text
(a+b)^2
  <= (1+eta)*a^2 + (1+1/eta)*b^2.                  (2)
```

Apply (1) coordinatewise to the terminal block quadratic

```text
Q(q4,q5,v4,v5) = 3(q4^2+q5^2) + 2(v4^2+v5^2).
```

For block vectors `x` and `r`, with coordinatewise sum `x+r`, we obtain the
source-independent exact theorem

```text
eta * Q(x+r)
 <= eta*(1+eta)*Q(x) + (eta+1)*Q(r).                (3)
```

For `eta>0`:

```text
Q(x+r)
 <= (1+eta) Q(x) + (1+1/eta) Q(r).                 (4)
```

The current coefficients are exactly the special case

```text
eta = 1/2:
1+eta     = 3/2,
1+1/eta   = 3.
```

So `(3/2,3)` is not intrinsic to the dynamics or terminal target; it is one
particular weighted Young split.

### Sharpness for fixed eta

The slack in (3) is the positive weighted sum of the squares

```text
3*(eta*x_q4-r_q4)^2
+3*(eta*x_q5-r_q5)^2
+2*(eta*x_v4-r_v4)^2
+2*(eta*x_v5-r_v5)^2.
```

Hence the weighted inequality is sharp for each fixed `eta`: equality occurs
when `r = eta*x` coordinatewise. There is no hidden constant improvement at a
fixed `eta` without additional correlation information.

## 2. Terminal comparator family

Assume the C5 decomposition supplies

```text
Q(x_lin) <= L,
Q(r)     <= g*D,
eta > 0.
```

Then (4) gives

```text
Q(x_lin+r)
 <= (1+eta)*L + (1+1/eta)*g*D.                     (5)
```

Thus the admissible residual threshold for terminal target `Q<12` is

```text
D < Dmax(eta)

Dmax(eta)
 = [12-(1+eta)L] / [(1+1/eta)g]
 = eta*[12-(1+eta)L] / [(1+eta)g],                 (6)
```

whenever the numerator is positive.

This cleanly separates three mathematical inputs:

1. the linear/kernel budget `L`;
2. the residual quadratic budget `gD`;
3. the freely selectable cross-term allocation `eta`.

## 3. Optimal eta and the sharp information-theoretic limit

For fixed nonnegative values `A=Q(x)` and `B=Q(r)`, minimizing the right side
of (4) over `eta>0` gives

```text
eta = sqrt(B/A)
```

when `A,B>0`, and the minimum

```text
(sqrt(A)+sqrt(B))^2.                                (7)
```

Equivalently, if only `Q(x)<=L` and `Q(r)<=gD` are known, no member of this
Young family can beat the sharp worst-case envelope

```text
Q(x+r) <= (sqrt(L)+sqrt(gD))^2.                    (8)
```

For the threshold problem `Q<12`, maximizing (6) gives the unique positive
optimizer

```text
eta_* = sqrt(12/L) - 1 ≈ 0.5054065174,
```

and the corresponding sharp residual threshold

```text
D_sharp = (sqrt(12)-sqrt(L))^2/g ≈ 2.24169853393.
```

This is a genuine limit of the information `Q(x)<=L`, `Q(r)<=gD` alone. To
improve beyond it one must exploit sign/correlation/orthogonality information
between the linear and residual terminal components, not another Young split.

## 4. A simple exact rational improvement: eta = 81/160

Choose

```text
eta0 = 81/160 = 0.50625,
```

which is close to `eta_*` but remains a small exact rational suitable for Lean.
For the repository's current exact `L`, `g`, and

```text
D_gate = 4483/2000 = 2.2415,
```

the weighted terminal right side is

```text
(1+eta0)*L + (1+1/eta0)*g*D_gate
  ≈ 11.9996510356021,
```

so the exact positive terminal margin is

```text
12 - RHS
 = 562809780911078327482773299144592251
   / 1612800000000000000000000000000000000000
 ≈ 3.48964397886e-4.                               (9)
```

By comparison, the current `eta=1/2` comparator has exact margin

```text
1785114471132399020014546178891853
/ 35840000000000000000000000000000000000
≈ 4.98078814490e-5.                                 (10)
```

Therefore `eta0=81/160` gives about **7.006 times more terminal arithmetic
margin** at the same `D_gate`.

The exact residual threshold generated by `eta0` is

```text
Dmax(81/160)
 = 811291800430081715258594006599252240467
   / 361910082180445161930697595332080823750
 ≈ 2.24169438868.                                  (11)
```

Its gap above the current `D_gate` is

```text
≈ 1.94388678508e-4,
```

whereas the current `eta=1/2` threshold is only about

```text
2.75168479741e-5
```

above `D_gate`. This is about a **7.06x widening** of the residual-budget
headroom.

## 5. Concrete stronger corollary: D <= 1401/625

A particularly useful exact-rational consequence is that the terminal theorem
can tolerate

```text
D <= 1401/625 = 2.2416,
```

which is exactly

```text
1/10000
```

larger than the current gate `4483/2000`.

At `eta0=81/160` and `D=1401/625`, the exact terminal margin remains positive:

```text
12 - [(1+eta0)L + (1+1/eta0)g*(1401/625)]
 = 11386738131946758247425634286621983
   / 67200000000000000000000000000000000000
 ≈ 1.69445507916e-4 > 0.                             (12)
```

Thus the following stronger scalar consequence is mathematically valid:

```text
Q(x_lin) <= L,
Q(r) <= g*D,
D <= 1401/625
-----------------------------------------------
Q(x_lin+r) < 12,
```

provided the weighted split uses `eta=81/160`.

This does **not** authorize changing the authoritative M4 `D_gate` by itself;
it shows that C5 is capable of accepting a strictly looser C4 residual budget
if the coordinator chooses to expose this improved theorem.

## 6. Lean-friendly theorem statements

The highest-value formalization is the division-free identity-based child.
For four scalar coordinates, define the existing `qpoly`, then prove:

```lean
theorem qpoly_weighted_split
    (eta : ℝ)
    (xq4 xq5 xv4 xv5 rq4 rq5 rv4 rv5 : ℝ) :
    eta * qpoly (xq4+rq4) (xq5+rq5) (xv4+rv4) (xv5+rv5)
      <= eta*(1+eta) * qpoly xq4 xq5 xv4 xv5
       + (eta+1) * qpoly rq4 rq5 rv4 rv5 := by
  have hq4 : 0 <= (eta*xq4-rq4)^2 := sq_nonneg _
  have hq5 : 0 <= (eta*xq5-rq5)^2 := sq_nonneg _
  have hv4 : 0 <= (eta*xv4-rv4)^2 := sq_nonneg _
  have hv5 : 0 <= (eta*xv5-rv5)^2 := sq_nonneg _
  -- unfold qpoly; nlinarith
```

Then expose the positive-eta divided form:

```lean
theorem qpoly_weighted_split_of_pos
    (heta : 0 < eta) :
    qpoly (x+r) <= (1+eta)*qpoly x + (1+1/eta)*qpoly r
```

and the concrete exact-rational corollary:

```lean
theorem terminal_qpoly_lt_twelve_eta81_160
    (hlin : qpoly x <= L)
    (hres : qpoly r <= g*D)
    (hD : D <= 1401/625) :
    qpoly (x+r) < 12
```

A theorem at the scalar abstraction level may also be useful:

```lean
theorem weighted_terminal_scalar
    (eta L g D Qlin Qres Q : ℝ)
    (heta : 0 < eta)
    (hQ : eta*Q <= eta*(1+eta)*Qlin + (eta+1)*Qres)
    (hlin : Qlin <= L)
    (hres : Qres <= g*D) :
    eta*Q <= eta*(1+eta)*L + (eta+1)*g*D
```

Formalization should keep the generic weighted inequality separate from the
repository-specific exact arithmetic corollary.

## 7. Failure boundary / what this does not solve

This result does not create `L`, `g`, or `D`; it only makes the terminal
cross-term handling sharper. In particular it does not prove:

- the variation-of-constants decomposition for the deployed dynamics;
- `Q(x_lin)<=L` from the actual full initial ball;
- `Q(r)<=gD` from the actual residual kernel;
- the C4 full-domain residual integral;
- first-exit/domain continuation;
- true-DH source binding or P8 coverage.

Also, once the optimized envelope (8) is reached, **further scalar tuning is a
dead end**. Any attempt to exceed `D_sharp≈2.24169853` while using only the two
separate quadratic bounds must fail: choose aligned terminal components so that
`r` is a positive scalar multiple of `x`, which saturates the cross term.

## Recommended next action

1. 苏梦辰/臭屁猪: formalize `qpoly_weighted_split` and the exact
   `eta=81/160`, `D<=1401/625` corollary in a portable CI sidecar.
2. 星宿仙尊 can keep `T-M4-002` focused on the linear/kernel dependency cone;
   this review supplies a sharper C5 consumer without taking over that task.
3. The physical math lane should compare its best available C4 bound against
   both `4483/2000` and the new safe `1401/625`. If it still exceeds the sharp
   `~2.24169853` limit, stop tuning Young constants and seek correlation or a
   better kernel/residual decomposition.

No compile command was run in this mathematical pass; formalization and final
verification belong to the designated formalization agents and 封不觉.
