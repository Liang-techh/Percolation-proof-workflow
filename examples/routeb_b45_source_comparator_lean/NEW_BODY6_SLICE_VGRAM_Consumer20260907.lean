import NEW_BODY6_SLICE_VGRAM_Tail20260907
import NEW_BODY6_SLICE_STEP6_Bridge20260907

set_option autoImplicit false

namespace NEW_BODY6_SLICE_VGRAM_Consumer20260907

noncomputable section

open NEW_BODY6_SLICE_VGRAM_Source20260907 NEW_BODY6_SLICE_VGRAM_Tail20260907
open RouteBO1PerBodyExactSource

/- UNCOMPILED final attachment to the earlier actual endpoint/center attempt.
   Core/Source/Tail do not depend on this file or any Fourier row data. -/
theorem center_offset_attempt : CenterOffsetTarget := by
  intro q a
  exact congrFun (NEW_BODY6_SLICE_STEP6_Bridge20260907.source_center_attempt q) a

theorem front_tail_block_attempt (q : Q6) :
    sourceBodyMass q (5 : Fin 6) 3 3 =
      (1 / 60 : ℝ) + (147 / 800000 : ℝ) * Real.sin (q 4) ^ 2 ∧
    sourceBodyMass q (5 : Fin 6) 4 4 = (40441 / 2400000 : ℝ) ∧
    sourceBodyMass q (5 : Fin 6) 3 4 = 0 ∧
    sourceBodyMass q (5 : Fin 6) 4 3 = 0 := by
  exact ⟨source_mass33_attempt center_offset_attempt q,
    source_mass44_attempt center_offset_attempt q,
    source_mass34_zero_attempt center_offset_attempt q,
    source_mass43_zero_attempt center_offset_attempt q⟩

/- No AllEntriesGramFourierTarget, EmptyFourierTarget, SourceBindingTarget,
   h_body_6, registry or coverage witness is supplied here. -/

end
end NEW_BODY6_SLICE_VGRAM_Consumer20260907
