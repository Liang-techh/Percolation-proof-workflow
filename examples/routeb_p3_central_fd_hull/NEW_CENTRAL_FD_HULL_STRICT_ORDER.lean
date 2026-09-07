import Mathlib.Data.Real.Basic
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic

/-!
# P3 strict weighted-cap order bridge

This leaf proves strictness from one strict component gap carrying positive
load.  It consumes an already assembled nonnegative load and an existing
capMax upper-bound premise; it does not rebuild the non-strict order or capMax
construction.
-/

open scoped BigOperators

set_option autoImplicit false

namespace RouteBP3CentralFDHullStrictOrder

noncomputable section

abbrev I6 := Fin 6
abbrev Vector6 := I6 → ℝ
abbrev Load6 := Vector6

def weightedLoad6 (load q : Vector6) : ℝ :=
  ∑ i, load i * q i

def capLoad6 (load qCap : Vector6) : ℝ :=
  ∑ i, load i * qCap i

def capMaxLoad6 (load : Load6) (capMax : ℝ) : ℝ :=
  capMax * ∑ i, load i

theorem strict_component_gap_sum6
    (load q qCap : Vector6) (jStar : I6)
    (hload : ∀ i, 0 ≤ load i)
    (hgap : q jStar < qCap jStar)
    (hpositive : 0 < load jStar)
    (horder : ∀ i, q i ≤ qCap i) :
    weightedLoad6 load q < weightedLoad6 load qCap := by
  let f : I6 → ℝ := fun i => load i * (qCap i - q i)
  have hf_nonneg : ∀ i, 0 ≤ f i := by
    intro i
    dsimp [f]
    exact mul_nonneg (hload i) (sub_nonneg.mpr (horder i))
  have hf_pos : 0 < f jStar := by
    dsimp [f]
    exact mul_pos hpositive (sub_pos.mpr hgap)
  have hrest : 0 ≤ ∑ i in Finset.univ.erase jStar, f i := by
    exact Finset.sum_nonneg (fun i hi => hf_nonneg i)
  have hsplit :
      (∑ i, f i) = f jStar + ∑ i in Finset.univ.erase jStar, f i := by
    simpa [add_comm] using
      (Finset.sum_erase_add f (Finset.mem_univ jStar)).symm
  have hsum_pos : 0 < ∑ i, f i := by
    rw [hsplit]
    linarith
  unfold weightedLoad6 at *
  dsimp [f] at hsum_pos
  nlinarith

/-! The context keeps the same-point and assembled-load premises visible. -/

structure StrictOrderContext6 (D : Type*) where
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
  load : Load6
  load_nonneg : ∀ i, 0 ≤ load i
  assembledLoad : Vector6 → Vector6 → Load6
  squaredVelocity : Vector6
  load_eq : ∀ i,
    load i = assembledLoad weight squaredVelocity i
  assembledLoad_eq : ∀ w s i,
    assembledLoad w s i = w i * s i

theorem strict_order_in_context6
    {D : Type*} (C : StrictOrderContext6 D)
    (q qCap : Vector6) (jStar : I6)
    (hgap : q jStar < qCap jStar)
    (hpositive : 0 < C.load jStar)
    (horder : ∀ i, q i ≤ qCap i) :
    weightedLoad6 C.load q < weightedLoad6 C.load qCap := by
  exact strict_component_gap_sum6 C.load q qCap jStar C.load_nonneg
    hgap hpositive horder

/-- Strict capMax consumer.  The non-strict cap-load-to-capMax comparison is
consumed as an explicit upstream premise. -/
theorem capMax_consumer_strict6
    {D : Type*} (C : StrictOrderContext6 D)
    (consumerValue : ℝ) (q qCap : Vector6) (capMax : ℝ) (jStar : I6)
    (hConsumer : consumerValue ≤ weightedLoad6 C.load q)
    (hgap : q jStar < qCap jStar)
    (hpositive : 0 < C.load jStar)
    (horder : ∀ i, q i ≤ qCap i)
    (hCapMax : capLoad6 C.load qCap ≤ capMaxLoad6 C.load capMax) :
    consumerValue < capMaxLoad6 C.load capMax := by
  have hStrict := strict_order_in_context6 C q qCap jStar
    hgap hpositive horder
  have hCap : weightedLoad6 C.load qCap = capLoad6 C.load qCap := by
    rfl
  have hStrictCap : weightedLoad6 C.load q < capLoad6 C.load qCap := by
    simpa [hCap] using hStrict
  exact lt_of_le_of_lt hConsumer (lt_of_lt_of_le hStrictCap hCapMax)

end

end RouteBP3CentralFDHullStrictOrder

#print axioms RouteBP3CentralFDHullStrictOrder.strict_component_gap_sum6
#print axioms RouteBP3CentralFDHullStrictOrder.strict_order_in_context6
#print axioms RouteBP3CentralFDHullStrictOrder.capMax_consumer_strict6
