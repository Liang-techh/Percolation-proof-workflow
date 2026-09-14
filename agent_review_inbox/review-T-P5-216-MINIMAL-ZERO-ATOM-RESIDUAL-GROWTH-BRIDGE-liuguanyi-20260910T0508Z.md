---
kind: review_result
review_id: review-T-P5-216-minimal-zero-atom-residual-growth-bridge-liuguanyi-20260910T0508Z
task_id: T-P5-216-MINIMAL-ZERO-ATOM-RESIDUAL-GROWTH-BRIDGE
reviewer: 柳冠一
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-10T05:08:00Z
claim_commit: d1a7b07381d5f70312c2ec0867b5da739e5647da
inspected_commit: cf066fdda159f508d62b59b859fda742150e9598
upstream_commits:
  - 4daeafdb1733f8bba97cd4576b68989cdcf31890  # T-P5-215 zero compatibility / clique decomposition
  - 6f8b539f94aba1fcf3a9106a8989ee88e7a1c38b  # T-P5-214 copositive zero support decomposition
  - 2f952c3ff2704671a74123e51d58e80f4b53b223  # T-P5-212 high-corank reduced-kernel extreme rays
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_minimal_zero_corank_one_characterization; add_atomic_zero_decomposition; add_aggregate_residual_extension; add_maximal_clique_zero_support_correspondence; replace_higher_corank_support_ray_search_by_atom_graph; add_exact_regressions
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact finite-dimensional copositive/PSD cone algebra and rational regressions; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-216 — minimal-zero atom / residual-compatible support-growth bridge

## 0. Verdict and seam closed

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-214 proves that the nonnegative zero set of a symmetric copositive matrix is a finite union of supportwise PSD principal-kernel cones. T-P5-215 then proves that once a complete zero-ray packet is available, pairwise zero-cross compatibility gives a clique decomposition and residual masks prune incompatible support growth.

The remaining mathematical gap was the phrase **"complete zero-ray packet"**: does one have to enumerate every higher-corank PSD support and extract its rays separately, or is there a canonical smaller atomic family from which every larger zero cone is recovered?

This child gives an exact answer.

For a symmetric copositive matrix `K`, define

`Z_+(K) := {x >= 0 : x^T K x = 0}`.

A nonzero zero `x` is called **support-minimal** when there is no nonzero `y in Z_+(K)` with

`supp(y) proper_subset supp(x)`.

Then:

1. support-minimal zeros are exactly the strict-positive corank-one principal-kernel rays;
2. every zero vector is a nonnegative combination of support-minimal zeros contained in its support;
3. those atoms are automatically pairwise compatible inside that decomposition;
4. therefore no higher-corank zero support contains a genuinely new primitive ray;
5. after the atoms are known, exact residual-mask clique growth reconstructs every larger zero cone;
6. for a current clique, one **aggregate residual mask** is sufficient and exact for deciding which atom may be added;
7. maximal cliques correspond exactly to maximal supports of zero vectors, and their union supports are automatically PSD principal supports.

Thus T-P5-215 Boundary A can be sharpened from "enumerate every supportwise PSD generator packet" to

**enumerate minimal-zero atoms once -> build the exact compatibility graph -> grow only residual-compatible cliques.**

This does **not** claim a polynomial-time atom enumeration algorithm. Finding all minimal supports can still be exponential in the worst case. What is removed is the redundant second enumeration of rays inside every higher-corank PSD support.

No actual P5 source identity, selector/cell/tube coverage, Float64/runtime semantics, Lean/kernel receipt, independent verification, admission, registry mutation, or parent closure is claimed.

---

## 1. Setup inherited from T-P5-214/T-P5-215

Assume throughout that

`K = K^T`

is copositive on the nonnegative orthant:

`x >= 0  =>  x^T K x >= 0`.

For every `x in Z_+(K)`, T-P5-214 gives the complementarity facts

`Kx >= 0`,

`x_i (Kx)_i = 0`,

and, if `S=supp(x)`,

`K_SS >= 0`,

`K_SS x_S = 0`.

T-P5-215 gives for any two zeros `x,y`:

`x^T K y >= 0`,

and

`x+y in Z_+(K)  <=>  x^T K y = 0`.

Call two zero rays **compatible** when their cross energy vanishes.

---

## 2. T216-A — support-minimal zero iff strict-positive corank-one principal kernel

Let `x in Z_+(K)`, `x != 0`, and put

`S := supp(x)`.

Then `x_S > 0` coordinatewise.

### Theorem A

The following are equivalent:

1. `x` is support-minimal in `Z_+(K)`;
2. `ker(K_SS) = span{x_S}`;
3. `K_SS >= 0`, `K_SS x_S=0`, and `corank(K_SS)=1`.

Equivalently, a subset `S` supports a minimal zero ray iff its principal block has a one-dimensional kernel containing a strict-positive vector.

### Proof: minimal zero implies corank one

T-P5-214 already gives

`K_SS >= 0`, `x_S in ker(K_SS)`.

Suppose `dim ker(K_SS) >= 2`. Choose

`d in ker(K_SS)`

not proportional to `x_S`.

Because `x_S>0`, the interval

`I := {t in R : x_S+t d >= 0}`

contains a neighborhood of `0`. Since `d` is not proportional to `x_S`, at least one finite nonzero endpoint `t_*` of this interval produces

`y_S := x_S+t_* d >= 0`

with at least one zero coordinate. Also `y_S != 0`; otherwise `d` would be proportional to `x_S`.

Because both `x_S` and `d` lie in `ker(K_SS)`, so does `y_S`, hence

`y_S^T K_SS y_S = 0`.

Zero-extending `y_S` outside `S` gives a nonzero `y in Z_+(K)` with

`supp(y) proper_subset S`,

contradicting support-minimality.

Therefore `dim ker(K_SS)=1`.

### Proof: corank one implies minimal zero

Conversely assume

`K_SS >= 0`,

`ker(K_SS)=span{x_S}`,

`x_S>0`.

Suppose there were a nonzero `y in Z_+(K)` with

`supp(y) proper_subset S`.

Then `y_S^T K_SS y_S=0`. Since `K_SS` is PSD,

`y_S in ker(K_SS)=span{x_S}`.

But every nonzero multiple of the strict-positive vector `x_S` has full support `S`, contradiction.

Hence `x` is support-minimal. QED.

### Exact checker consequence

Once global copositivity of `K` is independently established, an atom candidate on support `S` can be certified by the exact finite-dimensional packet

`xi_S > 0`,

`K_SS xi_S = 0`,

`rank(K_SS)=|S|-1`.

The PSD conclusion for `K_SS` is then inherited from the strict-positive zero/contact theorem of T-P5-214; it need not be guessed from floating eigenvalues.

---

## 3. T216-B — every zero decomposes into minimal atoms

Take any nonzero

`z in Z_+(K)`

and set

`U := supp(z)`.

By T-P5-214,

`K_UU >= 0`,

`z_U in ker(K_UU)`.

Consider the pointed polyhedral cone

`C_U := ker(K_UU) cap R_+^U`.

It is defined by linear equations and coordinate inequalities, so it has a finite extreme-ray generating family.

### Theorem B

Every extreme ray of `C_U`, zero-extended to the full coordinate set, is a support-minimal zero of `K`.

Consequently every `z in Z_+(K)` admits a finite decomposition

**`z = sum_a lambda_a xi_a`, `lambda_a >= 0`,**

where every `xi_a` is a support-minimal zero and

`supp(xi_a) subseteq supp(z)`.

### Proof

Let `r` span an extreme ray of `C_U`, and let

`S := supp(r)`.

If `r` were not support-minimal, there would exist a nonzero zero `y` with

`supp(y) proper_subset S`.

Since `supp(y) subset U` and `K_UU` is PSD,

`y_U^T K_UU y_U=0`

implies

`y_U in ker(K_UU)`.

For sufficiently small `alpha>0`,

`r-alpha y_U >= 0`.

Both `alpha y_U` and `r-alpha y_U` are nonzero elements of `C_U`, and they are not proportional to `r` because `y` has smaller support. This contradicts extremality of the ray `R_+ r`.

Hence every extreme ray is a minimal zero.

The finite extreme-ray generation theorem for the pointed polyhedral cone `C_U` then gives the stated decomposition of every `z_U`, and zero extension gives the full-coordinate formula. QED.

---

## 4. T216-C — the atoms in one zero decomposition are automatically compatible

Let

`z = sum_a lambda_a xi_a`, `lambda_a>0`,

be a decomposition from Theorem B inside the support `U=supp(z)`.

Each `xi_a` belongs to

`ker(K_UU)`.

Therefore for every pair `a,b`,

`xi_a^T K xi_b = (xi_a)_U^T K_UU (xi_b)_U = 0`.

Thus the atoms used to build any one zero vector form a clique in the T-P5-215 compatibility graph.

This gives the converse direction missing from a pure clique construction:

> every actual zero vector not only lies in some supportwise PSD cone; it is generated by a clique of support-minimal atoms.

---

## 5. T216-D — higher-corank supports contain no new primitive rays

Combine Theorems A and B.

If a support `U` has a PSD principal zero block with

`dim ker(K_UU) > 1`,

then every extreme ray of

`ker(K_UU) cap R_+^U`

is already a support-minimal atom on some support `S subseteq U` satisfying

`corank(K_SS)=1`.

Therefore a higher-corank support can enlarge the **cone of combinations**, but it cannot create a new primitive zero ray that was absent from the minimal-atom list.

This is the exact no-loss statement needed by the T-P5-214/T-P5-215 dispatcher.

### Corollary D1 — canonical complete atom packet

A complete atomic zero-ray packet for `K` is obtained by taking exactly one normalized generator from every support-minimal zero ray.

No additional ray extraction from higher-corank supports is required.

For example, normalize by

`1^T xi = 1`.

This removes positive scaling ambiguity without square roots or Euclidean normalization.

---

## 6. T216-E — aggregate residual gives an exact clique-extension test

Let

`C={xi_1,...,xi_m}`

be a current clique of minimal-zero atoms. Define its positive sum and residual

`z_C := xi_1+...+xi_m`,

`r_C := K z_C`.

Because the atoms are pairwise compatible,

`z_C in Z_+(K)`.

By T-P5-214,

`r_C >= 0`.

Let `eta` be another minimal-zero atom.

### Theorem E

The following are equivalent:

1. `eta` is compatible with every atom in `C`;
2. `z_C^T K eta = 0`;
3. `r_C^T eta = 0`;
4. `supp(eta) subseteq {j : (r_C)_j=0}`.

Hence one aggregate residual mask is an exact extension oracle for a partial clique.

### Proof

For every `i`, T-P5-215 gives

`xi_i^T K eta >= 0`.

Therefore

`z_C^T K eta = sum_i xi_i^T K eta`

vanishes iff every summand vanishes. This proves `1 <=> 2`.

Symmetry gives

`z_C^T K eta = (K z_C)^T eta = r_C^T eta`,

so `2 <=> 3`.

Finally `r_C>=0` and `eta>=0`, so their dot product is zero iff every positive coordinate of `r_C` is absent from the support of `eta`. Thus `3 <=> 4`. QED.

### Corollary E1 — mask intersection identity

Since

`r_C = sum_i K xi_i`

and every `Kxi_i>=0`,

`zeroMask(r_C) = intersection_i zeroMask(Kxi_i)`.

Thus maintaining the aggregate residual does not weaken the pairwise compatibility test; it compresses all currently accumulated masks into one exact object.

---

## 7. T216-F — a compatible atom clique automatically yields a PSD union support

Let `C` be a nonempty clique and define

`U_C := union_{xi in C} supp(xi)`.

The sum `z_C` from the previous section is strict-positive on `U_C`:

`(z_C)_{U_C}>0`.

Because `C` is a clique,

`z_C^T K z_C=0`.

Apply the strict-support theorem of T-P5-214 to `z_C`.

### Theorem F

**`K_{U_C,U_C} >= 0`.**

Moreover every atom in `C` lies in its ordinary kernel:

`K_{U_C,U_C} (xi)_{U_C}=0`.

Therefore the compatibility graph does more than say that selected atoms may be added: it automatically certifies that their union support is one legitimate ordinary-PSD zero face.

No separate floating PSD search on the grown support is mathematically necessary once atom compatibility and global copositivity have been established.

---

## 8. T216-G — maximal cliques exactly recover maximal zero supports

Assume a **complete** normalized minimal-atom family

`A={xi_1,...,xi_N}`.

Build the compatibility graph from T-P5-215:

`i ~ j  <=>  xi_i^T K xi_j=0`.

For a clique `C`, write

`U(C)=union_{i in C} supp(xi_i)`.

Call a coordinate set `U` a **zero support** if there exists `z in Z_+(K)` with

`supp(z)=U`.

Call it maximal if no strictly larger zero support exists.

### Theorem G

Maximal cliques of the complete atom compatibility graph are in bijection with maximal zero supports.

For a maximal clique `C`,

`U=U(C)`

is a maximal zero support, `K_UU` is PSD, and

**`Z_+(K) cap {x : supp(x) subseteq U}`
` = cone{xi_i : i in C}`
` = ker(K_UU) cap R_+^U`.**

### Proof: clique -> zero support

By Theorem F,

`z_C=sum_{i in C} xi_i`

is a zero with support exactly `U(C)`, so `U(C)` is a zero support.

Suppose there were a larger zero support `W proper_superset U(C)` with zero vector `y` strict-positive on `W`. By Theorem B, decompose `y` into minimal atoms supported in `W`. Because `K_WW` is PSD, every such atom is compatible with every atom of `C`. At least one atom in the decomposition uses a coordinate in `W\U(C)`. This gives a graph vertex outside `C` adjacent to every vertex of `C`, contradicting maximality of the clique.

Thus `U(C)` is maximal.

### Proof: maximal zero support -> clique

Let `U` be a maximal zero support and choose `z in Z_+(K)` with `supp(z)=U`.

Theorem B decomposes `z` into minimal atoms contained in `U`, and Theorem C makes those atoms pairwise compatible. Enlarge them to all minimal atoms supported in `U`; because `K_UU` is PSD, all such atoms remain mutually compatible.

If this clique were not maximal, a compatible atom with a new coordinate outside `U` could be added. Its sum with `z` would be a zero with support strictly larger than `U`, contradiction.

Thus the clique is maximal.

Finally, inside a maximal clique union support `U`, every extreme ray of `ker(K_UU) cap R_+^U` is a minimal atom by Theorem B, hence belongs to the complete clique by maximality. Therefore the atom cone equals the entire PSD kernel cone. QED.

---

## 9. Consequence for the T-P5-210 second-order debit search

T-P5-215 proves that once a complete zero-atom packet is known, a positive second-order debit witness requires at most

- one atom with positive self debit, or
- one compatible pair with positive cross debit.

T216 identifies a canonical complete packet: **all support-minimal zeros**.

Therefore the endpoint part of the higher-corank copositive branch can be routed as

`global K copositive`

`-> enumerate normalized minimal-zero atoms`

`-> exact residual compatibility graph`

`-> self-debit / compatible-pair scan`

for the yes/no T-P5-210 witness question.

There is no need to enumerate higher-corank PSD support cones merely to discover additional primitive debit directions.

If the full endpoint zero geometry is needed rather than only witness existence, enumerate maximal cliques and use Theorem G.

---

## 10. Exact rationality

Assume `K` has rational entries.

For a minimal support `S`, Theorem A gives

`rank(K_SS)=|S|-1`.

A one-dimensional kernel of a rational matrix has a nonzero rational generator. Since the real kernel ray contains a strict-positive vector, the rational generator may be oriented and positively scaled to a rational vector

`xi_S>0`.

Normalize by

`1^T xi_S=1`.

Then

- atom coordinates are rational;
- residuals `Kxi_S` are rational;
- compatibility tests are exact rational equalities;
- aggregate residual masks are exact;
- clique-union support construction introduces no roots, pseudoinverses, eigenvectors, or floating nullspace tolerances.

The remaining combinatorial search may be large, but the trusted arithmetic surface is exact and elementary.

---

## 11. Regression A — a corank-two support has no new primitive ray

Take

`K = [[1,-1,0],[-1,1,0],[0,0,0]]`.

Then for `x>=0`,

`x^T K x = (x1-x2)^2 >= 0`,

so `K` is copositive and in fact PSD.

The minimal zero atoms are

`xi_1=(1,1,0)`,

`xi_2=(0,0,1)`.

They are compatible:

`xi_1^T K xi_2=0`.

Their clique sum

`z=(1,1,1)`

has full support `{1,2,3}` and zero energy. The full block has corank two, but

`ker(K) cap R_+^3 = {a(1,1,0)+b(0,0,1) : a,b>=0}`.

Thus the larger corank-two support contributes combinations only; it contains no third primitive zero ray.

---

## 12. Regression B — maximal cliques are maximal zero supports

Take

`K = [[0,0,1],[0,0,0],[1,0,0]]`.

For `x>=0`,

`x^T K x = 2 x1 x3 >=0`,

so `K` is copositive.

The minimal atoms are the coordinate rays

`e1, e2, e3`.

Compatibility is

`e1 ~ e2`,

`e2 ~ e3`,

but

`e1 not~ e3`

because `e1^T K e3=1`.

The maximal cliques are exactly

`{e1,e2}` and `{e2,e3}`.

The zero set is exactly

`{x>=0 : x1 x3=0}`,

the union of the two corresponding coordinate-face cones. There is no zero with support `{1,2,3}`.

This regression shows that maximal-clique growth is not a heuristic compression: it reproduces the exact maximal zero-support geometry.

---

## 13. Regression C — positive high-corank contact is not primitive

Take

`K=0_2`.

The vector

`z=(1,1)>0`

is a zero on support `{1,2}`, but

`corank(K)=2`.

It is not support-minimal because

`e1`, `e2`

are smaller zeros and

`z=e1+e2`.

This is the minimal model for Theorem A: a strict-positive zero on a kernel of dimension greater than one necessarily admits support descent.

---

## 14. Regression D — atom discovery cannot start only from singleton zeros

Take

`K=[[1,-1],[-1,1]]`.

This matrix is PSD/capositive. Its unique nonnegative zero ray is

`(1,1)`.

Both singleton principal blocks are `[1]`, so neither `e1` nor `e2` is a zero.

Therefore a producer must **not** assume that every minimal atom can be reached by repeatedly growing from diagonal-zero singleton seeds. Minimal atoms themselves may first appear on supports of size greater than one.

T216 only says that once the complete minimal-atom set is known, all higher-corank zero geometry is recovered by compatibility growth. Atom enumeration remains its own exact support-search problem.

---

## 15. Failure/status semantics

The following are not mathematical FAIL states:

- a candidate support is not corank one: it is simply not a minimal atom support;
- a higher-corank support is skipped during atom enumeration: its primitive rays must already occur on smaller minimal supports, but only if atom completeness is separately established;
- a partial clique has no extension under its aggregate residual mask: that branch is maximal, not evidence that the whole zero set has been exhausted;
- maximal-clique enumeration is expensive: this is complexity, not a mathematical obstruction;
- an incomplete atom packet yields no positive debit witness: return `INCOMPLETE_MINIMAL_ZERO_PACKET`, not `NO_WITNESS`;
- a singleton-seeded search misses a size>1 atom: the search strategy is incomplete, not the theorem false.

A genuine complete no-witness conclusion still requires a certified complete minimal-atom packet plus the T-P5-215 self/pair debit exhaustion.

---

## 16. Minimal formal theorem statements

Suggested Lean/checker leaves:

1. `copositive_minimalZero_iff_principalKernel_corankOne`
   - support-minimal zero iff the strict-positive support principal block has one-dimensional kernel.

2. `psdKernelCone_extremeRay_is_minimalZero`
   - an extreme ray of `ker(K_UU) cap R_+^U` is a global support-minimal zero.

3. `copositive_zero_decompose_minimalAtoms`
   - every zero decomposes into finitely many minimal atoms contained in its support.

4. `zeroDecomposition_atoms_pairwiseCompatible`
   - atoms in one supportwise PSD-kernel decomposition have zero cross energy.

5. `higherCorankZeroSupport_noNewPrimitiveRay`
   - every extreme ray of a higher-corank support cone is already a minimal atom on a corank-one sub-support.

6. `zeroClique_aggregateResidual_extension_iff`
   - candidate atom extends a clique iff its support lies in the aggregate residual zero mask.

7. `zeroClique_unionSupport_principalPSD`
   - a compatible atom clique has PSD principal block on the union support.

8. `maximalZeroClique_iff_maximalZeroSupport`
   - under a complete normalized atom packet.

9. `maximalCliqueCone_eq_principalKernelCone`
   - the maximal clique cone equals `ker(K_UU) cap R_+^U`.

10. `rational_minimalZero_has_rational_normalizedGenerator`
    - rational corank-one support gives a rational `1^Txi=1` atom.

---

## 17. Boundaries deliberately left open

### Boundary A — atom enumeration complexity

The theorem identifies the canonical atoms but does not provide a polynomial-time algorithm for finding every minimal support. Worst-case support enumeration may remain exponential.

### Boundary B — global copositivity is inherited, not proved here

The PSD support upgrade and nonnegative residual/cross-energy facts use global copositivity of the reduced endpoint matrix `K`. This packet must not be applied to an arbitrary indefinite symmetric matrix.

### Boundary C — actual source binding

No same-key actual P5 matrix `K`, active/reduced Schur packet, selector identity, cell/tube membership, or source hash is bound here.

### Boundary D — debit semantics

T216 closes endpoint zero geometry. The self/pair second-order debit test remains the T-P5-210/T-P5-215 consumer and still needs the inherited common-zero debit copositivity semantics.

### Boundary E — runtime/formal/admission

Float64/interval sign classification, rational reification from deployed source, Lean/kernel proof, 封不觉 independent validation, P8/M4 propagation, registry mutation, and formal certificate admission all remain open.

---

## 18. Recommended handoff

For the copositive reduced-Schur branch, replace

`all supports -> PSD test -> kernel extreme rays -> merge cautiously`

by the sharper two-stage mathematical structure

**Stage 1 — atomic discovery**

`support S -> strict-positive one-dimensional principal kernel -> one normalized minimal atom`.

**Stage 2 — exact growth**

`atom residuals -> aggregate residual extension mask -> compatibility graph -> maximal cliques / self-pair debit scan`.

Once Stage 1 is complete, do not search a higher-corank support for "new" primitive rays; Theorem D proves there are none.

The next worthwhile mathematics is therefore no longer supportwise ray extraction. It is to derive a completeness certificate or branch-and-bound rule for **minimal-support atom enumeration itself**—for example, an exact rank/minor plus residual feasibility pruning rule that can reject whole families of candidate supports without assuming singleton seeds.