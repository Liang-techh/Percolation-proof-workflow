---
kind: review_result
review_id: review-T-P5-245-anisotropic-source-trust-region-reserve-kuangmanmozun-20260910T1236Z
task_id: T-P5-245-ANISOTROPIC-SOURCE-TRUST-REGION-RESERVE
reviewer: 狂蛮魔尊
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-10T12:36:00Z
claim_commit: 31fac0e92a841117cdde0683bda734b1c5ee4b23
inspected_commit: eefd1ad4be16a34e2a18d030286eae76d5e8a304
upstream_commits:
  - fb6c28d0f7492fc1f21856835e4c11a20047beed  # T-P5-244 scalar-Loewner source sensitivity
  - e8ba5dc69b700621893313a4202255a98267ebef  # T-P5-243 fixed-multiplier strict reserve
  - aa8124d17a0bfbed3572ed7cd3c20cdbe924964e  # T-P5-242 2D fiber S-lemma elimination
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_exact_anisotropic_source_radius_slemma; add_regular_fraction_free_radius_polynomial; add_singular_spectral_floor_gate; reuse_2d_cubic_classifier; preserve_source_coverage_float64_and_admission_gates
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact S-lemma algebra, Schur complement, adjugate elimination, generalized-eigenvalue threshold, exact rational counterexample; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-245 — Anisotropic source trust-region reserve

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-244 converts a shifted/shape-perturbed source ellipsoid to one scalar comparison `M' >= alpha M`, then pays the translated ball radius `(sqrt(R'/alpha)+sqrt(h^T M h))^2` against a strict fixed-multiplier Lyapunov reserve. That packet is robust, but after a nonzero center shift it can be sharply conservative because it lets the worst shape direction and the center direction align independently.

This child removes that collapse. It proves that the exact question

`sup { y^T M y : (y-h)^T M' (y-h) <= R' } <= B`

is itself a lossless one-constraint S-lemma/trust-region problem. For `R'>0` it is equivalent to a **single scalar multiplier** `mu>=0` and one PSD block. On the regular branch `mu M'-M>0`, the block reduces to a fraction-free univariate polynomial. For an `n`-dimensional source this polynomial has degree at most `n+1`; for a 2D source it is cubic and can reuse the exact T-P5-242 cubic machinery. The singular generalized-eigenvalue floor has an exact range/linear-solve hard gate, with no pseudoinverse.

Combined with the T-P5-243/T-P5-244 fixed multiplier reserve, this gives an exact certificate for how much **anisotropic shifted source motion** that particular radial reserve can tolerate. It is exact for reserve consumption, not a claim that failure of this packet means the actual target is unsafe.

No actual P5 same-key source metric, center/radius enclosure, coverage, Float64/interval semantics, Lean/kernel receipt, independent validation, admission, registry mutation, or P5/P8/M4 parent closure is claimed.

---

# Part I — base reserve interface

## 1. Fixed-multiplier radial envelope

Take the strict regular packet inherited from T-P5-243/T-P5-244:

`M in S_{++}^n`, `R>=0`,

`q(y)=A+2 l^T y+y^T G y`,

with one multiplier `lambda>=0` such that

`K0=lambda M-G>0`.

Let

`d0=det K0>0`, `J0=adj(K0)`,

`N0=d0(-A-lambda R)-l^T J0 l>0`,

`epsilon=N0/d0`.

Then the exact PSD completion from T-P5-243 gives, for every `y`,

**`q(y) <= -epsilon + lambda(y^T M y-R)`.**

If `lambda=0`, this is already the global bound `q<=-epsilon`; source enlargement costs nothing. The interesting source-motion branch is therefore `lambda>0`.

Define the largest base-metric radius allowed by this fixed reserve:

**`B := R + epsilon/lambda = R + N0/(d0 lambda)`.**

Then any domain `D` satisfying `y^T M y<=B` automatically satisfies `q<=0`.

Thus source motion reduces to one exact geometric question: does the perturbed source lie inside the base-metric ball of squared radius `B`?

---

# Part II — lossless anisotropic source-radius S-lemma

## 2. Perturbed ellipsoid

Let

`M' in S_{++}^n`, `R'>0`,

and

`E' := { y : (y-h)^T M' (y-h) <= R' }`.

We want to decide exactly whether

**`y^T M y <= B` for every `y in E'`.**

Because `R'>0`, `y=h` is a strict Slater point of the source inequality.

## 3. Exact multiplier block

Set

`g(y)=R'-(y-h)^T M'(y-h)`,

`f_B(y)=B-y^T M y`.

By the one-constraint lossless S-lemma,

`f_B>=0` on `{g>=0}`

iff there exists `mu>=0` such that

`f_B(y)-mu g(y)>=0` for every `y`.

Expanding gives

`f_B-mu g`

`= y^T(mu M'-M)y - 2 mu h^T M' y`

`  + B-mu R' + mu h^T M' h`.

Hence define

**`H_B(mu) := [[mu M'-M, -mu M' h],`

`               [-mu h^T M', B-mu R'+mu h^T M' h]]`.**

### Theorem A — `anisotropicSourceRadius_slemma`

For `M,M'>0` and `R'>0`,

**`sup_{E'} y^T M y <= B` iff `H_B(mu)>=0` for some `mu>=0`.**

This is exact. No scalar Loewner factor `alpha` is introduced.

Combining with the base radial envelope gives immediately:

### Corollary A1 — `anisotropicSourceReserve_transfer`

If `lambda>0` and some `mu>=0` satisfies `H_B(mu)>=0` with `B=R+epsilon/lambda`, then

**`q(y)<=0` for every `y in E'`.**

Again, this is an exact test for whether the **fixed radial reserve** proves safety on `E'`. If the test fails, a different target certificate may still prove safety.

---

# Part III — generalized spectral floor and regular Schur branch

## 4. The generalized spectral floor

Let

**`mu_* := lambda_max(M'^{-1/2} M M'^{-1/2})`.**

Equivalently `mu_*` is the largest generalized eigenvalue of

`M v = mu M' v`.

Since `M,M'>0`, `mu_*>0`. Put

`K(mu):=mu M'-M`.

Then

- `K(mu)>0` for every `mu>mu_*`;
- `K(mu)` is not PSD for `mu<mu_*`;
- `K(mu_*)>=0` is singular.

Therefore every exact source-radius multiplier lies either at the singular floor `mu_*` or on the regular half-line `mu>mu_*`.

For rational data, `mu_*` is an algebraic number determined by `det(mu M'-M)=0`; exact root isolation suffices. No floating eigenvector is part of the mathematical certificate.

## 5. Regular Schur identity

For `mu>mu_*`, `K(mu)>0`. Let

`z:=M h`, `H:=h^T M h`.

The Schur complement of the top-left block in `H_B(mu)` is

`B-mu R'+mu h^T M'h`

` - mu^2 h^T M' K(mu)^{-1} M' h`.

Using `mu M'=K+M`,

`mu^2 M'K^{-1}M' - mu M'`

`= (K+M)K^{-1}(K+M) - (K+M)`

`= M + M K^{-1} M`.

Therefore the Schur complement is exactly

**`B - [mu R' + H + z^T K(mu)^{-1} z]`.**

Define

**`C_req(mu) := mu R' + H + z^T K(mu)^{-1} z`.**

### Theorem B — `anisotropicSourceRadius_regular`

For `mu>mu_*`,

**`H_B(mu)>=0 iff C_req(mu)<=B`.**

The expression `C_req` is the exact regular-multiplier radius requirement.

## 6. Convexity and the hard-case geometry

Differentiate on `mu>mu_*`:

`C_req'(mu)=R' - z^T K^{-1} M' K^{-1} z`,

and

`C_req''(mu)=2 z^T K^{-1} M' K^{-1} M' K^{-1} z >=0`.

Indeed, with `w=K^{-1}z`, the last scalar is

`2 w^T M' K^{-1} M' w >=0`,

and it is strictly positive when `z!=0`.

Thus `C_req` is convex, strictly convex whenever `h!=0`, and tends to `+infinity` as `mu->+infinity` because `R'>0`.

Consequences:

- if the singular floor is compatible and minimizes the radius, the optimum is attained at `mu_*`;
- if the floor is incompatible and `h!=0`, the exact radius optimum lies at the unique interior stationary point;
- an optimizer search is not needed for a sign proof: the fraction-free polynomial below directly asks whether any regular multiplier meets `B`.

---

# Part IV — fraction-free regular certificate

## 7. Adjugate elimination

For `mu>mu_*`, define

`d(mu):=det K(mu)>0`,

`J(mu):=adj K(mu)`.

Then

`z^T K^{-1}z = z^T J z / d`.

Therefore `C_req(mu)<=B` is exactly

**`Phi_B(mu) := d(mu)(B-H-mu R') - z^T J(mu) z >=0`.**

No inverse remains.

If `M,M',h,R',B` are rational, `Phi_B` is a rational polynomial. Since

- `d(mu)` has degree `n`;
- `J(mu)` has degree at most `n-1`;

we obtain

**`deg Phi_B <= n+1`.**

The leading coefficient is `-R' det(M')<0`, so `Phi_B(mu)->-infinity` as `mu->+infinity`.

### Corollary B1 — 2D source

If `n=2`, `Phi_B` is cubic. Hence the exact local-maximum/discriminant machinery developed in T-P5-242 can be reused directly after replacing its target block by this source-radius block and retaining the singular-floor hard gate below.

This gives a concrete implementation path: anisotropic shifted source sensitivity in two dimensions costs one generalized-eigenvalue floor plus one cubic sign classifier, not an SDP or multidimensional optimizer.

## 8. Fully fraction-free composition with the base reserve

The base allowed radius is

`B=R+N0/(d0 lambda)`.

To avoid even this division, define

**`P(mu) := d(mu)[ d0 lambda (R-H-mu R') + N0 ]`

`          - d0 lambda z^T J(mu) z`.**

Because `d0 lambda>0`, on `mu>mu_*` we have

**`P(mu)>=0 iff Phi_B(mu)>=0 iff H_B(mu)>=0`.**

All coefficients of `P` are rational when the source/base packets are rational, and

`deg P<=n+1`.

This is the requested fraction-free anisotropic reserve packet.

## 9. Strict-margin rational witness

Suppose all data are rational and the perturbed source has strict room inside the allowed radius:

`sup_{E'} y^T M y < B`.

Then an S-lemma multiplier exists with strict scalar slack. If the optimum multiplier lies at the spectral floor, moving `mu` slightly into `mu>mu_*` preserves the strict inequality. Therefore there is an open interval of regular feasible multipliers. By density of `Q`, one may choose a **rational** `mu` in that interval.

Thus strict source-margin transport never forces the stored certificate to contain an algebraic multiplier. Algebraic root isolation is needed only for sharp/non-strict boundary classification.

---

# Part V — singular spectral-floor hard gate

## 10. Exact singular block criterion

At `mu=mu_*`, put

`K_*=mu_* M'-M >=0`,

`b_*:=mu_* M' h`,

`c_*:=B-mu_*R'+mu_* h^T M'h`.

The block

`[[K_*,-b_*],[-b_*^T,c_*]]`

is PSD iff both:

1. **range compatibility:** `b_* in range(K_*)`;
2. **Schur hard inequality:** for any solution `x` of `K_* x=b_*`,

   **`c_* - b_*^T x >=0`.**

The scalar is independent of the chosen solution because two solutions differ by a vector in `ker K_*`, orthogonal to `b_*` under the range condition.

This is the exact singular hard-case packet. It uses only a linear solve in the exact algebraic field containing `mu_*`; no pseudoinverse is required.

If `K_*=0`, the range gate reduces to `b_*=0`, after which the condition is simply `c_*>=0`.

## 11. Why singular incompatibility is not source failure

If `b_* notin range K_*`, the spectral-floor multiplier is inadmissible. This does **not** mean the radius inclusion fails: an interior `mu>mu_*` may still work. The dispatcher must continue to the regular polynomial `P(mu)` rather than report a mathematical FAIL.

This is the source-side analogue of the hard-case discipline in T-P5-242.

---

# Part VI — exact improvement over the scalar-alpha envelope

## 12. A rational 2D example

Take

`M=I_2`,

`M'=diag(100,1)`,

`R'=1`,

`h=e1`.

The perturbed ellipsoid is

`100(y1-1)^2 + y2^2 <=1`.

### T-P5-244 scalar collapse

The best scalar `alpha` satisfying `M'>=alpha M` is `alpha=1`. Therefore T-P5-244 uses

`a=R'/alpha=1`, `H=h^TMh=1`,

and obtains the sharp radius **for that scalar collapse**

`C_scalar=(sqrt a+sqrt H)^2=4`.

### Exact anisotropic radius

The generalized spectral floor is

`mu_*=1`,

because

`K(mu)=diag(100mu-1,mu-1)`.

At `mu=1`,

`K_*=diag(99,0)`,

and

`b_*=M'h=(100,0)`

lies in `range K_*`. Solve

`K_* x=b_*`

with `x=(100/99,0)`.

The exact radius condition at the floor gives

`C_exact = mu_*R' - mu_* h^TM'h + b_*^T x`

`=1-100+10000/99`

`=199/99`.

Equivalently the direct regular formula has boundary limit

`1+1+1/99=199/99`.

The same value is obtained by elementary optimization:
writing `y1=1+(1/10)c`, `y2=s` with `c^2+s^2<=1`,

`||y||^2 = 2 + (1/5)c - (99/100)c^2`,

whose maximum occurs at `c=10/99` and equals `199/99`.

Hence

**`C_exact=199/99 < 4=C_scalar`.**

The gap is not numerical noise; it is caused by the fact that the long axis of the ellipsoid is orthogonal to the center-shift direction.

## 13. Actual reserve packet where scalar comparison misses a PASS

Use the same base metric `M=I_2`, base radius `R=1`, and target

`q(y)= -5/2 + (1/2)||y||^2`.

Take fixed multiplier `lambda=1`. Then

`K0=lambda M-G=(1/2)I>0`,

and the fixed-multiplier vertical reserve is

`epsilon=3/2`.

Thus the allowed base-metric radius is

`B=R+epsilon/lambda=5/2`.

The scalar-alpha envelope produces `C_scalar=4>B`, so T-P5-244's scalar packet cannot certify this source motion.

But the exact anisotropic radius is

`199/99 < 5/2`.

Therefore T-P5-245 certifies `q<=0` on the whole shifted anisotropic ellipsoid. In fact the remaining radial reserve is

`5/2-199/99 = 97/198 >0`.

This is a strict, fully rational PASS missed by the scalar-collapse route.

---

# Part VII — important boundaries and failure semantics

## 14. Same-center case: no improvement if alpha is optimal

If `h=0`, then `z=0` and

`C_req(mu)=mu R'`.

Its minimum is attained at `mu=mu_*`, so

`sup_{y^TM'y<=R'} y^TMy = mu_* R'`.

But the **best** scalar `alpha` satisfying `M'>=alpha M` obeys

`1/alpha=mu_*`.

Thus, with an optimally chosen `alpha`, T-P5-244 is already exact for same-center ellipsoids. The new anisotropic child gains power specifically from coupling nonzero translation with directional shape, or when only a nonoptimal scalar comparison is available.

This prevents overclaiming the scope of the improvement.

## 15. Radius-zero branch

If `R'=0`, then positive definiteness of `M'` makes `E'={h}`. Strict Slater fails, so the S-lemma theorem above should not be invoked. The exact test is simply

**`h^T M h <= B`.**

## 16. Determinant alone is not a universal singular certificate

At a singular spectral floor, one must keep the range gate. In the repeated-eigenvalue case `M'=M`, `mu_*=1`, we have `K_*=0`. If `h!=0`, then `b_*=h!=0`, so the block cannot be PSD even though higher-dimensional determinants may vanish automatically from the zero top-left block. The exact rule is `b_*=0`, not “bordered determinant equals zero”.

## 17. Polynomial-search miss versus mathematical FAIL

For `R'>0`, the complete exact radius test consists of:

- the singular hard gate at `mu_*`; or
- existence of a regular `mu>mu_*` with `P(mu)>=0`.

If exact root isolation proves both branches impossible, then **the fixed radial reserve does not cover the entire perturbed source**.

This still must not be promoted to “the actual Lyapunov target is unsafe”. The radial envelope inherited from one fixed multiplier can be conservative. A fresh target S-lemma certificate, a different multiplier, a smaller actual source, or source-target correlation may still close the target.

Suggested failure label:

**`FIXED_RADIAL_RESERVE_ANISOTROPIC_SOURCE_NOT_COVERED`.**

Use a true mathematical FAIL only when an actual reachable `y in E'` with `q(y)>0` is separately constructed/bound.

---

# Part VIII — formalizable theorem statements

## 18. Core theorem skeletons

A Lean/checker-facing decomposition can be kept small:

1. `anisotropicSourceRadius_slemma`
   - assumptions: symmetric `M,M'`, `M>0`, `M'>0`, `R'>0`;
   - conclusion: ellipsoid inclusion iff existence of `mu>=0` with `H_B(mu)>=0`.

2. `anisotropicSourceRadius_regularSchur`
   - assumptions: `K=mu M'-M>0`;
   - conclusion: `H_B(mu)>=0` iff
     `d(B-H-mu R') - z^T adj(K)z >=0`.

3. `anisotropicSourceRadius_singularHard`
   - assumptions: `K>=0`;
   - conclusion: bordered block PSD iff `b in range K` and a linear-solve Schur scalar is nonnegative.

4. `anisotropicSourceReserve_fractionFree`
   - assumptions: T-P5-243 regular base packet, `lambda>0`, regular source multiplier;
   - conclusion: `P(mu)>=0 -> q<=0` on `E'`.

5. `anisotropicSourceRadius_convex`
   - assumptions: regular half-line;
   - conclusion: `C_req''>=0`, strict for `h!=0`.

6. `anisotropicSourceRadius_strictRationalWitness`
   - rational data + strict inclusion margin;
   - conclusion: existence of rational regular multiplier.

The S-lemma itself may remain an imported/trusted mathematical theorem until a dedicated formalization exists; this review does not claim a Lean receipt.

---

# Part IX — next step

## 19. Recommended next mathematical seam

The next genuinely distinct closure seam is **joint anisotropic source motion plus target-coefficient perturbation without first enclosing the moved source by one scalar base radius**. T-P5-244 currently composes them by first producing `C` and then charging all coefficient errors on `y^TMy<=C`; that can again lose directional correlation.

A natural next theorem would use a single joint block multiplier to absorb both the source metric/center perturbation and `(Delta A,Delta l,Delta G)` at once, then compare that block directly against the frozen strict S-lemma reserve. The useful goal is an exact or one-sided PSD matrix budget, not another scalar norm collapse.

Until a real source packet requires it, T-P5-245 is already the minimal exact cure for the scalar-alpha translation loss.

---

## 20. Non-claims

This child does not establish:

- actual P5 source/data equality or same-key binding;
- actual `M',h,R'` perturbation values;
- tube/cell/trajectory/FD-halo coverage;
- Float64 or interval enclosure;
- a Lean/kernel receipt;
- independent verification by 封不觉;
- admission/registry eligibility;
- P5/P8/M4 parent closure.

Status therefore remains **CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding**.