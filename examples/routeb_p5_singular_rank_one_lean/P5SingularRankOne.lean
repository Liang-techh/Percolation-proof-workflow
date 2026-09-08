import Mathlib

noncomputable section

namespace RouteBP5SingularRankOne

/-- Pareto decay coefficient inherited from the P5 block-(4,5) lane. -/
def decayRate (r : ℝ) : ℝ := (109 - r) / 200

/-- Symmetric two-channel quadratic form. -/
def quad (p q s u4 u5 : ℝ) : ℝ :=
  p * u4 ^ 2 + 2 * q * u4 * u5 + s * u5 ^ 2

/-- Linear bias paired with the two-channel state. -/
def bias (b4 b5 u4 u5 : ℝ) : ℝ := b4 * u4 + b5 * u5

/-- Determinant of the symmetric 2x2 block. -/
def det2 (p q s : ℝ) : ℝ := p * s - q ^ 2

/-- Adjugate numerator used by the positive-definite T-P5-044 completion. -/
def adjNumerator (p q s b4 b5 : ℝ) : ℝ :=
  s * b4 ^ 2 - 2 * q * b4 * b5 + p * b5 ^ 2

/--
On the rank-one boundary `p*s=q^2`, range compatibility `p*b5=q*b4`
turns the quadratic-plus-linear residual exactly into one square after clearing
`4*p`.
-/
theorem rank_one_completion_identity
    (p q s b4 b5 u4 u5 : ℝ)
    (hdet : p * s = q ^ 2)
    (hcompat : p * b5 = q * b4) :
    4 * p * (quad p q s u4 u5 + bias b4 b5 u4 u5) + b4 ^ 2 =
      (2 * (p * u4 + q * u5) + b4) ^ 2 := by
  dsimp [quad, bias]
  linear_combination 4 * u5 ^ 2 * hdet + 4 * u5 * hcompat

/-- Division-free sharp completion on the compatible rank-one branch. -/
theorem rank_one_bias_completion_cleared
    (p q s b4 b5 u4 u5 : ℝ)
    (hdet : p * s = q ^ 2)
    (hcompat : p * b5 = q * b4) :
    4 * p * (-quad p q s u4 u5 - bias b4 b5 u4 u5) ≤ b4 ^ 2 := by
  have hid := rank_one_completion_identity p q s b4 b5 u4 u5 hdet hcompat
  have hsquare : 0 ≤ (2 * (p * u4 + q * u5) + b4) ^ 2 :=
    sq_nonneg (2 * (p * u4 + q * u5) + b4)
  nlinarith

/-- Sharp finite additive charge on the compatible nonzero rank-one branch. -/
theorem rank_one_bias_completion
    (p q s b4 b5 u4 u5 : ℝ)
    (hp : 0 < p)
    (hdet : p * s = q ^ 2)
    (hcompat : p * b5 = q * b4) :
    -quad p q s u4 u5 - bias b4 b5 u4 u5 ≤ b4 ^ 2 / (4 * p) := by
  have hclear :=
    rank_one_bias_completion_cleared p q s b4 b5 u4 u5 hdet hcompat
  have h4p : 0 < 4 * p := by positivity
  apply (le_div_iff₀ h4p).2
  nlinarith

/-- The explicit kernel direction `(-q,p)` has zero quadratic cost. -/
theorem rank_one_kernel_quadratic
    (p q s t : ℝ)
    (hdet : p * s = q ^ 2) :
    quad p q s (-q * t) (p * t) = 0 := by
  dsimp [quad]
  linear_combination p * t ^ 2 * hdet

/-- Along the kernel family, the bias is exactly the range-compatibility defect. -/
theorem rank_one_kernel_bias
    (p q b4 b5 t : ℝ) :
    bias b4 b5 (-q * t) (p * t) = t * (p * b5 - q * b4) := by
  dsimp [bias]
  ring

/--
If the bias has a nonzero kernel component, the rank-one residual contribution
has no finite uniform upper bound along the explicit kernel family.
-/
theorem rank_one_incompatible_no_uniform_upper_bound
    (p q s b4 b5 : ℝ)
    (hdet : p * s = q ^ 2)
    (hneq : p * b5 ≠ q * b4) :
    ¬ ∃ C : ℝ, ∀ t : ℝ,
      -quad p q s (-q * t) (p * t) - bias b4 b5 (-q * t) (p * t) ≤ C := by
  intro hbound
  rcases hbound with ⟨C, hC⟩
  let d : ℝ := p * b5 - q * b4
  have hd : d ≠ 0 := by
    dsimp [d]
    exact sub_ne_zero.mpr hneq
  let t : ℝ := -(C + 1) / d
  have hq := rank_one_kernel_quadratic p q s t hdet
  have hb := rank_one_kernel_bias p q b4 b5 t
  have ht : t * d = -(C + 1) := by
    dsimp [t]
    exact div_mul_cancel₀ (-(C + 1)) hd
  have h := hC t
  rw [hq, hb] at h
  change -(t * d) ≤ C at h
  rw [ht] at h
  linarith

/--
Exact quarter-barrier inward gate on the compatible rank-one branch.  The
caller supplies only the already-established Lyapunov ledger inequality.
-/
theorem rank_one_first_exit_gate
    (r p q s b4 b5 V Vdot u4 u5 : ℝ)
    (hp : 0 < p)
    (hdet : p * s = q ^ 2)
    (hcompat : p * b5 = q * b4)
    (hledger :
      Vdot ≤ -decayRate r * V - quad p q s u4 u5 - bias b4 b5 u4 u5)
    (hVstar : V = 1 / 4)
    (hgate : 200 * b4 ^ 2 < (109 - r) * p) :
    Vdot < 0 := by
  have hcharge := rank_one_bias_completion p q s b4 b5 u4 u5 hp hdet hcompat
  have h4p : 0 < 4 * p := by positivity
  have hcharge_lt : b4 ^ 2 / (4 * p) < decayRate r / 4 := by
    apply (div_lt_iff₀ h4p).2
    dsimp [decayRate]
    nlinarith [hgate]
  rw [hVstar] at hledger
  nlinarith [hledger, hcharge, hcharge_lt]

/--
Exact incremental parameter-tube gate.  The bias is `dc * g`; compatibility is
checked on `g`, and nonzero `dc` supplies the strict square factor.
-/
theorem rank_one_parameter_tube_gate
    (r p q s g4 g5 dc Vdot u4 u5 : ℝ)
    (hp : 0 < p)
    (hdet : p * s = q ^ 2)
    (hcompat : p * g5 = q * g4)
    (hdc : dc ≠ 0)
    (hledger :
      Vdot ≤ -decayRate r * (dc ^ 2 / 12) - quad p q s u4 u5
        - dc * (g4 * u4 + g5 * u5))
    (hgate : 600 * g4 ^ 2 < (109 - r) * p) :
    Vdot < 0 := by
  have hcompat_dc : p * (dc * g5) = q * (dc * g4) := by
    linear_combination dc * hcompat
  have hcharge :=
    rank_one_bias_completion p q s (dc * g4) (dc * g5) u4 u5
      hp hdet hcompat_dc
  have hbias : bias (dc * g4) (dc * g5) u4 u5 = dc * (g4 * u4 + g5 * u5) := by
    dsimp [bias]
    ring
  rw [hbias] at hcharge
  have h4p : 0 < 4 * p := by positivity
  have hbase : g4 ^ 2 / (4 * p) < decayRate r / 12 := by
    apply (div_lt_iff₀ h4p).2
    dsimp [decayRate]
    nlinarith [hgate]
  have hdc2 : 0 < dc ^ 2 := by positivity
  have hscaled := mul_lt_mul_of_pos_right hbase hdc2
  have hcharge_lt :
      (dc * g4) ^ 2 / (4 * p) < decayRate r * dc ^ 2 / 12 := by
    calc
      (dc * g4) ^ 2 / (4 * p) = (g4 ^ 2 / (4 * p)) * dc ^ 2 := by ring
      _ < (decayRate r / 12) * dc ^ 2 := hscaled
      _ = decayRate r * dc ^ 2 / 12 := by ring
  nlinarith [hledger, hcharge, hcharge_lt]

/--
Under range compatibility, the positive-definite adjugate numerator factors by
exactly the determinant.  This is the algebraic continuity identity used to
connect T-P5-044 to the singular boundary.
-/
theorem compatible_adjugate_numerator_identity
    (p q s b4 b5 : ℝ)
    (hcompat : p * b5 = q * b4) :
    p * adjNumerator p q s b4 b5 = det2 p q s * b4 ^ 2 := by
  dsimp [adjNumerator, det2]
  linear_combination (p * b5 - q * b4) * hcompat

/--
On the compatible rank-one boundary the unreduced determinant numerator and
determinant both vanish; a checker must use the reduced rank-one gate instead
of demanding the strict interior determinant inequality.
-/
theorem rank_one_interior_gate_collapses
    (p q s b4 b5 : ℝ)
    (hp : 0 < p)
    (hdet : p * s = q ^ 2)
    (hcompat : p * b5 = q * b4) :
    det2 p q s = 0 ∧ adjNumerator p q s b4 b5 = 0 := by
  have hD : det2 p q s = 0 := by
    dsimp [det2]
    nlinarith [hdet]
  have hid := compatible_adjugate_numerator_identity p q s b4 b5 hcompat
  rw [hD] at hid
  have hp0 : p ≠ 0 := ne_of_gt hp
  have hB : adjNumerator p q s b4 b5 = 0 := by
    apply (mul_eq_zero.mp ?_).resolve_left hp0
    simpa using hid
  exact ⟨hD, hB⟩

#print axioms rank_one_completion_identity
#print axioms rank_one_bias_completion_cleared
#print axioms rank_one_bias_completion
#print axioms rank_one_kernel_quadratic
#print axioms rank_one_kernel_bias
#print axioms rank_one_incompatible_no_uniform_upper_bound
#print axioms rank_one_first_exit_gate
#print axioms rank_one_parameter_tube_gate
#print axioms compatible_adjugate_numerator_identity
#print axioms rank_one_interior_gate_collapses

end RouteBP5SingularRankOne
