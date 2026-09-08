import Mathlib

namespace RouteBP3CentralFDRemainder

/-- Symmetric centered finite-difference quotient, parameterized only by the
already evaluated forward/backward samples. -/
def centralFD (fplus fminus h : ℝ) : ℝ :=
  (fplus - fminus) / (2 * h)

/-- Division-free centered finite-difference defect relative to a proposed
exact derivative value `d`. -/
def rawDefect (fplus fminus h d : ℝ) : ℝ :=
  fplus - fminus - 2 * h * d

/-- Minimal algebraic Taylor packet consumed by the checker-facing centered-FD
lemma.  The analytic `C^3 -> Taylor remainder` bridge is intentionally outside
this structure: a source/analysis layer must supply the two exact expansions and
remainder bounds on the full shifted stencil. -/
structure TaylorPair where
  fplus : ℝ
  fminus : ℝ
  f0 : ℝ
  d : ℝ
  d2 : ℝ
  h : ℝ
  M : ℝ
  rplus : ℝ
  rminus : ℝ
  h_pos : 0 < h
  M_nonneg : 0 ≤ M
  plus_eq :
    fplus = f0 + h * d + (h ^ 2 / 2) * d2 + rplus
  minus_eq :
    fminus = f0 - h * d + (h ^ 2 / 2) * d2 + rminus
  rplus_abs : |rplus| ≤ M * h ^ 3 / 6
  rminus_abs : |rminus| ≤ M * h ^ 3 / 6

/-- Exact centered cancellation: zeroth- and second-order terms disappear and
only the difference of the two Taylor remainders survives. -/
theorem rawDefect_eq_remainder_diff (p : TaylorPair) :
    rawDefect p.fplus p.fminus p.h p.d = p.rplus - p.rminus := by
  unfold rawDefect
  rw [p.plus_eq, p.minus_eq]
  ring

/-- The two one-sided `M h^3 / 6` Taylor remainder bounds combine to the sharp
raw centered defect bound `M h^3 / 3`. -/
theorem rawDefect_abs_le_third (p : TaylorPair) :
    |rawDefect p.fplus p.fminus p.h p.d| ≤ p.M * p.h ^ 3 / 3 := by
  rw [rawDefect_eq_remainder_diff p]
  calc
    |p.rplus - p.rminus|
        = |p.rplus + (-p.rminus)| := by ring_nf
    _ ≤ |p.rplus| + |-p.rminus| := abs_add _ _
    _ = |p.rplus| + |p.rminus| := by rw [abs_neg]
    _ ≤ p.M * p.h ^ 3 / 6 + p.M * p.h ^ 3 / 6 :=
      add_le_add p.rplus_abs p.rminus_abs
    _ = p.M * p.h ^ 3 / 3 := by ring

/-- Preferred division-free checker form from the mathematical handoff. -/
theorem central_fd_raw_defect_le_of_taylor_pair (p : TaylorPair) :
    3 * |rawDefect p.fplus p.fminus p.h p.d| ≤ p.M * p.h ^ 3 := by
  have h := rawDefect_abs_le_third p
  linarith

/-- Exact relation between normalized centered-FD error and the raw defect.
Division happens only after the positive-step hypothesis is available. -/
theorem centralFD_error_eq_raw_div (p : TaylorPair) :
    centralFD p.fplus p.fminus p.h - p.d
      = rawDefect p.fplus p.fminus p.h p.d / (2 * p.h) := by
  unfold centralFD rawDefect
  field_simp [ne_of_gt p.h_pos]
  ring

/-- Sharp normalized centered-FD error bound `M h^2 / 6`, obtained purely from
`TaylorPair`; the analytic production of such a pair remains a separate leaf. -/
theorem central_fd_error_le_sixth_third_deriv (p : TaylorPair) :
    |centralFD p.fplus p.fminus p.h - p.d| ≤ p.M * p.h ^ 2 / 6 := by
  have hden : 0 < 2 * p.h := by positivity
  rw [centralFD_error_eq_raw_div p, abs_div, abs_of_pos hden]
  apply (div_le_iff₀ hden).2
  calc
    |rawDefect p.fplus p.fminus p.h p.d|
        ≤ p.M * p.h ^ 3 / 3 := rawDefect_abs_le_third p
    _ = (p.M * p.h ^ 2 / 6) * (2 * p.h) := by ring

/-- Pure interval arithmetic needed by the source-facing shifted-region
contract: every centered stencil from `[a,b]` with `0 ≤ h ≤ hmax` lies inside
`[a-hmax,b+hmax]`. -/
theorem shifted_stencil_contained
    (a b hmax x h : ℝ)
    (hx_lo : a ≤ x) (hx_hi : x ≤ b)
    (h_nonneg : 0 ≤ h) (h_le : h ≤ hmax) :
    a - hmax ≤ x - h ∧ x + h ≤ b + hmax := by
  constructor <;> linarith

/-- Once a `TaylorPair` is supplied at a step `h ≤ hmax`, the sharp pointwise
bound immediately gives the uniform `M hmax^2 / 6` envelope. -/
theorem central_fd_error_uniform_of_step_cap
    (p : TaylorPair) (hmax : ℝ) (h_le : p.h ≤ hmax) :
    |centralFD p.fplus p.fminus p.h - p.d| ≤ p.M * hmax ^ 2 / 6 := by
  have hmax_nonneg : 0 ≤ hmax := le_trans (le_of_lt p.h_pos) h_le
  have hsquares : p.h ^ 2 ≤ hmax ^ 2 := by
    nlinarith [sq_nonneg (hmax - p.h)]
  have hmul : p.M * p.h ^ 2 ≤ p.M * hmax ^ 2 :=
    mul_le_mul_of_nonneg_left hsquares p.M_nonneg
  calc
    |centralFD p.fplus p.fminus p.h - p.d|
        ≤ p.M * p.h ^ 2 / 6 := central_fd_error_le_sixth_third_deriv p
    _ ≤ p.M * hmax ^ 2 / 6 := by linarith

/-- Exact `x^3` regression: centered FD differs from the true derivative
`3*x^2` by exactly `h^2`, so the constant `1/6` is attained when `M=6`. -/
theorem central_fd_x_cube_sharp (x h : ℝ) (h_ne : h ≠ 0) :
    centralFD ((x + h) ^ 3) ((x - h) ^ 3) h - 3 * x ^ 2 = h ^ 2 := by
  unfold centralFD
  field_simp [h_ne]
  ring

/-- Division-free version of the same cubic sharpness regression. -/
theorem raw_defect_x_cube_sharp (x h : ℝ) :
    rawDefect ((x + h) ^ 3) ((x - h) ^ 3) h (3 * x ^ 2) = 2 * h ^ 3 := by
  unfold rawDefect
  ring

/-- Cubic family used for the pointwise-C2 obstruction. -/
def cubicFamily (A x0 t : ℝ) : ℝ :=
  A * (t - x0) ^ 3

/-- Every member of `A*(t-x0)^3` has the same algebraic value/first-/second-
jet formulas at the center.  This is the finite-dimensional regression behind
the information-boundary argument. -/
theorem cubic_family_same_center_two_jet (A x0 : ℝ) :
    cubicFamily A x0 x0 = 0
      ∧ 3 * A * (x0 - x0) ^ 2 = 0
      ∧ 6 * A * (x0 - x0) = 0 := by
  simp [cubicFamily]

/-- Yet the centered-FD error of that family at the center is `A h^2`, which
can be scaled arbitrarily while the center two-jet above stays fixed. -/
theorem cubic_family_center_fd_error (A x0 h : ℝ) (h_ne : h ≠ 0) :
    centralFD (cubicFamily A x0 (x0 + h))
        (cubicFamily A x0 (x0 - h)) h
      = A * h ^ 2 := by
  unfold centralFD cubicFamily
  field_simp [h_ne]
  ring

/-- Minimal two-term linear residual handoff.  It deliberately assumes the
caller has already source-bound the exact decomposition `e=e1+e2`; this theorem
does not authorize changing coefficients or residual normalization. -/
theorem central_fd_two_term_linear_residual_budget
    (e e1 e2 B1 B2 : ℝ)
    (hdecomp : e = e1 + e2)
    (h1 : 6 * |e1| ≤ B1)
    (h2 : 6 * |e2| ≤ B2) :
    6 * |e| ≤ B1 + B2 := by
  have htri : |e| ≤ |e1| + |e2| := by
    rw [hdecomp]
    exact abs_add e1 e2
  nlinarith

#print axioms rawDefect_eq_remainder_diff
#print axioms rawDefect_abs_le_third
#print axioms central_fd_raw_defect_le_of_taylor_pair
#print axioms centralFD_error_eq_raw_div
#print axioms central_fd_error_le_sixth_third_deriv
#print axioms shifted_stencil_contained
#print axioms central_fd_error_uniform_of_step_cap
#print axioms central_fd_x_cube_sharp
#print axioms raw_defect_x_cube_sharp
#print axioms cubic_family_same_center_two_jet
#print axioms cubic_family_center_fd_error
#print axioms central_fd_two_term_linear_residual_budget

end RouteBP3CentralFDRemainder
