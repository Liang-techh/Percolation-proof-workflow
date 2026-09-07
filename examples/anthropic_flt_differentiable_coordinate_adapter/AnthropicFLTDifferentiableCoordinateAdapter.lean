import Mathlib

/-!
# Anthropic FLT differentiable-coordinate adapter

This sidecar packages the non-number-theoretic finite-dimensional conclusion of
the audited upstream theorem.  It is an API adapter, not a reimplementation of
the upstream proof and not a Route-B/PDE theorem.

Provenance:
  repository: upstream/anthropics-fermats-last-theorem
  commit: aa2d8b34692b16c70f699536de0d8e75b9a3e9ef
  source: Theorems/Thm_Algebra_exists_bijOn_eval_differentiableOn_pi_of_smooth_of_kaehlerDifferential.lean
-/

set_option autoImplicit false

namespace AnthropicFLTDifferentiableCoordinateAdapter

open Topology

structure SmoothEvalCoordinateWitness
    (S : Type) [CommRing S] [IsDomain S] [Algebra ℂ S]
    {n : ℕ} (σ₀ : S →ₐ[ℂ] ℂ) (t : Fin n → S) where
  radius : ℝ
  neighborhood : Set (S →ₐ[ℂ] ℂ)
  radius_pos : 0 < radius
  center_mem : σ₀ ∈ neighborhood
  bijective_coordinate_map :
    Set.BijOn (fun σ : S →ₐ[ℂ] ℂ => fun i : Fin n => σ (t i)) neighborhood
      (Metric.ball (fun i : Fin n => σ₀ (t i)) radius)
  differentiable_factorization : ∀ s : S, ∃ F : (Fin n → ℂ) → ℂ,
    DifferentiableOn ℂ F (Metric.ball (fun i : Fin n => σ₀ (t i)) radius) ∧
      ∀ σ ∈ neighborhood, σ s = F (fun i : Fin n => σ (t i))
  finite_support_stability : ∀ σ ∈ neighborhood, ∃ (fs : Finset S) (ε : ℝ),
    0 < ε ∧
      ∀ σ' : S →ₐ[ℂ] ℂ, (∀ s ∈ fs, ‖σ' s - σ s‖ < ε) →
        σ' ∈ neighborhood

def UpstreamCoordinateConclusion
    (S : Type) [CommRing S] [IsDomain S] [Algebra ℂ S]
    {n : ℕ} (σ₀ : S →ₐ[ℂ] ℂ) (t : Fin n → S) : Prop :=
  ∃ (r : ℝ) (𝒰 : Set (S →ₐ[ℂ] ℂ)), 0 < r ∧ σ₀ ∈ 𝒰 ∧
    Set.BijOn (fun σ : S →ₐ[ℂ] ℂ => fun i : Fin n => σ (t i)) 𝒰
      (Metric.ball (fun i : Fin n => σ₀ (t i)) r) ∧
    (∀ s : S, ∃ F : (Fin n → ℂ) → ℂ,
      DifferentiableOn ℂ F (Metric.ball (fun i : Fin n => σ₀ (t i)) r) ∧
      ∀ σ ∈ 𝒰, σ s = F (fun i : Fin n => σ (t i))) ∧
    (∀ σ ∈ 𝒰, ∃ (fs : Finset S) (ε : ℝ), 0 < ε ∧
      ∀ σ' : S →ₐ[ℂ] ℂ, (∀ s ∈ fs, ‖σ' s - σ s‖ < ε) → σ' ∈ 𝒰)

theorem package_upstream_coordinate_conclusion
    (S : Type) [CommRing S] [IsDomain S] [Algebra ℂ S]
    (hsm : Algebra.Smooth ℂ S)
    {n : ℕ}
    (hrank : Module.rank S (KaehlerDifferential ℂ S) = n)
    (σ₀ : S →ₐ[ℂ] ℂ) (t : Fin n → S)
    (hdt : (RingHom.ker σ₀.toRingHom) •
        (⊤ : Submodule S (KaehlerDifferential ℂ S)) ⊔
        Submodule.span S (Set.range fun i : Fin n =>
          KaehlerDifferential.D ℂ S (t i)) = ⊤)
    (hSource : UpstreamCoordinateConclusion S σ₀ t) :
    ∃ W : SmoothEvalCoordinateWitness S σ₀ t, True := by
  rcases hSource with ⟨r, 𝒰, hr, hCenter, hBij, hFactor, hStable⟩
  exact ⟨{
    radius := r
    neighborhood := 𝒰
    radius_pos := hr
    center_mem := hCenter
    bijective_coordinate_map := hBij
    differentiable_factorization := hFactor
    finite_support_stability := hStable
  }, trivial⟩

end AnthropicFLTDifferentiableCoordinateAdapter

#print axioms AnthropicFLTDifferentiableCoordinateAdapter.package_upstream_coordinate_conclusion
