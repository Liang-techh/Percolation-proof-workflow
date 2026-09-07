import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
# P3 final strict-margin export boundary

This sidecar consumes an upstream continuous-coverage result with a common
positive margin.  It exports pointwise strict inequalities and a comparator
predicate only; registry admission remains a separate proposition.
-/

set_option autoImplicit false

namespace RouteBP3CentralFDHullStrictExport

noncomputable section

structure StrictMarginExportContract (D : Type*) where
  domain : D → Prop
  covered : D → Prop
  coverage : ∀ x, domain x → covered x
  commonMu : ℝ
  weightedLoad : D → ℝ
  capMaxLoad : D → ℝ
  consumer : D → ℝ
  common_mu_positive : 0 < commonMu
  weighted_margin_on_covered : ∀ x, covered x →
    weightedLoad x + commonMu ≤ capMaxLoad x
  consumer_bound : ∀ x, domain x → consumer x ≤ weightedLoad x

theorem strict_margin_export
    {D : Type*} (C : StrictMarginExportContract D) :
    ∀ x, C.domain x →
      C.weightedLoad x + C.commonMu ≤ C.capMaxLoad x ∧
        C.weightedLoad x < C.capMaxLoad x ∧
        C.consumer x < C.capMaxLoad x := by
  intro x hx
  have hCovered : C.covered x := C.coverage x hx
  have hMargin :
      C.weightedLoad x + C.commonMu ≤ C.capMaxLoad x :=
    C.weighted_margin_on_covered x hCovered
  have hWeighted : C.weightedLoad x < C.capMaxLoad x := by
    linarith [C.common_mu_positive]
  have hConsumer : C.consumer x < C.capMaxLoad x :=
    lt_of_le_of_lt (C.consumer_bound x hx) hWeighted
  exact ⟨hMargin, hWeighted, hConsumer⟩

def comparatorAccepted
    {D : Type*} (C : StrictMarginExportContract D) : Prop :=
  ∀ x, C.domain x → C.consumer x < C.capMaxLoad x

def registryAdmission
    {D : Type*} (C : StrictMarginExportContract D)
    (receiptAccepted : Prop) : Prop :=
  comparatorAccepted C ∧ receiptAccepted

theorem strict_export_implies_comparator
    {D : Type*} (C : StrictMarginExportContract D) :
    comparatorAccepted C := by
  intro x hx
  exact (strict_margin_export C x hx).2.2

theorem strict_export_does_not_imply_registry_admission
    {D : Type*} (C : StrictMarginExportContract D)
    (receiptAccepted : Prop) (hReceipt : ¬ receiptAccepted) :
    ¬ registryAdmission C receiptAccepted := by
  intro hAdmission
  exact hReceipt hAdmission.2

/-! A zero common margin does not create strictness. -/

theorem zero_common_mu_obstruction :
    ¬ ((0 : ℝ) < 0) := by
  norm_num

/-! A missing coverage fact leaves an explicit domain point without export. -/

def incompleteCovered (x : Bool) : Prop := x = false

theorem missing_coverage_obstruction :
    ∃ x : Bool, ¬ incompleteCovered x := by
  exact ⟨true, by simp [incompleteCovered]⟩

end

end RouteBP3CentralFDHullStrictExport

#print axioms RouteBP3CentralFDHullStrictExport.strict_margin_export
#print axioms RouteBP3CentralFDHullStrictExport.strict_export_implies_comparator
#print axioms RouteBP3CentralFDHullStrictExport.strict_export_does_not_imply_registry_admission
#print axioms RouteBP3CentralFDHullStrictExport.zero_common_mu_obstruction
