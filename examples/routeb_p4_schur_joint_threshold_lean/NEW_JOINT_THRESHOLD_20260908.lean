import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith

set_option autoImplicit false

namespace RouteBP4SchurJointThreshold

/-!
OPEN_UNCOMPILED: source-independent scalar candidates only.
No Lean/Lake run, elaboration, kernel check or axiom report was performed.
P = beta - L - 2*c - Q is an explicit hypothesis, not a source witness.
All scalars may have either sign; no PSD or coverage claim is implicit.
-/

variable (L Q c E_A t beta P : ℝ)

theorem binding_iff
    (hP : P = beta - L - 2 * c - Q) :
    E_A - Q ≤ P ↔ L + 2 * c + E_A ≤ beta := by
  constructor <;> intro h <;> linarith

theorem target_iff
    (hP : P = beta - L - 2 * c - Q) :
    t ≤ P ↔ L + 2 * c + (t + Q) ≤ beta := by
  constructor <;> intro h <;> linarith

/-- Keep the two obligations separate before introducing max. -/
theorem joint_iff_two_thresholds
    (hP : P = beta - L - 2 * c - Q) :
    (E_A - Q ≤ P ∧ t ≤ P) ↔
      (L + 2 * c + E_A ≤ beta ∧ L + 2 * c + (t + Q) ≤ beta) := by
  constructor
  · intro h
    exact ⟨(binding_iff L Q c E_A beta P hP).mp h.1,
      (target_iff L Q c t beta P hP).mp h.2⟩
  · intro h
    exact ⟨(binding_iff L Q c E_A beta P hP).mpr h.1,
      (target_iff L Q c t beta P hP).mpr h.2⟩

theorem joint_implies_max_threshold
    (hP : P = beta - L - 2 * c - Q)
    (hBinding : E_A - Q ≤ P) (hTarget : t ≤ P) :
    L + 2 * c + max E_A (t + Q) ≤ beta := by
  have hEA : E_A ≤ beta - L - 2 * c := by linarith
  have htQ : t + Q ≤ beta - L - 2 * c := by linarith
  have hm : max E_A (t + Q) ≤ beta - L - 2 * c :=
    max_le hEA htQ
  linarith

theorem max_threshold_implies_joint
    (hP : P = beta - L - 2 * c - Q)
    (hMax : L + 2 * c + max E_A (t + Q) ≤ beta) :
    E_A - Q ≤ P ∧ t ≤ P := by
  have hEA : E_A ≤ max E_A (t + Q) := le_max_left _ _
  have htQ : t + Q ≤ max E_A (t + Q) := le_max_right _ _
  constructor <;> linarith

theorem joint_iff_max_threshold
    (hP : P = beta - L - 2 * c - Q) :
    (E_A - Q ≤ P ∧ t ≤ P) ↔
      L + 2 * c + max E_A (t + Q) ≤ beta := by
  constructor
  · intro h
    exact joint_implies_max_threshold L Q c E_A t beta P hP h.1 h.2
  · intro h
    exact max_threshold_implies_joint L Q c E_A t beta P hP h

/-- Optional square-valued specialization; the signed cross term remains signed.
No identification with any particular Schur/Gram source is asserted. -/
theorem square_joint_iff (ell q e z c beta P : ℝ)
    (hP : P = beta - ell ^ 2 - 2 * c - q ^ 2) :
    (e ^ 2 - q ^ 2 ≤ P ∧ z ^ 2 ≤ P) ↔
      ell ^ 2 + 2 * c + max (e ^ 2) (z ^ 2 + q ^ 2) ≤ beta := by
  exact joint_iff_max_threshold (ell ^ 2) (q ^ 2) c (e ^ 2) (z ^ 2) beta P hP

end RouteBP4SchurJointThreshold
