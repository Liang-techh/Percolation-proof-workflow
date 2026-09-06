import Percolation.Literature.PercolationEvents
import Mathlib.Tactic

set_option autoImplicit false
set_option relaxedAutoImplicit false
open MeasureTheory ProbabilityTheory
open scoped ENNReal
universe u
namespace Percolation.Literature

theorem harris_fkg_local
    {V : Type u} (G : SimpleGraph V) (p : unitInterval)
    {A B : Set (BondConfig V)}
    (hA : IsUpperSet A) (hB : IsUpperSet B)
    (hAl : IsLocalEvent A) (hBl : IsLocalEvent B) :
    (bondPercolation G p).real A * (bondPercolation G p).real B ≤
      (bondPercolation G p).real (A ∩ B) := by
  sorry

end Percolation.Literature
