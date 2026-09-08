---
kind: review_result
review_id: review-T-P5-074-weighted-strong-monotone-scc-guyuefangyuan-20260908T0700
task_id: T-P5-074-WEIGHTED-STRONG-MONOTONE-SCC
agent: 古月方源
source_agent: 古月方源
claimed_at: 2026-09-08T06:47:00-06:00
created_at: 2026-09-08T07:00:00-06:00
claim_commit: 91520c945f9a6ba4f5ea8a01b5435bbb9787fad2
inspected_commits:
  - a3aca25105c5523ed4c0d98ef2a7c3aa8353e14a
  - 5a298beed9a85c918c75c8cbe02027b1b897d8e0
  - 0b9595aa2e9c8cba93a4b6a9270ee301fff4c06a
  - 18618ab0213677d83867b347a3b3acd7c9857b98
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: >-
  Add a source-independent general-SCC contact-chart consumer after T-P5-072. Use a positive diagonal weight and a signed symmetric-part / strong-monotonicity certificate before falling back to absolute small gain. This handles SCCs with chords and roots depending on multiple contacts, and can certify large negative/skew feedback that every absolute cycle-gain test rejects. Keep existence/coverage, derivative/source binding, Lean validation and admission separate.
---

# T-P5-074 — weighted strong-monotone contact chart for general SCCs

## 0. Result in one line

T-P5-070 handles acyclic contact graphs; T-P5-071/072 handle two-cycles and finite directed simple cycles by scalar elimination. The smallest genuinely new case is a strongly connected contact block with **branching/chords**, where one root may depend on several other contacts and no scalar return-map parity controls the whole block.

For such a block, define the recentering map

`Phi_y(x) = x - rho(x,y)`.

If there is a positive diagonal weight `W=diag(w_i)` and a rational `kappa>0` such that

`< W (Phi_y(x)-Phi_y(x')), x-x' > >= kappa * ||x-x'||_W^2`          (SM)

throughout the certified source box, then `Phi_y` is injective and has an exact quantitative inverse bound. If a common-core displacement packet is also available, Brouwer gives existence on that core, hence a unique chart inverse there.

The key checker-facing improvement is that (SM) can be certified from the **signed symmetric cross derivative**

`w_i D_ij + w_j D_ji`

*before* taking absolute values. Therefore large antisymmetric / negative-feedback couplings can cancel exactly. This is strictly stronger than absolute row-sum, cycle-product, or entrywise small-gain tests.

All trusted scalar gates below can be exact rational and division-free. Failure of this sufficient route is `NOT_CERTIFIED_BY_STRONG_MONOTONICITY`, not a proof of noninvertibility.

This result is mathematics only. It does not bind a deployed P5 SCC, Float64, FD/controller/solve semantics, P8/ODE coverage, Lean/kernel/comparator evidence, receipt/provenance, admission, registry mutation, or parent closure.

---

## 1. General contact block

Let `I_i=[c_i-H_i,c_i+H_i]`, `H_i>0`, and

`B = product_i I_i subset R^n`.

Let `(Y,d)` be the base-parameter metric space and let

`rho : B x Y -> R^n`

be the vector of contact-root locations. There is no triangularity assumption and no simple-cycle assumption: `rho_i` may depend on several coordinates `x_j`.

Define

**(1.1)** `Phi_y(x) = x-rho(x,y)`

and the recentered coordinates

**(1.2)** `xi = Phi_y(x)`.

For positive rational weights `w_i>0`, define

**(1.3)** `||z||_W^2 = sum_i w_i z_i^2`.

No matrix inverse is part of the primitive certificate.

---

## 2. Common-core existence for an arbitrary SCC

Assume the same type of uniform root displacement packet used in T-P5-070/071/072:

**(2.1)** `|rho_i(x,y)-c_i| <= delta_i` for every `x in B`,

with

**(2.2)** `0 <= delta_i < H_i`.

Define

**(2.3)** `K_i = H_i-delta_i`.

Fix `y` and any target chart coordinate satisfying

**(2.4)** `|xi_i| <= K_i` for all `i`.

Consider

**(2.5)** `G(x)=xi+rho(x,y)`.

Then for every `x in B`,

`|G_i(x)-c_i| <= |xi_i|+|rho_i(x,y)-c_i| <= K_i+delta_i = H_i`,

so

**(2.6)** `G(B) subset B`.

If `rho(.,y)` is continuous, `G` is a continuous self-map of the nonempty compact convex box `B`. Brouwer therefore gives some `x in B` with `G(x)=x`, i.e.

`xi = x-rho(x,y)=Phi_y(x)`.

### Theorem 2.1 — arbitrary-SCC common-core existence

Continuity plus the displacement packet (2.1)-(2.4) implies that the entire product chart core `product_i[-K_i,K_i]` lies in `Phi_y(B)`.

Unlike the simple-cycle proof, this genuinely uses a finite-dimensional fixed-point theorem. It should be kept as a separate existence/coverage layer: the strong-monotone theorem below proves uniqueness and stability but does not by itself assert that a requested `xi` lies in the image of a bounded source box.

For a first Lean implementation it is reasonable to formalize the uniqueness/stability consumer with an explicit `exists_preimage` premise and add the Brouwer box theorem later.

---

## 3. Weighted secant strong monotonicity

Assume that for a fixed `y` there is a rational `kappa>0` such that for all `x,x' in B`,

**(3.1)**

`kappa ||x-x'||_W^2`

`<= < W(Phi_y(x)-Phi_y(x')), x-x' >`.

This is the canonical source-independent theorem interface. It needs no differentiability.

### Theorem 3.1 — injectivity

Under (3.1), `Phi_y` is injective on `B`.

Proof. If `Phi_y(x)=Phi_y(x')`, the right side of (3.1) is zero, so

`kappa ||x-x'||_W^2 <= 0`.

Since `kappa>0` and every `w_i>0`, `x=x'`.

Combining with Theorem 2.1 gives a **unique inverse** on the common product core.

### Theorem 3.2 — same-parameter square inverse budget

Let

`xi=Phi_y(x)`, `xi'=Phi_y(x')`.

Write

`E = ||x-x'||_W^2`, `Z = ||xi-xi'||_W^2`.

From (3.1) and weighted Cauchy,

`kappa E <= sqrt(Z E)`.

If `E=0` the result is trivial; otherwise cancellation and squaring give the division-free conclusion

**(3.2)** `kappa^2 E <= Z`.

So a checker may consume the squared inequality directly. It never needs to construct `1/kappa` or a square root.

---

## 4. Base-parameter transport

For varying `y`, assume an independent parameter-variation packet at fixed physical coordinate:

**(4.1)**

`||rho(x,y)-rho(x,y')||_W^2 <= P * d(y,y')^2`

with rational `P>=0`.

Take two triples

`xi=Phi_y(x)`, `xi'=Phi_y'(x')`.

Let

`e=x-x'`, `z=xi-xi'`,

`q=rho(x',y)-rho(x',y')`, `D=d(y,y')`.

The exact identity is

**(4.2)**

`Phi_y(x)-Phi_y(x') = z+q`.

Hence strong monotonicity gives

`kappa ||e||_W^2 <= <W(z+q),e>`.

Weighted Cauchy yields

**(4.3)**

`kappa^2 ||e||_W^2 <= ||z+q||_W^2`.

For any rational `lambda>0`, Young's identity gives

`||z+q||_W^2 <= (1+lambda)||z||_W^2 + (1+1/lambda)||q||_W^2`.

Multiplying through by `lambda` removes the only division:

### Theorem 4.1 — rational two-source inverse budget

**(4.4)**

`lambda*kappa^2 ||x-x'||_W^2`

`<= (1+lambda) * (lambda ||xi-xi'||_W^2 + P*d(y,y')^2)`.

Everything in (4.4) is add/multiply/order over exact rationals once the source packet is frozen.

Two useful sharp specializations do not need Young slack:

- same base parameter: `kappa^2 E <= Z`;
- same chart coordinate: `kappa^2 E <= P D^2`.

Thus simultaneous coupled contact-center motion is controlled by the same strong-monotone chart certificate.

---

## 5. Jacobian route: signed symmetric part, not absolute gains

The secant theorem (3.1) is the preferred trusted consumer. A differentiable source can generate it cheaply.

Assume `Phi_y` is `C^1` on the convex box `B`. Write

`D_ij(x) = partial_j Phi_i(x)`.

Let `W=diag(w_i)`. Define the doubled weighted symmetric Jacobian

**(5.1)**

`T(x) = W D Phi_y(x) + D Phi_y(x)^T W`.

Its entries are

**(5.2)** `T_ii = 2 w_i D_ii`,

**(5.3)** `T_ij = w_i D_ij + w_j D_ji` for `i != j`.

For every vector `u`,

`u^T T u = 2 u^T W D Phi_y u`.

So it is the **signed pair sum** (5.3), not `|D_ij|+|D_ji|`, that controls the quadratic form.

Assume exact cell bounds

**(5.4)** `D_ii(x) >= d_i`,

**(5.5)** `|w_i D_ij(x)+w_j D_ji(x)| <= c_ij=c_ji`, `c_ij>=0`.

If for every `i`

**(5.6)**

`2 w_i d_i - sum_{j != i} c_ij >= 2 kappa w_i`,

then for every `u`

`u^T T u >= 2 kappa ||u||_W^2`.

Indeed,

`2 T_ij?` is already accounted for by the symmetric quadratic expansion:

`u^T T u = sum_i T_ii u_i^2 + 2 sum_{i<j} T_ij u_i u_j`.

Using

`2|u_i u_j| <= u_i^2+u_j^2`

gives

`u^T T u >= sum_i (T_ii-sum_{j!=i}|T_ij|)u_i^2`,

and (5.4)-(5.6) finish the bound.

Now integrate `D Phi_y` along the segment `x'+t(x-x')` inside the convex box. The pointwise quadratic bound gives exactly (3.1).

### Theorem 5.1 — signed diagonal-dominance generator

The rational row gates (5.6), together with source-valid derivative bounds (5.4)-(5.5), imply the weighted secant strong-monotonicity theorem (3.1).

This is the practical general-SCC checker.

---

## 6. Contact-root specialization and division-free source packet

In the usual recentered contact chart, `rho_i` is the location of the root in coordinate `x_i`, parametrized by the *other* coordinates. Thus `rho_i` normally has no self dependence and

`partial_i rho_i = 0`,

hence

**(6.1)** `D_ii = partial_i Phi_i = 1`.

The row gate becomes

**(6.2)**

`sum_{j!=i} c_ij <= 2(1-kappa) w_i`.

For `i!=j`, since `Phi_i=x_i-rho_i`,

**(6.3)**

`T_ij = -(w_i partial_j rho_i + w_j partial_i rho_j)`.

Therefore the source should bound the **signed combination first**:

**(6.4)**

`|w_i partial_j rho_i + w_j partial_i rho_j| <= c_ij`.

Taking separate absolute values first is safe but can destroy the main negative-feedback cancellation.

If the roots come implicitly from `h_i(x_i,x_-i,y)=0` with orientation-gauged active derivatives `d_i=partial_i h_i>0`, then

`partial_j rho_i = -(partial_j h_i)/d_i`.

A fully division-free source theorem for the pair `(i,j)` is therefore

**(6.5)**

`| w_i (partial_j h_i) d_j + w_j (partial_i h_j) d_i |`

`<= c_ij d_i d_j`.

Because `d_i d_j>0`, (6.5) is exactly sufficient for (6.4). This is preferable to separately bounding the two fractions: cancellation occurs in the polynomial/rational numerator before any absolute value.

No claim is made here that deployed source already provides (6.5); it is the suggested source packet.

---

## 7. Exact-rational checker

For one certified cell, the trusted packet can be only:

- positive rational weights `w_i`;
- positive rational target `kappa`;
- rational diagonal lower bounds `d_i`;
- symmetric rational cross bounds `c_ij>=0`;
- source/interval proofs of (5.4)-(5.5), or the cleared implicit-root form (6.5);
- optional rational parameter charge `P`.

Then the trusted algebra is:

1. for each row compute `R_i = 2 w_i d_i - sum_{j!=i} c_ij - 2 kappa w_i`;
2. require `R_i>=0` for every `i`;
3. consume the secant theorem;
4. use `kappa^2 E <= Z` for same-parameter inversion, or (4.4) for parameter transport.

No determinant, eigenvalue, matrix inverse, square root, nonlinear solve, or floating optimization is needed in the trusted arithmetic layer.

If a row gate fails, the correct status is `NOT_CERTIFIED_BY_THIS_STRONG_MONOTONE_BOUND`. The true chart may still be invertible.

---

## 8. Exact regression A: complete skew-feedback SCC defeats absolute small gain

Take the linear three-contact root map on `R^3`

`rho(x)=S x`,

with

`S = [[0, 2, -3],
      [-2,0,  4],
      [3,-4,  0]]`.

This is a complete strongly connected contact graph: every root depends on two other contacts, so it is outside the triangular and simple-cycle hypotheses.

Since `S^T=-S`,

`Phi(x)=(I-S)x`

satisfies, for every `e`,

`<Phi(e),e> = ||e||_2^2 - <Se,e> = ||e||_2^2`.

Thus `W=I`, `kappa=1` is exact, and

**(8.1)** `||x-x'||_2^2 <= ||xi-xi'||_2^2`.

The signed symmetric cross bounds are all exactly zero:

`D Phi + D Phi^T = 2I`.

But every pairwise absolute two-cycle gain product is already greater than one:

`|2*(-2)|=4`, `|(-3)*3|=9`, `|4*(-4)|=16`.

The directed three-cycle coefficient product `2*4*3=24` is positive as well. Hence neither “all absolute cycle gains <1” nor a naive cycle-parity rejection can capture this safe SCC. The cancellation is genuinely matrix/global and is exactly what the weighted symmetric-part gate preserves.

For reference, `det(I-S)=30`, but the certificate does not use this determinant.

---

## 9. Exact regression B: failure of strong monotonicity is not noninvertibility

Take

`rho(x1,x2) = (3/2 x2, 3/2 x1)`.

Then

`Phi = [[1,-3/2],[-3/2,1]]`.

Its determinant is

`1-9/4 = -5/4 != 0`,

so the linear chart is globally invertible. But its symmetric part is itself and has a negative direction, so no positive strong-monotonicity modulus exists in the Euclidean metric.

Therefore a failed T-P5-074 gate is only `NOT_APPLICABLE`; it is not a mathematical counterexample to invertibility.

At coefficient `1` instead of `3/2`, the determinant becomes zero, showing that genuine cyclic singularity is also possible. A later P-matrix / interval-Newton / exact determinant child may distinguish some cases that T-P5-074 intentionally leaves open.

---

## 10. Relation to T-P5-070/071/072

The hierarchy is now:

1. **acyclic graph** — T-P5-070: triangular recursion, nilpotent comparison matrix, no small gain;
2. **simple cycle** — T-P5-071/072: scalar return map; negative orientation parity gives no-small-gain uniqueness, otherwise strict cycle-product small gain;
3. **general SCC with branching/chords** — T-P5-074: weighted strong monotonicity from the signed symmetric part; handles cancellations that scalar cycle tests cannot see;
4. if T-P5-074 fails — keep `NOT_APPLICABLE`; possible future routes are P-matrix global univalence, interval Newton/Krawczyk, exact affine determinant, or source-specific decomposition.

The routing should prefer cheap graph structure first, then signed symmetric-part algebra, and only then heavier general nonlinear machinery.

---

## 11. Suggested Lean decomposition

The first Lean sidecar should **not** start with Brouwer or multivariable derivatives. The useful trusted algebra can be tiny.

Suggested theorem statements, schematically over `Fin n -> R`:

### 11.1 weighted square norm

`wNormSq w z := sum i, w i * (z i)^2`.

Prove positivity from `forall i, 0 < w i`.

### 11.2 secant consumer

`weighted_strong_monotone_injective`

Premises:

- `0<kappa`;
- positive weights;
- for all `x,x'`,
  `kappa*wNormSq w (x-x') <= sum i w_i*(Phi_i x-Phi_i x')*(x_i-x_i')`.

Conclusion: injective.

### 11.3 square inverse bound

`weighted_strong_monotone_sq_inverse_bound`

Same premises plus `xi=Phi x`, `xi'=Phi x'`.

Conclusion:

`kappa^2 * wNormSq w (x-x') <= wNormSq w (xi-xi')`.

This is pure ordered-ring/Cauchy algebra after the weighted inner product API is chosen.

### 11.4 parameter transport

`weighted_strong_monotone_param_sq_bound`

Add `lambda>0` and

`wNormSq w (rho x y-rho x y') <= P*D^2`.

Conclusion (4.4):

`lambda*kappa^2*E <= (1+lambda)*(lambda*Z+P*D^2)`.

### 11.5 signed row checker

`signed_sym_diag_dominant_quadratic_lower`

Pure finite-sum statement: if a symmetric scalar array has diagonal/off-diagonal bounds satisfying (5.6), then its quadratic form is at least `2*kappa*wNormSq`.

This can be proved with `2*abs(a*b) <= a^2+b^2`; no eigenvalue API is required.

### 11.6 later calculus bridge

`jacobian_signed_sym_gate_implies_weighted_secant`

Keep this separate because it needs segment integration / Frechet derivative infrastructure.

### 11.7 later existence bridge

`contact_box_core_exists_of_displacement`

This is the Brouwer box theorem from Section 2 and can be delayed until the algebraic consumer compiles.

---

## 12. Source-lane recommendation

Before spending effort on a general nonlinear solver, extract for each real SCC:

1. dependency graph and whether T-P5-070 or T-P5-072 already applies;
2. if not, candidate positive rational weights `w_i`;
3. diagonal derivative lower bounds `d_i`;
4. pairwise **signed** cross sums `w_i D_ij+w_j D_ji`, bounded before absolute value;
5. row reserves from (5.6);
6. optional parameter charge `P` and common-core displacement `delta_i`.

If the signed row gate passes, there is no reason to compute an inverse Jacobian or spectral radius. If it fails, retain the failure as a routing signal only.

For implicit root graphs, prefer direct cleared inequalities of the form (6.5). This preserves cancellation and keeps the checker in exact rational/polynomial arithmetic.

---

## 13. Boundary / unresolved obligations

`T-P5-074` remains `pending mathematical child`.

Not supplied here:

- any concrete deployed P5 contact SCC or dependency graph;
- actual weights `w_i`, derivative enclosures, or cleared cross-pair inequalities from the source;
- proof that a deployed source box satisfies the common-core displacement packet;
- Float64/libm, finite-difference, controller, solve or runtime semantics;
- P8/ODE/trajectory coverage;
- Lean compilation, kernel/comparator receipt, or independent verification by 封不觉;
- receipt/provenance/admission/re-audit work;
- P5/P8/M4 closure or registry mutation.

The mathematical advance is the general-SCC signed strong-monotonicity interface and its exact-rational diagonal-dominance realization, together with a regression showing that it certifies large complete skew feedback that every absolute small-gain cycle test rejects.
