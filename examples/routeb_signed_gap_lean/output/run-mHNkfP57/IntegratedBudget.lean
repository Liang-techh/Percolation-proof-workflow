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

theorem integrated_weighted_work (S k kd work etaPower : ℝ → ℝ) (a b : ℝ)
    (hS : ∀ t ∈ Set.uIcc a b, HasDerivAt S (work t - etaPower t) t)
    (hk : ∀ t ∈ Set.uIcc a b, HasDerivAt k (kd t) t)
    (hd : IntervalIntegrable (fun t => kd t * S t) volume a b)
    (hw : IntervalIntegrable (fun t => k t * work t) volume a b)
    (he : IntervalIntegrable (fun t => k t * etaPower t) volume a b) :
    (∫ t in a..b, k t * work t) = k b * S b - k a * S a -
      (∫ t in a..b, kd t * S t) + ∫ t in a..b, k t * etaPower t := by
  have hprod : ∀ t ∈ Set.uIcc a b, HasDerivAt (fun s => k s * S s)
      (kd t * S t + k t * work t - k t * etaPower t) t := by
    intro t ht
    convert (hk t ht).mul (hS t ht) using 1 <;> try rfl
    ring
  have hf := intervalIntegral.integral_eq_sub_of_hasDerivAt hprod ((hd.add hw).sub he)
  rw [intervalIntegral.integral_sub (hd.add hw) he,
    intervalIntegral.integral_add hd hw] at hf
  linarith

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

def inject {m n : ℕ} (B : Fin m → Fin n → ℝ) (x : Vec n) : Vec m :=
  fun i => ∑ j, B i j * x j
def pull {m n : ℕ} (B : Fin m → Fin n → ℝ) (x : Vec m) : Vec n :=
  fun j => ∑ i, B i j * x i

theorem injection_work {m n : ℕ} (B : Fin m → Fin n → ℝ) (x : Vec m) (y : Vec n) :
    dot x (inject B y) = dot (pull B x) y := by
  simp only [dot, inject, pull, Finset.mul_sum, Finset.sum_mul]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro i _
  apply Finset.sum_congr rfl
  intro j _
  ring

def storageD {m n : ℕ} (P Pd : Mat m) (Y F : Vec m) (vel eta : Vec n)
    (S k kd : ℝ) : ℝ := quad Pd Y + 2 * dot Y (mv P F) + kd * S - k * dot vel eta
def storageG {m n : ℕ} (P : Mat m) (M0 : Mat n) (B : Fin m → Fin n → ℝ)
    (Y : Vec m) (vel : Vec n) (k : ℝ) : Vec n :=
  fun j => pull B (mv P Y) j + (k/2) * mv M0 vel j

/-- The S5 coefficient split for any augmentation, in particular m=14,n=6.
F=A14*Y and B=Bdelta are supplied as actual drift/injection data. -/
theorem hasDerivAt_augmented_storage {m n : ℕ} (P : ℝ → Mat m) (Pd : Mat m)
    (M0 : Mat n) (B : Fin m → Fin n → ℝ) (Y : ℝ → Vec m)
    (F : Vec m) (vel eta delta : Vec n) (S k : ℝ → ℝ) (kd t : ℝ)
    (hP : ∀ i j, HasDerivAt (fun s => P s i j) (Pd i j) t)
    (hY : ∀ i, HasDerivAt (fun s => Y s i) (F i + inject B delta i) t)
    (hPs : Symmetric (P t)) (hM0 : Symmetric M0)
    (hS : HasDerivAt S (dot vel (mv M0 delta) - dot vel eta) t)
    (hk : HasDerivAt k kd t) :
    HasDerivAt (fun s => quad (P s) (Y s) + k s * S s)
      (storageD (P t) Pd (Y t) F vel eta (S t) (k t) kd +
        2 * dot (storageG (P t) M0 B (Y t) vel (k t)) delta) t := by
  have h := hasDerivAt_signed_storage P Y Pd (fun i => F i + inject B delta i)
    S k (dot vel (mv M0 delta) - dot vel eta) kd t hP hY hPs hS hk
  have hsplit : dot (Y t) (mv (P t) (fun i => F i + inject B delta i)) =
      dot (Y t) (mv (P t) F) + dot (pull B (mv (P t) (Y t))) delta := by
    have he : dot (Y t) (mv (P t) (fun i => F i + inject B delta i)) =
        dot (Y t) (mv (P t) F) + dot (Y t) (mv (P t) (inject B delta)) := by
      simp only [dot, mv, mul_add, Finset.sum_add_distrib]
    rw [he, dot_mv_symm (P t) (Y t) (inject B delta) hPs,
      dot_comm (inject B delta) (mv (P t) (Y t)), injection_work]
  have hg : dot (storageG (P t) M0 B (Y t) vel (k t)) delta =
      dot (pull B (mv (P t) (Y t))) delta + (k t / 2) * dot vel (mv M0 delta) := by
    have he : dot (storageG (P t) M0 B (Y t) vel (k t)) delta =
        dot (pull B (mv (P t) (Y t))) delta + (k t / 2) * dot (mv M0 vel) delta := by
      simp only [storageG, dot, add_mul, mul_assoc, Finset.sum_add_distrib, Finset.mul_sum]
    rw [he, dot_comm (mv M0 vel) delta, dot_mv_symm M0 delta vel hM0]
  rw [hsplit] at h
  convert h using 1 <;> try rfl
  rw [hg]
  dsimp [storageD]
  ring

/-- Concrete composition of differentiated S5 storage and the affine matrix gate. -/
theorem augmented_affine_dissipation {m n : ℕ} (P : ℝ → Mat m) (Pd : Mat m)
    (M0 M L Z : Mat n) (B : Fin m → Fin n → ℝ) (Y : ℝ → Vec m)
    (F : Vec m) (vel eta delta r z : Vec n) (S k : ℝ → ℝ) (kd t b : ℝ)
    (hP : ∀ i j, HasDerivAt (fun s => P s i j) (Pd i j) t)
    (hY : ∀ i, HasDerivAt (fun s => Y s i) (F i + inject B delta i) t)
    (hPs : Symmetric (P t)) (hM0 : Symmetric M0) (hM : Symmetric M)
    (hS : HasDerivAt S (dot vel (mv M0 delta) - dot vel eta) t)
    (hk : HasDerivAt k kd t) (balance : ∀ i, mv M delta i = r i)
    (hQ : QuadNonnegative (affineMatrix M L Z
      (storageG (P t) M0 B (Y t) vel (k t)) r z b
      (storageD (P t) Pd (Y t) F vel eta (S t) (k t) kd))) :
    quad L delta + deriv (fun s => quad (P s) (Y s) + k s * S s) t ≤ b :=
  affine_deriv_dissipation M L Z _ r z delta b _ t _ hM balance
    (hasDerivAt_augmented_storage P Pd M0 B Y F vel eta delta S k kd t
      hP hY hPs hM0 hS hk) hQ

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
#print axioms integrated_weighted_work
#print axioms hasDerivAt_signed_storage
#print axioms injection_work
#print axioms hasDerivAt_augmented_storage
#print axioms augmented_affine_dissipation
#print axioms integrated_dissipation
#print axioms prefix_budget
#print axioms signed_budget_prefix_bootstrap

end
end RouteBSignedGap
