kind: review_result
task_id: GH-MATH-P4-DESCRIPTOR-PUPPER
review_id: GH-MATH-P4-DESCRIPTOR-PUPPER-guyuefangyuan-20260908T1552Z
source_agent: 古月方源
agent: 古月方源
status: partial_math_result_blocked_on_same_source_mu_rhs

# GH-MATH-P4-DESCRIPTOR-PUPPER — exact interface and source obstruction

## Scope inspected

I prioritized the coordinator-assigned task and inspected the live target and the closest concrete DH-source bridge:

- `examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_DescriptorPUpper.lean`
- `NEW_P4_032_DHProducerBaseBridge.lean` and its review
- `NEW_P4_032_DHAnalyticAUpper.lean`
- `NEW_P4_032_SameSourceConsumerPacket.lean`
- `NEW_P4_032_SourcePositiveTargetBinding.lean`
- `NEW_P4_032_ActualRowMissingBase.review.md`

No receipt/provenance/admission claim is made here.

## 1. What the target theorem actually needs

For one cell, the target uses the full six-dimensional descriptor equation

`M a = rhs`

and a full-mass coercivity certificate

`mu * ||a||_2^2 <= <a, M a>`, with `mu > 0`.

Writing `H` for a same-cell bound `||rhs||_2^2 <= H`, the existing square-difference argument gives the division-free estimate

`mu^2 * ||a||_2^2 <= H`.

The compact DH producer metric is

`A_up = (1402217/12000000) a4^2 + (200739/4000000) a5^2`.

Because

`200739/4000000 < 1402217/12000000 =: Bmax`,

and `a4^2+a5^2 <= ||a||_2^2`, one gets

`mu^2 * A_up <= Bmax * H`.

This is the core exact interface. It uses only rational arithmetic and order; no inverse, square root, eigenvalue computation, or floating-point maximum is needed by the checker.

## 2. `K_i` is not an independent physical datum

The target currently asks for a rational witness `K_i` satisfying

`Bmax * H_i <= mu^2 * K_i`.

Hence once SAME-SOURCE `mu` and `H_i` are frozen, `K_i` is a certificate witness, not a third independent dynamics constant. A producer may choose the exact real value

`K_i = Bmax * H_i / mu^2`

or any rational enlargement. The trusted side should preferably verify only the cross-multiplied inequality

`Bmax * H_i <= mu^2 * K_i`.

So source search should not waste effort looking for a separately printed `K_i` token.

For a port coefficient `rhoSq_i >= 0`, and rational `P_i` satisfying `rhoSq_i*K_i <= P_i`, the whole cell closes by

`||port||^2 <= rhoSq_i*A_up <= rhoSq_i*K_i <= P_i`.

An even tighter division-free checker can avoid materializing `K_i` at all and check directly

`rhoSq_i * Bmax * H_i <= mu^2 * P_i`.

This follows by multiplying `mu^2*A_up <= Bmax*H_i` by nonnegative `rhoSq_i`, then using `||port||^2 <= rhoSq_i*A_up` and `mu^2>0`.

### Suggested Lean theorem

```lean
theorem same_cell_P_upper_direct
    ...
    (hmu : 0 < mu)
    (hcoercive : mu * fullSq a <= dot6 a (M *ᵥ a))
    (heq : M *ᵥ a = rhs)
    (hH : fullSq rhs <= (H : ℝ))
    (hrho : 0 <= (rhoSq : ℝ))
    (hport : sqNorm (src.port x) <= (rhoSq : ℝ) * metric src x)
    (hP : (rhoSq : ℝ) * metricMax * (H : ℝ) <= mu^2 * (P : ℝ)) :
    sqNorm (src.port x) <= (P : ℝ)
```

The proof is just the existing `full_descriptor_energy_bound`, `metric_le_full`, multiplication by `rhoSq`, and cancellation of positive `mu^2`. This is mathematically stronger/smaller than storing a redundant `K` array.

## 3. What the concrete DH bridge DOES freeze

`NEW_P4_032_DHProducerBaseBridge.lean` freezes the compact branch residual polynomials and exactly the same producer metric coefficients above. It also explicitly keeps the regularized mass matrices and descriptor identities as premises of `ProducerChain`; it does not freeze a six-dimensional full mass matrix/coercivity lower bound.

`NEW_P4_032_DHAnalyticAUpper.lean` gives a useful analytic upper bound on `||dhLBase||^2`, but that bound itself requires an `accelerationCap`/producer-metric cap. Its theorem `no_cap_from_angles_and_block_only` proves that angle/block/disturbance restrictions alone cannot supply such a cap: an unrestricted acceleration ray defeats every finite candidate.

Therefore that file cannot be recycled as the missing `H_i` source for the full descriptor; doing so would be circular.

## 4. Same-source fields still missing

In the repository material inspected this round I did NOT find either of the following frozen on the same physical cell/domain:

1. **Full-mass coercivity `mu`:** a theorem for the actual six-dimensional mass/source object
   `mu * fullSq a <= dot6 a (M a)` with one explicit positive rational `mu`.
2. **Full RHS caps `H_i`:** per-cell rational bounds
   `fullSq (rhs x) <= H_i`
   for the SAME descriptor equation `M a = rhs`.

The `mass_regularizer = 1e-6` token mentioned in the external ledger is not such a theorem and must not be substituted for `mu`. Likewise `SourceView.mu` in `NEW_P4_032_SourcePositiveTargetBinding.lean` is a different front/remainder field; the target file itself correctly warns that its `mu` is full-mass coercivity, not the scalar normalization `nu` or another identically named field.

`NEW_P4_032_ActualRowMissingBase.review.md` independently records that the selected external row supplies coefficients/slack but does not supply the missing same-state base/residual/metric budget. That does not by itself prove the full descriptor impossible; it confirms that the current numerical row is not the missing `mu,H_i` packet.

## 5. Why the missing `H_i` is a genuine mathematical obstruction

The target already contains the correct scalar counterexample. Fix any `mu>0` and any finite proposed acceleration cap `C`. Let

`a = C+1`, `rhs = mu*a`, `M = [mu]`.

Then the descriptor equation and coercivity identity both hold exactly, but `a^2>C`. Thus positive coercivity alone cannot produce an absolute acceleration/port cap. A same-domain RHS restriction is mathematically necessary.

There is an analogous necessity for positive `mu`: from

`mu^2 ||a||^2 <= H`

the acceleration budget scales as `H/mu^2`. Without a frozen strictly positive lower coercivity margin, no finite uniform bound follows from a fixed `H>0`.

## 6. Recommended source-side next step

Do not search for `K_i`. Freeze only the two irreducible SAME-SOURCE packets:

- one explicit rational `mu>0` proving full six-dimensional mass coercivity on the deployed DH target/cells;
- exact rational/dyadic `H_i` proving full squared RHS caps for those same cells.

Then generate either `K_i` by the cross-multiplied gate `Bmax*H_i <= mu^2*K_i`, or better generate `P_i` directly and check

`rhoSq_i * (1402217/12000000) * H_i <= mu^2 * P_i`.

This is the smallest exact route to an absolute `P_upper` and preserves the requested fail-closed semantics.

## Dependencies / non-closures

Depends on the same-source identity between the actual DH acceleration coordinates and `a[3],a[4]`, the actual full descriptor `M a = rhs`, the cell/domain binding, and the existing port inequality. Float64, interval coverage, source authentication, Lean compilation, receipt/provenance, and P4/M4 admission remain outside this result.
