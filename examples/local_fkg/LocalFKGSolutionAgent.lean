import LocalFKGReduction
import LocalFKGFinite
import LocalFKGMarginal

set_option autoImplicit false
set_option relaxedAutoImplicit false

universe u

namespace Percolation.Literature

open MeasureTheory ProbabilityTheory
open scoped ENNReal

theorem harris_fkg_local
    {V : Type u} (G : SimpleGraph V) (p : unitInterval)
    {A B : Set (BondConfig V)}
    (hA : IsUpperSet A) (hB : IsUpperSet B)
    (hAl : IsLocalEvent A) (hBl : IsLocalEvent B) :
    (bondPercolation G p).real A * (bondPercolation G p).real B ≤
      (bondPercolation G p).real (A ∩ B) := by
  apply LocalFKG.harris_fkg_local_of_children
  · intro ι _ q f g hf0 hg0 hf hg
    exact LocalFKG.finite_bernoulli_positive_correlation ι q f g hf0 hg0 hf hg
  · intro V G p F A hA
    exact LocalFKG.local_event_cube_expectation G p F A hA
  · exact hA
  · exact hB
  · exact hAl
  · exact hBl

end Percolation.Literature
