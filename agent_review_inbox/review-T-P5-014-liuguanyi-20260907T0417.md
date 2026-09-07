---
kind: review_result
review_id: review-T-P5-014-liuguanyi-20260907T0417
task_id: T-P5-014
source_agent: 柳冠一
claimed_at: 2026-09-07T04:05:00-06:00
created_at: 2026-09-07T04:17:00-06:00
inspected_commit: eeca1ab9dcbf1137d35811849dae4d677c1e2322
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_weighted_dual_coordinate_adapter_then_source_bind_runtime_remainders_in_generalized_force_coordinates
---

# T-P5-014 — weighted-dual execution-remainder adapter and coordinate-transport boundary

## Scope

`T-P5-013` gives a clean finite-horizon energy consumer for a genuine
nonconservative execution remainder `r`: with

```text
A(v) = v^T D v,
R_D(r) = r^T D^{-1} r,
```

one charges

```text
-g_R A + r^T v <= Rbar/(4 g_R)
```

whenever `R_D(r) <= Rbar`.  The remaining source/interface question is not the
energy inequality itself; it is how a checker that naturally reports
componentwise, Euclidean, normalized-coordinate, controller, solve, or IEEE
force errors can soundly produce this **weighted dual generalized-force cap**.

This review supplies that bridge.  It also isolates two sharp failure
boundaries:

1. a nonzero uniform force-error cap gives an **additive finite-horizon work
   budget**, but cannot in general be promoted to a velocity-relative damping
   bound near equilibrium;
2. if the damping quadratic has an undamped direction, a remainder component in
   that direction cannot be charged by the damping dual norm at all.

No numerical source interval is claimed.  This does not take over
`T-P5-013`'s finite-horizon barrier, `S_F`, `Hbar`, `W_min`, source/IEEE
execution tracing, P8 ramp-domain coverage, validation, provenance, admission,
or P5/M4 closure.

## 1. Exact diagonal weighted-dual bridge

Start in the generalized-force coordinates used by the mechanical power
pairing.  Let

```text
d_i > 0,
A(v) := sum_i d_i v_i^2,
R_D(r) := sum_i r_i^2 / d_i,
P(r,v) := sum_i r_i v_i.                                    (1)
```

Then

```text
P(r,v)^2 <= R_D(r) A(v).                                    (2)
```

This is ordinary weighted Cauchy, but there is a useful square-root-free
identity behind it:

```text
A(v) R_D(r) - P(r,v)^2
 = sum_{i<j} (d_i v_i r_j - d_j v_j r_i)^2 / (d_i d_j)
 >= 0.                                                       (3)
```

Hence the constant `1` in (2) is sharp.  Equality is attained whenever

```text
r_i = lambda d_i v_i                                       (4)
```

for a common scalar `lambda`.

Equation (3) is useful for formalization because the mathematical content does
not depend on a matrix square root.  The source-facing arithmetic below can
also be kept completely rational whenever the `d_i` and source bounds are
rational.

## 2. Componentwise source intervals -> exact dual cap

Suppose the source/checker proves, in the **same generalized-force
coordinates**, that

```text
|r_i| <= eps_i.                                             (5)
```

Then immediately

```text
R_D(r) <= sum_i eps_i^2 / d_i =: Rbar_box.                  (6)
```

Thus the exact division-free P5-013 rate-budget target is

```text
sum_i eps_i^2 / d_i <= 4 g_R B_R.                          (7)
```

After multiplying by a common positive denominator this becomes a pure
rational polynomial inequality.  There is no need to first collapse the force
box to an unrelated Euclidean norm.

For several execution sources already intervalized in the same force
coordinates, for example

```text
r = r_ctrl + r_solve + r_mass + r_C + r_G,                  (8)
```

with component caps `eps_{j,i}`, the direct worst-case box is

```text
|r_i| <= sum_j eps_{j,i},
R_D(r) <= sum_i (sum_j eps_{j,i})^2 / d_i.                  (9)
```

This is generally preferable to separately norming every source and then
adding coarse scalar norms, because the coordinate weights `1/d_i` are kept to
the end.

## 3. Implementation normalization must be transported explicitly

A common source artifact is not `r` itself but a raw/normalized error vector
`e`.  Let the actual generalized-force remainder be

```text
r = J e.                                                     (10)
```

For a positive-definite damping matrix `D`, the exact relation is

```text
R_D(r)
 = e^T (J^T D^{-1} J) e.                                   (11)
```

Therefore a Euclidean source bound

```text
e^T e <= Ebar                                               (12)
```

is sufficient only together with a certified metric-comparison constant
`lambda` satisfying

```text
J^T D^{-1} J <= lambda I                                    (13)
```

in Loewner order.  Then

```text
R_D(r) <= lambda Ebar.                                      (14)
```

This is the precise missing statement behind the warning in `T-P5-013` that a
uniform force norm in unrelated coordinates is not automatically the required
dual quantity.  The Euclidean norm is usable once the coordinate map and its
metric comparison are explicit; without `J`, there is no sound conversion.

### 3.1 Diagonal normalization

If

```text
J = diag(s_i),
D = diag(d_i),                                               (15)
```

then

```text
R_D(J e) = sum_i (s_i^2/d_i) e_i^2.                         (16)
```

Consequently, from an `l2` cap

```text
sum_i e_i^2 <= Ebar                                         (17)
```

we obtain the sharp constant

```text
lambda_diag := max_i (s_i^2/d_i),
R_D(J e) <= lambda_diag Ebar.                               (18)
```

The constant in (18) is sharp: choose `e` supported on a coordinate attaining
the maximum.

From a raw component box `|e_i| <= eta_i`, the tighter direct bound is

```text
R_D(J e) <= sum_i (s_i^2/d_i) eta_i^2.                      (19)
```

This is the preferred adapter when the source checker already has per-channel
intervals.

## 4. Power-dual coordinate changes preserve the dual quantity exactly

There is an important distinction between an arbitrary implementation scaling
(10) and a genuine change of generalized coordinates.

Let the velocity coordinates change by an invertible matrix `T`:

```text
v = T vhat.                                                  (20)
```

To preserve mechanical power, the generalized force covector and damping must
transform as

```text
rhat = T^T r,
Dhat = T^T D T.                                              (21)
```

Then two exact invariances hold:

```text
r^T v = rhat^T vhat,                                        (22)

v^T D v = vhat^T Dhat vhat,                                 (23)

r^T D^{-1} r = rhat^T Dhat^{-1} rhat.                       (24)
```

Thus the weighted dual quantity is coordinate-invariant **when force,
velocity, and damping are transported as a power-dual triple**.  If an
implementation reports a residual after only scaling the force vector while
leaving the consumer's damping metric unchanged, that is not such a coordinate
change; it is case (10), and the factor `J^T D^{-1}J` must be retained.

This gives a clean typed-interface rule:

```text
mechanical coordinate transform:
    transport (v,r,D) together -> exact invariance;
implementation normalization only:
    record J explicitly -> metric comparison required.
```

It prevents the normalization mistake already encountered on the P4 side from
reappearing in the P5 energy consumer.

## 5. Combining independently bounded dual remainders without square roots

Sometimes the checker cannot form the total interval vector before emitting
separate certified dual caps

```text
R_D(r_j) <= Rbar_j.                                         (25)
```

Let positive rational weights `theta_j` satisfy

```text
theta_j > 0,
sum_j theta_j = 1.                                          (26)
```

Weighted convexity/Cauchy gives

```text
R_D(sum_j r_j)
 <= sum_j R_D(r_j) / theta_j
 <= sum_j Rbar_j / theta_j.                                 (27)
```

For `m` sources, the equal-weight choice `theta_j=1/m` gives the simple
square-root-free fallback

```text
R_D(sum_j r_j) <= m * sum_j Rbar_j.                         (28)
```

This is not always sharp; (9) is better when a common coordinatewise interval
ledger exists.  But (27) is a sound composition theorem that lets independent
source checkers combine without introducing square roots into the final
certificate.  Rational `theta_j` may be optimized later without changing the
energy theorem.

## 6. Additive dual cap versus relative damping: exact failure boundary

A uniform runtime cap

```text
R_D(r) <= Rbar                                               (29)
```

is fully useful for the finite-horizon theorem of `T-P5-013`.  Combining (2)
with completion of the square gives, for every `g_R>0`,

```text
-g_R A(v) + r^T v <= Rbar/(4 g_R).                          (30)
```

So a fixed Float64/controller/solve error may be charged as an **additive
energy-rate budget**.

What (29) does *not* give is a homogeneous estimate

```text
|r^T v| <= gamma A(v)                                       (31)
```

uniformly near `v=0` when `r` can remain nonzero.

### Sharp counterexample

Fix any nonzero `r` and positive diagonal `D`.  Let

```text
v(t) := t D^{-1} r,    t>0.                                 (32)
```

Then

```text
r^T v(t) = t R_D(r),
A(v(t))   = t^2 R_D(r).                                     (33)
```

For any finite `gamma>0`, choosing `0<t<1/gamma` gives

```text
|r^T v(t)| > gamma A(v(t)).                                 (34)
```

Hence a nonzero reference/runtime bias cannot be silently moved into a
velocity-relative damping budget.  It must either be extracted as conservative
storage, proved to vanish proportionally to the dissipative state, or paid via
the additive `B_R` budget in `T-P5-013`.

The exact relative condition is instead something like

```text
R_D(r(v)) <= gamma^2 A(v).                                  (35)
```

Then (2) gives

```text
(r^T v)^2 <= gamma^2 A(v)^2,                                (36)
```

and for `gamma>=0`, `A>=0`,

```text
|r^T v| <= gamma A(v).                                      (37)
```

A source checker can establish (35) componentwise.  For diagonal `D`, if
nonnegative `kappa_i` satisfy

```text
r_i^2 <= kappa_i d_i A(v),                                  (38)
```

then

```text
R_D(r) <= (sum_i kappa_i) A(v).                             (39)
```

Thus `sum_i kappa_i <= gamma^2` is a division-free relative-damping target.
Merely proving `r(0)=0` is not enough; as in `T-P4-015`, a quantitative
increment/Lipschitz estimate is required.

## 7. Undamped-direction obstruction

`T-P5-013` assumes `D` is positive definite.  That assumption is not cosmetic.
For a diagonal positive-semidefinite damping form with some `d_k=0`, if a
remainder can have

```text
r_k != 0,                                                    (40)
```

then taking velocity only in coordinate `k` yields

```text
A(v)=0,
r^T v != 0.                                                 (41)
```

Therefore no finite constant `C` can satisfy

```text
(r^T v)^2 <= C A(v)                                         (42)
```

for all velocities.

For semidefinite damping the correct general condition is that `r` lie in the
range of `D` (equivalently, be orthogonal to `ker D` for symmetric `D`), after
which a Moore-Penrose/pseudodual quantity may be used on the damped subspace.
For the current P5 consumer the simpler contract is preferable:

```text
all residual directions charged to Rbar must have certified d_i>0;
otherwise route the undamped component to a different positive reserve or
redesign the storage/dissipation metric.                                    (43)
```

This should be checked before any source norm is accepted as a dual cap.

## 8. Direct source-facing instantiation of T-P5-013

The useful output of this child is a short adapter chain.  Suppose a checker
returns raw execution error `e`, a normalization map `J`, and a rational bound
`Ebar`.  If it also certifies

```text
e^T e <= Ebar,
J^T D^{-1} J <= lambda I,                                   (44)
```

then set

```text
Rbar := lambda Ebar.                                        (45)
```

The P5-013 division-free rate condition becomes simply

```text
lambda Ebar <= 4 g_R B_R.                                  (46)
```

For a diagonal source box the sharper replacement is

```text
sum_i (s_i^2/d_i) eta_i^2 <= 4 g_R B_R.                    (47)
```

Then `T-P5-013` may use `B_R` directly in its finite-horizon headroom condition

```text
Z0 + T*(Hbar+B_R) < Zstar.                                  (48)
```

This makes the layer boundary explicit:

```text
source/IEEE/controller/solve intervals
  -> actual generalized-force coordinates (record J)
  -> weighted dual cap Rbar via (6), (14), (19), or (27)
  -> rate budget Rbar <= 4 g_R B_R
  -> T-P5-013 finite-horizon energy barrier.
```

A uniform nonzero error is therefore **not** an obstruction to finite-horizon
closure; it is only an obstruction to pretending that the error is purely
relative damping.

## 9. Lean-friendly theorem decomposition

The first sidecar should avoid a heavy matrix inverse API and formalize the
diagonal finite-family interface used by a rational checker.

```lean
-- Diagonal weighted Cauchy, square-only consumer.
theorem weighted_dual_cauchy_diag
    {n : Nat} (d r v : Fin n -> R)
    (hd : forall i, 0 < d i) :
    (sum i, r i * v i)^2 <=
      (sum i, (r i)^2 / d i) * (sum i, d i * (v i)^2)
```

```lean
-- Component interval -> weighted dual cap.
theorem box_to_weighted_dual
    {n : Nat} (d r eps : Fin n -> R)
    (hd : forall i, 0 < d i)
    (hr : forall i, |r i| <= eps i) :
    (sum i, (r i)^2 / d i) <= sum i, (eps i)^2 / d i
```

```lean
-- Diagonal implementation normalization.
theorem diagonal_normalization_dual_identity
    {n : Nat} (d s e : Fin n -> R)
    (hd : forall i, 0 < d i) :
    weightedDual d (fun i => s i * e i)
      = sum i, (s i)^2 * (e i)^2 / d i
```

```lean
-- Coordinatewise relative budgets -> global relative dual budget.
theorem local_relative_to_dual
    {n : Nat} (d r kappa : Fin n -> R) (A : R)
    (hd : forall i, 0 < d i)
    (hk : forall i, 0 <= kappa i)
    (hr : forall i, (r i)^2 <= kappa i * d i * A) :
    weightedDual d r <= (sum i, kappa i) * A
```

```lean
-- Fixed nonzero force bias cannot satisfy a universal relative damping bound.
theorem fixed_bias_not_uniformly_relative
    {n : Nat} (d r : Fin n -> R)
    (hd : forall i, 0 < d i)
    (hr : exists i, r i != 0)
    (gamma : R) (hgamma : 0 <= gamma) :
    exists v,
      gamma * damping d v < |power r v|
```

For the last theorem, a finite-dimensional diagonal witness
`v=t*(r/d)` avoids matrix inversion and exposes the exact obstruction.  A
separate generic matrix theorem for (11)/(24) can be added only if the source
adapter actually needs a non-diagonal coordinate transform.

## 10. Remaining blockers and recommended next action

- The source lane still has to identify the actual generalized-force coordinate
  map `J` for each controller/IEEE/solve remainder.  This review does not infer
  that map from names or units.
- The actual damping coefficients/matrix used by the P5 energy ledger must be
  source-bound and shown positive in every remainder direction charged through
  this dual metric.
- Numerical `eta_i`, `Ebar`, or per-source `Rbar_j` values remain to be generated
  on the same P8 ramp-graph domain used by `S_F`, `Hbar`, and `W_min`.
- If the checker only has independent scalar dual caps, use (27); if it has
  coordinate intervals, aggregate intervals first and use (9), which is tighter.
- Constant nonzero execution bias should go through the additive `B_R` branch of
  `T-P5-013`, not through a fabricated relative-damping coefficient.

Recommended next action:

1. formalization lane: implement `weighted_dual_cauchy_diag`,
   `box_to_weighted_dual`, `diagonal_normalization_dual_identity`, and the
   relative-budget corollary as a small portable sidecar;
2. source/checker lane: emit the actual force-coordinate transform `J` and
   damping coefficients, then produce the rational left-hand side of (47) or a
   certified `lambda Ebar` from (46);
3. only after that, feed the resulting `Rbar` into `T-P5-013`'s finite-horizon
   barrier.

This result remains `pending`.  It is an interface theorem package, not source
authentication, P5 closure, P8 closure, M4 closure, validation, or admission.
