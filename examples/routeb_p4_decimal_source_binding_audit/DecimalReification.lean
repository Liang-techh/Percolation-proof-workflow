import Mathlib.Data.Real.Basic
import Mathlib.Tactic

set_option autoImplicit false

namespace RouteBP4DecimalSourceBindingAudit

noncomputable section

/- This leaf certifies only the exact interpretation of the exported decimal
   spelling. It contains no DH implementation and no Float64 semantics. -/
def exportedDecimal : ℝ := 0.116667666666667
def exportedRational : ℝ := 116667666666667 / 1000000000000000

theorem decimal_spelling_reifies_exactly :
    exportedDecimal = exportedRational := by
  norm_num [exportedDecimal, exportedRational]

theorem decimal_spelling_positive : 0 < exportedDecimal := by
  norm_num [exportedDecimal]

end
end RouteBP4DecimalSourceBindingAudit
