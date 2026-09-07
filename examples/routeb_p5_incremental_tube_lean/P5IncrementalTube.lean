import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
# Route-B P5 incremental hypocoercive-tube sidecar

Source-independent Lean decomposition of the algebraic core of
`review-T-P5-018-guyuefangyuan-20260907T0634.md`.

The file proves common-forcing cancellation for an actual/nominal pair, the
exact completed-square storage identity for the Route-B block-(4,5) rational
matrices, rational storage/state bounds, the improved ISS storage conversion,
and the division-free boundary-inward arithmetic.  It does not bind Julia/DH
or Float64 semantics, prove ODE existence/continuation, certify a P8 nominal
flowpipe, or close P5/P8/M4.
-/

set_option autoImplicit false

namespace RouteBP5IncrementalTube

noncomputable section

/-- Pointwise subtraction of two scalar second-order equations driven by the
same forcing removes that forcing exactly. -/
theorem common_forcing_cancels
    (m d b qdd qd q qbarDD qbarD qbar f l lbar : ℝ)
    (hact : m * qdd + d * qd + b * q = f - l)
    (hnom : m * qbarDD + d * qbarD + b * qbar = f - lbar) :
    m * (qdd - qbarDD) + d * (qd - qbarD) + b * (q - qbar) =
      -(l - lbar) := by
  linarith

/-- Two-channel version allowing the Route-B block coupling.  The shared
forcing may be arbitrary pointwise values; no affine-ramp hypothesis appears. -/
theorem block45_common_forcing_cancels
    (m4 m5 d4 d5 b44 b45 b54 b55
      q4dd q5dd q4d q5d q4 q5
      qb4dd qb5dd qb4d qb5d qb4 qb5
      f4 f5 l4 l5 lb4 lb5 : ℝ)
    (hact4 : m4*q4dd + d4*q4d + b44*q4 + b45*q5 = f4 - l4)
    (hact5 : m5*q5dd + d5*q5d + b54*q4 + b55*q5 = f5 - l5)
    (hnom4 : m4*qb4dd + d4*qb4d + b44*qb4 + b45*qb5 = f4 - lb4)
    (hnom5 : m5*qb5dd + d5*qb5d + b54*qb4 + b55*qb5 = f5 - lb5) :
    (m4*(q4dd-qb4dd) + d4*(q4d-qb4d) + b44*(q4-qb4) + b45*(q5-qb5)
        = -(l4-lb4)) ∧
    (m5*(q5dd-qb5dd) + d5*(q5d-qb5d) + b54*(q4-qb4) + b55*(q5-qb5)
        = -(l5-lb5)) := by
  constructor <;> linarith

/-- Route-B exactized block masses and damping coefficients. -/
def m4 : ℝ := 350003 / 3000000
def m5 : ℝ := 200739 / 4000000
def d4 : ℝ := 4 / 5
def d5 : ℝ := 13 / 20

/-- Symmetric part `K` of the block stiffness: off diagonal is `-3/400`. -/
def k44 : ℝ := 3 / 4
def k55 : ℝ := 29 / 50
def k45 : ℝ := -3 / 400

def massQuad (u4 u5 : ℝ) : ℝ := m4*u4^2 + m5*u5^2
def dampQuad (u4 u5 : ℝ) : ℝ := d4*u4^2 + d5*u5^2
def kQuad (u4 u5 : ℝ) : ℝ := k44*u4^2 + 2*k45*u4*u5 + k55*u5^2

def hQuad (u4 u5 : ℝ) : ℝ :=
  kQuad u4 u5 + dampQuad u4 u5 - massQuad u4 u5

/-- Incremental hypocoercive storage from T-P5-018. -/
def storage (x4 x5 y4 y5 : ℝ) : ℝ :=
  (1/2 : ℝ) * massQuad y4 y5 +
  (1/2 : ℝ) * kQuad x4 x5 +
  m4*x4*y4 + m5*x5*y5 +
  (1/2 : ℝ) * dampQuad x4 x5

/-- Exact completion
`Vd = 1/2 (y+x)^T M (y+x) + 1/2 x^T (K+D-M) x`. -/
theorem storage_completed_square (x4 x5 y4 y5 : ℝ) :
    storage x4 x5 y4 y5 =
      (1/2 : ℝ) * massQuad (y4+x4) (y5+x5) +
      (1/2 : ℝ) * hQuad x4 x5 := by
  simp [storage, massQuad, dampQuad, kQuad, hQuad]
  ring

/-- Exact rational lower mass bound `M >= (1/20) I`. -/
theorem mass_lower (u4 u5 : ℝ) :
    (1/20 : ℝ) * (u4^2 + u5^2) ≤ massQuad u4 u5 := by
  simp [massQuad, m4, m5]
  nlinarith [sq_nonneg u4, sq_nonneg u5]

/-- The mass is bounded above by its block-4 diagonal entry. -/
theorem mass_upper (u4 u5 : ℝ) :
    massQuad u4 u5 ≤ m4 * (u4^2 + u5^2) := by
  simp [massQuad, m4, m5]
  nlinarith [sq_nonneg u4, sq_nonneg u5]

/-- Exact rational lower bound `H = K+D-M >= (117/100) I`. -/
theorem h_lower (u4 u5 : ℝ) :
    (117/100 : ℝ) * (u4^2 + u5^2) ≤ hQuad u4 u5 := by
  simp [hQuad, kQuad, dampQuad, massQuad, k44, k55, k45, d4, d5, m4, m5]
  nlinarith [sq_nonneg (u4 - u5), sq_nonneg u4, sq_nonneg u5]

/-- Completed-square coercivity used for the tube-coordinate bounds. -/
theorem storage_lower_completed (x4 x5 y4 y5 : ℝ) :
    (1/40 : ℝ) * ((y4+x4)^2 + (y5+x5)^2) +
        (117/200 : ℝ) * (x4^2+x5^2) ≤ storage x4 x5 y4 y5 := by
  rw [storage_completed_square]
  have hm := mass_lower (y4+x4) (y5+x5)
  have hh := h_lower x4 x5
  nlinarith

/-- The symmetric stiffness satisfies the convenient upper bound
`K <= (303/400) I`. -/
theorem k_upper (u4 u5 : ℝ) :
    kQuad u4 u5 ≤ (303/400 : ℝ) * (u4^2 + u5^2) := by
  simp [kQuad, k44, k55, k45]
  nlinarith [sq_nonneg (u4 + u5), sq_nonneg u4, sq_nonneg u5]

/-- The damping block satisfies `D <= (4/5) I`. -/
theorem damp_upper (u4 u5 : ℝ) :
    dampQuad u4 u5 ≤ (4/5 : ℝ) * (u4^2 + u5^2) := by
  simp [dampQuad, d4, d5]
  nlinarith [sq_nonneg u4, sq_nonneg u5]

/-- Weighted Young bound for the storage cross term. -/
theorem mass_cross_upper (x4 x5 y4 y5 : ℝ) :
    m4*x4*y4 + m5*x5*y5 ≤
      (1/2 : ℝ) * massQuad x4 x5 + (1/2 : ℝ) * massQuad y4 y5 := by
  simp [massQuad, m4, m5]
  nlinarith [sq_nonneg (x4-y4), sq_nonneg (x5-y5)]

/-- Sharper rational storage upper estimate from T-P5-018. -/
theorem storage_upper_coefficients (x4 x5 y4 y5 : ℝ) :
    storage x4 x5 y4 y5 ≤
      (350003/3000000 : ℝ) * (y4^2+y5^2) +
      (5022503/6000000 : ℝ) * (x4^2+x5^2) := by
  have hmY := mass_upper y4 y5
  have hmX := mass_upper x4 x5
  have hk := k_upper x4 x5
  have hd := damp_upper x4 x5
  have hc := mass_cross_upper x4 x5 y4 y5
  simp [storage, m4] at *
  nlinarith

/-- Exact positive gap behind the clean `21/25` upper storage constant. -/
theorem storage_upper_gap :
    (21/25 : ℝ) - 5022503/6000000 = 17497/6000000 := by
  norm_num

/-- Clean storage equivalence `Vd <= (21/25) (||x||^2+||y||^2)`. -/
theorem storage_upper_21_25 (x4 x5 y4 y5 : ℝ) :
    storage x4 x5 y4 y5 ≤
      (21/25 : ℝ) * (x4^2+x5^2+y4^2+y5^2) := by
  have hu := storage_upper_coefficients x4 x5 y4 y5
  nlinarith [sq_nonneg x4, sq_nonneg x5, sq_nonneg y4, sq_nonneg y5]

/-- Position error bound extracted directly from the completed square. -/
theorem position_sq_bound (x4 x5 y4 y5 : ℝ) :
    x4^2 + x5^2 ≤ (200/117 : ℝ) * storage x4 x5 y4 y5 := by
  have h := storage_lower_completed x4 x5 y4 y5
  nlinarith [sq_nonneg (y4+x4), sq_nonneg (y5+x5)]

/-- Scalar identity used for the direct velocity estimate. -/
theorem velocity_completion_identity (x y : ℝ) :
    (1/20 : ℝ)*(y+x)^2 + (117/100 : ℝ)*x^2 =
      (117/2440 : ℝ)*y^2 + (61/50 : ℝ)*(x + (5/122 : ℝ)*y)^2 := by
  ring

/-- Direct velocity bound `||y||^2 <= (4880/117) Vd`, avoiding a triangle
inequality loss. -/
theorem velocity_sq_bound (x4 x5 y4 y5 : ℝ) :
    y4^2 + y5^2 ≤ (4880/117 : ℝ) * storage x4 x5 y4 y5 := by
  have h := storage_lower_completed x4 x5 y4 y5
  have hi4 := velocity_completion_identity x4 y4
  have hi5 := velocity_completion_identity x5 y5
  nlinarith [sq_nonneg (x4 + (5/122 : ℝ)*y4),
    sq_nonneg (x5 + (5/122 : ℝ)*y5)]

/-- Matching actual/nominal mechanical initial states give exactly zero
incremental storage. -/
theorem matching_initial_storage : storage 0 0 0 0 = 0 := by
  norm_num [storage, massQuad, kQuad, dampQuad, m4, m5, k44, k55, k45, d4, d5]

/-- Convert the `N`-dissipation inequality to the improved storage decay rate
using only `V <= 21/25 N`. -/
theorem iss_storage_refinement
    (V Vdot N R2 : ℝ)
    (hVupper : V ≤ (21/25 : ℝ) * N)
    (hdot : Vdot ≤ -(457/1600 : ℝ)*N + (800/457 : ℝ)*R2) :
    Vdot ≤ -(457/1344 : ℝ)*V + (800/457 : ℝ)*R2 := by
  nlinarith

/-- Division-free boundary test for the residual-only tube.  The integer
inequality `208849 Vstar > 1075200 L2` is exactly the condition making the
ISS upper bound strictly inward at `V=Vstar`. -/
theorem division_free_barrier_inward
    (Vstar L2 Vdot : ℝ)
    (hbar : 208849*Vstar > 1075200*L2)
    (hdot : Vdot ≤ -(457/1344 : ℝ)*Vstar + (800/457 : ℝ)*L2) :
    Vdot < 0 := by
  nlinarith

/-- The exact integer product appearing in the division-free barrier. -/
theorem barrier_integer_constants :
    (457 : ℤ)^2 = 208849 ∧ (800 : ℤ)*1344 = 1075200 := by
  norm_num

#print axioms common_forcing_cancels
#print axioms block45_common_forcing_cancels
#print axioms storage_completed_square
#print axioms mass_lower
#print axioms mass_upper
#print axioms h_lower
#print axioms storage_lower_completed
#print axioms k_upper
#print axioms damp_upper
#print axioms mass_cross_upper
#print axioms storage_upper_coefficients
#print axioms storage_upper_gap
#print axioms storage_upper_21_25
#print axioms position_sq_bound
#print axioms velocity_completion_identity
#print axioms velocity_sq_bound
#print axioms matching_initial_storage
#print axioms iss_storage_refinement
#print axioms division_free_barrier_inward
#print axioms barrier_integer_constants

end

end RouteBP5IncrementalTube
