import Mathlib.MeasureTheory.Integral.Prod
import Mathlib.Tactic

namespace HarrisReplay

open MeasureTheory

theorem difference_nonneg {Y : Type*} [LinearOrder Y] {φ ψ : Y → ℝ}
    (hφ : Monotone φ) (hψ : Monotone ψ) (x y : Y) :
    0 ≤ (φ x - φ y) * (ψ x - ψ y) := by
  rcases le_total x y with hxy | hyx
  · exact mul_nonneg_of_nonpos_of_nonpos
      (sub_nonpos.mpr (hφ hxy)) (sub_nonpos.mpr (hψ hxy))
  · exact mul_nonneg (sub_nonneg.mpr (hφ hyx)) (sub_nonneg.mpr (hψ hyx))

theorem iterated_nonneg {Y : Type*} [LinearOrder Y] [MeasurableSpace Y]
    {φ ψ : Y → ℝ} (hφ : Monotone φ) (hψ : Monotone ψ) (ν : Measure Y) :
    0 ≤ ∫ y, (∫ x, (φ x - φ y) * (ψ x - ψ y) ∂ν) ∂ν := by
  apply integral_nonneg
  intro y
  apply integral_nonneg
  intro x
  exact difference_nonneg hφ hψ x y

end HarrisReplay
