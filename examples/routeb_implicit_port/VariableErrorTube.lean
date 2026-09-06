import EnergyTube

namespace RouteBVariableErrorTube

/- R is a cumulative error budget, not a pointwise constant bound.
   Its derivative/source identification remains explicit. -/
theorem cumulative_ramp_budget
    {E R ep rp : ℝ → ℝ} {e0 beta c : ℝ}
    (hE0 : E 0 ≤ e0) (hR0 : R 0 = 0) (hbeta : 0 ≤ beta) (hc : c ^ 2 ≤ 3)
    (hEc : ContinuousOn E (Set.Icc 0 1)) (hRc : ContinuousOn R (Set.Icc 0 1))
    (hEd : ∀ t ∈ Set.Ico 0 1, HasDerivWithinAt E (ep t) (Set.Ici t) t)
    (hRd : ∀ t ∈ Set.Ico 0 1, HasDerivWithinAt R (rp t) (Set.Ici t) t)
    (hpower : ∀ t ∈ Set.Ico 0 1, ep t ≤ beta * (c * t) ^ 2 + rp t) :
    ∀ t ∈ Set.Icc 0 1, E t ≤ e0 + beta * t ^ 3 + R t := by
  have hstart : (fun t => E t - R t) 0 ≤ e0 := by simpa [hR0] using hE0
  have hderiv : ∀ t ∈ Set.Ico 0 1,
      HasDerivWithinAt (fun t => E t - R t) (ep t - rp t) (Set.Ici t) t := by
    intro t ht
    exact (hEd t ht).sub (hRd t ht)
  have hbound : ∀ t ∈ Set.Ico 0 1, ep t - rp t ≤ 3 * beta * t ^ 2 + 0 := by
    intro t ht
    have hm := mul_le_mul_of_nonneg_left
      (mul_le_mul_of_nonneg_right hc (sq_nonneg t)) hbeta
    have hp := hpower t ht
    nlinarith
  have htube := RouteBEnergyTube.cubic_tube hstart (hEc.sub hRc) hderiv hbound
  intro t ht
  have h := htube t ht
  simp only [zero_mul, add_zero] at h
  change E t - R t ≤ e0 + beta * t ^ 3 at h
  linarith

theorem capped_cumulative_ramp_budget
    {E R ep rp : ℝ → ℝ} {e0 beta c errorCap : ℝ}
    (hE0 : E 0 ≤ e0) (hR0 : R 0 = 0) (hbeta : 0 ≤ beta) (hc : c ^ 2 ≤ 3)
    (hEc : ContinuousOn E (Set.Icc 0 1)) (hRc : ContinuousOn R (Set.Icc 0 1))
    (hEd : ∀ t ∈ Set.Ico 0 1, HasDerivWithinAt E (ep t) (Set.Ici t) t)
    (hRd : ∀ t ∈ Set.Ico 0 1, HasDerivWithinAt R (rp t) (Set.Ici t) t)
    (hpower : ∀ t ∈ Set.Ico 0 1, ep t ≤ beta * (c * t) ^ 2 + rp t)
    (hRcap : ∀ t ∈ Set.Icc 0 1, R t ≤ errorCap) :
    ∀ t ∈ Set.Icc 0 1, E t ≤ e0 + beta + errorCap := by
  have hbase := cumulative_ramp_budget hE0 hR0 hbeta hc hEc hRc hEd hRd hpower
  intro t ht
  have ht3 : t ^ 3 ≤ 1 := by
    nlinarith [mul_nonneg ht.1 (sub_nonneg.mpr ht.2),
      mul_nonneg (sq_nonneg t) (sub_nonneg.mpr ht.2)]
  have hb := mul_le_mul_of_nonneg_left ht3 hbeta
  have he := hbase t ht
  have hr := hRcap t ht
  linarith

#print axioms cumulative_ramp_budget
#print axioms capped_cumulative_ramp_budget

end RouteBVariableErrorTube
