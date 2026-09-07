import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
# Route-B P5 moving-frame source transport sidecar

This file formalizes the source-independent algebra from
`review-T-P5-028-liuguanyi-20260907T1112.md`.

It proves the exact moving-frame actual-minus-nominal identities, exact
common-ramp-parameter cancellation, preservation of the ramp fiber under
straight interpolation at fixed `(t,c)`, finite-time component transport under
a controlled parameter mismatch, the corresponding rank-one correction to a
one-row anisotropic `K` envelope, and the obstruction showing that a finite
four-state centered gain forces constancy along parameter fibers.

The file deliberately does not certify a concrete Julia/Float64 Jacobian
envelope, source hash, cell chain, ODE/flowpipe coverage, P5/P8/M4 closure, or
registry admission.
-/

set_option autoImplicit false

namespace RouteBP5MovingFrameTransport

noncomputable section

/-- Position source coordinate induced by one moving-frame coordinate. -/
def sourceQ (h r t x c : ℝ) : ℝ := x + (h * t + r) * c

/-- Velocity source coordinate induced by one moving-frame coordinate. -/
def sourceV (h y c : ℝ) : ℝ := y + h * c

/-- Ramp source coordinate. -/
def sourceW (t c : ℝ) : ℝ := t * c

/-- Affine interpolation.  No interval hypothesis on `s` is needed for the
algebraic identity used by the path adapter. -/
def lerp (s a b : ℝ) : ℝ := (1 - s) * a + s * b

/-- Exact five-coordinate actual-minus-nominal moving-frame difference. -/
theorem movingFrameSourceDifference_exact
    (h4 h5 r4 r5 t x4 x4bar x5 x5bar y4 y4bar y5 y5bar c cbar : ℝ) :
    sourceQ h4 r4 t x4 c - sourceQ h4 r4 t x4bar cbar =
        (x4 - x4bar) + (h4 * t + r4) * (c - cbar) ∧
    sourceQ h5 r5 t x5 c - sourceQ h5 r5 t x5bar cbar =
        (x5 - x5bar) + (h5 * t + r5) * (c - cbar) ∧
    sourceV h4 y4 c - sourceV h4 y4bar cbar =
        (y4 - y4bar) + h4 * (c - cbar) ∧
    sourceV h5 y5 c - sourceV h5 y5bar cbar =
        (y5 - y5bar) + h5 * (c - cbar) ∧
    sourceW t c - sourceW t cbar = t * (c - cbar) := by
  constructor
  · simp [sourceQ]
    ring
  constructor
  · simp [sourceQ]
    ring
  constructor
  · simp [sourceV]
    ring
  constructor
  · simp [sourceV]
    ring
  · simp [sourceW]
    ring

/-- At common ramp parameter, all affine `c`-dependent centers cancel exactly;
`w` and the explicit parameter displacement are both zero. -/
theorem movingFrameCommonParameter_cancel
    (h4 h5 r4 r5 t x4 x4bar x5 x5bar y4 y4bar y5 y5bar c cbar : ℝ)
    (hc : c = cbar) :
    sourceQ h4 r4 t x4 c - sourceQ h4 r4 t x4bar cbar = x4 - x4bar ∧
    sourceQ h5 r5 t x5 c - sourceQ h5 r5 t x5bar cbar = x5 - x5bar ∧
    sourceV h4 y4 c - sourceV h4 y4bar cbar = y4 - y4bar ∧
    sourceV h5 y5 c - sourceV h5 y5bar cbar = y5 - y5bar ∧
    sourceW t c - sourceW t cbar = 0 ∧ c - cbar = 0 := by
  subst cbar
  constructor
  · simp [sourceQ]
  constructor
  · simp [sourceQ]
  constructor
  · simp [sourceV]
  constructor
  · simp [sourceV]
  constructor <;> simp [sourceW]

/-- The straight source segment induced by interpolating the four moving
coordinates at fixed `(t,c)` stays exactly on the same ramp fiber. -/
theorem movingFrameSegment_preservesRampFiber
    (h4 h5 r4 r5 t c s x40 x41 x50 x51 y40 y41 y50 y51 : ℝ) :
    sourceQ h4 r4 t (lerp s x40 x41) c =
        lerp s (sourceQ h4 r4 t x40 c) (sourceQ h4 r4 t x41 c) ∧
    sourceQ h5 r5 t (lerp s x50 x51) c =
        lerp s (sourceQ h5 r5 t x50 c) (sourceQ h5 r5 t x51 c) ∧
    sourceV h4 (lerp s y40 y41) c =
        lerp s (sourceV h4 y40 c) (sourceV h4 y41 c) ∧
    sourceV h5 (lerp s y50 y51) c =
        lerp s (sourceV h5 y50 c) (sourceV h5 y51 c) ∧
    sourceW t c = t * c := by
  constructor
  · simp [sourceQ, lerp]
    ring
  constructor
  · simp [sourceQ, lerp]
    ring
  constructor
  · simp [sourceV, lerp]
    ring
  constructor
  · simp [sourceV, lerp]
    ring
  · rfl

/-- Four-state weighted budget used to control a possible ramp-parameter
mismatch. -/
def gammaBudget
    (gamma1 gamma2 gamma3 gamma4 dx4 dx5 dy4 dy5 : ℝ) : ℝ :=
  gamma1 * |dx4| + gamma2 * |dx5| + gamma3 * |dy4| + gamma4 * |dy5|

/-- Nonnegative `gamma` entries make the parameter-control budget nonnegative. -/
theorem gammaBudget_nonneg
    (gamma1 gamma2 gamma3 gamma4 dx4 dx5 dy4 dy5 : ℝ)
    (hg1 : 0 ≤ gamma1) (hg2 : 0 ≤ gamma2)
    (hg3 : 0 ≤ gamma3) (hg4 : 0 ≤ gamma4) :
    0 ≤ gammaBudget gamma1 gamma2 gamma3 gamma4 dx4 dx5 dy4 dy5 := by
  simp only [gammaBudget]
  positivity

/-- Uniform five-coordinate transport on `0 ≤ t ≤ T`.  The endpoint envelope
bounds are hypotheses so a source checker may supply either exact-time or
interval-uniform rational constants. -/
theorem movingFrameUniformTransport_of_parameterControl
    (h4 h5 r4 r5 t T A4 A5 gamma1 gamma2 gamma3 gamma4
      dx4 dx5 dy4 dy5 dc : ℝ)
    (ht0 : 0 ≤ t) (htT : t ≤ T)
    (hT : 0 ≤ T) (hA4 : 0 ≤ A4) (hA5 : 0 ≤ A5)
    (hcoef4 : |h4 * t + r4| ≤ A4)
    (hcoef5 : |h5 * t + r5| ≤ A5)
    (hdc : |dc| ≤ gammaBudget gamma1 gamma2 gamma3 gamma4 dx4 dx5 dy4 dy5) :
    |dx4 + (h4 * t + r4) * dc| ≤
        |dx4| + A4 * gammaBudget gamma1 gamma2 gamma3 gamma4 dx4 dx5 dy4 dy5 ∧
    |dx5 + (h5 * t + r5) * dc| ≤
        |dx5| + A5 * gammaBudget gamma1 gamma2 gamma3 gamma4 dx4 dx5 dy4 dy5 ∧
    |dy4 + h4 * dc| ≤
        |dy4| + |h4| * gammaBudget gamma1 gamma2 gamma3 gamma4 dx4 dx5 dy4 dy5 ∧
    |dy5 + h5 * dc| ≤
        |dy5| + |h5| * gammaBudget gamma1 gamma2 gamma3 gamma4 dx4 dx5 dy4 dy5 ∧
    |t * dc| ≤ T * gammaBudget gamma1 gamma2 gamma3 gamma4 dx4 dx5 dy4 dy5 := by
  let G := gammaBudget gamma1 gamma2 gamma3 gamma4 dx4 dx5 dy4 dy5
  have hG : 0 ≤ G := le_trans (abs_nonneg dc) hdc
  have hq4 : |dx4 + (h4 * t + r4) * dc| ≤ |dx4| + A4 * G := by
    calc
      |dx4 + (h4 * t + r4) * dc| ≤ |dx4| + |(h4 * t + r4) * dc| := abs_add _ _
      _ = |dx4| + |h4 * t + r4| * |dc| := by rw [abs_mul]
      _ ≤ |dx4| + A4 * |dc| := by
        exact add_le_add_left (mul_le_mul_of_nonneg_right hcoef4 (abs_nonneg dc)) _
      _ ≤ |dx4| + A4 * G := by
        exact add_le_add_left (mul_le_mul_of_nonneg_left hdc hA4) _
  have hq5 : |dx5 + (h5 * t + r5) * dc| ≤ |dx5| + A5 * G := by
    calc
      |dx5 + (h5 * t + r5) * dc| ≤ |dx5| + |(h5 * t + r5) * dc| := abs_add _ _
      _ = |dx5| + |h5 * t + r5| * |dc| := by rw [abs_mul]
      _ ≤ |dx5| + A5 * |dc| := by
        exact add_le_add_left (mul_le_mul_of_nonneg_right hcoef5 (abs_nonneg dc)) _
      _ ≤ |dx5| + A5 * G := by
        exact add_le_add_left (mul_le_mul_of_nonneg_left hdc hA5) _
  have hv4 : |dy4 + h4 * dc| ≤ |dy4| + |h4| * G := by
    calc
      |dy4 + h4 * dc| ≤ |dy4| + |h4 * dc| := abs_add _ _
      _ = |dy4| + |h4| * |dc| := by rw [abs_mul]
      _ ≤ |dy4| + |h4| * G := by
        exact add_le_add_left (mul_le_mul_of_nonneg_left hdc (abs_nonneg h4)) _
  have hv5 : |dy5 + h5 * dc| ≤ |dy5| + |h5| * G := by
    calc
      |dy5 + h5 * dc| ≤ |dy5| + |h5 * dc| := abs_add _ _
      _ = |dy5| + |h5| * |dc| := by rw [abs_mul]
      _ ≤ |dy5| + |h5| * G := by
        exact add_le_add_left (mul_le_mul_of_nonneg_left hdc (abs_nonneg h5)) _
  have hw : |t * dc| ≤ T * G := by
    rw [abs_mul, abs_of_nonneg ht0]
    calc
      t * |dc| ≤ t * G := mul_le_mul_of_nonneg_left hdc ht0
      _ ≤ T * G := mul_le_mul_of_nonneg_right htT hG
  exact ⟨hq4, hq5, hv4, hv5, hw⟩

/-- One-row form of the exact rank-one correction
`K_eff = K0 + kappa ⊗ gamma`.  This is the finite-sum-free kernel interface
consumed componentwise by an anisotropic `K` adapter. -/
theorem movingFrameParameterCorrection_to_K
    (K1 K2 K3 K4 kappa gamma1 gamma2 gamma3 gamma4
      dz1 dz2 dz3 dz4 dc residual : ℝ)
    (hkappa : 0 ≤ kappa)
    (hbase :
      |residual| ≤
        K1 * |dz1| + K2 * |dz2| + K3 * |dz3| + K4 * |dz4| + kappa * |dc|)
    (hdc : |dc| ≤ gammaBudget gamma1 gamma2 gamma3 gamma4 dz1 dz2 dz3 dz4) :
    |residual| ≤
      (K1 + kappa * gamma1) * |dz1| +
      (K2 + kappa * gamma2) * |dz2| +
      (K3 + kappa * gamma3) * |dz3| +
      (K4 + kappa * gamma4) * |dz4| := by
  have hcharge :
      kappa * |dc| ≤
        kappa * gammaBudget gamma1 gamma2 gamma3 gamma4 dz1 dz2 dz3 dz4 :=
    mul_le_mul_of_nonneg_left hdc hkappa
  calc
    |residual| ≤
        K1 * |dz1| + K2 * |dz2| + K3 * |dz3| + K4 * |dz4| + kappa * |dc| := hbase
    _ ≤ K1 * |dz1| + K2 * |dz2| + K3 * |dz3| + K4 * |dz4| +
        kappa * gammaBudget gamma1 gamma2 gamma3 gamma4 dz1 dz2 dz3 dz4 :=
      add_le_add_left hcharge _
    _ =
      (K1 + kappa * gamma1) * |dz1| +
      (K2 + kappa * gamma2) * |dz2| +
      (K3 + kappa * gamma3) * |dz3| +
      (K4 + kappa * gamma4) * |dz4| := by
      simp [gammaBudget]
      ring

/-- Any finite four-state homogeneous centered gain valid across arbitrary
parameter pairs forces the residual to be constant on every fixed-state
parameter fiber. -/
theorem fourStateCenteredGain_implies_parameterFiberConstancy
    (E : (Fin 4 → ℝ) → ℝ → ℝ) (ell2 : ℝ)
    (hGain : ∀ z zbar c cbar,
      (E z c - E zbar cbar) ^ 2 ≤ ell2 * ∑ i, (z i - zbar i) ^ 2) :
    ∀ z c cbar, E z c = E z cbar := by
  intro z c cbar
  have hzero : (E z c - E z cbar) ^ 2 ≤ 0 := by
    simpa using hGain z z c cbar
  nlinarith [sq_nonneg (E z c - E z cbar)]

/-- Frozen block-(4,5) moving-frame coefficients. -/
def block45H4 : ℝ := 2340 / 8699

def block45H5 : ℝ := 1520 / 8699

def block45R4 : ℝ := -21912800 / 75672601

def block45R5 : ℝ := -15007200 / 75672601

def block45A4T1 : ℝ := 21912800 / 75672601

def block45A5T1 : ℝ := 15007200 / 75672601

/-- Exact endpoint arithmetic for coordinate 4. -/
theorem block45_h4_plus_r4 :
    block45H4 + block45R4 = -1557140 / 75672601 := by
  norm_num [block45H4, block45R4]

/-- Exact endpoint arithmetic for coordinate 5. -/
theorem block45_h5_plus_r5 :
    block45H5 + block45R5 = -1784720 / 75672601 := by
  norm_num [block45H5, block45R5]

/-- Exact absolute velocity coefficient for coordinate 4. -/
theorem block45_h4_abs : |block45H4| = 2340 / 8699 := by
  norm_num [block45H4, abs_of_nonneg]

/-- Exact absolute velocity coefficient for coordinate 5. -/
theorem block45_h5_abs : |block45H5| = 1520 / 8699 := by
  norm_num [block45H5, abs_of_nonneg]

/-- The exact `A4(1)` rational is a uniform affine-center envelope on
`0 ≤ t ≤ 1`. -/
theorem block45_A4_T1_bound (t : ℝ) (ht0 : 0 ≤ t) (ht1 : t ≤ 1) :
    |block45H4 * t + block45R4| ≤ block45A4T1 := by
  rw [abs_le]
  constructor
  · norm_num [block45H4, block45R4, block45A4T1] at *
    nlinarith
  · norm_num [block45H4, block45R4, block45A4T1] at *
    nlinarith

/-- The exact `A5(1)` rational is a uniform affine-center envelope on
`0 ≤ t ≤ 1`. -/
theorem block45_A5_T1_bound (t : ℝ) (ht0 : 0 ≤ t) (ht1 : t ≤ 1) :
    |block45H5 * t + block45R5| ≤ block45A5T1 := by
  rw [abs_le]
  constructor
  · norm_num [block45H5, block45R5, block45A5T1] at *
    nlinarith
  · norm_num [block45H5, block45R5, block45A5T1] at *
    nlinarith

#print axioms movingFrameSourceDifference_exact
#print axioms movingFrameCommonParameter_cancel
#print axioms movingFrameSegment_preservesRampFiber
#print axioms gammaBudget_nonneg
#print axioms movingFrameUniformTransport_of_parameterControl
#print axioms movingFrameParameterCorrection_to_K
#print axioms fourStateCenteredGain_implies_parameterFiberConstancy
#print axioms block45_h4_plus_r4
#print axioms block45_h5_plus_r5
#print axioms block45_h4_abs
#print axioms block45_h5_abs
#print axioms block45_A4_T1_bound
#print axioms block45_A5_T1_bound

end

end RouteBP5MovingFrameTransport
