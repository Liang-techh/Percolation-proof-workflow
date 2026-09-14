---
kind: review_result
review_id: review-T-P5-260-uniform-cell-ternary-gram-selection-guyuefangyuan-20260910T1624Z
task_id: T-P5-260-UNIFORM-CELL-TERNARY-GRAM-SELECTION
reviewer: 古月方源
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-10T16:24:00Z
claim_commit: a2f3ec7e9ad8ef3678516bb265e2a977d0d7e05c
inspected_commit: c379aca4e9f15bb23a8f5f7ef4825a83d45df50c
upstream_commits:
  - f3ebecf85cc090d2289b3b6480e4fd00e23bea0e  # T-P5-259 ternary quartic Gram bridge
  - a24047e5b78cc0cabb191cfac7fab4a99deb1fec  # T-P5-258 binary quartic realized-direction SOS
  - 44b112238f3be56d3915e4c8aa4270d40a79830e  # T-P5-257 radial quotient-factor certificate
  - e41a4f7fab94f40593cdbe66ae7c23094a8e7134  # T-P5-256 structured Hessian tensor Gram majorant
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_affine_polytope_vertex_Gram_reduction; add_simplex_and_multiaffine_selector_transport; add_Bernstein_Gram_hierarchy; record_strict_eventual_Bernstein_Gram_completeness; add_constant_gauge_and_boundary_counterexamples
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact convexity/Gram algebra, Bernstein coefficient identities, and rational counterexamples; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-260 — Uniform cell-dependent ternary Gram selection

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-259 closes the fixed-parameter ternary quartic branch: for a homogeneous quartic in three quotient coordinates, nonnegativity is equivalent (using the classical ternary-quartic theorem) to feasibility of a six-parameter `6 x 6` PSD Gram fiber, and strict rational positivity admits a rational positive-definite Gram witness.

The remaining source-facing question is uniformity over a parameter cell. A pointwise statement

`for every s, exists t(s), G(c(s),t(s)) >= 0`

does not by itself tell a finite checker which selector class to use.

This child gives the exact finite structure for the most important parameter classes and separates what is genuinely lossless from what is only sufficient:

1. **Affine coefficient family over a convex polytope:** uniform nonnegativity is exactly equivalent to checking the finitely many vertices. Independent Gram gauges may be used at different vertices. A common constant gauge is not required.
2. **Simplex:** the vertex gauges interpolate to one global affine Gram selector.
3. **Multi-affine coefficient family over a box:** the corner gauges interpolate to one global multi-affine Gram selector by tensor-product barycentric weights; the corner test is again lossless.
4. **General rational-polynomial family on a box, uniformly strictly positive:** after sufficiently high Bernstein degree elevation, every Bernstein control quartic is strictly positive. T-P5-259 then gives rational PD Gram matrices for all control quartics, yielding a finite rational polynomial PD Gram selector. Thus in the strict ternary branch, failure of a low-degree selector search is not a mathematical obstruction; some finite polynomial selector exists.
5. **Boundary/non-strict family:** the Bernstein-control hierarchy is not complete. An explicit nonnegative family below has a simple polynomial PSD Gram selector but has a negative Bernstein control quartic at every degree.
6. **General degree >=2 parameter dependence:** vertex-only checking is invalid. An explicit one-parameter quadratic family has strictly positive endpoint quartics but a negative interior quartic.

No deployed P5 coefficient map, actual source parameter cell, quotient dimension, same-key source identity, cell/tube/trajectory coverage, Float64/interval semantics, Lean/kernel receipt, independent verification, admission, registry mutation, or parent closure is claimed.

---

# Part I — affine structure of the six-gauge Gram fiber

## 1. Setup

Let `c in R^15` denote the coefficient vector of a homogeneous ternary quartic

`p_c(x,y,z)`.

Let

`m(x,y,z) = [x^2,y^2,z^2,xy,xz,yz]^T`.

T-P5-259 gives an explicit symmetric matrix

`Gamma(c,t) in Sym_6`, `t in R^6`,

such that

**(1.1)** `m(u)^T Gamma(c,t) m(u) = 2 p_c(u)`

and every Gram matrix representing `2p_c` is uniquely of this form.

The explicit formula is affine-linear jointly in `(c,t)`. Therefore whenever scalars `lambda_i` satisfy `sum_i lambda_i = 1`,

**(1.2)**

`Gamma(sum_i lambda_i c_i, sum_i lambda_i t_i)`

`= sum_i lambda_i Gamma(c_i,t_i)`.

This elementary identity is the entire transport mechanism for the cell-dependent results below.

When additionally `lambda_i >= 0`, PSD convexity gives

**(1.3)**

`Gamma(c_i,t_i) >= 0 for all i`

`=> Gamma(sum lambda_i c_i, sum lambda_i t_i) >= 0`.

No matrix square root, eigenvector, pseudoinverse, SDP duality, or numerical rank test is involved.

---

# Part II — affine coefficient families on convex polytopes

## 2. Theorem 1 — lossless vertex reduction

Let

`P = conv{v_1,...,v_N} subset R^d`

be a convex polytope, and let the ternary quartic coefficient map be affine:

**(2.1)** `c(s) = C s + c0`.

Then the following are equivalent:

1. `p_{c(s)}(u) >= 0` for every `s in P` and every `u in R^3`;
2. `p_{c(v_i)}(u) >= 0` for every vertex `v_i` and every `u`.

### Proof

The forward implication is trivial.

For the reverse implication, fix `s in P`. Choose any convex representation

`s = sum_i lambda_i v_i`, `lambda_i >= 0`, `sum_i lambda_i = 1`.

By affinity,

`c(s)=sum_i lambda_i c(v_i)`.

Therefore for every fixed physical direction `u`,

**(2.2)**

`p_{c(s)}(u) = sum_i lambda_i p_{c(v_i)}(u) >= 0`.

So the whole continuum cell is exactly reduced to finitely many vertex quartics.

This statement is more general than SOS/Gram theory; it is simply convexity in the parameter. The ternary Gram theorem becomes useful because it provides a finite exact certificate for each vertex quartic.

## 3. Corollary — independent vertex Gram gauges are enough

Assume the hypotheses above. If for every vertex there is a gauge `t_i` such that

`G_i := Gamma(c(v_i),t_i) >= 0`,

then for any convex representation of `s`, define

**(3.1)** `t_s := sum_i lambda_i t_i`.

Using (1.2),

**(3.2)**

`Gamma(c(s),t_s) = sum_i lambda_i G_i >= 0`.

Hence the parameterized Gram fiber is feasible at every point.

Important consequence: **uniform quartic nonnegativity does not require one common six-gauge vector.** The gauges may vary from vertex to vertex.

Conversely, by T-P5-259/Hilbert, if every vertex quartic is nonnegative then each vertex has a real PSD Gram witness. Thus, at the mathematical real layer, vertex Gram feasibility is lossless for affine coefficient families.

### Rational serialization boundary

If every rational vertex quartic is **strictly** positive away from the origin, T-P5-259 gives a rational PD gauge `t_i` at every vertex. Then all convex interpolation formulas below can be kept rational.

For merely semidefinite rational vertex quartics, T-P5-259 does not by itself guarantee a rational PSD Gram point on the boundary. The real theorem remains valid, but a rational checker may need an algebraic witness or an additional rational facial argument. Do not silently infer rational serialization from real feasibility on a singular Gram face.

---

# Part III — constant gauge versus variable selector

## 4. Theorem 2 — exact common-gauge criterion

For each vertex define the gauge spectrahedron

**(4.1)**

`F_i = { t in R^6 : Gamma(c(v_i),t) >= 0 }`.

There exists one constant gauge `t_*` valid on the whole affine polytope iff

**(4.2)** `intersection_i F_i` is nonempty.

Equivalently,

**(4.3)**

`exists t_*, Gamma(c(s),t_*) >= 0 for all s in P`

iff

`exists t_*, Gamma(c(v_i),t_*) >= 0 for all vertices i`.

### Proof

Necessity is restriction to vertices.

For sufficiency, the matrix `Gamma(c(s),t_*)` is affine in `s`, so for `s=sum lambda_i v_i`,

`Gamma(c(s),t_*)=sum lambda_i Gamma(c(v_i),t_*)>=0`.

Thus common-gauge search is a finite exact question, but it is strictly stronger than uniform nonnegativity.

## 5. Exact regression — constant gauge can fail while the family is uniformly nonnegative

Take `s in [0,1]` and

**(5.1)**

`p_s(x,y,z)`

`= (1-s)(x^2-y^2)^2 + 4s x^2 y^2 + z^4`.

Every term in this convex combination is nonnegative, so `p_s>=0` for all `s`.

In T-P5-259 coefficient notation,

`a=b=1-s`, `c=1`, `j=-2+6s`,

all other quartic coefficients zero.

Choose

`t1(s)=-2(1-s)`, `t2=t3=t4=t5=t6=0`.

Then the nonzero Gram blocks are

**(5.2)**

`[[2(1-s), -2(1-s)],`

` [-2(1-s), 2(1-s)]]`

on `[x^2,y^2]`,

`8s`

on `[xy]`, and `2` on `[z^2]`. Hence the Gram is PSD for every `s`, and the gauge selector is affine.

However no constant gauge can work.

At `s=0`, restrict any ternary PSD Gram to the principal subspace `[x^2,y^2,xy]`, equivalently set `z=0`. The binary quartic is

`(x^2-y^2)^2`.

Its one-parameter binary Gram family is

`[[2,0,tau],[0,-4-2tau,0],[tau,0,2]]`,

which is PSD only for `tau=-2`.

At `s=1`, the restricted binary quartic is `4x^2y^2`; its Gram is PSD only for `tau=0`.

The ternary gauge `t1` is exactly this binary `x^2-y^2` Gram cross-entry under restriction. Hence a constant ternary gauge would need simultaneously `t1=-2` and `t1=0`, impossible.

Therefore:

**(5.3)**

`uniform p_s >=0` does **not** imply `exists constant Gram gauge`.

A checker must route common-gauge infeasibility to a variable-selector branch, not to physical FAIL.

---

# Part IV — simplex and general polytope selectors

## 6. Theorem 3 — simplex affine selector

Let `P=conv{v_0,...,v_d}` be a simplex and let `lambda_i(s)` be its barycentric coordinates. For an affine coefficient map and vertex gauges `t_i` with PSD Grams, define

**(6.1)**

`t(s)=sum_{i=0}^d lambda_i(s)t_i`.

Because barycentric coordinates on a simplex are affine,

- `t(s)` is an affine six-vector;
- `Gamma(c(s),t(s)) = sum lambda_i(s) G_i >=0`.

So every vertex-feasible affine ternary-quartic family on a simplex has an explicit affine Gram selector.

If the simplex vertices and `t_i` are rational, the barycentric functions and the selector are rational affine after exact inversion of the rational simplex matrix.

## 7. General polytope — piecewise-affine selector

For a general convex polytope, one global affine selector need not interpolate arbitrarily chosen gauges at all vertices. But a triangulation gives an exact finite replacement.

Choose one Gram gauge `t_i` for every polytope vertex and a triangulation into simplices using those vertices. On each simplex use the barycentric formula (6.1).

Because neighboring simplices use the same gauge value on every shared vertex, their affine interpolants agree on the shared face. Hence the resulting selector is continuous and piecewise affine.

The selector is therefore finite-checker friendly:

- a finite simplex list;
- one vertex Gram packet per polytope vertex;
- exact barycentric interpolation;
- no global SDP over parameter/state space.

For proving only `p_s>=0`, even the triangulation is unnecessary: Theorem 1 already proves uniformity directly from the vertex quartics. The triangulation matters only if a downstream consumer requires an explicit pointwise Gram matrix.

---

# Part V — multi-affine box families

## 8. Theorem 4 — exact corner interpolation

Normalize a parameter box to

`B=[0,1]^d`.

Let the coefficient map `c(s)` be **multi-affine**, meaning affine in each coordinate separately. Cross terms such as `s1*s2` are allowed, but no variable appears with power larger than one.

For each corner `eps in {0,1}^d`, define

**(8.1)**

`w_eps(s) = product_j [ eps_j*s_j + (1-eps_j)*(1-s_j) ]`.

Then

- `w_eps(s)>=0` on the box;
- `sum_eps w_eps(s)=1`;
- every multi-affine map satisfies the exact interpolation formula

**(8.2)**

`c(s)=sum_eps w_eps(s)c(eps)`.

Therefore the following are equivalent:

1. `p_s(u)>=0` for every `s in B,u`;
2. every corner quartic `p_eps` is nonnegative.

If corner gauges `t_eps` are supplied, then

**(8.3)**

`t(s)=sum_eps w_eps(s)t_eps`

is a global multi-affine gauge selector and

**(8.4)**

`Gamma(c(s),t(s))=sum_eps w_eps(s)Gamma(c(eps),t_eps)>=0`.

This is the exact box analogue of simplex interpolation and is likely the highest-value deployed branch if source coefficients are produced by independent interval-affine parameters.

### Important scope

The lossless corner theorem applies to **multi-affine** parameter dependence, not arbitrary polynomials. A term `s_j^2` already leaves this class.

---

# Part VI — why general polynomial families need more than vertices

## 9. Exact counterexample — endpoint checks can all pass while the interior fails

Take `s in [-1,1]` and

**(9.1)**

`p_s(x,y,z) = (s^2-1/4)x^4 + y^4 + z^4`.

At the two cell vertices,

`p_{-1}=p_1=(3/4)x^4+y^4+z^4`,

which is strictly positive for every nonzero `(x,y,z)`.

But at the interior point `s=0`,

`p_0(1,0,0)=-1/4<0`.

Thus:

**(9.2)**

for quadratic-or-higher parameter dependence, vertex-only Gram checks are unsound unless additional structure such as multi-affinity is proved.

Failure here is a genuine physical/mathematical failure because an explicit interior state is supplied. In contrast, failure of a particular selector ansatz without a negative state remains only a proof-method obstruction.

---

# Part VII — Bernstein Gram hierarchy for polynomial parameter dependence

## 10. Exact Bernstein decomposition

Work on the normalized box `[0,1]^d`. Let `p(s,u)` be polynomial in `s` and homogeneous quartic in `u`, with rational coefficients.

Choose a tensor degree `n=(n_1,...,n_d)` at least as large as the parameter degree in every coordinate. Write the exact tensor Bernstein expansion

**(10.1)**

`p(s,u)=sum_{alpha<=n} B_{alpha,n}(s) p_{alpha,n}(u)`,

where

**(10.2)**

`B_{alpha,n}(s)=product_j binom(n_j,alpha_j) s_j^(alpha_j) (1-s_j)^(n_j-alpha_j)`.

For every `s in [0,1]^d`,

`B_{alpha,n}(s)>=0`,

and

`sum_alpha B_{alpha,n}(s)=1`.

The control quartics `p_{alpha,n}` are homogeneous ternary quartics. If the original parameter polynomial is rational, every control quartic has rational coefficients because the monomial-to-Bernstein conversion uses only rational binomial ratios.

For one variable, the exact degree-`n` Bernstein coefficient of the monomial `s^r` is

**(10.3)**

`binom(k,r)/binom(n,r) = (k)_r/(n)_r`.

The tensor-product formula is the product of these factors across coordinates.

## 11. Theorem 5 — PSD control Grams give a global polynomial selector

Assume every Bernstein control quartic has a Gram witness

`G_alpha=Gamma(c_alpha,t_alpha)>=0`.

Define

**(11.1)**

`G(s)=sum_alpha B_{alpha,n}(s)G_alpha`

and

**(11.2)**

`t(s)=sum_alpha B_{alpha,n}(s)t_alpha`.

Then by joint Gram affinity,

**(11.3)**

`G(s)=Gamma(c(s),t(s))`,

and by convexity,

**(11.4)** `G(s)>=0` on the whole box.

Therefore

`p(s,u)>=0` for every parameter and physical state.

This is a finite exact certificate:

- finitely many rational Bernstein control quartics;
- six gauges per control quartic;
- exact PSD/PD checks on fixed `6 x 6` matrices;
- a symbolic Bernstein identity.

No sampled parameter grid is used.

When `n_j=1` for all coordinates, the Bernstein control quartics are exactly the box corners, so Theorem 5 reduces to the lossless multi-affine theorem.

## 12. Strict branch — eventual completeness of the Bernstein-Gram hierarchy

The key new result is that the Bernstein hierarchy is not merely sufficient in the uniformly strict rational-polynomial ternary branch: at some finite degree it must succeed.

### Theorem 6

Let

`p(s,u) in Q[s_1,...,s_d,x,y,z]`

be homogeneous of degree four in `u`, and let `s in [0,1]^d`.

Assume

**(12.1)**

`p(s,u)>0` for every `s` and every `u!=0`.

Then there exists a finite tensor Bernstein degree `n` such that every control quartic `p_{alpha,n}` is strictly positive away from the origin.

Consequently, using the strict-rational ternary Gram result of T-P5-259, there exist rational PD matrices `G_alpha` representing the control quartics, and (11.1) is a **rational polynomial positive-definite Gram selector** for the whole cell.

### Proof

Because `p` is continuous and homogeneous, restrict `u` to the unit sphere `S^2`. The compact set

`[0,1]^d x S^2`

has a strict uniform margin

**(12.2)**

`mu := min p(s,u) > 0`.

For a fixed scalar parameter monomial `s^gamma`, its degree-elevated Bernstein control coefficient at multi-index `alpha` is

**(12.3)**

`product_j (alpha_j)_{gamma_j}/(n_j)_{gamma_j}`.

Uniformly over `0<=alpha_j<=n_j`,

`(alpha_j)_{r}/(n_j)_{r} - (alpha_j/n_j)^r -> 0`

as `n_j->infinity` for every fixed `r`.

There are only finitely many parameter monomials and fifteen quartic state coefficients. Hence, in any fixed norm on the finite-dimensional space of ternary quartic forms,

**(12.4)**

`sup_alpha || p_{alpha,n} - p(alpha/n, .) || -> 0`.

All norms on this finite-dimensional space are equivalent, so in particular the evaluation error on the unit sphere tends uniformly to zero. Choose `n` large enough that

**(12.5)**

`|p_{alpha,n}(u)-p(alpha/n,u)| < mu/2`

for every `alpha` and every `u in S^2`.

Then

`p_{alpha,n}(u) >= mu/2 > 0`

on `S^2`, so every control quartic is positive definite.

Because all input coefficients and binomial ratios are rational, each `p_{alpha,n}` is rational. T-P5-259 supplies a rational PD Gram `G_alpha`. Their Bernstein convex combination is therefore a rational polynomial PD Gram selector.

### Consequence for search semantics

For a uniformly strictly positive rational-polynomial ternary family, there is **no genuine finite-selector obstruction** at the level of existence: some finite polynomial selector always exists.

Thus:

- failure at degree `n` => increase degree/refine cell; **inconclusive**;
- success => exact global certificate;
- only an explicit negative state or a proof contradicting strict positivity may be called mathematical FAIL.

No effective a priori degree bound is claimed here. The theorem is an existence/completeness result for the hierarchy, not a complexity bound.

---

# Part VIII — non-strict boundary: Bernstein controls are not complete

## 13. A family with a polynomial PSD Gram selector but negative Bernstein controls at every degree

Take `s in [0,1]` and

**(13.1)**

`p_s(x,y,z)=(s-1/2)^2 x^4 + y^4 + z^4`.

This family is globally nonnegative. It even has the explicit polynomial PSD Gram selector

**(13.2)**

`G(s)=diag(2(s-1/2)^2, 2, 2, 0, 0, 0)`

in the monomial order `[x^2,y^2,z^2,xy,xz,yz]`.

So there is no physical obstruction and no polynomial-selector obstruction.

Now examine the scalar polynomial

`f(s)=(s-1/2)^2=s^2-s+1/4`.

Its degree-`n` Bernstein coefficient at index `k` is

**(13.3)**

`b_{k,n} = k(k-1)/(n(n-1)) - k/n + 1/4`, `n>=2`.

If `n` is even, choose `k=n/2`. Then

**(13.4)** `b_{n/2,n} = -1/[4(n-1)] < 0`.

If `n` is odd, choose `k=(n+1)/2`. Then

**(13.5)** `b_{(n+1)/2,n} = -1/(4n) < 0`.

Therefore **every finite Bernstein degree has at least one negative control coefficient** for the `x^4` term.

The corresponding control quartic is

`b_{k,n}x^4+y^4+z^4`,

which is negative at `(1,0,0)` and cannot have a PSD Gram.

Hence the coefficientwise Bernstein-control-Gram hierarchy fails at every degree even though the family has the explicit polynomial PSD selector (13.2).

This gives an exact boundary classifier:

**(13.6)**

`Bernstein control failure` is not equivalent to `no polynomial Gram selector` when the family touches the PSD boundary.

The strict margin in Theorem 6 is essential.

---

# Part IX — checker-facing dispatcher

## 14. Exact hierarchy

For a source-indexed ternary homogeneous quartic slack, the mathematically safe dispatcher is:

### Branch A — affine coefficient map on a convex polytope

- prove exact affinity of the fifteen coefficients;
- enumerate the true polytope vertices;
- certify one PSD Gram per vertex;
- conclude uniform nonnegativity exactly.

A common gauge is optional. Common-gauge infeasibility is not physical failure.

### Branch B — multi-affine coefficient map on a box

- prove exact multi-affinity;
- certify one PSD Gram per corner;
- use tensor barycentric interpolation;
- obtain an explicit global multi-affine Gram selector.

This branch is lossless.

### Branch C — general rational-polynomial family with a strict margin

- normalize the parameter cell to a rational box or partition it into rational boxes;
- form exact degree-elevated Bernstein control quartics;
- search rational PD six-gauge witnesses for all controls;
- on success, build the rational polynomial Gram selector (11.1).

Theorem 6 says some finite degree succeeds if strict positivity is genuinely true. Failure at a chosen degree is `INCONCLUSIVE_FROM_DEGREE`.

### Branch D — non-strict/boundary family

Coefficientwise Bernstein controls may fail forever. Try instead:

- direct polynomial Gram selector;
- cell subdivision;
- common-face/facial reduction of the Gram cone;
- source-specific factorization/syzygy;
- or an exact negative physical state.

Do **not** turn selector failure into physical FAIL.

### Branch E — arbitrary degree with only vertex data

Vertex checks are invalid. The quadratic counterexample (9.1) must remain a regression against accidental endpoint-only admission.

---

# Part X — theorem decomposition for Lean/checker work

## 15. Small algebraic leaves suitable for early formalization

The first formal leaves do not need Hilbert's theorem.

Suggested statements:

### `ternaryGram_convexCombination`

Assume `sum_i lambda_i=1`.

Prove

`Gamma(sum lambda_i c_i, sum lambda_i t_i)`

`= sum lambda_i Gamma(c_i,t_i)`.

This is finite linear algebra/ring normalization.

### `psd_convexCombination`

For `lambda_i>=0`, `sum lambda_i=1`, and `G_i>=0`, prove

`sum lambda_i G_i >=0`.

### `affineQuartic_nonneg_of_vertex_nonneg`

Input an explicit convex-combination witness for `s`. Consume coefficient affinity and vertex quartic nonnegativity. Conclude `p_s(u)>=0`.

This can be written without a polytope library at first: the theorem only needs a finite family of weights.

### `commonGauge_on_convexHull_of_vertices`

If the same `t` gives PSD Gram at all vertices, prove it gives PSD Gram at any supplied convex combination.

### `simplexGaugeSelector_psd`

Consume barycentric weights and vertex Gram packets; return the affine selector and PSD result.

### `multiaffineBox_vertexExpansion`

Prove the tensor-product interpolation identity (8.2), first for scalar maps, then componentwise for the fifteen coefficient vector.

### `multiaffineBox_GramSelector_psd`

Consume corner PSD Grams and conclude (8.4).

### `bernsteinGramSelector_psd`

Given nonnegative Bernstein weights summing to one and PSD control Grams, prove the matrix convex combination is PSD and represents the exact parameterized quartic.

These leaves are elementary and independent of source binding.

## 16. Heavier mathematical dependencies

The following should remain named dependencies until separately formalized:

1. T-P5-259's reverse ternary-quartic theorem `p>=0 -> exists PSD Gram`;
2. strict rational positive ternary quartic `->` rational PD Gram;
3. uniform degree-elevation convergence of Bernstein control coefficients;
4. compactness argument producing the strict margin `mu>0`.

A practical first Lean packet does not need to formalize Theorem 6. The checker can consume a **supplied finite Bernstein degree and supplied control Grams**; Theorem 6 is the mathematical completeness rationale for continuing the hierarchy when low degrees fail.

---

# Part XI — exact regressions to preserve

## 17. Regression R1 — no common gauge

Family (5.1):

- uniform nonnegative;
- affine selector exists;
- endpoint binary restrictions force `t1(0)=-2` and `t1(1)=0`;
- therefore no constant gauge.

Expected routing: `VARIABLE_SELECTOR_REQUIRED`, not FAIL.

## 18. Regression R2 — vertex-only unsound beyond multi-affine

Family (9.1):

- both endpoints strictly positive;
- `s=0,u=(1,0,0)` gives `-1/4`.

Expected routing: actual mathematical FAIL for the family; endpoint-only checker must reject its own inference.

## 19. Regression R3 — Bernstein boundary incompleteness

Family (13.1):

- exact polynomial PSD Gram selector exists;
- for every degree `n>=2`, a central Bernstein control quartic is negative.

Expected routing: `INCONCLUSIVE_FROM_BERNSTEIN_CONTROLS`; direct selector branch remains open.

---

# Part XII — remaining boundary and next seam

## 20. What this child does not close

This review does not prove:

1. that the deployed P5 quotient dimension is exactly three;
2. that the deployed fifteen quartic coefficients are affine, multi-affine, or polynomial in a particular certified source parameter;
3. that the parameter cell used by the source producer is the same cell used by the Lyapunov consumer;
4. any source-to-coefficient identity, Hessian/factor identity, cell/tube/trajectory coverage, FD halo, or continuation theorem;
5. any Float64/interval coefficient enclosure;
6. any concrete rational Gram packet for deployed coefficients;
7. Lean/kernel compilation;
8. independent verification by 封不觉;
9. admission, registry mutation, or parent closure.

## 21. Next distinct mathematical seam

The remaining selector difficulty is now concentrated on the **semidefinite boundary**.

The strict branch has an eventual rational polynomial selector; affine/multi-affine branches have exact finite vertex/corner selectors. The genuinely new problem is therefore:

**parameterized Gram facial reduction.**

If a non-strict family lies in a fixed proper face of the PSD cone, determine whether one can certify a common rational kernel/subspace, quotient that face, and recover a uniformly positive-definite reduced Gram family. If so, the strict Bernstein argument can be rerun on the reduced face. If the active Gram face changes with the parameter, identify the minimal piecewise face stratification or an exact obstruction.

This is a materially different child from another selector-degree search and is the natural next route for boundary families such as (13.1).

Status remains **CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding**.