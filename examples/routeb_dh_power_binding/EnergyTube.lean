import DHPowerBinding

namespace RouteBEnergyTube

/- Differential-to-integrated bridge for the source's ramp convention w=c*t.
   No existence, domain containment, or energy positivity is assumed implicitly. -/
theorem cubic_tube
    {E : ℝ → ℝ} {e0 beta defect : ℝ} {eprime : ℝ → ℝ}
    (he0 : E 0 ≤ e0)
    (hcont : ContinuousOn E (Set.Icc 0 1))
    (hderiv : ∀ t ∈ Set.Ico 0 1,
      HasDerivWithinAt E (eprime t) (Set.Ici t) t)
    (hbound : ∀ t ∈ Set.Ico 0 1, eprime t ≤ 3 * beta * t ^ 2 + defect) :
    ∀ t ∈ Set.Icc 0 1, E t ≤ e0 + beta * t ^ 3 + defect * t := by
  let B : ℝ → ℝ := fun t => e0 + beta * t ^ 3 + defect * t
  have hB : ∀ t, HasDerivAt B (3 * beta * t ^ 2 + defect) t := by
    intro t
    have hh := ((((hasDerivAt_id t).pow 3).const_mul beta).const_add e0).add
      ((hasDerivAt_id t).const_mul defect)
    convert hh using 1 <;> first
      | rfl
      | (simp [id]; ring)
  have hBcont : ContinuousOn B (Set.Icc 0 1) := by
    dsimp [B]
    fun_prop
  have hres := image_le_of_deriv_right_le_deriv_boundary
    (a := (0 : ℝ)) (b := 1) hcont hderiv (by simpa [B] using he0)
    hBcont (fun t _ => (hB t).hasDerivWithinAt) hbound
  intro t ht
  exact hres ht

theorem ramp_force_error_tube
    {E : ℝ → ℝ} {e0 defect c : ℝ} {eprime : ℝ → ℝ}
    (he0 : E 0 ≤ e0) (hc : c ^ 2 ≤ 3)
    (hcont : ContinuousOn E (Set.Icc 0 1))
    (hderiv : ∀ t ∈ Set.Ico 0 1,
      HasDerivWithinAt E (eprime t) (Set.Ici t) t)
    (hbound : ∀ t ∈ Set.Ico 0 1,
      eprime t ≤ (631227 / 1086800 : ℝ) * (c * t) ^ 2 + defect) :
    ∀ t ∈ Set.Icc 0 1,
      E t ≤ e0 + (631227 / 1086800 : ℝ) * t ^ 3 + defect * t := by
  apply cubic_tube he0 hcont hderiv
  intro t ht
  have hm := mul_le_mul_of_nonneg_right hc (sq_nonneg t)
  have hb := hbound t ht
  nlinarith

theorem ramp_terminal_budget
    {E : ℝ → ℝ} {e0 defect c : ℝ} {eprime : ℝ → ℝ}
    (he0 : E 0 ≤ e0) (hc : c ^ 2 ≤ 3)
    (hcont : ContinuousOn E (Set.Icc 0 1))
    (hderiv : ∀ t ∈ Set.Ico 0 1,
      HasDerivWithinAt E (eprime t) (Set.Ici t) t)
    (hbound : ∀ t ∈ Set.Ico 0 1,
      eprime t ≤ (631227 / 1086800 : ℝ) * (c * t) ^ 2 + defect) :
    E 1 ≤ e0 + (631227 / 1086800 : ℝ) + defect := by
  have h := ramp_force_error_tube he0 hc hcont hderiv hbound 1 (by constructor <;> norm_num)
  simpa using h

#print axioms cubic_tube
#print axioms ramp_force_error_tube
#print axioms ramp_terminal_budget

end RouteBEnergyTube
