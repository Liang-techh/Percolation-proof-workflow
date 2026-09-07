import RouteBO1Body4SourceGramTargets

set_option autoImplicit false

namespace RouteBO1Body4SourceJacobianBridge20260907

noncomputable section

open RouteBO1PerBodyExactSource
open RouteBO1Body4SourceGramTargets
open RouteBBodySemanticCore
open RouteBSourceContractAdapter
open RouteBSourceContractIndexAdapter
open RouteBFrameSlotAccessor
open RouteBRealDHStep

/-!
SOURCE_JACOBIAN_PROOF_SKELETON_UNCOMPILED.
No Lean/Lake run, elaboration result, kernel evidence, or admission claim.
Only original targets are imported; neither earlier proof attempt is imported.
The conditional ports below expose geometry premises explicitly; the final
jv_attempt/jw_attempt supply local geometry scripts, not new axioms/premises.
Those scripts still require elaboration of this entire module and its imports.
Endpoint: Body4JvTarget / Body4JwTarget, not a source mass or trace theorem.
-/

-- Human body 4 is index 3. Fin 4 enumerates its FOUR active joints.
def activeJoint (j : Fin 4) : Joint :=
  ⟨j.val, Nat.lt_trans j.isLt (by decide)⟩

def prefixSlot (j : Fin 4) : Fin 7 :=
  ⟨j.val, Nat.lt_trans j.isLt (by decide)⟩

theorem body4_index : body4 = (3 : Body) := rfl

theorem body4_com_indices :
    prevOrigin body4 = (3 : Fin 7) ∧ nextOrigin body4 = (4 : Fin 7) := by
  constructor <;> rfl

theorem parent_slot (j : Fin 4) :
    prevOrigin (activeJoint j) = prefixSlot j := by
  apply Fin.ext
  rfl

theorem active_guard (j : Fin 4) : (activeJoint j).val ≤ body4.val := by
  have hj := j.isLt
  change j.val ≤ 3
  omega

theorem activeJoint_roundtrip (j : Joint) (h : j.val < 4) :
    activeJoint ⟨j.val, h⟩ = j := by
  apply Fin.ext
  rfl

-- lift is the oriented cylindrical-to-world rotation used by target vec.
def lift (q : Q6) (u : V3) : V3 := vec q (u 0) (u 1) (u 2)

theorem lift_zero (q : Q6) : lift q 0 = 0 := by
  funext a
  fin_cases a <;> simp [lift, vec]

theorem lift_cross (q : Q6) (u v : V3) :
    cross3 (lift q u) (lift q v) = lift q (cross3 u v) := by
  funext a
  fin_cases a
  · change
      (u 0 * Real.sin (q 0) + u 1 * Real.cos (q 0)) * v 2 -
        u 2 * (v 0 * Real.sin (q 0) + v 1 * Real.cos (q 0)) =
      (u 1 * v 2 - u 2 * v 1) * Real.cos (q 0) -
        (u 2 * v 0 - u 0 * v 2) * Real.sin (q 0)
    ring
  · change
      u 2 * (v 0 * Real.cos (q 0) - v 1 * Real.sin (q 0)) -
        (u 0 * Real.cos (q 0) - u 1 * Real.sin (q 0)) * v 2 =
      (u 1 * v 2 - u 2 * v 1) * Real.sin (q 0) +
        (u 2 * v 0 - u 0 * v 2) * Real.cos (q 0)
    ring
  · change
      (u 0 * Real.cos (q 0) - u 1 * Real.sin (q 0)) *
          (v 0 * Real.sin (q 0) + v 1 * Real.cos (q 0)) -
        (u 0 * Real.sin (q 0) + u 1 * Real.cos (q 0)) *
          (v 0 * Real.cos (q 0) - v 1 * Real.sin (q 0)) =
        u 0 * v 1 - u 1 * v 0
    calc
      _ = (u 0 * v 1 - u 1 * v 0) *
          (Real.sin (q 0) ^ 2 + Real.cos (q 0) ^ 2) := by ring
      _ = u 0 * v 1 - u 1 * v 0 := by
        rw [Real.sin_sq_add_cos_sq (q 0)]
        ring

/-- Euclidean dot preservation. This does NOT assert metric `Isometry` for
the default Pi/sup norm on Fin 3 -> Real. Dot preservation alone also does
not imply the oriented cross transport used in the Jv proof. -/
theorem lift_dot_isometry (q : Q6) (u v : V3) :
    dot (lift q u) (lift q v) = dot u v := by
  have expand (x y : V3) :
      dot x y = x 0 * y 0 + x 1 * y 1 + x 2 * y 2 := by
    simp [dot, Fin.sum_univ_succ, add_assoc]
  rw [expand, expand]
  change
    (u 0 * Real.cos (q 0) - u 1 * Real.sin (q 0)) *
        (v 0 * Real.cos (q 0) - v 1 * Real.sin (q 0)) +
      (u 0 * Real.sin (q 0) + u 1 * Real.cos (q 0)) *
        (v 0 * Real.sin (q 0) + v 1 * Real.cos (q 0)) + u 2 * v 2 =
      u 0 * v 0 + u 1 * v 1 + u 2 * v 2
  calc
    _ = (u 0 * v 0 + u 1 * v 1) *
        (Real.sin (q 0) ^ 2 + Real.cos (q 0) ^ 2) + u 2 * v 2 := by ring
    _ = u 0 * v 0 + u 1 * v 1 + u 2 * v 2 := by
      rw [Real.sin_sq_add_cos_sq (q 0)]
      ring

theorem basis_cross : Body4BasisCrossTarget := by
  intro q r t z r' t' z'
  exact lift_cross q ![r, t, z] ![r', t', z']

-- Only origin/z columns of slots 0..3 are required; no slot-4 rotation.
-- Qualify Fourier constants; V3 here remains the vector alias from Targets.
macro "body4_jacobian_prefix_scalar" : tactic =>
  `(tactic|
    (norm_num [prefixSlot, routeBFrameSlot, prefixFrame, routeBStepFunction,
      routeBRealStepMatrix, realDHStep, routeBRealCos, routeBRealSin,
      RouteBB45Fourier.routeBCosAlpha, RouteBB45Fourier.routeBSinAlpha,
      RouteBB45Fourier.routeBA, RouteBB45Fourier.routeBD,
      RouteBFrameOriginAxis.origin, RouteBFrameOriginAxis.zAxis,
      RouteBFrameOriginAxis.embed3, Matrix.mul_apply, Matrix.one_apply,
      Fin.sum_univ_succ, prefixO, prefixZ, vec, b, c, d, phi,
      Real.sin_add, Real.cos_add] <;> ring))

theorem frame_origin_prefix (q : Q6) (s : Fin 4) :
    RouteBFrameOriginAxis.origin (routeBFrameSlot q (prefixSlot s)) =
      prefixO q s := by
  fin_cases s <;> funext a <;> fin_cases a <;> body4_jacobian_prefix_scalar

theorem frame_axis_prefix (q : Q6) (s : Fin 4) :
    RouteBFrameOriginAxis.zAxis (routeBFrameSlot q (prefixSlot s)) =
      prefixZ q s := by
  fin_cases s <;> funext a <;> fin_cases a <;> body4_jacobian_prefix_scalar

theorem step3_translation (q : Q6) (k : Fin 4) :
    routeBStepFunction q 3 k 3 =
      if k = 2 then (19 / 100 : ℝ) else if k = 3 then 1 else 0 := by
  fin_cases k <;>
    norm_num [routeBStepFunction, routeBRealStepMatrix, realDHStep,
      routeBRealCos, routeBRealSin, RouteBB45Fourier.routeBCosAlpha,
      RouteBB45Fourier.routeBSinAlpha, RouteBB45Fourier.routeBA,
      RouteBB45Fourier.routeBD]

theorem slot4_translation : Body4Slot4TranslationTarget := by
  intro q a
  have h4 : routeBFrameSlot q 4 =
      routeBFrameSlot q 3 * routeBStepFunction q 3 := rfl
  change routeBFrameSlot q 4 (RouteBFrameOriginAxis.embed3 a) 3 = _
  rw [h4, Matrix.mul_apply]
  simp [step3_translation, Fin.sum_univ_succ,
    RouteBFrameOriginAxis.origin, RouteBFrameOriginAxis.zAxis] <;> ring

theorem frame_origin4 (q : Q6) :
    RouteBFrameOriginAxis.origin (routeBFrameSlot q 4) =
      vec q (2 / 25 + b q + (19 / 100) * Real.sin (phi q)) d
        (1 / 10 + c q + (19 / 100) * Real.cos (phi q)) := by
  funext a
  rw [slot4_translation q a, frame_origin_prefix q 3, frame_axis_prefix q 3]
  fin_cases a <;> simp [prefixO, prefixZ, vec] <;> ring

theorem source_origin_prefix (q : Q6) (s : Fin 4) :
    (sourceContract q).origins (prefixSlot s) = prefixO q s := by
  calc
    _ = RouteBFrameOriginAxis.origin (routeBFrameSlot q (prefixSlot s)) := by
      exact congrFun (source_origin_function_eq_frame_contract q) (prefixSlot s)
    _ = prefixO q s := frame_origin_prefix q s

theorem source_axes : Body4SourceAxesTarget := by
  intro q j
  change (sourceContract q).axes (activeJoint j) = prefixZ q j
  rw [source_parent_axis_slot, parent_slot]
  exact frame_axis_prefix q j

theorem source_com : Body4ComTarget := by
  intro q
  change bodyCom (sourceContract q).origins (3 : Body) = _
  rw [source_body4_com_uses_slots_3_4, frame_origin_prefix q 3, frame_origin4]
  funext a
  fin_cases a <;>
    simp [RouteBBodySemanticCore.midpoint, prefixO, vec, aa, pp, e] <;> ring

theorem source_displacements : Body4DisplacementsTarget := by
  intro q j a
  change bodyCom (sourceContract q).origins body4 a -
    (sourceContract q).origins (prefixSlot j) a = displacement q j a
  rw [source_com, source_origin_prefix q j]
  fin_cases j <;> fin_cases a <;>
    simp [displacement, prefixO, vec, aa, pp, qq] <;> ring

-- Joint 3 is active. Its Jv vanishes by parallelism, not an ancestor cutoff.
theorem joint3_parallel (q : Q6) :
    displacement q 3 = (fun a => e * prefixZ q 3 a) := by
  funext a
  fin_cases a <;> simp [displacement, prefixZ, vec] <;> ring

theorem cross_parallel (u : V3) (k : ℝ) :
    cross3 u (fun a => k * u a) = 0 := by
  funext a
  fin_cases a <;> simp [cross3] <;> ring

theorem joint3_cross_zero (q : Q6) :
    cross3 (prefixZ q 3) (displacement q 3) = 0 := by
  rw [joint3_parallel]
  exact cross_parallel (prefixZ q 3) e

theorem active_cross_columns (q : Q6) (j : Fin 4) :
    cross3 (prefixZ q j) (displacement q j) = vcol q (activeJoint j) := by
  fin_cases j
  · dsimp only [prefixZ, displacement, vcol, activeJoint]
    rw [basis_cross]
    funext a
    fin_cases a <;> simp [vec] <;> ring
  · dsimp only [prefixZ, displacement, vcol, activeJoint]
    rw [basis_cross]
    funext a
    fin_cases a <;> simp [vec] <;> ring
  · dsimp only [prefixZ, displacement, vcol, activeJoint]
    rw [basis_cross]
    funext a
    fin_cases a <;> simp [vec] <;> ring
  · change cross3 (prefixZ q 3) (displacement q 3) = 0
    exact joint3_cross_zero q

theorem inactive : Body4InactiveTarget := by
  intro q a j h
  exact ⟨bodyJv_zero_of_inactive _ _ body4 j a h,
    bodyJw_zero_of_inactive _ body4 j a h⟩

-- Explicit conditional source-binding ports, NOT discharged source theorems.
theorem active_jv_of_geometry
    (hAxes : Body4SourceAxesTarget) (hDisp : Body4DisplacementsTarget)
    (q : Q6) (j : Fin 4) (a : Axis) :
    bodyJv (sourceContract q).origins (sourceContract q).axes body4 a
      (activeJoint j) = vcol q (activeJoint j) a := by
  rw [bodyJv_active_formula _ _ _ _ _ (active_guard j)]
  have hd : (fun k => bodyCom (sourceContract q).origins body4 k -
      (sourceContract q).origins (prevOrigin (activeJoint j)) k) =
        displacement q j := by
    rw [parent_slot]
    funext k
    exact hDisp q j k
  rw [hAxes q j, hd, active_cross_columns]

theorem jv_of_source_geometry
    (hAxes : Body4SourceAxesTarget) (hDisp : Body4DisplacementsTarget) :
    Body4JvTarget := by
  intro q a j
  by_cases h : j.val < 4
  · simpa only [activeJoint_roundtrip] using
      active_jv_of_geometry hAxes hDisp q ⟨j.val, h⟩ a
  · have hi : 3 < j.val := by omega
    rw [(inactive q a j hi).1]
    fin_cases j <;> norm_num [vcol] at h ⊢

theorem active_jw_of_axes (hAxes : Body4SourceAxesTarget)
    (q : Q6) (j : Fin 4) (a : Axis) :
    bodyJw (sourceContract q).axes body4 a (activeJoint j) =
      wcol q (activeJoint j) a := by
  rw [bodyJw_active_formula _ _ _ _ (active_guard j), hAxes q j]
  fin_cases j <;> rfl

theorem jw_of_source_axes (hAxes : Body4SourceAxesTarget) : Body4JwTarget := by
  intro q a j
  by_cases h : j.val < 4
  · simpa only [activeJoint_roundtrip] using
      active_jw_of_axes hAxes q ⟨j.val, h⟩ a
  · have hi : 3 < j.val := by omega
    rw [(inactive q a j hi).2]
    fin_cases j <;> norm_num [wcol] at h ⊢

-- Original unconditional target types, assembled ONLY from local scripts.
-- These are candidate proof bodies, not evidence of elaborated inhabitants.
theorem jv_attempt : Body4JvTarget := by
  exact jv_of_source_geometry source_axes source_displacements

theorem jw_attempt : Body4JwTarget := by
  exact jw_of_source_axes source_axes

theorem active_joint3_source_columns (q : Q6) (a : Axis) :
    bodyJv (sourceContract q).origins (sourceContract q).axes (3 : Body) a 3 = 0 ∧
    bodyJw (sourceContract q).axes (3 : Body) a 3 =
      vec q (Real.sin (phi q)) 0 (Real.cos (phi q)) a := by
  constructor
  · exact jv_attempt q a 3
  · exact jw_attempt q a 3

-- Prospective axiom inspections only. None has been executed.
#print axioms body4_index
#print axioms body4_com_indices
#print axioms parent_slot
#print axioms active_guard
#print axioms activeJoint_roundtrip
#print axioms lift_zero
#print axioms lift_cross
#print axioms lift_dot_isometry
#print axioms basis_cross
#print axioms frame_origin_prefix
#print axioms frame_axis_prefix
#print axioms step3_translation
#print axioms slot4_translation
#print axioms frame_origin4
#print axioms source_origin_prefix
#print axioms source_axes
#print axioms source_com
#print axioms source_displacements
#print axioms joint3_parallel
#print axioms cross_parallel
#print axioms joint3_cross_zero
#print axioms active_cross_columns
#print axioms inactive
#print axioms active_jv_of_geometry
#print axioms jv_of_source_geometry
#print axioms active_jw_of_axes
#print axioms jw_of_source_axes
#print axioms jv_attempt
#print axioms jw_attempt
#print axioms active_joint3_source_columns

end
end RouteBO1Body4SourceJacobianBridge20260907
