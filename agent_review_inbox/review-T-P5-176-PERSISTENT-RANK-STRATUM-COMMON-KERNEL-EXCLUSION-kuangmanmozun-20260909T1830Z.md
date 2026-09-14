---
kind: review_result
review_id: review-T-P5-176-persistent-rank-stratum-common-kernel-exclusion-kuangmanmozun-20260909T1830Z
task_id: T-P5-176-PERSISTENT-RANK-STRATUM-COMMON-KERNEL-EXCLUSION
reviewer: 狂蛮魔尊
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-09T18:30:00Z
claim_commit: d451f820cd30695a87c96edd7668dc0efee40987
inspected_commit: 325c862fb0a7906038fc1759d616b4693c9b2d27
upstream_commits:
  - e40396a17005bd9c5914adf7af140d6e60c03d1d  # T-P5-175 isolated high-corank algebraic contact bridge
  - 09a09a9df2b409fedc2cac32ad483e6baa005e5c  # T-P5-174 high-corank kernel-cone strict contact
  - 1b63698a429d0b2530de38e6632d29076b52e475  # T-P5-173 corank-one strict-complementarity minors
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: close_T175_persistent_high_corank_physical_contact_branch; add_psd_persistent_rank_common_kernel_lemma; specialize_to_nontrivial_floor_loading; route_all_physical_high_corank_contacts_to_T175_isolated_packet
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact block-rank / Schur-complement algebra; exact bordered-minor coefficient argument; exact SymPy rational regression for Sections 7-9
exit_code: 0 for exact symbolic regressions; no Lean/kernel run
---

# T-P5-176 — persistent rank stratum common-kernel exclusion

## 0. Verdict and closed seam

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-175 closes an isolated high-corank active contact by showing that the relevant floor is rational or quadratic algebraic and by constructing a fraction-free root-free contact packet. Its explicit Boundary A leaves open the case in which every rank-detecting `(r+1)` minor vanishes identically, so the active rank defect persists for the whole affine parameter family.

For the P5 additive-floor pencil, that persistent branch is not merely another difficult algebraic-number case. Under the physical contact hypotheses it is **empty**.

The key structural lemma is:

> If a real symmetric affine pencil `A_s=A+sL` has `A>=0`, `rank(A)=r`, and `rank(A_s)<=r` for every `s` in a neighborhood of zero (equivalently, all `(r+1)` minors vanish identically for the polynomial pencil), then every vector in `ker(A)` is also in `ker(L)`.

Thus a PSD rank defect that persists under a symmetric affine perturbation cannot have a moving kernel. The kernel is a common invariant nullspace of both the base matrix and the loading direction.

For the P5 loading

`L_g = (g 1^T + 1 g^T)/2`,

if the restricted loading vector `g` is nonzero, `ker(L_g)` contains **no nonzero nonnegative vector**. Therefore a nonzero physical orthant contact can never lie on a persistent rank stratum.

Consequently, at the actual rank of every physical positive-support zero contact with nontrivial P5 loading, **some `(r+1)` minor must be a nonzero polynomial**. Hence the contact rank drop is isolated and T-P5-175 always applies. The persistent high-corank branch left open there can be deleted from the physical contact decision tree, while remaining as a generic affine-pencil phenomenon outside the PSD/nontrivial-loading hypotheses.

No source binding, runtime/Float64 claim, global copositivity proof, Lean/kernel validation, independent validation, registry mutation, or parent closure is performed.

---

## 1. General affine symmetric pencil

Let `V` be a finite-dimensional real inner-product space and let

`A=A^T`, `L=L^T`.

Consider

`A_s := A + s L`.

Assume

1. `A >= 0`;
2. `rank(A)=r`;
3. `rank(A_s) <= r` for all `s` in some open interval containing `0`.

For a polynomial affine pencil, assumption 3 is equivalent to saying that every `(r+1)x(r+1)` minor polynomial vanishes identically: if it vanishes on an open interval, it is the zero polynomial; conversely zero minors force the rank bound for all real `s`.

Let

`K := ker(A)`.

Because `A>=0`,

`V = range(A) orthogonal_sum K`,

and `A` is positive definite on `range(A)`.

Choose an orthonormal basis adapted to this decomposition. Then

`A = [[C,0],[0,0]]`,

with `C>0` an `r x r` matrix, while

`L = [[E,F],[F^T,G]]`.

The theorem is that necessarily

`F=0`, `G=0`.

Equivalently,

`L K = {0}`.

---

## 2. T176-A — persistent PSD rank defect forces a common kernel

### Theorem `persistent_psd_rank_defect_common_kernel`

Under the hypotheses of Section 1,

`ker(A) subseteq ker(L)`.

Hence

`ker(A_s) superseteq ker(A)`

for every real `s`.

If in addition `rank(A_s)=r` at some `s`, then

`ker(A_s)=ker(A)`.

### Proof by exact rank / Schur complement

For sufficiently small `s`, the pivot block

`C_s := C+sE`

remains invertible. Write

`A_s = [[C_s, sF],[sF^T, sG]]`.

Because the upper-left block has rank `r`, the full matrix has rank at most `r` iff its Schur complement is exactly zero:

`S(s) = sG - s^2 F^T C_s^{-1} F = 0`.

For nonzero small `s`, divide by `s`:

`G - s F^T C_s^{-1}F = 0`.

Letting `s -> 0` gives

`G=0`.

Substituting this back yields

`F^T C_s^{-1}F=0`

for all sufficiently small nonzero `s`. Passing to `s=0`,

`F^T C^{-1}F=0`.

Since `C>0`, also `C^{-1}>0`, so for every vector `u`,

`u^T F^T C^{-1}F u = (Fu)^T C^{-1}(Fu) = 0`

implies `Fu=0`. Thus `F=0`.

Therefore

`L = [[E,0],[0,0]]`

in the range/kernel splitting, so `Lz=0` for every `z in K`. QED.

### Why PSD is doing real work

The conclusion is false for a general indefinite singular pencil; Section 8 gives a rank-two symmetric pencil with a genuinely moving kernel. The positive definiteness of `C^{-1}` is what kills the second-order cross block `F`.

---

## 3. Division-free bordered-minor proof

The same theorem can be expressed without treating an inverse as trusted data.

In the range/kernel basis, take any kernel indices `a,b`. Because every `(r+1)` minor of `A_s` vanishes, the bordered minor

`q_ab(s) = det [[C+sE, s f_b], [s f_a^T, s g_ab]]`

is the zero polynomial, where `f_a,f_b` are columns of `F` and `g_ab` is the `(a,b)` entry of `G`.

Using the exact adjugate determinant identity,

`q_ab(s) = s g_ab det(C+sE) - s^2 f_a^T adj(C+sE) f_b`.

The coefficient of `s` is

`g_ab det(C)`.

Since `det(C)>0`, polynomial identity forces

`g_ab=0`

for every `a,b`. Hence `G=0`.

Now take `a=b`. With `g_aa=0`,

`q_aa(s) = -s^2 f_a^T adj(C+sE) f_a`.

The coefficient of `s^2` is

`- f_a^T adj(C) f_a`.

Because `C>0`,

`adj(C)=det(C) C^{-1}>0`.

Therefore the zero-polynomial condition gives

`f_a=0`

for every kernel coordinate `a`, so `F=0`.

This is the preferred formalization path if the implementation wants determinant/cofactor identities only. It requires no eigenvectors, square roots, pseudoinverses, or numerical limiting argument.

---

## 4. T176-B — the persistent kernel is a rational common subspace

Now return to the original affine parameterization

`A_D = A_0 + D L`,

where `A_0,L` have rational entries.

Let `alpha` be any real parameter with

`A_alpha >= 0`, `rank(A_alpha)=r`,

and suppose the actual-rank stratum is persistent:

`rank(A_D)<=r` for all `D`.

Apply T176-A after shifting `s=D-alpha`. It gives

`ker(A_alpha) subseteq ker(L)`.

For `z in ker(A_alpha)`,

`0=A_alpha z=A_0 z+alpha Lz=A_0 z`.

Hence

`ker(A_alpha) subseteq ker(A_0) intersect ker(L)`.

The reverse inclusion is automatic, because a common kernel vector is killed by every `A_D`, in particular by `A_alpha`. Therefore

**(4.1)** `ker(A_alpha) = ker(A_0) intersect ker(L)`.

This is stronger than merely saying the kernel is locally constant. It says the persistent candidate kernel is an **alpha-independent rational subspace** determined by the two rational matrices already present in the source packet.

Thus, if a generic checker ever needs to inspect a persistent PSD stratum, it can compute the common kernel by exact rational row reduction on the stacked system

`A_0 z=0`, `Lz=0`.

No algebraic-number representation of `alpha` is required.

---

## 5. P5 loading geometry

For the additive floor matrix of T-P5-154/159, the active loading direction is

`L_g := (g 1^T + 1 g^T)/2`.

Here `1` is the all-ones vector on the active support and `g` is the corresponding vector of floor weights.

For any vector `z`,

**(5.1)** `2 L_g z = g (1^T z) + 1 (g^T z)`.

The following elementary fact is the decisive physical exclusion.

### Theorem T176-C — `floor_loading_kernel_has_no_nonnegative_ray`

Assume `g != 0`. Then

`ker(L_g) intersect {z >= 0} = {0}`.

### Proof

Suppose `z>=0`, `z!=0`, and `L_g z=0`. Let

`s:=1^T z`.

Because `z` is nonzero and nonnegative,

`s>0`.

Let

`t:=g^T z`.

Equation (5.1) gives

`s g + t 1 = 0`,

so

`g=-(t/s)1`.

Taking the dot product with `z` gives

`t = g^T z = -(t/s)(1^T z) = -t`.

Hence `t=0`, and therefore `g=0`, contradicting the hypothesis. QED.

### Stronger-than-positive-weight observation

The theorem does not require every `g_i>0`; it only requires that the restricted loading vector is not identically zero. In the actual P5 use case the weights are positive, so the gate is automatically satisfied on every nonempty support.

---

## 6. T176-D — persistent physical contact is impossible

Combine T176-A and T176-C.

### Theorem `persistent_floor_rank_stratum_excludes_orthant_contact`

Let

`A_D = A_0 + D L_g`

be an active principal block of the P5 additive-floor pencil. Assume at a candidate `alpha`:

1. `A_alpha >= 0`;
2. `rank(A_alpha)=r<m`;
3. every `(r+1)` minor polynomial of `A_D` vanishes identically, equivalently `rank(A_D)<=r` for all `D`;
4. the restricted loading vector `g` is nonzero.

Then

`ker(A_alpha) intersect R_{≥0}^m = {0}`.

In particular there is no nonzero nonnegative zero-energy contact, and therefore no strict positive-support contact.

### Proof

T176-A gives

`ker(A_alpha) subseteq ker(L_g)`.

T176-C says the latter kernel contains no nonzero nonnegative vector. QED.

### Physical route through copositivity

T-P5-173 proves that if a globally copositive candidate has a zero contact whose active coordinates are strictly positive on support `S`, then its active block is ordinary PSD. Therefore every physical zero contact enters the premises of T176-D automatically at its active support, provided the P5 loading is nontrivial there.

So this is not an extra artificial PSD assumption in the intended route; it is already supplied by the contact geometry.

---

## 7. T176-E — every physical contact rank drop is isolated

Fix a physical positive-support zero contact at `D=alpha`, and let

`r := rank(A_alpha)`

be its **actual** active rank.

There are exactly two algebraic possibilities for the `(r+1)` minors of the affine pencil:

1. at least one is a nonzero polynomial;
2. all are identically zero.

Case 2 is impossible by T176-D.

Therefore case 1 must hold.

By T-P5-172/T-P5-175, every such minor has degree at most two in `D`. Since it vanishes at `alpha`, the candidate is isolated in the rank-`<=r` locus and `alpha` is rational or quadratic algebraic.

Hence the T-P5-175 physical routing can be sharpened to:

> **For nontrivial P5 floor loading, every physical high-corank contact is isolated and admits the T-P5-175 root-free rational-polynomial packet. There is no separate persistent physical-contact branch.**

This also handles the “further rank drop inside a persistent coarser stratum” caveat from T-P5-175 Boundary B: simply recompute `r` as the candidate's actual rank. If the next-size minors are all identically zero, T176-D excludes the contact; otherwise the lower-rank point is isolated and T-P5-175 applies at that actual rank.

---

## 8. Exact P5 regression: positive contact is isolated

Take the two-vertex P5 active pencil

`A_D = [[D, D-1], [D-1, D]]`.

This has loading vector

`g=(1,1)`,

because

`L_g=[[1,1],[1,1]]`.

At

`alpha=1/2`,

`A_alpha = [[1/2,-1/2],[-1/2,1/2]] >= 0`,

with

`ker(A_alpha)=span{(1,1)}`.

Thus `(1,1)>0` is a genuine positive zero-energy contact.

The determinant is

`det(A_D)=2D-1`,

so the rank drop is isolated exactly as T176 predicts. The loading acts nontrivially on the contact:

`L_g(1,1)^T=(2,2)^T !=0`,

which is why the kernel cannot persist away from `D=1/2`.

This is a minimal rational regression of the full physical mechanism.

---

## 9. Counterexample: PSD is essential

A persistent symmetric singular pencil can have a moving kernel if the PSD contact hypothesis is removed.

Take

`A_D = [[0,0,-D], [0,0,1], [-D,1,0]]`.

Its determinant is identically zero and its rank is exactly two for every real `D`.

Its kernel is

`ker(A_D)=span{(1,D,0)}`,

which genuinely moves with `D`; there is no nonzero common kernel over all parameters.

At `D=0`,

`A_0=[[0,0,0],[0,0,1],[0,1,0]]`

has eigenvalues `1,-1,0`, so it is indefinite.

Therefore the common-kernel conclusion must not be generalized to arbitrary symmetric constant-rank pencils. The PSD premise is exactly what eliminates the singular Kronecker/moving-kernel behavior.

---

## 10. Counterexample: nontrivial loading is essential for the orthant exclusion

If the active loading is identically zero, a persistent PSD positive contact can exist.

Take

`g=0`, so `L_g=0`,

and the constant pencil

`A_D=[[1,-1],[-1,1]]`.

It is PSD of rank one for every `D`, and

`A_D(1,1)^T=0`

with `(1,1)>0`.

Thus T176-C/T176-D must retain the condition that the restricted loading vector is nonzero. In the deployed P5 floor family, positive floor weights make this condition automatic.

---

## 11. Root-free checker consequences

The persistent branch can now be handled before any algebraic root construction.

At a proposed active support `S` and actual rank `r`:

1. Form the degree-`<=2` `(r+1)` rank-detecting minors from T-P5-172.
2. If some minor is a nonzero polynomial, route to T-P5-175.
3. If all are identically zero, this is a persistent rank stratum.
4. If the candidate active block is PSD and the restricted P5 loading `g_S !=0`, return
   `PERSISTENT_PHYSICAL_CONTACT_IMPOSSIBLE`.
5. A generic/debug checker may additionally compute the exact rational common kernel
   `ker(A_0[S,S]) intersect ker(L_{g_S})`; no algebraic parameter is needed.

The producer does not need to provide:

- a Grassmannian path;
- an algebraic kernel basis depending on `D`;
- a pseudoinverse;
- an eigenvector/eigenspace continuation;
- a square root;
- floating rank tracking.

The entire physical persistent branch reduces to exact polynomial-zero tests plus the structural theorem above.

---

## 12. Minimal formalizable theorem packet

### T176-A — persistent PSD rank defect common kernel

For symmetric finite matrices `A,L`, if

`A>=0`, `rank(A)=r`, and `rank(A+sL)<=r` on a neighborhood of `0`,

then

`ker(A) subseteq ker(L)`.

A determinant-only proof may use an adapted range/kernel basis and the coefficients of the bordered minors.

### T176-B — rational common-kernel identity

For rational `A_0,L`, if `A_alpha=A_0+alpha L` satisfies T176-A's persistent hypotheses, then

`ker(A_alpha)=ker(A_0) intersect ker(L)`.

### T176-C — P5 loading orthant exclusion

For `L_g=(g1^T+1g^T)/2` with `g!=0`,

`L_g z=0`, `z>=0` implies `z=0`.

### T176-D — persistent physical contact exclusion

Under T176-A plus nontrivial P5 loading, a PSD persistent rank stratum has no nonzero nonnegative kernel contact.

### T176-E — physical rank-drop isolation

At the actual rank of every physical P5 positive-support zero contact, at least one next-size minor polynomial is nonzero; by T-P5-172 its degree is at most two, hence T-P5-175's isolated root-free packet is complete for the high-corank contact route.

---

## 13. Boundaries and fail-closed conditions

### Boundary A — global copositivity remains separate

T176 uses the PSD active block supplied by the contact branch. It does not certify full-matrix copositivity. Global PASS remains a separate T-P5-158/165/168/170-style obligation.

### Boundary B — loading must be nontrivial on the chosen support

Use `g_S !=0`, not merely a global `g!=0`, if some coordinates are allowed to have zero floor weight. If `g_S=0`, the persistent-contact exclusion does not apply.

### Boundary C — PSD cannot be weakened to symmetry

Section 9 gives an exact moving-kernel counterexample.

### Boundary D — approximate rank persistence is not enough

The theorem consumes exact rank persistence / identically-zero minors. A small determinant or numerically stable rank does not justify common-kernel transport.

### Boundary E — source/runtime/formal gates stay open

Actual `{g_i,K_ij,D}` source equality, same-key simplex semantics, cell/coverage, Float64/reification, ODE/P8/M4 semantics, Lean/kernel compilation, independent validation by 封不觉, admission, registry mutation, and parent closure all remain open.

---

## 14. Routing recommendation

Replace the T-P5-175 contact decision tree

- corank one;
- isolated corank >=2;
- persistent corank >=2 open

by the following physical P5 tree:

1. **corank one:** T-P5-173 fast adjugate/minor gates;
2. **corank >=2 with a nonzero next-size minor:** T-P5-175 fraction-free isolated algebraic packet;
3. **all next-size minors identically zero:** under PSD contact + nontrivial floor loading, reject the branch as `PERSISTENT_PHYSICAL_CONTACT_IMPOSSIBLE` by T176;
4. keep generic persistent affine-pencil logic only for nonphysical/debug situations where PSD or loading hypotheses are absent.

The main structural conclusion is:

> **A persistent symmetric rank defect can move only by exploiting indefinite geometry. Once the candidate active block is PSD, persistence freezes its kernel; the P5 rank-two floor loading then forbids that frozen kernel from containing any physical orthant contact.**
