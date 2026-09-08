import NEW_SOURCE_JACOBIAN_20260908_BODY4_PORTS

set_option autoImplicit false

namespace RouteBO1Body4FrameHandoff20260908

noncomputable section

open RouteBO1PerBodyExactSource
open RouteBO1Body4SourceGramTargets
open RouteBBodySemanticCore
open RouteBSourceContractAdapter
open RouteBSourceContractIndexAdapter
open RouteBFrameSlotAccessor

/-!
CONDITIONAL_SOURCE_JACOBIAN_SKELETON_UNCOMPILED; admission=pending.
The imported PORTS is also an uncompiled candidate, not verified evidence.
Only frame geometry premises are consumed here; no Gram premise can replace them.
No inhabitant of either frame target is supplied. No source mass/trace endpoint.
-/

theorem prefix_origin (h : Body4PrefixColumnsTarget) (q : Q6) (s : Fin 4) :
    RouteBFrameOriginAxis.origin
      (routeBFrameSlot q (RouteBO1Body4SourceJacobianPorts20260908.prefixSlot s)) =
        prefixO q s := by
  funext a
  exact (h q s a).2.2.2

theorem prefix_axis (h : Body4PrefixColumnsTarget) (q : Q6) (s : Fin 4) :
    RouteBFrameOriginAxis.zAxis
      (routeBFrameSlot q (RouteBO1Body4SourceJacobianPorts20260908.prefixSlot s)) =
        prefixZ q s := by
  funext a
  exact (h q s a).2.2.1

theorem source_axes_of_prefix (h : Body4PrefixColumnsTarget) :
    Body4SourceAxesTarget := by
  intro q j
  change (sourceContract q).axes
    (RouteBO1Body4SourceJacobianPorts20260908.activeJoint j) = prefixZ q j
  rw [source_parent_axis_slot,
    RouteBO1Body4SourceJacobianPorts20260908.parent_slot]
  exact prefix_axis h q j

theorem source_com_of_frames
    (hP : Body4PrefixColumnsTarget) (hT : Body4Slot4TranslationTarget) :
    Body4ComTarget := by
  intro q
  change bodyCom (sourceContract q).origins (3 : Body) = _
  rw [source_body4_com_uses_slots_3_4]
  funext a
  change (RouteBFrameOriginAxis.origin (routeBFrameSlot q 3) a +
    RouteBFrameOriginAxis.origin (routeBFrameSlot q 4) a) / 2 = _
  rw [hT q a, prefix_origin hP q 3, prefix_axis hP q 3]
  fin_cases a <;> simp [prefixO, prefixZ, vec, aa, pp, e] <;> ring

theorem source_displacements_of_frames
    (hP : Body4PrefixColumnsTarget) (hT : Body4Slot4TranslationTarget) :
    Body4DisplacementsTarget := by
  intro q j a
  have ho : (sourceContract q).origins
      (RouteBO1Body4SourceJacobianPorts20260908.prefixSlot j) = prefixO q j := by
    calc
      _ = RouteBFrameOriginAxis.origin
          (routeBFrameSlot q
            (RouteBO1Body4SourceJacobianPorts20260908.prefixSlot j)) := by
        simpa only [RouteBO1Body4SourceJacobianPorts20260908.parent_slot] using
          source_prev_origin_slot q
            (RouteBO1Body4SourceJacobianPorts20260908.activeJoint j)
      _ = prefixO q j := prefix_origin hP q j
  change bodyCom (sourceContract q).origins body4 a -
    (sourceContract q).origins
      (RouteBO1Body4SourceJacobianPorts20260908.prefixSlot j) a = _
  rw [source_com_of_frames hP hT q, ho]
  fin_cases j <;> fin_cases a <;>
    simp [displacement, prefixO, vec, aa, pp, qq] <;> ring

theorem geometry_of_frames
    (hP : Body4PrefixColumnsTarget) (hT : Body4Slot4TranslationTarget) :
    RouteBO1Body4SourceJacobianPorts20260908.SourceGeometry :=
  ⟨source_axes_of_prefix hP, source_displacements_of_frames hP hT⟩

theorem jacobians_of_frames
    (hP : Body4PrefixColumnsTarget) (hT : Body4Slot4TranslationTarget) :
    Body4JvTarget ∧ Body4JwTarget :=
  RouteBO1Body4SourceJacobianPorts20260908.jacobians_of_source_geometry
    (geometry_of_frames hP hT)

/-- Stronger dependency boundary for the active joint 3: translation alone
suffices for Jv=0. No prefix-coordinate formula or isometry is needed here.
COM uses slots 3,4; the active axis and parent origin both use slot 3. -/
theorem joint3_linear_of_translation (hT : Body4Slot4TranslationTarget)
    (q : Q6) (a : Axis) :
    bodyJv (sourceContract q).origins (sourceContract q).axes
      (3 : Body) a (3 : Joint) = 0 := by
  have hd : (fun k =>
      midpoint (RouteBFrameOriginAxis.origin (routeBFrameSlot q 3))
        (RouteBFrameOriginAxis.origin (routeBFrameSlot q 4)) k -
      RouteBFrameOriginAxis.origin (routeBFrameSlot q 3) k) =
      (fun k => e * RouteBFrameOriginAxis.zAxis (routeBFrameSlot q 3) k) := by
    funext k
    dsimp only [midpoint]
    rw [hT q k]
    dsimp only [e]
    ring
  calc
    _ = cross3 (RouteBFrameOriginAxis.zAxis (routeBFrameSlot q 3))
        (fun k =>
          midpoint (RouteBFrameOriginAxis.origin (routeBFrameSlot q 3))
            (RouteBFrameOriginAxis.origin (routeBFrameSlot q 4)) k -
          RouteBFrameOriginAxis.origin (routeBFrameSlot q 3) k) a :=
      source_body4_joint4_Jv_uses_parent_slot_3 q a
    _ = 0 := by
      rw [hd, RouteBO1Body4SourceJacobianPorts20260908.cross_parallel]
      rfl

theorem joint3_angular_of_prefix (hP : Body4PrefixColumnsTarget)
    (q : Q6) (a : Axis) :
    bodyJw (sourceContract q).axes (3 : Body) a (3 : Joint) =
      vec q (Real.sin (phi q)) 0 (Real.cos (phi q)) a := by
  calc
    _ = RouteBFrameOriginAxis.zAxis (routeBFrameSlot q 3) a :=
      source_body4_joint4_Jw_uses_parent_slot_3 q a
    _ = _ := congrFun (prefix_axis hP q 3) a

/-- Only columns 4,5 satisfy this cutoff. No geometry assumption is needed. -/
theorem inactive_columns : Body4InactiveTarget := by
  intro q a j hj
  exact ⟨bodyJv_zero_of_inactive _ _ body4 j a hj,
    bodyJw_zero_of_inactive _ body4 j a hj⟩

/-- Dot preservation and ORIENTED cross transport are separate obligations.
This is not metric Isometry for the default Pi/sup norm on V3, and does
not identify any source column by itself. Target vcol/wcol are already lifted. -/
theorem lift_laws (q : Q6) (u v : V3) :
    dot (RouteBO1Body4SourceJacobianPorts20260908.lift q u)
      (RouteBO1Body4SourceJacobianPorts20260908.lift q v) = dot u v ∧
    cross3 (RouteBO1Body4SourceJacobianPorts20260908.lift q u)
      (RouteBO1Body4SourceJacobianPorts20260908.lift q v) =
      RouteBO1Body4SourceJacobianPorts20260908.lift q (cross3 u v) :=
  ⟨RouteBO1Body4SourceJacobianPorts20260908.lift_dot_isometry q u v,
    RouteBO1Body4SourceJacobianPorts20260908.lift_cross q u v⟩

-- Prospective inspections only: never executed in this task.
#print axioms jacobians_of_frames
#print axioms joint3_linear_of_translation
#print axioms joint3_angular_of_prefix
#print axioms inactive_columns
#print axioms lift_laws

end
end RouteBO1Body4FrameHandoff20260908
