import Mathlib

/-!
Corrective spectral predicate sidecar for `T-FLT-SPECTRAL-PREDICATE`.

This file fixes the semantic weakness identified in the previous spectral
sidecar: the theorem statement below contains an actual eigenvector/eigenspace
predicate `T v = μ • v` and proves equality between a linear-map range and the
set of vectors satisfying that predicate.

Upstream provenance context:
- Anthropic FLT commit: `aa2d8b34692b16c70f699536de0d8e75b9a3e9ef`
- candidate declaration:
  `Submodule.exists_injective_linearMap_baseChange_torsionBySet_range_eq_eigenspace`
- candidate path:
  `Theorems/Thm_Submodule_exists_injective_linearMap_baseChange_torsionBySet_range_eq_eigenspace.lean`

Important boundary: this is a self-contained abstraction. It does not import or
re-prove the FLT-specific wrapper and therefore is not direct upstream theorem
reuse.
-/

namespace AnthropicFLTSpectralPredicateSidecar

section SpectralPredicate

variable {R V W : Type*}
variable [CommRing R]
variable [AddCommGroup V] [Module R V]
variable [AddCommGroup W] [Module R W]

/-- The set of vectors satisfying the explicit eigenvector equation for `T`
and eigenvalue `μ`. -/
def eigenspaceSet (T : V →ₗ[R] V) (μ : R) : Set V :=
  {v | T v = μ • v}

/-- A range is exactly the eigenspace predicate when the map lands in that
predicate and is onto every vector satisfying it. -/
theorem range_eq_eigenspaceSet
    (T : V →ₗ[R] V) (μ : R) (f : W →ₗ[R] V)
    (h_into : ∀ w : W, T (f w) = μ • f w)
    (h_onto : ∀ v : V, T v = μ • v → ∃ w : W, f w = v) :
    (LinearMap.range f : Set V) = eigenspaceSet T μ := by
  ext v
  constructor
  · intro hv
    rcases hv with ⟨w, rfl⟩
    change T (f w) = μ • f w
    exact h_into w
  · intro hv
    change T v = μ • v at hv
    rcases h_onto v hv with ⟨w, hw⟩
    exact ⟨w, hw⟩

/-- Version matching the upstream candidate's injective-map shape. Injectivity
is carried explicitly rather than inferred from the range/eigenspace equality. -/
theorem exists_injective_range_eq_eigenspaceSet
    (T : V →ₗ[R] V) (μ : R) (f : W →ₗ[R] V)
    (hf : Function.Injective f)
    (h_into : ∀ w : W, T (f w) = μ • f w)
    (h_onto : ∀ v : V, T v = μ • v → ∃ w : W, f w = v) :
    ∃ g : W →ₗ[R] V,
      Function.Injective g ∧
        (LinearMap.range g : Set V) = eigenspaceSet T μ := by
  refine ⟨f, hf, ?_⟩
  exact range_eq_eigenspaceSet T μ f h_into h_onto

end SpectralPredicate

#print axioms AnthropicFLTSpectralPredicateSidecar.range_eq_eigenspaceSet
#print axioms AnthropicFLTSpectralPredicateSidecar.exists_injective_range_eq_eigenspaceSet

end AnthropicFLTSpectralPredicateSidecar
