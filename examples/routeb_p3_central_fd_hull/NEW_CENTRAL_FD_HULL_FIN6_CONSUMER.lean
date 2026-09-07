import Mathlib.Data.Real.Basic
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic

/-!
# Fin 6 derivative-first consumer for the P3 central-FD hull

This file specializes the derivative-first convention to six coordinates.  Its
inputs are already typed as `T[k,i,j]`, `R[k,i,j]`, and `mu[k,i,j]`; the prior
slot adapter is responsible for transporting source-shaped `dM[i,j,k]` data.
No numerical radius is chosen here.
-/

open scoped BigOperators

set_option autoImplicit false

namespace RouteBP3CentralFDHullFin6Consumer

noncomputable section

abbrev I6 := Fin 6
abbrev Tensor6 := I6 → I6 → I6 → ℝ
abbrev Vector6 := I6 → ℝ

/-- Derivative-first Christoffel coefficient. -/
def gamma6 (T : Tensor6) (i j k : I6) : ℝ :=
  (T k i j + T j i k - T i j k) / 2

/-- Derivative-first velocity-quadratic consumer. -/
def force6 (T : Tensor6) (v : Vector6) (i : I6) : ℝ :=
  ∑ j, ∑ k, gamma6 T i j k * v j * v k

/-- Radius for one Christoffel coefficient induced by a derivative-first
remainder radius. -/
def gammaRadius6 (mu : Tensor6) (i j k : I6) : ℝ :=
  (mu k i j + mu j i k + mu i j k) / 2

/-- Explicit velocity-quadratic component bound consumed by a downstream
force/residual theorem. -/
def componentBound6 (mu : Tensor6) (v : Vector6) (i : I6) : ℝ :=
  ∑ j, ∑ k, gammaRadius6 mu i j k * |v j * v k|

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

/-- The six-coordinate aggregate power error.  This is a typed consumer of
the component bound and does not select a velocity box or a numerical gain. -/
theorem fd_power_error6
    (T R mu : Tensor6) (v : Vector6)
    (hmu : ∀ k i j, 0 ≤ mu k i j)
    (hR : ∀ k i j, |R k i j| ≤ mu k i j) :
    |∑ i, v i * (force6 (fun k i j => T k i j + R k i j) v i -
      force6 T v i)| ≤
      ∑ i, |v i| * componentBound6 mu v i := by
  calc
    |∑ i, v i * (force6 (fun k i j => T k i j + R k i j) v i -
      force6 T v i)| ≤
        ∑ i, |v i * (force6 (fun k i j => T k i j + R k i j) v i -
          force6 T v i)| := by
      simpa using
        (Finset.abs_sum_le_sum_abs
          (fun i => v i * (force6 (fun k i j => T k i j + R k i j) v i -
            force6 T v i)) Finset.univ)
    _ = ∑ i, |v i| * |
        force6 (fun k i j => T k i j + R k i j) v i - force6 T v i| := by
      apply Finset.sum_congr rfl
      intro i hi
      simp [abs_mul]
    _ ≤ ∑ i, |v i| * componentBound6 mu v i := by
      apply Finset.sum_le_sum
      intro i hi
      exact mul_le_mul_of_nonneg_left
        (fd_component_bound6 T R mu v i hmu hR)
        (abs_nonneg _)

end

end RouteBP3CentralFDHullFin6Consumer

#print axioms RouteBP3CentralFDHullFin6Consumer.gamma6_abs_le_radius6
#print axioms RouteBP3CentralFDHullFin6Consumer.fd_component_bound6
#print axioms RouteBP3CentralFDHullFin6Consumer.fd_power_error6
