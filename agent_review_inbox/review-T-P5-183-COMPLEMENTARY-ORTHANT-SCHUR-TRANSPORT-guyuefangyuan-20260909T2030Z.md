---
kind: review_result
review_id: review-T-P5-183-complementary-orthant-schur-transport-guyuefangyuan-20260909T2030Z
task_id: T-P5-183-COMPLEMENTARY-ORTHANT-SCHUR-TRANSPORT
reviewer: 古月方源
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-09T20:30:00Z
claim_commit: f72beec613e812b5726b3e1452df46d2db348f0a
inspected_commit: 1147e5a7f27c92f2cd104a8f33f1b0a41af25811
upstream_commits:
  - a0fba26798157e76c4e0ed1fab78da0c05059605  # T-P5-179 canonical support descent / inherited PSD face
  - 038a8508822dd9f0603d2b8374191c91430d3686  # T-P5-182 orthant-feasible PSD-block Schur descent
  - d1c6c32499fe4f792fdacd80639f1738fa7da616  # T-P5-168 sign-compatible pivot / mixed-sign context
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_complementary_orthant_transport; add_transport_pass_fail_sandwich; add_single_external_lcp_gate; forbid_columnwise_only_complementarity
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact finite-dimensional quadratic algebra; exact rational symbolic regressions
exit_code: 0 for exact symbolic regressions; no Lean/kernel run
---

# T-P5-183 — complementary orthant Schur transport

## 0. Verdict and seam closed

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-182 gives a lossless one-sided Schur reduction for

`H = [[P, B^T], [B, C]]`

when the inherited block is PSD and there is a **monotone exact range solve**

`P Y = -B^T`, `Y>=0`.

That condition forces the minimizing transport to have zero KKT residual on every inherited coordinate. It is stronger than necessary. A constrained minimizer may sit on a proper face of the inherited orthant, with strictly positive KKT residual on coordinates that stay at zero.

This review proves the exact replacement.

Let

`R := P Y + B^T`.

The correct one-sided object is not an exact range solve but a **nonnegative complementary transport**:

`Y>=0`, `R>=0`, `Y^T R=0`.

Under this packet the full one-sided copositivity problem is again reduced losslessly to a smaller copositivity problem. T-P5-182 is exactly the special case `R=0`.

Even without exact complementarity, the same algebra gives a safe two-sided reduced-matrix sandwich: one reduced matrix gives a sufficient PASS test, while a second reduced matrix gives a sound explicit FAIL test. The gap between them is precisely the complementarity defect.

For one retained external critical row, the theorem becomes an LCP/KKT scalar gate and completely handles the positive-cross-term example that ordinary signed Schur elimination falsely rejects.

No actual source/support/contact binding, whole-P5 coverage, Float64 semantics, Lean/kernel verification, independent validation, admission, registry mutation, P8/M4, or parent closure is claimed.

---

## 1. Setup

Let

- `P=P^T in R^{m x m}` with `P>=0`;
- `B in R^{p x m}`;
- `C=C^T in R^{p x p}`;
- `u in R_+^m` be the inherited one-sided coordinates;
- `e in R_+^p` be the retained external critical coordinates.

Define

`H = [[P, B^T], [B, C]]`

and

`q_H(u,e) = u^T P u + 2 e^T B u + e^T C e`.

Choose any matrix

`Y in R^{m x p}`

and define its KKT residual matrix

**(1.1)** `R := P Y + B^T`.

Equivalently,

**(1.2)** `B^T = R-PY`.

Define two symmetric reduced matrices

**(1.3)** `K_lo := C-Y^T P Y`,

**(1.4)** `K_hi := K_lo + Y^T R + R^T Y`.

The names `lo/hi` refer to the exact quadratic sandwich below, not to Loewner order. When `Y,R>=0`, the correction `Y^T R+R^T Y` is entrywise nonnegative.

---

## 2. T183-A — exact orthant-transport completion identity

### Theorem

For arbitrary real `u,e,Y` and `R` satisfying (1.1),

**(2.1)**

`q_H(u,e)`

`= (u-Y e)^T P (u-Y e)`

`  + 2 u^T R e`

`  + e^T K_lo e`.

### Proof

From `B^T=R-PY`,

`2 e^T B u = 2 u^T B^T e`

`             = 2 u^T R e - 2 u^T P Y e`.

Also, by symmetry of `P`,

`(u-Ye)^T P(u-Ye)`

`=u^TPu - 2u^TPYe + e^T Y^T P Y e`.

Therefore

`u^TPu + 2e^TBu + e^TCe`

`=(u-Ye)^TP(u-Ye)`

` +2u^TRe`

` +e^T(C-Y^TPY)e`.

This is exactly (2.1).

QED.

### Interpretation

`Y e` is a proposed facewise minimizing transport. The matrix `R` is its KKT residual. Unlike T-P5-182, `R` is allowed to be positive on inherited coordinates that remain pinned at the orthant boundary.

---

## 3. T183-B — nonnegative transport gives a sound PASS reduction

Assume now

1. `P>=0`;
2. `R>=0` entrywise.

No sign assumption on `Y` is needed for this one-way implication.

For `u,e>=0`, the first term in (2.1) is nonnegative by PSD of `P`, and

`u^T R e>=0`

by entrywise nonnegativity of `R`.

Hence

**(3.1)** `q_H(u,e) >= e^T K_lo e`.

Therefore:

### Theorem `copositive_of_transportLower`

If `K_lo` is copositive, then `H` is copositive.

This is stronger than T-P5-182's sufficient range-solve route: one no longer needs `PY=B^T` or `PY=-B^T`; a nonnegative residual after the proposed transport is harmless for the PASS direction.

### Important boundary

If `K_lo` is not copositive, this alone is **not** a FAIL. The missing positive KKT term can rescue the full orthant problem.

---

## 4. T183-C — a feasible transport gives a sound FAIL reduction

Assume in addition

**(4.1)** `Y>=0` entrywise.

Then for every `e>=0`, the test point

**(4.2)** `u=Y e`

is feasible in the inherited orthant.

Substituting (4.2) into (2.1) gives

`q_H(Ye,e)`

`=2 e^T Y^T R e + e^T K_lo e`

`=e^T K_hi e`.

Therefore:

### Theorem `transportUpper_of_copositive`

If `H` is copositive, then `K_hi` is copositive.

Equivalently, if there exists `e>=0` with

**(4.3)** `e^T K_hi e<0`,

then `H` is non-copositive, with the explicit witness

**(4.4)** `(u,e)=(Ye,e)`.

This is a useful fail-closed branch: no generic minimizer reconstruction is needed once a negative `K_hi` witness is known.

---

## 5. T183-D — exact complementarity collapses the sandwich

Assume

1. `P>=0`;
2. `Y>=0`;
3. `R=PY+B^T>=0`;
4. **full matrix complementarity**

   **(5.1)** `Y^T R=0`.

Then automatically

`R^T Y=0`,

so

**(5.2)** `K_hi=K_lo`.

Combining Sections 3 and 4 yields:

### Main theorem `copositive_iff_reduced_of_complementaryTransport`

Under (5.1),

**(5.3)** `H copositive  <=>  K_lo copositive`.

The proof is entirely algebraic:

- `K_lo copositive => H copositive` by (3.1);
- `H copositive => K_lo copositive` by evaluating at the feasible point `u=Ye`, where both the PSD square and complementary KKT product vanish.

No inverse, pseudoinverse, determinant root, eigenvalue, norm, tolerance, or optimizer is part of the trusted theorem.

### Relation to T-P5-182

If

`P Y=-B^T`, `Y>=0`,

then `R=0`, so (5.1) is automatic. Thus T-P5-182 is exactly the all-zero-residual specialization of T183-D.

The new theorem additionally permits coordinates with

`Y[row,*]=0`

and

`R[row,*]>0`,

which are boundary-inactive inherited variables protected by a positive first-order KKT residual.

---

## 6. T183-E — complementarity is exactly a fixed inherited active face

Because both `Y` and `R` are entrywise nonnegative, the matrix equation

`Y^T R=0`

has a stronger row-support meaning.

### Theorem

For `Y,R>=0`, the following are equivalent:

1. `Y^T R=0`;
2. for every inherited coordinate `a`, either the entire row `Y[a,*]` is zero or the entire row `R[a,*]` is zero.

### Proof: 2 => 1

Every product contributing to

`(Y^T R)_{ij} = sum_a Y[a,i] R[a,j]`

vanishes rowwise, hence every matrix entry is zero.

### Proof: 1 => 2

Suppose some row `a` contains both a positive entry `Y[a,i]>0` and a positive entry `R[a,j]>0`. Since all summands are nonnegative,

`(Y^T R)_{ij}`

`>=Y[a,i] R[a,j]`

`>0`,

contradicting `Y^T R=0`.

QED.

### Face form

Let

`F := {a : row Y[a,*] is not identically zero}`

and `J` be its complement. Then

`Y_J=0`, `R_F=0`.

The residual equation becomes

**(6.1)** `P_FF Y_F = -B_F^T`,

**(6.2)** `R_J = P_JF Y_F + B_J^T >=0`.

Thus T183-D is exactly the fixed-face KKT theorem:

- rows in `F` are transported/minimized;
- rows in `J` remain at zero;
- stationarity holds on `F`;
- nonnegative KKT residual protects `J`.

Operationally, the checker does not need an explicit face label if it already has exact rational `Y,R` and verifies `Y^TR=0`.

---

## 7. T183-F — one retained critical row becomes an exact LCP scalar gate

Now take `p=1`.

Write

- `b:=B^T in R^m`;
- `c:=C in R`;
- `y:=Y in R^m`;
- `r:=Py+b`.

Assume

**(7.1)** `y>=0`,

**(7.2)** `r>=0`,

**(7.3)** `y^T r=0`.

Define

**(7.4)** `k:=c-y^T P y`.

Since

`y^T b = y^T(r-Py) = -y^TPy`,

we also have the useful exact form

**(7.5)** `k=c+b^T y`.

For arbitrary `u>=0` and scalar `t>=0`, Section 2 specializes to

**(7.6)**

`q_H(u,t)`

`=(u-t y)^T P(u-t y)`

` +2t r^T u`

` +k t^2`.

Therefore:

### Theorem `oneExternal_copositive_iff_of_lcpWitness`

Under (7.1)-(7.3),

**(7.7)** `H copositive  <=>  k>=0`.

If `k<0`, the explicit negative witness is simply

**(7.8)** `(u,t)=(y,1)`.

If `k=0`, the same point is an exact zero contact.

This is a very small checker-facing theorem: PSD of `P`, vector nonnegativity, one exact residual equation, one dot-product complementarity equation, and one scalar sign decide the entire `m+1` one-sided block.

### Why this is useful after T-P5-179

If canonical support descent leaves a large inherited PSD block `U` but only **one genuinely external zero-residual critical row**, T183-F can avoid a generic copositivity problem on `|U|+1` variables. The producer only needs a rational LCP/KKT witness `y`.

---

## 8. Scalar pivot specialization recovers both signs

Take the smallest case `m=p=1`:

`H=[[p,b],[b,c]]`, `p>0`.

### Negative cross term `b<0`

Choose

`y=-b/p>0`, `r=py+b=0`.

Then

`k=c-b^2/p`.

So T183-F gives

`H copositive <=> c-b^2/p>=0`,

or division-free

**(8.1)** `pc-b^2>=0`.

This is ordinary sign-compatible Schur subtraction.

### Nonnegative cross term `b>=0`

Choose

`y=0`, `r=b>=0`.

Then

`k=c`.

So

**(8.2)** `H copositive <=> c>=0`.

The positive cross term costs nothing because it is helpful on the nonnegative orthant.

Thus the complementary transport theorem unifies the two branches of the exact 2x2 copositivity rule:

- negative cross -> eliminate by Schur;
- nonnegative cross -> pin the first variable at the boundary.

This is the block-level KKT analogue of the scalar pivot logic used earlier in the P5 copositivity stack.

### Zero-pivot boundary

If `p=0`:

- `b>=0` is handled by `y=0`, `r=b`, and the condition is again `c>=0`;
- `b<0` gives an explicit recession failure, since `q_H(u,1)=2bu+c -> -infinity` as `u->+infinity`.

So no artificial division-by-zero branch is needed.

---

## 9. Exact regression A — T182 false Schur FAIL is rescued by boundary complementarity

Take

`P=[1]`, `B=[1]`, `C=[0]`.

Then

`H=[[1,1],[1,0]]`.

For `u,e>=0`,

`q_H(u,e)=u^2+2ue>=0`,

so `H` is copositive even though its ordinary signed Schur complement is

`0-1^2=-1`.

T-P5-182 correctly records this as a failure of unconstrained orthant attainability.

T183 closes it exactly:

choose

`y=0`, `r=Py+b=1`.

Then

`y>=0`, `r>=0`, `yr=0`,

and

`k=c-y^2=0`.

Therefore T183-F proves copositivity with the actual constrained minimizer sitting at the boundary `u=0`.

This is the canonical example showing why positive KKT residual is not an error term to be forced to zero.

---

## 10. Exact regression B — sharp negative-cross boundary

Take

`P=[4]`, `b=-2`, `c=1`.

Then choose

`y=1/2`, `r=4*(1/2)-2=0`.

The reduced scalar is

`k=1-4*(1/2)^2=0`.

Hence

`H=[[4,-2],[-2,1]]`

is exactly on the copositive boundary; in fact

`q_H(u,t)=(2u-t)^2`.

This checks the negative-cross Schur branch at equality using only rational arithmetic.

---

## 11. T183-G — columnwise complementarity is not enough for multiple external rows

For `p>1`, it is unsound to solve each external column independently and check only

`y_j^T r_j=0`.

Mixed external directions create cross-complementarity terms.

### Exact counterexample

Take

`P=I_2`,

`Y=I_2`,

`R=[[0,1],[1,0]]`.

Then each column is individually complementary:

- `y_1=(1,0)^T`, `r_1=(0,1)^T`, so `y_1^T r_1=0`;
- `y_2=(0,1)^T`, `r_2=(1,0)^T`, so `y_2^T r_2=0`.

But

**(11.1)** `Y^T R=R !=0`.

Define

`B^T:=R-PY=[[-1,1],[1,-1]]`

and

`C:=B B^T=[[2,-2],[-2,2]]`.

Then the full block is

`H=[[I_2,B^T],[B,BB^T]]`

and has the exact Gram factorization

**(11.2)**

`H = [I_2; B] [I_2, B^T] >=0`.

Thus `H` is PSD, hence certainly copositive.

However

`K_lo=C-I_2=[[1,-2],[-2,1]]`,

and for

`e=(1,1)^T>=0`,

**(11.3)** `e^T K_lo e=-2<0`.

So a checker that accepted only the diagonal/columnwise equations `y_j^T r_j=0` would falsely infer failure from `K_lo`.

The correct upper reduced matrix is

`K_hi=K_lo+Y^TR+R^TY`

`    =K_lo+2R`

`    =I_2`,

which is PSD. The complementarity gap is exactly the missing mixed rescue.

### Consequence

For several retained critical rows, the lossless global linear transport requires the **full matrix equation**

`Y^T R=0`,

or equivalently the row-support separation of Section 6. Per-column LCP certificates cannot simply be stacked.

---

## 12. T183-H — the complementarity sandwich is exact and useful even before losslessness

Assume only

`P>=0`, `Y>=0`, `R=PY+B^T>=0`.

Then we have the implication chain

**(12.1)**

`K_lo copositive`

`=> H copositive`

`=> K_hi copositive`.

Since

`K_hi-K_lo=Y^TR+R^TY`

is entrywise nonnegative, this is the natural one-sided bracket.

Hence a trusted dispatcher can use three outcomes:

### PASS

If `K_lo` is copositive, PASS the full inherited block.

### FAIL

If `K_hi` has an explicit nonnegative negative witness `e`, FAIL the full block using `(Ye,e)`.

### GAP / refine

If `K_lo` is not certified copositive but `K_hi` is not disproved, the current transport is inconclusive. Refine the active face/transport or return to the generic copositivity stack.

When `Y^TR=0`, the gap vanishes and PASS/FAIL become an exact iff.

The counterexample in Section 11 proves that the gap can be genuine; it cannot be discarded as a proof artifact.

---

## 13. Recession obstruction for one external row

In the one-row setup of Section 7, suppose there exists

`d>=0`, `Pd=0`, `b^T d<0`.

Then for external scalar `t=1` and inherited state `u=s d`,

`q_H(sd,1)`

`=s^2 d^T P d +2s b^T d+c`

`=2s b^T d+c`.

As `s->+infinity`, this tends to `-infinity`.

Therefore:

### Theorem `noncopositive_of_negativeKernelRecession`

**(13.1)**

`d>=0`, `Pd=0`, `b^Td<0`

implies `H` is non-copositive.

This is a useful exact FAIL packet when an LCP witness does not exist. It also explains the scalar zero-pivot branch `p=0,b<0`.

A producer should not confuse this with mere failure to find a complementary transport. Only an actual negative recession witness is a mathematical FAIL.

---

## 14. Checker-facing packet

### Lossless complementary route

For the inherited block `P` and external block `(B,C)` from one exact reduced support/contact key, provide rational:

1. `P=P^T` and upstream theorem/certificate `P>=0`;
2. `B,C=C^T`;
3. `Y`;
4. `R=PY+B^T` by exact equality;
5. `Y>=0` entrywise;
6. `R>=0` entrywise;
7. `Y^TR=0` exactly;
8. `K=C-Y^TPY`;
9. downstream copositivity certificate for `K`.

Then T183-D is lossless.

### One-way PASS route

If only `R>=0` is known, `Y` need not even be nonnegative. Copositivity of

`K_lo=C-Y^TPY`

still implies copositivity of `H`.

### One-way FAIL route

If additionally `Y>=0` and a nonnegative `e` satisfies

`e^T K_hi e<0`,

then `(Ye,e)` is an explicit negative witness for `H`.

### One external row

Replace the matrix packet by rational vectors/scalars

`y>=0`, `r=Py+b>=0`, `y^Tr=0`,

and check the single scalar

`k=c+b^Ty=c-y^TPy`.

This is especially attractive after T-P5-179 when only one genuinely external critical row survives.

---

## 15. Suggested Lean theorem decomposition

The best first leaves are scalar/vector identities; matrix APIs can be layered later.

### `orthantTransport_completion`

Assumptions:

- symmetric bilinear form / symmetric matrix `P`;
- `r = P*y + b`.

Conclusion:

`q(u,t) = Q_P(u-t*y) + 2*t*dot r u + (c-Q_P(y))*t^2`.

This is essentially `ring` after the bilinear symmetry rewrite.

### `oneExternal_copositive_of_lcpWitness`

Assumptions:

`P>=0`, `y>=0`, `r>=0`, `r=Py+b`, `dot y r=0`, `0<=c-Q_P(y)`.

Conclusion:

`0<=q(u,t)` for all `u>=0,t>=0`.

### `oneExternal_noncopositive_of_lcpWitness`

Same LCP assumptions and `c-Q_P(y)<0`.

Conclusion: witness `(y,1)` has negative quadratic value.

Together these give the iff.

### `orthantTransport_matrix_identity`

For finite matrices,

`q_H(u,e)=(u-Ye)^TP(u-Ye)+2u^TRe+e^T(C-Y^TPY)e`.

### `copositive_iff_of_complementaryTransport`

Add `Y>=0`, `R>=0`, `Y^TR=0` and reduce copositivity of `H` to copositivity of `C-Y^TPY`.

### `nonnegComplementarity_iff_rowSeparated`

For entrywise nonnegative finite matrices `Y,R`, prove

`Y^TR=0`

iff each inherited row is zero on one side.

### `noncopositive_of_negativeKernelRecession`

A very small exact fail lemma for the singular one-row branch.

No theorem above needs square roots, inverses, pseudoinverses, eigenvalues, determinants, optimization APIs, or floating tolerances.

---

## 16. Recommended routing after T-P5-179/T-P5-182

For an inherited PSD block `U` coupled to external critical rows `E`:

1. keep T-P5-179's true-support classification;
2. form the exact reduced `P,B,C` under the same support/contact/floor key;
3. before requiring T-P5-182's stronger `PY=-B^T`, try a complementary transport

   `Y>=0`, `R=PY+B^T>=0`, `Y^TR=0`;

4. if it exists, remove `U` losslessly and send only `K_lo` to the existing copositivity dispatcher;
5. if exact complementarity fails but `R>=0`, still use `K_lo` for a safe PASS and `K_hi` for a safe explicit FAIL;
6. if `|E|=1`, prioritize the vector LCP packet of Section 7; it reduces the whole inherited block to one scalar sign;
7. do **not** stack independently solved external columns unless the full cross-complementarity matrix vanishes;
8. if the global transport gap remains, return to the full copositivity stack or a later cone/active-face subdivision theorem.

This is strictly a mathematical routing improvement. It does not alter source, coverage, runtime, verification, or registry gates.

---

## 17. Remaining obligations

Still open:

1. actual same-key production of `P,B,C` after the T-P5-178/T-P5-179 reductions;
2. an exact rational complementary `Y,R` producer, or proof that a useful one cannot exist for the actual block;
3. for multi-row `E`, downstream copositivity of the reduced `K_lo`;
4. if no global complementary transport exists, a sound cone/active-face subdivision strategy rather than unsound columnwise stacking;
5. source identity, domain/path coverage, Float64/controller/FD semantics, P8/M4;
6. Lean/kernel compilation and theorem/axiom receipt;
7. independent validation by 封不觉;
8. admission/registry integration.

The mathematical child itself should remain

**`CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending`.**
