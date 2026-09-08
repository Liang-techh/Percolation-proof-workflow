---
kind: review_result
agent: 柳冠一
source_agent: 柳冠一
task_id: T-P4-ACTIVE-ENERGY-ORIGIN
status: pending
created_at: 2026-09-07T19:00:00-06:00
claim_commit: e352e72d92eb6dfd19bd275ccf0a44c699bdc5a2
scope: mathematics/source-interface only
---

# T-P4-ACTIVE-ENERGY-ORIGIN — anchored gauge-equivalence bridge

## 1. Result in one sentence

The correct mathematical object for moving a physical potential into the current normalized active-energy expression is **not raw potential equality**, but equality modulo an additive constant on the connected/source-covered component; equivalently, equality of the anchored differences

`U₂(q) - U₂(q₀) = U₁(q) - U₁(q₀)`.

This `gauge equivalence` is exactly necessary and sufficient for equality of the normalized storages with common kinetic/controller terms.  It can be proved from derivative equality plus one certified segment/cell-chain connection, and its approximate version produces an explicit one-sided storage-transfer budget instead of silently changing the `V ≤ 1` threshold.

This is a mathematical child only.  It does **not** identify the currently active external `V`, and it does not turn the inspected raw/shifted energy formulas into the active candidate.

## 2. What was already present, and the remaining mathematical gap

The current source leaves already separate three facts correctly:

1. `normalizedEnergy M U kp linear q v = K(q,v) + U(q) - U(0) + Uctrl(q)` has value zero at `(q,v)=(0,0)`;
2. adding an arbitrary constant `beta` changes the origin value to `beta`, so derivative identities alone do not settle `V(0,0) ≤ 1`;
3. a pointwise binding `V 0 0 = normalizedEnergy ... 0 0` is sufficient for the BODY6 origin witness, while a scalar initial estimate for another storage is not.

The missing bridge is what source mathematics would be sufficient when two *physical potential formulas* differ by a reference convention.  The inspected exact numbers make this relevant: the raw Fourier-style gravity expression and the exact-real DH origin potential ledger have different absolute origin values.  That mismatch by itself neither proves nor disproves equality of the corresponding forces; it is a gauge/reference issue until a cross-domain relation is supplied.

The result below gives the minimal relation that downstream normalized storage actually needs.

## 3. Typed mathematical contract: gauge equivalence

Let `X` be a real affine/vector state space, let `D ⊆ X`, and fix an anchor `a ∈ D`.  For scalar functions `U₁,U₂ : X → ℝ`, define

`GaugeEq(a,D,U₁,U₂) :⇔ ∀ x∈D, U₂(x)-U₂(a) = U₁(x)-U₁(a)`.

Also define the raw offset relation

`OffsetEq(D,U₁,U₂,β) :⇔ ∀ x∈D, U₂(x)=U₁(x)+β`.

### Lemma A — gauge/offset equivalence

Assume `a∈D`.  Then

`GaugeEq(a,D,U₁,U₂)`

is equivalent to

`OffsetEq(D,U₁,U₂, U₂(a)-U₁(a))`.

**Proof.**  From gauge equality,

`U₂(x)-U₂(a)=U₁(x)-U₁(a)`

rearranges to

`U₂(x)=U₁(x)+[U₂(a)-U₁(a)]`.

The converse is the same identity with the constant subtracted at `x` and at `a`.  No calculus, topology, positivity, or source semantics are used.

This is the exact place where an additive reference constant belongs.  It should not be encoded by pretending two raw potentials are definitionally equal.

## 4. Normalization theorem: the additive constant disappears exactly once

Let `K : X×Y → ℝ` be a common kinetic term and `C : X → ℝ` a common controller/storage term.  Define anchored energies

`E₁(x,v) = K(x,v) + U₁(x)-U₁(a) + C(x)`

`E₂(x,v) = K(x,v) + U₂(x)-U₂(a) + C(x)`.

### Theorem B — normalized storage equality iff gauge equality

For every `x∈D` and every `v`,

`GaugeEq(a,D,U₁,U₂)  ⇒  E₂(x,v)=E₁(x,v)`.

Conversely, if the two displayed normalized storages are equal for each `x∈D` for even one common choice of `v=v(x)` (same `K` and `C` on both sides), then `GaugeEq(a,D,U₁,U₂)` follows by cancellation.

So, for this storage template, gauge equivalence is not merely sufficient; it is the **exact interface property** seen by the normalized-energy consumer.

In particular, if `U₂=U₁+β` on `D`, the normalized storages are identical for every `β`.  The raw constant must therefore be removed **once**, by the explicit `U(q)-U(a)` normalization.  A downstream adapter must not subtract it again.

This clarifies the current origin-value mismatch: different raw origin values are harmless *only if* the active candidate is explicitly bound to an anchored normalized storage and the two potential formulas are proved gauge-equivalent on the required domain.  The current raw/recorded-shift expressions are not thereby reinterpreted as normalized; their fixed-threshold origin values remain what the existing source leaf computed.

## 5. How to prove gauge equivalence without demanding raw function equality

A source may naturally know force/derivative identities rather than absolute potential equality.  The missing constant can be handled mathematically, but connectedness/path coverage is essential.

For `x∈D`, suppose we have a certified finite chain

`ξ⁰=a, ξ¹, …, ξᴿ=x`.

On segment `r`, let

`γᵣ(t)=ξʳ + t(ξʳ⁺¹-ξʳ)`, `0≤t≤1`,

and define the scalar offset along the segment

`φᵣ(t)=U₂(γᵣ(t))-U₁(γᵣ(t))`.

Assume every segment stays in a source region on which `φᵣ` is continuous on `[0,1]` and differentiable on `(0,1)`.

### Theorem C — exact finite-chain derivative transport

If

`φᵣ'(t)=0`

for every segment and every interior `t`, then

`U₂(x)-U₁(x)=U₂(a)-U₁(a)`.

Hence a certified chain from `a` to every `x∈D` proves `GaugeEq(a,D,U₁,U₂)`.

**Proof.**  On each segment the one-dimensional mean-value theorem gives

`φᵣ(1)=φᵣ(0)`.

Telescoping over the finite chain gives

`(U₂-U₁)(x)=(U₂-U₁)(a)`.

No multivariate integration theorem is required in the trusted consumer.

This is the storage analogue of the already useful cell-chain transport principle: global convexity is unnecessary.  A union of source cells is acceptable provided the source supplies an actual connecting chain and the derivative relation is valid on every traversed segment.

### Why the path premise cannot be dropped

Derivative equality on a disconnected covered set does not fix one global constant.  For example, on two disjoint components one may take `U₂-U₁=0` on the component containing `a` and `U₂-U₁=2` on the other; the derivative vanishes on both components, but there is no global gauge equality relative to `a`.  Therefore `same derivative on each covered cell` plus `endpoints covered` is not enough unless the cells are connected by a certified overlap/path chain.

## 6. Quantitative version: derivative mismatch becomes a storage budget

The exact derivative premise is stronger than necessary for a one-sided barrier transfer.

Assume instead that segment `r` satisfies

`|φᵣ'(t)| ≤ εᵣ`

throughout `(0,1)`.  The mean-value theorem gives

`|φᵣ(1)-φᵣ(0)| ≤ εᵣ`.

Telescoping and the triangle inequality yield

`|(U₂(x)-U₂(a)) - (U₁(x)-U₁(a))| ≤ Σᵣ εᵣ`.

Therefore the corresponding normalized energies satisfy

`E₂(x,v) ≤ E₁(x,v) + Σᵣ εᵣ`.

If a uniform source-side chain budget `Σᵣ εᵣ ≤ δ` is certified on the transfer domain, this directly instantiates the existing mathematical shape

`OneSidedComparison src dst scope δ`.

Consequently a source barrier `E₁≤cap` transfers to the active threshold `E₂≤1` whenever

`cap + δ ≤ 1`.

No arbitrary constant `β` appears in this normalized comparison: each potential subtracts its own anchor, so the constant cancels.  Only nonconstant mismatch is charged.

A common differential form is also immediate.  If on segment `r`

`||D(U₂-U₁)(γᵣ(t))||_* ≤ Lᵣ`

and the segment displacement has norm `dᵣ=||ξʳ⁺¹-ξʳ||`, then by duality one may take

`εᵣ = Lᵣ dᵣ`,

hence

`|E₂-E₁| ≤ Σᵣ Lᵣ dᵣ`.

This is a useful source contract for interval/Jacobian evidence: it turns a derivative enclosure plus a certified cell chain into a scalar storage-comparison budget without ever selecting an arbitrary absolute potential reference.

## 7. Exact logical hierarchy for the BODY6 origin obstruction

For the particular one-point BODY6 obstruction, global gauge equivalence is stronger than necessary.  The obligations should be kept at three levels:

### Level 0 — origin only (minimal)

To prove `0 ∈ activeQDomain V`, it is enough to supply

`V(0,0) ≤ 1`.

No derivative, connectedness, or global storage theorem is needed.

### Level 1 — bind to the explicit normalized candidate

If the actual typed candidate supplies

`V(0,0) = normalizedEnergy(M,U,kp,linear)(0,0)`,

then the existing algebraic normalization gives `V(0,0)=0≤1`.  This is currently the cleanest minimal source payload for the BODY6 origin witness.

A weaker one-sided point binding also suffices:

`V(0,0) ≤ normalizedEnergy(...)(0,0)+δ`

with `δ≤1`.

### Level 2 — reuse a normalized storage on a whole domain

If the goal is to reuse initial bounds, barriers, coercivity or trajectory statements between two storage constructions, then use `GaugeEq` or the quantitative chain theorem above.  A scalar `V0` match, a hash match, or a derivative identity without a connecting-path/constant treatment is not a substitute.

This prevents an origin-only necessity from being accidentally inflated into a global provenance task, while still giving the global bridge when the later P4 barrier consumer actually needs it.

## 8. Interaction with the currently inspected source definitions

The source leaf defines

`normalizedEnergy = kinetic + U(q)-U(0) + controller`.

The theorem above means that a future source proof relating `sourcePotential` and the Fourier/audited gravity potential does **not** need to prove equality of their absolute values.  It may instead prove their difference is constant on the relevant connected/source-covered component, or prove equality of the derivative of their difference along a certified chain.  Then their normalized potential parts are exactly equal.

However, the current `sourceG` object in `NEW_BODY6_SLICE_CANDIDATEDOMAIN20260907.lean` is a fixed-step central finite-difference construction.  Its equality to an analytic derivative must **not** be assumed.  A theorem about `sourceG` values at shifted points is not automatically the derivative premise of Theorem C.  The source lane must either:

- prove an analytic potential derivative identity for the actual potential formulas, or
- supply an interval bound for the true segment derivative of their difference, using the quantitative theorem, or
- bypass derivatives entirely and provide pointwise `GaugeEq` / `OneSidedComparison` evidence.

This is a typed mathematical boundary, not a provenance issue.

## 9. Minimal formalization statements recommended

The pure algebra should be formalized first; none of it needs calculus:

1. `gaugeEqAt_iff_constantOffset`
   - assumptions: `a∈D`;
   - conclusion: anchored-difference equality iff `U₂=U₁+β` on `D` with `β=U₂(a)-U₁(a)`.

2. `normalizedEnergy_congr_of_gaugeEqAt`
   - same `M/kinetic`, same controller coefficients, same anchor;
   - conclusion: normalized energies coincide on `D`.

3. `normalizedEnergy_comparison_of_gaugeError`
   - premise `|(U₂(x)-U₂(a))-(U₁(x)-U₁(a))|≤δ`;
   - conclusion `E₂(x,v)≤E₁(x,v)+δ`.

Then add a one-dimensional bridge whose consumer does not know multivariate calculus:

4. `segment_offset_bound_of_deriv_bound`
   - input is already the composed scalar function `φ : ℝ→ℝ`;
   - continuity on `[0,1]`, differentiability on `(0,1)`, `|φ'|≤ε`;
   - conclusion `|φ(1)-φ(0)|≤ε`.

5. `chain_gaugeError_le_sum`
   - finite telescoping composition of (4).

The source adapter can separately prove that its multivariate potential/Jacobian evidence instantiates each scalar segment premise.  This separation avoids forcing the active-energy theorem to depend on a large Fréchet-derivative or interval API.

## 10. Minimal obstruction / sharpness statements

Two negative controls should accompany the interface:

- **No anchor/normalization:** `U₁=0`, `U₂=2` have identical derivatives everywhere, but a fixed `≤1` raw-energy threshold changes.  Thus derivative equality alone cannot identify an unnormalized storage.
- **No connecting chain:** equal derivatives on separate components permit different constants per component.  Thus cellwise derivative equality cannot be upgraded to one global gauge class without a path/overlap relation.

For normalized storages, the quantitative coefficient `Σ εᵣ` is worst-case sharp given only per-segment scalar derivative caps: choose every segment derivative with the same sign and magnitude `εᵣ`.

## 11. Dependencies and nonclaims

Mathematical/source-interface dependencies inspected this round:

- `examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_ACTIVEENERGYORIGIN20260907.lean`
- `examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_ACTIVEENERGYORIGIN20260907.review.md`
- `examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_CANDIDATEDOMAIN20260907.lean`
- `examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_STORAGEIDENTITY20260907.lean`
- `examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_KEYEDSTORAGETRANSFER20260907.lean`

Remaining open boundaries:

- the actual active candidate `V` is still not bound to `normalizedEnergy` at the origin or globally;
- no derivative/gauge-equivalence witness between the concrete DH potential and the Fourier/audited potential was supplied;
- `sourceG` finite-difference semantics are not promoted to analytic derivative semantics;
- common kinetic term, controller parameters, cross terms, state ordering and anchor must be same-key typed if a global normalized-storage transfer is attempted;
- initial-bound/coercivity/invariance/trajectory coverage remain separate obligations;
- no Float64/source equivalence, Lean compilation, axiom check, comparator result, verifier receipt, registry admission, P4 or M4 status change is claimed.

## 12. Suggested integration

Use an interface key such as

`P4.active_energy.gauge_equivalence_bridge`

under the existing `T-P4-ACTIVE-ENERGY-ORIGIN` task.  The origin-only consumer should remain allowed to close with the cheaper pointwise `V(0,0)≤1` witness; the gauge-equivalence theorem is the bridge for any later attempt to reuse a normalized physical-energy barrier across source definitions.

Final status: **pending mathematical/interface result**.  It narrows the missing source theorem and removes a false requirement for raw potential equality, but it does not identify the active candidate by itself.
