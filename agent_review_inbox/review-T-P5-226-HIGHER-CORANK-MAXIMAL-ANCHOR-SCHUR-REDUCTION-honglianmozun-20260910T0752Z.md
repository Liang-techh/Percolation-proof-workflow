---
kind: review_result
review_id: review-T-P5-226-higher-corank-maximal-anchor-schur-reduction-honglianmozun-20260910T0752Z
task_id: T-P5-226-HIGHER-CORANK-MAXIMAL-ANCHOR-SCHUR-REDUCTION
reviewer: 红莲魔尊
agent: 红莲魔尊
source_agent: 红莲魔尊
created_at: 2026-09-10T07:52:00Z
claim_commit: 9e15f1684f74814f541a4abbd9c52b2eec6316a0
inspected_commit: 5e03cdb0fe28ebcf572d2d8f44446cf651f9e3cb
upstream_commits:
  - 53af0acf2a6a9f7146f0847d7ff860560cb035ae  # T-P5-224 signed-lineality Schur dispatcher
  - 3ea6316491536353fd7908122a0926e494906e13  # T-P5-225 corank-one adjugate reduction
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_rank_r_maximal_principal_anchor_kernel_basis; add_bordered_minor_range_gate; add_fraction_free_rank_r_schur_reduction; add_anchor_independence_checksum; add_constructive_kernel_cross_and_positive_debit_witnesses; add_rank_zero_base_case
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact finite-dimensional PSD linear algebra, Schur rank identity, adjugate identities, rational regressions; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-226 — higher-corank maximal-principal-anchor Schur reduction

## 0. Verdict and seam closed

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-224 reduces a physical endpoint clique with signed lineality coordinate `c` and pointed coordinate `a>=0` to

`q(c,a)=c^T A c + 2 c^T B a + a^T C0 a`.

In the negative-semidefinite lineality branch, set

`P := -A >= 0`.

T-P5-225 closed the singular corank-one case using `adj(P)`. Its own fail-closed boundary notes that when `corank(P)>=2`, `adj(P)=0`, so the single-adjugate range test cannot see kernel-cross obstructions.

This child closes that higher-corank algebraic seam for **arbitrary rational PSD rank `r`** without pseudoinverses or floating nullspaces. The key replacement is a maximal positive principal anchor.

Let `P=P^T>=0` be `ell x ell` of rank `r`, with `1<=r<ell`. Choose an index set `I` of size `r` such that

`P0 := P[I,I] > 0`,

and let `J=I^c`. Put

`delta := det(P0) > 0`,

`H := adj(P0)`.

Then:

1. the Schur remainder of `P` relative to `P0` is exactly zero;
2. a fraction-free matrix `Z` built from `H` is a complete basis of `ker(P)`;
3. `range(B) subset range(P)` is equivalent to one exact bordered-minor residual matrix `R` vanishing;
4. if `R!=0`, one nonzero entry gives an explicit signed-lineality direction along which `q` is unbounded above;
5. if `R=0`, a fraction-free scaled solve `P Ytilde = delta B` exists;
6. the T-P5-224 reduced orthant matrix satisfies

   `Dhat = delta C0 + B_I^T H B_I = delta D`,

   where `D=C0+Y^T P Y` and `Y=Ytilde/delta`;
7. hence positive endpoint debit exists iff `Dhat` has a positive quadratic value on the nonnegative orthant;
8. different maximal positive principal anchors give the same normalized reduced matrix, with an exact cross-multiplied checksum.

Thus the entire PSD signed-lineality dispatcher is now fraction-free not only for corank one but for every rank `r>0`. The only exceptional PSD base case is `P=0`, handled separately in Section 9.

No actual P5 same-key endpoint packet, selector/cell/tube coverage, trajectory semantics, Float64/interval transport, Lean/kernel receipt, independent validation, admission, registry mutation, or parent closure is claimed.

---

## 1. Setup

Write the endpoint debit in the T-P5-224 NSD branch as

`q(c,a) = - c^T P c + 2 c^T B a + a^T C0 a`,

with

- `P=P^T>=0`, size `ell x ell`;
- `B`, size `ell x m`;
- `C0=C0^T`, size `m x m`;
- `c in R^ell` free signed lineality coordinates;
- `a in R_+^m` pointed coordinates.

Assume

`rank(P)=r`, `1<=r<ell`.

Because `P` is PSD of rank `r`, there exists a principal `r x r` submatrix that is positive definite. Fix one such index set `I`, let `J=I^c`, and partition

`P = [[P0, P01], [P10, P11]]`,

`B = [B0; B1]`,

where `P0=P[I,I]>0` and `B0=B[I,:]`.

Define

`delta = det(P0)>0`,

`H=adj(P0)`.

Then

`P0 H = H P0 = delta I_r`.

All matrices remain rational when the source packet is rational.

---

## 2. T226-A — maximal PSD anchor forces zero Schur remainder

### Theorem A1

Under the setup above,

`P11 = P10 P0^{-1} P01`.

Equivalently, fraction-free,

`delta P11 = P10 H P01`.

### Proof

Because `P0` is invertible, the standard block elimination identity gives

`rank(P) = rank(P0) + rank(P11 - P10 P0^{-1} P01)`.

The left side and `rank(P0)` are both `r`, hence the Schur remainder has rank zero and therefore vanishes.

Multiplying by `delta` and using `P0^{-1}=H/delta` gives the fraction-free identity. QED.

### Why PSD matters

For a general rank-`r` symmetric matrix an invertible principal `r`-anchor may have determinant of either sign. Here PSD guarantees `P0>0` and hence `delta>0`, which is later essential for sign transport from `Dhat` to `D`.

---

## 3. T226-B — a fraction-free complete kernel basis

Define the `ell x (ell-r)` matrix `Z` by blocks

`Z_I = - H P01`,

`Z_J = delta I_(ell-r)`.

That is, for each outside coordinate `j in J`, the corresponding kernel candidate is

`z_j = (-H p_{I j}, delta e_j)`.

### Theorem B1

`P Z = 0`.

Moreover `Z` has full column rank `ell-r`, hence

`range(Z)=ker(P)`.

### Proof

For the anchor rows,

`P0 Z_I + P01 Z_J`
`= -P0 H P01 + delta P01`
`= -delta P01 + delta P01 = 0`.

For the outside rows,

`P10 Z_I + P11 Z_J`
`= -P10 H P01 + delta P11 = 0`

by Theorem A1.

Thus `PZ=0`. The `J` block of `Z` is `delta I`, so the columns are linearly independent. Their number is `ell-r=dim ker(P)`, hence they span the whole kernel. QED.

### Structural meaning

T-P5-225 used one adjugate column to expose the unique kernel line. Here the maximal principal anchor produces **all higher-corank kernel directions at once**, still without a nullspace solve.

---

## 4. T226-C — exact range compatibility is a bordered-minor residual

Define the fraction-free residual matrix

`R := delta B1 - P10 H B0`.

### Theorem C1 — exact range gate

The following are equivalent:

1. `range(B) subset range(P)`;
2. `Z^T B = 0`;
3. `R = 0`.

### Proof

Since `P` is symmetric,

`range(P)=ker(P)^perp`.

By Theorem B1, `range(Z)=ker(P)`. Hence `range(B) subset range(P)` iff every kernel basis vector is orthogonal to every column of `B`, i.e. iff `Z^T B=0`.

Now

`Z^T B`
`= (-H P01)^T B0 + delta B1`
`= -P10 H B0 + delta B1`
`= R`,

because `P0` and `H=adj(P0)` are symmetric. QED.

### Theorem C2 — bordered determinant form

For each `j in J` and pointed column `k`,

`R[j,k]`
`= det([[P0, B0[:,k]], [P[j,I], B[j,k]]])`.

### Proof

This is the one-row/one-column bordered determinant identity

`det([[M,u],[v^T,b]]) = det(M)b - v^T adj(M)u`.

Take `M=P0`. QED.

### Checker consequence

Higher-corank range compatibility can therefore be certified by vanishing of a finite family of exact `(r+1)x(r+1)` bordered minors. No pseudoinverse, SVD, tolerance, or symbolic nullspace normalization is required.

---

## 5. T226-D — failed range gate gives a constructive unbounded endpoint witness

Suppose `R[j,k] != 0`. Let `z_j` be the corresponding column of `Z`, and choose the pointed ray

`a=e_k`.

Because `P z_j=0`, along the signed lineality direction `c=t z_j`,

`q(t z_j,e_k)`
`= 2 t z_j^T B e_k + (C0)_{kk}`
`= 2 t R[j,k] + (C0)_{kk}`.

Choosing the sign of `t` to agree with `R[j,k]` and letting `|t|->infinity` gives

`q(t z_j,e_k)->+infinity`.

### Theorem D1

If `R!=0`, the T-P5-224 endpoint debit has an explicit positive witness and in fact is unbounded above in the signed lineality variable.

This is stronger than a failed reduction precondition. It is a mathematical obstruction to any global nonpositive endpoint-debit claim on that physical clique.

---

## 6. T226-E — compatible branch gives a fraction-free scaled solve

Assume now

`R=0`.

Define `Ytilde` of size `ell x m` by

`Ytilde_I = H B0`,

`Ytilde_J = 0`.

### Theorem E1

`P Ytilde = delta B`.

Hence

`Y := Ytilde/delta`

satisfies

`P Y = B`.

### Proof

On the anchor rows,

`P0 H B0 = delta B0`.

On the outside rows,

`P10 H B0 = delta B1`

is exactly `R=0`. QED.

This is the arbitrary-corank replacement for T-P5-225's corank-one scaled principal solve.

---

## 7. T226-F — fraction-free reduced Lyapunov/debit matrix

The T-P5-224 square completion in the compatible branch is

`q(c,a)`
`= -(c-Ya)^T P (c-Ya) + a^T D a`,

where

`D := C0 + Y^T P Y`.

Define the fraction-free matrix

`Dhat := delta C0 + B0^T H B0`.

### Theorem F1

`Dhat = delta D`.

### Proof

Because `P Ytilde = delta B`,

`Ytilde^T P Ytilde = delta Ytilde^T B`.

Since `Ytilde_J=0`,

`Ytilde^T B = B0^T H B0`.

Therefore

`Y^T P Y`
`= (1/delta^2) Ytilde^T P Ytilde`
`= (1/delta) B0^T H B0`.

So

`delta D = delta C0 + B0^T H B0 = Dhat`. QED.

Because `delta>0`, `D` and `Dhat` have exactly the same quadratic sign on every pointed vector.

---

## 8. T226-G — exact positive endpoint-debit equivalence and witness lift

### Theorem G1

Under `R=0`, the following are equivalent:

1. there exist `c in R^ell`, `a>=0` with `q(c,a)>0`;
2. there exists `a>=0` with `a^T D a>0`;
3. there exists `a>=0` with `a^T Dhat a>0`.

### Proof

The completed square gives

`q(c,a) <= a^T D a`

for every `c,a`, with equality at `c=Ya` (and also at `c=Ya+z` for any `z in ker(P)`). Thus 1 iff 2.

Theorem F1 and `delta>0` give 2 iff 3. QED.

### Constructive fraction-free lift

If `a0>=0` and

`a0^T Dhat a0>0`,

set

`a_star = delta a0`,

`c_star = Ytilde a0`.

Then `c_star=Y a_star`, so the negative square vanishes and

`q(c_star,a_star)`
`= a_star^T D a_star`
`= delta (a0^T Dhat a0)`
`>0`.

Thus an orthant witness returned by the existing copositivity stack can be lifted to a full signed-lineality endpoint witness using only multiplication and adjugates.

### No-witness form

There is no positive endpoint-debit witness iff

`a^T Dhat a <= 0` for all `a>=0`,

i.e. iff `-Dhat` is copositive. Hence the existing exact orthant checker remains the terminal consumer.

---

## 9. T226-H — rank-zero PSD base case

The maximal-principal-anchor construction assumes `r>=1`. The remaining PSD case is exact and simpler.

If

`P=0`,

then

`q(c,a)=2c^TBa+a^TC0a`.

### Theorem H1

- If `B!=0`, choose a nonzero entry `B[j,k]`; with `a=e_k`, `c=t e_j`, the debit is unbounded above as `t` takes the matching sign.
- If `B=0`, the signed lineality variable disappears and the endpoint problem reduces exactly to the orthant form `a^TC0a`.

So the full PSD dispatcher covers every rank without pseudoinverses:

- `rank(P)=0`: direct zero-block rule;
- `rank(P)>=1`: maximal positive principal anchor rule;
- corank one is recovered as the special case `|J|=1` treated by T-P5-225.

---

## 10. T226-I — anchor independence and exact checksum

Suppose `I` and `K` are two size-`r` principal anchors with

`delta_I=det(P[I,I])>0`,

`delta_K=det(P[K,K])>0`.

Assume the range gate passes. Build `Dhat_I` and `Dhat_K` by the construction above.

### Theorem I1

`Dhat_I/delta_I = Dhat_K/delta_K = D`,

where

`D=C0+Y^TPY`

for any solution `PY=B`.

Equivalently, division-free,

`delta_K Dhat_I = delta_I Dhat_K`.

### Proof

Every anchor construction produces a solution of `PY=B`. If `Y1,Y2` are two such solutions, then `P(Y1-Y2)=0`, so

`Y1^T P Y1 = Y2^T P Y2`.

Indeed writing `Y1=Y2+N` with `PN=0`, all mixed and pure `N` terms vanish. Therefore the normalized reduced matrix is canonical. The cross-multiplied checksum follows from Theorem F1 for each anchor. QED.

### Engineering value

If several maximal principal anchors are available, the cross-multiplication equality is a cheap exact internal consistency check. It does not prove source provenance, but it can catch anchor/index permutation mistakes before downstream copositivity work.

---

## 11. Exact rational regressions

### R1 — genuine corank-two compatible branch

Take

`P = [[1,0,1,2],`
`     [0,1,1,-1],`
`     [1,1,2,1],`
`     [2,-1,1,5]]`.

This is the Gram matrix of the four vectors

`(1,0), (0,1), (1,1), (2,-1)`,

so `P>=0` and `rank(P)=2`; hence the corank is two and `adj(P)=0`.

Choose anchor `I={1,2}`. Then

`P0=I_2`, `delta=1`, `H=I_2`.

Let

`B=(1,2,3,0)^T`, `C0=-4`.

The outside compatibility equations are

`B3=B1+B2=3`,

`B4=2B1-B2=0`,

so `R=0`.

The reduced fraction-free scalar is

`Dhat = -4 + (1^2+2^2) = 1 > 0`.

The explicit lifted witness is

`a_star=1`,

`c_star=(1,2,0,0)^T`,

and direct evaluation gives

`q(c_star,1)=1>0`.

Thus the higher-corank branch finds a real endpoint witness even though the ordinary full adjugate is identically zero.

### R2 — same packet, different maximal anchor

For the same `P,B,C0`, choose anchor `K={2,4}`. Then

`P[K,K]=[[1,-1],[-1,5]]`,

`delta_K=4`.

Its adjugate is

`[[5,1],[1,1]]`,

and `B_K=(2,0)^T`, so

`B_K^T adj(P[K,K]) B_K = 20`.

Therefore

`Dhat_K = 4*(-4)+20 = 4`.

The first anchor gave `delta_I=1`, `Dhat_I=1`; hence

`delta_K Dhat_I = 4 = delta_I Dhat_K`.

This exactly exercises the anchor-independence checksum with unequal determinant scales.

### R3 — compatibility gate cannot be skipped

Keep the same rank-two `P`, but take

`B_bad=e3`, `C0=0`.

With anchor `I={1,2}`, `B0=0` while the first outside row equals one, so

`R=(1,0)^T != 0`.

The corresponding kernel basis vector is

`z3=(-1,-1,1,0)^T`,

and indeed `P z3=0`, `z3^T B_bad=1`.

Hence

`q(t z3,1)=2t -> +infinity`.

A naive principal solve that ignores `R` would see `B0=0` and produce the spurious reduced scalar `Dhat=0`. This is a false no-witness result. Therefore the bordered-minor/range gate is mandatory before Schur reduction.

### R4 — rank-zero base case

Take `P=0`, `B=e1`, `C0=0`. Then

`q(t e1,1)=2t`,

so the debit is unbounded above. If instead `B=0`, the lineality coordinate is exactly irrelevant and only `C0` remains.

---

## 12. Candidate theorem statements for formalization

Suggested exact-real Lean decomposition:

1. `psd_rank_exists_positive_principal_anchor`
   - symmetric PSD `P`, rank `r`;
   - produce an index set `I` of cardinality `r` with principal block positive definite.

2. `maximal_principal_anchor_zero_schur_remainder`
   - `P>=0`, `rank P=r`, `P_II>0`;
   - prove `delta * P_JJ = P_JI * adj(P_II) * P_IJ`.

3. `fractionFree_kernel_basis_of_maximal_principal_anchor`
   - define `Z_I=-adj(P_II)P_IJ`, `Z_J=delta I`;
   - prove `PZ=0` and `range Z=ker P`.

4. `range_subset_iff_maximal_anchor_residual_zero`
   - prove `range(B) subset range(P)` iff `delta B_J-P_JI adj(P_II)B_I=0`.

5. `bordered_minor_eq_maximal_anchor_residual_entry`
   - identify each residual entry with an `(r+1)x(r+1)` bordered determinant.

6. `kernel_cross_unbounded_of_anchor_residual_ne_zero`
   - from one nonzero residual entry, construct `z,a` and prove unbounded positive endpoint debit.

7. `rankR_fractionFree_scaled_solve`
   - under residual zero, prove `P Ytilde=delta B` for `Ytilde_I=adj(P_II)B_I`, `Ytilde_J=0`.

8. `rankR_fractionFree_schur_identity`
   - prove `Dhat=delta*C0+B_I^T adj(P_II)B_I=delta*D`.

9. `rankR_signedOrthant_positive_iff_fractionFree_positive`
   - endpoint positive witness iff `exists a>=0, a^T Dhat a>0`.

10. `rankR_fractionFree_witness_lift`
    - lift `a0` to `(Ytilde a0, delta a0)`.

11. `rankR_anchor_crossmultiply_invariant`
    - for two positive maximal anchors, prove `delta_K Dhat_I=delta_I Dhat_K`.

12. `rankZero_signedLineality_dispatcher`
    - exact `P=0` branch separating `B!=0` unboundedness from `B=0` orthant reduction.

Formalization may initially take the maximal positive principal anchor as an explicit premise; the endpoint consumer itself does not need a theorem that algorithmically finds the anchor.

---

## 13. Fail-closed boundary

This child does **not** establish:

- that any actual P5 signed-lineality block is PSD or has a particular rank;
- that a selected principal anchor belongs to the same source/key/cell/face packet as the physical endpoint debit;
- completeness of actual endpoint cliques or face-lift/gauge packets;
- the final copositivity sign of any actual `-Dhat`;
- Float64/interval/rational-reconstruction semantics;
- PDE/ODE/Newton-Euler trajectory coverage or Lyapunov decay along deployed dynamics;
- Lean/kernel compilation or axiom audit;
- independent validation by 封不觉;
- admission, registry mutation, or parent closure.

If `P` is not PSD, the positive determinant/sign arguments here are invalid and the dispatcher must return to T-P5-224's generic signed-block branch. If the claimed anchor has size smaller than `rank(P)`, its Schur remainder need not vanish and the construction is invalid. If the range residual is not proved zero, Schur reduction is forbidden because the true endpoint debit is unbounded in a kernel-cross direction.

---

## 14. Structural fingerprint and next mathematical seam

The new structural fingerprint is

**PSD signed lineality -> maximal PD principal anchor -> zero Schur remainder -> fraction-free kernel basis -> bordered-minor range gate -> constructive kernel-cross obstruction OR scaled solve -> orthant reduced Lyapunov debit.**

This closes the algebraic higher-corank seam left by T-P5-225.

A non-overlapping next mathematics target is no longer another singular linear-algebra reduction. The more consequential remaining energy seam is to combine this signed-lineality dispatcher with the T-P5-222 face-lift quotient-radical gate **before** clique-wise T-P5-215 one-ray/pair debit pruning, and prove an exact commutation theorem: quotienting debit-radical face gauge and eliminating compatible signed physical lineality should yield the same reduced orthant debit independent of the order of the two reductions. A counterexample should be required when the gauge is only storage-zero but not debit-radical.
