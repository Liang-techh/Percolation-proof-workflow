---
kind: review_result
task_id: T-P4-020E-ENERGY-BETA
agent: 红莲魔尊
source_agent: 红莲魔尊
status: pending
parent_tasks:
  - T-P4-020
claim_file: agent_review_inbox/claim-T-P4-020E-energy-beta-honglianmozun-20260908T0752.md
depends_on:
  - B45SchurResidualRepair.schur_remainder_bound
  - T-P5-044
  - T-P5-051
  - T-P4-034
scope: mathematics_only_energy_side_beta_consumption_of_schur_remainder
---

# T-P4-020E — Schur remainder → Lyapunov beta contract

## 0. Scope / non-overlap

This child does **not** redo the one-cell sharp Schur/remainder enclosure, source interval arithmetic, Float64 rounding, partition construction, 5×5 PMI source binding, or Lean implementation owned by the main T-P4-020 lane. It treats the Schur lane's output as an upstream hypothesis and asks only: **what exact one-sided information must be exported so that an energy/Lyapunov consumer can absorb the remainder and affine residual without losing more coercivity than necessary?**

The answer is a small 2×2 algebraic interface, together with a precise obstruction showing that a determinant margin alone is not enough for an affine-forced energy estimate.

## 1. Reference block and dual quadratic

Let

- `u = (x,y)`,
- `D0(u) = a x^2 + 2 b x y + c y^2`,
- `Delta = a*c - b^2`,
- assume `a > 0` and `Delta > 0`.

Then `D0` is positive definite. For an affine residual / evaluator forcing `e=(e1,e2)`, define the adjugate-dual quadratic

`N0(e) = c e1^2 - 2 b e1 e2 + a e2^2`.

The basic scaled completion needed below is

`-lambda D0(u) - e·u <= N0(e)/(4 lambda Delta)`

for every `lambda>0`.

A division-free SOS witness is obtained by defining

`z1 = 2 lambda (a x + b y) + e1`,

`z2 = 2 lambda (b x + c y) + e2`.

Then the exact polynomial identity is

`c z1^2 - 2 b z1 z2 + a z2^2`

`= 4 lambda^2 Delta D0(u) + 4 lambda Delta (e1 x + e2 y) + N0(e)`.

Moreover

`a (c z1^2 - 2 b z1 z2 + a z2^2)`

`= (a z2 - b z1)^2 + Delta z1^2 >= 0`.

Thus the whole consumer can be formalized with ring identities, square nonnegativity, and ordered-field arithmetic; no inverse matrix, eigenvalue, or square-root API is mathematically required.

## 2. Preferred handoff: one-sided relative Schur loss

Suppose the actual energy contribution has the form

`-D0(u) + R_S(u) - e·u`,

and the Schur lane proves the **one-sided** relative estimate

`R_S(u) <= theta D0(u)`

with `0 <= theta < 1`. Define the surviving coercivity

`m = 1 - theta > 0`.

The sign is important: a negative Schur remainder is beneficial, so the energy consumer does **not** need `|R_S| <= theta D0`; the one-sided upper bound is strictly sharper.

### Theorem A — relative Schur-loss affine absorption

For any `lambda` with `0 < lambda <= m`,

`-D0(u) + R_S(u) - e·u`

`<= -(m-lambda) D0(u) + N0(e)/(4 lambda Delta)`.

Proof: `-D0+R_S <= -m D0`; split

`-m D0 = -(m-lambda)D0 - lambda D0`

and apply the scaled completion above to `-lambda D0-e·u`.

A fully division-free beta gate is therefore:

if

`N0(e) <= 4 lambda Delta beta`,

then

`-D0 + R_S - e·u <= -(m-lambda)D0 + beta`.

### Exact retained-dissipation / beta frontier

If the downstream theorem wants to retain a prescribed reference dissipation coefficient `rho` with

`0 <= rho < m`,

set `lambda = m-rho`. Then

`-D0 + R_S - e·u`

`<= -rho D0(u) + N0(e)/(4 (m-rho) Delta)`.

Equivalently, a target additive charge `beta` is certified by the polynomial inequality

`N0(e) <= 4 (m-rho) Delta beta`.

This is the exact Pareto frontier available from the information `(theta,H0,e)` alone:

- `rho=0` gives the smallest additive affine charge `N0(e)/(4mDelta)` but spends all surviving reference dissipation;
- increasing `rho` preserves more dissipation and necessarily raises the worst-case charge;
- the charge diverges as `rho -> m` unless `e=0`.

The frontier is worst-case sharp at this information level: if `R_S = theta D0` saturates the one-sided Schur bound, the affine completion itself is attained at the usual translated quadratic minimizer.

## 3. Fallback handoff: additive Schur remainder

If the upstream certificate can only be typed into the Lyapunov derivative as

`R_S(u) <= r_S`

for a scalar `r_S >= 0`, then for every `0 < lambda <= 1`,

`-D0(u) + R_S(u) - e·u`

`<= -(1-lambda) D0(u) + r_S + N0(e)/(4 lambda Delta)`.

Thus the legal Lyapunov budget is

`beta_total = r_S + beta_affine`,

with division-free affine gate

`N0(e) <= 4 lambda Delta beta_affine`.

This fallback is weaker near the equilibrium: a nonzero constant `r_S` produces a first-exit / ultimate-ball budget even when `u=0`. Therefore, whenever the Schur remainder is genuinely state-quadratic, exporting the **relative** estimate `R_S<=theta D0` is mathematically preferable to replacing it prematurely by a cellwise constant.

### Relation to `B45SchurResidualRepair`

`B45SchurResidualRepair.schur_remainder_bound` currently gives an algebraic scalar inequality of the form

`betaMin * sqNorm(blockResidual) <= betaMin * gamma`

under its stated nonnegativity and squared-residual hypotheses. This is a useful upstream budget, but `gamma` itself is still a **squared residual budget**, not automatically a Lyapunov `beta`.

A typed bridge must first establish that the scalar on the left is exactly (or upper-bounds) a `+R_S` contribution in the same Lyapunov derivative and with the correct sign/units. Only after that bridge is proved may `betaMin*gamma` be consumed as an additive `r_S`. If instead the source theorem can compare that Schur contribution directly with `D0(u)`, then Theorem A should be used instead.

## 4. Signed error rectangles: four exact corner checks suffice

Suppose the source lane gives a signed outward rectangle

`L1 <= e1 <= U1`,

`L2 <= e2 <= U2`.

Because `N0(e1,e2)` is separately convex in each coordinate (`a>0` and, from `a>0, Delta>0`, also `c>0`), its maximum on the rectangle occurs at a corner. Hence it is enough to check the four exact-rational inequalities

`N0(r1,r2) <= 4 lambda Delta beta_affine`

for

`r1 in {L1,U1}`, `r2 in {L2,U2}`.

Combining with the relative Schur theorem gives the uniform cell statement

`-D0 + R_S - e·u <= -(m-lambda)D0 + beta_affine`.

Combining with the additive Schur theorem gives

`-D0 + R_S - e·u <= -(1-lambda)D0 + r_S + beta_affine`.

This is the exact energy-side consumer shape for a signed O2 error rectangle; there is no need to discard signs before forming the adjugate quadratic.

## 5. First-exit gates

Assume on a barrier `V=Vstar` that

`Vdot <= -gammaV V - D0(u) + R_S(u) - e·u + beta0`.

### Relative Schur-loss branch

If `R_S<=theta D0`, `m=1-theta`, and `0<lambda<=m`, then it suffices that

`gammaV * Vstar > beta0`

and

`N0(e) < 4 lambda Delta (gammaV*Vstar - beta0)`.

Then `Vdot<0` on the barrier. If no retained `D0` term is needed by a later consumer, choosing `lambda=m` maximizes the affine-error allowance.

For a signed error rectangle, replace the single inequality by the same strict inequality at all four corners.

### Additive Schur branch

If only `R_S<=r_S` is available, it suffices that

`gammaV * Vstar > beta0 + r_S`

and, for some `0<lambda<=1`,

`N0(e) < 4 lambda Delta (gammaV*Vstar - beta0 - r_S)`.

Again `lambda=1` gives the weakest affine gate when no residual `D0` coefficient must be retained.

## 6. Exact obstruction: determinant margin alone is not an energy-beta certificate

A Schur/PMI lane must **not** hand the energy consumer only a determinant lower bound and expect a uniform affine beta to follow.

Fix any `delta>0` and consider

`H_M = diag(M, delta/M)`, `M>0`.

Then

`det(H_M)=delta`

for every `M`, so the determinant margin is identical across the family. But for the fixed forcing direction

`e=(0,1)`,

the sharp affine charge is

`(1/4) e^T H_M^{-1} e = M/(4 delta) -> infinity`.

Equivalently, the adjugate numerator is `N_M(e)=M` while `Delta=delta` remains fixed.

Therefore a determinant certificate alone contains insufficient directional/coercivity information to determine any uniform finite affine-error beta. The energy handoff must provide at least one of:

1. the actual effective 2×2 coefficients, enough to evaluate both `Delta` and the dual numerator `N(e)`;
2. an explicit comparison `H_eff >= m H0` with `m>0` against a known positive-definite reference block `H0` (the preferred contract above);
3. an equivalent coercivity / pivot / scale packet strong enough to bound the inverse action in the forcing directions.

This is a genuine mathematical information obstruction, not looseness from Young's inequality.

## 7. Failure boundaries

1. **All coercivity consumed (`m=0`).** A generic nonzero fixed affine forcing cannot be absorbed while retaining homogeneous global decay. Singular range-compatible exceptions require separate kernel/range structure; they are not supplied by a scalar Schur-loss budget.

2. **Negative curvature.** If the effective quadratic form has a direction `v` with `v^T H_eff v<0`, then along `u=t v` the term `-u^T H_eff u-e·u` tends to `+infinity`; no finite global additive beta exists.

3. **Zero beta with nonzero forcing.** For positive-definite `H0`, `N0(e)>0` whenever `e!=0`, so an absolute nonzero affine forcing cannot be silently absorbed with `beta=0`.

4. **Additive versus relative Schur budget is not a cosmetic distinction.** Replacing a state-quadratic `R_S<=theta D0` by `R_S<=r_S` destroys the zero-slice property at `u=0` and turns a homogeneous decay statement into an ultimate-ball / first-exit statement.

5. **Squared-residual budget is not yet an energy term.** A bound `||r||^2<=gamma` must first be connected, with sign and coefficient, to the actual scalar Schur contribution appearing in `Vdot`; otherwise treating `gamma` as `beta` is a type/units error.

## 8. Candidate theorem statements for a later Lean lane

Minimal algebraic children suggested by this review:

- `relative_schur_affine_energy_absorption`
- `relative_schur_beta_gate`
- `relative_schur_retained_dissipation_pareto`
- `additive_schur_affine_energy_absorption`
- `schur_signed_rectangle_beta_gate`
- `schur_first_exit_beta_gate_relative`
- `schur_first_exit_beta_gate_additive`
- `determinant_margin_alone_not_affine_beta_sufficient`

The core proofs can be organized around the displayed adjugate SOS identity and should need only ring normalization, `sq_nonneg`, positivity of `a,Delta,lambda`, and ordered-field arithmetic.

## 9. Exact handoff requested from the main T-P4-020 lane

For each certified cell, the energy side can consume either of the following, in descending order of preference:

**Preferred relative packet**

- exact/certified reference coefficients `(a,b,c)` with `a>0`, `Delta=ac-b^2>0`;
- a one-sided relative Schur-loss certificate `R_S(u)<=theta D0(u)` with exact/certified `0<=theta<1`;
- signed affine residual/error set, preferably a rectangle or stronger correlated set, in the same `(4,5)` coordinates.

**Fallback additive packet**

- the same positive-definite reference block;
- a typed scalar `r_S` satisfying `R_S(u)<=r_S` in the actual Lyapunov derivative;
- the signed affine residual/error set.

A determinant margin alone, or a raw squared-residual `gamma` without the scalar energy bridge, is insufficient.

## 10. Status / not claimed

`pending mathematical child`.

No concrete P4 cell is claimed closed. No DH/Float64/libm/interval evaluator, one-cell Schur calculation, partition coverage, 5×5 PMI source binding, ODE/flowpipe, provenance, receipt, admission, or parent-task closure is claimed here.
