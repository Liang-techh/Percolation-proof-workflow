import Mathlib

/-!
Minimal spectral sidecar for the Anthropic FLT review.

Provenance:
  review task: T-FLT-SPECTRAL-SIDECAR
  source review: agent_review_inbox/review-T-FLT-spectral-linear.md
  upstream commit: aa2d8b34692b16c70f699536de0d8e75b9a3e9ef

This file deliberately stops at an abstract eigenspace/range bridge. It is not
a direct proof of the upstream theorem
`Submodule.exists_injective_linearMap_baseChange_torsionBySet_range_eq_eigenspace`.
-/

namespace AnthropicFLTSpectralSidecar

open scoped TensorProduct

section AbstractBridge

variable {R S V W : Type*}
variable [CommRing R] [CommRing S]
variable [AddCommGroup V] [Module R V]
variable [AddCommGroup W] [Module S W]

theorem abstract_eigenspace_range_bridge
    (f : V →ₗ[R] W) (h : Function.Injective f) :
    ∃ g : V →ₗ[R] W, Function.Injective g ∧ LinearMap.range g = LinearMap.range f := by
  refine ⟨f, h, rfl⟩

theorem abstract_range_mem_eigenspace_bridge
    (f : V →ₗ[R] W) :
    LinearMap.range f = LinearMap.range f := by
  rfl

end AbstractBridge

/-!
`#print axioms` is kept on purpose so the sidecar surface exposes any non-kernel
assumptions immediately in a focused compile.
-/
#print axioms AnthropicFLTSpectralSidecar.abstract_eigenspace_range_bridge

end AnthropicFLTSpectralSidecar
