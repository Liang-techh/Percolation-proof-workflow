---
kind: review_result
review_id: review-T-P5-160-degenerate-support-kernel-branch-guyuefangyuan-20260909T1432Z
task_id: T-P5-160-DEGENERATE-SUPPORT-KERNEL-BRANCH
reviewer: 古月方源
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-09T14:32:00Z
claim_commit: 3fbb1fec1aff70714d16f262451df205b585839a
inspected_commit: 3976d1cadb0999e33f8b39ee5f11de6c1fd178ac
upstream_commits:
  - fce11e2368dfd33d225a49adfbeb4a880a7c01ae  # T-P5-158 fixed-D support/KKT decision
  - 1710eb0b113e44bbe7a4d60367e0bcc8f941ccf9  # T-P5-159 monotone symbolic-floor bracketing
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_positive_kernel_PSD_collapse_and_tangent_curvature_branch; specialize_T159_determinant_degree_to_at_most_two_for_the_T154_loading; deflate_common_kernel_before_symbolic_root_search; never_use_full_determinant_zero_as_an_active-support_certificate
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: none; exact finite-dimensional real/rational algebra only
exit_code: n/a
---

# T-P5-160 — degenerate support kernel branch and tangent-curvature reduction

## 0. Verdict and exact seam

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-159 proves that every positive sharp uniform floor has an active support `S` with a strictly positive normalized zero-level kernel vector

`M_D,SS lambda = 0`, `lambda>0`, `1^T lambda=1`,

and notes an unresolved symbolic corner: a principal determinant polynomial may vanish identically, so determinant-root enumeration alone is not a complete active-support mechanism.

For the specific T-P5-154 family this seam is much more structured than a generic affine matrix pencil. Write, on one fixed support,

`M_D = M_0 + D L_g`,

where

`M_0[i,i]=0`, `2 M_0[i,j]=K_ij`,

and

`L_g = (g 1^T + 1 g^T)/2`.

This child proves four useful facts.

1. A symmetric copositive matrix with a **strictly positive kernel vector is automatically PSD**. Hence every active sharp support from T-P5-159 is not merely copositive: its principal block is PSD and singular.
2. Because `v^T L_g v=0` on the simplex tangent space `1^T v=0`, a positive zero-kernel candidate admits an exact **D-independent tangent-curvature criterion**. At such a candidate, support validity is equivalent to nonnegativity of `M_0` on `1^perp`.
3. The T-P5-154 loading has rank at most two. Therefore every nonzero principal determinant polynomial has degree at most **two**, not merely at most `|S|`. A positive sharp floor is thus at worst quadratic algebraic whenever an ordinary determinant polynomial detects it.
4. If the full determinant is identically zero because of a permanent common kernel, quotient that kernel first. A three-vertex exact rational example has `det M_D = 0` for every `D`, yet the reduced determinant is `16(D-1)` and the exact sharp floor is `D=1`. Thus determinant-zero by itself is neither sharpness nor failure.

No source equality, physical boundary attainability, runtime/Float64 semantics, Lean receipt, provenance/admission, registry mutation, or independent validation is claimed.

---

## 1. Structured loading inherited from T-P5-154

For a fixed support of size `n`, let `g_i>0` and pair coefficients `K_ij=K_ji`, `K_ii=0`.

T-P5-154 defines

`M_D[i,i] = D g_i`,

`2 M_D[i,j] = K_ij + D(g_i+g_j)` for `i!=j`.

Hence

`M_D = M_0 + D L_g`,

with

`L_g = (g 1^T + 1 g^T)/2`.

For every vector `v`,

**(1.1)** `v^T L_g v = (1^T v)(g^T v)`.

In particular,

**(1.2)** `1^T v=0  ==>  v^T L_g v=0`.

So the uniform-floor loading changes the affine level/tilt on the simplex but contributes **zero quadratic curvature along every simplex tangent direction**.

This special rank-two structure is the main extra information not used in the generic determinant discussion of T-P5-159.

---

## 2. Positive-kernel collapse: copositive becomes PSD

### Theorem T160-A — `copositive_with_positive_kernel_iff_psd`

Let `M` be a real symmetric matrix. Assume there exists `lambda` with

`lambda_i>0` for every coordinate,

and

`M lambda = 0`.

Then

**`M is copositive  <=>  M is PSD`.**

The reverse direction is immediate. For the nontrivial direction, assume `M` is copositive and take an arbitrary real vector `x`.

Because every `lambda_i>0`, choose `t>=0` sufficiently large that

`x+t lambda >=0`

componentwise. Since `M lambda=0` and `M` is symmetric,

`(x+t lambda)^T M (x+t lambda)`

`= x^T M x + 2t x^T M lambda + t^2 lambda^T M lambda`

`= x^T M x`.

The left side is nonnegative by copositivity. Hence `x^T M x>=0` for every real `x`, so `M` is PSD. ∎

### Consequence for T-P5-159

At every positive sharp floor `D_*>0`, T-P5-159 supplies an active support `S` and `lambda_S>0` with

`M_{D_*,SS} lambda_S=0`.

Global validity implies the principal block is copositive. T160-A therefore upgrades this to

**(2.1)** `M_{D_*,SS} >= 0` in the ordinary PSD sense.

So a genuine sharp interior support touches the PSD boundary. It is not a mysterious copositive-but-indefinite boundary point.

This is useful both mathematically and for a trusted checker: once a strictly positive zero-kernel packet is present, exact PSD machinery is no longer merely a sufficient fallback; on that support it is exact.

---

## 3. The tangent-curvature identity removes D from the validity test

Let `lambda` satisfy

`1^T lambda=1`,

`M_D lambda=0`.

Take any other affine-simplex point `mu` with `1^T mu=1`, and put

`v=mu-lambda`.

Then `1^T v=0`. Expanding around the zero-kernel point,

`mu^T M_D mu`

`= (lambda+v)^T M_D(lambda+v)`

`= v^T M_D v`

because `M_D lambda=0`. Using (1.2),

`v^T M_D v`

`= v^T M_0 v + D v^T L_g v`

`= v^T M_0 v`.

Therefore:

### Theorem T160-B — `zeroKernel_simplex_recenter`

If `1^T lambda=1`, `M_D lambda=0`, and `1^T mu=1`, then

**(3.1)**

`mu^T M_D mu = (mu-lambda)^T M_0 (mu-lambda)`.

This is exact and contains no approximation, norm inequality, inverse, square root, or eigenvalue.

### Corollary T160-C — exact tangent criterion

Assume additionally `lambda>0`. Then the following are equivalent on this support:

1. `M_D` is copositive;
2. `M_D` is PSD;
3. `v^T M_0 v>=0` for every `v` satisfying `1^T v=0`.

Proof:

- `1 <=> 2` is T160-A.
- `2 => 3`: on tangent vectors, `v^T M_D v=v^T M_0 v`.
- `3 => 1`: every nonzero `x>=0` can be normalized to a simplex point `mu=x/(1^T x)`; (3.1) then gives `mu^T M_D mu>=0`, and homogeneity returns `x^T M_D x>=0`.

Thus **the curvature test is independent of D**. D only needs to place a positive stationary point at zero level.

### Support-pruning obstruction

If there exists one tangent vector `v`, `1^T v=0`, with

`v^T M_0 v<0`,

then this support can never host a valid strictly-positive zero-kernel sharp candidate for any D.

Indeed any proposed positive kernel `lambda` would permit sufficiently small `epsilon` with `lambda+epsilon v` still inside the simplex, and (3.1) would give negative value.

This is a useful source-independent support pruning gate before any algebraic root search.

---

## 4. Exact support-floor theorem at a positive kernel

### Theorem T160-D — `supportSharp_of_tangentPSD_positiveKernel`

Assume

- every `g_i>0`;
- `D>=0`;
- `lambda>0`, `1^T lambda=1`;
- `M_D lambda=0`;
- `v^T M_0 v>=0` for every `v` with `1^T v=0`.

Then:

1. `D` is valid on the entire support simplex;
2. for every `D'<D`, the same `lambda` is a strict failure witness;
3. therefore `D` is the **least valid floor for that support**.

For item 2, T-P5-154 gives

`lambda^T M_{D'} lambda`

`= lambda^T M_D lambda + (D'-D) lambda^T L_g lambda`

`= (D'-D) g_lambda`,

where

`g_lambda=sum_i g_i lambda_i>0`.

Thus `D'<D` implies strict negativity.

For a support equal to the full uncertainty simplex, T160-D already proves the exact global sharp floor. For a proper support, it proves the exact floor of that face; other supports must still be checked through T-P5-158/T-P5-159 before a global claim is made.

---

## 5. Kernel dimension greater than one is not a problem

The sharpness certificate does not require a one-dimensional kernel.

If `ker M_D` has dimension greater than one and contains **any** strictly positive normalized vector, T160-A/B/C apply unchanged.

If a nonnegative kernel vector has zero coordinates, shrink to its positive support. On that principal support the restricted vector is strictly positive, so the same theorem applies there. This matches T-P5-158's support-lattice discipline: a zero coordinate is a face signal, not a full-support certificate.

Conversely, a singular matrix whose kernel has no nonzero nonnegative vector need not represent an active simplex contact at all. This distinction is exactly what a determinant-only protocol loses.

A fixed rational candidate `D` can test positive-kernel feasibility by the exact rational LP

`M_D lambda=0`,

`1^T lambda=1`,

`lambda_i>=t`,

maximize `t`.

A positive optimum means the kernel meets the strict simplex interior. This is the `alpha=0` boundary analogue of T-P5-158's support-margin LP and needs no determinant.

---

## 6. Stronger degree bound: every principal determinant is at most quadratic in D

T-P5-159 gave the general coarse bound `deg det(M_D,SS) <= |S|`. For the T-P5-154 loading we can sharpen this to two.

### Theorem T160-E — `structuredFloor_det_degree_le_two`

For every fixed support `S`,

**`p_S(D)=det(M_0,SS + D L_g,SS)` has degree at most 2.**

Reason: every column of `L_g` lies in

`span{g,1}`,

which has dimension at most two. Expand the determinant multilinearly in the columns. Any coefficient of `D^k` with `k>=3` selects at least three columns from `L_g`; those selected columns are linearly dependent, so that determinant term is zero.

Equivalently, `rank L_g<=2` forces the determinant polynomial degree to be at most two.

If `g` is proportional to `1` on the support, then `rank L_g<=1` and

**`deg p_S<=1`.**

### Consequence

Whenever `p_S` is not identically zero, every sharp candidate generated by that support is at worst a root of a rational quadratic polynomial. Thus the irrational example in T-P5-159 is representative of the worst algebraic degree allowed by this particular floor family; arbitrary high-degree algebraic roots do not arise from a single support determinant here.

A trusted checker still need not evaluate radicals. T-P5-159's rational PASS/FAIL bracketing remains the clean fail-closed consumer.

---

## 7. Identically zero determinant: common-kernel deflation

A simple and important cause of `det M_D identically 0` is a permanent common kernel.

Assume a matrix `Z` has independent columns and

`M_0 Z=0`,

`L_g Z=0`.

Then

`M_D Z=0`

for every D.

Choose any complement matrix `P` so that the square matrix

`B=[P Z]`

is invertible. By symmetry,

`P^T M_D Z=0`, `Z^T M_D P=0`, `Z^T M_D Z=0`.

Hence

### Theorem T160-F — `commonKernel_congruence_deflation`

**(7.1)**

`B^T M_D B = [[P^T M_D P, 0],[0,0]]`.

Therefore

**(7.2)** `M_D is PSD <=> P^T M_D P is PSD`.

So a permanent geometric nullspace should be removed **before** determinant/root logic. The reduced determinant can be nonzero even when the original determinant is identically zero.

This theorem is root-free and exact over rational data when rational `Z,P` are supplied.

### Boundary of this deflation theorem

Not every identically singular symmetric affine pencil must be assumed to possess a constant common kernel. A genuinely moving-kernel pencil is a separate rank-stratified case. The safe architecture is:

1. peel any exact common kernel that is actually proved;
2. if the reduced determinant is nonzero, use the degree-<=2 candidate logic;
3. if the reduced pencil remains identically singular without a proved common kernel, do **not** invent one and do not treat determinant zero as sharpness;
4. use T-P5-159 rational bracketing and fixed-D T-P5-158/positive-kernel feasibility as the fail-closed fallback until a lower-rank pencil theorem is supplied.

Thus this child closes the common-kernel degeneracy and the active positive-kernel validity test, but does not pretend every singular pencil has a constant nullspace.

---

## 8. Exact three-vertex regression: full determinant useless, reduced determinant exact

Take

`g=(1,1,1)`,

`K_12=K_13=-4`,

`K_23=0`.

Then

`M_D =`

```text
[ D    D-2  D-2 ]
[ D-2  D    D   ]
[ D-2  D    D   ].
```

Rows 2 and 3 coincide for every D, so

**`det M_D = 0 for every D`.**

The permanent common kernel contains

`z=(0,1,-1)`.

Yet the simplex quadratic is completely nontrivial:

`q_D(lambda)`

`= D - 4 lambda_1 lambda_2 - 4 lambda_1 lambda_3`

`= D - 4 lambda_1(1-lambda_1)`.

Since

`4 lambda_1(1-lambda_1) <= 1`,

we have

`q_D(lambda)>=D-1`,

with equality whenever `lambda_1=1/2`.

Therefore the exact sharp floor is

**`D_*=1`.**

At `D=1`,

```text
M_1 = [ 1 -1 -1 ]
      [-1  1  1 ]
      [-1  1  1 ]
```

`= u u^T`, with `u=(1,-1,-1)`,

so `M_1` is PSD of rank one. A strictly positive normalized kernel witness is

`lambda_*=(1/2,1/4,1/4)`.

Indeed `M_1 lambda_*=0`.

For every `D<1`, the same witness gives

`q_D(lambda_*)=D-1<0`.

Now deflate the common kernel using complement columns

`p_1=e_1`,

`p_2=(0,1,1)`.

Then

`P^T M_D P =`

```text
[ D      2D-4 ]
[ 2D-4   4D   ],
```

whose determinant is

**`16(D-1)`.**

For `D>=0`, the reduced block is PSD exactly when `D>=1`.

Thus the original determinant is identically zero and contains **no information about the threshold**, while the correctly deflated determinant recovers the exact sharp value immediately.

This example also shows why singularity alone is not an active-support certificate. For `D>1` the permanent kernel `span(0,1,-1)` remains, but it contains no nonzero nonnegative vector. At `D=1` the kernel dimension increases and acquires positive vectors. The active event is a **positive-kernel/rank-drop event**, not the mere fact that a determinant is zero.

---

## 9. Checker architecture suggested by the mathematics

For one support `S` in the T-P5-154 family:

1. Build exact rational `M_0,S` and `g_S`.
2. Form the tangent space `1^perp`. If its rational quadratic restriction of `M_0,S` has a negative witness, discard this support as incapable of hosting a valid positive-kernel sharp contact.
3. If a rational trial `D` is being checked, solve the exact positive-kernel LP `M_D lambda=0`, `1^Tlambda=1`, `lambda_i>=t`.
4. If `t>0`, support validity is now exactly equivalent to tangent PSD / ordinary PSD; no generic copositivity oracle is needed on that support.
5. For symbolic candidate generation, first deflate any **proved** common kernel of `M_0` and `L_g`.
6. On a regular reduced support pencil, its determinant has degree at most two. Isolate/bracket only those quadratic candidates.
7. If an identically singular reduced pencil remains with no proved common kernel, fall back to T-P5-159 monotone rational bracketing plus T-P5-158 fixed-D support decisions. Do not infer sharpness from `det=0`.

This separates candidate generation from trusted validity in a fail-closed way.

---

## 10. Suggested Lean theorem decomposition

The lowest-cost leaves are independent of determinant APIs.

### T160-L1 — structured loading tangent identity

```text
(sum v = 0) -> quad (L_g) v = 0
```

with `L_g=(g*1^T+1*g^T)/2`.

### T160-L2 — zero-kernel simplex recenter

```text
sum lambda = 1
sum mu = 1
(M0 + D*Lg) * lambda = 0
-> quad (M0 + D*Lg) mu = quad M0 (mu-lambda)
```

### T160-L3 — positive kernel collapses copositivity to PSD

```text
Symmetric M
(forall i, 0 < lambda_i)
M * lambda = 0
Copositive M
-> PSD M
```

The proof only needs the existence of a sufficiently large scalar shift `x+t lambda>=0` and quadratic expansion.

### T160-L4 — support sharpness

```text
0 <= D
g_i > 0
lambda > 0
sum lambda = 1
M_D * lambda = 0
(forall v, sum v = 0 -> 0 <= quad M0 v)
-> ValidOnSupport D
   and forall D' < D, not (ValidOnSupport D')
```

### T160-L5 — common-kernel deflation

```text
M0 * Z = 0
Lg * Z = 0
Invertible [P Z]
-> PSD (M0 + D*Lg) <-> PSD (P^T*(M0+D*Lg)*P)
```

The determinant-degree theorem can be formalized later via multilinearity/rank at most two; it is not needed to trust L1-L4.

---

## 11. Remaining open boundaries

1. **Actual source equality remains open.** No deployed reset/cell packet is bound here to concrete `g_i,K_ij`.
2. **Boundary attainability remains open.** Face-level algebra is not automatically a physical reset witness.
3. **Genuinely moving-kernel identically singular pencils remain a symbolic-generation branch.** This review gives a safe fallback but not a complete Kronecker/minimal-index classification.
4. **Tangent PSD needs a concrete exact checker/Lean consumer.** It is rational quadratic algebra, but no receipt is claimed.
5. **Algebraic root handling remains optional.** The degree bound is at most two, but rational bracketing from T-P5-159 remains safer for the current architecture.
6. **No parent status changes.** P5/P4/P8/M4, source/coverage, Float64, admission, registry, and independent verification all remain pending.

---

## 12. Recommended next mathematical/source handoff

The highest-value next source packet is no longer merely `det(M_D,SS)`.

For each actual same-key support, provide:

- exact rational `g_i,K_ij`;
- an exact tangent basis `P_T` for `1^perp` and the rational Gram `P_T^T M_0 P_T`;
- any proved common-kernel basis `Z` satisfying both `M_0 Z=0` and `L_g Z=0`;
- candidate/trial `D` with a positive-kernel witness when available.

Then the consumer can prune impossible supports by tangent curvature, deflate permanent degeneracy, and use only a quadratic symbolic candidate or T-P5-159 rational bracket.

**Do not use `det(M_D)=0` alone as evidence of an active robust-reset boundary.** The exact regression above shows that the determinant may vanish for every D while only one D is sharp.
