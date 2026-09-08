---
kind: review_result
review_id: GH-MATH-P4-ADJUGATE-SOURCE-WITNESS-honglianmozun-20260908T1957Z
task_id: GH-MATH-P4-ADJUGATE-SOURCE-WITNESS
source_agent: 红莲魔尊
created_at: 2026-09-08T19:57:00Z
inspected_commit: 36defb1faf7c24cb7fcb79a862be3c8f7ac40f23
claim_commit: e2af894c25c91b3aa85b87ac071321f03095cefd
admission: pending
integration_target: frontier_theorem_and_source_witness
requested_action: retain exact transcribed packet; require noncircular authenticated source packet before SameCellEvidence/source admission
---

## Question

Can the existing signed projected-adjugate theorem be bound to one **actual same-source** descriptor/determinant/projected-numerator/observable packet, without replacing the signed numerator by independent absolute boxes or silently using the desired acceleration cap as an input?

## Inspected evidence

- `examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_AdjugateAcceleration.lean`, blob `28b1477a073e239225be50656d890714cb242be0`.
- `examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_DHProducerBaseBridge.lean`, blob `4cf5f526f18f3368ae5f1fc1dcabb5031ccce6e7`.
- `examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_DHAnalyticAUpper.lean`, blob `86aa5f56ec35734a9ee23241298cbf6b8fac9ae2`.
- `examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_DescriptorPUpper.lean`, blob `0104ede00712086a945da1409845a4edc26c9cec`.

No Lean compile, receipt, provenance promotion, registry mutation, Float64 claim or physical trajectory claim was performed.

## Positive mathematical result: a same-state **transcription-level** diagonal adjugate packet exists

Write

`alpha = 350003/3000000`, `gamma = 200739/4000000`,

and let `g1,g2` be the two components of `nominalForce x`, `r1,r2` the two components of `dhLBase x`, and `u1,u2` the two components of `x.acceleration`.

Expanding the committed definitions gives the exact identities

`alpha*u1 = g1-r1`,

`gamma*u2 = g2-r2`.

Thus the transcribed compact branch can instantiate the abstract 2x2 rows with

`a=alpha`, `b=0`, `c=gamma`, `f1=g1-r1`, `f2=g2-r2`.

The determinant is the positive exact rational

`D = alpha*gamma = 23419750739 / 4000000000000 > 0`.

For every fixed observable coefficients `ell1,ell2`, the signed projected numerator is therefore

`N = gamma*ell1*(g1-r1) + alpha*ell2*(g2-r2)`,

and the exact division-free identity is

`D*(ell1*u1 + ell2*u2) = N`.

This is the correct place to preserve cross-channel cancellation: one should enclosure the single signed scalar `N`, not separately enclosure `|g1-r1|` and `|g2-r2|` and then sum their magnitudes.

Candidate theorem statement:

`dh_transcription_projected_identity :`
`D * (ell1*x.acceleration 0 + ell2*x.acceleration 1)`
`= gamma*ell1*(nominalForce x 0 - dhLBase x 0)`
` + alpha*ell2*(nominalForce x 1 - dhLBase x 1)`.

It is a `ring`/definitional theorem and requires no inverse or square root.

## Exact obstruction 1: this is not yet an authenticated physical descriptor witness

`NEW_P4_032_DHProducerBaseBridge.lean` explicitly labels `dhLBase` as a compact-DH **source transcription**, not an authenticated true-DH equation. Its `ProducerChain.descriptor` premise is a different block equation,

`tailMass * distalCorrection + deltaCross * acceleration = 0`,

and does not provide the two B-row equations needed to identify the above diagonal pair as the deployed physical acceleration solve. The current committed source therefore supplies a mathematically exact transcription identity, but not the required true-source equality for `SameCellEvidence.row1/row2`.

In particular, the packet cannot be promoted merely because the constants `alpha,gamma` occur in the residual definition.

## Exact obstruction 2: the definitional diagonal packet is circular as an acceleration certificate unless `N` is bounded independently

Because the preceding identity is exact and `D>0`, for any `U>=0` one has

`|N| <= D*U  <->  |ell1*u1+ell2*u2| <= U`.

Hence a `numerator_upper` manufactured from an already assumed cap on the same observable acceleration proves nothing new: the projected-adjugate consumer just returns its own premise. This is a precise self-certification loop.

The committed analytic residual bound does not automatically remove this issue: `dh_residual_analytic_upper` itself contains the positive `producerMetric` acceleration term. Any attempt to use it to create `N` must explicitly close that dependence algebraically; it cannot be relabeled as an acceleration-independent RHS envelope.

Candidate obstruction theorem:

`projected_numerator_gate_iff_target_cap_of_exact_identity`

under `0<D` and `N=D*u`, proves

`|N| <= D*U <-> |u| <= U`.

This is the minimal formal guard against circular source packets.

## Exact obstruction 3: observable semantics are still missing

`SameCellEvidence.observable_binding` requires the actual downstream observable to equal `ell1*u1+ell2*u2` on the same domain/cell. The abstract theorem allows arbitrary `ell1,ell2`; the inspected physical/transcription files do not select a deployed observable, its units, or its source key. Defining a new function to equal that linear combination would satisfy the type but would not bind the consumer actually used by P4/P5.

## Minimal noncircular source packet that would close this child

For one fixed cell and source key, provide all of the following from the same physical producer:

1. two authenticated descriptor rows `a*u1+b*u2=f1`, `b*u1+c*u2=f2`;
2. an exact/outward lower bound `delta <= a*c-b^2` with `delta>0`;
3. the actual observable coefficients/units and equality `observable=ell1*u1+ell2*u2`;
4. a signed same-cell enclosure of
   `N=ell1*(c*f1-b*f2)+ell2*(a*f2-b*f1)`
   obtained from source quantities independently of the target observable-acceleration cap;
5. one cell/domain/source identity tying all four items to the same producer revision.

Once these hold, `projected_accel_bound` consumes them directly with the division-free gate `R <= delta*upper`; no coordinatewise acceleration boxes are needed.

## Failure boundary / status

**CONDITIONAL mathematical progress, admission `pending`.** The signed adjugate algebra has a concrete same-state transcription specialization and a positive exact determinant, but the repository evidence inspected here does not provide a noncircular authenticated `SameCellEvidence` packet for the deployed physical descriptor and observable. The missing object is now narrower than “find an acceleration bound”: it is specifically a same-source signed projected-numerator enclosure plus physical row/observable binding. Do not substitute the definitional residual rearrangement or an acceleration-dependent numerator cap for that witness.