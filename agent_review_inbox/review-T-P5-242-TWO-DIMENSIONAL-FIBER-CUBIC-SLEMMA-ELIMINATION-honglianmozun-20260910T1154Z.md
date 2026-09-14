---
kind: review_result
review_id: review-T-P5-242-two-dimensional-fiber-cubic-slemma-elimination-honglianmozun-20260910T1154Z
task_id: T-P5-242-TWO-DIMENSIONAL-FIBER-CUBIC-SLEMMA-ELIMINATION
reviewer: 红莲魔尊
agent: 红莲魔尊
source_agent: 红莲魔尊
created_at: 2026-09-10T11:54:00Z
claim_commit: 8d75848dc2a5e49e273c7365b161e2bc622be834
inspected_commit: 71bc4c6447db8b496085b5497a494995bfe364ba
upstream_commits:
  - 73e5febae1d3ac2733d7bdea067fc244e2f551d1  # corrected T-P5-239 rank-one two-cap fiber/secular bridge
  - 56fdaebc2c0ca45fce1791923abb8311a54e14f9  # T-P5-240 quotient rank-one pivot transport
  - a51db882b62de65dbd964bb9e18bbb97ecfc7b2a  # T-P5-241 one-dimensional fiber quartic closure
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_2d_fiber_cubic_slemma_classifier; add_singular_boundary_hard_case; add_squarefree_localmax_gates; add_outer_coordinate_degree12_partition; preserve_source_coverage_and_exact_field_gates
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact S-lemma reduction, 2x2 adjugate algebra, cubic critical-point elimination, polynomial degree accounting, exact rational regressions; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-242 — Two-dimensional fiber cubic S-lemma elimination

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-239 reduces the rank-one two-cap affine-quadratic problem to an outer scalar coordinate `s` and one ordinary transverse trust region. T-P5-241 closes the one-dimensional transverse case directly. The next case is a **two-dimensional transverse fiber** (quotient dimension three).

The main result here is that the Lyapunov **sign decision** in a 2D fiber does not need the usual quartic primal secular equation. The lossless S-lemma converts safety to existence of one multiplier `lambda`; after exploiting that the transverse block is `2x2`, the relevant bordered determinant is only a **cubic** in `lambda`. Once the spectral floor is handled, existence of a safe multiplier is decided by the cubic's unique later local maximum. Its location is controlled by a quadratic discriminant, and its sign can be made square-root-free using the cubic discriminant.

For the outer rank-one coordinate, on every fixed source-radius branch the cubic coefficients have degree at most two in `s`. The multiplier can therefore be eliminated into a one-variable semialgebraic sign problem whose highest new polynomial degree is at most **12**, rather than carrying the quartic secular root as a second quantified variable.

No actual P5 same-key source pair, source/domain equality, tube/cell coverage, Float64 enclosure, Lean/kernel receipt, independent validation, admission, registry mutation, or parent closure is claimed.

---

# Part I — exact 2D fiber packet

## 1. Fiber and debit

Let

`M in S_{++}^2`, `R>0`, `G in S^2`, `l in R^2`, `A in R`,

and consider

`F_R := { y in R^2 : y^T M y <= R }`,

with affine-quadratic Lyapunov debit

`q(y) := A + 2 l^T y + y^T G y`.

Because `R>0`, the source inequality has strict Slater point `y=0`.

Define the S-lemma block

`S(lambda) := [[K(lambda), -l],[-l^T, c(lambda)]]`,

where

`K(lambda):=lambda M-G`,

`c(lambda):=-A-lambda R`.

Then the ordinary lossless S-lemma gives the exact equivalence

**`q(y)<=0 for all y in F_R`**

iff

**there exists `lambda>=0` with `S(lambda)>=0`.**

Indeed `S(lambda)>=0` is exactly the statement

`q(y)+lambda(R-y^TMy)<=0`

for every `y`.

This child only simplifies that exact multiplier search; it does not introduce a relaxation.

## 2. Spectral floor

Let `Lambda` be the largest generalized eigenvalue of the pencil

`G v = lambda M v`.

Equivalently, `Lambda` is the largest real root of

`det(lambda M-G)=0`.

Set

`L := max(0,Lambda)`.

Since `M>0`,

- `K(lambda)>0` for every `lambda>L`;
- `K(lambda)` cannot be PSD for `0<=lambda<L`;
- at `lambda=L`, either `K(L)>0` (only when `Lambda<0`, hence `L=0`) or `K(L)>=0` is singular.

Therefore every S-lemma certificate lies at `lambda=L` or in the regular half-line `lambda>L`.

For rational `M,G`, `Lambda` belongs to an ordered extension of degree at most two because `det(lambda M-G)` is quadratic. No floating eigensystem is mathematically required.

---

# Part II — cubic bordered determinant instead of quartic secular equation

## 3. Regular branch

For `lambda>L`, `K(lambda)>0`. By Schur complement,

`S(lambda)>=0`

iff

`c(lambda)-l^T K(lambda)^{-1} l >=0`.

Multiplying by the positive scalar `det K(lambda)` gives the equivalent condition

**`p(lambda)>=0`,**

where

`p(lambda):=det S(lambda)`

`= det K(lambda) c(lambda) - l^T adj(K(lambda)) l`.

Because `K` is `2x2`, `det K` is quadratic in `lambda` and `adj K` is affine in `lambda`. Hence

**`p` is a cubic.**

More explicitly, write

`det K(lambda)=d2 lambda^2+d1 lambda+d0`,

`adj K(lambda)=J1 lambda+J0`,

with `d2=det M>0`. Then

`p(lambda)=a3 lambda^3+a2 lambda^2+a1 lambda+a0`,

where

`a3 = -d2 R`,

`a2 = -d2 A - d1 R`,

`a1 = -d1 A - d0 R - l^T J1 l`,

`a0 = -d0 A - l^T J0 l`.

In particular

**`a3=-R det(M)<0`.**

So `p(lambda)->-infinity` as `lambda->+infinity`.

## 4. Why this is smaller than the primal secular equation

The regular primal optimizer is

`y(lambda)=K(lambda)^{-1} l`.

If the ellipsoid boundary is active, its trust-region KKT multiplier satisfies

`y(lambda)^T M y(lambda)=R`.

After clearing denominators this becomes

`l^T adj(K(lambda)) M adj(K(lambda)) l - R det(K(lambda))^2 = 0`,

which is generically **quartic** in `lambda` even in dimension two.

For a Lyapunov proof we only need to decide whether the worst-case debit is nonpositive, equivalently whether some S-lemma certificate exists. We do **not** need the primal maximizing multiplier. Existence is the sign question `p(lambda)>=0` on the regular half-line, hence a cubic problem.

This distinction is the key reduction of this child.

---

# Part III — exact cubic local-maximum classifier

## 5. Boundary certificate first

At `lambda=L` there are two possibilities.

### 5.1 `K(L)>0`

Then the boundary multiplier is regular and

`S(L)>=0 <=> p(L)>=0`.

If this holds, safety is already proved.

### 5.2 `K(L)>=0` singular

A determinant sign alone is not enough. The exact singular hard case is handled in Part IV below. Denote by

`HARD(L)`

the exact predicate `S(L)>=0` evaluated with its range/pivot gate.

If `HARD(L)` holds, safety is proved at the spectral boundary.

If no boundary certificate holds, then necessarily `p(L)<=0`. Therefore any regular certificate `lambda>L` must arise because the cubic rises to a nonnegative local maximum after `L` before eventually going to `-infinity`.

## 6. Critical invariants

For

`p(lambda)=a3 lambda^3+a2 lambda^2+a1 lambda+a0`, `a3<0`,

define

**`Delta := a2^2 - 3 a3 a1`,**

and

**`U := 2 a2^3 - 9 a3 a2 a1 + 27 a3^2 a0`.**

The derivative is

`p'(lambda)=3a3 lambda^2+2a2 lambda+a1`.

Its discriminant is `4 Delta`.

If `Delta<=0`, then `p'<=0` everywhere (with only a double horizontal tangent when `Delta=0`), so a cubic starting nonpositive at `L` can never become positive later. Thus no later regular certificate exists.

If `Delta>0`, the larger critical point is the unique local maximum:

**`lambda_m = (-a2 - sqrt(Delta))/(3a3)`.**

(The denominator is negative, so this is the larger of the two derivative roots.)

## 7. Exact location gate without retaining a square root

Define

`T := -a2 - 3 a3 L`.

Because `3a3<0`,

`lambda_m>L`

iff

`sqrt(Delta)>T`.

Hence the exact square-root-free sign-gated condition is

**`T<0`,**

or

**`T>=0` and `Delta>T^2`.**

When `L` is quadratic algebraic, this comparison is performed in the ordered field `Q(L)`; it still uses exact arithmetic.

## 8. Exact local-maximum value

Modulo the derivative relation, the cubic reduces to a linear expression. Direct substitution gives

**`p(lambda_m) = [U + 2 Delta^(3/2)]/(27 a3^2)`.**

Since the denominator is positive, nonnegativity of the local maximum is equivalent to

`U+2 Delta^(3/2)>=0`.

This can also be made square-root-free with the necessary sign gate:

- if `U>=0`, the local maximum is automatically strictly positive because `Delta>0`;
- if `U<0`, then

  `p(lambda_m)>=0`

  iff

  **`4 Delta^3-U^2>=0`.**

Moreover

**`4 Delta^3-U^2 = 27 a3^2 Disc_lambda(p)`.**

Thus, in the `U<0` branch, the last gate is simply nonnegativity of the ordinary cubic discriminant.

## 9. Theorem A — exact 2D fiber safety classifier

Assume `M>0` and `R>0`. Let `L`, `p`, `Delta`, `U`, `T` be as above.

Then

`q(y)<=0` for every `y^TMy<=R`

if and only if at least one of the following holds:

1. **spectral-boundary certificate:** `S(L)>=0`, checked by the regular or singular hard-case rules below;

2. **later regular certificate:** all of

   - `Delta>0`;
   - `T<0`, or `T>=0` and `Delta>T^2`;
   - `U>=0`, or `U<0` and `4Delta^3-U^2>=0`.

In branch 2 the multiplier `lambda_m` satisfies `lambda_m>L`, hence `K(lambda_m)>0`, and the final value gate is exactly `p(lambda_m)>=0`. Therefore `S(lambda_m)>=0` by Schur complement.

### Proof of necessity

By the S-lemma, safety gives some `lambda>=L` with `S(lambda)>=0`. If `lambda=L`, branch 1 holds.

Otherwise `lambda>L`, so `K(lambda)>0` and `p(lambda)>=0`. If branch 1 failed, `p(L)<=0`, while `p(lambda)->-infinity`. Hence `p` must possess a local maximum strictly to the right of `L`, and that local maximum must be nonnegative. A cubic with negative leading coefficient has such a local maximum iff `Delta>0`; its location and value are exactly the expressions above. This gives branch 2.

### Proof of sufficiency

Branch 1 is a direct S-lemma certificate. In branch 2, the location gate gives `lambda_m>L`, so `K(lambda_m)>0`; the value gate gives `p(lambda_m)>=0`. Positive definiteness of `K` and nonnegative Schur determinant imply `S(lambda_m)>=0`, hence the S-lemma proves safety.

QED.

---

# Part IV — singular hard case at the spectral floor

## 10. Rank-one singular `K(L)`

Suppose `K:=K(L)>=0` has rank one. Since it is `2x2`, `adj(K)>=0` has rank one and spans `ker(K)`.

The exact range condition for the cross term is

**`adj(K) l = 0`.**

This is equivalent to `l in range(K)`.

Choose either pivot `i` with `K_ii>0`. Under the range condition,

`S(L)>=0`

iff

**`K_ii c(L)-l_i^2>=0`.**

Indeed write the rank-one PSD matrix as `K=k vv^T`; range compatibility makes `l` parallel to `v`, and the displayed pivot inequality is precisely the one-dimensional Schur complement after quotienting the kernel. It is independent of which positive pivot is chosen.

Thus the rank-one hard packet is entirely exact and rational/algebraic:

`K>=0`, `det K=0`, `K!=0`, `adj(K)l=0`, and one positive-pivot minor `K_ii c-l_i^2>=0`.

No pseudoinverse is needed.

## 11. Rank-zero singular `K(L)`

If `K(L)=0`, then the block matrix can be PSD only if

**`l=0`**

and

**`c(L)>=0`.**

This covers the repeated-generalized-eigenvalue case `G=L M` exactly.

## 12. Why `det S(L)=0` is not a hard-case certificate

Take

`M=I`, `R=1`, `G=diag(1,0)`, `l=(0,1)`, `A=-1`.

Then `L=1` and

`K(L)=diag(0,1)`.

The cross term is range-compatible because `l in range K`, and `det S(L)=0` automatically because `det K=0`. But

`c(L)=-A-LR=0`,

while the positive-pivot gate gives

`1*0-1^2=-1<0`.

Indeed

`q(x,y)=-1+2y+x^2`

has `q(0,1)=1>0` on the unit disk.

Therefore a checker that accepts a singular multiplier from `det S=0` alone gives a false PASS. The range/pivot hard gate is mandatory.

---

# Part V — outer rank-one coordinate and degree bound

## 13. Data inherited from T-P5-239

On one fixed source-radius branch of the rank-one two-cap decomposition, let the outer coordinate be `s` and the two-dimensional transverse variable be `y`.

T-P5-239 has the form

`y^T M y <= R(s)`,

`q_s(y)=A(s)+2 l(s)^T y+y^T G y`,

where

- `M>0` is constant on the branch;
- `G` is constant;
- `R(s)` has degree at most two (in the concrete centered rank-one pair it is affine in `s^2`);
- `A(s)` has degree at most two;
- `l(s)` has degree at most one.

The spectral floor `L` depends only on `M,G`, hence is constant in `s`.

## 14. Cubic coefficients have degree at most two

Using the explicit formulas of Section 3,

`a3(s),a2(s),a1(s),a0(s)`

all have degree at most two in `s`:

- products of `A(s)` or `R(s)` with the constant pencil coefficients have degree at most two;
- `l(s)^T J l(s)` has degree at most two.

Consequently

**`deg_s Delta <=4`,**

**`deg_s U <=6`,**

and

**`deg_s [4Delta^3-U^2] <=12`.**

The local-maximum location gate has

`T(s)=-a2(s)-3a3(s)L`, `deg_s T<=2`,

so

`deg_s [Delta-T^2] <=4`.

The spectral-boundary regular/hard predicates use only degree-at-most-two expressions in `s` (plus fixed exact algebraic coefficients from `L`).

## 15. Theorem B — finite one-variable semialgebraic closure

On any interval where

1. one source radius `R_j(s)` is active;
2. `R_j(s)>0`;
3. the source switch and feasibility signs are fixed,

universal 2D-fiber Lyapunov safety is equivalent to a finite Boolean combination of exact one-variable sign conditions involving polynomials of degree at most **12** over `Q(L)`.

If the source data and target coefficients are rational, `Q(L)` has degree at most two over `Q`.

Therefore an exact checker may:

1. partition the outer `s` interval by the source switch and `R_j=0` endpoints;
2. isolate roots of the degree `<=4`, `<=6`, and `<=12` gate polynomials;
3. evaluate the fixed branch predicates on each resulting cell using Sturm/subresultant arithmetic over the ordered quadratic field;
4. handle `R_j(s)=0` endpoints separately by the trivial fiber condition `A(s)<=0`.

This eliminates the trust-region multiplier as a quantified variable. The hardest new sign polynomial has degree at most twelve.

The packet is exact but is a **sign/closure** packet. If one wants the actual worst-case point or exact worst-case value, the primal quartic secular equation from T-P5-239 may still be useful.

---

# Part VI — exact regressions and checker boundaries

## 16. PSD gate cannot be replaced by determinant positivity

Take

`M=I`, `R=1`, `G=diag(2,1)`, `l=0`, `A=-1`.

The target is

`q(x,y)=-1+2x^2+y^2`,

which is unsafe because `q(1,0)=1`.

At the inadmissible multiplier `lambda=0`, however,

`K(0)=diag(-2,-1)`

is negative definite and

`p(0)=det S(0)=2>0`.

Thus `p(lambda)>=0` is meaningful only after the principal PSD gate has forced `lambda>=L` (or directly `K(lambda)>0` in the regular branch). A naked bordered-determinant sign is unsound.

## 17. Exact tangent example for the cubic branch

Take

`M=I`, `R=1`, `G=diag(1,0)`, `l=(1/4,0)`, `A=-3/2`.

Then

`q(x,y)=-3/2 + (1/2)x + x^2`.

On the unit disk the maximum is attained at `(1,0)` and equals zero, so this is an exact non-strict Lyapunov boundary case.

Here

`K(lambda)=diag(lambda-1,lambda)`,

and

`p(lambda)=lambda(lambda-1)(3/2-lambda)-lambda/16`

factors as

**`p(lambda) = -lambda(4lambda-5)^2/16`.**

The spectral boundary `L=1` is singular and range-incompatible with `l`, so the hard branch fails. The later local maximum is exactly

`lambda_m=5/4`,

with `K(lambda_m)>0` and `p(lambda_m)=0`.

Thus Theorem A accepts the exact tangent regular certificate without solving the quartic primal secular equation.

## 18. Rational strict-margin certificate

Suppose all fixed fiber data `M,G,l,A,R` are rational and the true inequality is strict:

`q(y)<0` for every `y^TMy<=R`.

Compactness gives a margin `epsilon>0`. Apply the S-lemma to `q+epsilon/2`; then return to `q`. If the resulting top block is singular, a sufficiently small positive perturbation of `lambda` makes `K` positive definite while the inherited Schur slack stays positive. Hence there is an open interval of regular multipliers with

`S(lambda)>0`.

Rational numbers are dense, so one may choose

**a rational `lambda` with a strictly positive-definite rational `3x3` S-lemma block.**

Therefore strict-margin consumers never need to store the quadratic radical `sqrt(Delta)` or the generalized eigenvalue `L` in the trusted packet. The algebraic classifier is only needed to prove sharp non-strict boundaries or to perform exact symbolic partitioning.

## 19. Exact-boundary certificate format

When the only valid multiplier is algebraic, the regular local maximum has degree at most two over the coefficient field because it satisfies

`3a3 lambda^2+2a2 lambda+a1=0`.

A trusted exact packet may store:

- this quadratic polynomial;
- an isolating rational interval selecting the larger root;
- exact checks of `lambda>L` and `p(lambda)>=0` in the ordered quadratic extension.

For the rank-one source outer problem, if `L` is itself quadratic algebraic, a generic composition can produce a degree-at-most-four extension. This is still finite exact algebra, but the strict-margin rational-certificate route should be preferred whenever available.

---

# Part VII — dependencies, structural fingerprint, and open boundary

## 20. Dependencies used

This child uses only:

- the exact rank-one two-cap fiber decomposition from T-P5-239;
- the fact that T-P5-240 can transport the quotient geometry without changing the physical fiber problem;
- standard finite-dimensional S-lemma/trust-region duality under the strict source Slater point;
- exact `2x2` determinant/adjugate identities;
- elementary cubic calculus and discriminant identities.

It does not consume provenance receipts, admission state, or Lean compilation.

## 21. Candidate theorem statements

Suggested theorem/interface names:

- `twoDimFiber_slemma_iff_cubicCertificate`
- `twoDimFiber_spectralBoundary_hardCase`
- `cubicLaterLocalMax_squareFreeClassifier`
- `rankOneTwoCap_quotient3_degree12SafetyPartition`
- `strictRationalFiberSafety_hasRationalPDMultiplier`

The implementation should keep the hard spectral-boundary branch separate from the regular cubic branch; merging them by determinant equality is unsound.

## 22. Structural fingerprint

The new exact structural fingerprint is

**rank-one two-cap source -> outer scalar fiber -> 2D transverse ellipsoid -> lossless S-lemma -> 3x3 bordered PSD block -> cubic determinant in multiplier -> spectral-floor hard gate OR later cubic local maximum -> square-free discriminant test -> one-variable degree-12 outer partition.**

This is the two-dimensional analogue of T-P5-241's scalar-fiber closure, but its decisive object is a bordered determinant rather than direct endpoint evaluation.

## 23. Failure / non-applicability boundary

This child must fail closed in the following cases:

1. `M` is only PSD rather than positive definite: the source lacks the coercive compact ellipsoid assumed here; route to the earlier kernel/range machinery before applying this theorem.
2. `R<0`: the fiber is empty and belongs to source-feasibility logic, not this Lyapunov theorem.
3. `R=0`: the fiber is `{0}` and safety is simply `A<=0`; do not use the negative-leading-cubic argument because `a3=0`.
4. At singular `K(L)`, `det S(L)=0` alone is never a certificate; enforce range and pivot conditions.
5. A positive cubic determinant at a multiplier with indefinite `K` is meaningless; enforce the spectral/PSD gate.
6. The degree-12 outer statement presumes `M,G` are constant on the fixed source-radius branch, `l` is affine, and `A,R` are quadratic at worst. Higher-degree physical lifts require recomputing the degree bound.
7. None of these algebraic results proves that an actual P5 source pair has the rank-one/common-center structure or that the outer `s` interval covers the true trajectory/cell/tube.

## 24. What remains open

Still open and not claimed here:

- actual same-key P5 source binding for a quotient-dimension-three rank-one cap pair;
- proof that the required `M,G,A,l,R` packet comes from the same physical cell/face/source evaluator;
- exact outer interval / tube / trajectory coverage;
- implementation of ordered quadratic-field Sturm/root isolation;
- Float64/interval enclosure of generated coefficients;
- Lean/kernel formalization and independent validation by 封不觉;
- admission, registry mutation, or any P5/P8/M4 parent closure.

## 25. Next smallest mathematical seam

The next non-source-facing energy seam is the **strict-margin sensitivity problem for the cubic certificate**: quantify how a rational outward perturbation of `A,l,G` (coming from support-cap rounding or FD/DH remainder budgets) changes the maximum safe margin, so the source/support solver can be given an explicit admissible coefficient-error budget without rerunning full root partitioning.

A separate source-facing lane may instead instantiate T-P5-239/240/241/242 on one actual same-key source pair. That is deliberately not claimed by this mathematical child.
