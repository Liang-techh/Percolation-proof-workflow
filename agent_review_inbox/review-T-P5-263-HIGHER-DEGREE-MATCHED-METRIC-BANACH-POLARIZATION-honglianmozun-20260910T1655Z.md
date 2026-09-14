---
kind: review_result
review_id: review-T-P5-263-higher-degree-matched-metric-banach-polarization-honglianmozun-20260910T1655Z
task_id: T-P5-263-HIGHER-DEGREE-MATCHED-METRIC-BANACH-POLARIZATION
reviewer: 红莲魔尊
agent: 红莲魔尊
source_agent: 红莲魔尊
created_at: 2026-09-10T16:55:00Z
claim_commit: b8fc7dbd908b707ff68ace9023354da8f7a0e6f5
inspected_commit: 2d4cfbc440f7e9972fa99a760e294e4a6fe7ccae
upstream_commits:
  - f17933375d1275a5ad9ecff9bf810d0678e5c113  # T-P5-261 matched-metric polarization
  - a24047e5b78cc0cabb191cfac7fab4a99deb1fec  # T-P5-258 binary realized-direction quartic
  - f3ebecf85cc090d2289b3b6480e4fd00e23bea0e  # T-P5-259 ternary quartic Gram bridge
concurrent_nonoverlap_claim:
  - 2d4cfbc440f7e9972fa99a760e294e4a6fe7ccae  # T-P5-262 mixed-metric AM-GM lane, 古月方源
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_higher_degree_matched_metric_Banach_equivalence; add_canonical_Jacobian_gate; add_fraction_free_homogeneous_serialization; add_source_ball_endpoint_and_increment_scaling; add_nonhomogeneous_counterexample
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: finite-dimensional Hilbert/symmetric-tensor algebra, Euler homogeneous identity, line-segment energy estimate, exact rational regressions; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-263 — Higher-degree matched-metric Banach polarization and canonical Jacobian energy gate

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-261 proved that for a homogeneous quadratic vector map and one matched SPD metric, the realized-direction Lyapunov inequality is exactly equivalent to the matrix inequality for the canonical symmetric polarization. Its own boundary section explicitly left `degree > 2` open because the elementary quadratic `u+tv / u-tv` argument no longer applies in the same form.

This child closes that mathematical seam in every finite degree.

The key observation is that the quadratic result is not exceptional. For a homogeneous degree-`d` vector polynomial `P`, the unique symmetric `d`-linear polarization `T` is controlled by the diagonal polynomial with **exactly the same norm constant** when the source uses one Hilbert/SPD metric. This is the classical Banach symmetric-tensor norm theorem, applied after scalarizing the output. Consequently the intrinsic Jacobian factor

`J_P(u)/d`

is a lossless replacement for an arbitrary factor `A(u)` satisfying `A(u)u=P(u)`, and the exact matrix packet is

**(0.1)**

`J_P(u)^T J_P(u) <= d^2 kappa (u^T W u)^(d-1) W`.

No polarization factorials, tensor coordinates, matrix square roots, pseudoinverses, eigenvectors, SOS theorem, or quotient-dimension restriction are required in the serialized packet. If the coefficients are rational, (0.1) is a rational polynomial-matrix inequality.

This is deliberately disjoint from the concurrently claimed T-P5-262 lane: that task studies **two nonmatching metrics** and AM-GM distortion. The present theorem keeps one matched SPD metric and instead removes the `degree=2` restriction.

No deployed P5 polynomial, actual same-key metric, source cell, parameter family, trajectory/FD-halo coverage, Float64 semantics, Lean receipt, independent verification, admission, registry mutation, or parent closure is claimed.

---

## 1. Setup

Let `V=R^r` and let `W=W^T>0`. Define the source/storage quadratic

**(1.1)** `Q(u)=u^T W u`.

Let `H` be a finite-dimensional real Hilbert output space with norm `||.||`.

Let

`P : V -> H`

be a homogeneous polynomial map of degree `d>=2`.

There is a unique symmetric `d`-linear map

`T : V^d -> H`

such that

**(1.2)** `P(u)=T(u,...,u)`.

Write `J_P(u)` for the Jacobian of `P` at `u`, viewed as a linear map `V -> H`.

Because `P` is homogeneous of degree `d`, Euler's identity gives

**(1.3)** `J_P(u) u = d P(u)`.

Differentiating the polarized representation gives the stronger identity

**(1.4)**

`J_P(u) v = d T(u,...,u,v)`,

with `u` occupying `d-1` slots.

---

## 2. Analytic dependency — Banach's symmetric multilinear norm theorem

For a continuous symmetric scalar `d`-linear form `L` on a real Hilbert space,

**(2.1)**

`sup_{||x_i||<=1} |L(x_1,...,x_d)| = sup_{||x||<=1} |L(x,...,x)|`.

Equivalently, the spectral norm of a real symmetric tensor is attained on a symmetric rank-one direction. This is the classical theorem usually referred to as Banach's theorem for symmetric tensors/homogeneous polynomials.

Modern references discussing this theorem include the symmetric-tensor literature; e.g. Jiang–Li–Zhang, SIAM J. Matrix Anal. Appl. 37 (2016), DOI `10.1137/141002256`, and Carando–Rodríguez, arXiv `1810.09373` / Linear Algebra Appl. 563 (2019).

The present review **uses (2.1) as an analytic dependency**. It does not claim that the repository already contains a Lean proof/import of (2.1). A future formalization should either import a theorem with exactly this real finite-dimensional statement or prove the needed finite-dimensional specialization.

The rest of the derivation below is elementary once (2.1) is available.

---

## 3. Theorem 1 — all-degree matched-metric polarization is lossless

Let `kappa>=0`. The following statements are equivalent.

### (A) Diagonal / realized-direction Lyapunov bound

For every `u in V`,

**(3.1)**

`||P(u)||^2 <= kappa Q(u)^d`.

### (B) Full symmetric multilinear bound

For every `u_1,...,u_d in V`,

**(3.2)**

`||T(u_1,...,u_d)||^2 <= kappa product_i Q(u_i)`.

Thus the same sharp `kappa` controls the diagonal polynomial and every polarized slot combination.

### Proof: (B) => (A)

Set all arguments equal to `u`. Then `T(u,...,u)=P(u)`, so (3.2) becomes (3.1).

### Proof: (A) => (B)

Equip `V` with the Hilbert norm

`||u||_W := sqrt(Q(u))`.

Fix a unit output vector `h in H` and scalarize the symmetric tensor:

**(3.3)**

`L_h(u_1,...,u_d) := <h,T(u_1,...,u_d)>`.

Its diagonal polynomial is

`L_h(u,...,u)=<h,P(u)>`.

By Cauchy–Schwarz in the output and (3.1),

`|L_h(u,...,u)| <= ||P(u)|| <= sqrt(kappa) ||u||_W^d`.

Applying Banach's theorem (2.1) in the `W`-Hilbert norm yields

**(3.4)**

`|L_h(u_1,...,u_d)| <= sqrt(kappa) product_i ||u_i||_W`.

Now take the supremum over all unit `h`. Since

`||z|| = sup_{||h||=1} |<h,z>|`,

(3.4) gives

`||T(u_1,...,u_d)|| <= sqrt(kappa) product_i ||u_i||_W`.

Squaring proves (3.2).

QED.

### Structural meaning

For a **single matched Hilbert metric**, polarization itself costs zero Lyapunov constant in every degree. The low-dimensional binary/ternary quartic exceptional theorems are therefore not needed merely because the nonlinear remainder has degree three, four, or higher. They remain relevant when the right-hand-side metrics are mismatched or when the polynomial packet has a different non-Hilbert structure.

---

## 4. Theorem 2 — exact canonical Jacobian matrix gate

Under the same assumptions, (3.1) is equivalent to the polynomial matrix inequality

**(4.1)**

`J_P(u)^T J_P(u) <= d^2 kappa Q(u)^(d-1) W`

for every `u`.

This is the direct all-degree extension of T-P5-261.

### Proof: diagonal bound => Jacobian gate

Fix `u,v`. By (1.4) and Theorem 1,

`||J_P(u)v||^2`

`= d^2 ||T(u,...,u,v)||^2`

`<= d^2 kappa Q(u)^(d-1) Q(v)`.

Since `Q(v)=v^T W v`, this says

`v^T J_P(u)^T J_P(u) v`

`<= v^T [d^2 kappa Q(u)^(d-1) W] v`

for every `v`, which is exactly (4.1).

### Proof: Jacobian gate => diagonal bound

Test (4.1) on `v=u`. Euler's identity (1.3) gives

`||J_P(u)u||^2 = d^2 ||P(u)||^2`.

The right side is

`d^2 kappa Q(u)^(d-1) Q(u)=d^2 kappa Q(u)^d`.

Cancel `d^2` to recover (3.1).

QED.

### Important consequence

The Jacobian gate is not merely a sufficient Lipschitz relaxation. For homogeneous `P` and one matched SPD metric it is **exactly equivalent** to the realized-direction energy inequality.

The only nontrivial analytic ingredient is the symmetric-tensor Banach theorem used in the forward direction.

---

## 5. Corollary — equality of the sharp diagonal and Jacobian constants

Define

**(5.1)**

`k_diag := sup_{u!=0} ||P(u)||^2 / Q(u)^d`,

and

**(5.2)**

`k_J := sup_{u!=0,v!=0} ||J_P(u)v||^2 / [d^2 Q(u)^(d-1)Q(v)]`.

Then

**(5.3)** `k_diag = k_J`.

Theorem 2 gives `k_J<=k_diag`.

Conversely set `v=u`. Euler gives

`||J_P(u)u||^2/[d^2Q(u)^d] = ||P(u)||^2/Q(u)^d`,

so `k_J>=k_diag`.

Therefore the intrinsic Jacobian factor introduces **zero sharp-constant loss**.

The coefficient `d^2` is forced by Euler and cannot be improved in a universal Jacobian statement. In one dimension, `P(x)=x^d`, `Q=x^2`, `J=d x^(d-1)` gives equality everywhere.

---

## 6. Canonical factorization and higher-degree syzygy purge

An implementation may be handed some homogeneous matrix polynomial `A(u)` of degree `d-1` such that

**(6.1)** `A(u)u=P(u)`.

There is no reason for a matrix norm/PSD test on this arbitrary factor to be lossless. It may contain a large radial syzygy invisible to the physical nonlinear vector.

The intrinsic factor is

**(6.2)**

`A_can(u) := J_P(u)/d`.

Euler gives

`A_can(u)u=P(u)`.

For any other factor define

`N(u)=A(u)-A_can(u)`.

Then

**(6.3)** `N(u)u=0` identically.

So all factor-gauge freedom is isolated in a radial syzygy. T-P5-261 performed this purge for degree two by symmetric input-slot polarization. Equation (6.2) is the all-degree intrinsic version.

### Checker rule

If `P` itself is the source object, construct `J_P` directly and test (4.1). Do not charge a producer-specific `A(u)` before removing the `N(u)u=0` gauge.

---

## 7. Fraction-free rational serialization

Suppose every component of `P` is a homogeneous degree-`d` polynomial with rational coefficients, `W` is rational SPD, and

`kappa=a/b`, with integers/rationals `a>=0`, `b>0`.

Then (4.1) is equivalent to the denominator-cleared polynomial-matrix PSD packet

**(7.1)**

`d^2 a Q(u)^(d-1) W - b J_P(u)^T J_P(u) >= 0`.

Every coefficient in (7.1) is rational.

This packet has several proof-engineering advantages:

- no `1/d` is serialized;
- no explicit symmetric `d`-tensor coordinates are serialized;
- no polarization sum with `2^d d!` denominators is needed;
- no matrix square root of `W` is needed;
- no pseudoinverse or eigenvector is needed;
- the polynomial degree is exactly `2d-2` in `u` on both sides.

The global PSD verification method is still a separate obligation. For example, a degree-four matrix polynomial may still require SOS, exact cell decomposition, or another trusted positivity checker. The theorem only proves that choosing the canonical Jacobian has not introduced extra mathematical conservatism.

---

## 8. Corollary — centered source ball gives exact endpoint leakage scaling

Assume (3.1) and let

**(8.1)** `B_R={u:Q(u)<=R}`.

For every `u in B_R`,

**(8.2)**

`||P(u)||^2 <= kappa R^(d-1) Q(u)`.

This is immediate from

`Q(u)^d = Q(u)^(d-1)Q(u) <= R^(d-1)Q(u)`.

Hence if a Lyapunov estimate has the form

**(8.3)**

`dot V <= -gamma Q(u) + L ||P(u)||^2`,

then the homogeneous nonlinear remainder is absorbed on `B_R` whenever

**(8.4)**

`L kappa R^(d-1) <= gamma`.

A strict decay reserve remains if the inequality is strict.

### Scaling fingerprint

A homogeneous degree-`d` nonlinear remainder consumes an endpoint energy budget of order

**(8.5)** `R^(d-1)`

relative to the quadratic storage metric.

For `d=2`, this is the familiar `O(R)` quadratic-remainder leakage. For cubic remainders it becomes `O(R^2)`, etc.

---

## 9. Corollary — source-ball Jacobian/increment leakage

The centered `W`-ball `B_R` is convex. If `x,y in B_R`, then the entire segment

`z(t)=y+t(x-y)`, `0<=t<=1`,

lies in `B_R`.

By the fundamental theorem of calculus,

**(9.1)**

`P(x)-P(y)=integral_0^1 J_P(z(t))(x-y) dt`.

From the exact Jacobian gate (4.1), every point on the segment satisfies

`||J_P(z(t))(x-y)||`

`<= d sqrt(kappa) R^((d-1)/2) ||x-y||_W`.

Integrating yields

**(9.2)**

`||P(x)-P(y)|| <= d sqrt(kappa) R^((d-1)/2) ||x-y||_W`.

Therefore

**(9.3)**

`||P(x)-P(y)||^2 <= d^2 kappa R^(d-1) Q(x-y)`.

This is the trajectory/FD-increment counterpart of the endpoint estimate (8.2).

The factor `d^2` is expected here: increments pay the Jacobian norm, while a single endpoint uses the sharper radial identity.

### Connection to the earlier Hessian/Jacobian lane

For `d=2`, (9.3) gives the exact homogeneous-quadratic scaling

`delta_J(R)=4 kappa R`.

Thus the desired `O(R)` Jacobian leakage appearing in the earlier nonlinear closure lane follows automatically once the quadratic remainder has a matched-metric realized-direction certificate. No separate projector or arbitrary-factor norm estimate is needed in that homogeneous branch.

---

## 10. Rational cubic regression — radial cubic map

Take `V=H=R^2`, `W=I`,

`Q(x,y)=x^2+y^2`,

and the cubic map

**(10.1)**

`P(u)=Q(u)u`.

Then

`||P(u)||^2=Q(u)^3`,

so (3.1) holds sharply with

`d=3`, `kappa=1`.

The Jacobian is

**(10.2)**

`J_P(u)=Q I + 2 u u^T`.

Because `(u u^T)^2=Q u u^T`,

**(10.3)**

`J_P(u)^T J_P(u)=Q^2 I + 8Q u u^T`.

The predicted exact gate is

`J^T J <= 9 Q^2 I`.

Indeed

**(10.4)**

`9Q^2 I-J^TJ = 8Q(QI-u u^T)`.

In two dimensions,

**(10.5)**

`QI-u u^T = [[y^2,-xy],[-xy,x^2]]`

`= [y,-x]^T [y,-x]`.

Hence the slack is an explicit rational rank-one SOS matrix times `8Q`, so it is PSD for every `u`.

On the radial test vector `v=u`, equality holds:

`J_P(u)u=3Q u=3P(u)`

and

`||J_P(u)u||^2=9Q^3`.

Therefore the `d^2=9` Jacobian coefficient is sharp even in this simple polynomial energy model.

---

## 11. Failure boundary — bounded-domain nonhomogeneous endpoint bounds do not differentiate

Homogeneity is substantive. A bounded-domain estimate that only looks like a degree-`d` radial bound cannot be differentiated into (4.1).

Take one dimension with

`Q(x)=x^2`,

source interval

**(11.1)** `3/4 <= x <= 1`,

and the nonhomogeneous polynomial

**(11.2)** `P(x)=x(1-x)=x-x^2`.

On this source interval,

`(1-x)/x <= 1/3`,

so

**(11.3)**

`P(x)^2 = x^2(1-x)^2 <= (1/9)x^4 = (1/9)Q(x)^2`.

Thus if one incorrectly treated this as a homogeneous quadratic packet with `d=2`, `kappa=1/9`, the fake Jacobian rule would predict

**(11.4)**

`|P'(x)|^2 <= (4/9)x^2`.

But at `x=1`,

`P'(1)=1-2=-1`,

so

`|P'(1)|^2=1 > 4/9`.

Therefore a local endpoint Lyapunov estimate on a bounded source set does **not** imply the derivative gate unless the homogeneous tensor structure is genuinely present.

This obstruction is exact and rational. For nonhomogeneous remainders, either split homogeneous components with separately justified bounds or return to the bounded-fiber/Hessian/interval machinery; do not invoke T-P5-263 wholesale.

---

## 12. Other fail-closed boundaries

1. **Mixed metrics.** The theorem requires one SPD Hilbert metric `W` repeated in every input slot. The product `(u^T M u)(u^T W u)` with nonproportional `M,W` is the separate T-P5-262 lane and is not solved here.

2. **Semidefinite `W`.** If `W` has a kernel, first prove that `P` descends to the quotient / annihilates the null directions in the required multilinear sense. Otherwise the Hilbert norm used by Banach's theorem is not defined on the original space.

3. **Sector/truncated-domain-only data.** For homogeneous `P`, a bound on a full centered ball of positive radius scales to all directions. A bound only on a sector or non-star-shaped cell does not automatically determine the full symmetric tensor norm.

4. **Nonhomogeneous polynomial.** Section 11 shows the endpoint-to-Jacobian implication can fail even in one dimension with rational data.

5. **Arbitrary factor.** The exact matrix gate belongs to `J_P/d`, not to a producer-specific `A(u)` satisfying only `A(u)u=P(u)`.

6. **Polynomial-matrix positivity remains.** Equation (7.1) is the right exact object, but this review does not claim a complete checker for its global PSD positivity in arbitrary degree/dimension.

7. **Formal dependency remains.** Banach's symmetric multilinear norm theorem is not shown to exist in the pinned Lean environment in this review.

---

## 13. Candidate theorem statements for formalization

A minimal Lean-facing decomposition could be:

### Lemma A — homogeneous Euler identity

For a degree-`d` homogeneous polynomial map `P`,

`deriv P u u = d • P u`.

In finite coordinates this can be stated directly for homogeneous polynomial tensors.

### Lemma B — diagonal-to-multilinear Banach bridge

For a symmetric `d`-linear real map `T` into a finite-dimensional inner-product space, with `P u=T u ... u`,

`(forall u, ||P u||^2 <= k * Q u ^ d)`

implies

`forall u_1 ... u_d, ||T u_1 ... u_d||^2 <= k * product_i Q u_i`.

This is the only lemma needing Banach's theorem / symmetric spectral-norm machinery.

### Lemma C — canonical Jacobian gate

Using

`J_P(u)v=d*T(u,...,u,v)`,

prove

`J_P(u)^T J_P(u) <= d^2*k*Q(u)^(d-1)*W`.

### Lemma D — converse via radial test

Test the matrix gate on `u` and use Euler to recover the diagonal bound.

### Lemma E — source-ball increment

On `Q<=R`, combine Lemma C with line integration on the convex ellipsoid to obtain (9.3).

The theorem split keeps the analytic Banach dependency isolated from the elementary polynomial/Lyapunov bookkeeping.

---

## 14. New structural fingerprint

The resulting higher-degree fingerprint is

**homogeneous nonlinear remainder -> intrinsic symmetric tensor -> Banach diagonal norm equality in one Hilbert metric -> canonical Jacobian `J/d` -> exact polynomial-matrix Lyapunov gate -> endpoint `R^(d-1)` absorption or increment `d^2 R^(d-1)` leakage.**

This extends the T-P5-261 matched-metric mechanism from quadratic maps to every homogeneous degree without invoking low-dimensional quartic SOS exceptionalism.

---

## 15. Remaining obligations

Still open and explicitly not upgraded by this child:

- bind the actual deployed P5 nonlinear remainder to a homogeneous polynomial `P`;
- prove the same-key source/storage metric is genuinely one SPD `W` or first quotient a PSD metric;
- obtain the actual rational `kappa` on the deployed parameter cell;
- prove source ball/cell, trajectory, FD stencil and halo coverage;
- choose/verify an exact polynomial-matrix positivity checker for (7.1) if the packet is consumed directly;
- provide Float64/interval semantics where numerical coefficients enter;
- formalize/import the finite-dimensional real Banach symmetric-tensor norm theorem;
- obtain pinned Lean/kernel evidence and independent 封不觉 verification;
- admission/registry propagation remains coordinator-owned.

---

## 16. Next nonoverlapping mathematical seam

A natural continuation that does not collide with T-P5-262 is the **sum-of-homogeneous-degrees energy allocator**:

`P(u)=P_2(u)+...+P_D(u)`.

If each homogeneous component has a matched-metric sharp constant `kappa_j`, seek an exact or optimally weighted bound for

`||sum_j P_j(u)||^2`

on `Q(u)<=R` that preserves signed/vector cancellation as far as possible instead of paying the naive `(sum_j sqrt(kappa_j) R^((j-1)/2))^2` triangle budget. A useful child should identify when orthogonality or common tensor range makes the cross-degree energy terms exact, and should give a rational fallback when cancellation cannot be certified.
