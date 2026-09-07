import Mathlib.Data.Real.Basic
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic

/-!
# P3 unified four-layer input for the existing Fin 6 power consumer

This is a small radius-side adapter.  It proves only the pointwise addition
and nonnegativity facts needed to pass four derivative-first remainder layers
as one `R`/`mu` pair to an existing weighted-power consumer.  The force map and
the power inequality are intentionally not repeated here.
-/

open scoped BigOperators

set_option autoImplicit false

namespace RouteBP3CentralFDHullUnifiedInput

noncomputable section

abbrev I6 := Fin 6
abbrev Tensor6 := I6 → I6 → I6 → ℝ
abbrev Vector6 := I6 → ℝ

def unifiedRemainder6
    (R₀ R₁ R₂ R₃ : Tensor6) : Tensor6 :=
  fun k i j => R₀ k i j + R₁ k i j + R₂ k i j + R₃ k i j

def unifiedMu6
    (mu₀ mu₁ mu₂ mu₃ : Tensor6) : Tensor6 :=
  fun k i j => mu₀ k i j + mu₁ k i j + mu₂ k i j + mu₃ k i j

theorem unified_mu_nonneg6
    (mu₀ mu₁ mu₂ mu₃ : Tensor6)
    (h₀ : ∀ k i j, 0 ≤ mu₀ k i j)
    (h₁ : ∀ k i j, 0 ≤ mu₁ k i j)
    (h₂ : ∀ k i j, 0 ≤ mu₂ k i j)
    (h₃ : ∀ k i j, 0 ≤ mu₃ k i j) :
    ∀ k i j, 0 ≤ unifiedMu6 mu₀ mu₁ mu₂ mu₃ k i j := by
  intro k i j
  unfold unifiedMu6
  linarith [h₀ k i j, h₁ k i j, h₂ k i j, h₃ k i j]

theorem unified_remainder_bound6
    (R₀ R₁ R₂ R₃ mu₀ mu₁ mu₂ mu₃ : Tensor6)
    (h₀ : ∀ k i j, |R₀ k i j| ≤ mu₀ k i j)
    (h₁ : ∀ k i j, |R₁ k i j| ≤ mu₁ k i j)
    (h₂ : ∀ k i j, |R₂ k i j| ≤ mu₂ k i j)
    (h₃ : ∀ k i j, |R₃ k i j| ≤ mu₃ k i j) :
    ∀ k i j,
      |unifiedRemainder6 R₀ R₁ R₂ R₃ k i j| ≤
        unifiedMu6 mu₀ mu₁ mu₂ mu₃ k i j := by
  intro k i j
  unfold unifiedRemainder6 unifiedMu6
  calc
    |R₀ k i j + R₁ k i j + R₂ k i j + R₃ k i j| ≤
        |R₀ k i j| + |R₁ k i j| + |R₂ k i j| + |R₃ k i j| := by
      calc
        |R₀ k i j + R₁ k i j + R₂ k i j + R₃ k i j| ≤
            |R₀ k i j + R₁ k i j + R₂ k i j| + |R₃ k i j| :=
          abs_add_le _ _
        _ ≤ (|R₀ k i j + R₁ k i j| + |R₂ k i j|) +
            |R₃ k i j| := by
          gcongr
          exact abs_add_le _ _
        _ ≤ (|R₀ k i j| + |R₁ k i j|) + |R₂ k i j| +
            |R₃ k i j| := by
          gcongr
          exact abs_add_le _ _
    _ ≤ mu₀ k i j + mu₁ k i j + mu₂ k i j + mu₃ k i j := by
      gcongr
      · exact h₀ k i j
      · exact h₁ k i j
      · exact h₂ k i j
      · exact h₃ k i j

/-! Common premises are carried explicitly so all four layers and the power
consumer use one declared point and one declared velocity/weight pair. -/

structure CommonPremises6 (D : Type*) where
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

/-- The exact input shape expected by the existing weighted-power consumer. -/
structure UnifiedWeightedPowerInput6 (D : Type*) where
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
  remainder : Tensor6
  radius : Tensor6
  remainder_bound : ∀ k i j, |remainder k i j| ≤ radius k i j
  radius_nonneg : ∀ k i j, 0 ≤ radius k i j

theorem build_unified_weighted_power_input6
    {D : Type*} (P : CommonPremises6 D)
    (R₀ R₁ R₂ R₃ mu₀ mu₁ mu₂ mu₃ : Tensor6)
    (hR₀ : ∀ k i j, |R₀ k i j| ≤ mu₀ k i j)
    (hR₁ : ∀ k i j, |R₁ k i j| ≤ mu₁ k i j)
    (hR₂ : ∀ k i j, |R₂ k i j| ≤ mu₂ k i j)
    (hR₃ : ∀ k i j, |R₃ k i j| ≤ mu₃ k i j)
    (hmu₀ : ∀ k i j, 0 ≤ mu₀ k i j)
    (hmu₁ : ∀ k i j, 0 ≤ mu₁ k i j)
    (hmu₂ : ∀ k i j, 0 ≤ mu₂ k i j)
    (hmu₃ : ∀ k i j, 0 ≤ mu₃ k i j) :
    UnifiedWeightedPowerInput6 D := by
  have hR : ∀ k i j,
      |unifiedRemainder6 R₀ R₁ R₂ R₃ k i j| ≤
        unifiedMu6 mu₀ mu₁ mu₂ mu₃ k i j :=
    unified_remainder_bound6 R₀ R₁ R₂ R₃ mu₀ mu₁ mu₂ mu₃
      hR₀ hR₁ hR₂ hR₃
  have hmu : ∀ k i j,
      0 ≤ unifiedMu6 mu₀ mu₁ mu₂ mu₃ k i j :=
    unified_mu_nonneg6 mu₀ mu₁ mu₂ mu₃ hmu₀ hmu₁ hmu₂ hmu₃
  exact
    { point := P.point
      commonDomain := P.commonDomain
      machine_in_common := P.machine_in_common
      centralFD_in_common := P.centralFD_in_common
      derivativeHull_in_common := P.derivativeHull_in_common
      exportCenter_in_common := P.exportCenter_in_common
      velocity := P.velocity
      velocityPremise := P.velocityPremise
      velocityPremise_ok := P.velocityPremise_ok
      weight := P.weight
      weight_nonneg := P.weight_nonneg
      remainder := unifiedRemainder6 R₀ R₁ R₂ R₃
      radius := unifiedMu6 mu₀ mu₁ mu₂ mu₃
      remainder_bound := hR
      radius_nonneg := hmu }

end

end RouteBP3CentralFDHullUnifiedInput

#print axioms RouteBP3CentralFDHullUnifiedInput.unified_mu_nonneg6
#print axioms RouteBP3CentralFDHullUnifiedInput.unified_remainder_bound6
#print axioms RouteBP3CentralFDHullUnifiedInput.build_unified_weighted_power_input6
