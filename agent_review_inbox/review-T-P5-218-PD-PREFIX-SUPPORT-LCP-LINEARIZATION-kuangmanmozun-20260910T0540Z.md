---
kind: review_result
review_id: review-T-P5-218-pd-prefix-support-lcp-linearization-kuangmanmozun-20260910T0540Z
task_id: T-P5-218-PD-PREFIX-SUPPORT-LCP-LINEARIZATION
reviewer: 狂蛮魔尊
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-10T05:40:00Z
claim_commit: 2afc6b7a731845b6fe0f5785ce0b41dedd5dd0bf
inspected_commit: ac51da9bfa8bab550ed0ed66a9224590d909ffcd
upstream_commits:
  - a81288eb83a2a4e7d3c596893c200dd814197bc0  # T-P5-217 PD-prefix completeness / residual-Farkas family prune
  - 803e7681f61385fee8a9c1c00b97c1d76061ee71  # T-P5-216 minimal-zero atoms
  - 6f8b539f94aba1fcf3a9106a8989ee88e7a1c38b  # T-P5-214 copositive zero-support decomposition
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_fraction_free_pd_prefix_reconstruction_identity; add_cone_local_schur_copositivity; add_support_fixed_zero_lp_equivalence; add_support_farkas_prune; add_schur_corank_atom_gate; add_exact_regressions
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact finite-dimensional block algebra, complementarity, Schur congruence, Farkas alternative, rational regressions; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-218 — PD-prefix support-fixed LCP linearization

## 0. Verdict and exact seam closed

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-217 gives a strong whole-family prune for a positive-definite prefix `T`:

`lambda >= 0`, `C lambda >= 1`, `Hhat lambda >= 0`.

If this relaxation is infeasible, a rational Farkas witness prunes every atom descendant. But T-P5-217 deliberately leaves the feasible case inconclusive because it omits complementarity / zero-energy.

This child closes that mathematical gap at **fixed remaining support** without introducing a quadratic optimizer.

The main result is:

> After eliminating a PD prefix, once the support `J` of the remaining coordinates is fixed, exact zero-descendant existence is a purely linear rational feasibility problem. The quadratic zero condition collapses to a kernel equation on the principal Schur block.

More precisely, for each nonempty `J` in the remaining coordinate set `R`, define the normalized support LP

`Hhat_JJ mu = 0`,

`mu >= 1`,

`C_J mu >= 1`.

Under the inherited assumption that the original symmetric matrix `K` is globally copositive, this LP is feasible **iff** there exists a copositive zero whose support is exactly `T union J` and which is strict-positive on the already chosen prefix `T`.

No off-support residual inequality needs to be added: it follows automatically from global copositivity once the strict-positive support vector and the principal kernel equation are present.

A feasible support LP gives a **minimal-zero atom** exactly when

`rank(Hhat_JJ)=|J|-1`.

Thus the coarse T-P5-217 residual LP can be followed by an exact finite linear disjunction over supports. Each support is either certified by a rational primal vector or rejected by a rational Farkas dual packet. Worst-case support enumeration remains exponential; no polynomial-time claim is made.

No actual same-key P5 matrix/source, selector/cell/tube identity, Float64/interval semantics, Lean/kernel receipt, independent validation, admission, registry mutation, or P5/P8/M4 parent closure is claimed.

---

## 1. Setup and fraction-free notation

Let `K=K^T` be indexed by a disjoint partition `T union R`, and assume

`K = [[A, B], [B^T, D]]`,

with

`A := K_TT > 0`.

Set

`d := det(A) > 0`,

`C := -adj(A) B`,

`Hhat := d D - B^T adj(A) B`.

These are exactly the fraction-free objects used by T-P5-217.

For any `lambda in R^R`, define the reconstructed full vector

`x(lambda) := ( C lambda / d , lambda )`.

Because `A adj(A)=d I`, direct block multiplication gives the key identity

**(I1)** `K x(lambda) = ( 0 , Hhat lambda / d )`.

Consequently

**(I2)** `x(lambda)^T K x(lambda) = lambda^T Hhat lambda / d`.

Both identities are exact and use no inverse in the checker-visible packet.

---

## 2. Cone-local Schur copositivity — do not demand global copositivity of `Hhat`

Define the reconstruction cone

`Gamma_T := { lambda >= 0 : C lambda >= 0 }`.

For `lambda in Gamma_T`, `x(lambda)>=0`. Since the original `K` is assumed copositive,

`0 <= x(lambda)^T K x(lambda)`.

Using (I2) and `d>0`,

**(CONE)** `lambda^T Hhat lambda >= 0` for every `lambda in Gamma_T`.

So `Hhat` is automatically copositive on the **polyhedral reconstruction cone** `Gamma_T`.

This statement is deliberately weaker than ordinary orthant copositivity of `Hhat`, and that distinction is essential.

### Counterexample: Schur block can fail orthant copositivity

Take

`K = [[1,-1,1],[-1,1,1],[1,1,0]]`.

For `x,y,z>=0`,

`[x,y,z] K [x,y,z]^T = (x-y)^2 + 2 z (x+y) >= 0`,

so `K` is copositive.

Choose `T={1}`, `R={2,3}`. Then

`A=[1]`, `d=1`,

`C=[1,-1]`,

`Hhat=[[0,2],[2,-1]]`.

`Hhat` is **not** copositive on the full orthant because

`e_2^T Hhat e_2 = -1`

(where `e_2` denotes the second coordinate in the reduced two-dimensional space).

But the reconstruction cone is

`Gamma_T={ (a,b)>=0 : a-b>=0 }`,

and on that cone

`(a,b)^T Hhat (a,b) = 4ab-b^2 = b(4a-b) >= 3 b^2 >=0`.

Therefore a checker must not reject a valid PD-prefix reduction merely because `Hhat` is indefinite or non-copositive on reduced directions whose reconstructed `T` coordinates would be negative.

---

## 3. Exact fixed-support zero reduction

Fix a nonempty subset

`J subseteq R`.

Let `C_J` denote the columns of `C` indexed by `J`, and let

`H_J := Hhat_JJ`.

### Theorem A — support-fixed zero iff positive Schur-kernel reconstruction

Under global copositivity of `K`, the following are equivalent.

1. There exists `x>=0` with

   `supp(x)=T union J`,

   `x_T>0`, `x_J>0`,

   and

   `x^T K x=0`.

2. There exists `lambda_J>0` such that

   **(A1)** `H_J lambda_J = 0`,

   **(A2)** `C_J lambda_J > 0`.

Here `lambda` is extended by zero outside `J`.

### Proof: zero -> linear kernel system

Let `x` satisfy (1). A nonnegative zero of a copositive symmetric matrix obeys complementarity:

`Kx>=0`,

and every positive coordinate has zero residual.

Since `x_T>0`,

`A x_T + B_J x_J = 0`.

Multiplying by `adj(A)` gives

`d x_T = -adj(A) B_J x_J = C_J x_J`.

Thus with `lambda_J=x_J>0`, condition (A2) holds.

Since `x_J>0`, the residual on `J` also vanishes. Using (I1),

`0=(Kx)_J=H_J lambda_J/d`,

so (A1) holds.

### Proof: linear kernel system -> zero

Conversely assume `lambda_J>0`, `C_J lambda_J>0`, `H_J lambda_J=0`.

Define

`x_T := C_J lambda_J/d`,

`x_J := lambda_J`,

`x_{R\J}:=0`.

Then `x>=0` and its support is exactly `T union J`. Identity (I1) gives zero residual on `T` and on `J`. Identity (I2) gives

`x^T K x = lambda_J^T H_J lambda_J/d = 0`.

Hence `x` is the required nonnegative zero. QED.

### Corollary A1 — inactive residual inequalities are automatic

For the reconstructed zero above, global copositivity implies

`Kx>=0`.

By (I1), therefore

**`Hhat_{R\J,J} lambda_J >=0`.**

So the off-support residual inequality need not be included in the support-fixed primal certificate. It is a theorem consequence, not an independent search variable.

This is exactly where the trusted global-copositivity premise matters.

---

## 4. Homogeneous strict positivity becomes a closed rational LP

The conditions in Theorem A contain strict inequalities. Because the system is homogeneous, they can be normalized without approximation.

### Theorem B — normalized support LP

The system

`lambda_J>0`,

`C_J lambda_J>0`,

`H_J lambda_J=0`

is feasible iff the closed linear system

**(P_J)**

`H_J mu = 0`,

`mu >= 1_J`,

`C_J mu >= 1_T`

is feasible.

### Proof

If the strict system has a solution, let

`m := min( min_j lambda_j , min_i (C_J lambda)_i ) > 0`.

Choose any positive scalar `s>=1/m`. Then `mu=s lambda` satisfies both lower bounds by `1`, while the kernel equality is homogeneous.

The converse is immediate because every coordinate lower-bounded by `1` is strict-positive. QED.

### Rationality

If `K` is rational, then `d`, `C_J`, and `H_J` are rational. The normalized feasible set `(P_J)` is a rational polyhedron intersected with a rational linear subspace. Therefore, whenever it is nonempty, it contains a rational point.

Hence a support-zero witness can be transported as exact rational data; no floating tolerance is mathematically required.

---

## 5. Exact Farkas certificate for rejecting one support

Write `(P_J)` as

`H_J mu=0`,

`[I; C_J] mu >= [1_J;1_T]`.

### Theorem C — support-level Farkas alternative

Exactly one of the following holds.

#### Primal zero-support packet

There exists `mu` satisfying `(P_J)`.

#### Dual support-prune packet

There exist

`y in R^J` free,

`p>=0` in `R^J`,

`q>=0` in `R^T`,

such that

**(C1)** `H_J^T y + p + C_J^T q = 0`,

and

**(C2)** `1^T p + 1^T q > 0`.

The dual may be normalized to

`1^T p + 1^T q = 1`.

### Direct checker proof that the dual prunes

If both primal and dual existed, then

`0 = mu^T(H_J^T y+p+C_J^T q)`

`  = p^T mu + q^T C_J mu`

` >= 1^T p + 1^T q`

` > 0`,

contradiction.

The converse is standard finite-dimensional Farkas separation for linear equalities plus inequalities.

If the coefficients are rational and the primal is infeasible, a rational normalized dual certificate exists.

### Meaning

T-P5-217's whole-family dual `(p,q)` can prune an entire remaining coordinate pool before support branching. T-P5-218's dual is different: it can reject a **specific candidate support** even after the coarse family relaxation passes.

A support-LP miss is therefore a mathematical exclusion for that support, not merely a solver failure, provided the displayed exact dual packet is present.

---

## 6. Minimal-zero atom criterion after the support LP

Let

`S := T union J`.

Suppose `(P_J)` is feasible, so Theorem A produces a strict-positive zero on `S`.

Because `K` is globally copositive, T-P5-214 implies

`K_SS >=0`.

Since `A>0`, standard block congruence gives

`K_SS ~ diag( A, H_J/d )`.

Explicitly, with

`R_J=[[I,-A^{-1}B_J],[0,I]]`,

one has

`R_J^T K_SS R_J = diag(A, H_J/d)`.

Hence

**(CORANK)** `corank(K_SS)=corank(H_J)`.

T-P5-216 characterizes minimal-zero atoms as strict-positive PSD support zeros of corank one. Therefore:

### Theorem D — exact atom gate

A support `S=T union J` carries a minimal-zero atom iff

1. `(P_J)` is feasible, and
2. **`rank(H_J)=|J|-1`**.

Equivalently, `ker(H_J)` is one-dimensional and its ray contains a vector whose reconstructed prefix is strict-positive.

Under the inherited global-copositivity premise, no separate floating PSD/eigenvalue test for `H_J` is needed: feasibility creates a strict-positive zero, global copositivity yields `K_SS>=0`, and the Schur congruence transfers PSD to `H_J`.

If `(P_J)` is feasible but `corank(H_J)>1`, then `S` supports a nonminimal zero cone, not an atom. T-P5-216 says such zeros decompose into smaller minimal atoms.

---

## 7. Exact family statement: the coarse relaxation can be completed by a finite linear disjunction

Let `R` be the remaining coordinate pool after the PD prefix `T`.

### Theorem E — zero-descendant existence

There exists a nonzero copositive zero `x` with

`T subseteq supp(x) subseteq T union R`

and `x_T>0`

iff there exists a nonempty support `J subseteq R` for which `(P_J)` is feasible.

A minimal-zero atom descendant exists iff at least one such `J` also satisfies

`rank(H_J)=|J|-1`.

Thus T-P5-217's coarse residual feasibility packet is an inexpensive convex relaxation, while the exact completion is

`OR_{nonempty J subseteq R} (P_J feasible)`.

Each disjunct is only linear algebra / LP feasibility. The nonconvexity of complementarity is isolated entirely in the finite support choice.

This is an exact semantics for the phrase "after the residual LP passes, inspect complementarity".

---

## 8. Relation to T-P5-217's one-step determinant/cofactor atom gate

Take `J={j}`.

Then `H_J` is the scalar

`Hhat_jj = d K_jj - K_jT adj(A) K_Tj`,

which is exactly T-P5-217's scaled Schur determinant numerator `sigma` for adding `j`.

Also `C_J=-adj(A)K_Tj` is exactly its scaled kernel prefix `u`.

The support LP becomes

`sigma mu=0`,

`mu>=1`,

`u mu>=1`.

Since `mu>0`, this is feasible iff

`sigma=0`

and

`u>0` coordinatewise.

Therefore T-P5-218 strictly generalizes the T-P5-217 singleton-child atom gate to an arbitrary reduced support `J`; it does not alter the earlier theorem.

---

## 9. Regression A — T-P5-217 coarse primal can pass while every zero equation fails

Take the positive-definite matrix

`K=[[1,-1/2],[-1/2,1]]`.

Choose `T={1}`, `R={2}`. Then

`A=[1]`, `d=1`,

`C=[1/2]`,

`Hhat=[3/4]`.

The T-P5-217 coarse primal is feasible: `lambda=2` gives

`C lambda=1`,

`Hhat lambda=3/2>=0`.

But the exact support LP additionally requires

`(3/4) mu=0`,

`mu>=1`,

which is impossible.

An exact normalized T-P5-218 dual prune is

`p=0`, `q=1`, `y=-2/3`.

Indeed

`(3/4)(-2/3)+0+(1/2)(1)=0`,

and `p+q=1`.

So this child removes the false-positive branch left intentionally open by T-P5-217 Regression E.

---

## 10. Regression B — singular Schur block is not enough; reconstruction positivity is essential

Take

`K=[[1,1],[1,1]]`.

This matrix is PSD and hence copositive. With `T={1}`, `J={2}`,

`A=[1]`,

`C=[-1]`,

`H_J=[0]`.

The reduced Schur block has a positive kernel vector `lambda=1`, but

`C lambda=-1<0`.

The reconstructed vector would be `(x_T,x_J)=(-1,1)`, outside the orthant. In fact

`x^T K x=(x_1+x_2)^2`

has no nonzero orthant zero.

Therefore `H_J lambda=0`, even with `lambda>0`, must never be converted into a zero/atom certificate unless `C_J lambda>0` is also checked.

---

## 11. Regression C — a feasible support zero can be higher-corank and therefore nonminimal

Let

`v=(1,-1,-1)`

and

`K=v v^T`

so

`K=[[1,-1,-1],[-1,1,1],[-1,1,1]]`.

`K` is PSD. Choose `T={1}`, `J={2,3}`. Then

`A=[1]`,

`C=[1,1]`,

`H_J=0_{2x2}`.

The normalized support LP is feasible, for example with `mu=(1,1)`:

`H_J mu=0`,

`mu>=1`,

`C mu=2>=1`.

It reconstructs the strict-positive zero

`x=(2,1,1)`.

But

`corank(H_J)=2`,

so this support is not a minimal atom. Indeed it decomposes into the two smaller zero atoms

`(1,1,0)` and `(1,0,1)`.

Thus support-LP feasibility proves a zero support, not minimality; the corank-one gate in Theorem D is essential.

---

## 12. Regression D — inactive residual is genuinely automatic, while global Schur copositivity is false

Return to

`K=[[1,-1,1],[-1,1,1],[1,1,0]]`,

with `T={1}`.

For support `J={2}`, take `lambda=1`. Then

`C_J lambda=1>0`,

`H_J lambda=0`.

The reconstructed zero is

`x=(1,1,0)`.

The remaining inactive residual is

`Hhat_{3,2} lambda=2>=0`,

exactly as Corollary A1 predicts.

At the same time `Hhat` has negative quadratic value on the reduced direction `(0,1)`, which lies outside the reconstruction cone because `C(0,1)=-1`.

This regression simultaneously checks the two boundaries:

- off-support residual nonnegativity follows from the original copositive-zero theorem;
- full-orthant copositivity of the reduced `Hhat` is neither true nor required.

---

## 13. Suggested exact dispatcher after T-P5-217

A safe producer/checker sequence is now:

1. start with a certified globally copositive `K` and a PD prefix `T`;
2. form exact fraction-free `d,C,Hhat`;
3. run T-P5-217 whole-family residual LP;
4. if its normalized Farkas dual exists, prune the entire remaining family;
5. if it passes, do **not** call that an atom;
6. for a selected nonempty support `J`, run `(P_J)`;
7. if `(P_J)` is infeasible, store the normalized support-Farkas dual and reject exactly that support;
8. if `(P_J)` is feasible, reconstruct the exact zero and use `rank(H_J)`:
   - corank `1` -> minimal-zero atom;
   - corank `>1` -> higher-corank zero support, not an atom;
9. feed only genuine minimal atoms into the T-P5-216 compatibility graph / aggregate residual machinery.

The determinant/cofactor branch-and-bound of T-P5-217 remains the preferred cheap atom enumerator. T-P5-218 is the exact **complementarity completion layer** when a producer wants to work in the reduced Schur coordinates after the coarse family LP passes.

---

## 14. Failure / non-FAIL semantics

The following statuses should remain distinct.

- T-P5-217 coarse primal feasible: **INCONCLUSIVE**, not atom PASS.
- `(P_J)` infeasible with exact dual: **ZERO_SUPPORT_J_PRUNED**; not global copositivity FAIL.
- `(P_J)` feasible and `corank(H_J)=1`: **MINIMAL_ZERO_ATOM_J** mathematically, subject to upstream/global/source gates.
- `(P_J)` feasible and `corank(H_J)>1`: **HIGHER_CORANK_ZERO_SUPPORT_NONATOM**.
- `Hhat` not copositive on the full reduced orthant: not a FAIL if the negative directions violate `C lambda>=0`.
- missing trusted global copositivity of `K`: the automatic PSD/residual consequences are unavailable; report **PD_PREFIX_ZERO_REDUCTION_PREMISE_NOT_ESTABLISHED**, not mathematical FAIL.
- floating near-zero rank/determinant only: insufficient for exact atom classification.

---

## 15. Suggested Lean theorem leaves

A formalization can be split into small exact-real leaves.

1. `pdPrefix_fractionFree_reconstruction`
   - prove `K * x(lambda) = (0,Hhat*lambda/d)` from `A*adj(A)=det(A)I`.

2. `pdPrefix_fractionFree_energy`
   - derive `x(lambda)^T K x(lambda)=lambda^T Hhat lambda/d`.

3. `pdPrefix_schur_copositive_on_reconstructionCone`
   - original copositivity plus `lambda>=0`, `C lambda>=0` implies reduced quadratic nonnegativity.

4. `pdPrefix_zeroSupport_iff_positiveKernelReconstruction`
   - Theorem A for a fixed finite support `J`.

5. `positiveKernelReconstruction_implies_inactiveResidual_nonneg`
   - invoke the copositive-zero complementarity theorem.

6. `strictHomogeneousSupportSystem_iff_normalizedLP`
   - Theorem B.

7. `supportLP_dualCertificate_prunes`
   - the direct dot-product contradiction in Theorem C; no general Farkas library theorem is needed to check a supplied dual packet.

8. `supportLP_infeasible_has_dualCertificate`
   - optional finite-dimensional Farkas converse.

9. `pdPrefix_zeroSupport_corank_eq_schurCorank`
   - block congruence / rank transfer.

10. `pdPrefix_minimalAtom_iff_supportLP_and_corankOne`
    - Theorem D, consuming T-P5-216.

11. `singletonSupportLP_eq_scaledSchurAtomGate`
    - specialization recovering T-P5-217's `sigma=0` and positive scaled-kernel condition.

A practical Lean order is `1 -> 2 -> 4 -> 6 -> 7 -> 9 -> 10`; the abstract Farkas converse can remain later because checker verification of an externally supplied dual only needs theorem 7.

---

## 16. Boundaries left open

### Boundary A — support combinatorics

The exact completion is a finite disjunction over nonempty `J subseteq R`; exponential worst-case behavior remains possible. This child proves soundness/completeness of each support test, not a polynomial enumeration theorem.

### Boundary B — source binding

No actual P5 same-key `K`, `A`, `B`, `D`, selector/cell/tube packet, source hash, or rational reification route is instantiated here.

### Boundary C — trusted global copositivity

The automatic inactive-residual and PSD/corank consequences use the inherited global copositivity of the original `K`. If a caller has only a heuristic or sampled copositivity claim, those consequences are unavailable.

### Boundary D — deployed numeric semantics

Float64 determinant/rank sign decisions, interval guards around zero, Bareiss overflow/complexity, and deployed checker behavior remain separate engineering obligations.

### Boundary E — formal/admission

No Lean/kernel compile, `#print axioms`, 封不觉 independent validation, registry mutation, P8/M4 propagation, or parent closure is performed.

---

## 17. Recommended next mathematical handoff

The next non-duplicate mathematics should exploit the new cone-local statement rather than re-run atom enumeration.

Two useful continuations are:

1. construct an exact extreme-ray generator `V` for the reconstruction cone `Gamma_T={lambda>=0:C lambda>=0}` and transport `Hhat` to the ordinary copositive matrix `G=V^T Hhat V`, proving precisely when this reduces dimension / support count; or
2. derive family-level certificates that rule out **all** support LPs in a block of masks without enumerating them one by one, stronger than T-P5-217's coarse residual Farkas relaxation but still exact rational.

The present child itself is complete as the fixed-support complementarity layer.