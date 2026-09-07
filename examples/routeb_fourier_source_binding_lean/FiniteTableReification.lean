import Mathlib
import ExactCoefficientBridge

set_option autoImplicit false

namespace RouteBFourierSourceBinding

/-!
  A deliberately small reification seam for the P3 source binding.

  A payload is data, not a theorem: the caller must provide the rows and the
  three structural checks below.  In particular, this file does not encode
  the Julia source or invent the 610 rows.
-/

abbrev Entry := V6 × V6

structure Row where
  entry : Entry
  frequency : Frequency
  coefficient : Coefficient
deriving DecidableEq

namespace Row

def key (r : Row) : Entry × Frequency := (r.entry, r.frequency)

end Row

structure FiniteCoefficientTable where
  rows : List Row
  entries : Finset Entry
  support : Entry → Finset Frequency
  /-- No two rows describe the same matrix-entry/frequency coefficient. -/
  keys_nodup : (rows.map Row.key).Nodup
  /-- The finite support is exactly the support represented by the rows. -/
  support_complete : ∀ e ν, ν ∈ support e ↔ (e, ν) ∈ rows.map Row.key
  /-- Every declared matrix entry occurs in at least one row, and no other
      entry occurs. -/
  entries_complete : ∀ e, e ∈ entries ↔ ∃ r ∈ rows, r.entry = e

def FullEntries : Finset Entry := Finset.univ

theorem full_entries_card : FullEntries.card = 36 := by
  simp [FullEntries, Fintype.card_prod, Fintype.card_fin]

def HasShape (table : FiniteCoefficientTable) (entryCount rowCount : Nat) : Prop :=
  table.entries.card = entryCount ∧ table.rows.length = rowCount

theorem shape36_forces_all_matrix_entries
    (table : FiniteCoefficientTable) (rowCount : Nat)
    (hshape : HasShape table 36 rowCount) :
    table.entries = FullEntries := by
  apply Finset.eq_univ_of_card
  simpa [FullEntries] using hshape.1

theorem rows_give_map_equality_on_support
    (source csv : CoefficientMap) (table : FiniteCoefficientTable)
    (hsource : ∀ r ∈ table.rows,
      source r.entry.1 r.entry.2 r.frequency = r.coefficient)
    (hcsv : ∀ r ∈ table.rows,
      csv r.entry.1 r.entry.2 r.frequency = r.coefficient) :
    ∀ i j ν, ν ∈ table.support (i, j) → source i j ν = csv i j ν := by
  intro i j ν hν
  have hkey : ((i, j), ν) ∈ table.rows.map Row.key :=
    (table.support_complete (i, j) ν).mp hν
  rcases List.mem_map.mp hkey with ⟨r, hr, hrow⟩
  have hentry : r.entry = (i, j) := congrArg Prod.fst hrow
  have hfrequency : r.frequency = ν := congrArg Prod.snd hrow
  have hs := hsource r hr
  have hc := hcsv r hr
  simpa [hentry, hfrequency] using hs.trans hc.symm

theorem finite_table_checker_sound
    (source csv : CoefficientMap) (table : FiniteCoefficientTable)
    (hsource : ∀ r ∈ table.rows,
      source r.entry.1 r.entry.2 r.frequency = r.coefficient)
    (hcsv : ∀ r ∈ table.rows,
      csv r.entry.1 r.entry.2 r.frequency = r.coefficient) :
    ∀ i j, ∀ ν ∈ table.support (i, j),
      source i j ν = csv i j ν := by
  exact rows_give_map_equality_on_support source csv table hsource hcsv

/- A tiny concrete smoke instance.  It checks the seam without pretending to
   be a fragment of the 610-row artifact. -/
def smokeRow : Row :=
  { entry := (0, 0), frequency := fun _ => 0, coefficient := (1, 0) }

def smokeTable : FiniteCoefficientTable where
  rows := [smokeRow]
  entries := {(0, 0)}
  support := fun e => if e = (0, 0) then {fun _ => 0} else ∅
  keys_nodup := by simp [smokeRow, Row.key]
  support_complete := by
    intro e ν
    by_cases he : e = (0, 0)
    · subst e
      simp [smokeRow, Row.key]
    · simp [smokeRow, Row.key, he]
  entries_complete := by
    intro e
    by_cases he : e = (0, 0)
    · subst e
      simp [smokeRow]
    · simp [smokeRow, he, Ne.symm he]

theorem smoke_shape : HasShape smokeTable 1 1 := by
  simp [HasShape, smokeTable]

theorem smoke_checker_example
    (source csv : CoefficientMap)
    (hsource : ∀ r ∈ smokeTable.rows,
      source r.entry.1 r.entry.2 r.frequency = r.coefficient)
    (hcsv : ∀ r ∈ smokeTable.rows,
      csv r.entry.1 r.entry.2 r.frequency = r.coefficient) :
    ∀ i j, ∀ ν ∈ smokeTable.support (i, j),
      source i j ν = csv i j ν := by
  exact finite_table_checker_sound source csv smokeTable hsource hcsv

/- The intended 610-row use is simply a future value of `payload` supplied by
   a generated, reviewed Lean file.  Keeping it as a parameter makes the
   first missing equality explicit instead of hiding it behind an axiom. -/
theorem routeB_610_payload_obligation
    (payload : FiniteCoefficientTable)
    (_hshape : HasShape payload 36 610)
    (source csv : CoefficientMap)
    (hsource : ∀ r ∈ payload.rows,
      source r.entry.1 r.entry.2 r.frequency = r.coefficient)
    (hcsv : ∀ r ∈ payload.rows,
      csv r.entry.1 r.entry.2 r.frequency = r.coefficient) :
    ∀ i j, ∀ ν ∈ payload.support (i, j),
      source i j ν = csv i j ν := by
  exact finite_table_checker_sound source csv payload hsource hcsv

#print axioms full_entries_card
#print axioms shape36_forces_all_matrix_entries
#print axioms rows_give_map_equality_on_support
#print axioms finite_table_checker_sound
#print axioms smoke_checker_example
#print axioms routeB_610_payload_obligation

end RouteBFourierSourceBinding
