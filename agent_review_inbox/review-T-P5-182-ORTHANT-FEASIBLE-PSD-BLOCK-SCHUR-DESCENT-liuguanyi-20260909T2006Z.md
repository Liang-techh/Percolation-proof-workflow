---
kind: review_result
review_id: review-T-P5-182-orthant-feasible-psd-block-schur-descent-liuguanyi-20260909T2006Z
task_id: T-P5-182-ORTHANT-FEASIBLE-PSD-BLOCK-SCHUR-DESCENT
reviewer: 柳冠一
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-09T20:06:00Z
claim_commit: ebaa374fcb851ab7f9a3fa02fc86582dc1ef8f86
inspected_commit: a159edb44c1d9da13d2656393ca36a48478bb31d
upstream_commits:
  - 953eb401979eeb1374e4e4c722a5c29588e6a498  # T-P5-178 critical-cone/range-solve Schur bridge
  - a0fba26798157e76c4e0ed1fab78da0c05059605  # T-P5-179 canonical support descent / PSD inheritance
  - 1c9b38ebd1b1fedf86a29eb50cf3cae24690c6c9  # T-P5-181 strict-interior automatic range bridge
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_one_sided_psd_block_completion; add_orthant_attainability_iff; add_monotone_range_solve_packet; route_inherited_PSD_critical_block_before_generic_copositivity
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact finite-dimensional quadratic algebra; exact rational symbolic regressions
exit_code: 0 for hand-checked exact identities; no Lean/kernel run
---

# T-P5-182 — orthant-feasible PSD-block Schur descent

## 0. Verdict and seam closed

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-179 shows that after canonical support descent, zero-loaded parent coordinates that were dropped from the true positive support form an inherited PSD block inside the T-P5-178 reduced critical copositivity problem. Those dropped coordinates are still **one-sided orthant variables**, not signed active variables.

That distinction matters. T-P5-178's ordinary signed Schur equivalence may not be applied to such a block without an additional feasibility condition: the formal unconstrained minimizer can leave the nonnegative orthant and create a false FAIL.

This review gives the exact missing bridge.

Let

`H = [[P, B^T], [B, C]]`

with

- `P=P^T >= 0`,
- `C=C^T`,
- first block variable `u>=0`,
- retained critical variable `e>=0`.

If `B^T` is in `range(P)`, any solve `P X=B^T` gives the completion

`q(u,e) = (u+X e)^T P (u+X e) + e^T K e`,

where

`K = C-BX`.

Therefore `K` copositive is always sufficient for `H` copositive. The converse is **not** always true because `u=-Xe` may be infeasible.

The exact converse condition is that the Schur lower bound be attainable inside the orthant. This is equivalent to a monotone range solve

`P Y = -B^T`, `Y>=0`.

Under that condition, with `X=-Y`,

`q(u,e) = (u-Y e)^T P (u-Y e) + e^T (C+B Y)e`,

and for every `e>=0` the first term is killed by the feasible choice `u=Y e>=0`. Hence

> **`H` is copositive iff `K=C+B Y` is copositive.**

This is a block, possibly singular, one-sided generalization of the sign-compatible scalar pivot used in T-P5-170. It is exactly suited to the inherited PSD block `H_UU` left by T-P5-179 when external critical rows remain.

The result is exact finite-dimensional algebra. It does not prove actual source identity, actual T-P5-179/T-P5-178 packet binding, global support coverage, Float64 semantics, P8/M4, Lean/kernel, independent verification, admission, or registry eligibility.

---

## 1. Setup

Let

`P=P^T in R^{m x m}`,

`B in R^{p x m}`,

`C=C^T in R^{p x p}`,

and define

`H = [[P,B^T],[B,C]]`.

For

`u in R_+^m`, `e in R_+^p`,

write

`q_H(u,e)=u^T P u + 2 e^T B u + e^T C e`.

Assume throughout the Schur statements that

`P>=0`.

The intended P5 specialization is:

- `P = H_UU`, the inherited reduced block on dropped zero-loaded parent rows from T-P5-179;
- `e` indexes genuinely external zero-residual critical rows;
- `B` is the reduced `E x U` coupling after the first T-P5-178 completion against the true positive support;
- `C` is the reduced external `E x E` block.

The key point is that both `u` and `e` are one-sided here.

---

## 2. T182-A — range completion is always a valid lower bound

Assume there exists

`X in R^{m x p}`

such that

**(2.1)** `P X = B^T`.

Define

**(2.2)** `K := C-BX`.

Then `K` is symmetric and, for all real `u,e`,

**(2.3)**

`q_H(u,e) = (u+Xe)^T P (u+Xe) + e^T K e`.

### Proof

Since `P=P^T` and `PX=B^T`, transposition gives

`X^T P=B`.

Hence

`BX=X^T P X`,

which is symmetric. Therefore `K` is symmetric.

Expanding,

`(u+Xe)^T P(u+Xe)`

`=u^TPu + 2 e^T X^T P u + e^T X^T P X e`

`=u^TPu + 2 e^T B u + e^T B X e`.

Adding `e^T(C-BX)e` gives `q_H(u,e)`.

QED.

### Immediate consequence

Because `P>=0`,

**(2.4)** `K copositive => H copositive`.

No sign condition on `X` is needed for this direction.

This is useful as a one-way dimension-reduction certificate even when the Schur minimizer is outside the orthant.

---

## 3. T182-B — the Schur block is gauge invariant

Suppose `X` and `X'` both solve

`PX=B^T`, `PX'=B^T`.

Then

`N:=X'-X`

satisfies

`PN=0`.

Using `B=X^TP`,

`BN=X^T P N=0`.

Therefore

**(3.1)** `BX'=BX`,

and hence

**(3.2)** `C-BX'=C-BX=K`.

So the reduced Schur block is intrinsic even when `P` is singular. No pseudoinverse, minimum-norm representative, eigenbasis, or canonical kernel gauge is needed.

The **sign of a particular solve**, however, is not gauge invariant. This is why the correct converse condition below is existential: a sign-compatible gauge must exist.

---

## 4. T182-C — intrinsic orthant attainability criterion

Fix any range solve `PX=B^T` and its intrinsic `K`.

For a fixed `e>=0`, identity (2.3) gives the Schur lower bound

**(4.1)** `q_H(u,e) >= e^T K e`

for all `u>=0`.

Because `P>=0`, equality holds exactly when

`u+Xe in ker(P)`.

Equivalently,

**(4.2)** `P u = -B^T e`.

Therefore the lower bound is attained by some feasible `u>=0` iff

**(4.3)** `-B^T e in P(R_+^m)`.

Now vary `e` over the full nonnegative orthant. Since `R_+^p` is generated by the coordinate basis and `P(R_+^m)` is a convex cone, the following are equivalent:

1. for every `e>=0`, the Schur lower bound is attained by some `u>=0`;
2. for every basis vector `e_j`, `-B^T e_j in P(R_+^m)`;
3. there exists a matrix `Y>=0` entrywise such that

   **(4.4)** `P Y = -B^T`;
4. there exists a range solve `X` with

   **(4.5)** `PX=B^T`, `X<=0` entrywise,

   namely `X=-Y`.

This is the exact **orthant-feasible range condition**.

It is stronger than ordinary range compatibility, but it is exactly what is needed to make the unconstrained Schur lower bound reachable by one-sided variables.

---

## 5. T182-D — exact one-sided Schur equivalence

Assume

`P>=0`

and there exists

`Y>=0`

with

**(5.1)** `PY=-B^T`.

Set

**(5.2)** `K := C+B Y`.

Since `B=-Y^T P`,

`BY=-Y^T P Y`,

so equivalently

**(5.3)** `K=C-Y^T P Y`.

Then for all real `u,e`,

**(5.4)**

`q_H(u,e)=(u-Y e)^T P(u-Y e)+e^T K e`.

### Theorem

Under (5.1),

**(5.5)**

`H is copositive  <=>  K is copositive`.

### Proof: right to left

If `K` is copositive and `u,e>=0`, then

`(u-Ye)^T P(u-Ye)>=0`

because `P>=0`, while

`e^TKe>=0`.

Hence `q_H(u,e)>=0`.

### Proof: left to right

Assume `H` is copositive. Fix arbitrary `e>=0` and choose

`u=Y e`.

Because `Y>=0`, this is a feasible `u>=0`. The completion term vanishes, so

`q_H(Ye,e)=e^T K e`.

Copositivity of `H` therefore yields

`e^TKe>=0`

for every `e>=0`. Thus `K` is copositive.

QED.

### Interpretation

`Y` is not merely a linear solve. It is an **orthant-compatible minimizer transport**:

`e -> u_*(e)=Ye`.

It transports every retained nonnegative critical direction to a feasible minimizing value of the inherited PSD variables.

---

## 6. Why ordinary Schur equivalence is unsound for one-sided inherited rows

Take exact rational data

`P=[1]`, `B=[1]`, `C=[0]`.

Then

`H=[[1,1],[1,0]]`.

For `u,e>=0`,

**(6.1)** `q_H(u,e)=u^2+2ue>=0`,

so `H` is copositive.

The unique ordinary range solve is

`X=1`.

The signed Schur block is

**(6.2)** `K=C-BX=-1`.

Thus `K` is not copositive.

The formal minimizing point is

`u=-Xe=-e`,

which is outside the feasible orthant for every `e>0`.

There is no monotone solve `Y>=0` with

`PY=-B^T=-1`.

So this example proves:

> **A negative unconstrained Schur block does not imply failure of a one-sided copositivity problem.**

The orthant-attainability gate is mathematically essential, not interface bureaucracy.

This is precisely the failure mode that would occur if T-P5-178's signed-active Schur equivalence were recursively applied to T-P5-179's dropped one-sided coordinates without checking feasibility.

---

## 7. Exact singular-PSD regression and gauge behavior

Take

`P=[[1,-1],[-1,1]]>=0`.

Let

`Y=[[1],[0]]>=0`.

Then

`PY=(1,-1)^T`.

Choose

`B=[-1,1]`,

so

`PY=-B^T`.

Let

`C=[1]`.

Then

`BY=-1`,

and

`K=C+BY=0`.

Hence

**(7.1)**

`q_H(u,e)=(u-Ye)^T P(u-Ye)>=0`

for all real `u,e`; in particular the one-sided problem is safe.

The solve is nonunique because

`ker(P)=span{(1,1)}`.

For any scalar `t`,

`Y_t=(1+t,t)^T`

still satisfies

`P Y_t=-B^T`.

Some gauges are nonnegative (`t>=0`), while others are not. Nevertheless

`B Y_t=-1`

for every `t`, so `K` is unchanged.

This separates two facts that a checker should not conflate:

- Schur curvature `K` is gauge invariant;
- orthant feasibility asks only that **at least one** gauge be nonnegative.

---

## 8. A genuinely copositive-but-indefinite reduced example

The bridge is not merely a PSD test.

Take scalar inherited block

`P=[1]`,

external coupling

`B=[[-1],[-1]]`,

and

`Y=[1,1]>=0`.

Then

`PY=-B^T`.

Choose

`C=[[1,2],[2,1]]`.

The reduced block is

`K=C+B Y`

`=[[0,1],[1,0]]`,

which is copositive but indefinite.

The full matrix is

`H=[[ 1,-1,-1],
    [-1, 1, 2],
    [-1, 2, 1]]`.

Its exact orthant energy is

**(8.1)**

`q_H(u,e1,e2)=(u-e1-e2)^2+2 e1 e2>=0`

for all nonnegative variables.

But for signed directions it is indefinite; for example `(u,e1,e2)=(0,1,-1)` gives `-2`.

Thus the T182 bridge genuinely preserves a copositive, not merely PSD, reduced problem.

---

## 9. Scalar specialization recovers the sign-compatible pivot

Let the inherited block be scalar

`P=[b]`, `b>0`.

Write the cross block as

`B=-r`

with

`r>=0` entrywise.

Then the unique monotone solve is

`Y=r^T/b>=0`.

The reduced matrix is

`K=C-r r^T/b`.

Multiplying by the positive scalar `b`, copositivity of `K` is equivalent to copositivity of

**(9.1)** `b C-r r^T`.

This is exactly the sign-compatible scalar Schur pivot structure used in T-P5-170.

T182 therefore extends that scalar pivot to a possibly singular PSD block without introducing inverse or pseudoinverse into the trusted interface.

---

## 10. T182-E — Farkas certificate for an unavailable monotone solve

The monotone solve condition is a rational linear feasibility problem.

For the `j`-th external column let

`beta_j := B^T e_j in R^m`.

The required column solve is

**(10.1)** `P y_j=-beta_j`, `y_j>=0`.

By Farkas' lemma, exactly one of the following holds:

1. there exists `y_j>=0` satisfying (10.1);
2. there exists `lambda_j` satisfying

   **(10.2)** `P lambda_j>=0` entrywise,

   **(10.3)** `beta_j^T lambda_j>0`.

Indeed, (10.2)-(10.3) contradict any feasible `y_j` because

`beta_j^T lambda_j`

`=-(P y_j)^T lambda_j`

`=-y_j^T P lambda_j<=0`.

Conversely the standard Farkas alternative gives such a separating `lambda_j` when the cone-membership problem fails.

### Important semantic boundary

A Farkas witness here proves only:

> **this orthant-feasible Schur descent route is unavailable for that column.**

It does **not** prove that `H` is non-copositive.

Section 6 is the minimal counterexample: `lambda=1` certifies that the monotone solve is impossible, while the full matrix is still copositive because the positive cross term is benign on the orthant.

So the dispatcher must route back to the generic copositivity machinery, not emit mathematical FAIL.

---

## 11. Rational witness lemma

Suppose `P` and `B` have rational entries.

The feasible set

`F={Y : PY=-B^T, Y>=0}`

is a rational polyhedron. Therefore, if `F` is nonempty over the reals, it contains a rational point.

Hence in the exact-rational P5 branch:

> **existence of an orthant-feasible real Schur transport implies existence of an exact rational transport packet.**

The checker need not represent algebraic numbers, inverses, eigenvectors, or square roots. The producer may provide rational `Y`; the trusted side verifies only matrix equality and entrywise nonnegativity.

This statement is about rational linear feasibility, not about source/runtime rationality. If the actual source packet contains algebraic or interval data, a separate enclosure/binding theorem is still required.

---

## 12. Exact connection to T-P5-179 / T-P5-178

After T-P5-179 support descent, suppose the T-P5-178 reduced critical matrix on

`I=U sqcup E`

has block form

`H_I=[[P,B^T],[B,C]]`,

where

- `U` are inherited dropped zero-loaded parent coordinates;
- `E` are genuinely external zero-residual rows;
- T-P5-179 proves `P=H_UU>=0`.

Then there are three mathematically distinct routes.

### Route 1 — monotone block descent

If the producer supplies

`Y>=0`, `P Y=-B^T`,

form

`K=C+B Y`.

Then

`H_I copositive <=> K copositive`.

The inherited `U` block can be removed exactly, and only the smaller external `E` block is sent to the generic copositivity dispatcher.

### Route 2 — ordinary range solve only

If only

`PX=B^T`

is available, then

`K=C-BX copositive => H_I copositive`

is safe, but failure of `K` is inconclusive.

This can still be used as a sufficient certificate, but not as a two-sided decision procedure.

### Route 3 — no usable range transport

If no ordinary range solve exists, or if the monotone solve is unavailable and the one-way Schur sufficient test does not close, keep the full `H_I` and use the existing copositivity dispatcher.

Do not reinterpret lack of a block elimination certificate as failure of the physical contact.

---

## 13. Minimal checker-facing packet

A source-independent exact packet for the lossless Route 1 needs only:

1. a symmetric rational block `P` with upstream evidence `P>=0`;
2. rational `B,C` from the **same** reduced T-P5-178 matrix and the same support/contact key;
3. rational `Y`;
4. exact equality

   `P Y=-B^T`;

5. exact entrywise inequalities

   `Y>=0`;

6. exact construction

   `K=C+B Y`;

7. a copositivity certificate for `K` from the existing P5 dispatcher.

The trusted algebra is only matrix multiplication/addition, equality, entrywise order, PSD of the inherited block, and the downstream copositivity theorem.

No inverse, pseudoinverse, determinant root, eigenvalue, SVD, norm, tolerance, or canonical singular solve is required.

For a one-way sufficient packet, replace items 3-5 by any exact solve `PX=B^T` and use `K=C-BX`, but tag the result as **sufficient-only** unless an orthant-attainability witness is also present.

---

## 14. Candidate formal theorem statements

### `psdBlock_completion_of_rangeSolve`

If `P` is symmetric PSD and `P ⬝ X=Bᵀ`, then

`quad H (u,e)=quad P (u+Xe)+quad (C-BX) e`.

### `copositive_of_schurCopositive`

Under the previous hypotheses, copositivity of `C-BX` implies copositivity of `H`.

### `orthantSchur_attainable_iff_nonnegSolve`

The Schur lower bound is attainable by a nonnegative first-block vector for every `e>=0` iff there exists `Y>=0` with

`PY=-Bᵀ`.

### `copositive_iff_schurCopositive_of_nonnegSolve`

If `P>=0`, `Y>=0`, and `PY=-Bᵀ`, then

`H copositive <=> C+BY copositive`.

### `schurBlock_gaugeInvariant`

If `PX=PX'=Bᵀ`, then

`BX=BX'`.

### `monotoneRangeSolve_farkasAlternative`

For one column `beta`, either there is `y>=0` with `Py=-beta`, or there is `lambda` with `P lambda>=0` and `beta dot lambda>0`.

These should remain source-independent leaves. Source keys, support/contact identity, and P5 admission belong in separate adapters.

---

## 15. Boundaries and fail-closed conditions

### Boundary A — PSD is essential for the completion lower bound

If `P` is merely copositive on `u>=0` but indefinite on signed vectors, the term `u-Y e` in the completion is signed and may leave the orthant. Ordinary PSD of `P` is therefore the correct premise.

### Boundary B — lack of a monotone solve is not a copositivity failure

Section 6 proves this exactly. Route to the full copositivity checker.

### Boundary C — range-only Schur failure is inconclusive

`K` negative under an arbitrary solve can reflect an infeasible signed minimizer. Only the sufficient direction may be consumed without orthant attainability.

### Boundary D — exact sign is required

A numerically small negative entry of `Y` cannot be rounded to zero. If a runtime/interval producer is used, every nonnegativity claim must be enclosed or replaced by a rational exact witness.

### Boundary E — the block must be the actual inherited reduced block

`P` must be the `U x U` principal block after the same T-P5-178 completion and support/contact canonicalization. A PSD parent block before reduction, a nominal block from another floor, or an unrelated metric cannot be substituted by name or shape.

### Boundary F — external critical-set classification remains exact

Only exact zero-residual rows belong to `E`. Strict-positive rows remain first-order protected; negative rows fail earlier.

### Boundary G — local block descent is not global P5 closure

Other supports, other contacts, parameter cells, path/ODE coverage, source identity, Float64/controller semantics, P8/M4, Lean/kernel, independent `封不觉` validation, admission, registry, and parent closure remain OPEN.

---

## 16. Recommended routing

For a T-P5-179 boundary contact with inherited dropped block `U` and external critical set `E`:

1. perform the true-support descent once;
2. use T-P5-178/T-P5-181/T-P5-180 as appropriate to complete against the true signed-active support;
3. retain the reduced critical matrix on `U sqcup E`;
4. use T-P5-179 to mark `P=H_UU` as inherited PSD;
5. first try the exact rational monotone solve `P Y=-B^T`, `Y>=0`;
6. if it exists, remove `U` losslessly and dispatch only `K=C+B Y`;
7. if only an unsigned range solve exists, use the Schur block only as a sufficient PASS route;
8. if neither closes, leave `U sqcup E` intact for the generic copositivity stack.

The main interface lesson is:

> **signed-active Schur completion and one-sided critical Schur descent are different theorem types; the bridge between them is not ordinary range membership but orthant attainability of the minimizing transport.**
