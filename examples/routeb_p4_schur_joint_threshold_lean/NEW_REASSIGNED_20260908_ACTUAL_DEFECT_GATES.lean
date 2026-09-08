import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith

set_option autoImplicit false

namespace RouteBP4ReassignedActualDefectGates20260908

/-!
OPEN_UNCOMPILED. Pure Real gates only; the identities are supplied hypotheses.
Intended meanings: u=<ell,d>_H, s=<ell+r0,d>_H, D=||d||_H^2.
This module does not construct a source residual, metric, or enclosure.
No local Lean/Lake run and no admission claim.
-/

theorem actual_binding_iff
    (E beta L c0 u Qactual Pactual : ℝ)
    (hActual : Pactual = beta - L - 2 * (c0 + u) - Qactual) :
    (E - Qactual ≤ Pactual) ↔
      2 * u ≤ beta - L - 2 * c0 - E := by
  constructor <;> intro h <;> linarith

theorem actual_target_iff
    (P0 Pactual t s D : ℝ)
    (hChange : Pactual = P0 - 2 * s - D) :
    (t ≤ Pactual) ↔ 2 * s + D ≤ P0 - t := by
  constructor <;> intro h <;> linarith

/-- Signed projections can be bounded separately without replacing the
actual residual by the nominal residual or charging its square twice. -/
theorem joint_of_signed_defect_caps
    (E beta L c0 u Qactual Pactual P0 t s D U S Dcap : ℝ)
    (hActual : Pactual = beta - L - 2 * (c0 + u) - Qactual)
    (hChange : Pactual = P0 - 2 * s - D)
    (hu : u ≤ U) (hs : s ≤ S) (hD : D ≤ Dcap)
    (hBindingAllocation : 2 * U ≤ beta - L - 2 * c0 - E)
    (hTargetAllocation : 2 * S + Dcap ≤ P0 - t) :
    E - Qactual ≤ Pactual ∧ t ≤ Pactual := by
  constructor
  · apply (actual_binding_iff E beta L c0 u Qactual Pactual hActual).mpr
    linarith
  · apply (actual_target_iff P0 Pactual t s D hChange).mpr
    linarith

/-- If the signed nominal binding gap is zero, an adverse positive
ell-defect projection destroys the binding regardless of the actual cap. -/
theorem positive_projection_breaks_zero_gap
    (E beta L c0 u Qactual Pactual : ℝ)
    (hActual : Pactual = beta - L - 2 * (c0 + u) - Qactual)
    (hZeroGap : beta - L - 2 * c0 - E = 0)
    (hu : 0 < u) :
    Pactual < E - Qactual := by
  linarith

-- Prospective commands only; not executed.
#print axioms actual_binding_iff
#print axioms actual_target_iff
#print axioms joint_of_signed_defect_caps
#print axioms positive_projection_breaks_zero_gap

end RouteBP4ReassignedActualDefectGates20260908

