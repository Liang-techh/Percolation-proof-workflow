---
kind: review_result
task_id: T-P4-033
subtask_id: T-P4-033-CORRELATED-METRIC
review_id: T-P4-033-correlated-metric-kuangmanmozun-20260907T1441
source_agent: 狂蛮魔尊
created_at: 2026-09-07T14:41:00-06:00
integration_status: pending
admission: pending
claim_status: claimed
inspected_commit: 6ae939335bff0fcc1bbccb7fc5413a40b5585a59
inspected_paths:
  - agent_review_inbox/README.md
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/collaboration_board.md
  - agent_review_inbox/review-T-P4-033-joint-defect-metric-liuguanyi-20260907T1422.md
  - agent_review_inbox/review-T-P4-033-sumengchen-20260907T1425.md
  - agent_review_inbox/review-T-P4-024-kuangmanmozun-20260907T1248.md
depends_on:
  - T-P4-033
  - T-P4-024
proposed_integration_target: theorem
requested_action: harvest as the exact correlated-scalar specialization between the generic 6x6 joint-metric theorem and the block-diagonal scalar fallback; hand the square identities / sharp iff to the Lean lane without changing any source, coverage, provenance, registry, or admission state
---

# T-P4-033 — exact correlated two-block defect metric closure

## 0. Why this child is disjoint and useful

The current T-P4-033 mathematical review gives the correct generic matrix statement

`C_s^* C_s <= mu W`

and the compiled sidecar gives a sharp **block-diagonal scalar** fallback.  The missing intermediate case is a source metric that retains exactly one scalar D-B correlation coefficient.  Throwing that cross term away before the P4 consumer can lose a large amount of margin; solving a generic generalized eigenproblem is unnecessary in this 2-block scalar case.

This review derives an exact rational-friendly closed form, a division-free square identity, a sharp equality witness, the precise sign-flip rule, and a singular-boundary obstruction.  No deployed-source metric is asserted to satisfy these premises.

## 1. Correlated source metric

Let `H` be a real inner-product space and let `x,y : H`.  Think of `x` as one normalized/transferred distal-defect coordinate in the physical B-space and `y` as the local B-defect coordinate.  Let

`Q(x,y) = alpha ||x||^2 + 2 chi <x,y> + beta ||y||^2`.

Let `s` be a sign with `s^2=1`, and consider the correction

`C_s(x,y) = s tau x + y`.

Define

`D := alpha beta - chi^2`,

`N_s := beta tau^2 - 2 s chi tau + alpha`.

The coercive regime is

`alpha > 0`, `D > 0`.

This already implies `beta>0` and positive definiteness of the scalar two-block metric.

## 2. Two exact square identities

The source metric itself has the division-free completion

`alpha Q(x,y)`
`= ||alpha x + chi y||^2 + D ||y||^2`.        (1)

Hence `Q>=0` whenever `alpha>0` and `D>=0`.

More importantly, using only `s^2=1`,

`N_s Q(x,y) - D ||s tau x + y||^2`
`= ||(alpha - s chi tau)x + (chi - s beta tau)y||^2`.   (2)

This is the exact correlated analogue of the block-diagonal square from the current T-P4-033 sidecar.  It is a pure `ring`/inner-product expansion; no inverse, square root, eigenvalue, or optimizer is needed.

A third scalar identity controls the sign of the coefficient:

`alpha N_s = (alpha - s chi tau)^2 + D tau^2`.          (3)

Under `alpha>0` and `D>0`, (3) gives `N_s>0` automatically.

## 3. Sharp pushforward theorem

Suppose

`alpha>0`, `D>0`, `s^2=1`, and `Q(x,y) <= E`.

Then from (2) and `N_s>0`,

**`D ||s tau x + y||^2 <= N_s E`.**                    (4)

Equivalently,

`||C_s(x,y)||^2 <= mu_* E`,

with the exact coefficient

**`mu_* = N_s / D`
`      = (beta tau^2 - 2 s chi tau + alpha)/(alpha beta-chi^2)`.**   (5)

This coefficient is sharp for the information model `Q<=E`.

Take any nonzero direction `e in H` and set

`x = (s beta tau - chi)e`,

`y = (alpha - s chi tau)e`.

The square on the right of (2) vanishes.  The witness is nonzero because otherwise `D=0`.  Moreover

`C_s(x,y) = N_s e`,

and, using `N_s>0`, equality in (2) gives

`Q(x,y) = D N_s ||e||^2`.

Therefore

`||C_s||^2 / Q = N_s/D = mu_*`.

No smaller universal scalar multiplier is possible.

## 4. Exact scalar PMI iff, without generalized eigenvalues

For scalar coordinates `x,y in R`, define the 2x2 source matrix

`W = [[alpha, chi],[chi,beta]]`

and correction row

`c_s = [s tau, 1]`.

In the coercive regime `alpha>0`, `D>0`, the universal quadratic domination

`mu W - c_s^T c_s >= 0`

is equivalent to the single scalar condition

**`mu D >= N_s`.**                                      (6)

Necessity follows by evaluating the quadratic form at the sharp witness above.  Sufficiency can be proved with no matrix library.  Combining (1) and (2) gives the exact SOS identity

`alpha D [ mu Q(x,y) - (s tau x+y)^2 ]`
`= (mu D-N_s)[ (alpha x+chi y)^2 + D y^2 ]`
`  + alpha [ (alpha-s chi tau)x + (chi-s beta tau)y ]^2`.   (7)

Thus `mu D>=N_s` immediately implies nonnegativity.

For a conventional 2x2 principal-minor proof, note also

`det(mu W-c_s^T c_s) = mu (mu D-N_s)`,

and

`alpha N_s - tau^2 D = (alpha-s chi tau)^2 >=0`,

so (6) automatically supplies the leading-minor condition as well.

This is a useful checker surface: a rational correlated scalar certificate needs only `alpha>0`, `D>0`, and one rational inequality `mu D>=N_s`.

## 5. Block-diagonal fallback is recovered exactly

Setting `chi=0` gives

`D=alpha beta`,

`N_s=alpha+beta tau^2`,

hence

`mu_* = tau^2/alpha + 1/beta`.

This is exactly the coefficient already obtained in T-P4-033 for the separable scalar metric.  The present theorem therefore strictly extends, rather than replaces, the compiled block-diagonal child.

## 6. Correlation can change the cost by a large exact factor

Take the entirely rational example

`alpha=beta=2`, `chi=1`, `tau=1`.

Then `D=3`.

For `s=+1`,

`N_+=2`, so `mu_+=2/3`.

For `s=-1` **if the same cross coefficient is incorrectly copied unchanged**,

`N_-=6`, so `mu_-=2`.

Thus the wrong convention can change the sharp defect multiplier by a factor of exactly `3`.

The block-diagonal discard `chi=0` would give `mu=1`, which lies between them.  Hence correlation is neither automatically beneficial nor automatically harmful; its sign relative to the physical correction map matters.

## 7. Exact force/O1 sign-flip invariance

The T-P4-033 convention theorem says that changing from `s` to `-s` must also flip the D-B cross block.  In this scalar specialization that is exactly

`(s,chi) -> (-s,-chi)`.

Under the simultaneous change,

`D(-chi)=D(chi)`,

`N_{-s}(-chi)=N_s(chi)`.

Therefore the sharp coefficient `mu_*=N/D` is exactly invariant.

If one flips `s` but not `chi`, the numerator changes by

`N_{-s}(chi)-N_s(chi)=4 s chi tau`.

The rational factor-three example above is therefore a concrete under/over-charge witness for copying a correlated metric across defect conventions without congruence.

## 8. Singular boundary: exact obstruction

Assume `alpha>0`, `D=0`.  Then

`alpha N_s = (alpha-s chi tau)^2`.

Take the metric-null direction

`x = chi e`,

`y = -alpha e`.

By (1), `Q(x,y)=0`.  But

`C_s(x,y) = (s chi tau-alpha)e`.

Hence if `N_s>0`, this correction is nonzero on a zero-cost source direction, and **no finite multiplier `mu` can satisfy `||C_s||^2 <= mu Q`**.

The exceptional degenerate case `D=0=N_s` is compatible (`C_s` vanishes on the source kernel) and must be treated separately; this review does not claim impossibility there.

This is the exact 2-block scalar realization of 柳冠一's general `ker(W) subset ker(C_s)` obstruction.

## 9. Direct composition with the fixed-lambda T-P4-024 consumer

Suppose a source/checker eventually proves the correlated metric budget

`Q(x,y) <= E`.

Equation (4) supplies the raw defect budget without first scalarizing the two defect components:

`D ||delta||^2 <= N_s E`.

T-P4-024 can then consume this through its fixed rational `lambda>1`.  A division-free sufficient condition is

**`D (lambda-1) b_base`
`>= D lambda ||l_base||^2 + lambda(lambda-1) N_s E`.**   (8)

Indeed, divide only conceptually by positive `D(lambda-1)` to recover the already-proved T-P4-024 requirement with `R=(N_s/D)E`.

For the preferred `lambda=2` candidate, (8) collapses to

**`D b_base >= 2 D ||l_base||^2 + 2 N_s E`.**            (9)

This gives the source/checker lane a completely rational combined-Schur interface even when the source defect enclosure carries one correlated cross coefficient.

If `E=kappa A+B0`, retain that split:

`D ||delta||^2 <= N_s kappa A + N_s B0`.

A nonzero `B0` remains additive; correlation does not justify relabelling it as a pure `rho A` term on a domain containing `A=0`.

## 10. Formalizable theorem decomposition

Recommended minimal Lean children:

1. `correlated_metric_energy_identity`
   - proves (1).

2. `correlated_metric_pushforward_identity`
   - hypothesis `hs : s^2=1`;
   - proves (2).

3. `correlated_metric_N_positive`
   - uses (3), `0<alpha`, `0<D` to prove `0<N_s`.

4. `correlated_metric_pushforward`
   - premises `0<alpha`, `0<D`, `s^2=1`, `Q<=E`;
   - conclusion `D*||s tau x+y||^2 <= N_s*E`.

5. `correlated_scalar_pmi_iff`
   - scalar `x,y : R` theorem:
     `forall x y, 0 <= mu*Q-(s*tau*x+y)^2` iff `N_s <= mu*D`.
   - the forward direction uses the explicit witness; the reverse direction uses (7).

6. `correlated_metric_sign_flip`
   - proves `N (-s) (-chi)=N s chi` and hence exact multiplier invariance.

7. `correlated_metric_singular_obstruction`
   - uses `(x,y)=(chi,-alpha)` when `D=0` and `N_s>0`.

8. Optional `correlated_combined_schur_lambda`
   - consumes the division-free defect budget and proves (8), delegating the final norm-square step to the already compiled T-P4-024 theorem.

The first three identities should be close to `ring` plus `real_inner`/norm-square expansion.  A scalar-only sidecar can be even smaller if Hilbert-space API friction is undesirable.

## 11. Failure branches and evidence boundary

- `chi` must be a genuine source-bound cross-correlation coefficient in the same coordinates as `x,y`; it cannot be invented by fitting samples.
- The theorem does not turn a raw distal defect `d` into `x=T d` unless the source adapter separately proves that typed map and any normalization used in the metric.
- If only a scalar operator norm for `T` is known and the source metric is on `(d,b)`, a nonzero cross term involving `<d,b>` is generally not transportable through a non-scalar `T` without additional structure.  In that case use the existing block-diagonal fallback or a full matrix `W`.
- `D<=0` is not a coercive source metric.  `D=0,N_s>0` has the explicit kernel counterexample above.
- The factor-three example is an algebraic convention counterexample, not a physical trajectory claim.
- No concrete `alpha,beta,chi,tau,E` is asserted for deployed Route-B, and no Float64/source/interval/coverage premise is supplied.
- No P4/P8/M4 status, theorem registry, provenance/admission state, or final gate is changed.

## 12. Recommended next step

If the source/interval lane can produce a correlated defect enclosure, export one exact tuple

`(alpha,beta,chi,tau,s,E)`

plus its coordinate/source key.  The checker can then consume only

`D=alpha*beta-chi^2 > 0`,

`N=beta*tau^2-2*s*chi*tau+alpha`,

and the one scalar PMI test `mu*D>=N`.

If no trustworthy cross-correlation is available, set `chi=0` and fall back exactly to the already compiled block-diagonal theorem.  Do not estimate a sign-unknown `chi` merely to obtain a smaller multiplier.

**Result:** the correlated two-block scalar case is now closed sharply and division-free.  It quantifies exactly when correlation buys margin, when the convention sign flips it, and when a singular source metric makes any finite multiplicative defect budget impossible.  Status remains `pending`;待封不觉独立验证 / 待梁智炜最终整合。
