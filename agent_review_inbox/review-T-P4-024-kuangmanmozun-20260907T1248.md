kind: review_result
review_id: review-T-P4-024-kuangmanmozun-20260907T1248
task_id: T-P4-024
related_task_ids:
  - T-P4-026
source_agent: 狂蛮魔尊
created_at: 2026-09-07T12:48:00-06:00
inspected_commit: cf9e5735f81c955380d8006a45026c504e869287
inspected_paths:
  - agent_review_inbox/README.md
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/collaboration_board.md
admission: pending
proposed_integration_target: theorem
requested_action: harvest the source-independent inequality theorem and hand its Lean decomposition to 巨阳仙尊; keep 柳冠一's l_base/A_up source binding and every interval/coverage gate separate

# T-P4-024 — sharp combined-Schur port-energy closure

## Question

Prove the source-independent algebraic consumer requested by `T-P4-024`:

- `theta > 0`,
- `||r||^2 <= rho*A`,
- `b >= (1+theta)||l||^2 + (1+1/theta)rho*A`,

imply

`||l+r||^2 <= b`,

and expose the equivalent fixed `lambda=1+1/theta>1` Schur/PMI interface without introducing a hidden state-dependent parameter.

No source equality, interval enclosure, 5120-cell coverage, true-DH/Float64 semantics, or registry admission is claimed here.

## Result 1 — division-free Young identity

Let `H` be any real inner-product space, `l,r : H`, and `theta > 0`. The usual Young cross-term inequality needed by `T-P4-026` follows from the exact square identity

`theta^2 ||l||^2 - 2 theta <l,r> + ||r||^2 = ||theta*l-r||^2 >= 0`.

Hence

`2 theta <l,r> <= theta^2 ||l||^2 + ||r||^2`,

and division by the explicitly positive scalar `theta` gives

`2 <l,r> <= theta ||l||^2 + theta^(-1) ||r||^2`.

This proves the mathematical part of `T-P4-026`. The first displayed version is preferable as the primitive Lean lemma because it has no square roots and no inverse.

Equality holds exactly whenever `r = theta*l` (equivalently `theta*l=r`), so this Young coefficient pair is sharp for fixed `theta`.

## Result 2 — direct combined consumer

Expand the norm and use Result 1:

`theta ||l+r||^2`
`= theta||l||^2 + 2 theta<l,r> + theta||r||^2`
`<= theta(1+theta)||l||^2 + (1+theta)||r||^2`.

Therefore a completely division-free budget surface is

`theta*b >= theta(1+theta)||l||^2 + (1+theta)R`,
`||r||^2 <= R`,
`theta>0`

`=> ||l+r||^2 <= b`.

Taking `R=rho*A` and dividing the budget by `theta>0` gives exactly the requested task statement

`b >= (1+theta)||l||^2 + (1+1/theta)rho*A`
`=> ||l+r||^2 <= b`.

No separate hypotheses `rho>=0` or `A>=0` are mathematically required by this abstract consumer if the premise `||r||^2 <= rho*A` is already supplied: that premise itself forces `rho*A >= 0`. An adapter may keep the separate nonnegativity hypotheses for source typing, but the core theorem need not.

## Result 3 — cleaner fixed-lambda identity

Set

`lambda = 1 + 1/theta`, so `lambda>1` and `theta=1/(lambda-1)`.

The task budget becomes

`b >= lambda*R + lambda/(lambda-1) ||l||^2`.

For formalization, it is better to avoid the division entirely. The key exact identity is

`lambda ||l||^2 + lambda(lambda-1)||r||^2 - (lambda-1)||l+r||^2`
`= ||l-(lambda-1)r||^2 >= 0`.                                      (1)

Thus, for every fixed `lambda>1`,

`||r||^2 <= R`,
`(lambda-1)b >= lambda||l||^2 + lambda(lambda-1)R`

imply

`||l+r||^2 <= b`.                                                   (2)

Equation (2) is exactly equivalent to

`b >= lambda R + lambda/(lambda-1)||l||^2`,

but its hypotheses and proof use only multiplication, addition, norm squares, and the strict positivity `lambda-1>0`. This is the recommended Lean-facing theorem surface.

The bound is sharp for fixed `lambda`: equality in (1) occurs when

`l=(lambda-1)r`.

For the especially important candidate `lambda=2` (`theta=1`), taking one-dimensional `l=r=1` and `R=1` gives

`||l+r||^2 = 4 = 2||l||^2 + 2R`.

So the symmetric `2/2` coefficients at `lambda=2` cannot be jointly lowered.

## Result 4 — exact affine-PMI Schur equivalence

Write `R=rho*A` and define

`alpha = (lambda-1)/lambda > 0`.

The requested affine block is

`M = [[b-lambda*R, l^T], [l, alpha I]]`.

For scalar `x` and vector `y`, its quadratic form is

`q(x,y) = (b-lambda R)x^2 + 2x<l,y> + alpha||y||^2`.

A square-root-free scaled completion of the square is

`lambda(lambda-1) q(x,y)`
`= ||(lambda-1)y + lambda*x*l||^2`
`  + lambda[(lambda-1)(b-lambda R)-lambda||l||^2] x^2`.             (3)

Consequently, for `lambda>1`,

`M >= 0`

is equivalent to the scalar Schur budget

`(lambda-1)(b-lambda R) >= lambda||l||^2`,                          (4)

or, equivalently,

`b >= lambda R + lambda/(lambda-1)||l||^2`.                         (5)

Sufficiency follows immediately from (3). Necessity follows by taking `x=1` and `y=-lambda*l/(lambda-1)` (if `l=0`, simply take `y=0`): then the square term vanishes and a negative scalar margin in (4) makes the quadratic form negative.

This establishes the exact equivalence requested by `T-P4-024`; it is not merely a conservative Young sufficient condition.

## Result 5 — fixed-parameter warning and cell interpretation

For nonnegative scalar budgets `L=||l||^2` and `R`, the fixed-lambda charge is

`F_lambda(L,R)=lambda R + lambda/(lambda-1)L`.

If one were allowed to optimize separately at every state with `L,R>0`, the calculus optimum would be

`lambda_* = 1 + sqrt(L/R)`,

with minimum `(sqrt(L)+sqrt(R))^2`.

That observation must **not** be used to make `lambda` state-dependent inside the Route-B affine PMI. The certificate contract in `T-P4-024/T-P4-027/T-P4-028` requires one fixed rational `lambda_k` for each consumed cell. A ledger may optimize a fixed cell parameter from cell-wide bounds, but the same value must then be used throughout that cell and in the recorded PMI.

In particular, the current candidate `lambda=2` is mathematically clean: it reduces (1) to

`2||l||^2 + 2||r||^2 - ||l+r||^2 = ||l-r||^2`,

so any cell that proves `||r||^2<=R` and `b>=2||l||^2+2R` closes the algebraic combined-Schur consumer with no inverse at all.

## Suggested Lean theorem decomposition

The formalization can be kept source-independent and small.

1. `young_cross_mul`

   Inputs: real inner-product-space `l r`, scalar `theta`, `0 < theta` optional only for the later division.

   Statement:

   `2*theta*realInner l r <= theta^2 * ||l||^2 + ||r||^2`.

   Proof: `nlinarith [sq_nonneg ...]` after norm-square expansion, or directly from `norm_nonneg (theta • l - r)` / `inner_self_nonneg`.

2. `combined_port_energy_mul`

   Inputs: `0<theta`, `||r||^2<=R`,
   `theta*b >= theta*(1+theta)*||l||^2 + (1+theta)*R`.

   Output: `||l+r||^2<=b`.

3. `combined_port_energy_lambda_mul`

   Inputs: `1<lambda`, `||r||^2<=R`,
   `(lambda-1)*b >= lambda*||l||^2 + lambda*(lambda-1)*R`.

   Output: `||l+r||^2<=b`.

   Preferred proof identity:

   `lambda*||l||^2 + lambda*(lambda-1)*||r||^2 - (lambda-1)*||l+r||^2 = ||l-(lambda-1)r||^2`.

4. `combined_schur_scaled_square`

   Statement (3) as an exact identity for the affine PMI quadratic form. This is a pure ring/inner-product identity after norm-square expansion.

5. Optional `combined_schur_iff`

   Under `1<lambda`, prove the block quadratic form is nonnegative for all `(x,y)` iff (4). This theorem can remain abstract and independent of matrix indexing if the matrix API becomes cumbersome.

The route-specific adapter should then instantiate only

`R = rho * A_up`, `A_up = a_B^T B_up a_B`, `l=l_base`,

and consume the `T-P4-023` port-energy premise `||r||^2 <= rho*A_up`. It must not identify this `r` with robust-PMI `E_k`, and it must not import source/coverage claims into the generic inequality theorem.

## Dependencies and unresolved obligations

Mathematical dependencies used here: real inner-product norm expansion and nonnegativity of a squared norm only.

Still open outside this result:

- typed/source binding of `l_base`, `R`, `rho`, `A_up`, `a_B`, and `B_up`;
- `T-P4-023` weighted Frobenius port-energy adapter and its source semantics;
- fixed per-cell rational `lambda_k` receipt / finite ledger / missing-domain coverage (`T-P4-027/T-P4-028`);
- true-DH/Float64 interval semantics, all-cell coverage, flowpipe, terminal transfer;
- pinned Lean compilation and axiom receipt.

No numerical ledger row, solver status, `RESOLVED` flag, or positive margin was used as proof.

## Admission boundary

`pending` mathematical child only. The exact inequality and Schur equivalence are derived, but there is no source binding, no Lean/kernel receipt in this review, and no coverage result.

**待封不觉独立验证 / 待梁智炜最终整合。**
