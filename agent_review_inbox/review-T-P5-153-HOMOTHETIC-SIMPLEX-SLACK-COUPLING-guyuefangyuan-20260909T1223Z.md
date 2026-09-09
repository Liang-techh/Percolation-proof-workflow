---
kind: review_result
review_id: review-T-P5-153-homothetic-simplex-slack-coupling-guyuefangyuan-20260909T1223Z
task_id: T-P5-153-HOMOTHETIC-SIMPLEX-SLACK-COUPLING
reviewer: 古月方源
source_agent: 古月方源
created_at: 2026-09-09T12:23:00Z
claim_commit: 360faf9205d55b175240ce110bb2fb63c6fad1d8
inspected_commit: 125ef333fe17e0a012c5c1682ea6c44f83c04c9c
upstream_reviews:
  - path: agent_review_inbox/review-T-P5-152-PARAMETER-DEPENDENT-CELL-SLACK-COUPLING-liuguanyi-20260909T1201Z.md
    commit: 49dd8628383fae302ddba40c7268e06046f5ca9c
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_an_exact_simplex_wide_no_per_parameter_SDP_route_for_homothetic_quadratic_cells; use_pairwise_tau_vs_effective_radius_order_as_the_exact_zero_additive_floor_gate; when_it_fails_use_the_cross_multiplied_additive_deficit_gate; retain_general_matrix_pairwise_PSD_only_as_a_sufficient_shortcut
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: none; exact finite-dimensional ordered-field and quadratic-form algebra only
exit_code: n/a
---

# T-P5-153 — homothetic simplex-wide slack coupling

## 0. Narrow seam and non-overlap

T-P5-152 reduces a parameter-dependent feasible-cell problem to the signed slack implication

`c_lambda(m) >= 0  ==>  h_lambda(m) >= 0`,

where `c_lambda` is the interpolated physical-cell slack and `h_lambda` is the barycentrically weighted multiplier slack. It gives a pointwise-in-`lambda` centered-ellipsoid Route B using a scalar `rho_lambda`, but explicitly leaves open robust checking over a continuum of simplex weights when no common multiplier is available.

This child closes that continuum problem **exactly** for the smallest nontrivial analytic family: centered homothetic ellipsoids. It also gives one broader pairwise-PSD shortcut for general quadratic cells, clearly marked as sufficient rather than exact.

No source/admission/provenance audit, receipt work, runtime/Float64 claim, coverage promotion, or registry mutation is performed.

---

## 1. Homothetic cell family

Fix one nonnegative quadratic form

`Q(m) >= 0`.

For each uncertainty vertex `j`, write the signed cell slack as

**(1.1)** `c_j(m) = r_j - g_j Q(m)`,

with

**(1.2)** `g_j > 0`,

and let the already-proved vertex gap multiplier satisfy

**(1.3)** `tau_j >= 0`.

This includes centered homothetic ellipsoids

`G_j = g_j G0`, `R_j = r_j`, `Q(m)=m^T G0 m`.

For simplex weights `lambda_j>=0`, `sum lambda_j=1`, define

**(1.4)**

`g = sum_j lambda_j g_j`,

`r = sum_j lambda_j r_j`,

`b = sum_j lambda_j tau_j g_j`,

`a = sum_j lambda_j tau_j r_j`.

Then

**(1.5)** `c_lambda(m)=r-g Q(m)`,

and

**(1.6)** `h_lambda(m)=a-b Q(m)`.

Because every `g_j>0`, one has `g>0`; because every `tau_j>=0` and `g_j>0`, one has `b>=0`.

---

## 2. Main exact division-free identity

Define the determinant-like scalar

**(2.1)** `Delta_lambda := a g - b r`.

Then there is an exact identity

**(2.2)**

`g h_lambda = Delta_lambda + b c_lambda`.

Indeed,

`Delta_lambda + b c_lambda`

`= (a g-b r)+b(r-gQ)`

`= g(a-bQ)`

`= g h_lambda`.

Therefore:

### Theorem A — homothetic slack coupling without `rho`

If

- `g>0`,
- `b>=0`,
- `c_lambda(m)>=0`,
- `Delta_lambda>=0`,

then

**(2.3)** `h_lambda(m)>=0`.

The proof is purely ordered-ring algebra: the right-hand side of (2.2) is nonnegative, hence `g h_lambda>=0`; since `g>0`, `h_lambda>=0`.

This theorem removes the per-parameter `rho_lambda` search entirely. A trusted rational checker only needs affine sums, products, and sign checks.

---

## 3. Exact relation to T-P5-152 Route B

For homothetic centered cells,

`G_lambda = g G0`,

`B_lambda = b G0`.

T-P5-152 Route B asks for some `rho>=0` such that

**(3.1)** `(rho g-b) G0 >= 0`,

**(3.2)** `a-rho r >= 0`.

For a proper cell with `g>0`, `r>0`, and nonzero positive shape `G0`, existence of such a `rho` is equivalent to

**(3.3)** `Delta_lambda = a g-b r >= 0`.

Necessity follows by multiplying the scalar inequalities `rho g>=b` and `a>=rho r`:

`a g >= rho r g >= b r`.

For sufficiency one may choose the rational witness `rho=b/g`; however the trusted theorem does not need to divide. Identity (2.2) already proves the cell implication directly from the cross-multiplied gate `Delta_lambda>=0`.

Thus, in this family, `Delta_lambda>=0` is not a conservative replacement for Route B. It is the exact scalar specialization of Route B.

---

## 4. Pairwise barycentric identity

The central new observation is that `Delta_lambda` has no genuine high-dimensional simplex complexity.

For every pair `i<j`, define

**(4.1)**

`K_ij := (tau_i-tau_j) (r_i g_j-r_j g_i)`.

Then

### Theorem B — pairwise expansion

**(4.2)**

`Delta_lambda = sum_{i<j} lambda_i lambda_j K_ij`.

Proof: expand

`a g-b r`

`= sum_{i,j} lambda_i lambda_j tau_i (r_i g_j-g_i r_j)`

and pair the `(i,j)` and `(j,i)` terms. Diagonal terms vanish, and each unordered pair contributes exactly (4.1).

This is a finite-sum polynomial identity; no convex optimizer or S-procedure is hidden in it.

---

## 5. Exact simplex-wide criterion

### Theorem C — all-simplex zero-additive-floor criterion

Assume every two-vertex interpolated cell has an attainable boundary point with

`Q(m)=r/g`

(for example `Q(m)=m^T G0 m` with `G0>0` on a nonzero finite-dimensional space and positive radii).

Then the following are equivalent:

1. for **every** simplex weight `lambda`, `c_lambda>=0` implies `h_lambda>=0`;
2. for every pair `i<j`,

   **(5.1)** `K_ij >= 0`.

#### Sufficiency

If all `K_ij>=0`, then every term in (4.2) is nonnegative because `lambda_i lambda_j>=0`. Hence `Delta_lambda>=0` for every simplex point, and Theorem A gives the cell implication.

#### Necessity

Fix one pair `(i,j)` and restrict the uncertainty simplex to that edge:

`lambda_i=t`, `lambda_j=1-t`, all other weights zero, with `0<t<1`.

Then

**(5.2)** `Delta_lambda = t(1-t) K_ij`.

If `K_ij<0`, then `Delta_lambda<0`. At an attainable boundary point `c_lambda=0`, identity (2.2) becomes

`g h_lambda=Delta_lambda<0`,

so `h_lambda<0`. Therefore robust slack coupling fails on that edge.

Hence checking all `N choose 2` pairwise scalar gates is **exact** for the entire continuum of barycentric weights in the homothetic family.

---

## 6. Effective-radius interpretation

Since `g_i,g_j>0`, define the effective squared radius in the common `Q` metric by

**(6.1)** `s_j := r_j/g_j`.

Then

`r_i g_j-r_j g_i = g_i g_j (s_i-s_j)`.

Therefore (5.1) is equivalent to

**(6.2)**

`(tau_i-tau_j)(s_i-s_j) >= 0`

for every pair.

So the exact structural fingerprint is:

> **vertex multipliers must be co-monotone with the effective cell radius.**

This immediately recovers two important T-P5-152 special cases:

- if all `tau_j` are equal, every pair gate is equality regardless of the moving radii;
- if all effective radii `s_j` are equal, then every cell slack is a positive scalar multiple of one common signed slack, so arbitrary nonnegative `tau_j` are safe.

The pairwise criterion strictly generalizes both cases: neither common multiplier nor identical cell set is required.

---

## 7. Exact additive deficit when pairwise ordering fails

A failed pairwise gate does not merely say "Route B failed". In the homothetic family the required additive repair is explicit.

For fixed `lambda`, let `D>=0`. Then

**(7.1)**

`g (h_lambda + D)`

`= (Delta_lambda + g D) + b c_lambda`.

Hence the root-free gate

**(7.2)** `Delta_lambda + g D >= 0`

is sufficient for

**(7.3)** `c_lambda>=0 ==> h_lambda + D >= 0`.

If the boundary `c_lambda=0` is attainable, (7.2) is also necessary. Thus the minimum additive slack repair is conceptually

`D_* = max(0,-Delta_lambda/g)`,

but the trusted checker never needs to evaluate that quotient; it only verifies (7.2).

### Pairwise failure gives an explicit uniform-floor lower bound

If one pair has `K_ij<0`, choose the midpoint edge weight

`lambda_i=lambda_j=1/2`.

Then

`Delta=K_ij/4`,

`g=(g_i+g_j)/2`.

Therefore any uniform additive repair `D_unif` valid over the full simplex must satisfy

**(7.4)**

`2 (g_i+g_j) D_unif + K_ij >= 0`.

So a negative pair coefficient is not only a qualitative obstruction; it yields an exact cross-multiplied lower bound on the additive floor that any robust consumer must pay.

---

## 8. Regression: T-P5-152 counterexample becomes equality

T-P5-152 used the one-dimensional pair

`c_1=1-m^2`, `tau_1=1`,

`c_2=9-m^2`, `tau_2=0`.

Here

`g_1=g_2=1`, `r_1=1`, `r_2=9`,

so

**(8.1)** `K_12=(1-0)(1*1-9*1)=-8`.

At the midpoint uncertainty weight,

`Delta=K_12/4=-2`, `g=1`.

Thus the exact minimum additive slack repair is `D_*=2`, matching the explicit boundary violation in T-P5-152 exactly.

This is a useful regression because the new criterion does not merely detect the old counterexample; it recovers its sharp deficit.

---

## 9. Broader sufficient shortcut for non-homothetic quadratic cells

The exact pairwise scalar theorem above relies on the one-dimensional shape reduction `c_j=r_j-g_j Q`. For general quadratic cells, a related pairwise identity still gives a useful **sufficient** continuum shortcut.

Write each signed quadratic cell slack in homogeneous form

**(9.1)**

`c_j(m) = [1;m]^T C_j [1;m]`,

where, for T-P5-152 notation,

`C_j = [[r_j, d_j^T], [d_j, -G_j]]`.

Let

`C_lambda=sum lambda_j C_j`,

`C_tau=sum lambda_j tau_j C_j`,

`tau_bar=sum lambda_j tau_j`.

Then there is an exact matrix identity

### Theorem D — affine-`rho` pairwise matrix identity

**(9.2)**

`C_tau - tau_bar C_lambda`

`= sum_{i<j} lambda_i lambda_j (tau_i-tau_j)(C_i-C_j)`.

Therefore, if every pair satisfies

**(9.3)**

`(tau_i-tau_j)(C_i-C_j) >= 0`

in Loewner order, then choosing

**(9.4)** `rho_lambda=tau_bar`

makes the entire T-P5-152 Route C augmented matrix PSD for every simplex weight.

For centered cells this reduces to the pair of sufficient conditions

**(9.5)** `(tau_i-tau_j)(R_i-R_j) >= 0`,

**(9.6)** `(tau_i-tau_j)(G_j-G_i) >= 0` in Loewner order.

This route is root-free and inverse-free, but unlike Theorem C it is **not claimed necessary** for general non-homothetic cells. In particular, a parameter-dependent `rho_lambda` can succeed even when the affine choice `rho_lambda=tau_bar` does not.

---

## 10. Why the homothetic exact theorem is genuinely stronger than the general affine-`rho` shortcut

In the homothetic case `G_j=g_jG0`, the general centered shortcut (9.5)--(9.6) requires, whenever `tau_i>tau_j`, both

`r_i>=r_j`

and

`g_i<=g_j`.

Those imply `r_i/g_i >= r_j/g_j`, but they are stronger than the exact condition

`(tau_i-tau_j)(r_i/g_i-r_j/g_j)>=0`.

Hence one should not replace Theorem C by the easier Loewner-monotone test when the source actually has a common shape. Doing so would create artificial failures and unnecessary additive floors.

The correct hierarchy is:

1. common signed slack / common multiplier when available;
2. homothetic exact pairwise effective-radius criterion;
3. general quadratic affine-`rho` pairwise PSD shortcut;
4. full T-P5-152 pointwise Route B/C search when none of the analytic structures hold.

---

## 11. Minimal Lean theorem surface

The following leaves are small and source-independent.

### Leaf 1 — `homotheticSlack_identity`

Real scalars `g r a b q c h Delta` with

`c = r-g*q`,

`h = a-b*q`,

`Delta = a*g-b*r`.

Conclusion:

`g*h = Delta + b*c`.

This is `ring`.

### Leaf 2 — `homotheticSlack_nonneg`

Assume Leaf 1 plus

`0<g`, `0<=b`, `0<=c`, `0<=Delta`.

Conclusion:

`0<=h`.

This is ordered-ring algebra / `nlinarith`.

### Leaf 3 — `homotheticSlack_additive`

Assume Leaf 1 plus `0<g`, `0<=b`, `0<=c`, `0<=Delta+g*D`.

Conclusion:

`0<=h+D`.

Again purely scalar.

### Leaf 4 — `pairwiseDet_twoVertex`

For two vertices and weight `t`, prove

`Delta = t*(1-t)*(tau1-tau2)*(r1*g2-r2*g1)`.

This is `ring` and gives the necessity/counterexample leaf without any finite-sum API.

### Leaf 5 — `pairwiseDet_finiteSum`

For finite vertex set and barycentric weights, prove

`a*g-b*r = sum_{i<j} lambda_i*lambda_j*(tau_i-tau_j)*(r_i*g_j-r_j*g_i)`.

This is a finite-sum reindexing theorem; it can be formalized after the scalar leaves.

### Leaf 6 — `quadraticCell_pairwiseAffineRho`

For symmetric matrices `C_j`, prove identity (9.2). A downstream PSD corollary consumes pairwise PSD hypotheses and nonnegative `lambda_i lambda_j`.

No theorem above requires matrix inverse, pseudoinverse, square root, eigensystem, optimizer semantics, or deployed source identity.

---

## 12. Source-facing producer packet

For a homothetic parameter-dependent cell, the smallest useful same-key packet is

`(uncertaintyKey, cellSlackFamilyKey, commonShapeKey, {g_j,r_j,tau_j,E_j})`

with exact identities

`c_j = r_j-g_j Q`,

`f_lambda=sum lambda_j f_j`,

`c_lambda=sum lambda_j c_j`,

and the global vertex gap already required by T-P5-152.

The producer should then compute every exact rational pair coefficient

`K_ij=(tau_i-tau_j)(r_i g_j-r_j g_i)`.

- If all `K_ij>=0`, the entire uncertainty simplex is closed with **no per-parameter `rho` solve** and no additive slack tax.
- If some `K_ij<0`, record the violating pair and the exact midpoint lower-bound gate (7.4) before attempting any numerical continuum search.
- Only if the cell family is not homothetic should the producer fall back to the general Route B/C machinery.

The same `cellSlackFamilyKey` matters: separately normalizing vertex cell slacks and then interpolating different normalized objects can change the multiplier-coupling problem even when the underlying vertex feasible sets look identical.

---

## 13. Open boundaries after this child

Still open:

- actual source/runtime uncertainty parameterization and proof that reset and cell use the same barycentric weights;
- proof that deployed cell matrices are genuinely homothetic, if this fast path is to be used;
- actual rational `{g_j,r_j,tau_j}` and vertex gap packets;
- non-homothetic continuum Route B/C when pairwise affine-`rho` PSD conditions fail;
- multiple interacting quadratic cell families or intersections of cells;
- parameter-dependent chart/reference-knot composition;
- Float64/directed-rounding semantics;
- P8/flowpipe/same-tube coverage;
- Lean/kernel compilation and independent validation by 封不觉;
- provenance/admission/registry/P5 parent closure.

In particular, this child is a mathematical continuum-elimination theorem, not a claim that the deployed uncertainty cell has the required homothetic structure.

---

## 14. Requested handoff

The next mathematical/source step should be structure detection, not another generic SDP derivation:

1. inspect the actual parameter-dependent cell packet under one frozen `uncertaintyKey`;
2. test whether every `G_j` is an exact positive rational scalar multiple of one common `G0`;
3. if yes, compute exact `s_j=r_j/g_j` ordering against `tau_j` through the cross-multiplied pair gates `K_ij>=0`;
4. if a pair fails, report its exact additive floor lower bound from (7.4);
5. if the family is not homothetic, try the sufficient pairwise augmented-matrix condition (9.3) before launching pointwise-in-parameter Route B/C searches.

This is the smallest route that turns the T-P5-152 continuum caveat into a finite exact-rational checker problem whenever the source cell family has a common shape.
