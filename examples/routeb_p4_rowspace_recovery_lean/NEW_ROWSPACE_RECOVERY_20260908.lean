import Mathlib.Data.Real.Basic
import Mathlib.LinearAlgebra.Basic
import Mathlib.Algebra.BigOperators.Group.Finset.Basic

set_option autoImplicit false

namespace RouteBP4RowspaceRecovery

/-!
OPEN_UNCOMPILED. No local/remote compilation or axiom audit.
X, source row maps, coordinate map and domain membership are explicit inputs.
The coordinate is a linear functional, not automatically a physical slot.
-/

variable {X ι : Type*} [AddCommGroup X] [Module ℝ X]

/-- A finite row-combination certificate recovers a scalar from affine row data.
The certificate is required only at the queried x, not on the whole space. -/
theorem recover_from_combination (s : Finset ι)
    (row : ι → X →ₗ[ℝ] ℝ) (coordinate : X →ₗ[ℝ] ℝ)
    (weight rhs : ι → ℝ) (x : X)
    (hCombination : coordinate x = ∑ i ∈ s, weight i * row i x)
    (hRows : ∀ i ∈ s, row i x = rhs i) :
    coordinate x = ∑ i ∈ s, weight i * rhs i := by
  rw [hCombination]
  apply Finset.sum_congr rfl
  intro i hi
  rw [hRows i hi]

/-- A row-combination identity on K yields kernel inclusion on that same K. -/
theorem kernel_on_of_combination (K : Set X) (s : Finset ι)
    (row : ι → X →ₗ[ℝ] ℝ) (coordinate : X →ₗ[ℝ] ℝ) (weight : ι → ℝ)
    (hCombination : ∀ z ∈ K,
      coordinate z = ∑ i ∈ s, weight i * row i z) :
    ∀ z ∈ K, (∀ i ∈ s, row i z = 0) → coordinate z = 0 := by
  intro z hz hRows
  rw [hCombination z hz]
  apply Finset.sum_eq_zero
  intro i hi
  rw [hRows i hi, mul_zero]

/-- Kernel information must apply to x-y, not merely to x and y separately. -/
theorem coordinate_eq_of_kernel_on (K : Set X) (s : Finset ι)
    (row : ι → X →ₗ[ℝ] ℝ) (coordinate : X →ₗ[ℝ] ℝ)
    (hKernel : ∀ z ∈ K, (∀ i ∈ s, row i z = 0) → coordinate z = 0)
    (x y : X) (hDifference : x - y ∈ K)
    (hRows : ∀ i ∈ s, row i x = row i y) : coordinate x = coordinate y := by
  have hz : ∀ i ∈ s, row i (x - y) = 0 := by
    intro i hi
    rw [map_sub, hRows i hi, sub_self]
  have hc : coordinate (x - y) = 0 := hKernel (x - y) hDifference hz
  have hs : coordinate x - coordinate y = 0 := by
    simpa only [map_sub] using hc
  exact sub_eq_zero.mp hs

/-- Affine recovery relative to an admitted reference state.
Domain membership alone supplies neither the reference nor difference closure. -/
theorem recover_on_domain (D K : Set X) (s : Finset ι)
    (row : ι → X →ₗ[ℝ] ℝ) (coordinate : X →ₗ[ℝ] ℝ)
    (rhs : ι → ℝ) (value : ℝ)
    (hKernel : ∀ z ∈ K, (∀ i ∈ s, row i z = 0) → coordinate z = 0)
    (hDifference : ∀ x ∈ D, ∀ y ∈ D, x - y ∈ K)
    (reference : X) (hReference : reference ∈ D)
    (hReferenceRows : ∀ i ∈ s, row i reference = rhs i)
    (hReferenceValue : coordinate reference = value)
    (x : X) (hx : x ∈ D) (hRows : ∀ i ∈ s, row i x = rhs i) :
    coordinate x = value := by
  have heq : coordinate x = coordinate reference :=
    coordinate_eq_of_kernel_on K s row coordinate hKernel x reference
      (hDifference x hx reference hReference)
      (fun i hi => (hRows i hi).trans (hReferenceRows i hi).symm)
  exact heq.trans hReferenceValue

end RouteBP4RowspaceRecovery
