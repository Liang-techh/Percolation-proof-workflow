import Mathlib

namespace RouteBTerminalCapAE

/- The two quadratic forms are kept separate: `p` is the domain/storage
   quantity, while `qpoly` is the requested terminal output. -/
noncomputable def p (q4 q5 v4 v5 : ℝ) : ℝ :=
  (3 / 2 : ℝ) * (q4 ^ 2 + q5 ^ 2) + (4 / 5 : ℝ) * (v4 ^ 2 + v5 ^ 2)

noncomputable def qpoly (q4 q5 v4 v5 : ℝ) : ℝ :=
  3 * (q4 ^ 2 + q5 ^ 2) + 2 * (v4 ^ 2 + v5 ^ 2)

theorem qpoly_le_five_halves_p (q4 q5 v4 v5 : ℝ) :
    qpoly q4 q5 v4 v5 ≤ (5 / 2 : ℝ) * p q4 q5 v4 v5 := by
  unfold qpoly p
  nlinarith [sq_nonneg q4, sq_nonneg q5, sq_nonneg v4, sq_nonneg v5]

/-- Exact terminal cap requested by AE: the stronger storage cap 24/5
    transfers to qpoly <= 12. -/
theorem p_cap_24_over_5_implies_qpoly_cap_12
    (q4 q5 v4 v5 : ℝ)
    (hp : p q4 q5 v4 v5 ≤ (24 / 5 : ℝ)) :
    qpoly q4 q5 v4 v5 ≤ 12 := by
  linarith [qpoly_le_five_halves_p q4 q5 v4 v5]

/-- Direct storage-comparison interface.  This is weaker than requiring the
    particular p-form: any storage S with the displayed comparison suffices. -/
theorem direct_storage_comparison_implies_qpoly_cap_12
    (S q4 q5 v4 v5 : ℝ)
    (hcompare : qpoly q4 q5 v4 v5 ≤ (5 / 2 : ℝ) * S)
    (hS : S ≤ (24 / 5 : ℝ)) :
    qpoly q4 q5 v4 v5 ≤ 12 := by
  linarith

/- The original 28/5 tube threshold cannot discharge the terminal cap by
   this comparison alone; this is a set-level arithmetic obstruction only. -/
theorem p_cap_28_over_5_only_gives_14
    (q4 q5 v4 v5 : ℝ)
    (hp : p q4 q5 v4 v5 ≤ (28 / 5 : ℝ)) :
    qpoly q4 q5 v4 v5 ≤ 14 := by
  linarith [qpoly_le_five_halves_p q4 q5 v4 v5]

theorem p_cap_28_over_5_does_not_imply_qpoly_cap_12 :
    ¬ (∀ q4 q5 v4 v5 : ℝ,
      p q4 q5 v4 v5 ≤ (28 / 5 : ℝ) → qpoly q4 q5 v4 v5 ≤ 12) := by
  intro h
  have hbad := h 0 0 (5 / 2) 0 (by norm_num [p])
  norm_num [qpoly] at hbad

#print axioms qpoly_le_five_halves_p
#print axioms p_cap_24_over_5_implies_qpoly_cap_12
#print axioms direct_storage_comparison_implies_qpoly_cap_12
#print axioms p_cap_28_over_5_only_gives_14
#print axioms p_cap_28_over_5_does_not_imply_qpoly_cap_12

end RouteBTerminalCapAE
