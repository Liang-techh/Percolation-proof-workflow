---
kind: review_result
review_id: review-T-P5-010-youhunmozun-20260907T0026
task_id: T-P5-010
source_agent: 幽魂魔尊
claimed_at: 2026-09-07T00:20:00-06:00
created_at: 2026-09-07T00:26:00-06:00
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_cubic_power_small_gain_and_bind_fd_tensor_error
---

# T-P5-010 — central-FD Christoffel cubic-power small gain, local radius theorem, and global obstruction

## Scope

`T-P5-008` removes the mass regularizer and the frozen-potential gravity FD term from the residual ledger by changing storage, leaving the central-FD Christoffel mismatch as a structurally cubic power term. This review attacks the next hard mathematical question:

> Under what exact same-domain hypotheses can the cubic C-FD power be absorbed by the quadratic damping, and why is any global velocity-unbounded absorption claim impossible unless the cubic mismatch vanishes identically?

This is a source-independent mathematical continuation. It does not identify the frozen Fourier tensor with deployed DH, prove the FD tensor bound, establish flowpipe coverage, or make any admission/provenance claim.

Inspected inputs:

- `review-T-P5-008-honglianmozun-20260906T2348.md`: storage-renormalized P5 ledger and the cubic mismatch formula;
- `examples/routeb_source_binding_audit/snapshots/current_exact/ChristoffelPower.lean`: generic exact Christoffel power identity;
- `examples/routeb_supply_core/RouteBSupplyCore.lean`: damping coefficients
  `d = [13/10, 11/10, 19/20, 4/5, 13/20, 1/2]`.

## 1. Exact cubic object

Let

```text
DeltaT[k,i,j] := T[k,i,j] - Tfd[k,i,j].
```

By linearity of the already-proved Christoffel power identity, the C-FD power mismatch is exactly

```text
P_C(v)
 = 1/2 * sum_{k,i,j} DeltaT[k,i,j] * v_k * v_i * v_j.       (1)
```

Assume a same-domain pointwise tensor envelope

```text
|DeltaT[k,i,j]| <= mu[k,i,j],
mu[k,i,j] >= 0.                                               (2)
```

Then

```text
|P_C(v)|
 <= 1/2 * sum_{k,i,j} mu[k,i,j] |v_k v_i v_j|.               (3)
```

The relevant damping quadratic is

```text
A(v) := sum_i d_i v_i^2,   d_i>0.                             (4)
```

The P5 question is to establish `|P_C(v)| <= kappa_C A(v)` with `kappa_C<1` on the same covered state/velocity domain.

## 2. Global obstruction: a nonzero cubic can never be uniformly absorbed by quadratic damping on all velocities

This is an exact scaling obstruction, not a weakness of a particular inequality.

Let `C(v)` be any homogeneous cubic form and `A(v)` any positive-definite homogeneous quadratic form. Suppose there exists `v0` with

```text
C(v0) != 0.
```

For `t>0`, homogeneity gives

```text
|C(t v0)| = t^3 |C(v0)|,
A(t v0)   = t^2 A(v0).
```

Hence a putative global estimate

```text
|C(v)| <= kappa A(v)   for every v                           (5)
```

would imply

```text
t |C(v0)| <= kappa A(v0)
```

for every `t>0`, which fails once

```text
t > kappa A(v0)/|C(v0)|.                                     (6)
```

Therefore:

```text
[global quadratic absorption of a homogeneous cubic]
        ==> [the cubic form is identically zero].             (7)
```

Applied to C-FD: unless the derivative error tensor happens to have zero cubic contraction identically, **a velocity/sublevel/flowpipe bound is mathematically necessary**. Any future proof attempt that seeks a constant `kappa_C` on all `v in R^6` is a dead end.

A Lean-friendly obstruction theorem is:

```lean
theorem cubic_not_globally_quadratic_absorbable
    (C A : (Fin 6 -> R) -> R)
    (hcubic : forall t v, C (fun i => t*v i) = t^3 * C v)
    (hquad  : forall t v, A (fun i => t*v i) = t^2 * A v)
    (v0 : Fin 6 -> R) (hC0 : C v0 != 0) (hA0 : 0 < A v0)
    (kappa : R) :
    not (forall v, |C v| <= kappa * A v)
```

with the witness `t` chosen above (or an algebraically larger explicit positive `t`).

## 3. Coordinate-box reduction: cubic power becomes a quadratic form

Assume the same covered domain also supplies coordinate velocity radii

```text
|v_k| <= R_k,   R_k >= 0.                                    (8)
```

From (3),

```text
|P_C(v)|
 <= 1/2 * sum_{i,j} [sum_k mu[k,i,j] R_k] |v_i| |v_j|.       (9)
```

Define

```text
B_ij := 1/2 * sum_k mu[k,i,j] R_k,
H    := (B+B^T)/2,
x_i  := |v_i|.                                                (10)
```

Since `x^T B x = x^T H x`, equation (9) is

```text
|P_C(v)| <= x^T H x.                                         (11)
```

Thus the nonlinear cubic problem reduces exactly to a finite-dimensional quadratic small-gain condition after the velocity box is supplied.

Let `D=diag(d_i)`. A sufficient condition is the matrix inequality

```text
H <= kappa_C D                                                (12)
```

in quadratic-form order. Then

```text
|P_C(v)| <= kappa_C A(v).                                    (13)
```

If `kappa_C<1`, the C-FD term retains `(1-kappa_C)` of the damping before other residual channels are charged.

This is the cleanest interface between:

```text
P3/P8: tensor-error + velocity-domain bounds
                -> H
P5: H <= kappa_C D
                -> dissipative absorption.
```

No component-wise force-relative theorem `|e_C,i|<=rho_i|v_i|` is needed.

## 4. Rational/Lean-friendly diagonal certificate without eigenvalues or square roots

The matrix condition (12) can be discharged by a scaled Young certificate.
For any positive weights `a_i>0`, use

```text
2 x_i x_j <= (a_j/a_i) x_i^2 + (a_i/a_j) x_j^2.              (14)
```

Because `H` is symmetric,

```text
x^T H x
 <= sum_i q_i(a) x_i^2,                                      (15)
```

where

```text
q_i(a)
 := H_ii + sum_{j != i} H_ij * (a_j/a_i).                    (16)
```

Therefore the purely scalar conditions

```text
q_i(a) <= kappa_C d_i   for every i                           (17)
```

imply (13).

This is useful for formalization and exact-rational certification: one may choose rational positive `a_i`, prove six rational inequalities, and avoid a spectral/eigenvalue API. Choosing all `a_i=1` yields the coarser row-sum test

```text
sum_j H_ij <= kappa_C d_i.                                   (18)
```

The free `a_i` are not cosmetic: they allow damping-rich channels to absorb more cross-coupling and can materially improve over the unscaled row-sum bound.

Recommended theorem decomposition:

```lean
theorem cubic_box_to_quadratic
    (Delta mu : Fin 6 -> Fin 6 -> Fin 6 -> R)
    (R v : Fin 6 -> R)
    (hmu : forall k i j, |Delta k i j| <= mu k i j)
    (hmu0 : forall k i j, 0 <= mu k i j)
    (hR : forall k, |v k| <= R k)
    (hR0 : forall k, 0 <= R k) :
    |(1/2) * sum k,i,j, Delta k i j * v k*v i*v j|
      <= sum i,j, B mu R i j * |v i|*|v j|
```

followed by a separate `scaled_young_quadratic_absorption` theorem implementing (14)--(17).

## 5. Energy-sublevel alternative: one scalar squared certificate

If a coordinate box is inconvenient, the same cubic can be controlled directly by the damping energy.
Define

```text
Lambda
 := 1/4 * sum_{k,i,j} mu[k,i,j]^2/(d_k d_i d_j).              (19)
```

Weighted Cauchy-Schwarz gives

```text
|P_C(v)|^2 <= Lambda * A(v)^3.                               (20)
```

Reason: write each term as

```text
[mu/(2 sqrt(d_k d_i d_j))]
  * [sqrt(d_k)|v_k| sqrt(d_i)|v_i| sqrt(d_j)|v_j|],
```

then the squared norm of the second triple-index array factorizes exactly as

```text
(sum_k d_k v_k^2)(sum_i d_i v_i^2)(sum_j d_j v_j^2)
 = A(v)^3.
```

Consequently, on a damping sublevel

```text
A(v) <= R^2                                                   (21)
```

if

```text
Lambda * R^2 <= kappa_C^2,   kappa_C>=0,                     (22)
```

then

```text
|P_C(v)| <= kappa_C A(v).                                    (23)
```

The statement (20)+(22)->(23) can be formalized largely without explicit square roots; (20) is a squared inequality and the final step only compares nonnegative squares.

This is the natural consumer if P8/first-exit supplies an energy/sublevel radius rather than coordinatewise velocity radii.

## 6. Exact coarse scalar corollary for the current six damping coefficients

Suppose a simpler source theorem only gives

```text
mu[k,i,j] <= mu   for every k,i,j,
|v_k| <= V        for every k.                                (24)
```

Then from (3), first sum over `k` and use weighted Cauchy on the remaining two velocity sums:

```text
|P_C|
 <= (mu/2) * (sum_k |v_k|) * (sum_i |v_i|)^2
 <= (mu/2) * (6V) * S_d * A(v),                              (25)
```

where

```text
S_d := sum_i 1/d_i
     = 10/13 + 10/11 + 20/19 + 5/4 + 20/13 + 2
     = 81721/10868.                                           (26)
```

Hence

```text
|P_C| <= (245163/10868) * mu * V * A(v),                     (27)
```

with

```text
245163/10868 ~= 22.5582443872.                                (28)
```

So the coarse sufficient strict-absorption condition is

```text
(245163/10868) * mu * V < 1.                                 (29)
```

This is only a fallback scalar bound; the tensor/matrix certificate (12)/(17) should be preferred when anisotropic `mu[k,i,j]` values are available.

## 7. Combination with the relative-residual lane

After the storage renormalization of `T-P5-008`, suppose the zero-input derivative has the schematic form

```text
E_tilde_dot
 <= -A(v) + P_C(v) + P_rel(v) + P_bias(v).                    (30)
```

Assume

```text
|P_C(v)| <= kappa_C A(v),
P_rel(v)  <= kappa_R A(v),
kappa_C >= 0,
kappa_R >= 0,
kappa_C + kappa_R < 1.                                        (31)
```

Then

```text
E_tilde_dot
 <= -(1-kappa_C-kappa_R) A(v) + P_bias(v).                    (32)
```

Thus the correct P5 small-gain budget is **additive at the power level**:

```text
kappa_C + kappa_R < 1.                                       (33)
```

If the controller/solve bias lane proves `P_bias<=0` (or exact zero at zero input), strict damping follows for every nonzero velocity in the covered local domain. If only an absolute bias bound is available, (32) falls back to the P5-004 ultimate-bound architecture; no amount of cubic tuning fixes a genuine additive equilibrium bias.

This gives a clean composition theorem between the new C-FD cubic lane and the already-developed weighted relative-residual lane.

Lean-friendly scalar consumer:

```lean
theorem cubic_relative_small_gain
    (A PC PR PB dE kC kR : R)
    (hA : 0 <= A)
    (hkC : 0 <= kC) (hkR : 0 <= kR)
    (hgain : kC+kR < 1)
    (hE : dE <= -A + PC + PR + PB)
    (hPC : PC <= kC*A)
    (hPR : PR <= kR*A) :
    dE <= -(1-kC-kR)*A + PB
```

The strict-negative corollary should separately assume `0<A` and `PB<=0`.

## 8. Failure boundaries and next mathematical targets

This review rules out two tempting but wrong routes:

1. **Global C-FD absorption without a velocity bound:** impossible for any nonzero cubic mismatch by scaling (6).
2. **Trying to convert C-FD into a componentwise affine force-relative bound:** unnecessary and generally much stronger than the actual energy requirement. The power-level small-gain condition (12), (17), or (22) is the right interface.

Still open:

- a same-domain source theorem for `|DeltaT[k,i,j]| <= mu[k,i,j]` for the deployed central-FD mass derivatives (`T-P3-008`/source lane);
- a P8/first-exit velocity box `R_k` or energy radius `R` on exactly the same domain;
- exact rational evaluation of the six-by-six matrix `H` or scalar `Lambda` once `mu` and the domain radii are available;
- controller and Float64 solve power/bias closure from `T-P5-008`;
- physical source binding and final P5/M4 admission.

## Recommended next action

Once `T-P3-008` supplies a derivative-error tensor envelope, do **not** immediately collapse it to six force offsets. Feed it directly into (10) and compute the rational matrix `H` using the current P8 velocity box. Try the scaled certificate (17) first; only use the coarse scalar (29) if the tensor data are unavailable. If no bounded velocity domain can be supplied, stop: the scaling obstruction proves that global cubic absorption cannot close.

No Lean/checker/provenance command was run in this mathematical pass; formalization and independent validation remain separate lanes.
