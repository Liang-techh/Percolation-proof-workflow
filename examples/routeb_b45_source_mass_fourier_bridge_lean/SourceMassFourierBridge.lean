import Mathlib

set_option autoImplicit false

namespace RouteBB45SourceMassFourierBridge

noncomputable section

abbrev V3 := Fin 3
abbrev V6 := Fin 6
abbrev Vec6 := V6 → ℝ
abbrev Mat6 := V6 → V6 → ℝ

/- The source table is kept on the exact-real side.  No CSV or Float64 value is
   used by this sidecar. -/
def sourceMassTable : V6 → ℝ :=
  ![1, 4 / 5, 3 / 5, 2 / 5, 3 / 10, 3 / 20]

def sourceInertiaScalarTable : V6 → ℝ :=
  ![1 / 3, 1 / 5, 7 / 60, 1 / 15, 1 / 30, 1 / 60]

def bodyContribution
    (Jv Jw : V6 → V3 → V6 → ℝ) (body i j : V6) : ℝ :=
  sourceMassTable body *
      (∑ a : V3, Jv body a i * Jv body a j) +
    sourceInertiaScalarTable body *
      (∑ a : V3, Jw body a i * Jw body a j)

def sourceUnregularizedMass
    (Jv Jw : V6 → V3 → V6 → ℝ) : Mat6 :=
  fun i j => ∑ body : V6, bodyContribution Jv Jw body i j

def addMassRegularizer (M : Mat6) : Mat6 :=
  fun i j => M i j + if i = j then (1 / 1000000 : ℝ) else 0

/- `fourierBody` is deliberately an abstract exact evaluator for one body.
   The physical DH-to-Fourier comparator is the only premise below. -/
def fullSixBodyFourierMass
    (fourierBody : V6 → Vec6 → V6 → V6 → ℝ)
    (q : Vec6) : Mat6 :=
  fun i j => ∑ body : V6, fourierBody body q i j

theorem sourceMassTable_exact_entries :
    sourceMassTable 0 = 1 ∧
    sourceMassTable 1 = 4 / 5 ∧
    sourceMassTable 2 = 3 / 5 ∧
    sourceMassTable 3 = 2 / 5 ∧
    sourceMassTable 4 = 3 / 10 ∧
    sourceMassTable 5 = 3 / 20 := by
  constructor
  · rfl
  constructor
  · rfl
  constructor
  · rfl
  constructor
  · rfl
  constructor
  · rfl
  · rfl

theorem sourceMass_to_regularized_fullSixBodyFourier
    (Jv Jw : V6 → V3 → V6 → ℝ)
    (fourierBody : V6 → Vec6 → V6 → V6 → ℝ)
    (q : Vec6) (i j : V6)
    (h_body : ∀ body, ∀ r s,
      bodyContribution Jv Jw body r s = fourierBody body q r s) :
    addMassRegularizer (sourceUnregularizedMass Jv Jw) i j =
      fullSixBodyFourierMass fourierBody q i j +
        if i = j then (1 / 1000000 : ℝ) else 0 := by
  unfold addMassRegularizer sourceUnregularizedMass fullSixBodyFourierMass
  congr 1
  apply Finset.sum_congr rfl
  intro body hmem
  exact h_body body i j

theorem sourceMass_to_regularized_fullSixBodyFourier_offdiag
    (Jv Jw : V6 → V3 → V6 → ℝ)
    (fourierBody : V6 → Vec6 → V6 → V6 → ℝ)
    (q : Vec6) {i j : V6} (hij : i ≠ j)
    (h_body : ∀ body, ∀ r s,
      bodyContribution Jv Jw body r s = fourierBody body q r s) :
    addMassRegularizer (sourceUnregularizedMass Jv Jw) i j =
      fullSixBodyFourierMass fourierBody q i j := by
  rw [sourceMass_to_regularized_fullSixBodyFourier Jv Jw fourierBody q i j h_body]
  simp [hij]

/- This is the exact logical seam: the table and regularizer are proved here;
   `h_body` still has to be supplied by the DH/frame/Jacobian/Fourier audit. -/
#print axioms sourceMass_to_regularized_fullSixBodyFourier
#print axioms sourceMass_to_regularized_fullSixBodyFourier_offdiag

end
end RouteBB45SourceMassFourierBridge
