import RealDHStep

set_option autoImplicit false

namespace RouteBFrameOriginAxis

noncomputable section

open RouteBRealDHStep

abbrev RealFrame := Matrix (Fin 4) (Fin 4) ℝ
abbrev Vec3 := Fin 3 → ℝ

def embed3 (i : Fin 3) : Fin 4 :=
  ⟨i.1, Nat.lt_trans i.2 (by decide)⟩

def origin (F : RealFrame) : Vec3 := fun i => F (embed3 i) 3

def zAxis (F : RealFrame) : Vec3 := fun i => F (embed3 i) 2

/- This is the source-level frame list: the current parent is recorded first,
   then the current DH step is multiplied on the right before recursion. -/
def sourceFrames (parent : RealFrame) : List RealFrame → List RealFrame
  | [] => [parent]
  | current :: tail => parent :: sourceFrames (parent * current) tail

def sourceOrigins (parent : RealFrame) : List RealFrame → List Vec3
  | [] => [origin parent]
  | current :: tail => origin parent :: sourceOrigins (parent * current) tail

def sourceAxes (parent : RealFrame) : List RealFrame → List Vec3
  | [] => [zAxis parent]
  | current :: tail => zAxis parent :: sourceAxes (parent * current) tail

def sourceOriginArray (parent : RealFrame) (steps : List RealFrame) : List Vec3 :=
  (sourceFrames parent steps).map origin

def sourceAxisArray (parent : RealFrame) (steps : List RealFrame) : List Vec3 :=
  (sourceFrames parent steps).map zAxis

theorem sourceFrames_cons (parent current : RealFrame) (tail : List RealFrame) :
    sourceFrames parent (current :: tail) =
      parent :: sourceFrames (parent * current) tail := by
  rfl

theorem sourceOrigins_cons (parent current : RealFrame) (tail : List RealFrame) :
    sourceOrigins parent (current :: tail) =
      origin parent :: sourceOrigins (parent * current) tail := by
  rfl

theorem sourceAxes_cons (parent current : RealFrame) (tail : List RealFrame) :
    sourceAxes parent (current :: tail) =
      zAxis parent :: sourceAxes (parent * current) tail := by
  rfl

theorem sourceOriginArray_eq_sourceOrigins (parent : RealFrame)
    (steps : List RealFrame) :
    sourceOriginArray parent steps = sourceOrigins parent steps := by
  induction steps generalizing parent with
  | nil => rfl
  | cons current tail ih =>
      simp only [sourceOriginArray, sourceFrames, List.map_cons,
        sourceOrigins]
      exact congrArg (fun xs => origin parent :: xs) (ih (parent * current))

theorem sourceAxisArray_eq_sourceAxes (parent : RealFrame)
    (steps : List RealFrame) :
    sourceAxisArray parent steps = sourceAxes parent steps := by
  induction steps generalizing parent with
  | nil => rfl
  | cons current tail ih =>
      simp only [sourceAxisArray, sourceFrames, List.map_cons, sourceAxes]
      exact congrArg (fun xs => zAxis parent :: xs) (ih (parent * current))

theorem parent_axis_recorded_before_current (parent current : RealFrame)
    (tail : List RealFrame) :
    (sourceAxisArray parent (current :: tail)).head? = some (zAxis parent) := by
  rfl

theorem parent_origin_recorded_before_current (parent current : RealFrame)
    (tail : List RealFrame) :
    (sourceOriginArray parent (current :: tail)).head? = some (origin parent) := by
  rfl

theorem current_step_changes_parent_before_recursion (parent current : RealFrame)
    (tail : List RealFrame) :
    (sourceFrames parent (current :: tail)).tail =
      sourceFrames (parent * current) tail := by
  rfl

theorem sourceFrames_length (parent : RealFrame) (steps : List RealFrame) :
    (sourceFrames parent steps).length = steps.length + 1 := by
  induction steps generalizing parent with
  | nil => rfl
  | cons current tail ih =>
      simp only [sourceFrames, List.length_cons]
      rw [ih (parent * current)]
      omega

def routeBRealSteps (q : Fin 6 → ℝ) : List RealFrame :=
  (List.finRange 6).map (fun k => routeBRealStepMatrix k (q k))

def routeBSourceFrames (q : Fin 6 → ℝ) : List RealFrame :=
  sourceFrames (1 : RealFrame) (routeBRealSteps q)

def routeBSourceOrigins (q : Fin 6 → ℝ) : List Vec3 :=
  sourceOriginArray (1 : RealFrame) (routeBRealSteps q)

def routeBSourceAxes (q : Fin 6 → ℝ) : List Vec3 :=
  sourceAxisArray (1 : RealFrame) (routeBRealSteps q)

theorem routeB_source_origins_semantics (q : Fin 6 → ℝ) :
    routeBSourceOrigins q =
      (routeBSourceFrames q).map origin := by
  rfl

theorem routeB_source_axes_semantics (q : Fin 6 → ℝ) :
    routeBSourceAxes q =
      (routeBSourceFrames q).map zAxis := by
  rfl

theorem routeB_first_axis_is_world_z (q : Fin 6 → ℝ) :
    (routeBSourceAxes q).head? = some (zAxis (1 : RealFrame)) := by
  rfl

theorem routeB_first_origin_is_world_origin (q : Fin 6 → ℝ) :
    (routeBSourceOrigins q).head? = some (origin (1 : RealFrame)) := by
  rfl

theorem routeB_six_steps_have_seven_frames (q : Fin 6 → ℝ) :
    (routeBSourceFrames q).length = 7 := by
  rw [sourceFrames_length]
  simp [routeBRealSteps]

#print axioms sourceFrames_cons
#print axioms sourceOrigins_cons
#print axioms sourceAxes_cons
#print axioms sourceOriginArray_eq_sourceOrigins
#print axioms sourceAxisArray_eq_sourceAxes
#print axioms parent_axis_recorded_before_current
#print axioms parent_origin_recorded_before_current
#print axioms current_step_changes_parent_before_recursion
#print axioms routeB_source_origins_semantics
#print axioms routeB_source_axes_semantics
#print axioms routeB_first_axis_is_world_z
#print axioms routeB_first_origin_is_world_origin
#print axioms routeB_six_steps_have_seven_frames

end
end RouteBFrameOriginAxis
