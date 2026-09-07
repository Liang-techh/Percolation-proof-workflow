import Mathlib

/-!
# Anthropic FLT dependent-product subtype transport adapter

This sidecar records the additive form of the audited generic API
`ContinuousAddEquiv.piEquivPiSubtypeProd`.  It splits a dependent product
along a decidable predicate and preserves only topological/additive
structure.  It is an architecture-only interface; it is not a coverage,
regularity, PDE, or FLT arithmetic theorem.

Provenance:
  repository: upstream/anthropics-fermats-last-theorem
  commit: aa2d8b34692b16c70f699536de0d8e75b9a3e9ef
  source: Definitions/Def_Mathlib_Topology_Algebra_ContinuousMonoidHom.lean
  source blob: 7829c8e30b406c8bb1dcbddf8e8d49745ec5c8ea
-/

set_option autoImplicit false

namespace AnthropicFLTPiSubtypeTransportAdapter

/--
Typed wrapper for the additive product-splitting transport.  The two
subtype-indexed factors together carry exactly the original dependent
product, but no analytic or quantitative property is added.
-/
def piEquivPiSubtypeProd {ι : Type*} (p : ι → Prop) (Y : ι → Type*)
    [(i : ι) → TopologicalSpace (Y i)] [(i : ι) → Add (Y i)]
    [DecidablePred p] :
    ((i : ι) → Y i) ≃ₜ+ ((i : { x : ι // p x }) → Y i) ×
      ((i : { x : ι // ¬p x }) → Y i) :=
  {Homeomorph.piEquivPiSubtypeProd p Y with map_add' _ _ := rfl}

end AnthropicFLTPiSubtypeTransportAdapter

#print axioms AnthropicFLTPiSubtypeTransportAdapter.piEquivPiSubtypeProd
