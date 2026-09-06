import FrameOriginAxis

set_option autoImplicit false

namespace RouteBFramePrefixIndex

noncomputable section

open RouteBFrameOriginAxis
open RouteBRealDHStep

abbrev RealFrame := Matrix (Fin 4) (Fin 4) ℝ

def step (q : Fin 6 → ℝ) (k : Fin 6) : RealFrame :=
  routeBRealStepMatrix k (q k)

/- The generic seven-frame prefix.  Keeping the six steps abstract is
   important: the list theorem should not unfold any DH matrix entries. -/
def prefix6 (s : Fin 6 → RealFrame) : List RealFrame :=
  [1,
   1 * s 0,
   (1 * s 0) * s 1,
   ((1 * s 0) * s 1) * s 2,
   (((1 * s 0) * s 1) * s 2) * s 3,
   ((((1 * s 0) * s 1) * s 2) * s 3) * s 4,
   (((((1 * s 0) * s 1) * s 2) * s 3) * s 4) * s 5]

theorem finRange6_map (s : Fin 6 → RealFrame) :
    (List.finRange 6).map s = [s 0, s 1, s 2, s 3, s 4, s 5] := by
  simp [List.finRange, List.map]

def explicitFrames (q : Fin 6 → ℝ) : List RealFrame :=
  prefix6 (fun k => step q k)

theorem source_frames_prefix6 (s : Fin 6 → RealFrame) :
    sourceFrames (1 : RealFrame) ((List.finRange 6).map s) = prefix6 s := by
  rw [finRange6_map]
  rfl

theorem source_frames_explicit (q : Fin 6 → ℝ) :
    routeBSourceFrames q = explicitFrames q := by
  change sourceFrames (1 : RealFrame)
      ((List.finRange 6).map (fun k => routeBRealStepMatrix k (q k))) =
    prefix6 (fun k => routeBRealStepMatrix k (q k))
  exact source_frames_prefix6 _

theorem source_frames_length_explicit (q : Fin 6 → ℝ) :
    (explicitFrames q).length = 7 := by
  simp [explicitFrames, prefix6]

theorem source_frame_zero (q : Fin 6 → ℝ) :
    (explicitFrames q).head? = some (1 : RealFrame) := by
  simp [explicitFrames, prefix6]

theorem source_frame_one (q : Fin 6 → ℝ) :
    (explicitFrames q).tail.head? = some (1 * step q 0) := by
  rfl

theorem source_frame_two (q : Fin 6 → ℝ) :
    ((explicitFrames q).drop 2).head? = some ((1 * step q 0) * step q 1) := by
  rfl

theorem source_frame_last (q : Fin 6 → ℝ) :
    (explicitFrames q).getLast? =
      some (((((1 * step q 0) * step q 1) * step q 2) * step q 3) * step q 4) * step q 5) := by
  rfl

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
