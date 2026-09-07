import Mathlib.Data.Real.Basic
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic

/-!
# P3 family-level strict slack consumer

This sidecar consumes an upstream quantitative component-gap lower bound and an
upstream cap-load-to-capMax comparison.  It proves only their same-point
strict-slack composition; no old gap, load witness, or cap theorem is rebuilt.
-/

open scoped BigOperators

set_option autoImplicit false

namespace RouteBP3CentralFDHullFamilySlack

noncomputable section

abbrev I6 := Fin 6
abbrev Tensor6 := I6 → I6 → I6 → ℝ
abbrev Vector6 := I6 → ℝ

def weightedLoad6 (load q : Vector6) : ℝ :=
  ∑ i, load i * q i

def capLoad6 (load qCap : Vector6) : ℝ :=
  ∑ i, load i * qCap i

def capMaxLoad6 (load : Vector6) (capMax : ℝ) : ℝ :=
  capMax * ∑ i, load i

def selectedGap6
    (load q qCap : Vector6) (jStar : I6) : ℝ :=
  load jStar * (qCap jStar - q jStar)

/-! A family context is explicit about the point at which all data are used. -/

structure FamilySlackContext6 (D : Type*) where
  point : D
  commonDomain : D → Prop
  machine_in_common : commonDomain point
  centralFD_in_common : commonDomain point
  derivativeHull_in_common : commonDomain point
  exportCenter_in_common : commonDomain point
  muBar : D → Tensor6
  componentize : Tensor6 → Vector6 → Vector6
  velocity : D → Vector6
  componentRadius : D → Vector6
  component_radius_eq : ∀ x, commonDomain x →
    componentRadius x = componentize (muBar x) (velocity x)
  componentRadius_nonneg : ∀ x, commonDomain x → ∀ i,
    0 ≤ componentRadius x i
  qCap : D → Vector6
  qCap_nonneg : ∀ x, commonDomain x → ∀ i, 0 ≤ qCap x i
  velocityPremise : Prop
  velocityPremise_ok : velocityPremise
  weight : D → Vector6
  weight_nonneg : ∀ x, commonDomain x → ∀ i, 0 ≤ weight x i
  load : D → Vector6
  load_nonneg : ∀ x, commonDomain x → ∀ i, 0 ≤ load x i
  capMax : D → ℝ

theorem family_strict_slack6
    {D : Type*} (C : FamilySlackContext6 D) (jStar : I6)
    (hCommon : C.commonDomain C.point)
    (hOrder : ∀ i, C.componentRadius C.point i ≤ C.qCap C.point i)
    (hGapLower : selectedGap6 (C.load C.point)
        (C.componentRadius C.point) (C.qCap C.point) jStar ≤
      capLoad6 (C.load C.point) (C.qCap C.point) -
        weightedLoad6 (C.load C.point) (C.componentRadius C.point))
    (hGapPositive : 0 < selectedGap6 (C.load C.point)
        (C.componentRadius C.point) (C.qCap C.point) jStar)
    (hCapMax : capLoad6 (C.load C.point) (C.qCap C.point) ≤
      capMaxLoad6 (C.load C.point) (C.capMax C.point)) :
    weightedLoad6 (C.load C.point) (C.componentRadius C.point) +
        selectedGap6 (C.load C.point) (C.componentRadius C.point)
          (C.qCap C.point) jStar ≤
      capMaxLoad6 (C.load C.point) (C.capMax C.point) ∧
    weightedLoad6 (C.load C.point) (C.componentRadius C.point) <
      capMaxLoad6 (C.load C.point) (C.capMax C.point) := by
  have hGapToCap :
      weightedLoad6 (C.load C.point) (C.componentRadius C.point) +
          selectedGap6 (C.load C.point) (C.componentRadius C.point)
            (C.qCap C.point) jStar ≤
        capLoad6 (C.load C.point) (C.qCap C.point) := by
    linarith
  have hSlack := hGapToCap.trans hCapMax
  constructor
  · exact hSlack
  · linarith

theorem family_strict_slack_consumer6
    {D : Type*} (C : FamilySlackContext6 D) (consumerValue : ℝ)
    (jStar : I6) (hCommon : C.commonDomain C.point)
    (hOrder : ∀ i, C.componentRadius C.point i ≤ C.qCap C.point i)
    (hGapLower : selectedGap6 (C.load C.point)
        (C.componentRadius C.point) (C.qCap C.point) jStar ≤
      capLoad6 (C.load C.point) (C.qCap C.point) -
        weightedLoad6 (C.load C.point) (C.componentRadius C.point))
    (hGapPositive : 0 < selectedGap6 (C.load C.point)
        (C.componentRadius C.point) (C.qCap C.point) jStar)
    (hCapMax : capLoad6 (C.load C.point) (C.qCap C.point) ≤
      capMaxLoad6 (C.load C.point) (C.capMax C.point))
    (hConsumer : consumerValue ≤
      weightedLoad6 (C.load C.point) (C.componentRadius C.point)) :
    consumerValue < capMaxLoad6 (C.load C.point) (C.capMax C.point) := by
  have hStrict := family_strict_slack6 C jStar hCommon hOrder
    hGapLower hGapPositive hCapMax
  exact lt_of_le_of_lt hConsumer hStrict.2

end

end RouteBP3CentralFDHullFamilySlack

#print axioms RouteBP3CentralFDHullFamilySlack.family_strict_slack6
#print axioms RouteBP3CentralFDHullFamilySlack.family_strict_slack_consumer6
