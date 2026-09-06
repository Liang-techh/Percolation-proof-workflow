import FrameOriginAxis

set_option autoImplicit false

namespace RouteBFramePrefixIndex

noncomputable section

open RouteBFrameOriginAxis
open RouteBRealDHStep

abbrev RealFrame := Matrix (Fin 4) (Fin 4) ℝ

def step (q : Fin 6 → ℝ) (k : Fin 6) : RealFrame :=
  routeBRealStepMatrix k (q k)

/- The seven source frames written as a finite prefix list.  This explicit
   form is useful for small indexed body leaves and avoids putting a dependent
   List.length proof in every downstream theorem. -/
def explicitFrames (q : Fin 6 → ℝ) : List RealFrame :=
  [1,
   step q 0,
   step q 0 * step q 1,
   (step q 0 * step q 1) * step q 2,
   ((step q 0 * step q 1) * step q 2) * step q 3,
   (((step q 0 * step q 1) * step q 2) * step q 3) * step q 4,
   ((((step q 0 * step q 1) * step q 2) * step q 3) * step q 4) * step q 5]

theorem source_frames_explicit (q : Fin 6 → ℝ) :
    routeBSourceFrames q = explicitFrames q := by
  simp [routeBSourceFrames, routeBRealSteps, sourceFrames,
    explicitFrames, step]

theorem source_frames_length_explicit (q : Fin 6 → ℝ) :
    (explicitFrames q).length = 7 := by
  simp [explicitFrames]

theorem source_frame_zero (q : Fin 6 → ℝ) :
    (explicitFrames q).head? = some (1 : RealFrame) := by
  rfl

theorem source_frame_one (q : Fin 6 → ℝ) :
    (explicitFrames q).tail.head? = some (step q 0) := by
  rfl

theorem source_frame_two (q : Fin 6 → ℝ) :
    (explicitFrames q).drop 2 |>.head? = some (step q 0 * step q 1) := by
  rfl

theorem source_frame_last (q : Fin 6 → ℝ) :
    (explicitFrames q).getLast? =
      some (((((step q 0 * step q 1) * step q 2) * step q 3) * step q 4) * step q 5) := by
  simp [explicitFrames]

theorem explicit_frames_are_source_projections (q : Fin 6 → ℝ) :
    (explicitFrames q).map origin = routeBSourceOrigins q ∧
    (explicitFrames q).map zAxis = routeBSourceAxes q := by
  constructor
  · rw [← source_frames_explicit q]
    rfl
  · rw [← source_frames_explicit q]
    rfl

#print axioms source_frames_explicit
#print axioms source_frames_length_explicit
#print axioms source_frame_zero
#print axioms source_frame_one
#print axioms source_frame_two
#print axioms source_frame_last
#print axioms explicit_frames_are_source_projections

end
end RouteBFramePrefixIndex
