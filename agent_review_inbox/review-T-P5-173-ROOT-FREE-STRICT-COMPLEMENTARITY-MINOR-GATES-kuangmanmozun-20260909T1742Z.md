---
kind: review_result
review_id: review-T-P5-173-root-free-strict-complementarity-minor-gates-kuangmanmozun-20260909T1742Z
task_id: T-P5-173-ROOT-FREE-STRICT-COMPLEMENTARITY-MINOR-GATES
reviewer: 狂蛮魔尊
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-09T17:42:00Z
claim_commit: dbab4a9f09a8d17062fe811b425929b36683e7ef
inspected_commit: ba82f6c6f8b38f050a21d970e65f47b04652cb87
upstream_commits:
  - 8caf78bf7ce97b3a727a46c12739583a12d777f7  # T-P5-171 contact/KKT pivot transport
  - c4e82b5839bc037672c73635775399632e515406  # T-P5-172 low-degree symbolic pivot corridor
  - 300fec2e52d7a3a78107110f25df0ab016dc81d2  # T-P5-169 sharp-floor contact localization
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_strict_complementarity_contact_minor_gate; derive_active_principal_PSD_from_positive_contact; use_one_adjugate_column_as_division_free_positive_kernel_witness_in_corank_one_branch; encode_inactive_KKT_residuals_as_row_replacement_minors; combine_with_T172_quadratic_interval_sign_checker_to_certify_algebraic_floor_contacts_without_root_representation
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact finite-dimensional determinant/adjugate algebra; local SymPy exact-rational regression for Section 8 only
exit_code: 0 for exact symbolic regression; no Lean/kernel run
---

# T-P5-173 — root-free strict-complementarity gates from contact minors

## 0. Verdict and exact seam

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-171 proves that a zero contact of a certified copositive matrix is an orthant-KKT contact and that a T-P5-170 pivot chain transports the terminal contact back to the original coordinates. It deliberately leaves **strict complementarity** as a separate open obligation. T-P5-172 then removes the high-degree symbolic-`D` artifact for principal and almost-principal minors, but it does not say how to certify strict complementarity at an algebraic sharp floor without explicitly solving for the contact vector.

This review closes exactly that seam in the nondegenerate (corank-one active block) branch.

The main result is:

> at a positive-support copositive zero contact, the active principal block is automatically PSD; if that active block has corank one, one column of its adjugate is a positive division-free kernel vector, and every inactive KKT residual is exactly a row-replacement determinant. In the P5 rank-two floor pencil, all of those kernel and strict-complementarity gates are degree at most two in `D`. Hence an irrational sharp floor can be certified using only rational interval sign checks on quadratic polynomials, without representing the root or normalizing a nullvector.

The corank-one hypothesis is essential for this adjugate interface; a strict contact may exist with a higher-dimensional active kernel while the whole adjugate vanishes. A separate exact kernel-basis/LP branch is required there.

No source/provenance audit, runtime/Float64 claim, Lean/kernel validation, independent re-audit, admission, registry mutation, or parent closure is performed.

---

## 1. Setup

Let `M=M^T` be a finite real symmetric matrix. Let

`q_M(x) := x^T M x`.

Assume `M` is copositive:

**(1.1)** `x>=0  =>  q_M(x)>=0`.

Let `z>=0`, `z!=0`, and assume

**(1.2)** `q_M(z)=0`.

Let the positive support be

`S := {i : z_i>0}`

and let

`A := M[S,S]`.

Write `z_S` for the restriction of `z` to `S`; by definition

**(1.3)** `z_S>0` componentwise.

T-P5-171 gives the orthant complementarity conclusion

**(1.4)** `Mz>=0`,

**(1.5)** `(Mz)_i=0` for every `i in S`,

hence

**(1.6)** `A z_S=0`.

The first new point is that `A` is not merely copositive: the existence of an **interior** zero contact in the support forces ordinary PSD.

---

## 2. A positive-support zero contact forces the active principal block to be PSD

### Theorem T173-A — `copositive_zero_contact_active_principal_psd`

Under (1.1)-(1.6),

**(2.1)** `A >= 0` in the ordinary PSD sense:

`y^T A y >=0` for every real vector `y` on `S`.

### Proof

Fix any real `y` on `S`.

Because `z_S>0` and `S` is finite, choose `c>0` large enough that both

`c z_S + y >=0`

and

`c z_S - y >=0`

componentwise. Pad either vector by zero outside `S`; copositivity of `M` gives nonnegative quadratic value.

Using `A z_S=0` and `z_S^T A z_S=0`, exact expansion gives

`q_A(c z_S + y) = y^T A y`,

and similarly

`q_A(c z_S - y) = y^T A y`.

Therefore `y^T A y>=0` for arbitrary real `y`. QED.

### Consequence

At every positive-support sharp contact, the active face is an ordinary semidefinite face even when the full matrix is copositive but indefinite.

This matters because the active support may now use exact PSD/corank-one algebra without incorrectly upgrading the **whole** matrix to PSD.

---

## 3. Corank-one contact: one adjugate column is a positive kernel witness

Assume now that the active block `A` is singular and has corank one.

Equivalently in a checker-friendly form, it is enough to know

**(3.1)** `det(A)=0`

and that one diagonal cofactor is positive.

Fix an active anchor `a in S`. Let `e_a` denote the coordinate basis vector in the ordered active block and define

**(3.2)** `w := adj(A) e_a`.

The adjugate identity gives

**(3.3)** `A w = det(A) e_a = 0`.

The anchor entry is

**(3.4)** `w_a = Cof_{a,a}(A)`.

### Theorem T173-B — `positive_adjugate_column_of_corank_one_contact`

Suppose `A` is PSD, `rank(A)=|S|-1`, and `z_S>0` spans `ker(A)`. Then every anchor `a in S` satisfies

**(3.5)** `Cof_{a,a}(A)>0`,

and the adjugate column is a positive multiple of the contact:

**(3.6)** `w = c_a z_S` for some `c_a>0`.

Hence

**(3.7)** `w_i>0` for every `i in S`.

### Proof

Because `A` is PSD of rank `|S|-1`, every principal cofactor is nonnegative and at least one is nonzero. The kernel is one-dimensional and spanned by the strictly positive vector `z_S`.

For any anchor with `w!=0`, (3.3) forces `w=c z_S`. Since `w_a=Cof_{a,a}(A)>=0` and `z_a>0`, nonzero implies `c>0`, so the entire column is positive.

In fact in the corank-one PSD case every diagonal cofactor is positive: deleting any one coordinate from a one-dimensional kernel generated by a vector whose deleted coordinate is nonzero leaves a nonsingular principal compression. Since every coordinate of `z_S` is positive, this applies to every anchor. QED.

### More checker-oriented variant

A producer does not need to submit a rank integer. The following finite gates suffice:

- `det(A)=0`;
- choose one anchor `a`;
- submit `w_i=Cof_{a,i}(A)>0` for all active `i`.

Then `w!=0`, so `adj(A)!=0`; together with `det(A)=0`, this forces `rank(A)=|S|-1`. Equation `Aw=0` follows from the adjugate identity, and `w>0` is explicit.

Thus the corank-one positive contact can be represented with determinants only: no inverse, pseudoinverse, square root, eigenvector, or normalization is required.

---

## 4. Every inactive KKT residual is a row-replacement determinant

Let `j notin S` be an inactive coordinate. Define the inactive residual of the adjugate contact by

**(4.1)**

`h_j := M[j,S] w`.

Because `w>0` and `Aw=0`, padding `w` by zero outside `S` gives a zero contact of `M`. If `M` is copositive, T-P5-171 implies `h_j>=0` automatically.

Strict complementarity at inactive coordinate `j` is exactly

**(4.2)** `h_j>0`.

Now let `A^{a<-j}` be the square matrix obtained from `A` by replacing active row position `a` by the row `M[j,S]`, **without changing the column order**.

### Theorem T173-C — `inactive_residual_eq_row_replacement_det`

**(4.3)**

`h_j = det(A^{a<-j})`.

### Proof

Expand `det(A^{a<-j})` along the replaced row. The cofactors of that row depend only on the undeleted rows and columns, which are identical to those of `A`. Therefore

`det(A^{a<-j})`
`= sum_{i in S} M[j,i] Cof_{a,i}(A)`
`= M[j,S] adj(A)e_a`
`= M[j,S]w`
`= h_j`.

QED.

### Important sign convention

There is no hidden permutation sign if the checker literally constructs the active ordered matrix and replaces row **position** `a` by the inactive row. If instead it sorts the new row-index set after replacement, the induced permutation sign must be tracked explicitly.

This row-position formulation is therefore the safer theorem/checker interface.

---

## 5. Exact determinant-only strict-complementarity certificate

The previous sections give a compact exact certificate.

### Theorem T173-D — `strict_complementarity_from_contact_minors`

Let `M` be symmetric and copositive. Fix an ordered nonempty active set `S` and an anchor position `a`. Put `A=M[S,S]`.

Assume:

1. **contact determinant**
   `det(A)=0`;

2. **positive adjugate column**
   `Cof_{a,i}(A)>0` for every `i in S`;

3. **strict inactive row-replacement minors**
   `det(A^{a<-j})>0` for every `j notin S`.

Define

`w_i := Cof_{a,i}(A)`.

Then:

**(5.1)** `w>0`;

**(5.2)** `Aw=0`;

**(5.3)** the padded vector `x=pad_S(w)` is a nonzero zero contact of `M`;

**(5.4)** `(Mx)_i=0` for `i in S`;

**(5.5)** `(Mx)_j>0` for `j notin S`.

Thus `x` satisfies orthant KKT with **strict complementarity** on every inactive coordinate.

Moreover `adj(A)!=0`, so the active block is automatically corank one.

### Proof

(5.1) is assumption 2. The adjugate identity plus `det(A)=0` gives (5.2). Hence `x^T M x=w^T A w=0`, proving (5.3). Active residuals vanish by `Aw=0`. Inactive residuals are exactly the row-replacement determinants by T173-C, and assumption 3 makes them strictly positive. QED.

### Why the global copositivity PASS stays separate

The determinant gates construct a strict orthant-KKT zero contact, but by themselves do **not** prove the entire matrix copositive. A saddle matrix can possess such a stationary cone point while failing elsewhere.

Therefore the intended composition is:

- T-P5-170/155/157/158/161 or another exact route proves fixed-candidate copositivity;
- T-P5-173 identifies a strict corank-one contact at that same candidate;
- T-P5-169/T-P5-159 consume the contact for sharp-floor localization.

No gate is silently promoted across layers.

---

## 6. Rank-two P5 floor pencil: every strict-complementarity gate has degree at most two

Now specialize to the P5 additive-floor pencil

**(6.1)**

`M_D = M_0 + D L_g`,

where

`L_g=(g 1^T + 1 g^T)/2`

has rank at most two.

T-P5-172 proves that **every square minor** of `M_D`, principal or non-principal, is a polynomial in `D` of degree at most two.

Apply that theorem to the T-P5-173 gates.

### Active kernel coordinates

For fixed active support `S` and anchor `a`,

**(6.2)**

`w_i(D)=Cof_{a,i}(A_D)`

is, up to the fixed cofactor sign `(-1)^{a+i}`, a square minor of `M_D`. Hence

**(6.3)** `deg_D w_i <= 2`.

### Inactive strict-complementarity residuals

For `j notin S`,

**(6.4)**

`h_j(D)=det(A_D^{a<-j})`

is itself a square row/column minor of `M_D` with fixed order. Hence

**(6.5)** `deg_D h_j <=2`.

### Contact determinant

Likewise

**(6.6)** `p_S(D)=det(A_D)`

has degree at most two.

### Consequence

The complete nondegenerate contact certificate at symbolic floor parameter `D` is therefore a finite system consisting only of:

- one quadratic equality `p_S(D)=0`;
- finitely many quadratic strict inequalities `w_i(D)>0`;
- finitely many quadratic strict inequalities `h_j(D)>0`.

No recursive reduced-matrix polynomial degree appears.

This is the strict-complementarity analogue of T-P5-172's symbolic pivot corridor.

---

## 7. Root-free certification at an irrational sharp floor

The previous polynomial degree bound removes the need to represent an algebraic contact root.

Let `[L,U]` be a rational interval. Suppose a separate exact root-isolation gate proves that the contact determinant `p_S(D)` has a unique root

`D_* in [L,U]`.

Suppose further that exact rational quadratic interval checks prove, **throughout the whole interval**,

**(7.1)** `w_i(D)>0` for every active `i`,

and

**(7.2)** `h_j(D)>0` for every inactive `j`.

Then evaluating at the unknown root `D_*` gives every T173-D gate except the separate fixed-candidate copositivity PASS.

Therefore:

### Theorem T173-E — `strict_contact_at_isolated_root_without_root_representation`

If

- `p_S` has a unique root `D_*` in a rational interval `[L,U]`;
- all active cofactor-column quadratics are strictly positive on `[L,U]`;
- all inactive row-replacement quadratics are strictly positive on `[L,U]`;
- `M_{D_*}` is separately certified copositive;

then `D_*` has a strict corank-one contact on support `S`, even if `D_*` is irrational and is never represented inside the certificate.

T-P5-172 already supplies a root-free interval checker for quadratic sign conditions using rational endpoints, derivative signs, and `4ac-b^2`. The present child only identifies the correct strict-contact polynomials to feed into that checker.

### Practical consequence

A symbolic floor packet may contain only:

- rational coefficients of `p_S,w_i,h_j`;
- rational isolating endpoints `L,U`;
- exact interval-sign certificates;
- fixed-candidate copositivity evidence from the existing cone chain.

It need not contain:

- `sqrt(discriminant)`;
- an algebraic-number object for `D_*`;
- a normalized nullvector;
- a pseudoinverse;
- a floating eigenvector or KKT solve.

---

## 8. Exact irrational-root regression in the actual P5 floor form

Take three vertices with

`g=(1,2,1)`

and pair data

`K_12=-1`, `K_13=1`, `K_23=1`.

The P5 floor matrix is

`M_D[ii]=D g_i`,

`M_D[i,j]=(K_ij + D(g_i+g_j))/2` for `i!=j`.

Choose active support `S={1,2}`. Then

`A_D = [[D, (-1+3D)/2],
        [(-1+3D)/2, 2D]]`.

Its determinant is

**(8.1)**

`p(D)=(-D^2+6D-1)/4`.

The smaller root is algebraically `3-2 sqrt(2)`, but the certificate never needs that expression.

### Rational root isolation

At rational endpoints,

`p(1/6)=-1/144 <0`,

`p(1/5)=1/25 >0`.

Also

`p'(D)=(3-D)/2 >0`

on `[1/6,1/5]`. Hence there is exactly one root

**(8.2)** `D_* in (1/6,1/5)`.

### Positive adjugate column

Use anchor `a=1`. Then

**(8.3)**

`w(D)=adj(A_D)e_1
     =(2D, (1-3D)/2)`.

On `[1/6,1/5]`, both coordinates are strictly positive:

`2D >=1/3>0`,

`(1-3D)/2 >=1/5>0`.

Thus the root contact is positive and corank one.

### Strict inactive residual

The inactive row is

`M_D[3,S]=((1+2D)/2, (1+3D)/2)`.

The row-replacement determinant / inactive residual is

**(8.4)**

`h_3(D)=(-D^2+4D+1)/4`.

On `[1/6,1/5]`, its derivative `(2-D)/2` is positive, so

`h_3(D) >= h_3(1/6)=59/144>0`.

Thus strict complementarity is certified on the entire rational isolating interval.

### Full copositivity at the root

At `D_*<1/5<1/3`, the active off-diagonal `(-1+3D_*)/2` is negative. The active block has positive diagonal and zero determinant, hence is PSD rank one. The two couplings from vertex 3 to the active support are strictly positive, and `M_33=D_*>0`. Therefore for `x>=0`,

`x^T M_{D_*}x`

is the sum of the nonnegative active PSD quadratic, a nonnegative `x_3^2` term, and nonnegative cross terms from vertex 3. Hence `M_{D_*}` is copositive.

For `D<D_*` sufficiently near the root, the same positive active contact direction has negative energy because the floor loading contributes

`(D-D_*) (1^T w)(g^T w)<0`.

So this is a genuine sharp irrational floor with a root-free strict-complementarity certificate.

The local SymPy exact-rational regression used only the identities

`det(A_D)=(-D^2+6D-1)/4`,

`h_3(D)=(-D^2+4D+1)/4`.

No numerical root was used as evidence.

---

## 9. Corank-one is essential for the adjugate-column interface

The strict contact itself does **not** force corank one.

Consider

`M = [[0,0,1],
      [0,0,1],
      [1,1,1]]`.

For every `x>=0`,

`x^T M x = 2 x_3(x_1+x_2)+x_3^2 >=0`,

so `M` is copositive.

Take

`z=(1,1,0)`.

Then

`q_M(z)=0`,

and

`Mz=(0,0,2)`.

Thus `S={1,2}` is a strict contact: the inactive residual is `2>0`.

But

`A=M[S,S]=0_{2x2}`

has corank two and

`adj(A)=0`.

Therefore every adjugate-column/cofactor witness vanishes even though a strict positive-support contact exists.

### Fail-closed conclusion

If all candidate adjugate columns vanish, the checker must **not** report absence of strict contact. It may report only

`CORANK_ONE_MINOR_GATE_NOT_APPLICABLE`.

The higher-corank branch needs an explicit exact kernel basis and a separate cone/LP feasibility problem for

- a positive vector `w in ker(A)`,
- strict inactive residuals `M[j,S]w>0`.

That branch is intentionally not solved here and should not be hidden behind a pseudoinverse.

---

## 10. Strict sign is essential for support isolation

Nonnegative inactive residuals are guaranteed by copositivity, but replacing `>0` by `>=0` loses strict-complementarity information.

Consider

`M = [[1,-1,0],
      [-1,1,0],
      [0,0,0]]`.

This matrix is PSD, hence copositive. The contact

`z=(1,1,0)`

has active support `{1,2}` and zero inactive residual at coordinate 3.

But in fact

`(1,1,t)`

is a zero contact for every `t>=0`.

So the support `{1,2}` is not isolated at all; it can enlarge continuously.

Therefore any statement such as “the sharp contact has stable/identified inactive set” must use **strict** row-replacement minors. A zero minor is a genuine degeneracy boundary, not a harmless equality case.

---

## 11. Formalization-ready theorem statements

The useful Lean split is small and does not need a global algebraic-number layer.

### T173-L1 — active-face PSD

`copositive M -> x>=0 -> x^T M x=0 -> S=support_pos x -> IsPSD (M[S,S])`.

The proof should use the interior-of-support perturbation argument plus T-P5-171's active kernel equation.

### T173-L2 — adjugate kernel column

For square `A` and anchor `a`:

`det A=0 -> A *ᵥ (adjugate A *ᵥ e_a)=0`.

Then a finite-coordinate positivity wrapper turns positive cofactors into a positive kernel vector and infers corank one from `adj(A)!=0`.

### T173-L3 — row replacement

`det (replaceRow A a r) = dotProduct r (adjugate A *ᵥ e_a)`.

This is pure determinant expansion and should be proved with a fixed row position, not sorted index sets.

### T173-L4 — strict contact from minors

Assuming a separate `Copositive M` premise:

- `det A=0`;
- every selected cofactor in one adjugate column is positive;
- every inactive row-replacement determinant is positive;

imply the padded cofactor vector is a strict orthant-KKT zero contact.

### T173-L5 — rank-two floor specialization

Reuse T-P5-172's arbitrary-square-minor degree-`<=2` theorem to show:

- active cofactors are quadratic in `D`;
- inactive row-replacement determinants are quadratic in `D`.

Do **not** re-expand recursive Schur matrices.

---

## 12. Integration guidance

The intended dispatch/checker order for a candidate sharp floor is now:

1. use T-P5-169 to localize the winning negative component when available;
2. use T-P5-170/T-P5-172 to establish a fixed-candidate copositivity corridor and isolate a candidate contact root;
3. choose an active support `S` and one anchor `a`;
4. evaluate only the original-minor polynomials `p_S(D)`, `w_i(D)`, `h_j(D)`;
5. certify `p_S=0` at the isolated root and strict positivity of every `w_i,h_j` on the rational isolating interval;
6. obtain a strict corank-one KKT contact without any algebraic root or nullvector object;
7. if the adjugate column vanishes, fail closed into a higher-corank kernel-basis branch rather than declaring failure of copositivity or strict contact.

This closes the strict-complementarity seam left explicit by T-P5-171 in the generic nondegenerate branch.

---

## 13. Admission boundary

This review establishes only finite-dimensional exact mathematics.

It does **not** establish:

- that the actual P5 source packet supplies a particular `{g_i,K_ij}` pencil;
- that a particular support `S` is reached by the deployed source/coverage semantics;
- Float64/libm/directed-rounding correctness;
- any Lean/kernel receipt;
- independent verification by 封不觉;
- registry/admission eligibility;
- P5/P8/M4 parent closure.

Final status remains

**`CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding`.**