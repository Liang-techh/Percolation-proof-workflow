import Mathlib

set_option autoImplicit false
open scoped BigOperators

namespace RouteBFourierSourceBinding

noncomputable section

abbrev V6 := Fin 6
abbrev Frequency := V6 → ℤ
abbrev Vec6 := V6 → ℝ
abbrev Mat6 := V6 → V6 → ℝ
abbrev Coefficient := ℚ × ℚ
abbrev CoefficientMap := V6 → V6 → Frequency → Coefficient
abbrev SupportMap := V6 → V6 → Finset Frequency

def phase (ν : Frequency) (q : Vec6) : ℝ :=
  ∑ k : V6, (ν k : ℝ) * q k

def evalCoefficient (c : Coefficient) (ν : Frequency) (q : Vec6) : ℝ :=
  (c.1 : ℝ) * Real.cos (phase ν q) -
    (c.2 : ℝ) * Real.sin (phase ν q)

def evalMatrix (coeff : CoefficientMap) (support : SupportMap)
    (q : Vec6) : Mat6 :=
  fun i j => ∑ ν ∈ support i j, evalCoefficient (coeff i j ν) ν q

theorem evalMatrix_congr_of_coefficients
    (source csv : CoefficientMap) (support : SupportMap) (q : Vec6)
    (hcoeff : ∀ i j ν, source i j ν = csv i j ν) :
    evalMatrix source support q = evalMatrix csv support q := by
  funext i j
  apply Finset.sum_congr rfl
  intro ν hν
  rw [hcoeff i j ν]

/- Coefficients outside the finite support are irrelevant to the finite
   Fourier evaluator.  This lemma only rewrites entries selected by the
   finite sums; it does not claim arbitrary off-support map equality. -/
theorem evalMatrix_congr_on_support
    (source csv : CoefficientMap) (support : SupportMap) (q : Vec6)
    (hcoeff : ∀ i j ν, ν ∈ support i j → source i j ν = csv i j ν) :
    evalMatrix source support q = evalMatrix csv support q := by
  funext i j
  apply Finset.sum_congr rfl
  intro ν hν
  rw [hcoeff i j ν hν]

theorem routeB_36_entry_coefficient_bridge
    (source csv : CoefficientMap) (support : SupportMap) :
    (∀ i j ν, source i j ν = csv i j ν) →
      ∀ q, evalMatrix source support q = evalMatrix csv support q := by
  intro hcoeff q
  exact evalMatrix_congr_of_coefficients source csv support q hcoeff

theorem routeB_has_36_matrix_entries : Fintype.card V6 * Fintype.card V6 = 36 := by
  norm_num

end
end RouteBFourierSourceBinding
