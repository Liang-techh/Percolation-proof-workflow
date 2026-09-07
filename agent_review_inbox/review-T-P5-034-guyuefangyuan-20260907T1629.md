---
kind: review_result
review_id: review-T-P5-034-guyuefangyuan-20260907T1629
task_id: T-P5-034
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-07T16:29:00-06:00
inspected_commit: 5517ca9f3d745c117cab1b82cf127117bd28a009
inspected_paths:
  - agent_review_inbox/README.md
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/collaboration_board.md
  - agent_review_inbox/review-T-P5-033-honglianmozun-20260907T1604.md
  - examples/routeb_p5_block45_93_sos_lean/P5Block45NinetyThreeSOS.lean
related_tasks:
  - T-P5-019
  - T-P5-030
  - T-P5-031
  - T-P5-032
  - T-P5-033
integration_status: pending
admission_label: pending
proposed_integration_target: P5.block45_near_sharp_Q_over_V_coercivity
requested_action: replace_the_source_independent_93_over_100_Q_to_V_constant_by_31_over_33_after_independent_validation; retain_the_explicit_47_over_50_failure_as_a_global_homogeneous_obstruction; after_that_prioritize_residual_source_binding_over_further_global_Q_over_V_constant_tuning
---

# T-P5-034 — `31/33` exact coercivity and a `47/50` explicit upper obstruction

## 0. Result

`T-P5-033` strengthened the exact block-(4,5) coercivity to

```text
Q >= (93/100) V.
```

For the **same** exact rational storage `V` and dissipation `Q`, this child proves the stronger global bound

```text
Q >= (31/33) V.                                           (0.1)
```

The proof is an exact four-square rational identity; no numerical eigenvalue, square root, source table, Float64 semantics, ODE argument, coverage, or registry evidence is used.

Moreover the nearby coefficient

```text
47/50 = 0.94
```

is impossible globally: at the explicit rational state

```text
(x4,x5,y4,y5) = (12,50,1,2)                              (0.2)
```

one has

```text
Q - (47/50)V = -4448279/50000000 < 0.                    (0.3)
```

Hence if `k_*` denotes the best global homogeneous constant in `Q >= k V`, then purely from exact rational certificates

```text
31/33 <= k_* < 47/50.                                    (0.4)
```

This is already a very tight bracket:

```text
(47/50)/(31/33) = 1551/1550 = 1 + 1/1550.               (0.5)
```

So after adopting `31/33`, **less than 0.06452% multiplicative headroom remains** in the global source-independent `Q/V` constant.  This gives a route-level stopping rule: further global coercivity optimization is unlikely to matter compared with residual/source-domain tightening.

Relative to `T-P5-033`, the improvement is exactly

```text
(31/33)/(93/100) = 100/99.                               (0.6)
```

Thus every downstream capacity controlled linearly by this coercivity constant gains exactly `100/99`, about 1.0101%, with no new source premise.

---

## 1. Exact quadratic forms

Use exactly the `T-P5-033` matrices

```text
M = diag(350003/3000000, 200739/4000000),
D = diag(4/5, 13/20),
K = [[3/4,    -3/400],
     [-3/400, 29/50]],
A = [[0, 1/400],
     [-1/400, 0]].                                        (1.1)
```

For `x=(x4,x5)` and `y=(y4,y5)`,

```text
V := (1/2)y^T M y + (1/2)x^T K x + x^T M y + (1/2)x^T D x,
Q := y^T(D-M)y + x^T K x - y^T A x.                      (1.2)
```

The derivative identity remains unchanged:

```text
V' = -Q - (x+y)^T l.                                     (1.3)
```

This child changes only the exact `Q -> V` coercivity constant.

---

## 2. Matrix of `Q-(31/33)V`

In coordinate order

```text
z = (x4,x5,y4,y5),
```

the symmetric quadratic-form matrix `H31` satisfying

```text
z^T H31 z = Q - (31/33)V
```

is

```text
H31 =
[[ 29/1320,              -7/1760,              -10850093/198000000,     1/800],
 [ -7/1760,               1/440,                -1/800,                  -188573/8000000],
 [ -10850093/198000000,  -1/800,                 124449709/198000000,     0],
 [ 1/800,                 -188573/8000000,       0,                       4609949/8000000 ]]. (2.1)
```

For reference, its leading principal minors are all strictly positive:

```text
29/1320,
317/9292800,
60533356003619/4312440000000000000,
61653484662773374020014731/
  27599616000000000000000000000000.                      (2.2)
```

The proof below does not need to trust a numerical Sylvester/eigenvalue call; (2.2) only explains why the exact completion succeeds.

---

## 3. Exact four-square identity

Define the four rational linear forms

```text
F1 := (4350000*x4 - 787500*x5 - 10850093*y4 + 247500*y5)
      / 4350000,

F2 := (11887500*x5 - 85520651*y4 - 178731861*y5)
      / 11887500,

F3 := (3874134784231616*y4 - 1551880143101277*y5)
      / 3874134784231616,

F4 := y5.                                                  (3.1)
```

Then direct exact rational expansion gives

```text
Q - (31/33)V
 = (29/1320) * F1^2
 + (317/204160) * F2^2
 + (60533356003619/147107812500000) * F3^2
 + (61653484662773374020014731/
    387413478423161600000000000) * F4^2.                 (3.2)
```

Every coefficient in (3.2) is strictly positive. Therefore

```text
Q - (31/33)V >= 0,                                       (3.3)
```

which proves (0.1).

An equivalent integer-linear-form version, convenient for a `ring` proof, is

```text
Q - (31/33)V
 = (4350000*x4 - 787500*x5 - 10850093*y4 + 247500*y5)^2
     / 861300000000000

 + (11887500*x5 - 85520651*y4 - 178731861*y5)^2
     / 91010700000000000

 + (3874134784231616*y4 - 1551880143101277*y5)^2
     / 36474591580062241478400000000000

 + (61653484662773374020014731/
    387413478423161600000000000) * y5^2.                 (3.4)
```

Thus the trusted mathematical core can remain “exact identity by `ring` + nonnegativity of four squares”.  No matrix inverse, eigenvalue API, or irrational coefficient is required.

---

## 4. Explicit `47/50` failure

At

```text
z0 := (12,50,1,2),                                       (4.1)
```

exact substitution gives

```text
V(z0) = 4953531571/3000000 > 0,
Q(z0) = 232802639/150000,                                 (4.2)
```

and hence

```text
Q(z0) - (47/50)V(z0)
 = -4448279/50000000
 < 0.                                                     (4.3)
```

Therefore the global theorem

```text
forall z, Q(z) >= (47/50)V(z)                             (4.4)
```

is false.

This is stronger than a floating determinant/eigenvalue warning because it is a concrete exact rational counterexample.

There is also a useful domain observation. Both `Q` and `V` are homogeneous quadratic forms, so for every real `t`,

```text
Q(t z0) - (47/50)V(t z0)
 = t^2 * (-4448279/50000000).                            (4.5)
```

Consequently, for every `t != 0` the same strict failure persists.  Hence any state domain containing sufficiently small nonzero multiples of `z0`—in particular any full-dimensional neighborhood/box around the origin in these four coordinates—cannot support the uniform `47/50` constant either.  A lower-dimensional or otherwise direction-excluding physical domain could still admit a larger domain-specific constant; this review does not rule that out.

---

## 5. Near-sharpness consequence

Let `Kglobal` be the set of real constants `k` for which

```text
forall z, k*V(z) <= Q(z).                                 (5.1)
```

Section 3 proves `31/33 in Kglobal`; section 4 proves `47/50 notin Kglobal`.
Therefore any best/supremal global coefficient lies in the bracket (0.4).

The multiplicative gap between the proved lower certificate and the explicit failure point is exactly

```text
(47/50) / (31/33)
 = (47*33)/(50*31)
 = 1551/1550.                                             (5.2)
```

So even a mathematically optimal global constant below `47/50` can improve the `31/33` certificate by **strictly less than `1/1550` in relative terms**.

This is the main route-selection conclusion of the child: after `31/33`, the dominant remaining work should be the residual/source/coverage terms rather than continued global `Q/V` constant hunting, unless a downstream domain-specific anisotropic restriction becomes available.

---

## 6. Updated residual-coupled decay

Reuse unchanged `T-P5-019/033` data

```text
5 ||x+y||^2 <= 17 Q.                                     (6.1)
```

The same half-Young step gives

```text
|(x+y)^T l| <= (1/2)Q + (17/10)||l||^2.                 (6.2)
```

Combining (1.3), (6.2), and `Q >= (31/33)V` yields

```text
V' <= -(31/66)V + (17/10)||l||^2.                        (6.3)
```

For a constant cap `||l||^2 <= L2`, the ultimate coefficient is now

```text
(17/10)/(31/66) = 561/155.                               (6.4)
```

At a first-exit boundary `V=Vstar`, strict inwardness follows from the division-free gate

```text
561 L2 < 155 Vstar.                                       (6.5)
```

For the existing quarter-energy choice `Vstar=1/4`, this is

```text
2244 L2 < 155,                                            (6.6)
```

i.e.

```text
L2 < 155/2244.                                            (6.7)
```

Compared with `T-P5-033`'s `L2 < 93/1360`, the admitted residual-square budget improves by exactly

```text
(155/2244)/(93/1360) = 100/99.                           (6.8)
```

---

## 7. Updated incremental parameter tube

Under the existing incremental residual premise

```text
||Dl||^2 <= mu*Vd + nu*dc^2,
mu >= 0,
nu >= 0,                                                  (7.1)
```

the same calculation becomes

```text
Vd'
 <= -[(31/66)-(17/10)mu] Vd
    + (17/10)nu dc^2.                                     (7.2)
```

At the already-used tube boundary

```text
Vd = (1/12) dc^2,                                         (7.3)
```

strict inwardness is exactly implied by

```text
561 mu + 6732 nu < 155.                                  (7.4)
```

This is again a factor `100/99` enlargement over the corresponding `93/100` coercivity budget.

If the `T-P5-031` bridge supplies

```text
mu = U+p,
nu = W+q,
p*q >= U*W,
p,q,U,W >= 0,                                             (7.5)
```

then the new rational checker target is simply

```text
561(U+p) + 6732(W+q) < 155.                              (7.6)
```

A pre-search obstruction can be written with

```text
R31 := 155 - 561U - 6732W.                               (7.7)
```

Strict real slack feasibility in this aggregated bridge requires

```text
R31 > 0,
R31^2 > 15106608 U W.                                    (7.8)
```

As before, a trusted checker need not use a square root: it can output rational `p,q` and verify (7.5)-(7.6) directly.

---

## 8. Suggested Lean theorem decomposition

The smallest useful source-independent additions are:

### `block45_Q_minus_31_33_V_four_square`

Use the exact scalar definitions already present in the `T-P5-033` sidecar and prove the identity (3.4) by `ring`.

### `block45_Q_ge_31_33_V`

From the previous identity, prove

```text
(31/33 : Real) * V45 x4 x5 y4 y5
  <= Q45 x4 x5 y4 y5.                                    (8.1)
```

Only square nonnegativity and positive rational coefficients are needed.

### `block45_47_50_counterexample`

Prove by exact normalization that

```text
Q45 12 50 1 2 - (47/50 : Real) * V45 12 50 1 2
  = -4448279/50000000.                                    (8.2)
```

and therefore the `47/50` universal inequality is false.

### `block45_47_50_counterexample_scaled`

For arbitrary `t`, prove the homogeneous identity

```text
Q45 (12*t) (50*t) t (2*t)
 - (47/50 : Real) * V45 (12*t) (50*t) t (2*t)
 = -(4448279/50000000) * t^2.                            (8.3)
```

This is the cleanest local-domain obstruction consumer.

### downstream arithmetic corollaries

Formalize only if useful:

```text
Vdot <= -(31/66)V + (17/10)L2,
561*L2 < 155*Vstar,
561*mu + 6732*nu < 155.                                  (8.4)
```

These are source-independent arithmetic consumers and must not manufacture the physical residual premises.

---

## 9. Boundaries / non-claims

1. `31/33` is proved globally for exactly the same rational `V,Q` definitions as `T-P5-033`; it is not a source-binding theorem for a different storage or different mass/stiffness normalization.
2. The `47/50` counterexample is a global homogeneous obstruction. A domain that excludes the counterexample direction may admit a better **domain-specific** constant.
3. No exact optimal generalized eigenvalue is claimed. The only near-optimality statement is the rigorous rational bracket `31/33 <= k_* < 47/50`.
4. No Float64/solve/controller residual bound, source Jacobian gain, flowpipe/first-exit coverage, ODE existence, true-DH identity, provenance, receipt, registry, P5/P8/M4 admission, or theorem promotion is performed here.
5. `T-P5-034` remains `pending` until independently validated/harvested.

The substantive conclusion is mathematical: the global block-(4,5) coercivity bottleneck is essentially exhausted.  The next material gains should come from tightening the residual/source bridge or exploiting a genuinely smaller physical domain, not from another round of unconstrained global `Q/V` constant tuning.