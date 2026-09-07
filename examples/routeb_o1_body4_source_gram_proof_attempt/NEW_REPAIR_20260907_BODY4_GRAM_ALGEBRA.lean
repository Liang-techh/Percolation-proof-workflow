import RouteBO1Body4SourceGramTargets

set_option autoImplicit false

namespace RouteBO1Body4SourceGramRepair20260907

noncomputable section

-- Only these two namespaces are opened: Q6/Joint/Axis come from ExactSource,
-- and V3/dot/vec come from Targets. In particular, V3 is a vector, not Fin 3.
open RouteBO1PerBodyExactSource
open RouteBO1Body4SourceGramTargets

/-!
EXPERIMENTAL_REPAIR_UNCOMPILED. No Lean/Lake execution or kernel evidence.
This module imports the original targets, NOT the old proof-attempt module.
The five target declarations retain their original types. The sixth theorem
generalizes the old diagonal_angular_sum helper to arbitrary vectors.
No source Jacobian or terminal handoff is asserted in this module.
-/

/-- Repair 1: fix the finite sum shape before scalar ring normalization. -/
theorem basis_dot : Body4BasisDotTarget := by
  intro q r t z r' t' z'
  have expand (u v : V3) :
      dot u v = u 0 * v 0 + u 1 * v 1 + u 2 * v 2 := by
    simp [dot, Fin.sum_univ_succ, add_assoc]
  rw [expand]
  change
    (r * Real.cos (q 0) - t * Real.sin (q 0)) *
        (r' * Real.cos (q 0) - t' * Real.sin (q 0)) +
      (r * Real.sin (q 0) + t * Real.cos (q 0)) *
        (r' * Real.sin (q 0) + t' * Real.cos (q 0)) + z * z' =
      r * r' + t * t' + z * z'
  calc
    _ = (r * r' + t * t') *
        (Real.sin (q 0) ^ 2 + Real.cos (q 0) ^ 2) + z * z' := by ring
    _ = r * r' + t * t' + z * z' := by
      rw [Real.sin_sq_add_cos_sq (q 0)]
      ring

/-- Repair 2: each cross component has an explicit scalar goal. -/
theorem basis_cross : Body4BasisCrossTarget := by
  intro q r t z r' t' z'
  funext a
  fin_cases a
  · change
      (r * Real.sin (q 0) + t * Real.cos (q 0)) * z' -
          z * (r' * Real.sin (q 0) + t' * Real.cos (q 0)) =
        (t * z' - z * t') * Real.cos (q 0) -
          (z * r' - r * z') * Real.sin (q 0)
    ring
  · change
      z * (r' * Real.cos (q 0) - t' * Real.sin (q 0)) -
          (r * Real.cos (q 0) - t * Real.sin (q 0)) * z' =
        (t * z' - z * t') * Real.sin (q 0) +
          (z * r' - r * z') * Real.cos (q 0)
    ring
  · change
      (r * Real.cos (q 0) - t * Real.sin (q 0)) *
          (r' * Real.sin (q 0) + t' * Real.cos (q 0)) -
        (r * Real.sin (q 0) + t * Real.cos (q 0)) *
          (r' * Real.cos (q 0) - t' * Real.sin (q 0)) = r * t' - t * r'
    calc
      _ = (r * t' - t * r') *
          (Real.sin (q 0) ^ 2 + Real.cos (q 0) ^ 2) := by ring
      _ = r * t' - t * r' := by
        rw [Real.sin_sq_add_cos_sq (q 0)]
        ring

/-- Repair 3: reduce the table, then the basis, then the unique trig cell. -/
theorem linear_gram : Body4LinearGramTarget := by
  intro q i j
  -- The backward rewrite below has vector type; it cannot rewrite scalar 0.
  have hzero : vec q 0 0 0 = (0 : V3) := by
    funext a
    fin_cases a <;> simp [vec]
  fin_cases i <;> fin_cases j
  all_goals
    dsimp only [vcol, gv]
    simp only [← hzero, basis_dot]
    try ring
  -- Only (i,j)=(2,2) needs the unit-circle identity. Keep e opaque.
  calc
    _ = e ^ 2 * (Real.sin (phi q) ^ 2 + Real.cos (phi q) ^ 2) := by ring
    _ = e ^ 2 := by
      rw [Real.sin_sq_add_cos_sq (phi q)]
      ring

/-- Repair 4: all 36 entries, retaining the active joint-3 angular column. -/
theorem angular_gram : Body4AngularGramTarget := by
  intro q i j
  have hzero : vec q 0 0 0 = (0 : V3) := by
    funext a
    fin_cases a <;> simp [vec]
  fin_cases i <;> fin_cases j
  all_goals
    dsimp only [wcol, gw]
    simp only [← hzero, basis_dot]
    try ring
  -- Only (i,j)=(3,3) remains. The (0,3)/(3,0) cos terms were kept above.
  calc
    _ = Real.sin (phi q) ^ 2 + Real.cos (phi q) ^ 2 := by ring
    _ = 1 := Real.sin_sq_add_cos_sq (phi q)

/-- Repair 5: the body index and inertia-entry type are explicit. -/
theorem inertia : Body4InertiaTarget := by
  change routeBMass (3 : Body) = (2 / 5 : ℝ) ∧
    ∀ row col : Fin 3,
      routeBInertia (3 : Body) row col =
        if row = col then (1 / 15 : ℝ) else 0
  constructor
  · norm_num [routeBMass]
  · intro row col
    change (if row = col then routeBInertiaScalar (3 : Body) else 0) =
      if row = col then (1 / 15 : ℝ) else 0
    norm_num [routeBInertiaScalar]

/-- Repair 6: diagonal contraction for arbitrary vectors, without a matrix API.
Specialize with u := wcol q i and v := wcol q j for the old helper's type. -/
theorem diagonal_angular_sum (u v : V3) :
    (∑ row : Fin 3, ∑ col : Fin 3,
      u row * routeBInertia body4 row col * v col) =
      (1 / 15 : ℝ) * dot u v := by
  have hI : ∀ row col : Fin 3,
      routeBInertia body4 row col =
        if row = col then (1 / 15 : ℝ) else 0 := inertia.2
  calc
    _ = ∑ row : Fin 3, (1 / 15 : ℝ) * (u row * v row) := by
      apply Finset.sum_congr rfl
      intro row _hrow
      calc
        (∑ col : Fin 3, u row * routeBInertia body4 row col * v col) =
            ∑ col : Fin 3,
              if col = row then (1 / 15 : ℝ) * (u row * v row) else 0 := by
          apply Finset.sum_congr rfl
          intro col _hcol
          rw [hI row col]
          by_cases h : col = row
          · subst col
            simp only [if_pos rfl]
            ring
          · simp [h, Ne.symm h]
        _ = (1 / 15 : ℝ) * (u row * v row) := by simp
    _ = (1 / 15 : ℝ) * dot u v := by
      simp only [dot, Finset.mul_sum]

-- Prospective checks only: these commands have not been run.
#print axioms basis_dot
#print axioms basis_cross
#print axioms linear_gram
#print axioms angular_gram
#print axioms inertia
#print axioms diagonal_angular_sum

end
end RouteBO1Body4SourceGramRepair20260907
