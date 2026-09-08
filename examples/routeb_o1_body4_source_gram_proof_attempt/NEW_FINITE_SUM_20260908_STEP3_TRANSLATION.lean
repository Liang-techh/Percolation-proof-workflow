import RouteBO1Body4SourceGramTargets

set_option autoImplicit false

namespace RouteBO1Body4FiniteSum20260908

noncomputable section

open RouteBO1PerBodyExactSource
open RouteBO1Body4SourceGramTargets
open RouteBFrameSlotAccessor
open RouteBRealDHStep

/-!
EXACT_REAL_FINITE_SUM_CANDIDATE_UNCOMPILED; admission=pending.
No old proof-attempt imports. No geometry premise or copied constant table.
The four step entries are reduced from the imported exact source definitions.
Snapshot hashes live in the paired review; hashing is not a semantic proof.
No claim about Julia Float64 execution or a mass/Gram theorem is made here.
-/

/-- Human step 4 = zero-based step 3; column 3 is homogeneous translation. -/
theorem step3_column (q : Q6) :
    routeBStepFunction q 3 0 3 = 0 ∧
    routeBStepFunction q 3 1 3 = 0 ∧
    routeBStepFunction q 3 2 3 = (19 / 100 : ℝ) ∧
    routeBStepFunction q 3 3 3 = 1 := by
  norm_num [routeBStepFunction, routeBRealStepMatrix, realDHStep,
    routeBRealCos, routeBRealSin, RouteBB45Fourier.routeBA,
    RouteBB45Fourier.routeBD]

/-- Association and multiplication order are definitionally the source order. -/
theorem slot4_product (q : Q6) :
    routeBFrameSlot q 4 = routeBFrameSlot q 3 * routeBStepFunction q 3 := rfl

/-- Expose all four summands BEFORE substituting the step entries. -/
theorem product_column_four_terms (F T : F4) (r : Fin 4) :
    (F * T) r 3 =
      F r 0 * T 0 3 + F r 1 * T 1 3 +
      F r 2 * T 2 3 + F r 3 * T 3 3 := by
  rw [Matrix.mul_apply]
  simp [Fin.sum_univ_succ, add_assoc]

/-- This generic row identity applies to all three spatial rows, without
expanding F3 rotation or assuming that F3 is orthogonal/homogeneous. -/
theorem source_row_four_terms (q : Q6) (r : Fin 4) :
    routeBFrameSlot q 4 r 3 =
      routeBFrameSlot q 3 r 0 * 0 + routeBFrameSlot q 3 r 1 * 0 +
      routeBFrameSlot q 3 r 2 * (19 / 100 : ℝ) +
      routeBFrameSlot q 3 r 3 * 1 := by
  rw [slot4_product, product_column_four_terms]
  rcases step3_column q with ⟨h0, h1, h2, h3⟩
  rw [h0, h1, h2, h3]

theorem source_row_translation (q : Q6) (r : Fin 4) :
    routeBFrameSlot q 4 r 3 = routeBFrameSlot q 3 r 3 +
      (19 / 100 : ℝ) * routeBFrameSlot q 3 r 2 := by
  rw [source_row_four_terms]
  ring

/-- Explicit x/y/z output fields; the fourth homogeneous row is not required. -/
theorem spatial_translation_fields (q : Q6) :
    routeBFrameSlot q 4 0 3 = routeBFrameSlot q 3 0 3 +
      (19 / 100 : ℝ) * routeBFrameSlot q 3 0 2 ∧
    routeBFrameSlot q 4 1 3 = routeBFrameSlot q 3 1 3 +
      (19 / 100 : ℝ) * routeBFrameSlot q 3 1 2 ∧
    routeBFrameSlot q 4 2 3 = routeBFrameSlot q 3 2 3 +
      (19 / 100 : ℝ) * routeBFrameSlot q 3 2 2 :=
  ⟨source_row_translation q 0, source_row_translation q 1,
    source_row_translation q 2⟩

/-- Exact original target type, with a candidate proof body, not a new premise.
Still NOT an established inhabitant until this module/imports are elaborated. -/
theorem slot4_translation_attempt : Body4Slot4TranslationTarget := by
  intro q a
  change routeBFrameSlot q 4 (RouteBFrameOriginAxis.embed3 a) 3 =
    routeBFrameSlot q 3 (RouteBFrameOriginAxis.embed3 a) 3 +
      (19 / 100 : ℝ) *
        routeBFrameSlot q 3 (RouteBFrameOriginAxis.embed3 a) 2
  exact source_row_translation q (RouteBFrameOriginAxis.embed3 a)

-- Future inspections only. No commands below have been executed.
#print axioms step3_column
#print axioms slot4_product
#print axioms product_column_four_terms
#print axioms source_row_four_terms
#print axioms spatial_translation_fields
#print axioms slot4_translation_attempt

end
end RouteBO1Body4FiniteSum20260908
