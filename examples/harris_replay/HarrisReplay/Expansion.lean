import Mathlib.MeasureTheory.Integral.Prod
import Mathlib.Tactic

namespace HarrisReplay

open MeasureTheory

theorem inner_expansion {Y : Type*} [MeasurableSpace Y]
    (ν : Measure Y) [IsProbabilityMeasure ν] {φ ψ : Y → ℝ}
    (hf : Integrable φ ν) (hg : Integrable ψ ν)
    (hfg : Integrable (fun x => φ x * ψ x) ν) (y : Y) :
    (∫ x, (φ x - φ y) * (ψ x - ψ y) ∂ν) =
      (∫ x, φ x * ψ x ∂ν) - φ y * (∫ x, ψ x ∂ν) -
        ψ y * (∫ x, φ x ∂ν) + φ y * ψ y := by
  have hpoint : (fun x => (φ x - φ y) * (ψ x - ψ y)) =
      (fun x => ((φ x * ψ x - φ y * ψ x) - ψ y * φ x) + φ y * ψ y) := by
    funext x
    ring
  rw [hpoint]
  have hsub : Integrable (fun x => φ x * ψ x - φ y * ψ x) ν :=
    hfg.sub (hg.const_mul (φ y))
  have hsub' : Integrable (fun x => φ x * ψ x - φ y * ψ x - ψ y * φ x) ν :=
    hsub.sub (hf.const_mul (ψ y))
  rw [integral_add hsub' (integrable_const (φ y * ψ y))]
  rw [integral_sub hsub (hf.const_mul (ψ y))]
  rw [integral_sub hfg (hg.const_mul (φ y))]
  simp only [integral_const_mul, integral_const, probReal_univ,
    one_smul]

end HarrisReplay
