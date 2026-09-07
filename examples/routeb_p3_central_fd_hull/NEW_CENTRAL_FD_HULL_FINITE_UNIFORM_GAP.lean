import Mathlib.Data.Real.Basic
import Mathlib.Data.Finset.Lattice
import Mathlib.Tactic

/-!
# P3 finite-grid uniform gap extraction

For a nonempty Finset, pointwise positive exact-real gaps have a positive
finite infimum.  The result is deliberately scoped to the supplied Finset;
the final Bool example records why this cannot be promoted to a global-domain
statement without a coverage theorem.
-/

set_option autoImplicit false

namespace RouteBP3CentralFDHullFiniteUniformGap

noncomputable section

def finiteUniformGap {D : Type*}
    (grid : Finset D) (hGrid : grid.Nonempty) (gap : D → ℝ) : ℝ :=
  grid.inf' hGrid gap

theorem finite_uniform_gap_positive
    {D : Type*} (grid : Finset D) (hGrid : grid.Nonempty)
    (gap : D → ℝ)
    (hPointwise : ∀ x, x ∈ grid → 0 < gap x) :
    0 < finiteUniformGap grid hGrid gap := by
  have hMem : finiteUniformGap grid hGrid gap ∈ grid.image gap := by
    exact Finset.inf'_mem grid hGrid gap
  rcases hMem with ⟨x, hx, hValue⟩
  rw [← hValue]
  exact hPointwise x hx

theorem finite_uniform_gap_lower
    {D : Type*} (grid : Finset D) (hGrid : grid.Nonempty)
    (gap : D → ℝ) (x : D) (hx : x ∈ grid) :
    finiteUniformGap grid hGrid gap ≤ gap x := by
  exact Finset.inf'_le grid hGrid gap hx

theorem finite_uniform_gap_certificate
    {D : Type*} (grid : Finset D) (hGrid : grid.Nonempty)
    (gap : D → ℝ)
    (hPointwise : ∀ x, x ∈ grid → 0 < gap x) :
    0 < finiteUniformGap grid hGrid gap ∧
      ∀ x, x ∈ grid → finiteUniformGap grid hGrid gap ≤ gap x := by
  constructor
  · exact finite_uniform_gap_positive grid hGrid gap hPointwise
  · exact finite_uniform_gap_lower grid hGrid gap

/-! A finite-grid lower bound does not control an omitted point. -/

def boundaryGrid : Finset Bool := {false}

def boundaryGap : Bool → ℝ
  | false => 1
  | true => 0

theorem finite_grid_lower_bound_not_global :
    (∀ x, x ∈ boundaryGrid → (1 : ℝ) ≤ boundaryGap x) ∧
      (∃ y, boundaryGap y < (1 : ℝ)) := by
  constructor
  · intro x hx
    have hFalse : x = false := by
      simpa [boundaryGrid] using hx
    subst x
    norm_num [boundaryGap]
  · exact ⟨true, by norm_num [boundaryGap]⟩

end

end RouteBP3CentralFDHullFiniteUniformGap

#print axioms RouteBP3CentralFDHullFiniteUniformGap.finite_uniform_gap_positive
#print axioms RouteBP3CentralFDHullFiniteUniformGap.finite_uniform_gap_lower
#print axioms RouteBP3CentralFDHullFiniteUniformGap.finite_grid_lower_bound_not_global
