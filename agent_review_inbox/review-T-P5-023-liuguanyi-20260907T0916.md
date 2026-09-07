---
kind: review_result
review_id: review-T-P5-023-liuguanyi-20260907T0916
task_id: T-P5-023
source_agent: 柳冠一
agent: 柳冠一
claimed_at: 2026-09-07T09:02:00-06:00
created_at: 2026-09-07T09:16:00-06:00
inspected_commit: 8e2773065a77559fb9e0671f529580a5400ddc4e
continuation_of:
  - review-T-P5-022-liuguanyi-20260907T0820
related_reviews:
  - review-T-P5-022-juyangxianzun-20260907T0846
  - review-T-P5-020-guyuefangyuan-20260907T0743
  - review-T-P8-008-guyuefangyuan-20260907T0231
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_piecewise_increment_transport_and_require_source_flowpipe_checkers_to_emit_a_certified_connecting_cell_chain_or_equivalent_path_variation_contract_before_using_local_jacobian_bounds_as_a_P5_centered_gain
---

# T-P5-023 — piecewise-cell / path transport from local Jacobian certificates to the P5 centered gain

## 0. Result in one sentence

`T-P5-022` correctly transports a source Jacobian bound through state and force coordinates, but its calculus justification uses one certified straight segment.  A real P8/source enclosure is more naturally a finite union of boxes/cells with **cell-local** Jacobian bounds.  The missing interface theorem is a finite telescoping/path transport: local increment bounds may be composed along any certified cell chain, and the same `ell2` consumer follows with an explicit path-variation charge.  Conversely, endpoint coverage plus cell-local Jacobian bounds is mathematically insufficient if no certified connecting path is supplied.

This is interface mathematics only.  It does not certify a Julia/Float64 Jacobian, a concrete cell chain, P8 flowpipe coverage, ODE continuation, source provenance, P5/P8/M4 closure, or registry admission.

---

## 1. The seam left by T-P5-022

The algebraic sidecar formalized from `T-P5-022` now accepts component contracts of the form

```text
|delta xi_j| <= sum_k S[j,k] |delta z_k|,
|delta e_i|  <= sum_j H[i,j] |delta xi_j|,
```

and transports them through a force-coordinate map `A` to

```text
||r_c||^2 <= ell2 ||delta z||^2.
```

That theorem is already the right downstream consumer.  The remaining source-to-math issue is how a checker obtains the second line when its derivative evidence is only local to cells.

A single FTOC argument is immediate when the entire segment from the nominal state to the actual state lies in one convex certified domain.  But a flowpipe/tube is often represented as a union of boxes, and the segment may cross several cells.  Replacing every local derivative interval by an unexplained global maximum is safe only if the checker has actually certified all points of the connecting segment.  Membership of the two endpoints in the covered union is not enough.

---

## 2. Finite piecewise increment transport theorem

Fix one time `t`; time is a parameter in this theorem.

Let

```text
dz in R^k                                      consumer-state displacement,
xi^0, xi^1, ..., xi^R in R^n                  source-space path points,
e(t,xi) in R^m                                raw residual,
A : R^m -> R^p                                raw residual -> consumer force.
```

For segment `r=1,...,R`, write

```text
dxi^r_j := xi^r_j - xi^(r-1)_j,
de^r_i  := e_i(t,xi^r) - e_i(t,xi^(r-1)).
```

Assume the checker/source mathematics supplies nonnegative tables `H^r` and `S^r` with

```text
|de^r_i|  <= sum_j H^r[i,j] |dxi^r_j|,                 (1)
|dxi^r_j| <= sum_k S^r[j,k] |dz_k|.                    (2)
```

Define the path-transport table

```text
K_path[a,k]
 := sum_r sum_i sum_j
      |A[a,i]| H^r[i,j] S^r[j,k].                      (3)
```

and

```text
ell2_path := sum_a sum_k K_path[a,k]^2.                (4)
```

Let the centered consumer-force residual be

```text
r_c := A ( e(t,xi^R) - e(t,xi^0) ).                    (5)
```

### Theorem — piecewise transported centered gain

Under (1)-(2),

```text
|r_c[a]| <= sum_k K_path[a,k] |dz_k|                   (6)
```

for every force component `a`, and therefore

```text
||r_c||^2 <= ell2_path ||dz||^2.                       (7)
```

### Proof

The residual difference telescopes exactly:

```text
e_i(t,xi^R)-e_i(t,xi^0) = sum_r de^r_i.                (8)
```

Hence

```text
|r_c[a]|
 = |sum_i A[a,i] sum_r de^r_i|
 <= sum_r sum_i |A[a,i]| |de^r_i|
 <= sum_r sum_i sum_j |A[a,i]| H^r[i,j] |dxi^r_j|
 <= sum_r sum_i sum_j sum_k
      |A[a,i]| H^r[i,j] S^r[j,k] |dz_k|
 = sum_k K_path[a,k] |dz_k|.
```

This proves (6).  Applying the same row-wise finite Cauchy inequality already used in `T-P5-022` gives (7).

The important point is that no global convexity or global Jacobian interval appears in the algebraic theorem.  All domain geometry has been isolated into the per-segment increment premises (1)-(2).

---

## 3. How local cell Jacobians discharge the segment premise

Suppose segment `r` lies entirely in a convex certified source cell `C_r`, and the exact-real residual map is differentiable there with

```text
|partial_j e_i(t,x)| <= H^r[i,j]     for all x in C_r. (9)
```

Then the one-segment FTOC argument gives exactly

```text
|de^r_i| <= sum_j H^r[i,j] |dxi^r_j|.                  (10)
```

Thus a finite cell chain

```text
[xi^0,xi^1] subset C_1,
[xi^1,xi^2] subset C_2,
...
[xi^(R-1),xi^R] subset C_R                            (11)
```

is enough.  The union of all cells need not be convex.

This separates the proof obligations cleanly:

```text
cell/path geometry         -> certified segment chain (11),
local source calculus      -> H^r and (10),
state-coordinate transport -> S^r and (2),
finite algebra             -> K_path, ell2_path,
P5 consumer                -> T-P5-020 / T-P5-021.
```

The existing `T-P5-022` sidecar can be reused after the first four layers produce the final component row bound; it does not need to know anything about cells.

---

## 4. Straight-segment cell partition: sharper effective Jacobian

There is a useful specialization when the desired path is still the straight source segment

```text
xi(s) = xi^0 + s Delta_xi,    0 <= s <= 1,             (12)
```

but the segment crosses multiple certified cells.

Let

```text
0=t_0 < t_1 < ... < t_R=1,
lambda_r := t_r-t_(r-1),                                (13)
```

and suppose subsegment `r` is contained in cell `C_r` with local Jacobian table `H^r`.

Then

```text
|dxi^r_j| = lambda_r |Delta_xi_j|.                     (14)
```

If the endpoint source displacement already satisfies

```text
|Delta_xi_j| <= sum_k S[j,k] |dz_k|,                   (15)
```

we may take

```text
S^r[j,k] = lambda_r S[j,k].                            (16)
```

Define the path-averaged Jacobian envelope

```text
Hbar[i,j] := sum_r lambda_r H^r[i,j].                  (17)
```

Then (3) simplifies exactly to

```text
K_path[a,k]
 = sum_i sum_j |A[a,i]| Hbar[i,j] S[j,k].              (18)
```

So the checker does **not** need to replace all local tables by the entrywise maximum.  It can preserve the fraction of the straight segment spent in each cell.

If exact `lambda_r` is inconvenient, rational upper bounds

```text
0 <= lambda_r <= omega_r                               (19)
```

may be used instead, giving the safe envelope

```text
Hbar[i,j] <= sum_r omega_r H^r[i,j].                   (20)
```

No condition `sum_r omega_r=1` is needed for soundness; excess total weight simply records conservatism.

---

## 5. General path distortion is a real mathematical charge

For a polygonal or curved certified path, the total coordinate variation may exceed the endpoint displacement.  This cannot be discarded.

A convenient continuous version of the same interface is: for an absolutely continuous path `gamma:[0,1]->R^n`, assume

```text
int_0^1 |gamma'_j(s)| ds
  <= sum_k S_path[j,k] |dz_k|.                         (21)
```

If a uniform pathwise derivative envelope `H[i,j]` holds, then

```text
|e_i(gamma(1))-e_i(gamma(0))|
 <= sum_j H[i,j] int_0^1 |gamma'_j(s)| ds
 <= sum_j sum_k H[i,j] S_path[j,k] |dz_k|.             (22)
```

Thus the same `T-P5-022` transport applies with `S=S_path`.

For a piecewise cell path, (21) is represented discretely by the collection `S^r`.  If the path doubles back, its larger variation produces a larger `ell2_path`.  There is no valid theorem that silently replaces path variation by endpoint displacement unless straightness, coordinate monotonicity, or another variation bound is proved.

This is the correct mathematical price of using a nonconvex certified domain.

---

## 6. Endpoint coverage is not enough: explicit obstruction

Cell-local derivative bounds plus endpoint membership do **not** imply a centered gain across disconnected or unbridged cells.

Take one source coordinate and two certified cells

```text
C_- = (-infinity,-1],
C_+ = [1,infinity).                                    (23)
```

For any `M>0`, define a `C^1` function

```text
e(x)=0,                              x <= -1,
e(x)=M * psi((x+1)/2),              -1 < x < 1,
e(x)=M,                               x >= 1,           (24)
```

where

```text
psi(s)=3s^2-2s^3,    0<=s<=1.                           (25)
```

Because `psi'(0)=psi'(1)=0`, this function is `C^1`.  On both certified cells its derivative is exactly zero, so the local checker may truthfully report

```text
H_- = H_+ = 0.                                         (26)
```

Yet for endpoints `x_-=-2`, `x_+=2`,

```text
|e(x_+)-e(x_-)| = M,                                   (27)
```

which is arbitrary.

All variation occurred in the uncovered gap.  Therefore no theorem may infer a cross-cell Lipschitz/centered residual bound from

```text
endpoint in covered union + derivative bounds inside each endpoint cell
```

alone.

A source checker must additionally certify a connecting path whose every segment lies in a domain where the relevant increment/Jacobian bound is valid.  This is a mathematical coverage condition, not provenance bookkeeping.

---

## 7. P8 ramp-graph specialization

The bridge is particularly compatible with `T-P8-008`.

At fixed time `t`, both actual and nominal P8 mechanical states can be evaluated at the same adapter tail

```text
w=c0*t,
c=c0.                                                   (28)
```

If the centered comparison really shares these tail values, a certified source path can keep the tail coordinates constant.  Their segment displacements are then exactly zero:

```text
dxi^r_w = dxi^r_c = 0                                  (29)
```

for every segment.  Hence the corresponding rows of every `S^r` may be zero even when the source residual has large Jacobian columns in `w` or `c`.

This does **not** solve the distal-coordinate issue identified in `T-P5-022`.  If a non-block mechanical coordinate differs between actual and nominal states, its path variation must still be covered by a nonzero `S^r` row, included in an expanded consumer norm, or routed to a separate additive/transverse budget.

The P8 source lane therefore needs more than a list of covered endpoint boxes.  For each centered comparison family it needs either:

1. one convex common box containing the entire connecting segment; or
2. a finite certified cell chain with per-segment variation/Jacobian data; or
3. another explicit path-variation theorem equivalent to (21).

---

## 8. Force-coordinate normalization remains exactly once

All formulas above preserve the `T-P5-022` force-map rule.

If each local residual increment `de^r` is still in raw PMI force coordinates, use

```text
A = I_B = diag(1/5,1/10)                               (30)
```

exactly once when forming `K_path`.

If the local increment is already a `DHPowerBinding.forceError` / generalized-force quantity, use

```text
A = I.                                                  (31)
```

The fact that the source path is split across cells does not authorize another normalization.  In particular, the force map must be common across the telescoping sum or each segment must carry its own explicitly typed map and be transported to a common consumer force coordinate before summation.

---

## 9. Checker-facing finite certificate

A source checker can emit the following finite certificate for each residual family and time/domain slab:

```text
force_coordinate_tag,
A,
consumer displacement convention dz,
ordered path/cell chain r=1..R,
per-segment H^r,
per-segment S^r  (or straight-segment lambda_r plus common S),
K_path,
ell2_path.                                             (32)
```

The trusted arithmetic check is only

```text
K_path[a,k]
 = sum_r sum_i sum_j |A[a,i]| H^r[i,j] S^r[j,k],

ell2_path
 = sum_a sum_k K_path[a,k]^2.                          (33)
```

Then `ell2_path` can be substituted directly into the already-derived `T-P5-021` discriminant/barrier.  Cell geometry and calculus evidence remain separate source obligations; the scalar P5 consumer should not be taught about interval-box topology.

For a straight segmented path, the checker may instead emit `Hbar` from (17)/(20), reducing the downstream artifact to the exact same shape as `T-P5-022`.

---

## 10. Minimal Lean theorem decomposition

The new formalization should reuse the existing `T-P5-022` Frobenius consumer rather than duplicate it.

### 10.1 `piecewise_component_transport`

Use finite segment increments directly, avoiding calculus in the sidecar:

```text
hSegErr:
  |de[r,i]| <= sum_j H[r,i,j] |dxi[r,j]|

hSegState:
  |dxi[r,j]| <= sum_k S[r,j,k] |dz[k]|

rc[a] = sum_i A[a,i] * sum_r de[r,i]
```

Define

```text
K[a,k] = sum_r sum_i sum_j |A[a,i]| H[r,i,j] S[r,j,k].
```

Conclusion:

```text
|rc[a]| <= sum_k K[a,k] |dz[k]|.
```

This is finite sums, triangle inequality, monotonicity, and distributivity only.

### 10.2 `piecewise_transported_centered_gain`

Feed the row bound from 10.1 into the already compiled `frobenius_centered_gain` theorem to obtain

```text
sum_a rc[a]^2
 <= (sum_a sum_k K[a,k]^2) * sum_k dz[k]^2.
```

### 10.3 `straight_partition_effective_jacobian`

Formalize the exact reindexing identity

```text
S^r = lambda_r S
=>
K_path(A,H,S^r)
 = K_single(A, Hbar, S),

Hbar[i,j]=sum_r lambda_r H[r,i,j].
```

A separate monotonic corollary can replace `lambda_r` by rational upper weights `omega_r`.

No ODE API, interval arithmetic, or source semantics is required in these Lean lemmas.

---

## 11. What remains unclosed

This theorem closes only the **mathematical composition rule** for cell-local source increments.  The physical/source lane still must establish:

1. a concrete certified path/cell chain for every actual/nominal pair on the P5 first-exit domain, or a stronger common-convex-domain statement;
2. cell-local exact-real Jacobian/increment bounds `H^r`;
3. path/source-coordinate variation bounds `S^r`, including every distal coordinate that can move independently;
4. the one-time force-coordinate map `A`;
5. separate treatment of non-smooth IEEE/controller/solve residuals unless a direct centered increment certificate is available;
6. P8 nominal/actual same-time domain coverage, ODE existence/continuation, and concrete source semantic binding.

The new precise obstruction is item 1: **covered endpoints are not a centered-gain certificate**.  The covered set must support a certified connecting path on which the residual increment evidence is valid.

---

## 12. Admission boundary

`pending` mathematical/interface result only.

No provenance/receipt/admission re-audit was performed, no existing theorem was independently revalidated, and no P5/P8/M4 or registry status is changed.

Recommended next formalization target: `piecewise_component_transport` plus the straight-partition reindexing corollary, reusing the compiled `T-P5-022` Frobenius theorem.  Recommended source/P8 target: make cell-chain/path connectivity an explicit field of the centered-residual certificate rather than inferring it from endpoint box membership.
