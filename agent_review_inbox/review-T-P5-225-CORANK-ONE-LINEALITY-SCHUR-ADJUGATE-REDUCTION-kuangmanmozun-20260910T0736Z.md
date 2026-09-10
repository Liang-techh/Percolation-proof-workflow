---
kind: review_result
review_id: review-T-P5-225-corank-one-lineality-schur-adjugate-reduction-kuangmanmozun-20260910T0736Z
task_id: T-P5-225-CORANK-ONE-LINEALITY-SCHUR-ADJUGATE-REDUCTION
reviewer: 狂蛮魔尊
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-10T07:36:00Z
claim_commit: 9037cf7e9185327ca8a4eecdb0599d7a44f1e60a
inspected_commit: acc8c742395ea3747db340dd6eb2c10b77b68dbe
upstream_commits:
  - 53af0acf2a6a9f7146f0847d7ff860560cb035ae  # T-P5-224 lineality Schur endpoint reduction
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_corank_one_adjugate_range_gate; add_fraction_free_anchored_schur_reduction; add_constructive_cross_and_reduced_witnesses; add_anchor_independence_checksum; add_counterexamples_and_lean_targets
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact finite-dimensional symmetric linear algebra, adjugate identities, principal-minor Schur completion, rational counterexamples; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-225 — corank-one lineality Schur reduction without pseudoinverses

## 0. Verdict and seam closed

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-224 reduces one physical endpoint clique with signed lineality coordinates `c` and pointed coordinates `a>=0` to

`q(c,a) = c^T A c + 2 c^T B a + a^T C0 a`.

Its exact dispatcher first asks whether `A<=0`, then whether `range(B) subset range(A)`, and, if so, solves `A Y=-B` and tests the reduced orthant form

`D = C0 - Y^T A Y`.

This child closes the frequent **corank-one negative-semidefinite lineality block** case by replacing the singular solve / pseudoinverse viewpoint by exact determinants and adjugates.

Set

`P := -A`.

Assume throughout this child that `P=P^T >= 0` and `rank(P)=ell-1` for `ell>=2`. Let

`J := adj(P)`.

Then the T-P5-224 range/kernel branch becomes a two-way exact rational dispatcher:

1. **kernel-cross obstruction:** `J B != 0` iff `range(B)` is not contained in `range(P)`; a nonzero entry of `JB` directly yields a kernel vector and an unbounded positive debit witness;
2. **compatible branch:** if `JB=0`, choose any anchor `i` with `delta_i := J_ii > 0`. The principal block `P_II`, `I={1,...,ell}\{i}`, is positive definite. Define

   `H_i := adj(P_II)`,

   `Dhat_i := delta_i C0 + B_I^T H_i B_I`.

   Then `Dhat_i = delta_i D`, with `delta_i>0`. Therefore the sign problem on `D` is exactly the sign problem on the fraction-free rational matrix `Dhat_i`.

No inverse, Moore-Penrose pseudoinverse, spectral tolerance, or floating nullspace is needed for the checker-facing statement.

No actual P5 same-key `A/B/C0`, endpoint packet, selector/cell/tube, trajectory coverage, Float64/interval semantics, Lean/kernel receipt, independent validation, admission, registry mutation, or parent closure is claimed.

---

## 1. Corank-one adjugate structure

Let `P=P^T>=0` and `rank(P)=ell-1`.

### Theorem A1 — adjugate is the exact kernel projector up to positive scale

`J=adj(P)` is nonzero, symmetric, positive semidefinite, rank one, and

`range(J)=ker(P)`.

Equivalently, if `z` spans `ker(P)`, then for some `gamma>0`,

`J = gamma z z^T`.

### Proof

Because `rank(P)=ell-1`, `det(P)=0` but at least one `(ell-1)x(ell-1)` minor is nonzero, hence `adj(P)!=0`. The adjugate identity gives

`P J = J P = det(P) I = 0`,

so `range(J) subset ker(P)`. Both spaces have dimension one, hence equality and `rank(J)=1`.

Since `P` is symmetric PSD with one zero eigenvalue and all other eigenvalues positive, orthogonal diagonalization gives

`P = U diag(lambda_1,...,lambda_{ell-1},0) U^T`, `lambda_k>0`.

The adjugate is

`J = (prod_k lambda_k) u_0 u_0^T`,

where `u_0` spans the nullspace. Thus `J>=0` and has the stated rank-one form. QED.

### Exact rational consequence

For rational `P`, all entries of `J` are rational. Corank one can be fail-closed by an exact rank certificate or, equivalently under `det(P)=0`, by `J!=0` together with the already-established PSD/rank premise.

---

## 2. T225-B — the T-P5-224 range gate becomes `JB=0`

### Theorem B1 — adjugate range criterion

Under the assumptions above,

`range(B) subset range(P)`

iff

`J B = 0`.

Equivalently, because `J>=0` has rank one,

`B^T J B = 0`.

### Proof

Write `J=gamma z z^T` with `gamma>0` and `ker(P)=span(z)`. Since `P` is symmetric,

`range(P)=ker(P)^perp=z^perp`.

Thus every column of `B` lies in `range(P)` iff `z^T B=0`. But

`J B = gamma z (z^T B)`,

so this is equivalent to `JB=0`. Also

`B^T J B = gamma (B^T z)(z^T B)>=0`,

and it vanishes iff `z^T B=0`. QED.

### Constructive failure witness

If `(JB)_{ij} != 0`, define

`z_i := J e_i`.

Then `P z_i=0` and

`z_i^T B e_j = (JB)_{ij} != 0`.

For the original endpoint debit with `A=-P`, choose `a=e_j`. Along signed lineality

`c=t z_i`,

we have

`q(t z_i,e_j)=2 t (JB)_{ij} + (C0)_{jj}`.

Choosing the sign and magnitude of `t` yields `q>0`, indeed `sup_t q=+infinity`.

So in the corank-one NSD corridor, **`JB!=0` is not merely a failed reduction gate; it is an explicit mathematical positive-debit obstruction/witness.**

---

## 3. T225-C — a positive diagonal cofactor gives a PD anchor

Because `J>=0`, each diagonal cofactor

`delta_i := J_ii = det(P_II)`

is nonnegative, where `I` deletes coordinate `i`. Since `J!=0` and rank one PSD, at least one diagonal entry is strictly positive.

### Theorem C1 — good anchor criterion

If `delta_i>0`, then `P_II` is positive definite.

### Proof

`P_II` is a principal submatrix of a PSD matrix, hence PSD. Its determinant is `delta_i>0`. A PSD matrix with positive determinant has no zero eigenvalue, therefore it is PD. QED.

In the rank-one representation `J=gamma z z^T`,

`delta_i=gamma z_i^2`.

Hence `delta_i>0` is exactly the coordinate-free statement that the deleted coordinate sees the one-dimensional kernel.

---

## 4. T225-D — fraction-free anchored solve

Assume now `JB=0`, and choose any anchor `i` with `delta:=delta_i>0`. Let `I` denote all coordinates except `i`, set

`P0 := P_II`,

`H := adj(P0)`,

and define an `ell x r` matrix `Ytilde` by

`(Ytilde)_i,* = 0`,

`(Ytilde)_I,* = H B_I`.

### Theorem D1 — exact scaled solve

`P Ytilde = delta B`.

Consequently

`Y := Ytilde/delta`

satisfies

`P Y=B`, equivalently `A Y=-B`.

### Proof

On the retained rows `I`,

`(P Ytilde)_I = P0 H B_I = det(P0) B_I = delta B_I`.

Thus the residual

`r := P Ytilde - delta B`

is supported only on coordinate `i`.

Let `z:=J e_i`. Since `delta=J_ii>0`, `z_i=delta!=0`. Also `Pz=0`, and from `JB=0`,

`z^T B = e_i^T J B =0`.

Therefore

`z^T r = z^T P Ytilde - delta z^T B =0`.

But `r` is supported at `i`, so `z^T r=z_i r_i=delta r_i`; hence `r_i=0`. Thus `r=0` and `P Ytilde=delta B`. QED.

This proof never inverts the singular full matrix `P`.

---

## 5. T225-E — fraction-free reduced orthant matrix

Define

`Dhat_i := delta C0 + B_I^T H B_I`.

### Theorem E1 — exact Schur scaling identity

For `Y=Ytilde/delta`, the T-P5-224 reduced matrix

`D := C0 + Y^T P Y`

satisfies

`Dhat_i = delta D`.

### Proof

From `P Ytilde=delta B`,

`Ytilde^T P Ytilde = delta Ytilde^T B`.

Since the anchor row of `Ytilde` is zero,

`Ytilde^T B = B_I^T H B_I`.

Hence

`Y^T P Y = (1/delta^2)Ytilde^T P Ytilde
           = (1/delta) B_I^T H B_I`.

Multiplying `D=C0+Y^TPY` by `delta` gives the claim. QED.

Because `delta>0`, for every `a>=0`,

`sign(a^T D a) = sign(a^T Dhat_i a)`.

Thus

`-D copositive` iff `-Dhat_i copositive`.

The singular full solve has been reduced to one PD principal block determinant/adjugate and one ordinary orthant quadratic check.

---

## 6. T225-F — exact corank-one dispatcher

Combining T-P5-224 with the preceding identities gives a complete two-branch theorem.

### Theorem F1 — positive-debit existence in the corank-one NSD lineality corridor

Let

`q(c,a)=-c^T P c + 2c^T B a + a^T C0 a`, `a>=0`,

with `P=P^T>=0`, `rank(P)=ell-1`.

Then exactly one of the following compatible cases governs the checker:

#### F1a. `JB!=0`

A positive debit witness exists, and the debit is unbounded above along a signed kernel direction with one pointed coordinate fixed.

#### F1b. `JB=0`

Choose any `i` with `delta_i>0` and form `Dhat_i` as above. Then

`exists c, a>=0 : q(c,a)>0`

iff

`exists a>=0 : a^T Dhat_i a>0`.

Equivalently,

`forall c, a>=0, q(c,a)<=0`

iff

`-Dhat_i` is copositive.

### Proof of compatible branch

The exact completion is

`q(c,a)=-(c-Ya)^T P(c-Ya)+a^T D a`.

Since `P>=0`, the first term is nonpositive. At fixed `a`, therefore

`sup_c q(c,a)=a^T D a`,

and the supremum is attained at every

`c=Ya+t z`, `z in ker(P)`.

Using `Dhat_i=delta_i D` and `delta_i>0` proves the equivalence. QED.

This eliminates Branch G1 of T-P5-224 automatically: in this corridor `A=-P<=0`, so pure signed-lineality self-debit cannot be positive. The only possible positive mechanisms are exactly the kernel-cross escape (`JB!=0`) or the reduced pointed orthant debit (`Dhat_i`).

---

## 7. T225-G — division-free positive witness reconstruction

Suppose `JB=0` and a pointed vector `a0>=0` satisfies

`a0^T Dhat_i a0 > 0`.

The obvious witness uses `c=Y a0`, which contains a division by `delta`. A checker can avoid this division entirely.

Define

`a_star := delta a0`,

`c_star := Ytilde a0`.

Then

`P c_star = B a_star`,

so the completed negative square vanishes, and

`q(c_star,a_star)
 = a_star^T D a_star
 = delta * (a0^T Dhat_i a0)
 > 0`.

Thus an orthant witness for `Dhat_i` lifts to an exact positive endpoint-debit witness by multiplication and adjugates only.

For integer-cleared source data, the entire witness can remain integer-cleared as well.

---

## 8. T225-H — anchor independence and exact checksum

Different positive cofactors may be used as anchors. Let `i,k` satisfy

`delta_i>0`, `delta_k>0`.

Construct `Dhat_i,Dhat_k` separately.

### Theorem H1 — canonical normalized reduced matrix

`Dhat_i/delta_i = Dhat_k/delta_k = D`.

Equivalently, without division,

`delta_k Dhat_i = delta_i Dhat_k`.

### Proof

Both anchored constructions solve `P Y=B` and T-P5-224 already shows the reduced matrix `D=C0+Y^TPY` is independent of the chosen solution, since two solutions differ by a kernel vector and `P` kills that difference. Applying Theorem E1 for each anchor gives the cross-multiplied identity. QED.

### Checker value

When more than one positive cofactor is available, the equality

`delta_k Dhat_i = delta_i Dhat_k`

is a cheap exact algebraic checksum. A mismatch is evidence that at least one purported block/anchor construction is not the same mathematical packet. This checksum is not source provenance and does not by itself establish same-key binding.

---

## 9. Exact rational regressions and negative controls

### R1 — kernel compatibility cannot be skipped

Take

`P=[[1,-1],[-1,1]]`,

`A=-P`,

`B=(1,0)^T`,

`C0=0`.

Then

`J=adj(P)=[[1,1],[1,1]]`,

so `JB=(1,1)^T!=0`.

With `z=(1,1)` and pointed scalar `a=1`,

`q(tz,1)=2t`,

which is unbounded above.

But if one naively deletes the first coordinate and performs only the retained principal solve, then `P_II=[1]`, `B_I=[0]`, and one would obtain the spurious reduced value `Dhat=0`. This is a false NO-WITNESS conclusion. Therefore **the exact `JB=0` gate must precede principal-block Schur reduction.**

### R2 — the deleted coordinate must have positive cofactor

Take

`P=diag(1,0,1)`.

Then `P>=0`, corank one, and

`J=diag(0,1,0)`.

Deleting coordinate 1 gives `delta_1=0` and leaves a singular principal block. Deleting coordinate 2 gives `delta_2=1` and leaves `diag(1,1)>0`.

Thus the anchor rule is not “delete any coordinate”; it is exactly `J_ii>0`.

### R3 — anchor independence with unequal cofactors

Let

`P=[[1,0,-1],[0,1,-2],[-1,-2,5]]`,

so

`x^T P x=(x1-x3)^2+(x2-2x3)^2>=0`,

and `ker(P)=span(1,2,1)`. Its adjugate is

`J=[[1,2,1],[2,4,2],[1,2,1]]`.

Take

`B=(1,0,-1)^T`, `C0=0`.

Then `JB=0`. Anchoring coordinate 1 gives

`delta_1=1`, `Dhat_1=1`.

Anchoring coordinate 2 gives

`delta_2=4`, `Dhat_2=4`.

Both yield the same normalized reduced scalar

`D=1`.

The exact checksum is `4*Dhat_1=1*Dhat_2=4`.

### R4 — PSD is essential for sign transport

Take

`P=diag(1,-1,0)`.

This matrix is corank one but not PSD. Its third cofactor is `delta_3=-1`. With `B=0`, `C0=1`, the true reduced scalar is `D=1`, while the formal fraction-free quantity is `Dhat_3=-1`.

Thus the sign of `Dhat` is reversed. The positivity equivalence relies essentially on `P>=0`, which guarantees a **positive** anchor determinant. This branch must not be applied to an indefinite `P`.

### R5 — corank one is essential for the adjugate gate

Take

`P=diag(1,0,0)`, `B=e2`, `C0=0`.

Then `P>=0` but has corank two, and `adj(P)=0`. Hence `JB=0` trivially, even though `B` is not in `range(P)`. Indeed with `c=t e2`, `a=1`,

`q(c,1)=2t`

is unbounded above.

Therefore `adj(P)B=0` is an exact range test only under the explicit rank-`ell-1` premise. Higher-corank lineality must route back to the generic T-P5-224 kernel/range dispatcher (or a later compound-minor generalization).

---

## 10. Implementation-facing exact algorithm

For a T-P5-224 clique whose signed lineality block is suspected corank one:

1. set `P=-A`;
2. certify ordinary `P>=0` and `rank(P)=ell-1` exactly;
3. compute `J=adj(P)`;
4. if `JB!=0`, extract a nonzero entry `(i,j)`, use `z=J e_i`, and emit the T225-B kernel-cross positive witness;
5. if `JB=0`, choose any `i` with `delta=J_ii>0`;
6. compute the PD principal block `P_II`, `H=adj(P_II)`, and `Dhat=delta C0+B_I^T H B_I`;
7. call the existing orthant quadratic/copositivity machinery on `-Dhat`;
8. if it returns `a0>=0` with `a0^T Dhat a0>0`, lift it by `c_star=Ytilde a0`, `a_star=delta a0`;
9. if multiple positive cofactors are convenient, optionally cross-check `delta_k Dhat_i=delta_i Dhat_k`.

Every algebraic step can be exact over `Q` after common denominator clearing.

A failed corank-one gate is **NOT** a mathematical failure:

- if `P` is not PSD, route to the earlier general signed-block branch;
- if `rank(P)<ell-1`, route to the generic T-P5-224 range/kernel solve or a higher-corank child;
- if no actual same-key packet is available, remain pending source binding.

---

## 11. Formalizable theorem decomposition

Suggested exact-real Lean leaves, deliberately avoiding pseudoinverses:

1. `adjugate_psd_corank_one_rank_one`
   - hypotheses: symmetric PSD `P`, rank `ell-1`;
   - result: `adj(P)` is PSD rank one, nonzero, and its range is `ker(P)`.

2. `range_subset_iff_adjugate_mul_eq_zero_of_corank_one`
   - `range(B) subset range(P) <-> adj(P) ⬝ B = 0`.

3. `positive_principal_minor_of_positive_adjugate_diagonal`
   - `adj(P) i i > 0 -> P_II` positive definite.

4. `corankOne_scaled_principal_solve`
   - define `Ytilde_i=0`, `Ytilde_I=adj(P_II) B_I`;
   - prove `P Ytilde = det(P_II) B` under `adj(P)B=0`.

5. `corankOne_fractionFree_schur_identity`
   - prove `Dhat=delta*C0+B_I^T adj(P_II) B_I = delta*D`.

6. `corankOne_signedOrthant_positive_iff_fractionFree_positive`
   - exact positive-witness equivalence for `q`.

7. `corankOne_fractionFree_witness_lift`
   - from `a0^T Dhat a0>0`, produce `(Ytilde a0, delta a0)` and prove positive debit.

8. `corankOne_anchor_crossmultiply_invariant`
   - `delta_k Dhat_i = delta_i Dhat_k` for two positive-cofactor anchors.

A first formalization can take the corank-one adjugate structure as an explicit premise if Mathlib's rank/adjugate API is inconvenient; the consumer theorem itself only needs `PJ=0`, rank-one/range facts, one positive diagonal cofactor, and the scaled-solve identity.

---

## 12. Remaining obligations / fail-closed boundary

Still open and not claimed here:

- actual same-key P5 lineality/debit blocks `A,B,C0`;
- proof that a real source packet is in the corank-one `P=-A>=0` corridor;
- actual endpoint clique / face-gauge / pointed-ray packet and T-P5-224 compatibility premises;
- source/selector/cell/tube identity and physical trajectory coverage;
- Float64/interval transport and rounding semantics;
- final orthant copositivity result for an actual `Dhat`;
- Lean/kernel compilation and axiom audit;
- independent validation by 封不觉;
- admission, registry, or P5/P8/M4 parent closure.

The theorem should remain `CONDITIONAL_PASS_MATHEMATICAL_CHILD` until those separate gates are supplied.

## 13. Recommended next mathematical seam

The corank-one case is now completely fraction-free. The next non-overlapping hard seam is the **higher-corank signed-lineality block** where `adj(P)=0`: replace the single adjugate by a maximal-rank principal minor / kernel-basis or compound-matrix certificate, while preserving an exact pre-check that detects `range(B) not subset range(P)` and produces a constructive kernel-cross witness. A worthwhile target is a rank-`r` principal-block formula whose reduced `Dhat` is invariant under the chosen maximal nonsingular principal anchor up to a positive determinant scale.