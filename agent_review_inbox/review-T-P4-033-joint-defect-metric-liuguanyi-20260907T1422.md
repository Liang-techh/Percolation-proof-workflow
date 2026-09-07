kind: review_result
review_id: review-T-P4-033-joint-defect-metric-liuguanyi-20260907T1422
task_id: T-P4-033
related_task_ids:
  - T-P4-032
  - T-P4-024
source_agent: 柳冠一
created_at: 2026-09-07T14:22:00-06:00
inspected_commit: 19200c3d4c0a8ccc5f071bd1a2027188f47e74e1
inspected_paths:
  - agent_review_inbox/README.md
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/collaboration_board.md
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_DefectConvention_REVIEW.md
  - agent_review_inbox/review-T-P4-024-kuangmanmozun-20260907T1248.md
admission: pending
proposed_integration_target: theorem
requested_action: harvest as a source-independent P4 defect-metric bridge; hand only the small PSD/congruence lemmas to 巨阳仙尊 if desired, while keeping concrete source metric, left-inverse, interval/coverage and admission obligations open

# T-P4-033 — joint defect metric pushforward and convention-safe Schur bridge

## 1. Bottleneck

The newly harvested T-P4-032 typed adapter makes the correction term precise, but there are now two equivalent-looking defect conventions that must not be silently identified:

- force-side correction: `delta_F = e_B - T e_D`,
- O1 correction: `delta_O = T d_O + b_O`,

with `T = M_BD M_DD_inv`.

T-P4-032 already established that a full balance adapter is not the same thing as merely copying or sign-flipping two defect fields. T-P4-024, separately, can consume any proven squared residual budget `||r||^2 <= R`.

The smallest missing mathematical interface is therefore:

**how a source-level joint quadratic budget on the typed defect pair is pushed through the linear correction map into the B-port squared residual budget, without prematurely replacing the pair by separate scalar Young charges.**

This is especially relevant when interval/source evidence has correlation, a weighted norm, or a coordinate normalization. A separable three-term bound discards that structure.

No source equality, numerical interval, Lean compilation, receipt, provenance, coverage, registry or admission claim is made below.

## 2. Exact joint-metric theorem

Let `D` and `B` be finite-dimensional real inner-product spaces and let

`T : D -> B`.

For a sign `s in {+1,-1}`, define the typed defect correction map

`C_s(d,b) = s T d + b`.

Thus:

- O1 uses `s=+1`,
- force-side uses `s=-1`.

Let `z=(d,b)` and let `W` be any symmetric positive-semidefinite quadratic source metric on `D x B`. Suppose the source layer proves

`<z, W z> <= E`.

If a nonnegative scalar `mu` satisfies the quadratic-form inequality

`C_s^* C_s <= mu W`,

meaning

`<z, (mu W - C_s^* C_s) z> >= 0` for every `z`,

then immediately

`||C_s z||^2 <= mu E`.

The proof is one line:

`||C_s z||^2 = <z,C_s^*C_s z> <= mu <z,Wz> <= mu E`.

This is the recommended abstract theorem surface. It has no square root, no matrix inverse, no spectral norm and no state-dependent optimization. If `T`, `W` and `mu` are rational matrices/scalars, the source-facing checker only has to certify the rational PSD matrix

`mu W - C_s^* C_s`.

For the actual 4+2 P4 defect dimensions this is a fixed 6x6 PSD problem, not a large SOS problem.

## 3. Sharpness and the singular-metric obstruction

When `W` is positive definite, the least admissible coefficient is exactly

`mu_* = sup_{z != 0} ||C_s z||^2 / <z,Wz>`.

Equivalently, it is the largest generalized eigenvalue of the pair `(C_s^*C_s, W)`. The matrix condition above is therefore not merely sufficient; with the optimal `mu` it is exact.

This also exposes a useful obstruction when `W` is only semidefinite. If there exists a nonzero `z` with

`W z = 0` but `C_s z != 0`,

then no finite `mu` can satisfy `C_s^*C_s <= mu W`. Indeed the right-hand quadratic form is zero on that vector while the left-hand side is strictly positive.

Hence every singular source metric used for a pure multiplicative defect budget must satisfy the necessary condition

`ker(W) subset ker(C_s)`.

This is the joint-metric analogue of the earlier P5 zero-damping-direction obstruction: an uncharged source direction cannot produce a nonzero physical port correction.

## 4. Exact coordinate-congruence theorem

Let `P` be any invertible change of defect coordinates and set

`z = P z'`,
`W' = P^* W P`,
`C' = C_s P`.

Then

`mu W' - C'^* C' = P^* (mu W - C_s^* C_s) P`.

Therefore

`C_s^*C_s <= mu W`

holds iff

`C'^* C' <= mu W'`.

The physical residual bound is thus invariant under a typed defect-coordinate change **only if the source metric and the correction map are transformed together**. This is the precise normalization rule behind the adapter; changing only the defect vector labels or only the coefficient matrix is not coordinate equivalence.

This theorem is particularly useful for the force-side/O1 sign convention.

## 5. Force-side versus O1 sign flip: the cross block must flip too

Consider the correction-only relation explicitly isolated in the T-P4-032 convention review:

`d_O = -e_D`,
`b_O = e_B`.

Define

`J = diag(-I_D, I_B)`.

Then

`z_O = J z_F`,

and

`C_+ J = C_-`,

because

`[T, I] diag(-I,I) = [-T,I]`.

Suppose the force-side source metric is block-partitioned as

`W_F = [[W_D, X], [X^*, W_B]]`.

The equivalent O1 metric is not generally the same matrix. Congruence gives

`W_O = J^* W_F J = [[W_D, -X],[-X^*,W_B]]`.

Therefore every distal/port cross-correlation block changes sign under the correction-only convention flip.

This yields a concrete interface warning:

**if a joint metric contains nonzero D-B cross terms, one may not copy that metric unchanged from force-side defect coordinates into O1 defect coordinates.**

The copied matrix represents a different source assumption.

The exception is exactly the common separable case `X=0`. Then `W_O=W_F`, which explains why componentwise or block-diagonal norm budgets are insensitive to the `+T d` versus `-T d` convention even though a correlated quadratic budget is not.

This is also why T-P4-032 was correct to keep the two defect structures as distinct types.

## 6. Sharp scalar-metric corollary without square roots

A very source-friendly special case is a block-diagonal scalar metric. Assume

`alpha > 0`, `beta > 0`,

`alpha ||d||^2 + beta ||b||^2 <= E`,

and a transfer bound

`||T d||^2 <= tau^2 ||d||^2`, with `tau >= 0`.

Then for either sign `s=+1` or `s=-1`,

`alpha beta ||s T d + b||^2 <= (beta tau^2 + alpha) E`.

Equivalently,

`||s T d + b||^2 <= (tau^2/alpha + 1/beta) E`.

The division-free proof is worth recording because it is exact-rational friendly. Let `x=||d||` and `y=||b||`. By triangle inequality and the transfer bound,

`||sTd+b|| <= tau x + y`.

The scalar identity

`(beta tau^2 + alpha)(alpha x^2 + beta y^2) - alpha beta (tau x + y)^2`

`= (alpha x - beta tau y)^2 >= 0`

gives the result immediately.

Given only the scalar operator bound `tau` and the weighted source energy `(alpha,beta)`, the coefficient

`tau^2/alpha + 1/beta`

is sharp whenever the top transfer direction is attained: choose `d` in a maximizing singular direction, choose `b` parallel to `sTd`, and impose `alpha||d|| = beta tau ||b||` so the final square vanishes.

Thus this corollary is not a looser reformulation of two successive arbitrary Young inequalities; it is the optimal scalar-metric pushforward for the available information.

## 7. Relative-plus-additive source budget

If the source/interface layer can prove the joint metric budget in the form

`<z,Wz> <= kappa A + B0`,

then the matrix theorem gives directly

`||C_s z||^2 <= mu kappa A + mu B0`.

This preserves the same relative/additive split already needed elsewhere in Route-B:

- if `B0=0`, the joint defect correction becomes a pure relative port-energy term and can be folded into the existing P4 `rho A` lane;
- if `B0>0`, the additive charge must remain explicit and cannot be relabelled as `rho A` on a domain containing `A=0`.

For the scalar metric, the division-free form is

`alpha beta ||C_s z||^2 <= (beta tau^2+alpha)(kappa A+B0)`.

This is convenient for a rational checker because it avoids dividing by `alpha beta` until a downstream consumer actually needs the normalized coefficient.

## 8. Connection to T-P4-024 without duplicating it

Let the full O1 residual be

`r_B = u + delta`,

where

`u = R_port a_B`

and

`delta = T e_D + e_B`.

T-P4-033 should stop after producing a typed squared budget

`||delta||^2 <= R_def`.

The already completed T-P4-024 theorem can then combine `u` and `delta` using its fixed rational `lambda`/Young-Schur surface. There is no reason to re-prove that combined-Schur theorem here.

If future source evidence instead provides one genuinely joint quadratic metric on `(a_B,e_D,e_B)`, the same pushforward principle applies with the larger linear map

`L = [R_port, T, I]`.

Then `L^*L <= mu W_full` gives a direct one-shot residual budget. This is a valid future strengthening, but the current minimal child should keep the already separate nominal-port and defect-source lanes intact.

## 9. Why this is better than immediate three-term scalarization

The T-P4-032 weighted-three-term theorem remains the correct fallback when all source evidence is separate scalar norm caps. In that information model it is already sharp in the worst case because all vectors may align.

T-P4-033 adds value only when the source layer knows more:

- a correlated quadratic enclosure of `(e_D,e_B)`,
- a weighted metric arising from a solve residual or interval Jacobian,
- a normalization transform that should be propagated by congruence,
- or a block structure that makes `mu W-C^*C` easier/tighter than independent norm charging.

In those cases, collapsing to `||T e_D||` and `||e_B||` separately destroys cross information before the P4 consumer sees it.

## 10. Suggested minimal theorem statements

The Lean/math adapter can be split into very small source-independent lemmas.

1. `joint_metric_pushforward`

   Premises: `W` symmetric PSD, `mu>=0`, and quadratic-form nonnegativity of `mu W-C^*C`.

   Input budget: `<z,Wz> <= E`.

   Conclusion: `||Cz||^2 <= mu E`.

2. `joint_metric_congruence`

   Statement:

   `P^*(mu W-C^*C)P = mu(P^*WP) - (CP)^*(CP)`.

   No positivity theorem is needed beyond applying a PSD form to `Pz`.

3. `defect_sign_flip_metric`

   For `J=diag(-I_D,I_B)`, prove

   `C_+ J=C_-`

   and the block identity

   `J^* [[W_D,X],[X^*,W_B]] J = [[W_D,-X],[-X^*,W_B]]`.

4. `scalar_weighted_defect_pushforward_mul`

   Under `alpha,beta>0` and `||Td||^2<=tau^2||d||^2`, prove the division-free inequality

   `alpha*beta*||sTd+b||^2 <= (beta*tau^2+alpha)*(alpha||d||^2+beta||b||^2)`.

5. Optional `singular_metric_kernel_obstruction`

   If `<z,Wz>=0` and `Cz!=0`, conclude no finite `mu` can satisfy the universal quadratic domination `C^*C<=mu W`.

No matrix inverse construction is required by these lemmas; `T` is an already typed linear map supplied by the O1/source adapter.

## 11. Dependencies and unresolved boundaries

Mathematical dependencies used here are only finite-dimensional linear maps, adjoints/quadratic forms, congruence, triangle inequality and one scalar square identity.

Still open outside this result:

- proof that the concrete deployed/source defect pair equals either typed force-side or typed O1 variables;
- proof of the actual `T=M_BD M_DD_inv` source identity and left-inverse/solve semantics on the same domain;
- a concrete source/interval joint metric `W` or scalar `(alpha,beta,tau)` with exact coordinate ordering;
- Float64/controller/solve error semantics and whether their enclosure is correlated or separable;
- the reference-state terms in the full T-P4-032 adapter; the correction-only sign flip is not a substitute for the full balance adapter;
- fixed-cell/domain coverage and all remaining P4/P8/M4 physical obligations;
- Lean compilation, axioms/comparator receipts and any registry/admission action.

## 12. Admission boundary

`pending` mathematical/interface child only.

The exact pushforward, sign-convention congruence, singular-metric obstruction and scalar sharp corollary are proved algebraically, but no concrete Route-B source metric or domain has been bound and no kernel verification was performed.
