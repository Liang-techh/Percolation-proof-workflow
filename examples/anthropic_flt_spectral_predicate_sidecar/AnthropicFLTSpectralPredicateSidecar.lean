import Mathlib.LinearAlgebra.Eigenspace.Basic
import Mathlib.Data.Matrix.Basic

set_option autoImplicit false

/-!
Minimal spectral predicate sidecar for `T-FLT-SPECTRAL-PREDICATE`.

Provenance:
  task id: T-FLT-SPECTRAL-PREDICATE
  source agent: Codex
  scope: concrete finite-dimensional abstraction only

This is deliberately not a direct proof of any upstream FLT theorem. It only
packages a tiny operator-family / scalar-predicate statement and a range-to-
eigenspace equality in a two-dimensional model.
-/

namespace AnthropicFLTSpectralPredicateSidecar

noncomputable section

open scoped Matrix

def operatorFamily : Unit → (Fin 2 → ℚ) →ₗ[ℚ] (Fin 2 → ℚ) :=
  fun _ =>
    { toFun := fun x =>
        ![(x 0), 0]
      map_add' := by
        intro x y
        ext <;> simp
      map_smul' := by
        intro c x
        ext <;> simp }

def scalarPredicate : Unit → ℚ := fun _ => 1

def eigenspacePredicate : Prop :=
  LinearMap.range
      ({ toFun := fun q : ℚ => ![q, 0]
         map_add' := by
           intro a b
           ext <;> simp
         map_smul' := by
           intro c q
           ext <;> simp } : ℚ →ₗ[ℚ] (Fin 2 → ℚ))
    = (operatorFamily ()).eigenspace (scalarPredicate ())

theorem range_eq_eigenspace_of_operatorFamily :
    LinearMap.range
        ({ toFun := fun q : ℚ => ![q, 0]
           map_add' := by
             intro a b
             ext <;> simp
           map_smul' := by
             intro c q
             ext <;> simp } : ℚ →ₗ[ℚ] (Fin 2 → ℚ))
      = (operatorFamily ()).eigenspace (scalarPredicate ()) := by
  ext x
  constructor
  · rintro ⟨q, rfl⟩
    simp [operatorFamily, scalarPredicate, LinearMap.mem_eigenspace_iff]
  · intro hx
    rcases (LinearMap.mem_eigenspace_iff.mp hx) with hx
    refine ⟨x 0, ?_⟩
    ext i
    fin_cases i <;> simp [operatorFamily] at hx ⊢

theorem eigenspacePredicate_iff :
    eigenspacePredicate ↔
      LinearMap.range
          ({ toFun := fun q : ℚ => ![q, 0]
             map_add' := by
               intro a b
               ext <;> simp
             map_smul' := by
               intro c q
               ext <;> simp } : ℚ →ₗ[ℚ] (Fin 2 → ℚ))
        = (operatorFamily ()).eigenspace (scalarPredicate ()) := by
  rfl

#print axioms range_eq_eigenspace_of_operatorFamily

end
end AnthropicFLTSpectralPredicateSidecar
