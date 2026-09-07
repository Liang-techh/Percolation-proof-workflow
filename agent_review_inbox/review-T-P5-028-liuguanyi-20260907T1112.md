---
kind: review_result
review_id: review-T-P5-028-liuguanyi-20260907T1112
task_id: T-P5-028
source_agent: 柳冠一
agent: 柳冠一
claimed_at: 2026-09-07T11:00:00-06:00
created_at: 2026-09-07T11:12:00-06:00
inspected_commit: a3e00b66ae6c738d3f876b1efcf88ab0a2a67f65
continuation_of:
  - review-T-P5-022-liuguanyi-20260907T0820
  - review-T-P5-023-liuguanyi-20260907T0916
  - review-T-P5-025-liuguanyi-20260907T1020
related_reviews:
  - review-T-P5-026-guyuefangyuan-20260907T1031
  - review-T-P8-008-guyuefangyuan-20260907T0231
  - companion-T-P5-017-honglianmozun-20260907
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_sparse_moving_frame_difference_and_common_parameter_cancellation_then_use_it_as_source_S_or_direct_K_adapter
---

# T-P5-028 — exact moving-frame difference transport into the source Jacobian / `K_path` interface

## 0. Result in one sentence

The block-(4,5) moving frame used by the P5 energy lane has an exact sparse actual-minus-nominal transport into the P8/source coordinates.  At a fixed time, if actual and nominal trajectories use the **same ramp parameter `c`**, then the affine ramp center cancels completely:

```text
Delta q4 = Delta x4,
Delta q5 = Delta x5,
Delta v4 = Delta y4,
Delta v5 = Delta y5,
Delta w  = 0,
Delta c  = 0.
```

Therefore the `w/c` Jacobian columns cost exactly zero in the P5 centered gain, even if the residual is highly sensitive to `w/c`.  If the two compared states are allowed to have different `c`, then the correction has an explicit rank-one form `K_eff = K0 + kappa(T) ⊗ gamma` provided one proves `|Delta c| <= gamma · |Delta z|`.  Without common `c`, such a control, an enlarged consumer state, or an additive/transverse lane, a four-state centered-gain theorem is mathematically impossible whenever the residual varies along a fixed-`z` parameter fiber.

This is source-to-math interface mathematics only.  It does not certify any concrete Julia Jacobian/Float64 increment, source hash, cell chain, flowpipe coverage, P5/P8/M4 closure, or registry admission.

---

## 1. Inputs already established by the surrounding P5/P8 work

Use the block-(4,5) moving coordinates from the P5 moving-frame lane:

```text
x = q - h w - r c,
y = v - h c,
w = c t.
```

For the two block coordinates the frozen rational coefficients are

```text
h4 = 2340/8699,
h5 = 1520/8699,
r4 = -21912800/75672601,
r5 = -15007200/75672601,

75672601 = 8699^2.
```

Thus, at fixed time `t`,

```text
q_i = x_i + (h_i t + r_i)c,
v_i = y_i + h_i c,
w   = t c.                                               (1)
```

`T-P8-008` separately establishes that the correct source-facing ramp interface is the first-12 mechanical source evaluated at `w=c t`; the literal 13th source derivative remains zero and is not reinterpreted as `w'=c`.

`T-P5-022` gives the generic source-coordinate transport theorem.  Its input is a nonnegative matrix `S` satisfying component bounds

```text
|Delta xi_j| <= sum_k S[j,k] |Delta z_k|,               (2)
```

followed by a raw Jacobian envelope `H` and exactly one force-coordinate map.  `T-P5-023` extends this to a certified cell chain, while `T-P5-025/T-P5-026` can consume the resulting anisotropic component matrix directly rather than collapsing it immediately to one Frobenius scalar.

The missing bridge was the exact `S` induced by (1), and in particular the distinction between a common ramp parameter and a parameter mismatch.

---

## 2. Exact sparse moving-frame map

At fixed `t`, introduce the five-dimensional moving input

```text
eta = (x4,x5,y4,y5,c)^T.
```

Define the relevant absolute source-coordinate block

```text
Phi_t(eta)
 := (q4,q5,v4,v5,w)^T

 = (x4 + (h4 t+r4)c,
    x5 + (h5 t+r5)c,
    y4 + h4 c,
    y5 + h5 c,
    t c)^T.                                              (3)
```

If a downstream residual/controller also takes `c` as an explicit source parameter, use the augmented map

```text
PhiTilde_t(eta) := (Phi_t(eta),c).                       (4)
```

For two tuples `eta` and `etaBar`, write `Delta` for their difference.  Because `Phi_t` is linear at fixed `t`, subtraction gives the exact identities

```text
Delta q4 = Delta x4 + (h4 t+r4) Delta c,
Delta q5 = Delta x5 + (h5 t+r5) Delta c,
Delta v4 = Delta y4 + h4 Delta c,
Delta v5 = Delta y5 + h5 Delta c,
Delta w  = t Delta c.                                   (5)
```

Equivalently,

```text
Delta Phi_t = J_t Delta eta,                             (6)
```

with sparse matrix

```text
J_t =
[1 0 0 0 h4*t+r4]
[0 1 0 0 h5*t+r5]
[0 0 1 0 h4]
[0 0 0 1 h5]
[0 0 0 0 t].                                            (7)
```

The augmented map adds the final row

```text
[0 0 0 0 1].                                            (8)
```

No inequality has entered yet.  This is the exact coordinate-difference theorem that should sit immediately upstream of the generic `S/H/A` adapter from `T-P5-022`.

---

## 3. Common-parameter cancellation is exact, not a small-error estimate

### Theorem 3.1 — common ramp parameter cancellation

If

```text
c = cBar,                                                (9)
```

then `Delta c=0`, and (5) reduces exactly to

```text
Delta q4 = Delta x4,
Delta q5 = Delta x5,
Delta v4 = Delta y4,
Delta v5 = Delta y5,
Delta w  = 0.                                            (10)
```

If `c` is carried as an explicit source parameter, its difference is also zero.

Therefore, for the consumer ordering

```text
Delta z = (Delta x4,Delta x5,Delta y4,Delta y5),         (11)
```

the relevant rows of the `T-P5-022` transport matrix can be chosen **exactly** as

```text
S_common =
[1 0 0 0]   q4
[0 1 0 0]   q5
[0 0 1 0]   v4
[0 0 0 1]   v5
[0 0 0 0]   w
```

with another zero row for an explicit `c` coordinate.                       (12)

This has an important source-interface consequence:

> Under common `c` at common time, Jacobian sensitivity with respect to `w` or `c` does not consume centered gain at all, because the actual-minus-nominal displacement in those coordinates is exactly zero.

It would be wrong to add `H[:,w]` or `H[:,c]` to `ell2/K_path` merely because those Jacobian columns are numerically large.  Centered gain charges derivative sensitivity times **actual coordinate displacement**, and that displacement is zero here.

### Proof

Substitute `Delta c=0` into (5).  QED.

---

## 4. The straight source segment stays on the same ramp fiber

The common-parameter cancellation also repairs one subtle premise in the FTOC route of `T-P5-022`.

Let two moving states at fixed `(t,c)` be `z0,z1 in R^4`.  For `0<=s<=1` define

```text
z_s = (1-s) z0 + s z1.                                  (13)
```

Then linearity of the common-`c` map gives

```text
Phi_t(z_s,c)
 = (1-s) Phi_t(z0,c) + s Phi_t(z1,c).                   (14)
```

In particular every point of the straight source segment has the same

```text
w = c t,
c = c                                                     (15)
```

when `c` is explicit.  Thus the segment does not leave the ramp fiber merely because one interpolates between actual and nominal block states.

### Corollary 4.1

If the two source endpoints lie in one convex certified source box/cell at fixed `(t,c)`, then the entire source segment required by the `T-P5-022` Jacobian/FTOC theorem lies in that same cell automatically.

This corollary does **not** replace `T-P5-023` when the endpoints lie in different cells.  In that case a certified cell chain/path is still required.

---

## 5. Uniform finite-time transport when the parameters differ

Suppose now `Delta c` is not assumed zero.  For `0<=t<=T`, `T>=0`, define the exact affine endpoint envelope

```text
Ai(T) := max(|r_i|, |h_i*T+r_i|).                       (16)
```

Because `t -> h_i t+r_i` is affine and absolute value is convex,

```text
|h_i t+r_i| <= Ai(T)                                    (17)
```

on the whole interval.  Equation (5) therefore gives

```text
|Delta q4| <= |Delta x4| + A4(T)|Delta c|,
|Delta q5| <= |Delta x5| + A5(T)|Delta c|,
|Delta v4| <= |Delta y4| + |h4||Delta c|,
|Delta v5| <= |Delta y5| + |h5||Delta c|,
|Delta w|  <= T|Delta c|.                               (18)
```

For the present block at `T=1`, exact arithmetic gives

```text
h4+r4 = -1557140/75672601,
h5+r5 = -1784720/75672601,                              (19)
```

while `r4,r5<0` and `h4,h5>0`.  Hence the affine centers remain negative and decrease in magnitude on `[0,1]`, so

```text
A4(1) = 21912800/75672601,
A5(1) = 15007200/75672601,                              (20)

|h4| = 2340/8699,
|h5| = 1520/8699.                                       (21)
```

These are exact rational transport constants; decimals are unnecessary.

---

## 6. Controlled parameter mismatch gives an explicit `S` matrix

Let

```text
Delta z = (Delta x4,Delta x5,Delta y4,Delta y5).        (22)
```

Assume a source/P8 contract proves, on the same domain,

```text
|Delta c|
 <= gamma1|Delta x4|
  + gamma2|Delta x5|
  + gamma3|Delta y4|
  + gamma4|Delta y5|,                                   (23)
```

with `gamma_k>=0`.

Write `gamma=(gamma1,...,gamma4)` and `e_k` for the four standard nonnegative rows.  Combining (18) with (23) gives the explicit uniform transport rows

```text
S_q4 = e1 + A4(T) gamma,
S_q5 = e2 + A5(T) gamma,
S_v4 = e3 + |h4| gamma,
S_v5 = e4 + |h5| gamma,
S_w  = T gamma,                                         (24)
```

and, if `c` is an explicit source input,

```text
S_c = gamma.                                            (25)
```

### Theorem 6.1 — moving-frame uniform transport under parameter control

Hypothesis (23) implies all component inequalities

```text
|Delta xi_j| <= sum_k S[j,k]|Delta z_k|                 (26)
```

with `S` given by (24)-(25).  Hence this `S` is immediately admissible as the source-coordinate input to `T-P5-022` or segmentwise to `T-P5-023`.

The common-parameter theorem is the special case `gamma=0`, where (24) collapses to the identity/zero structure (12).

---

## 7. Direct correction of `K_path`: no need to rebuild or scalarize the whole adapter

The previous section can be composed one level further and expressed directly in the component matrix consumed by `T-P5-025/T-P5-026`.

Let raw residual components be indexed by `i`, consumer force components by `a`, and let `F[a,i]` be the **single** raw-force-to-consumer-force map.  Let the nonnegative raw Jacobian envelope on the source coordinates be

```text
H[i,q4], H[i,q5], H[i,v4], H[i,v5], H[i,w]              (27)
```

and optionally `H[i,c]` if `c` is an explicit source argument.

### Common-`c` base matrix

Under `Delta c=0`, define

```text
K0[a,1] = sum_i |F[a,i]| H[i,q4],
K0[a,2] = sum_i |F[a,i]| H[i,q5],
K0[a,3] = sum_i |F[a,i]| H[i,v4],
K0[a,4] = sum_i |F[a,i]| H[i,v5].                       (28)
```

There is **no** `H[:,w]` or `H[:,c]` term in (28).

### Parameter-sensitivity charge

For `0<=t<=T`, define

```text
kappa_a(T)
 := sum_i |F[a,i]| *
      ( H[i,q4] A4(T)
      + H[i,q5] A5(T)
      + H[i,v4] |h4|
      + H[i,v5] |h5|
      + H[i,w] T
      + H[i,c] ),                                       (29)
```

where the final `H[i,c]` term is omitted if `c` is not an explicit source coordinate.

Then (18) and the Jacobian component envelope give

```text
|r_c,a|
 <= sum_k K0[a,k]|Delta z_k| + kappa_a(T)|Delta c|.     (30)
```

Using (23),

```text
|r_c,a|
 <= sum_k K_eff[a,k]|Delta z_k|                         (31)
```

with the exact nonnegative rank-one update

```text
K_eff[a,k]
 = K0[a,k] + kappa_a(T) gamma_k.                        (32)
```

In matrix notation,

```text
K_eff = K0 + kappa(T) tensor gamma.                     (33)
```

### Theorem 7.1 — parameter correction to anisotropic centered gain

Under the source Jacobian envelope and parameter-control hypothesis (23), the direct component envelope (31) holds with (32).  Therefore:

```text
K_eff
 -> T-P5-025 orthant quadratic consumer
 -> T-P5-026 feasible-cone/SPN consumer                 (34)
```

without first collapsing to a Frobenius scalar.

If a scalar fallback is desired, only then form the corresponding `ell2` from `K_eff` and use `T-P5-024/T-P5-027`.

### Cell-chain specialization

For `T-P5-023`, apply (28)-(32) per certified segment/cell.  At a fixed time one may use the exact coefficient `|h_i t+r_i|`; for a checker that wants one interval-uniform matrix use `A_i(T)`.  Segment contributions then telescope/sum exactly as in `T-P5-023`.

---

## 8. Sharp obstruction: a four-state centered gain forces parameter-fiber constancy

The previous positive theorem also identifies the exact failure boundary.

Let `E_t(z,c)` be any residual composition in consumer-force coordinates.  Suppose one claims a finite four-state centered gain on a domain containing two points with the same `z` but different parameters:

```text
||E_t(z,c)-E_t(zBar,cBar)||^2
 <= ell2 ||z-zBar||^2                                   (35)
```

for all allowed pairs.

### Theorem 8.1 — centered gain implies fiber constancy

If (35) holds with finite `ell2`, then for every fixed `z` and every two allowed `c,cBar` in that fiber,

```text
E_t(z,c) = E_t(z,cBar).                                 (36)
```

### Proof

Set `zBar=z`.  The right-hand side of (35) is zero, so the squared norm on the left is at most zero.  Norm squares are nonnegative, hence it is zero and the two residuals are equal.  QED.

Thus, if the residual actually varies with `c` while the four moving coordinates are held fixed, **no finite four-state `ell2` exists** for arbitrary cross-parameter comparisons.

The scalar example

```text
E_t(z,c)=c                                               (37)
```

is already a complete counterexample.

This is not a numerical weakness of `T-P5-022`; it is an information-theoretic obstruction.  A valid architecture must choose one of four typed routes:

1. **common parameter:** actual and nominal use the same `c`; use the exact cancellation (10)-(12);
2. **controlled mismatch:** prove (23), yielding the rank-one correction (32);
3. **expanded consumer:** add `c` (and any other independent coordinate) to the Lyapunov/error norm;
4. **additive/transverse lane:** keep the parameter-induced residual outside the homogeneous centered gain and charge it through an existing bias/reserve consumer.

There is no fifth option in which one silently ignores `Delta c` while still allowing arbitrary cross-parameter pairs.

---

## 9. Force normalization still happens exactly once

The moving-frame map is a **state-coordinate transport**.  It does not authorize an additional force normalization.

Retain the `T-P5-022/T-P5-019` rule:

```text
raw PMI residual              -> F = diag(1/5,1/10)  (when that is the defined generalized-force map),
already generalized force     -> F = I.                                      (38)
```

In particular, if `DHPowerBinding.forceError` is already in generalized-force coordinates, `F=I` in (28)-(29).  Applying `I_B` again would undercharge the residual and is mathematically unrelated to the moving-frame cancellation.

---

## 10. Cross-layer composition now available

The interface chain can now be written without an untyped jump:

```text
P5 relative moving-frame state z
 + P8 ramp relation / common-parameter contract
        |
        v
exact source displacement map (this review)
        |
        v
T-P5-022 single-cell H transport
or T-P5-023 certified cell-chain transport
        |
        v
source-bound K0, or K0 + kappa tensor gamma
        |
        +--> T-P5-025 direct orthant quadratic route
        +--> T-P5-026 18-cone/SPN route
        +--> scalarize only if needed -> T-P5-024/T-P5-027.                 (39)
```

The moving-frame source-box result from the P5-017 companion is complementary: it can certify that the absolute source coordinates lie in a box on which a Jacobian/interval envelope is valid.  It does not itself prove the Jacobian envelope `H`.

Likewise `T-P8-008` supplies the honest first-12 `w=c t` source semantics.  No full 13-coordinate source equality is needed or permitted for nonzero `c`.

---

## 11. Minimal theorem decomposition for Lean

This child should stay algebraic and avoid ODE/FTOC APIs; the generic Jacobian/path theorems already live downstream.

Suggested source-independent targets:

### `movingFrameSourceDifference_exact`

For explicit scalar definitions of (3), prove all five identities in (5) by `ring`.

### `movingFrameCommonParameter_cancel`

From `c=cBar`, prove (10), including the zero `w`/optional `c` differences.

### `movingFrameSegment_preservesRampFiber`

At fixed `(t,c)`, prove (14) coordinatewise and hence fixed `w=ct` on the interpolating segment.

### `movingFrameUniformTransport_of_parameterControl`

Consume `0<=t<=T`, the endpoint bounds `|h_i t+r_i|<=A_i(T)`, and (23) to prove the five component inequalities encoded by (24)-(25).

### `movingFrameParameterCorrection_to_K`

From a nonnegative `H`, force map absolute coefficients, the component inequalities, and (23), prove

```text
|r_a| <= sum_k (K0[a,k] + kappa_a*gamma_k)|Delta z_k|.  (40)
```

This theorem is only finite-sum/triangle algebra and composes directly with the already formalized `K` consumers.

### `fourStateCenteredGain_implies_parameterFiberConstancy`

From (35) with `zBar=z`, prove (36).  The theorem can be stated using component equality if avoiding a norm API is desirable.

Concrete exact-rational corollaries:

```text
block45_A4_T1 = 21912800/75672601,
block45_A5_T1 = 15007200/75672601,
block45_h4_abs = 2340/8699,
block45_h5_abs = 1520/8699.                              (41)
```

---

## 12. Remaining obligations and admission boundary

Still open and intentionally outside this child:

```text
- a concrete source/Float64 centered-increment or Jacobian envelope H;
- the actual source ordering for every non-block/distal coordinate;
- a proof that actual/nominal compare the same c, or a concrete gamma if not;
- certified P8 cell-chain/path connectivity and interval membership;
- runtime/controller/solve discontinuous remainder routing;
- true-DH/source hash binding;
- ODE existence/continuation and flowpipe coverage;
- pinned Lean compile/axiom receipt for this new algebraic child;
- independent verification;
- P5/P8/M4 closure or registry admission.
```

The strongest practical recommendation is to make the source checker explicitly tag the comparison mode as either

```text
common_ramp_parameter
```

or

```text
controlled_parameter_mismatch(gamma).
```

For `common_ramp_parameter`, emit the exact zero `w/c` rows rather than conservative nonzero bounds.  For a controlled mismatch, emit `gamma` and the rank-one update (32).  If neither is available and the residual changes with `c`, preserve the obstruction rather than fabricating a finite four-state centered gain.

`admission_label = pending`.

待封不觉独立验证 / 待梁智炜最终整合。
