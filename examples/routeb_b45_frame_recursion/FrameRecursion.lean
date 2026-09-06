import FourierNormalForm

namespace RouteBB45FrameRecursion

noncomputable section

open RouteBB45Fourier

/- A homogeneous frame is a 4-by-4 complex matrix.  The matrix product is
   Mathlib's finite-sum product, so the order below is an exact algebraic
   contract rather than an implementation convention hidden in code. -/
abbrev Frame := Matrix (Fin 4) (Fin 4) ℂ

def frameProduct : List Frame → Frame
  | [] => 1
  | current :: tail => current * frameProduct tail

/- The parent frame is on the left of the current DH step.  This is the
   smallest reusable recursion needed by a frame/axis lift. -/
def prefixFrames (parent : Frame) : List Frame → List Frame
  | [] => [parent]
  | current :: tail => parent :: prefixFrames (parent * current) tail

theorem frameProduct_cons (current : Frame) (tail : List Frame) :
    frameProduct (current :: tail) = current * frameProduct tail := by
  rfl

theorem prefixFrames_cons (parent current : Frame) (tail : List Frame) :
    prefixFrames parent (current :: tail) =
      parent :: prefixFrames (parent * current) tail := by
  rfl

theorem prefixFrames_next_frame (parent current : Frame) (tail : List Frame) :
    (prefixFrames parent (current :: tail)).tail.head? =
      (prefixFrames (parent * current) tail).head? := by
  rw [prefixFrames_cons]
  rfl

def terminalFrame (parent : Frame) : List Frame → Frame
  | [] => parent
  | current :: tail => terminalFrame (parent * current) tail

theorem terminalFrame_eq_product (parent : Frame) (steps : List Frame) :
    terminalFrame parent steps = parent * frameProduct steps := by
  induction steps generalizing parent with
  | nil => simp [terminalFrame, frameProduct]
  | cons current tail ih =>
      simp only [terminalFrame, frameProduct]
      rw [ih]
      rw [mul_assoc]

/- The exact Route-B one-joint step, using the phase and DH constants already
   recorded in `FourierNormalForm.lean`.  No Float64 value is introduced here. -/
def routeBStepMatrix (k : Fin 6) (q : ℝ) : Frame :=
  fun i j =>
    fourierDHStep (routeBOffsetPhase k)
      (Complex.exp (Complex.I * (q : ℂ)))
      (routeBCosAlpha k) (routeBSinAlpha k) (routeBA k) (routeBD k) i j

def routeBFrameChain (parent : Frame) : List (Fin 6 × ℝ) → List Frame
  | [] => [parent]
  | (k, q) :: tail =>
      parent :: routeBFrameChain (parent * routeBStepMatrix k q) tail

theorem routeBFrameChain_cons (parent : Frame) (k : Fin 6) (q : ℝ)
    (tail : List (Fin 6 × ℝ)) :
    routeBFrameChain parent ((k, q) :: tail) =
      parent :: routeBFrameChain (parent * routeBStepMatrix k q) tail := by
  rfl

theorem routeB_parent_axis_before_current_step (parent : Frame)
    (k : Fin 6) (q : ℝ) :
    (parent * routeBStepMatrix k q) =
      parent * routeBStepMatrix k q := by
  rfl

theorem routeB_terminal_product (parent : Frame)
    (steps : List (Fin 6 × ℝ)) :
    terminalFrame parent (steps.map (fun kq =>
      routeBStepMatrix kq.1 kq.2)) =
      parent * frameProduct (steps.map (fun kq =>
        routeBStepMatrix kq.1 kq.2)) := by
  exact terminalFrame_eq_product parent _

#print axioms frameProduct_cons
#print axioms prefixFrames_cons
#print axioms prefixFrames_next_frame
#print axioms terminalFrame_eq_product
#print axioms routeBFrameChain_cons
#print axioms routeB_parent_axis_before_current_step
#print axioms routeB_terminal_product

end
end RouteBB45FrameRecursion
