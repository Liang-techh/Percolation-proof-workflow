import RouteBO1Body5SourceTraceTargets

set_option autoImplicit false

namespace NEW_BODY5_GramTraceSkeleton20260907

noncomputable section

open RouteBO1PerBodyExactSource RouteBO1PerBodyTraceAdapter
open RouteBO1Body5SourceTraceTargets RouteBBodySemanticCore
open RouteBSourceContractAdapter

/-!
OPEN / UNCOMPILED proof skeleton. No declaration in this file has been
parsed, elaborated or kernel checked in this task. Concrete tactic bodies
are repair candidates, not proof receipts.

G3 consumes the ACTUAL source columns as an explicit premise. Reading the
existing G1/G2 attempt does not supply an accepted witness. This file does
not import that attempt, so scalar work can be checked independently later.
G4 concerns only the frozen local columns and frozen piecewise expression.
-/

theorem diagonal_inertia_attempt (u v : V3) :
    (∑ a : Fin 3, ∑ b : Fin 3,
      u a * routeBInertia body5Index a b * v b) =
        (1 / 30 : ℝ) * body5Dot u v := by
  norm_num [routeBInertia, routeBInertiaScalar, body5Index,
    body5Dot, Fin.sum_univ_succ] <;> ring

theorem columns_to_gram_attempt : Body5ColumnsToGramTarget := by
  intro hcols hiso q i j
  rw [sourceBodyMass_eq_bodyMass]
  change (3 / 10 : ℝ) * body5Dot
      (fun a => bodyJv (sourceContract q).origins (sourceContract q).axes body5Index a i)
      (fun a => bodyJv (sourceContract q).origins (sourceContract q).axes body5Index a j) +
    (∑ a : Fin 3, ∑ b : Fin 3,
      bodyJw (sourceContract q).axes body5Index a i *
        routeBInertia body5Index a b *
        bodyJw (sourceContract q).axes body5Index b j) = _
  rw [diagonal_inertia_attempt]
  rw [(hcols q i).1, (hcols q j).1, (hcols q i).2, (hcols q j).2]
  rw [hiso q, hiso q]
  rfl

theorem dot_swap_attempt (u v : V3) : body5Dot u v = body5Dot v u := by
  unfold body5Dot
  apply Finset.sum_congr rfl
  intro a _
  exact mul_comm _ _

theorem gram_swap_attempt (q : Q6) (i j : Fin 6) :
    body5Gram q i j = body5Gram q j i := by
  unfold body5Gram
  rw [dot_swap_attempt (body5VLocal q i), dot_swap_attempt (body5WLocal q i)]

theorem piecewise_swap_attempt (q : Q6) (i j : Fin 6) :
    body_5_piecewise q i j = body_5_piecewise q j i := by
  fin_cases i <;> fin_cases j <;> norm_num [body_5_piecewise]

/- Three scalar leaves avoid expanding DH prefixes or Fourier folds. -/
theorem sin_square_attempt (t : ℝ) :
    Real.sin t ^ 2 = (1 - Real.cos (2 * t)) / 2 := by
  have hu := Real.sin_sq_add_cos_sq t
  have hc := Real.cos_add t t
  rw [show t + t = 2 * t by ring] at hc
  linear_combination (1 / 2 : ℝ) * hu + (1 / 2 : ℝ) * hc

theorem sin_cross_attempt (q : Q6) :
    Real.sin (q 1) * Real.sin (body5Phi q) =
      (Real.cos (q 2) - Real.cos (2 * q 1 + q 2)) / 2 := by
  have hd := Real.cos_sub (body5Phi q) (q 1)
  have ha := Real.cos_add (body5Phi q) (q 1)
  rw [show body5Phi q - q 1 = q 2 by dsimp [body5Phi]; ring] at hd
  rw [show body5Phi q + q 1 = 2 * q 1 + q 2 by dsimp [body5Phi]; ring] at ha
  linear_combination (1 / 2 : ℝ) * ha - (1 / 2 : ℝ) * hd

theorem cos_cross_attempt (q : Q6) :
    Real.cos (q 1) * Real.cos (body5Phi q) +
      Real.sin (q 1) * Real.sin (body5Phi q) = Real.cos (q 2) := by
  have h := Real.cos_sub (body5Phi q) (q 1)
  rw [show body5Phi q - q 1 = q 2 by dsimp [body5Phi]; ring] at h
  linear_combination -h

theorem pq_norm_attempt (q : Q6) :
    body5P q ^ 2 + body5Q q ^ 2 =
      (401 / 5000 : ℝ) + (399 / 5000 : ℝ) * Real.cos (q 2) := by
  have hx := Real.sin_sq_add_cos_sq (q 1)
  have hp := Real.sin_sq_add_cos_sq (body5Phi q)
  have hc := cos_cross_attempt q
  dsimp [body5P, body5Q]
  linear_combination (441 / 10000 : ℝ) * hx +
    (361 / 10000 : ℝ) * hp + (399 / 5000 : ℝ) * hc

theorem pq_projection_attempt (q : Q6) :
    body5P q * Real.cos (body5Phi q) + body5Q q * Real.sin (body5Phi q) =
      (19 / 100 : ℝ) + (21 / 100 : ℝ) * Real.cos (q 2) := by
  have hp := Real.sin_sq_add_cos_sq (body5Phi q)
  have hc := cos_cross_attempt q
  dsimp [body5P, body5Q]
  linear_combination (19 / 100 : ℝ) * hp + (21 / 100 : ℝ) * hc

theorem q3_product_to_sum_attempt : Body5Q3ProductToSumTarget := by
  intro q
  rw [Real.cos_sub, Real.cos_add]
  ring

theorem gram00_attempt (q : Q6) : body5Gram q 0 0 = body_5_piecewise q 0 0 := by
  have hx := sin_square_attempt (q 1)
  have hp := sin_square_attempt (body5Phi q)
  have hc := sin_cross_attempt q
  rw [show 2 * body5Phi q = 2 * q 1 + 2 * q 2 by dsimp [body5Phi]; ring] at hp
  norm_num [body5Gram, body5Dot, body5VLocal, body5WLocal,
    Fin.sum_univ_succ, body_5_piecewise]
  dsimp [body5A]
  change _ = (1441 / 30000 : ℝ) + (63 / 6250) * Real.sin (q 1) +
    (57 / 6250) * Real.sin (body5Phi q) - (1323 / 200000) * Real.cos (2 * q 1) +
    (1197 / 100000) * Real.cos (q 2) - (1197 / 100000) * Real.cos (2 * q 1 + q 2) -
    (1083 / 200000) * Real.cos (2 * q 1 + 2 * q 2)
  linear_combination (1323 / 100000 : ℝ) * hx +
    (1083 / 100000 : ℝ) * hp + (1197 / 50000 : ℝ) * hc

theorem gram11_attempt (q : Q6) : body5Gram q 1 1 = body_5_piecewise q 1 1 := by
  have h := pq_norm_attempt q
  norm_num [body5Gram, body5Dot, body5VLocal, body5WLocal,
    Fin.sum_univ_succ, body_5_piecewise]
  linear_combination (3 / 10 : ℝ) * h

theorem gram12_attempt (q : Q6) : body5Gram q 1 2 = body_5_piecewise q 1 2 := by
  have h := pq_projection_attempt q
  norm_num [body5Gram, body5Dot, body5VLocal, body5WLocal,
    Fin.sum_univ_succ, body_5_piecewise]
  linear_combination (57 / 1000 : ℝ) * h

theorem gram22_attempt (q : Q6) : body5Gram q 2 2 = body_5_piecewise q 2 2 := by
  have h := Real.sin_sq_add_cos_sq (body5Phi q)
  norm_num [body5Gram, body5Dot, body5VLocal, body5WLocal,
    Fin.sum_univ_succ, body_5_piecewise]
  linear_combination (1083 / 100000 : ℝ) * h

theorem gram33_attempt (q : Q6) : body5Gram q 3 3 = body_5_piecewise q 3 3 := by
  have h := Real.sin_sq_add_cos_sq (body5Phi q)
  norm_num [body5Gram, body5Dot, body5VLocal, body5WLocal,
    Fin.sum_univ_succ, body_5_piecewise]
  linear_combination (1 / 30 : ℝ) * h

/- Factor the quartic norm BEFORE applying the two unit-circle identities. -/
theorem w4_norm_attempt (q : Q6) : body5Dot (body5WLocal q 4) (body5WLocal q 4) = 1 := by
  calc
    _ = Real.sin (q 3) ^ 2 *
        (Real.sin (body5Phi q) ^ 2 + Real.cos (body5Phi q) ^ 2) +
          Real.cos (q 3) ^ 2 := by
      norm_num [body5Dot, body5WLocal, Fin.sum_univ_succ] <;> ring
    _ = 1 := by
      rw [Real.sin_sq_add_cos_sq (body5Phi q), mul_one]
      exact Real.sin_sq_add_cos_sq (q 3)

theorem gram44_attempt (q : Q6) : body5Gram q 4 4 = body_5_piecewise q 4 4 := by
  rw [body5Gram, w4_norm_attempt]
  norm_num [body5Dot, body5VLocal, Fin.sum_univ_succ, body_5_piecewise]

theorem gram_upper_attempt (q : Q6) (i j : Fin 6) (hij : i.val ≤ j.val) :
    body5Gram q i j = body_5_piecewise q i j := by
  fin_cases i <;> fin_cases j
  all_goals try omega
  all_goals first
    | exact gram00_attempt q
    | exact gram11_attempt q
    | exact gram12_attempt q
    | exact gram22_attempt q
    | exact gram33_attempt q
    | exact gram44_attempt q
    | (norm_num [body5Gram, body5Dot, body5VLocal, body5WLocal,
        Fin.sum_univ_succ, body_5_piecewise, body5P, body5Phi,
        Real.cos_add, Real.cos_sub]; ring)

theorem gram_to_piecewise_attempt : Body5GramToPiecewiseTarget := by
  intro q i j
  by_cases hij : i.val ≤ j.val
  · exact gram_upper_attempt q i j hij
  · calc
      body5Gram q i j = body5Gram q j i := gram_swap_attempt q i j
      _ = body_5_piecewise q j i := gram_upper_attempt q j i (by omega)
      _ = body_5_piecewise q i j := piecewise_swap_attempt q j i

/- Source-bound output remains CONDITIONAL on G1/G2 columns and isometry.
   It is deliberately not assembled with the uncompiled geometry witness. -/
theorem source_piecewise_conditional_attempt
    (hcols : Body5ColumnsTarget) (hiso : Body5LiftIsometryTarget) :
    h_body_5_expected_entry_target := by
  intro q i j
  exact (columns_to_gram_attempt hcols hiso q i j).trans
    (gram_to_piecewise_attempt q i j)

end
end NEW_BODY5_GramTraceSkeleton20260907
