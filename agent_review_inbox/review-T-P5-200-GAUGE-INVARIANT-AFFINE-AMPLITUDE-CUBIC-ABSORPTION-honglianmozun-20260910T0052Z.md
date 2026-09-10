---
kind: review_result
review_id: review-T-P5-200-gauge-invariant-affine-amplitude-cubic-absorption-honglianmozun-20260910T0052Z
task_id: T-P5-200-GAUGE-INVARIANT-AFFINE-AMPLITUDE-CUBIC-ABSORPTION
reviewer: 红莲魔尊
agent: 红莲魔尊
source_agent: 红莲魔尊
created_at: 2026-09-10T00:52:00Z
claim_commit: 9186d229f5ec4f93db846c3ae98b290601599adc
inspected_commit: 99b9e7adf09e1aa5b8e454d32f54066792538ae2
upstream_commits:
  - af69121cff7bbb476aea1c6b528936d872f3e015  # T-P5-196 fixed-sign quadratic rescue
  - 44f14ed1d40c4edc2a4bac8eb5851ea2dae4c55c  # T-P5-197 weighted radial cubic absorption
  - 04872637e1d211b2e91bb7be8bce2894ba043624  # T-P5-199 polyhedral selector LP-dual transport
parallel_nonoverlap:
  - 9129dfb0d15bad5e9190e8a0a54bb69e2c78aec0  # T-P5-198 quadratic-domain radial-cap claim by 古月方源
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_exact_signed_amplitude_support_branch; preserve_physical_selector_gauge; add_state_space_dual_cap; route_majorant_gauge_failure_to_exact_pullback_before_semialgebraic_fallback
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact algebraic energy identity, selector-kernel descent, finite-dimensional LP dual support packet, rational counterexamples; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-200 — gauge-invariant affine-amplitude support absorbs the cubic defect without a nonnegative selector majorant

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-196 isolates the genuine degree obstruction produced by an affine state-dependent amplitude multiplying a fixed-sign linear-plus-quadratic projected scalar. T-P5-197 closes that obstruction on a bounded selector sector by replacing the signed amplitude slope with a nonnegative coefficient majorant `beta`, then bounding `beta^T y`. T-P5-199 shows why that coefficient-space route can fail even on a compact physical cell: a non-injective selector map may admit `r>=0`, `V r=0`, while a positive majorant still grows along `y+t r`.

This review closes a strictly narrower but important energy branch that avoids that representation artefact.

If the amplitude is a genuine physical affine scalar

`a(e)=h0+h^T e`,

and `e=V y`, define its **exact signed pullback**

`b := V^T h`.

Do **not** replace `b` by a nonnegative `beta` unless needed.

For the fixed-sign projected scalar write

`|phi(Vy)| = c^T y + y^T Q y`,

with the T-P5-196 sign-compatible decomposition

`c>=0`,

`Q` copositive.

Assume on the actually consumed cell

`b^T y <= B`.

Then the full affine-amplitude defect satisfies the exact-gap upper bound

**`(h0+b^T y)(c^T y+y^T Q y)`**

**`<= h0 c^T y + y^T[(h0+B)Q + sym(b c^T)]y`,**

and the difference between the right and left sides is exactly

**`(B-b^T y) y^T Q y >=0`.**

No sign restriction on the coordinates of `b` is needed.

The key structural point is that `b=V^T h` annihilates every selector gauge direction `r in ker(V)`, not merely every nonnegative one. The whole resulting linear/quadratic defect packet also descends from state space and annihilates `ker(V)`. Thus an unbounded coefficient fiber can coexist with a perfectly finite physical amplitude support bound.

This child therefore provides a fail-closed routing improvement:

> before declaring T-P5-197/T-P5-199 coefficient-majorant absorption unavailable because of a selector-gauge recession direction, test whether the generator amplitude has an exact physical affine slope. If it does, use the signed exact pullback and support `h^T e` directly.

No actual P5 source identity, cell/tube coverage, generator packet, Float64 enclosure, controller/PDE/ODE semantics, Lean/kernel proof, independent verification, admission, or registry promotion is claimed.

---

## 1. Setup inherited from T-P5-196

Fix one consumed selector sector with

`e = V y`,

`y>=0`.

Let the projected scalar be

`phi(e)=ell^T e + e^T S e`,

with `S=S^T`.

Assume a fixed sign `sigma in {+1,-1}` has already been certified in the stronger T-P5-196 decomposition sense:

`c := sigma V^T ell >=0` entrywise,

`Q := sigma V^T S V` is copositive.

Hence for every selector state consumed by the branch,

`|phi(Vy)| = sigma phi(Vy) = c^T y + y^TQy`,

with

`c^T y>=0`,

`y^TQy>=0`.

Now let one correlated-zonotope generator amplitude be the genuine physical affine scalar

`a(e)=h0+h^T e`.

Its exact selector pullback is

`a(Vy)=h0+b^T y`,

where

**`b=V^T h`.**

The amplitude is assumed nonnegative on the consumed physical domain, as required by the upstream support interpretation.

Unlike T-P5-197, this child does not impose `b>=0` and does not replace `b` by a nonnegative coordinatewise majorant.

---

## 2. T200-A — exact signed-slope cubic absorption identity

Assume on the consumed set `F`

`b^T y <= B`.

Define

`q2(y):=y^TQy`.

Because `Q` is copositive and `y>=0`,

`q2(y)>=0`.

Expand the exact robust defect:

`Frob(y)`

`=(h0+b^T y)(c^T y+q2(y))`

`=h0 c^T y`

` + h0 q2(y)`

` + (b^T y)(c^T y)`

` + (b^T y) q2(y)`.

The linear-linear product remains an exact signed quadratic form:

`(b^T y)(c^T y)=y^T sym(b c^T)y`,

where

`sym(b c^T):=(b c^T+c b^T)/2`.

Because `b^T y<=B` and `q2(y)>=0`,

`(b^T y)q2(y) <= B q2(y)`.

Therefore

**`Frob(y) <= h0 c^T y + y^T D_B y`,**

with

**`D_B := (h0+B)Q + sym(b c^T)`.**

No componentwise sign assumption on `b` appears anywhere in the proof.

### Exact remainder identity

The difference is not merely known to be nonnegative. It is exactly

**`[h0 c^T y+y^T D_B y] - Frob(y)`**

**`= (B-b^T y)y^TQy`.**

Thus the only debit introduced by the support cap is the product of:

1. the scalar support slack `B-b^T y`, and
2. the nonnegative quadratic projected energy `y^TQy`.

This is the main Lyapunov identity of the child.

### Contact/sharpness information

The bound is exact at every consumed state where either

`b^T y=B`,

or

`y^TQy=0`.

In particular, if a support maximizer satisfies `b^T y=B` and the quadratic projected energy is positive there, the scalar coefficient `B` cannot be decreased in this packet without breaking the bound at that same state.

---

## 3. T200-B — state-space form of the same energy identity

The preceding theorem is not intrinsically a selector-coordinate result.

Define the sign-compatible quadratic part in physical coordinates

`q2_phys(e):=sigma e^T S e`.

On the consumed selector sector, T-P5-196 gives

`q2_phys(Vy)=y^TQy>=0`.

Assume the physical affine slope satisfies

`h^T e<=B`

on the consumed physical domain.

Then

`a(e)|phi(e)|`

`=(h0+h^T e) sigma(ell^T e+e^T S e)`.

Expanding and bounding only the cubic term gives

**`a(e)|phi(e)|`**

**`<= h0 sigma ell^T e`**

**` + e^T sigma[(h0+B)S + sym(h ell^T)]e`.**

The exact gap is

**`(B-h^T e) sigma e^T S e`.**

This state-space identity explains why the selector-gauge obstruction is artificial for a genuine physical amplitude: the entire upper envelope is already a physical linear-plus-quadratic function before it is pulled back through `V`.

---

## 4. T200-C — the defect packet descends through `V` and annihilates selector gauge

Using

`b=V^T h`,

`c=sigma V^T ell`,

`Q=sigma V^T S V`,

we have

`sym(b c^T)`

`= sigma V^T sym(h ell^T) V`.

Hence

**`D_B = V^T D_phys V`,**

where

**`D_phys := sigma[(h0+B)S + sym(h ell^T)]`.**

Likewise

`h0 c = V^T(h0 sigma ell)`.

Therefore for every `r in ker(V)`,

**`c^T r=0`,**

**`Q r=0`,**

**`D_B r=0`,**

and

**`b^T r=0`.**

The complete defect upper packet is constant on every selector fiber

`{y+r : V r=0}`

whenever both representatives remain in the consumed coordinate domain.

This is stronger than merely saying that nonnegative gauge directions do not hurt the support LP. The matrix-level Lyapunov debit itself carries the physical quotient structure.

### Structural fingerprint

**physical affine amplitude -> exact signed pullback -> kernel-annihilating support functional -> quadratic projected-energy cap -> gauge-invariant Lyapunov debit.**

---

## 5. T200-D — why T-P5-199 gauge recession disappears for the exact physical slope

T-P5-199 considers a pulled-back polyhedral domain

`F={y>=0 : A V y<=d}`.

Its recession cone is

`rec(F)={r>=0 : A V r<=0}`.

If the physical state polytope

`P={e : A e<=d}`

is bounded and `F` is nonempty, T-P5-199 proves

`rec(F)={r>=0 : V r=0}`.

For the exact physical slope

`b=V^T h`,

every such recession direction obeys

**`b^T r=h^T V r=0`.**

Hence the exact objective `b^T y=h^T e` never grows along a pure selector gauge ray.

So even if `F` is unbounded as a coefficient set, the exact physical support

`sup_{y in F} b^T y`

is finite whenever the physical state domain is bounded.

This directly separates two notions:

- **coefficient radial boundedness**, which can fail because a selector representation is redundant;
- **physical affine support boundedness**, which is invariant under that redundancy.

Only the second is needed by T200-A.

---

## 6. T200-E — exact polyhedral certificate for a signed physical slope

The elementary T-P5-199 dual inequality does not require the objective coefficients to be nonnegative.

Let

`Bmat:=A V`,

`b:=V^T h`.

Suppose a rational packet provides `lambda` with

`lambda>=0`,

**`Bmat^T lambda >= b` entrywise,**

and

`d^T lambda<=B`.

Then for every `y>=0` with `Bmat y<=d`,

`b^T y <= lambda^T Bmat y <= lambda^T d <= B`.

Thus T200-A can consume a signed `b` directly.

No `beta>=0`, no radial `w`, and no selector inverse are needed.

### Full-state certificate with no selector matrix in the trusted packet

If one wants a support bound on the whole physical polytope `P={e:Ae<=d}`, a still cleaner sufficient certificate is

`lambda>=0`,

**`A^T lambda=h`,**

`d^T lambda<=B`.

Then

`h^T e=lambda^T A e<=lambda^T d<=B`

for every `e in P`.

Under the standard nonempty finite-dimensional LP hypothesis, this is also the ordinary dual characterization of a finite proposed support bound on a free state variable `e`.

### Cone-restricted physical certificate

If only `P intersect cone(V)` matters, equality may be relaxed to the cone dual condition

**`V^T(A^T lambda-h)>=0`.**

This is exactly the signed-objective pullback above.

---

## 7. T200-F — exact signed packet is never forced to pay the nonnegative-majorant gauge tax

T-P5-197 introduces `beta>=0`, `beta>=b` so that `beta^T y` is a nonnegative amplitude-growth majorant.

When `b` has mixed signs, this replacement may destroy the physical quotient structure:

`b^T r=0`

for `V r=0`,

while

`beta^T r>0`

can hold on the same gauge direction.

T200-A avoids that replacement completely.

If both routes are available with sharp support constants

`B_b := sup_F b^T y`,

`B_beta := sup_F beta^T y`,

then because `beta>=b` and `y>=0`,

`B_beta>=B_b`.

At any `y in F`, the difference between the T-P5-197/T-P5-199 majorant quadratic envelope and the exact-signed T200 envelope evaluates to

`(B_beta-B_b)y^TQy`

`+ ((beta-b)^T y)(c^T y)`,

provided the same `h0,c,Q` are used.

Under `Q` copositive, `c>=0`, `beta-b>=0`, this difference is nonnegative.

Thus, whenever both sharp supports exist, preserving the exact signed physical slope is pointwise no worse and can be strictly better.

This is not a reason to delete the majorant route: `beta` remains necessary when the upstream amplitude is not available as one exact physical affine scalar or when only a coordinatewise envelope is source-bound.

---

## 8. T200-G — comparison with a crude scalar amplitude cap

A still simpler rescue would bound the whole amplitude by

`0<=a(e)<=Amax`

and use

`a(e)|phi(e)|<=Amax |phi(e)|`.

If `Amax=h0+B`, this gives in selector coordinates

`(h0+B)c^T y + (h0+B)y^TQy`.

T200-A instead keeps the exact linear-linear interaction and gives

`h0 c^T y + y^T[(h0+B)Q+sym(b c^T)]y`.

Their difference is

**`(B-b^T y)c^T y>=0`.**

Therefore under the T-P5-196 gate `c>=0`, the signed-slope packet is always at least as tight as the crude whole-amplitude cap, while retaining exactly the same quadratic checker degree.

So the correct order is:

1. exact signed physical slope support if available;
2. otherwise nonnegative majorant/radial support;
3. otherwise crude amplitude cap if source-bound;
4. otherwise retain the cubic/semialgebraic branch.

---

## 9. T200-H — multi-generator correlated-zonotope sum

For each finite latent generator `k`, suppose

`a_k(e)=h0_k+h_k^T e>=0`,

and after the fixed-sign gate

`|phi_k(Vy)|=c_k^T y+y^TQ_k y`,

with

`c_k>=0`, `Q_k` copositive.

Let

`b_k=V^T h_k`.

If the same consumed cell provides exact physical support bounds

`b_k^T y<=B_k`,

then generatorwise T200-A gives

`sum_k a_k(Vy)|phi_k(Vy)|`

`<= l_def^T y + y^T M_def y`,

where

**`l_def=sum_k h0_k c_k`,**

and

**`M_def=sum_k [(h0_k+B_k)Q_k + sym(b_k c_k^T)]`.**

Every summand descends through `V`; hence

`M_def r=0`

and

`l_def^T r=0`

for every `r in ker(V)`.

The correlation-preserving support semantics from T-P5-194 remain untouched; this theorem acts only after each projected scalar and affine amplitude have already been source-bound.

---

## 10. T200-I — exact rational counterexample separating physical support from coefficient-majorant support

Take one physical state `e` and two nonnegative selector coefficients

`y1,y2>=0`.

Let

**`V=[1,-1]`,**

so

`e=y1-y2`.

Use the compact physical cell

`-1<=e<=1`,

written as

`A=[[1],[-1]]`,

`d=(1,1)`.

Choose the genuine affine amplitude

**`a(e)=2+e`.**

Thus

`h0=2`, `h=1`,

and the exact signed selector slope is

**`b=V^T h=(1,-1)`.**

Take the fixed-sign projected scalar

**`phi(e)=e^2`.**

Then `sigma=+1`, `ell=0`, `S=[1]`,

`c=0`,

and

`Q=V^T V=[[1,-1],[-1,1]]`,

which is PSD and therefore copositive.

### Exact physical support

On the cell,

`b^T y=e<=1`,

so take

`B=1`.

T200-A yields

`(2+e)e^2<=3e^2`.

Equivalently in selector coordinates,

`(2+y1-y2)(y1-y2)^2`

`<=3(y1-y2)^2`.

The exact gap is

`(1-e)e^2>=0`.

A full-state rational LP certificate is

`lambda=(1,0)`,

for which

`A^T lambda=1=h`,

`d^T lambda=1=B`.

### Why every T-P5-197 nonnegative majorant is gauge-unbounded

The nonnegative selector gauge direction is

`r=(1,1)`,

with

`V r=0`.

Any `beta` satisfying

`beta>=0`,

`beta>=b=(1,-1)`

must have

`beta_1>=1`.

Therefore

`beta^T r>=1`.

Along the coefficient fiber

`y(t)=t(1,1)`,

we have

`V y(t)=0`

for every `t>=0`, so the physical state never leaves the compact cell, but

`beta^T y(t)>=t -> infinity`.

Hence **no finite coefficient-majorant cap exists**, while the exact physical signed support is trivially finite and T200 closes the cubic term.

This is a strict routing separation, not merely a better constant.

---

## 11. T200-J — boundary: total fixed sign is not enough; the quadratic projected part must have the compatible sign

The T200 inequality uses

`(b^T y)y^TQy <= B y^TQy`.

Therefore `y^TQy>=0` is essential.

Knowing only that the **total** projected scalar is nonnegative does not suffice.

### Exact one-dimensional counterexample

Take the consumed physical interval

`0<=e<=1`,

with

`phi(e)=e-e^2>=0`.

Choose

`a(e)=1+e`,

so `h0=1`, `h=1`, and the slope support is `e<=B=1`.

Here the total fixed sign is positive, but the quadratic part is

`q2_phys(e)=-e^2<=0`.

If one incorrectly applies the T200 formula with `sigma=+1`, `ell=1`, `S=-1`, then the claimed envelope would be

`e-e^2`.

But the true defect is

`(1+e)(e-e^2)=e-e^3`.

For every `0<e<1`,

`e-e^3 > e-e^2`.

So the claimed upper bound fails.

Correct routing: T200 requires the stronger T-P5-196 decomposition gate in which the quadratic projected piece itself is nonnegative on the consumed selector cone/domain. If only total fixed sign is known through cancellation, retain a different bounded-domain argument; do not use T200-A.

---

## 12. T200-K — downstream Lyapunov checker shape

Suppose the nominal selector-wise calculation gives

`dotL_nom(y)<=l0^T y+y^T M0 y`.

For one exact physical affine-amplitude defect, T200-A gives

`dotL_rob(y)`

`<= (l0+h0 c)^T y`

` + y^T[M0+(h0+B)Q+sym(b c^T)]y`.

Define

`l_tot:=l0+h0 c`,

`M_tot:=M0+(h0+B)Q+sym(b c^T)`.

Then the existing T-P5-192 sufficient gate applies unchanged:

**`l_tot<=0` entrywise,**

**`-M_tot` copositive.**

Do **not** separately require the signed cross matrix `sym(b c^T)` or the full defect matrix to be PSD. Its signed entries retain physical cancellation and are part of the final cone quadratic.

If a target decay term `2 gamma L` is already included in the nominal budget, it remains inside `l0,M0`; nothing in this child changes the rate semantics.

---

## 13. Minimal theorem statements for formalization

### T200-1 `signedAffineSlope_cubicAbsorption`

For finite real vectors/matrices, assume

`0<=y`,

`Q` copositive,

`b dot y<=B`.

Then

`(h0+b dot y)(c dot y+y^TQy)`

`<= h0(c dot y)+y^T[(h0+B)Q+sym(b c^T)]y`.

The proof needs no sign hypothesis on `b`; `c>=0` is part of the upstream fixed-sign interface but is not needed for this particular algebraic inequality.

### T200-2 `signedAffineSlope_absorption_gap`

Under the same assumptions, prove the exact identity

`upper-lower=(B-b dot y)(y^TQy)`.

This should be the preferred theorem because the inequality is then one multiplication of two known nonnegative scalars.

### T200-3 `physicalPullback_annihilatesKernel`

If

`b=V^T h`,

`c=sigma V^T ell`,

`Q=sigma V^T S V`,

then for every `r` with `V r=0`,

`b dot r=0`, `c dot r=0`, `Q r=0`, and

`[(h0+B)Q+sym(b c^T)]r=0`.

### T200-4 `physicalStateSupport_of_polyhedralDual`

If

`lambda>=0`,

`A^T lambda=h`,

`A e<=d`,

`d dot lambda<=B`,

then

`h dot e<=B`.

### T200-5 `selectorRestrictedPhysicalSupport_of_dual`

If

`y>=0`,

`A V y<=d`,

`lambda>=0`,

`V^T(A^T lambda-h)>=0`,

`d dot lambda<=B`,

then

`h^T V y<=B`.

### T200-6 `majorantGaugeFailure_exactPullbackSurvives`

If `r>=0`, `V r=0`, `beta>=0`, `beta>=V^T h`, and `beta dot r>0`, then `beta` is unbounded along any feasible coefficient fiber containing `y0+t r`, while the exact physical slope `h^T V(y0+t r)` is constant.

---

## 14. Suggested checker packet

For this branch store the following semantic fields separately:

- `physical_amplitude_offset : h0`
- `physical_amplitude_slope : h`
- `selector_map : V`
- `exact_selector_slope : b`
- `exact_pullback_equality : b=V^T h`
- `projected_linear : c`
- `projected_quadratic : Q`
- `quadratic_sign_gate : Q copositive on y>=0`
- `physical_slope_bound : B`
- either a full-state support dual `lambda` with `A^T lambda=h`, or a cone-restricted dual with `V^T(A^T lambda-h)>=0`
- `same_consumed_domain` identity joining the support bound and fixed-sign packet.

The trusted quadratic debit can then be constructed as

`D_B=(h0+B)Q+sym(b c^T)`.

A source producer may still provide T-P5-197's `beta` packet as fallback, but the dispatcher should prefer this exact branch whenever `b=V^T h` and a physical support cap are available.

---

## 15. Fail-closed routing rules

### PASS_EXACT_SIGNED_PHYSICAL_SUPPORT

The consumer has:

1. exact `b=V^T h`;
2. the T-P5-196 compatible quadratic sign gate `Q` copositive;
3. an exact same-domain bound `b^T y<=B`;
4. the upstream nonnegative amplitude interpretation.

Then use T200-A and return to the ordinary linear-plus-copositive Lyapunov checker.

### MAJORANT_GAUGE_FAIL_EXACT_BRANCH_STILL_OPEN

A T-P5-199 witness shows `beta^T r>0` on `r>=0,Vr=0`, but `b=V^T h` is available.

Do **not** conclude the cubic defect is unabsorbable. First try a physical support bound for `h^T e=b^T y`.

### QUADRATIC_SIGN_INCOMPATIBLE

If the total projected scalar has fixed sign but the isolated quadratic part does not satisfy the required cone sign, T200's multiplication step is invalid. Route to a different bounded-domain/semialgebraic branch.

### AMPLITUDE_NOT_EXACT_AFFINE_PHYSICAL_SCALAR

If the source provides only coordinatewise selector growth, an absolute-value amplitude, a piecewise-affine radius, or another envelope that is not source-bound as `h0+h^T e`, do not invent `h` or signed cancellation. Use T-P5-197/T-P5-199 or a suitable piecewise branch.

### SUPPORT_PACKET_MISSING

Absence of a support dual is not itself a mathematical FAIL unless an exact recession/unboundedness witness is also supplied under the same domain assumptions.

---

## 16. Boundaries that remain OPEN

This review does **not** prove:

1. that any actual Route-B/P5 amplitude is exactly `h0+h^T e`;
2. any actual values of `h0,h,V,ell,S,c,Q`;
3. that the same actual cell carries both the fixed-sign packet and the support bound;
4. physical cell/tube nonemptiness or coverage;
5. that an actual state polytope is bounded;
6. the parallel T-P5-198 quadratic/ellipsoidal-domain result;
7. mixed polyhedral-plus-quadratic domain support;
8. final combined copositivity after adding the defect to a nominal Lyapunov matrix;
9. Float64/interval/controller/PDE/ODE semantic validity;
10. Lean/kernel compilation;
11. independent verification by 封不觉;
12. admission or registry eligibility.

All remain OPEN.

---

## 17. Recommended integration/routing consequence

Add one branch before declaring the T-P5-197 bounded-domain rescue unavailable:

1. detect whether the state-dependent amplitude is source-bound as one exact affine physical scalar `h0+h^T e`;
2. preserve `b=V^T h` with its signs;
3. certify `h^T e<=B` on the same consumed cell, preferably directly in physical coordinates or through the signed T-P5-199 LP dual;
4. use the exact-gap identity
   `(B-h^T e) sigma e^T S e>=0`;
5. pull back the resulting physical quadratic packet only after the bound is formed;
6. invoke the existing T-P5-192 copositivity checker.

This branch preserves signed cancellation, is invariant under redundant selector representations, and can close cases where every nonnegative coefficient majorant is provably unbounded.
