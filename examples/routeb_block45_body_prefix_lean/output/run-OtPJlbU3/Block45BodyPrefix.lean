import BodyMass
import FramePrefixIndex

set_option autoImplicit false

namespace RouteBBlock45BodyPrefix

noncomputable section

open RouteBMassFunctional
open RouteBBodyMass
open RouteBFrameOriginAxis
open RouteBFramePrefixIndex

abbrev RealFrame := Matrix (Fin 4) (Fin 4) ℝ
abbrev Vec3 := Fin 3 → ℝ
abbrev IMat := Fin 3 → Fin 3 → ℝ

/- A fixed Fin 7 accessor for the explicit prefix.  It is intentionally
   independent of List.get: downstream block lemmas should only see the
   seven source slots and not carry a dependent length proof. -/
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

def prefixOrigins (s : Fin 6 → RealFrame) : Fin 7 → Vec3 :=
  fun i => origin (prefixFrame s i)

def jointFrameIndex (j : Fin 6) : Fin 7 :=
  ⟨j.val, by omega⟩

def prefixAxes (s : Fin 6 → RealFrame) : Fin 6 → Vec3 :=
  fun j => zAxis (prefixFrame s (jointFrameIndex j))

def block45Link4Jv (s : Fin 6 → RealFrame) :
    Fin 3 → Fin 6 → ℝ :=
  bodyJv (prefixOrigins s) (prefixAxes s) 3

def block45Link4Jw (s : Fin 6 → RealFrame) :
    Fin 3 → Fin 6 → ℝ :=
  bodyJw (prefixAxes s) 3

def block45Link5Jv (s : Fin 6 → RealFrame) :
    Fin 3 → Fin 6 → ℝ :=
  bodyJv (prefixOrigins s) (prefixAxes s) 4

def block45Link5Jw (s : Fin 6 → RealFrame) :
    Fin 3 → Fin 6 → ℝ :=
  bodyJw (prefixAxes s) 4

def block45Link4Mass (s : Fin 6 → RealFrame) (mass : ℝ) (inertia : IMat) :
    Mat 6 6 :=
  bodyMass (prefixOrigins s) (prefixAxes s) 3 mass inertia

def block45Link5Mass (s : Fin 6 → RealFrame) (mass : ℝ) (inertia : IMat) :
    Mat 6 6 :=
  bodyMass (prefixOrigins s) (prefixAxes s) 4 mass inertia

theorem block45_prefix_frame_zero (s : Fin 6 → RealFrame) :
    prefixFrame s 0 = 1 := by
  rfl

theorem block45_prefix_frame_four (s : Fin 6 → RealFrame) :
    prefixFrame s 4 = (((1 * s 0) * s 1) * s 2) * s 3 := by
  rfl

theorem block45_link4_com_midpoint (s : Fin 6 → RealFrame) :
    bodyCom (prefixOrigins s) 3 =
      midpoint (prefixOrigins s (prevOrigin 3))
        (prefixOrigins s (nextOrigin 3)) := by
  exact bodyCom_midpoint (prefixOrigins s) 3

theorem block45_link4_joint5_inactive
    (s : Fin 6 → RealFrame) (a : Fin 3) :
    block45Link4Jv s a 4 = 0 := by
  exact bodyJv_zero_of_inactive (prefixOrigins s) (prefixAxes s) 3 4 a
    (by decide)

theorem block45_link5_joint5_active
    (s : Fin 6 → RealFrame) (a : Fin 3) :
    block45Link5Jv s a 4 =
      cross3 (prefixAxes s 4) (fun b =>
        bodyCom (prefixOrigins s) 4 b - prefixOrigins s (prevOrigin 4) b) a := by
  exact bodyJv_active_formula (prefixOrigins s) (prefixAxes s) 4 4 a
    (by decide)

theorem block45_link5_angular_joint5_active
    (s : Fin 6 → RealFrame) (a : Fin 3) :
    block45Link5Jw s a 4 = prefixAxes s 4 a := by
  exact bodyJw_active_formula (prefixAxes s) 4 4 a (by decide)

theorem block45_link5_mass_linkMass
    (s : Fin 6 → RealFrame) (mass : ℝ) (inertia : IMat) :
    block45Link5Mass s mass inertia =
      linkMass (block45Link5Jv s) (block45Link5Jw s) mass inertia := by
  exact bodyMass_is_linkMass (prefixOrigins s) (prefixAxes s) 4 mass inertia

#print axioms block45_prefix_frame_zero
#print axioms block45_prefix_frame_four
#print axioms block45_link4_com_midpoint
#print axioms block45_link4_joint5_inactive
#print axioms block45_link5_joint5_active
#print axioms block45_link5_angular_joint5_active
#print axioms block45_link5_mass_linkMass

end
end RouteBBlock45BodyPrefix
