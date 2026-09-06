import SourceContractAdapter

set_option autoImplicit false

namespace RouteBSourceContractIndexAdapter

noncomputable section

open RouteBFrameOriginAxis
open RouteBFrameSlotAccessor
open RouteBBodySemanticCore
open RouteBBodyContractCore
open RouteBSourceContractAdapter

/- Human body numbers 4 and 5 are zero-based `Fin 6` indices 3 and 4.
   These first three lemmas expose the index transport without expanding any
   DH matrix entries. -/
theorem source_prev_origin_slot (q : Fin 6 → ℝ) (body : Fin 6) :
    (sourceContract q).origins (prevOrigin body) =
      origin (routeBFrameSlot q (prevOrigin body)) := by
  simpa [frameContract] using
    congrFun (source_origin_function_eq_frame_contract q) (prevOrigin body)

theorem source_next_origin_slot (q : Fin 6 → ℝ) (body : Fin 6) :
    (sourceContract q).origins (nextOrigin body) =
      origin (routeBFrameSlot q (nextOrigin body)) := by
  simpa [frameContract] using
    congrFun (source_origin_function_eq_frame_contract q) (nextOrigin body)

theorem source_parent_axis_slot (q : Fin 6 → ℝ) (joint : Fin 6) :
    (sourceContract q).axes joint =
      zAxis (routeBFrameSlot q (prevOrigin joint)) := by
  simpa [frameContract] using
    congrFun (source_axis_function_eq_frame_contract q) joint

/- Body 4 has COM endpoints at frame slots 3 and 4. -/
theorem source_body4_com_uses_slots_3_4 (q : Fin 6 → ℝ) :
    bodyCom (sourceContract q).origins 3 =
      midpoint (origin (routeBFrameSlot q 3))
        (origin (routeBFrameSlot q 4)) := by
  change midpoint ((sourceContract q).origins (prevOrigin 3))
      ((sourceContract q).origins (nextOrigin 3)) = _
  rw [source_prev_origin_slot, source_next_origin_slot]
  rfl

/- The last active joint for body 4 is human joint 4: its angular/linear
   columns use parent-axis slot 3, while the COM uses slots 3 and 4. -/
theorem source_body4_joint4_Jv_uses_parent_slot_3
    (q : Fin 6 → ℝ) (a : Fin 3) :
    contractJv (sourceContract q) 3 a 3 =
      cross3 (zAxis (routeBFrameSlot q 3))
        (fun b =>
          midpoint (origin (routeBFrameSlot q 3))
              (origin (routeBFrameSlot q 4)) b -
            origin (routeBFrameSlot q 3) b) a := by
  change bodyJv (sourceContract q).origins (sourceContract q).axes 3 a 3 = _
  rw [bodyJv_active_formula _ _ _ _ _ (by decide)]
  rw [source_parent_axis_slot, source_body4_com_uses_slots_3_4,
    source_prev_origin_slot]
  rfl

theorem source_body4_joint4_Jw_uses_parent_slot_3
    (q : Fin 6 → ℝ) (a : Fin 3) :
    contractJw (sourceContract q) 3 a 3 =
      zAxis (routeBFrameSlot q 3) a := by
  change bodyJw (sourceContract q).axes 3 a 3 = _
  rw [bodyJw_active_formula _ _ _ _ (by decide)]
  rw [source_parent_axis_slot]
  rfl

/- Human joint 5 is outside body 4's ancestor set. -/
theorem source_body4_joint5_Jv_inactive
    (q : Fin 6 → ℝ) (a : Fin 3) :
    contractJv (sourceContract q) 3 a 4 = 0 := by
  change bodyJv (sourceContract q).origins (sourceContract q).axes 3 a 4 = 0
  exact bodyJv_zero_of_inactive _ _ _ _ _ (by decide)

theorem source_body4_joint5_Jw_inactive
    (q : Fin 6 → ℝ) (a : Fin 3) :
    contractJw (sourceContract q) 3 a 4 = 0 := by
  change bodyJw (sourceContract q).axes 3 a 4 = 0
  exact bodyJw_zero_of_inactive _ _ _ _ (by decide)

/- Body 5 has COM endpoints at frame slots 4 and 5. -/
theorem source_body5_com_uses_slots_4_5 (q : Fin 6 → ℝ) :
    bodyCom (sourceContract q).origins 4 =
      midpoint (origin (routeBFrameSlot q 4))
        (origin (routeBFrameSlot q 5)) := by
  change midpoint ((sourceContract q).origins (prevOrigin 4))
      ((sourceContract q).origins (nextOrigin 4)) = _
  rw [source_prev_origin_slot, source_next_origin_slot]
  rfl

/- Human joint 5 is active for body 5 and must read parent-axis slot 4. -/
theorem source_body5_joint5_Jv_uses_parent_slot_4
    (q : Fin 6 → ℝ) (a : Fin 3) :
    contractJv (sourceContract q) 4 a 4 =
      cross3 (zAxis (routeBFrameSlot q 4))
        (fun b =>
          midpoint (origin (routeBFrameSlot q 4))
              (origin (routeBFrameSlot q 5)) b -
            origin (routeBFrameSlot q 4) b) a := by
  change bodyJv (sourceContract q).origins (sourceContract q).axes 4 a 4 = _
  rw [bodyJv_active_formula _ _ _ _ _ (by decide)]
  rw [source_parent_axis_slot, source_body5_com_uses_slots_4_5,
    source_prev_origin_slot]
  rfl

theorem source_body5_joint5_Jw_uses_parent_slot_4
    (q : Fin 6 → ℝ) (a : Fin 3) :
    contractJw (sourceContract q) 4 a 4 =
      zAxis (routeBFrameSlot q 4) a := by
  change bodyJw (sourceContract q).axes 4 a 4 = _
  rw [bodyJw_active_formula _ _ _ _ (by decide)]
  rw [source_parent_axis_slot]
  rfl

/- Human joint 6 is outside body 5's ancestor set. -/
theorem source_body5_joint6_Jv_inactive
    (q : Fin 6 → ℝ) (a : Fin 3) :
    contractJv (sourceContract q) 4 a 5 = 0 := by
  change bodyJv (sourceContract q).origins (sourceContract q).axes 4 a 5 = 0
  exact bodyJv_zero_of_inactive _ _ _ _ _ (by decide)

theorem source_body5_joint6_Jw_inactive
    (q : Fin 6 → ℝ) (a : Fin 3) :
    contractJw (sourceContract q) 4 a 5 = 0 := by
  change bodyJw (sourceContract q).axes 4 a 5 = 0
  exact bodyJw_zero_of_inactive _ _ _ _ (by decide)

#print axioms source_prev_origin_slot
#print axioms source_next_origin_slot
#print axioms source_parent_axis_slot
#print axioms source_body4_com_uses_slots_3_4
#print axioms source_body4_joint4_Jv_uses_parent_slot_3
#print axioms source_body4_joint4_Jw_uses_parent_slot_3
#print axioms source_body4_joint5_Jv_inactive
#print axioms source_body4_joint5_Jw_inactive
#print axioms source_body5_com_uses_slots_4_5
#print axioms source_body5_joint5_Jv_uses_parent_slot_4
#print axioms source_body5_joint5_Jw_uses_parent_slot_4
#print axioms source_body5_joint6_Jv_inactive
#print axioms source_body5_joint6_Jw_inactive

end
end RouteBSourceContractIndexAdapter
