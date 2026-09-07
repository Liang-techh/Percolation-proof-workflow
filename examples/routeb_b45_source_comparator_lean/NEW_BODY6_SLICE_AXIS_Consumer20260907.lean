import NEW_BODY6_SLICE_AXIS_Geometry20260907
import NEW_BODY6_SLICE_STEP6_DataLeaf20260907

set_option autoImplicit false

namespace NEW_BODY6_SLICE_AXIS_Consumer20260907

noncomputable section

open NEW_BODY6_SLICE_AXIS_Core20260907 NEW_BODY6_SLICE_AXIS_Geometry20260907
open NEW_BODY6_SLICE_20260907 NEW_BODY6_SLICE_STEP6_Bridge20260907
open NEW_BODY6_SLICE_STEP6_DataLeaf20260907 RouteBO1PerBodyExactSource

/- UNCOMPILED consumer attachment. Geometry has no dependency on this file,
   the 610-row data or the Fourier fold. No coverage/registry object is created. -/

theorem source_axis_dot_target_attempt : SourceAxisDotTarget := by
  intro q i
  simpa [dotResult, phi, sixthAxisDot] using source_dot_all_attempt q i

theorem sixth_source_slice_attempt :
    ∀ q i, sourceBodyMass q (5 : Fin 6) i (5 : Fin 6) =
      sliceEvaluator q i (5 : Fin 6) :=
  source_sixth_column_with_axis_premise_attempt source_axis_dot_target_attempt

theorem sixth_source_diagonal_attempt (q : Q6) :
    sourceBodyMass q (5 : Fin 6) (5 : Fin 6) (5 : Fin 6) = (1 / 60 : ℝ) := by
  have h := NEW_BODY6_SLICE_20260907.source_sixth_column_attempt
    source_gram_attempt source_axis_dot_target_attempt q (5 : Fin 6)
  simpa [sixthColumnFormula, sixthAxisDot] using h

/- The new sixth-column attempt does not fill either of these premises.
   All 36 entries and the four-entry zero complement remain explicit. -/
theorem full_source_boundary_attempt
    (hall : AllEntriesGramFourierTarget) (hzero : EmptyFourierTarget) :
    SourceBindingTarget ∧
      (∀ q i j, EmptyEntry i j → sourceBodyMass q (5 : Fin 6) i j = 0) :=
  global_source_and_zero_seam_attempt hall hzero

end
end NEW_BODY6_SLICE_AXIS_Consumer20260907
