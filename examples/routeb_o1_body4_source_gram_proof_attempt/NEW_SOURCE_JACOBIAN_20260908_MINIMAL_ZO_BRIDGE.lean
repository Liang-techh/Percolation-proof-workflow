import NEW_SOURCE_JACOBIAN_20260908_FRAME_HANDOFF

set_option autoImplicit false

namespace RouteBO1Body4MinimalZOBridge20260908

noncomputable section

open RouteBO1PerBodyExactSource
open RouteBO1Body4SourceGramTargets
open RouteBBodySemanticCore
open RouteBSourceContractAdapter
open RouteBSourceContractIndexAdapter
open RouteBFrameSlotAccessor
open RouteBO1Body4SourceJacobianPorts20260908

/-!
CONDITIONAL_SOURCE_JACOBIAN_SKELETON_UNCOMPILED; admission=pending.
Imports FRAME_HANDOFF and PORTS as uncompiled candidates, not evidence.
This local interface reduces the consumed frame fields to Z/O. It neither
changes nor inhabits the original Body4PrefixColumnsTarget (which also has X/Y).
No inhabitant of PrefixZO or Body4Slot4TranslationTarget is supplied here.
-/

/-- 24 scalar equations: four parent slots, three rows, two columns.
These concern the actual imported frame accessor, not substitute geometry. -/
structure PrefixZO : Prop where
  axis : ∀ (q : Q6) (s : Fin 4),
    RouteBFrameOriginAxis.zAxis (routeBFrameSlot q (prefixSlot s)) = prefixZ q s
  origin : ∀ (q : Q6) (s : Fin 4),
    RouteBFrameOriginAxis.origin (routeBFrameSlot q (prefixSlot s)) = prefixO q s

/-- One-way projection only; no recovery of X/Y is asserted. -/
theorem zo_of_full_prefix (h : Body4PrefixColumnsTarget) : PrefixZO := by
  constructor
  · intro q s
    funext a
    exact (h q s a).2.2.1
  · intro q s
    funext a
    exact (h q s a).2.2.2

theorem source_axes_of_zo (h : PrefixZO) : Body4SourceAxesTarget := by
  intro q j
  change (sourceContract q).axes (activeJoint j) = prefixZ q j
  rw [source_parent_axis_slot, parent_slot]
  exact h.axis q j

theorem source_origins_of_zo (h : PrefixZO) (q : Q6) (s : Fin 4) :
    (sourceContract q).origins (prefixSlot s) = prefixO q s := by
  calc
    _ = RouteBFrameOriginAxis.origin (routeBFrameSlot q (prefixSlot s)) := by
      simpa only [parent_slot] using source_prev_origin_slot q (activeJoint s)
    _ = prefixO q s := h.origin q s

/-- Body index 3 has COM endpoints 3 and 4, not 2 and 3. -/
theorem source_com_of_zo
    (h : PrefixZO) (hT : Body4Slot4TranslationTarget) : Body4ComTarget := by
  intro q
  change bodyCom (sourceContract q).origins (3 : Body) = _
  rw [source_body4_com_uses_slots_3_4]
  funext a
  change (RouteBFrameOriginAxis.origin (routeBFrameSlot q 3) a +
    RouteBFrameOriginAxis.origin (routeBFrameSlot q 4) a) / 2 = _
  rw [hT q a, h.origin q 3, h.axis q 3]
  fin_cases a <;> simp [prefixO, prefixZ, vec, aa, pp, e] <;> ring

theorem source_displacements_of_zo
    (h : PrefixZO) (hT : Body4Slot4TranslationTarget) :
    Body4DisplacementsTarget := by
  intro q j a
  change bodyCom (sourceContract q).origins body4 a -
    (sourceContract q).origins (prefixSlot j) a = displacement q j a
  rw [source_com_of_zo h hT q, source_origins_of_zo h q j]
  fin_cases j <;> fin_cases a <;>
    simp [displacement, prefixO, vec, aa, pp, qq] <;> ring

theorem source_geometry_of_zo
    (h : PrefixZO) (hT : Body4Slot4TranslationTarget) : SourceGeometry :=
  ⟨source_axes_of_zo h, source_displacements_of_zo h hT⟩

/-- Original target types, still conditional on actual source frame geometry. -/
theorem jacobians_of_zo
    (h : PrefixZO) (hT : Body4Slot4TranslationTarget) :
    Body4JvTarget ∧ Body4JwTarget :=
  jacobians_of_source_geometry (source_geometry_of_zo h hT)

/-- Angular binding needs no origin or translation premise. -/
theorem jw_of_axis_columns
    (hZ : ∀ (q : Q6) (s : Fin 4),
      RouteBFrameOriginAxis.zAxis (routeBFrameSlot q (prefixSlot s)) =
        prefixZ q s) : Body4JwTarget := by
  apply jw_of_source_axes
  intro q j
  change (sourceContract q).axes (activeJoint j) = prefixZ q j
  rw [source_parent_axis_slot, parent_slot]
  exact hZ q j

/-- Index 3 is ACTIVE. Translation gives displacement = (19/200)*Z3,
so its linear column vanishes by parallel cross, not by the inactive guard.
No PrefixZO premise is required for this zero linear column. -/
theorem joint3_linear_of_translation_only
    (hT : Body4Slot4TranslationTarget) (q : Q6) (a : Axis) :
    bodyJv (sourceContract q).origins (sourceContract q).axes
      (3 : Body) a (3 : Joint) = 0 :=
  RouteBO1Body4FrameHandoff20260908.joint3_linear_of_translation hT q a

theorem joint3_angular_of_zo (h : PrefixZO) (q : Q6) (a : Axis) :
    bodyJw (sourceContract q).axes (3 : Body) a (3 : Joint) =
      vec q (Real.sin (phi q)) 0 (Real.cos (phi q)) a := by
  exact jw_of_axis_columns h.axis q a 3

/-- Exactly joints 4 and 5 are inactive for body index 3. -/
theorem inactive_index_iff (j : Joint) :
    3 < j.val ↔ j = (4 : Joint) ∨ j = (5 : Joint) := by
  fin_cases j <;> norm_num

theorem inactive_source_columns : Body4InactiveTarget := inactive

/-- Dot preservation is Euclidean, NOT Isometry for the default Pi/sup norm.
The oriented cross identity is separate; dot preservation alone is insufficient.
Target vcol/wcol already live in world coordinates and must not be lifted twice. -/
theorem lift_transport (q : Q6) (u v : V3) :
    dot (lift q u) (lift q v) = dot u v ∧
    cross3 (lift q u) (lift q v) = lift q (cross3 u v) :=
  ⟨lift_dot_isometry q u v, lift_cross q u v⟩

-- No sourceBodyMass, Gram-table, expected-entry, Fourier or trace endpoint.
-- Future checks only: none of these commands has been executed in this task.
#print axioms zo_of_full_prefix
#print axioms source_geometry_of_zo
#print axioms jacobians_of_zo
#print axioms jw_of_axis_columns
#print axioms joint3_linear_of_translation_only
#print axioms joint3_angular_of_zo
#print axioms inactive_index_iff
#print axioms inactive_source_columns
#print axioms lift_transport

end
end RouteBO1Body4MinimalZOBridge20260908
