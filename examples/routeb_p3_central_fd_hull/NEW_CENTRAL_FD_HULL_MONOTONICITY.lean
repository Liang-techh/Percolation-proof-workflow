import Mathlib.Data.Real.Basic
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic

/-!
# P3 monotonicity seam for a unified derivative-first radius

This sidecar does not repeat the weighted-power inequality.  It consumes an
already established bound with component radius `R` and lifts its right-hand
side to a larger nonnegative radius `Qbar`.  It also proves the finite-sum
monotonicity needed to obtain component `Q` from a derivative-first tensor
radius `mu`.
-/

open scoped BigOperators

set_option autoImplicit false

namespace RouteBP3CentralFDHullMonotonicity

noncomputable section

abbrev I6 := Fin 6
abbrev Tensor6 := I6 → I6 → I6 → ℝ
abbrev Vector6 := I6 → ℝ

def gammaRadius6 (mu : Tensor6) (i j k : I6) : ℝ :=
  (mu k i j + mu j i k + mu i j k) / 2

def componentQ6 (mu : Tensor6) (v : Vector6) (i : I6) : ℝ :=
  ∑ j, ∑ k, gammaRadius6 mu i j k * |v j * v k|

theorem gammaRadius6_nonneg
    (mu : Tensor6) (hmu : ∀ k i j, 0 ≤ mu k i j)
    (i j k : I6) :
    0 ≤ gammaRadius6 mu i j k := by
  unfold gammaRadius6
  linarith [hmu k i j, hmu j i k, hmu i j k]

theorem gammaRadius6_mono
    (mu muBar : Tensor6)
    (hmu : ∀ k i j, 0 ≤ mu k i j)
    (hle : ∀ k i j, mu k i j ≤ muBar k i j)
    (i j k : I6) :
    gammaRadius6 mu i j k ≤ gammaRadius6 muBar i j k := by
  unfold gammaRadius6
  gcongr
  · exact hle k i j
  · exact hle j i k
  · exact hle i j k

theorem componentQ6_nonneg
    (mu : Tensor6) (v : Vector6)
    (hmu : ∀ k i j, 0 ≤ mu k i j)
    (i : I6) :
    0 ≤ componentQ6 mu v i := by
  unfold componentQ6
  apply Finset.sum_nonneg
  intro j hj
  apply Finset.sum_nonneg
  intro k hk
  exact mul_nonneg
    (gammaRadius6_nonneg mu hmu i j k) (abs_nonneg _)

theorem componentQ6_mono
    (mu muBar : Tensor6) (v : Vector6)
    (hmu : ∀ k i j, 0 ≤ mu k i j)
    (hle : ∀ k i j, mu k i j ≤ muBar k i j)
    (i : I6) :
    componentQ6 mu v i ≤ componentQ6 muBar v i := by
  unfold componentQ6
  apply Finset.sum_le_sum
  intro j hj
  apply Finset.sum_le_sum
  intro k hk
  exact mul_le_mul_of_nonneg_right
    (gammaRadius6_mono mu muBar hmu hle i j k) (abs_nonneg _)

/-- Finite-sum monotonicity for the nonnegative coefficient carried by a
weighted-power consumer. -/
theorem weighted_sum_mono6
    (a x y : Vector6)
    (ha : ∀ i, 0 ≤ a i)
    (hxy : ∀ i, x i ≤ y i) :
    ∑ i, a i * x i ≤ ∑ i, a i * y i := by
  apply Finset.sum_le_sum
  intro i hi
  exact mul_le_mul_of_nonneg_left (hxy i) (ha i)

def weightedRadiusSum6 (w v q : Vector6) : ℝ :=
  ∑ i, w i * |v i| * q i

theorem weightedRadiusSum6_mono
    (w v q qBar : Vector6)
    (hw : ∀ i, 0 ≤ w i)
    (hq : ∀ i, 0 ≤ q i)
    (hqBar : ∀ i, 0 ≤ qBar i)
    (hqqBar : ∀ i, q i ≤ qBar i) :
    weightedRadiusSum6 w v q ≤ weightedRadiusSum6 w v qBar := by
  unfold weightedRadiusSum6
  apply weighted_sum_mono6
  · intro i
    exact mul_nonneg (hw i) (abs_nonneg _)
  · intro i
    exact hqqBar i

/-! The following context carries the same-domain and velocity/weight premises
without using them to manufacture any numerical bound. -/

structure ConsumerContext6 (D : Type*) where
  point : D
  commonDomain : D → Prop
  machine_in_common : commonDomain point
  centralFD_in_common : commonDomain point
  derivativeHull_in_common : commonDomain point
  exportCenter_in_common : commonDomain point
  velocity : Vector6
  velocityPremise : Prop
  velocityPremise_ok : velocityPremise
  weight : Vector6
  weight_nonneg : ∀ i, 0 ≤ weight i

/-- Monotonicity-only consumer lift.  `hConsumer` is the existing weighted
power theorem's output with radius `q`; this theorem only enlarges its radius
to `qBar`. -/
theorem existing_consumer_lift_to_qbar6
    {D : Type*} (C : ConsumerContext6 D)
    (consumerValue : ℝ) (q qBar : Vector6)
    (hConsumer : consumerValue ≤
      weightedRadiusSum6 C.weight C.velocity q)
    (hq : ∀ i, 0 ≤ q i)
    (hqBar : ∀ i, 0 ≤ qBar i)
    (hqqBar : ∀ i, q i ≤ qBar i) :
    consumerValue ≤ weightedRadiusSum6 C.weight C.velocity qBar := by
  exact hConsumer.trans
    (weightedRadiusSum6_mono C.weight C.velocity q qBar
      C.weight_nonneg hq hqBar hqqBar)

/-- The error-bound premise is retained explicitly while the actual proof uses
only the already-composed consumer inequality. -/
theorem existing_consumer_lift_with_error_bound6
    {D : Type*} (C : ConsumerContext6 D)
    (consumerValue : ℝ) (error R qBar : Vector6)
    (hError : ∀ i, |error i| ≤ R i)
    (hConsumer : consumerValue ≤
      weightedRadiusSum6 C.weight C.velocity R)
    (hR : ∀ i, 0 ≤ R i)
    (hqBar : ∀ i, 0 ≤ qBar i)
    (hRqBar : ∀ i, R i ≤ qBar i) :
    consumerValue ≤ weightedRadiusSum6 C.weight C.velocity qBar := by
  exact existing_consumer_lift_to_qbar6 C consumerValue R qBar
    hConsumer hR hqBar hRqBar

end

end RouteBP3CentralFDHullMonotonicity

#print axioms RouteBP3CentralFDHullMonotonicity.gammaRadius6_mono
#print axioms RouteBP3CentralFDHullMonotonicity.componentQ6_mono
#print axioms RouteBP3CentralFDHullMonotonicity.weightedRadiusSum6_mono
#print axioms RouteBP3CentralFDHullMonotonicity.existing_consumer_lift_with_error_bound6
