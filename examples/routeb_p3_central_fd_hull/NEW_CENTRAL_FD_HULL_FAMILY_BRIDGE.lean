import Mathlib.Data.Real.Basic
import Mathlib.Algebra.BigOperators.Fin

/-!
# P3 family-to-point derivative-radius/load bridge

This sidecar specializes a family of exact-real radius/load premises at one
common-domain point.  It does not repeat any radius, force, monotonicity, or
weighted-power estimate; it only prevents data evaluated at different points
from being silently combined.
-/

open scoped BigOperators

set_option autoImplicit false

namespace RouteBP3CentralFDHullFamilyBridge

noncomputable section

abbrev I6 := Fin 6
abbrev Tensor6 := I6 → I6 → I6 → ℝ
abbrev Vector6 := I6 → ℝ

def weightedLoad6
    (weight velocity componentRadius : Vector6) : ℝ :=
  ∑ i, weight i * |velocity i| * componentRadius i

structure RadiusLoadFamily6 (D : Type*) where
  commonDomain : D → Prop
  machineDomain : D → Prop
  centralFDDomain : D → Prop
  derivativeHullDomain : D → Prop
  exportCenterDomain : D → Prop
  muBar : D → Tensor6
  componentize : Tensor6 → Vector6 → Vector6
  componentRadius : D → Vector6
  velocity : D → Vector6
  weight : D → Vector6
  consumerValue : D → ℝ
  component_radius_eq : ∀ x, commonDomain x →
    componentRadius x = componentize (muBar x) (velocity x)
  component_radius_nonneg : ∀ x, commonDomain x →
    ∀ i, 0 ≤ componentRadius x i
  weight_nonneg : ∀ x, commonDomain x → ∀ i, 0 ≤ weight x i
  consumer_bound : ∀ x, commonDomain x →
    consumerValue x ≤ weightedLoad6 (weight x) (velocity x)
      (componentRadius x)

structure WeightedLoadAtPoint6 (D : Type*) where
  point : D
  commonDomain_ok : Prop
  commonDomain_proof : commonDomain_ok
  machineDomain_ok : Prop
  machineDomain_proof : machineDomain_ok
  centralFDDomain_ok : Prop
  centralFDDomain_proof : centralFDDomain_ok
  derivativeHullDomain_ok : Prop
  derivativeHullDomain_proof : derivativeHullDomain_ok
  exportCenterDomain_ok : Prop
  exportCenterDomain_proof : exportCenterDomain_ok
  muBar : Tensor6
  componentRadius : Vector6
  velocity : Vector6
  weight : Vector6
  consumerValue : ℝ
  component_radius_nonneg : ∀ i, 0 ≤ componentRadius i
  weight_nonneg : ∀ i, 0 ≤ weight i
  consumer_bound :
    consumerValue ≤ weightedLoad6 weight velocity componentRadius

theorem specialize_family_at_point6
    {D : Type*} (F : RadiusLoadFamily6 D) (x : D)
    (hCommon : F.commonDomain x)
    (hMachine : F.machineDomain x)
    (hCentralFD : F.centralFDDomain x)
    (hDerivativeHull : F.derivativeHullDomain x)
    (hExportCenter : F.exportCenterDomain x) :
    WeightedLoadAtPoint6 D :=
  { point := x
    commonDomain_ok := F.commonDomain x
    commonDomain_proof := hCommon
    machineDomain_ok := F.machineDomain x
    machineDomain_proof := hMachine
    centralFDDomain_ok := F.centralFDDomain x
    centralFDDomain_proof := hCentralFD
    derivativeHullDomain_ok := F.derivativeHullDomain x
    derivativeHullDomain_proof := hDerivativeHull
    exportCenterDomain_ok := F.exportCenterDomain x
    exportCenterDomain_proof := hExportCenter
    muBar := F.muBar x
    componentRadius := F.componentRadius x
    velocity := F.velocity x
    weight := F.weight x
    consumerValue := F.consumerValue x
    component_radius_nonneg := F.component_radius_nonneg x hCommon
    weight_nonneg := F.weight_nonneg x hCommon
    consumer_bound := F.consumer_bound x hCommon }

end

end RouteBP3CentralFDHullFamilyBridge

#print axioms RouteBP3CentralFDHullFamilyBridge.specialize_family_at_point6
