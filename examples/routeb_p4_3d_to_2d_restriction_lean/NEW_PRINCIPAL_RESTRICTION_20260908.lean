import Mathlib.Data.Real.Basic
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic.Linarith

set_option autoImplicit false

namespace RouteBP4PrincipalRestriction

/-!
OPEN_UNCOMPILED. Pure finite-dimensional scalar identities, not a DH witness.
No Lean/Lake run, elaboration, kernel verification or axiom audit.
Local slots 0,1,2 may represent physical joints 4,5,6 only after a source map.
-/

abbrev Mat3 := Fin 3 → Fin 3 → ℝ
abbrev Vec3 := Fin 3 → ℝ

def principal (T : Mat3) (i j : Fin 2) : ℝ := T i.castSucc j.castSucc
def retained (a : Vec3) (j : Fin 2) : ℝ := a j.castSucc
def rhsHead (g : Vec3) (i : Fin 2) : ℝ := g i.castSucc
def coupling (T : Mat3) (i : Fin 2) : ℝ := T i.castSucc 2
def a6 (a : Vec3) : ℝ := a 2

/-- Fixed coordinate split; no row deletion or zero-coupling assumption. -/
theorem split_three (f : Fin 3 → ℝ) :
    (∑ j : Fin 3, f j) = (∑ j : Fin 2, f j.castSucc) + f 2 := by
  simp [Fin.sum_univ_succ, add_assoc]

/-- T*a=g implies A*u=p-h*v with v=a6. No hypothesis on the last diagonal. -/
theorem principal_rows (T : Mat3) (a g : Vec3)
    (heq : ∀ i : Fin 3, (∑ j : Fin 3, T i j * a j) = g i) :
    ∀ i : Fin 2,
      (∑ j : Fin 2, principal T i j * retained a j) =
        rhsHead g i - coupling T i * a6 a := by
  intro i
  have hr := heq i.castSucc
  rw [split_three] at hr
  change (∑ j : Fin 2, T i.castSucc j.castSucc * a j.castSucc) =
    g i.castSucc - T i.castSucc 2 * a 2
  linarith

/-- Dropping the coupling needs its product to vanish, not just a principal block. -/
theorem principal_rows_of_zero_coupling (T : Mat3) (a g : Vec3)
    (heq : ∀ i : Fin 3, (∑ j : Fin 3, T i j * a j) = g i)
    (hz : ∀ i : Fin 2, coupling T i * a6 a = 0) :
    ∀ i : Fin 2,
      (∑ j : Fin 2, principal T i j * retained a j) = rhsHead g i := by
  intro i
  have hr := principal_rows T a g heq i
  rw [hz i, sub_zero] at hr
  exact hr

end RouteBP4PrincipalRestriction
