---
kind: review_result
review_id: review-T-P5-240-quotient-rankone-pivot-transport-guyuefangyuan-20260910T1121Z
task_id: T-P5-240-QUOTIENT-RANKONE-PIVOT-TRANSPORT
reviewer: 古月方源
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-10T11:21:00Z
claim_commit: 88862cf741dcba389986eae8810b2b5c718658a6
inspected_commit: 73e5febae1d3ac2733d7bdea067fc244e2f551d1
upstream_commits:
  - daefc28428fc4aeb2461cb70a454e4052cfa3555  # T-P5-239 rank-one two-cap fiber/secular bridge
  - 73e5febae1d3ac2733d7bdea067fc244e2f551d1  # corrected T-P5-239 determinant/gradient typo
  - fedaaff853ce28e1e4496d227382498f1e7d06ad  # T-P5-236 quotient coercivity / recentering
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_common_center_quotient_transport; add_rankone_pivot_certificate; add_whitening_free_axial_fiber_decomposition; add_generalized_metric_fractionfree_secular_packet; add_dimension_ge3_rational_repeated_eigenvalue_gate; preserve_dim2_algebraic_branch
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact finite-dimensional quadratic algebra, congruence/rank identities, determinant multiplicity argument, rational regression; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-240 — quotient rank-one pivot transport without whitening

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-239 leaves a source-facing seam: the useful affine-target branch assumes that, after equality quotient, common recentering, radius normalization and whitening of the first source cap, the second cap is `a I + rank-one`. The source should not have to construct a floating matrix square root or floating eigenvectors merely to decide whether this branch applies.

This child removes that requirement. The whole branch can be recognized and consumed in exact quotient coordinates.

The main results are:

1. common constrained recentering commutes exactly with the equality quotient;
2. `scalar + rank-one after whitening` is equivalent to the **unwhitened** rank condition `rank(B2-a B1)=1`;
3. for a nonzero symmetric rank-one difference, one diagonal pivot gives an O(n^2) fraction-free certificate `d D = c c^T`;
4. the pivot certificate produces a square-root-free axial/transverse decomposition in the `B1` metric and reproduces the exact T-P5-239 two-cap fiber geometry;
5. the affine-quadratic fiber trust-region/secular packet can be written directly in a rational transverse metric, with no whitening;
6. in quotient dimension `n>=3`, a nonproportional rational cap pair can only have this branch at a **rational** repeated generalized eigenvalue `a`; in dimension two this is false and an algebraic-root branch must be retained.

No actual P5 cap pair, same-key quotient map, tube/cell coverage, Float64 enclosure, Lean receipt, independent validation, admission, registry mutation, or parent closure is claimed.

---

# Part I — exact common-center transport through the equality quotient

## 1. Source packet before quotient

Let the two source caps on a lifted coordinate `y in R^m` be

`phi_i(y) = y^T P_i y + 2 h_i^T y + c_i <= rho_i`,  `i=1,2`,

with the linear equality

`A y = 0`.

Assume there is one **common constrained center** `y_c` and multipliers `nu_i` such that

`A y_c = 0`,

`P_i y_c + h_i + A^T nu_i = 0`,  `i=1,2`.

For any equality-feasible displacement `x` with `A x=0`,

`phi_i(y_c+x)`

`= phi_i(y_c) + x^T P_i x + 2 x^T(P_i y_c+h_i)`

`= phi_i(y_c) + x^T P_i x`,

because the cross term is `-2 x^T A^T nu_i=0`.

Define the effective radii

`r_i := rho_i - phi_i(y_c)`.

The nondegenerate ellipsoid branch is `r_i>0`. If `r_i=0`, that cap collapses on any direction where its quotient form is positive; if `r_i<0`, the common-center equality fiber is empty. These branches must not be silently normalized by a negative or zero radius.

Let `N` be any exact full-column basis of `ker(A)`, so `x=N xi`. Put

`K_i := N^T P_i N`.

Then the two source caps are exactly

`xi^T K_i xi <= r_i`.

For `r_i>0`, define the normalized quotient forms

`B_i := K_i / r_i`.

The source intersection is exactly

`xi^T B_1 xi <= 1`,

`xi^T B_2 xi <= 1`.

### Theorem A — `commonConstrainedCenter_quotientCentering`

The equations above are identities. In particular, one may do constrained recentering first and quotient second, or quotient first and use the induced center; the centered quadratic packet is the same up to a quotient basis congruence.

## 2. Quotient-basis invariance

If another exact quotient basis is `N' = N T` with invertible `T`, then

`B_i' = T^T B_i T`.

Therefore for every scalar `a`,

`B_2' - a B_1' = T^T (B_2-aB_1) T`.

Hence rank, definiteness, and the existence of the rank-one branch are quotient-coordinate invariants.

---

# Part II — whitening is unnecessary for the rank-one gate

## 3. Congruence equivalence

Assume `B_1>0`. A conceptual whitening uses the symmetric positive square root and forms

`C = B_1^{-1/2} B_2 B_1^{-1/2}`.

Then

`C-a I = B_1^{-1/2} (B_2-aB_1) B_1^{-1/2}`.

Because the congruence factor is invertible,

**`rank(C-aI) = rank(B_2-aB_1)`.**

Thus the T-P5-239 hypothesis

`C = a I + rank-one`

is equivalent to the exact unwhitened condition

**`rank(D)=1`, where `D:=B_2-aB_1`.**

No square root or eigenvector is needed to test the branch.

For source data stored before radius division, one may instead use

`Dhat_a := r_1 K_2 - a r_2 K_1`.

Since `Dhat_a = r_1 r_2 D`, positive radii imply

`rank(Dhat_a)=rank(D)`.

This is the fully denominator-cleared source-facing gate.

---

# Part III — one-pivot fraction-free rank-one certificate

## 4. Symmetric pivot identity

Let `D` be symmetric and nonzero. Suppose there is an index `p` with

`d := D_pp != 0`.

Let

`c := D e_p`,

so `c` is the p-th column and `c_p=d`.

Then the following are equivalent:

1. `rank(D)=1`;
2. the entrywise matrix identity

   **`d D = c c^T`**

   holds.

### Proof

If the identity holds, then `D=(1/d) c c^T`, so `rank(D)=1` because `c_p=d!=0`.

Conversely, any nonzero symmetric rank-one matrix has the form `sigma u u^T`. Choose `p` with `u_p!=0`; then `d=sigma u_p^2!=0` and `c=sigma u_p u`, giving

`c c^T = sigma^2 u_p^2 u u^T = d D`.

QED.

A nonzero symmetric rank-one matrix always has at least one nonzero diagonal entry, so the pivot search is complete.

### Checker consequence

The producer may submit `(a,p)`. The checker computes `D`, `d`, `c` and checks only

- `d != 0`;
- `d*D_ij = c_i*c_j` for all `i,j`.

This replaces generic 2x2-minor enumeration, SVD, eigensystems, and rank tolerances. If normalized denominators are undesirable, the identical pivot test is applied to `Dhat_a`.

### Important branch split

- `D=0`: proportional caps; route to the dominant/equal-cap branch rather than calling it rank one.
- pivot identity passes: exact rank-one branch.
- pivot identity fails for a proposed `a`: only that candidate is rejected. Unless `a` has been generated by a complete repeated-eigenvalue search, this is not yet a proof that no rank-one scalarization exists.

---

# Part IV — square-root-free generalized axial decomposition

## 5. Construct the generalized axis by one exact linear solve

Assume

`B_1>0`,

`D=B_2-aB_1=(1/d)c c^T`,

with `d!=0`.

Let `v` solve

`B_1 v = c`.

Define

`kappa := c^T v`.

Since `B_1>0` and `c!=0`,

**`kappa>0`.**

No explicit inverse is required in a certificate: a rational producer can submit `v`, and the checker verifies `B_1 v=c` and `kappa=c^T v>0`.

Define

`b := kappa/d`,

`mu := a+b`.

Equivalently the checker may use the division-free equation

`d b = kappa`,

then `mu=a+b`.

## 6. Exact decomposition of every quotient point

For any `xi`, set

`alpha := (c^T xi)/kappa`,

`w := xi-alpha v`.

Then

`c^T w = 0`,

and `xi=alpha v+w` is unique with `c^T w=0`.

Because `B_1 v=c`,

`v^T B_1 w = c^T w=0`,

and

`v^T B_1 v = c^T v=kappa`.

Therefore

**`xi^T B_1 xi = w^T B_1 w + kappa alpha^2`.**

For the second cap,

`B_2=aB_1+(1/d)cc^T`,

so

`xi^T B_2 xi`

`= a w^T B_1 w + a kappa alpha^2 + (c^T xi)^2/d`

`= a w^T B_1 w + kappa (a+kappa/d) alpha^2`

and hence

**`xi^T B_2 xi = a w^T B_1 w + mu kappa alpha^2`.**

This is exactly the T-P5-239 whitening decomposition, but expressed entirely in the original rational quotient metric.

## 7. Generalized spectrum without eigenvectors

The operator `B_1^{-1}B_2` acts as

`a I + v c^T/d`.

Hence every `w` with `c^T w=0` is a generalized eigenvector with eigenvalue `a`, while

`B_1^{-1}B_2 v = mu v`.

Thus the generalized spectrum consists of

- `a` with multiplicity `n-1`;
- `mu` with multiplicity `1`.

In particular, in the rank-one branch

**`B_2>0 iff a>0 and mu>0`.**

This is an exact positivity gate for the second normalized source cap after `B_1>0` is known.

---

# Part V — exact two-cap fiber geometry in the B1 metric

## 8. Transverse radius

Put

`t := w^T B_1 w >= 0`.

The two normalized source caps become

`t + kappa alpha^2 <= 1`,

`a t + mu kappa alpha^2 <= 1`.

Assume `a>0` and `mu>0`. For a fixed feasible `alpha`, the transverse variable lies in the exact `B_1`-metric ball

`t <= R^2(alpha)`,

where

**`R^2(alpha) = min(1-kappa alpha^2, [1-mu kappa alpha^2]/a)`.**

No Euclidean normalization is needed.

The scalar interval is the set on which both right-hand sides are nonnegative; equivalently

`kappa alpha^2 <= 1`

and

`mu kappa alpha^2 <= 1`.

## 9. Dominance and crossing directly from two rational scalars

Because the only generalized eigenvalues are `a` and `mu`:

- first cap contained in second iff `a<=1` and `mu<=1`;
- second cap contained in first iff `a>=1` and `mu>=1`;
- the genuine non-dominating crossing regime is exactly

  **`(a-1)(mu-1)<0`.**

When `mu!=a`, the two transverse radius formulas switch where

`1-kappa alpha^2 = [1-mu kappa alpha^2]/a`.

Thus

**`alpha_*^2 = (1-a)/(kappa (mu-a))`.**

In the crossing regime this quantity is positive and lies in the feasible axial interval. If one instead uses the whitened unit axial coordinate `s=sqrt(kappa) alpha`, this reduces to the T-P5-239 formula

`s_*^2=(1-a)/(mu-a)`.

The square root is therefore only a presentation choice, not part of the trusted mathematics.

---

# Part VI — affine target trust region in a rational transverse metric

## 10. Transverse coordinates

Let `Z` be any exact basis of the hyperplane

`ker(c^T)={w:c^T w=0}`.

Write `w=Z eta`. Define

`M := Z^T B_1 Z`.

Since `B_1>0` and `Z` has full column rank,

`M>0`.

Let the deployed quotient debit be the arbitrary affine quadratic

`q(xi)=q0+2 g^T xi+xi^T H xi`,

with symmetric `H`.

Substituting `xi=alpha v+Z eta` gives

`q(alpha,eta)`

`= q0 + 2 alpha g^T v + alpha^2 v^T H v`

`  + 2 ell(alpha)^T eta + eta^T G eta`,

where

`ell(alpha):=Z^T(g+alpha H v)`,

`G:=Z^T H Z`.

For fixed `alpha`, the source constraint is exactly

`eta^T M eta <= R^2(alpha)`.

Thus each fiber is an ordinary generalized-metric trust-region problem, still with exact rational matrices if the source packet is rational.

## 11. Fraction-free secular packet without whitening

For a fixed fiber radius square `r2=R^2(alpha)`, define

`K(lambda):=lambda M-G`.

In the regular boundary branch `K(lambda)>0`, the KKT stationarity equation is

`K(lambda) eta = ell(alpha)`,

and an active boundary satisfies

`eta^T M eta=r2`.

Let

`Delta(lambda):=det K(lambda)`,

`J(lambda):=adj K(lambda)`.

Since `eta=J ell/Delta`, the active-boundary secular equation is the exact denominator-cleared identity

**`ell^T J^T M J ell = r2 * Delta^2`.**

The packet also checks

- `lambda>=0`;
- `K(lambda)>=0` (strict in this regular inverse branch);
- the correct active source-radius branch for `R^2(alpha)`;
- feasibility of `alpha`.

If `Delta=0`, do not divide: retain the usual range/kernel hard-case branch. This is the direct generalized-metric analogue of T-P5-239 and removes the last mathematical need for whitening from the rank-one fiber dispatcher.

---

# Part VII — complete rational candidate generation in dimension >= 3

## 12. Why a valid repeated scalar is rational for rational source data

Assume `B_1,B_2` are rational symmetric matrices, `B_1>0`, quotient dimension `n>=3`, and the pair is nonproportional. Suppose there exists a real scalar `a` with

`rank(B_2-aB_1)=1`.

Then the generalized characteristic polynomial

`p(t):=det(B_2-tB_1) in Q[t]`

has `a` as a root of multiplicity `n-1`; the only other generalized eigenvalue is `mu!=a`.

If `a` were irrational with minimal polynomial degree at least two over `Q`, every Galois conjugate of `a` would also occur in `p` with multiplicity `n-1`. Therefore `p` would have degree at least

`2(n-1)>n`,

contradiction.

Hence

**for `n>=3`, any nonproportional rational rank-one scalarization has `a in Q`.**

This matters operationally: a rational checker is complete for this branch once it derives the repeated root exactly; it is not merely searching a rational subset of a real parameter.

## 13. GCD extraction packet

In the nonproportional rank-one branch,

`p(t)=const*(a-t)^(n-1)*(mu-t)`.

Therefore

`gcd(p,p')=const*(t-a)^(n-2)`.

For `n>=3`, an exact polynomial-GCD computation over `Q` can recover the unique repeated scalar `a`; the one-pivot identity then verifies rank one directly. This separates candidate generation from the trusted rank certificate.

A simple checker route is:

1. compute `p(t)=det(B_2-tB_1)` exactly;
2. compute `g=gcd(p,p')` over `Q`;
3. if the repeated-root pattern has the required degree/shape, extract rational `a`;
4. verify the pivot identity `d(B_2-aB_1)=c c^T`;
5. solve `B_1 v=c`, compute `kappa`, `mu`, and route by dominance/crossing signs.

The pivot identity remains the local proof object; the polynomial step only makes the search complete.

## 14. Dimension-two warning

For quotient dimension `n=2`, the rationality conclusion is false. Any nonproportional symmetric definite pair becomes a 2x2 symmetric matrix after conceptual whitening, and subtracting either generalized eigenvalue leaves rank one. Those eigenvalues can be quadratic irrational numbers even when both source matrices are rational.

Therefore an implementation must **not** reject the 2D rank-one branch merely because no rational `a` is found. It should either

- carry an algebraic root/isolation certificate for the generalized eigenvalue, or
- stay in an exact direct 2D quadratic solver.

This is a genuine completeness boundary of a rational-only repeated-root dispatcher.

---

# Part VIII — exact rational regression

## 15. Non-Euclidean 3D crossing example

Take

`B_1 = diag(2,3,5)`,

`a=1/2`,

`c=(1,2,1)^T`,

`d=1`,

and

`D=c c^T`

` = [[1,2,1],[2,4,2],[1,2,1]]`.

Then

`B_2=aB_1+D`

` = [[2,2,1],[2,11/2,2],[1,2,7/2]]`.

The pivot at coordinate 1 has `d=1`, first column `c`, and the identity `dD=cc^T` is exact.

Solving `B_1 v=c` gives

`v=(1/2,2/3,1/5)^T`,

and

`kappa=c^T v`

`=1/2+4/3+1/5`

`=61/30`.

Hence

`mu=a+kappa/d`

`=1/2+61/30`

`=38/15`.

Thus

`a=1/2<1<38/15=mu`,

so the caps are genuinely crossing. The exact switch is

`alpha_*^2`

`=(1-1/2)/[(61/30)(61/30)]`

`=450/3721`.

Equivalently the whitened axial square would be

`kappa alpha_*^2 = 15/61`.

This example demonstrates that all branch decisions can be made rationally in a non-Euclidean source metric; no square root or numerical eigenvector is present anywhere in the certificate.

---

# Part IX — failure modes and dispatcher contract

## 16. What a failed local gate does and does not mean

The following distinctions are essential:

1. `D=0` is not failure; it is the proportional/dominant branch.
2. Failure of the pivot identity for one guessed `a` only rejects that scalar.
3. For `n>=3`, exact repeated-root extraction plus failed pivot identity does rule out the desired `scalar + rank-one` structure at that repeated root; if the characteristic polynomial lacks an `(n-1)`-fold root altogether, the branch is structurally absent.
4. For `n=2`, absence of a rational `a` is inconclusive because the valid generalized eigenvalue can be algebraic.
5. Absence of the rank-one branch is not a mathematical safety FAIL. It only routes the source pair back to the generic noncommuting multi-cap branch. A true FAIL still needs a primal feasible source point with positive debit or another exact impossibility theorem.

## 17. Suggested theorem leaves

Minimal Lean/formalization leaves:

1. `commonConstrainedCenter_quotientCentering`
2. `quotientBasis_rankDifference_invariant`
3. `whitenedRankOne_iff_unwhitenedRankOne`
4. `symmetric_rankOne_iff_pivotOuterProduct`
5. `rankOnePivot_metricAxis_decomposition`
6. `rankOnePivot_secondCap_decomposition`
7. `rankOnePivot_posDef_iff_twoGeneralizedScalarsPos`
8. `rankOnePivot_exactFiberRadius`
9. `rankOnePivot_dominance_crossing_classifier`
10. `generalMetricFiber_fractionFreeSecular`
11. `rationalPencil_rankOneScalarization_repeatedScalar_rational_of_dim_ge_three`
12. `twoDimensional_rationalPair_rankOneScalarization_may_be_algebraic`

The first formal pass can avoid matrix square roots entirely. For `v`, use an explicit equation `B_1 v=c`; for the secular branch use `adj/det`; and for the repeated scalar use a producer-supplied exact polynomial-GCD packet.

---

# Part X — remaining obligations

## 18. Still open

This child does not prove:

- which actual P5 same-key source caps should be paired;
- an actual equality matrix `A`, quotient basis `N`, or common constrained center `y_c`;
- actual positive effective radii `r_1,r_2`;
- actual rational/exact quotient matrices `K_1,K_2`;
- that the deployed source pair passes the rank-one pivot/GCD gate;
- a deployed affine target `(q0,g,H)` or its fiber inequality;
- an actual same-tube/cell coverage statement;
- Float64/interval semantics;
- Lean/kernel compilation;
- independent validation by 封不觉;
- admission, registry, or P5/P8/M4 parent closure.

## 19. Next smallest source-facing seam

The next useful action is now concrete rather than generic:

**export one actual same-key pair of P5 quadratic source caps together with the existing equality quotient/common-center packet, form exact `r_i,K_i`, and run the denominator-cleared repeated-root + pivot classifier.**

The desired producer packet is only

`(A,N,y_c,nu_1,nu_2,r_1,r_2,K_1,K_2,a,p,c,d,v,kappa,mu)`

with exact equalities/signs. If the `(n-1)`-fold generalized root is absent, record that structural obstruction and keep the generic noncommuting branch; do not spend another mathematical round on whitening or numerical eigensystem reconstruction.
