import Mathlib

namespace RouteBP5BaseStorageCollar

/-- Compress one signed base-energy ledger into a relative-plus-additive rate bound. -/
theorem energy_ledger_rate_compression
    (Udot U D P c alpha theta beta : ℝ)
    (hledger : Udot ≤ -c*U - D + P)
    (hpower : P ≤ alpha*U + theta*D + beta)
    (hD : 0 ≤ D)
    (htheta : theta ≤ 1) :
    Udot ≤ -(c-alpha)*U + beta := by
  have hshare : 0 ≤ (1-theta)*D :=
    mul_nonneg (sub_nonneg.mpr htheta) hD
  nlinarith

/-- Two defect channels compose by adding their relative, dissipative and additive debits. -/
theorem two_channel_allocation_composes
    (U D P1 P2 a1 a2 t1 t2 b1 b2 : ℝ)
    (h1 : P1 ≤ a1*U + t1*D + b1)
    (h2 : P2 ≤ a2*U + t2*D + b2) :
    P1 + P2 ≤ (a1+a2)*U + (t1+t2)*D + (b1+b2) := by
  nlinarith

/-- Division-free ledger-to-collar compiler, including the inner-level additive gate. -/
theorem base_storage_collar_of_energy_ledger
    (Udot U D P c alpha theta beta Rin Rout : ℝ)
    (hledger : Udot ≤ -c*U - D + P)
    (hpower : P ≤ alpha*U + theta*D + beta)
    (hD : 0 ≤ D)
    (halpha : alpha < c)
    (htheta : theta ≤ 1)
    (hgate : beta ≤ (c-alpha)*Rin)
    (hlevels : Rin < Rout) :
    0 < c-alpha ∧
      (c-alpha)*Udot ≤ -((c-alpha)^2)*U + (c-alpha)*beta ∧
      (c-alpha)*beta ≤ (c-alpha)^2*Rin ∧
      Rin < Rout := by
  have hnu : 0 < c-alpha := sub_pos.mpr halpha
  have hrate : Udot ≤ -(c-alpha)*U + beta :=
    energy_ledger_rate_compression Udot U D P c alpha theta beta
      hledger hpower hD htheta
  have hscaled := mul_le_mul_of_nonneg_left hrate (le_of_lt hnu)
  have hgateScaled := mul_le_mul_of_nonneg_left hgate (le_of_lt hnu)
  constructor
  · exact hnu
  constructor
  · nlinarith [hscaled]
  constructor
  · nlinarith [hgateScaled]
  · exact hlevels

def qform2 (a b c x y : ℝ) : ℝ := a*x^2 + 2*b*x*y + c*y^2

def bilinear2 (a b c u1 u2 v1 v2 : ℝ) : ℝ :=
  a*u1*v1 + b*u1*v2 + b*u2*v1 + c*u2*v2

def lin1 (m11 m12 x y : ℝ) : ℝ := m11*x + m12*y

def lin2 (m21 m22 x y : ℝ) : ℝ := m21*x + m22*y

def symActionQ2 (wa wb wc a11 a12 a21 a22 x y : ℝ) : ℝ :=
  bilinear2 wa wb wc (lin1 a11 a12 x y) (lin2 a21 a22 x y) x y +
  bilinear2 wa wb wc x y (lin1 a11 a12 x y) (lin2 a21 a22 x y)

/-- Algebraic raw derivative for a lifted base storage. The two metric-drift triples
are caller-bound to `W_t-DW[F]` and `DW[b]`, respectively. -/
def liftedBaseRawQ2
    (wa wb wc nma nmb nmc bma bmb bmc
      a11 a12 a21 a22 b11 b12 b21 b22 x y e1 e2 : ℝ) : ℝ :=
  -symActionQ2 wa wb wc a11 a12 a21 a22 x y +
    symActionQ2 wa wb wc b11 b12 b21 b22 x y +
    qform2 nma nmb nmc x y + qform2 bma bmb bmc x y +
    2*bilinear2 wa wb wc x y e1 e2

def nominalContractionQ2
    (wa wb wc nma nmb nmc a11 a12 a21 a22 x y : ℝ) : ℝ :=
  symActionQ2 wa wb wc a11 a12 a21 a22 x y - qform2 nma nmb nmc x y

def baseLieDefectQ2
    (wa wb wc bma bmb bmc b11 b12 b21 b22 x y : ℝ) : ℝ :=
  qform2 bma bmb bmc x y + symActionQ2 wa wb wc b11 b12 b21 b22 x y

/-- Exact lifted-base-storage identity `Udot = -C0 + Sb + 2 <zeta,W e_lift>`. -/
theorem lifted_base_storage_q2_identity
    (wa wb wc nma nmb nmc bma bmb bmc
      a11 a12 a21 a22 b11 b12 b21 b22 x y e1 e2 : ℝ) :
    liftedBaseRawQ2 wa wb wc nma nmb nmc bma bmb bmc
        a11 a12 a21 a22 b11 b12 b21 b22 x y e1 e2 =
      -nominalContractionQ2 wa wb wc nma nmb nmc
          a11 a12 a21 a22 x y +
        baseLieDefectQ2 wa wb wc bma bmb bmc
          b11 b12 b21 b22 x y +
        2*bilinear2 wa wb wc x y e1 e2 := by
  simp only [liftedBaseRawQ2, nominalContractionQ2, baseLieDefectQ2]
  ring

/-- A pointwise nonnegative weighted square gives the exact completion used by the collar. -/
theorem lift_weighted_square_completion
    (wa wb wc nu x y d1 d2 : ℝ)
    (hsquare : 0 ≤ qform2 wa wb wc (nu*x-d1) (nu*y-d2)) :
    2*nu*bilinear2 wa wb wc x y d1 d2 ≤
      nu^2*qform2 wa wb wc x y + qform2 wa wb wc d1 d2 := by
  simp only [qform2, bilinear2] at hsquare ⊢
  nlinarith

/-- Robust lifted collar: nominal contraction, signed base Lie defect, relative lift
power, and one additive metric budget imply the T-P5-096 scalar inequality. -/
theorem lifted_base_storage_robust_collar
    (U C0 Sb rCross dCross Qd Ebar mu rhoB rhoR nu Udot : ℝ)
    (hnu : nu = mu-rhoB-rhoR)
    (hnuPos : 0 < nu)
    (hUdot : Udot = -C0 + Sb + 2*rCross + 2*dCross)
    (hC0 : 2*mu*U ≤ C0)
    (hSb : Sb ≤ 2*rhoB*U)
    (hr : rCross ≤ rhoR*U)
    (hsquare : 2*nu*dCross ≤ nu^2*U + Qd)
    (hQd : Qd ≤ Ebar) :
    nu*Udot ≤ -(nu^2)*U + Ebar := by
  have hrate : Udot ≤ -2*nu*U + 2*dCross := by
    rw [hUdot]
    nlinarith
  have hscaled := mul_le_mul_of_nonneg_left hrate (le_of_lt hnuPos)
  nlinarith [hscaled, hsquare, hQd]

/-- The additive gate makes the inner collar boundary inward-pointing. -/
theorem lifted_base_storage_inner_boundary
    (nu Udot U Rin Ebar : ℝ)
    (hnuPos : 0 < nu)
    (hmain : nu*Udot ≤ -(nu^2)*U + Ebar)
    (hboundary : U = Rin)
    (hgate : Ebar ≤ nu^2*Rin) :
    Udot ≤ 0 := by
  rw [hboundary] at hmain
  have hmul : nu*Udot ≤ 0 := by
    nlinarith
  by_contra hnot
  have hUdotPos : 0 < Udot := lt_of_not_ge hnot
  have hprodPos : 0 < nu*Udot := mul_pos hnuPos hUdotPos
  nlinarith

/-- Under `U_tilde = a U + k`, the collar additive budget is
`E_tilde = a E + nu^2 k`; keeping `E` unchanged is not covariant. -/
theorem affine_storage_normalization_transport
    (nu U Udot E a k : ℝ)
    (ha : 0 < a)
    (hbase : nu*Udot ≤ -(nu^2)*U + E) :
    nu*(a*Udot) ≤ -(nu^2)*(a*U+k) + (a*E + nu^2*k) := by
  have hscaled := mul_le_mul_of_nonneg_left hbase (le_of_lt ha)
  nlinarith [hscaled]

/-- The inner additive gate is exactly invariant under positive affine storage scaling. -/
theorem affine_storage_gate_covariant
    (nu E Rin a k : ℝ)
    (ha : 0 < a) :
    (a*E + nu^2*k ≤ nu^2*(a*Rin+k)) ↔ E ≤ nu^2*Rin := by
  constructor
  · intro hshift
    by_contra hnot
    have hstrict : nu^2*Rin < E := lt_of_not_ge hnot
    have hscaled : a*(nu^2*Rin) < a*E :=
      mul_lt_mul_of_pos_left hstrict ha
    nlinarith
  · intro hbase
    have hscaled := mul_le_mul_of_nonneg_left hbase (le_of_lt ha)
    nlinarith [hscaled]

/-- Positive affine normalization preserves the strict two-level collar gap. -/
theorem affine_storage_gap_covariant
    (Rin Rout a k : ℝ)
    (ha : 0 < a)
    (hgap : Rin < Rout) :
    a*Rin+k < a*Rout+k := by
  have hscaled := mul_lt_mul_of_pos_left hgap ha
  nlinarith

/-- Exact scalar nonlinear regression: for `F(x)=x+x^3`, `zeta=x`, `W=1`,
the lift defect is `2x^3`, and omitting it misses exactly `4x^4`. -/
theorem nonlinear_identity_lift_defect_regression (x : ℝ) :
    (-x-x^3) - (-(1+3*x^2)*x) = 2*x^3 ∧
      (-2*x^2-2*x^4) - (-2*(1+3*x^2)*x^2) = 4*x^4 ∧
      -2*(1+3*x^2)*x^2 + 2*x*(2*x^3) = -2*x^2-2*x^4 := by
  constructor
  · ring
  constructor <;> ring

#print axioms energy_ledger_rate_compression
#print axioms two_channel_allocation_composes
#print axioms base_storage_collar_of_energy_ledger
#print axioms lifted_base_storage_q2_identity
#print axioms lift_weighted_square_completion
#print axioms lifted_base_storage_robust_collar
#print axioms lifted_base_storage_inner_boundary
#print axioms affine_storage_normalization_transport
#print axioms affine_storage_gate_covariant
#print axioms affine_storage_gap_covariant
#print axioms nonlinear_identity_lift_defect_regression

end RouteBP5BaseStorageCollar
