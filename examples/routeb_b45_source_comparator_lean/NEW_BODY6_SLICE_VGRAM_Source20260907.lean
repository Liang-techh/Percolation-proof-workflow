import NEW_BODY6_SLICE_VGRAM_Core20260907
import NEW_BODY6_SLICE_AXIS_Geometry20260907
import RouteBO1PerBodyExactSource

set_option autoImplicit false

namespace NEW_BODY6_SLICE_VGRAM_Source20260907

noncomputable section

open NEW_BODY6_SLICE_AXIS_Core20260907 NEW_BODY6_SLICE_AXIS_Geometry20260907
open NEW_BODY6_SLICE_VGRAM_Core20260907
open RouteBO1PerBodyExactSource RouteBBodySemanticCore RouteBSourceContractAdapter
open RouteBFrameOriginAxis RouteBFrameSlotAccessor RouteBRealDHStep RouteBB45Fourier

/- UNCOMPILED typed source skeleton. Body index is 5; all six joints are active.
   A geometric zero column must never be confused with an inactive joint. -/

def frontJoint (i : Fin 5) : Fin 6 := ⟨i.val, by omega⟩
def offset : ℝ := 7 / 200
def sourceZ (q : Q6) (i : Fin 6) : AVec := (sourceContract q).axes i
def parentO (q : Q6) (i : Fin 6) : AVec := (sourceContract q).origins (prevOrigin i)
def terminalO (q : Q6) : AVec := (sourceContract q).origins (5 : Fin 7)
def sourceV (q : Q6) (i : Fin 6) : AVec :=
  fun a => bodyJv (sourceContract q).origins (sourceContract q).axes (5 : Fin 6) a i
def baseV (q : Q6) (i : Fin 6) : AVec :=
  crossV (sourceZ q i) (fun a => terminalO q a - parentO q i a)
def frontLinearGram (q : Q6) (i j : Fin 5) : ℝ :=
  linearGram5 (fun k => sourceV q (frontJoint k)) i j

def CenterOffsetTarget : Prop :=
  ∀ q a, bodyCom (sourceContract q).origins (5 : Fin 6) a =
    terminalO q a + offset * sourceZ q (5 : Fin 6) a

theorem front_joint_value_attempt (i : Fin 5) : (frontJoint i).val = i.val := rfl

theorem all_six_active_attempt (i : Fin 6) : i.val ≤ (5 : Fin 6).val := by
  have hi := i.isLt
  omega

theorem no_inactive_body6_joint_attempt (i : Fin 6) : ¬ (5 : Fin 6).val < i.val := by
  have hi := all_six_active_attempt i
  omega

theorem source_active_velocity_attempt (q : Q6) (i : Fin 6) :
    sourceV q i = crossV (sourceZ q i)
      (fun a => bodyCom (sourceContract q).origins (5 : Fin 6) a - parentO q i a) := by
  funext a
  exact bodyJv_active_formula _ _ _ _ _ (all_six_active_attempt i)

theorem source_velocity_decomposition_attempt (hc : CenterOffsetTarget)
    (q : Q6) (i : Fin 6) :
    sourceV q i = fun a => baseV q i a + offset * crossV (sourceZ q i) (sourceZ q 5) a := by
  rw [source_active_velocity_attempt]
  have hcenter : (fun a => bodyCom (sourceContract q).origins (5 : Fin 6) a - parentO q i a) =
      (fun a => terminalO q a + offset * sourceZ q 5 a - parentO q i a) := by
    funext a
    rw [hc q a]
  rw [hcenter]
  exact displaced_velocity_split_attempt _ _ _ _ _

/- Small origin leaves: step 4 translates by 19/100 along its parent z;
   step 5 has zero translation. Prefix F is arbitrary. -/
theorem origin_step3_attempt (F : Matrix (Fin 4) (Fin 4) ℝ) (t : ℝ) :
    origin (F * routeBRealStepMatrix 3 t) =
      (fun a => origin F a + (19 / 100 : ℝ) * zAxis F a) := by
  funext a
  fin_cases a <;>
    norm_num [origin, zAxis, RouteBFrameOriginAxis.embed3, Matrix.mul_apply,
      Fin.sum_univ_succ, routeBRealStepMatrix, realDHStep, routeBA, routeBD] <;> ring

theorem origin_step4_attempt (F : Matrix (Fin 4) (Fin 4) ℝ) (t : ℝ) :
    origin (F * routeBRealStepMatrix 4 t) = origin F := by
  funext a
  fin_cases a <;>
    norm_num [origin, RouteBFrameOriginAxis.embed3, Matrix.mul_apply,
      Fin.sum_univ_succ, routeBRealStepMatrix, realDHStep, routeBA, routeBD]

theorem source_origin_slot_attempt (q : Q6) (s : Fin 7) :
    (sourceContract q).origins s = origin (routeBFrameSlot q s) := by
  exact congrFun (source_origin_function_eq_frame_contract q) s

theorem terminal_origin4_attempt (q : Q6) : terminalO q = parentO q (4 : Fin 6) := by
  change (sourceContract q).origins 5 = (sourceContract q).origins 4
  simp_rw [source_origin_slot_attempt]
  change origin (routeBFrameSlot q 4 * routeBRealStepMatrix 4 (q 4)) = _
  exact origin_step4_attempt _ _

theorem terminal_origin3_attempt (q : Q6) (a : Fin 3) :
    terminalO q a = parentO q (3 : Fin 6) a + (19 / 100 : ℝ) * sourceZ q 3 a := by
  rw [terminal_origin4_attempt]
  change (sourceContract q).origins 4 a =
    (sourceContract q).origins 3 a + (19 / 100 : ℝ) * (sourceContract q).axes 3 a
  have hz := congrFun (source_axis_function_eq_frame_contract q) (3 : Fin 6)
  simp_rw [source_origin_slot_attempt]
  rw [hz]
  change origin (routeBFrameSlot q 3 * routeBRealStepMatrix 3 (q 3)) a = _
  exact congrFun (origin_step3_attempt _ _) a

theorem source_velocity3_attempt (hc : CenterOffsetTarget) (q : Q6) :
    sourceV q (3 : Fin 6) = fun a => offset * crossV (sourceZ q 3) (sourceZ q 5) a := by
  rw [source_velocity_decomposition_attempt hc]
  have hbase : baseV q (3 : Fin 6) = 0 :=
    parallel_lever_zero_attempt _ _ _ (19 / 100) (terminal_origin3_attempt q)
  rw [hbase]
  simp

theorem source_velocity4_attempt (hc : CenterOffsetTarget) (q : Q6) :
    sourceV q (4 : Fin 6) = fun a => offset * crossV (sourceZ q 4) (sourceZ q 5) a := by
  rw [source_velocity_decomposition_attempt hc]
  have hbase : baseV q (4 : Fin 6) = 0 := by
    funext a
    fin_cases a <;> simp [baseV, terminal_origin4_attempt, crossV]
  rw [hbase]
  simp

/- L0,L1,L2 retain the actual nonzero parent lever arms. No zero premise is added. -/
def FirstThreeLeverTarget (v : Q6 → Fin 3 → AVec) : Prop :=
  ∀ q (i : Fin 3), baseV q ⟨i.val, by omega⟩ = v q i

theorem inertia_trace_attempt (u v : AVec) :
    (∑ a : Fin 3, ∑ b : Fin 3, u a * routeBInertia (5 : Fin 6) a b * v b) =
      (1 / 60 : ℝ) * dot3 u v := by
  norm_num [routeBInertia, routeBInertiaScalar, dot3, Fin.sum_univ_succ] <;> ring

theorem source_mass_gram_attempt (q : Q6) (i j : Fin 6) :
    sourceBodyMass q (5 : Fin 6) i j =
      (3 / 20 : ℝ) * dot3 (sourceV q i) (sourceV q j) +
      (1 / 60 : ℝ) * dot3 (sourceZ q i) (sourceZ q j) := by
  rw [sourceBodyMass_eq_bodyMass]
  change (3 / 20 : ℝ) * dot3 (sourceV q i) (sourceV q j) +
    (∑ a : Fin 3, ∑ b : Fin 3,
      bodyJw (sourceContract q).axes (5 : Fin 6) a i *
      routeBInertia (5 : Fin 6) a b * bodyJw (sourceContract q).axes (5 : Fin 6) b j) = _
  rw [inertia_trace_attempt]
  have hi : (fun a => bodyJw (sourceContract q).axes (5 : Fin 6) a i) = sourceZ q i := by
    funext a
    exact bodyJw_active_formula _ _ _ _ (all_six_active_attempt i)
  have hj : (fun a => bodyJw (sourceContract q).axes (5 : Fin 6) a j) = sourceZ q j := by
    funext a
    exact bodyJw_active_formula _ _ _ _ (all_six_active_attempt j)
  rw [hi, hj]

theorem front_source_gram_attempt (q : Q6) (i j : Fin 5) :
    sourceBodyMass q (5 : Fin 6) (frontJoint i) (frontJoint j) =
      (3 / 20 : ℝ) * frontLinearGram q i j +
      (1 / 60 : ℝ) * dot3 (sourceZ q (frontJoint i)) (sourceZ q (frontJoint j)) :=
  source_mass_gram_attempt q (frontJoint i) (frontJoint j)

theorem front_linear_symmetric_attempt (q : Q6) (i j : Fin 5) :
    frontLinearGram q i j = frontLinearGram q j i := linear_gram5_symmetric_attempt _ _ _

theorem source_mass_symmetric_attempt (q : Q6) (i j : Fin 6) :
    sourceBodyMass q (5 : Fin 6) i j = sourceBodyMass q (5 : Fin 6) j i := by
  rw [source_mass_gram_attempt, source_mass_gram_attempt]
  rw [dot_swap_attempt (sourceV q i) (sourceV q j), dot_swap_attempt (sourceZ q i) (sourceZ q j)]

end
end NEW_BODY6_SLICE_VGRAM_Source20260907
