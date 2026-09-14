---
kind: review_result
review_id: review-T-P5-198-quadratic-domain-radial-cap-copositive-reduction-guyuefangyuan-20260910T0028Z
task_id: T-P5-198-QUADRATIC-DOMAIN-RADIAL-CAP-COPOSITIVE-REDUCTION
reviewer: 古月方源
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-10T00:28:00Z
claim_commit: 9129dfb0d15bad5e9190e8a0a54bb69e2c78aec0
inspected_commit: d17e13db6d5aa98623d04a72a59fc27fcd345415
upstream_commits:
  - 86d3e6a59cf11c4d1bd28ffa5a6ab7a66cd20eda  # T-P5-192 selector-cone Lyapunov margin
  - af69121cff7bbb476aea1c6b528936d872f3e015  # T-P5-196 sign-definite quadratic rescue
  - 44f14ed1d40c4edc2a4bac8eb5851ea2dae4c55c  # T-P5-197 weighted radial cubic absorption
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_quadratic_domain_radial_cap_gate; allow_copositive_not_only_psd_rank_one_gate; feed_direct_beta_cap_into_T197; preserve_zero_curvature_recession_failure
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact homogeneous scaling, rank-one quadratic reduction, 2x2 copositivity specialization, rational counterexamples; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-198 — exact radial-cap extraction from a quadratic selector domain

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-197 turns the cubic robust term back into the existing linear-plus-quadratic/copotisivity architecture once the consumed selector sector supplies a bound such as

`beta^T y <= B`.

The remaining domain seam is that a physical/source lane will often already have a quadratic energy or ellipsoidal cap rather than an independently exported weighted `L1` cap.

This review proves an exact homogeneous reduction. Let

`D_rho(P) := { y >= 0 : y^T P y <= rho }`,

where `P=P^T` is copositive, `rho>0`, and let `beta>=0`, `B>=0`. Then

**`beta^T y <= B` for every `y in D_rho(P)`**

if and only if the rank-one loaded matrix

**`M_B := B^2 P - rho beta beta^T`**

is copositive.

This is an iff, not merely a Cauchy/PSD sufficient condition. It remains exact when `P` is singular on the orthant: zero-curvature rays carrying positive `beta` are automatically rejected, while zero-curvature rays invisible to `beta` are harmless.

The checker is entirely rational. A proposed rational `B` requires only construction of `M_B` and the same copositivity machinery already present in the P5 route. No square root, inverse, generalized eigenvalue, ellipsoid optimizer, or new oracle syntax is required.

For a physical homogeneous ellipsoid `e^T W e<=rho` and selector pullback `e=V y`, one may simply take

`P=V^T W V`.

This statement is only a mathematical adapter: this review does not claim that a particular source packet already provides `W,V,rho`, nor that any existing physical domain has been bound to the selector coordinates.

---

## 1. Setup

Fix a finite-dimensional real symmetric matrix `P`, a nonnegative vector `beta`, and scalars

`rho>0`, `B>=0`.

Assume only orthant nonnegativity of the quadratic gauge:

`y>=0 -> y^T P y >=0`.

Equivalently, `P` is copositive. Global PSD is deliberately not assumed.

Define

`q(y)=y^T P y`,

`s(y)=beta^T y`.

Because `beta>=0`, every `y>=0` has `s(y)>=0`.

The desired finite radial cap is

`q(y)<=rho -> s(y)<=B`

for all `y>=0`.

Both `q` and `s` are homogeneous, with degrees two and one respectively. That homogeneity is what makes the exact rank-one reduction possible.

---

## 2. T198-A — exact quadratic-domain/radial-cap equivalence

### Theorem A

Assume

1. `P=P^T`;
2. `P` is copositive;
3. `beta>=0`;
4. `rho>0`;
5. `B>=0`.

Then the following are equivalent:

### (Radial cap)

For every `y>=0`,

`y^T P y <= rho  ->  beta^T y <= B`.

### (Rank-one copositive gate)

For every `y>=0`,

`y^T (B^2 P-rho beta beta^T) y >=0`.

Equivalently,

**`B^2 P-rho beta beta^T` is copositive.**

### Proof: rank-one gate implies radial cap

Fix `y>=0` with `q(y)<=rho`.

Copositivity of `M_B` gives

`0 <= y^T M_B y`

`  = B^2 q(y) - rho s(y)^2`.

Hence

`rho s(y)^2 <= B^2 q(y) <= B^2 rho`.

Because `rho>0`,

`s(y)^2 <= B^2`.

Since both `s(y)` and `B` are nonnegative,

`s(y)<=B`.

No strict positivity of `q(y)` was used.

### Proof: radial cap implies rank-one gate

Fix arbitrary `y>=0`.

Because `P` is copositive, `q(y)>=0`.

#### Case 1: `q(y)=0`

Every scaled point `t y`, `t>=0`, remains in `D_rho(P)`, because

`q(t y)=t^2 q(y)=0<=rho`.

The radial cap therefore gives

`t s(y)<=B`

for every `t>=0`.

A finite `B` forces `s(y)=0`. Consequently

`y^T M_B y=B^2 q(y)-rho s(y)^2=0`.

#### Case 2: `q(y)>0`

Scale the ray until the quadratic boundary is reached. At the boundary one has a positive scalar `t` with

`t^2 q(y)=rho`.

The radial cap yields

`t s(y)<=B`.

Squaring and substituting `t^2=rho/q(y)` gives

`rho s(y)^2 <= B^2 q(y)`.

Thus

`y^T M_B y>=0`.

Since `y>=0` was arbitrary, `M_B` is copositive. QED.

### Trusted-checker note

The proof may describe boundary normalization, but the **certificate does not contain the normalization or any square root**. The trusted input is only rational `P,beta,rho,B`; the gate is the polynomial matrix `B^2P-rho beta beta^T`.

---

## 3. T198-B — zero-curvature recession rays are handled exactly

The singular case is important because `P=V^T W V` may be singular when the cone-generator matrix `V` is redundant, or the physical quadratic form may be semidefinite on a reduced model.

Let

`K_0 := { y>=0 : y^T P y=0 }`.

A finite radial cap can exist only if

**`beta^T y=0` for every `y in K_0`.**

This is not an extra assumption; it is forced by Theorem A and is detected by the same rank-one copositive gate.

Indeed, on `K_0`,

`y^T M_B y = -rho (beta^T y)^2`.

So any zero-curvature ray with positive `beta` immediately gives an exact negative witness for `M_B`.

### Regression 1 — genuine unbounded radial direction

Take

`P=diag(1,0)`, `beta=(0,1)`, `rho=1`.

The domain is

`y_1^2<=1`, `y_2>=0`,

so `y_2` is unbounded. No finite `B` can bound `beta^T y=y_2`.

For every proposed `B`,

`M_B=diag(B^2,-1)`,

and the standard ray `e_2` gives value `-1`.

### Regression 2 — harmless unbounded direction

Take the same

`P=diag(1,0)`, `rho=1`,

but now `beta=(1,0)` and `B=1`.

The domain is still unbounded in `y_2`, but the requested functional ignores that direction. Here

`M_B=0`,

so the exact gate passes and indeed `y_1<=1` on the whole domain.

Therefore a checker must not replace `P` by a blanket positive-definiteness requirement. Semidefinite quadratic domains can still provide exactly the radial cap needed by T-P5-197.

---

## 4. T198-C — PSD is sufficient but can be strictly too strong

A common full-ellipsoid derivation would demand

`M_B=B^2P-rho beta beta^T >=0`

as a PSD matrix. This is sufficient, but on the selector orthant it is not necessary.

### Exact rational regression

Take

`P = [[1,1/2],[1/2,1]]`,

`beta=(1,0)`,

`rho=1`,

`B=1`.

The quadratic domain is

`y_1^2+y_1y_2+y_2^2 <=1`, `y_1,y_2>=0`.

Since every term added to `y_1^2` is nonnegative,

`y_1^2 <= y_1^2+y_1y_2+y_2^2 <=1`,

hence the exact sharp radial cap is

`beta^T y=y_1<=1`.

The rank-one matrix is

`M_B=[[0,1/2],[1/2,1]]`.

For `y>=0`,

`y^T M_B y = y_1 y_2+y_2^2>=0`,

so `M_B` is copositive.

But

`det(M_B)=-1/4<0`,

so `M_B` is indefinite and fails PSD.

Thus replacing the exact orthant gate by PSD would create a false rejection even for a positive-definite physical quadratic form `P`.

This is precisely why the existing copositivity machinery is the correct downstream consumer.

---

## 5. T198-D — direct sharpening of the T-P5-197 absorption coefficient

T-P5-197 uses a weighted cap `w^T y<=R` plus `beta<=kappa w` to infer

`beta^T y<=kappa R`.

When a quadratic domain is already available, the intermediate `w,kappa,R` factorization is unnecessary.

Suppose a fixed-sign projected generator has

`|phi(Vy)| = c^T y+y^T Q y`,

with

`c>=0`, `Q` copositive,

and affine amplitude

`a(Vy)=h0+b^T y>=0`.

Choose any rational majorant

`beta>=0`, `beta>=b`.

If a rational candidate `B>=0` satisfies

**`B^2P-rho beta beta^T` copositive,**

then on the quadratic domain

`beta^T y<=B`.

Repeating the T-P5-197 expansion gives

`a(Vy)|phi(Vy)|`

`<= (h0+beta^T y)(c^T y+y^TQy)`

`= h0 c^T y`

`  + h0 y^TQy`

`  + y^T sym(beta c^T)y`

`  + (beta^T y)(y^TQy)`.

Since `Q` is copositive and `beta^T y<=B`,

`(beta^T y)(y^TQy) <= B y^TQy`.

Therefore

**`a(Vy)|phi(Vy)| <= h0 c^T y + y^T D_B y`,**

with the direct quadratic-domain defect matrix

**`D_B=(h0+B)Q+sym(beta c^T)`.**

This is exactly the T-P5-197 matrix with `kappa R` replaced by a directly certified radial radius `B`.

### Why this can be tighter

The old route first chooses a weighted gauge `w`, then a domination scalar `kappa`, then a cap `R`. Every such packet produces `B=kappa R` and therefore remains valid here.

But the rank-one copositive gate can certify `beta^T y<=B` directly on the actual quadratic sector without separately majorizing `beta` by another gauge. It therefore cannot be worse than a fixed preselected `w,kappa,R` factorization, and can be strictly better when the quadratic domain contains useful cross-coordinate geometry.

---

## 6. T198-E — finite correlated-zonotope family without a common radial weight

For the multi-generator packet of T-P5-194/T-P5-197, generator `k` may use its own majorant `beta_k`.

Assume the same quadratic domain

`y>=0`, `y^T P y<=rho`.

For each generator choose a rational `B_k>=0` and check

**`B_k^2 P-rho beta_k beta_k^T` copositive.**

Then

`beta_k^T y<=B_k`

holds simultaneously for every generator on the same domain, and

`sum_k a_k(Vy)|phi_k(Vy)|`

`<= l_def^T y+y^T M_def y`,

where

`l_def = sum_k h0_k c_k`,

and

**`M_def = sum_k [(h0_k+B_k)Q_k + sym(beta_k c_k^T)]`.**

So a producer no longer needs to find one common positive weight vector `w` that dominates all amplitude-growth directions. A single same-key quadratic domain plus one rational rank-one copositive gate per latent generator is enough.

This can materially reduce the artificial coupling between unrelated generators.

---

## 7. T198-F — 2x2 root-free specialization

When the pulled-back selector sector has two nonnegative coordinates, write

`P=[[p11,p12],[p12,p22]]`,

`beta=(b1,b2)`.

For a proposed `B`, define

`m11=B^2 p11-rho b1^2`,

`m22=B^2 p22-rho b2^2`,

`m12=B^2 p12-rho b1 b2`.

Then Theorem A reduces the exact radial-cap check to the ordinary 2x2 copositivity criterion:

**`m11>=0`, `m22>=0`, and (`m12>=0` or `m12^2<=m11*m22`).**

This is entirely root-free and rational. It is the same binary gate already used elsewhere in the P5 copositivity route.

Therefore a two-ray selector sector can obtain its T-P5-197 radial cap with only additions, multiplications, squares, and order comparisons.

No general optimizer is needed.

---

## 8. T198-G — pullback from a homogeneous physical quadratic domain

Suppose a source/domain lane has already established, under one immutable configuration/domain key,

`e^T W e <= rho`,

and one selector cone is represented by

`e=V y`, `y>=0`.

Then exactly

`e^T W e = y^T (V^T W V)y`.

Hence define

**`P:=V^T W V`.**

If `W` is PSD, then `P` is PSD and therefore copositive. More generally, the mathematical adapter only needs `P` copositive on the selector orthant.

The producer-facing packet can therefore be as small as

```text
selector/domain key,
V,
W,
rho>0,
beta>=0,
B>=0,
P=V^T W V,
Copositive(B^2 P-rho beta beta^T).
```

The last line can itself be discharged by the existing low-dimensional/copositivity lanes, including T-P5-157/T-P5-164/T-P5-168/T-P5-170/T-P5-172 style special cases where applicable.

### Important source boundary

This review does not infer a centered homogeneous ellipsoid from an arbitrary bounded physical set. If the actual domain is shifted, affine, box-like, time-dependent, or only a sampled cloud, the producer must supply the correct containment statement first. One must not silently replace it by `e^T W e<=rho`.

---

## 9. T198-H — optimal radius interpretation

Define the smallest admissible radial radius

`B_* := inf {B>=0 : beta^T y<=B for all y>=0 with y^T P y<=rho}`.

Theorem A gives the equivalent rank-one copositive threshold

`B_* = inf {B>=0 : B^2P-rho beta beta^T is copositive}`.

Thus radial-cap extraction is not a new optimization species. It is a one-parameter rank-one loading problem inside the same copositivity geometry already developed for P5.

When a rational safety radius is enough, there is no reason to represent `B_*` symbolically. Producer may propose rational `B`; checker verifies the rank-one copositive gate. PASS is safe. A failed proposal only means that radius is too small or this branch cannot prove it; it is not by itself a physical-system FAIL unless accompanied by a genuine domain witness with `beta^T y>B`.

---

## 10. Counterexample-guided implementation rules

The mathematics above fixes several dispatcher rules.

1. **Do not require `P>0`.** Semidefinite domains may still control every amplitude-growth direction; Regression 2 is exact.
2. **Do not require `M_B` PSD.** Copositivity is the exact orthant condition; the rational example in section 4 is copositive but indefinite.
3. **Do not ignore a zero-curvature ray.** If `q(y)=0` and `beta^T y>0`, no finite radial cap exists; the same ray is a negative witness for `M_B`.
4. **Do not turn a failed candidate `B` into source FAIL without a witness.** It may only mean that `B` must increase or generic copositivity is unresolved.
5. **Do not mix domain keys.** `P,rho,V,beta,B` must refer to the same consumed selector/domain packet before the bound can feed T-P5-197.
6. **Prefer direct per-generator `B_k` over a forced common `w` when a quadratic domain is already available.** This preserves more domain geometry and removes an unnecessary majorization layer.

---

## 11. Suggested Lean theorem statements

The first leaf can avoid matrices completely:

```text
quadraticDomain_linearCap_of_rankOneNonneg:
  0 < rho -> 0 <= B ->
  (forall y, 0 <=vec y -> 0 <= q y) ->
  (forall y, 0 <=vec y -> rho * (betaDot y)^2 <= B^2 * q y) ->
  forall y, 0 <=vec y -> q y <= rho -> betaDot y <= B.
```

The converse should include the zero-curvature branch explicitly:

```text
rankOneNonneg_of_quadraticDomain_linearCap:
  0 < rho -> 0 <= B -> 0 <=vec beta ->
  (forall y, 0 <=vec y -> 0 <= q y) ->
  (forall y, 0 <=vec y -> q y <= rho -> betaDot y <= B) ->
  forall y, 0 <=vec y -> rho * (betaDot y)^2 <= B^2 * q y.
```

Then package the quadratic form:

```text
quadraticDomain_linearCap_iff_rankOneCopositive:
  Copositive P -> 0 <=vec beta -> 0 < rho -> 0 <= B ->
  ((forall y>=0, y^T P y <= rho -> beta^T y <= B)
    <-> Copositive (B^2 • P - rho • outer beta beta)).
```

The T-P5-197 bridge is then a short scalar leaf:

```text
fixedSignDefect_bound_of_quadraticDomainCap:
  beta^T y <= B -> 0 <= y^T Q y ->
  (h0 + b^T y) * (c^T y + y^T Q y)
    <= h0*c^T y + y^T ((h0+B)Q + sym(beta*c^T)) y
```

under the existing premises `y>=0`, `beta>=0`, `beta>=b`, amplitude nonnegativity, and fixed-sign packet.

For 2x2 consumers, reuse the already-developed binary root-free copositivity theorem instead of creating a new optimizer theorem.

---

## 12. Open obligations / nonclaims

Still open and intentionally outside this mathematical child:

- actual source/domain extraction of a homogeneous quadratic cap;
- same-key binding of `W,V,rho` to a consumed selector sector;
- proof that pulled-back amplitude coefficients/majorants are the actual deployed residual packet;
- construction of rational `B_k` for actual numerical instances;
- higher-dimensional copositivity closure where no existing special branch applies;
- Float64/directed-rounding semantics;
- physical trajectory/path coverage;
- Lean compilation/kernel/axiom audit;
- independent verifier review by 封不觉;
- admission, registry mutation, or parent P5 closure.

The precise next source-facing question is now smaller than T-P5-197's original weighted-cap request: **does an already certified selector/domain quadratic form pull back to a same-key rational `P,rho`?** If yes, every affine-amplitude majorant `beta_k` can obtain a direct radial radius through one rank-one copositive gate, with no common `w` required.

---

## 13. Final classification

`CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending`.

The mathematical domain-to-radial bridge is exact and root-free at the certificate level. It closes the abstract bounded-domain seam between an existing quadratic selector/domain certificate and T-P5-197's cubic absorption, while preserving fail-closed behavior about actual source/domain semantics.
