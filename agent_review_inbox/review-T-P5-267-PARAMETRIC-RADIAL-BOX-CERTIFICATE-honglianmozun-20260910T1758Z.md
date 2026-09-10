---
kind: review_result
review_id: review-T-P5-267-parametric-radial-box-certificate-honglianmozun-20260910T1758Z
task_id: T-P5-267-PARAMETRIC-RADIAL-BOX-CERTIFICATE
reviewer: 红莲魔尊
agent: 红莲魔尊
source_agent: 红莲魔尊
created_at: 2026-09-10T17:58:00Z
claim_commit: 046fe800b70e13f2739b263068164680c2fcd750
inspected_commit: 8c61769493e1bb8bb154ea1ec370913fe69dbf96
upstream_commits:
  - d062e528bc248cd24f09973dcde7cfcf7c00ffae  # T-P5-266 zero-margin radial Sturm certificate
  - 913ed31d66c77016e82fe2371d3734b033e76e5f  # T-P5-265 rational Bernstein radial interval certificate
  - 32dbdb379152b48355b110682cfc1314c0ff231a  # T-P5-264 parity-symmetric homogeneous energy allocator
  - f4704792f1420aef65ad19af2e03ece571bf494e  # T-P5-263 higher-degree matched-metric Banach polarization
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_separately_convex_parameter_vertex_reduction; add_multiaffine_exact_vertex_identity; add_quadratic_parameter_convexity_gate; add_tensor_Bernstein_box_certificate; add_strict_margin_finite_box_completeness; add_zero_margin_bivariate_obstruction; preserve_source_binding_and_coverage_boundaries
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact finite-dimensional convexity algebra, rational polynomial/Taylor-to-Bernstein conversion, tensor de Casteljau subdivision, exact counterexample regressions; no provenance/receipt/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-267 — Parametric radial box certificate: exact vertex reduction and tensor Bernstein fallback

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-265 and T-P5-266 make the one-variable radial consumer decision-complete once the energy packet has the form

`||P(u)||^2 <= q A(q)`, `q=Q(u) in [0,R]`,

with rational polynomial `A`. T-P5-266 correctly leaves the next seam at source realization: an actual same-cell coefficient may depend on an additional cell/source parameter, producing `A(q,s)` rather than a single `A(q)`.

This child proves a two-level structured closure.

1. If the parameter dependence is **separately convex** on a fixed rational box, then the worst parameter value occurs at a box vertex for every radial value `q`. Hence the full parametric Lyapunov gate is **exactly equivalent** to finitely many univariate radial gates. Multi-affine dependence is the lossless algebraic special case and needs no curvature estimate.
2. For one quadratic parameter, the convexity premise itself reduces to the univariate sign of the quadratic coefficient, so T-P5-265/T-P5-266 can also decide that gate exactly.
3. For a general rational bivariate polynomial, tensor-product Bernstein coefficients give a finite sound box certificate. Under a strict positive margin, sufficiently fine rational subdivision is guaranteed to terminate with a positive certificate.
4. That strict-margin completeness cannot be extended to arbitrary zero-margin bivariate polynomials by tensor Bernstein subdivision alone. The exact nonnegative polynomial `(x-y)^2` gives a structural obstruction on every finite axis-aligned subdivision.

Thus there is now a precise dispatcher:

`parametric radial packet`

`-> separately convex / multi-affine ?`

`-> YES: exact vertex reduction -> T-P5-265/T-P5-266`

`-> NO: tensor Bernstein strict-margin box certificate`

`-> zero-margin + nonconvex genuinely bivariate: keep open / stronger algebraic geometry required`.

No actual deployed P5 coefficient family, source parameterization, same-key box, metric/radius, cell/trajectory/FD-halo coverage, Float64 semantics, Lean/kernel proof, independent verifier action, admission, registry mutation, or parent closure is claimed.

---

## 1. Parametric radial Lyapunov setup

Let

`q := Q(u)=u^T W u`, `W=W^T>0`, `0<=q<=R`, `R>0`.

Let the additional source/cell parameter be

`theta=(theta_1,...,theta_m)`

in the fixed rational box

**(1.1)** `B := product_j [a_j,b_j]`, `a_j<b_j`.

Assume a source-specific energy identity/envelope has already produced

**(1.2)** `||P(u,theta)||^2 <= q A(q,theta)`

for all admissible `(u,theta)`, where the target coefficient `A` is real-valued. The desired constant-form Lyapunov consumer is

**(1.3)** `A(q,theta) <= K`

for every `(q,theta) in [0,R] x B`.

If (1.3) holds, then

**(1.4)** `||P(u,theta)||^2 <= K Q(u)`.

Consequently an energy inequality

`dot V <= -gamma Q(u) + L ||P(u,theta)||^2`

closes as

**(1.5)** `dot V <= -(gamma-LK)Q(u)`.

No division by `q` is needed, so the point `q=0` is included without a special limiting argument.

---

## 2. Theorem A — separately convex parameter dependence reduces exactly to vertices

Assume that for every fixed `q in [0,R]`, the map

`theta -> A(q,theta)`

is convex in each coordinate separately: holding all other coordinates fixed, the one-variable function of `theta_j` is convex on `[a_j,b_j]`.

Let `Vert(B)` be the `2^m` box vertices. Then for every fixed `q`,

**(2.1)** `sup_{theta in B} A(q,theta) = max_{v in Vert(B)} A(q,v)`.

Therefore

**(2.2)**

`A(q,theta)<=K for all (q,theta) in [0,R]xB`

**iff**

`A(q,v)<=K for all q in [0,R] and all v in Vert(B)`.

### Proof

For one coordinate, write

`theta_j=(1-t_j)a_j+t_j b_j`, `0<=t_j<=1`.

Convexity gives

**(2.3)**

`A(...,theta_j,...) <= (1-t_j)A(...,a_j,...)+t_j A(...,b_j,...)`.

Apply (2.3) successively to coordinates `1,...,m`. This yields

**(2.4)**

`A(q,theta) <= sum_{v in Vert(B)} lambda_v(theta) A(q,v)`,

where

`lambda_v(theta)=product_j [t_j if v_j=b_j else (1-t_j)]`.

Every `lambda_v>=0` and `sum_v lambda_v=1`, hence

`A(q,theta) <= max_v A(q,v)`.

The reverse inequality for the supremum is immediate because every vertex belongs to `B`. This proves (2.1), and (2.2) follows by taking the supremum also over `q`. QED.

### Structural interpretation

The extra source parameter does **not** automatically force a genuinely bivariate sign problem. If the target energy coefficient is separately convex, parameter elimination is free and exact: only the radial variable remains.

This is especially useful because the maximizing vertex may vary with `q`; no global monotonicity choice is required.

---

## 3. Theorem B — multi-affine dependence gives an exact barycentric identity

Suppose `A(q,theta)` is affine in each `theta_j` separately. Cross-products such as `theta_1 theta_2` are allowed; the condition is degree at most one in each individual parameter.

Then every inequality in the proof of Theorem A becomes equality:

**(3.1)**

`A(q,theta) = sum_{v in Vert(B)} lambda_v(theta) A(q,v)`.

Thus the parameter dependence is literally a convex combination of vertex radial polynomials.

If `A in Q[q,theta]` and all `a_j,b_j` are rational, every substituted vertex packet

**(3.2)** `A_v(q):=A(q,v)`

lies in `Q[q]`.

Hence the combined exact decision procedure is:

1. enumerate the finite vertex set;
2. form `p_v(q)=K-A_v(q)` exactly;
3. use T-P5-265 as the fast strict-margin Bernstein path;
4. use T-P5-266 for zero-margin/touching cases;
5. PASS the full box iff every vertex radial packet PASSes.

This route is complete for non-strict uniform bounds in the multi-affine branch because T-P5-266 is complete on each rational univariate polynomial.

### Why a single sampled endpoint is not enough

Take one parameter `s in [-1,1]`, `q in [0,1]`, and

**(3.3)** `A(q,s)=s(2q-1)`.

For `q<1/2`, the maximizing endpoint is `s=-1`; for `q>1/2`, it is `s=1`. Thus no single endpoint selected from a sample or from a nominal slope is uniformly correct.

The two endpoint polynomials are

`A(q,1)=2q-1`,

`A(q,-1)=1-2q`,

and checking both gives the exact global bound `A<=1`.

---

## 4. One quadratic parameter — convexity is itself a univariate radial gate

Consider one parameter `s in [a,b]` and

**(4.1)**

`A(q,s)=A_0(q)+A_1(q)s+A_2(q)s^2`,

where `A_0,A_1,A_2 in Q[q]`.

Then

**(4.2)** `partial_s^2 A(q,s)=2 A_2(q)`.

Therefore

**(4.3)**

`A(q,.) is convex on [a,b] for every q in [0,R]`

**iff**

`A_2(q)>=0 on [0,R]`.

The right-hand side is exactly another univariate rational-polynomial nonnegativity problem. T-P5-265/T-P5-266 can decide it without a bivariate solver.

If (4.3) passes, Theorem A gives

**(4.4)**

`A(q,s)<=K on [0,R]x[a,b]`

iff both

`A(q,a)<=K` and `A(q,b)<=K` on `[0,R]`.

Thus a quadratic parameter packet with nonnegative radial curvature coefficient is still completely reduced to finitely many univariate exact checks.

### Failure boundary when the curvature has the opposite sign

For

**(4.5)** `A(s)=4s(1-s)` on `[0,1]`,

both endpoints are zero while `A(1/2)=1`. Here `A''=-8<0`; endpoint reduction for an upper bound is invalid.

So `separately_convex` is a real mathematical gate, not a convenience label.

---

## 5. Reserve transport through the vertex reduction

Suppose each vertex check proves a stronger rational margin

**(5.1)** `A(q,v) <= K-eta_v`, `eta_v>=0`,

for all `q in [0,R]`.

From (2.4),

`A(q,theta)`

`<= sum_v lambda_v (K-eta_v)`

`=K-sum_v lambda_v eta_v`

`<=K-min_v eta_v`.

Therefore

**(5.2)** `A(q,theta) <= K-eta_*`,

where

**(5.3)** `eta_*:=min_v eta_v`.

The exact radial reserve exported by T-P5-265 at each vertex can therefore be transported through the parameter box without introducing a new norm or Young constant.

If some vertex has a zero-margin T-P5-266 PASS, then `eta_*=0`; the global result remains a valid non-strict PASS but no strict perturbation reserve may be invented.

---

## 6. General bivariate fallback — tensor Bernstein representation

The separately-convex gate can fail even though the true parametric energy bound is safe. A general polynomial `p(q,s)=K-A(q,s)` therefore needs a fallback that preserves both variables.

Let

`p in Q[q,s]`,

and consider a rational rectangle

**(6.1)** `D=[q_0,q_0+h] x [s_0,s_0+k]`, `h,k>0`.

Let the bidegree of `p` be at most `(n,m)`. Normalize

`x=(q-q_0)/h`, `y=(s-s_0)/k`,

so `(x,y) in [0,1]^2`.

The tensor Bernstein basis is

**(6.2)** `B_{i,n}(x) B_{j,m}(y)`.

It satisfies

- every basis function is nonnegative on the unit square;
- the double sum of all basis functions is one.

The exact Taylor expansion at the lower-left corner is

**(6.3)**

`p(q_0+hx,s_0+ky)`

`= sum_{r=0}^n sum_{t=0}^m c_{rt} x^r y^t`,

with

**(6.4)**

`c_{rt}=h^r k^t [partial_q^r partial_s^t p(q_0,s_0)]/(r! t!)`.

Using the one-variable power-to-Bernstein identity in each coordinate gives

**(6.5)**

`p(q_0+hx,s_0+ky)`

`=sum_{i=0}^n sum_{j=0}^m beta_{ij}[D] B_{i,n}(x)B_{j,m}(y)`,

where

**(6.6)**

`beta_{ij}[D]`

`=sum_{r=0}^i sum_{t=0}^j`

`  [binom(i,r)/binom(n,r)] [binom(j,t)/binom(m,t)] c_{rt}`.

All quantities are rational when the polynomial and rectangle are rational.

---

## 7. Theorem C — tensor Bernstein convex-hull certificate

From the positivity and partition-of-unity property of the tensor basis,

**(7.1)**

`min_{i,j} beta_{ij}[D] <= p(q,s) <= max_{i,j} beta_{ij}[D]`

for every `(q,s) in D`.

Therefore:

- if every `beta_{ij}[D]>=0`, then `p>=0` on the whole rectangle;
- if every `beta_{ij}[D]>0`, then `p>=min beta_{ij}>0`;
- applied to `p=K-A`, this is a finite exact-rational Lyapunov certificate.

The trusted core may clear positive common denominators and compare integers; no floating root finder, eigenproblem, square root, pseudoinverse, or sampled maximization is required.

Tensor de Casteljau subdivision is obtained by applying the ordinary one-dimensional recurrence successively in `q` and `s`. Rational split coordinates preserve rational coefficients exactly.

---

## 8. Theorem D — strict positivity has a finite rational tensor-Bernstein tree

Assume

**(8.1)** `p(q,s)>=delta>0`

on a rational compact rectangle.

Then a sufficiently fine rational axis-aligned subdivision yields positive tensor Bernstein coefficients on every leaf.

### Proof with an explicit derivative budget

Normalize the global rectangle to `[0,1]^2` and write the resulting rational polynomial as

**(8.2)** `p_hat(x,y)=sum_{a,b} c_{ab} x^a y^b`.

For every derivative order `(r,t)`, define the rational coefficient bound

**(8.3)**

`M_{rt}:=sum_{a>=r,b>=t} |c_{ab}| binom(a,r) binom(b,t)`.

On `[0,1]^2`,

**(8.4)**

`|partial_x^r partial_y^t p_hat(x,y)|/(r!t!) <= M_{rt}`.

Now take a normalized leaf of widths `H,K`. Formula (6.6) and the bounds

`0<=binom(i,r)/binom(n,r)<=1`,

`0<=binom(j,t)/binom(m,t)<=1`

give

**(8.5)**

`|beta_{ij}-p_hat(x_0,y_0)| <= E(H,K)`,

where

**(8.6)**

`E(H,K):=sum_{(r,t)!=(0,0)} M_{rt} H^r K^t`.

Because every nonconstant term contains a positive power of `H` or `K`,

`E(H,K)->0` as `(H,K)->(0,0)`.

Choose positive rational `H,K` such that `E(H,K)<delta`. A finite rational grid, in particular a sufficiently deep dyadic tensor subdivision, can make every leaf width no larger than these values. On every leaf,

`beta_{ij} >= p_hat(x_0,y_0)-E(H,K) >= delta-E(H,K)>0`.

Hence all leaves pass Theorem C. QED.

### Consequence

Tensor Bernstein subdivision is **semidecision-complete for strict parametric PASS**. A checker need not know `delta` in advance; repeated exact subdivision must eventually expose a positive finite tree whenever a strict margin exists.

The minimum passing leaf coefficient is itself an exact rational reserve for downstream perturbation layers.

---

## 9. Exact obstruction — zero-margin bivariate positivity is not Bernstein-tree complete

The univariate zero-margin gap was closed by T-P5-266. The analogous statement is false for finite axis-aligned tensor Bernstein subdivision.

Consider

**(9.1)** `p(x,y)=(x-y)^2`

on `[0,1]^2`.

Clearly `p>=0`, with a whole diagonal zero set.

In bidegree `(2,2)`, the tensor Bernstein coefficients on the unit square are

**(9.2)**

`[[0, 0, 1],`

` [0,-1/2,0],`

` [1, 0, 0]]`.

So the coarse tensor certificate fails despite exact nonnegativity.

More importantly, **no finite axis-aligned subdivision can repair this by requiring every leaf coefficient to be nonnegative.**

### Proof

Take any finite subdivision into axis-aligned rectangles. The union of all leaf boundaries is a finite union of vertical and horizontal segments. It cannot contain the entire diagonal segment `{(x,x):0<x<1}`. Hence there exists a diagonal point `(xi,xi)` lying in the strict interior of some leaf rectangle.

At an interior point of a leaf, every tensor Bernstein basis function of fixed bidegree `(2,2)` is strictly positive. If all leaf coefficients were nonnegative, then the equality

`0=p(xi,xi)=sum_{i,j} beta_{ij} B_{i,2}(x_*)B_{j,2}(y_*)`

would force **every** coefficient `beta_{ij}` to vanish. That would make the polynomial identically zero on that leaf, contradicting `(x-y)^2`.

Therefore every finite axis-aligned subdivision has at least one leaf with a negative Bernstein coefficient. QED.

### Meaning

The strict-margin hypothesis in Theorem D is not merely a proof artifact. General zero-margin bivariate nonnegativity needs a stronger exact method—e.g. special factorization, resultant/CAD machinery, a structure-specific SOS/Gram theorem, or another exact algebraic-geometric certificate.

It must not be reported as mathematical FAIL merely because tensor Bernstein subdivision never closes.

---

## 10. Additional negative controls

### 10.1 Parameter endpoint checking without convexity is unsound

The polynomial

`A(s)=4s(1-s)`

has `A(0)=A(1)=0` but `A(1/2)=1`. Any dispatcher that applies vertex reduction before proving multi-affinity/separate convexity can false-PASS.

### 10.2 A parameter box depending on `q` is a different geometry

Theorem A assumes a fixed product set `[0,R] x B`. If the admissible fiber is

`s in [a(q),b(q)]`,

substituting only the vertices of one frozen box can be conservative or wrong depending on how the box was obtained. The moving endpoints must be included in the source geometry before parameter elimination.

### 10.3 Rational denominators need an independent sign gate

If `A=N/D` rather than a polynomial, clearing `D` is legal only after proving `D>0` on the same rectangle. A denominator sign change cannot be hidden inside the Bernstein or vertex packet.

### 10.4 A source subset is not automatically the full box

Checking a containing box is sound for an upper bound but may be conservative. The equivalence (2.2) is an exact statement for the declared full box. If the true source set is a strict curved subset, failure on an unused box vertex is not a physical counterexample without a source-membership witness.

---

## 11. Candidate theorem statements for a formal layer

### Theorem 1 — separately convex vertex maximum

For a fixed box `B=product_j[a_j,b_j]`, if `f : B -> R` is convex in each coordinate separately, then

`forall theta in B, f(theta) <= max_{v in Vert(B)} f(v)`.

Applying this pointwise in `q` gives Theorem A.

### Theorem 2 — multi-affine barycentric identity

If `f` is affine in each coordinate separately, then

`f(theta)=sum_v lambda_v(theta) f(v)`

with the product barycentric weights from (2.4).

### Theorem 3 — parametric radial Lyapunov consumer

Assume (1.2), separate convexity of `A(q,.)`, and

`forall v in Vert(B), forall q in [0,R], A(q,v)<=K`.

Then

`forall u,theta, Q(u)<=R -> theta in B -> ||P(u,theta)||^2 <= K Q(u)`.

### Theorem 4 — tensor Bernstein leaf soundness

If a rational polynomial on a rational rectangle has a tensor Bernstein representation with all coefficients nonnegative, then it is nonnegative on the whole rectangle.

### Theorem 5 — strict finite subdivision completeness

If a rational bivariate polynomial is strictly positive on a rational compact rectangle, then there exists a finite rational axis-aligned subdivision for which every tensor Bernstein coefficient on every leaf is strictly positive.

The zero-margin converse is intentionally **not** proposed because Section 9 disproves it.

---

## 12. Structural fingerprint

The new reusable fingerprint is

**parametric radial energy**

`-> identify radial variable q and nuisance/source parameters theta`

`-> preserve signed A(q,theta)`

`-> prove multi-affine or separate convexity in theta`

`-> exact box-vertex elimination`

`-> univariate rational vertex packets`

`-> Bernstein fast path + Sturm zero-margin path`

`-> export exact global Lyapunov reserve`.

If the convexity gate fails but a strict full-box margin exists:

`-> retain both variables`

`-> tensor Bernstein rational subdivision`

`-> finite strict certificate`.

This prevents two opposite errors: prematurely destroying parameter cancellation with absolute scalar caps, and falsely collapsing a genuinely bivariate nonconvex problem to sampled parameter endpoints.

---

## 13. Remaining obligations / fail-closed boundary

Still open and explicitly **not** proved here:

1. actual deployed P5 source identity producing `A(q,theta)`;
2. proof that `q=Q(u)` and the parameter coordinates use the same source key/cell;
3. proof that the declared parameter set is the true fixed box, or a sound containing box;
4. multi-affinity/separate convexity of the actual coefficient family;
5. actual rational coefficient extraction and denominator-sign semantics;
6. cell, trajectory, flowed-sheet, FD-halo and reference-halo coverage;
7. Float64/libm/interval semantics;
8. Lean/kernel formalization;
9. independent verification by 封不觉;
10. admission, registry mutation, or P5 parent closure.

A failure of the vertex branch without a convexity premise is `VERTEX_REDUCTION_NOT_APPLICABLE`, not mathematical FAIL. A failure of finite tensor Bernstein subdivision at zero reserve is `BIVARIATE_ZERO_MARGIN_CERTIFICATE_OPEN`, not mathematical FAIL.

---

## 14. Requested next step

The clean remaining non-overlapping mathematics seam is the **concave quadratic parameter branch**. If

`A(q,s)=A_0(q)+A_1(q)s-A_2(q)s^2`, `A_2(q)>0`,

the parameter maximum can lie in the interior. Completing the square suggests an exact clamped-vertex reduction to the rational expression

`A_0(q)+A_1(q)^2/(4A_2(q))`

on the branch where `s_*(q)=A_1(q)/(2A_2(q))` lies inside `[a,b]`, with endpoint branches elsewhere. The next child should derive the fraction-free branch inequalities, denominator positivity gates, and a finite univariate Sturm/Bernstein dispatcher without introducing floating roots.

That would extend the present exact vertex lane to the first genuinely interior parameter maximizer while preserving the current source/coverage boundaries.
