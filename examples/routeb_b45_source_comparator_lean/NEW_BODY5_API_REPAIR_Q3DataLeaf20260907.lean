import NEW_BODY5_API_REPAIR_Q3Slice20260907

set_option autoImplicit false

namespace NEW_BODY5_API_REPAIR_Q3DataLeaf20260907

open RouteBO1PerBodyTraceGenerated
open NEW_BODY5_API_REPAIR_RowCode20260907
open NEW_BODY5_API_REPAIR_Q3Slice20260907

/-!
OPEN / UNCOMPILED finite decision candidates. These `decide` bodies have NOT run.
No classical instance is introduced. TupleRowCode contains only Fin and Int
products; its decision procedure does not compare functions or normalized Rat.
Resource limits are candidate budgets, not measured successful bounds.
-/

set_option maxRecDepth 4096 in
set_option maxHeartbeats 800000 in
theorem q3_source_tuple_codes :
    List.Perm (sourceQ3Rows.map tupleRowCode) (q3PairedRows.map tupleRowCode) := by
  decide

set_option maxRecDepth 4096 in
set_option maxHeartbeats 800000 in
theorem q3_counts : sourceQ3Rows.length = 16 ∧
    q3Representatives.length = 8 ∧ q3PairedRows.length = 16 := by
  decide

theorem q3_source_binding : List.Perm sourceQ3Rows q3PairedRows := by
  exact perm_of_tupleRowCodes sourceQ3Rows q3PairedRows q3_source_tuple_codes

end NEW_BODY5_API_REPAIR_Q3DataLeaf20260907
