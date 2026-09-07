---
kind: review_result
review_id: review-FLT-topology-quotient-clm
source_agent: Codex
created_at: 2026-09-06T00:00:00-06:00
integration_status: pending
repository: upstream/anthropic-fermats-last-theorem
commit: aa2d8b3
scope: topology, quotient, subsingleton, connected, continuity, ContinuousLinearMap, ContinuousMap, homeomorphism, transport
admission_label: architecture_only
---

# Anthropic FLT non-number-theory scan: topology / quotient / transport

This is a read-only scan of `upstream/anthropic-fermats-last-theorem` at commit `aa2d8b3`.
I did not run a whole-repo Lean build. I only inspected the requested non-number-theory
surface area and selected theorems that could plausibly help with PDE, flowpipe, or adapter
work.

The key boundary is that "usable" here means reusable as topology/transport infrastructure,
not as a closed PDE or flowpipe theorem. Anything below still needs a target-side admission
check in the destination repository.

## Level 1: directly reusable infrastructure

These are the strongest candidates for immediate adapter work because their conclusion is
already in the right shape and the hypotheses are standard topological typeclass gates.

| Path | Theorem / def | Hypotheses | Potential reuse | Risk |
|---|---|---|---|---|
| `Definitions/Def_Mathlib_Topology_Algebra_Module_Quotient.lean:5-18` | `Submodule.Quotient.continuousLinearEquiv` | `[Ring R] [AddCommGroup G] [Module R G] [AddCommGroup H] [Module R H] [TopologicalSpace G] [TopologicalSpace H]` plus `e : G ≃L[R] H` and `h : Submodule.map e.toLinearMap G' = H'` | Quotient-level transport of continuous linear equivalences. Good for kernel/boundary quotient maps in flowpipe state compression or adapter normalization. | Only works when the quotient is genuinely a `Submodule` quotient and the submodule map equality is available. |
| `Definitions/Def_Mathlib_Topology_Algebra_Module_Quotient.lean:20-37` | `Submodule.quotientPiContinuousLinearEquiv` | `[CommRing R]`, finite index `ι`, `[Fintype ι] [DecidableEq ι]`, per-coordinate `AddCommGroup`, `Module`, `TopologicalSpace`, `IsTopologicalAddGroup` and `p : ι → Submodule R (G i)` | Finite-product quotient transport. Useful for blockwise flowpipes, coordinate splitting, and quotienting per-mode error states. | Requires finite indexing and the exact `pi`-submodule quotient form; not a drop-in for infinite product spaces. |
| `Definitions/Def_Mathlib_Topology_Bases.lean:5-16` | `TopologicalSpace.secondCountableTopology_of_countable_cover'` | `[TopologicalSpace α]`, `Countable ι`, each `U i` second countable, each `f i` an open embedding, and a countable open cover witness `hc` | Good topological bookkeeping for chart/cell covers and for turning a countable family of local pieces into a global separability basis. | It closes second countability, not quantitative enclosure or reachability. |

## Level 2: reusable after local adaptation

These are useful, but the names, scalar choices, or target carriers are specialized enough that
I would rewrite the API around the target object rather than import them wholesale.

| Path | Theorem / def | Hypotheses | Potential reuse | Risk |
|---|---|---|---|---|
| `Definitions/Def_Mathlib_Topology_Algebra_ContinuousMonoidHom.lean:6-19` | `ContinuousAddEquiv.toIntContinuousLinearEquiv` | `[AddCommGroup M] [TopologicalSpace M] [AddCommGroup M₂] [TopologicalSpace M₂]` and `e : M ≃ₜ+ M₂` | A ready-made bridge from additive homeomorphism to `ContinuousLinearEquiv`. Useful when an adapter wants continuous additive structure, but the target is really linear over `ℤ` or a discretized module. | The `ℤ`-linearization is often the wrong scalar for PDE state spaces, so this usually needs a target-specific replacement. |
| `Definitions/Def_Mathlib_Topology_Algebra_ContinuousMonoidHom.lean:13-23` | `ContinuousAddEquiv.quotientPi` | Same finite-product quotient shape, but for `AddSubgroup` and `≃ₜ+` | Good template for quotienting additive state decompositions, especially where a flowpipe is naturally additive rather than linear. | Stays at `AddSubgroup`/`Additive` level; if the target is linear, prefer a `ContinuousLinearEquiv` version. |
| `Definitions/Def_Mathlib_Topology_Algebra_ContinuousMonoidHom.lean:24-38` | `ContinuousMulEquiv.piUnique`, `ContinuousMulEquiv.piEquivPiSubtypeProd`, `ContinuousMulEquiv.units_map` | `piUnique`: `[Unique ι]`; `piEquivPiSubtypeProd`: `DecidablePred p`; `units_map`: `Monoid` + topology on source and target | Good as a transport skeleton when a product space needs to be split into a constrained subproduct, or when a homeomorphism should be lifted to units. | Multiplicative-only APIs are not a direct fit for additive PDE state spaces without a translation layer. |
| `Definitions/Def_Mathlib_Topology_Algebra_ContinuousMonoidHom.lean:48-52` | `ContinuousMulEquiv.coe_toHomeomorph` | `[CommMonoid M] [CommMonoid N] [TopologicalSpace M] [TopologicalSpace N]` | Useful to convert a continuous multiplicative equivalence into a `Homeomorph` explicitly, which is handy for transport adapters that need a topological witness rather than just an equivalence. | This is just a coercion lemma; it gives no new continuity content by itself. |
| `Definitions/Def_AutomorphicForm_BaseChangePlaces.lean:246-261` | `baseChangeHomeomorph`, `continuous_baseChangeEquiv`, `continuous_baseChangeEquiv_symm` | `K L` number fields, `Algebra K L`, and `IsModuleTopology` on the tensor-product carrier built in the section | Strong adapter shape for turning a ring equivalence into a homeomorphism plus both directional continuity proofs. The same pattern is useful when transporting a PDE state representation across a change of coordinates. | The carrier is adelic/tensor-product specific; reuse the pattern, not the arithmetic domain. |
| `Definitions/Def_NumberField_PlaceTransport.lean:101-130` | `uniformContinuous_congr_of_smul_eq`, `transport`, `continuous_transport` | `σ : K ≃ₐ[E] K`, `h : σ • w = w'`, valuation compatibility, and the adic completion infrastructure | This is one of the cleanest transport templates in the snapshot: prove valuation compatibility, lift to a uniform continuous map, then package a continuous transport equivalence. Good for completion-valued adapters. | It is valuation/completion specific and depends on number-field structure, so only the transport architecture is reusable. |
| `Definitions/Def_NumberField_PlaceTransport.lean:131-170` | `valued_transport`, `transport_mem_adicCompletionIntegers_iff`, `transportIntegers`, `transportUnits`, `transportIntegerUnits` | Same transport hypotheses, plus adic completion integer/unit substructures | Useful when an adapter must preserve an integrality predicate across a transport map. The `*_iff` lemma is a nice pattern for invariant preservation through completion. | The valuation/integrality predicate is highly specialized; do not treat it as a general topological invariant lemma. |
| `Definitions/Def_AlgebraicCurve_CurveModelTransport.lean:171-216` | `transport`, `transport_ffEquiv`, `transport_placeOfPoint`, `transport_pointEquivPlace` | Curve model isomorphism data `c e he`; later `IsAlgClosed K` for the point/place equivalence theorem | Strong carrier-preserving transport shape: build the transported object, then expose the canonical equivalences and simp lemmas. This is useful for adapter-style reindexing or provenance-preserving coordinate changes. | The scheme/curve object is too specialized to be a general topology theorem; only the transport API shape is reusable. |

## Level 3: architecture only

These are worth copying as proof-plumbing ideas, but I would not register them as generic
theorems for PDE or flowpipe work.

| Path | Theorem / def | Hypotheses | Potential reuse | Risk |
|---|---|---|---|---|
| `Theorems/Thm_PrimeSpectrum_apply_eq_apply_of_forall_le_of_connectedSpace.lean:6-10` | `PrimeSpectrum.apply_eq_apply_of_forall_le_of_connectedSpace` | `[CommRing R] [IsNoetherianRing R] [ConnectedSpace (PrimeSpectrum R)]` and an order-monotone equality hypothesis `h : ∀ p q, p ≤ q → φ p = φ q` | Good pattern for “monotone-on-order + connectedness collapses to global constancy.” That proof shape can inspire connected-state or region-wise invariance arguments. | It is a specific PrimeSpectrum theorem, not a generic connected-space constancy result for arbitrary metric or flowpipe states. |
| `Theorems/Thm_exists_spanningTree_of_connected.lean:5-12` | `exists_spanningTree_of_connected` | finite `V`, `E`, decidable equality, incidence data `hd tl`, and a connectivity witness `hconn` | Architecture for extracting a tree-like witness from connectivity data. Could inform graph abstraction layers or region adjacency bookkeeping in a workflow. | It is combinatorial and discrete; it does not provide analytic connectedness or topology-of-state-space closure. |
| `Theorems/Thm_AlgebraicCurve_Place_connectedSpace_of_chartedSpace_of_meromorphicOrderAt_eq_ord_complex.lean:14-25` | `AlgebraicCurve.Place.connectedSpace_of_chartedSpace_of_meromorphicOrderAt_eq_ord_complex` | `[Field F] [Algebra ℂ F]`, existence of a transcendental generator, `FiniteDimensional` condition, `[IsCurveOver ℂ F]`, `TopologicalSpace`, `ChartedSpace`, `CompactSpace`, and a meromorphic-order compatibility hypothesis `hF` | Useful as a “local analytic control implies global connectedness” proof skeleton, especially where charts plus a local regularity predicate drive a global topological conclusion. | The domain is a complex algebraic-curve place space, so this is only a proof architecture reference. |
| `Definitions/Def_AlgebraicCurve_PlaceCompletion.lean:70-158` | `kw_ffgc_uniformContinuous_withValMapAlgebraMap`, `kw_ffgc_adicCompletionComap`, `kw_ffgc_continuous_adicCompletionComap`, `kw_ffgc_valued_adicCompletionComap` | valuation/completion data for `W.restrict F`, `W.heightOneSpectrum.valuation`, and a number-field tower | A strong template for turning valuation compatibility into a uniform continuous map and then into a continuous completion map. | Completion and valuation hypotheses are very specific; this is not directly a PDE continuity theorem. |
| `Definitions/Def_AutomorphicForm_BaseChangePlaces.lean:317-394` | `continuous_glMap`, `glCongr`, `continuous_tensorArch`, `continuous_tensorPlace`, `continuous_semiLocalEval`, `continuous_semiLocalComponent` | `CommRing` / `IsTopologicalRing` on carriers, plus the ad hoc base-change infrastructure in that file | Good adapter layering: prove continuity once at the scalar map level, then lift to matrices and componentwise maps. | The arithmetic carriers are specialized; use it as an architecture pattern, not as a reusable mathematical result. |
| `Definitions/Def_Mathlib_Topology_Algebra_RestrictedProduct_Equiv.lean` and `Definitions/Def_Mathlib_Topology_Algebra_RestrictedProduct_TopologicalSpace.lean` | restricted product congruence/homeomorphism APIs | restricted-product topology and eventually-compatibility hypotheses | Potentially helpful if the PDE/flowpipe model uses “all but finitely many coordinates stable” or a filtered product construction. | The restricted-product setting is a fairly narrow fit and should stay architecture-only unless the target model is actually filtered/product-like. |
| `Definitions/Def_Mathlib_Topology_Algebra_UniformRing.lean` | completion/map APIs such as `UniformSpace.Completion.mapSemialgHom` | uniform/topological ring/completion hypotheses | Nice pattern for lifting a continuous map through completion. | This is a completion-level adapter pattern, not a generic enclosure or flowpipe theorem. |

## Negative filter

I did not promote the following to direct reuse, even though they mention `connected`,
`subsingleton`, or `quotient`, because their content is too domain-specific:

- `Theorems/Thm_TwoChartCech_finrank_H0_gluedLinesSections_eq_one_and_subsingleton_H1.lean`
- `Theorems/Thm_WeierstrassCurve_subsingleton_torsionBy_algClosure_point_of_not_isElliptic_of_charZero_of_c4_eq_zero.lean`
- `Definitions/Def_AlgebraicCurve_CurveModelConstruction.lean:1928-1949` with `subsingleton_gInf_mem`
- the large family of `P2M/Sol/*quotient*`, `*subsingleton*`, and `*continuous*` theorems that are pure number-theory or sheaf/cohomology packaging

Those may be mathematically correct, but they are not the right admission boundary for
PDE, flowpipe, or generic adapter work.

## Practical order of acquisition

If I were turning this into a target-side adapter, I would acquire in this order:

1. `Submodule.Quotient.continuousLinearEquiv`
2. `Submodule.quotientPiContinuousLinearEquiv`
3. `TopologicalSpace.secondCountableTopology_of_countable_cover'`
4. `baseChangeHomeomorph`-style continuity layering
5. `NumberField.PlaceTransport.transport`-style completion transport only if the target really needs a valuation/completion analogue

## Bottom line

Best immediate reuse:

- quotient continuous linear transport;
- finite product quotient transport;
- countable open-cover second countability;
- explicit homeomorphism/transport layering for adapters.

Best structural borrowing only:

- connectedness collapse via order-monotone hypotheses;
- transport-by-compatibility on valuation/completion objects;
- carrier-preserving transport APIs.

Worst fit for direct reuse:

- any theorem whose apparent `quotient`, `connected`, or `subsingleton` content is actually tied to places, curves, sheaves, or automorphic forms.
