import Mathlib.Data.Real.Basic
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic

/-!
# Fin 6 weighted power seam for the central-FD derivative hull

This sidecar keeps the derivative-first order `T[k,i,j]` explicit while
connecting four telescoped tensor remainders to componentwise and weighted
cubic power consumers.  It contains no numerical radius or source instance.
-/

open scoped BigOperators

set_option autoImplicit false

namespace RouteBP3CentralFDHullPowerSeam

noncomputable section

abbrev I6 := Fin 6
abbrev Tensor6 := I6 → I6 → I6 → ℝ
abbrev Vector6 := I6 → ℝ
abbrev Radius6 := Tensor6

/-- Derivative-first Christoffel coefficient. -/
def gamma6 (T : Tensor6) (i j k : I6) : ℝ :=
  (T k i j + T j i k - T i j k) / 2

/-- Velocity-quadratic force in the derivative-first convention. -/
def force6 (T : Tensor6) (v : Vector6) (i : I6) : ℝ :=
  ∑ j, ∑ k, gamma6 T i j k * v j * v k

/-- Three-index radius after the Christoffel combination. -/
def gammaRadius6 (mu : Radius6) (i j k : I6) : ℝ :=
  (mu k i j + mu j i k + mu i j k) / 2

/-- Per-component velocity-quadratic radius. -/
def componentBound6 (mu : Radius6) (v : Vector6) (i : I6) : ℝ :=
  ∑ j, ∑ k, gammaRadius6 mu i j k * |v j * v k|

/-- Four remainder layers, kept as a pointwise tensor sum. -/
def tensorAdd4 (R₀ R₁ R₂ R₃ : Tensor6) : Tensor6 :=
  fun k i j => R₀ k i j + R₁ k i j + R₂ k i j + R₃ k i j

def radiusAdd4 (mu₀ mu₁ mu₂ mu₃ : Radius6) : Radius6 :=
  fun k i j => mu₀ k i j + mu₁ k i j + mu₂ k i j + mu₃ k i j

/-- Exact four-step telescoping in derivative-first tensor order. -/
theorem four_term_telescoping6
    (X₀ X₁ X₂ X₃ X₄ : Tensor6) :
    (fun k i j => X₀ k i j - X₄ k i j) =
      tensorAdd4
        (fun k i j => X₀ k i j - X₁ k i j)
        (fun k i j => X₁ k i j - X₂ k i j)
        (fun k i j => X₂ k i j - X₃ k i j)
        (fun k i j => X₃ k i j - X₄ k i j) := by
  funext k i j
  unfold tensorAdd4
  ring

theorem nested_abs_sum_bound6 (f : I6 → I6 → ℝ) :
    |∑ j, ∑ k, f j k| ≤ ∑ j, ∑ k, |f j k| := by
  calc
    |∑ j, ∑ k, f j k| ≤ ∑ j, |∑ k, f j k| := by
      simpa using
        (Finset.abs_sum_le_sum_abs (fun j => ∑ k, f j k) Finset.univ)
    _ ≤ ∑ j, ∑ k, |f j k| := by
      apply Finset.sum_le_sum
      intro j hj
      simpa using
        (Finset.abs_sum_le_sum_abs (fun k => f j k) Finset.univ)

theorem gamma6_abs_le_radius6
    (R mu : Tensor6)
    (hmu : ∀ k i j, 0 ≤ mu k i j)
    (hR : ∀ k i j, |R k i j| ≤ mu k i j)
    (i j k : I6) :
    |gamma6 R i j k| ≤ gammaRadius6 mu i j k := by
  have hnum :
      |R k i j + R j i k - R i j k| ≤
        mu k i j + mu j i k + mu i j k := by
    calc
      |R k i j + R j i k - R i j k| ≤
          |R k i j + R j i k| + |R i j k| := by
        simpa [sub_eq_add_neg, abs_neg] using
          (abs_add_le (R k i j + R j i k) (-R i j k))
      _ ≤ (|R k i j| + |R j i k|) + |R i j k| := by
        gcongr
        exact abs_add_le _ _
      _ ≤ mu k i j + mu j i k + mu i j k := by
        gcongr
        · exact hR k i j
        · exact hR j i k
        · exact hR i j k
  unfold gamma6 gammaRadius6
  rw [abs_div]
  norm_num
  exact div_le_div_of_nonneg_right hnum (by norm_num)

theorem fd_component_bound6
    (T R mu : Tensor6) (v : Vector6) (i : I6)
    (hmu : ∀ k i j, 0 ≤ mu k i j)
    (hR : ∀ k i j, |R k i j| ≤ mu k i j) :
    |force6 (fun k i j => T k i j + R k i j) v i - force6 T v i| ≤
      componentBound6 mu v i := by
  have hGamma : ∀ j k, |gamma6 R i j k| ≤ gammaRadius6 mu i j k := by
    intro j k
    exact gamma6_abs_le_radius6 mu R hmu hR i j k
  have hsplit :
      force6 (fun k i j => T k i j + R k i j) v i =
        force6 T v i + force6 R v i := by
    unfold force6 gamma6
    simp only [Pi.add_apply]
    apply Finset.sum_congr rfl
    intro j hj
    apply Finset.sum_congr rfl
    intro k hk
    ring
  calc
    |force6 (fun k i j => T k i j + R k i j) v i - force6 T v i| =
        |force6 R v i| := by
      rw [hsplit]
      congr 1
      ring
    _ ≤ ∑ j, ∑ k, |gamma6 R i j k * v j * v k| := by
      exact nested_abs_sum_bound6
        (fun j k => gamma6 R i j k * v j * v k)
    _ = ∑ j, ∑ k, |gamma6 R i j k| * |v j * v k| := by
      apply Finset.sum_congr rfl
      intro j hj
      apply Finset.sum_congr rfl
      intro k hk
      simp [abs_mul, mul_assoc]
    _ ≤ componentBound6 mu v i := by
      unfold componentBound6
      apply Finset.sum_le_sum
      intro j hj
      apply Finset.sum_le_sum
      intro k hk
      exact mul_le_mul_of_nonneg_right (hGamma j k) (abs_nonneg _)

/-! ## Zero and diagonal bookkeeping -/

theorem zero_velocity_term6
    (mu : Radius6) (v : Vector6) (i j k : I6)
    (hzero : v j = 0 ∨ v k = 0) :
    gammaRadius6 mu i j k * |v j * v k| = 0 := by
  rcases hzero with hj | hk
  · simp [hj]
  · simp [hk]

theorem zero_radius_term6
    (mu : Radius6) (v : Vector6) (i j k : I6)
    (h₁ : mu k i j = 0) (h₂ : mu j i k = 0) (h₃ : mu i j k = 0) :
    gammaRadius6 mu i j k * |v j * v k| = 0 := by
  simp [gammaRadius6, h₁, h₂, h₃]

theorem diagonal_velocity_term6
    (mu : Radius6) (v : Vector6) (i j : I6) :
    gammaRadius6 mu i j j * |v j * v j| =
      gammaRadius6 mu i j j * |v j| ^ 2 := by
  simp [abs_mul, pow_two]

/-! ## Weighted power summation -/

def weightedPower6 (w v e : Vector6) : ℝ :=
  ∑ i, w i * v i * e i

def weightedPowerBound6 (w : Vector6) (mu : Radius6) (v : Vector6) : ℝ :=
  ∑ i, w i * |v i| * componentBound6 mu v i

theorem weighted_power_error6
    (w : Vector6) (mu : Radius6) (v e : Vector6)
    (hw : ∀ i, 0 ≤ w i)
    (he : ∀ i, |e i| ≤ componentBound6 mu v i) :
    |weightedPower6 w v e| ≤ weightedPowerBound6 w mu v := by
  unfold weightedPower6 weightedPowerBound6
  calc
    |∑ i, w i * v i * e i| ≤
        ∑ i, |w i * v i * e i| := by
      simpa using
        (Finset.abs_sum_le_sum_abs
          (fun i => w i * v i * e i) Finset.univ)
    _ = ∑ i, w i * |v i| * |e i| := by
      apply Finset.sum_congr rfl
      intro i hi
      rw [abs_mul, abs_mul, abs_of_nonneg (hw i)]
    _ ≤ ∑ i, w i * |v i| * componentBound6 mu v i := by
      apply Finset.sum_le_sum
      intro i hi
      exact mul_le_mul_of_nonneg_left
        (he i) (mul_nonneg (hw i) (abs_nonneg _))

theorem four_term_remainder_bound6
    (R₀ R₁ R₂ R₃ mu₀ mu₁ mu₂ mu₃ : Tensor6)
    (h₀ : ∀ k i j, |R₀ k i j| ≤ mu₀ k i j)
    (h₁ : ∀ k i j, |R₁ k i j| ≤ mu₁ k i j)
    (h₂ : ∀ k i j, |R₂ k i j| ≤ mu₂ k i j)
    (h₃ : ∀ k i j, |R₃ k i j| ≤ mu₃ k i j)
    (k i j : I6) :
    |tensorAdd4 R₀ R₁ R₂ R₃ k i j| ≤
      radiusAdd4 mu₀ mu₁ mu₂ mu₃ k i j := by
  unfold tensorAdd4 radiusAdd4
  calc
    |R₀ k i j + R₁ k i j + R₂ k i j + R₃ k i j| ≤
        |R₀ k i j| + |R₁ k i j| + |R₂ k i j| + |R₃ k i j| := by
      calc
        |R₀ k i j + R₁ k i j + R₂ k i j + R₃ k i j| ≤
            |R₀ k i j + R₁ k i j + R₂ k i j| + |R₃ k i j| :=
          abs_add_le _ _
        _ ≤ (|R₀ k i j + R₁ k i j| + |R₂ k i j|) + |R₃ k i j| := by
          gcongr
          exact abs_add_le _ _
        _ ≤ (|R₀ k i j| + |R₁ k i j|) + |R₂ k i j| + |R₃ k i j| := by
          gcongr
          exact abs_add_le _ _
    _ ≤ mu₀ k i j + mu₁ k i j + mu₂ k i j + mu₃ k i j := by
      gcongr
      · exact h₀ k i j
      · exact h₁ k i j
      · exact h₂ k i j
      · exact h₃ k i j

theorem four_term_to_weighted_power6
    (T R₀ R₁ R₂ R₃ mu₀ mu₁ mu₂ mu₃ : Tensor6)
    (w v : Vector6)
    (hw : ∀ i, 0 ≤ w i)
    (hmu : ∀ k i j, 0 ≤ radiusAdd4 mu₀ mu₁ mu₂ mu₃ k i j)
    (h₀ : ∀ k i j, |R₀ k i j| ≤ mu₀ k i j)
    (h₁ : ∀ k i j, |R₁ k i j| ≤ mu₁ k i j)
    (h₂ : ∀ k i j, |R₂ k i j| ≤ mu₂ k i j)
    (h₃ : ∀ k i j, |R₃ k i j| ≤ mu₃ k i j) :
    |∑ i, w i * v i *
        (force6 (fun k i j => T k i j + tensorAdd4 R₀ R₁ R₂ R₃ k i j) v i -
          force6 T v i)| ≤
      ∑ i, w i * |v i| *
        componentBound6 (radiusAdd4 mu₀ mu₁ mu₂ mu₃) v i := by
  let R : Tensor6 := tensorAdd4 R₀ R₁ R₂ R₃
  let mu : Radius6 := radiusAdd4 mu₀ mu₁ mu₂ mu₃
  have hR : ∀ k i j, |R k i j| ≤ mu k i j := by
    intro k i j
    exact four_term_remainder_bound6 R₀ R₁ R₂ R₃ mu₀ mu₁ mu₂ mu₃
      h₀ h₁ h₂ h₃ k i j
  have hComponent : ∀ i,
      |force6 (fun k i j => T k i j + R k i j) v i - force6 T v i| ≤
        componentBound6 mu v i := by
    intro i
    exact fd_component_bound6 T R mu v i hmu hR
  have hWeighted := weighted_power_error6
    w mu v (fun i => force6 (fun k i j => T k i j + R k i j) v i - force6 T v i)
    hw hComponent
  simpa [R, mu, weightedPower6, weightedPowerBound6] using hWeighted

end

end RouteBP3CentralFDHullPowerSeam

#print axioms RouteBP3CentralFDHullPowerSeam.zero_velocity_term6
#print axioms RouteBP3CentralFDHullPowerSeam.diagonal_velocity_term6
#print axioms RouteBP3CentralFDHullPowerSeam.four_term_telescoping6
#print axioms RouteBP3CentralFDHullPowerSeam.weighted_power_error6
#print axioms RouteBP3CentralFDHullPowerSeam.four_term_remainder_bound6
#print axioms RouteBP3CentralFDHullPowerSeam.four_term_to_weighted_power6
