---
kind: review_result
review_id: review-T-P5-022-liuguanyi-20260907T0820
task_id: T-P5-022
source_agent: 柳冠一
agent: 柳冠一
claimed_at: 2026-09-07T08:10:00-06:00
created_at: 2026-09-07T08:20:00-06:00
inspected_commit: 90d992f478f9e1fb3bf2b7f45c1b23cd96c54490
continuation_of:
  - review-T-P5-009-liuguanyi-20260907T0606
  - review-T-P5-019-liuguanyi-20260907T0730
related_reviews:
  - review-T-P5-018-guyuefangyuan-20260907T0634
  - review-T-P5-020-guyuefangyuan-20260907T0743
  - review-T-P5-021-honglianmozun-20260907T0800
  - review-T-P4-018-liuguanyi-20260907T0522
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_the_coordinate_transport_lemma_and_make_source_checkers_emit_A_S_H_anchor_boxes_plus_ell2_B2_instead_of_untyped_norms
---

# T-P5-022 — coordinate-aware source Jacobian / anchor-box transport into the P5 centered-gain consumer

## 0. Result in one sentence

`T-P5-020` and `T-P5-021` reduce the block-(4,5) residual problem to two scalars, a centered squared gain `ell2` and a nominal-anchor squared bias `B2`, but the source program generally lives in a different state ordering/scaling and may still be in raw PMI force coordinates.  The missing interface theorem is an explicit transport through **both** coordinate maps: from source-state displacement bounds and raw Jacobian intervals to a generalized-force centered gain, and from raw anchor component boxes to the generalized-force anchor norm.  The resulting formulas use only finite sums, absolute values, squares, and rational arithmetic.

This is a source-to-math adapter theorem only.  It does not certify any concrete Julia Jacobian interval, Float64 derivative, source hash, flowpipe coverage, or registry admission.

---

## 1. Why a new bridge is needed

`T-P5-020` uses the four-dimensional consumer error

```text
z = (x4,x5,y4,y5),
N = ||z||^2,
```

and asks for a centered generalized-force residual `r_c in R^2` satisfying

```text
||r_c||^2 <= ell2 * N.                                  (1)
```

Its source-facing discussion gives the special case in which the residual is already a smooth map `E : R^4 -> R^2` in exactly those coordinates.

The deployed/source layer need not have that shape.  In general:

1. the source state can contain more coordinates and a different ordering/scaling;
2. some source coordinates, notably a common ramp tail at fixed time, have zero actual-minus-nominal displacement even though the residual depends on them;
3. the source residual may be expressed in raw PMI coordinates and only later mapped to generalized-force coordinates;
4. some existing abstractions, such as `DHPowerBinding.forceError`, are already generalized-force quantities, in which case applying `I_B` again would be a double normalization.

Therefore a checker needs a typed map, not a bare Euclidean norm bound.

---

## 2. Abstract source-state transport contract

Let

```text
z, zbar in R^k                      consumer/error coordinates,
xi, xibar in R^n                    full source coordinates,
e(t,xi) in R^m                      raw residual map,
A : R^m -> R^p                      raw-force -> consumer-force linear map.
```

For Route-B block-(4,5), the intended consumer dimensions are `k=4`, `p=2`, but the theorem does not need those fixed dimensions.

Do **not** require an exact linear identity `xi-xibar = S(z-zbar)`.  A source checker often has only component-wise transport bounds.  Assume a nonnegative matrix `S[j,k]` such that, on the same first-exit domain,

```text
|xi_j - xibar_j|
  <= sum_k S[j,k] |z_k-zbar_k|                         (2)
```

for every source coordinate `j`.

This single interface covers several useful cases:

- exact permutation/scaling: `xi-xibar = T(z-zbar)`, by taking `S=|T|` entrywise;
- a source coordinate shared exactly by actual and nominal paths: set the corresponding row of `S` to zero;
- a distal/source coordinate controlled by the block error through a separate tube lemma: encode that component bound in its row of `S`;
- a coordinate that varies independently of the block error: no finite row of `S` exists, which is the correct obstruction rather than silently omitting that coordinate.

The row-zero case is important for the P8 ramp graph.  At a fixed time, if actual and nominal trajectories use the same `w=c0*t` and the same `c=c0`, then their `w` and `c` differences are exactly zero.  Any source Jacobian columns with respect to `w` or `c` therefore cost **nothing** in the centered gain; their `S` rows are zero.

---

## 3. Raw Jacobian intervals -> centered generalized-force gain

Assume that for fixed `t`, the segment

```text
xi_s = xibar + s (xi-xibar),    0 <= s <= 1
```

lies in a certified source domain and that `e(t,.)` is differentiable there.  Suppose the checker proves nonnegative bounds

```text
|partial_j e_i(t,xi_s)| <= H[i,j]                       (3)
```

for every raw residual component `i`, source coordinate `j`, and all points of the segment/domain.

Let `A[a,i]` be the force-coordinate map and define the nonnegative transported entry bound

```text
K[a,k]
 := sum_i sum_j |A[a,i]| H[i,j] S[j,k].                 (4)
```

Finally define

```text
ell2_transport := sum_a sum_k K[a,k]^2.                 (5)
```

### Theorem — coordinate-transported centered gain

For

```text
r_c := A (e(t,xi)-e(t,xibar)),                           (6)
```

the hypotheses (2)-(3) imply

```text
||r_c||^2
  <= ell2_transport * ||z-zbar||^2.                     (7)
```

Thus `T-P5-020` can consume

```text
ell2 = ell2_transport.                                   (8)
```

### Proof

By the fundamental theorem of calculus on the source segment,

```text
e_i(t,xi)-e_i(t,xibar)
 = integral_0^1 sum_j partial_j e_i(t,xi_s)
                  (xi_j-xibar_j) ds.
```

Hence, using (2)-(3),

```text
|e_i(t,xi)-e_i(t,xibar)|
 <= sum_j H[i,j] |xi_j-xibar_j|
 <= sum_j sum_k H[i,j] S[j,k] |z_k-zbar_k|.             (9)
```

Applying `A` and the triangle inequality gives each consumer-force component

```text
|r_c,a|
 <= sum_k K[a,k] |z_k-zbar_k|.                          (10)
```

Cauchy row by row gives

```text
r_c,a^2
 <= (sum_k K[a,k]^2) (sum_k |z_k-zbar_k|^2).            (11)
```

Summing over `a` proves (7).

No inverse coordinate map, singular value, square root, or spectral-norm computation is needed.

### Sharpness boundary

The formula (5) is a **safe entrywise/Frobenius transport**, not generally a sharp operator norm.  Conservatism enters at three explicit places: entrywise absolute values in `A`, the component envelope `S`, and row-wise Cauchy.  A future checker with a certified operator-norm bound may replace `ell2_transport` by a smaller scalar, but it must preserve the same coordinate semantics.

---

## 4. Raw anchor component boxes -> `B2`

Let `n(t,xibar)` denote the nominal raw residual used by the nominal equation.  The anchor branch before force normalization is

```text
b_raw := e(t,xibar)-n(t,xibar).                          (12)
```

Assume component-wise source bounds

```text
|b_raw,i| <= c_i,
c_i >= 0.                                                 (13)
```

Define

```text
C_a := sum_i |A[a,i]| c_i,
B2_transport := sum_a C_a^2.                            (14)
```

For the generalized-force anchor

```text
b := A b_raw,                                            (15)
```

we obtain immediately

```text
||b||^2 <= B2_transport.                                (16)
```

Hence the `T-P5-020` / `T-P5-021` anchor input can be chosen as

```text
B2 = B2_transport.                                       (17)
```

Again, this is an exact finite-arithmetic adapter once the `c_i` boxes and `A` are source-bound.

---

## 5. Diagonal normalization corollary

The most common Route-B case is diagonal force normalization and an exact state permutation/scaling.  Suppose

```text
A = diag(alpha_i),
xi_j-xibar_j = beta_j (z_{pi(j)}-zbar_{pi(j)})
```

for the varying source coordinates.  Then the transport can be written without a matrix product:

```text
K[i,k]
 = |alpha_i| * sum_{j: pi(j)=k} H[i,j] |beta_j|,        (18)

ell2
 = sum_i sum_k K[i,k]^2.                                (19)
```

If there is exactly one source coordinate for each consumer coordinate, this reduces further to

```text
ell2 = sum_i sum_k alpha_i^2 * H[i,k]^2 * beta_k^2.     (20)
```

For raw anchor boxes,

```text
B2 = sum_i alpha_i^2 c_i^2.                             (21)
```

These are particularly convenient for exact-rational checkers.

---

## 6. Route-B force-coordinate specialization and the double-normalization rule

For a two-channel **raw PMI** force residual, if the consumer is the existing generalized-force coordinate with

```text
I_B = diag(1/5,1/10),
```

then use

```text
A = I_B.                                                 (22)
```

For example, with raw Jacobian bounds `H[1,j], H[2,j]`, the transported rows are

```text
K[1,k] = (1/5)  * sum_j H[1,j] S[j,k],
K[2,k] = (1/10) * sum_j H[2,j] S[j,k].                  (23)
```

and a raw anchor box `(c1,c2)` gives

```text
B2 = c1^2/25 + c2^2/100.                                (24)
```

However, if the upstream object is already the generalized-force quantity used by `DHPowerBinding.forceError` / the P5 consumer, then the correct map is

```text
A = I.                                                   (25)
```

Applying `I_B` again would undercharge the squared residual by factors up to `1/25` or `1/100`.  The checker contract therefore must record an explicit coordinate tag such as

```text
raw_pmi_force
```

or

```text
generalized_force
```

and choose `A` exactly once.  This is the P5 analogue of the force-coordinate correction already exposed in `T-P4-018` and `T-P5-019`.

---

## 7. Direct composition with T-P5-021: one rational checker frontend

Once the checker has produced exact rational upper bounds

```text
ell2 := ell2_transport,
B2   := B2_transport,
Vstar > 0,
```

`T-P5-021` eliminates the auxiliary split parameter `mu`.

Define

```text
C
 := 2285*Vstar
    -13600*ell2*Vstar
    -11424*B2.                                          (26)
```

Then the strict centered-plus-anchor P5 barrier has the no-search sufficient/exact scalar test

```text
C > 0,                                                   (27)
C^2 > 621465600 * ell2 * Vstar * B2.                    (28)
```

When (27)-(28) hold, the rational witness

```text
mu_bal
 = (2285*Vstar + 13600*ell2*Vstar - 11424*B2)
   / (4570*Vstar)                                       (29)
```

satisfies the strict centered and anchor inequalities used by `T-P5-020`.

Therefore a source-facing checker can be organized as the deterministic chain

```text
raw source state/force contract
 -> S, A
 -> Jacobian interval matrix H
 -> anchor component boxes c
 -> K
 -> ell2, B2
 -> C, discriminant
 -> rational mu_bal
 -> existing P5 centered/anchor consumer.               (30)
```

No norm convention is implicit in this chain.

### Quarter barrier

For `Vstar=1/4`, define

```text
Cq := 2285 - 13600*ell2 - 45696*B2.                    (31)
```

The exact checker conditions become

```text
Cq > 0,
Cq^2 > 2485862400 * ell2 * B2,                          (32)
```

with

```text
mu_q = (2285 + 13600*ell2 - 45696*B2)/4570.            (33)
```

Thus all arithmetic after source interval generation can remain rational and division-free until the optional witness emission.

---

## 8. Important full-state obstruction: block-only `ell2` is not automatic

This bridge exposes a source/domain issue that the abstract four-state notation can hide.

Suppose the actual residual depends on a full source coordinate `xi_j`, and actual and nominal trajectories can differ in that coordinate independently of the block error `z-zbar`.  Then no finite coefficient row `S[j,*]` satisfying (2) exists.  In that case a bound on `partial_j e_i` cannot be charged to the four-state `N` of `T-P5-020`.

A concrete abstract counterexample is

```text
e(z,eta) = eta,
actual:  z=zbar,
         eta != etabar.
```

Then `N=||z-zbar||^2=0` but the centered residual is nonzero.  No finite `ell2` can satisfy (1).

Therefore every non-block source coordinate on which the residual depends must be routed by exactly one of the following typed choices:

1. **common coordinate:** prove actual and nominal values are identical; use a zero row in `S`;
2. **transported coordinate:** prove its displacement is controlled by the block error; encode that row of `S`;
3. **expanded consumer:** enlarge the Lyapunov/state norm so that the coordinate is part of `N`;
4. **additive/transverse route:** keep its variation outside the centered gain and charge it through a separate `B2`/transverse consumer.

This is especially relevant when joining P5 to the P8 12-state mechanical flowpipe.  The common ramp tail is benign because its actual-minus-nominal difference can be zero; uncontrolled distal mechanical coordinates are not benign merely because the P5 energy is written only for block `(4,5)`.

---

## 9. Float64 boundary

The theorem above is valid for a differentiable exact-real residual map with a certified Jacobian bound.  It does not turn a derivative bound for an underlying real formula into a derivative theorem for the lifted IEEE program.

For Float64/controller/solve remainders, the source lane must do one of the following:

- prove a genuine centered increment contract directly and encode it as `S/H`-equivalent data;
- isolate a smooth exact-real component and a separate IEEE increment remainder;
- leave the execution remainder in the anchor/additive branch.

A discontinuous rounding map can violate any derivative-based Lipschitz inference near rounding boundaries.  This is the same mathematical obstruction already identified in `T-P5-009`; the coordinate transport theorem does not remove it.

---

## 10. Minimal theorem decomposition for Lean

The interface is best formalized in small finite-sum lemmas rather than importing a heavy matrix/operator-norm stack.

### 10.1 Component transport

```lean
-- H,S,Aabs are nonnegative scalar tables.
-- hState: |dxi j| <= sum k, S j k * |dz k|
-- hJac:   |de i| <= sum j, H i j * |dxi j|
-- hForce: |rc a| <= sum i, Aabs a i * |de i|
-- K a k := sum i, sum j, Aabs a i * H i j * S j k
-- conclusion: |rc a| <= sum k, K a k * |dz k|
```

This is only finite-sum monotonicity and distributivity.

### 10.2 Frobenius consumer

```lean
-- from |rc a| <= sum k K a k * |dz k|
-- prove sum a (rc a)^2
--    <= (sum a, sum k, (K a k)^2) * (sum k, (dz k)^2)
```

This is finite-dimensional Cauchy-Schwarz, or can be decomposed row-by-row.

Suggested theorem name:

```text
transported_jacobian_centered_gain
```

### 10.3 Anchor box transport

```lean
-- |braw i| <= c i
-- |b a| <= sum i Aabs a i * c i
-- conclude sum a (b a)^2 <= sum a (sum i Aabs a i*c i)^2
```

Suggested theorem name:

```text
force_map_anchor_box_to_B2
```

### 10.4 Diagonal exact-rational corollary

For diagonal `A`, a focused arithmetic theorem can expose (20)-(21) directly.  A Route-B-specific corollary may instantiate `A=(1/5,1/10)` but should be clearly tagged `raw_pmi_force`; the generalized-force specialization must instantiate `A=I`.

### 10.5 Composition frontend

A final scalar theorem need only reuse `T-P5-021`:

```text
ell2 <= ell2_transport,
B2 <= B2_transport,
C_transport > 0,
C_transport^2 > 621465600*ell2_transport*Vstar*B2_transport
```

implies existence of the rational `mu_bal` witness for the P5 centered/anchor consumer.

No source semantics should be hidden inside that scalar theorem.

---

## 11. What remains unclosed

This child reduces, but does not solve, the physical interface.  The source/P8 lanes still need to provide:

1. the exact consumer-to-source state ordering/scaling or component transport matrix `S` on the same first-exit domain;
2. a force-coordinate tag and map `A`, with no double normalization;
3. certified Jacobian intervals `H` for smooth exact-real residual components, or a direct centered increment theorem for non-smooth execution components;
4. nominal-anchor component boxes `c_i` along the same nominal flowpipe;
5. for every distal/non-block source coordinate, either a zero-difference proof, a transport row in `S`, an expanded Lyapunov state, or a separate additive/transverse routing;
6. P8 nominal flowpipe coverage / ODE continuation and the usual source semantic binding.

The most important new obstruction is item 5: a four-state `ell2` cannot consume source variation in an independently moving full-state coordinate.

---

## 12. Recommended checker contract

A future source checker should emit one typed object per residual family:

```text
consumer_state_order
source_state_order
state_transport_S
force_coordinate = raw_pmi_force | generalized_force
force_map_A
jacobian_abs_bound_H
anchor_component_box_c
ell2_transport
B2_transport
barrier_Vstar
C
Delta = C^2 - 621465600*ell2_transport*Vstar*B2_transport
```

plus the source/domain binding for every interval.  The mathematical checker then only recomputes the finite sums and verifies `C>0`, `Delta>0`.

This avoids three recurring mistakes at once: hidden state-order mismatches, charging common ramp coordinates unnecessarily, and applying the force normalization twice.

**Status:** `pending`.  待封不觉独立验证 / 待梁智炜收割与最终整合。 No P5/P8/M4 or registry status is changed by this review.
