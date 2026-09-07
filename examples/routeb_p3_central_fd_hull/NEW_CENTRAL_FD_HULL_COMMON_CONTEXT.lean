import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
# P3 common-domain context and premise reuse

This sidecar is a predicate-transport seam.  Four named layers are required to
use one common point; a common-domain proof is transported to their predicate
intersection.  Velocity, weight, and an already established consumer bound
are then packaged without redoing any force, radius, or power estimate.
-/

set_option autoImplicit false

namespace RouteBP3CentralFDHullCommonContext

noncomputable section

abbrev I6 := Fin 6
abbrev Vector6 := I6 → ℝ

inductive Layer6 : Type
  | machineLift
  | centralFD
  | derivativeHull
  | exportCenter

def layerIntersection6 {X : Type*}
    (layerDomain : Layer6 → X → Prop) (x : X) : Prop :=
  ∀ layer, layerDomain layer x

structure CommonDomainContext6 (X : Type*) where
  point : X
  commonDomain : X → Prop
  layerDomain : Layer6 → X → Prop
  common_to_layer : ∀ layer x, commonDomain x → layerDomain layer x
  point_in_common : commonDomain point

theorem common_to_layer_intersection6
    {X : Type*} (C : CommonDomainContext6 X)
    (x : X) (hx : C.commonDomain x) :
    layerIntersection6 C.layerDomain x := by
  intro layer
  exact C.common_to_layer layer x hx

theorem point_in_layer_intersection6
    {X : Type*} (C : CommonDomainContext6 X) :
    layerIntersection6 C.layerDomain C.point :=
  common_to_layer_intersection6 C C.point C.point_in_common

theorem layer_intersection_transport6
    {X : Type*} (C : CommonDomainContext6 X)
    (x y : X) (hxy : x = y)
    (hx : layerIntersection6 C.layerDomain x) :
    layerIntersection6 C.layerDomain y := by
  simpa [hxy] using hx

structure VelocityWeightPremises6 where
  velocity : Vector6
  velocityPremise : Prop
  velocityPremise_ok : velocityPremise
  weight : Vector6
  weight_nonneg : ∀ i, 0 ≤ weight i

structure ExistingWeightedConsumerBound6 where
  consumerValue : ℝ
  consumerRadiusBudget : ℝ
  consumer_bound : consumerValue ≤ consumerRadiusBudget

/-- A composed record carrying exactly the premises needed at the consumer
boundary. The consumer bound is abstract so this file does not duplicate its
weighted-power proof. -/
structure ComposedConsumerContext6 (X : Type*) where
  domain : CommonDomainContext6 X
  all_layers_at_point : layerIntersection6 domain.layerDomain domain.point
  velocityWeight : VelocityWeightPremises6
  existingConsumer : ExistingWeightedConsumerBound6

theorem compose_existing_consumer_context6
    {X : Type*}
    (domain : CommonDomainContext6 X)
    (velocityWeight : VelocityWeightPremises6)
    (existingConsumer : ExistingWeightedConsumerBound6) :
    ComposedConsumerContext6 X :=
  { domain := domain
    all_layers_at_point := point_in_layer_intersection6 domain
    velocityWeight := velocityWeight
    existingConsumer := existingConsumer }

theorem reuse_common_and_velocity_premises6
    {X : Type*} (C : ComposedConsumerContext6 X) :
    layerIntersection6 C.domain.layerDomain C.domain.point ∧
      C.velocityWeight.velocityPremise ∧
      (∀ i, 0 ≤ C.velocityWeight.weight i) ∧
      C.existingConsumer.consumerValue ≤
        C.existingConsumer.consumerRadiusBudget := by
  exact ⟨C.all_layers_at_point,
    C.velocityWeight.velocityPremise_ok,
    C.velocityWeight.weight_nonneg,
    C.existingConsumer.consumer_bound⟩

theorem transport_consumer_context_point6
    {X : Type*} (C : ComposedConsumerContext6 X)
    (y : X) (hpoint : C.domain.point = y) :
    layerIntersection6 C.domain.layerDomain y ∧
      C.velocityWeight.velocityPremise ∧
      (∀ i, 0 ≤ C.velocityWeight.weight i) ∧
      C.existingConsumer.consumerValue ≤
        C.existingConsumer.consumerRadiusBudget := by
  have hLayers := layer_intersection_transport6 C.domain C.domain.point y
    hpoint C.all_layers_at_point
  exact ⟨hLayers,
    C.velocityWeight.velocityPremise_ok,
    C.velocityWeight.weight_nonneg,
    C.existingConsumer.consumer_bound⟩

end

end RouteBP3CentralFDHullCommonContext

#print axioms RouteBP3CentralFDHullCommonContext.common_to_layer_intersection6
#print axioms RouteBP3CentralFDHullCommonContext.point_in_layer_intersection6
#print axioms RouteBP3CentralFDHullCommonContext.compose_existing_consumer_context6
#print axioms RouteBP3CentralFDHullCommonContext.reuse_common_and_velocity_premises6
