import Mathlib.Data.Real.Basic
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic

/-!
# P3 scalar-cap parameter monotonicity

The load vector is abstracted as an already assembled nonnegative coefficient.
This leaf proves only monotonicity of the scalar cap budget and its strict form;
it does not repeat the component-radius or force constructions.
-/

open scoped BigOperators

set_option autoImplicit false

namespace RouteBP3CentralFDHullCapMonotonicity

noncomputable section

abbrev I6 := Fin 6
abbrev Load6 := I6 → ℝ

def totalLoad6 (load : Load6) : ℝ :=
  ∑ i, load i

def scalarCapLoad6 (load : Load6) (cap : ℝ) : ℝ :=
  cap * totalLoad6 load

theorem totalLoad6_nonneg
    (load : Load6) (hload : ∀ i, 0 ≤ load i) :
    0 ≤ totalLoad6 load := by
  unfold totalLoad6
  exact Finset.sum_nonneg (fun i hi => hload i)

theorem scalarCapLoad6_mono
    (load : Load6) (cap₁ cap₂ : ℝ)
    (hload : ∀ i, 0 ≤ load i)
    (hcap : cap₁ ≤ cap₂) :
    scalarCapLoad6 load cap₁ ≤ scalarCapLoad6 load cap₂ := by
  unfold scalarCapLoad6
  exact mul_le_mul_of_nonneg_right hcap
    (totalLoad6_nonneg load hload)

theorem scalarCapLoad6_gap_identity
    (load : Load6) (cap₁ cap₂ : ℝ) :
    scalarCapLoad6 load cap₂ - scalarCapLoad6 load cap₁ =
      (cap₂ - cap₁) * totalLoad6 load := by
  unfold scalarCapLoad6
  ring

theorem scalarCapLoad6_strict_mono
    (load : Load6) (cap₁ cap₂ : ℝ)
    (hTotal : 0 < totalLoad6 load)
    (hcap : cap₁ < cap₂) :
    scalarCapLoad6 load cap₁ < scalarCapLoad6 load cap₂ := by
  have hgap : 0 < cap₂ - cap₁ := sub_pos.mpr hcap
  have hprod : 0 < (cap₂ - cap₁) * totalLoad6 load :=
    mul_pos hgap hTotal
  rw [← sub_pos]
  rw [scalarCapLoad6_gap_identity load cap₁ cap₂]
  exact hprod

end

end RouteBP3CentralFDHullCapMonotonicity

#print axioms RouteBP3CentralFDHullCapMonotonicity.totalLoad6_nonneg
#print axioms RouteBP3CentralFDHullCapMonotonicity.scalarCapLoad6_mono
#print axioms RouteBP3CentralFDHullCapMonotonicity.scalarCapLoad6_strict_mono
