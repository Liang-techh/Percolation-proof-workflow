import FiniteTableReification
import PayloadRows

set_option autoImplicit false
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000

namespace RouteBFourierPayloadLean

open RouteBFourierSourceBinding

def payloadSupport (e : Entry) : Finset Frequency :=
  (payloadRows.filter (fun r => r.entry = e)).map Row.frequency |>.toFinset

def payloadEntries : Finset Entry :=
  payloadNonemptyEntries

def payloadSupportMap : SupportMap :=
  fun i j => payloadSupport (i, j)

def payloadTable : FiniteCoefficientTable where
  rows := payloadRows
  entries := payloadEntries
  support := payloadSupport
  keys_nodup := by
    decide
  support_complete := by
    intro e ν
    simp only [payloadSupport, List.mem_toFinset, List.mem_map,
      List.mem_filter, Row.key]
    simp only [decide_eq_true_eq, Prod.mk.injEq]
    constructor
    · rintro ⟨a, ⟨ha, hae⟩, hav⟩
      exact ⟨a, ha, ⟨hae, hav⟩⟩
    · rintro ⟨a, ha, ⟨hae, hav⟩⟩
      exact ⟨a, ⟨ha, hae⟩, hav⟩
  entries_complete := by
    intro e
    fin_cases e <;> decide

theorem payload_rows_length : payloadTable.rows.length = 610 := by
  decide

theorem payload_unique_keys : (payloadTable.rows.map Row.key).Nodup := by
  exact payloadTable.keys_nodup

theorem payload_nonempty_entry_card : payloadTable.entries.card = 32 := by
  decide

theorem payload_full_entry_card : FullEntries.card = 36 := by
  exact full_entries_card

theorem payload_support_complete :
    ∀ e ν, ν ∈ payloadTable.support e ↔
      (e, ν) ∈ payloadTable.rows.map Row.key := by
  exact payloadTable.support_complete

theorem payload_missing_entries_have_empty_support
    (e : Entry) (he : e ∉ payloadTable.entries) :
    payloadTable.support e = ∅ := by
  ext ν
  constructor
  · intro h
    have hkey := (payloadTable.support_complete e ν).mp h
    rcases List.mem_map.mp hkey with ⟨r, hr, hrow⟩
    have hex : ∃ r ∈ payloadTable.rows, r.entry = e :=
      ⟨r, hr, congrArg Prod.fst hrow⟩
    exact False.elim (he ((payloadTable.entries_complete e).mpr hex))
  · intro h
    simp at h

def HasFullMatrixShape (table : FiniteCoefficientTable) (rowCount : Nat) : Prop :=
  FullEntries.card = 36 ∧ table.rows.length = rowCount ∧
    ∀ e, e ∈ FullEntries → e ∈ table.entries ∨ table.support e = ∅

theorem payload_full_matrix_shape : HasFullMatrixShape payloadTable 610 := by
  refine ⟨payload_full_entry_card, payload_rows_length, ?_⟩
  intro e he
  by_cases h : e ∈ payloadTable.entries
  · exact Or.inl h
  · exact Or.inr (payload_missing_entries_have_empty_support e h)

def lookupCoefficient : (Entry × Frequency) → List Row → Option Coefficient
  | _, [] => none
  | key, r :: rs =>
      if Row.key r = key then some r.coefficient
      else lookupCoefficient key rs

theorem lookupCoefficient_of_mem
    {xs : List Row} (hnodup : (xs.map Row.key).Nodup)
    {r : Row} (hr : r ∈ xs) :
    lookupCoefficient (Row.key r) xs = some r.coefficient := by
  induction xs with
  | nil => simp at hr
  | cons x xs ih =>
    have hparts : (Row.key x :: xs.map Row.key).Nodup := by
      simpa using hnodup
    rcases List.nodup_cons.mp hparts with ⟨hx, htail⟩
    have hr' : r = x ∨ r ∈ xs := by
      simpa only [List.mem_cons] using hr
    rcases hr' with rfl | hr
    · simp [lookupCoefficient]
    · have hne : Row.key x ≠ Row.key r := by
        intro heq
        apply hx
        rw [heq]
        exact List.mem_map.mpr ⟨r, hr, rfl⟩
      simp [lookupCoefficient, hne, ih htail hr]

def frozenCsvCoeff : CoefficientMap :=
  fun i j ν =>
    (lookupCoefficient ((i, j), ν) payloadTable.rows).getD (0, 0)

theorem frozen_csv_row_equality (r : Row) (hr : r ∈ payloadTable.rows) :
    frozenCsvCoeff r.entry.1 r.entry.2 r.frequency = r.coefficient := by
  change (lookupCoefficient (Row.key r) payloadTable.rows).getD (0, 0) = r.coefficient
  rw [lookupCoefficient_of_mem payloadTable.keys_nodup hr]
  rfl

theorem conditional_source_csv_equality_on_support
    (source : CoefficientMap)
    (hsource : ∀ r ∈ payloadTable.rows,
      source r.entry.1 r.entry.2 r.frequency = r.coefficient) :
    ∀ i j, ∀ ν ∈ payloadTable.support (i, j),
      source i j ν = frozenCsvCoeff i j ν := by
  exact finite_table_checker_sound source frozenCsvCoeff payloadTable hsource
    (fun r hr => frozen_csv_row_equality r hr)

theorem conditional_source_evaluator_equality
    (source : CoefficientMap) (q : Vec6)
    (hsource : ∀ r ∈ payloadTable.rows,
      source r.entry.1 r.entry.2 r.frequency = r.coefficient) :
    evalMatrix source payloadSupportMap q =
      evalMatrix frozenCsvCoeff payloadSupportMap q := by
  apply evalMatrix_congr_on_support source frozenCsvCoeff payloadSupportMap q
  intro i j ν hν
  exact conditional_source_csv_equality_on_support source hsource i j ν hν

/-
Open obligation, intentionally not a declaration of a source map:

  exactizedDHSourceCoeff i j ν = frozenCsvCoeff i j ν

The exactized DH map is not reified in this sidecar.  Consequently the
conditional source theorems above do not close that equality and cannot be
reported as a Lean theorem about the external DH implementation.
-/

end RouteBFourierPayloadLean
