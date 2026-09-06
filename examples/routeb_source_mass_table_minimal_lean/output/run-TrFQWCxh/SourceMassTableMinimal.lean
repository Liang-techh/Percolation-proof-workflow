import Mathlib

set_option autoImplicit false

namespace RouteBSourceMassTableMinimal

noncomputable section

abbrev V3 := Fin 3
abbrev V6 := Fin 6
abbrev Mat (m n : ℕ) := Fin m → Fin n → ℝ
abbrev JMat := Mat 3 6
abbrev Mat3 := Mat 3 3

def weightedGram (J : Mat 3 6) (W : Mat 3 3) : Mat 6 6 :=
  fun i j => ∑ a : V3, ∑ b : V3, J a i * W a b * J b j

def scalarIdentity (s : ℝ) : Mat3 :=
  fun a b => if a = b then s else 0

def linkMass (Jv Jw : JMat) (mass scalar : ℝ) : Mat 6 6 :=
  fun i j =>
    mass * (∑ a : V3, Jv a i * Jv a j) +
      weightedGram Jw (scalarIdentity scalar) i j

def sourceMassTable : V6 → ℚ :=
  ![1, 4 / 5, 3 / 5, 2 / 5, 3 / 10, 3 / 20]

def sourceInertiaScalarTable : V6 → ℚ :=
  ![1 / 3, 1 / 5, 7 / 60, 1 / 15, 1 / 30, 1 / 60]

theorem sourceMassTable_values (k : V6) :
    sourceMassTable k =
      ![(1 : ℚ), 4 / 5, 3 / 5, 2 / 5, 3 / 10, 3 / 20] k := by
  rfl

theorem sourceInertiaScalarTable_values (k : V6) :
    sourceInertiaScalarTable k =
      ![(1 : ℚ) / 3, 1 / 5, 7 / 60, 1 / 15, 1 / 30, 1 / 60] k := by
  rfl

theorem sourceMassTable_nonnegative (k : V6) : 0 ≤ sourceMassTable k := by
  fin_cases k <;> norm_num [sourceMassTable]

theorem sourceInertiaScalarTable_nonnegative (k : V6) :
    0 ≤ sourceInertiaScalarTable k := by
  fin_cases k <;> norm_num [sourceInertiaScalarTable]

theorem scalarIdentity_entry (s : ℝ) (a b : V3) :
    scalarIdentity s a b = if a = b then s else 0 := by
  rfl

theorem weightedGram_scalarIdentity_entry (J : JMat) (s : ℝ) (i j : V6) :
    weightedGram J (scalarIdentity s) i j =
      s * (∑ a : V3, J a i * J a j) := by
  simp [weightedGram, scalarIdentity, Fin.sum_univ_succ]
  ring_nf

theorem linkMass_entry_scalarIdentity (Jv Jw : JMat)
    (mass scalar : ℝ) (i j : V6) :
    linkMass Jv Jw mass scalar i j =
      mass * (∑ a : V3, Jv a i * Jv a j) +
        scalar * (∑ a : V3, Jw a i * Jw a j) := by
  simp only [linkMass]
  rw [weightedGram_scalarIdentity_entry]

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

theorem sourceInertiaScalarTable_exact_entries :
    sourceInertiaScalarTable 0 = 1 / 3 ∧
    sourceInertiaScalarTable 1 = 1 / 5 ∧
    sourceInertiaScalarTable 2 = 7 / 60 ∧
    sourceInertiaScalarTable 3 = 1 / 15 ∧
    sourceInertiaScalarTable 4 = 1 / 30 ∧
    sourceInertiaScalarTable 5 = 1 / 60 := by
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

#print axioms sourceMassTable_exact_entries
#print axioms sourceInertiaScalarTable_exact_entries
#print axioms linkMass_entry_scalarIdentity

end
end RouteBSourceMassTableMinimal
