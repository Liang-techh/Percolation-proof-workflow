import ResidualMultiplier
import PrefixSmallGain

set_option autoImplicit false
open scoped BigOperators Interval
open MeasureTheory

namespace RouteBSignedGap
noncomputable section

/-- FTC gives a real interval-integral work identity. S remains signed. -/
theorem integrated_signed_work (S work etaPower : ℝ → ℝ) (a b : ℝ)
    (hS : ∀ t ∈ Set.uIcc a b, HasDerivAt S (work t - etaPower t) t)
    (hw : IntervalIntegrable work volume a b)
    (he : IntervalIntegrable etaPower volume a b) :
    (∫ t in a..b, work t) = S b - S a + ∫ t in a..b, etaPower t := by
  have hf := intervalIntegral.integral_eq_sub_of_hasDerivAt hS (hw.sub he)
  rw [intervalIntegral.integral_sub hw he] at hf
  linarith

theorem hasDerivAt_weighted_gap (S k : ℝ → ℝ) (Sd kd t : ℝ)
    (hS : HasDerivAt S Sd t) (hk : HasDerivAt k kd t) :
    HasDerivAt (fun s => k s * S s) (kd * S t + k t * Sd) t :=
  hk.mul hS

/-- The differentiated quadratic part is also a real finite-sum derivative. -/
theorem hasDerivAt_signed_storage {n : ℕ} (P : ℝ → Mat n) (Y : ℝ → Vec n)
    (Pd : Mat n) (Yd : Vec n) (S k : ℝ → ℝ) (Sd kd t : ℝ)
    (hP : ∀ i j, HasDerivAt (fun s => P s i j) (Pd i j) t)
    (hY : ∀ i, HasDerivAt (fun s => Y s i) (Yd i) t)
    (hPs : Symmetric (P t)) (hS : HasDerivAt S Sd t) (hk : HasDerivAt k kd t) :
    HasDerivAt (fun s => quad (P s) (Y s) + k s * S s)
      (quad Pd (Y t) + 2 * dot (Y t) (mv (P t) Yd) + kd * S t + k t * Sd) t := by
  have h := (hasDerivAt_bilinear P Y Y Pd Yd Yd t hP hY hY).add (hk.mul hS)
  rw [dot_mv_symm (P t) Yd (Y t) hPs] at h
  convert h using 1 <;> try rfl
  dsimp [quad]
  ring

/-- Integration consumes the proved differential inequality, not an assumed
integrated energy equality. Endpoint storage is permitted to be negative. -/
theorem integrated_dissipation (ell V Vd supply : ℝ → ℝ) (a b : ℝ)
    (hab : a ≤ b) (hcont : ContinuousOn V (Set.Icc a b))
    (hderiv : ∀ t ∈ Set.Ioo a b, HasDerivAt V (Vd t) t)
    (hell : IntervalIntegrable ell volume a b)
    (hvd : IntervalIntegrable Vd volume a b)
    (hsupply : IntervalIntegrable supply volume a b)
    (hpoint : ∀ t ∈ Set.Icc a b, ell t + Vd t ≤ supply t) :
    (∫ t in a..b, ell t) + V b - V a ≤ ∫ t in a..b, supply t := by
  have hi := intervalIntegral.integral_mono_on hab (hell.add hvd) hsupply hpoint
  rw [intervalIntegral.integral_add hell hvd,
    intervalIntegral.integral_eq_sub_of_hasDerivAt_of_le hab hcont hderiv hvd] at hi
  linarith

/-- Uniform-prefix data: every possible stopping endpoint needs its own lower
storage bound and supply cap. No positivity of V or S is requested. -/
structure PrefixCertificate (ell V Vd supply : ℝ → ℝ) (t lower : ℝ) : Prop where
  continuous : ContinuousOn V (Set.Icc 0 t)
  derivative : ∀ s ∈ Set.Ioo 0 t, HasDerivAt V (Vd s) s
  cost_integrable : IntervalIntegrable ell volume 0 t
  derivative_integrable : IntervalIntegrable Vd volume 0 t
  supply_integrable : IntervalIntegrable supply volume 0 t
  dissipation : ∀ s ∈ Set.Icc 0 t, ell s + Vd s ≤ supply s
  endpoint_lower : lower ≤ V t

theorem prefix_budget (ell V Vd supply : ℝ → ℝ) (t lower initial cap : ℝ)
    (ht : 0 ≤ t) (hinitial : V 0 ≤ initial)
    (hcert : PrefixCertificate ell V Vd supply t lower)
    (hcap : initial - lower + (∫ s in 0..t, supply s) ≤ cap) :
    (∫ s in 0..t, ell s) ≤ cap := by
  have hi := integrated_dissipation ell V Vd supply 0 t ht hcert.continuous
    hcert.derivative hcert.cost_integrable hcert.derivative_integrable
    hcert.supply_integrable hcert.dissipation
  have hl := hcert.endpoint_lower
  linarith

/-- Noncircular all-prefix bootstrap, reusing the cached compact first-hit proof.
This proves a budget on the supplied interval, not existence/continuation of an ODE. -/
theorem signed_budget_prefix_bootstrap (ell V Vd supply lower : ℝ → ℝ)
    (T initial margin cap : ℝ) (hT : 0 ≤ T) (hcap : 0 < cap)
    (hJ : ContinuousOn (fun t => ∫ s in 0..t, ell s) (Set.Icc 0 T))
    (hinitial : V 0 ≤ initial) (hmargin : margin < cap)
    (hprefix : ∀ t ∈ Set.Icc 0 T,
      (∀ u ∈ Set.Icc 0 t, (∫ s in 0..u, ell s) < cap) →
      PrefixCertificate ell V Vd supply t (lower t) ∧
        initial - lower t + (∫ s in 0..t, supply s) ≤ margin) :
    ∀ t ∈ Set.Icc 0 T, (∫ s in 0..t, ell s) < cap := by
  apply RouteBPrefixSmallGain.continuousOn_strict_prefix_bootstrap hT hJ
    (by simpa using hcap) hmargin
  intro t ht hsafe
  obtain ⟨hc, hb⟩ := hprefix t ht hsafe
  exact prefix_budget ell V Vd supply t (lower t) initial margin ht.1 hinitial hc hb

#print axioms integrated_signed_work
#print axioms hasDerivAt_weighted_gap
#print axioms hasDerivAt_signed_storage
#print axioms integrated_dissipation
#print axioms prefix_budget
#print axioms signed_budget_prefix_bootstrap

end
end RouteBSignedGap
