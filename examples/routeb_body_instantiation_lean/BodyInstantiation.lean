import BodyMass
import FrameOriginAxis

set_option autoImplicit false

namespace RouteBBodyInstantiation

noncomputable section

open RouteBFrameOriginAxis
open RouteBBodyMass
open RouteBMassFunctional

abbrev Vec3 := Fin 3 → ℝ
abbrev JMat := Fin 3 → Fin 6 → ℝ
abbrev IMat := Fin 3 → Fin 3 → ℝ

def routeBFrameAt (q : Fin 6 → ℝ) (i : Fin 7) : RealFrame :=
  match i.val with
  | 0 => 1
  | 1 => routeBRealStepMatrix 0 (q 0)
  | 2 => routeBRealStepMatrix 0 (q 0) *
      routeBRealStepMatrix 1 (q 1)
  | 3 => (routeBRealStepMatrix 0 (q 0) *
      routeBRealStepMatrix 1 (q 1)) *
      routeBRealStepMatrix 2 (q 2)
  | 4 => ((routeBRealStepMatrix 0 (q 0) *
      routeBRealStepMatrix 1 (q 1)) *
      routeBRealStepMatrix 2 (q 2)) *
      routeBRealStepMatrix 3 (q 3)
  | 5 => (((routeBRealStepMatrix 0 (q 0) *
      routeBRealStepMatrix 1 (q 1)) *
      routeBRealStepMatrix 2 (q 2)) *
      routeBRealStepMatrix 3 (q 3)) *
      routeBRealStepMatrix 4 (q 4)
  | 6 => ((((routeBRealStepMatrix 0 (q 0) *
      routeBRealStepMatrix 1 (q 1)) *
      routeBRealStepMatrix 2 (q 2)) *
      routeBRealStepMatrix 3 (q 3)) *
      routeBRealStepMatrix 4 (q 4)) *
      routeBRealStepMatrix 5 (q 5)
  | _ => 1

def routeBOrigins (q : Fin 6 → ℝ) : Fin 7 → Vec3 :=
  fun i => origin (routeBFrameAt q i)

def jointFrameIndex (j : Fin 6) : Fin 7 :=
  ⟨j.val, by omega⟩

def routeBAxes (q : Fin 6 → ℝ) : Fin 6 → Vec3 :=
  fun j => zAxis (routeBFrameAt q (jointFrameIndex j))

def routeBBodyCom (q : Fin 6 → ℝ) (body : Fin 6) : Vec3 :=
  bodyCom (routeBOrigins q) body

def routeBBodyJv (q : Fin 6 → ℝ) (body : Fin 6) : JMat :=
  bodyJv (routeBOrigins q) (routeBAxes q) body

def routeBBodyJw (q : Fin 6 → ℝ) (body : Fin 6) : JMat :=
  bodyJw (routeBAxes q) body

def routeBBodyMass (q : Fin 6 → ℝ) (body : Fin 6)
    (mass : ℝ) (inertia : IMat) : Mat 6 6 :=
  bodyMass (routeBOrigins q) (routeBAxes q) body mass inertia

theorem routeB_frame_count (q : Fin 6 → ℝ) :
    (routeBSourceFrames q).length = 7 := by
  exact routeB_six_steps_have_seven_frames q

theorem routeB_body_com_midpoint (q : Fin 6 → ℝ) (body : Fin 6) :
    routeBBodyCom q body =
      midpoint (routeBOrigins q (prevOrigin body))
        (routeBOrigins q (nextOrigin body)) := by
  exact bodyCom_midpoint (routeBOrigins q) body

theorem routeB_body_jv_zero_of_inactive
    (q : Fin 6 → ℝ) (body j : Fin 6) (a : Fin 3)
    (h : body.val < j.val) :
    routeBBodyJv q body a j = 0 := by
  exact bodyJv_zero_of_inactive (routeBOrigins q) (routeBAxes q) body j a h

theorem routeB_body_jw_zero_of_inactive
    (q : Fin 6 → ℝ) (body j : Fin 6) (a : Fin 3)
    (h : body.val < j.val) :
    routeBBodyJw q body a j = 0 := by
  exact bodyJw_zero_of_inactive (routeBAxes q) body j a h

theorem routeB_body_jv_active_formula
    (q : Fin 6 → ℝ) (body j : Fin 6) (a : Fin 3)
    (h : j.val ≤ body.val) :
    routeBBodyJv q body a j =
      cross3 (routeBAxes q j) (fun b =>
        routeBBodyCom q body b - routeBOrigins q (prevOrigin j) b) a := by
  exact bodyJv_active_formula (routeBOrigins q) (routeBAxes q) body j a h

theorem routeB_body_jw_active_formula
    (q : Fin 6 → ℝ) (body j : Fin 6) (a : Fin 3)
    (h : j.val ≤ body.val) :
    routeBBodyJw q body a j = routeBAxes q j a := by
  exact bodyJw_active_formula (routeBAxes q) body j a h

theorem routeB_body_mass_is_linkMass
    (q : Fin 6 → ℝ) (body : Fin 6) (mass : ℝ) (inertia : IMat) :
    routeBBodyMass q body mass inertia =
      linkMass (routeBBodyJv q body) (routeBBodyJw q body) mass inertia := by
  exact bodyMass_is_linkMass (routeBOrigins q) (routeBAxes q) body mass inertia

#print axioms routeB_frame_count
#print axioms routeB_body_com_midpoint
#print axioms routeB_body_jv_zero_of_inactive
#print axioms routeB_body_jw_zero_of_inactive
#print axioms routeB_body_jv_active_formula
#print axioms routeB_body_jw_active_formula
#print axioms routeB_body_mass_is_linkMass

end
end RouteBBodyInstantiation
