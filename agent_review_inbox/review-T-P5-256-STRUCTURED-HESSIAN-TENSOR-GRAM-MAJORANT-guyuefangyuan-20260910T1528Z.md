---
kind: review_result
review_id: review-T-P5-256-structured-hessian-tensor-gram-majorant-guyuefangyuan-20260910T1528Z
task_id: T-P5-256-STRUCTURED-HESSIAN-TENSOR-GRAM-MAJORANT
reviewer: 古月方源
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-10T15:28:00Z
claim_commit: 94ee87b00055ddc3c61db5cc2f29fe4732c7e12e
inspected_commit: e26b81d7442c0520b19ff292d29ed1b6313e73fd
upstream_commits:
  - 17e8f3fec31828ef7992411c81102b4aa1852e01  # T-P5-255 Hessian-to-Jacobian Gram reserve
  - 598db594c600e1999d4ddf12cb0fb23df4ffbd70  # T-P5-254 shared-quotient Jacobian leakage certificate
  - ced7eda6a74e19487f9d5f7be60bc4610cb28c97  # T-P5-253 nonlinear source transversality reserve
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_coefficient_outerGram_CP_transport; add_fractionFree_ellipsoid_tensor_envelope; add_graded_polynomial_Hessian_majorant; add_affine_Hessian_twoGrade_corollary; add_singular_metric_and_mixed_kernel_dispatch
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact finite-dimensional PSD/Kronecker/tensor algebra; rational cancellation regressions; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-256 — Structured Hessian tensor Gram majorant

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-255 reduced the mixed nonlinear producer problem to the source-facing matrix
obligation

`B(s,theta)^T B(s,theta) <= kappa (theta^T M theta) G`,

where `G=D^T D`, and explicitly left open how to obtain `kappa` from a structured
polynomial/affine Hessian without collapsing to an ambient operator norm.

This child gives such a route.  The central observation is that coefficient
uncertainty should be transported as an **outer-Gram matrix**, not as independent
absolute-value bounds.  If

`B(a)=sum_i a_i B_i`

and the source gives the correlated coefficient packet

`a a^T <= h C`,

then, with `S v=(B_1 v,...,B_m v)`, one has the exact completely-positive
transport

**`B(a)^T B(a) <= h S^T (C tensor I) S`.**

This preserves signed/correlated cancellation encoded in `C`; no spectral norm,
SVD, pseudoinverse, square root, or floating rank decision is needed.

For a polynomial Hessian on an ellipsoid, homogeneous tensor powers then give a
graded bound with the correct radius law.  If `q(theta)=theta^T M theta <= R`
and the degree-`r` contracted Hessian mode is homogeneous of degree `r` in
`theta`, its Gram charge is `O(q R^(r-1))`.  A rational weighted-Young merge of
the finitely many grades produces one exact PSD matrix which can be compared
directly with `kappa G`.

No actual P5 Hessian tensor, source evaluator, same-cell/tube/trajectory
coverage, Float64/interval semantics, Lean receipt, independent verification,
admission, registry mutation, or parent closure is claimed.

---

# Part I — coefficient outer-Gram transport

## 1. Setup

Let `X,Y` be finite-dimensional real Euclidean spaces and let

`B_i : X -> Y`,  `i=1,...,m`,

be fixed linear maps.  For a coefficient vector `a in R^m`, define

`B(a)=sum_i a_i B_i`.

Define the stacked map

`S : X -> Y^m`,

`S v=(B_1 v,...,B_m v)`.

For a symmetric coefficient matrix `C`, write `C tensor I_Y` for its block
Kronecker lift to `Y^m`.

## 2. Lemma — exact outer-Gram identity

For every `a`,

**(2.1)**

`B(a)^T B(a) = S^T ((a a^T) tensor I_Y) S`.

Indeed, for every `v`,

`v^T B(a)^T B(a) v`
`= ||sum_i a_i B_i v||^2`
`= sum_ij a_i a_j <B_i v,B_j v>`.

This is exactly the quadratic form of the right-hand side.

## 3. Theorem 1 — completely-positive coefficient transport

Assume `h>=0`, `C=C^T>=0`, and

**(3.1)** `a a^T <= h C`.

Then

**(3.2)**

`B(a)^T B(a) <= h H_C`,

where

**`H_C := S^T (C tensor I_Y) S >=0`.**

### Proof

Kronecker multiplication by `I_Y` preserves PSD order:

`(a a^T) tensor I_Y <= h (C tensor I_Y)`.

Congruence by `S` preserves PSD order.  Apply (2.1). QED.

### Why this is the right source interface

The map

`C |-> S^T(C tensor I)S`

is positive.  Hence all exact coefficient correlations can be retained until the
last matrix comparison with `G`; they do not need to be replaced by a single
ambient norm.

A producer may use singular `C`.  This is important: singularity often records
an exact algebraic relation among coefficients and can encode cancellation that
an independent box loses.

---

# Part II — exact correlated-cancellation regression

## 4. Independent boxes can create a false obstruction

Take `X=Y=R`,

`B_1=1`, `B_2=-1`,

and the true one-parameter coefficient family

`a=t(1,1)`, `h=t^2`.

Then `B(a)=t-t=0` identically.

The exact correlated outer-Gram packet is

`a a^T = h C_exact`,

`C_exact=[[1,1],[1,1]]`.

With `S=(1,-1)^T`,

`H_exact=S^T C_exact S=0`.

Thus Theorem 1 recovers zero charge exactly.

If one forgets the relation `a_1=a_2` and keeps only the independent bounds
`|a_i|<=|t|`, a standard valid envelope is

`a a^T <= h (2 I)`

for all independent signs.  It gives

`H_box=S^T(2I)S=4`.

For a target quotient Gram `G=0`, the correlated packet proves the true identity
while the independent-box packet cannot pass any finite `kappa G` comparison.

Therefore **failure after coefficient decorrelation is only a failure of that
relaxation, not a mathematical failure of the Hessian branch.**  Exact linear
relations/syzygies among source coefficients should be compressed before the
Gram majorant is formed.

---

# Part III — ellipsoid rank-one envelope without whitening

## 5. Source ellipsoid packet

Let

`q(theta)=theta^T M theta`,

with `M=M^T>0` on the chosen source quotient.  Let

`d=det(M)>0`, `A=adj(M)`.

Then

`M A=A M=d I`, `A>0`.

The usual ellipsoid Cauchy inequality can be written without serializing
`M^{-1}` as

**(5.1)**

`d theta theta^T <= q(theta) A`.

Equivalently, for every `v`,

`d (v^T theta)^2 <= q(theta) v^T A v`.

A checker may consume `(d,A)` through the exact identities `MA=dI` and the PSD
facts instead of computing a floating inverse or square root.

## 6. Lemma — tensor-power envelope

For every integer `r>=1`, PSD Kronecker monotonicity applied repeatedly to (5.1)
gives

**(6.1)**

`d^r [theta^(tensor r)][theta^(tensor r)]^T`
`<= q(theta)^r A^(tensor r)`.

If `q(theta)<=R`, then `q^r<=q R^(r-1)`, hence

**(6.2)**

`d^r [theta^(tensor r)][theta^(tensor r)]^T`
`<= q(theta) R^(r-1) A^(tensor r)`.

More generally, for any fixed rational linear compression map `L_r`, let

`c_r(theta)=L_r theta^(tensor r)`.

Congruence by `L_r` gives

**(6.3)**

`d^r c_r c_r^T <= q R^(r-1) C_hat_r`,

where

**`C_hat_r=L_r A^(tensor r) L_r^T >=0`.**

Thus a producer may use the full tensor basis or any exact symmetric-monomial
compression.  Correlations created by duplicated monomials are retained by
`C_hat_r` rather than discarded.

If an additional scalar factor `s^(r-1)` occurs with `0<=s<=1`, the same envelope
remains valid because `s^(2r-2)<=1`.

---

# Part IV — homogeneous Hessian modes

## 7. One homogeneous mode

Suppose the degree-`r` contracted Hessian mode has a fixed expansion

`B_r(theta)=sum_i c_{r,i}(theta) B_{r,i}`,

where `c_r=L_r theta^(tensor r)` as above.  Let `S_r` be the stack of the
`B_{r,i}` and define

**(7.1)**

`H_hat_r := S_r^T (C_hat_r tensor I) S_r >=0`.

Theorem 1 plus (6.3) gives the fraction-free mode estimate

**(7.2)**

`d^r B_r(theta)^T B_r(theta)`
`<= q(theta) R^(r-1) H_hat_r`.

This is the desired anisotropic replacement for an ambient Hessian operator norm.
The whole tensor family is reduced once to the fixed matrix `H_hat_r`, which is
then compared against the actual quotient metric `G=D^TD`.

---

# Part V — graded polynomial Hessian merge

## 8. Rational matrix Young inequality

Let

`B(theta)=sum_{r=1}^p B_r(theta)`.

Choose positive rational weights

`lambda_r>0`, `sum_r lambda_r=1`.

For every `v`, weighted Cauchy gives

`||sum_r B_r v||^2`
`<= sum_r lambda_r^(-1) ||B_r v||^2`.

Therefore

**(8.1)**

`B^T B <= sum_r lambda_r^(-1) B_r^T B_r`.

The weights are producer choices.  Exact rational weights preserve checker
simplicity and can approximate an optimal balancing without introducing square
roots.

## 9. Theorem 2 — graded tensor Gram majorant

Assume `q(theta)<=R` and the mode packets (7.2).  Let `p` be the largest grade.
Then

**(9.1)**

`d^p B(theta)^T B(theta)`
`<= q(theta) K_hat(R,lambda)`,

with

**(9.2)**

`K_hat(R,lambda)`
`:= sum_{r=1}^p lambda_r^(-1) R^(r-1) d^(p-r) H_hat_r`.

Hence the single fixed PSD check

**(9.3)**

`kappa d^p G - K_hat(R,lambda) >=0`

implies, throughout the source ellipsoid,

**(9.4)**

`B(theta)^T B(theta) <= kappa q(theta) G`.

This is exactly the T-P5-255 mixed Hessian packet.

All variable dependence has disappeared from the final consumer matrix.  The
only source-side data are finite rational tensor coefficients, `(M,d,A)`, the
radius `R`, the rational Young weights, and one PSD comparison against `G`.
Rational denominators in the `lambda_r` may be cleared once by multiplying
(9.3) by a common positive integer.

---

# Part VI — application to polynomial/affine Hessians

## 10. Polynomial Hessian grading

Suppose the Hessian has a polynomial tensor expansion

`H_b(x)=H_0 + H_1[x] + ... + H_{p-1}[x^(tensor(p-1))]`.

T-P5-255 uses

`B(s,theta)v = E H_b(s theta)[theta,v]`.

The term coming from `H_{r-1}` equals

`s^(r-1) E H_{r-1}[theta^(tensor(r-1))][theta,v]`,

so it is homogeneous of degree exactly `r` in `theta`.  Therefore it has the
form required in Part IV, with the harmless factor `s^(r-1)` bounded by one on
`0<=s<=1`.

Consequently Theorem 2 converts any finite polynomial Hessian tensor into a
finite matrix packet with the sharp structural radius scaling

**degree `r` contracted mode -> charge proportional to `R^(r-1)`.**

No generic Hessian norm is needed.

## 11. Corollary — affine Hessian needs only two fixed Gram matrices

For the common affine case

`H_b(x)=H_0+H_1[x]`,

write

`B=B_1+B_2`,

where `B_1` is degree one in `theta` and `B_2` is degree two.  With one rational
`lambda in (0,1)`, Theorem 2 reduces the entire source family to

**(11.1)**

`kappa d^2 G`
`- lambda^(-1) d H_hat_1`
`- (1-lambda)^(-1) R H_hat_2 >=0`.

For the simple exact choice `lambda=1/2`, this becomes

**(11.2)**

`kappa d^2 G - 2 d H_hat_1 - 2 R H_hat_2 >=0`.

Thus affine Hessian certification is not an infinite family of operator-norm
checks: after exact tensor reification it is one rational PSD matrix inequality.
The producer may tune rational `lambda` if the symmetric `1/2` split is too
expensive.

---

# Part VII — singular metrics and kernel dispatch

## 12. Singular source metric `M`

The ellipsoid-to-tensor corollary above intentionally assumes `M>0` on the
chosen source quotient.  If ambient `M>=0` is singular, `q(theta)<=R` alone does
not control arbitrary motion in `ker(M)`: along `z in ker(M)`, `q(tz)=0` for all
`t`.

For a linear coefficient map `c=L theta`, existence of any finite global packet

`c c^T <= q C`

therefore forces

**`ker(M) subset ker(L)`.**

So a producer has three sound options:

1. quotient by exact source equalities until `M` is positive definite;
2. prove directly a coefficient outer-Gram packet `c c^T<=q C` on the true
   constrained source set;
3. if neither is available, report this adapter as inapplicable.

Failure of ambient positive definiteness is **not** a physical FAIL.

## 13. Mixed `ker(D)` gate survives exactly

Because every `H_hat_r>=0`, the final comparison (9.3) has a useful exact kernel
consequence.  If `v in ker(D)=ker(G)`, then

`v^T K_hat v=0`,

and hence every positively weighted mode charge satisfies

**`v^T H_hat_r v=0`.**

Equivalently,

`(C_hat_r^(1/2) tensor I) S_r v=0`

conceptually; no square root needs to be serialized.  With singular
`C_hat_r`, this only kills coefficient combinations visible on the true
coefficient support, which is precisely why correlation must be preserved.

A concrete violation of the actual T-P5-255 gate

`B(s,theta)v !=0` for some `v in ker(D)`

blocks the mixed/Jacobian lane.  By T-P5-255 it still does not block the weaker
radial endpoint lane.

Conversely, failure of (9.3) without such an actual kernel witness may merely be
Young/envelope conservatism.  The correct fallback is tighter coefficient
correlation or the direct matrix/radial polynomial, not a physical FAIL label.

---

# Part VIII — producer/checker contract

## 14. Minimal exact packet

A polynomial-Hessian producer can now serialize:

1. one common source key and `q(theta)=theta^TMtheta<=R`;
2. rational `d>0`, `A`, with the exact adjugate/inverse identities needed for
   `d theta theta^T<=qA` on the chosen quotient;
3. for each grade `r`, an exact coefficient map `L_r` and fixed tensor slices
   `B_{r,i}`;
4. `C_hat_r=L_r A^(tensor r)L_r^T`;
5. `H_hat_r=S_r^T(C_hat_r tensor I)S_r`;
6. positive rational Young weights summing to one;
7. a rational `kappa>=0` and the single PSD gate (9.3).

The consumer may then emit T-P5-255's

`delta_J(R)=kappa R`

and, when the same mixed packet is used directly at endpoint level,

`delta_b(R)=kappa R/4`.

Source reification must still establish that the recorded tensor slices really
are the Hessian of the same deployed source on the covered domain.

---

# Part IX — Lean decomposition

## 15. Suggested first leaves

The mathematical core can be formalized in small independent leaves:

- `coefficient_outerGram_cp_transport`
  - from `a*a^T <= h*C`, prove
    `(sum a_i B_i)^T(sum a_i B_i) <= h*S^T(C tensor I)S`;
- `ellipsoid_rankOne_adjugate_bound`
  - from the SPD/adjugate packet, prove
    `d theta theta^T <= (theta^T M theta) A`;
- `tensorPower_outerGram_bound`
  - transport the previous inequality through Kronecker powers;
- `homogeneousTensorMode_gram_bound`
  - prove (7.2) after a rational compression `L_r`;
- `weightedSum_gram_le`
  - matrix form of weighted Cauchy (8.1);
- `gradedPolynomialHessian_gram_majorant`
  - assemble (9.1)--(9.4);
- `affineHessian_twoGrade_majorant`
  - specialize to (11.1)/(11.2);
- `singularSourceMetric_coefficientKernelNecessary`
  - `c c^T<=qC` implies `ker(M) subset ker(L)` for linear `c=L theta`;
- `mixedMajorant_kernel_dispatch`
  - final `K_hat<=kappa G` forces zero mode charge on `ker(D)`.

The first implementation does not need pseudoinverse, matrix square root,
eigensystem, numerical rank, or a general optimizer.

---

# Part X — boundaries and next seam

## 16. What this closes

This child closes the pure mathematical chain

`structured polynomial Hessian tensor`

`=> correlated coefficient outer-Gram envelopes`

`=> graded fixed PSD majorant`

`=> T-P5-255 mixed Hessian Gram packet`.

It also shows why preserving coefficient covariance is not cosmetic: destroying
exact correlations can turn an identically zero Hessian combination into an
artificial positive charge.

## 17. What remains independent

This review does not establish:

- actual deployed P5 Hessian coefficients or their source hash;
- same-key `M,R,D,E` and tensor-basis convention;
- exact source-code-to-tensor reification;
- whether the mixed matrix gate or only the weaker radial gate is valid on the
  real domain;
- cell/tube/trajectory/flowpipe/stencil/continuation coverage;
- Float64/interval semantics;
- Lean/kernel compilation;
- independent verification by `封不觉`;
- admission, registry, or P5/P8/M4 parent closure.

## 18. Next distinct mathematical seam

After this result, a genuinely new lane is needed only if the fixed PSD majorant
(9.3) is too conservative on the actual packet.  The first fallback should not
be an ambient norm.  It should preserve the **radial polynomial** required by
T-P5-255:

`kappa q(theta)(theta^T G theta) - ||B(s,theta)theta||^2 >=0`.

A useful next child would identify exact tensor factorizations of
`B(s,theta)theta` through `D theta`, or give a quotient-covariant SOS/Gram
certificate for this scalar polynomial.  That route can succeed even when the
mixed `ker(D)` condition fails, and is therefore mathematically distinct from
further tightening the matrix-Gram lane.

Status remains **CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding**.
No provenance/receipt/admission upgrade or parent closure is asserted.