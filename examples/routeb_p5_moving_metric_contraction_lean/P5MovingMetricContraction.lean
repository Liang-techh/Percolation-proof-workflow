import Mathlib

namespace RouteBP5MovingMetricContraction

/-- Symmetric 2x2 quadratic form with entries `a,b,c`, representing
`[[a,b],[b,c]]`. -/
def qform2 (a b c x y : ℝ) : ℝ :=
  a * x ^ 2 + 2 * b * x * y + c * y ^ 2

/-- Bilinear form associated with the same symmetric 2x2 matrix. -/
def bilinear2 (a b c u1 u2 v1 v2 : ℝ) : ℝ :=
  a * u1 * v1 + b * u1 * v2 + b * u2 * v1 + c * u2 * v2

/-- First component of a 2x2 linear action. -/
def lin1 (m11 m12 x y : ℝ) : ℝ := m11 * x + m12 * y

/-- Second component of a 2x2 linear action. -/
def lin2 (m21 m22 x y : ℝ) : ℝ := m21 * x + m22 * y

/-- Quadratic form of the pulled-back metric `M = Jᵀ W J`, represented without
forming an inverse or a matrix square root. -/
def pullbackQ2
    (wa wb wc j11 j12 j21 j22 x y : ℝ) : ℝ :=
  qform2 wa wb wc (lin1 j11 j12 x y) (lin2 j21 j22 x y)

/-- Bilinear companion of `pullbackQ2`. -/
def pullbackBilinear2
    (wa wb wc j11 j12 j21 j22 u1 u2 v1 v2 : ℝ) : ℝ :=
  bilinear2 wa wb wc
    (lin1 j11 j12 u1 u2) (lin2 j21 j22 u1 u2)
    (lin1 j11 j12 v1 v2) (lin2 j21 j22 v1 v2)

/-- The pulled-back quadratic packet is the pulled-back bilinear packet on the
diagonal. -/
theorem pullback_quadratic_eq_bilinear
    (wa wb wc j11 j12 j21 j22 x y : ℝ) :
    pullbackQ2 wa wb wc j11 j12 j21 j22 x y
      = pullbackBilinear2 wa wb wc j11 j12 j21 j22 x y x y := by
  simp [pullbackQ2, pullbackBilinear2, qform2, bilinear2, lin1, lin2]
  ring

/-- Symmetric Jacobian packet `v ↦ <Av,v>_W + <v,Av>_W`. -/
def symJacobianQ2
    (wa wb wc a11 a12 a21 a22 x y : ℝ) : ℝ :=
  bilinear2 wa wb wc
      (lin1 a11 a12 x y) (lin2 a21 a22 x y) x y
    + bilinear2 wa wb wc
      x y (lin1 a11 a12 x y) (lin2 a21 a22 x y)

/-- Physical contraction quadratic packet
`AᵀW + WA - L_F W` at one variational vector. -/
def physicalContractionQ2
    (wa wb wc lfa lfb lfc a11 a12 a21 a22 x y : ℝ) : ℝ :=
  symJacobianQ2 wa wb wc a11 a12 a21 a22 x y
    - qform2 lfa lfb lfc x y

/-- Quadratic packet for the material derivative of the pulled-back metric.
`K` represents the moving-frame connection `J_t - D J[G]`. -/
def pullbackMaterialQ2
    (wa wb wc lfa lfb lfc
      j11 j12 j21 j22 k11 k12 k21 k22 x y : ℝ) : ℝ :=
  bilinear2 wa wb wc
      (lin1 k11 k12 x y) (lin2 k21 k22 x y)
      (lin1 j11 j12 x y) (lin2 j21 j22 x y)
    + qform2 lfa lfb lfc
      (lin1 j11 j12 x y) (lin2 j21 j22 x y)
    + bilinear2 wa wb wc
      (lin1 j11 j12 x y) (lin2 j21 j22 x y)
      (lin1 k11 k12 x y) (lin2 k21 k22 x y)

/-- Symmetric normalized Jacobian packet in the pulled-back metric. -/
def normalizedSymQ2
    (wa wb wc j11 j12 j21 j22 b11 b12 b21 b22 x y : ℝ) : ℝ :=
  pullbackBilinear2 wa wb wc j11 j12 j21 j22
      (lin1 b11 b12 x y) (lin2 b21 b22 x y) x y
    + pullbackBilinear2 wa wb wc j11 j12 j21 j22
      x y (lin1 b11 b12 x y) (lin2 b21 b22 x y)

/-- Normalized contraction packet `BᵀM + MB - L_G M`. -/
def normalizedContractionQ2
    (wa wb wc lfa lfb lfc
      j11 j12 j21 j22 k11 k12 k21 k22
      b11 b12 b21 b22 x y : ℝ) : ℝ :=
  normalizedSymQ2 wa wb wc j11 j12 j21 j22 b11 b12 b21 b22 x y
    - pullbackMaterialQ2 wa wb wc lfa lfb lfc
      j11 j12 j21 j22 k11 k12 k21 k22 x y

/-- Algebraic variational-energy identity: once the actual derivative is
provided as `L_F W - (AᵀW+WA)` at quadratic-form level, it is exactly the
negative physical contraction packet. This deliberately isolates calculus from
this kernel leaf. -/
theorem physical_variation_rate_identity
    (wa wb wc lfa lfb lfc a11 a12 a21 a22 x y dV : ℝ)
    (hdV : dV = qform2 lfa lfb lfc x y
      - symJacobianQ2 wa wb wc a11 a12 a21 a22 x y) :
    dV = - physicalContractionQ2
      wa wb wc lfa lfb lfc a11 a12 a21 a22 x y := by
  calc
    dV = qform2 lfa lfb lfc x y
      - symJacobianQ2 wa wb wc a11 a12 a21 a22 x y := hdV
    _ = -(symJacobianQ2 wa wb wc a11 a12 a21 a22 x y
      - qform2 lfa lfb lfc x y) := by ring
    _ = - physicalContractionQ2
      wa wb wc lfa lfb lfc a11 a12 a21 a22 x y := by rfl

/-- Main T-P5-090 algebraic kernel. If the moving-frame connection acts on the
current variational vector as `Kη = J(Bη) - A(Jη)`, then the complete normalized
contraction quadratic packet is exactly the physical contraction packet at
`Jη`. No inverse or square root is used. -/
theorem moving_metric_contraction_tensor_congruence
    (wa wb wc lfa lfb lfc
      j11 j12 j21 j22
      k11 k12 k21 k22
      b11 b12 b21 b22
      a11 a12 a21 a22
      x y : ℝ)
    (hk1 : lin1 k11 k12 x y
      = lin1 j11 j12 (lin1 b11 b12 x y) (lin2 b21 b22 x y)
        - lin1 a11 a12 (lin1 j11 j12 x y) (lin2 j21 j22 x y))
    (hk2 : lin2 k21 k22 x y
      = lin2 j21 j22 (lin1 b11 b12 x y) (lin2 b21 b22 x y)
        - lin2 a21 a22 (lin1 j11 j12 x y) (lin2 j21 j22 x y)) :
    normalizedContractionQ2
      wa wb wc lfa lfb lfc
      j11 j12 j21 j22 k11 k12 k21 k22
      b11 b12 b21 b22 x y
      = physicalContractionQ2
        wa wb wc lfa lfb lfc a11 a12 a21 a22
        (lin1 j11 j12 x y) (lin2 j21 j22 x y) := by
  simp only [lin1, lin2] at hk1 hk2
  simp only [normalizedContractionQ2, normalizedSymQ2,
    pullbackMaterialQ2, pullbackBilinear2, physicalContractionQ2,
    symJacobianQ2, qform2, bilinear2, lin1, lin2]
  rw [hk1, hk2]
  ring

/-- Pure quadratic-form substitution: any physical contraction rate `mu`
transports to the pulled-back metric with exactly the same numerical rate. -/
theorem contraction_rate_pullback
    (wa wb wc lfa lfb lfc a11 a12 a21 a22
      j11 j12 j21 j22 mu x y : ℝ)
    (hphys : ∀ u v : ℝ,
      physicalContractionQ2
        wa wb wc lfa lfb lfc a11 a12 a21 a22 u v
        ≥ 2 * mu * qform2 wa wb wc u v) :
    physicalContractionQ2
        wa wb wc lfa lfb lfc a11 a12 a21 a22
        (lin1 j11 j12 x y) (lin2 j21 j22 x y)
      ≥ 2 * mu * pullbackQ2 wa wb wc j11 j12 j21 j22 x y := by
  simpa [pullbackQ2] using
    hphys (lin1 j11 j12 x y) (lin2 j21 j22 x y)

/-- Consumer-facing rate theorem: a separately checked congruence identity plus
the physical quadratic lower certificate is enough to obtain the normalized
rate, so the forward path stays division-free. -/
theorem normalized_rate_of_congruence
    (wa wb wc lfa lfb lfc a11 a12 a21 a22
      j11 j12 j21 j22 mu x y cz : ℝ)
    (hcong : cz = physicalContractionQ2
      wa wb wc lfa lfb lfc a11 a12 a21 a22
      (lin1 j11 j12 x y) (lin2 j21 j22 x y))
    (hphys : ∀ u v : ℝ,
      physicalContractionQ2
        wa wb wc lfa lfb lfc a11 a12 a21 a22 u v
        ≥ 2 * mu * qform2 wa wb wc u v) :
    cz ≥ 2 * mu * pullbackQ2 wa wb wc j11 j12 j21 j22 x y := by
  rw [hcong]
  exact contraction_rate_pullback
    wa wb wc lfa lfb lfc a11 a12 a21 a22
    j11 j12 j21 j22 mu x y hphys

/-- One-dimensional regression for the first unsound shortcut: with `A=0` and
material metric derivative `L_F W=1`, the true contraction scalar is `-1`,
whereas freezing the metric would retain only the zero Jacobian packet. -/
def physicalContraction1 (A W LF : ℝ) : ℝ := 2 * A * W - LF

theorem dropping_material_metric_derivative_counterexample :
    physicalContraction1 0 1 1 = (-1 : ℝ)
      ∧ (2 : ℝ) * 0 * 1 = 0 := by
  norm_num [physicalContraction1]

/-- One-dimensional moving affine chart regression. The denominator-cleared
identity `(1+t)B=1` is already enough to show that the apparent normalized
Jacobian contraction is canceled exactly by the pulled-back metric derivative. -/
theorem moving_affine_chart_material_cancellation
    (t B : ℝ) (hB : (1 + t) * B = 1) :
    2 * B * (1 + t) ^ 2 - 2 * (1 + t) = 0 := by
  calc
    2 * B * (1 + t) ^ 2 - 2 * (1 + t)
        = 2 * (1 + t) * ((1 + t) * B - 1) := by ring
    _ = 0 := by rw [hB]; ring

#print axioms pullback_quadratic_eq_bilinear
#print axioms physical_variation_rate_identity
#print axioms moving_metric_contraction_tensor_congruence
#print axioms contraction_rate_pullback
#print axioms normalized_rate_of_congruence
#print axioms dropping_material_metric_derivative_counterexample
#print axioms moving_affine_chart_material_cancellation

end RouteBP5MovingMetricContraction
