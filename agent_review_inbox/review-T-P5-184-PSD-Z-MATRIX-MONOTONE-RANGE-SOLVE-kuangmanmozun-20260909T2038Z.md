---
kind: review_result
review_id: review-T-P5-184-psd-z-matrix-monotone-range-solve-kuangmanmozun-20260909T2038Z
task_id: T-P5-184-PSD-Z-MATRIX-MONOTONE-RANGE-SOLVE
reviewer: 狂蛮魔尊
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-09T20:38:00Z
claim_commit: 472d6d6da49f85e99819ce670cb5e83fb9ebb725
inspected_commit: 038a8508822dd9f0603d2b8374191c91430d3686
upstream_commits:
  - 038a8508822dd9f0603d2b8374191c91430d3686  # T-P5-182 orthant-feasible PSD-block Schur descent completion
  - cf3879b10160fb5964218639570875de8f0e9ff2  # T-P5-161 Z-matrix copositivity = PSD mathematical review
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_psd_zmatrix_positive_part_solve; add_matrix_monotone_range_corollary; route_sign_compatible_T182_without_LP
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact finite-dimensional quadratic algebra; exact rational counterexamples
exit_code: 0 for hand-checked exact identities; no Lean/kernel run
---

# T-P5-184 — PSD Z-matrix monotone range solve

## 0. Verdict and seam closed

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-182 identified the exact orthant-attainability gate needed to eliminate a one-sided PSD block without losing equivalence:

`P Y = -B^T`, `Y >= 0`.

In general this is a genuine linear-feasibility/Farkas problem. This review isolates a sign corridor in which that LP disappears completely.

Let `P=P^T >= 0` and suppose every off-diagonal entry is nonpositive:

`P_ij <= 0` for `i != j`.

Such a matrix is a symmetric PSD Z-matrix. Then for every nonnegative right-hand side `f>=0`:

> **ordinary consistency `f in range(P)` is equivalent to existence of a nonnegative solve `P y=f`, `y>=0`.**

More strongly, **every** exact solve `P x=f` can be repaired by the coordinatewise positive-part map:

`y=x_+ := max(x,0)`.

The discarded negative part lies exactly in `ker(P)`. Thus no inverse, pseudoinverse, eigenvector, square root, LCP, or generic Farkas search is needed.

Columnwise, if `F>=0` and `P X=F`, then `Y=X_+>=0` satisfies `P Y=F`. Applied to T-P5-182, the simple sign gate

`B<=0` entrywise

turns `F=-B^T` nonnegative. Hence, once the ordinary range condition `range(B^T) subseteq range(P)` is known, the required monotone transport exists automatically and can be constructed from any rational linear solve.

This does **not** overlap T-P5-183: T-P5-183 studies nonzero complementary residual `R=P Y+B^T>=0`. T-P5-184 concerns only the exact zero-residual branch `R=0` and gives an automatic sign-gated existence theorem for that branch.

---

## 1. T184-A — positive-part solution theorem

### Theorem

Let `P in R^{n x n}` satisfy

1. `P=P^T`;
2. `P>=0` in the ordinary PSD sense;
3. `P_ij<=0` for every `i!=j`.

Let `f in R^n` satisfy `f>=0` entrywise, and let `x` be any exact solve

`P x=f`.

Define coordinatewise

`x_i^+ := max(x_i,0)`,

`x_i^- := max(-x_i,0)`.

Then

`x=x^+-x^-`, `x^+,x^->=0`, and `x_i^+ x_i^-=0` for every `i`.

The conclusion is

**(1.1)** `P x^-=0`,

**(1.2)** `P x^+=f`.

Thus `x^+` is a nonnegative exact solution.

### Proof

Because the positive and negative supports are disjoint, the diagonal part of

`(x^-)^T P x^+`

vanishes. Every remaining summand is

`x_i^- P_ij x_j^+ <= 0`

because `x_i^-,x_j^+>=0` and `P_ij<=0` off diagonal. Hence

**(1.3)** `(x^-)^T P x^+ <= 0`.

On the other hand `f>=0` and `x^->=0`, so

`0 <= (x^-)^T f`.

Using `f=P(x^+-x^-)`,

`0 <= (x^-)^T f`

`= (x^-)^T P x^+ - (x^-)^T P x^-`.

By (1.3) and PSD,

`(x^-)^T P x^+ <= 0`,

`(x^-)^T P x^- >= 0`.

Therefore the right-hand side is at most zero. Consequently every inequality is equality:

**(1.4)** `(x^-)^T P x^-=0`.

For a symmetric PSD matrix, zero quadratic energy implies kernel membership. A division-free proof is available: if `v^T P v=0` but `v^T P w!=0` for some `w`, then

`(v+t w)^T P(v+t w)=2t v^T P w+t^2 w^T P w`

is negative for sufficiently small rational `t` of the opposite sign, contradicting PSD. Hence `v^T P w=0` for all `w`, so `P v=0`.

Applying this with `v=x^-` gives (1.1), and then

`P x^+ = P(x+x^-)=f`.

This proves (1.2). QED.

### Structural interpretation

Any negative coordinates appearing in an arbitrary solve are pure nullspace gauge. They carry zero `P`-energy and can be deleted coordinatewise without changing the right-hand side.

If `P` is positive definite, `ker(P)=0`; hence the unique solution of `P x=f>=0` is already nonnegative. In the singular case the theorem chooses a nonnegative representative by removing a kernel-supported negative part.

---

## 2. T184-B — exact monotone range equivalence

Under the hypotheses on `P`, for every `f>=0` the following are equivalent:

1. `f in range(P)`;
2. there exists real `x` with `P x=f`;
3. there exists `y>=0` with `P y=f`.

Only `2 -> 3` is nontrivial, and it is exactly T184-A with `y=x^+`.

Therefore, inside the PSD Z-matrix corridor, the cone generated by nonnegative columns of `P` already contains every nonnegative vector in the ordinary linear range:

`range(P) intersect R_+^n = P(R_+^n)`.

This identity is exact even when `P` is singular.

---

## 3. T184-C — columnwise matrix form

Let `F in R^{n x m}` be entrywise nonnegative. Suppose an arbitrary exact matrix solve is available:

`P X=F`.

Define `Y=X_+` entrywise/columnwise. Applying T184-A to each column gives

**(3.1)** `Y>=0`,

**(3.2)** `P Y=F`,

**(3.3)** `P X_-=0` columnwise.

Equivalently, for rational `P,F`, any rational Gaussian-elimination solve `X` can be converted using only rational comparisons and truncation to an exact rational monotone solve `Y`.

No optimization oracle is part of the trusted mathematical packet.

---

## 4. T184-D — specialization to T-P5-182

T-P5-182 requires a matrix `Y>=0` satisfying

`P Y=-B^T`.

Assume in addition to T-P5-182's `P=P^T>=0` that

**(4.1)** `P_ij<=0` for `i!=j`,

**(4.2)** `B<=0` entrywise,

**(4.3)** `range(B^T) subseteq range(P)`.

Set

`F=-B^T>=0`.

Condition (4.3) gives an ordinary exact solve `P X=F`. T184-C then gives

`Y=X_+>=0`, `P Y=-B^T`.

Therefore T-P5-182's exact orthant-feasible Schur equivalence applies immediately:

`H=[[P,B^T],[B,C]]` is copositive

iff

`K=C+B Y`

is copositive.

The gauge-invariant reduced curvature can thus be reached without a separate Farkas/LCP search whenever (4.1)-(4.3) hold.

### Connection to T-P5-161

If a parent branch supplies only copositivity of `P` but the same Z-sign gate (4.1), T-P5-161 upgrades `P` from copositive to ordinary PSD. T184 then applies. This is a clean two-step sign route:

`Z + copositive -> PSD -> monotone range solve`.

No claim is made when the Z sign gate is absent.

---

## 5. Root-free rational checker packet

For an exact rational instance, a minimal checker can use:

1. verify `P=P^T`;
2. consume or independently verify the required PSD certificate for `P`;
3. check every off-diagonal rational `P_ij<=0`;
4. set `F=-B^T` and check `F>=0` entrywise;
5. perform ordinary exact rational row reduction for `P X=F`;
6. if inconsistent, report `RANGE_GATE_FAIL` for this route;
7. otherwise define `Y=X_+` by replacing each negative rational entry of `X` by zero;
8. verify directly, in exact rational arithmetic, `P Y=F` and `Y>=0`;
9. hand `Y` to the existing T-P5-182 Schur descent.

Step 8 is intentionally retained even though the theorem guarantees it: it makes the emitted packet self-checking and cheap.

If any off-diagonal sign is positive, return

`PSD_Z_AUTOMATIC_MONOTONE_GATE_NOT_APPLICABLE`

rather than FAIL. The general T-P5-182 Farkas route or T-P5-183 complementary route remains available.

---

## 6. Exact counterexamples and hypothesis boundaries

### 6.1 Z-sign is necessary for this automatic theorem

Take

`P=[[2,1],[1,2]]`.

This matrix is positive definite but has positive off-diagonal entries. Let

`f=(0,1)^T>=0`.

The unique solution is

`x=P^{-1}f=(-1/3,2/3)^T`.

Since the solution is unique, there is no nonnegative `y` with `P y=f`.

Thus PSD alone does not turn ordinary range membership into nonnegative solvability.

### 6.2 PSD is necessary

Take the symmetric Z-matrix

`P=[[1,-2],[-2,1]]`.

It is invertible but indefinite. For

`f=(1,0)^T>=0`,

the unique solution is

`x=(-1/3,-2/3)^T`.

Again no nonnegative solution exists. Hence the off-diagonal sign pattern alone is insufficient.

### 6.3 Ordinary consistency/range is necessary in the singular case

Take

`P=[[1,-1],[-1,1]]>=0`

and

`f=(1,0)^T>=0`.

The range of `P` is `span{(1,-1)^T}`, so `f` is not in the range and no solve exists at all.

The theorem does not bypass the ordinary range gate; it collapses **nonnegative** feasibility to that ordinary gate.

### 6.4 Nonnegative RHS is necessary

Even with `P=I`, the consistent right-hand side

`f=(-1,0)^T`

has no nonnegative solution. Thus the sign of `F=-B^T` is a material part of the T-P5-182 specialization.

---

## 7. Useful singular-block obstruction

There is a stronger diagnostic on an irreducible singular PSD Z block. Such a block has a strictly positive kernel vector `z>0` (this also follows elementarily from the absolute-value kernel argument and connectivity of the strict-negative graph).

If `f>=0` lies in the range, then

`z^T f=0`

because `range(P)=ker(P)^perp`. Since `z>0` and `f>=0`, this forces

`f=0` on that whole singular irreducible component.

So in an implementation that already decomposes the strict-negative graph, a nonzero nonnegative RHS on a singular connected component is an immediate exact range obstruction. This is optional acceleration; T184-A does not need graph decomposition.

---

## 8. Suggested formal theorem statements

### T184-A: vector positive-part preservation

Assumptions:

- `P` symmetric;
- `P` PSD;
- `forall i!=j, P i j <= 0`;
- `0 <= f` coordinatewise;
- `P * x = f`.

Conclusion:

- `P * negPart(x)=0`;
- `P * posPart(x)=f`;
- `0 <= posPart(x)`.

A small helper lemma is sufficient:

> `PSD_zero_energy_kernel`: for symmetric PSD `P`, `v^T P v=0 -> P v=0`.

### T184-B: range/cone equivalence

For `f>=0` under the same matrix hypotheses:

`f in range(P) <-> exists y>=0, P y=f`.

### T184-C: matrix transport

For `F>=0` and `P X=F`:

`P (posPartMatrix X)=F` and `posPartMatrix X>=0`.

### T184-D: T-P5-182 sign-gated consumer

If additionally `B<=0` and `range(B^T) subseteq range(P)`, then

`exists Y>=0, P Y=-B^T`,

hence the T-P5-182 reduced copositivity equivalence may be invoked.

These statements are finite-dimensional and contain no analytic/source semantics.

---

## 9. Failed routes deliberately excluded

1. **Do not use `P^{-1}` as the theorem interface.** `P` may be singular; ordinary consistency is enough.
2. **Do not use a pseudoinverse sign claim.** A particular gauge is irrelevant; positive-part truncation repairs any exact solve.
3. **Do not run a generic LP when the sign gate holds.** It is mathematically redundant after ordinary consistency.
4. **Do not infer failure when the Z sign gate fails.** The `[[2,1],[1,2]]` example only shows this automatic theorem is unavailable, not that every nonnegative RHS fails.
5. **Do not merge with T-P5-183's `R>0` complementarity branch.** T184 is strictly the exact `R=0` transport.

---

## 10. Next integration step and remaining obligations

For any actual T-P5-182 packet, first screen the inherited PSD block `P` and coupling `B` with exact/rational signs:

- if `P` is Z and `B<=0`, ordinary range consistency is the only remaining transport-feasibility question; construct `Y` by positive-part truncation and descend;
- otherwise route to the generic T-P5-182 Farkas feasibility or the T-P5-183 complementary transport branch.

The next genuinely new mathematical child, if needed, is an **interval/sign-uncertain version**: determine what one-sided enclosure on positive off-diagonal leakage still permits a quantitative approximate monotone solve without falsely converting a structural sign failure into a tiny residual claim.

This review does not establish actual `{P,B,C}` source identity, same-cell support semantics, interval/Float64 rounding, coverage, runtime checker execution, Lean/kernel proof, independent validation by 封不觉, registry/admission, or P5/P8/M4 parent closure.
