import FramePrefixIndex

set_option autoImplicit false

namespace RouteBFrameSlotAccessor

noncomputable section

open RouteBFrameOriginAxis
open RouteBFramePrefixIndex
open RouteBRealDHStep

abbrev RealFrame := Matrix (Fin 4) (Fin 4) ℝ

/- Fixed seven-slot accessor for the source frame list.  The multiplication
   shape deliberately matches `prefix6`, so slot proofs are structural and do
   not ask simp to normalize Matrix multiplication. -/
def prefixFrame (s : Fin 6 → RealFrame) (i : Fin 7) : RealFrame :=
  match i.val with
  | 0 => 1
  | 1 => 1 * s 0
  | 2 => (1 * s 0) * s 1
  | 3 => ((1 * s 0) * s 1) * s 2
  | 4 => (((1 * s 0) * s 1) * s 2) * s 3
  | 5 => ((((1 * s 0) * s 1) * s 2) * s 3) * s 4
  | 6 => (((((1 * s 0) * s 1) * s 2) * s 3) * s 4) * s 5
  | _ => 1

theorem prefixFrame_slot (s : Fin 6 → RealFrame) (i : Fin 7) :
    (prefix6 s).getD i.val (0 : RealFrame) = prefixFrame s i := by
  fin_cases i <;> rfl

def routeBStepFunction (q : Fin 6 → ℝ) : Fin 6 → RealFrame :=
  fun k => routeBRealStepMatrix k (q k)

def routeBFrameSlot (q : Fin 6 → ℝ) (i : Fin 7) : RealFrame :=
  prefixFrame (routeBStepFunction q) i

theorem routeB_source_frame_slot (q : Fin 6 → ℝ) (i : Fin 7) :
    (routeBSourceFrames q).getD i.val (0 : RealFrame) = routeBFrameSlot q i := by
  rw [source_frames_explicit]
  exact prefixFrame_slot (routeBStepFunction q) i

theorem routeB_source_origin_slot (q : Fin 6 → ℝ) (i : Fin 7) :
    (routeBSourceOrigins q).getD i.val (0 : Vec3) =
      origin (routeBFrameSlot q i) := by
  rw [show routeBSourceOrigins q =
      (routeBSourceFrames q).map origin from rfl]
  rw [source_frames_explicit]
  fin_cases i <;> rfl

theorem routeB_source_axis_slot (q : Fin 6 → ℝ) (i : Fin 7) :
    (routeBSourceAxes q).getD i.val (0 : Vec3) =
      zAxis (routeBFrameSlot q i) := by
  rw [show routeBSourceAxes q =
      (routeBSourceFrames q).map zAxis from rfl]
  rw [source_frames_explicit]
  fin_cases i <;> rfl

#print axioms prefixFrame_slot
#print axioms routeB_source_frame_slot
#print axioms routeB_source_origin_slot
#print axioms routeB_source_axis_slot

end
end RouteBFrameSlotAccessor
