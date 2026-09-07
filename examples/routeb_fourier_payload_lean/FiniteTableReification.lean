import Mathlib
import ExactCoefficientBridge

set_option autoImplicit false

namespace RouteBFourierSourceBinding

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
  keys_nodup : (rows.map Row.key).Nodup
  support_complete : ∀ e ν, ν ∈ support e ↔ (e, ν) ∈ rows.map Row.key
  entries_complete : ∀ e, e ∈ entries ↔ ∃ r ∈ rows, r.entry = e

def FullEntries : Finset Entry := Finset.univ

theorem full_entries_card : FullEntries.card = 36 := by
  simp [FullEntries, Fintype.card_prod, Fintype.card_fin]

def HasShape (table : FiniteCoefficientTable) (entryCount rowCount : Nat) : Prop :=
  table.entries.card = entryCount ∧ table.rows.length = rowCount

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

end RouteBFourierSourceBinding
