import RouteBO1Body5SourceTraceTargets

set_option autoImplicit false

namespace RouteBO1Body5GeometryColumnsProofAttempt20260907

noncomputable section

open RouteBO1PerBodyExactSource
open RouteBO1Body5SourceTraceTargets
open RouteBBodySemanticCore
open RouteBSourceContractAdapter
open RouteBSourceContractIndexAdapter
open RouteBFrameOriginAxis
open RouteBFrameSlotAccessor
open RouteBRealDHStep
open RouteBB45Fourier

/-!
UNCOMPILED PROOF ATTEMPT. Human body 5 is body 4; joint 5 below is
zero-based (human joint 6). Every declaration below needs elaboration and
dependency auditing before it can be treated as a theorem result.
The imported G1/G2 targets are consumed unchanged. No trace fold is unfolded.
The unconditional source leaves do not assume Body5GeometryTarget.
-/

abbrev F4 := Matrix (Fin 4) (Fin 4) ℝ

def frameColumn (F : F4) (k : Fin 4) : V3 := fun a => F (embed3 a) k

/- Only one multiplication is exposed here; F remains arbitrary. -/
theorem origin_mul_step4_attempt (F : F4) (t : ℝ) :
    origin (F * routeBRealStepMatrix 4 t) = origin F := by
  funext a
  fin_cases a <;>
    norm_num [origin, embed3, Matrix.mul_apply, Fin.sum_univ_succ,
      routeBRealStepMatrix, realDHStep, routeBA, routeBD]

theorem origin_mul_step3_attempt (F : F4) (t : ℝ) :
    origin (F * routeBRealStepMatrix 3 t) =
      (fun a => origin F a + (19 / 100 : ℝ) * zAxis F a) := by
  funext a
  fin_cases a <;>
    norm_num [origin, zAxis, embed3, Matrix.mul_apply, Fin.sum_univ_succ,
      routeBRealStepMatrix, realDHStep, routeBA, routeBD] <;> ring

theorem axis_mul_step3_attempt (F : F4) (t : ℝ) :
    zAxis (F * routeBRealStepMatrix 3 t) =
      (fun a => -Real.sin t * frameColumn F 0 a +
        Real.cos t * frameColumn F 1 a) := by
  funext a
  fin_cases a <;>
    norm_num [zAxis, frameColumn, embed3, Matrix.mul_apply, Fin.sum_univ_succ,
      routeBRealStepMatrix, realDHStep, routeBRealCos, routeBRealSin,
      routeBCosAlpha, routeBSinAlpha] <;> ring

theorem frame_slot4_step_attempt (q : Q6) :
    routeBFrameSlot q 4 = routeBFrameSlot q 3 * routeBRealStepMatrix 3 (q 3) := by
  rfl

theorem frame_slot5_step_attempt (q : Q6) :
    routeBFrameSlot q 5 = routeBFrameSlot q 4 * routeBRealStepMatrix 4 (q 4) := by
  rfl

theorem source_origin_slot_attempt (q : Q6) (k : Fin 7) :
    (sourceContract q).origins k = origin (routeBFrameSlot q k) := by
  exact congrFun (source_origin_function_eq_frame_contract q) k

theorem source_o5_eq_o4_attempt (q : Q6) :
    (sourceContract q).origins 5 = (sourceContract q).origins 4 := by
  rw [source_origin_slot_attempt, source_origin_slot_attempt,
    frame_slot5_step_attempt, origin_mul_step4_attempt]

theorem source_o4_sub_o3_attempt (q : Q6) :
    (fun a => (sourceContract q).origins 4 a - (sourceContract q).origins 3 a) =
      (fun a => (19 / 100 : ℝ) * (sourceContract q).axes 3 a) := by
  rw [source_origin_slot_attempt, source_origin_slot_attempt,
    source_parent_axis_slot]
  change (fun a => origin (routeBFrameSlot q 4) a -
      origin (routeBFrameSlot q 3) a) =
    (fun a => (19 / 100 : ℝ) * zAxis (routeBFrameSlot q 3) a)
  rw [frame_slot4_step_attempt, origin_mul_step3_attempt]
  funext a
  dsimp
  ring

theorem source_com_eq_o4_attempt (q : Q6) :
    bodyCom (sourceContract q).origins body5Index = (sourceContract q).origins 4 := by
  change midpoint ((sourceContract q).origins 4) ((sourceContract q).origins 5) = _
  rw [source_o5_eq_o4_attempt]
  funext a
  dsimp [midpoint]
  ring

theorem cross3_self_scale_attempt (u : V3) (r : ℝ) :
    cross3 u (fun a => r * u a) = 0 := by
  funext a
  fin_cases a <;> simp [cross3] <;> ring

theorem source_v3_zero_attempt (q : Q6) :
    (fun a => bodyJv (sourceContract q).origins (sourceContract q).axes
      body5Index a 3) = 0 := by
  have hc : (fun a => bodyJv (sourceContract q).origins (sourceContract q).axes
      body5Index a 3) = cross3 ((sourceContract q).axes 3)
        (fun a => bodyCom (sourceContract q).origins body5Index a -
          (sourceContract q).origins 3 a) := by
    funext a
    exact bodyJv_active_formula _ _ _ _ _ (by decide)
  rw [hc, source_com_eq_o4_attempt, source_o4_sub_o3_attempt]
  exact cross3_self_scale_attempt _ _

theorem source_v4_zero_attempt (q : Q6) :
    (fun a => bodyJv (sourceContract q).origins (sourceContract q).axes
      body5Index a 4) = 0 := by
  funext a
  rw [bodyJv_active_formula _ _ _ _ _ (by decide), source_com_eq_o4_attempt]
  change cross3 ((sourceContract q).axes 4)
    (fun b => (sourceContract q).origins 4 b - (sourceContract q).origins 4 b) a = 0
  fin_cases a <;> simp [cross3]

theorem source_joint5_inactive_attempt (q : Q6) :
    (fun a => bodyJv (sourceContract q).origins (sourceContract q).axes
      body5Index a 5) = 0 ∧
    (fun a => bodyJw (sourceContract q).axes body5Index a 5) = 0 := by
  constructor
  · funext a
    exact bodyJv_zero_of_inactive _ _ _ _ _ (by decide)
  · funext a
    exact bodyJw_zero_of_inactive _ _ _ _ (by decide)

/- Cylindrical coordinates form an oriented rotation, not just an isometry. -/
theorem lift_zero_attempt (q : Q6) : body5Lift q 0 = 0 := by
  funext a
  fin_cases a <;> simp [body5Lift]

theorem lift_sub_attempt (q : Q6) (u v : V3) :
    body5Lift q (fun a => u a - v a) =
      (fun a => body5Lift q u a - body5Lift q v a) := by
  funext a
  fin_cases a <;> simp [body5Lift] <;> ring

theorem lift_cross_attempt (q : Q6) (u v : V3) :
    cross3 (body5Lift q u) (body5Lift q v) = body5Lift q (cross3 u v) := by
  have h := Real.sin_sq_add_cos_sq (q 0)
  funext a
  fin_cases a <;> simp [body5Lift, cross3] <;>
    first | ring | linear_combination (u 0 * v 1 - u 1 * v 0) * h

theorem lift_isometry_attempt : Body5LiftIsometryTarget := by
  intro q u v
  have h := Real.sin_sq_add_cos_sq (q 0)
  simp [body5Dot, body5Lift, Fin.sum_univ_succ]
  linear_combination (u 0 * v 0 + u 1 * v 1) * h

/- Bounded scalar reductions only: prefix slots 0..3. Later slots use the
   one-step identities above. This tactic never unfolds source lists/folds. -/
macro "body5_prefix_scalar" : tactic =>
  `(tactic|
    (norm_num [routeBFrameSlot, prefixFrame, routeBStepFunction,
      routeBRealStepMatrix, realDHStep, routeBRealCos, routeBRealSin,
      routeBCosAlpha, routeBSinAlpha, routeBA, routeBD,
      origin, zAxis, frameColumn, embed3, Matrix.mul_apply, Matrix.one_apply,
      Fin.sum_univ_succ, body5Lift, body5OriginLocal, body5WLocal,
      body5Phi, Real.sin_add, Real.cos_add] <;> ring))

theorem frame_origins_0_to_3_attempt (q : Q6) (k : Fin 4) :
    origin (routeBFrameSlot q ⟨k.val, by omega⟩) =
      body5Lift q (body5OriginLocal q ⟨k.val, by omega⟩) := by
  fin_cases k <;> funext a <;> fin_cases a <;> body5_prefix_scalar

theorem frame_axes_0_to_3_attempt (q : Q6) (j : Fin 4) :
    zAxis (routeBFrameSlot q ⟨j.val, by omega⟩) =
      body5Lift q (body5WLocal q ⟨j.val, by omega⟩) := by
  fin_cases j <;> funext a <;> fin_cases a <;> body5_prefix_scalar

theorem frame3_x_attempt (q : Q6) :
    frameColumn (routeBFrameSlot q 3) 0 =
      body5Lift q ![Real.cos (body5Phi q), 0, -Real.sin (body5Phi q)] := by
  funext a
  fin_cases a <;> body5_prefix_scalar

theorem frame3_y_attempt (q : Q6) :
    frameColumn (routeBFrameSlot q 3) 1 = body5Lift q ![0, 1, 0] := by
  funext a
  fin_cases a <;> body5_prefix_scalar

theorem frame_origin4_attempt (q : Q6) :
    origin (routeBFrameSlot q 4) = body5Lift q (body5OriginLocal q 4) := by
  rw [frame_slot4_step_attempt, origin_mul_step3_attempt,
    frame_origins_0_to_3_attempt q 3, frame_axes_0_to_3_attempt q 3]
  funext a
  fin_cases a <;>
    norm_num [body5Lift, body5OriginLocal, body5WLocal, body5A, body5P] <;> ring

theorem frame_origin5_attempt (q : Q6) :
    origin (routeBFrameSlot q 5) = body5Lift q (body5OriginLocal q 5) := by
  rw [frame_slot5_step_attempt, origin_mul_step4_attempt]
  exact frame_origin4_attempt q

theorem frame_axis4_attempt (q : Q6) :
    zAxis (routeBFrameSlot q 4) = body5Lift q (body5WLocal q 4) := by
  rw [frame_slot4_step_attempt, axis_mul_step3_attempt, frame3_x_attempt,
    frame3_y_attempt]
  funext a
  fin_cases a <;> norm_num [body5Lift, body5WLocal] <;> ring

/- G1 witness attempt: explicit actual source bindings, no geometry premise. -/
theorem body5_geometry_attempt : Body5GeometryTarget := by
  intro q
  constructor
  · intro k hk
    rw [source_origin_slot_attempt]
    fin_cases k
    · exact frame_origins_0_to_3_attempt q 0
    · exact frame_origins_0_to_3_attempt q 1
    · exact frame_origins_0_to_3_attempt q 2
    · exact frame_origins_0_to_3_attempt q 3
    · exact frame_origin4_attempt q
    · exact frame_origin5_attempt q
    · omega
  · intro j hj
    rw [source_parent_axis_slot]
    fin_cases j
    · exact frame_axes_0_to_3_attempt q 0
    · exact frame_axes_0_to_3_attempt q 1
    · exact frame_axes_0_to_3_attempt q 2
    · exact frame_axes_0_to_3_attempt q 3
    · exact frame_axis4_attempt q
    · omega

theorem local_cross_columns_attempt (q : Q6) (j : Fin 6) (hj : j.val ≤ 4) :
    cross3 (body5WLocal q j)
      (fun a => body5OriginLocal q 4 a - body5OriginLocal q (prevOrigin j) a) =
        body5VLocal q j := by
  fin_cases j
  all_goals try omega
  all_goals
    funext a
    fin_cases a <;>
      norm_num [prevOrigin, cross3, body5OriginLocal, body5WLocal, body5VLocal,
        body5A, body5P, body5Q] <;> ring

/- G2 witness attempt consumes the existing G1 target, supplies all active
   cross-product work, and handles joint 5 with the actual ancestor guard. -/
theorem body5_geometry_to_columns_attempt : Body5GeometryToColumnsTarget := by
  intro hgeom q j
  by_cases hj : j.val ≤ 4
  · have ho4 := (hgeom q).1 4 (by decide)
    have hop := (hgeom q).1 (prevOrigin j) (by change j.val ≤ 5; omega)
    have haw := (hgeom q).2 j hj
    constructor
    · have hv : (fun a => bodyJv (sourceContract q).origins (sourceContract q).axes
          body5Index a j) = cross3 ((sourceContract q).axes j)
            (fun a => bodyCom (sourceContract q).origins body5Index a -
              (sourceContract q).origins (prevOrigin j) a) := by
        funext a
        exact bodyJv_active_formula _ _ _ _ _ hj
      rw [hv, source_com_eq_o4_attempt, ho4, hop, haw,
        ← lift_sub_attempt, lift_cross_attempt, local_cross_columns_attempt q j hj]
    · funext a
      rw [bodyJw_active_formula _ _ _ _ hj]
      exact congrFun haw a
  · have hj5 : j = (5 : Fin 6) := by
      apply Fin.ext
      have hlt := j.isLt
      change j.val = 5
      omega
    subst j
    constructor
    · simpa [body5VLocal, lift_zero_attempt] using (source_joint5_inactive_attempt q).1
    · simpa [body5WLocal, lift_zero_attempt] using (source_joint5_inactive_attempt q).2

/- Unconditional G2 output attempt, assembled from the actual G1 attempt.
   This is not sourceBodyMass, G3/G4, a trace equality, or h_body_5. -/
theorem body5_columns_attempt : Body5ColumnsTarget := by
  exact body5_geometry_to_columns_attempt body5_geometry_attempt

end
end RouteBO1Body5GeometryColumnsProofAttempt20260907
