import Mathlib

namespace RouteBBlockTargets

noncomputable def p (q4 q5 v4 v5 : ℝ) : ℝ :=
  (3 / 2 : ℝ) * (q4 ^ 2 + q5 ^ 2) + (4 / 5 : ℝ) * (v4 ^ 2 + v5 ^ 2)

noncomputable def terminal (q4 q5 v4 v5 : ℝ) : ℝ :=
  3 * (q4 ^ 2 + q5 ^ 2) + 2 * (v4 ^ 2 + v5 ^ 2)

theorem target_sandwich (q4 q5 v4 v5 : ℝ) :
    2 * p q4 q5 v4 v5 ≤ terminal q4 q5 v4 v5 ∧
    terminal q4 q5 v4 v5 ≤ (5 / 2 : ℝ) * p q4 q5 v4 v5 := by
  unfold p terminal
  constructor <;> nlinarith [sq_nonneg q4, sq_nonneg q5, sq_nonneg v4, sq_nonneg v5]

theorem tube_alone_terminal_fourteen (q4 q5 v4 v5 : ℝ)
    (hp : p q4 q5 v4 v5 ≤ (28 / 5 : ℝ)) :
    terminal q4 q5 v4 v5 ≤ 14 := by
  linarith [(target_sandwich q4 q5 v4 v5).2]

theorem tighter_p_implies_terminal (q4 q5 v4 v5 : ℝ)
    (hp : p q4 q5 v4 v5 ≤ (24 / 5 : ℝ)) :
    terminal q4 q5 v4 v5 ≤ 12 := by
  linarith [(target_sandwich q4 q5 v4 v5).2]

/- Rational set witness only, not claimed dynamically reachable from X0. -/
theorem tube_does_not_imply_terminal :
    ¬ ∀ q4 q5 v4 v5, p q4 q5 v4 v5 ≤ (28 / 5 : ℝ) →
      terminal q4 q5 v4 v5 ≤ 12 := by
  intro h
  have bad := h 0 0 (5 / 2) 0 (by norm_num [p])
  norm_num [terminal] at bad

#print axioms target_sandwich
#print axioms tube_alone_terminal_fourteen
#print axioms tighter_p_implies_terminal
#print axioms tube_does_not_imply_terminal

end RouteBBlockTargets
