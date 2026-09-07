import Mathlib

/-!
# Anthropic FLT countable-cover topology adapter

This sidecar wraps the audited standard theorem that a countable open-embedding
cover by second-countable spaces gives a second-countable target.  It is
topological infrastructure only; it does not prove quantitative coverage or a
Route-B/PDE enclosure.

Provenance:
  repository: upstream/anthropics-fermats-last-theorem
  commit: aa2d8b34692b16c70f699536de0d8e75b9a3e9ef
  source: Definitions/Def_Mathlib_Topology_Bases.lean
-/

set_option autoImplicit false

namespace AnthropicFLTCountableCoverAdapter

theorem second_countable_from_countable_open_embedding_cover {α : Type*}
    [TopologicalSpace α] {ι : Sort*} [Countable ι]
    {U : ι → Type*} [∀ i, TopologicalSpace (U i)]
    [∀ i, SecondCountableTopology (U i)]
    (f : ∀ i, U i → α)
    (hf : ∀ i, Topology.IsOpenEmbedding (f i))
    (hc : ∀ a, ∃ (i : ι) (u : U i), f i u = a) :
    SecondCountableTopology α := by
  exact TopologicalSpace.secondCountableTopology_of_countable_cover' f hf hc

/-! A map from one sampled patch does not establish a cover of the target. -/

def sampledPatch (_ : Unit) : Bool := false

theorem sampled_patch_missing_target_point :
    ∃ a : Bool, ¬ ∃ u : Unit, sampledPatch u = a := by
  exact ⟨true, by simp [sampledPatch]⟩

end AnthropicFLTCountableCoverAdapter

#print axioms AnthropicFLTCountableCoverAdapter.second_countable_from_countable_open_embedding_cover
#print axioms AnthropicFLTCountableCoverAdapter.sampled_patch_missing_target_point
