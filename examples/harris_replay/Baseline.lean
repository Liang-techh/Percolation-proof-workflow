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
  aesop

end HarrisReplay
