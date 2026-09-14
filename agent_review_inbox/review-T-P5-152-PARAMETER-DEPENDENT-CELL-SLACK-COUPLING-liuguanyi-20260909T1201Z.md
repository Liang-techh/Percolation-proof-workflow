---
kind: review_result
review_id: review-T-P5-152-parameter-dependent-cell-slack-coupling-liuguanyi-20260909T1201Z
task_id: T-P5-152-PARAMETER-DEPENDENT-CELL-SLACK-COUPLING
reviewer: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-09T12:01:00Z
claim_commit: 1e9516f0b12a556e89a21c662ac986e0621d7d96
inspected_commit: bc84a85e7aa2caadffdd87e920521a660b2f9a95
upstream_reviews:
  - path: agent_review_inbox/review-T-P5-151-VERTEXWISE-END-TO-END-ROBUST-RESET-honglianmozun-20260909T1150Z.md
    commit: 0b8117e5f6b829f1e6bc161d1e0cb80ee2fd3671
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: allow_affine_parameter_dependent_quadratic_cells_only_when_vertex_gap_multipliers_are_coupled_through_the_same_affine_cell_slack; use_common_tau_as_the_zero-overhead_route; otherwise_require_a_second_stage_quadratic_slack_coupling_PSD_certificate_before_taking_the_vertexwise_scalar_max
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: none; exact finite-dimensional convex-combination and quadratic-slack algebra only
exit_code: n/a
---

# T-P5-152 — parameter-dependent cell slack coupling

## 0. Narrow seam and non-overlap

T-P5-151 proves that, on one **common** physical quotient cell, each uncertainty vertex may use its own augmented residual cap and its own cell multiplier, and only the final scalar reset floor needs to be shared.

T-P5-151 also explicitly leaves open the case in which the physical admissible cell itself depends on the uncertainty parameter. That restriction is real: once the cell varies, a state can be feasible for an interior uncertainty value while being outside one or more vertex cells, so vertexwise cell-valid inequalities cannot simply be convex-combined.

This review closes exactly that mathematical seam.

The key observation is:

> when both the reset family and the cell slack are affine in the same uncertainty weights, the quantity that must survive convexification is not the vertex multiplier itself but the **signed weighted cell slack**.

A common multiplier makes that weighted slack equal to the interior cell slack times one nonnegative scalar and therefore gives a zero-overhead bridge. More generally, distinct vertex multipliers remain valid only if a second-stage quadratic slack-coupling certificate proves that their weighted slack is nonnegative on the interior cell.

No deployed source binding, coverage promotion, provenance/admission audit, Lean/kernel claim, Float64/runtime claim, or registry mutation is made.

---

## 1. Abstract affine-family setup

Let the uncertainty point be represented by barycentric weights

`lambda_j >= 0`, `sum_j lambda_j = 1`.

For each vertex `j`, let

- `f_j(e,m)` be the full reset/Lyapunov increment to upper-bound;
- `c_j(m)` be the signed physical-cell slack, with the convention

  `c_j(m) >= 0`  iff  `m` is feasible for vertex `j`;

- `E_j` be a scalar vertex floor;
- `tau_j >= 0` be a proof multiplier.

Assume the uncertainty interpolation is exact at the level of the **original signed objects**:

**(1.1)**

`f_lambda(e,m) = sum_j lambda_j f_j(e,m)`,

**(1.2)**

`c_lambda(m) = sum_j lambda_j c_j(m)`.

Assume also that each vertex proof has a globally valid gap inequality

**(1.3)**

`E_j - f_j(e,m) >= tau_j c_j(m)`

for every `(e,m)`, not merely for states inside the vertex cell.

In T-P5-151 this global inequality is exactly what remains after the residual square and quotient-completion square are discarded from the nonnegative gap decomposition.

Define

**(1.4)** `E_lambda := sum_j lambda_j E_j`,

and the weighted multiplier slack

**(1.5)**

`h_lambda(m) := sum_j lambda_j tau_j c_j(m)`.

Then summing (1.3) gives the exact master inequality

**(1.6)**

`E_lambda - f_lambda(e,m) >= h_lambda(m)`.

Therefore the entire parameter-dependent-cell problem has been reduced to one question:

**(1.7)**

`c_lambda(m) >= 0  ==>  h_lambda(m) >= 0`.

This is the missing bridge behind T-P5-151's common-cell caveat.

---

## 2. Main abstract theorem: slack coupling is sufficient

### Theorem A — affine reset plus affine cell plus coupled signed slack

Assume (1.1)--(1.3). Fix one uncertainty weight vector `lambda`.

If

**(2.1)**

`h_lambda(m) >= 0`

for every `m` satisfying `c_lambda(m)>=0`, then

**(2.2)**

`f_lambda(e,m) <= E_lambda`

for every `e` and every `m` feasible for the interior uncertainty value.

Consequently any common scalar `E` satisfying

**(2.3)** `E >= E_j` for every vertex `j`

also satisfies

**(2.4)**

`f_lambda(e,m) <= E`

on every parameter-dependent cell for which (2.1) is certified.

### Proof

From (1.6), feasibility and (2.1) give

`E_lambda - f_lambda >= h_lambda >= 0`.

Hence `f_lambda<=E_lambda`. Since `E_lambda` is a convex combination of the `E_j`, `E_lambda<=max_j E_j<=E`.

QED.

The theorem is elementary, but it identifies the exact mathematical object that has to be transported across the uncertainty/cell interface.

---

## 3. Zero-overhead route: one common multiplier

Suppose all vertices use the same nonnegative multiplier

**(3.1)** `tau_j = tau >= 0`.

Then, by affine cell interpolation,

**(3.2)**

`h_lambda = sum_j lambda_j tau c_j`

`= tau sum_j lambda_j c_j`

`= tau c_lambda`.

Therefore interior feasibility `c_lambda>=0` immediately gives `h_lambda>=0`.

### Corollary B — common-multiplier parameter-dependent-cell theorem

Under (1.1)--(1.3), if all vertices share one `tau>=0`, then the T-P5-151 scalar robustification remains valid even when the physical cell varies affinely with uncertainty.

No common `G`, no common radius, and no common vertex completion vector are required. The only shared proof datum is the scalar multiplier `tau` attached to the same affine cell-slack family.

This is the shortest safe adapter for parameter-dependent cells.

---

## 4. Why T-P5-151 allowed distinct multipliers on a common cell

The common-cell case is a special algebraic degeneracy.

If every vertex has exactly the same slack

`c_j = c`,

then

**(4.1)**

`h_lambda = (sum_j lambda_j tau_j) c`.

The effective interior multiplier is simply

**(4.2)** `tau_lambda := sum_j lambda_j tau_j >= 0`.

Thus distinct `tau_j` are harmless on a common cell.

More generally, if

**(4.3)** `c_j = alpha_j c`

with `alpha_j>=0`, then any nonnegative `tau_j` remain safe: whenever `c_lambda=(sum lambda_j alpha_j)c>=0`, either the active scale is zero and `h_lambda=0`, or `c>=0`, in which case

`h_lambda=(sum lambda_j tau_j alpha_j)c>=0`.

So the real invariant is not equality of the textual cell description; it is nonnegative proportionality of the **signed slack**.

---

## 5. Centered ellipsoids: checker-friendly exact coupling gate

Now specialize to centered parameter-dependent ellipsoids

**(5.1)**

`c_j(m) := R_j - m^T G_j m`,

with symmetric `G_j` and scalar `R_j`.

Define the affine interior cell

**(5.2)**

`R_lambda := sum_j lambda_j R_j`,

**(5.3)**

`G_lambda := sum_j lambda_j G_j`,

so

**(5.4)**

`c_lambda(m)=R_lambda-m^T G_lambda m`.

For distinct vertex multipliers define

**(5.5)**

`a_lambda := sum_j lambda_j tau_j R_j`,

**(5.6)**

`B_lambda := sum_j lambda_j tau_j G_j`.

Then

**(5.7)**

`h_lambda(m)=a_lambda-m^T B_lambda m`.

### Theorem C — second-stage scalar/PSD slack-coupling certificate

If the producer supplies a scalar `rho_lambda>=0` such that

**(5.8)**

`rho_lambda G_lambda - B_lambda >= 0`

in Loewner order, and

**(5.9)**

`a_lambda - rho_lambda R_lambda >= 0`,

then

**(5.10)**

`c_lambda(m)>=0  ==>  h_lambda(m)>=0`.

### Exact proof

The signed weighted slack has the decomposition

**(5.11)**

`h_lambda(m)`

`= rho_lambda c_lambda(m)`

`  + (a_lambda-rho_lambda R_lambda)`

`  + m^T(rho_lambda G_lambda-B_lambda)m`.

Every term on the right is nonnegative on the interior cell.

QED.

This is completely inverse-free and root-free. A trusted exact-rational checker needs only affine sums, one scalar nonnegativity check, and one PSD check.

### Common multiplier is the equality case

If `tau_j=tau` for all `j`, then

`a_lambda=tau R_lambda`,

`B_lambda=tau G_lambda`.

Taking `rho_lambda=tau` makes both (5.8) and (5.9) exact equalities.

So Corollary B is literally the zero-defect case of Theorem C.

---

## 6. Exactness of the centered coupling gate on a proper ellipsoid

Theorem C is sufficient without any strictness assumption. On a proper centered ellipsoid it is also lossless.

Assume

**(6.1)** `G_lambda > 0`,

**(6.2)** `R_lambda > 0`.

Then the following are equivalent:

1. `h_lambda(m)>=0` for every `m` with `m^T G_lambda m<=R_lambda`;
2. there exists `rho_lambda>=0` satisfying (5.8)--(5.9).

### Proof sketch without matrix inverse in the checker

Because `G_lambda>0`, the generalized Rayleigh quotient

`m^T B_lambda m / (m^T G_lambda m)`

attains a finite maximum `L` on the `G_lambda`-unit sphere.

If `L<=0`, then `B_lambda<=0`. Feasibility at `m=0` implies `a_lambda>=0`, so `rho_lambda=0` works.

If `L>0`, choose a maximizing direction and scale it to the boundary `m^T G_lambda m=R_lambda`. The assumed nonnegativity of `h_lambda` gives

`a_lambda >= R_lambda L`.

Taking `rho_lambda=L` gives

`B_lambda <= rho_lambda G_lambda`

and

`a_lambda >= rho_lambda R_lambda`.

Thus (5.8)--(5.9) hold.

The checker never needs to compute `L`; the producer may propose a rational `rho_lambda` and the trusted side verifies only the polynomial/PSD gates.

---

## 7. General quadratic cells, including moving centers

The centered theorem is enough for many P5 packets, but a reference-knot or chart update may move the ellipsoid center. It is cleaner to expand the cell into a signed quadratic rather than transport center labels informally.

Write each vertex slack as

**(7.1)**

`c_j(m)=r_j + 2 d_j^T m - m^T G_j m`.

A shifted ellipsoid

`R_j-(m-a_j)^T G_j(m-a_j)`

has

`r_j=R_j-a_j^T G_j a_j`,

`d_j=G_j a_j`.

Define the affine combinations

`r_lambda=sum lambda_j r_j`,

`d_lambda=sum lambda_j d_j`,

`G_lambda=sum lambda_j G_j`,

and the multiplier-weighted combinations

`r_tau=sum lambda_j tau_j r_j`,

`d_tau=sum lambda_j tau_j d_j`,

`G_tau=sum lambda_j tau_j G_j`.

Then

`c_lambda=r_lambda+2d_lambda^Tm-m^TG_lambda m`,

`h_lambda=r_tau+2d_tau^Tm-m^TG_tau m`.

### Theorem D — homogenized quadratic slack-coupling PSD gate

If `rho_lambda>=0` and the augmented matrix

**(7.2)**

`M_lambda(rho_lambda) :=`

`[[ r_tau-rho_lambda r_lambda,`

`   (d_tau-rho_lambda d_lambda)^T ],`

` [ d_tau-rho_lambda d_lambda,`

`   rho_lambda G_lambda-G_tau ]]`

is PSD, then

**(7.3)**

`h_lambda(m) - rho_lambda c_lambda(m)`

`= [1;m]^T M_lambda(rho_lambda) [1;m] >= 0`.

Hence `c_lambda>=0` implies `h_lambda>=0`, and Theorem A applies.

This is the natural typed contract for moving centers: transport the **expanded signed quadratic slack**, not merely `(center,radius,metric)` as unrelated fields.

Under the usual strict-feasibility hypothesis for one quadratic constraint, the classical one-constraint S-lemma makes this second-stage multiplier representation lossless. The trusted theorem itself requires only the explicit PSD implication above; no appeal to the S-lemma is needed to verify a supplied packet.

---

## 8. Instantiation with T-P5-151 vertex reset certificates

For each uncertainty vertex `j`, suppose T-P5-151 or T-P5-149 provides a fixed-vertex residual cap and a quotient completion yielding coefficients `(C_j,b_j,H_j)`.

Let the vertex cell be

`c_j(m)=R_j-m^TG_jm`.

Choose `tau_j>=0`, define

**(8.1)** `K_j:=H_j+tau_j G_j`,

assume

**(8.2)** `K_j>=0`,

and provide

**(8.3)** `K_j y_j=b_j`.

Let

**(8.4)**

`E_j:=C_j+tau_jR_j+(1/4)b_j^Ty_j`.

Then the same square completion as T-P5-151 gives globally

**(8.5)**

`E_j-f_j(e,m)`

`>= tau_j c_j(m)`.

Therefore:

- if all `tau_j` are equal, robust closure over the affine parameter-dependent cell follows immediately;
- if the `tau_j` differ, closure follows whenever Theorem C or D supplies the second-stage slack-coupling certificate;
- if neither condition is available, the vertex floors cannot be safely maxed merely because each is valid on its own vertex cell.

The final robust scalar may still be taken as

**(8.6)** `E=max_j E_j`.

A parameter-aware consumer may retain the sharper affine certificate floor

**(8.7)** `E_lambda=sum_j lambda_jE_j`.

---

## 9. Hard counterexample: unrelated vertex multipliers fail

This example is exact and one-dimensional. There is no residual variable `e`.

Take vertex 1:

**(9.1)**

`c_1(m)=1-m^2`,

`f_1(m)=m^2-1=-c_1(m)`.

The sharp vertex floor is `E_1=0`, with exact multiplier `tau_1=1`:

`E_1-f_1=c_1`.

Take vertex 2:

**(9.2)**

`c_2(m)=9-m^2`,

`f_2(m)=0`.

The sharp vertex floor is `E_2=0`, with `tau_2=0`:

`E_2-f_2=0`.

Both vertex certificates are exact and lossless on their own cells.

Now choose the interior uncertainty weight

`lambda_1=lambda_2=1/2`.

The interpolated cell is

**(9.3)**

`c_lambda(m)=5-m^2`.

The interpolated reset is

**(9.4)**

`f_lambda(m)=(1/2)(m^2-1)`.

At the feasible boundary state `m^2=5`,

**(9.5)**

`f_lambda=2`,

while

`max(E_1,E_2)=0`.

Thus sharp vertex floors do **not** robustify over an affinely moving cell.

The failed weighted slack is

**(9.6)**

`h_lambda=(1/2)(1-m^2)`,

which equals `-2` at `m^2=5`.

Theorem C detects the obstruction exactly. Here

`G_lambda=1`, `R_lambda=5`,

`B_lambda=1/2`, `a_lambda=1/2`.

Any coupling multiplier would need simultaneously

`rho_lambda >= 1/2`

and

`1/2 >= 5 rho_lambda`,

which is impossible.

This is not a source/provenance issue; it is a mathematical failure of the uncoupled interface.

---

## 10. A common shape is not enough

The counterexample above already has

`G_1=G_2=1`.

Only the radius changes.

Therefore sharing the same ellipsoid metric/shape does **not** justify independent vertex multipliers. The full signed slack, including the radius/offset term, must participate in the uncertainty interpolation.

Likewise, sharing a radius while changing the metric is not enough in general.

This is important for typed source packets: equality of `metricKey` alone is weaker than equality/proportionality of the complete `cellSlackKey`.

---

## 11. Robust sharpness interpretation

Suppose every vertex floor `E_j` is the true supremum of `f_j` on its own vertex cell.

Without slack coupling, `max_jE_j` need not equal or even upper-bound the robust supremum; section 9 shows this.

If Theorem A's coupling condition holds for every uncertainty point, then

`sup_{lambda,e,m:c_lambda>=0} f_lambda <= max_jE_j`.

The reverse inequality holds because every uncertainty vertex is itself allowed and its own cell is recovered there. Hence

**(11.1)**

`sup_{lambda,e,m:c_lambda>=0} f_lambda = max_j E_j`.

So, once the signed slack coupling is proved, sharp vertex floors again imply a sharp robust floor even for parameter-dependent cells.

The obstruction is therefore exactly the cell-slack coupling, not convex uncertainty by itself.

---

## 12. Checker-friendly theorem surface

A future exact checker can consume one of three routes.

### Route A — common multiplier

For all uncertainty vertices:

- exact affine reset/cell identities;
- vertex global gap certificate `E_j-f_j >= tau c_j` with one shared `tau>=0`.

Then no second-stage matrix is required.

### Route B — centered cell, distinct multipliers

For the chosen uncertainty weights:

- `R_lambda=sum lambda_jR_j`;
- `G_lambda=sum lambda_jG_j`;
- `a_lambda=sum lambda_jtau_jR_j`;
- `B_lambda=sum lambda_jtau_jG_j`;
- proposed `rho_lambda>=0`;
- exact gates

  `rho_lambda G_lambda-B_lambda >=0`,

  `a_lambda-rho_lambda R_lambda>=0`.

Then `f_lambda<=sum lambda_jE_j` on the interior cell.

### Route C — general quadratic cell

Use expanded slack coefficients `(r_j,d_j,G_j)` and verify the single augmented PSD block (7.2).

All routes are inverse-free and root-free once the producer supplies rational witnesses.

---

## 13. Minimal theorem statements for formalization

### Leaf A — affine gap summation

Assumptions:

- `lambda_j>=0`, `sum lambda_j=1`;
- `f=sum lambda_jf_j`;
- `c=sum lambda_jc_j`;
- `E_j-f_j>=tau_jc_j`.

Conclusion:

`sum lambda_jE_j - f >= sum lambda_jtau_jc_j`.

This is linear ordered-ring algebra.

### Leaf B — common multiplier transport

Assumptions:

- Leaf A;
- all `tau_j=tau>=0`;
- `c>=0`.

Conclusion:

`f<=sum lambda_jE_j`.

### Leaf C — centered quadratic slack coupling

Assumptions:

- `c=R-m^TGm`;
- `h=a-m^TBm`;
- `rho>=0`;
- `rho G-B>=0`;
- `a-rho R>=0`;
- `c>=0`.

Conclusion:

`h>=0`.

Proof is identity (5.11).

### Leaf D — homogenized moving-center coupling

Assumptions:

- `c=r+2d^Tm-m^TGm`;
- `h=r_tau+2d_tau^Tm-m^TG_tau m`;
- augmented matrix (7.2) PSD;
- `rho>=0`, `c>=0`.

Conclusion:

`h>=0`.

These leaves are independent of P5 source admission and should remain reusable as generic finite-dimensional interface mathematics.

---

## 14. Structural fingerprint

This child adds a refinement to the T-P5-151 fingerprint:

**affine uncertainty + moving feasible cell => robustify the signed proof slack, not only the reset value.**

The safe order is

1. preserve the original vertex reset and vertex cell slack as signed objects;
2. form the vertex proof gap before taking absolute values;
3. transport both reset and cell slack with the same barycentric weights;
4. prove weighted multiplier slack is nonnegative on the interior cell;
5. only then take the common scalar reset floor.

A common cell makes step 4 automatic even with distinct multipliers. A moving cell does not.

---

## 15. Open boundaries after this child

Still open:

- actual source/runtime uncertainty polytope and exact barycentric/affine identity;
- proof that the deployed residual map and deployed cell slack use the **same uncertainty parameterization**;
- actual source-derived `(G_j,R_j)` or expanded `(r_j,d_j,G_j)` cell packets;
- actual T-P5-151 vertex caps/range solves and quotient coefficients;
- whether one common `tau` exists with acceptable floors, or whether distinct `tau_j` require a nontrivial second-stage `rho` certificate;
- robust checking of Route B/C over a continuum of uncertainty weights when no analytic common-`tau` simplification is available;
- parameter-dependent chart/reference-knot composition beyond one quadratic slack family;
- Float64/directed-rounding semantics;
- P8/flowpipe and same-tube/path coverage;
- Lean/kernel formalization and independent validation by 封不觉;
- provenance/admission/registry/P5 parent closure.

In particular, a finite list of vertex cell certificates is not by itself a robust cell certificate for interior uncertainty points.

---

## 16. Requested handoff

The shortest safe producer packet for a parameter-dependent cell is now:

`(uncertaintyKey, cellSlackFamilyKey, resetKey, {f_j,c_j,E_j,tau_j})`

with exact affine identities

`f_lambda=sum lambda_jf_j`,

`c_lambda=sum lambda_jc_j`.

Preferred route:

- choose one shared `tau>=0` across all vertices.

Fallback route for centered ellipsoids:

- keep vertex-specific `tau_j`;
- provide `rho_lambda` and exact checks

  `rho_lambda G_lambda-B_lambda >=0`,

  `a_lambda-rho_lambdaR_lambda>=0`.

Fallback route for moving-center/general quadratic cells:

- expand the signed slack and provide the augmented PSD gate (7.2).

Only after this coupling is established may the consumer safely use

`E=max_jE_j`

as the robust scalar reset floor over a parameter-dependent feasible cell.