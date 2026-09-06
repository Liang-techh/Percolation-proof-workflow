import Mathlib.MeasureTheory.Integral.Prod
import Mathlib.Tactic

open MeasureTheory
universe u

-- The children are assumptions, not imports of proved or placeholder theorems.
theorem harris_reduction
    (positive : ∀ {Y : Type u} [LinearOrder Y] [MeasurableSpace Y]
      {φ ψ : Y → ℝ}, Monotone φ → Monotone ψ → ∀ (ν : Measure Y),
      0 ≤ ∫ y, (∫ x, (φ x - φ y) * (ψ x - ψ y) ∂ν) ∂ν)
    (expand : ∀ {Y : Type u} [MeasurableSpace Y]
      (ν : Measure Y) [IsProbabilityMeasure ν] {φ ψ : Y → ℝ},
      Integrable φ ν → Integrable ψ ν →
      Integrable (fun x => φ x * ψ x) ν → ∀ (y : Y),
      (∫ x, (φ x - φ y) * (ψ x - ψ y) ∂ν) =
        (∫ x, φ x * ψ x ∂ν) - φ y * (∫ x, ψ x ∂ν) -
          ψ y * (∫ x, φ x ∂ν) + φ y * ψ y)
    {Y : Type u} [MeasurableSpace Y] [LinearOrder Y]
    (ν : Measure Y) [IsProbabilityMeasure ν] {φ ψ : Y → ℝ}
    (hφ : Monotone φ) (hψ : Monotone ψ)
    (hφm : Measurable φ) (hψm : Measurable ψ) {C : ℝ}
    (hφb : ∀ y, ‖φ y‖ ≤ C) (hψb : ∀ y, ‖ψ y‖ ≤ C) :
    (∫ y, φ y ∂ν) * (∫ y, ψ y ∂ν) ≤ ∫ y, φ y * ψ y ∂ν := by
  have hf : Integrable φ ν :=
    Integrable.of_bound hφm.aestronglyMeasurable C (Filter.Eventually.of_forall hφb)
  have hg : Integrable ψ ν :=
    Integrable.of_bound hψm.aestronglyMeasurable C (Filter.Eventually.of_forall hψb)
  have hfg : Integrable (fun y => φ y * ψ y) ν := by
    apply Integrable.of_bound (hφm.mul hψm).aestronglyMeasurable (C * C)
    exact Filter.Eventually.of_forall fun y => by
      change ‖φ y * ψ y‖ ≤ C * C
      rw [norm_mul]
      exact mul_le_mul (hφb y) (hψb y) (norm_nonneg _) ((norm_nonneg _).trans (hφb y))
  have hout :
      (∫ y, (∫ x, (φ x - φ y) * (ψ x - ψ y) ∂ν) ∂ν) =
        2 * ((∫ y, φ y * ψ y ∂ν) -
          (∫ y, φ y ∂ν) * (∫ y, ψ y ∂ν)) := by
    simp_rw [expand ν hf hg hfg]
    have hfirst : Integrable
        (fun y => (∫ x, φ x * ψ x ∂ν) - φ y * (∫ x, ψ x ∂ν)) ν :=
      (integrable_const _).sub (hf.mul_const _)
    have hsecond : Integrable
        (fun y => (∫ x, φ x * ψ x ∂ν) - φ y * (∫ x, ψ x ∂ν) -
          ψ y * (∫ x, φ x ∂ν)) ν := hfirst.sub (hg.mul_const _)
    rw [integral_add hsecond hfg, integral_sub hfirst (hg.mul_const _),
      integral_sub (integrable_const _) (hf.mul_const _)]
    simp only [integral_mul_const, integral_const, probReal_univ, one_smul]
    ring
  have hn := positive hφ hψ ν
  rw [hout] at hn
  linarith
