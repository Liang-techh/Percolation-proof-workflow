import NEW_P4_032_DefectNormBudget
import Mathlib.Algebra.Order.BigOperators.Ring.Finset

/-!
UNCOMPILED source-independent weighted quadratic budget skeleton.
No Lean/Lake run, source/coverage/admission or numerical weight instance.
Uses coordinatewise weighted Cauchy and Euclidean squared norms; does not
repeat scalar triangle or quadratic-load propagation.
-/

set_option autoImplicit false

namespace RouteBP4032WeightedThreeTerm

open scoped BigOperators
open RouteBP4032BlockDefects
open RouteBP4032DefectNormBudget

noncomputable section

/-- Slot order: port term u, transported distal defect D, local defect B. -/
structure Weights where
  value : Fin 3 → ℝ
  positive : ∀ i, 0 < value i
  reciprocal : (∑ i : Fin 3, 1 / value i) ≤ 1

theorem reciprocal_iff_polynomial (lu lD lB : ℝ)
    (hu : 0 < lu) (hD : 0 < lD) (hB : 0 < lB) :
    1 / lu + 1 / lD + 1 / lB ≤ 1 ↔
      lD * lB + lu * lB + lu * lD ≤ lu * lD * lB := by
  have hp : 0 < lu * lD * lB := mul_pos (mul_pos hu hD) hB
  have hclear : (1 / lu + 1 / lD + 1 / lB) * (lu * lD * lB) =
      lD * lB + lu * lB + lu * lD := by
    field_simp [ne_of_gt hu, ne_of_gt hD, ne_of_gt hB]
    <;> ring
  constructor
  · intro h
    have hm := mul_le_mul_of_nonneg_right h hp.le
    simpa only [hclear, one_mul] using hm
  · intro h
    have hm : (1 / lu + 1 / lD + 1 / lB) * (lu * lD * lB) ≤
        1 * (lu * lD * lB) := by
      rw [hclear, one_mul]
      exact h
    exact le_of_mul_le_mul_right hm hp

def ofReciprocal (lu lD lB : ℝ) (hu : 0 < lu) (hD : 0 < lD) (hB : 0 < lB)
    (hrec : 1 / lu + 1 / lD + 1 / lB ≤ 1) : Weights where
  value := ![lu, lD, lB]
  positive i := by
    fin_cases i
    · exact hu
    · exact hD
    · exact hB
  reciprocal := by simpa [Fin.sum_univ_succ, add_assoc] using hrec

def ofPolynomial (lu lD lB : ℝ) (hu : 0 < lu) (hD : 0 < lD) (hB : 0 < lB)
    (hpoly : lD * lB + lu * lB + lu * lD ≤ lu * lD * lB) : Weights :=
  ofReciprocal lu lD lB hu hD hB ((reciprocal_iff_polynomial lu lD lB hu hD hB).mpr hpoly)

/-- Weighted scalar Cauchy with exact reciprocal weights and no square roots. -/
theorem weighted_scalar (weights : Weights) (x : Fin 3 → ℝ) :
    (∑ i : Fin 3, x i)^2 ≤ ∑ i : Fin 3, weights.value i * (x i)^2 := by
  have hE : 0 ≤ ∑ i : Fin 3, weights.value i * (x i)^2 :=
    Finset.sum_nonneg (fun i _ => mul_nonneg (weights.positive i).le (sq_nonneg _))
  have hc : (∑ i : Fin 3, x i)^2 ≤
      (∑ i : Fin 3, weights.value i * (x i)^2) * (∑ i : Fin 3, 1 / weights.value i) := by
    apply Finset.sum_sq_le_sum_mul_sum_of_sq_le_mul
      (r := x) (f := fun i => weights.value i * (x i)^2)
      (g := fun i => 1 / weights.value i)
    · intro i _
      exact mul_nonneg (weights.positive i).le (sq_nonneg _)
    · intro i _
      exact (one_div_pos.mpr (weights.positive i)).le
    · intro i _
      have hi : weights.value i ≠ 0 := ne_of_gt (weights.positive i)
      have hid : (x i)^2 = (weights.value i * (x i)^2) * (1 / weights.value i) := by
        field_simp [hi]
      exact hid.le
  exact hc.trans (by simpa only [mul_one] using
    mul_le_mul_of_nonneg_left weights.reciprocal hE)

theorem norm2_sq_sum {n : ℕ} (v : Fin n → ℝ) :
    (norm2 v)^2 = ∑ j, (v j)^2 := by
  simpa [norm2, PiLp.toLp_apply] using
    EuclideanSpace.real_norm_sq_eq (WithLp.toLp 2 v : EuclideanSpace ℝ (Fin n))

/-- Any finite Euclidean dimension, including the two-dimensional B force.
The proof sums coordinatewise weighted inequalities, not a scalar triangle cap. -/
theorem weighted_three_term_norm_sq {n : ℕ} (weights : Weights)
    (u v w : Fin n → ℝ) :
    (norm2 (u + v + w))^2 ≤ weights.value 0 * (norm2 u)^2 +
      weights.value 1 * (norm2 v)^2 + weights.value 2 * (norm2 w)^2 := by
  simp only [norm2_sq_sum]
  calc
    (∑ j, ((u + v + w) j)^2) ≤
        ∑ j, (weights.value 0 * (u j)^2 + weights.value 1 * (v j)^2 +
          weights.value 2 * (w j)^2) := by
      apply Finset.sum_le_sum
      intro j _
      simpa [Fin.sum_univ_succ, Pi.add_apply, add_assoc] using
        weighted_scalar weights ![u j, v j, w j]
    _ = _ := by simp [Finset.sum_add_distrib, Finset.mul_sum]

/-- Direct consumption of three SQUARED budgets on the same vectors. -/
theorem routeB_port_defect_quadratic_budget (weights : Weights) (rB u v w : BVec)
    (rhoA energy UD UB : ℝ)
    (identity : rB = u + v + w)
    (hPort : (norm2 u)^2 ≤ rhoA * energy)
    (hD : (norm2 v)^2 ≤ UD) (hB : (norm2 w)^2 ≤ UB) :
    (norm2 rB)^2 ≤ weights.value 0 * (rhoA * energy) +
      weights.value 1 * UD + weights.value 2 * UB := by
  rw [identity]
  exact (weighted_three_term_norm_sq weights u v w).trans
    (add_le_add (add_le_add
      (mul_le_mul_of_nonneg_left hPort (weights.positive 0).le)
      (mul_le_mul_of_nonneg_left hD (weights.positive 1).le))
      (mul_le_mul_of_nonneg_left hB (weights.positive 2).le))

/-- Propagate a squared defect budget without choosing a square root of ED. -/
theorem action_squared_budget (T : BD) (tau ED : ℝ) (e : DVec)
    (hT : ActionBound T tau) (hE : (norm2 e)^2 ≤ ED) :
    (norm2 (T *ᵥ e))^2 ≤ tau^2 * ED := by
  calc
    (norm2 (T *ᵥ e))^2 ≤ (tau * norm2 e)^2 := square_budget _ _ (hT.bound e)
    _ = tau^2 * (norm2 e)^2 := by ring
    _ ≤ tau^2 * ED := mul_le_mul_of_nonneg_left hE (sq_nonneg tau)

structure DistalForceDefect where
  value : DVec
structure DistalAccelDefect where
  value : DVec
structure LocalPortDefect where
  value : BVec

def forceTerm (MBD : BD) (J : DD) (e : DistalForceDefect) : BVec := (MBD * J) *ᵥ e.value
def accelTerm (MBD : BD) (e : DistalAccelDefect) : BVec := MBD *ᵥ e.value

/-- A conversion between force and forward-acceleration defects needs this
explicit relation. No backward-residual sign or approximate inverse is inferred. -/
theorem force_accel_term_identity (MBD : BD) (J : DD)
    (ef : DistalForceDefect) (ea : DistalAccelDefect)
    (hConversion : ea.value = J *ᵥ ef.value) : forceTerm MBD J ef = accelTerm MBD ea := by
  unfold forceTerm accelTerm
  rw [hConversion, Matrix.mulVec_mulVec]

/-- Force-equation defect uses MBD*J. All three terms are already B generalized forces. -/
theorem force_defect_budget (weights : Weights) (R : BB) (MBD : BD) (J : DD)
    (aB : BlockAcceleration) (rB : PortGeneralizedForce)
    (eD : DistalForceDefect) (eB : LocalPortDefect)
    (rhoA energy tau ED EB : ℝ)
    (identity : rB.value = R *ᵥ aB.value + forceTerm MBD J eD + eB.value)
    (hPort : (norm2 (R *ᵥ aB.value))^2 ≤ rhoA * energy)
    (hT : ActionBound (MBD * J) tau)
    (hD : (norm2 eD.value)^2 ≤ ED) (hB : (norm2 eB.value)^2 ≤ EB) :
    (norm2 rB.value)^2 ≤ weights.value 0 * (rhoA * energy) +
      weights.value 1 * (tau^2 * ED) + weights.value 2 * EB :=
  routeB_port_defect_quadratic_budget weights rB.value (R *ᵥ aB.value)
    (forceTerm MBD J eD) eB.value rhoA energy (tau^2 * ED) EB identity hPort
    (action_squared_budget (MBD * J) tau ED eD.value hT hD) hB

/-- Forward-acceleration defect uses MBD alone; no extra J is inserted. -/
theorem accel_defect_budget (weights : Weights) (R : BB) (MBD : BD)
    (aB : BlockAcceleration) (rB : PortGeneralizedForce)
    (eD : DistalAccelDefect) (eB : LocalPortDefect)
    (rhoA energy tau ED EB : ℝ)
    (identity : rB.value = R *ᵥ aB.value + accelTerm MBD eD + eB.value)
    (hPort : (norm2 (R *ᵥ aB.value))^2 ≤ rhoA * energy)
    (hT : ActionBound MBD tau)
    (hD : (norm2 eD.value)^2 ≤ ED) (hB : (norm2 eB.value)^2 ≤ EB) :
    (norm2 rB.value)^2 ≤ weights.value 0 * (rhoA * energy) +
      weights.value 1 * (tau^2 * ED) + weights.value 2 * EB :=
  routeB_port_defect_quadratic_budget weights rB.value (R *ᵥ aB.value)
    (accelTerm MBD eD) eB.value rhoA energy (tau^2 * ED) EB identity hPort
    (action_squared_budget MBD tau ED eD.value hT hD) hB

end

-- Future audit commands only; NOT executed in this round.
#print axioms reciprocal_iff_polynomial
#print axioms ofPolynomial
#print axioms weighted_scalar
#print axioms weighted_three_term_norm_sq
#print axioms routeB_port_defect_quadratic_budget
#print axioms action_squared_budget
#print axioms force_accel_term_identity
#print axioms force_defect_budget
#print axioms accel_defect_budget

end RouteBP4032WeightedThreeTerm
