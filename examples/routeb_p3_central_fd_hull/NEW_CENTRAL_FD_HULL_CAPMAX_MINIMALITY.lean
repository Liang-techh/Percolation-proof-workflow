import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
# P3 capMax minimality and witness equivalence

This sidecar consumes the explicit upper-bound/attainment witness shape from
the preceding capMax leaf.  It proves only finite order algebra: capMax is the
least scalar upper bound, two witnesses for the same cap vector have the same
scalar, and attainment indices are value-equivalent but need not be unique.
-/

set_option autoImplicit false

namespace RouteBP3CentralFDHullCapMaxMinimality

noncomputable section

abbrev I6 := Fin 6
abbrev Vector6 := I6 → ℝ

/-- Shape-compatible copy of the preceding explicit cap-max contract. -/
structure CapMaxWitness6 where
  qCap : Vector6
  capMax : ℝ
  qCap_nonneg : ∀ i, 0 ≤ qCap i
  upper_bound : ∀ i, qCap i ≤ capMax
  attained : ∃ i, qCap i = capMax

theorem capMax_le_candidate6
    (W : CapMaxWitness6) (candidate : ℝ)
    (hCandidate : ∀ i, W.qCap i ≤ candidate) :
    W.capMax ≤ candidate := by
  obtain ⟨i, hi⟩ := W.attained
  rw [← hi]
  exact hCandidate i

theorem candidate_equals_capMax6
    (W : CapMaxWitness6) (candidate : ℝ)
    (hCandidate : ∀ i, W.qCap i ≤ candidate)
    (hCandidate_attained : ∃ i, W.qCap i = candidate) :
    candidate = W.capMax := by
  apply le_antisymm
  · obtain ⟨i, hi⟩ := hCandidate_attained
    rw [← hi]
    exact W.upper_bound i
  · exact capMax_le_candidate6 W candidate hCandidate

theorem capMax_unique_of_same_caps6
    (W₁ W₂ : CapMaxWitness6)
    (hCaps : W₁.qCap = W₂.qCap) :
    W₁.capMax = W₂.capMax := by
  apply le_antisymm
  · exact capMax_le_candidate6 W₁ W₂.capMax (by
      intro i
      rw [hCaps]
      exact W₂.upper_bound i)
  · exact capMax_le_candidate6 W₂ W₁.capMax (by
      intro i
      rw [← hCaps]
      exact W₁.upper_bound i)

theorem attainment_values_equivalent6
    (W : CapMaxWitness6) (i₁ i₂ : I6)
    (h₁ : W.qCap i₁ = W.capMax)
    (h₂ : W.qCap i₂ = W.capMax) :
    W.qCap i₁ = W.qCap i₂ := by
  rw [h₁, h₂]

theorem upper_attainment_equiv_capMax6
    (W : CapMaxWitness6) (candidate : ℝ)
    (hUpper : ∀ i, W.qCap i ≤ candidate) :
    (∃ i, W.qCap i = candidate) ↔ candidate = W.capMax := by
  constructor
  · intro hAttained
    exact candidate_equals_capMax6 W candidate hUpper hAttained
  · intro hEq
    obtain ⟨i, hi⟩ := W.attained
    refine ⟨i, ?_⟩
    rw [hi, hEq]

end

end RouteBP3CentralFDHullCapMaxMinimality

#print axioms RouteBP3CentralFDHullCapMaxMinimality.capMax_le_candidate6
#print axioms RouteBP3CentralFDHullCapMaxMinimality.candidate_equals_capMax6
#print axioms RouteBP3CentralFDHullCapMaxMinimality.capMax_unique_of_same_caps6
#print axioms RouteBP3CentralFDHullCapMaxMinimality.attainment_values_equivalent6
