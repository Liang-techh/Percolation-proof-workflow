---
kind: review_result
review_id: review-T-P5-193-affine-box-defect-bridge-liuguanyi-20260909T2301Z
task_id: T-P5-193-AFFINE-BOX-DEFECT-BRIDGE
reviewer: 柳冠一
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-09T23:01:00Z
claim_commit: 5a2eefaed099d89135bcf7e6bc991bb5e9018973
inspected_commit: 9ed16126b857cba5bc76ce7b4567b13aeefaa618
upstream_commits:
  - ef1dfbc4779541e30d02843b282cdd9e892912a2  # T-P5-191 affine finite-cone viability
  - 86d3e6a59cf11c4d1bd28ffa5a6ab7a66cd20eda  # T-P5-192 selector-cone Lyapunov margin
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_affine_box_normal_viability_lift; add_selector_box_sign_fan; add_constant_defect_origin_obstruction; preserve_box_vs_correlated_source_semantics
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact finite-dimensional interval-box duality, polyhedral Farkas algebra, selector-cone quadratic pullback, exact rational counterexamples; no source/provenance audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-193 — affine componentwise defect box bridge for viability and Lyapunov decay

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-191 gives an exact Metzler lift for an affine external ODE on a polyhedral finite-value cone. T-P5-192 gives a seam-safe Lyapunov margin on each exact KKT selector cone, again for an affine external field. A realistic source adapter is usually not exactly affine: after extracting an affine core, one has a remainder/uncertainty field.

This review closes one narrow but substantive source-to-math interface when that remainder is certified by a state-dependent componentwise box

`e' = A e + c + rho`,

`-h(e) <= rho <= h(e)`,

`h(e) = H e + h0 >= 0` on the intended cone.

There are two exact algebraic bridges:

1. **facet-normal viability:** the worst box defect in a normal `n` is exactly `-|n| h`; therefore robust viability of `E_N={e:N e>=0}` reduces to the Metzler packet

   **`N A - |N| H = Lambda N`,**

   **`Lambda_ij>=0` for `i!=j`,**

   **`N c >= |N| h0`;**

2. **selector Lyapunov defect:** on a sign sector where `Sigma G e>=0`, the exact worst frozen-gradient defect is

   **`sup rho^T G e = (H e+h0)^T Sigma G e`;**

   hence T-P5-192's robust derivative margin is again one symmetric quadratic plus one linear form, and can be pulled back to ordinary copositivity on finite cone generators.

The important semantic boundary is also exact: if the source only proves that a correlated residual lies **inside** this box, every PASS remains safe, but a box FAIL is not an actual source obstruction. Exact FAIL semantics require the independent box itself to be the allowed differential inclusion, or a same-state residual witness that attains the bad sign choice.

No source binding, physical coverage, Float64 interval correctness, Lean/kernel proof, or admission is claimed here.

---

## 1. Setup and typed contract

Let `e in R^p` be the external state. Assume the actual field is decomposed as

`f(e,rho) = A e + c + rho`.

Let the defect half-width be affine:

`h(e) = H e + h0`.

The box contract is

`B(e) := {rho in R^p : -h(e) <= rho <= h(e)}`,

with componentwise order and the side condition

**`h(e)>=0` on the full intended domain.**

This side condition is mathematical, not formatting. If the domain is a rational cone `cone(V)`, one sufficient and exact generator-side packet for affine `h` on the whole cone is

`h0>=0`,

`H V>=0` entrywise.

If the source already supplies `h(e)` as an outward-rounded nonnegative interval radius, that source fact can discharge the same premise; this review does not prove such a source fact.

Two source semantics must remain distinct:

- **exact independent box semantics:** every `rho in B(e)` is an allowed instantaneous defect;
- **outer enclosure semantics:** the actual correlated residual set `R(e)` only satisfies `R(e) subseteq B(e)`.

All PASS theorems below are valid under outer enclosure semantics. Necessity / robust-FAIL conclusions are valid only for exact independent box semantics unless an actual source witness is separately produced.

---

## 2. T193-A — exact support function of a componentwise box

Let `h>=0` and

`B_h={rho:-h<=rho<=h}`.

For every vector `w`,

**`sup_(rho in B_h) w^T rho = |w|^T h`,**

**`inf_(rho in B_h) w^T rho = -|w|^T h`.**

Here `|w|` is componentwise absolute value.

### Proof

For every admissible `rho`,

`w_j rho_j <= |w_j| |rho_j| <= |w_j| h_j`.

Summing gives the upper bound. Equality is attained componentwise by

`rho_j = sign(w_j) h_j`

(with either sign when `w_j=0`). The lower formula follows by replacing `w` by `-w`.

This one-line identity is the essential adapter lemma. It is incorrect to transport a signed normal through the half-width without absolute values.

---

## 3. T193-B — exact box-robust facet-normal condition

Let

`E_N := {e : N e>=0}`,

with rows `n_i^T`. For the affine-core-plus-box field, robust tangency on active face `i` asks

`n_i^T(Ae+c+rho)>=0`

for every

`e in E_N`, `n_i^T e=0`, `rho in B(e)`.

By T193-A, this is equivalent to

`n_i^T A e + n_i^T c - |n_i|^T(H e+h0) >=0`

on that face.

Define

`r_i^T := n_i^T A - |n_i|^T H`,

`b_i := n_i^T c - |n_i|^T h0`.

Then the robust face condition is simply

`r_i^T e+b_i>=0` on `F_i={e:Ne>=0,n_i^T e=0}`.

Because `F_i` is a cone, exactly the same scaling argument as T-P5-191 separates this into

**`b_i>=0`,**

and

**`r_i^T e>=0` for every `e in F_i`.**

No Euclidean norm and no scalar Lipschitz conversion is needed.

---

## 4. T193-C — exact Metzler lift with state-dependent box width

Apply the T-P5-191 face-duality theorem to the modified rows `r_i`.

The following are equivalent to the all-face robust tangency conditions under exact independent box semantics:

there exists `Lambda` with free diagonal and nonnegative off-diagonal entries such that

**`N A - |N| H = Lambda N`,**

**`N c - |N| h0 >=0`.**

Equivalently,

**`N A - |N| H = Lambda N`,**

**`Lambda` Metzler,**

**`N c >= |N| h0`.**

Here `|N|` is entrywise absolute value.

### Direct forward-invariance proof

Let `y=N e`. Every defect satisfying the box enclosure obeys

`N rho >= -|N| h(e)`

`= -|N|H e - |N|h0`.

Using the matrix identity,

`N A e = Lambda N e + |N|H e`.

Hence along every admissible trajectory,

`y' = N A e+N c+N rho`

`>= Lambda y + (N c-|N|h0)`.

The forcing vector is nonnegative and `Lambda` is Metzler. The same positive-system comparison argument as T-P5-191 therefore gives

**`y(0)>=0  =>  y(t)>=0` for all forward times.**

Thus the packet is a sound global viability certificate even when the box is merely an outer enclosure.

### Necessity boundary

If every point of `B(e)` is genuinely allowed, the worst-sign choice from T193-A is available on every active face, so the same Farkas argument makes the packet exact for robust all-face tangency.

If the actual residual is correlated and occupies only a strict subset of the box, failure of this packet may be pure enclosure conservatism.

---

## 5. Why `|N|` is mandatory: exact rational counterexample

Take one facet normal

`n=(1,-1)`

and constant half-width

`h=(1,1)`.

The signed contraction is

`n^T h=0`.

A naive adapter using `n^T h` would therefore claim zero worst normal defect.

But the allowed box point

`rho=(-1,1)`

gives

**`n^T rho=-2`.**

The exact support formula gives

`-|n|^T h=-(1+1)=-2`,

which is sharp.

Therefore replacing `|N|H` or `|N|h0` by the signed products `NH` or `Nh0` is mathematically unsound.

---

## 6. T193-D — exact box defect in a frozen selector gradient

Now use the T-P5-192 selector notation. On a selector cone `C_alpha`, let

`u=Y_alpha e`

be an exact KKT minimizer and define

`Q_alpha := Y_alpha^T P Y_alpha + Y_alpha^T B^T + B Y_alpha + C`,

`G_alpha := B Y_alpha + C`,

`L_alpha := A^T G_alpha + G_alpha^T A`.

Then T-P5-192's frozen-minimizer Dini bound becomes, for the perturbed field,

`D^+ Phi(e)`

`<= e^T L_alpha e + 2 c^T G_alpha e + 2 rho^T G_alpha e`.

At a fixed `e`, T193-A gives the exact box worst case

**`sup_(rho in B(e)) rho^T G_alpha e = h(e)^T |G_alpha e|`.**

Therefore

**`D^+ Phi(e) <= e^T L_alpha e + 2 c^T G_alpha e + 2 h(e)^T |G_alpha e|`.**

This retains all signed cancellation in `G_alpha e`; no norm bound has yet been introduced.

---

## 7. T193-E — finite sign fan removes the absolute value exactly

For a sign vector `sigma in {+1,-1}^p`, let

`Sigma := diag(sigma)`.

Define the sign sector

`C_(alpha,sigma) := C_alpha intersect {e : Sigma G_alpha e>=0}`.

Every `e in C_alpha` belongs to at least one such sector; if a component of `G_alpha e` is zero, it may belong to multiple sectors, which is harmless.

On `C_(alpha,sigma)`,

`|G_alpha e| = Sigma G_alpha e`.

Hence

`2 h(e)^T |G_alpha e|`

`= 2(H e+h0)^T Sigma G_alpha e`

`= e^T D_(alpha,sigma) e + 2 d_(alpha,sigma)^T e`,

where

**`D_(alpha,sigma) := H^T Sigma G_alpha + G_alpha^T Sigma H`,**

**`d_(alpha,sigma) := G_alpha^T Sigma h0`.**

Thus the worst-box frozen derivative on that sector is exactly

**`e^T (L_alpha+D_(alpha,sigma)) e + 2 ell_(alpha,sigma)^T e`,**

with

**`ell_(alpha,sigma) := G_alpha^T c + G_alpha^T Sigma h0`.**

No square root, absolute-value primitive, nonlinear optimizer, or interval branching remains inside the checker once a sector is fixed.

### Rational finite fan

If `C_alpha` is rational polyhedral and `G_alpha` is rational, every nonempty `C_(alpha,sigma)` is rational polyhedral. By Minkowski-Weyl it has a finite rational generator representation. One need not enumerate all `2^p` sign patterns in advance: the producer may emit only nonempty sectors plus an exact cover certificate.

---

## 8. T193-F — robust exponential-rate packet on one sign sector

Fix a target `gamma>=0`. On `C_alpha`,

`Phi(e)=e^T Q_alpha e`.

On sign sector `C_(alpha,sigma)`, robustly over the defect box it is sufficient to require

`D^+ Phi(e) <= -2 gamma Phi(e)`.

Using T193-E, this is exactly the T-P5-192-style mixed-degree inequality

`e^T M_(alpha,sigma)(gamma)e + 2 ell_(alpha,sigma)^T e <=0`,

where

**`M_(alpha,sigma)(gamma)`**

`:= L_alpha + 2 gamma Q_alpha`

`   + H^T Sigma G_alpha + G_alpha^T Sigma H`,

and

**`ell_(alpha,sigma) := G_alpha^T(c+Sigma h0)`.**

Because the sign sector is a cone, the quadratic and linear parts again separate exactly:

**quadratic gate**

`e^T M_(alpha,sigma)(gamma)e<=0` on the sector;

**linear gate**

`ell_(alpha,sigma)^T e<=0` on the sector.

If

`C_(alpha,sigma)=cone(V_(alpha,sigma))`,

these become the finite checker packet

**`-V^T M_(alpha,sigma)(gamma) V` copositive,**

**`V^T ell_(alpha,sigma)<=0` entrywise.**

Thus the state-dependent box remainder does not require a new global nonlinear solver. It only refines each selector cone by a finite sign fan and reuses the fixed copositivity machinery already developed in the P5 chain.

---

## 9. Exactness level of the Lyapunov packet

There are two different meanings of “exact” here and they must not be conflated.

### Exact box maximization

For a fixed state and frozen selector gradient, the reduction

`sup rho^T G e = h^T|Ge|`

and its sign-sector quadratic formula are exact whenever the allowed uncertainty is the full independent box.

### Frozen-selector Dini layer

T-P5-192 itself uses a chosen current minimizer to upper-bound the Dini derivative. At a nonsmooth seam, another minimizer may give a smaller slope. Therefore failure of one frozen-selector packet is not automatically a physical instability theorem.

For certification, this is fine: if every covering selector/sign sector passes, the desired robust Dini inequality holds globally. For a FAIL claim, either use T-P5-190's exact minimum-slope directional formula or give an actual trajectory/source witness.

---

## 10. T193-G — constant symmetric defect creates an origin-scale obstruction

The affine half-width naturally separates into

`H e` — a state-proportional error,

and

`h0` — a state-independent error floor.

The latter has a qualitatively different scaling near the cone vertex.

Assume for simplicity `c=0`. Along a ray `e=t r`, the nominal quadratic derivative and target decay margin are `O(t^2)`, while the box contribution from `h0` is

`2 t h0^T |G r|`.

If

`h0^T |G r|>0`,

then for all sufficiently small `t>0`, the positive `O(t)` box term dominates every `O(t^2)` quadratic decay budget. Hence no uniform robust exponential decay-to-zero certificate can hold on that ray for the full symmetric box.

Therefore:

### Theorem T193-G

For `c=0`, a necessary condition for robust local decay to the cone vertex under an exact symmetric box with constant radius `h0` is

**`h0^T |G_alpha r|=0` for every relevant ray `r`.**

In particular, if every component is Lyapunov-visible and `h0>0`, asymptotic decay to the exact origin is impossible for the full box inclusion; one can at best seek practical stability / an ultimate bound unless the uncertainty shrinks with the state.

### One-dimensional regression

Take

`Phi(e)=e^2`,

`e'=-e+rho`,

`|rho|<=epsilon`, `epsilon>0`.

Then for `e>0`,

`sup d/dt Phi = -2e^2+2 epsilon e`.

This is positive whenever `0<e<epsilon`. Thus the nonzero constant defect floor really does destroy robust decay to the origin; this is not a proof-artifact of the sign fan.

---

## 11. Correlation boundary: box FAIL is not source FAIL under outer enclosure

Take the ray

`e=(t,0)`, `t>=0`,

and choose a frozen gradient matrix with

`G e=(t,t)`.

Let the actual correlated residual family be

`rho=(s,-s)`, `|s|<=t`.

Then for every actual residual,

**`rho^T G e = s t - s t = 0`.**

However the smallest obvious componentwise outer box is

`|rho_1|<=t`, `|rho_2|<=t`.

That box also contains the unattainable point

`rho=(t,t)`,

for which

`rho^T G e=2t^2`.

Hence the box support function reports a positive worst-case defect although the true correlated source defect cancels identically.

This pins the source semantics:

- a box PASS is sound for every residual subset of the box;
- a box FAIL only proves that the **box relaxation** is too large;
- to promote FAIL to a source obstruction, bind the bad sign choice to one actual same-state residual or use a correlation-preserving uncertainty representation.

This is directly analogous to the correlation warning in T-P5-167, now at the ODE/vector-field remainder layer.

---

## 12. A single shared source packet can feed both T191 and T192 consumers

The main interface benefit is that one same-key remainder packet

`rho(e) in [-H e-h0, H e+h0]`

can be consumed twice without changing its mathematical meaning.

### Viability consumer

Check

`N A-|N|H=Lambda N`,

`Lambda` Metzler,

`N c>=|N|h0`.

This guarantees the finite-value cone remains viable under every residual in the box.

### Lyapunov consumer

For each exact KKT selector `Y_alpha`, refine by signs of `G_alpha e`; on each nonempty sector check

`-V^T M_(alpha,sigma)(gamma)V` copositive,

`V^T ell_(alpha,sigma)<=0`.

This guarantees the T-P5-192 frozen-selector robust Dini margin under every residual in the same box.

The two consumers use different dual views of the same uncertainty:

- viability sees facet normals `N` and therefore `|N|h`;
- energy sees frozen gradients `G_alpha e` and therefore `h^T|G_alpha e|`.

A source adapter should not replace either by a generic Euclidean norm unless it deliberately accepts the resulting conservatism.

---

## 13. Minimal theorem statements for formalization

Suggested leaf statements, deliberately source-independent:

1. `box_sup_dot`
   - `h>=0 -> sup {rho | -h<=rho<=h} (w·rho) = |w|·h`.

2. `box_inf_dot`
   - corresponding lower support identity.

3. `polyhedralCone_boxRobustTangent_iff_metzlerLift`
   - for affine `h(e)=He+h0`, exact full-box robust tangency iff
     `NA-|N|H=Lambda N`, `Lambda` Metzler, `Nc>=|N|h0`.

4. `boxMetzlerLift_forwardInvariant`
   - same packet plus outer-box inclusion is sufficient for forward invariance.

5. `selector_boxWorstFrozenSlope_onSignSector`
   - on `Sigma G e>=0`, replace `2 rho^T G e` by the exact symmetric quadratic-plus-linear expression.

6. `selectorSignSector_decay_iff_pullbackGates`
   - for a conic sector `cone(V)`, the mixed robust upper bound is equivalent to copositivity of `-V^TMV` plus `V^Tell<=0`.

7. `constantBoxFloor_obstructs_originDecay`
   - the `O(t)` versus `O(t^2)` scaling obstruction when `h0^T|Gr|>0`.

These leaves need only finite-dimensional real linear algebra, entrywise order, finite sums, and the existing copositivity definition. They do not require pseudoinverse, spectral theory, or nonlinear optimization.

---

## 14. Suggested typed source interface

A minimal producer object should distinguish the mathematical enclosure from source provenance:

`AffineBoxDefectPacket`

- `state_key` / `cell_key`;
- exact `A,c,H,h0` after whatever rationalization policy the source layer proves;
- theorem/evidence that `h(e)=He+h0>=0` on the intended domain;
- theorem/evidence that actual `rho(e)` satisfies `-h(e)<=rho(e)<=h(e)` on the same domain;
- `box_semantics = outer_enclosure | exact_independent_inclusion`;
- optional correlation-preserving refinement if the box is known to be loose.

The mathematical child should consume only the proved inequalities/equalities. It must not infer `exact_independent_inclusion` merely because interval endpoints are present in a JSON/CSV file.

For the Lyapunov lane, each sign-sector packet additionally needs

- selector id `alpha` and its exact `Y_alpha`;
- exact `G_alpha,Q_alpha,L_alpha` derivation;
- sign vector `sigma`;
- rational generator matrix `V_(alpha,sigma)`;
- exact sector inclusion/cover statement;
- fixed-`gamma` copositivity and linear-sign result.

---

## 15. What this result closes

Mathematically, T-P5-193 closes the following narrow bridge:

**state-dependent componentwise source remainder box**

`-> exact facet-normal worst case`

`-> Metzler finite-value-cone viability`

and simultaneously

`-> exact frozen-gradient box support`

`-> finite sign fan`

`-> quadratic + linear selector margin`

`-> ordinary copositivity pullback`.

This removes the need to insert a generic norm bound between an interval/source remainder and the P5 cone/Lyapunov consumers, preserving signed geometry at both layers.

---

## 16. Remaining open boundaries

This review does **not** close:

1. actual same-key source extraction of `A,c,H,h0`;
2. proof that a Float64/interval producer's endpoints are outward-rounded and valid on the full cell/tube;
3. proof that `h(e)>=0` on the actual finite-value domain;
4. exact correlation structure if the componentwise box is only an outer hull;
5. construction and coverage of the actual selector/sign sectors;
6. the fixed copositivity certificates on those sectors;
7. T-P5-191/192 source binding for the real ODE/PDE vector field;
8. PDE-to-finite-dimensional external-state closure, if `rho` includes unresolved PDE modes;
9. practical-stability redesign when `h0!=0` obstructs decay to the origin;
10. P8/M4, physical path/trajectory coverage, Lean/kernel compilation, independent verification by 封不觉, admission, or registry promotion.

A particularly useful next mathematics target is a **correlation-preserving defect adapter** (zonotope/polytope or shared-parameter affine image) that replaces the independent box without losing the exact support-function/copotivity reduction. That would attack the only deliberate conservatism introduced by the present child.
