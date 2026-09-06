import SourceMassFourierBridge

set_option autoImplicit false

namespace RouteBB45Full610AggregateComparator

noncomputable section

abbrev V6 := Fin 6
abbrev V3 := Fin 3
abbrev Vec6 := V6 → ℝ
abbrev Mat6 := V6 → V6 → ℝ
abbrev Row := Fin 610

def toJuliaIndex (i : V6) : Nat := i.val + 1

theorem toJuliaIndex_is_one_based (i : V6) :
    1 ≤ toJuliaIndex i ∧ toJuliaIndex i ≤ 6 := by
  simp [toJuliaIndex]

def fromJuliaIndex (n : Nat) (h : 1 ≤ n ∧ n ≤ 6) : V6 :=
  ⟨n - 1, by omega⟩

theorem fromJuliaIndex_roundtrip (n : Nat) (h : 1 ≤ n ∧ n ≤ 6) :
    toJuliaIndex (fromJuliaIndex n h) = n := by
  simp [fromJuliaIndex, toJuliaIndex]
  omega

/- The row schema mirrors the full mass CSV, after transporting its one-based
   row/column labels to `Fin 6`.  A row is a Fourier atom of one matrix entry;
   the CSV itself does not carry a body label. -/
structure CsvMassRow where
  row : V6
  col : V6
  frequency : V6 → ℤ
  realCoeff : ℚ
  imagCoeff : ℚ

def phase (r : CsvMassRow) (q : Vec6) : ℝ :=
  ∑ k : V6, (r.frequency k : ℝ) * q k

def evalRow (r : CsvMassRow) (q : Vec6) : ℝ :=
  (r.realCoeff : ℝ) * Real.cos (phase r q) -
    (r.imagCoeff : ℝ) * Real.sin (phase r q)

def csvAggregate (payload : Row → CsvMassRow) (q : Vec6) : Mat6 :=
  fun i j => ∑ n : Row,
    if (payload n).row = i ∧ (payload n).col = j
    then evalRow (payload n) q
    else 0

def csvAggregateBodySum
    (fourierBody : V6 → Vec6 → V6 → V6 → ℝ)
    (q : Vec6) : Mat6 :=
  fun i j => ∑ body : V6, fourierBody body q i j

def regularizedSourceMass
    (Jv Jw : V6 → V3 → V6 → ℝ) : Mat6 :=
  RouteBB45SourceMassFourierBridge.addMassRegularizer
    (RouteBB45SourceMassFourierBridge.sourceUnregularizedMass Jv Jw)

/- This is the exact minimum comparator contract for the 610-row payload.
   It deliberately separates the data-level aggregate binding from the
   six-body semantic sum.  The premise is the unresolved DH/Fourier/source
   comparator, not an opaque theorem axiom. -/
theorem regularized_source_eq_full_610_aggregate
    (Jv Jw : V6 → V3 → V6 → ℝ)
    (payload : Row → CsvMassRow)
    (fourierBody : V6 → Vec6 → V6 → V6 → ℝ)
    (q : Vec6)
    (i j : V6)
    (h_aggregate : ∀ i j,
      csvAggregate payload q i j =
        csvAggregateBodySum fourierBody q i j)
    (h_body : ∀ body, ∀ i j,
      RouteBB45SourceMassFourierBridge.bodyContribution Jv Jw body i j =
        fourierBody body q i j) :
    regularizedSourceMass Jv Jw i j =
      csvAggregate payload q i j +
        if i = j then (1 / 1000000 : ℝ) else 0 := by
  unfold regularizedSourceMass
  rw [RouteBB45SourceMassFourierBridge.sourceMass_to_regularized_fullSixBodyFourier
    Jv Jw fourierBody q i j h_body]
  rw [h_aggregate]
  rfl

theorem regularized_source_eq_full_610_aggregate_matrix
    (Jv Jw : V6 → V3 → V6 → ℝ)
    (payload : Row → CsvMassRow)
    (fourierBody : V6 → Vec6 → V6 → V6 → ℝ)
    (q : Vec6)
    (h_aggregate : ∀ i j,
      csvAggregate payload q i j =
        csvAggregateBodySum fourierBody q i j)
    (h_body : ∀ body, ∀ i j,
      RouteBB45SourceMassFourierBridge.bodyContribution Jv Jw body i j =
        fourierBody body q i j) :
    regularizedSourceMass Jv Jw =
      fun i j => csvAggregate payload q i j +
        if i = j then (1 / 1000000 : ℝ) else 0 := by
  funext i j
  exact regularized_source_eq_full_610_aggregate Jv Jw payload fourierBody q
    i j h_aggregate h_body

/- The payload cardinality is part of the contract, so this theorem cannot be
   discharged by substituting the separate 17-row potential table. -/
theorem payload_has_full_mass_row_cardinality : Fintype.card Row = 610 := by
  exact Fintype.card_fin 610

#print axioms regularized_source_eq_full_610_aggregate
#print axioms regularized_source_eq_full_610_aggregate_matrix
#print axioms payload_has_full_mass_row_cardinality
#print axioms fromJuliaIndex_roundtrip

end
end RouteBB45Full610AggregateComparator
