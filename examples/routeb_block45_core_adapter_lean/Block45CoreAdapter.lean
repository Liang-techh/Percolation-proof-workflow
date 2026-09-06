import BodySemanticCore
import FrameSlotAccessor

set_option autoImplicit false

namespace RouteBBlock45CoreAdapter

noncomputable section

open RouteBBodySemanticCore
open RouteBFrameSlotAccessor
open RouteBFrameOriginAxis

abbrev RealFrame := Matrix (Fin 4) (Fin 4) ℝ
abbrev Vec3 := Fin 3 → ℝ

def routeBOrigins (q : Fin 6 → ℝ) : Fin 7 → Vec3 :=
  fun i => origin (routeBFrameSlot q i)

def routeBJointFrame (j : Fin 6) : Fin 7 :=
  ⟨j.val, by omega⟩

def routeBAxes (q : Fin 6 → ℝ) : Fin 6 → Vec3 :=
  fun j => zAxis (routeBFrameSlot q (routeBJointFrame j))

def link4Jv (q : Fin 6 → ℝ) : JMat :=
  bodyJv (routeBOrigins q) (routeBAxes q) 3

def link5Jv (q : Fin 6 → ℝ) : JMat :=
  bodyJv (routeBOrigins q) (routeBAxes q) 4

def link5Jw (q : Fin 6 → ℝ) : JMat :=
  bodyJw (routeBAxes q) 4

theorem link4_com_midpoint (q : Fin 6 → ℝ) :
    bodyCom (routeBOrigins q) 3 =
      midpoint (routeBOrigins q (prevOrigin 3))
        (routeBOrigins q (nextOrigin 3)) := by
  exact bodyCom_midpoint (routeBOrigins q) 3

theorem link4_joint5_inactive (q : Fin 6 → ℝ) (a : Fin 3) :
    link4Jv q a 4 = 0 := by
  simpa only [link4Jv] using
    (block45_link4_joint5_inactive (routeBOrigins q) (routeBAxes q) a)

theorem link5_joint5_active (q : Fin 6 → ℝ) (a : Fin 3) :
    link5Jv q a 4 =
      cross3 (routeBAxes q 4) (fun b =>
        bodyCom (routeBOrigins q) 4 b - routeBOrigins q (prevOrigin 4) b) a := by
  simpa only [link5Jv] using
    (block45_link5_joint5_active (routeBOrigins q) (routeBAxes q) a)

theorem link5_joint5_angular_active (q : Fin 6 → ℝ) (a : Fin 3) :
    link5Jw q a 4 = routeBAxes q 4 a := by
  simpa only [link5Jw] using
    (block45_link5_angular_joint5_active (routeBAxes q) a)

end
end RouteBBlock45CoreAdapter
