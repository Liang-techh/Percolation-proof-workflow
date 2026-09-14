---
kind: review_result
review_id: review-T-P5-227-quotient-lineality-schur-commutation-liuguanyi-20260910T0810Z
task_id: T-P5-227-QUOTIENT-LINEALITY-SCHUR-COMMUTATION
reviewer: 柳冠一
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-10T08:10:00Z
claim_commit: 2cd4ff524ae3a7432cc1fa46192e21e3e3878f61
inspected_commit: 606e7fba1e7223ceda93e9043b6bb1bb5ca9ab78
upstream_commits:
  - 467527fa4670608070e0d74e64e6b7087a8b3094  # T-P5-222 face-lift quotient debit descent
  - 53af0acf2a6a9f7146f0847d7ff860560cb035ae  # T-P5-224 signed-lineality Schur dispatcher
  - 3ea6316491536353fd7908122a0926e494906e13  # T-P5-225 corank-one adjugate branch
  - 6a10ef29433a4dd050d593d8053383f4ba7fd204  # T-P5-226 arbitrary-corank maximal-anchor branch
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_radical_gauge_gram_block_invariance; add_quotient_lineality_schur_commutation; add_gauge_augmented_signed_dispatcher_equivalence; add_fraction_free_anchor_commutation_corollary; add_nonradical_counterexample
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact finite-dimensional symmetric-bilinear and Schur algebra; exact rational regressions; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-227 — debit-radical face quotient commutes with signed-lineality Schur reduction

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-222 proves that face-lift gauge can be quotiented only when it is radical for the endpoint debit form on the consumed packet. T-P5-224 then discovers genuine *physical* lineality in that quotient cone and retains it as free signed coordinates. T-P5-225/226 eliminate those signed coordinates by a Schur argument, including singular PSD lineality blocks.

The remaining ambiguity was order: must one first quotient the face gauge and then build the signed-lineality Schur packet, or can one keep gauge coordinates in the ambient lifted packet and run the signed dispatcher first?

This review proves the two operations commute exactly under the T-P5-222 radical gate.

The key identity is simple but structurally important. If `G` spans face-gauge directions, `L` spans signed physical-lineality representatives, `R` spans pointed endpoint representatives, and `Q=Q^T` is the endpoint debit form, assume on the consumed span

`G^T Q G = 0`,

`G^T Q L = 0`,

`G^T Q R = 0`.

Then for every gauge coordinate `s`, signed lineality coordinate `c`, and pointed coordinate `a>=0`,

`q(Gs+Lc+Ra) = c^T A c + 2 c^T B a + a^T C a`,

with

`A=L^T Q L`, `B=L^T Q R`, `C=R^T Q R`.

Thus the gauge coordinates disappear *before any optimization or Schur step*. Quotient-first and Schur-first therefore see exactly the same three Gram blocks.

In the negative-semidefinite signed branch `A=-P`, `P>=0`, this implies the same positive-direction test, the same kernel/cross obstruction, the same range gate `range(B) subset range(P)`, and—when the range gate passes—the same reduced orthant matrix

`D = C + Y^T P Y`,  where `P Y = B`.

The result also survives the T-P5-226 arbitrary-corank fraction-free implementation: adding radical gauge coordinates merely appends zero rows/columns to `P` and zero rows to `B`; the maximal-anchor residual, scaled solve, and `Dhat` are unchanged.

Therefore the T-P5-215 one-ray / compatible-pair positive-debit decision is independent of whether the T-P5-222 quotient is performed before or after the T-P5-224/225/226 signed-lineality reduction.

A rational counterexample below shows that this fails if the gauge is only storage-zero—or even debit-isotropic `g^TQg=0`—without being debit-radical. In that case two representatives of the same quotient ray can produce different Schur-reduced debit.

No actual P5 same-key face packet, source/cell/tube binding, trajectory coverage, Float64/interval semantics, Lean/kernel receipt, independent validation, admission, registry mutation, or parent closure is claimed.

---

## 1. Setup

Let `Y=R^n` and let `Q=Q^T` be the symmetric endpoint/debit matrix.

Fix one already-established storage-zero compatibility clique. Within that clique let

- `G in R^{n x g}` span the admissible face-lift gauge subspace `N`;
- `L in R^{n x ell}` contain representatives of the genuine physical lineality basis in `Y/N`;
- `R in R^{n x m}` contain representatives of the remaining pointed endpoint generators.

Coordinates are

- `s in R^g`, free gauge coordinates;
- `c in R^ell`, free signed physical-lineality coordinates;
- `a in R_+^m`, pointed coordinates.

The ambient representative is

`x(s,c,a)=G s + L c + R a`.

The T-P5-222 restricted radical gate on this consumed span is

`G^T Q G=0`,

`G^T Q L=0`,

`G^T Q R=0`.

Because `Q` is symmetric, these identities also kill the transposed cross blocks.

Define

`A=L^T Q L`,

`B=L^T Q R`,

`C=R^T Q R`.

---

## 2. Theorem A — radical gauge deletes as a zero Gram block

### Statement

Under the setup above,

`x(s,c,a)^T Q x(s,c,a)`

is independent of `s`, and exactly

**`c^T A c + 2 c^T B a + a^T C a`.**

Equivalently the full Gram matrix in coordinates `(s,c,a)` is

`[[0, 0, 0],
  [0, A, B],
  [0, B^T, C]]`.

### Proof

Expand bilinearly:

`q = s^T G^TQG s + 2 s^T G^TQL c + 2 s^T G^TQR a`

`    + c^T L^TQL c + 2 c^T L^TQR a + a^T R^TQR a`.

The first three terms vanish by the radical gate. The remaining terms are exactly the claimed expression. QED.

### Meaning

This is stronger than saying only that `q(Gs)=0`. It says gauge is orthogonal, for the debit bilinear form, to every lineality and pointed direction used by the consumer. Thus the entire relevant Gram matrix factors through the quotient.

---

## 3. Theorem B — representative changes by gauge leave all Schur input blocks unchanged

Let `S in R^{g x ell}` and `T in R^{g x m}` be arbitrary. Replace the chosen lifts by

`L' = L + G S`,

`R' = R + G T`.

These define the same quotient classes as `L,R`.

### Statement

Under the radical gate,

**`L'^T Q L' = A`,**

**`L'^T Q R' = B`,**

**`R'^T Q R' = C`.**

### Proof

For example,

`L'^T Q R'`

`=L^TQR + S^T G^TQR + L^TQG T + S^T G^TQG T`

`=L^TQR=B`.

The other two identities are identical expansions. QED.

### Consequence

Every branch decision in T-P5-224 that depends only on `(A,B,C)` is already a quotient invariant. This includes the positive signed-direction branch, the singular kernel/cross branch, and the Schur-reduced pointed branch.

---

## 4. Theorem C — generic signed-lineality dispatcher commutes with the quotient

Consider

`q(c,a)=c^T A c + 2 c^T B a + a^T C a`, `a>=0`.

There are three mathematical branches exactly as in T-P5-224.

### C1. Positive lineality direction

If there exists `c0` with `c0^T A c0>0`, then `q(t c0,0)=t^2 c0^T A c0>0` for every nonzero `t`.

Since `A` is lift-representative invariant by Theorem B, quotient-first and ambient-first dispatch identically.

### C2. Negative-semidefinite branch and kernel/cross obstruction

Assume `A<=0` and set `P=-A>=0`.

If there exist `z in ker(P)` and `a>=0` with

`z^T B a != 0`,

then along signed scaling `c=t z`,

`q(tz,a)=2t z^TBa + a^T C a`.

Choosing the sign of `t` gives arbitrarily large positive values. Therefore finite Schur elimination is legal only if

**`z^T B=0` for every `z in ker(P)`,**

equivalently

**`range(B) subset range(P)`.**

Both `P` and `B` are quotient invariant, so this obstruction is the same in either order.

### C3. Range-compatible Schur branch

Assume `range(B) subset range(P)` and choose any `Y` satisfying

`P Y = B`.

Then

`q(c,a)`

`= -(c-Ya)^T P(c-Ya) + a^T D a`,

where

**`D := C + Y^T P Y`.**

Indeed expansion of the first term gives

`-c^TPc + 2c^TPYa - a^TY^TPYa`,

and `PY=B`; adding `a^T(C+Y^TPY)a` recovers `q`.

If `Y1,Y2` are two solves, then `P(Y1-Y2)=0`; hence

`Y1^T P Y1 = Y2^T P Y2`,

so `D` is solve-independent.

Since `(P,B,C)` are representative invariant, **the same `D` is obtained whether the face-gauge quotient is taken before or after the signed-lineality Schur step.**

---

## 5. Theorem D — keeping radical gauge as extra signed coordinates gives the identical dispatcher

The strongest form of the commutation statement is to *not quotient at all* initially. Treat gauge and physical lineality together as signed coordinates.

Define

`L_aug = [G, L]`.

By Theorem A the signed Gram block and signed/pointed cross block are

`A_aug = [[0,0],[0,A]]`,

`B_aug = [0; B]`.

In the NSD branch set

`P_aug=-A_aug=[[0,0],[0,P]]`.

### D1. Range compatibility equivalence

**`range(B_aug) subset range(P_aug)` iff `range(B) subset range(P)`.**

Proof: `P_aug [u;v]=[0;Pv]`, while `B_aug=[0;B]`. Thus solvability column by column is exactly `Pv=B`. QED.

### D2. Kernel-cross equivalence

The augmented kernel is

`ker(P_aug)=R^g x ker(P)`.

For `(u,z)` in this kernel,

`(u,z)^T B_aug = z^T B`.

Hence pure gauge directions contribute no new kernel-cross obstruction, and every physical kernel-cross obstruction is preserved exactly.

### D3. Reduced debit equivalence

A solve of

`P_aug Y_aug=B_aug`

has arbitrary gauge rows and physical rows `Y` satisfying `PY=B`. Therefore

`Y_aug^T P_aug Y_aug = Y^T P Y`.

So the reduced matrix is again exactly

**`D=C+Y^TPY`.**

This proves literal commutation: deleting the radical gauge block first or leaving it inside the singular signed block until after Schur elimination produces the same pointed quadratic.

---

## 6. Corollary — T-P5-226 arbitrary-corank fraction-free packet commutes with gauge deletion

Assume now rational data, `P=P^T>=0`, `rank(P)=r>0`, and use T-P5-226.

Choose a maximal positive principal anchor `I` of size `r` in the physical lineality coordinates. Let

`P0=P[I,I]>0`,

`delta=det(P0)>0`,

`H=adj(P0)`.

For the physical packet the T-P5-226 range residual on non-anchor rows is

`R_phys = delta B_J - P_JI H B_I`.

After adding `g` radical gauge coordinates, the augmented PSD signed block is

`P_aug = diag(0_g,P)`,

and the augmented cross block is `[0;B]`.

The same anchor `I` remains a maximal rank-`r` positive principal anchor. Every gauge row of the T-P5-226 residual is

`delta*0 - 0*H*B_I = 0`,

while every physical non-anchor row is exactly the old residual. Hence

**`R_aug = [0; R_phys]`.**

Therefore:

1. the exact range gate passes/fails identically;
2. the fraction-free kernel basis merely gains pure gauge columns `delta e_g`;
3. the scaled solve on the physical rows is unchanged;
4. the reduced numerator remains

   **`Dhat = delta C + B_I^T H B_I`;**
5. sign decisions agree because `delta>0`.

Thus T-P5-226's higher-corank implementation is not merely abstractly quotient invariant; its exact bordered-minor / adjugate packet is unchanged except for trivially zero gauge rows and columns.

T-P5-225 is the corank-one special case.

---

## 7. Exact rational regression — higher-corank gauge augmentation changes nothing

Take ambient coordinates `(g,l1,l2,r)` and

`Q = [[0,0,0,0],
      [0,-1,-1,2],
      [0,-1,-1,2],
      [0, 2, 2,1]]`.

Let gauge `G=e_g`, physical signed lineality lifts `L=[e_l1,e_l2]`, and pointed lift `R=e_r`.

Then `QG=0`, so the global radical condition holds. The physical blocks are

`A=[[-1,-1],[-1,-1]]`,

`P=-A=[[1,1],[1,1]]`,

`B=(2,2)^T`,

`C=1`.

Here `rank(P)=1`. Choose anchor `I={l1}`. Then

`delta=1`, `H=[1]`.

The outside physical range residual is

`1*2 - 1*1*2 = 0`.

A solve is `Y=(2,0)^T`, so

`Y^T P Y=4`,

and

**`D=1+4=5`.**

The fraction-free numerator gives the same value directly:

`Dhat=delta*C+B_I^T H B_I=1+4=5`.

Now retain the gauge coordinate as an extra signed variable. Then

`P_aug=diag(0,P)`

has rank one and corank two. The gauge residual row is exactly zero; the old physical residual remains zero; the same anchor gives `Dhat=5`.

Finally change representatives by gauge:

`l1' = l1 + 3g`,

`l2' = l2 - 2g`,

`r'  = r - 5g`.

Because `Qg=0`, all Gram blocks remain exactly `(A,B,C)`, hence `Dhat=5` again.

This exercises simultaneously representative change, a genuine singular physical lineality block, extra gauge corank, and the fraction-free anchor branch.

---

## 8. Counterexample — storage-zero and even debit-isotropic gauge is not enough

It is not sufficient that the gauge be storage-zero, nor is it sufficient to check only `g^TQg=0`.

Take `Y=R^3` with coordinates `(g,l,r)`. Let a storage matrix be

`K=diag(0,1,1)`.

Then `g=e1` is a genuine storage-radical direction: `Kg=0`.

Let endpoint debit matrix

`Q = [[0, 0, 1],
     [0,-1, 0],
     [1, 0, 0]]`.

Then

`g^T Q g = 0`,

so the gauge is even *isotropic* for the debit quadratic. But

`g^T Q r = 1`,

so it is not debit-radical on the consumed span.

Use signed lineality lift `L=l=e2` and pointed lift `R=r=e3`. The blocks are

`A=-1`, `B=0`, `C=0`,

so the Schur-reduced pointed debit is

`D=0`.

Now choose another representative of the **same quotient pointed ray**,

`R' = r + g`.

Modulo `span(g)`, `R'` and `R` are identical. But

`C' = (r+g)^T Q(r+g)`

`   = r^TQr + 2g^TQr + g^TQg`

`   = 0 + 2 + 0 = 2`.

The signed cross block is still zero, so the new Schur reduction gives

**`D'=2`.**

Thus quotient-identical representatives produce different positive-debit decisions.

This counterexample proves that the commutation theorem genuinely needs the T-P5-222 *cross-radical* conditions such as `G^TQR=0`; storage zero or the weaker scalar test `G^TQG=0` cannot replace them.

---

## 9. Consequence for T-P5-215 one-ray / pair pruning

Within one already-certified storage-zero compatibility clique, suppose the pointed endpoint packet after signed-lineality reduction is represented by columns of `R` and reduced quadratic matrix `D`.

T-P5-215 asks only for self and compatible-pair positive-debit witnesses, i.e. entries / two-ray restrictions of the pulled pointed Gram quadratic.

By Theorems B–D, radical face-gauge quotient and signed-lineality Schur elimination produce exactly the same `D`. Therefore every one-ray self debit and every compatible-pair cross debit is identical in either order.

So the safe dispatcher order may be chosen for implementation convenience:

`storage-zero clique -> face-gauge radical gate -> quotient -> physical lineality split -> Schur -> one/pair pruning`

or

`storage-zero clique -> face-gauge radical gate -> keep gauge as zero signed block -> physical lineality split -> augmented Schur -> delete gauge -> one/pair pruning`.

The outputs are mathematically identical.

The radical gate itself may **not** be postponed or omitted: Section 8 shows why.

---

## 10. Minimal theorem statements for formalization

A Lean-facing decomposition can avoid quotient types initially and prove only matrix identities.

### Leaf 1 — Gram block invariance

Given symmetric `Q` and matrices `G,L,R`, assume

`G^T*Q*G=0`, `G^T*Q*L=0`, `G^T*Q*R=0`.

For arbitrary `S,T`, prove the three identities for `L+GS`, `R+GT`.

### Leaf 2 — augmented range gate

For `P>=0`, prove

`range([0;B]) subset range(diag(0,P)) <-> range(B) subset range(P)`.

A columnwise existential formulation may be easier than abstract range syntax.

### Leaf 3 — augmented kernel-cross gate

Show every kernel vector of `diag(0,P)` is `(u,z)` with `Pz=0`, and its cross pairing with `[0;B]` is `z^TB`.

### Leaf 4 — augmented Schur value

Assuming `PY=B`, prove directly

`[U;Y]^T diag(0,P) [U;Y] = Y^TPY`

for arbitrary gauge row block `U`.

### Leaf 5 — fraction-free anchor row extension

Under T-P5-226 hypotheses, prove that appending zero rows/columns to `P` and zero rows to `B` appends zero rows to the bordered-minor residual and preserves `Dhat`.

These are algebraic leaves; no quotient library or pseudoinverse is required.

---

## 11. Boundaries left open

This review deliberately does **not** close:

1. the actual source identity of any `G,L,R,Q` packet;
2. proof that a particular face-gauge family satisfies the restricted radical gate on every consumed clique;
3. the storage-zero compatibility graph / maximal-clique coverage;
4. construction of physical lineality generators for the actual endpoint cone;
5. actual T-P5-226 anchor/range residual data;
6. actual reduced `D` copositivity or positive-debit witness;
7. cell/tube/trajectory and PDE/ODE semantics;
8. Float64 / interval / rounding transport;
9. Lean compilation, `#print axioms`, comparator or kernel receipt;
10. independent validation by 封不觉;
11. admission, registry, M4, or parent closure.

Failure of a real packet to satisfy the radical gate is not by itself failure of the physical theorem. It means only that this quotient-first endpoint representation is invalid; one must retain the relevant lift degrees of freedom or redesign the physical endpoint coordinates.

---

## 12. Structural fingerprint and next seam

The new structural fingerprint is

**debit-radical face gauge -> zero Gram block -> quotient/representative invariance -> signed physical lineality dispatcher -> singular Schur reduction -> invariant pointed debit.**

The face gauge and physical lineality are different objects but their reductions commute because the former is radical for the debit form.

A non-overlapping next mathematical seam is now the *actual radical-gate producer*: given a face-lift family generated from source-side tangent/endpoint equations, derive `G^TQG=0`, `G^TQL=0`, and `G^TQR=0` from a structural annihilation identity (for example a constraint-adjoint or conservation/symmetry identity) rather than checking every Gram entry independently. If such an identity does not exist for the real source packet, the correct result is a concrete obstruction, not silent quotienting.