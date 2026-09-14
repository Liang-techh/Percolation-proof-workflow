---
kind: review_result
review_id: review-T-P5-265-rational-radial-polynomial-interval-certificate-guyuefangyuan-20260910T1729Z
task_id: T-P5-265-RATIONAL-RADIAL-POLYNOMIAL-INTERVAL-CERTIFICATE
reviewer: 古月方源
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-10T17:29:00Z
claim_commit: f0411e8b1af058c095d9cf618b19765d1504b4da
inspected_commit: 66ce97393a21d0db9a52f75dc1f271af751fd70c
upstream_commits:
  - 32dbdb379152b48355b110682cfc1314c0ff231a  # T-P5-264 parity-symmetric homogeneous energy allocator
  - f4704792f1420aef65ad19af2e03ece571bf494e  # T-P5-263 higher-degree matched-metric Banach polarization
  - 7a684d6d780bc287bd62ffab96d4db3897767851  # T-P5-262 rational AM-GM metric bridge
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_local_Bernstein_interval_identity; add_Bernstein_convex_hull_bound; add_exact_deCasteljau_subdivision; add_strict_margin_finite_rational_certificate; add_radial_energy_consumer; keep_zero_margin_fallback_open
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact univariate polynomial algebra, Bernstein-basis conversion, rational de Casteljau subdivision, coefficient/derivative estimates, exact rational regressions; no provenance/receipt/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-265 — Rational Bernstein certificate for signed radial energy polynomials

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-264 shows that once same-parity or same-total-degree cancellation is retained, a consumer must verify the resulting signed radial expression on the **entire** interval `0 <= q <= R`; checking only `q=R` is unsound because a negative high-order coefficient reverses the usual outer-radius inequality.

This child closes the missing exact-real interval-consumer layer for polynomial radial envelopes. The central result is:

> For a rational polynomial `A(q)` and rational `R>0`, every strict bound
>
> `A(q) < K  for all q in [0,R]`
>
> admits a finite, entirely rational Bernstein-subdivision certificate. Each leaf consists only of rational endpoints and rational Bernstein coefficients. No floating root finder, eigensystem, square root, pseudoinverse, or sampled maximization is required.

The certificate is **sound for non-strict bounds** whenever all leaf coefficients pass, and it is **complete for strict bounds** in the sense above. Failure to find such a tree is therefore not a mathematical FAIL at zero reserve; exact touching cases may need algebraic factorization, Sturm/subresultant root isolation, or another univariate nonnegativity witness.

No deployed P5 polynomial split, source chart, actual radial metric/radius, cell/trajectory/FD-halo coverage, Float64 semantics, Lean/kernel proof, independent verifier action, admission, registry mutation, or parent closure is claimed.

---

## 1. Radial consumer produced by T-P5-264

Write

`q := Q(u) = u^T W u`,  `0 <= q <= R`.

After exact homogeneous decomposition and any permitted same-total-degree / same-parity simplification, a typical energy packet has the form

**(1.1)** `||P(u)||^2 <= q A(q)`

with a rational polynomial

**(1.2)** `A(q)=a_0+a_1 q+...+a_m q^m`.

The coefficients `a_j` are allowed to have either sign. Their sign is the whole point: a negative higher-order energy layer may represent genuine cancellation and should not be destroyed by replacing it with an absolute value.

To consume a constant Lyapunov reserve `K q`, it is enough to prove

**(1.3)** `A(q) <= K  on [0,R]`.

Equivalently define

**(1.4)** `p(q):=K-A(q)`

and prove `p(q)>=0` on the full radial interval.

Everything below is one-dimensional exact algebra applied to (1.4).

---

## 2. Local Bernstein coordinates on a rational interval

Let `p` have degree at most `n`. Fix rational `a<b` and set

`h=b-a`, `t=(q-a)/h in [0,1]`.

The degree-`n` Bernstein basis is

**(2.1)** `B_{i,n}(t)=binom(n,i) t^i (1-t)^(n-i)`,  `0<=i<=n`.

These basis functions satisfy

**(2.2)** `B_{i,n}(t)>=0`,

**(2.3)** `sum_i B_{i,n}(t)=1`.

Taylor expansion around `a` is exact:

**(2.4)**

`p(a+h t)=sum_{k=0}^n c_k t^k`,

where

**(2.5)** `c_k = h^k p^(k)(a)/k!`.

Use the exact power-to-Bernstein identity

**(2.6)**

`t^k = sum_{i=k}^n [binom(i,k)/binom(n,k)] B_{i,n}(t)`.

Therefore

**(2.7)**

`p(a+h t)=sum_{i=0}^n beta_i[a,b] B_{i,n}(t)`

with local Bernstein coefficients

**(2.8)**

`beta_i[a,b] = sum_{k=0}^i [binom(i,k)/binom(n,k)] h^k p^(k)(a)/k!`.

If the coefficients of `p` and the endpoints `a,b` are rational, every `beta_i[a,b]` is rational. In particular

`beta_0=p(a)`, `beta_n=p(b)`.

No approximation occurs in (2.7)-(2.8).

---

## 3. Theorem A — Bernstein convex-hull interval bound

From (2.2)-(2.3), equation (2.7) is a convex combination of the numbers `beta_i[a,b]`. Hence for every `q in [a,b]`,

**(3.1)**

`min_i beta_i[a,b] <= p(q) <= max_i beta_i[a,b]`.

Consequences:

1. If every `beta_i[a,b]>=0`, then `p(q)>=0` on the whole interval.
2. If every `beta_i[a,b]>0`, then

   `p(q)>=min_i beta_i[a,b]>0`.
3. Applied directly to `A`, if every Bernstein coefficient of `A` on `[a,b]` is at most `K`, then `A(q)<=K` on that interval.

This is a finite rational certificate: verify the coefficient conversion exactly, then compare finitely many rationals.

### Division-free serialization

The ratios in (2.8) have positive integer denominators. A checker may clear the common positive denominator `D` and verify

`D beta_i >= 0`

using integer arithmetic. The theorem does not rely on a particular denominator-clearing scheme.

---

## 4. Exact de Casteljau subdivision

A single Bernstein hull can be conservative. The standard de Casteljau recurrence provides exact rational refinement without re-expanding the polynomial.

Given coefficients `b_i^(0)=beta_i` and a rational split parameter `theta in [0,1]`, recursively define

**(4.1)**

`b_i^(r)=(1-theta)b_i^(r-1)+theta b_{i+1}^(r-1)`

for `r=1,...,n` and `i=0,...,n-r`.

Then the Bernstein coefficients of the restriction to the left subinterval are

**(4.2)** `L_r=b_0^(r)`, `r=0,...,n`,

and the right coefficients are the opposite edge of the same triangle,

**(4.3)** `R_r=b_r^(n-r)`, `r=0,...,n`

with the natural order chosen from the split point to the right endpoint.

For rational `theta`, every child coefficient is rational. The two child Bernstein polynomials represent exactly the same parent polynomial restricted to the two subintervals.

Thus a certificate tree needs only:

- rational leaf intervals;
- either their directly recomputed coefficients (2.8), or parent coefficients plus rational de Casteljau split data;
- at each leaf, finite coefficient inequalities.

There is no numerical root or maximum computation in the trusted core.

---

## 5. Theorem B — strict positivity has a finite rational subdivision certificate

The important point is not merely soundness. For a strict Lyapunov margin, the Bernstein tree is complete.

Assume

**(5.1)** `p(q)>=delta>0` for every `q in [0,R]`.

Write the rational power expansion

`p(q)=sum_{j=0}^n c_j q^j`.

For each `k>=1`, define the explicit coefficient bound

**(5.2)**

`M_k := sum_{j=k}^n |c_j| binom(j,k) R^(j-k)`.

Since

`p^(k)(q)/k! = sum_{j=k}^n c_j binom(j,k) q^(j-k)`,

we have for every `q in [0,R]`,

**(5.3)** `|p^(k)(q)|/k! <= M_k`.

Now take any subinterval `[a,b]` of length `h`. From (2.8), for each Bernstein coefficient,

`beta_i[a,b]-p(a)`

`= sum_{k=1}^i [binom(i,k)/binom(n,k)] h^k p^(k)(a)/k!`.

Because `0<=binom(i,k)/binom(n,k)<=1`, equations (5.2)-(5.3) imply

**(5.4)**

`|beta_i[a,b]-p(a)| <= E(h)`

where

**(5.5)** `E(h):=sum_{k=1}^n M_k h^k`.

Hence if

**(5.6)** `E(h)<delta`,

then every coefficient on every interval of length at most `h` satisfies

**(5.7)** `beta_i[a,b] >= delta-E(h)>0`.

For rational data, every `M_k` is rational. Choose a rational `h>0` satisfying (5.6), then use a finite rational partition of `[0,R]` with mesh at most `h`; a sufficiently deep dyadic subdivision works whenever `R` is rational.

Therefore every strictly positive rational polynomial on a rational compact interval has a **finite rational positive-Bernstein tree**.

### Corollary — semidecision completeness for strict PASS

If the true bound satisfies

**(5.8)** `A(q) <= K-epsilon` on `[0,R]` for some `epsilon>0`,

then `p=K-A` satisfies (5.1), so repeated rational subdivision must eventually reach a finite tree whose every leaf coefficient is positive.

The checker does not need to know the unknown exact minimizer of `p`; the leaf coefficients themselves provide a certified rational lower margin once a tree passes.

---

## 6. Certified reserve extracted from a passing tree

Suppose a finite partition `[a_s,b_s]` covers `[0,R]` and every leaf coefficient of `p=K-A` is nonnegative. Let

**(6.1)** `eta := min_{s,i} beta_i[a_s,b_s]`.

Then by Theorem A,

**(6.2)** `p(q)>=eta` on `[0,R]`.

If `eta>0`, the tree therefore proves the stronger bound

**(6.3)** `A(q)<=K-eta`.

Returning `eta` is useful downstream: the radial polynomial checker does not merely say PASS; it can export an exact rational reserve that later source/Float64 perturbation layers may consume.

---

## 7. Direct integration with T-P5-264 energy layers

Suppose T-P5-264 or a source-specific producer proves

**(7.1)**

`||P(u)||^2 <= q A(q)`, `q=Q(u)`, `0<=q<=R`.

If a Bernstein tree proves `K-A(q)>=0` on `[0,R]`, then

**(7.2)** `||P(u)||^2 <= K Q(u)`

through the whole centered source ball.

This permits genuine signed cross-degree cancellation to survive. No step replaces a negative coefficient by its absolute value, and no step applies the unsound rule

`negative * q^m <= negative * R^(m-1) q`.

If the tree returns `eta>0`, then the stronger result is

**(7.3)** `||P(u)||^2 <= (K-eta)Q(u)`.

That is exactly the constant-form interface expected by many Lyapunov reserve consumers.

### Rational-function extension

If a later allocator yields `A(q)=N(q)/D(q)` rather than a polynomial, the same route remains valid provided the source separately proves `D(q)>0` on `[0,R]`. Then

`A(q)<=K  <=>  K D(q)-N(q)>=0`.

Both denominator positivity and numerator-margin positivity may be given their own Bernstein trees. A denominator with unproved sign must not be cleared silently.

---

## 8. Exact regressions / negative controls

### Regression 1 — endpoint-only checking is false

Take `R=1` and

**(8.1)** `A(q)=4q(1-q)`.

Then

`A(0)=A(1)=0`,

but

`A(1/2)=1`.

Thus checking both radial endpoints would incorrectly certify any `K<1`.

In degree-2 Bernstein coordinates on `[0,1]`,

**(8.2)** `A(q)=0*B_{0,2}+2*B_{1,2}+0*B_{2,2}`.

The coarse convex-hull upper bound is `2`, so the checker correctly refuses `K=1` at this level.

Split exactly at `1/2`. The left Bernstein coefficients are

**(8.3)** `[0,1,1]`,

and the right coefficients are

**(8.4)** `[1,1,0]`.

Now the refined tree certifies the **sharp** bound `A(q)<=1` with rational arithmetic only.

This illustrates why subdivision is not cosmetic: it can recover cancellation/curvature hidden by the parent control polygon.

### Regression 2 — T-P5-264 radial cancellation example

For

`P(x)=x-x^3`, `q=x^2`, `0<=q<=1`,

we have

**(8.5)** `P(x)^2=q(1-q)^2`.

Hence `A(q)=(1-q)^2`. The outer boundary `q=1` alone gives `A(1)=0`, which cannot be used as a uniform zero reserve. The degree-2 Bernstein coefficients on `[0,1]` are

**(8.6)** `[1,0,0]`,

so the exact radial consumer immediately returns `A(q)<=1`, retaining the negative middle power instead of discarding it.

### Regression 3 — a true nonnegative polynomial may fail a coarse coefficient test

Take

**(8.7)** `p(q)=(q-1/2)^2>=0` on `[0,1]`.

Its degree-2 Bernstein coefficients on the whole interval are

**(8.8)** `[1/4,-1/4,1/4]`.

Therefore `all parent coefficients >=0` is only a sufficient test, not a necessary one. A split at `1/2` yields nonnegative child coefficients and closes this example, but the general zero-margin case is deliberately not declared complete by Theorem B.

---

## 9. Zero-margin boundary and fail-closed semantics

The strict-completeness theorem is intentionally a **strict-margin theorem**.

If `p(q)>=0` but `min p=0`, then the derivative estimate (5.7) has no positive `delta` to dominate local coefficient excursions. A particular polynomial may still admit a finite nonnegative Bernstein tree, as Regression 3 does, but the present argument does not prove that every exact-touching rational polynomial will do so under rational subdivision.

Therefore the dispatcher must distinguish:

1. `BERNSTEIN_PASS`: a finite tree proves every required coefficient inequality. This is a valid exact interval theorem, even at zero margin.
2. `STRICT_SEARCH_NOT_YET_CLOSED`: subdivision has not yet passed. This is not evidence of a violating `q`.
3. `EXPLICIT_NEGATIVE_WITNESS`: an exact rational `q0 in [0,R]` with `p(q0)<0`, or another certified algebraic witness, gives real mathematical FAIL for that proposed bound.
4. `ZERO_MARGIN_ALGEBRAIC_FALLBACK`: if exact equality matters, use source-specific factorization/square identities or a proper Sturm/subresultant/algebraic-root certificate rather than rounding a numerical minimizer.

In particular, a timeout or depth limit in a Bernstein search is **INCONCLUSIVE**, not FAIL.

---

## 10. Monotonicity is an optional cheap special case

Sometimes the exact radial polynomial is monotone. If an independent Bernstein tree certifies

`A'(q)>=0` on `[0,R]`,

then

**(10.1)** `A(q)<=A(R)`.

Likewise, if `A'<=0`, the maximum is `A(0)`.

This is a sound endpoint reduction because the derivative sign is proved on the full interval. It must not be confused with checking endpoints without a monotonicity theorem.

The same rational Bernstein machinery can certify the derivative sign, so no new analytic primitive is needed.

---

## 11. Minimal certificate packet

A source-independent consumer can serialize:

```text
radial_polynomial_interval_packet:
  polynomial_coefficients: [c_0,...,c_n]   # exact rationals for p(q)=K-A(q)
  radius: R                                 # exact rational >0
  partition_tree:
    - interval: [a,b]
      bernstein_coefficients: [beta_0,...,beta_n]
      # OR parent coefficients + exact rational de Casteljau split transcript
  leaf_gate: all beta_i >= 0
  optional_exported_margin: eta = min leaf beta_i
```

Checker obligations:

- verify that leaves form a gap-free, overlap-compatible cover of `[0,R]`;
- verify each local Bernstein identity, either from (2.8) or by checked de Casteljau recursion;
- verify every coefficient inequality exactly;
- export `eta` only as the minimum of checked leaf coefficients;
- never infer a counterexample merely because a finite search depth failed.

For a rational-function packet, add a separately certified positive denominator tree before cross multiplication.

---

## 12. Suggested Lean theorem decomposition

The first formalization does not need root isolation.

Suggested leaves:

1. `pow_eq_sum_bernsteinBasis`  
   prove (2.6) over `ℚ`/`ℝ`.
2. `polynomial_eq_localBernsteinExpansion`  
   derive (2.7)-(2.8) after affine interval reparameterization.
3. `bernsteinBasis_nonneg` and `sum_bernsteinBasis_eq_one`.
4. `localBernstein_min_le_eval_le_max`  
   Theorem A.
5. `localBernstein_nonneg_of_coeff_nonneg`.
6. `deCasteljau_split_preserves_polynomial`  
   exact left/right restriction identity.
7. `powerCoeff_derivative_bound_on_nonneg_interval`  
   prove (5.3) from (5.2).
8. `localBernstein_coeff_close_to_leftEndpoint`  
   prove (5.4).
9. `strictPositive_has_finite_dyadicBernsteinCertificate`  
   analytic/existence layer for Theorem B; this may be formalized after the finite checker leaves.
10. `radialEnergy_le_quadratic_of_BernsteinCertificate`  
    combine (7.1) with `p=K-A>=0`.
11. `radialEnergy_strictReserve_of_positiveLeafMargin`  
    export (7.3).

For the trusted checker path, leaves 1-6 and 10-11 are already enough to validate a supplied finite certificate. The search-completeness theorem 9 is mathematically useful but need not sit in the kernel-critical execution path.

---

## 13. What this closes and the next seam

This child closes the abstract full-interval consumer left open by T-P5-264:

- signed radial cancellation can be retained safely;
- a finite rational certificate proves the complete interval bound;
- strict true bounds are guaranteed to possess some finite rational subdivision certificate;
- a passing tree exports an exact rational residual margin;
- endpoint-only and search-failure shortcuts are explicitly ruled out.

The next genuinely source-facing seam is now narrower: extract the **actual P5 homogeneous components in one fixed source chart/output metric**, compute the exact total-degree energy layers `H_n`, simplify algebraic cancellations before absolute-value/Young allocation, and feed any resulting radial polynomial into this T-P5-265 consumer. If the actual cell is shifted rather than centered, first re-expand about the certified cell center (or prove a one-sided affine-cell theorem) instead of silently applying the `u -> -u` symmetry from T-P5-264.

All actual source reification, chart/metric identity, cell symmetry, parameter compatibility, trajectory/FD-halo coverage, Float64/interval semantics, Lean/kernel receipt, independent verification by 封不觉, admission, and registry decisions remain OPEN.
