import Mathlib.Data.Real.Basic
import Mathlib.Algebra.BigOperators.Fin

/-!
# P3 derivative-radius to downstream weighted-load payload bridge

This is a conditional typed payload constructor.  The componentization map and
the existing consumer inequality are explicit premises; no new radius or
power estimate is proved here.  The purpose is to keep one point, one
derivative radius payload, one velocity/weight pair, and the four layer-domain
memberships together at the downstream boundary.
-/

open scoped BigOperators

set_option autoImplicit false

namespace RouteBP3CentralFDHullRadiusLoadBridge

noncomputable section

abbrev I6 := Fin 6
abbrev Tensor6 := I6 → I6 → I6 → ℝ
abbrev Vector6 := I6 → ℝ

def downstreamWeightedLoad6
    (weight velocity componentRadius : Vector6) : ℝ :=
  ∑ i, weight i * |velocity i| * componentRadius i

/-! `componentize` is deliberately opaque: this leaf does not rebuild the
derivative-first Christoffel or component-radius formula. -/

structure RadiusLoadContext6 (D : Type*) where
  point : D
  commonDomain : D → Prop
  machine_in_common : commonDomain point
  centralFD_in_common : commonDomain point
  derivativeHull_in_common : commonDomain point
  exportCenter_in_common : commonDomain point
  muBar : Tensor6
  componentize : Tensor6 → Vector6 → Vector6
  velocity : Vector6
  velocityPremise : Prop
  velocityPremise_ok : velocityPremise
  componentRadius : Vector6
  component_radius_eq :
    componentRadius = componentize muBar velocity
  componentRadius_nonneg : ∀ i, 0 ≤ componentRadius i
  weight : Vector6
  weight_nonneg : ∀ i, 0 ≤ weight i
  consumerValue : ℝ
  consumer_bound :
    consumerValue ≤ downstreamWeightedLoad6 weight velocity componentRadius

structure DownstreamWeightedLoadInput6 (D : Type*) where
  point : D
  commonDomain : D → Prop
  machine_in_common : commonDomain point
  centralFD_in_common : commonDomain point
  derivativeHull_in_common : commonDomain point
  exportCenter_in_common : commonDomain point
  muBar : Tensor6
  componentRadius : Vector6
  component_radius_nonneg : ∀ i, 0 ≤ componentRadius i
  velocity : Vector6
  velocityPremise : Prop
  velocityPremise_ok : velocityPremise
  weight : Vector6
  weight_nonneg : ∀ i, 0 ≤ weight i
  consumerValue : ℝ
  weightedLoadBound :
    consumerValue ≤ downstreamWeightedLoad6 weight velocity componentRadius

theorem component_radius_transport6
    {D : Type*} (C : RadiusLoadContext6 D) :
    C.componentRadius = C.componentize C.muBar C.velocity :=
  C.component_radius_eq

/-- Constructor for the downstream payload.  All semantic facts are copied as
premises; the theorem performs no physical instantiation. -/
theorem compose_downstream_weighted_load6
    {D : Type*} (C : RadiusLoadContext6 D) :
    DownstreamWeightedLoadInput6 D :=
  { point := C.point
    commonDomain := C.commonDomain
    machine_in_common := C.machine_in_common
    centralFD_in_common := C.centralFD_in_common
    derivativeHull_in_common := C.derivativeHull_in_common
    exportCenter_in_common := C.exportCenter_in_common
    muBar := C.muBar
    componentRadius := C.componentRadius
    component_radius_nonneg := C.componentRadius_nonneg
    velocity := C.velocity
    velocityPremise := C.velocityPremise
    velocityPremise_ok := C.velocityPremise_ok
    weight := C.weight
    weight_nonneg := C.weight_nonneg
    consumerValue := C.consumerValue
    weightedLoadBound := C.consumer_bound }

theorem reuse_downstream_weighted_load_premises6
    {D : Type*} (P : DownstreamWeightedLoadInput6 D) :
    P.componentRadius = P.componentRadius ∧
      (∀ i, 0 ≤ P.componentRadius i) ∧
      P.velocityPremise ∧
      (∀ i, 0 ≤ P.weight i) ∧
      P.consumerValue ≤ downstreamWeightedLoad6 P.weight P.velocity
        P.componentRadius := by
  exact ⟨rfl, P.component_radius_nonneg,
    P.velocityPremise_ok, P.weight_nonneg, P.weightedLoadBound⟩

end

end RouteBP3CentralFDHullRadiusLoadBridge

#print axioms RouteBP3CentralFDHullRadiusLoadBridge.component_radius_transport6
#print axioms RouteBP3CentralFDHullRadiusLoadBridge.compose_downstream_weighted_load6
#print axioms RouteBP3CentralFDHullRadiusLoadBridge.reuse_downstream_weighted_load_premises6
