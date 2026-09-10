---
kind: review_result
review_id: review-T-P5-199-polyhedral-domain-selector-lp-dual-transport-kuangmanmozun-20260910T0030Z
task_id: T-P5-199-POLYHEDRAL-DOMAIN-SELECTOR-LP-DUAL-TRANSPORT
reviewer: 狂蛮魔尊
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-10T00:30:00Z
claim_commit: b4c870bae4095a79fbd9539dc7fee4b1cc5a064a
inspected_commit: 9129dfb0d15bad5e9190e8a0a54bb69e2c78aec0
upstream_commits:
  - 85a96adf98569071e07bb7b8b2ed1f098d492d35  # T-P5-195 projected-skew affine-generator gate
  - af69121cff7bbb476aea1c6b528936d872f3e015  # T-P5-196 fixed-sign quadratic rescue
  - 44f14ed1d40c4edc2a4bac8eb5851ea2dae4c55c  # T-P5-197 weighted radial cubic absorption
parallel_nonoverlap:
  - 9129dfb0d15bad5e9190e8a0a54bb69e2c78aec0  # T-P5-198 claim: quadratic/ellipsoidal-domain route by 古月方源
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_polyhedral_selector_dual_cap; add_direct_beta_support_dual; add_noninjective_selector_gauge_obstruction; route_polyhedral_domains_to_exact_rational_lp_certificate
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: finite-dimensional LP/Farkas dual derivation, recession-cone analysis, exact rational examples and counterexamples; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-199 — polyhedral state-domain to selector-cap transport without inverting the selector map

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-197 left one source-to-selector seam explicit: the cubic absorption theorem wants a coefficient-space cap such as

`w^T y <= R`,

while a real cell/tube is more naturally stored in state coordinates

`e = V y`, `y>=0`,

with a polyhedral description

`A e <= d`.

A false inverse of `V` is especially dangerous because the conic representation may be redundant or non-injective.

This review closes the **polyhedral** half of that seam exactly.

Let

`F := { y : y>=0 and A V y <= d }`.

For a proposed coefficient bound `w^T y<=R`, a finite exact certificate is any vector `lambda>=0` satisfying

**`(A V)^T lambda >= w` entrywise**

and

**`d^T lambda <= R`.**

Then for every `y in F`,

`w^T y <= lambda^T A V y <= lambda^T d <= R`.

No inverse of `V`, norm, square root, eigenvalue, pseudoinverse, or semialgebraic solver is needed.

Under the standard nonempty finite-dimensional LP hypothesis, this certificate is also **necessary**: if `w^T y<=R` for every `y in F`, LP strong duality/Farkas gives such a `lambda`. For rational `A,V,d,w,R`, whenever the bound is true there is a rational certificate, so the checker surface is exact rational arithmetic.

There is a stronger direct compression for T-P5-197. Instead of first inventing `w,R,kappa`, directly certify an upper bound on the amplitude majorant:

`beta^T y <= B` on `F`.

It is enough, and under nonemptiness equivalent, to supply

`lambda>=0`,

`(A V)^T lambda >= beta`,

`d^T lambda <= B`.

Then the T-P5-197 fixed-sign defect closes with

**`D = (h0+B) Q + sym(beta c^T)`**,

which can be strictly sharper than routing through an arbitrary weighted radial gauge `beta<=kappa w`, `w^T y<=R` and using `B=kappa R`.

Finally, the review identifies the exact obstruction caused by a non-injective selector map. Even a **bounded state polytope** need not bound coefficient weights. If `r>=0`, `V r=0`, and `w^T r>0`, then every feasible `y0` generates the same physical state along

`y0+t r`, `t>=0`,

while `w^T(y0+t r)` diverges. This is a representation-gauge obstruction, not a physical unboundedness of the state domain.

No actual P5 polytope, same-cell source identity, Float64/interval enclosure, selector coverage, Lean/kernel proof, independent verification, admission, or registry promotion is claimed.

---

## 1. Setup

Let

- `V : R^p -> R^n` be the selector generator map;
- `y in R^p`, with `y>=0` coordinatewise;
- `e=V y` be the physical/state coordinate;
- `A in R^(m x n)` and `d in R^m` describe a polyhedral consumed domain
  `P={e : A e<=d}`;
- `w in R^p`, normally `w>=0` in the T-P5-197 radial packet.

The pulled-back selector feasible set is

`F={y>=0 : A V y<=d}`.

Write

`Bmat := A V`.

The mathematical question is:

> When does the state-space polyhedral contract imply `w^T y<=R` for every selector representation consumed by the proof?

The answer is an ordinary LP dual certificate on `Bmat`; no inverse or left inverse of `V` is part of the theorem.

---

## 2. T199-A — one-line exact dual certificate

### Theorem A1 — sufficient checker-facing certificate

Assume

`y>=0`,

`Bmat y<=d`,

`lambda>=0`,

`Bmat^T lambda>=w`,

`d^T lambda<=R`.

Then

**`w^T y<=R`.**

### Proof

Because `y>=0` and `Bmat^T lambda-w>=0` entrywise,

`w^T y <= lambda^T Bmat y`.

Because `lambda>=0` and `Bmat y<=d`,

`lambda^T Bmat y <= lambda^T d`.

Finally `lambda^T d<=R`.

Hence

`w^T y <= lambda^T Bmat y <= lambda^T d <= R`.

Every step is a finite sum of ordered scalar products.

### Checker surface

A rational checker only needs to verify:

1. `lambda_i>=0` for every domain row;
2. `(Bmat^T lambda)_j-w_j>=0` for every selector coordinate;
3. `R-d^T lambda>=0`.

No optimization is needed to consume a supplied certificate.

---

## 3. T199-B — exact iff for a proposed radial bound

Assume `F` is nonempty.

Consider the primal LP

`p* = sup { w^T y : y>=0, Bmat y<=d }`.

Its dual is

`q* = inf { d^T lambda : lambda>=0, Bmat^T lambda>=w }`.

### Theorem B1 — exact proposed-bound certificate

For nonempty `F`, the following are equivalent:

1. `w^T y<=R` for every `y in F`;
2. there exists `lambda>=0` such that
   `Bmat^T lambda>=w` and `d^T lambda<=R`.

### Proof

`(2)->(1)` is Theorem A1.

For `(1)->(2)`, the primal is feasible and has finite optimum `p*<=R`.
Finite-dimensional LP strong duality gives a dual feasible minimizer `lambda*` with

`d^T lambda* = p* <= R`.

Thus `lambda*` is the required certificate.

Equivalently, this can be packaged as a standard finite-dimensional Farkas alternative and need not expose an optimizer in a formal theorem consumer.

### Empty-domain guard

The nonempty premise is mathematically important. If `F` is empty, the universal inequality is vacuously true while a chosen dual certificate need not exist. A source/domain packet should therefore carry either an explicit feasible point or an independently proved nonemptiness statement before using the iff direction.

The **sufficient** direction A1 never needs nonemptiness.

---

## 4. T199-C — direct amplitude-majorant dual, eliminating the artificial radial gauge

T-P5-197 writes the fixed-sign projected quantity on `y>=0` as

`L(y)=c^T y+y^T Q y`,

with

`c>=0`,

`Q` copositive,

so `L(y)>=0`.

Its affine amplitude satisfies

`a(y)=h0+b^T y>=0`.

Choose the same nonnegative majorant used by T-P5-197:

`beta>=0`,

`beta>=b` entrywise.

Then for `y>=0`,

`a(y)<=h0+beta^T y`.

The weighted-radial route of T-P5-197 obtains

`beta^T y<=kappa R`

from two separate packets `beta<=kappa w` and `w^T y<=R`.

On a polyhedral domain, that intermediate gauge is unnecessary.

### Theorem C1 — direct beta support certificate

If there exists `lambda>=0` such that

**`Bmat^T lambda>=beta`**

and

**`d^T lambda<=B`**,

then for all `y in F`,

**`beta^T y<=B`.**

This is Theorem A1 with `w=beta`.

### Theorem C2 — direct polyhedral cubic-to-quadratic absorption

Under the T-P5-197 sign gates and the direct beta bound above,

`a(y)L(y)`

is bounded by

**`h0 c^T y + y^T D_B y`**,

where

**`D_B=(h0+B)Q+sym(beta c^T)`**,

and

`sym(beta c^T)=(beta c^T+c beta^T)/2`.

### Proof

Since `L(y)>=0` and `a(y)<=h0+beta^T y`,

`a(y)L(y) <= (h0+beta^T y)(c^T y+y^TQy)`.

Expand:

`=h0 c^T y + h0 y^TQy + (beta^T y)(c^T y) + (beta^T y)(y^TQy)`.

The mixed linear product is exactly

`(beta^T y)(c^T y)=y^T sym(beta c^T)y`.

Because `Q` is copositive, `y^TQy>=0`; because `beta^T y<=B`,

`(beta^T y)(y^TQy)<=B(y^TQy)`.

Collect terms to obtain

`h0 c^T y+y^T[(h0+B)Q+sym(beta c^T)]y`.

### Consequence

For polyhedral cells, the optimal possible scalar in this proof architecture is

`B_* = max_{y in F} beta^T y`

and LP duality gives

**`B_* = min_{lambda>=0, Bmat^T lambda>=beta} d^T lambda`**

whenever `F` is nonempty and the support is finite.

Thus a producer can sharpen the defect coefficient without changing the checker: optimize `lambda` externally, then store only an exact rational feasible `lambda` and rational `B`.

---

## 5. T199-D — recession criterion and the non-injective selector obstruction

The recession cone of `F` is

`rec(F)={r>=0 : Bmat r<=0}`.

If `y0 in F` and `r in rec(F)`, then

`y0+t r in F`

for every `t>=0`.

Therefore, if

`w^T r>0`,

then

`w^T(y0+t r)=w^T y0+t w^T r -> +infinity`.

### Theorem D1 — exact finite-support criterion

Assume `F` is nonempty. Then `sup_F w^T y` is finite iff

**`w^T r<=0` for every `r in rec(F)`.**

For the T-P5-197 regime `w>=0` and `r>=0`, this simplifies to

**`w^T r=0` for every `r>=0` with `A V r<=0`.**

This is the exact obstruction test before trying to optimize a radial cap.

---

## 6. T199-E — bounded state polytope does not imply bounded selector coefficients

Suppose now that the physical state polytope

`P={e : A e<=d}`

is bounded and `F` is nonempty.

### Theorem E1 — all selector recession is pure representation gauge

Under these assumptions,

**`rec(F) = {r>=0 : V r=0}`.**

### Proof

If `r>=0` and `V r=0`, then `A V r=0<=0`, so `r in rec(F)`.

Conversely let `r in rec(F)` and choose `y0 in F`. Then

`e_t=V(y0+t r)=V y0+t V r`

lies in `P` for every `t>=0`, because

`A e_t=A V y0+t A V r<=d`.

If `V r` were nonzero, `||e_t||` would diverge linearly, contradicting boundedness of `P`. Therefore `V r=0`.

### Corollary E2 — exact gauge criterion

For bounded nonempty `P`, a finite bound on `w^T y` over `F` exists iff

**`w^T r=0` for every `r>=0` with `V r=0`.**

If `w>0` strictly componentwise, this becomes

**`ker(V) intersect R_+^p = {0}`.**

So a bounded physical cell is enough only when the selector representation has no positively weighted nonnegative gauge direction.

This is exactly why the transport theorem must not use an arbitrary inverse or pseudoinverse of `V`.

---

## 7. Exact counterexample — bounded state cell, unbounded selector radial coordinate

Take one state coordinate `e in R` and two selector coefficients `y1,y2>=0`.

Let

`V=[1,-1]`,

so

`e=y1-y2`.

Let the physical state polytope be the bounded interval

`P=[-1,1]`,

written as

`A=[[1],[-1]]`,

`d=(1,1)`.

Take

`w=(1,1)`.

For every `t>=0`, choose

`y(t)=(t,t)`.

Then

`V y(t)=0 in P`,

but

`w^T y(t)=2t -> infinity`.

The nonnegative gauge direction is

`r=(1,1)`,

with

`V r=0`,

`w^T r=2>0`.

Thus even a compact state domain does **not** imply a selector radial cap.

This counterexample directly excludes the tempting but false rule

> "bounded `e` plus finite generators `V` implies bounded nonnegative coefficients `y`."

It does not.

---

## 8. Rational sharp example — dual certificate attains the exact selector cap

Take `V=I_2` and the state/selector simplex

`F={y1,y2>=0 : y1+y2<=1}`.

Thus

`A=[1,1]`,

`d=1`.

Let

`w=(2,1)`.

The sharp bound is clearly

`2y1+y2<=2`,

attained at `y=(1,0)`.

Choose the one-row dual certificate

`lambda=2`.

Then

`A^T lambda=(2,2)>=w`,

`d^T lambda=2`.

Therefore Theorem A1 gives `w^T y<=2`, and primal equality at `(1,0)` proves sharpness.

All data and the certificate are rational.

---

## 9. Why this is different from T-P5-198

T-P5-198 was already claimed by 古月方源 before this task started. Its scope is the distinct quadratic-domain question:

`y^T P y<=rho`

and a copositivity characterization of a radial cap.

This review does not touch that route.

T-P5-199 handles the **polyhedral state-domain** case

`A e<=d`, `e=V y`,

and resolves the non-injective-selector issue through linear dual certificates and recession analysis.

The two branches can coexist in the checker:

- polyhedral cell/tube -> T-P5-199 exact LP/Farkas certificate;
- homogeneous quadratic/ellipsoidal selector-domain -> T-P5-198 copositivity certificate.

No task ownership overlaps.

---

## 10. Fail-closed routing rules

A checker using this child should distinguish four outcomes.

### PASS_POLYHEDRAL_DUAL_CAP

A supplied rational `lambda` verifies

`lambda>=0`,

`(A V)^T lambda>=w`,

`d^T lambda<=R`.

Then the radial cap is mathematically proved conditional on the supplied domain/source binding.

### PASS_DIRECT_BETA_DUAL

A supplied rational `lambda_beta` verifies

`lambda_beta>=0`,

`(A V)^T lambda_beta>=beta`,

`d^T lambda_beta<=B`.

Then T-P5-197 may use the sharper defect matrix

`(h0+B)Q+sym(beta c^T)`.

### FAIL_GAUGE_RECESSION_WITNESS

A rational witness `r` verifies

`r>=0`,

`A V r<=0`,

`w^T r>0`.

Given a nonempty feasible set, no finite radial cap exists for that `w` on the pulled-back polyhedron.

If the physical state polytope is already known bounded, it is enough to verify the simpler witness

`r>=0`, `V r=0`, `w^T r>0`.

### DUAL_PACKET_NOT_AVAILABLE

Absence of a supplied dual certificate is **not** by itself a source-system failure. Unless the exact LP alternative has also been run under a proved nonempty domain, route back to LP/Farkas generation or to another domain representation. Do not infer a mathematical counterexample from a missing producer artifact.

---

## 11. Minimal theorem statements for formalization

### T199-1 `polyhedralSelectorBound_of_dual`

For finite real matrices/vectors:

if

`0<=y`, `A*(V*y)<=d`, `0<=lambda`, `w<=transpose(A*V)*lambda`, and `d dot lambda<=R`,

then

`w dot y<=R`.

This is elementary ordered finite-sum algebra.

### T199-2 `polyhedralSelectorBound_iff_dual`

Assume `F={y>=0 : A V y<=d}` is nonempty. Then

`forall y in F, w dot y<=R`

iff

`exists lambda>=0, transpose(A V) lambda>=w and d dot lambda<=R`.

This leaf may be formalized through an existing finite-dimensional Farkas/LP duality theorem rather than reproving simplex theory.

### T199-3 `polyhedralDirectBetaAbsorption`

Under T-P5-197's `c>=0`, `Q` copositive, `beta>=b`, `beta>=0`, `a(y)>=0`, plus

`beta dot y<=B`,

prove

`a(y)(c dot y+y^TQy)`

`<=h0(c dot y)+y^T[(h0+B)Q+sym(beta c^T)]y`.

### T199-4 `boundedState_selectorRecession_eq_nonnegKernel`

If `P={e:Ae<=d}` is bounded and the pullback `F` is nonempty, then

`{r>=0 : A V r<=0}={r>=0 : V r=0}`.

### T199-5 `nonnegativeGauge_obstructsRadialCap`

If `y0 in F`, `r>=0`, `A V r<=0`, and `w dot r>0`, then for every finite `R` there exists `t>=0` with

`w dot (y0+t r)>R`

and

`y0+t r in F`.

---

## 12. Suggested packet schema

For a polyhedral source/domain consumer keep these fields explicit:

- `selector_generators : V`
- `domain_matrix : A`
- `domain_rhs : d`
- `domain_nonempty_witness : y0` or a separate nonempty theorem
- `radial_weight : w`
- `radial_bound : R`
- `dual_multiplier : lambda`
- `dual_nonnegative : lambda>=0`
- `dual_selector_domination : (A V)^T lambda>=w`
- `dual_objective_bound : d^T lambda<=R`

For the direct T-P5-197 compression additionally allow:

- `amplitude_majorant : beta`
- `direct_amplitude_bound : B`
- `amplitude_dual_multiplier : lambda_beta`
- `amplitude_dual_domination : (A V)^T lambda_beta>=beta`
- `amplitude_dual_objective : d^T lambda_beta<=B`.

The source/domain identity `A e<=d` and the selector identity `e=V y` must remain separate semantic premises from the rational LP certificate.

---

## 13. Boundaries that remain OPEN

This review does **not** prove:

1. that the actual P5 cell/tube is polyhedral;
2. any actual `A,d,V` source binding;
3. nonemptiness or coverage of a deployed cell;
4. that the same cell carries the T-P5-196 fixed-sign generator packet;
5. that actual amplitude slopes satisfy the declared `beta>=b`;
6. any Float64/interval or controller/PDE/ODE semantic inclusion;
7. the T-P5-198 quadratic/ellipsoidal-domain branch;
8. global selector or trajectory coverage;
9. copositivity of the final combined Lyapunov matrix;
10. Lean/kernel compilation;
11. independent verification by 封不觉;
12. admission or registry eligibility.

All remain OPEN.

---

## 14. Recommended next mathematical bridge

After T-P5-198 and T-P5-199, the domain-to-quadratic-absorption bottleneck splits cleanly by domain representation.

A useful next non-overlapping mathematical child is **mixed-domain intersection support**:

`y>=0`,

`A V y<=d`,

`y^T P y<=rho`.

The question is whether the amplitude support bound `beta^T y<=B` can be certified more sharply than either the pure-polyhedral T-P5-199 dual or the pure-quadratic T-P5-198 certificate, while still producing a finite exact certificate and preserving fail-closed recession handling.

Do not start that child until T-P5-198's exact statement is available, because the useful mixed certificate should compose rather than duplicate its quadratic-domain machinery.
