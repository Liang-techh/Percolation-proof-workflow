import Mathlib

set_option autoImplicit false

namespace RouteBBodySemanticCore

noncomputable section

abbrev Vec3 := Fin 3 → ℝ
abbrev Mat (m n : ℕ) := Fin m → Fin n → ℝ
abbrev JMat := Mat 3 6
abbrev IMat := Mat 3 3

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

def bodyJv (origins : Fin 7 → Vec3) (axes : Fin 6 → Vec3)
    (body : Fin 6) : JMat :=
  fun a j => if j.val ≤ body.val then
    cross3 (axes j) (fun b =>
      bodyCom origins body b - origins (prevOrigin j) b) a else 0

def bodyJw (axes : Fin 6 → Vec3) (body : Fin 6) : JMat :=
  fun a j => if j.val ≤ body.val then axes j a else 0

def linkMass (Jv Jw : JMat) (mass : ℝ) (inertia : IMat) : Mat 6 6 :=
  fun i j =>
    mass * (∑ a : Fin 3, Jv a i * Jv a j) +
    (∑ a : Fin 3, ∑ b : Fin 3,
      Jw a i * inertia a b * Jw b j)

def bodyMass (origins : Fin 7 → Vec3) (axes : Fin 6 → Vec3)
    (body : Fin 6) (mass : ℝ) (inertia : IMat) : Mat 6 6 :=
  linkMass (bodyJv origins axes body) (bodyJw axes body) mass inertia

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
      cross3 (axes j) (fun b =>
        bodyCom origins body b - origins (prevOrigin j) b) a := by
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

theorem block45_link4_joint5_inactive
    (origins : Fin 7 → Vec3) (axes : Fin 6 → Vec3) (a : Fin 3) :
    bodyJv origins axes 3 a 4 = 0 := by
  exact bodyJv_zero_of_inactive origins axes 3 4 a (by decide)

theorem block45_link5_joint5_active
    (origins : Fin 7 → Vec3) (axes : Fin 6 → Vec3) (a : Fin 3) :
    bodyJv origins axes 4 a 4 =
      cross3 (axes 4) (fun b =>
        bodyCom origins 4 b - origins (prevOrigin 4) b) a := by
  exact bodyJv_active_formula origins axes 4 4 a (by decide)

theorem block45_link5_angular_joint5_active
    (axes : Fin 6 → Vec3) (a : Fin 3) :
    bodyJw axes 4 a 4 = axes 4 a := by
  exact bodyJw_active_formula axes 4 4 a (by decide)

#print axioms bodyCom_midpoint
#print axioms bodyJv_zero_of_inactive
#print axioms bodyJw_zero_of_inactive
#print axioms bodyJv_active_formula
#print axioms bodyJw_active_formula
#print axioms bodyMass_is_linkMass
#print axioms block45_link4_joint5_inactive
#print axioms block45_link5_joint5_active
#print axioms block45_link5_angular_joint5_active

end
end RouteBBodySemanticCore
