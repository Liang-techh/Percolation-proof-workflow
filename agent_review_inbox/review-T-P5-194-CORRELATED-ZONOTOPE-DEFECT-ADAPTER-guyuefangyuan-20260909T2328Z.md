---
kind: review_result
review_id: review-T-P5-194-correlated-zonotope-defect-adapter-guyuefangyuan-20260909T2328Z
task_id: T-P5-194-CORRELATED-ZONOTOPE-DEFECT-ADAPTER
reviewer: 古月方源
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-09T23:28:00Z
claim_commit: f9e420b1bdf6d77655d8dd0efeffd3db816747e3
inspected_commit: 24a886e686a2faf4dc52d29dc576c19893597676
upstream_commits:
  - ef1dfbc4779541e30d02843b282cdd9e892912a2  # T-P5-191 affine finite-cone viability
  - 86d3e6a59cf11c4d1bd28ffa5a6ab7a66cd20eda  # T-P5-192 selector-cone Lyapunov margin
  - d412e3deb9d63b72685ccf3ac202665863b5525d  # T-P5-193 affine-box defect bridge
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_zonotope_support_adapter; add_zonotope_metzler_viability_packet; add_latent_sign_fan_lyapunov_packet; preserve_correlated_source_semantics
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact finite-dimensional support-function algebra, polyhedral Farkas reduction, selector-cone quadratic pullback, exact rational counterexamples; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-194 — correlation-preserving zonotope defect adapter

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-193 deliberately replaced a correlated source remainder by an independent componentwise box. That bridge is safe for PASS when the box is an outer enclosure, but it can be strictly conservative because different output coordinates are then allowed to choose unrelated worst-case signs.

This review closes the next narrow mathematics seam: preserve a finite set of shared latent error directions instead of expanding them into an axis-aligned box.

Let the external state be `e in R^p`. Fix a generator matrix

`Z = [z_1 ... z_m] in R^(p x m)`

and nonnegative state-dependent amplitudes

`a(e) = H e + h0 in R^m`,

`a(e) >= 0` on the intended domain.

The correlated defect set is the centered zonotope

**`U_Z(e) := { Z diag(a(e)) xi : -1 <= xi <= 1 }`.**

The same latent coordinate `xi_k` multiplies the entire vector direction `z_k`; hence correlations between physical output coordinates are retained.

The main exact identities are:

1. for every test direction `w`,

   **`sup_{rho in U_Z(e)} w^T rho = |Z^T w|^T a(e)`**,

   and the infimum is its negative;

2. for a polyhedral finite-value cone `E_N={e:N e>=0}`, define

   **`S := |N Z|`** entrywise.

   Exact full-zonotope robust tangency is equivalent to the T-P5-191 Metzler packet

   **`N A - S H = Lambda N`,**

   **`Lambda_ij>=0` for `i!=j`,**

   **`N c >= S h0`;**

3. for a T-P5-192 selector with frozen gradient `G e`, set

   **`F := Z^T G`.**

   The exact worst zonotope defect is

   **`a(e)^T |F e|`.**

   On each latent sign sector `Sigma F e>=0`, this becomes one explicit symmetric quadratic plus one linear form, so the existing finite-generator/copositivity checker applies unchanged;

4. the zonotope packet is never more conservative than first replacing the same set by its exact coordinate box hull. Quantitatively,

   **`|Z^T w|^T a <= |w|^T |Z| a`.**

   The inequality can be strict by an arbitrarily large relative factor, including exact cancellation to zero.

No source extraction, Float64 interval soundness, PDE closure, actual sector coverage, Lean/kernel proof, independent verification, or registry admission is claimed.

---

## 1. Typed setup

Use the following dimensions:

- external state `e in R^p`;
- latent uncertainty `xi in R^m`;
- generator matrix `Z in R^(p x m)`;
- affine amplitude map `a(e)=H e+h0`, with `H in R^(m x p)`, `h0 in R^m`;
- external affine core `f0(e)=A e+c`.

Assume

**`a(e)>=0`**

on every state where the defect packet is consumed.

Define

`rho(e,xi) := Z diag(a(e)) xi`

for `|xi_k|<=1`.

Equivalently,

`rho = sum_k xi_k a_k(e) z_k`.

The important semantic distinction is:

- **exact zonotope inclusion:** every `xi in [-1,1]^m` is an allowed instantaneous uncertainty;
- **outer zonotope enclosure:** the actual residual set is only a subset of `U_Z(e)`.

All PASS statements below remain sound for an outer enclosure. Necessity and robust-FAIL semantics require exact inclusion, or a separately source-bound bad latent witness.

A producer must not infer exact latent independence merely because it stores generators and interval amplitudes.

---

## 2. T194-A — exact support function of the correlated zonotope

For any `w in R^p` and any nonnegative amplitude vector `a`,

`w^T rho = w^T Z diag(a) xi`

`= sum_k xi_k a_k (z_k^T w)`.

Since each latent coordinate satisfies `-1<=xi_k<=1`,

`xi_k a_k (z_k^T w) <= a_k |z_k^T w|`.

Summing gives

`w^T rho <= sum_k a_k |z_k^T w|`.

Equality is attained by the single latent choice

`xi_k = sign(z_k^T w)`

(with either sign when the scalar is zero). Therefore

### Exact support identity

**`sup_{rho in U_Z(e)} w^T rho = sum_k a_k(e)|z_k^T w|`**

or, in matrix notation,

**`sup w^T rho = |Z^T w|^T a(e)`.**

Because the zonotope is centrally symmetric,

**`inf_{rho in U_Z(e)} w^T rho = -|Z^T w|^T a(e)`.**

This is the direct correlated analogue of T-P5-193's box identity. The difference is crucial: the absolute value is applied **after projecting each shared generator into the tested direction**, not independently to every physical coordinate.

---

## 3. T194-B — exact axis-aligned hull and a quantified conservatism inequality

The smallest centered coordinate box containing `U_Z(e)` has half-width

**`b(e) = |Z| a(e)`**, entrywise.

Indeed, coordinate `j` satisfies

`|rho_j| = |sum_k Z_jk a_k xi_k|`

`<= sum_k |Z_jk| a_k`,

and equality in that coordinate is attained by choosing `xi_k=sign(Z_jk)`.

The support function of this coordinate hull is therefore

`h_box(w)=|w|^T |Z| a`.

By the triangle inequality, generator by generator,

`|z_k^T w| = |sum_j Z_jk w_j|`

`<= sum_j |Z_jk||w_j|`.

Multiplying by `a_k>=0` and summing gives the exact dominance relation

### Zonotope-versus-box support inequality

**`|Z^T w|^T a <= |w|^T |Z| a`.**

Thus replacing a zonotope by its axis-aligned hull can never improve a robust PASS test and may strictly worsen it.

Equality for a fixed `w` holds precisely when, for every active generator `k` with `a_k>0`, the nonzero scalars `w_j Z_jk` do not cancel in sign. Any generator that contributes with opposite signs across coordinates creates a strict box-hull tax.

This gives a source-side diagnostic: before accepting the T-P5-193 box expansion, compute the exact projected generator supports. If large cancellation is present in important facet normals or Lyapunov gradients, keeping the latent generator representation can materially enlarge the provable domain.

---

## 4. T194-C — exact rational example: box hull can reject an invariant correlated system

Take `p=2`, one latent generator,

`Z = [[1],[1]]`,

and constant amplitude `a=1`.

Then

`U_Z = { xi(1,1) : |xi|<=1 }`.

Consider the cone/half-space

`E={e : n^T e>=0}`

with

`n=(1,-1)`.

For every allowed zonotope defect,

`n^T rho = xi(1-1)=0`.

Therefore under the pure uncertainty dynamics

`e'=rho`

this facet is exactly invariant: the defect is tangent to it.

But the smallest coordinate box hull is

`[-1,1]^2`.

T-P5-193's box support gives

`|n|^T(1,1)=2`.

The spurious box point

`rho_box=(-1,1)`

gives

`n^T rho_box=-2`.

Hence the box-robust viability test rejects while the exact correlated zonotope test passes with zero defect margin.

This is not a numerical edge case. It is a structural loss of shared-sign information. Scaling the amplitude makes the box penalty arbitrarily large while the exact zonotope normal penalty remains identically zero.

---

## 5. T194-D — exact zonotope-robust polyhedral cone viability lift

Let

`E_N={e : N e>=0}`

with rows `n_i^T` and affine core

`e' = A e+c+rho`,

`rho in U_Z(e)`.

Define the nonnegative facet/generator support matrix

**`S := |N Z|`**

(entrywise absolute value), so

`S_ik = |n_i^T z_k|`.

By T194-A, for row `i`,

`inf_{rho in U_Z(e)} n_i^T rho`

`= -sum_k |n_i^T z_k| a_k(e)`

`= -(S H e + S h0)_i`.

Therefore exact robust tangency on active face `i` is

`n_i^T A e+n_i^T c-(S H e+S h0)_i >=0`

for every `e` on that face.

Set

`A_N := N A-S H`,

`c_N := N c-S h0`.

The condition is now precisely the affine face-tangency problem already solved by T-P5-191. Consequently:

### Exact Metzler lift for the zonotope

Under exact zonotope inclusion, all-face robust tangency is equivalent to existence of `Lambda` such that

**`N A-S H = Lambda N`,**

**`Lambda_ij>=0` for every `i!=j`,**

**`N c>=S h0`.**

No square roots, norm conversion, SDP, or online latent optimization is required.

The diagonal of `Lambda` remains unrestricted exactly as in T-P5-191.

### Direct invariance inequality

Let `y=N e`. Every allowed zonotope defect satisfies componentwise

`N rho >= -S a(e)`

`= -S H e-S h0`.

Using the lift,

`N A e-S H e = Lambda N e`.

Hence

**`y' >= Lambda y + (N c-S h0)`.**

If `Lambda` is Metzler and the forcing is nonnegative, positive-system comparison keeps `y>=0` forward invariant.

This direct proof makes the outer-enclosure semantics clear: even if the actual residual occupies only a strict subset of `U_Z(e)`, the same packet remains a sound sufficient certificate.

---

## 6. T194-E — box bridge is recovered exactly as a special case

Choose

`Z=I_p`.

Then each latent coordinate controls exactly one physical coordinate and

`S=|N I|=|N|`.

The zonotope becomes

`U_Z(e)={rho : |rho|<=a(e)}`,

so T194-D reduces verbatim to T-P5-193:

`N A-|N|H=Lambda N`,

`N c>=|N|h0`.

Thus T-P5-194 is a strict structural generalization, not a competing adapter.

At the opposite extreme, a low-rank generator matrix with `m<<p` can preserve strong cross-coordinate correlations while requiring only `m` latent sign decisions in the Lyapunov branch below.

---

## 7. T194-F — exact worst zonotope term in the frozen-selector derivative

Use T-P5-192 notation on one exact selector cone `C_alpha`:

- selector `u=Y_alpha e`;
- branch energy `Phi(e)=e^T Q_alpha e`;
- frozen gradient matrix `G_alpha=B Y_alpha+C`;
- affine-core derivative matrix `L_alpha=A^T G_alpha+G_alpha^T A`.

For the perturbed field,

`D^+ Phi(e)`

`<= e^T L_alpha e + 2 c^T G_alpha e + 2 rho^T G_alpha e`.

Apply T194-A with

`w=G_alpha e`.

Define

**`F_alpha := Z^T G_alpha`**

of shape `m x p`.

Then at fixed `e`,

### Exact frozen-gradient zonotope support

**`sup_{rho in U_Z(e)} rho^T G_alpha e`**

**`= a(e)^T |F_alpha e|`.**

Therefore

**`D^+ Phi(e) <= e^T L_alpha e + 2 c^T G_alpha e + 2 a(e)^T |F_alpha e|`.**

This is strictly sharper than first taking the coordinate box hull, because T194-B gives

`a^T|Z^T G e| <= (|Z|a)^T |G e|`.

No generic Euclidean norm has been introduced.

---

## 8. T194-G — finite latent sign fan gives an exact quadratic-plus-linear branch

Fix `sigma in {+1,-1}^m` and let

`Sigma=diag(sigma)`.

Define the latent sign sector

**`C_(alpha,sigma) := C_alpha intersect {e : Sigma F_alpha e>=0}`.**

Because `F_alpha e` is linear in `e`, this is again a polyhedral cone whenever `C_alpha` is polyhedral.

On the sector,

`|F_alpha e|=Sigma F_alpha e`.

Since `a(e)=H e+h0`,

`2 a(e)^T |F_alpha e|`

`=2(H e+h0)^T Sigma F_alpha e`

`= e^T D_(alpha,sigma)e + 2 d_(alpha,sigma)^T e`,

where

**`D_(alpha,sigma)`**

`:= H^T Sigma F_alpha + F_alpha^T Sigma H`,

and

**`d_(alpha,sigma) := F_alpha^T Sigma h0`.**

The matrix `D_(alpha,sigma)` is symmetric by construction.

Hence the exact robust frozen-selector derivative upper bound on one latent sign sector is

**`e^T (L_alpha+D_(alpha,sigma)) e`**

`+ 2 (G_alpha^T c+d_(alpha,sigma))^T e`.

This is exactly the same algebraic shape consumed by T-P5-192/T-P5-193, but the sign fan now tracks shared latent generator projections `Z^T G e`, not independent physical coordinates.

If `m<p`, the ambient maximum number of sign patterns drops from `2^p` to `2^m`; only nonempty sectors need to be emitted.

---

## 9. T194-H — exact target-rate packet and copositivity pullback

Fix target rate `gamma>=0`.

On one selector/latent-sign sector define

**`M_(alpha,sigma)(gamma)`**

`:= L_alpha + 2 gamma Q_alpha`

`   + H^T Sigma F_alpha + F_alpha^T Sigma H`,

and

**`ell_(alpha,sigma)`**

`:= G_alpha^T c + F_alpha^T Sigma h0`.

A robust target decay inequality

`D^+ Phi(e) <= -2 gamma Phi(e)`

is implied exactly on that sector by

`e^T M_(alpha,sigma)(gamma)e + 2 ell_(alpha,sigma)^T e <=0`.

Because the sector is a cone, the T-P5-192 scaling argument separates this mixed-degree inequality exactly into

**quadratic gate**

`e^T M_(alpha,sigma)(gamma)e<=0`,

and

**linear gate**

`ell_(alpha,sigma)^T e<=0`.

If the sector is represented as

`C_(alpha,sigma)=cone(V_(alpha,sigma))`,

then these are equivalent to finite algebraic checks:

1. **copositivity**

   `-V^T M_(alpha,sigma)(gamma)V` is copositive;

2. **entrywise linear sign**

   `V^T ell_(alpha,sigma)<=0`.

Thus all fixed rational copositivity machinery from T-P5-158 and later fast paths can be reused unchanged.

The only new producer-side objects are `Z`, the affine amplitude map, and the latent sign-sector generators.

---

## 10. Nonnegative-amplitude gate is exact and must remain explicit

The support formula uses `a_k(e)>=0` as a half-width/amplitude premise.

If a sign sector is an unbounded cone `cone(V)`, then for affine amplitudes

`a(e)=H e+h0`,

nonnegativity on the entire cone is equivalent to the two finite conditions

**`h0>=0`,**

**`H V>=0` entrywise.**

Sufficiency is immediate.

Necessity follows because `e=0` gives `h0>=0`; and if some generator direction makes one component of `H V` negative, scaling that ray eventually makes the affine amplitude negative regardless of the constant offset.

For a bounded physical cell rather than a cone, the correct amplitude check is a bounded-polytope minimum and must not be silently replaced by the cone criterion.

This premise is a mathematical gate, not a source-format convention.

---

## 11. Constant latent defect and the origin-decay obstruction are correlation-sensitive

T-P5-193 notes that a nonzero constant box half-width can obstruct exponential decay to the origin through an `O(t)` defect term.

For the zonotope, the exact first-order penalty along a ray `r` is instead

**`h0^T |F_alpha r|`.**

Therefore a nonzero `h0` does **not** by itself obstruct origin decay.

If the constant uncertainty directions lie in the frozen-gradient nullspace,

`F_alpha r = Z^T G_alpha r=0`,

then their first-order energetic effect vanishes exactly.

Conversely, if on a candidate sector

`(G_alpha^T c + F_alpha^T Sigma h0)^T r >0`

for some `r` in the sector, then the mixed decay inequality fails on sufficiently small positive multiples `t r`, because the positive linear term dominates every quadratic damping term as `t downarrow 0`.

Thus correlation can remove a box-induced practical-stability floor when the actual shared error directions are energy-orthogonal, and the checker can detect that cancellation exactly.

---

## 12. A second exact example: nonzero uncertainty with zero Lyapunov supply

Take again

`Z=(1,1)^T`,

constant amplitude `a=1`, and a frozen energy gradient direction

`G e = t(1,-1)`

for some scalar `t`.

Then

`Z^T G e = (1,1) dot t(1,-1)=0`.

Hence every allowed correlated defect satisfies

`rho^T G e=0`.

The exact zonotope supply penalty is zero.

The coordinate box hull, however, allows independent signs and assigns penalty

`|G e|^T(1,1)=2|t|`.

So the same correlation cancellation that rescues facet viability can also rescue a Lyapunov derivative margin. This is exactly the geometry that an axis-aligned outer box discards.

---

## 13. General latent polytope boundary

The zonotope formula exploits the latent cube because its support separates into a sum of absolute values.

A more general fixed latent polytope

`Xi=conv{xi^1,...,xi^R}`

with the same map

`rho=Z diag(a(e)) xi`

also has an exact finite reduction:

`sup_{xi in Xi} w^T Z diag(a(e))xi`

`= max_r w^T Z diag(a(e)) xi^r`.

For facet viability each vertex gives an affine-in-`e` field and can therefore consume the vertexwise T-P5-191 lift. For selector energy each vertex gives one quadratic-plus-linear branch and can consume T-P5-192.

This is mathematically straightforward but may require `R` packets. The centered zonotope/cube deserves its own adapter because the absolute-value support representation avoids enumerating all `2^m` latent vertices and reduces instead to only the sign sectors actually intersecting the state cone.

This review does not claim an optimal representation for arbitrary noncentrally-symmetric source uncertainty.

---

## 14. Exact PASS/FAIL semantics

The trusted-side distinction should be explicit.

### PASS

If the real source residual satisfies

`rho_actual(e) in U_Z(e)`

on the same domain, then every viability or Lyapunov PASS proved against the full zonotope is sound for the real residual, even if the zonotope is only an outer enclosure.

### FAIL

Failure of a full-zonotope robust gate means only that **some** latent zonotope point is bad.

It becomes an actual source obstruction only if either:

1. the source semantics states that every latent `xi in [-1,1]^m` is an allowed instantaneous uncertainty; or
2. the failing latent vector is separately realized/bound by a same-state source witness.

If the true residual occupies a strict correlated subset of the zonotope, a zonotope FAIL can still be enclosure conservatism.

This is the same logical boundary highlighted by T-P5-193 for boxes, one level sharper.

---

## 15. Suggested source packet

A minimal `AffineZonotopeDefectPacket` should contain, under one state/cell key:

- exact/rationalized generator matrix `Z` and declared coordinate/unit ordering;
- exact affine amplitude map `a(e)=H e+h0`;
- proof/evidence that `a(e)>=0` on the consumed domain;
- proof/evidence that the actual residual lies in `Z diag(a(e))[-1,1]^m`;
- semantics tag `outer_enclosure | exact_latent_cube_inclusion`;
- external affine core `A,c` if the viability consumer is used;
- for each selector, the exact `G_alpha,Q_alpha,L_alpha` derivation;
- nonempty latent sign sectors or an exact cover certificate;
- sector generator matrices for the copositivity pullback.

A producer may additionally emit the coordinate box hull `b=|Z|a` as a fallback, but it should not discard `Z` before the consumer has tested whether projected cancellation materially improves the gates.

---

## 16. Suggested Lean theorem statements

The smallest reusable source-independent leaves are:

1. `zonotope_sup_dot`
   - `a>=0 -> sup_{|xi|<=1} w dot (Z * diag(a) * xi) = sum k, a_k * |z_k dot w|`.

2. `zonotope_inf_dot`
   - corresponding negative support identity.

3. `zonotope_support_le_coordinateBoxHull`
   - `|Z^T w| dot a <= |w| dot (|Z|a)`.

4. `polyhedralCone_zonotopeRobustTangent_iff_metzlerLift`
   - with `S=|NZ|`, robust full-zonotope tangency iff
     `NA-SH=Lambda N`, `Lambda` Metzler, `Nc>=Sh0`.

5. `zonotopeMetzlerLift_forwardInvariant`
   - outer-zonotope inclusion plus the same packet implies forward invariance.

6. `selector_zonotopeWorstFrozenSlope`
   - `sup rho^T G e = (He+h0)^T |Z^T G e|`.

7. `selector_zonotopeSignSector_quadraticExpansion`
   - on `Sigma Z^T G e>=0`, expand the exact factor into
     `e^T(H^T Sigma F+F^T Sigma H)e + 2(F^T Sigma h0)^T e` after the derivative factor `2` is included.

8. `selectorZonotopeSignSector_decay_iff_pullbackGates`
   - sector `cone(V)` iff the corresponding copositivity and linear-sign gates hold.

9. `affineAmplitude_nonneg_on_cone_iff_generators`
   - `He+h0>=0` on `cone(V)` iff `h0>=0` and `HV>=0`.

The first three are finite-sum/absolute-value algebra. The sector expansion is `ring`-level. The Metzler theorem should reuse T-P5-191 rather than duplicate Farkas and positive-system infrastructure.

---

## 17. What this closes

Mathematically the new path is

**shared latent correlated residual**

`rho = Z diag(He+h0) xi`, `|xi|<=1`

`-> exact support |Z^T w|^T(He+h0)`

and then, for viability,

`-> S=|NZ|`

`-> exact Metzler cone packet`,

while for Lyapunov decay,

`-> F=Z^T G`

`-> finite latent sign fan`

`-> exact quadratic + linear sector inequality`

`-> existing copositivity pullback`.

This preserves all cancellation carried by shared generator directions and proves that the T-P5-193 independent-box route is the special case `Z=I`.

---

## 18. Remaining open boundaries

This result does **not** close:

1. actual same-key extraction of a generator matrix `Z` from the deployed residual producer;
2. proof that source uncertainty genuinely has shared latent coefficients rather than merely correlated samples;
3. outward-rounded validity of amplitude bounds on the full intended cell/tube;
4. exact `a(e)>=0` on the physical domain;
5. actual selector/latent-sign sector construction and finite cover;
6. fixed copositivity certificates for those real sectors;
7. nonlinear or state-rotating generator directions `Z(e)`; the present theorem fixes `Z` and puts state dependence only in nonnegative amplitudes;
8. noncentrally-symmetric latent uncertainty beyond the finite-vertex observation above;
9. PDE unresolved-mode reduction to a finite latent generator packet;
10. Float64/controller/FD semantics, P8/M4 physical coverage, Lean/kernel compilation, independent verification by 封不觉, admission, or registry promotion.

The most useful next mathematics target, if the source naturally produces state-rotating generators, is a **piecewise-affine generator-direction adapter**: determine when `Z(e)` can still be reduced to finite polyhedral sign cells without turning the selector supply into a genuinely quartic/semi-algebraic checker. Until such a source need appears, the fixed-direction affine-amplitude zonotope is the smallest exact correlation-preserving bridge.