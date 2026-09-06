import Mathlib

set_option autoImplicit false

namespace RouteBAgentExactDHLoop

noncomputable section

abbrev V3 := Fin 3 → ℝ
abbrev Frame := Matrix (Fin 4) (Fin 4) ℝ
abbrev Jacobian := Fin 3 → Fin 6 → ℝ
abbrev Inertia := Fin 3 → Fin 3 → ℝ
abbrev MassMatrix := Matrix (Fin 6) (Fin 6) ℝ

def dhStep (ct st ca sa a d : ℝ) : Frame := fun i j =>
  match i.1, j.1 with
  | 0, 0 => ct | 0, 1 => -st * ca | 0, 2 => st * sa | 0, 3 => ct * a
  | 1, 0 => st | 1, 1 => ct * ca | 1, 2 => -ct * sa | 1, 3 => st * a
  | 2, 0 => 0 | 2, 1 => sa | 2, 2 => ca | 2, 3 => d
  | 3, 0 => 0 | 3, 1 => 0 | 3, 2 => 0 | 3, 3 => 1
  | _, _ => 0

def step (q α a d : Fin 6 → ℝ) (k : Fin 6) : Frame :=
  dhStep (Real.cos (q k)) (Real.sin (q k)) (Real.cos (α k))
    (Real.sin (α k)) (a k) (d k)

def frameAt (q α a d : Fin 6 → ℝ) : Fin 7 → Frame
  | ⟨0, _⟩ => 1
  | ⟨n + 1, h⟩ => frameAt q α a d ⟨n, by omega⟩ * step q α a d ⟨n, by omega⟩
termination_by i => i.1

def embed3 (i : Fin 3) : Fin 4 := ⟨i.1, by omega⟩
def origin (F : Frame) : V3 := fun i => F (embed3 i) 3
def axis (F : Frame) : V3 := fun i => F (embed3 i) 2

def origins (q α a d : Fin 6 → ℝ) : Fin 7 → V3 :=
  fun i => origin (frameAt q α a d i)
def axes (q α a d : Fin 6 → ℝ) : Fin 7 → V3 :=
  fun i => axis (frameAt q α a d i)

def prev (j : Fin 6) : Fin 7 := ⟨j.1, by omega⟩
def next (j : Fin 6) : Fin 7 := ⟨j.1 + 1, by omega⟩
def midpoint (x y : V3) : V3 := fun i => (x i + y i) / 2
def com (O : Fin 7 → V3) (body : Fin 6) : V3 := midpoint (O (prev body)) (O (next body))

def cross (u v : V3) : V3 := ![
  u 1 * v 2 - u 2 * v 1,
  u 2 * v 0 - u 0 * v 2,
  u 0 * v 1 - u 1 * v 0]

def Jv (O : Fin 7 → V3) (Z : Fin 7 → V3) (body : Fin 6) : Jacobian :=
  fun i j => if j.1 ≤ body.1 then cross (Z (prev j))
    (fun k => com O body k - O (prev j) k) i else 0

def Jw (Z : Fin 7 → V3) (body : Fin 6) : Jacobian :=
  fun i j => if j.1 ≤ body.1 then Z (prev j) i else 0

def linkMass (Jv Jw : Jacobian) (m : ℝ) (I : Inertia) : MassMatrix :=
  fun i j => m * (∑ k : Fin 3, Jv k i * Jv k j) +
    ∑ k : Fin 3, ∑ l : Fin 3, Jw k i * I k l * Jw l j

def bodyMass (q α a d m : Fin 6 → ℝ) (I : Fin 6 → Inertia)
    (body : Fin 6) : MassMatrix :=
  linkMass (Jv (origins q α a d) (axes q α a d) body)
    (Jw (axes q α a d) body) (m body) (I body)

def massFromLinks (q α a d m : Fin 6 → ℝ) (I : Fin 6 → Inertia) : MassMatrix :=
  fun i j => ∑ body : Fin 6, bodyMass q α a d m I body i j

def massMatrix (q α a d m : Fin 6 → ℝ) (I : Fin 6 → Inertia) : MassMatrix :=
  fun i j => ∑ body : Fin 6,
    (m body * (∑ k : Fin 3,
      Jv (origins q α a d) (axes q α a d) body k i *
      Jv (origins q α a d) (axes q α a d) body k j) +
    ∑ k : Fin 3, ∑ l : Fin 3,
      Jw (axes q α a d) body k i * I body k l *
      Jw (axes q α a d) body l j)

theorem bodyMass_eq_expanded (q α a d m : Fin 6 → ℝ) (I : Fin 6 → Inertia)
    (body i j : Fin 6) :
    bodyMass q α a d m I body i j =
      m body * (∑ k : Fin 3,
        Jv (origins q α a d) (axes q α a d) body k i *
        Jv (origins q α a d) (axes q α a d) body k j) +
      ∑ k : Fin 3, ∑ l : Fin 3,
        Jw (axes q α a d) body k i * I body k l *
        Jw (axes q α a d) body l j := by
  rfl

theorem massMatrix_eq_massFromLinks (q α a d m : Fin 6 → ℝ)
    (I : Fin 6 → Inertia) :
    massMatrix q α a d m I = massFromLinks q α a d m I := by
  funext i j
  simp only [massMatrix, massFromLinks, bodyMass, linkMass]

theorem six_step_exact_real_structure (q α a d : Fin 6 → ℝ)
    (m : Fin 6 → ℝ) (I : Fin 6 → Inertia) :
    massMatrix q α a d m I = massFromLinks q α a d m I :=
  massMatrix_eq_massFromLinks q α a d m I

#print axioms massMatrix_eq_massFromLinks
#print axioms six_step_exact_real_structure

end
end RouteBAgentExactDHLoop
