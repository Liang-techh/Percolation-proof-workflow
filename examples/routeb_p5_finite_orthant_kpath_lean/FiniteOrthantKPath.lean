import Mathlib

noncomputable section

namespace RouteBP5FiniteOrthantKPath

/-- Two generalized-force residual channels consumed by the P5 block-(4,5) power term. -/
structure ForceResidual45 where
  ch4 : ℝ
  ch5 : ℝ

/--
A typed 2×4 transported component-gain table.  The field order is deliberately
explicit: residual-force channel first, then the four P5 state coordinates
`(x4,x5,y4,y5)`.
-/
structure Gain24 where
  k4x4 : ℝ
  k4x5 : ℝ
  k4y4 : ℝ
  k4y5 : ℝ
  k5x4 : ℝ
  k5x5 : ℝ
  k5y4 : ℝ
  k5y5 : ℝ

/-- Semantic side condition expected from a source/checker `K_path` artifact. -/
def Gain24.Nonnegative (K : Gain24) : Prop :=
  0 ≤ K.k4x4 ∧ 0 ≤ K.k4x5 ∧ 0 ≤ K.k4y4 ∧ 0 ≤ K.k4y5 ∧
  0 ≤ K.k5x4 ∧ 0 ≤ K.k5x5 ∧ 0 ≤ K.k5y4 ∧ 0 ≤ K.k5y5

/-- Row-4 absolute component envelope. -/
def row4Envelope (K : Gain24) (x4 x5 y4 y5 : ℝ) : ℝ :=
  K.k4x4 * |x4| + K.k4x5 * |x5| + K.k4y4 * |y4| + K.k4y5 * |y5|

/-- Row-5 absolute component envelope. -/
def row5Envelope (K : Gain24) (x4 x5 y4 y5 : ℝ) : ℝ :=
  K.k5x4 * |x4| + K.k5x5 * |x5| + K.k5y4 * |y4| + K.k5y5 * |y5|

/-- Exact centered P5 residual power pairing `L z · r`. -/
def residualPower
    (r : ForceResidual45) (x4 x5 y4 y5 : ℝ) : ℝ :=
  (x4 + y4) * r.ch4 + (x5 + y5) * r.ch5

/-- Direct support-function envelope `|Lz|ᵀ K |z|`. -/
def directSupport
    (K : Gain24) (x4 x5 y4 y5 : ℝ) : ℝ :=
  |x4 + y4| * row4Envelope K x4 x5 y4 y5 +
  |x5 + y5| * row5Envelope K x4 x5 y4 y5

/-- Exact block-(4,5) quadratic `zᵀ P z` from T-P5-024/T-P5-025. -/
def qDissipation (x4 x5 y4 y5 : ℝ) : ℝ :=
  (3 / 4 : ℝ) * x4 ^ 2 +
  (29 / 50 : ℝ) * x5 ^ 2 +
  (2049997 / 3000000 : ℝ) * y4 ^ 2 +
  (2399261 / 4000000 : ℝ) * y5 ^ 2 -
  (3 / 200 : ℝ) * x4 * x5 -
  (1 / 400 : ℝ) * x5 * y4 +
  (1 / 400 : ℝ) * x4 * y5

/--
Componentwise residual bounds imply the direct power envelope without any
Frobenius / Euclidean collapse.
-/
theorem component_envelope_power_bound
    (K : Gain24) (r : ForceResidual45) (x4 x5 y4 y5 : ℝ)
    (h4 : |r.ch4| ≤ row4Envelope K x4 x5 y4 y5)
    (h5 : |r.ch5| ≤ row5Envelope K x4 x5 y4 y5) :
    |residualPower r x4 x5 y4 y5| ≤ directSupport K x4 x5 y4 y5 := by
  calc
    |residualPower r x4 x5 y4 y5| =
        |(x4 + y4) * r.ch4 + (x5 + y5) * r.ch5| := by
          rfl
    _ ≤ |(x4 + y4) * r.ch4| + |(x5 + y5) * r.ch5| := abs_add _ _
    _ = |x4 + y4| * |r.ch4| + |x5 + y5| * |r.ch5| := by
          rw [abs_mul, abs_mul]
    _ ≤ |x4 + y4| * row4Envelope K x4 x5 y4 y5 +
          |x5 + y5| * row5Envelope K x4 x5 y4 y5 := by
          exact add_le_add
            (mul_le_mul_of_nonneg_left h4 (abs_nonneg _))
            (mul_le_mul_of_nonneg_left h5 (abs_nonneg _))
    _ = directSupport K x4 x5 y4 y5 := by
          rfl

/-- Boolean sign selector, used so the checker has a finite 2^6 orthant domain. -/
def boolSign (b : Bool) : ℝ := if b then 1 else -1

/-- Every real scalar admits a Boolean sign selector that realizes its absolute value. -/
theorem exists_boolSign_mul_eq_abs (x : ℝ) :
    ∃ b : Bool, boolSign b * x = |x| := by
  by_cases hx : 0 ≤ x
  · refine ⟨true, ?_⟩
    simp [boolSign, abs_of_nonneg hx]
  · have hx' : x ≤ 0 := le_of_not_ge hx
    refine ⟨false, ?_⟩
    simp [boolSign, abs_of_nonpos hx']

/-- Signed row-4 expression on one state orthant. -/
def signedRow4
    (K : Gain24) (sx4 sx5 sy4 sy5 : Bool)
    (x4 x5 y4 y5 : ℝ) : ℝ :=
  K.k4x4 * (boolSign sx4 * x4) +
  K.k4x5 * (boolSign sx5 * x5) +
  K.k4y4 * (boolSign sy4 * y4) +
  K.k4y5 * (boolSign sy5 * y5)

/-- Signed row-5 expression on one state orthant. -/
def signedRow5
    (K : Gain24) (sx4 sx5 sy4 sy5 : Bool)
    (x4 x5 y4 y5 : ℝ) : ℝ :=
  K.k5x4 * (boolSign sx4 * x4) +
  K.k5x5 * (boolSign sx5 * x5) +
  K.k5y4 * (boolSign sy4 * y4) +
  K.k5y5 * (boolSign sy5 * y5)

/--
Directional support form for one of the finitely many `(sigma,tau)` sign pairs.
This is the scalar quadratic-form interface a rational PSD/SOS checker must bound.
-/
def orthantSupport
    (K : Gain24)
    (sx4 sx5 sy4 sy5 st4 st5 : Bool)
    (x4 x5 y4 y5 : ℝ) : ℝ :=
  (boolSign st4 * (x4 + y4)) * signedRow4 K sx4 sx5 sy4 sy5 x4 x5 y4 y5 +
  (boolSign st5 * (x5 + y5)) * signedRow5 K sx4 sx5 sy4 sy5 x4 x5 y4 y5

/-- Exact transport from sign-selector identities to the direct support function. -/
theorem orthant_support_eq_direct_support_of_signs
    (K : Gain24)
    (sx4 sx5 sy4 sy5 st4 st5 : Bool)
    (x4 x5 y4 y5 : ℝ)
    (hx4 : boolSign sx4 * x4 = |x4|)
    (hx5 : boolSign sx5 * x5 = |x5|)
    (hy4 : boolSign sy4 * y4 = |y4|)
    (hy5 : boolSign sy5 * y5 = |y5|)
    (ht4 : boolSign st4 * (x4 + y4) = |x4 + y4|)
    (ht5 : boolSign st5 * (x5 + y5) = |x5 + y5|) :
    orthantSupport K sx4 sx5 sy4 sy5 st4 st5 x4 x5 y4 y5 =
      directSupport K x4 x5 y4 y5 := by
  simp only [orthantSupport, signedRow4, signedRow5, directSupport,
    row4Envelope, row5Envelope]
  rw [hx4, hx5, hy4, hy5, ht4, ht5]

/-- Every concrete state chooses one of the 64 Boolean sign pairs exactly. -/
theorem exists_orthant_support_eq_direct_support
    (K : Gain24) (x4 x5 y4 y5 : ℝ) :
    ∃ sx4 sx5 sy4 sy5 st4 st5 : Bool,
      orthantSupport K sx4 sx5 sy4 sy5 st4 st5 x4 x5 y4 y5 =
        directSupport K x4 x5 y4 y5 := by
  obtain ⟨sx4, hx4⟩ := exists_boolSign_mul_eq_abs x4
  obtain ⟨sx5, hx5⟩ := exists_boolSign_mul_eq_abs x5
  obtain ⟨sy4, hy4⟩ := exists_boolSign_mul_eq_abs y4
  obtain ⟨sy5, hy5⟩ := exists_boolSign_mul_eq_abs y5
  obtain ⟨st4, ht4⟩ := exists_boolSign_mul_eq_abs (x4 + y4)
  obtain ⟨st5, ht5⟩ := exists_boolSign_mul_eq_abs (x5 + y5)
  refine ⟨sx4, sx5, sy4, sy5, st4, st5, ?_⟩
  exact orthant_support_eq_direct_support_of_signs
    K sx4 sx5 sy4 sy5 st4 st5 x4 x5 y4 y5 hx4 hx5 hy4 hy5 ht4 ht5

/--
Finite-orthant checker contract.  Because all six selectors are `Bool`, this is
exactly a finite family of 64 directional quadratic inequalities; a checker may
quotient the global-sign symmetry and emit only 32 distinct rational witnesses.
-/
def OrthantSmallGainCertificate (K : Gain24) (mu : ℝ) : Prop :=
  ∀ sx4 sx5 sy4 sy5 st4 st5 : Bool,
    ∀ x4 x5 y4 y5 : ℝ,
      orthantSupport K sx4 sx5 sy4 sy5 st4 st5 x4 x5 y4 y5 ≤
        mu * qDissipation x4 x5 y4 y5

/--
Core T-P5-025 theorem: a component envelope plus the finite orthant checker
implies the centered P5 small-gain bound, without forming `ell2_path`.
-/
theorem orthant_quadratic_small_gain
    (K : Gain24) (r : ForceResidual45) (mu x4 x5 y4 y5 : ℝ)
    (h4 : |r.ch4| ≤ row4Envelope K x4 x5 y4 y5)
    (h5 : |r.ch5| ≤ row5Envelope K x4 x5 y4 y5)
    (hcert : OrthantSmallGainCertificate K mu) :
    |residualPower r x4 x5 y4 y5| ≤
      mu * qDissipation x4 x5 y4 y5 := by
  obtain ⟨sx4, sx5, sy4, sy5, st4, st5, hsupp⟩ :=
    exists_orthant_support_eq_direct_support K x4 x5 y4 y5
  calc
    |residualPower r x4 x5 y4 y5| ≤ directSupport K x4 x5 y4 y5 :=
      component_envelope_power_bound K r x4 x5 y4 y5 h4 h5
    _ = orthantSupport K sx4 sx5 sy4 sy5 st4 st5 x4 x5 y4 y5 := hsupp.symm
    _ ≤ mu * qDissipation x4 x5 y4 y5 :=
      hcert sx4 sx5 sy4 sy5 st4 st5 x4 x5 y4 y5

/-- Boolean negation flips the selected real sign. -/
theorem boolSign_not (b : Bool) : boolSign (!b) = -boolSign b := by
  cases b <;> simp [boolSign]

/--
Global reversal `(sigma,tau) ↦ (-sigma,-tau)` leaves the directional support
form unchanged, justifying the 64-to-32 checker reduction.
-/
theorem orthant_support_global_reversal
    (K : Gain24)
    (sx4 sx5 sy4 sy5 st4 st5 : Bool)
    (x4 x5 y4 y5 : ℝ) :
    orthantSupport K (!sx4) (!sx5) (!sy4) (!sy5) (!st4) (!st5)
        x4 x5 y4 y5 =
      orthantSupport K sx4 sx5 sy4 sy5 st4 st5 x4 x5 y4 y5 := by
  simp only [orthantSupport, signedRow4, signedRow5, boolSign_not]
  ring

/-- The finite checker seam does not consume `K` nonnegativity implicitly. -/
theorem nonnegative_gain_is_explicit_interface
    (K : Gain24) (hK : K.Nonnegative) : K.Nonnegative := by
  exact hK

#print axioms component_envelope_power_bound
#print axioms exists_boolSign_mul_eq_abs
#print axioms orthant_support_eq_direct_support_of_signs
#print axioms exists_orthant_support_eq_direct_support
#print axioms orthant_quadratic_small_gain
#print axioms boolSign_not
#print axioms orthant_support_global_reversal
#print axioms nonnegative_gain_is_explicit_interface

end RouteBP5FiniteOrthantKPath

end
