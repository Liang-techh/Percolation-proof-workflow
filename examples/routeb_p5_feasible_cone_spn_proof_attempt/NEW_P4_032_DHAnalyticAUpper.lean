import NEW_P4_032_ExactCellLambdaConsumer

/-!
OPEN_UNCOMPILED / pending. Analytic squared-residual envelope from the
transcribed compact-DH coefficients. No sampling or claimed acceleration
envelope, true-DH source authentication, Lean/Lake run or registry action.
-/
set_option autoImplicit false

namespace RouteBP4032DHAnalyticAUpper

open RouteBP4032SameSourceConsumerPacket RouteBP4032DHProducerBaseBridge
open RouteBP4032ExactCellLambdaConsumer RouteBP4032BlockDefects

noncomputable section

def nominalForce (x : State) : BVec := ![
  -(3 / 4) * x.angles 2 - (4 / 5) * x.velocity 0 +
    (1 / 5) * x.disturbance + (1 / 100) * x.angles 3,
  -(29 / 50) * x.angles 3 - (13 / 20) * x.velocity 1 +
    (1 / 10) * x.disturbance + (1 / 200) * x.angles 2]

def nominalInertiaForce (x : State) : BVec := ![
  (350003 / 3000000) * x.acceleration 0,
  (200739 / 4000000) * x.acceleration 1]

theorem residual_split (x : State) :
    (fun j => nominalForce x j + -(nominalInertiaForce x j)) = dhLBase x := by
  funext j
  fin_cases j <;> simp [nominalForce, nominalInertiaForce, dhLBase, sub_eq_add_neg]

theorem four_term_square (a b c d : ℝ) :
    (a + b + c + d)^2 ≤ 4 * (a^2 + b^2 + c^2 + d^2) := by
  nlinarith [sq_nonneg (a-b), sq_nonneg (a-c), sq_nonneg (a-d),
    sq_nonneg (b-c), sq_nonneg (b-d), sq_nonneg (c-d)]

theorem nominal_force_upper (x : State) :
    sqNorm (nominalForce x) ≤ (16 / 5) * blockP x + (1 / 5) * x.disturbance^2 := by
  have h4 := four_term_square (-(3 / 4) * x.angles 2) (-(4 / 5) * x.velocity 0)
    ((1 / 5) * x.disturbance) ((1 / 100) * x.angles 3)
  have h5 := four_term_square (-(29 / 50) * x.angles 3) (-(13 / 20) * x.velocity 1)
    ((1 / 10) * x.disturbance) ((1 / 200) * x.angles 2)
  dsimp [sqNorm, nominalForce, blockP]
  nlinarith [sq_nonneg (x.angles 2), sq_nonneg (x.angles 3),
    sq_nonneg (x.velocity 0), sq_nonneg (x.velocity 1)]

theorem inertia_force_upper (x : State) :
    2 * sqNorm (nominalInertiaForce x) ≤ (1 / 4) * producerMetric x := by
  dsimp [sqNorm, nominalInertiaForce, producerMetric]
  nlinarith [sq_nonneg (x.acceleration 0), sq_nonneg (x.acceleration 1)]

/-- Global polynomial inequality, with no physical-domain premise. -/
theorem dh_residual_analytic_upper (x : State) :
    sqNorm (dhLBase x) ≤ (32 / 5) * blockP x +
      (2 / 5) * x.disturbance^2 + (1 / 4) * producerMetric x := by
  have hy := young_two_vectors (nominalForce x) (fun j => -(nominalInertiaForce x j))
  rw [residual_split] at hy
  have hn : sqNorm (fun j => -(nominalInertiaForce x j)) = sqNorm (nominalInertiaForce x) := by
    simp [sqNorm]
  rw [hn] at hy
  have hf := nominal_force_upper x
  have hi := inertia_force_upper x
  linarith

theorem conditional_cell_A_upper (x : State) (accelerationCap : ℝ)
    (hp : blockP x ≤ 28 / 5) (hw : x.disturbance^2 ≤ 3)
    (ha : producerMetric x ≤ accelerationCap) :
    sqNorm (dhLBase x) ≤ 926 / 25 + accelerationCap / 4 := by
  have h := dh_residual_analytic_upper x
  linarith

/-- Exact adapter for the A_upper field of SameSourceCharges. It does not
construct the remaining P_upper, D_lower or cover obligations. -/
theorem rational_A_upper_field {ι : Type*} (key : SourceKey)
    (D : State → Prop) (base : State → ℝ) (cell : ι → State → Prop)
    (c : RationalCharges ι) (accelerationCap : ι → ℚ)
    (hp : ∀ i x, D x → cell i x → blockP x ≤ 28 / 5)
    (hw : ∀ i x, D x → cell i x → x.disturbance^2 ≤ 3)
    (ha : ∀ i x, D x → cell i x → producerMetric x ≤ (accelerationCap i : ℝ))
    (hfit : ∀ i, 926 / 25 + accelerationCap i / 4 ≤ c.A i) :
    ∀ i x, (source key D base).domain x → cell i x →
      sqNorm ((source key D base).lBase x) ≤ (c.A i : ℝ) := by
  intro i x hx hi
  have h := conditional_cell_A_upper x (accelerationCap i : ℝ)
    (hp i x hx hi) (hw i x hx hi) (ha i x hx hi)
  have hfitR : (926 / 25 : ℝ) + (accelerationCap i : ℝ) / 4 ≤ (c.A i : ℝ) := by
    exact_mod_cast hfit i
  exact h.trans hfitR

/-- Any finite nonnegative proposed A cap is defeated on the unrestricted
acceleration ray. It still satisfies p45=0, w=0 and producer angle geometry. -/
theorem no_cap_from_angles_and_block_only (cap : ℝ) (hc : 0 ≤ cap) :
    ∃ x : State, producerGeometry x ∧ blockP x ≤ 28 / 5 ∧
      x.disturbance^2 ≤ 3 ∧ cap < sqNorm (dhLBase x) := by
  let z : ℝ := (3000000 / 350003) * (cap + 1)
  refine ⟨accelerationRay z, ray_producer_geometry z, ?_, ?_, ?_⟩
  · norm_num [blockP, accelerationRay]
  · norm_num [accelerationRay]
  · rw [ray_base_residual]
    have heq : (350003 / 3000000 : ℝ)^2 * z^2 = (cap + 1)^2 := by
      dsimp [z]
      ring
    rw [heq]
    nlinarith [sq_nonneg cap]

end
end RouteBP4032DHAnalyticAUpper
