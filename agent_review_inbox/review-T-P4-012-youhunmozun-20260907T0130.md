---
kind: review_result
review_id: review-T-P4-012-youhunmozun-20260907T0130
task_id: T-P4-012
source_agent: 幽魂魔尊
claimed_at: 2026-09-07T01:23:00-06:00
created_at: 2026-09-07T01:30:00-06:00
inspected_commit: 233187bd15b973d1ec14f5261189f7930bed94ed
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_mass_block_remote_action_transfer_then_bind_distal_acceleration_energy_on_P8_domain
---

# T-P4-012 — remote `M_BD a_D` mass-metric transfer, sharp constant, and a no-entrywise-bound P4 seam

## Scope

`T-P4-008` proves that the true block force residual contains the remote term

```text
r_remote := M_BD(q) a_D,
```

and that no theorem depending only on local `(q4,q5,v4,v5,w)` can represent or bound that term unless an additional distal/full-state contract is supplied. This review attacks the next mathematical question:

> Can the special fact that `M` is a mechanical mass matrix turn the unknown remote force into a controlled energy quantity without separately bounding every entry of `M_BD`?

The answer is yes. Positive-semidefiniteness of the full DH mass matrix gives a sharp constant-one contraction from distal acceleration energy into the local mass dual norm. This produces a substantially shorter P4 obligation: bind one distal quadratic quantity `a_D^T M_DD a_D` (or its unregularized analogue), rather than six/eight separate cross-block entry envelopes.

This is exact-real mathematics only. It does not assert Float64 PSD, source-semantic equality, P8 coverage, P4 admission, provenance, or registry promotion.

## Inputs inspected

- `review-T-P4-008-liuguanyi-20260907T0120.md`: exact residual decomposition and the `+ M_BD a_D` obstruction; it also corrects the force-coordinate `kc` term to `(q5/100,q4/200)` after the `I_B` normalization.
- `review-T-P3-010-guyuefangyuan-20260907T0035.md`: exact-real block-(4,5) formula, positivity, and diagonal bounds.
- `examples/routeb_source_binding_audit/snapshots/original_target/dhport_lib.jl:31-60`: the mass matrix is built as a sum of translational and rotational Gram terms plus a diagonal regularizer.
- `review-T-P4-011-kuangmanmozun-20260907T0046.md`: the source-independent `c=1/4` sharp-Schur residual consumer, while noting that its original `kc` vector was in raw PMI-`f` coordinates rather than the force coordinate corrected by `T-P4-008`.

## 1. Exact block notation

Work first with the **unregularized exact-real** mechanical mass matrix

```text
Mhat(q) = [[B(q), E(q)],
           [E(q)^T, D(q)]],
```

where `B` is the local block for joints `(4,5)` and `D` is the complementary distal block. The deployed diagonal regularizer does not change the off-diagonal block, so for

```text
M(q) = Mhat(q) + eps I,   eps = 10^-6,
```

we still have

```text
M_BD(q) = E(q).
```

The exact-real DH/Jacobian construction is a sum of terms

```text
m_i Jv_i^T Jv_i + Jw_i^T R_i I_i R_i^T Jw_i,
```

with positive masses/inertias. Hence

```text
Mhat(q) >= 0                                                   (1)
```

as a quadratic form.

For block `(4,5)`, `T-P3-010` further gives

```text
B(q)=diag(b4(q5),b5),

b4(q5)=7/60 + (147/800000) sin(q5)^2,
b5     =40147/800000,
```

so `B(q)>0` for every real `q`.

Define the distal acceleration energy and remote local force

```text
E_D(a_D) := a_D^T D a_D,
r := E a_D.                                                   (2)
```

## 2. Sharp remote-action dual-norm theorem

Because the full block matrix (1) is PSD and `B>0`, its Schur complement is PSD:

```text
D - E^T B^(-1) E >= 0.                                       (3)
```

Therefore for every distal acceleration `a_D`,

```text
r^T B^(-1) r
 = a_D^T E^T B^(-1) E a_D
 <= a_D^T D a_D
 = E_D(a_D).                                                  (4)
```

This is the key theorem:

> **The remote force is a contraction of distal acceleration energy in the local mass dual norm, with constant exactly 1.**

No entrywise `M_BD` bound appears.

### Sharpness

The constant `1` cannot be improved from block-PSD information alone. In the scalar family

```text
M_c = [[1,c],[c,1]],    0<c<1,
```

we have `M_c>0`, while for `a_D=1`,

```text
r^2/B = c^2,
E_D   = 1.
```

The ratio tends to `1` as `c -> 1`. Thus any universal claim

```text
r^T B^(-1) r <= k E_D   with k<1
```

is false without extra structural information.

## 3. Even cleaner: scaled block-PSD absorption without inverses

For P4, one can avoid inverses completely. From PSD of `Mhat`, for arbitrary local vector `x`, distal vector `a_D`, and scalar `theta>0`, evaluate the full quadratic form at `(theta x, a_D)`:

```text
0 <= theta^2 x^T B x
     + 2 theta x^T E a_D
     + a_D^T D a_D.
```

After division by `theta`,

```text
2 x^T r
 >= - theta x^T B x - (1/theta) E_D(a_D).                    (5)
```

The opposite sign follows by replacing `a_D` with `-a_D`, hence

```text
2 |x^T r|
 <= theta x^T B x + (1/theta) E_D(a_D).                      (6)
```

Now suppose the actual P4 local positive quadratic satisfies a metric comparison

```text
P(x) >= theta x^T B x                                        (7)
```

on the same domain. Then (5) gives

```text
P(x) + 2 x^T r + d y^2
 >= d y^2 - (1/theta) E_D(a_D).                              (8)
```

Therefore the **single distal-energy condition**

```text
E_D(a_D) <= theta d y^2                                      (9)
```

is sufficient for complete absorption of the remote action:

```text
P(x) + 2 x^T M_BD a_D + d y^2 >= 0.                         (10)
```

This is the shortest useful bridge from the physical mass geometry into a Schur/PMI consumer. It replaces an entrywise force-envelope task by two scalar/matrix comparisons:

```text
P >= theta B,
E_D <= theta d y^2.
```

If the P4 positive block is literally `B`, take `theta=1`; then the sharp condition is simply `E_D <= d y^2`.

## 4. Regularizer-aware strengthening

Write the deployed exact-real regularized blocks as

```text
B_eps = B + eps I,
D_eps = D + eps I,
eps = 1/1000000.
```

The remote block `E` is unchanged. Since `B_eps >= B > 0`,

```text
B_eps^(-1) <= B^(-1).
```

Combining with (4),

```text
r^T B_eps^(-1) r
 <= E_D(a_D)
 = a_D^T D_eps a_D - eps ||a_D||^2.                         (11)
```

Thus the diagonal mass regularizer is not an additional remote-force bias. In this particular Schur channel it actually creates a (small) strict margin of

```text
eps ||a_D||^2.
```

This is consistent with the energy-ledger observation in `T-P5-008` that the mass regularizer should be absorbed into storage rather than charged as a generic residual.

## 5. Exact component bounds from the newly derived `(4,5)` block

Equation (4) also yields coordinate bounds without estimating `E=M_BD` entrywise. For any coordinate unit vector `e_i`, weighted Cauchy gives

```text
r_i^2 <= B_ii * (r^T B^(-1) r) <= B_ii * E_D.                (12)
```

For the exact-real unregularized block from `T-P3-010`,

```text
B44(q) <= U4 := 280441/2400000 ~= 0.1168504166667,
B55(q)  = U5 := 40147/800000   ~= 0.05018375.                (13)
```

Hence globally in the exact-real geometry,

```text
r4^2 <= (280441/2400000) E_D,
r5^2 <= (40147/800000)   E_D.                                (14)
```

These are exact rational constants and are much better typed than a generic Euclidean `||M_BD||` estimate: they preserve generalized-force units and expose exactly which distal quadratic quantity must be bounded.

## 6. Concrete conditional seam with the corrected force-coordinate `kc`

`T-P4-008` shows that after the PMI normalization the actual force-coordinate `kc` terms are

```text
kc4 = q5/100,
kc5 = q4/200,                                                (15)
```

not the larger raw-`f` coefficients `q5/20,q4/20` used in the earlier arithmetic exploration.

Assume a future **force-coordinate** P4 adapter proves the same cross-coordinate map needed by the quarter residual theorem and, for the moment, charge only

```text
r_total = r_remote + r_kc.
```

### Channel 4

To fit

```text
|r_total,4| <= (1/4)|q5|,
```

the corrected `kc4` consumes `1/100`, leaving remote coefficient

```text
1/4 - 1/100 = 6/25.                                         (16)
```

By (14), a square-root-free sufficient condition is

```text
E_D <= gamma4 q5^2,
gamma4 := (6/25)^2 / U4
        = 138240/280441
        ~= 0.4929379085.                                    (17)
```

Indeed `U4*gamma4=(6/25)^2`, so `|r4|<=(6/25)|q5|`, and triangle inequality with (15) gives the quarter envelope.

### Channel 5

Here the corrected `kc5` consumes only `1/200`, leaving

```text
1/4 - 1/200 = 49/200.                                       (18)
```

A sufficient distal-energy condition is therefore

```text
E_D <= gamma5 q4^2,
gamma5 := (49/200)^2 / U5
        = 48020/40147
        ~= 1.1961043166.                                    (19)
```

These constants are not physical claims yet. They are **exact source targets**: if P8/source mathematics can prove the corresponding same-domain distal acceleration-energy inequality, then the remote action plus the corrected `kc` term fits the existing rational `c=1/4` force envelope before any other residual channel is charged.

### With an additional residual reserve

More generally, if another force contribution in channel `i` is already bounded by

```text
|r_other,i| <= beta_i |y_i|,
```

and `k_i` is the corrected `kc` coefficient (`1/100` or `1/200`), choose any rational `c_i>0` with

```text
k_i + beta_i + c_i <= 1/4.                                  (20)
```

Then it is enough to prove

```text
E_D <= (c_i^2/U_i) y_i^2.                                   (21)
```

This is the right bookkeeping interface for source lanes: each additional force term simply consumes linear coefficient reserve, while the remote action is certified through one distal quadratic energy bound.

## 7. Robust perturbation form for a future Float64/source adapter

The exact contraction (4) should not be silently applied to a rounded execution matrix if PSD/source equality has not been proved. However, there is a clean perturbative fallback.

Suppose the source-side remote block is

```text
E_exec = E + DeltaE
```

and on the same domain

```text
||DeltaE a_D|| <= delta ||a_D||,
B >= lambda I,   lambda>0.                                  (22)
```

For `r_exec=E_exec a_D` and any `eta>0`, weighted Young gives

```text
r_exec^T B^(-1) r_exec
 <= (1+eta) E_D
    + (1+1/eta) * (delta^2/lambda) * ||a_D||^2.              (23)
```

Thus an operation-level enclosure for the cross-block rounding error can be inserted as an explicit second-order term; it need not destroy the entire mass-metric route.

For block `(4,5)`, the exact-real global lower bound

```text
lambda = 40147/800000
```

is already available from `T-P3-010`. The still-open source problem is to provide a legitimate `delta` (and to keep any `B` perturbation separately accounted for), not to rerun a generic Schur search.

## 8. Failure boundaries ruled out

This review rules out / refines three routes:

1. **Entrywise `M_BD` bounding is not mathematically necessary.** Full mass PSD already gives the stronger invariant (4).
2. **Local-state-only closure is still impossible without a distal-energy contract.** The `T-P4-008` counterexample remains valid; (4) merely identifies the minimal extra quantity to control.
3. **No universal gain smaller than 1 can replace (4) using PSD alone.** The scalar `M_c` family proves sharpness, so effort should go into bounding `E_D`, exploiting extra DH sparsity, or comparing the P4 positive block with `B`, rather than trying to improve the abstract contraction constant.

## Lean-friendly theorem decomposition

A formalization lane can avoid matrix inverses first and prove the block-quadratic version.

```text
remote_scaled_cross_bound
  fullPSD : forall x a,
    0 <= QB(x) + 2*C(x,a) + QD(a)
  theta > 0
  -----------------------------------------------
  2*C(x,a) >= -theta*QB(x) - QD(a)/theta
```

Then the direct consumer:

```text
remote_schur_absorption
  fullPSD
  theta > 0
  P(x) >= theta*QB(x)
  QD(a) <= theta*d*y^2
  -----------------------------------------------
  0 <= P(x) + 2*C(x,a) + d*y^2.
```

A second finite-dimensional theorem may state the sharp inverse form

```text
M=[[B,E],[E^T,D]] >= 0, B>0, r=E*a
-----------------------------------
r^T B^{-1} r <= a^T D a.
```

For exact-rational downstream use, separate scalar corollaries should record

```text
U4 = 280441/2400000,
U5 = 40147/800000,
gamma4 = 138240/280441,
gamma5 = 48020/40147.
```

No source-specific object should be hidden in the definitions of these abstract lemmas.

## What remains open

- Deployed Float64 execution has not been proved equal to the exact-real PSD mass map; operation/interval error remains a source-semantic obligation.
- P8/source lane must still bound `a_D^T D a_D` (or a compatible upper surrogate) on the same covered domain.
- P4 must specify whether its positive quadratic block `P` is in generalized-force coordinates and prove the comparison `P >= theta B`; one must not identify the old scalar `p` with a mass entry by name alone.
- Other force residual terms in `T-P4-008` — `(M_BB-M0_BB)a_B`, `C_B`, gravity/reference mismatch, controller/solve effects — still need their own same-domain charges and no-double-counting ledger.
- The cross-coordinate `y <-> q_cross` adapter is still required if the scalar quarter-residual route is used.
- No P4/P8/M4 parent or registry entry is closed by this result.

## Recommended next action

1. Source/P8 math: target one bound on the distal acceleration energy `a_D^T D a_D` over the covered domain, rather than entrywise `M_BD` bounds.
2. P4 interface math: prove a metric comparison `P >= theta B` for the actual generalized-force Schur positive block. Then consume (9) directly; this is shorter and sharper than component-wise force envelopes.
3. If the existing scalar quarter consumer is retained, use the corrected force-coordinate coefficients and the explicit targets (17)/(19), reserving additional coefficient budget for the remaining residual terms.
4. Float64 lane: if exact PSD binding is unavailable, produce an explicit cross-block perturbation bound and use (23); do not assume rounded Gram assembly preserves the exact-real theorem automatically.

Admission remains `pending`; this is a mathematical hard-bottleneck reduction for 梁智炜 to harvest, not final integration or validation.
