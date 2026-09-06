import MassFunctional

set_option autoImplicit false

namespace RouteBBodyMass

noncomputable section

open RouteBMassFunctional

abbrev Vec3 := Fin 3 → ℝ
abbrev JMat := Fin 3 → Fin 6 → ℝ
abbrev IMat := Fin 3 → Fin 3 → ℝ

def prevOrigin (j : Fin 6) : Fin 7 :=
  ⟨j.val, by omega⟩

def nextOrigin (i : Fin 6) : Fin 7 :=
  ⟨i.val + 1, by omega⟩

def midpoint (x y : Vec3) : Vec3 :=
  fun a => (x a + y a) / 2

def cross3 (u v : Vec3) : Vec3 := ![
  u 1 * v 2 - u 2 * v 1,
  u 2 * v 0 - u 0 * v 2,
  u 0 * v 1 - u 1 * v 0]

def bodyCom (origins : Fin 7 → Vec3) (body : Fin 6) : Vec3 :=
  midpoint (origins (prevOrigin body)) (origins (nextOrigin body))

def activeColumn (body j : Fin 6) : Prop := j.val ≤ body.val

def bodyJv (origins : Fin 7 → Vec3) (axes : Fin 6 → Vec3)
    (body : Fin 6) : JMat :=
  fun a j => if j.val ≤ body.val then
    cross3 (axes j) (fun b => bodyCom origins body b -
      origins (prevOrigin j) b) a else 0

def bodyJw (axes : Fin 6 → Vec3) (body : Fin 6) : JMat :=
  fun a j => if j.val ≤ body.val then axes j a else 0

def bodyMass (origins : Fin 7 → Vec3) (axes : Fin 6 → Vec3)
    (body : Fin 6) (mass : ℝ) (inertia : IMat) : Mat 6 6 :=
  linkMass (bodyJv origins axes body) (bodyJw axes body) mass inertia

theorem prevOrigin_val (j : Fin 6) : (prevOrigin j).val = j.val := by
  rfl

theorem nextOrigin_val (i : Fin 6) : (nextOrigin i).val = i.val + 1 := by
  rfl

theorem bodyCom_midpoint (origins : Fin 7 → Vec3) (body : Fin 6) :
    bodyCom origins body =
      midpoint (origins (prevOrigin body)) (origins (nextOrigin body)) := by
  rfl

theorem bodyJv_zero_of_inactive
    (origins : Fin 7 → Vec3) (axes : Fin 6 → Vec3)
    (body j : Fin 6) (a : Fin 3)
    (h : body.val < j.val) :
    bodyJv origins axes body a j = 0 := by
  simp [bodyJv, Nat.not_le_of_lt h]

theorem bodyJw_zero_of_inactive
    (axes : Fin 6 → Vec3) (body j : Fin 6) (a : Fin 3)
    (h : body.val < j.val) :
    bodyJw axes body a j = 0 := by
  simp [bodyJw, Nat.not_le_of_lt h]

theorem bodyJv_active_formula
    (origins : Fin 7 → Vec3) (axes : Fin 6 → Vec3)
    (body j : Fin 6) (a : Fin 3)
    (h : j.val ≤ body.val) :
    bodyJv origins axes body a j =
      cross3 (axes j) (fun b => bodyCom origins body b -
        origins (prevOrigin j) b) a := by
  simp [bodyJv, h]

theorem bodyJw_active_formula
    (axes : Fin 6 → Vec3) (body j : Fin 6) (a : Fin 3)
    (h : j.val ≤ body.val) :
    bodyJw axes body a j = axes j a := by
  simp [bodyJw, h]

theorem bodyMass_is_linkMass
    (origins : Fin 7 → Vec3) (axes : Fin 6 → Vec3)
    (body : Fin 6) (mass : ℝ) (inertia : IMat) :
    bodyMass origins axes body mass inertia =
      linkMass (bodyJv origins axes body) (bodyJw axes body) mass inertia := by
  rfl

theorem body_mass_entry_expanded
    (origins : Fin 7 → Vec3) (axes : Fin 6 → Vec3)
    (body : Fin 6) (mass : ℝ) (inertia : IMat) (i j : Fin 6) :
    bodyMass origins axes body mass inertia i j =
      mass * (∑ a : Fin 3,
        bodyJv origins axes body a i * bodyJv origins axes body a j) +
      (∑ a : Fin 3, ∑ b : Fin 3,
        bodyJw axes body a i * inertia a b * bodyJw axes body b j) := by
  rfl

end
end RouteBBodyMass

#print axioms RouteBBodyMass.prevOrigin_val
#print axioms RouteBBodyMass.nextOrigin_val
#print axioms RouteBBodyMass.bodyCom_midpoint
#print axioms RouteBBodyMass.bodyJv_zero_of_inactive
#print axioms RouteBBodyMass.bodyJw_zero_of_inactive
#print axioms RouteBBodyMass.bodyJv_active_formula
#print axioms RouteBBodyMass.bodyJw_active_formula
#print axioms RouteBBodyMass.bodyMass_is_linkMass
#print axioms RouteBBodyMass.body_mass_entry_expanded
