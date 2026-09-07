import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
# P3 strict scalar-budget to downstream-margin bridge

This sidecar consumes an already established nonuniform-to-scalar budget
comparison and a strict scalar-budget margin relation.  The result is only
order transitivity; it does not derive either premise.
-/

set_option autoImplicit false

namespace RouteBP3CentralFDHullMarginBridge

noncomputable section

abbrev I6 := Fin 6
abbrev Vector6 := I6 → ℝ

/-- Shape-compatible capMax witness consumed by the scalar budget interface. -/
structure CapMaxWitness6 where
  qCap : Vector6
  capMax : ℝ
  upper_bound : ∀ i, qCap i ≤ capMax
  attained : ∃ i, qCap i = capMax

def scalarCapBudget6 (W : CapMaxWitness6) (totalLoad : ℝ) : ℝ :=
  W.capMax * totalLoad

theorem strict_margin_transitivity6
    (nonuniformBudget scalarBudget downstreamMargin : ℝ)
    (hOrder : nonuniformBudget ≤ scalarBudget)
    (hMargin : scalarBudget < downstreamMargin) :
    nonuniformBudget < downstreamMargin :=
  lt_of_le_of_lt hOrder hMargin

/-- CapMax-specialized strict consumer.  The scalar strict-margin premise is
deliberately explicit and remains the only source of strictness. -/
theorem capMax_budget_strictly_below_margin6
    (W : CapMaxWitness6) (totalLoad nonuniformBudget downstreamMargin : ℝ)
    (hOrder : nonuniformBudget ≤ scalarCapBudget6 W totalLoad)
    (hMargin : scalarCapBudget6 W totalLoad < downstreamMargin) :
    nonuniformBudget < downstreamMargin := by
  exact strict_margin_transitivity6 nonuniformBudget
    (scalarCapBudget6 W totalLoad) downstreamMargin hOrder hMargin

structure StrictMarginBridge6 where
  capMax : ℝ
  nonuniformBudget : ℝ
  downstreamMargin : ℝ
  nonuniform_le_scalar : nonuniformBudget ≤ capMax
  scalar_strict_margin : capMax < downstreamMargin

theorem strict_margin_bridge_record6
    (B : StrictMarginBridge6) :
    B.nonuniformBudget < B.downstreamMargin := by
  exact lt_of_le_of_lt B.nonuniform_le_scalar B.scalar_strict_margin

end

end RouteBP3CentralFDHullMarginBridge

#print axioms RouteBP3CentralFDHullMarginBridge.strict_margin_transitivity6
#print axioms RouteBP3CentralFDHullMarginBridge.capMax_budget_strictly_below_margin6
#print axioms RouteBP3CentralFDHullMarginBridge.strict_margin_bridge_record6
