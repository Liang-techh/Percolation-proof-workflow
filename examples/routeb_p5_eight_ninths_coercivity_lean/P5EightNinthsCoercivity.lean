import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
# Route-B P5 exact 8/9 hypocoercive coercivity sidecar

Source-independent Lean decomposition of
`agent_review_inbox/review-T-P5-032-honglianmozun-20260907T1253.md`.

The file freezes the exact block-(4,5) storage/dissipation quadratics, proves
an explicit nine-square identity for `Q - (8/9) V`, derives `Q >= (8/9) V`,
and exposes the sharpened ISS/barrier/parameter-tube arithmetic consumers.

It does not bind source gains, Julia/DH/Float64 semantics, P8 coverage, ODE
first-exit/continuation, provenance/admission, registry state, or final
integration.
-/

set_option autoImplicit false

namespace RouteBP5EightNinthsCoercivity

noncomputable section

/-- Exact rational block constants inherited from the established P5 algebra. -/
def m4 : ℝ := 350003 / 3000000
def m5 : ℝ := 200739 / 4000000
def d4 : ℝ := 4 / 5
def d5 : ℝ := 13 / 20
def k44 : ℝ := 3 / 4
def k55 : ℝ := 29 / 50
def k45 : ℝ := -3 / 400

/-- The exact `eps = 1` block-(4,5) hypocoercive storage. -/
def vStorage (x4 x5 y4 y5 : ℝ) : ℝ :=
  (1/2 : ℝ) * m4 * y4^2 + (1/2 : ℝ) * m5 * y5^2 +
  (1/2 : ℝ) * (k44*x4^2 + 2*k45*x4*x5 + k55*x5^2) +
  m4*x4*y4 + m5*x5*y5 +
  (1/2 : ℝ) * (d4*x4^2 + d5*x5^2)

/-- The exact dissipation quadratic `yᵀ(D-M)y + xᵀKx - yᵀAx`. -/
def qDissipation (x4 x5 y4 y5 : ℝ) : ℝ :=
  (d4-m4)*y4^2 + (d5-m5)*y5^2 +
  k44*x4^2 + 2*k45*x4*x5 + k55*x5^2 +
  (1/400 : ℝ)*x4*y5 - (1/400 : ℝ)*x5*y4

/-- Exact nine-square identity supplied by T-P5-032. -/
theorem nine_square_gap_identity (x4 x5 y4 y5 : ℝ) :
    qDissipation x4 x5 y4 y5 - (8/9 : ℝ) * vStorage x4 x5 y4 y5 =
      (51869/13500000 : ℝ) * x4^2 +
      (16837/3000000 : ℝ) * x5^2 +
      (15616199/27000000 : ℝ) * y4^2 +
      (6647479/12000000 : ℝ) * y5^2 +
      (1/240 : ℝ) * (x4-x5)^2 +
      (350003/6750000 : ℝ) * (x4-y4)^2 +
      (1/800 : ℝ) * (x4+y5)^2 +
      (1/800 : ℝ) * (x5-y4)^2 +
      (66913/3000000 : ℝ) * (x5-y5)^2 := by
  simp [qDissipation, vStorage, m4, m5, d4, d5, k44, k55, k45]
  ring

/-- Every coefficient in the explicit nine-square certificate is positive. -/
theorem nine_square_coefficients_positive :
    (0 : ℝ) < 51869/13500000 ∧
    (0 : ℝ) < 16837/3000000 ∧
    (0 : ℝ) < 15616199/27000000 ∧
    (0 : ℝ) < 6647479/12000000 ∧
    (0 : ℝ) < 1/240 ∧
    (0 : ℝ) < 350003/6750000 ∧
    (0 : ℝ) < 1/800 ∧
    (0 : ℝ) < 66913/3000000 := by
  norm_num

/-- Main sharpened coercivity theorem: `Q >= (8/9) V`. -/
theorem q_ge_eight_ninths_storage (x4 x5 y4 y5 : ℝ) :
    (8/9 : ℝ) * vStorage x4 x5 y4 y5 ≤ qDissipation x4 x5 y4 y5 := by
  have hid := nine_square_gap_identity x4 x5 y4 y5
  have hgap : 0 ≤
      (51869/13500000 : ℝ) * x4^2 +
      (16837/3000000 : ℝ) * x5^2 +
      (15616199/27000000 : ℝ) * y4^2 +
      (6647479/12000000 : ℝ) * y5^2 +
      (1/240 : ℝ) * (x4-x5)^2 +
      (350003/6750000 : ℝ) * (x4-y4)^2 +
      (1/800 : ℝ) * (x4+y5)^2 +
      (1/800 : ℝ) * (x5-y4)^2 +
      (66913/3000000 : ℝ) * (x5-y5)^2 := by
    positivity
  linarith

/-- Replace the old Euclidean detour by direct `Q >= (8/9)V` after the
unchanged half-`Q` residual absorption. -/
theorem improved_iss_refinement
    (V Vdot Q R2 : ℝ)
    (hQV : (8/9 : ℝ) * V ≤ Q)
    (hdot : Vdot ≤ -(1/2 : ℝ)*Q + (17/10 : ℝ)*R2) :
    Vdot ≤ -(4/9 : ℝ)*V + (17/10 : ℝ)*R2 := by
  nlinarith

/-- Exact ultimate coefficient `(17/10)/(4/9) = 153/40`. -/
theorem ultimate_gain_constant :
    (17/10 : ℝ) / (4/9 : ℝ) = 153/40 := by
  norm_num

/-- Exact improvement over the old `457/1344` decay coefficient. -/
theorem decay_improvement_factor :
    (4/9 : ℝ) / (457/1344 : ℝ) = 1792/1371 ∧
      (1 : ℝ) < 1792/1371 := by
  constructor <;> norm_num

/-- Generic division-free inward barrier for the sharpened ISS inequality. -/
theorem improved_barrier_inward
    (Vstar L2 Vdot : ℝ)
    (hbar : 153*L2 < 40*Vstar)
    (hdot : Vdot ≤ -(4/9 : ℝ)*Vstar + (17/10 : ℝ)*L2) :
    Vdot < 0 := by
  nlinarith

/-- Existing `Vstar=1/4` specialization: `153 L2 < 10`. -/
theorem quarter_barrier_inward
    (L2 Vdot : ℝ)
    (hbar : 153*L2 < 10)
    (hdot : Vdot ≤ -(4/9 : ℝ)*(1/4 : ℝ) + (17/10 : ℝ)*L2) :
    Vdot < 0 := by
  nlinarith

/-- The exact T-P5-030 initial coefficient still fits inside `Kc=1/12`. -/
theorem initial_coefficient_lt_one_twelfth :
    (474733828336525417 / 5726342542105201000 : ℝ) < 1/12 := by
  norm_num

/-- Generic first-exit arithmetic seam for a positive parameter-cell diameter.
The source/ODE layer is responsible for supplying the displayed derivative
bound at the tube boundary `V = Kc*dc^2`. -/
theorem parameter_tube_boundary_inward
    (mu nu Kc dc Vdot : ℝ)
    (hdc : 0 < dc^2)
    (hgate : 153*nu < (40 - 153*mu)*Kc)
    (hdot : Vdot ≤
      -(4/9 : ℝ)*(Kc*dc^2) +
        (17/10 : ℝ)*(mu*(Kc*dc^2) + nu*dc^2)) :
    Vdot < 0 := by
  have hscaled := mul_lt_mul_of_pos_right hgate hdc
  nlinarith

/-- `Kc=1/12` turns the generic boundary gate into
`153*mu + 1836*nu < 40`. -/
theorem one_twelfth_parameter_tube_gate
    (mu nu : ℝ)
    (hgate : 153*mu + 1836*nu < 40) :
    153*nu < (40 - 153*mu)*(1/12 : ℝ) := by
  nlinarith

/-- Direct downstream specialization for the T-P5-031 assignment
`mu=U+p`, `nu=W+q`. -/
theorem physical_slack_to_one_twelfth_gate
    (U W p q : ℝ)
    (hgate : 153*(U+p) + 1836*(W+q) < 40) :
    153*(W+q) < (40 - 153*(U+p))*(1/12 : ℝ) := by
  nlinarith

/-- Square-root-free necessity diagnostic for any nonnegative product slack
passing a residual budget `R`. -/
theorem slack_feasibility_necessity
    (U W p q R : ℝ)
    (hp : 0 ≤ p) (hq : 0 ≤ q)
    (hprod : U*W ≤ p*q)
    (hcost : 153*p + 1836*q < R) :
    0 < R ∧ 1123632*U*W < R^2 := by
  have hcost0 : 0 ≤ 153*p + 1836*q := by positivity
  have hR : 0 < R := lt_of_le_of_lt hcost0 hcost
  have hamgm : 1123632*p*q ≤ (153*p + 1836*q)^2 := by
    nlinarith [sq_nonneg (153*p - 1836*q)]
  have hscaled : 1123632*U*W ≤ 1123632*p*q := by
    nlinarith
  have hcostsq : (153*p + 1836*q)^2 < R^2 := by
    nlinarith
  constructor
  · exact hR
  · nlinarith

/-- Freezes the exact integer factor `4*153*1836`. -/
theorem exact_feasibility_factor :
    (4 : ℤ) * 153 * 1836 = 1123632 := by
  norm_num

#print axioms nine_square_gap_identity
#print axioms nine_square_coefficients_positive
#print axioms q_ge_eight_ninths_storage
#print axioms improved_iss_refinement
#print axioms ultimate_gain_constant
#print axioms decay_improvement_factor
#print axioms improved_barrier_inward
#print axioms quarter_barrier_inward
#print axioms initial_coefficient_lt_one_twelfth
#print axioms parameter_tube_boundary_inward
#print axioms one_twelfth_parameter_tube_gate
#print axioms physical_slack_to_one_twelfth_gate
#print axioms slack_feasibility_necessity
#print axioms exact_feasibility_factor

end

end RouteBP5EightNinthsCoercivity
