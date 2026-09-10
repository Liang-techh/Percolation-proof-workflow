---
kind: review_result
review_id: review-T-P5-217-pd-prefix-atom-completeness-branch-bound-guyuefangyuan-20260910T0530Z
task_id: T-P5-217-PD-PREFIX-ATOM-COMPLETENESS-BRANCH-BOUND
reviewer: 古月方源
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-10T05:30:00Z
claim_commit: 653ded0ec3ee18465213b5dea06c231ab152b317
inspected_commit: c86ded59ea35431750f5c150062fe1c75fe0a37e
upstream_commits:
  - 803e7681f61385fee8a9c1c00b97c1d76061ee71  # T-P5-216 minimal-zero atoms
  - 4daeafdb1733f8bba97cd4576b68989cdcf31890  # T-P5-215 compatibility cliques
  - 6f8b539f94aba1fcf3a9106a8989ee88e7a1c38b  # T-P5-214 zero-support PSD decomposition
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_pd_prefix_necessity; add_fraction_free_atom_gate; add_nonpd_subtree_prune; add_residual_feasibility_farkas_prune; add_complete_search_transcript_semantics
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact finite-dimensional linear algebra, Schur complement, Farkas alternative, rational regressions; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-217 — PD-prefix minimal-zero atom completeness / branch-and-bound

## 0. Verdict and seam closed

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-216 identifies the canonical primitive zero packet of a symmetric copositive matrix `K`: the support-minimal zeros, equivalently strict-positive corank-one principal-kernel rays. It deliberately leaves the next problem open: how to certify that the minimal-support atom enumeration is complete without relying on singleton-zero seeds and without separately extracting rays from every higher-corank support.

This child gives an exact branch-and-bound theorem.

The key structure is stronger than a generic subset search:

1. every **proper** principal subblock of a minimal-zero support is positive definite;
2. therefore the first non-positive-definite prefix on any support branch kills the entire descendant family;
3. from a positive-definite prefix, one determinant plus one cofactor vector gives an inverse-free trichotomy: continue / emit one atom / prune;
4. a still stronger optional whole-family prune is obtained by eliminating the PD prefix and asking a purely linear **positive-kernel + nonnegative-residual feasibility** problem on all remaining coordinates;
5. infeasibility has a finite Farkas dual certificate with exact rational arithmetic;
6. a finite ordered search transcript whose unexpanded branches all carry one of these local certificates proves that the emitted atom packet is complete.

This remains exponential in the worst case. It is a **completeness certificate and exact pruning rule**, not a polynomial-time claim.

No actual P5 source identity, selector/cell/tube coverage, Float64 semantics, Lean/kernel receipt, independent verification, admission, registry mutation, or parent closure is claimed.

---

## 1. Setup from T-P5-214/T-P5-216

Assume throughout

`K = K^T`

and `K` is copositive:

`x >= 0  =>  x^T K x >= 0`.

For every nonnegative zero `x`, T-P5-214 gives

`Kx >= 0`,

`x_i (Kx)_i = 0`,

and on `S=supp(x)`,

`K_SS >= 0`,

`K_SS x_S = 0`.

T-P5-216 proves that a nonzero zero `x` is support-minimal iff

`x_S > 0`,

`K_SS >= 0`,

`ker(K_SS)=span{x_S}`.

Equivalently, `K_SS` is PSD of corank one with a strict-positive kernel ray.

Call such a normalized ray a **minimal-zero atom**.

---

## 2. T217-A — every proper principal subblock of an atom support is PD

### Theorem A

Let `x` be a minimal-zero atom with support `S`. Then for every nonempty proper subset

`T proper_subset S`,

one has

**`K_TT > 0` (positive definite).**

### Proof

By T-P5-216,

`K_SS >= 0`

and

`ker(K_SS)=span{x_S}`

with `x_S>0`.

Every principal submatrix `K_TT` is therefore PSD. Suppose some proper `T` were singular. Choose nonzero

`v_T in ker(K_TT)`.

Extend it by zero to a vector `v_S` on all of `S`. Then

`v_S^T K_SS v_S = v_T^T K_TT v_T = 0`.

Because `K_SS` is PSD, zero quadratic energy implies

`v_S in ker(K_SS)=span{x_S}`.

But `v_S` vanishes on the nonempty set `S\T`, while every nonzero multiple of `x_S` is strict-positive or strict-negative on every coordinate of `S`. Contradiction.

Hence `K_TT` is nonsingular PSD, therefore positive definite. QED.

### Corollary A1 — exact subtree prune

If a coordinate set `T` is **not** positive definite, then no minimal-zero atom support can strictly contain `T`.

This is the first exact branch-and-bound rule.

It is important that the conclusion is only about **minimal-zero atom descendants**. A non-PD principal block does not imply that global copositivity fails; copositive matrices may have indefinite principal blocks.

### Corollary A2 — singleton semantics

For a globally copositive `K`, every diagonal satisfies `K_ii>=0`.

- If `K_ii=0`, then `e_i` is already a singleton minimal-zero atom, and no larger minimal atom can contain `i`.
- If `K_ii>0`, `{i}` is a legitimate PD search prefix.
- `K_ii<0` contradicts the assumed global copositivity and is not a normal atom-search branch state.

Thus atom enumeration does **not** start from singleton zeros only. It starts from every positive diagonal coordinate as a PD prefix, while diagonal-zero coordinates are emitted immediately as singleton atoms.

---

## 3. T217-B — one-step fraction-free Schur/determinant atom gate

Let `T` be a current support prefix with

`A := K_TT > 0`.

Choose a new coordinate `j notin T`, and write

`b := K_{T,j}`,

`c := K_jj`.

Let

`d := det(A) > 0`,

`u := -adj(A) b`,

and define the scaled Schur numerator

`σ := d c - b^T adj(A) b`.

By the block determinant identity,

**`σ = det K_{T union {j}, T union {j}}`.**

Since `A^{-1}=adj(A)/d`, the ordinary scalar Schur complement is

`δ = c-b^T A^{-1} b = σ/d`.

Because `d>0`, `σ` and `δ` have the same sign.

### Theorem B — exact trichotomy

For the child support `S=T union {j}`:

#### Case B1: `σ>0`

Then

`K_SS > 0`.

The child remains a PD prefix and may contain a larger minimal atom. Continue the branch.

#### Case B2: `σ<0`

Then `K_SS` is not positive definite. By Corollary A1, **no minimal atom can contain `S`**. Prune the entire descendant branch.

#### Case B3: `σ=0`

Then `K_SS` is PSD of corank one, and the exact scaled kernel generator is

**`w_S = (u,d)`**, with the entries ordered as `T` followed by `j`.

Indeed,

`A u + b d = -A adj(A)b + b det(A)=0`,

and

`b^T u + c d = -b^T adj(A)b + cd = σ=0`.

The Schur complement is zero, so the block is PSD; because `A` is nonsingular, the corank is exactly one.

Therefore:

**`S` is a minimal-zero atom support iff `u>0` componentwise.**

The last coordinate `d` is already strictly positive. If `u>0`, zero-extension of `w_S` gives a strict-positive corank-one principal-kernel zero, hence a minimal atom by T-P5-216.

If `u` has any zero or negative coordinate, the unique kernel line contains no strict-positive vector, so `S` is not an atom support. Since `K_SS` is singular, Corollary A1 also kills every strict descendant containing `S`.

### Exact arithmetic consequence

For rational `K`, this gate uses only

- determinant,
- adjugate/cofactors,
- matrix-vector multiplication,
- sign comparisons.

No square root, eigenvector, pseudoinverse, numerical nullspace tolerance, or algebraic-number reification is needed.

A normalized atom can be emitted as

`xi_S = w_S / (1^T w_S)`.

Since all entries are rational, the normalization remains rational.

---

## 4. T217-C — canonical ordered search is complete

Fix once and for all a coordinate order, for example

`1 < 2 < ... < n`.

Enumerate supports by increasing ordered subsets. Every nonempty subset appears exactly once as a branch whose coordinates are added in increasing order.

### Search rule

At a singleton `{i}`:

- `K_ii=0`: emit `e_i` and terminate that branch;
- `K_ii>0`: enter the PD-prefix recursion;
- `K_ii<0`: the global copositivity premise has failed.

At a PD prefix `T`, for each admissible next coordinate `j>max(T)`, apply Theorem B:

- `σ>0`: recurse on `T union {j}`;
- `σ=0` and `u>0`: emit the atom and terminate that child;
- `σ=0` and `u not>0`: terminate that child as singular non-atom;
- `σ<0`: terminate that child as non-PD.

### Theorem C — soundness and completeness

The atoms emitted by this search are **exactly all support-minimal nonnegative zeros of `K`**, each exactly once.

### Proof: soundness

Every emitted nonsingleton support comes from `A>0`, `σ=0`, `u>0`. Theorem B gives a PSD corank-one principal block with strict-positive kernel. T-P5-216 converts it to a minimal-zero atom. Singleton emissions are the same theorem in dimension one.

### Proof: completeness

Let `S={i_1<...<i_m}` be the support of any minimal atom.

If `m=1`, global copositivity and zero energy give `K_{i_1 i_1}=0`, so the singleton is emitted.

Assume `m>=2`. For every proper ordered prefix

`T_r={i_1,...,i_r}`, `1<=r<m`,

Theorem A gives

`K_{T_r,T_r}>0`.

Therefore the canonical branch for `S` cannot be cut by a non-PD or singular-prefix prune before the final coordinate.

At the final step `T_{m-1} -> S`, the full atom block is PSD corank one, so `σ=det(K_SS)=0`. Its kernel is spanned by the positive atom vector. Since the scaled kernel generator `(u,d)` has `d>0`, it must have the same orientation as that atom and hence `u>0`. The branch emits `S`.

Uniqueness follows from the fixed increasing coordinate order. QED.

### Consequence

T-P5-216 Regression D is no longer an obstruction to a tree search. The invalid strategy was **singleton-zero-seeded growth**. The valid complete strategy is **PD-prefix growth**.

---

## 5. T217-D — whole-family positive-kernel + residual feasibility prune

The determinant gate prunes one child support at a time. A stronger optional rule can reject **every** atom extension of a PD prefix `T` using a whole remaining coordinate pool `R` in one linear certificate.

Let

`A=K_TT>0`,

`d=det(A)>0`,

and let `R` contain every coordinate still allowed to appear later on this canonical branch.

Define the exact rational matrices

**`C := -adj(A) K_{T,R}`**

and

**`Hhat := d K_{R,R} - K_{R,T} adj(A) K_{T,R}`.**

`Hhat=dH`, where `H` is the ordinary Schur complement of `A`, but no division is required.

### Theorem D — necessary extension feasibility

If there exists any minimal-zero atom `x` whose support strictly contains `T` and uses only coordinates from `T union R`, then there exists a vector `λ>=0` such that

**`C λ > 0`**

and

**`Hhat λ >= 0`.**

Equivalently, by positive scaling of `λ`, the rational linear system

**`λ >= 0`,**

**`C λ >= 1`,**

**`Hhat λ >= 0`**

is feasible, where `1` is the all-ones vector of length `|T|`.

### Proof

Let `x` be such an atom and extend its coordinates on `R` by zero outside the atom support:

`λ := x_R >=0`.

Because every coordinate of `x_T` is positive and `x` is a copositive zero, complementarity gives

`(Kx)_T=0`.

Thus

`A x_T + K_{T,R} λ = 0`.

Multiply by `adj(A)`:

`d x_T = -adj(A)K_{T,R}λ = Cλ`.

Since `d>0` and `x_T>0`, this proves `Cλ>0`.

Global copositivity plus zero energy also gives the full residual

`Kx>=0`.

On the remaining coordinates,

`(Kx)_R = K_{R,T}x_T + K_{R,R}λ >=0`.

Multiply by `d` and substitute `d x_T=Cλ=-adj(A)K_{T,R}λ`:

`d(Kx)_R`
`= [dK_RR-K_RT adj(A)K_TR] λ`
`= Hhat λ >=0`.

Finally, if `Cλ>0`, scale `λ` by a sufficiently large positive scalar so that `Cλ>=1`. The `Hhat` inequality is homogeneous. QED.

### Interpretation

`Cλ>0` says that the eliminated PD prefix would reconstruct a strict-positive active vector

`x_T = Cλ/d`.

`Hhatλ>=0` is exactly the scaled nonnegative residual condition on every still-available coordinate.

Hence this is not a heuristic geometric filter. It is a necessary projection of the full copositive-zero KKT/complementarity conditions.

It deliberately does **not** enforce the final complementarity equalities or zero quadratic energy, so feasibility is not an atom certificate. It is a safe **prune-only** test.

---

## 6. T217-E — exact Farkas dual certificate for family pruning

Write the primal feasibility system from Theorem D as

`λ>=0`,

`Cλ>=1`,

`Hhatλ>=0`.

### Theorem E — alternative

Exactly one of the following holds:

#### Primal extension-feasibility packet

There exists `λ>=0` with

`Cλ>=1`,

`Hhatλ>=0`.

#### Dual prune packet

There exist vectors

`p>=0`, `q>=0`

such that

**`1^T p > 0`**

and

**`C^T p + Hhat^T q <= 0`.**

Since `Hhat` is symmetric, the last term may be written `Hhat q`.

### Why the dual packet proves pruning

Assume both packets existed. Then

`λ^T(C^T p+Hhat^T q)`
`= p^T Cλ + q^T Hhatλ`
`>= p^T 1`
`>0`.

But `λ>=0` and `C^T p+Hhat^T q<=0` force the same quantity to be `<=0`, contradiction.

The converse existence of a dual certificate when the primal is infeasible is the standard finite-dimensional Farkas alternative applied to the stacked system

`[C; Hhat] λ >= [1;0]`, `λ>=0`.

One may normalize `p` so that

`1^T p=1`.

### Rationality

If `K` is rational, then `A,d,adj(A),C,Hhat` are rational. When the primal rational polyhedron is infeasible, the Farkas certificate may be chosen rational and normalized by `1^Tp=1`.

Therefore an entire coordinate-family prune can be checked by exact rational matrix multiplication and order comparisons only.

### Corollary E1 — cheaper positive-kernel-only prune

Setting `q=0` gives a cheaper sufficient prune certificate:

`p>=0`, `p!=0`, `C^T p<=0`.

This is the Gordan/Stiemke separation showing that no `λ>=0` can make `Cλ>0`.

The full `(p,q)` certificate is strictly stronger because it also uses residual nonnegativity.

---

## 7. T217-F — finite search transcript certifies atom-packet completeness

The previous pieces give a concrete completeness object, not merely an algorithm description.

A **PD-prefix atom search transcript** records, for every canonical support branch, one of the following terminal reasons:

1. `SINGLETON_ATOM`: `K_ii=0`;
2. `ATOM`: parent block PD, `σ=0`, scaled kernel `(u,d)>0`;
3. `SINGULAR_NONATOM_PRUNE`: parent PD, `σ=0`, but `u not>0`;
4. `NEGATIVE_SCHUR_PRUNE`: parent PD, `σ<0`;
5. `FARKAS_FAMILY_PRUNE`: current prefix PD and a normalized rational `(p,q)` satisfies the dual packet;
6. `EXHAUSTED_PD_LEAF`: the branch has no remaining coordinate and the final prefix is PD;
7. `EXPANDED_PD_CHILD`: `σ>0`, with child branches recursively covered.

### Theorem F — transcript completeness

If every root coordinate and every admissible canonical child is covered by such a finite transcript, then the collection of all `SINGLETON_ATOM` and `ATOM` emissions is a **complete minimal-zero atom packet** for `K`.

### Proof sketch

Take any minimal atom support `S` and follow its unique increasing-prefix branch.

By Theorem A, every proper prefix is PD, so the path cannot encounter terminal reasons 1, 3, or 4 before the final support. It also cannot encounter a Farkas family prune: Theorem D constructs a primal feasible `λ` from the atom itself, contradicting the dual packet. It cannot end at an exhausted proper PD leaf because the next coordinate of `S` remains available.

Thus the path is recursively expanded until the final support, where Theorem B forces the `ATOM` case. Singleton atoms are handled at the root.

Therefore no minimal atom is omitted. Soundness was already proved in Theorem C. QED.

### Consumer consequence for T-P5-216

T-P5-216 says that a **complete** atom packet is sufficient to reconstruct every higher-corank zero cone by compatibility cliques and to exhaust the T-P5-210 self/pair debit witness test.

T217 supplies a finite exact meaning of the word **complete**: a closed PD-prefix transcript with local determinant/cofactor or Farkas certificates on every unexpanded branch.

No second higher-corank support-ray extraction is needed.

---

## 8. Regression A — finds a size-two atom with no singleton zero seed

Take

`K=[[1,-1],[-1,1]]`.

This matrix is PSD, hence copositive. Neither singleton is a zero because both diagonals equal `1`.

Start from the PD prefix `T={1}`:

`A=[1]`, `d=1`, `b=[-1]`, `c=1`.

Then

`σ = 1*1-(-1)^2 = 0`,

`u=-adj(A)b=1>0`.

The scaled kernel generator is

`(u,d)=(1,1)>0`.

So the algorithm emits the unique minimal atom `(1,1)` immediately.

This directly closes T-P5-216 Regression D: singleton-**zero** seeding is incomplete, but singleton **PD-prefix** seeding is complete.

---

## 9. Regression B — singular mixed-sign child prunes descendants

Take the all-ones PSD matrix

`K=J_3`.

At `T={1}`, adding coordinate `2` gives

`A=[1]`, `b=[1]`, `c=1`,

`σ=0`,

`u=-1<0`.

Thus the child block on `{1,2}` is singular PSD, but its kernel is spanned by `(1,-1)`, not by a positive vector. It is not an atom support.

More importantly, **no minimal atom can contain `{1,2}`**, because an atom's proper principal subblocks must all be PD. Hence pruning strict descendants is sound.

The same example also permits an even earlier family prune from `T={1}`, `R={2,3}`:

`C=[-1,-1]`.

No nonnegative `λ` can satisfy `Cλ>0`. The dual certificate `p=1`, `q=0` proves the entire subtree impossible.

---

## 10. Regression C — negative determinant is a branch prune, not global copositivity FAIL

Take

`K=[[1,2],[2,1]]`.

For `x>=0`,

`x^T K x = x1^2+4x1x2+x2^2 >0`

for every nonzero `x`, so `K` is strictly copositive.

Yet from the PD prefix `{1}`,

`σ=det(K)=-3<0`.

Therefore `{1,2}` cannot be a minimal-zero support and the branch is pruned.

This prevents an incorrect implementation from interpreting `σ<0` as failure of global copositivity.

---

## 11. Regression D — residual feasibility is strictly stronger than positive-kernel feasibility

Take the positive-definite matrix

`K = [[1,-1,2],[-1,2,-3],[2,-3,6]]`.

Use prefix `T={1}` and remaining coordinates `R={2,3}`.

Then

`A=[1]`, `d=1`,

`K_TR=[-1,2]`,

so

`C=[1,-2]`.

The positive-kernel-only test is feasible: for example

`λ=(3,1)`

gives

`Cλ=1>0`.

However

`Hhat`
`= K_RR-K_RT K_TR`
`= [[1,-1],[-1,2]]`.

The full residual-feasibility system requires

`λ1-2λ2 >= 1`,

`λ1-λ2 >= 0`,

`-λ1+2λ2 >=0`.

The first inequality forces `λ1>2λ2`, while the third forces `λ1<=2λ2`. Hence it is infeasible.

A normalized exact dual certificate is

`p=1`,

`q=(0,1)`.

Indeed

`C^T p + Hhat q`
`= (1,-2)^T + (-1,2)^T`
`= (0,0)^T <=0`,

and `1^Tp=1`.

Thus the residual-aware Farkas packet prunes the whole remaining family even though the cheaper positive-kernel test cannot.

---

## 12. Regression E — primal feasibility is prune-only, not an atom certificate

Take

`K=[[1,-1/2],[-1/2,1]]`.

This matrix is positive definite. With `T={1}`, `R={2}`,

`C=[1/2]`,

`Hhat=[3/4]`.

The primal feasibility test passes, e.g. `λ=2` gives

`Cλ=1`,

`Hhatλ=3/2>=0`.

But the child determinant is

`σ=3/4>0`,

so the full block remains PD and there is no zero atom.

Therefore a producer must never convert **LP feasible** into `ATOM_EXISTS`. Only **LP infeasible + dual certificate** is a terminal mathematical prune.

---

## 13. Implementation/checker semantics

A safe exact producer can maintain a branch state

`(T, det(K_TT), exact factor/cofactor data, remaining R)`

with the invariant

`K_TT>0`.

For each child it may choose either:

- the cheap one-step determinant/cofactor trichotomy; or
- before child expansion, the stronger family residual LP and an exact Farkas dual if infeasible.

For large exact rationals, Bareiss/fraction-free elimination may replace explicit adjugate construction operationally, provided the checker-visible semantics are equivalent to

`d=det(A)`,

`C=-adj(A)K_TR`,

`Hhat=dK_RR-K_RT adj(A)K_TR`.

The mathematics does not require floating LDL tolerances.

### Important non-FAIL statuses

- `σ<0` under a certified globally copositive `K`: branch has no atom descendant; not global FAIL.
- `σ=0` with mixed-sign kernel: singular non-atom branch; not global FAIL.
- family LP feasible: inconclusive, continue; not PASS and not FAIL.
- no dual Farkas packet found: incomplete pruning attempt; continue exact search.
- search transcript missing an unexpanded branch: `INCOMPLETE_MINIMAL_ZERO_PACKET`, never `NO_ATOM`.

---

## 14. Suggested Lean theorem leaves

The first formalization should stay in small linear-algebra pieces:

1. `minimalZero_properPrincipal_posDef`
   - strict-positive corank-one PSD support implies every proper principal subblock is PD.

2. `pdBlock_scaledSchur_det_identity`
   - `det([[A,b],[b^T,c]]) = det(A)c-b^T adj(A)b` for invertible/PD `A`.

3. `pdPrefix_zeroDet_scaledKernel`
   - if `A>0` and `σ=0`, `( -adj(A)b, det(A) )` spans the child kernel and the child is PSD corank one.

4. `pdPrefix_zeroDet_minimalAtom_iff_scaledKernel_pos`
   - under global copositivity / T216 bridge.

5. `nonPosDefPrefix_no_minimalZero_superset`
   - direct corollary of Theorem A.

6. `minimalAtomExtension_residualLP_feasible`
   - actual atom extension produces `λ>=0`, `Cλ>=1`, `Hhatλ>=0` after scaling.

7. `residualLP_dualCertificate_prunes`
   - the one-line dot-product contradiction; this can be formalized before the full Farkas converse.

8. `residualLP_infeasible_has_dualCertificate`
   - finite-dimensional Farkas theorem, possibly later if mathlib interface is inconvenient.

9. `pdPrefixSearch_complete_minimalAtoms`
   - induction on the finite ordered subset tree.

10. `rational_residualLP_infeasible_has_rationalDual`
    - optional exact-source leaf.

A practical Lean order is `1 -> 3 -> 5 -> 6 -> 7 -> 9`; the abstract Farkas converse need not block using externally produced dual prune certificates, because checking a supplied dual packet only needs theorem 7.

---

## 15. Boundaries deliberately left open

### Boundary A — worst-case combinatorics

The ordered PD-prefix search can still visit exponentially many PD supports. T217 provides exact pruning and a completeness transcript, not a polynomial-time guarantee.

### Boundary B — global copositivity premise

The minimal-zero characterization, complementarity, and residual nonnegativity inherit global copositivity from T-P5-214/T-P5-216. This child does not certify an arbitrary input `K` copositive.

### Boundary C — Farkas feasibility is only necessary

Passing the residual LP does not imply that any zero atom exists. Complementarity/zero-energy and the final singular positive-kernel gate remain necessary.

### Boundary D — actual source binding

No actual same-key P5 `K`, Schur packet, selector/cell/tube identity, rational reification path, or source hash is bound here.

### Boundary E — runtime/formal/admission

Float64/interval robustness, deployed determinant/cofactor sign classification, Lean/kernel proof, 封不觉 independent validation, P8/M4 propagation, registry mutation, and formal certificate admission remain open.

---

## 16. Recommended handoff

The T-P5-214 -> T-P5-216 endpoint-zero route can now use the following exact dispatcher:

`certified global K copositive`

`-> ordered PD-prefix atom search`

`-> optional residual-Farkas whole-family pruning`

`-> complete minimal-atom packet + closed search transcript`

`-> T-P5-216 aggregate residual compatibility graph`

`-> maximal zero cones / T-P5-210 self-pair debit scan`.

The next useful mathematics is no longer "how do we know the atom packet is complete?" in the abstract: T217 gives a finite certificate semantics. A further child should either (i) derive a sharper lower-dimensional complementarity reduction after the residual LP passes, or (ii) prove complexity/ordering heuristics that preserve transcript completeness while reducing the number of PD prefixes visited. Those would be optimizations, not prerequisites for soundness of the present theorem.