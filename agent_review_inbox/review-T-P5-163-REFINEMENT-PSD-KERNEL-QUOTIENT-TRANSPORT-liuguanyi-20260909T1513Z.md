---
kind: review_result
review_id: review-T-P5-163-refinement-psd-kernel-quotient-transport-liuguanyi-20260909T1513Z
task_id: T-P5-163-REFINEMENT-PSD-KERNEL-QUOTIENT-TRANSPORT
reviewer: 柳冠一
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-09T15:13:00Z
claim_commit: 4126f50bc261409737d278eefce4cf94536669a2
inspected_commit: e45733450516abebd54d1e89969e9c98bf1c85c7
upstream_commits:
  - 6b24af619a6649229803f4b12125a14bcf6e22c0  # T-P5-156 simplex refinement weighted-slack covariance
  - 1710eb0b113e44bbe7a4d60367e0bcc8f941ccf9  # T-P5-159 monotone symbolic-floor bracketing
  - 7024791953977bb79404d788d3d1246a20a37a57  # T-P5-160 degenerate support / tangent curvature
  - cf3879b10160fb5964218639570875de8f0e9ff2  # T-P5-161 Z-matrix copositivity = PSD
  - 4cdafba95db0d3cfee9c29ace026e77eea8f88f1  # T-P5-162 tangent-PD affine support continuation
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: transport_final_PSD_and_tangent_coercivity_through_refinement_congruence; tag_and_quotient_representation_kernel_before_interpreting_refined_singularity; never_require_refined_Z_sign_pattern_after_a_coarse_Z_to_PSD_proof; use_same_pulled_metric_to_avoid_condition_number_tax
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: none; exact finite-dimensional real/rational algebra only
exit_code: n/a
---

# T-P5-163 — refinement PSD/kernel quotient transport

## 0. Verdict and exact seam

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-156 proves that a simplex refinement/reparameterization with nonnegative column-stochastic map

`lambda = P mu`

transports a coarse quadratic proof matrix by congruence

`M_ref = P^T M P`.

T-P5-161 gives an exact fast path in a coarse coordinate system when `M` is a symmetric Z-matrix: copositivity then equals PSD. T-P5-160 and T-P5-162 subsequently use PSD/tangent-curvature and support-kernel structure.

The unclosed representation seam is that the **syntactic hypotheses used to discover a proof need not survive a change of barycentric coordinates**, while the mathematical proof itself does. In particular:

1. a coarse Z-matrix may cease to be a Z-matrix after a perfectly valid simplex refinement, even under an injective full-dimensional affine subcell map;
2. PSD nevertheless transports exactly by congruence;
3. if the refinement coordinates are redundant, `P^T M P` acquires an exact representation kernel even when the coarse physical quadratic is strictly positive;
4. that artificial kernel lies in the refined simplex tangent space for a column-stochastic `P`, so raw refined-coordinate tangent-PD and determinant tests can fail for purely coordinate reasons;
5. the correct invariant object is the quotient/image quadratic, or equivalently the pulled metric `P^T G P`, not an unrelated Euclidean norm on the refined coordinate vector.

This child proves the precise bridge and supplies exact rational counterexamples. It does not perform source admission, provenance/receipt audit, runtime/Float64 validation, Lean/kernel validation, or registry mutation.

---

## 1. Setup: refinement as a typed physical map

Let the coarse barycentric space have dimension `n` and the refined coordinate space dimension `m`. Let

`P in R^{n x m}`

have nonnegative entries and column sums equal to one:

**(1.1)** `P >= 0`,

**(1.2)** `1_n^T P = 1_m^T`.

Thus every refined simplex point `mu>=0`, `1_m^T mu=1` is sent to the coarse simplex point

`lambda=P mu >=0`, `1_n^T lambda=1`.

Let `M=M^T` be any coarse symmetric proof matrix and define

**(1.3)** `M_ref = P^T M P`.

Then for every refined vector `u`,

**(1.4)** `u^T M_ref u = (P u)^T M(P u)`.

This identity, not a norm estimate, is the entire transport mechanism.

---

## 2. PSD and copositivity transport

### Theorem T163-A — `psd_congruence_refinement`

If `M>=0` in the ordinary PSD sense, then

**`P^T M P >=0`**

for every real matrix `P`.

### Proof

For every `u`, equation (1.4) gives

`u^T P^T M P u = (Pu)^T M(Pu) >=0`. ∎

No invertibility, rank assumption, singular value, square root, or condition number is needed.

### Theorem T163-B — `copositive_pushforward_refinement`

If `M` is copositive and `P>=0`, then `P^T M P` is copositive.

### Proof

For `u>=0`, nonnegativity of `P` gives `Pu>=0`. Hence

`u^T P^T M P u=(Pu)^T M(Pu)>=0`. ∎

The converse is not true for an arbitrary refinement map because `P` may cover only a subcone/subsimplex. Converse transport requires a genuine coverage/surjectivity statement and is therefore a separate typed obligation.

### Corollary T163-C — transport the result of the Z fast path, not the syntax

Suppose the coarse matrix `M` satisfies the T-P5-161 Z-matrix gate and its coarse copositivity has therefore been upgraded to exact PSD. Then every refinement matrix inherits the PSD certificate

**`M_ref=P^T M P>=0`**

whether or not `M_ref` still has nonpositive off-diagonal entries.

Thus a downstream consumer must not rerun the Z-matrix sign gate after coordinate refinement and interpret its failure as a mathematical failure. Z-structure is a **discovery/decision fast-path type**; PSD is the transported mathematical certificate type.

---

## 3. Z-matrix structure is not refinement invariant

The loss occurs even for an injective rational affine subcell map.

Take

`M = I_2`,

which is PSD and a symmetric Z-matrix because its only off-diagonal entries are zero. Let

`P = [[1, 1/2],
      [0, 1/2]]`.

Both columns are nonnegative and sum to one, and `det P=1/2`, so this is injective. It represents the subsegment whose refined vertices are `e_1` and the midpoint `(e_1+e_2)/2`.

Yet

`P^T M P = [[1,   1/2],
             [1/2, 1/2]]`.

Its off-diagonal entry is **positive**. Hence it is not a Z-matrix. Nevertheless

`det(P^T M P)=1/4>0`

and the matrix is positive definite.

Therefore:

**(3.1)** `coarse Z + valid affine refinement` does **not** imply `refined Z`;

**(3.2)** failing the refined Z sign test can coexist with a strict transported PSD proof.

A sufficient syntactic condition for the refined matrix to remain Z is simply the exact cross-column gate

`p_alpha^T M p_beta <=0` for all `alpha!=beta`,

where `p_alpha` are the columns of `P`. But this is optional. Once coarse PSD has already been proved, no Z gate is mathematically required downstream.

---

## 4. Exact kernel transport

The next seam is more structural.

### Theorem T163-D — `kernel_of_psd_congruence`

Assume `M=M^T>=0`. Then

**`ker(P^T M P) = {u : P u in ker M}`.**

### Proof

For a symmetric PSD matrix, `x^T M x=0` if and only if `Mx=0`. Hence, using (1.4),

`u in ker(P^T M P)`

iff

`u^T P^T M P u=0`

iff

`(Pu)^T M(Pu)=0`

iff

`Pu in ker M`. ∎

### Corollary T163-E — positive-definite coarse form

If `M>0`, then

**`ker(P^T M P)=ker P`.**

So a redundant refinement can create singularity only because several refined coordinate vectors describe the same coarse/physical vector.

### Corollary T163-F — common representation kernel for a matrix family

For any family `M_D`, regardless of D,

**`ker P subseteq ker(P^T M_D P)`**.

Thus, if `P` has a nontrivial kernel, the refined family has a D-independent common kernel before any physical sharpness mechanism is considered.

In particular, if `m>rank(P)`, every full refined determinant

`det(P^T M_D P)`

vanishes identically in D. This can happen even when every coarse `M_D` is nonsingular.

This is exactly the representation-level obstruction that must be removed before applying the determinant/root language of T-P5-159 or the common-kernel branch of T-P5-160.

---

## 5. Column-stochastic refinement sends tangent space to tangent space

Define the simplex tangent spaces

`T_m = {u in R^m : 1_m^T u=0}`,

`T_n = {z in R^n : 1_n^T z=0}`.

### Theorem T163-G — `refinement_maps_tangent_to_tangent`

Under the column-sum identity `1_n^T P=1_m^T`,

**`P(T_m) subseteq T_n`.**

Indeed, for `u in T_m`,

`1_n^T P u = 1_m^T u =0`.

Moreover,

**`ker P subseteq T_m`**,

because `Pu=0` implies

`1_m^T u = 1_n^T P u =0`.

So every representation-null direction produced by a column-stochastic refinement is automatically a **refined simplex tangent direction**.

This matters directly for T-P5-162.

---

## 6. Tangent-PD transports as quotient-PD, not necessarily raw PD

Assume the coarse base quadratic is strictly positive on the coarse tangent space:

**(TPD-coarse)** `z^T M_0 z>0` for every nonzero `z in T_n`.

Set

`M_0^ref=P^T M_0 P`.

### Theorem T163-H — `tangentPD_refinement_mod_kernel`

For every `u in T_m`,

`u^T M_0^ref u = (Pu)^T M_0(Pu) >=0`,

and equality holds exactly when `Pu=0`.

Equivalently,

**`ker(M_0^ref | T_m)=ker P`,**

and the induced quadratic form on the quotient

**`T_m / ker P`**

is strictly positive definite.

### Proof

By T163-G, `Pu in T_n`. The coarse tangent-PD hypothesis makes `(Pu)^T M_0(Pu)` strictly positive whenever `Pu!=0`, and zero when `Pu=0`. ∎

### Consequence for T-P5-162

If `ker P != {0}`, then the raw refined tangent-PD hypothesis used by T-P5-162 **must fail**, even though the physical/coarse tangent curvature is perfectly strict. Therefore a consumer must choose one of two mathematically correct routes:

1. run the T-P5-162 affine-support continuation in coarse/image coordinates and transport its result through `P`; or
2. quotient/deflate `ker P` before invoking tangent-PD in refined coordinates.

Treating raw refined-coordinate tangent singularity as a new physical degeneracy is incorrect.

---

## 7. Quantitative coercivity transports with the same constant in the pulled metric

The qualitative quotient statement has an exact quantitative version that avoids every Jacobian/condition-number penalty.

Let `G=G^T>=0` be a coarse tangent metric and suppose

**(7.1)** `z^T M_0 z >= alpha z^T G z`

for all `z in T_n`, with `alpha>=0`.

Define the pulled metric

**(7.2)** `G_ref=P^T G P`.

### Theorem T163-I — `tangent_coercivity_pullback_same_constant`

For every `u in T_m`,

**`u^T M_0^ref u >= alpha u^T G_ref u`.**

### Proof

Use T163-G and apply (7.1) to `z=Pu`:

`u^T M_0^ref u=(Pu)^T M_0(Pu)`

`>= alpha (Pu)^T G(Pu)`

`= alpha u^T G_ref u`. ∎

The **same alpha** survives. No smallest singular value of `P` appears because the metric is transported covariantly with the quadratic form.

If a downstream implementation instead insists on a lower bound against an unrelated Euclidean norm `||u||^2`, then an injectivity/conditioning bound for `P` on the chosen quotient/complement is genuinely required. When `ker P!=0`, no positive global Euclidean constant can exist on raw `T_m`. That is not a weakness of the proof; it is the exact coordinate redundancy.

---

## 8. Exact rational overcomplete regression: artificial tangent kernel

Take again `M=I_2`, but now use the overcomplete barycentric map

`P = [[1, 0, 1/2],
      [0, 1, 1/2]]`.

The three refined coordinates represent the two coarse vertices and their midpoint. Then

`M_ref=P^T P`

`= [[1,   0,   1/2],
    [0,   1,   1/2],
    [1/2, 1/2, 1/2]]`.

The vector

**`k=(-1,-1,2)^T`**

satisfies

`Pk=0`,

and also

`1_3^T k=0`.

Hence

`M_ref k=0`

and `k` is a nonzero refined **tangent** zero mode. The coarse matrix `I_2` is strictly positive in every nonzero direction; the zero mode is 100% representation redundancy.

Consequences:

- `det M_ref=0` does not indicate a physical sharp floor;
- raw refined T-P5-162 tangent-PD fails although coarse TPD is strict;
- a common-kernel detector sees a real algebraic kernel, but its semantic type is `representation_kernel`, not `physical_kernel`;
- quotienting by `span{k}` recovers the two-dimensional image form exactly.

This example is rational and can be used as a regression fixture.

---

## 9. Refined version of the T-P5-162 energy split

The quotient need not be materialized explicitly.

Assume the coarse T-P5-162 branch supplies a stationary point `lambda_D` on `1_n^T lambda=1` and its scalar value `phi(D)`, with exact gap identity

`q_D(lambda)-phi(D)`

`= (lambda-lambda_D)^T M_0(lambda-lambda_D)`.

Suppose a refined witness `mu_D` satisfies

**(9.1)** `P mu_D=lambda_D`.

Then for every refined affine point `nu` with `1_m^T nu=1`,

### Theorem T163-J — `refined_energy_gap_through_image`

**`q_D^ref(nu)-phi(D)`**

**`= (P(nu-mu_D))^T M_0 P(nu-mu_D)`.**

Under coarse tangent-PD this is nonnegative, and equality holds exactly when

**`P nu=lambda_D`.**

Thus the refined minimizer is generally not a unique coordinate vector; it is the entire representation fiber over the unique physical minimizer.

If `mu_D>=0`, then `lambda_D` is actually represented in the refined simplex, so the physical FAIL/zero witness from T-P5-162 is available in the refined coordinates as well. If no nonnegative `mu_D` exists, the refinement is a genuine domain restriction/subsimplex and the coarse stationary point lies outside that local cell; one must then use the appropriate face/subcell branch rather than inventing a coordinate residual.

This cleanly separates:

- **representation multiplicity**: several `mu` map to the same physical `lambda`; from
- **domain restriction**: the local refined simplex does not contain a given coarse point.

---

## 10. Determinant/root search must deflate representation kernel first

T-P5-159 proves a necessary active-support condition: at a positive sharp floor, an active support block is singular. T-P5-160 then explains how permanent kernels can make determinant polynomials identically zero.

T163-F shows a new typed source of such permanent kernels:

**every nonzero `ker P` is automatically a common kernel of every refined congruence family `P^T M_D P`.**

Therefore the following inference is invalid after an overcomplete refinement:

`det(P^T M_D P)=0  =>  physical active support / sharp floor candidate`.

The left side may hold for every D solely because of barycentric redundancy.

The correct order is:

1. bind the refinement map `P`;
2. identify or implicitly quotient its representation kernel;
3. transport the coarse quadratic to the image/quotient;
4. only then interpret any **additional** kernel as a physical tangent/support degeneracy.

A trusted checker does not need an orthonormal kernel basis. It may instead retain the image formulation `(Pu)^T M_D(Pu)` and equality witness `P u=0`; all identities remain exact and rational.

---

## 11. Minimal theorem statements for formalization

A small formal layer is enough.

### T163-A

`psd M -> psd (P^T M P)`.

### T163-B

`copositive M -> entrywise_nonneg P -> copositive (P^T M P)`.

### T163-D

`psd M -> ker(P^T M P) = preimage P (ker M)`.

### T163-G

`one^T P = one^T -> P(tangent_m) subset tangent_n` and `ker P subset tangent_m`.

### T163-H

`tangentPD M0 -> ker((P^T M0 P)|tangent_m)=ker P`.

### T163-I

`tangentLower M0 alpha G -> tangentLower (P^T M0 P) alpha (P^T G P)`.

### T163-J

`P muD=lambdaD -> refinedGap = coarseGap after P`.

All are finite-dimensional exact algebra. None requires matrix inversion, spectral decomposition, square root, singular value, or floating-point semantics.

---

## 12. Suggested typed producer/checker packet

For any use of a refined simplex certificate, bind the following to the same `parameterKey/cellKey/certificateKey`:

- exact refinement matrix `P`;
- proof that `P>=0` when copositive/nonnegative-cone transport is used;
- exact column-sum identity `1^T P=1^T` when simplex/tangent semantics are used;
- coarse proof matrix `M` or family `M_D`;
- transported matrix identity `M_ref=P^T M P` if materialized;
- coarse PSD/copositive/tangent-coercive theorem type;
- pulled metric `G_ref=P^T G P` when quantitative coercivity is consumed;
- a representation-kernel tag when `ker P!=0`, or an injectivity witness when local refined coordinates are nonredundant;
- for T-P5-162 witness transport, a signed/exact solve `P mu_D=lambda_D` and `mu_D>=0` if a refined physical simplex witness is claimed.

Consumer rule:

> A sign-pattern fast path such as Z-matrix is not a coordinate-invariant proof type. Once it has established PSD, transport PSD. A raw refined-coordinate zero mode is not a physical zero mode until the representation kernel has been removed or ruled out.

---

## 13. Open boundaries

This review intentionally leaves OPEN:

1. whether the actual uncertainty/refinement producer uses one overcomplete barycentric map or a collection of injective simplicial subcell maps;
2. exact source equality for the actual `P` matrices;
3. whether each local refinement covers the whole coarse simplex or only a strict subcell;
4. source binding of the actual `M_D`, `G`, and floor parameters;
5. actual rank/injectivity certificates for each local `P`;
6. Float64/runtime barycentric computation and solver semantics;
7. whole-cell/path/flowpipe coverage;
8. P8/M4 downstream integration;
9. Lean/kernel formalization;
10. independent validation by 封不觉;
11. admission/registry mutation.

No status above is upgraded by this mathematical child.

---

## 14. Bottom line

The coordinate-invariant chain is

**`coarse Z fast path -> coarse PSD -> congruence transport -> quotient/image PSD or tangent coercivity`.**

It is **not**

**`coarse Z -> refine coordinates -> demand refined Z again`.**

And when refinement coordinates are redundant,

**`refined singularity = physical singularity`**

is false in general. The exact replacement is

**`ker(P^T M P) = P^{-1}(ker M)`** for PSD `M`,

so `ker P` is the representation kernel that must be removed before interpreting any remaining null direction as a physical active-support obstruction.