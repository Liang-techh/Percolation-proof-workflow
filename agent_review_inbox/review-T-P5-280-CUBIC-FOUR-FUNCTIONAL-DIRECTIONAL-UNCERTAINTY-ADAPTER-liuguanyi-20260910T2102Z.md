---
kind: review_result
review_id: review-T-P5-280-cubic-four-functional-directional-uncertainty-adapter-liuguanyi-20260910T2102Z
task_id: T-P5-280-CUBIC-FOUR-FUNCTIONAL-DIRECTIONAL-UNCERTAINTY-ADAPTER
reviewer: 柳冠一
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-10T21:02:00Z
claim_commit: b1d8c0467934429313fe97bf15715a44e638f31a
inspected_commit: f0cf42ddad5fa5b5a24c2e8ebb66b5c66e2fe4d8
upstream_commits:
  - 33443b55882d1560aabf53c0fe329dd2655dfbcf # T-P5-279 one-sided cubic lower support
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_cubicChordBarrier_identity; add_cubicFourFunctional_coordinateEquiv; add_directionalFeatureBox_lowerSupport; add_scalarBarrier_minimaxSharp; add_affineFiber_covariance; preserve_same_source_key_and_fail_closed_boundaries
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact polynomial identity derivation; endpoint-feature inversion; minimax information-class proof; affine fiber-coordinate transport; no provenance/receipt/admission audit and no Lean/kernel run
exit_code: not_applicable
source_hashes: source_independent_mathematical_child
---

# T-P5-280 — Cubic four-functional directional uncertainty adapter

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-279 established that signed cubic information on an oriented clamp fiber can be consumed directly rather than first being replaced by a symmetric absolute-value tube. The remaining source-to-math question is: if the producer naturally exposes a cubic coefficient/FD uncertainty family, what is the smallest interval-adapted summary that a clamp consumer can use without throwing away the useful directionality?

This review proves that, on a nondegenerate fixed interval, a cubic is exactly coordinatized by four endpoint-adapted linear functionals: its two endpoint values and the two endpoint values of an affine chord-remainder/curvature functional. Four one-sided bounds on those quantities give an exact shape-preserving directional lower support. If the downstream consumer must stay quadratic, the affine remainder can be replaced by its optimal scalar upper envelope `max(k_L,k_R)`, and that scalar is minimax sharp given only the four independent one-sided feature bounds.

No actual P5 source packet is bound here.

---

## 1. Setup

Let

`d(t) = a3 t^3 + a2 t^2 + a1 t + a0`,

on a fixed interval

`L <= t <= R`, `Delta := R-L > 0`.

Define endpoint values

`d_L := d(L)`, `d_R := d(R)`.

Define the affine chord-remainder functional

`r(t) := a3 (t+L+R) + a2`,

with endpoint values

`r_L := r(L) = a2 + a3(2L+R)`,

`r_R := r(R) = a2 + a3(L+2R)`.

Finally set

`h(t) := (t-L)(R-t) >= 0`

and the endpoint chord

`C(t) := ((R-t)d_L + (t-L)d_R)/Delta`.

The role of `r` is intrinsic: it is exactly the quotient between the cubic and its endpoint chord after the universal factor `(t-L)(R-t)` is removed.

---

## 2. Exact chord-barrier identity

### Theorem 2.1 — cubic chord factorization

For every cubic `d` and every `t`,

`d(t) = C(t) - h(t) r(t)`.

Equivalently, in fraction-free form,

`Delta d(t)`
` = (R-t)d_L + (t-L)d_R`
`   - Delta (t-L)(R-t) [a3(t+L+R)+a2]`.

### Proof

The difference between `d` and its affine endpoint interpolant vanishes at `L` and `R`; hence it contains `(t-L)(t-R)`. Direct expansion gives

`Delta d(t) - [(R-t)d(L)+(t-L)d(R)]`
` = Delta (t-L)(t-R)[a3(t+L+R)+a2]`.

Since `(t-L)(t-R) = -h(t)`, the displayed identity follows. ∎

Because `r` is affine,

`r(t) = ((R-t)r_L + (t-L)r_R)/Delta`.

Thus the entire cubic is reconstructed from exactly four endpoint features.

---

## 3. The four endpoint features are coordinates on cubic space

Define the feature map

`Phi_{L,R}(d) := (d_L,d_R,r_L,r_R)`.

In coefficient coordinates `(a0,a1,a2,a3)`, its matrix is

`[[1,L,L^2,L^3],`
` [1,R,R^2,R^3],`
` [0,0,1,2L+R],`
` [0,0,1,L+2R]]`.

Its determinant is

`(R-L)^2 = Delta^2 > 0`.

Hence `Phi_{L,R}` is a linear isomorphism.

An explicit inverse is

`a3 = (r_R-r_L)/Delta`,

`a2 = r_L - a3(2L+R)`,

`a1 = [d_R-d_L-a3(R^3-L^3)-a2(R^2-L^2)]/Delta`,

`a0 = d_L-a1 L-a2 L^2-a3 L^3`.

### Consequence 3.1

The packet `(d_L,d_R,r_L,r_R)` is not an auxiliary heuristic or a lossy transform. For fixed `L<R`, it is an exact Hermite-like interval coordinate system for the four-dimensional vector space of cubics.

This is important for source adapters: a coefficient uncertainty family can be projected into these four **linear** directions without solving for critical points and without taking absolute values of the raw coefficients.

---

## 4. One-sided four-functional source packet

Let `D` be any family of cubics on `[L,R]`. Suppose the source proves four one-sided bounds, valid for every `d in D`:

`d_L >= ell_L`,

`d_R >= ell_R`,

`r_L <= k_L`,

`r_R <= k_R`.

Define the affine endpoint interpolants

`A(t) := (R-t) ell_L + (t-L) ell_R`,

`B(t) := (R-t) k_L + (t-L) k_R`.

### Theorem 4.1 — shape-preserving directional lower support

For every `d in D` and `L<=t<=R`,

`Delta d(t) >= A(t) - h(t) B(t)`.

Equivalently,

`d(t) >= A(t)/Delta - h(t) B(t)/Delta`.

### Proof

The barycentric weights `(R-t)/Delta` and `(t-L)/Delta` are nonnegative. Therefore

`C(t) >= A(t)/Delta`.

Similarly, affine interpolation of the two upper bounds gives

`r(t) <= B(t)/Delta`.

Since `h(t)>=0`, multiplying the latter inequality by `-h(t)` reverses the useful direction:

`-h(t)r(t) >= -h(t)B(t)/Delta`.

Add this to the chord bound and apply Theorem 2.1. ∎

### Interpretation

This is the direct source-to-clamp adapter sought after T-P5-279. The source need not produce symmetric bounds `|Delta a_j|<=eps_j`. It may instead optimize four physically relevant linear functionals of the actual coefficient/FD uncertainty set.

If the projected feature set contains correlations, an even tighter pointwise support can be obtained by minimizing the exact linear combination induced by Theorem 2.1 over that joint feature set. The four-scalar theorem is the sharp guarantee after the producer intentionally retains only the four independent one-sided marginals above.

---

## 5. Degree-preserving quadratic consumer

The shape-preserving support in Theorem 4.1 is cubic because `h B` is quadratic times affine. Some existing P5 consumers intentionally stay in the quadratic clamp lane.

Set

`kappa := max(k_L,k_R)`.

Since `r` is affine,

`r(t) <= kappa`

on the whole interval. Therefore:

### Theorem 5.1 — quadratic lower barrier

For every `d in D`,

`d(t) >= A(t)/Delta - kappa h(t)`.

Fraction-free:

`Delta d(t) >= A(t) - Delta kappa h(t)`.

The right-hand side is quadratic in `t`.

If a downstream debit schema insists that the uncertainty penalty coefficient itself be nonnegative, use

`kappa_+ := max(0,k_L,k_R)`.

That is the optimal scalar under the additional schema constraint `kappa_+>=0`; mathematically, a negative `kappa` is valid and represents favorable curvature information.

---

## 6. Minimax sharpness of the scalar barrier

The previous scalar is not merely a convenient estimate.

### Theorem 6.1 — information-class optimality

Assume the consumer is told only the four independent inequalities

`d_L>=ell_L`, `d_R>=ell_R`, `r_L<=k_L`, `r_R<=k_R`

and wishes to replace the affine remainder by a single universal scalar `k` in

`d(t) >= A(t)/Delta - k h(t)`

for all compatible cubics.

Then necessarily

`k >= max(k_L,k_R)`.

Hence `kappa=max(k_L,k_R)` is minimax sharp.

### Proof

By Section 3, there exists a unique cubic whose four features simultaneously equal

`d_L=ell_L`, `d_R=ell_R`, `r_L=k_L`, `r_R=k_R`.

For this cubic the proposed inequality reduces, at every interior point where `h(t)>0`, to

`r(t) <= k`.

If `k_R=max(k_L,k_R)` and `k<k_R`, continuity of affine `r` implies `r(t)>k` for all interior `t` sufficiently close to `R`; the proposed lower barrier fails there. The case in which `k_L` is maximal is symmetric near `L`. ∎

### Corollary 6.2 — pointwise sharpness of the affine shape packet

Because the same compatible cubic can saturate all four endpoint features simultaneously, the affine remainder bound

`r(t) <= B(t)/Delta`

and hence Theorem 4.1 are pointwise sharp in the information class defined only by those four marginal bounds.

Thus any improvement must use extra source information: joint correlations, additional directional supports, degree structure, sign constraints, or realizability—not another manipulation of the same four numbers.

---

## 7. Exact source-side production from coefficient/FD uncertainty

Each feature is a linear functional of the coefficient vector `a=(a0,a1,a2,a3)`:

`d_L = [1,L,L^2,L^3] a`,

`d_R = [1,R,R^2,R^3] a`,

`r_L = [0,0,1,2L+R] a`,

`r_R = [0,0,1,L+2R] a`.

Therefore a convex coefficient/FD uncertainty set `U` may supply the packet using four exact directional optimization problems:

`ell_L = inf_{a in U} d_L(a)`,

`ell_R = inf_{a in U} d_R(a)`,

`k_L = sup_{a in U} r_L(a)`,

`k_R = sup_{a in U} r_R(a)`.

For a rational polytope these are ordinary exact rational linear programs / extreme-vertex checks. For an interval coefficient box they reduce to sign-aware endpoint choices in each of the four linear forms.

The key interface point is that **the producer should optimize the four interval-adapted directions directly whenever possible**. First replacing `U` by independent symmetric coefficient magnitudes and only then evaluating the four forms can be strictly looser, because it destroys coefficient correlations and direction signs before the clamp sees them.

No claim is made here that the deployed P5 producer actually exposes such a convex exact set; that is a source-binding obligation.

---

## 8. Affine fiber-coordinate covariance

The packet is compatible with the exact affine-chart philosophy of T-P5-247.

Let

`t = alpha u + beta`, `alpha>0`,

and write

`L=alpha l+beta`, `R=alpha r+beta`,

so `Delta_t = alpha Delta_u`.

Define

`d_tilde(u):=d(alpha u+beta)`.

Then endpoint values are unchanged as geometric values:

`d_tilde(l)=d(L)=d_L`,

`d_tilde(r)=d(R)=d_R`.

If `r_tilde` denotes the chord-remainder affine function constructed from the coefficients of `d_tilde` on `[l,r]`, direct substitution gives

`r_tilde(u) = alpha^2 r(alpha u+beta)`.

Hence

`r_tilde_l = alpha^2 r_L`,

`r_tilde_r = alpha^2 r_R`.

Also

`h_t(alpha u+beta)=alpha^2 h_u(u)`.

Therefore

`h_u(u) r_tilde(u) = h_t(t) r(t)`,

while the barycentric chord weights are invariant. The full support identity and all inequalities in Sections 4–6 are therefore exactly covariant under positive affine reparameterization.

For `alpha<0`, sort the transformed interval and swap the left/right endpoint labels; the two remainder endpoint values still scale by `alpha^2`. No floating normalization is mathematically required.

### Interface consequence 8.1

A pure affine reparameterization of the fiber must not be charged as coefficient uncertainty. Transport the four functionals exactly; only genuine source/model perturbations should consume Lyapunov reserve.

---

## 9. Algebraic or moving endpoints

If `L=L(q)` and `R=R(q)` are selected algebraic endpoint branches of the kind handled in T-P5-270/T-P5-276, all four features remain algebraic linear functionals of the cubic coefficients at fixed `q`:

`d(L(q))`, `d(R(q))`,

`a2+a3(2L(q)+R(q))`,

`a2+a3(L(q)+2R(q))`.

The identities of this review remain exact in the corresponding real algebraic field.

For an exact rational downstream packet there are two sound routes:

1. keep selected-root/algebraic signs and supports symbolically; or
2. replace the algebraic quantities by **certified outward rational** lower bounds for `ell_L,ell_R` and upper bounds for `k_L,k_R`.

An unproved Float64 evaluation of an algebraic endpoint is not an exact source packet and cannot inherit the theorem merely by numerical proximity.

---

## 10. Minimal theorem statements for formalization

A compact formal layer can be split as follows.

### 10.1 Exact identity

`cubic_chord_remainder_identity`

Assumptions: commutative ordered field, `L<R`, cubic coefficient tuple.

Conclusion:

`(R-L)*d(t)`
` = (R-t)*d(L)+(t-L)*d(R)`
`   -(R-L)*(t-L)*(R-t)*(a3*(t+L+R)+a2)`.

### 10.2 Coordinate equivalence

`cubic_fourFunctional_equiv`

For `L<R`, the linear map

`(a0,a1,a2,a3) -> (d_L,d_R,r_L,r_R)`

is invertible; determinant `(R-L)^2` and the inverse formulas of Section 3 are witnesses.

### 10.3 Directional box support

`cubic_fourFunctional_lowerSupport`

Assume the four one-sided inequalities in Section 4. Then the fraction-free lower support of Theorem 4.1 holds for every `t in [L,R]`.

### 10.4 Scalar minimax result

`cubic_scalarRemainder_minimax`

The least scalar `k` implied by only `r_L<=k_L`, `r_R<=k_R` such that `r(t)<=k` on `[L,R]` is `max(k_L,k_R)`.

### 10.5 Affine covariance

`cubic_fourFunctional_affine_covariant`

Under `t=alpha u+beta`, `alpha>0`, endpoint values are invariant, remainder endpoints scale by `alpha^2`, and `h*r` is invariant.

All checker-facing versions should prefer multiplication by the known positive `Delta` over division.

---

## 11. Suggested typed packet

A source-facing mathematical contract may be represented schematically as

```text
CubicDirectionalPacket(L,R):
  proof_delta_pos : 0 < Delta = R-L
  ell_L, ell_R, k_L, k_R
  source_key
  chart_id
  domain_id
  proof_same_family : forall d in source_family(source_key,chart_id,domain_id),
      d(L) >= ell_L
      d(R) >= ell_R
      r_L(d) <= k_L
      r_R(d) <= k_R
```

Consumers may expose two lanes:

```text
shape_support(t):
  Delta*d(t) >= A(t) - h(t)*B(t)

quadratic_support(t):
  Delta*d(t) >= A(t) - Delta*max(k_L,k_R)*h(t)
```

The first retains all four directional features. The second intentionally pays the exact information-loss price required to remain quadratic.

---

## 12. Fail-closed boundaries

1. **Degenerate fiber `R=L`.** The coordinate map is singular because the source set is a single point. Handle this separately as the scalar condition at that point; do not divide by `Delta`.

2. **Reversed orientation.** Sort/swap endpoints before applying the packet. Orientation changes labels, not the physical support.

3. **Feature-box failure is not physical failure.** If the four independent margins cannot fit the remaining Lyapunov reserve, report `INCONCLUSIVE_FROM_DIRECTIONAL_SUMMARY`. Correlations in the actual uncertainty set may still certify safety.

4. **A symmetric coefficient box is only a fallback.** It can produce sound feature bounds, but it may erase precisely the odd/directional information that T-P5-279 was designed to retain.

5. **Same-key requirement remains mathematical.** The four inequalities must refer to the same source uncertainty family, chart, interval and domain. Bounds spliced from incompatible packets do not define a valid common cubic family.

6. **Outer-envelope versus realizability.** A negative lower support for an outer coefficient envelope is not an actual state/trajectory counterexample. Physical FAIL still needs source-valid realization or an independently valid necessity theorem.

7. **No numerical exactness by declaration.** Float64/interval semantics, outward rounding and algebraic-endpoint evaluation remain source obligations.

---

## 13. What is closed / what remains open

### Closed mathematically in this child

- exact cubic chord-barrier factorization;
- exact four-functional coordinate isomorphism;
- shape-preserving lower support from four one-sided source bounds;
- optimal quadratic scalar barrier within the four-marginal information class;
- exact linear-functional producer directions;
- affine fiber-coordinate covariance;
- compatibility statement for selected algebraic endpoints;
- fail-closed semantics when the summary is insufficient.

### Still OPEN

- actual deployed P5 coefficient/FD perturbation family;
- proof that its four directional extrema come from one source key / chart / domain;
- whether joint feature correlations should be retained instead of a four-number box;
- exact source-cell and trajectory/state realizability;
- parameter/domain/FD-halo coverage;
- Float64 / interval / outward-rounding semantics;
- Lean/kernel formalization;
- independent verification by 封不觉;
- provenance / receipt / admission / registry / parent propagation.

---

## 14. Next mathematical seam

The next source-facing seam is now narrower than “bound cubic coefficients.” Given an actual P5 perturbation polytope or interval/affine-arithmetic packet in a fixed source key, compute its projection into the four feature coordinates and determine whether the **joint projected polytope** has exploitable correlations.

If it does, the exact pointwise lower uncertainty support is

`inf_{f in F} w(t)^T f`,

where `f=(d_L,d_R,r_L,r_R)` and the weights are those from Theorem 2.1. A useful next bridge would characterize source classes for which this support remains a low-degree piecewise polynomial/rational function of `t`, so that the gain over the independent four-margin box can be consumed without general-purpose CAD.
