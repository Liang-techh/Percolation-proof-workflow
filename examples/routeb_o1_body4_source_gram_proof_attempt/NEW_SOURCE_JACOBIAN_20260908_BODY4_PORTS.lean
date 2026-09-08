import RouteBO1Body4SourceGramTargets

set_option autoImplicit false

namespace RouteBO1Body4SourceJacobianPorts20260908

noncomputable section

open RouteBO1PerBodyExactSource
open RouteBO1Body4SourceGramTargets
open RouteBBodySemanticCore
open RouteBSourceContractAdapter

/-!
CONDITIONAL_SOURCE_JACOBIAN_SKELETON_UNCOMPILED; admission=pending.
Independent of earlier proof attempts: only the original targets are imported.
Geometry is an explicit input, NOT an asserted inhabitant or a new axiom.
No source mass, expected-entry, Fourier/trace, or registry theorem is exported.
Reuses the reviewed local index/lift/column scripts from the 20260907 bridge;
isolates them from its unelaborated DH-prefix expansion.
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


/-- Exact open source contract, not a substitute source evaluator.
The two fields must ultimately be proved for the imported sourceContract.
No inhabitant of this structure is supplied by this module. -/
structure SourceGeometry : Prop where
  axes : Body4SourceAxesTarget
  displacements : Body4DisplacementsTarget

/-- Convenient source-level constructor: COM plus all five source origins
suffice for displacement; neither a Gram table nor dot preservation suffices. -/
theorem geometry_of_source_targets
    (hOrigins : Body4SourceOriginsTarget)
    (hAxes : Body4SourceAxesTarget) (hCom : Body4ComTarget) :
    SourceGeometry := by
  refine ⟨hAxes, ?_⟩
  intro q j a
  have ho : ∀ s : Fin 4,
      (sourceContract q).origins (prefixSlot s) = prefixO q s := by
    intro s
    fin_cases s
    · exact (hOrigins q).1
    · exact (hOrigins q).2.1
    · exact (hOrigins q).2.2.1
    · exact (hOrigins q).2.2.2.1
  change bodyCom (sourceContract q).origins body4 a -
    (sourceContract q).origins (prefixSlot j) a = displacement q j a
  rw [hCom q, ho j]
  fin_cases j <;> fin_cases a <;>
    simp [displacement, prefixO, vec, aa, pp, qq] <;> ring

theorem jacobians_of_source_geometry (h : SourceGeometry) :
    Body4JvTarget ∧ Body4JwTarget :=
  ⟨jv_of_source_geometry h.axes h.displacements, jw_of_source_axes h.axes⟩

/-- Human joint 4 (index 3) remains active in BOTH source formulas. -/
theorem joint3_source_columns (h : SourceGeometry) (q : Q6) (a : Axis) :
    bodyJv (sourceContract q).origins (sourceContract q).axes (3 : Body) a 3 = 0 ∧
    bodyJw (sourceContract q).axes (3 : Body) a 3 =
      vec q (Real.sin (phi q)) 0 (Real.cos (phi q)) a := by
  constructor
  · exact (jacobians_of_source_geometry h).1 q a 3
  · exact (jacobians_of_source_geometry h).2 q a 3

/-- Transport a local dot calculation ONLY after source Jacobian binding.
This is not Body4SourceGramTarget: mass/inertia and the Gram tables remain
separate obligations. No second lift is applied to world-coordinate columns. -/
theorem source_column_dots (h : SourceGeometry) (q : Q6) (i j : Joint) :
    dot (fun a => bodyJv (sourceContract q).origins
        (sourceContract q).axes body4 a i)
      (fun a => bodyJv (sourceContract q).origins
        (sourceContract q).axes body4 a j) = dot (vcol q i) (vcol q j) ∧
    dot (fun a => bodyJw (sourceContract q).axes body4 a i)
      (fun a => bodyJw (sourceContract q).axes body4 a j) =
        dot (wcol q i) (wcol q j) := by
  rcases jacobians_of_source_geometry h with ⟨hv, hw⟩
  constructor
  · simp only [hv]
  · simp only [hw]

-- Prospective checks only; not executed locally or remotely.
#print axioms lift_dot_isometry
#print axioms lift_cross
#print axioms inactive
#print axioms geometry_of_source_targets
#print axioms jacobians_of_source_geometry
#print axioms joint3_source_columns
#print axioms source_column_dots

end
end RouteBO1Body4SourceJacobianPorts20260908
