import Mathlib

set_option autoImplicit false

namespace NEW_BODY6_SLICE_ONESHIFTREPAIR20260908
noncomputable section

/- OPEN_UNCOMPILED. Independent arithmetic consumer for the reviewed chain.
   No pending BODY6 module is imported, and no source identity is reproved. -/
theorem single_shift_step_attempt (s g a beta B bar : ℝ)
    (hCap : s ≤ a + beta) (hValue : g = s + B)
    (hBudget : (a + beta) + B ≤ bar) : g ≤ bar := by
  rw [hValue]
  linarith

/- Commuting the addition changes no budget and introduces no extra B. -/
theorem repaired_budget_equivalent_attempt (cap B bar : ℝ) :
    cap + B ≤ bar ↔ B + cap ≤ bar := by rw [add_comm cap B]

theorem single_shift_path_consumer_attempt {X C : Type*}
    (project : X → C) (D : ℝ → Set X) (Q : Set C) (path : ℝ → X)
    (F G : ℝ → X → ℝ) (a beta B bar : ℝ)
    (hProjection : ∀ t ∈ Set.Icc (0 : ℝ) 1, ∀ x ∈ D t, project x ∈ Q)
    (hPath : ∀ t ∈ Set.Icc (0 : ℝ) 1, path t ∈ D t)
    (hSource : ∀ t ∈ Set.Icc (0 : ℝ) 1, F t (path t) ≤ a + beta)
    (hValue : ∀ t ∈ Set.Icc (0 : ℝ) 1, ∀ x, project x ∈ Q → G t x = F t x + B)
    (hBudget : (a + beta) + B ≤ bar) :
    ∀ t ∈ Set.Icc (0 : ℝ) 1, G t (path t) ≤ bar := by
  intro t ht
  have hq := hProjection t ht (path t) (hPath t ht)
  exact single_shift_step_attempt (F t (path t)) (G t (path t)) a beta B bar
    (hSource t ht) (hValue t ht (path t) hq) hBudget

def exactB : ℝ := 4079979/400000

/- Saturated exact example: a legitimate cap uses B once. Charging it twice
   is an extra restriction that falsely rejects this valid shifted cap. -/
theorem saturated_single_shift_counterexample_attempt :
    ∃ s g cap bar : ℝ,
      g = s + exactB ∧ s ≤ cap ∧ cap + exactB ≤ bar ∧
      g ≤ bar ∧ ¬ g + exactB ≤ bar := by
  refine ⟨0, exactB, 0, exactB, ?_, ?_, ?_, ?_, ?_⟩ <;> norm_num [exactB]

/- This does not validate the repaired module or downstream imports.
   Initial/growth, source-value, domain and path premises remain external. -/
end
end NEW_BODY6_SLICE_ONESHIFTREPAIR20260908
