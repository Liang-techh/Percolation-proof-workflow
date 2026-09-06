import VariableErrorTube
import LocalEnergyBudget

namespace RouteBLocalTubeAssembly

open RouteBLocalEnergyBudget

noncomputable def energy (x : ℝ → Fin 12 → ℝ) (t : ℝ) : ℝ :=
  VB (x t 3) (x t 4) (x t 9) (x t 10)

noncomputable def power (x : ℝ → Fin 12 → ℝ) (a4 a5 : ℝ → ℝ) (t : ℝ) : ℝ :=
  derivativeExpr (x t 3) (x t 4) (x t 9) (x t 10) (a4 t) (a5 t)

/- Conditional original-domain AND original-terminal outputs for a full
   12-coordinate curve. Remote coordinates are not fixed or discarded.
   This is not a theorem asserting existence, source semantics, or the budget. -/
theorem conditional_original_block_outputs
    (x : ℝ → Fin 12 → ℝ) (a4 a5 e4 e5 R : ℝ → ℝ) (c : ℝ)
    (hinit : full12Ball (x 0)) (hc : c ^ 2 ≤ 3) (hR0 : R 0 = 0)
    (hEc : ContinuousOn (energy x) (Set.Icc 0 1))
    (hRc : ContinuousOn R (Set.Icc 0 1))
    (hEd : ∀ t ∈ Set.Ico 0 1,
      HasDerivWithinAt (energy x) (power x a4 a5 t) (Set.Ici t) t)
    (hRd : ∀ t ∈ Set.Ico 0 1,
      HasDerivWithinAt R (residualCost (e4 t) (e5 t)) (Set.Ici t) t)
    (h4 : ∀ t ∈ Set.Ico 0 1, m44 * a4 t =
      -(3 / 5) * x t 3 - (4 / 5) * x t 9 + (1 / 5) * (c * t) + e4 t)
    (h5 : ∀ t ∈ Set.Ico 0 1, m55 * a5 t =
      -(1 / 2) * x t 4 - (13 / 20) * x t 10 + (1 / 10) * (c * t) + e5 t)
    (hRcap : ∀ t ∈ Set.Icc 0 1, R t ≤ (1 / 10 : ℝ)) :
    (∀ t ∈ Set.Icc 0 1, p (x t 3) (x t 4) (x t 9) (x t 10) < (28 / 5 : ℝ)) ∧
      qterminal (x 1 3) (x 1 4) (x 1 9) (x 1 10) < 12 := by
  have h0 : energy x 0 ≤ (27 / 4000 : ℝ) := full12Ball_initial_VB (x 0) hinit
  have hbound : ∀ t ∈ Set.Ico 0 1,
      power x a4 a5 t ≤ (17 / 520 : ℝ) * (c * t) ^ 2 + residualCost (e4 t) (e5 t) := by
    intro t ht
    have hd := derivative_budget (x t 3) (x t 4) (x t 9) (x t 10)
      (a4 t) (a5 t) (c * t) (e4 t) (e5 t) (power x a4 a5 t)
      rfl (h4 t ht) (h5 t ht)
    dsimp [residualCost]
    linarith
  have hcap := RouteBVariableErrorTube.capped_cumulative_ramp_budget
    h0 hR0 (by norm_num : (0 : ℝ) ≤ 17 / 520) hc hEc hRc hEd hRd hbound hRcap
  have hout (t : ℝ) (ht : t ∈ Set.Icc 0 1) :
      p (x t 3) (x t 4) (x t 9) (x t 10) < (28 / 5 : ℝ) ∧
      qterminal (x t 3) (x t 4) (x t 9) (x t 10) < 12 := by
    apply outputs_of_cap
    exact hcap t ht
  exact ⟨fun t ht => (hout t ht).1, (hout 1 (by constructor <;> norm_num)).2⟩

#print axioms conditional_original_block_outputs

end RouteBLocalTubeAssembly
