import Mathlib.Data.Real.Basic
import Mathlib.Tactic

set_option autoImplicit false

namespace RouteBF4DirectQpolyComparator

noncomputable section

def L : ℝ :=
  741313139497426595085940983587251157 /
    140000000000000000000000000000000000

def g : ℝ :=
  1544607345405575083521649488080013 /
    2560000000000000000000000000000000

def D_gate : ℝ := 4483 / 2000

def qpoly (q4 q5 v4 v5 : ℝ) : ℝ :=
  3 * (q4 ^ 2 + q5 ^ 2) + 2 * (v4 ^ 2 + v5 ^ 2)

def qpolyAtOne (q4 q5 v4 v5 : ℝ) : ℝ := qpoly q4 q5 v4 v5

theorem direct_qpoly_terminal_inequality
    (Q D : ℝ)
    (hcompare : Q ≤ (3 / 2 : ℝ) * L + 3 * g * D) :
    Q ≤ (3 / 2 : ℝ) * L + 3 * g * D := by
  exact hcompare

theorem g_pos : 0 < g := by
  norm_num [g]

theorem D_gate_lt_D_max :
    D_gate <
      (4 - L / 2) / g := by
  norm_num [D_gate, L, g]

theorem exact_threshold_identity :
    (4 - L / 2) / g =
      3029494884020587239312472131301990744 /
        1351531427229878198081443302070011375 := by
  norm_num [L, g]

theorem exact_threshold_gap :
    (4 - L / 2) / g - D_gate =
      595038157044133006671515392963951 /
        21624502835678051169303092833120182000 := by
  norm_num [L, g, D_gate]

theorem rhs_at_D_gate :
    (3 / 2 : ℝ) * L + 3 * g * D_gate =
      430078214885528867600979985453821108147 /
        35840000000000000000000000000000000000 := by
  norm_num [L, g, D_gate]

theorem exact_strict_margin :
    12 - ((3 / 2 : ℝ) * L + 3 * g * D_gate) =
      1785114471132399020014546178891853 /
        35840000000000000000000000000000000000 := by
  norm_num [L, g, D_gate]

theorem strict_margin_pos :
    0 < 12 - ((3 / 2 : ℝ) * L + 3 * g * D_gate) := by
  norm_num [L, g, D_gate]

theorem terminal_qpoly_lt_twelve
    (Q D : ℝ)
    (hcompare : Q ≤ (3 / 2 : ℝ) * L + 3 * g * D)
    (hD : D ≤ D_gate) :
    Q < 12 := by
  have hg : 0 ≤ (3 : ℝ) * g := by
    exact le_of_lt (mul_pos (by norm_num) g_pos)
  have hbound :
      (3 / 2 : ℝ) * L + 3 * g * D ≤
        (3 / 2 : ℝ) * L + 3 * g * D_gate := by
    have hDmul : (3 : ℝ) * g * D ≤ 3 * g * D_gate :=
      mul_le_mul_of_nonneg_left hD hg
    linarith
  have hmargin :
      (3 / 2 : ℝ) * L + 3 * g * D_gate < 12 := by
    have := strict_margin_pos
    linarith
  exact lt_of_le_of_lt (hcompare.trans hbound) hmargin

theorem qpoly_terminal_comparator
    (q4 q5 v4 v5 D : ℝ)
    (hcompare : qpolyAtOne q4 q5 v4 v5 ≤
      (3 / 2 : ℝ) * L + 3 * g * D)
    (hD : D ≤ D_gate) :
    qpolyAtOne q4 q5 v4 v5 < 12 := by
  exact terminal_qpoly_lt_twelve _ _ hcompare hD

/- The old p-only route is intentionally absent: this leaf compares qpoly
   directly against the exact L,g,D expression. -/

#print axioms direct_qpoly_terminal_inequality
#print axioms exact_threshold_identity
#print axioms exact_threshold_gap
#print axioms terminal_qpoly_lt_twelve
#print axioms qpoly_terminal_comparator

end
end RouteBF4DirectQpolyComparator
