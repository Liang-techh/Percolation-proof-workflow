import Mathlib.Data.Real.Basic
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic.Ring

/-!
Christoffel power by finite-sum reindexing, for an arbitrary real tensor.
The generic finite-index result specializes to Fin 6 without enumeration.
-/

open scoped BigOperators

namespace RouteBChristoffelPower

noncomputable section

variable {ι : Type*} [Fintype ι]

/-- The velocity-quadratic Christoffel force, with index order T k i j. -/
def christoffelForce (T : ι → ι → ι → ℝ) (v : ι → ℝ) (i : ι) : ℝ :=
  ∑ j, ∑ k, ((T k i j + T j i k - T i j k) / 2) * v j * v k

/-- The directional contraction of the tensor with velocity. -/
def massRate (T : ι → ι → ι → ℝ) (v : ι → ℝ) (i j : ι) : ℝ :=
  ∑ k, T k i j * v k

/-- The matrix convention used in mechanical_energy_power_identity. -/
def christoffelMatrix (T : ι → ι → ι → ℝ) (v : ι → ℝ) (i j : ι) : ℝ :=
  ∑ k, ((T k i j + T j i k - T i j k) / 2) * v k

/-- Swapping the two outer dummy indices leaves a cubic contraction unchanged.
No permutation symmetry of T is assumed. -/
theorem contraction_swap (T : ι → ι → ι → ℝ) (v : ι → ℝ) :
    (∑ i, ∑ j, ∑ k, T j i k * v i * v j * v k) =
      ∑ i, ∑ j, ∑ k, T i j k * v i * v j * v k := by
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro i _
  apply Finset.sum_congr rfl
  intro j _
  apply Finset.sum_congr rfl
  intro k _
  ring

/-- Purely algebraic Christoffel power identity on any finite index type. -/
theorem christoffel_power_identity (T : ι → ι → ι → ℝ) (v : ι → ℝ) :
    (∑ i, v i * christoffelForce T v i) =
      (1 / 2 : ℝ) * ∑ i, v i * (∑ j, massRate T v i j * v j) := by
  calc
    (∑ i, v i * christoffelForce T v i) =
        (1 / 2 : ℝ) *
          ((∑ i, ∑ j, ∑ k, T k i j * v i * v j * v k) +
           (∑ i, ∑ j, ∑ k, T j i k * v i * v j * v k) -
           (∑ i, ∑ j, ∑ k, T i j k * v i * v j * v k)) := by
      simp only [christoffelForce, mul_sub, mul_add, Finset.mul_sum,
        ← Finset.sum_add_distrib, ← Finset.sum_sub_distrib]
      apply Finset.sum_congr rfl
      intro i _
      apply Finset.sum_congr rfl
      intro j _
      apply Finset.sum_congr rfl
      intro k _
      ring
    _ = (1 / 2 : ℝ) *
        (∑ i, ∑ j, ∑ k, T k i j * v i * v j * v k) := by
      rw [contraction_swap T v]
      ring
    _ = _ := by
      simp only [massRate, Finset.mul_sum, Finset.sum_mul]
      apply Finset.sum_congr rfl
      intro i _
      apply Finset.sum_congr rfl
      intro j _
      apply Finset.sum_congr rfl
      intro k _
      ring

theorem christoffelMatrix_mul_velocity (T : ι → ι → ι → ℝ) (v : ι → ℝ)
    (i : ι) :
    (∑ j, christoffelMatrix T v i j * v j) = christoffelForce T v i := by
  simp only [christoffelMatrix, christoffelForce, Finset.sum_mul]
  apply Finset.sum_congr rfl
  intro j _
  apply Finset.sum_congr rfl
  intro k _
  ring

/-- Exact Fin 6 statement with the tensor formula fully exposed. -/
theorem christoffel_power_identity_fin6 (T : Fin 6 → Fin 6 → Fin 6 → ℝ)
    (v : Fin 6 → ℝ) :
    (∑ i, v i * (∑ j, ∑ k,
      ((T k i j + T j i k - T i j k) / 2) * v j * v k)) =
      (1 / 2 : ℝ) * ∑ i, v i * (∑ j, (∑ k, T k i j * v k) * v j) :=
  christoffel_power_identity T v

/-- The exact orientation and matrix shape of the target's hC premise. -/
theorem mechanical_energy_hC (T : Fin 6 → Fin 6 → Fin 6 → ℝ)
    (v : Fin 6 → ℝ) :
    (1 / 2 : ℝ) * (∑ i, v i * (∑ j, massRate T v i j * v j)) =
      ∑ i, v i * (∑ j, christoffelMatrix T v i j * v j) := by
  simp_rw [christoffelMatrix_mul_velocity]
  exact (christoffel_power_identity T v).symm

end

#print axioms contraction_swap
#print axioms christoffel_power_identity
#print axioms christoffelMatrix_mul_velocity
#print axioms christoffel_power_identity_fin6
#print axioms mechanical_energy_hC

end RouteBChristoffelPower
