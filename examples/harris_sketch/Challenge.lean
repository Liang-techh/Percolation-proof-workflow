import Mathlib.MeasureTheory.Integral.Prod
import Mathlib.Tactic

open MeasureTheory
namespace HarrisReplay

theorem harris {Y : Type*} [MeasurableSpace Y] [LinearOrder Y]
    (ν : Measure Y) [IsProbabilityMeasure ν] {φ ψ : Y → ℝ}
    (hφ : Monotone φ) (hψ : Monotone ψ)
    (hφm : Measurable φ) (hψm : Measurable ψ) {C : ℝ}
    (hφb : ∀ y, ‖φ y‖ ≤ C) (hψb : ∀ y, ‖ψ y‖ ≤ C) :
    (∫ y, φ y ∂ν) * (∫ y, ψ y ∂ν) ≤ ∫ y, φ y * ψ y ∂ν := by
  sorry

end HarrisReplay

namespace HarrisReplay

theorem iterated_nonneg {Y : Type*} [LinearOrder Y] [MeasurableSpace Y]
    {φ ψ : Y → ℝ} (hφ : Monotone φ) (hψ : Monotone ψ) (ν : Measure Y) :
    0 ≤ ∫ y, (∫ x, (φ x - φ y) * (ψ x - ψ y) ∂ν) ∂ν := by
  sorry

theorem inner_expansion {Y : Type*} [MeasurableSpace Y]
    (ν : Measure Y) [IsProbabilityMeasure ν] {φ ψ : Y → ℝ}
    (hf : Integrable φ ν) (hg : Integrable ψ ν)
    (hfg : Integrable (fun x => φ x * ψ x) ν) (y : Y) :
    (∫ x, (φ x - φ y) * (ψ x - ψ y) ∂ν) =
      (∫ x, φ x * ψ x ∂ν) - φ y * (∫ x, ψ x ∂ν) -
        ψ y * (∫ x, φ x ∂ν) + φ y * ψ y := by
  sorry

end HarrisReplay
