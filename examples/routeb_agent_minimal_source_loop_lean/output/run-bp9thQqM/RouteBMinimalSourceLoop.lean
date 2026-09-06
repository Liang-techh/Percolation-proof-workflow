import Mathlib

set_option autoImplicit false

namespace RouteBMinimalSourceLoop

noncomputable section

abbrev Body := Fin 6
abbrev Axis := Fin 3
abbrev Joint := Fin 6
abbrev Vec3 := Axis → ℝ
abbrev JMat := Axis → Joint → ℝ
abbrev Mat6 := Joint → Joint → ℝ
abbrev Mat3 := Axis → Axis → ℝ

def cutoffBody (cutoff : Fin 7) (body : Body) : Prop := body.castSucc < cutoff

def gated (cutoff : Fin 7) (body : Body) (x : ℝ) : ℝ :=
  if cutoffBody cutoff body then x else 0

def scalarIdentity (s : ℝ) : Mat3 :=
  fun a b => if a = b then s else 0

def rotatedIsotropic (R : Mat3) (s : ℝ) : Mat3 :=
  fun i j => ∑ a : Axis, ∑ b : Axis,
    R a i * scalarIdentity s a b * R b j

def linkTerm (mass : ℝ) (Jv Jw : JMat) (I : Mat3) : Mat6 :=
  fun i j =>
    mass * (∑ a : Axis, Jv a i * Jv a j) +
      ∑ a : Axis, ∑ b : Axis, Jw a i * I a b * Jw b j

def massFromLinks (mass : Body → ℝ) (Jv Jw : Body → JMat)
    (inertia : Body → Mat3) (cutoff : Fin 7) : Mat6 :=
  fun i j => ∑ body : Body,
    linkTerm (gated cutoff body (mass body))
      (fun a k => gated cutoff body (Jv body a k))
      (fun a k => gated cutoff body (Jw body a k))
      (fun a b => gated cutoff body (inertia body a b)) i j

def juliaMass : Body → ℝ :=
  ![1, 4 / 5, 3 / 5, 2 / 5, 3 / 10, 3 / 20]

def juliaCom (q : Joint → ℝ) (body : Body) : Vec3 :=
  fun a => q ⟨(body : ℕ) % 6, by omega⟩ + (a : ℝ) / 10

def juliaJv (q : Joint → ℝ) (body : Body) : JMat :=
  fun a k => gated 6 body (if a = 0 then q k else (a : ℝ) / 10)

def juliaJw (q : Joint → ℝ) (body : Body) : JMat :=
  fun a k => gated 6 body (if a = 1 then q k else (a : ℝ) / 20)

def juliaRotation (q : Joint → ℝ) (body : Body) : Mat3 :=
  fun a b => if a = b then 1 else (q ⟨(body : ℕ) % 6, by omega⟩) / 100

def juliaInertiaScalar : Body → ℝ :=
  ![1 / 3, 1 / 5, 7 / 60, 1 / 15, 1 / 30, 1 / 60]

def juliaInertia (q : Joint → ℝ) (body : Body) : Mat3 :=
  rotatedIsotropic (juliaRotation q body) (juliaInertiaScalar body)

def juliaMassMatrix (q : Joint → ℝ) (cutoff : Fin 7) : Mat6 :=
  fun i j => ∑ body : Body,
    linkTerm (gated cutoff body (juliaMass body))
      (fun a k => gated cutoff body (juliaJv q body a k))
      (fun a k => gated cutoff body (juliaJw q body a k))
      (fun a b => gated cutoff body (juliaInertia q body a b)) i j

theorem julia_mass_matrix_is_finite_body_sum (q : Joint → ℝ) (cutoff : Fin 7)
    (i j : Joint) :
    juliaMassMatrix q cutoff i j =
      ∑ body : Body,
        linkTerm (gated cutoff body (juliaMass body))
          (fun a k => gated cutoff body (juliaJv q body a k))
          (fun a k => gated cutoff body (juliaJw q body a k))
          (fun a b => gated cutoff body (juliaInertia q body a b)) i j := by
  rfl

theorem julia_mass_matrix_eq_generic_massFromLinks (q : Joint → ℝ)
    (cutoff : Fin 7) :
    juliaMassMatrix q cutoff =
      massFromLinks juliaMass (juliaJv q) (juliaJw q)
        (juliaInertia q) cutoff := by
  funext i j
  rfl

theorem cutoff_is_zero_above_cutoff (cutoff : Fin 7) (body : Body)
    (h : ¬ cutoffBody cutoff body) (x : ℝ) : gated cutoff body x = 0 := by
  simp [gated, h]

theorem rotated_isotropic_is_explicit (q : Joint → ℝ) (body : Body)
    (i j : Axis) :
    juliaInertia q body i j =
      ∑ a : Axis, ∑ b : Axis,
        juliaRotation q body a i * scalarIdentity (juliaInertiaScalar body) a b *
          juliaRotation q body b j := by
  rfl

#print axioms julia_mass_matrix_is_finite_body_sum
#print axioms julia_mass_matrix_eq_generic_massFromLinks
#print axioms cutoff_is_zero_above_cutoff
#print axioms rotated_isotropic_is_explicit

end
end RouteBMinimalSourceLoop
