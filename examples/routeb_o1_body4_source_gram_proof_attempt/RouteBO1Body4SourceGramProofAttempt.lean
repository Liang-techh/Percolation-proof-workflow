import RouteBO1Body4SourceGramTargets

set_option autoImplicit false

namespace RouteBO1Body4SourceGramProofAttempt

noncomputable section

open RouteBO1PerBodyExactSource
open RouteBO1PerBodyTraceAdapter
open RouteBO1Body4SourceGramTargets
open RouteBBodySemanticCore
open RouteBSourceContractAdapter
open RouteBSourceContractIndexAdapter
open RouteBFrameSlotAccessor
open RouteBRealDHStep
open RouteBB45Fourier

/-!
EXPERIMENTAL_PROOF_ATTEMPT_UNCOMPILED. No local Lean/Lake execution.
Every target below has a concrete proof script, not a new premise.
Declaration text is NOT evidence that an inhabitant has been elaborated.
Repair this isolated module in a single pinned remote environment; do not
change imported targets/adapters or turn failing children into assumptions.
The endpoint is expected-entry, not the tagged trace fold or h_body_4.
-/

-- A. Scalar leaves. Only the three standard trig API names below are needed.
theorem unit_circle : Body4UnitCircleTarget := by
  intro x
  exact Real.sin_sq_add_cos_sq x

theorem angle_addition : Body4AngleAdditionTarget := by
  intro x y
  exact ⟨Real.sin_add x y, Real.cos_add x y⟩

theorem mixed_trig : Body4MixedTrigTarget := by
  intro x y
  rw [(angle_addition x y).1, (angle_addition x y).2]
  linear_combination Real.cos y * unit_circle x

theorem square_trig : Body4SquareTrigTarget := by
  intro x
  have hc := unit_circle x
  have hd : Real.cos (2 * x) = Real.cos x * Real.cos x -
      Real.sin x * Real.sin x := by
    rw [show 2 * x = x + x by ring]
    exact (angle_addition x x).2
  nlinarith only [hc, hd]

theorem product_trig : Body4ProductTrigTarget := by
  intro x y
  have hm := mixed_trig x y
  have ha : Real.cos (2 * x + y) =
      Real.cos x * Real.cos (x + y) - Real.sin x * Real.sin (x + y) := by
    rw [show 2 * x + y = x + (x + y) by ring]
    exact (angle_addition x (x + y)).2
  linarith only [hm, ha]

-- B. Small finite coordinate calculations; the basis is right-handed.
theorem basis_dot : Body4BasisDotTarget := by
  intro q r t z r' t' z'
  have hc := unit_circle (q 0)
  simp [dot, vec, Fin.sum_univ_succ]
  linear_combination (r * r' + t * t') * hc

theorem basis_cross : Body4BasisCrossTarget := by
  intro q r t z r' t' z'
  have hc := unit_circle (q 0)
  funext a
  fin_cases a <;> simp [cross3, vec] <;>
    first | ring | linear_combination (r * t' - t * r') * hc

theorem dot_zero_left (v : V3) : dot 0 v = 0 := by
  simp [dot]

theorem dot_zero_right (v : V3) : dot v 0 = 0 := by
  simp [dot]

-- C. Frame calculations never unfold the source list or the trace evaluator.
theorem prefix_slots : Body4PrefixSlotsTarget := by
  intro q
  exact ⟨rfl, rfl, rfl, rfl, rfl⟩

theorem prefix_columns : Body4PrefixColumnsTarget := by
  intro q s a
  -- First remote geometry repair point: 4 slots x 3 rows x 4 columns.
  -- Finite products retain the association in prefixFrame.
  fin_cases s <;> fin_cases a <;> refine ⟨?_, ?_, ?_, ?_⟩
  all_goals
    norm_num [routeBFrameSlot, prefixFrame, routeBStepFunction,
      routeBRealStepMatrix, realDHStep, routeBRealCos, routeBRealSin,
      routeBCosAlpha, routeBSinAlpha, routeBA, routeBD,
      RouteBFrameOriginAxis.embed3, Matrix.mul_apply, Fin.sum_univ_succ,
      prefixX, prefixY, prefixZ, prefixO, vec, b, c, d, phi,
      Real.sin_add, Real.cos_add] <;> ring

theorem step3_translation (q : Q6) (k : Fin 4) :
    routeBStepFunction q 3 k 3 =
      if k = 2 then (19 / 100 : ℝ) else if k = 3 then 1 else 0 := by
  fin_cases k <;>
    norm_num [routeBStepFunction, routeBRealStepMatrix, realDHStep,
      routeBRealCos, routeBRealSin, routeBCosAlpha, routeBSinAlpha,
      routeBA, routeBD]

theorem slot4_translation : Body4Slot4TranslationTarget := by
  intro q a
  have h4 : routeBFrameSlot q 4 =
      routeBFrameSlot q 3 * routeBStepFunction q 3 := rfl
  change routeBFrameSlot q 4 (RouteBFrameOriginAxis.embed3 a) 3 = _
  rw [h4, Matrix.mul_apply]
  simp [step3_translation, Fin.sum_univ_succ,
    RouteBFrameOriginAxis.origin, RouteBFrameOriginAxis.zAxis]
  ring

theorem frame_origin_prefix (q : Q6) (s : Fin 4) :
    RouteBFrameOriginAxis.origin
      (routeBFrameSlot q ⟨s.val, Nat.lt_trans s.isLt (by decide)⟩) =
      prefixO q s := by
  funext a
  exact (prefix_columns q s a).2.2.2

theorem frame_axis_prefix (q : Q6) (s : Fin 4) :
    RouteBFrameOriginAxis.zAxis
      (routeBFrameSlot q ⟨s.val, Nat.lt_trans s.isLt (by decide)⟩) =
      prefixZ q s := by
  funext a
  exact (prefix_columns q s a).2.2.1

theorem frame_origin4 (q : Q6) :
    RouteBFrameOriginAxis.origin (routeBFrameSlot q 4) =
      vec q (2 / 25 + b q + (19 / 100) * Real.sin (phi q)) d
        (1 / 10 + c q + (19 / 100) * Real.cos (phi q)) := by
  funext a
  rw [slot4_translation q a, frame_origin_prefix q 3, frame_axis_prefix q 3]
  fin_cases a <;> simp [prefixO, prefixZ, vec] <;> ring

theorem source_origin_prefix (q : Q6) (s : Fin 4) :
    (sourceContract q).origins
      ⟨s.val, Nat.lt_trans s.isLt (by decide)⟩ = prefixO q s := by
  rw [source_origin_function_eq_frame_contract]
  exact frame_origin_prefix q s

theorem source_origins : Body4SourceOriginsTarget := by
  intro q
  refine ⟨source_origin_prefix q 0, source_origin_prefix q 1,
    source_origin_prefix q 2, source_origin_prefix q 3, ?_⟩
  rw [source_origin_function_eq_frame_contract]
  exact frame_origin4 q

theorem source_axes : Body4SourceAxesTarget := by
  intro q j
  rw [source_parent_axis_slot]
  exact frame_axis_prefix q j

theorem com : Body4ComTarget := by
  intro q
  change bodyCom (sourceContract q).origins 3 = _
  rw [source_body4_com_uses_slots_3_4, frame_origin_prefix q 3, frame_origin4]
  funext a
  fin_cases a <;>
    simp [RouteBBodySemanticCore.midpoint, prefixO, vec, aa, pp, e] <;> ring

theorem displacements : Body4DisplacementsTarget := by
  intro q j a
  rw [com, source_origin_prefix q j]
  fin_cases j <;> fin_cases a <;>
    simp [displacement, prefixO, vec, aa, pp, qq] <;> ring

-- D. Active joint 3 is handled by cross, never by the inactive lemma.
theorem inactive : Body4InactiveTarget := by
  intro q a j h
  exact ⟨bodyJv_zero_of_inactive _ _ body4 j a h,
    bodyJw_zero_of_inactive _ body4 j a h⟩

theorem active_jv (q : Q6) (j : Fin 4) (a : Axis) :
    bodyJv (sourceContract q).origins (sourceContract q).axes body4 a
      ⟨j.val, Nat.lt_trans j.isLt (by decide)⟩ =
      vcol q ⟨j.val, Nat.lt_trans j.isLt (by decide)⟩ a := by
  rw [bodyJv_active_formula _ _ _ _ _ (by have hj := j.isLt; dsimp [body4]; omega)]
  have hd : (fun k => bodyCom (sourceContract q).origins body4 k -
      (sourceContract q).origins
        (prevOrigin ⟨j.val, Nat.lt_trans j.isLt (by decide)⟩) k) =
      displacement q j := by
    funext k
    exact displacements q j k
  rw [source_axes q j, hd]
  -- All four branches are active, including j=3 with parallel vectors.
  fin_cases j <;>
    norm_num [prefixZ, displacement, vcol, basis_cross] <;>
    fin_cases a <;> simp [vec] <;> ring

theorem jv : Body4JvTarget := by
  intro q a j
  by_cases h : j.val < 4
  · exact active_jv q ⟨j.val, h⟩ a
  · have hi : 3 < j.val := by omega
    rw [(inactive q a j hi).1]
    fin_cases j <;> norm_num [vcol] at h ⊢

theorem active_jw (q : Q6) (j : Fin 4) (a : Axis) :
    bodyJw (sourceContract q).axes body4 a
      ⟨j.val, Nat.lt_trans j.isLt (by decide)⟩ =
      wcol q ⟨j.val, Nat.lt_trans j.isLt (by decide)⟩ a := by
  rw [bodyJw_active_formula _ _ _ _ (by have hj := j.isLt; dsimp [body4]; omega)]
  rw [source_axes q j]
  fin_cases j <;> rfl

theorem jw : Body4JwTarget := by
  intro q a j
  by_cases h : j.val < 4
  · exact active_jw q ⟨j.val, h⟩ a
  · have hi : 3 < j.val := by omega
    rw [(inactive q a j hi).2]
    fin_cases j <;> norm_num [wcol] at h ⊢

-- E. Complete 6x6 tables, including inactive rows AND columns.
theorem linear_gram : Body4LinearGramTarget := by
  intro q i j
  have hc := unit_circle (phi q)
  fin_cases i <;> fin_cases j <;>
    norm_num [vcol, gv, basis_dot, dot_zero_left, dot_zero_right] <;>
    first | ring | linear_combination e ^ 2 * hc

theorem angular_gram : Body4AngularGramTarget := by
  intro q i j
  have hc := unit_circle (phi q)
  fin_cases i <;> fin_cases j <;>
    norm_num [wcol, gw, basis_dot, dot_zero_left, dot_zero_right] <;>
    first | ring | linear_combination hc

theorem inertia : Body4InertiaTarget := by
  constructor
  · norm_num [routeBMass, body4]
  · intro a b
    simp [routeBInertia, routeBInertiaScalar, body4]

theorem diagonal_angular_sum (q : Q6) (i j : Joint) :
    (∑ a : Axis, ∑ b : Axis,
      wcol q i a * routeBInertia body4 a b * wcol q j b) =
      (1 / 15 : ℝ) * dot (wcol q i) (wcol q j) := by
  -- Nine scalar summands; avoids dependence on a diagonal-matrix API.
  simp [inertia.2, dot, Fin.sum_univ_succ]
  ring

theorem source_gram : Body4SourceGramTarget := by
  intro q i j
  rw [sourceBodyMass_eq_bodyMass]
  unfold bodyMass linkMass
  simp only [jv, jw, inertia.1]
  rw [diagonal_angular_sum]
  change (2 / 5 : ℝ) * dot (vcol q i) (vcol q j) +
    (1 / 15 : ℝ) * dot (wcol q i) (wcol q j) = _
  rw [linear_gram, angular_gram]

-- F. Rational/trigonometric normalization is separate from source semantics.
theorem quadratic_reduction : Body4QuadraticReductionTarget := by
  intro q
  have hx := unit_circle (q 1)
  have hp := unit_circle (phi q)
  have hm := mixed_trig (q 1) (q 2)
  change Real.sin (q 1) * Real.sin (phi q) +
    Real.cos (q 1) * Real.cos (phi q) = Real.cos (q 2) at hm
  constructor
  · dsimp [pp, qq, b, c, e]
    linear_combination (441 / 10000 : ℝ) * hx +
      (361 / 40000 : ℝ) * hp + (399 / 10000 : ℝ) * hm
  · dsimp [pp, qq, b, c, e]
    linear_combination (361 / 40000 : ℝ) * hp + (399 / 20000 : ℝ) * hm

theorem scalar00 : Body4Scalar00Target := by
  intro q
  have hx := square_trig (q 1)
  have hp := square_trig (phi q)
  have hm := product_trig (q 1) (q 2)
  change Real.sin (q 1) * Real.sin (phi q) =
    (Real.cos (q 2) - Real.cos (2 * q 1 + q 2)) / 2 at hm
  have hangle : 2 * phi q = 2 * q 1 + 2 * q 2 := by unfold phi; ring
  rw [hangle] at hp
  norm_num [body_4_piecewise]
  dsimp [aa, b, d, e]
  dsimp only [phi] at hp hm ⊢
  -- These are exactly the coefficients of sin(x)^2, sin(phi)^2,
  -- and sin(x)*sin(phi) in (2/5)*A^2. No opaque trig automation.
  linear_combination (441 / 25000 : ℝ) * hx +
    (361 / 100000 : ℝ) * hp + (399 / 25000 : ℝ) * hm

theorem gram_to_piecewise : Body4GramToPiecewiseTarget := by
  intro q i j
  have h00 := scalar00 q
  have h11 := (quadratic_reduction q).1
  have h12 := (quadratic_reduction q).2
  -- Use the small quadratic lemmas before expanding P and Q.
  fin_cases i <;> fin_cases j <;>
    norm_num only [gv, gw, Fin.reduceFinMk, mul_one, mul_zero, add_zero, zero_add] <;>
    first
    | exact h00
    | (simp only [h11, h12]
       norm_num [body_4_piecewise,
        pp, qq, b, c, d, e, phi] <;> ring)

-- G. No target-valued arguments: these refer to the attempted inhabitants.
theorem expected_entry_handoff : Body4ExpectedEntryHandoffTarget := by
  intro q i j
  exact (source_gram q i j).trans (gram_to_piecewise q i j)

theorem expanded_handoff : Body4ExpandedHandoffTarget := by
  intro q i j
  change bodyMass (sourceContract q).origins (sourceContract q).axes
    3 (routeBMass 3) (routeBInertia 3) i j = body_4_piecewise q i j
  exact expected_entry_handoff q i j

-- For a future remote run. These commands have NOT been executed here.
#print axioms prefix_slots
#print axioms prefix_columns
#print axioms slot4_translation
#print axioms source_origins
#print axioms source_axes
#print axioms com
#print axioms displacements
#print axioms basis_dot
#print axioms basis_cross
#print axioms inactive
#print axioms jv
#print axioms jw
#print axioms linear_gram
#print axioms angular_gram
#print axioms inertia
#print axioms source_gram
#print axioms unit_circle
#print axioms angle_addition
#print axioms mixed_trig
#print axioms square_trig
#print axioms product_trig
#print axioms quadratic_reduction
#print axioms scalar00
#print axioms gram_to_piecewise
#print axioms expected_entry_handoff
#print axioms expanded_handoff

end
end RouteBO1Body4SourceGramProofAttempt
