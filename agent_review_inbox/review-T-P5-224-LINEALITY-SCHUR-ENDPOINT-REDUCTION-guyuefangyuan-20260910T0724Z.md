---
kind: review_result
review_id: review-T-P5-224-lineality-schur-endpoint-reduction-guyuefangyuan-20260910T0724Z
task_id: T-P5-224-LINEALITY-SCHUR-ENDPOINT-REDUCTION
reviewer: 古月方源
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-10T07:24:00Z
claim_commit: 9ce3a0d9df0915126ed535e5ee141d9196c6bb02
inspected_commit: 54acf2bfc56353950a0e91fb3732a2021ef80040
upstream_commits:
  - d5426eb17fb3d2466af3e287237ce6f18d4f55f5  # T-P5-221 heterogeneous-chart bilinear transport
  - 467527fa4670608070e0d74e64e6b7087a8b3094  # T-P5-222 face-lift quotient debit descent
  - 405ed7c3265609c7827967b53a5480c007c8a3ae  # T-P5-223 quotient-cone Gram invariance
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_quotient_cone_lineality_positive_cycle_characterization; add_lineality_pointed_split; add_exact_extreme_ray_transcript; add_signed_orthant_schur_endpoint_dispatcher; add_counterexamples_and_lean_targets
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact finite-dimensional cone/quotient algebra, Farkas separation, symmetric Schur completion, rational counterexamples; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-224 — quotient-cone lineality split and signed/orthant Schur endpoint reduction

## 0. Verdict and the seam actually closed

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-223 shows how to replace one lifted endpoint generator packet by another through exact nonnegative transport modulo the T-P5-222 lift gauge. Its suggested next step is to compress each maximal storage-zero compatibility cone down to its minimal physical endpoint rays.

There is one subtle obstruction before that compression is mathematically safe: after quotienting the face-lift gauge, the physical endpoint cone need not be pointed. Distinct nonnegative storage-zero combinations can map to opposite endpoint directions. Such **physical lineality is not the same object as face-lift gauge**. T-P5-222 makes the debit invariant under gauge, but it does not imply that the debit is invariant under adding a genuine lineality direction.

This child gives the exact finite-dimensional split and the correct endpoint-debit dispatcher.

Let `W=[w_1 ... w_r]` be one lifted generator packet inside a fixed storage-zero compatibility clique, let `N=range(G)` be the already-certified T-P5-222 gauge subspace, and write

`C := { [W a] in Y/N : a >= 0 }`.

Then:

1. a generator belongs to the physical lineality space `lin(C)=C cap (-C)` **iff it participates with positive coefficient in a nonnegative cycle modulo gauge**;
2. the set of all such generators spans exactly `lin(C)`;
3. after separating those lineality generators and quotienting by their span, the remaining finite cone is pointed;
4. on that pointed quotient, iterative exact conic-redundancy deletion plus a Farkas separator yields a complete extreme-ray transcript;
5. one may quotient the lineality out of the **debit** only under an additional radical condition. Without it, doing so can delete a real positive endpoint-debit witness;
6. if lineality is retained as free signed coordinates `c` and pointed rays as nonnegative coordinates `a`, the endpoint debit has a mixed block form

   `q(c,a)=c^T A c + 2 c^T B a + a^T C0 a`.

   There is an exact three-way Schur dispatcher for existence of a positive debit witness:

   - positive direction of `A`;
   - a kernel/cross obstruction `ker(A)` versus `B`;
   - otherwise an orthant quadratic test on the reduced matrix `D=C0-Y^T A Y`, where `A Y=-B`.

This is the missing bridge between quotient-cone compression and the T-P5-210/215 endpoint debit consumer. It also gives a precise negative control: **lineality may be eliminated from the endpoint packet only when it is debit-radical, not merely because it is lineality for the physical endpoint cone.**

No actual P5 same-key `W/G/Q`, chart/face packet, selector/cell/tube, trajectory coverage, Float64/interval semantics, Lean/kernel receipt, independent validation, admission, registry mutation, or parent closure is claimed.

---

## 1. Setup and notation

Let `Y=R^m`. Let `G in R^{m x g}` have column span `N` and let

`pi : Y -> Y/N`

be the quotient map. Let

`W=[w_1 ... w_r] in R^{m x r}`

be lifted endpoint generators belonging to **one already-established storage-zero compatibility clique**. The physical endpoint cone represented by the packet is

`C = pi(W R_+^r)`.

Assume throughout the T-P5-222 restricted radical condition needed to make the endpoint debit well-defined modulo `N`. For a symmetric endpoint/debit matrix `Q=Q^T`, this can be expressed on the packet span by

`G^T Q W = 0`,

`G^T Q G = 0`.

Nothing below identifies physical lineality with `N`.

---

## 2. T224-A — lineality is exactly positive-cycle participation

Define the physical lineality space

`L := lin(C) = C cap (-C)`.

For a generator index `j`, consider the following exact feasibility statement:

there exist `a>=0` and `s` such that

`W a = G s`

and

`a_j > 0`.

Equivalently, after positive rescaling, one may require `a_j >= 1`.

### Theorem A1 — generator lineality iff positive gauge-cycle participation

For every index `j`, the following are equivalent:

1. `pi(w_j) in L`;
2. there exist `a>=0`, `s` with `a_j>0` and `W a=G s`.

### Proof

Assume 1. Since `pi(w_j) in L`, also `-pi(w_j) in C`. Hence there is `b>=0` with

`-pi(w_j)=pi(W b)`.

Thus

`pi(W(e_j+b))=0`,

so `W(e_j+b)` lies in `range(G)`. Taking `a=e_j+b` gives `a>=0` and `a_j>=1`.

Conversely assume 2. Modulo `N`,

`sum_k a_k pi(w_k)=0`.

Because `a_j>0`,

`-pi(w_j)=sum_{k != j} (a_k/a_j) pi(w_k)`

belongs to `C`. Of course `pi(w_j)` itself belongs to `C`. Therefore `pi(w_j) in C cap (-C)=L`.

QED.

### Rational certificate consequence

If `W,G` are rational, lineality membership admits an exact rational primal certificate. The normalized system

`W a = G s`, `a>=0`, `a_j>=1`

is a rational polyhedron. If it has a real point, it has a rational point. A producer therefore never needs a floating nullspace tolerance to certify that a generator participates in lineality.

---

## 3. T224-B — the participating generators span the whole lineality space

Let

`I_L := { j : pi(w_j) in L }`.

### Theorem B1 — exact lineality generator theorem

`L = span{ pi(w_j) : j in I_L }`.

In fact the conic hull of those same generators already equals `L`:

`L = cone{ pi(w_j) : j in I_L }`.

### Proof

Every `pi(w_j)` with `j in I_L` lies in the subspace `L`, so their cone and span are contained in `L`.

For the reverse inclusion, take arbitrary `ell in L`. Since `ell in C` and `-ell in C`, there exist `a,b>=0` with

`ell = sum_i a_i pi(w_i)`,

`-ell = sum_i b_i pi(w_i)`.

Adding gives

`sum_i (a_i+b_i) pi(w_i)=0`.

Whenever `a_i+b_i>0`, Theorem A1 says `i in I_L`. Therefore the displayed representation of `ell` uses only indices in `I_L`. Hence `ell` lies in the conic hull of the lineality generators.

QED.

### Practical packet

A complete lineality certificate can therefore consist of:

- the index set `I_L`;
- for each `j in I_L`, one rational positive-cycle witness `(a^(j),s^(j))`;
- for each `j notin I_L`, a dual infeasibility certificate for the normalized positive-cycle system.

The last item is optional for soundness if a separate complete polyhedral solver transcript is trusted, but it is the cleanest fail-closed exact interface.

---

## 4. T224-C — quotienting the physical lineality leaves a pointed cone

Choose a matrix `U` whose columns are representatives whose quotient classes form a basis of `L`. Set

`H := [G U]`.

Let `R` denote the submatrix of `W` consisting only of indices not in `I_L`. Consider the projected cone

`C_pt := { [R a] in Y/range(H) : a>=0 }`.

### Theorem C1 — pointed quotient

`C_pt` is pointed.

### Proof

Suppose a class `x` belongs to both `C_pt` and `-C_pt`. Then for some `a,b>=0`,

`x=[R a]`, `-x=[R b]`

modulo `range(H)`. Therefore

`R(a+b)`

is congruent modulo `N` to a vector in `L`.

Assume some coordinate `j` of `a+b` is positive. Write `c=a+b`. Since `pi(Rc) in L`, also `-pi(Rc) in C`. Hence

`-c_j pi(w_j) = -pi(Rc) + sum_{k != j} c_k pi(w_k)`

belongs to `C`. Thus `-pi(w_j) in C`, and therefore `j in I_L` by Theorem A1, contradicting the construction of `R`.

Hence `a+b=0`; with `a,b>=0`, this forces `a=b=0`, so `x=0`.

QED.

This theorem is what makes an exact **extreme-ray** interpretation available after lineality has been separated.

---

## 5. T224-D — exact extreme-ray transcript after the lineality split

Work now in the pointed quotient `Y/range(H)` with remaining generators `r_1,...,r_p` (columns of `R`).

A candidate generator `r_j` is conically redundant modulo `H` exactly when there exist

`t>=0`, `s`

such that

`r_j = R_{-j} t + H s`.

### Theorem D1 — exact redundancy deletion

If the above equation holds, deleting column `j` does not change `C_pt`.

This is the T-P5-223 deletion theorem with physical lineality included in the quotient carrier.

### Theorem D2 — Farkas separator for a kept generator

If the redundancy system is infeasible, there exists a separator `y` satisfying

`H^T y = 0`,

`R_{-j}^T y >= 0`,

`r_j^T y < 0`.

Conversely, any such `y` proves infeasibility immediately.

For rational `R,H`, a rational separator exists whenever the system is infeasible; it may be positively rescaled to a root-free normalization such as `r_j^T y <= -1`.

### Theorem D3 — irredundant generators of the pointed quotient are exactly extreme rays

Suppose all zero columns have been removed and a final packet generates `C_pt` with no column conically redundant modulo the others. Then every surviving generator spans an extreme ray of `C_pt`, and every extreme ray of `C_pt` is represented by at least one surviving generator. Because duplicates are redundant, the final packet has exactly one ray representative per extreme ray up to positive scaling.

### Proof of the nontrivial direction

Let `v_j` be a surviving generator and suppose its ray is not extreme. Then

`v_j=x+y`

with `x,y in C_pt` and neither `x` nor `y` belonging to the ray `R_+ v_j`. Expand `x,y` in the final generators and combine coefficients:

`v_j = alpha_j v_j + sum_{k != j} alpha_k v_k`, `alpha_k>=0`.

If `alpha_j<1`, then

`v_j = sum_{k != j} alpha_k/(1-alpha_j) v_k`,

contradicting irredundancy.

If `alpha_j>1`, then a nonzero negative multiple of `v_j` lies in `C_pt`, contradicting pointedness.

If `alpha_j=1`, then `sum_{k != j} alpha_k v_k=0`. Pointedness forces every nonzero summand to vanish, so `x` and `y` can only be nonnegative multiples of `v_j`, again contradicting the assumed non-extreme decomposition.

Therefore the ray is extreme.

QED.

### Complete producer transcript

Inside one maximal storage-zero compatibility clique, a producer can now compress the endpoint packet by a finite exact transcript:

1. certify all physical-lineality indices by positive cycles modulo `G`;
2. choose a rational basis `U` for their quotient span;
3. quotient by `[G U]`;
4. delete redundant remaining columns using exact nonnegative transport;
5. for every kept column, emit a rational Farkas separator.

The resulting kept columns are a complete minimal physical endpoint-ray packet **of the pointed quotient**.

---

## 6. T224-E — physical lineality is not automatically debit gauge

The previous section is only a geometric compression. The endpoint debit may not factor through the additional quotient by `L`.

Let `Q=Q^T` and retain the T-P5-222 gauge radical condition for `G`.

### Theorem E1 — exact gate for quotienting lineality out of debit

The endpoint bilinear form is invariant under adding physical lineality directions on the relevant packet span iff

`U^T Q W = 0`.

Given the existing T-P5-222 gauge radical condition and `range(U) subset span(W,G)`, this is equivalent to saying the lineality space is contained in the radical of the endpoint debit restricted to the represented physical span.

Under this gate, all debit values factor through the pointed quotient and the extreme-ray packet from Section 5 is a lossless endpoint-debit representation.

Without this gate, quotienting by `L` is unsound.

### Exact counterexample E2 — deleting lineality deletes a positive witness

Take endpoint space `Y=R`, no face gauge, and lifted endpoint generators

`W=[1,-1]`.

Then `C=R`, so the whole endpoint cone is lineality. Let

`Q=[1]`.

Both physical directions have positive debit `q_Q(1)=q_Q(-1)=1`. If one quotients the lineality away merely because the pointed quotient is `{0}`, the positive debit witness disappears completely.

This can occur even inside a perfectly valid storage-zero clique: take storage matrix `K=0_2`, so every nonnegative coefficient vector is a storage zero and both atoms are compatible.

Therefore the lineality split is not a license to erase lineality from T-P5-210/215.

---

## 7. T224-F — exact signed/orthant Schur reduction when lineality must be retained

Choose a basis `U` of the physical lineality `L` and a minimal pointed generator matrix `R` from Section 5. Every physical endpoint class in the clique can be represented as

`U c + R a`,

where

`c in R^ell` is **free signed** and `a in R_+^p` is nonnegative.

Define the endpoint debit blocks

`A := U^T Q U`,

`B := U^T Q R`,

`C0 := R^T Q R`.

Then

`q(c,a) = c^T A c + 2 c^T B a + a^T C0 a`.

The endpoint no-positive-debit question is

`q(c,a) <= 0` for all `c in R^ell`, `a>=0`.

### Theorem F1 — complete mixed signed/orthant no-positive criterion

The following are equivalent:

1. `q(c,a)<=0` for every signed `c` and nonnegative `a`;
2. all three conditions hold:

   **F1a.** `A` is negative semidefinite;

   **F1b.** every column of `B` lies in `range(A)`; equivalently

   `z^T B=0` for every `z in ker(A)`;

   **F1c.** for one/every matrix `Y` satisfying

   `A Y = -B`,

   the reduced matrix

   **`D := C0 - Y^T A Y`**

   is nonpositive on the coefficient orthant:

   `a^T D a <= 0` for all `a>=0`.

Equivalently `-D` is copositive.

### Proof: 1 implies 2

Set `a=0`. Then `c^T A c<=0` for every `c`, so `A<=0`.

Now take `z in ker(A)` and one pointed generator coordinate `e_j`. For arbitrary real `t`,

`q(tz,e_j)=2t z^T B e_j + (C0)_{jj}`.

If `z^T B e_j != 0`, choose the sign of `t` and let `|t|` grow. The expression becomes positive, contradicting item 1. Hence `z^T B=0` for all `z in ker(A)`. Because `A` is symmetric in finite dimension,

`range(A)=ker(A)^perp`,

so `range(B) subset range(A)` and a solution `Y` of `A Y=-B` exists.

For any `a>=0`, choose `c=Y a`. Then the completed-square term below vanishes, leaving

`a^T D a = q(Y a,a) <=0`.

Thus F1c holds.

### Proof: 2 implies 1

Using `A Y=-B`, expand

`(c-Y a)^T A (c-Y a)`

`=c^T A c + 2c^T B a + a^T Y^T A Y a`.

Therefore

**`q(c,a) = (c-Y a)^T A(c-Y a) + a^T D a`.**

The first term is nonpositive because `A<=0`, and the second is nonpositive by F1c. Hence `q(c,a)<=0` for all allowed `(c,a)`.

QED.

### Independence of the chosen solution `Y`

If `Y1,Y2` both solve `A Y=-B`, their difference `Z=Y1-Y2` has columns in `ker(A)`. Thus `AZ=0`, and

`Y1^T A Y1 = Y2^T A Y2`.

So `D` is canonical despite possible singularity of `A`; no pseudoinverse is needed.

---

## 8. T224-G — exact positive-debit witness dispatcher

Negating Theorem F1 gives a constructive three-branch dispatcher.

### Branch G1 — lineality self-debit

If `A` has a vector `c` with

`c^T A c > 0`,

then `(c,0)` is already a positive endpoint-debit witness.

### Branch G2 — kernel/cross escape

Assume `A<=0`, but F1b fails. Then there exist

`z in ker(A)` and a pointed coordinate `j`

with

`beta:=z^T B e_j != 0`.

For `a=e_j`,

`q(tz,e_j)=2t beta+(C0)_{jj}`.

Choosing the sign of `t` so `t beta>0` and taking `|t|` large gives an explicit positive witness. In fact the debit is unbounded above along this signed lineality direction.

### Branch G3 — reduced orthant debit

Assume `A<=0` and `range(B) subset range(A)`. Solve `A Y=-B` exactly. If some `a>=0` satisfies

`a^T D a>0`,

then

`c=Y a`

makes the negative-semidefinite square vanish, and `(c,a)` is a positive endpoint-debit witness with exact value `a^T D a`.

Conversely, if none of G1/G2/G3 occurs, no positive debit witness exists anywhere in the physical endpoint cone represented by the clique.

This is an exact finite-dimensional theorem, not a relaxation.

---

## 9. T224-H — important special cases

### H1. Debit-radical lineality

If

`A=0`, `B=0`,

then physical lineality is completely invisible to debit and

`D=C0`.

This is exactly the additional radical gate of Section 6. Only in this branch is it safe simply to drop the lineality coordinates before the endpoint consumer.

### H2. Zero self-debit does not imply lineality is harmless

If `A=0` but `B != 0`, Branch G2 fires. Thus checking only `c^T A c=0` on every lineality basis vector is insufficient. The cross block with pointed rays is essential.

### H3. Negative-definite lineality block

If `A<0`, then

`Y=-A^{-1}B`

and

`D = C0 - B^T A^{-1} B = C0 + B^T(-A)^{-1}B`.

The correction is positive semidefinite. Optimizing over signed lineality can therefore make positive endpoint debit **more likely**, even when every pure lineality direction has negative debit.

The inverse formula is explanatory only; the theorem itself needs only the exact solve `A Y=-B`, so rational fraction-free elimination/LDL can be used.

---

## 10. Exact rational regressions

### Regression R1 — pure lineality positive debit

`W=[1,-1]`, `G` empty, `Q=[1]`.

The endpoint cone is all of `R`; pointed quotient is zero, but debit has value `1` on either unit lineality direction. Any checker that deletes physical lineality without the Q-radical gate gives a false NO-WITNESS result.

### Regression R2 — cross-only positive debit with zero self debit

Take

`W=[e1,-e1,e2]` in `R^2`,

so lineality is `span(e1)` and the pointed quotient ray is `e2`. Let

`Q=[[0,1],[1,0]]`.

Then

`A=[0]`, `B=[1]`, `C0=[0]`.

Every generator has zero self debit, yet

`q(c,a)=2ca`.

With `c=a=1`, debit is `2>0`. This is exactly Branch G2: `A=0` but the lineality/pointed cross block is nonzero. It proves that separate self scans of lineality and extreme rays are incomplete.

### Regression R3 — negative lineality curvature, Schur-created positive debit

With the same cone, let

`Q=[[-1,1],[1,0]]`.

Then

`A=[-1]`, `B=[1]`, `C0=[0]`.

The exact solve is `Y=[1]`, and

`D = 0 - 1*(-1)*1 = 1`.

Hence Branch G3 gives the witness `c=1,a=1`, with

`q(1,1)=1`.

So even strictly negative lineality self-debit cannot be discarded before completing the signed Schur term.

### Regression R4 — genuinely harmless lineality

Let

`Q=[[0,0],[0,1]]`

on the same cone. Then `A=0`, `B=0`, `C0=1`. Physical lineality is Q-radical, so quotienting it out is lossless and the pointed ray alone carries the positive debit witness.

---

## 11. Relation to T-P5-221/222/223 and the main endpoint route

This child does not replace the three upstream results; it orders them.

A safe endpoint pipeline inside one maximal storage-zero compatibility cone is now:

1. **T-P5-221:** reconstruct endpoint pairings across heterogeneous PD-prefix charts;
2. **T-P5-222:** quotient only the face-lift gauge that is radical for `Q`;
3. **T-P5-223:** merge/delete conically redundant lifted generators modulo that gauge;
4. **T-P5-224-A/B:** detect genuine physical endpoint lineality by nonnegative cycles modulo gauge;
5. **T-P5-224-C/D:** quotient the lineality geometrically and produce a minimal pointed extreme-ray transcript;
6. **T-P5-224-E:** if lineality is also Q-radical, delete it from the debit consumer;
7. otherwise retain a signed lineality basis and use **T-P5-224-F/G** to reduce the mixed signed/orthant endpoint debit to a negative-semidefinite gate, a range/kernel gate, and one orthant copositivity-equivalent gate on `-D`.

This gives a canonical role for lineality rather than silently confusing it with lift gauge.

The storage-zero compatibility boundary from T-P5-223 remains mandatory: all of this compression happens **inside one maximal storage-zero compatibility cone**. No cross-clique endpoint cone merge is licensed.

---

## 12. Suggested Lean theorem decomposition

The mathematics can be formalized without quotient bases at first. A small exact-real vector/matrix API is enough.

Recommended leaves:

1. `quotientCone_generator_mem_lineality_iff_positiveCycle`
   - input `W,G,j`;
   - prove the equivalence between `-pi(w_j)` conic representability and a nonnegative gauge cycle with positive j-th coefficient.

2. `quotientCone_lineality_span_positiveCycleGenerators`
   - prove the lineality space/cone is generated by the participating columns.

3. `quotientCone_removeLineality_isPointed`
   - with a certified complete lineality index set/basis, prove the remaining cone modulo `[G,U]` is pointed.

4. `cone_redundancy_farkas_separator`
   - producer-facing exact separator lemma; a first Lean version can verify a supplied separator without formalizing Farkas completeness.

5. `irredundant_generators_extreme_of_pointed`
   - finite cone theorem turning a deletion transcript into extreme-ray completeness.

6. `linealityDebit_radical_iff_crossBlockZero`
   - express the extra gate `U^T Q W=0` for lossless debit quotienting.

7. `signedOrthantQuadratic_nonpos_iff_schurRangeCopositive`
   - main theorem F1 using `A<=0`, `A Y=-B`, and copositivity of `-(C0-Y^TAY)`.

8. `positiveDebit_of_linealityKernelCross`
   - explicit Branch G2 witness.

9. `positiveDebit_of_reducedOrthantWitness`
   - explicit Branch G3 witness `c=Ya`.

A first formalization should avoid pseudoinverses. Let the producer supply `Y` together with the exact equation `A Y=-B`; singular-solution independence is a separate tiny lemma.

---

## 13. Remaining obligations / fail-closed boundary

Still open and not claimed here:

- actual same-key P5 lifted endpoint packet `W` and face-gauge packet `G`;
- proof that the generators belong to one maximal storage-zero compatibility clique;
- actual endpoint/debit matrix `Q` and its relation to T-P5-210/215;
- complete lineality-cycle enumeration for a real source packet;
- exact rational basis `U` and final extreme-ray transcript for that packet;
- source/selector/cell/tube identity and physical trajectory coverage;
- Float64/interval transport and rounding semantics;
- Lean/kernel compilation and `#print axioms`;
- independent verification by 封不觉;
- admission, registry, or parent P5/P8/M4 closure.

A negative result from the lineality dispatcher is useful: if actual packet data produce Branch G1/G2/G3, it is a real mathematical endpoint obstruction/witness under the stated same-key premises. But no such actual source packet was instantiated in this child.

## 14. Recommended next mathematical/source step

For the next source-facing P5 producer, do **not** immediately run a generic quadratic search on every zero atom pair. First, within each already-certified storage-zero compatibility clique:

- compute positive cycles modulo the T-P5-222 gauge to identify physical lineality;
- reduce the pointed quotient to an irredundant ray packet with exact nonnegative-transport and separator certificates;
- form the small debit blocks `A=U^TQU`, `B=U^TQR`, `C0=R^TQR`;
- dispatch G1/G2/G3.

If `A=B=0`, the consumer can safely ignore lineality and operate only on the minimal pointed endpoint rays. If not, the signed Schur block is mathematically unavoidable and should be preserved rather than hidden by a quotient-basis normalization.