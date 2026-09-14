---
kind: review_result
review_id: review-T-P5-237-two-quadratic-sprocedure-gate-kuangmanmozun-20260910T1030Z
task_id: T-P5-237-TWO-QUADRATIC-SPROCEDURE-GATE
reviewer: 狂蛮魔尊
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-10T10:30:00Z
claim_commit: cf99e8ca7973b62afcf4704700e1a532c464b522
inspected_commit: 6f87f1b29a67349f7b3da444272fc38671dbf148
upstream_commits:
  - fedaaff853ce28e1e4496d227382498f1e7d06ad  # T-P5-236 noninjective pullback / quotient coercivity
  - fde193bcd1c1231efc817e804d5d985b7a244d5b  # T-P5-235 equality + ellipsoid rank-free KKT
  - 69e1214a25f1e14137fb606bb6025b33ae187dd3  # T-P5-234 rank-deficient equality quotient dual
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_common_center_commuting_multiquadratic_lossless_gate; add_fraction_free_generalized_commutator_gate; add_two_ellipsoid_sprocedure_counterexample; route_generic_multi_sprocedure_miss_as_not_proof_of_failure
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact finite-dimensional quadratic / LP / matrix algebra only; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-237 — two-quadratic source intersection and the exact S-procedure gate

## 0. Verdict and seam

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-236 removes the false requirement that a pulled-back source ellipsoid be positive definite in all redundant ambient coordinates. It leaves the next mathematical seam explicitly open: a real tube may carry several simultaneous quadratic/energy caps, and one quotient-coercive positive combination of those caps does **not** by itself imply that the ordinary multi-constraint scalar S-procedure is lossless.

This child supplies both sides of that boundary:

1. a **lossless positive class**: after one common quotient recentering, if the source quadratic parts and the target quadratic part are simultaneously diagonalizable by congruence, the whole multi-quadratic problem is exactly a linear program in coordinate squares;
2. an exact **fraction-free generalized-commutator gate** which detects that positive class after whitening by any coercive positive combination, without constructing a matrix square root;
3. an exact one-dimensional **two translated ellipsoid counterexample** with Slater interior and coercive quadratic parts where the safety statement is true but no nonnegative scalar two-multiplier S-procedure certificate exists;
4. a checker routing rule: failure of the generic scalar-multiplier PSD search is `CERTIFICATE_NOT_FOUND`, not mathematical FAIL, unless an actual primal/source witness is separately produced.

No actual P5 source matrices, same-cell/tube maps, quotient chart, common center, Float64 enclosure, Lean receipt, independent validation, admission, registry mutation, or parent closure is claimed.

---

# Part I — quotient-centered multi-quadratic packet

## 1. Setup

Work after the T-P5-234/236 equality quotient and exact affine recentering have already been performed. Thus the surviving quotient coordinate is `z in R^n`, and the source packet consists of

`z^T D_i z <= rho_i`,  `i=1,...,m`,

with symmetric `D_i`.

The target debit/safety statement is

`q(z) := q0 + z^T H z <= 0`,

with symmetric `H`.

The essential semantic hypothesis here is **one common center**. In pre-shift coordinates `y`, this means there is a single `y_c` on the affine equality manifold such that every source cap and the target have zero linear term after `z=y-y_c`. Equivalently, if

`g_i(y)=y^T P_i y + 2 h_i^T y + c_i-rho_i`,

then on the quotient the same `y_c` satisfies the corresponding stationarity equations for every `i`; it is not enough to recenter each source ellipsoid independently at a different point.

Assume the source intersection

`F := {z : z^T D_i z <= rho_i for all i}`

is nonempty.

A useful boundedness packet is the existence of `theta_i>=0` such that

`C := sum_i theta_i D_i > 0`.

Then every `z in F` satisfies

`z^T C z <= sum_i theta_i rho_i`,

so `F` is compact. This is exactly the role of the quotient-coercive positive combination: it supplies compactness, but, as Part IV shows, compactness alone is not enough for a lossless multi-S-procedure.

---

# Part II — simultaneous-diagonal square lifting is lossless

## 2. Exact square-coordinate reduction

Assume there exists an invertible matrix `S` such that

`S^T D_i S = diag(d_i1,...,d_in)` for every source `i`,

and

`S^T H S = diag(h_1,...,h_n)`.

Write `z=Sx` and introduce

`s_j := x_j^2 >= 0`.

Then source feasibility is exactly

`sum_j d_ij s_j <= rho_i`,  `i=1,...,m`,

and the target is exactly

`q0 + sum_j h_j s_j <= 0`.

There is no relaxation here. Every `x` produces `s>=0`, and conversely every `s>=0` is realized by some real `x`, e.g. `x_j=sqrt(s_j)`.

Hence the quadratic optimization problem

`sup_{z in F} q(z)`

is identical to the linear program

`q0 + sup { h^T s : Dsq s <= rho, s>=0 }`,

where `(Dsq)_{ij}=d_ij`.

### Theorem A — `commonCenter_simultaneouslyDiagonal_multiQuadratic_exactLP`

Under the common-center and simultaneous-congruence hypotheses above,

`sup_{z in F} (q0+z^THz)`

`= q0 + sup_{s>=0, Dsq s<=rho} h^T s`.

If one nonnegative combination `C=sum theta_i D_i` is positive definite and `F` is nonempty, the LP is feasible and bounded.

### Proof of boundedness in square coordinates

In the same congruence chart,

`S^T C S = diag(c_1,...,c_n)`

with every `c_j>0`, and `c_j=sum_i theta_i d_ij`.

For a feasible `s`,

`sum_j c_j s_j <= sum_i theta_i rho_i`.

Since `s_j>=0` and all `c_j>0`, every coordinate is bounded. QED.

---

## 3. Lossless scalar multi-multiplier certificate

The LP dual is

`min rho^T lambda`

subject to

`lambda>=0`,

`Dsq^T lambda >= h`.

Finite-dimensional LP strong duality therefore gives the exact safety criterion.

### Theorem B — `commonCenter_simultaneouslyDiagonal_multiSprocedure_lossless`

Assume:

- `F` is nonempty;
- some `theta>=0` gives `C=sum theta_iD_i>0`;
- all `D_i` and `H` are simultaneously diagonalizable by one congruence `S`;
- all quadratics use the same center.

Then the following are equivalent:

1. `q0+z^THz <=0` for every `z in F`;
2. there exists `lambda_i>=0` such that

   **`sum_i lambda_i D_i - H >= 0`**

   and

   **`q0 + sum_i lambda_i rho_i <= 0`.**

This is precisely the centered scalar multi-S-procedure, and in this class it is **necessary and sufficient**, not merely sufficient.

### Direct sufficiency

For feasible `z`,

`z^T H z <= sum_i lambda_i z^T D_i z <= sum_i lambda_i rho_i`,

hence

`q(z)<=q0+sum_i lambda_i rho_i<=0`.

### Necessity

Transform to the simultaneous diagonal chart. Safety says the primal square-LP optimum is at most `-q0`. LP strong duality supplies `lambda>=0` with

`Dsq^Tlambda>=h`,

`rho^Tlambda<=-q0`.

The componentwise first inequality is exactly

`S^T(sum_i lambda_iD_i-H)S>=0`.

Congruence by invertible `S` gives the matrix PSD inequality in the original quotient coordinates. QED.

---

## 4. Rational certificate subclass

If the data are rational and the simultaneous congruence `S` can itself be chosen rational, then all diagonal coefficients in the square-LP are rational. A feasible bounded rational LP has a rational optimal dual solution. Therefore a true boundary safety statement admits an exact rational multiplier vector `lambda`.

### Corollary B1 — `rationalDiagonalChart_exactRationalMultipliers`

For rational `q0,rho,D_i,H,S`, with rational invertible `S` simultaneously diagonalizing all forms and with the hypotheses of Theorem B, safety implies existence of **rational** `lambda_i>=0` satisfying the exact matrix/scalar certificate.

A second, weaker rationalization rule is available whenever a real certificate has strict reserve:

`sum lambda_iD_i-H >0`,

`q0+rho^Tlambda<0`.

The strict inequalities are open, so the positive multiplier components can be approximated by rationals while zero components remain zero. Thus a nearby rational certificate survives. Boundary semidefinite certificates should not be declared rational merely from rational input unless an additional rational chart/solve witness is supplied.

---

# Part III — square-root-free generalized commutator gate

## 5. Whitening by a coercive source combination

The simultaneous congruence hypothesis can be checked without explicitly constructing a square root.

Let

`C=sum_i theta_iD_i >0`.

Define the whitened symmetric matrices conceptually by

`A_i=C^(-1/2)D_iC^(-1/2)`,

`A_H=C^(-1/2)HC^(-1/2)`.

Real symmetric matrices are simultaneously orthogonally diagonalizable iff they commute pairwise. Therefore the source/target forms are simultaneously diagonalizable by congruence whenever

`A_i A_j=A_j A_i` for all `i,j`,

and

`A_H A_i=A_i A_H` for all `i`.

Multiplying out the whitening gives an equivalent rational-matrix condition:

**`D_i C^(-1) D_j = D_j C^(-1) D_i`**,

**`H C^(-1) D_i = D_i C^(-1) H`.**

If `C` has rational entries, let `d=det(C)>0` and `J=adj(C)`. Since `C^(-1)=J/d`, the checker can use the completely fraction-free equalities

**`D_i J D_j = D_j J D_i`**,

**`H J D_i = D_i J H`.**

No matrix square root is required by the checker.

### Theorem C — `coerciveCombination_generalizedCommute_impliesSimultaneousCongruence`

If `C>0` and the generalized commutators above vanish, then there exists invertible real `S` simultaneously diagonalizing `C`, every `D_i`, and `H` by congruence; moreover `S^T C S=I` can be chosen.

### Proof

The whitened matrices are real symmetric and commute pairwise, so the spectral theorem gives one orthogonal `Q` diagonalizing them all. Set `S=C^(-1/2)Q`. Then

`S^T C S=I`,

and `S^TD_iS`, `S^THS` are diagonal. QED.

This yields an exact routing gate:

`COERCIVE_COMBINATION + FRACTION_FREE_GENERALIZED_COMMUTATORS = 0`

`=> LOSSLESS_SQUARE_LP_MULTI_SPROCEDURE`.

The proof may use the real spectral theorem internally; the finite checker only needs exact rational determinant/PSD and adjugate-product equalities.

---

# Part IV — coercivity + Slater do NOT make two-constraint S-procedure lossless

## 6. Exact one-dimensional counterexample

Take a single real variable `x` and the two convex quadratic source constraints

`c1(x) := (1/2)x^2 - x <= 0`,

`c2(x) := x^2 - 1 <= 0`.

Equivalently,

`c1(x) = (1/2)(x-1)^2 - 1/2`,

`c2(x) = x^2 - 1`.

Thus

`c1<=0  <=> x in [0,2]`,

`c2<=0  <=> x in [-1,1]`,

and the exact intersection is

**`F=[0,1]`.**

Both quadratic parts are strictly positive:

`D1=1/2>0`, `D2=1>0`.

Hence, for example,

`D1+D2=3/2>0`.

So a positive source combination is not merely quotient-coercive; each source quadratic is individually coercive.

There is also strict Slater interior: at `x=1/2`,

`c1(1/2)=-3/8<0`,

`c2(1/2)=-3/4<0`.

Now choose the safety target

`q(x):=x^2-x = (x-1/2)^2-1/4`.

Because `F=[0,1]`,

**`q(x)<=0` for every source-feasible x.**

In fact the target sublevel is exactly the source intersection.

---

## 7. No scalar two-multiplier S-procedure certificate exists

Suppose, toward contradiction, that there are `lambda1,lambda2>=0` such that the standard global S-procedure polynomial

`p(x):=q(x)-lambda1*c1(x)-lambda2*c2(x)`

satisfies

`p(x)<=0` for every real `x`.

Expanding,

`p(x)`

`= (1-lambda1/2-lambda2)x^2 + (-1+lambda1)x + lambda2`.

At `x=0`, global nonpositivity gives

`lambda2=p(0)<=0`.

Since `lambda2>=0`, necessarily

**`lambda2=0`.**

Now `p(0)=0` and `p` is globally nonpositive. Therefore zero is a global maximizer of the differentiable polynomial, so

`p'(0)=0`.

Hence

`-1+lambda1=0`,

so

**`lambda1=1`.**

But then

`p(x)=(1/2)x^2`,

which is positive for every nonzero `x`. Contradiction.

### Theorem D — `twoTranslatedEllipsoids_safe_but_scalarSprocedureFails`

The above one-dimensional packet has all of the following simultaneously:

- two strict convex quadratic/ellipsoidal source caps;
- nonempty strict Slater interior;
- a coercive positive combination of source quadratic parts;
- compact source intersection;
- a quadratic target nonpositive on the entire exact intersection;
- **no** nonnegative scalar two-multiplier global S-procedure certificate.

Therefore the implication

`positive combination coercive + Slater + target safe`

`=> scalar multi-S-procedure certificate`

is false, already in dimension one.

This is the required decisive obstruction to any checker that tries to promote `multiplier infeasible` into `mathematical FAIL`.

---

## 8. Why the counterexample escapes the positive class

The two source caps do not share a center:

- `c1` is centered at `x=1`;
- `c2` is centered at `x=0`;
- the target is centered at `x=1/2`.

Thus there is no single translation turning all three forms into homogeneous functions of `x^2`. The square-coordinate LP reduction is unavailable.

The failure is not caused by lack of boundedness, lack of coercivity, rank deficiency, or lack of interior. It is caused by affine-center geometry that a single global conic aggregation cannot preserve.

---

# Part V — what the generic multi-S-procedure is really doing

## 9. One conic aggregate interpretation

For general quadratic constraints `c_i(z)<=0`, a scalar multi-S-procedure certificate is

`q(z)-sum_i lambda_i c_i(z) <=0` globally,

with `lambda_i>=0`.

If `lambda` is nonzero, write

`mu := sum_i lambda_i >0`,

`theta_i:=lambda_i/mu`.

Then this is exactly

`q(z)-mu*c_theta(z)<=0`,

where

`c_theta:=sum_i theta_i c_i`.

Thus the ordinary scalar multi-S-procedure is equivalent to:

1. replace the true intersection `c_i<=0 all i` by **one conic aggregate cap** `c_theta<=0`, which contains the intersection;
2. apply the one-constraint S-procedure to that aggregate.

This gives a clean geometric explanation of conservatism: a single aggregate ellipsoid may strictly contain unsafe points that are removed only by the intersection of the original caps.

### Counterexample aggregate geometry

Normalize `theta in[0,1]` and form

`c_theta=theta*c1+(1-theta)*c2`.

If `theta<1`, then

`c_theta(0)=-(1-theta)<0`.

Hence by continuity the aggregate feasible set contains some negative `x`, but every negative `x` has

`q(x)=x^2-x>0`.

If `theta=1`, the aggregate is simply `c1<=0`, namely `[0,2]`, and it contains for example `x=3/2`, where

`q(3/2)=3/4>0`.

So **every** conic aggregate source cap contains a target-violating point, even though their true intersection is exactly safe.

This is why no scalar multiplier vector can succeed.

---

# Part VI — checker and theorem-routing consequences

## 10. Exact routing rule

A safe implementation should distinguish the following cases.

### Route A — lossless commuting/common-center packet

Require:

1. exact quotient/common-center binding;
2. nonempty source intersection;
3. a nonnegative coercive combination `C=sum theta_iD_i>0` on the quotient;
4. fraction-free generalized commutators
   `D_i adj(C) D_j = D_j adj(C) D_i` and
   `H adj(C) D_i = D_i adj(C) H`;
5. then solve the resulting square-LP / dual multiplier problem.

In this route, dual infeasibility is a genuine mathematical obstruction to the requested centered target safety statement on the exact source intersection, because the reduction is lossless.

Suggested status labels:

- `LOSSLESS_MULTIQUADRATIC_SQUARE_LP_PASS`;
- `LOSSLESS_MULTIQUADRATIC_SQUARE_LP_FAIL`.

A FAIL witness should still respect source-model semantics: if the quadratic source is only an outer approximation to reachability, an unsafe point in the outer set is not automatically a trajectory witness.

### Route B — generic scalar multi-S-procedure

If common-center or generalized-commutation gates fail, a found multiplier certificate is still a valid sufficient PASS.

But multiplier infeasibility must be labeled only

**`MULTI_SPROCEDURE_CERTIFICATE_NOT_FOUND`**

or

**`GENERIC_AGGREGATE_ROUTE_INCONCLUSIVE`.**

It is not mathematical FAIL. Theorem D is an exact negative control for this routing decision.

### Route C — actual primal counterexample

A true FAIL requires an actual point satisfying all exact source constraints and violating the target, plus any source-membership/reachability semantics needed by the parent theorem.

---

# Part VII — formalizable theorem leaves

## 11. Suggested Lean decomposition

The mathematical child can be split into small finite-dimensional leaves:

1. `positiveCombination_compact_intersection`
   - from `theta>=0`, `sum theta_iD_i>0`, and all source caps, obtain boundedness/compactness.

2. `simultaneousDiagonal_squareImage_exact`
   - prove `{(x_j^2)} = R_+^n` as a set image and transport all diagonal quadratic constraints to linear inequalities in squares.

3. `simultaneousDiagonal_multiQuadratic_toLP`
   - exact primal objective/set equivalence.

4. `diagonalMultiQuadratic_dualCertificate_sufficient`
   - matrix/scalar multiplier packet implies target safety.

5. `diagonalMultiQuadratic_dualCertificate_necessary`
   - consume finite LP strong duality.

6. `generalizedCommute_whitened_commute`
   - `D_i C^-1 D_j=D_j C^-1D_i` iff whitened symmetric matrices commute.

7. `adjugate_generalizedCommute_fractionFree`
   - with `det C !=0`, replace `C^-1` by `adj(C)/det(C)`.

8. `generalizedCommute_simultaneousCongruence`
   - commuting real symmetric whitened family -> one orthogonal diagonalizer.

9. `twoTranslatedEllipsoids_exactIntersection`
   - prove the two one-dimensional sublevel identities and intersection `[0,1]`.

10. `twoTranslatedEllipsoids_targetSafe`
    - `x in[0,1] -> x^2-x<=0`.

11. `twoTranslatedEllipsoids_noScalarSprocedure`
    - evaluate the putative global polynomial at zero, use derivative at global maximum, derive `p=x^2/2`, contradiction.

12. `multiSprocedure_eq_singleConicAggregate`
    - normalize nonzero multiplier vector into `mu*theta`.

No source binding, Float64 semantics, coverage, kernel receipt, registry, or parent admission should be imported into these leaves.

---

# Part VIII — assumptions, failure branches, and next seam

## 12. Assumptions that must remain explicit

The lossless theorem depends on all of:

- exact common-center quotient coordinates;
- simultaneous congruence of the source quadratic parts **and target quadratic part**;
- nonempty exact source intersection;
- one coercive nonnegative source combination for boundedness/strong-dual applicability;
- exact-real quadratic semantics.

Dropping any of those without replacement changes the theorem contract.

In particular:

- separate recentering of each source at its own center does not produce a common square variable;
- simultaneous diagonalization of the sources alone is insufficient for the LP reduction if the target retains cross terms;
- a positive source combination gives compactness but does not make the generic multi-S-procedure lossless;
- Slater interior does not repair the multi-constraint failure;
- failure of a sufficient multiplier search is not a primal counterexample.

## 13. Remaining obligations

Still open:

- actual same-key P5 multi-quadratic source caps;
- actual equality quotient and common-center witness;
- actual coercive combination `theta` and matrix `C`;
- actual fraction-free generalized-commutator check;
- rational/interval enclosure for source matrices and radii;
- concrete multiplier or primal witness;
- source-map exact/outer semantics and tube/trajectory coverage;
- Lean implementation and pinned compile;
- independent validation by 封不觉;
- admission / registry / P5-P8-M4 parent closure.

## 14. Next smallest mathematical seam

The next useful seam is the **noncommuting but common-center two-cap branch**. The natural object is the joint image of the source quadratic forms and the target quadratic form. A worthwhile next child should determine a small exact positive class beyond simultaneous diagonalization—e.g. rank-one commutator / two-dimensional invariant-block cases—or give a second counterexample showing that common center alone is insufficient. The goal should be a finite exact routing condition, not a generic SDP black box.
