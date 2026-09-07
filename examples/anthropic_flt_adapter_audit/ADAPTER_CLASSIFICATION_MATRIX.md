# Anthropic FLT generic adapter classification matrix

Status: audit-only.  This file adds no Lean sidecar and does not promote any
candidate to the verified registry.

## Scope

The matrix covers the four principal adapters currently available for reuse:
quotient transport, differentiable coordinates, countable-cover topology, and
additive-to-`ℤ`-linear transport.  The later `piEquivPiSubtypeProd` scan is
listed separately because it is architecture-only and is not a fifth
validation candidate.

| Adapter | Classification | Theorem-DAG role | Main contract | Value / limiting boundary | Next action |
|---|---|---|---|---|---|
| `Submodule.Quotient.continuousLinearEquiv`, `Submodule.quotientPiContinuousLinearEquiv` | `direct_reuse` | finite quotient and coordinate-product transport | ring/module structure, finite-index product, topological additive groups | highest structural reuse for quotient/projected-state interfaces; no coverage, residual, or flowpipe result | pinned compile and exact source/adapter audit |
| `Algebra.exists_bijOn_eval_differentiableOn_pi_of_smooth_of_kaehlerDifferential` | `direct_reuse` | local coordinate and differentiable-factorization node | complex finite-type smooth domain, Kähler-differential rank/generation, evaluation hom, coordinate family | closest to an analytic theorem-DAG boundary; does not yield a real/PDE chart without separate scalar, domain, and regularity obligations | recommended single candidate for 流川枫 |
| `TopologicalSpace.secondCountableTopology_of_countable_cover'` | `direct_reuse` | topological bookkeeping side condition | countable index, second-countable source fibers, open embeddings, point-hit witness | useful for chart topology; a hit witness is not quantitative domain coverage | keep pending; no priority verification |
| `ContinuousAddEquiv.toIntContinuousLinearEquiv` | `light_adaptation` | additive transport seam | additive commutative groups, topologies, additive homeomorphism | output is only `M ≃L[ℤ] M₂`; it is not polymorphic real/complex-linear PDE transport | retain as scalar-boundary reference |

## Separate architecture-only scan record

`ContinuousAddEquiv.piEquivPiSubtypeProd` is classified
`architecture_only`.  It only splits a dependent product along a decidable
predicate into two subtype-indexed factors.  The factors may be empty, and
the equivalence proves neither domain coverage nor analytic regularity.  It
should not be handed to verification while the four principal candidates
remain unresolved.

## Verification priority

The single best candidate to hand to 流川枫 is the
differentiable-coordinate adapter.  It has the strongest nontrivial analytic
interface among the four and can serve as a typed local-coordinate node in a
theorem DAG.  The handoff must remain fail-closed:

1. check the pinned commit, source blob, imports, and exact declaration type;
2. compile only the isolated sidecar or a minimal source-derived probe;
3. check that the conclusion is the displayed complex/algebraic conclusion,
   not a real scalar PDE chart;
4. keep the result `pending` until domain, scalar, regularity, provenance,
   and any downstream admission obligations are independently discharged.

The quotient adapter is the strongest structural runner-up, but it is more
generic and already has a dedicated sidecar.  The countable-cover and
additive-`ℤ` adapters are lower-value support seams, while the subtype-product
adapter is intentionally architecture-only.

No registry/shared state was modified and no wide regression was run.
