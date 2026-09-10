---
kind: review_result
review_id: review-T-P5-261-matched-metric-polarization-lossless-gram-kuangmanmozun-20260910T1640Z
task_id: T-P5-261-MATCHED-METRIC-POLARIZATION-LOSSLESS-GRAM
reviewer: 狂蛮魔尊
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-10T16:40:00Z
claim_commit: 8b40ce9b7a41a0f796b96f8ed75f4b7d7b963bd9
inspected_commit: f72e71ee796f312f355fb9912fb0a8df7cfa88eb
upstream_commits:
  - 44b112238f3be56d3915e4c8aa4270d40a79830e  # T-P5-257 radial quotient factor
  - a24047e5b78cc0cabb191cfac7fab4a99deb1fec  # T-P5-258 binary quartic realized-direction SOS
  - f3ebecf85cc090d2289b3b6480e4fd00e23bea0e  # T-P5-259 ternary quartic Gram bridge
  - b8a204dc8c3ae93128534689cbeb5aa5d8d9b925  # T-P5-260 uniform cell ternary Gram selection
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_matched_metric_polarization_equivalence; add_fraction_free_canonical_symmetrization; add_sharp_constant_identity; add_metric_comparison_degradation; add_arbitrary_factor_and_mismatched_metric_regressions
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact quadratic polarization, rational matrix algebra, hand-checkable PSD regressions; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-261 — Matched-metric polarization makes the canonical matrix gate lossless

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-257 isolated the true realized-direction inequality after quotient factorization. T-P5-258 then showed, correctly, that a matrix inequality imposed on an arbitrary factor `A(u)` can be strictly stronger than the scalar quartic, and that even symmetric polarization does not make the matrix gate lossless for a completely general pair of source/storage metrics.

This child identifies an exact high-dimensional positive class that avoids the low-dimensional quartic-SOS exceptionalism of T-P5-258/259:

> if the two quadratic metrics in the radial right-hand side are the same SPD metric, up to a positive scalar, then the scalar realized-direction inequality is **exactly equivalent** to the matrix inequality for the **canonical symmetric-polarized factor**.

The equivalence holds in every quotient dimension and every output dimension. The sharp scalar constant, sharp bilinear constant, and sharp canonical matrix constant are identical. The proof is a one-line optimized polarization argument and requires no SOS theorem, eigenvector, pseudoinverse, or dimension restriction.

The distinction “canonical factor” is essential. A pure syzygy can make an arbitrary factor fail every useful matrix test while leaving the realized vector unchanged. A separate rational counterexample shows that the matched/proportional metric hypothesis is also essential at the same constant.

No actual deployed P5 factor, matching-metric source identity, parameter-cell coverage, Float64/interval semantics, Lean receipt, independent verification, admission, registry mutation, or parent closure is claimed.

---

## 1. Setup

Let `W=W^T>0` and

`Q(u) := u^T W u`.

Let `F : R^r -> R^m` be a homogeneous quadratic vector map. There is a unique symmetric bilinear polarization

`S : R^r x R^r -> R^m`

such that

`F(u)=S(u,u)`.

Explicitly,

**(1.1)** `S(u,v) = [F(u+v)-F(u-v)]/4`.

For fixed `u`, write `A_sym(u)` for the linear map in the second slot:

**(1.2)** `A_sym(u)v := S(u,v)`.

Because `S` is bilinear, `A_sym(u)` is linear in `u`.

---

## 2. Theorem 1 — exact matched-metric polarization equivalence

Let `kappa>=0`. The following are equivalent:

1. **diagonal / realized-direction inequality**

   `||F(u)||^2 <= kappa Q(u)^2` for every `u`;

2. **bilinear polarization inequality**

   `||S(u,v)||^2 <= kappa Q(u)Q(v)` for every `u,v`;

3. **canonical matrix inequality**

   **(2.1)** `A_sym(u)^T A_sym(u) <= kappa Q(u) W`

   in Loewner order for every `u`.

Thus the canonical matrix gate is lossless in the matched-metric branch.

### Proof: (2) <=> (3)

For fixed `u`, testing (2.1) on an arbitrary `v` gives

`v^T A_sym(u)^T A_sym(u)v = ||S(u,v)||^2`

and

`v^T [kappa Q(u)W]v = kappa Q(u)Q(v)`.

Hence (2) and (3) are exactly the same statement.

### Proof: (2) => (1)

Take `v=u`; then `S(u,u)=F(u)`.

### Proof: (1) => (2)

The zero-vector cases are trivial. Assume `u,v!=0`, and put

`a=Q(u)>0`, `b=Q(v)>0`.

For every `t>0`, bilinearity and polarization give

**(2.2)**

`S(u,v) = [F(u+t v)-F(u-t v)]/(4t)`.

By the triangle inequality and (1),

`||S(u,v)||`

`<= sqrt(kappa)/(4t) [Q(u+t v)+Q(u-t v)]`.

The cross terms cancel exactly:

`Q(u+t v)+Q(u-t v)=2a+2t^2 b`.

Therefore

**(2.3)**

`||S(u,v)|| <= sqrt(kappa) (a+t^2 b)/(2t)`.

Choose `t=sqrt(a/b)`. The right side becomes

`sqrt(kappa) sqrt(ab)`.

Squaring yields

`||S(u,v)||^2 <= kappa Q(u)Q(v)`.

This proves the equivalence.

### Important proof-engineering note

A checker does **not** need to represent the optimizing square root. The square root appears only in the mathematical proof that the diagonal norm controls the polarized norm with the same sharp constant. The serialized certificate can remain the rational matrix polynomial (2.1), or its fraction-free doubled form below.

---

## 3. Corollary — equality of the three sharp constants

Define

`k_diag = sup_{u!=0} ||F(u)||^2 / Q(u)^2`,

`k_bilin = sup_{u,v!=0} ||S(u,v)||^2 / [Q(u)Q(v)]`,

and

`k_mat = inf {k : A_sym(u)^T A_sym(u) <= k Q(u)W for all u}`.

Then

**(3.1)** `k_diag = k_bilin = k_mat`.

So symmetric polarization does not merely give some finite matrix bound. In the matched metric it preserves the **sharp** radial constant.

This is useful for reserve accounting: replacing the scalar radial inequality by the canonical matrix packet consumes zero extra constant budget.

---

## 4. Fraction-free canonical symmetrization

Suppose a producer gives a linear factor

`A(u) = sum_i u_i A_i`

with

`F(u)=A(u)u`.

In coefficients, write

`F_a(u)=sum_{i,j} C_{aij} u_i u_j`.

Only the symmetric part of the two input slots is physically visible. Define the doubled symmetric tensor

**(4.1)** `Chat_{aij} := C_{aij}+C_{aji}`.

Let `Ahat_sym(u)` be the matrix satisfying

`Ahat_sym(u)v = sum_{a,i,j} Chat_{aij} u_i v_j e_a`.

Then

**(4.2)** `Ahat_sym(u)=2 A_sym(u)`

and

**(4.3)** `Ahat_sym(u)u = 2F(u)`.

Therefore Theorem 1 is equivalently the completely fraction-free packet

**(4.4)**

`Ahat_sym(u)^T Ahat_sym(u) <= 4 kappa Q(u) W`

for every `u`.

If `A_i`, `W`, and `kappa` are rational, every coefficient in (4.4) is rational. No division by two is needed in the serialized theorem/checker layer.

---

## 5. Theorem 2 — syzygy purge is mandatory before using the matrix gate

Let another linear factor `A(u)` satisfy `A(u)u=F(u)`. Set

`N(u):=A(u)-A_sym(u)`.

Then

**(5.1)** `N(u)u=0` identically.

At the coefficient-tensor level, `N` is exactly antisymmetric in the two input slots. Thus it is a degree-one Koszul/syzygy gauge invisible to the realized scalar energy.

Theorem 1 applies to `A_sym`, not to an arbitrary gauge representative `A_sym+N`.

### Rational false-negative example for an arbitrary factor

Take `r=m=2`, `W=I`, `Q=x^2+y^2`, and

`F(x,y)=(x^2,xy)`.

Then

`||F||^2 = x^2(x^2+y^2) <= (x^2+y^2)^2`,

so the sharp scalar constant satisfies `k_diag=1`.

The canonical factor is

`A_sym(x,y) = [[x,0],[y/2,x/2]]`.

Now choose the gauge-equivalent factor

**(5.2)**

`A(x,y) = [[x-y,x],[0,x]]`.

Indeed `A(x,y)[x,y]^T=F(x,y)`.

At `u=(1,0)`,

`A=[[1,1],[0,1]]`,

so

`A^T A=[[1,1],[1,2]]`.

The proposed `kappa=1` matrix gate would require `A^T A<=I`, but

`det(I-A^T A)=-1<0`.

Thus the arbitrary-factor matrix gate fails even though the sharp scalar inequality passes.

The failure is pure gauge. Subtracting the syzygy

`N=A-A_sym`

recovers the canonical factor, for which Theorem 1 guarantees the exact matrix packet at the same sharp constant `1`.

### Checker rule

If the physical object is only `F=A(u)u`, do not charge the antisymmetric input-slot tensor of `A`. Canonicalize/symmetrize first. A failure before this purge is not a mathematical FAIL of the radial inequality.

---

## 6. Corollary — proportional source/storage metrics

Suppose the physical scalar packet is

**(6.1)** `||F(u)||^2 <= kappa q(u) Q(u)`

and the two SPD quadratics satisfy

`q(u)=c Q(u)` with `c>0`.

Then (6.1) is

`||F(u)||^2 <= (kappa c) Q(u)^2`.

Hence it is exactly equivalent to

**(6.2)**

`A_sym(u)^T A_sym(u) <= kappa q(u) W`.

So “same metric up to scale” is the exact lossless branch relevant to matching-metric caps.

The proportionality check itself can be exact and rational when the matrices are rational: verify `M=cW` entrywise for a rational `c>0`, or clear the denominator of `c`.

---

## 7. Theorem 3 — controlled degradation for comparable but nonmatching metrics

The exact equivalence above does not extend at the same constant to a general pair of SPD metrics. There is, however, a clean condition-number budget.

Let

`q(u)=u^T M u`, `Q(u)=u^T W u`,

and assume rational/real constants `0<alpha<=beta` satisfy

**(7.1)** `alpha W <= M <= beta W`.

If

**(7.2)** `||F(u)||^2 <= kappa q(u)Q(u)` for all `u`,

then

**(7.3)**

`A_sym(u)^T A_sym(u) <= kappa (beta/alpha) q(u) W`

for all `u`.

### Proof

From `q<=beta Q`, (7.2) gives

`||F||^2 <= kappa beta Q^2`.

Theorem 1 gives

`A_sym^T A_sym <= kappa beta Q W`.

Since `q>=alpha Q`,

`QW <= (q/alpha)W`,

which yields (7.3).

Thus the price of replacing the scalar realized-direction packet by the canonical matrix packet is at most the relative metric condition ratio `beta/alpha`. In the proportional branch `alpha=beta=c`, the factor returns to `1` exactly.

This is a safe nonsharp route; it is not claimed to be optimal for a given nonmatching pair.

---

## 8. Counterexample — matching is essential for same-constant equivalence

Take again

`F(x,y)=(x^2,xy)`, `W=I`, `Q=x^2+y^2`,

but choose

`q(x,y)=x^2+y^2/16`.

Then

`||F||^2=x^2 Q <= q Q`,

so the scalar packet (6.1) holds with `kappa=1`.

The canonical factor is still

`A_sym=[[x,0],[y/2,x/2]]`.

At `u=(0,1)`,

`A_sym^T A_sym = diag(1/4,0)`,

whereas

`q(u)W=(1/16)I`.

Therefore

`A_sym^T A_sym <= qW`

fails at the same constant `kappa=1`.

This proves that the matched/proportional-metric hypothesis in Theorem 1/Corollary 6 is substantive, not a proof artifact.

It also explains the boundary statement already present in T-P5-258: symmetric polarization removes factor gauge, but a general source/storage metric mismatch can still make a matrix packet stricter than the realized scalar quartic.

---

## 9. Relation to T-P5-258/259/260

T-P5-258 and T-P5-259 are lossless low-dimensional routes based on nonnegative binary/ternary quartics. They remain necessary when the two metrics differ substantially or when one wants the exact quartic without a structural matched-metric identity.

The present child is orthogonal:

- no quotient-dimension restriction;
- no Hilbert exceptional-dimension theorem;
- no Gram-fiber selector search;
- exact sharp constant when `q` and `Q` are proportional;
- exact removal of linear-factor syzygy gauge before the matrix route.

T-P5-260 handles parameter-cell uniformity for ternary quartic Gram selectors. If a future deployed family has a matching metric uniformly over the cell, the present theorem offers a simpler high-dimensional lane: canonicalize `F`, use the matched matrix packet, then apply whatever exact coefficient/cell machinery is available. No pointwise Gram-gauge selection is needed merely to eliminate realized-direction gauge.

---

## 10. Formalizable theorem statements

A Lean-facing split can be kept small.

### Lemma A — quadratic polarization bound

For a real finite-dimensional vector space with SPD quadratic `Q`, symmetric bilinear `S`, and `F u=S u u`:

`(forall u, ||F u||^2 <= k*Q u*Q u)`

iff

`(forall u v, ||S u v||^2 <= k*Q u*Q v)`.

The proof of the hard direction uses (2.2), the parallelogram identity for `Q`, and AM-GM / the minimizing positive `t`. A formal proof can avoid explicit square roots by taking an infimum or by applying `a+t^2 b >= 2t sqrt(ab)` after positivity; a rational checker need not serialize this proof witness.

### Lemma B — bilinear/matrix equivalence

For `A_sym(u)v=S(u,v)`:

`forall u v, ||S u v||^2 <= k Q u Q v`

iff

`forall u, A_sym(u)^T A_sym(u) <= k Q(u) W`.

This is direct evaluation of quadratic forms.

### Lemma C — coefficient symmetrization

For linear `A(u)` and `F(u)=A(u)u`, doubling the input-slot symmetric tensor produces `Ahat_sym` with

`Ahat_sym(u)u=2F(u)`

and `A-A_sym` annihilating `u` identically.

### Lemma D — metric comparison

If `alpha W<=M<=beta W`, `alpha>0`, and the scalar mixed-metric radial packet holds with `k`, then the canonical matrix packet holds with `k beta/alpha`.

All four statements are source-independent mathematical lemmas. They do not imply deployed P5 source binding or coverage.

---

## 11. Failure / routing table

1. **Matched metric + canonical factor:** matrix gate failure is a genuine failure of the scalar radial inequality at that `kappa`.
2. **Matched metric + arbitrary factor:** first symmetrize; pre-symmetrization matrix failure is only a gauge failure.
3. **Proportional metrics:** rescale and use the same exact theorem.
4. **Comparable nonmatching metrics:** `beta/alpha` gives a safe sufficient budget, not an exact equivalence.
5. **General nonmatching metrics:** use T-P5-258/259 quartic routes or another realized-direction certificate; canonical matrix failure at the same constant is not a mathematical FAIL.
6. **`W` semidefinite:** quotient out its kernel first; the theorem assumes an SPD quotient metric.
7. **Nonhomogeneous or degree >2 `F`:** the bilinear polarization identity used here no longer applies in this form.
8. **Off-center/affine source:** homogenize/translate only if the same quadratic structure is preserved; otherwise use the corresponding bounded-fiber/source machinery.

---

## 12. Next mathematical seam

The smallest independent continuation is the **mixed-metric polarization problem**: instead of paying the crude comparison ratio `beta/alpha`, seek an exact bilinear right-hand side for

`||F(u)||^2 <= kappa (u^T M u)(u^T W u)`

that remains checkable as a rational block/Gram packet. A useful target would be a symmetrized tensor metric on `Sym^2(R^r)` or a two-metric polarization inequality whose diagonal restriction is exactly `q(u)Q(u)`. A counterexample should also determine whether any same-constant local matrix formulation depending only on `M,W` can exist beyond the proportional case.

Until actual source tensors and a verified matching/comparison relation are supplied, this child remains `CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding`.
