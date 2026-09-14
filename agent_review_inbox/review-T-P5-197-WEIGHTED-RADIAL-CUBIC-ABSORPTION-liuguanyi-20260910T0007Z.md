---
kind: review_result
review_id: review-T-P5-197-weighted-radial-cubic-absorption-liuguanyi-20260910T0007Z
task_id: T-P5-197-WEIGHTED-RADIAL-CUBIC-ABSORPTION
reviewer: 柳冠一
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-10T00:07:00Z
claim_commit: e0c1fdad685614d0c3c1fd33e5af86aae86ec5ec
inspected_commit: 904dd5a6a2ce72076c8b83c240b7e11de9dea2df
upstream_commits:
  - 86d3e6a59cf11c4d1bd28ffa5a6ab7a66cd20eda  # T-P5-192 selector-cone Lyapunov margin
  - f6a493131c273ba0739ede6c2f7a986b71660ae1  # T-P5-194 correlated-zonotope defect adapter
  - 85a96adf98569071e07bb7b8b2ed1f098d492d35  # T-P5-195 projected-skew affine-generator gate
  - af69121cff7bbb476aea1c6b528936d872f3e015  # T-P5-196 sign-definite quadratic rescue
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_weighted_radial_cap_adapter; add_cubic_to_quadratic_absorption; add_multi_generator_defect_packet; route_zero_weight_failure_to_domain_refinement
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact cone pullback, weighted gauge domination, homogeneous degree bookkeeping, symmetric outer-product identity, rational examples; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-197 — weighted radial cap bridge that absorbs the T-P5-196 cubic defect back into a quadratic copositivity packet

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-196 proves that a fixed-sign projected generator

`phi(e)=ell^T e + e^T S e`

can be handled exactly on a selector cone, but an affine nonnegative amplitude

`a(e)=h0+h^T e`

generically creates a positive cubic term. On an unbounded cone that cubic term is a genuine obstruction to any closure whose remaining negative budget is only quadratic.

This review closes the smallest bounded-domain seam: if the *actual consumed selector sector* carries an exact positive weighted radial cap, the cubic term can be absorbed into an explicit quadratic form using only rational arithmetic and the existing copositivity machinery.

After pulling the selector cone back as

`e = V y`, `y>=0`,

write the fixed-sign scalar as

`|phi(Vy)| = c^T y + y^T Q y`,

with

`c>=0` entrywise and `Q` copositive.

Let the amplitude be

`a(Vy)=h0+b^T y >=0`.

Choose any componentwise nonnegative rational majorant `beta>=b`, and assume the consumed sector has a certified weighted cap

`w^T y <= R`,

with `w>=0`, `R>=0`, and every coordinate carrying positive amplitude growth also carrying positive radial weight.

Define the least scalar satisfying `beta<=kappa w` componentwise:

`kappa_* = max_{j:w_j>0} beta_j/w_j`,

provided `w_j=0 -> beta_j=0`.

Then on the capped sector,

**`beta^T y <= kappa_* R`.**

Consequently the entire fixed-sign affine-amplitude defect satisfies the explicit degree-two bound

**`a(Vy)|phi(Vy)| <= h0 c^T y + y^T D y`,**

where

**`D = (h0+kappa_* R) Q + sym(beta c^T)`**

and

`sym(beta c^T) = (beta c^T + c beta^T)/2`.

Thus the bounded-sector fallback promised but not closed by T-P5-196 returns *exactly* to the T-P5-192 shape: one linear term plus one symmetric quadratic form, hence an entrywise linear sign gate plus one copositivity test after combining with the nominal Lyapunov budget.

The bridge is exact-rational when the source packet is rational. No norm, inverse, square root, eigenvalue, pseudoinverse, or semialgebraic cubic checker is required.

A missing radial cap is not a source-system FAIL. It means only that this quadratic absorption route is unavailable; the consumer must retain the cubic/semialgebraic branch or obtain a stronger physical domain certificate.

---

## 1. Setup inherited from T-P5-196

Fix one selector cone

`C = cone(V) = {Vy : y>=0}`.

For one state-dependent zonotope generator, T-P5-195/T-P5-196 reduce the projected scalar to

`phi(e)=ell^T e + e^T S e`, `S=S^T`.

Assume T-P5-196 has already certified a fixed sign `sigma in {+1,-1}` on the cone. Define

`c := sigma V^T ell`,

`Q := sigma V^T S V`.

Then the T-P5-196 gate gives

`c>=0` entrywise,

and

`Q` copositive,

so for every `y>=0`,

`|phi(Vy)| = sigma phi(Vy) = c^T y + y^T Q y >=0`.

The affine amplitude pulls back to

`a(Vy)=h0+b^T y`.

The physical robust-support term is therefore

`F(y) := (h0+b^T y)(c^T y+y^T Q y)`.

On an unbounded cone, the last product contains the T-P5-196 cubic obstruction

`(b^T y)(y^T Q y)`.

The question is whether a bounded *source/domain* premise can absorb this term without destroying the existing quadratic checker architecture.

---

## 2. T197-A — exact weighted gauge domination on the nonnegative cone

Let

`beta>=0`, `w>=0`.

We seek a finite scalar `kappa>=0` such that

`beta^T y <= kappa w^T y`

for every `y>=0`.

### Theorem A1 — componentwise iff

The following are equivalent:

1. `beta^T y <= kappa w^T y` for every `y>=0`;
2. `beta_j <= kappa w_j` for every coordinate `j`.

### Proof

`(2)->(1)` follows by multiplying each coordinate inequality by `y_j>=0` and summing.

For `(1)->(2)`, choose `y=e_j`, the `j`-th standard basis vector. Then

`beta_j <= kappa w_j`.

No duality theorem is needed.

### Corollary A2 — existence of a finite domination constant

A finite `kappa` exists iff

**`w_j=0 -> beta_j=0`.**

If this support condition holds and `beta` is not identically zero, the least possible constant is

**`kappa_* = max_{j:w_j>0} beta_j/w_j`.**

If `beta=0`, take `kappa_*=0`.

### Proof of sharpness

Every admissible `kappa` must satisfy `kappa>=beta_j/w_j` for every `w_j>0` by the standard-basis test. Hence `kappa>=kappa_*`.

Conversely, the definition of `kappa_*` gives `beta_j<=kappa_* w_j` for every positive-weight coordinate, while zero-weight coordinates have `beta_j=0`. Theorem A1 then proves the global inequality.

Thus `kappa_*` is not a heuristic norm constant. It is the exact optimal scalar for the weighted gauge comparison on the nonnegative cone.

### Exact-rational property

If `beta,w` are rational, `kappa_*` is the maximum of finitely many rational ratios and is therefore rational. A checker can avoid division entirely by accepting a rational candidate `kappa` and verifying

`beta_j <= kappa w_j`

entrywise. Producer-side minimization is optional.

---

## 3. T197-B — bounded weighted sector turns the cubic term into a quadratic term

Assume the actual consumed sector is

`D_R := {y>=0 : w^T y <= R}`

with `R>=0`, and let `kappa` satisfy

`beta<=kappa w`.

Then for every `y in D_R`,

`beta^T y <= kappa w^T y <= kappa R`.

Because `Q` is copositive,

`y^T Q y >=0`.

Multiplying the scalar bound by this nonnegative quadratic gives

**`(beta^T y)(y^T Q y) <= kappa R y^T Q y`.**

This is the required cubic-to-quadratic absorption.

### Important semantic point

The proof uses both premises:

- `w^T y<=R`, a physical/domain cap;
- `Q` copositive, inherited from the fixed-sign gate.

Without the first, the coefficient is unbounded. Without the second, multiplying an upper bound by `y^TQy` could reverse the inequality.

So the T-P5-196 sign certificate is not merely about removing an absolute value; it is also what makes this one-line degree reduction sound.

---

## 4. T197-C — arbitrary signed affine slope via a nonnegative majorant

T-P5-196 considered amplitudes nonnegative on the consumed region. The coefficient vector `b` itself need not be componentwise nonnegative if the region is bounded or if some directions decrease amplitude.

For an upper bound, there is no need to require `b>=0`.

Choose any

`beta>=0`

such that

`b<=beta`

entrywise.

Then for `y>=0`,

`b^T y <= beta^T y`.

Since the amplitude and fixed-sign scalar are both nonnegative,

`h0+b^T y >=0`,

`c^T y+y^TQy >=0`,

we have

`F(y)`

`=(h0+b^T y)(c^T y+y^TQy)`

`<= (h0+beta^T y)(c^T y+y^TQy)`.

A canonical exact-rational choice is the componentwise positive part

`beta_j=max(b_j,0)`,

but the trusted interface does not need a `max` primitive: producer may submit any rational `beta` and checker verifies only

`beta>=0`, `beta>=b`.

This preserves sign-sensitive source information better than replacing `b` by a scalar norm.

---

## 5. T197-D — explicit linear-plus-quadratic defect matrix

Expand the majorized defect:

`(h0+beta^T y)(c^T y+y^TQy)`

`= h0 c^T y`

`  + h0 y^TQy`

`  + (beta^T y)(c^T y)`

`  + (beta^T y)(y^TQy)`.

The mixed linear-linear product is exactly quadratic:

`(beta^T y)(c^T y)`

`= y^T sym(beta c^T) y`,

where

`sym(beta c^T)=(beta c^T+c beta^T)/2`.

By T197-B, on `D_R`,

`(beta^T y)(y^TQy) <= kappa R y^TQy`.

Therefore

**`F(y) <= h0 c^T y + y^T D y`**

with

**`D=(h0+kappa R)Q + sym(beta c^T)`.**

This is the main bridge theorem.

### No hidden definiteness assumption on `D`

`D` need not be PSD. The theorem is an *upper bound identity plus copositive multiplication step*. What matters to the downstream Lyapunov gate is the sign of the **combined nominal-plus-defect quadratic form** on `y>=0`.

The downstream checker should therefore not separately demand `D>=0` or PSD. It should add `D` to the nominal quadratic coefficient and invoke the ordinary copositivity condition required by T-P5-192.

---

## 6. T197-E — exact return to the T-P5-192 checker shape

Suppose the nominal selector-wise Lyapunov calculation has already produced an upper bound

`dotL_nom(y) <= l0^T y + y^T M0 y`

on the same consumed sector.

Adding the robust generator defect and applying T197-D yields

`dotL_rob(y)`

`<= (l0+h0 c)^T y`

` + y^T [M0 + (h0+kappa R)Q + sym(beta c^T)] y`.

Define

`l_tot := l0+h0 c`,

`M_tot := M0+(h0+kappa R)Q+sym(beta c^T)`.

Then the completely familiar sufficient gate is

**`l_tot <=0` entrywise**

and

**`-M_tot` copositive.**

Indeed, for every `y>=0`,

`l_tot^T y<=0`

and

`y^T M_tot y<=0`.

Hence `dotL_rob(y)<=0` on the capped sector.

The same statement applies when `dotL_nom` already includes a target decay term such as `2 gamma L`; all such nominal terms are simply part of `l0,M0`.

### Architecture consequence

The bounded-domain fallback does **not** require a new cubic trusted checker. It requires only one additional typed premise

`w^T y<=R`

plus the rational inequalities

`beta>=b`, `beta>=0`, `beta<=kappa w`.

After that, the old linear/copotisivity machinery is reused unchanged.

---

## 7. T197-F — finite family / correlated-zonotope summation theorem

T-P5-194 supplies a finite sum of latent-generator support contributions. Apply the preceding theorem generator by generator.

For generator `k`, assume after its fixed-sign gate

`|phi_k(Vy)| = c_k^T y+y^T Q_k y`,

with

`c_k>=0`, `Q_k` copositive,

and amplitude

`a_k(Vy)=h0_k+b_k^T y>=0`.

Choose `beta_k>=0`, `beta_k>=b_k`, and a scalar `kappa_k` satisfying

`beta_k<=kappa_k w`.

The *same* domain cap

`w^T y<=R`

then gives

`sum_k a_k(Vy)|phi_k(Vy)|`

`<= l_def^T y + y^T M_def y`,

where

**`l_def = sum_k h0_k c_k`,**

and

**`M_def = sum_k [(h0_k+kappa_k R)Q_k + sym(beta_k c_k^T)]`.**

Thus a correlation-preserving zonotope packet with finitely many state-rotating generators can still collapse to one quadratic selector packet whenever each projected scalar has fixed sign and the physical selector sector has one common weighted radial cap.

Nothing in this summation step assumes independence of latent generators; correlation has already been handled exactly by the zonotope support representation upstream.

---

## 8. T197-G — zero-weight obstruction is a domain-interface obstruction

The support condition

`w_j=0 -> beta_j=0`

is mathematically necessary for any finite scalar absorption constant.

### Exact counterexample

Take two nonnegative coordinates and

`w=(1,0)`,

`beta=(0,1)`.

Then the alleged capped sector

`w^T y=y_1<=R`

places no bound on `y_2`.

For `y=t e_2`,

`beta^T y=t`,

while

`w^T y=0`.

So no finite `kappa` can satisfy

`beta^T y<=kappa w^T y`.

If also `Q_22>0`, the cubic term grows like `t^3` along this uncapped ray and the T-P5-196 obstruction survives unchanged.

### Routing meaning

This is **not** a proof that the physical PDE/ODE system is unstable or that no Lyapunov certificate exists.

It proves only that the proposed radial descriptor fails to control an amplitude-growing direction. Correct responses are:

1. strengthen the domain cap by assigning positive weight to that direction;
2. prove `beta_j=0` from source on the uncapped direction;
3. retain the cubic/semialgebraic checker for that branch;
4. use a different bounded physical coordinate chart.

A dispatcher must not turn `w_j=0, beta_j>0` into a source-level mathematical FAIL.

---

## 9. T197-H — why an actual cap is indispensable

A one-dimensional exact example isolates the degree issue.

Take

`y>=0`,

`h0=1`, `b=1`,

`c=1`, `Q=[1]`.

Then

`F(y)=(1+y)(y+y^2)=y+2y^2+y^3`.

No fixed quadratic polynomial `A y^2+B y` can dominate `F(y)` on the whole ray, because the ratio `F(y)/y^2` grows like `y`.

On the capped interval `0<=y<=R`, however,

`y^3<=R y^2`,

and T197-D gives exactly

`F(y)<=y+(2+R)y^2`.

So the bounded-domain premise changes the degree obstruction in a mathematically essential way; it is not bookkeeping.

---

## 10. T197-I — exact rational two-dimensional regression with sharp `kappa`

Take

`w=(2,1)`, `R=3`,

`beta=(1,2)`,

`c=(1,3)`,

`h0=1/2`,

and

`Q=[[1,-1/2],[-1/2,1]]`.

`Q` is PSD and hence copositive.

The sharp gauge ratio is

`kappa_*=max((1)/(2),(2)/(1))=2`.

Thus on

`2 y_1+y_2<=3`,

`beta^T y=y_1+2y_2<=6`.

The defect matrix is

`D=(1/2+2*3)Q + sym(beta c^T)`

`=(13/2)Q + [[1,5/2],[5/2,6]]`

`=[[15/2,-3/4],[-3/4,25/2]]`.

The linear term is

`h0 c=(1/2,3/2)`.

So the checker-ready bound is

`F(y) <= (1/2)y_1+(3/2)y_2`

`       + (15/2)y_1^2-(3/2)y_1y_2+(25/2)y_2^2`.

The radial scalar is genuinely sharp for this packet: on `y=3 e_2`,

`w^T y=3`,

`beta^T y=6=kappa_* R`,

and

`y^TQy=9>0`,

so the cubic absorption step itself is attained with equality.

All numbers are rational; there is no hidden square root.

---

## 11. Minimal theorem statements for formalization

The following leaves are enough for a later Lean lane.

### T197-1 `weightedConeLinearDom_iff_componentwise`

For finite vectors `beta,w` and scalar `kappa`, with `beta,w>=0`:

`(forall y>=0, beta·y <= kappa*(w·y))`

iff

`beta <= kappa • w` entrywise.

### T197-2 `weightedConeLinearDom_minRatio`

Under `w_j=0 -> beta_j=0`, the least nonnegative domination scalar is

`max_{w_j>0} beta_j/w_j`.

For a checker-facing theorem, this leaf may be omitted in favor of a supplied `kappa` plus the entrywise inequality.

### T197-3 `radialCap_cubicAbsorb`

If

`y>=0`, `w·y<=R`, `beta<=kappa w`, and `Q` is copositive,

then

`(beta·y)*(y^TQy) <= kappa*R*(y^TQy)`.

### T197-4 `fixedSignAffineAmplitude_radialQuadraticUpper`

If

`a(y)=h0+b·y>=0`,

`b<=beta`, `beta>=0`,

`c>=0`, `Q` copositive,

`w·y<=R`, `beta<=kappa w`,

then

`a(y)*(c·y+y^TQy)`

`<= h0(c·y)+y^T[(h0+kappa R)Q+sym(beta c^T)]y`.

### T197-5 `finiteGenerator_radialDefectSum`

Sum T197-4 over a finite latent-generator index set and collect the linear/quadratic coefficients exactly.

### T197-6 `radialDefect_to_copositiveLyapunovGate`

If the nominal upper bound is `l0·y+y^TM0y`, define `l_tot,M_tot` as in Section 6. If `l_tot<=0` entrywise and `-M_tot` is copositive, the robust derivative is nonpositive on the capped sector.

These are elementary finite-dimensional real lemmas; none requires spectral theory.

---

## 12. Suggested typed interface

A consumer-side packet should keep the following fields separate:

- `selector_generators : V`
- `fixed_sign : sigma`
- `projected_linear : c`
- `projected_quadratic : Q`
- `amplitude_offset : h0`
- `amplitude_slope : b`
- `amplitude_majorant : beta`
- `radial_weights : w`
- `radial_cap : R`
- `radial_multiplier : kappa`
- `majorant_nonnegative : beta>=0`
- `majorant_dominates_source_slope : beta>=b`
- `weighted_domination : beta<=kappa w`
- `sector_domain_binding : w^T y<=R`
- `linear_defect : h0 c`
- `quadratic_defect : (h0+kappa R)Q+sym(beta c^T)`.

The crucial separation is between

**algebraic packet** `beta<=kappa w`

and

**physical/domain packet** `w^T y<=R`.

The first can be checked from rational coefficients. The second must come from an actual same-cell/source/domain theorem. Storing them as one opaque `bounded=true` flag would erase the mathematical boundary T-P5-196 exposed.

---

## 13. Boundaries that remain OPEN

This review does **not** prove:

1. that the actual P5 selector sector has a weighted radial cap;
2. that a proposed `V,w,R` is bound to the same physical cell/tube as the source remainder;
3. that the actual affine amplitude is nonnegative on that sector;
4. that `beta` majorizes the same-key source slope `b` under Float64/interval semantics;
5. that every state-rotating generator satisfies the T-P5-196 fixed-sign gate;
6. that the resulting combined `-M_tot` is copositive;
7. global selector coverage or trajectory/path coverage;
8. PDE/ODE graph binding, P8/M4 propagation, or terminal-transfer obligations;
9. Lean/kernel compilation;
10. independent verification by 封不觉;
11. admission or registry eligibility.

All remain OPEN.

---

## 14. Recommended next bridge

The next mathematical question is now very narrow.

If the real physical cell/tube is already described by a polytope or ellipsoid in *state coordinates* rather than selector coefficients `y`, prove an exact transport theorem producing

`w^T y<=R`

from that actual domain description without introducing a false inverse of a non-injective generator matrix `V`.

For a polyhedral domain this is a linear-program dual certificate. For an ellipsoidal domain it requires a separate quadratic-support bound and should not be silently identified with the polyhedral radial packet.

That source-to-selector-domain transport is a better next target than a new cubic solver, because once it is available the present theorem routes the T-P5-196 bounded branch back into the existing P5 copositivity stack.