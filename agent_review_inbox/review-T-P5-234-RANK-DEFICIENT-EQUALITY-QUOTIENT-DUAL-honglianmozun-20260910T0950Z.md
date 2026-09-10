---
kind: review_result
review_id: review-T-P5-234-rank-deficient-equality-quotient-dual-honglianmozun-20260910T0950Z
task_id: T-P5-234-RANK-DEFICIENT-EQUALITY-QUOTIENT-DUAL
reviewer: 红莲魔尊
agent: 红莲魔尊
source_agent: 红莲魔尊
created_at: 2026-09-10T09:50:00Z
claim_commit: c44c54adf4f02dee5d1ad3cad941956fc06beecc
inspected_commit: 91817309af5e6b1ef68128914ba0ac96e7ee6b34
upstream_commits:
  - 4b309ccdccf423d949421138b2b980e071fb2f49  # T-P5-233 linear-equality conditional curvature
  - 580ac9aef688269631f738f61bb24b4a7e196625  # T-P5-232 coupled-fiber conditional Schur reduction
  - 95fc7a17795dda55ed0f493d5588c573ef84151d  # T-P5-230 trust-region / range-kernel closure
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_rank_deficient_equality_compression; add_feasible_quotient_basis_invariance; add_rank_free_dual_schur_packet; preserve_inconsistent_row_constraints
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact finite-dimensional rational quadratic algebra only; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-234 — rank-deficient equality quotient and rank-free dual Lyapunov closure

## 0. Verdict and seam

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-233 produced a sharp fraction-free conditional-curvature packet for the centered equality

`C v = B z`,

under the packet hypothesis that `C` has full row rank. It explicitly left the rank-deficient case open and warned that dependent rows cannot simply be deleted, because their right-hand sides may impose additional constraints on `z`.

This child closes that mathematical gap in two complementary ways.

1. A **primal row-space compression packet** keeps one maximal independent row set but also keeps an exact compatibility matrix `E_hat`; the original equality is equivalent to the compressed equality plus `E_hat z=0`. The T-P5-233 curvature then remains exact on the feasible `z` quotient. Different row bases may produce different ambient matrices, but they induce exactly the same bilinear form on the feasible subspace.

2. A **rank-free dual multiplier packet** avoids row compression entirely for the final second-Schur/Lyapunov closure. It works for arbitrary rank `C` and reduces the exact unrestricted equality-manifold supremum to one rational KKT system. For rational data, whenever the supremum is finite, a rational certificate exists.

No actual P5 source equality, same-cell/tube coverage, Float64 enclosure, Lean/kernel receipt, independent validation, admission, registry mutation, or parent closure is claimed.

---

## 1. Setup

Let

`H = H^T > 0` in `Q^(r x r)`,

`C in Q^(m x r)`,

`B in Q^(m x p)`,

with no row-rank assumption on `C`.

The centered source equality is

**`C v = B z`,**

where `v=u-tx` is the same centered curved displacement used by T-P5-232/233.

Set

`d := det(H) > 0`,

`J := adj(H)`,

so

`HJ=JH=d I`,

and `J=d H^(-1)>0`.

The rank-free multiplier Gram matrix is

**`S_hat := C J C^T >= 0`.**

Unlike the T-P5-233 full-row-rank packet, `S_hat` may now be singular.

---

# Part I — exact primal row-space compression

## 2. A fraction-free maximal-minor reconstruction

Let

`s := rank(C)`.

Assume first `s>0`.

Choose row indices `I` of cardinality `s` such that

`C0 := C[I,:]`

has full row rank `s`, and set

`B0 := B[I,:]`.

Choose column indices `J0` of cardinality `s` such that the square minor

`A := C0[:,J0]`

is invertible. Let

`alpha := det(A) != 0`,

`eta := alpha^2 > 0`,

and define the fraction-free row reconstruction matrix

**`T_hat := alpha * C[:,J0] * adj(A)`.**

### Theorem A — `maximalMinor_fractionFreeRowReconstruction`

One has

**`T_hat C0 = eta C`.**

### Proof

Because the rows of `C0` form a basis of the row space of `C`, each row `c_i` of `C` has a unique coefficient row `tau_i` with

`c_i = tau_i C0`.

Restricting to columns `J0`,

`c_i[J0] = tau_i A`.

Multiplying by `adj(A)` gives

`c_i[J0] adj(A) = alpha tau_i`.

Therefore

`alpha c_i[J0] adj(A) C0`

`= alpha^2 tau_i C0`

`= eta c_i`.

Stacking all rows proves the identity. QED.

### Remark

The squared determinant is not mathematically necessary; it is used only so the reconstruction scale `eta` is manifestly positive. A checker may instead use any nonzero rational scale and any exact matrix satisfying `T_hat C0=eta C`.

---

## 3. Dependent rows become an exact compatibility constraint

Define

**`E_hat := eta B - T_hat B0`.**

This is the information that is lost if one merely deletes dependent rows.

### Theorem B — `rankDeficientEquality_compressed_iff`

For every `v,z`,

**`C v = B z`**

if and only if

**`C0 v = B0 z`**

and

**`E_hat z = 0`.**

### Proof

If `Cv=Bz`, selecting rows `I` gives `C0v=B0z`. Also

`E_hat z`

`= eta Bz - T_hat B0z`

`= eta Cv - T_hat C0v`

`= 0`

by Theorem A.

Conversely, if `C0v=B0z` and `E_hat z=0`, then

`eta Cv`

`= T_hat C0v`

`= T_hat B0z`

`= eta Bz`.

Since `eta>0`, `Cv=Bz`. QED.

### Feasible kernel-coordinate subspace

Define

**`Z := {z : E_hat z = 0}`.**

Because `C0` has full row rank, for every `z` there exists some `v` with `C0v=B0z`. Hence

**`Z = {z : Bz in range(C)}`.**

Thus `Z` is intrinsic; it does not depend on which maximal independent row set was chosen.

For `z notin Z`, the original equality fiber is empty. The correct conditional energy is `+infinity`, not a finite quadratic cost obtained after silently dropping rows.

---

## 4. T-P5-233 descends exactly to the feasible quotient

Apply the T-P5-233 construction to the full-row-rank compressed pair `(C0,B0)`:

`S0_hat := C0 J C0^T > 0`,

`delta := det(S0_hat) > 0`,

`K0 := adj(S0_hat)`,

**`R_hat := d B0^T K0 B0 >= 0`,**

**`Y := J C0^T K0 B0`.**

For every pair satisfying the compressed equality,

`delta^2 v^T H v`

`= (delta v-Yz)^T H (delta v-Yz) + delta z^T R_hat z`.

The new point is that, for `z in Z`, the equality-attaining minimizer is also feasible for the **original** rank-deficient system.

### Theorem C — `rankDeficientEquality_exactConditionalEnergyOnFeasibleSubspace`

For every `z in Z`,

**`inf_{Cv=Bz} v^T H v = (1/delta) z^T R_hat z`.**

The infimum is attained at

**`v_*(z)=Yz/delta`.**

For `z notin Z`, the original fiber is empty.

### Proof

For `z in Z`, T-P5-233 gives

`C0 v_*=B0z`.

Together with `E_hat z=0`, Theorem B gives `Cv_*=Bz`. The T-P5-233 completed-square identity then proves both optimality and the displayed value. QED.

### Interpretation

The ambient matrix `R_hat/delta` is not itself canonical away from `Z`. The canonical object is its restriction to the feasible quotient/subspace `Z`.

---

## 5. Basis invariance is exact on `Z`, not necessarily off `Z`

Take two valid maximal-row compression packets, indexed `a` and `b`, producing

`(delta_a,R_hat_a,E_hat_a)`

and

`(delta_b,R_hat_b,E_hat_b)`.

Both compatibility kernels equal the intrinsic feasible subspace `Z`.

### Theorem D — `rankDeficientEquality_curvature_basisInvariantOnFeasibleSubspace`

For all `z,w in Z`,

**`z^T (delta_b R_hat_a - delta_a R_hat_b) w = 0`.**

Equivalently, the two rational forms

`R_hat_a/delta_a`

and

`R_hat_b/delta_b`

have the same restriction to `Z x Z`.

### Proof

By Theorem C, for every `z in Z`,

`z^T R_hat_a z / delta_a`

and

`z^T R_hat_b z / delta_b`

both equal the same intrinsic value

`inf_{Cv=Bz} v^T H v`.

Their quadratic-form difference vanishes on the vector subspace `Z`. Polarization then gives vanishing of the associated symmetric bilinear form on `Z x Z`. Multiplying by `delta_a delta_b` yields the fraction-free identity. QED.

### Corollary — all-`z` compatibility

If

`range(B) subseteq range(C)`,

then `Z=Q^p`, equivalently `E_hat=0`, and the ambient matrices themselves obey

**`delta_b R_hat_a = delta_a R_hat_b`.**

So the full-row-rank T-P5-233 matrix becomes globally basis-independent exactly when every kernel coordinate is compatible with the original equality.

---

## 6. The true feasible radical is still `ker(B)`

### Theorem E — `rankDeficientEquality_feasibleCurvatureRadical_eq_kerB`

For `z in Z`, the exact conditional energy is zero if and only if

**`Bz=0`.**

Hence the radical of the canonical conditional-curvature form on `Z` is exactly

**`ker(B)`.**

### Proof

If `Bz=0`, choose `v=0`; then `Cv=Bz=0`, so the minimum energy is zero.

Conversely, if the exact conditional energy is zero, Theorem C attains it at a feasible `v_*`. Since `H>0`, `v_*^T H v_*=0` implies `v_*=0`. Feasibility then gives `Bz=Cv_*=0`. QED.

This is useful for the Lyapunov dispatcher: row dependence in `C` changes which `z` are feasible, but among feasible directions the genuinely flat forcing directions are still exactly `ker(B)`.

---

# Part II — a rank-free dual packet for the final Lyapunov closure

## 7. The unrestricted equality-manifold second-Schur problem

Consider

**`q_t(v,z) := a t^2 + 2 t b^T z - v^T H v`,**

subject only to

`Cv=Bz`.

Here `a` is the already accumulated quadratic base coefficient from the first completion.

The T-P5-233 route first builds a pointwise curvature matrix and then performs a second Schur solve. In the rank-deficient case, the same final answer has a cleaner basis-free dual description.

---

## 8. Any equality multiplier gives a global upper bound

Let `mu in Q^m` satisfy

**`B^T mu = b`.**

For every feasible `Cv=Bz`,

`b^Tz = mu^T Bz = mu^T Cv = (C^Tmu)^T v`.

Completing the `H` square gives

`2t b^Tz-v^THv`

`<= t^2 (C^Tmu)^T H^(-1)(C^Tmu)`

`= (t^2/d) mu^T S_hat mu`.

Therefore

### Theorem F — `rankFreeDual_anyMultiplier_upper`

If `B^Tmu=b`, then for every feasible `(v,z)`,

**`q_t(v,z) <= t^2 [ a + (mu^T S_hat mu)/d ]`.**

This statement requires no rank assumption on `C` and no row compression.

A sufficient fraction-free PASS gate is therefore

**`d a + mu^T S_hat mu <= 0`.**

But an arbitrary multiplier may be conservative. The next theorem gives an exact stationary certificate.

---

## 9. A rational KKT packet makes the upper bound sharp

Assume there exist rational vectors `mu in Q^m`, `nu in Q^p` satisfying

**`B^T mu = b`,**

**`S_hat mu = B nu`.**

The second relation is the stationarity condition for minimizing multiplier energy along the affine set `B^Tmu=b`.

### Theorem G — `rankFreeDual_stationaryMultiplier_isOptimal`

For every other `mu'` with `B^Tmu'=b`,

**`mu'^T S_hat mu' >= mu^T S_hat mu`.**

### Proof

Write `mu'=mu+eta`. Then `B^Teta=0`. Since `S_hat mu=Bnu`,

`eta^T S_hat mu = eta^T Bnu = 0`.

Thus

`mu'^T S_hat mu'`

`= mu^T S_hat mu + eta^T S_hat eta`

`>= mu^T S_hat mu`,

because `S_hat=CJC^T>=0`. QED.

### Theorem H — `rankFreeDual_exactSecondSchur`

Under the same two rational equations, for every `t`,

**`sup_{Cv=Bz} q_t(v,z)`**

**`= t^2 [ a + (mu^T S_hat mu)/d ]`.**

Equality is attained at the explicit rationally scaled pair

**`v_* = (t/d) J C^T mu`,**

**`z_* = (t/d) nu`.**

### Proof

Theorem F supplies the upper bound. For the proposed pair,

`Cv_*`

`= (t/d) CJC^T mu`

`= (t/d) S_hat mu`

`= (t/d) Bnu`

`= Bz_*`,

so it is feasible.

Also

`v_*^T H v_* = (t^2/d) mu^T S_hat mu`,

while

`b^Tnu = mu^T Bnu = mu^T S_hat mu`.

Therefore

`2t b^Tz_* - v_*^THv_*`

`= (t^2/d) mu^T S_hat mu`,

which attains the upper bound. QED.

### Exact fraction-free Lyapunov gate

The unrestricted centered equality manifold is nonpositive exactly when the certified scalar satisfies

**`d a + mu^T S_hat mu <= 0`.**

Strict negativity of this rational scalar gives a strict quadratic reserve.

No inverse, square root, pseudoinverse, nullspace eigenvector, or row-basis choice is needed in the trusted packet.

---

## 10. Finite versus unbounded: the same exact range obstruction survives all row ranks

### Theorem I — `rankFreeDual_rangeFailure_unbounded`

For `t>0`, if

**`b notin range(B^T)`,**

then

**`sup_{Cv=Bz} q_t(v,z)=+infinity`.**

### Proof

By finite-dimensional orthogonality there exists

`n in ker(B)`

with `b^Tn != 0`.

Set `v=0`, `z=s n`. Then `Cv=Bz=0`, so the pair is feasible for every real `s`, and

`q_t(0,sn)=a t^2+2ts b^Tn`.

Choose the sign of `s` and let `|s| -> infinity`. QED.

Thus, for the **unrestricted** exact equality manifold,

**finite second-Schur closure iff `b in range(B^T)`.**

If the actual source additionally bounds the surviving `ker(B)` coordinate, range failure must instead route to the bounded support/exponent machinery of T-P5-229/231. It is not then an automatic physical FAIL.

---

## 11. Rational certificate completeness

Assume all data `H,C,B,b` are rational and `b in range(B^T)`.

The affine multiplier set

`M={mu:B^Tmu=b}`

is nonempty. The PSD quadratic `mu^T S_hat mu` attains a minimum on this affine set. At a minimizer `mu_*`, first-order stationarity along every `eta in ker(B^T)` gives

`eta^T S_hat mu_*=0`.

Hence

`S_hat mu_* in (ker(B^T))^perp = range(B)`,

so some `nu_*` satisfies

`S_hat mu_*=Bnu_*`.

The joint KKT equations

`B^Tmu=b`,

`S_hatmu-Bnu=0`

are a linear system with rational coefficients and rational right-hand side. Since they are consistent over `R`, Gaussian elimination yields a rational solution.

### Corollary — `rankFreeDual_rationalPacket_completeWhenFinite`

For rational data, whenever the unrestricted equality-manifold second-Schur supremum is finite, there exists a fully rational pair `(mu,nu)` satisfying the exact stationarity packet of Theorem H.

This is stronger than merely approximating an irrational optimizer: the trusted proof object itself can be rational.

---

## 12. Relation to the T-P5-233 full-row-rank packet

When `C` has full row rank, T-P5-233 gives the exact coefficient by first forming its induced curvature `R_hat/delta` and then solving the second Schur problem.

Theorem H gives the same coefficient by minimizing the multiplier energy

`mu^T C H^(-1) C^T mu`

subject to `B^Tmu=b`.

The two coefficients are identical because both equal the same exact primal supremum

`sup_{Cv=Bz} [2b^Tz-v^THv]`.

Thus the new dual packet is not a relaxation or a competing bound. It is a basis-free continuation of T-P5-233 that remains valid when `C` loses row rank.

---

# Part III — exact regressions and failure boundaries

## 13. Regression A: two different row bases give the same physical curvature

Take

`H=[1]`,

`C=[[1],[2]]`,

`B=[[1],[2]]`.

The original equality is simply

`v=z`.

Using the first row as the compressed basis gives

`C0=[1]`, `B0=[1]`,

and T-P5-233 returns conditional energy

`z^2`.

Using the second row gives

`C0=[2]`, `B0=[2]`.

Here

`S0_hat=4`, `delta=4`, `R_hat=4`,

so again

`z^T R_hat z/delta = z^2`.

The fraction-free cross-basis checksum is

`4*1 = 1*4`.

Since `range(B) subseteq range(C)`, the compatibility subspace is all `z`, so the two ambient forms coincide globally.

For `b=1`, choose the dual packet

`mu=(1,0)`, `nu=1`.

Then

`B^Tmu=1`,

`S_hatmu=B`,

and Theorem H gives exact coefficient `1`, matching

`sup_z (2z-z^2)=1`.

---

## 14. Regression B: silently deleting an inconsistent dependent row is unsound

Take

`H=[1]`,

`C=[[1],[2]]`,

`B=[[1],[0]]`.

The original equality means simultaneously

`v=z`,

`2v=0`.

Hence the true feasible set is

**`v=z=0`.**

### First-row compression

Choose `C0=[1]`, `B0=[1]`. A valid row reconstruction is

`T=[[1],[2]]`,

so

`E=B-TB0=(0,-2)^T`.

The compatibility equation `Ez=0` correctly restores `z=0`.

If one deletes the second row but forgets `Ez=0`, one falsely enlarges the source fiber to `v=z`.

### Second-row compression

Choose `C0=[2]`, `B0=[0]`. The compressed conditional curvature is identically zero, but its compatibility equation again forces `z=0`.

Thus the two ambient curvature matrices differ away from the feasible subspace, yet both are exactly correct on the intrinsic feasible subspace `Z={0}`.

This proves why basis invariance must be stated **on `Z`** unless all `z` are compatible.

### Dual packet detects the same cancellation without choosing a row basis

For `b=1`, take

`mu=(1,-1/2)`, `nu=0`.

Then

`B^Tmu=1`,

while

`S_hatmu=0=Bnu`.

Therefore Theorem H gives exact coefficient zero, matching the fact that the only feasible `z` is zero.

This example is a strict separation from a naive independent-row deletion: the rank-free dual sees the hidden dependent-row compatibility automatically.

---

## 15. Rank-zero base case

If

`rank(C)=0`,

then `C=0` and the equality becomes

**`Bz=0`.**

The curved variable `v` is unconstrained, so its minimum energy is zero. The feasible conditional-curvature form is therefore identically zero on `ker(B)` and undefined / `+infinity` off the compatible subspace.

The dual packet handles this case without a special inverse:

`S_hat=0`.

If `b in range(B^T)`, choose `mu` with `B^Tmu=b` and set `nu=0`; then Theorem H gives zero second-Schur surcharge. If `b notin range(B^T)`, Theorem I gives the unbounded kernel ray.

So the dual dispatcher covers every rank of `C`, including rank zero.

---

## 16. Failure boundaries

This child is exact only under the following semantic boundaries.

### 16.1 Centering remains mandatory

The equality must constrain the same displacement `v=u-tx` used in the completed square. An affine offset must be re-centered explicitly. T-P5-233 already gave a false-PASS counterexample when this is ignored; rank compression does not repair a centering error.

### 16.2 Exact equality cannot be replaced by a relaxed outer tube

The implication

`Cv=Bz -> conditional curvature`

cannot be consumed merely from a relaxation such as `||Cv-Bz||<=eps`. A relaxed outer relation may admit lower-energy pairs and invalidate the PASS-oriented lower curvature.

### 16.3 A positive outer supremum is not a source-level FAIL

If the actual source fiber is a strict subset of the equality manifold, Theorem F/H gives a valid PASS-oriented upper bound. A positive value only says this outer equality manifold is not sufficient to certify safety; it does not prove an actual source trajectory violates the Lyapunov inequality.

### 16.4 Row compression without compatibility is forbidden

Any producer that keeps only `C0v=B0z` must also export either the exact compatibility relation `E_hat z=0` or a proof that `E_hat=0` on the entire consumed `z` domain. Omitting it can create spurious flat directions or erase source constraints.

---

## 17. Suggested trusted packets

### Pointwise conditional-curvature packet

For source code that needs an explicit curvature form on `z`:

1. `H=H^T>0`, `d=det(H)`, `J=adj(H)`;
2. a maximal independent row set `I`, compressed `C0,B0`;
3. a nonzero maximal minor `A=C0[:,J0]`;
4. `alpha=det(A)`, `eta=alpha^2`, `T_hat=alpha C[:,J0]adj(A)`;
5. exact reconstruction `T_hat C0=eta C`;
6. `E_hat=eta B-T_hat B0`;
7. T-P5-233 data `S0_hat,delta,K0,R_hat,Y`;
8. consume the finite curvature only under `E_hat z=0`.

### Final unrestricted second-Schur packet

If only the scalar Lyapunov closure is needed, the smaller rank-free packet is preferable:

1. `d=det(H)>0`, `HJ=dI`;
2. `S_hat=CJC^T`;
3. rational `mu,nu`;
4. `B^Tmu=b`;
5. `S_hatmu=Bnu`;
6. scalar gate

**`d a + mu^T S_hat mu <= 0`.**

This packet is row-basis invariant by construction.

---

## 18. Lean-facing decomposition

Suggested finite-dimensional theorem leaves:

1. `maximalMinor_fractionFreeRowReconstruction`
   - prove `T_hat C0=eta C` from a selected nonsingular rank minor.

2. `rankDeficientEquality_compressed_iff`
   - prove `Cv=Bz <-> C0v=B0z and E_hat z=0`.

3. `rankDeficientEquality_exactConditionalEnergyOnFeasibleSubspace`
   - consume the existing full-row-rank T-P5-233 identity on `C0`.

4. `rankDeficientEquality_curvature_basisInvariantOnFeasibleSubspace`
   - equality of scaled bilinear forms on the compatibility kernel.

5. `rankDeficientEquality_feasibleCurvatureRadical_eq_kerB`.

6. `rankFreeDual_anyMultiplier_upper`
   - one completed-square theorem from `B^Tmu=b`.

7. `rankFreeDual_stationaryMultiplier_isOptimal`
   - use `S_hatmu=Bnu` and `S_hat>=0`.

8. `rankFreeDual_exactSecondSchur`
   - explicit equality witness `(v_*,z_*)`.

9. `rankFreeDual_rangeFailure_unbounded`
   - explicit `ker(B)` ray.

The first formalization should keep source binding, Float64 semantics, and admission entirely outside these finite-dimensional algebraic leaves.

---

## 19. Remaining obligations and next seam

Still open:

- actual same-key P5 extraction of the centered equality `Cv=Bz`;
- proof that dependent source rows are represented by the exact rational/interval packet rather than a rounded fit;
- whether the equality manifold is exact, inner, or an outer source model;
- additional inequalities that may further reduce the supremum;
- cell/tube/trajectory coverage and source dilation law;
- interval/Float64 enclosure for `H,C,B,b,a`;
- concrete strict scalar reserve `d a+mu^T S_hatmu<0`;
- Lean implementation and pinned compile;
- independent validation by 封不觉;
- admission / registry / parent closure.

The next smallest mathematical seam is the **equality-plus-ellipsoid constrained dual**: when the equality manifold is intersected with an actual bounded quadratic source fiber, combine the rank-free multiplier quotient above with the T-P5-230 S-lemma/trust-region multiplier without first projecting to an explicit nullspace basis. The target should be an exact block/KKT packet and a sharp statement of when the equality multiplier and trust-region multiplier commute.