---
kind: review_result
review_id: review-T-P5-221-cross-chart-fraction-free-bilinear-transport-guyuefangyuan-20260910T0620Z
task_id: T-P5-221-CROSS-CHART-FRACTION-FREE-BILINEAR-TRANSPORT
reviewer: 古月方源
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-10T06:20:00Z
claim_commit: dde9b3080554215652def10db0a07c9fc344da82
inspected_commit: f055d39594e4314f90c0e6bafe2ed6ad9d6c32bb
upstream_commits:
  - a81288eb83a2a4e7d3c596893c200dd814197bc0  # T-P5-217 complete PD-prefix atom search
  - 8e18bf65daa1c307c154506d86e85bd5b5df6c7b  # T-P5-219 same-chart compatibility/debit reduction
  - 3aeaf3ce38bbc455da4c1a3162236567b6a7d0ae  # T-P5-220 nested-chart projective transport
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_cross_chart_reconstruction_numerator; add_cross_chart_energy_pairing; add_transition_reciprocity; add_cross_chart_residual_mask; add_cross_chart_debit_pairing; add_projective_chart_invariance; add_exact_regression
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact finite-dimensional block algebra, copositive zero complementarity, projective scaling, rational regression; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-221 — cross-chart fraction-free bilinear transport

## 0. Verdict and seam closed

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-217 can emit minimal-zero atoms from different PD-prefix branches. T-P5-219 gives a very cheap compatibility/debit consumer once two atoms live in the same reduced chart. T-P5-220 proves that nested PD-prefix refinements represent the same physical object up to a positive graded projective scale.

The remaining mathematical seam is a pair of atoms represented in **different, non-nested PD-prefix charts**. Their reduced coordinates have different meanings, so one may not feed one chart's coordinate vector into the other chart's residual mask.

This child supplies a universal chart glue. Each PD-prefix chart has an exact full-coordinate **reconstruction numerator map** `M_T`. For two arbitrary charts `a,b`, define

`Khat_ab := M_a^T K M_b`.

Then

**`d_a d_b * x_a(lambda)^T K x_b(mu) = lambda^T Khat_ab mu`.**

No nesting assumption is required. Moreover `Khat_ab` can be computed from one local Schur numerator plus a small cross-chart extraction map, without reconstructing rational physical vectors:

**`Khat_ab = Hhat_a P_{a<-b} = P_{b<-a}^T Hhat_b`.**

For genuine copositive zeros, this yields an exact cross-chart residual-mask test. For an arbitrary symmetric endpoint/debit form `Q`, the parallel packet

`Qhat_ab=M_a^T Q M_b`

transports all self/cross debit signs. The packets are invariant under T-P5-220 nested refinement in the only correct sense: they scale by a positive product of chart scales, so zero/sign statements are unchanged, while quantitative pair formulas must carry the denominators with their homogeneous degree.

No actual same-key P5 matrix, selector/cell/tube binding, trajectory coverage, Float64 semantics, Lean receipt, independent validation, admission, registry mutation, or parent closure is claimed.

---

## 1. One PD-prefix chart as a fraction-free numerator map

Let `K=K^T` be an `n x n` matrix. Pick a coordinate partition `T union R={1,...,n}` and write

`K = [[A,B],[B^T,D]]`

in `(T,R)` order, with

`A=A^T>0`.

Set

`d := det(A)>0`,

`C := -adj(A) B`,

`Hhat := d D - B^T adj(A) B`.

Define the full-coordinate linear numerator map

`M_T : R^R -> R^n`

by

`(M_T lambda)_T = C lambda`,

`(M_T lambda)_R = d lambda`.

Thus the physical reconstruction used by T-P5-218/219 is simply

**`x_T(lambda)=M_T lambda / d`.**

The key fraction-free residual identity is

### Theorem A

**`K M_T = E_R Hhat`,**

where `E_R` embeds an `R`-vector into full coordinates with zeros on `T`.

### Proof

On the `T` rows,

`A C + d B`

`= -A adj(A)B + dB`

`= -dB+dB=0`.

On the `R` rows,

`B^T C+dD`

`= -B^T adj(A)B+dD`

`= Hhat`.

So the full residual numerator is exactly zero on the eliminated prefix and equals `Hhat lambda` on the remaining coordinates. QED.

For a same-chart pair this immediately recovers T-P5-219:

`M_T^T K M_T = d Hhat`.

---

## 2. Two arbitrary PD-prefix charts

Now choose two legal PD-prefix charts `a` and `b` for the same full matrix `K`. They need not be nested, disjoint, or of equal dimension.

For chart `a` write

`(T_a,R_a,d_a,M_a,Hhat_a)`.

For chart `b` write

`(T_b,R_b,d_b,M_b,Hhat_b)`.

Define the cross-chart energy numerator matrix

**`Khat_ab := M_a^T K M_b`.**

It has shape `|R_a| x |R_b|` and need not be symmetric; instead

**`Khat_ba = Khat_ab^T`.**

### Theorem B — cross-chart fraction-free energy identity

For arbitrary reduced vectors `lambda in R^{R_a}` and `mu in R^{R_b}`,

**`d_a d_b * x_a(lambda)^T K x_b(mu)`**

**`= lambda^T Khat_ab mu`.**

### Proof

Since `x_a=M_a lambda/d_a` and `x_b=M_b mu/d_b`,

`x_a^T K x_b`

`= lambda^T M_a^T K M_b mu/(d_a d_b)`.

Multiply by the strictly positive denominator. QED.

No copositivity premise is needed for Theorem B. It is pure block algebra.

---

## 3. Cross-chart transition matrices and reciprocity

Let `E_R^T` denote coordinate restriction from the full state to the coordinates in `R`.

Define the chart extraction/transition matrices

**`P_{a<-b} := E_{R_a}^T M_b`,**

**`P_{b<-a} := E_{R_b}^T M_a`.**

These matrices do **not** claim that every reduced vector in chart `b` is a legal reduced vector in chart `a`. They only extract from a chart-`b` numerator the coordinates on which the chart-`a` residual can be nonzero.

Using Theorem A,

`K M_a = E_{R_a} Hhat_a`,

`K M_b = E_{R_b} Hhat_b`.

Therefore

`Khat_ab`

`= M_a^T K M_b`

`= (K M_a)^T M_b`

`= Hhat_a E_{R_a}^T M_b`

`= Hhat_a P_{a<-b}`.

The other orientation gives

`Khat_ab`

`= M_a^T E_{R_b}Hhat_b`

`= P_{b<-a}^T Hhat_b`.

Hence:

### Theorem C — exact cross-chart reciprocity

**`Hhat_a P_{a<-b} = P_{b<-a}^T Hhat_b`.**

This is a useful checker-visible seam. Two independently produced chart packets that claim the same full `K` cannot violate this identity.

For `a=b`, `P_{a<-a}=d_a I` on the remaining coordinates, so Theorem C reduces to

`M_a^T K M_a=d_a Hhat_a`,

exactly the T-P5-219 self-chart formula.

---

## 4. Genuine copositive zeros: cross-chart residual-mask test

Now assume `K` is copositive on the nonnegative orthant.

Let

`x_a = x_a(lambda)>=0`,

`x_b = x_b(mu)>=0`

be genuine zeros:

`x_a^T K x_a=0`,

`x_b^T K x_b=0`.

Copositive zero complementarity gives

`Kx_a>=0`, `Kx_b>=0`.

Since `d_a,d_b>0`, the numerator vectors

`v_a:=M_a lambda=d_a x_a`,

`v_b:=M_b mu=d_b x_b`

are nonnegative, and Theorem A gives

`Hhat_a lambda>=0`,

`Hhat_b mu>=0`.

Also

`P_{a<-b}mu=E_{R_a}^T v_b>=0`.

Therefore the cross energy numerator is a dot product of two nonnegative vectors:

### Theorem D

**`lambda^T Khat_ab mu`**

**`= (Hhat_a lambda)^T (P_{a<-b}mu) >=0`.**

Consequently the two zero rays are compatible exactly when

**`(Hhat_a lambda)^T(P_{a<-b}mu)=0`.**

Equivalently,

**`supp(P_{a<-b}mu) subseteq {j in R_a : (Hhat_a lambda)_j=0}`.**

The symmetric chart-`b` mask gives the same answer by Theorem C.

This is the correct extension of T-P5-219's same-chart bit-mask rule. The transition matrix is essential: `mu` by itself lives in the wrong coordinate system.

### Boundary

`P_{a<-b}` may contain negative entries as a matrix. Only on a **genuine reconstruction-feasible zero packet** do we know `P_{a<-b}mu>=0`. Therefore Theorem D's support-mask interpretation must not be applied to arbitrary reduced test vectors outside the reconstruction cone.

---

## 5. Global chart-glued zero graph

Suppose a complete atom search has emitted genuine zero atoms `x_i`, possibly from many charts. For each packet choose its chart numerator `v_i=M_i lambda_i=d_i x_i`.

For any pair define

`k_ij:=v_i^T K v_j`.

Copositive zero complementarity implies `k_ij>=0`. Moreover

`(sum_i theta_i v_i)^T K (sum_i theta_i v_i)`

`=2 sum_{i<j} theta_i theta_j k_ij`

for `theta_i>=0`, because every self term vanishes.

Hence a family of atoms spans a zero cone iff every pair has `k_ij=0`.

The T-P5-215 compatibility-clique theorem therefore remains valid when atoms come from heterogeneous PD-prefix charts: compute each edge with `Khat_ij`, not by coercing all local coordinates into one chart.

This is especially useful after T-P5-217, because a branch-and-bound implementation is free to emit an atom at whichever PD prefix reaches its singular boundary first.

---

## 6. Arbitrary endpoint/debit bilinear form

Let `Q=Q^T` be any fixed full-coordinate symmetric endpoint/debit form. No positivity hypothesis is needed for the algebra below.

Define

**`Qhat_ab := M_a^T Q M_b`.**

Then:

### Theorem E — cross-chart debit identity

**`d_a d_b * x_a(lambda)^T Q x_b(mu)`**

**`=lambda^T Qhat_ab mu`.**

Also

`Qhat_ba=Qhat_ab^T`.

For `a=b`, this is exactly the T-P5-219 fraction-free debit pullback

`Qhat_aa=M_a^T Q M_a`.

Thus self-debit and pair-debit signs can be scanned without converting the atoms to rational full-state vectors.

If the T-P5-210/T-P5-215 small-perturbation premise makes the debit Gram copositive on a zero clique, their sparse self/pair witness alternative can be consumed across mixed charts with the same logic. The present child does not re-prove that premise.

---

## 7. Correct denominator clearing for a mixed-chart pair

A subtlety appears when one evaluates the **sum** of two physical representatives rather than a single cross sign.

Let

`x=x_a(lambda)+x_b(mu)`.

A common numerator is

**`w := d_b M_a lambda + d_a M_b mu`,**

so

`x=w/(d_a d_b)`.

For any symmetric `Q`,

`(d_a d_b)^2 x^TQx`

`= d_b^2 lambda^T Qhat_aa lambda`

`  + 2 d_a d_b lambda^T Qhat_ab mu`

`  + d_a^2 mu^T Qhat_bb mu`.

This formula is the mixed-chart analogue of T-P5-220's graded normalization rule.

It is **wrong** to add raw self/cross `Qhat` entries from different chart scales without the `d_a,d_b` weights. Sign-only tests of a single self or cross term are safe because the omitted factor is positive; quantitative sums and margins must be denominator-homogeneous.

---

## 8. Positive projective chart invariance

T-P5-220 shows that nested fraction-free refinement may replace a chart packet by a positively rescaled representation of the same physical map.

Abstractly, suppose chart `a` is rescaled by `alpha_a>0`:

`M_a' = alpha_a M_a`,

`d_a' = alpha_a d_a`,

`Hhat_a' = alpha_a Hhat_a`.

Likewise chart `b` is rescaled by `alpha_b>0`.

Then

`x_a'=M_a'lambda/d_a'=x_a`,

and

`Khat_ab' = alpha_a alpha_b Khat_ab`,

`Qhat_ab' = alpha_a alpha_b Qhat_ab`,

`P_{a<-b}' = alpha_b P_{a<-b}`.

Thus

`Hhat_a' P_{a<-b}'`

`=alpha_a alpha_b Hhat_a P_{a<-b}`.

### Theorem F

Under arbitrary positive projective chart rescaling:

- cross-energy zero/nonzero sign is invariant;
- compatibility is invariant;
- cross-debit sign is invariant;
- positive residual masks are invariant;
- the common-denominator pair formula in Section 7 is invariant as a physical quadratic form.

Therefore the T-P5-220 nested-prefix refinement can be applied independently on either side of a T-P5-221 pair edge without changing the physical edge classification.

The chart-local raw matrices are not canonical numerical objects; their positive projective classes with denominators are canonical.

---

## 9. Exact counterexample: local masks without transition give a false compatibility edge

Take

`K = [[ 1,-1,-1],`
`     [-1, 1, 2],`
`     [-1, 2, 1]]`.

For `x,y,z>=0`,

`[x,y,z]K[x,y,z]^T`

`=(x-y-z)^2+2yz>=0`,

so `K` is copositive.

It has the two minimal zero rays

`a=(1,1,0)`,

`b=(1,0,1)`.

They are **not** compatible because

`Ka=(0,0,1)`,

hence

`a^T K b=1`.

### Chart a

Choose prefix `T_a={1}` and remaining order `R_a=(2,3)`.

Then

`d_a=1`,

`C_a=(1,1)`,

`Hhat_a=[[0,1],[1,0]]`.

The atom `a` is represented by

`lambda=(1,0)`.

Its local residual is

`Hhat_a lambda=(0,1)`.

### Chart b

Choose prefix `T_b={3}` and remaining order `R_b=(1,2)`.

Then

`d_b=1`,

`C_b=(1,-2)`,

`Hhat_b=[[0,1],[1,-3]]`.

The atom `b` is represented by

`mu=(1,0)`.

If one **incorrectly** treats `mu` as though it were a vector in chart `a`, then

`(Hhat_a lambda)^T mu=(0,1).(1,0)=0`,

which would create a false compatibility edge.

The correct transition is

`P_{a<-b}=E_{(2,3)}^T M_b`

`=[[0,1],[1,-2]]`.

Thus

`P_{a<-b}mu=(0,1)`,

and the correct cross numerator is

`(Hhat_a lambda)^T P_{a<-b}mu`

`=(0,1).(0,1)=1`,

exactly equal to `a^T K b`.

This is an exact rational regression proving that local reduced coordinate positions cannot be compared across non-nested charts without an explicit transition packet.

---

## 10. A second structural warning: transition matrices are not global coordinate changes

The map

`P_{a<-b}=E_{R_a}^T M_b`

only extracts the part of a chart-`b` numerator visible to chart-`a` residuals. It generally loses the coordinates in `T_a` and therefore need not be invertible, square, nonnegative entrywise, or satisfy a naive cocycle identity through a third chart.

Accordingly, a producer must not treat heterogeneous PD-prefix charts as ordinary bases of the same reduced vector space.

What **is** canonical is the full numerator map `M_T`, together with the identities

`K M_T=E_R Hhat`

and

`Hhat_aP_{a<-b}=P_{b<-a}^T Hhat_b`.

The cross-chart pair consumer should be built from these identities rather than from an invented reduced-coordinate equivalence.

---

## 11. Optional normalized-ray de-duplication

If two packets are normalized to represent the same physical zero vector, rather than merely the same ray, then

`M_a lambda/d_a = M_b mu/d_b`

is equivalent to the division-free equality

**`d_b M_a lambda = d_a M_b mu`.**

This gives a cheap exact duplicate check across charts.

If packets are only ray-normalized independently, one must first account for the chosen positive normalization; raw numerator equality is not expected.

T-P5-217's minimal-support uniqueness can often de-duplicate by support before this arithmetic check, but the cross-multiplied identity is useful when two producers use different normalization conventions.

---

## 12. Recommended global dispatcher

For a complete T-P5-217 atom-search transcript:

1. let each branch retain whichever legal PD-prefix chart emitted its atom;
2. store `(d_i,M_i,Hhat_i,lambda_i)` rather than forcing all atoms into one artificial common Schur chart;
3. for a pair `(i,j)`, form `P_{i<-j}=E_{R_i}^TM_j` or directly `Khat_ij=M_i^T K M_j`;
4. for genuine zeros, test compatibility with the nonnegative residual dot product `(Hhat_i lambda_i)^T(P_{i<-j}lambda_j)`;
5. use the exact reciprocity identity as a consistency check when both orientations are available;
6. for a fixed endpoint/debit form `Q`, cache `Qhat_ij=M_i^T Q M_j` only for compatible pairs that survive the graph filter;
7. use sign-only self/cross debit tests directly, but use the denominator-cleared formula of Section 7 for any quantitative pair combination;
8. reconstruct an actual rational full-state witness only after a pair/ray is selected for export.

This removes the hidden assumption in a same-chart implementation that all atoms came from one PD-prefix branch.

---

## 13. Minimal Lean theorem leaves

Recommended source-independent leaves:

- `pdChart_residualNumerator`
  - `K * M_T = E_R * Hhat`.
- `pdChart_crossEnergy_fractionFree`
  - `d_a*d_b*<x_a,K x_b> = <lambda,Khat_ab mu>`.
- `pdChart_crossTransition_reciprocity`
  - `Hhat_a*P_ab = P_ba^T*Hhat_b`.
- `copositiveZeros_crossChartPair_nonneg`
  - genuine zero packets imply the cross numerator is nonnegative.
- `copositiveZeros_crossChartCompatible_iff_mask`
  - compatibility iff the transitioned numerator support avoids the positive residual mask.
- `pdChart_crossDebit_fractionFree`
  - the analogous identity for arbitrary symmetric `Q`.
- `pdChart_pairQuadratic_commonDenominator`
  - Section 7's denominator-cleared expansion.
- `pdChart_crossPair_projectiveInvariant`
  - positive independent chart rescalings preserve zero/sign semantics.
- `pdChart_normalizedDuplicate_iff_crossMultiply`
  - normalized physical equality iff `d_b M_a lambda=d_a M_b mu`.

The first implementation needs only finite matrices, coordinate embeddings, transpose, determinant/adjugate identities, and ordered-field positivity. No square root, eigenvector, pseudoinverse, or floating normalization is required.

---

## 14. Failure / non-FAIL boundaries

1. **One prefix is not PD.** Its T-P5-218 fraction-free chart is unavailable. Route that atom through the singular-support/kernel machinery rather than inventing `M_T` with a pseudoinverse.
2. **A reduced vector is not reconstruction-feasible.** The algebraic bilinear identities remain valid, but nonnegative residual-mask semantics do not follow.
3. **The two packets do not share the same full `K`.** Cross-chart reciprocity is not expected. This is a source/key mismatch, not a theorem counterexample.
4. **Face-dependent endpoint lift.** One fixed `Q` must represent the same full physical bilinear form on both packets. Different face lifts require an independently proved cross-face transport before forming `Qhat_ab`.
5. **Raw reduced-coordinate comparison.** Unsound across non-nested charts; Section 9 gives an exact false-edge regression.
6. **Raw fraction-free magnitude comparison.** Unsound across chart depth/projective scaling; only sign/zero or denominator-homogeneous formulas are invariant.
7. **Incomplete atom packet.** A found compatibility/debit witness is valid, but absence of all witnesses is not certified until the T-P5-217 transcript is complete.
8. **Floating zero masks.** Compatibility is an exact zero statement. Float64 tolerance is not a replacement for rational/interval reification.

---

## 15. Boundaries left open

- actual same-key P5 `K,Q` and heterogeneous chart packets from the source producer;
- whether the deployed producer actually emits atoms from multiple non-nested PD-prefix branches;
- physical selector/cell/tube identity and trajectory coverage;
- exact interval/Float64 reification of zero masks and determinant gates;
- computational policy for caching `P_ab` versus direct `Khat_ab`;
- Lean/kernel compilation and axiom audit;
- 封不觉 independent validation;
- admission, registry mutation, and P5/P8/M4 parent propagation.

The mathematical child closes the heterogeneous-chart seam itself: **different PD-prefix branches can share one exact compatibility/debit graph without rational division and without forcing a common Schur chart, provided pair edges are transported through the full reconstruction numerators or their exact transition matrices.**