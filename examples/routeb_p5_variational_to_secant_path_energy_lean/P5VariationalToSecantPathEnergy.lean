import Mathlib

open scoped BigOperators

namespace RouteBP5VariationalToSecantPathEnergy

/-- Explicit symmetric 2x2 quadratic form with cross coefficient `b`. -/
def qform2 (a b c x y : ℝ) : ℝ := a * x^2 + 2 * b * x * y + c * y^2

/--
Pure arithmetic leaf behind the one-step rational decay argument.
The calculus layer only has to provide the integrated derivative inequality
`Vb - Va ≤ -2*mu*I` and the monotonicity-derived lower bound
`(b-a)*Vb ≤ I`.
-/
theorem one_step_rational_decay_from_integral_packet
    (mu a b Va Vb I : ℝ)
    (hmu : 0 ≤ mu)
    (hfund : Vb - Va ≤ -2 * mu * I)
    (hint : (b - a) * Vb ≤ I) :
    (1 + 2 * mu * (b - a)) * Vb ≤ Va := by
  have hcoef : -2 * mu ≤ 0 := by
    nlinarith
  have hscale : (-2 * mu) * I ≤ (-2 * mu) * ((b - a) * Vb) :=
    mul_le_mul_of_nonpos_left hint hcoef
  nlinarith

/-- Relative/signed rate reuse: the trusted arithmetic only sees `mu-rho`. -/
theorem relative_rate_one_step_from_integral_packet
    (mu rho a b Va Vb I : ℝ)
    (hnu : 0 ≤ mu - rho)
    (hfund : Vb - Va ≤ -2 * (mu - rho) * I)
    (hint : (b - a) * Vb ≤ I) :
    (1 + 2 * (mu - rho) * (b - a)) * Vb ≤ Va := by
  exact one_step_rational_decay_from_integral_packet
    (mu - rho) a b Va Vb I hnu hfund hint

/--
Finite path-energy quadrature leaf: a pointwise weighted tangent inequality
sums without any Jensen loss. This is the finite-sum analogue of integrating
`A qOut(s) ≤ B qIn(s)` along a witness path.
-/
theorem finite_sum_path_energy_contraction
    {ι : Type*} [DecidableEq ι]
    (s : Finset ι) (A B : ℝ) (qOut qIn : ι → ℝ)
    (hpoint : ∀ i ∈ s, A * qOut i ≤ B * qIn i) :
    A * s.sum qOut ≤ B * s.sum qIn := by
  calc
    A * s.sum qOut = s.sum (fun i => A * qOut i) := by
      rw [Finset.mul_sum]
    _ ≤ s.sum (fun i => B * qIn i) := by
      exact Finset.sum_le_sum fun i hi => hpoint i hi
    _ = B * s.sum qIn := by
      rw [Finset.mul_sum]

/--
Exact midpoint Jensen leaf for a symmetric quadratic form. Full PSD is stronger
than needed here; it suffices that the form is nonnegative on the difference
of the two sampled tangent vectors.
-/
theorem quadratic_midpoint_jensen_of_psd_direction
    (a b c x1 y1 x2 y2 : ℝ)
    (hpsd : 0 ≤ qform2 a b c (x1 - x2) (y1 - y2)) :
    qform2 a b c ((x1 + x2) / 2) ((y1 + y2) / 2) ≤
      (qform2 a b c x1 y1 + qform2 a b c x2 y2) / 2 := by
  simp only [qform2] at hpsd ⊢
  nlinarith

/--
Minimal two-sample secant/Jensen consumer. It deliberately assumes the two
pointwise tangent bounds instead of pretending to have a full FTC/integral API.
-/
theorem two_sample_secant_packet
    (a b c A B qIn x1 y1 x2 y2 : ℝ)
    (hA : 0 ≤ A)
    (hpsd : 0 ≤ qform2 a b c (x1 - x2) (y1 - y2))
    (h1 : A * qform2 a b c x1 y1 ≤ B * qIn)
    (h2 : A * qform2 a b c x2 y2 ≤ B * qIn) :
    A * qform2 a b c ((x1 + x2) / 2) ((y1 + y2) / 2) ≤ B * qIn := by
  have hjensen := quadratic_midpoint_jensen_of_psd_direction
    a b c x1 y1 x2 y2 hpsd
  have hscaled := mul_le_mul_of_nonneg_left hjensen hA
  nlinarith

/-- Nonlinear normalized chart used by the exact fail-closed counterexample. -/
def normalizedMap (z : ℝ) : ℝ := 2 * z

/-- Pullback of the constant physical metric through `T(z)=1/z`. -/
noncomputable def pullbackMetric (z : ℝ) : ℝ := 1 / z^4

/-- Raw Euclidean chord squared expands by exactly four under `Psi(z)=2z`. -/
theorem raw_normalized_chord_sq_expands (z1 z2 : ℝ) :
    (normalizedMap z1 - normalizedMap z2)^2 = 4 * (z1 - z2)^2 := by
  simp only [normalizedMap]
  ring

/--
Despite raw normalized chord expansion, the pulled-back tangent energy keeps
exactly the physical contraction factor `1/4`.
-/
theorem pullback_tangent_contracts (z v : ℝ) (hz : z ≠ 0) :
    pullbackMetric (normalizedMap z) * (2 * v)^2 =
      (1 / 4 : ℝ) * pullbackMetric z * v^2 := by
  simp only [pullbackMetric, normalizedMap]
  field_simp [hz]
  all_goals ring

/-- Concrete unit-point sanity check for the nonlinear-chart packet. -/
theorem nonlinear_chart_unit_packet :
    (normalizedMap 2 - normalizedMap 1)^2 = 4 ∧
    pullbackMetric (normalizedMap 1) * (2 : ℝ)^2 =
      (1 / 4 : ℝ) * pullbackMetric 1 := by
  constructor
  · norm_num [normalizedMap]
  · norm_num [pullbackMetric, normalizedMap]

#print axioms one_step_rational_decay_from_integral_packet
#print axioms relative_rate_one_step_from_integral_packet
#print axioms finite_sum_path_energy_contraction
#print axioms quadratic_midpoint_jensen_of_psd_direction
#print axioms two_sample_secant_packet
#print axioms raw_normalized_chord_sq_expands
#print axioms pullback_tangent_contracts
#print axioms nonlinear_chart_unit_packet

end RouteBP5VariationalToSecantPathEnergy
