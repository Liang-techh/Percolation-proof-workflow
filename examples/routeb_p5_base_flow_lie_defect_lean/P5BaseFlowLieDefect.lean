import Mathlib

namespace RouteBP5BaseFlowLieDefect

def qform2 (a b c x y : ℝ) : ℝ := a*x^2 + 2*b*x*y + c*y^2

def bilinear2 (a b c u1 u2 v1 v2 : ℝ) : ℝ :=
  a*u1*v1 + b*u1*v2 + b*u2*v1 + c*u2*v2

def lin1 (m11 m12 x y : ℝ) : ℝ := m11*x + m12*y

def lin2 (m21 m22 x y : ℝ) : ℝ := m21*x + m22*y

def symJacobianQ2 (wa wb wc a11 a12 a21 a22 x y : ℝ) : ℝ :=
  bilinear2 wa wb wc (lin1 a11 a12 x y) (lin2 a21 a22 x y) x y +
  bilinear2 wa wb wc x y (lin1 a11 a12 x y) (lin2 a21 a22 x y)

def physicalContractionQ2
    (wa wb wc lfa lfb lfc a11 a12 a21 a22 x y : ℝ) : ℝ :=
  symJacobianQ2 wa wb wc a11 a12 a21 a22 x y - qform2 lfa lfb lfc x y

def baseLieDefectQ2
    (wa wb wc dwa dwb dwc b11 b12 b21 b22 x y : ℝ) : ℝ :=
  qform2 dwa dwb dwc x y + symJacobianQ2 wa wb wc b11 b12 b21 b22 x y

def perturbedContractionQ2
    (wa wb wc lfa lfb lfc dwa dwb dwc
      a11 a12 a21 a22 b11 b12 b21 b22 x y : ℝ) : ℝ :=
  physicalContractionQ2 wa wb wc lfa lfb lfc a11 a12 a21 a22 x y -
  baseLieDefectQ2 wa wb wc dwa dwb dwc b11 b12 b21 b22 x y

/-- Exact algebraic form of `Vdot = -Q_C0 + Q_Sb`. -/
theorem base_flow_lie_defect_q2_identity
    (wa wb wc lfa lfb lfc dwa dwb dwc
      a11 a12 a21 a22 b11 b12 b21 b22 x y : ℝ) :
    qform2 lfa lfb lfc x y + qform2 dwa dwb dwc x y -
        symJacobianQ2 wa wb wc a11 a12 a21 a22 x y +
        symJacobianQ2 wa wb wc b11 b12 b21 b22 x y =
      -perturbedContractionQ2 wa wb wc lfa lfb lfc dwa dwb dwc
        a11 a12 a21 a22 b11 b12 b21 b22 x y := by
  simp only [perturbedContractionQ2, physicalContractionQ2, baseLieDefectQ2]
  ring

/-- Signed Lie-defect certificate loses exactly `rho` from the nominal rate. -/
theorem base_flow_lie_defect_rate_loss
    (QW C0 Sb mu rho dV : ℝ)
    (hdV : dV = -C0 + Sb)
    (hC0 : 2*mu*QW ≤ C0)
    (hSb : Sb ≤ 2*rho*QW) :
    dV ≤ -2*(mu-rho)*QW := by
  rw [hdV]
  nlinarith

/-- A separate relative variational defect is charged after the exact base-flow packet. -/
theorem base_flow_plus_variational_defect_rate
    (QW C0 Sb rCross dCross mu rho sigma dV : ℝ)
    (hdV : dV = -C0 + Sb + 2*rCross + 2*dCross)
    (hC0 : 2*mu*QW ≤ C0)
    (hSb : Sb ≤ 2*rho*QW)
    (hr : rCross ≤ sigma*QW) :
    dV ≤ -2*(mu-rho-sigma)*QW + 2*dCross := by
  rw [hdV]
  nlinarith

/-- Vectorwise PSD premise gives the weighted square-completion inequality. -/
theorem weighted_square_completion
    (wa wb wc nu x y d1 d2 : ℝ)
    (hsquare : 0 ≤ qform2 wa wb wc (nu*x-d1) (nu*y-d2)) :
    2*nu*bilinear2 wa wb wc x y d1 d2 ≤
      nu^2*qform2 wa wb wc x y + qform2 wa wb wc d1 d2 := by
  simp only [qform2, bilinear2] at hsquare ⊢
  nlinarith

/-- Main mixed relative-plus-additive division-free energy bound. -/
theorem base_flow_mixed_defect_energy
    (QW C0 Sb rCross dCross Qd Ebar mu rho sigma nu dV : ℝ)
    (hnu : nu = mu-rho-sigma)
    (hnu_pos : 0 < nu)
    (hdV : dV = -C0 + Sb + 2*rCross + 2*dCross)
    (hC0 : 2*mu*QW ≤ C0)
    (hSb : Sb ≤ 2*rho*QW)
    (hr : rCross ≤ sigma*QW)
    (hsquare : 2*nu*dCross ≤ nu^2*QW + Qd)
    (hQd : Qd ≤ Ebar) :
    nu*dV ≤ -(nu^2)*QW + Ebar := by
  have hrate : dV ≤ -2*nu*QW + 2*dCross := by
    rw [hnu]
    exact base_flow_plus_variational_defect_rate
      QW C0 Sb rCross dCross mu rho sigma dV hdV hC0 hSb hr
  have hmul : nu*dV ≤ nu*(-2*nu*QW + 2*dCross) :=
    mul_le_mul_of_nonneg_left hrate (le_of_lt hnu_pos)
  nlinarith

/-- Boundary form of the invariant-tube gate. -/
theorem base_flow_mixed_defect_invariant_boundary
    (nu dV V Vstar Ebar : ℝ)
    (hnu_pos : 0 < nu)
    (hmain : nu*dV ≤ -(nu^2)*V + Ebar)
    (hboundary : V = Vstar)
    (hgate : Ebar ≤ nu^2*Vstar) : dV ≤ 0 := by
  have hmul : nu*dV ≤ nu*0 := by
    rw [hboundary] at hmain
    nlinarith
  exact (mul_le_mul_left hnu_pos).mp hmul

/-- Constant Euclidean metric: a skew base Jacobian has zero Lie-defect cost. -/
theorem constant_metric_skew_base_defect_zero (k x y : ℝ) :
    baseLieDefectQ2 1 0 1 0 0 0 0 (-k) k 0 x y = 0 := by
  simp [baseLieDefectQ2, qform2, symJacobianQ2, bilinear2, lin1, lin2]
  ring

def contraction1 (A W LF : ℝ) : ℝ := 2*A*W - LF

def baseLieDefect1 (DWb B W : ℝ) : ℝ := DWb + 2*B*W

/-- `Db=0` can still lose contraction when state-dependent metric transport is omitted. -/
theorem dropping_metric_transport_of_base_defect_counterexample :
    contraction1 (1/4 : ℝ) 1 0 = 1/2 ∧
    baseLieDefect1 1 0 1 = 1 ∧
    contraction1 (1/4 : ℝ) 1 0 - baseLieDefect1 1 0 1 = -1/2 := by
  norm_num [contraction1, baseLieDefect1]

#print axioms base_flow_lie_defect_q2_identity
#print axioms base_flow_lie_defect_rate_loss
#print axioms base_flow_plus_variational_defect_rate
#print axioms weighted_square_completion
#print axioms base_flow_mixed_defect_energy
#print axioms base_flow_mixed_defect_invariant_boundary
#print axioms constant_metric_skew_base_defect_zero
#print axioms dropping_metric_transport_of_base_defect_counterexample

end RouteBP5BaseFlowLieDefect
