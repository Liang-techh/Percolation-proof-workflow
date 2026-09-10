---
kind: review_result
review_id: review-T-P5-238-loewner-dominant-cap-single-slemma-honglianmozun-20260910T1051Z
task_id: T-P5-238-LOEWNER-DOMINANT-CAP-SINGLE-SLEMMA
reviewer: 红莲魔尊
agent: 红莲魔尊
source_agent: 红莲魔尊
created_at: 2026-09-10T10:51:00Z
claim_commit: 0aef505e72a42fd8e37b81d209cf8e8c5c9e6794
inspected_commit: a432476664e053d5c0d0725c99255ad0c3ef3da7
upstream_commits:
  - b13ca2b762a123748783cf2324b25b08f8b6b30d  # T-P5-237 multi-quadratic S-procedure gate
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_exact_centered_ellipsoid_containment_gate; add_dominant_cap_intersection_collapse; add_single_slemma_arbitrary_quadratic_debit_packet; add_fraction_free_rational_multiplier_packet; route_no_dominant_cap_as_inconclusive_not_fail
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact finite-dimensional quadratic algebra / S-lemma / Schur-complement reasoning only; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-238 — Loewner-dominant source cap and exact single-S-lemma Lyapunov closure

## 0. Verdict and seam

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-237 proves a useful lossless multi-quadratic class when all centered source quadratic parts and the centered target quadratic part are simultaneously diagonalizable by one congruence. It explicitly leaves the noncommuting branch open.

This child identifies a different exact positive class which is strictly beyond that simultaneous-congruence branch:

> If one centered positive-definite source ellipsoid is contained in every other source cap, the whole multi-cap intersection is exactly that one ellipsoid. The target may then be an arbitrary quadratic Lyapunov debit, including a signed linear cross term and a quadratic matrix which does not commute with any source matrix. The ordinary one-constraint S-lemma is lossless.

The containment test is an exact Loewner-order statement and has a fraction-free rational form. The resulting S-lemma certificate is a single PSD block and also has a fraction-free rational form. No square root, matrix inverse, pseudoinverse, eigenvector, simultaneous diagonalizer, generic SDP black box, or coordinatewise absolute-value relaxation is required in the trusted packet.

This is a mathematical child only. No actual P5 source matrices, same-key/tube binding, trajectory coverage, Float64 enclosure, Lean/kernel receipt, independent validation, admission, registry mutation, or parent closure is claimed.

---

# Part I — exact centered ellipsoid containment

## 1. Setup

Work after any equality quotient / redundant-coordinate removal has already been performed. Let the common source center be the origin in quotient coordinate `z in R^n`.

For source cap `i`, write

`E_i := { z : z^T D_i z <= rho_i }`,

with

- `D_i` symmetric;
- `rho_i > 0`.

For the cap proposed as the dominant one, indexed by `k`, assume additionally

`D_k > 0`.

It is convenient to define the normalized quadratic matrix

`A_i := D_i / rho_i`.

Then

`E_i = { z : z^T A_i z <= 1 }`.

## 2. Exact containment theorem

### Theorem A — `centeredEllipsoid_containment_iff_loewner`

If `D_k > 0` and `rho_k,rho_i>0`, then

**`E_k subseteq E_i` if and only if `A_i <= A_k` in Loewner order.**

Equivalently, without division,

**`rho_i D_k - rho_k D_i >= 0`.**

### Proof: sufficiency

Assume

`rho_i D_k - rho_k D_i >= 0`.

For any `z in E_k`,

`rho_k z^T D_i z <= rho_i z^T D_k z <= rho_i rho_k`.

Since `rho_k>0`,

`z^T D_i z <= rho_i`,

so `z in E_i`.

### Proof: necessity

Assume `E_k subseteq E_i`. Fix arbitrary nonzero `x`. Since `D_k>0`,

`x^T D_k x > 0`.

Scale `x` to the boundary of `E_k`:

`z = sqrt(rho_k/(x^T D_k x)) x`.

Then `z^T D_k z=rho_k`, hence `z in E_i`. Therefore

`z^T D_i z <= rho_i`.

Substituting the scale and cancelling the positive denominator gives

`rho_k x^T D_i x <= rho_i x^T D_k x`.

Since this holds for every `x`,

`rho_i D_k-rho_k D_i >=0`.

QED.

### Trusted arithmetic consequence

For rational `D_i,D_k,rho_i,rho_k`, the containment gate is already fraction-free:

`R_ki := rho_i D_k-rho_k D_i >=0`.

A checker only needs exact rational PSD verification of `R_ki`; no generalized eigenvalue or square root is required.

---

# Part II — dominant-cap collapse of a multi-source intersection

## 3. Intersection collapse

Let

`F := intersection_i E_i`.

Suppose there is an index `k` such that

`D_k>0`, `rho_k>0`,

and for every `i`,

`rho_i D_k-rho_k D_i >=0`.

Then Theorem A gives `E_k subseteq E_i` for all `i`. Since `F` is an intersection containing the factor `E_k`,

**`F = E_k`.**

### Theorem B — `dominantCenteredCap_intersection_eq`

Under the hypotheses above,

`intersection_i {z : z^T D_i z <= rho_i}`

`= {z : z^T D_k z <= rho_k}`.

No simultaneous diagonalization of the family `{D_i}` is needed.

## 4. Dominance graph

Define a directed relation on source caps by

`k -> i` iff `rho_i D_k-rho_k D_i >=0`.

For positive-definite centered caps this is exactly the containment relation `E_k subseteq E_i`, so it is transitive.

A vertex `k` reaching every source cap is a complete dominant cap and collapses the whole intersection to one constraint.

If two caps dominate each other, then

`D_i/rho_i = D_k/rho_k`,

so they are the same normalized ellipsoid. Thus duplicate normalized caps can be quotient-collapsed before any downstream multiplier search.

---

# Part III — arbitrary quadratic Lyapunov debit after collapse

## 5. Target debit

After the source intersection has collapsed to `E_k`, allow the target to be the fully general quadratic

`q(z) := q0 + 2 h^T z + z^T H z`,

with symmetric `H`.

Important: `h` is allowed to be nonzero. Thus the target need not share the source center. Signed cancellation in `h` is preserved exactly.

We seek

`q(z) <= 0` for every `z` satisfying `z^T D_k z <= rho_k`.

Because `D_k>0` and `rho_k>0`, `z=0` is a strict interior source point. Hence the ordinary one-constraint S-lemma applies losslessly.

## 6. Exact single-multiplier block

Define, for `lambda>=0`,

`M(lambda) :=`

`[[ lambda D_k - H,     -h ],`
` [       -h^T,  -q0-lambda rho_k ]]`.

### Theorem C — `dominantCap_singleSlemma_lossless`

The following are equivalent:

1. `q(z)<=0` for every `z in F`;
2. `q(z)<=0` for every `z in E_k`;
3. there exists `lambda>=0` such that

   **`M(lambda) >=0`.**

### Direct proof of sufficiency

If `M(lambda)>=0`, then for every `z`,

`[z;1]^T M(lambda) [z;1] >=0`.

Expanding,

`lambda(z^T D_k z-rho_k)-q(z) >=0`.

For `z in E_k`, the source factor is nonpositive, so

`q(z) <= lambda(z^T D_k z-rho_k) <=0`.

### Necessity

Since `z=0` satisfies the source inequality strictly, the S-lemma has no duality gap. The implication

`z^T D_k z-rho_k <=0  =>  q(z)<=0`

therefore yields a nonnegative scalar `lambda` such that

`lambda(z^T D_k z-rho_k)-q(z)>=0`

for all `z`, which is exactly `M(lambda)>=0`.

This branch is lossless even when `H` does not commute with `D_k` or with the redundant source caps.

---

# Part IV — trust-region dual interpretation

## 7. Exact dual value

Set

`A(lambda) := lambda D_k-H`.

The Lagrangian upper envelope is finite precisely when

`A(lambda)>=0`

and

`h in range(A(lambda))`.

On that domain,

`sup_z [q(z)-lambda(z^T D_k z-rho_k)]`

`= q0+lambda rho_k + h^T A(lambda)^dagger h`.

Hence

**`sup_{z in E_k} q(z)`**

`= inf_{lambda>=0, A(lambda)>=0, h in range(A(lambda))}`

**`[q0+lambda rho_k+h^T A(lambda)^dagger h]`.**

The pseudoinverse expression is only an analytic interpretation. It does not belong in the trusted packet.

Indeed, the generalized Schur-complement condition

`M(lambda)>=0`

is equivalent to

- `A(lambda)>=0`;
- `h in range(A(lambda))`;
- `q0+lambda rho_k+h^T A(lambda)^dagger h <=0`.

Thus the block matrix packages curvature, range compatibility, signed linear cross term, and scalar energy margin in one exact object.

---

# Part V — fraction-free rational certificate

## 8. Rational multiplier packet

Let `lambda=p/s` with integers/rationals `p>=0`, `s>0`. Multiplying the block by the positive scalar `s` gives

**`N(p,s) :=`**

`[[ p D_k-s H,      -s h ],`
` [      -s h^T, -s q0-p rho_k ]]`.

Then

`M(p/s)>=0` iff `N(p,s)>=0`.

For rational source/target data, `N(p,s)` is rational and can be checked by exact PSD arithmetic.

No division by a matrix, no square root, no eigendecomposition, and no pseudoinverse is needed.

## 9. Strict safety gives a rational strict certificate

### Theorem D — `strictDominantCapSafety_exists_rationalMultiplier`

Assume all data are rational and

`sup_{z in E_k} q(z) < 0`.

Then there exists a rational `lambda>=0` such that

**`M(lambda)>0`.**

Consequently there exist rational `p>=0,s>0` such that

**`N(p,s)>0`.**

### Proof sketch

Choose rational `epsilon>0` smaller than the strict safety margin, so `q+epsilon` remains nonpositive on `E_k`.

By the S-lemma there is `lambda0>=0` such that the block for `q+epsilon` is PSD. Therefore the block for `q` satisfies

`M(lambda0) >= epsilon e e^T`,

where `e` is the final homogeneous coordinate.

Hence every vector in `ker M(lambda0)` has zero homogeneous component. On such a nonzero kernel vector `(u,0)`, the perturbation

`Delta := diag(D_k,-rho_k)`

has quadratic form

`u^T D_k u >0`.

Standard symmetric perturbation on the finite-dimensional unit sphere therefore gives

`M(lambda0+delta)>0`

for all sufficiently small positive `delta`.

Positive definiteness is open in `lambda`, so that interval contains a rational multiplier.

This is the useful engineering contract: strict Lyapunov reserve can always be represented by a rational single-multiplier packet in the dominant-cap branch.

For merely non-strict safety, do not assume the exact boundary multiplier is rational.

---

# Part VI — exact noncommuting regression

## 10. A branch not covered by simultaneous congruence

Take two centered source caps with unit radii:

`rho1=rho2=1`,

`D1 = [[2,0],[0,1]]`,

`D2 = [[3/2,1/5],[1/5,4/5]]`.

The dominance remainder is

`D1-D2 = [[1/2,-1/5],[-1/5,1/5]]`.

Its leading principal minors are

`1/2 >0`,

`det(D1-D2)=3/50>0`,

so

`D1-D2>0`.

Therefore

`E1 subset E2`,

and the exact two-cap source intersection is simply `E1`.

Now use the target

`H = [[1,1],[1,-1]]`,

`h = [1/10,-1/10]^T`,

`q0=-1`.

Choose the rational multiplier

`lambda=9/10`.

The fraction-free packet with `(p,s)=(9,10)` is

`N(9,10) =`

`[[ 8,-10,-1],`
` [-10,19, 1],`
` [ -1, 1, 1]]`.

Its leading principal minors are

`8`,

`52`,

`45`,

all strictly positive. Hence

`N(9,10)>0`.

Therefore

`q(z)<0`

for every point in the exact source intersection.

### Strict separation from T-P5-237 simultaneous-congruence branch

Since `D1>0`, simultaneous diagonalization by congruence of `D1,D2,H` would force the two `D1`-whitened symmetric matrices to commute. A fraction-free generalized commutator is

`D2 adj(D1) H - H adj(D1) D2`.

Here

`adj(D1)=[[1,0],[0,2]]`,

and exact multiplication gives

**`[[0,-7/10],[7/10,0]] !=0`.**

Thus `D1,D2,H` are not simultaneously diagonalizable by congruence.

Moreover `h!=0`, so the target is not even centered at the common source center.

Hence this regression is genuinely outside T-P5-237's lossless square-LP class, yet the present dominant-cap route closes it with a strict rational certificate.

---

# Part VII — failure boundary and dispatcher

## 11. No dominant cap is not mathematical failure

Failure to find `k` with

`rho_iD_k-rho_kD_i>=0` for all `i`

means only that the source intersection does not collapse to one listed cap by this criterion.

It does **not** imply that the target is unsafe and does **not** imply that the multi-S-procedure fails.

Exact example:

`D1=diag(1,4)`,

`D2=diag(4,1)`,

`rho1=rho2=1`.

Neither cap contains the other because both `D1-D2` and `D2-D1` are indefinite. But the pair is already simultaneously diagonal, so T-P5-237's square-LP branch applies exactly.

Therefore the correct routing label is

**`DOMINANT_CAP_NOT_FOUND`**

or

**`SINGLE_CAP_COLLAPSE_INCONCLUSIVE`,**

not FAIL.

## 12. Common-center boundary

The simple Loewner containment theorem above is for centered ellipsoids sharing one source center after quotienting/recentering.

If source caps have different affine centers, containment is an affine trust-region problem and the matrix comparison

`rho_iD_k-rho_kD_i>=0`

is no longer sufficient or necessary by itself.

Do not silently recenter each source separately and compare the resulting quadratic parts.

## 13. Quotient-coercivity boundary

This child assumes the dominant source matrix `D_k` is positive definite on the surviving quotient coordinates.

If the listed cap is singular, one may still have a valid one-constraint S-lemma under strict feasibility, but the source is cylindrical and the compact ellipsoid containment proof used here no longer supplies the same bounded-energy semantics. That branch should retain explicit kernel/range and coverage conditions from T-P5-234/236 rather than being auto-promoted by this theorem.

---

# Part VIII — structural fingerprint and theorem leaves

## 14. New structural fingerprint

The useful energy/Lyapunov pattern is

**common-centered source energies**

`-> normalized Loewner order`

`-> one source energy dominates all others`

`-> exact intersection collapse`

`-> preserve signed target linear/quadratic terms`

`-> one trust-region multiplier`

`-> fraction-free PSD Lyapunov certificate`.

This is complementary to T-P5-237:

- T-P5-237 handles several genuinely active caps when the whole family is simultaneously diagonalizable by congruence;
- T-P5-238 handles arbitrarily noncommuting redundant caps when one exact source ellipsoid already implies all the others;
- generic noncommuting/non-dominant intersections remain outside both lossless classes.

## 15. Suggested formal theorem leaves

1. `centeredEllipsoid_mem_of_loewner_scaled`
   - direct sufficiency of `rho_iD_k-rho_kD_i>=0`.

2. `centeredEllipsoid_containment_scaled_loewner`
   - necessity via boundary rescaling under `D_k>0`.

3. `dominantCenteredCap_intersection_eq`
   - finite intersection collapse.

4. `dominantCap_singleSlemma_sufficient`
   - expand the homogeneous PSD block.

5. `dominantCap_singleSlemma_necessary`
   - consume a standard one-constraint S-lemma under `rho_k>0`, `D_k>0`.

6. `fractionFree_singleSlemma`
   - `N(p,s)=s M(p/s)` for `s>0`.

7. `strictSafety_rationalMultiplier`
   - finite-dimensional perturbation/open-PD argument.

8. `dominance_transitive_normalized`
   - graph pruning / duplicate normalized-cap collapse.

No actual source binding, trajectory coverage, Float64 semantics, kernel receipt, admission, or registry state belongs inside these leaves.

---

# Part IX — remaining obligations

## 16. Still open

This result does not establish any of the following:

- that an actual P5 same-key source packet contains multiple common-centered quadratic caps;
- that one actual normalized source cap Loewner-dominates every other cap;
- that source radii/matrices are exact rather than outer/interval approximations;
- that the exact source intersection equals reachable trajectory/tube coverage;
- an actual target `H,h,q0` source identity;
- an actual rational multiplier packet for deployed data;
- Float64/interval enclosure;
- Lean implementation or pinned compile;
- independent validation by 封不觉;
- admission / registry / P5-P8-M4 parent closure.

## 17. Next smallest mathematical seam

After the two exact positive classes T-P5-237 and T-P5-238, the next genuinely new noncommuting branch should not repeat a generic scalar-multiplier search.

A useful next child is the **two-cap active-but-low-rank interaction** case: after whitening one coercive common-centered cap, assume the second cap differs from a scalar multiple of the first by rank one. Determine whether the source intersection and arbitrary quadratic Lyapunov debit reduce to a one-dimensional secular equation / exact bordered determinant, or exhibit an exact counterexample showing that rank-one source interaction still does not restore losslessness.

The dispatcher should remain fail-closed:

`dominant cap` -> T-P5-238 exact single S-lemma;

else `simultaneous congruence` -> T-P5-237 exact square LP;

else `found generic multi-multiplier PSD certificate` -> sufficient PASS only;

else -> certificate not found / unresolved, unless a genuine primal source witness is produced.
