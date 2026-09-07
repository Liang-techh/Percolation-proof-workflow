import BodyTraceEvaluator
import NEW_BODY5_API_REPAIR_ListFinset20260907

set_option autoImplicit false

namespace NEW_BODY5_API_REPAIR_RowCode20260907

open RouteBO1PerBodyTraceGenerated
open NEW_BODY5_API_REPAIR_ListFinset20260907

/-!
OPEN / UNCOMPILED. Same raw fields as the finite skeleton, in a fresh namespace.
No BodyTraceRow equality instance, rational normalization, or skeleton import.
The tuple encoding is an alternative decision surface, with an explicit decoder.
-/

abbrev RowCode := Fin 6 × Fin 6 × Fin 6 × (Fin 6 → ℤ) × ℤ × ℤ × ℤ × ℤ

def rowCode (r : BodyTraceRow) : RowCode :=
  (r.body, r.row, r.col, r.frequency, r.realCoeff.numerator,
    r.realCoeff.denominator, r.imagCoeff.numerator, r.imagCoeff.denominator)

def decodeRow (c : RowCode) : BodyTraceRow :=
  let (b, i, j, nu, rn, rd, imn, imd) := c
  ⟨b, i, j, nu, ⟨rn, rd⟩, ⟨imn, imd⟩⟩

theorem decode_rowCode (r : BodyTraceRow) : decodeRow (rowCode r) = r := by
  cases r with
  | mk b i j nu re im =>
      cases re
      cases im
      rfl

theorem perm_of_rowCodes (xs ys : List BodyTraceRow)
    (h : List.Perm (xs.map rowCode) (ys.map rowCode)) : List.Perm xs ys := by
  exact perm_of_encoded rowCode decodeRow decode_rowCode xs ys h

abbrev FrequencyCode := ℤ × ℤ × ℤ × ℤ × ℤ × ℤ
abbrev TupleRowCode := Fin 6 × Fin 6 × Fin 6 × FrequencyCode × ℤ × ℤ × ℤ × ℤ

def tupleRowCode (r : BodyTraceRow) : TupleRowCode :=
  (r.body, r.row, r.col,
    (r.frequency 0, r.frequency 1, r.frequency 2,
      r.frequency 3, r.frequency 4, r.frequency 5),
    r.realCoeff.numerator, r.realCoeff.denominator,
    r.imagCoeff.numerator, r.imagCoeff.denominator)

def decodeTupleRow (c : TupleRowCode) : BodyTraceRow :=
  let (b, i, j, (n0, n1, n2, n3, n4, n5), rn, rd, imn, imd) := c
  ⟨b, i, j, ![n0, n1, n2, n3, n4, n5], ⟨rn, rd⟩, ⟨imn, imd⟩⟩

theorem frequency_eta (nu : Fin 6 → ℤ) :
    ![nu 0, nu 1, nu 2, nu 3, nu 4, nu 5] = nu := by
  funext k
  fin_cases k <;> rfl

theorem decode_tupleRowCode (r : BodyTraceRow) : decodeTupleRow (tupleRowCode r) = r := by
  cases r with
  | mk b i j nu re im =>
      cases re
      cases im
      simp only [tupleRowCode, decodeTupleRow, frequency_eta]

theorem perm_of_tupleRowCodes (xs ys : List BodyTraceRow)
    (h : List.Perm (xs.map tupleRowCode) (ys.map tupleRowCode)) : List.Perm xs ys := by
  exact perm_of_encoded tupleRowCode decodeTupleRow decode_tupleRowCode xs ys h

/-- Equality of tuple codes still transports complete raw records. -/
theorem tuple_codes_to_row_codes (xs ys : List BodyTraceRow)
    (h : List.Perm (xs.map tupleRowCode) (ys.map tupleRowCode)) :
    List.Perm (xs.map rowCode) (ys.map rowCode) := by
  exact List.Perm.map rowCode (perm_of_tupleRowCodes xs ys h)

end NEW_BODY5_API_REPAIR_RowCode20260907
