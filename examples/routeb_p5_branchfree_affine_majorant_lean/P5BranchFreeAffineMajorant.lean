import Mathlib

noncomputable section

namespace RouteBP5BranchFreeAffineMajorant

/-- Signed two-channel quadratic dissipation in the T-P5-045 scaled cross coordinate. -/
def quad (p s sigma x y : ℝ) : ℝ :=
  p * x ^ 2 + sigma * x * y + s * y ^ 2

/-- Affine/bias power term in the same two coordinates. -/
def bias (b4 b5 x y : ℝ) : ℝ := b4 * x + b5 * y

/-- The scaled determinant invariant `4*det(H)`. -/
def det4 (p s sigma : ℝ) : ℝ := 4 * p * s - sigma ^ 2

/-- Squared affine magnitude used by the trace gate. -/
def biasSq (b4 b5 : ℝ) : ℝ := b4 ^ 2 + b5 ^ 2

/-- Adjugate numerator in the scaled `sigma = 2*q` convention. -/
def adjNumerator (p s sigma b4 b5 : ℝ) : ℝ :=
  s * b4 ^ 2 - sigma * b4 * b5 + p * b5 ^ 2

/--
Division-free square completion for a generic scaled symmetric `2x2` quadratic
form `a*x^2 + m*x*y + c*y^2`.
-/
theorem sym2_scaled_qf_completion_identity
    (a m c x y : ℝ) :
    4 * a * (a * x ^ 2 + m * x * y + c * y ^ 2) =
      (2 * a * x + m * y) ^ 2 + (4 * a * c - m ^ 2) * y ^ 2 := by
  ring

/--
Matrix-free `2x2` PSD consumer.  Nonnegative trace and scaled determinant are
sufficient for global nonnegativity of the quadratic form.
-/
theorem sym2_scaled_qf_nonneg_of_trace_det4
    (a m c x y : ℝ)
    (htrace : 0 ≤ a + c)
    (hdet : 0 ≤ 4 * a * c - m ^ 2) :
    0 ≤ a * x ^ 2 + m * x * y + c * y ^ 2 := by
  by_cases ha0 : a = 0
  · subst a
    have hm : m = 0 := by
      nlinarith [sq_nonneg m]
    subst m
    have hc : 0 ≤ c := by
      simpa using htrace
    exact mul_nonneg hc (sq_nonneg y)
  · rcases le_or_gt a 0 with ha_nonpos | ha_pos
    · have ha_neg : a < 0 := lt_of_le_of_ne ha_nonpos ha0
      have hac : 0 ≤ a * c := by
        nlinarith [sq_nonneg m]
      have hc_nonpos : c ≤ 0 := by
        by_contra hc
        have hc_pos : 0 < c := lt_of_not_ge hc
        have hac_neg : a * c < 0 := mul_neg_of_neg_of_pos ha_neg hc_pos
        linarith
      nlinarith
    · have hid := sym2_scaled_qf_completion_identity a m c x y
      have htail : 0 ≤ (4 * a * c - m ^ 2) * y ^ 2 :=
        mul_nonneg hdet (sq_nonneg y)
      have hmul : 0 ≤ 4 * a * (a * x ^ 2 + m * x * y + c * y ^ 2) := by
        rw [hid]
        exact add_nonneg (sq_nonneg (2 * a * x + m * y)) htail
      have h4a : 0 < 4 * a := by nlinarith
      by_contra hq
      have hq_neg : a * x ^ 2 + m * x * y + c * y ^ 2 < 0 :=
        lt_of_not_ge hq
      have hprod_neg :
          4 * a * (a * x ^ 2 + m * x * y + c * y ^ 2) < 0 :=
        mul_neg_of_pos_of_neg h4a hq_neg
      linarith

/-- Exact trace identity for the branch-free majorant quadratic. -/
theorem majorant_trace_identity
    (kappa p s b4 b5 : ℝ) :
    (4 * kappa * p - b4 ^ 2) + (4 * kappa * s - b5 ^ 2) =
      4 * kappa * (p + s) - biasSq b4 b5 := by
  dsimp [biasSq]
  ring

/-- Exact scaled determinant identity for `G_kappa = 4*kappa*H - b*b^T`. -/
theorem majorant_det4_identity
    (kappa p s sigma b4 b5 : ℝ) :
    4 * (4 * kappa * p - b4 ^ 2) * (4 * kappa * s - b5 ^ 2)
        - (4 * kappa * sigma - 2 * b4 * b5) ^ 2 =
      16 * kappa *
        (kappa * det4 p s sigma - adjNumerator p s sigma b4 b5) := by
  dsimp [det4, adjNumerator]
  ring

/--
Exact branch-free completion identity.  No inverse, square root, eigenvalue, or
case split on `det(H)` appears.
-/
theorem affine_majorant_scaled_identity
    (kappa p s sigma b4 b5 x y : ℝ) :
    4 * kappa * (quad p s sigma x y + bias b4 b5 x y + kappa) =
      (4 * kappa * p - b4 ^ 2) * x ^ 2
        + (4 * kappa * sigma - 2 * b4 * b5) * x * y
        + (4 * kappa * s - b5 ^ 2) * y ^ 2
        + (bias b4 b5 x y + 2 * kappa) ^ 2 := by
  dsimp [quad, bias]
  ring

/--
Main forward consumer from the two correlated polynomial gates to the global
affine-energy budget.  The two gates are precisely the trace/determinant gates
for the scaled majorant quadratic.
-/
theorem affine_energy_le_of_two_invariant_gates
    (kappa p s sigma b4 b5 x y : ℝ)
    (hkappa : 0 < kappa)
    (htraceGate : biasSq b4 b5 ≤ 4 * kappa * (p + s))
    (hdetGate :
      adjNumerator p s sigma b4 b5 ≤ kappa * det4 p s sigma) :
    -quad p s sigma x y - bias b4 b5 x y ≤ kappa := by
  have htrace :
      0 ≤ (4 * kappa * p - b4 ^ 2) + (4 * kappa * s - b5 ^ 2) := by
    rw [majorant_trace_identity]
    linarith
  have hdetBase :
      0 ≤ kappa * det4 p s sigma - adjNumerator p s sigma b4 b5 := by
    linarith
  have hk16 : 0 ≤ 16 * kappa := by nlinarith
  have hdet :
      0 ≤ 4 * (4 * kappa * p - b4 ^ 2) * (4 * kappa * s - b5 ^ 2)
        - (4 * kappa * sigma - 2 * b4 * b5) ^ 2 := by
    rw [majorant_det4_identity]
    exact mul_nonneg hk16 hdetBase
  have hG :=
    sym2_scaled_qf_nonneg_of_trace_det4
      (4 * kappa * p - b4 ^ 2)
      (4 * kappa * sigma - 2 * b4 * b5)
      (4 * kappa * s - b5 ^ 2)
      x y htrace hdet
  have hid := affine_majorant_scaled_identity kappa p s sigma b4 b5 x y
  have hmul :
      0 ≤ 4 * kappa * (quad p s sigma x y + bias b4 b5 x y + kappa) := by
    rw [hid]
    exact add_nonneg hG (sq_nonneg (bias b4 b5 x y + 2 * kappa))
  have h4k : 0 < 4 * kappa := by nlinarith
  by_contra hgoal
  have hsum_neg : quad p s sigma x y + bias b4 b5 x y + kappa < 0 := by
    nlinarith
  have hprod_neg :
      4 * kappa * (quad p s sigma x y + bias b4 b5 x y + kappa) < 0 :=
    mul_neg_of_pos_of_neg h4k hsum_neg
  linarith

/-- Same consumer stated directly in the source-checker remainder convention. -/
theorem affine_energy_le_of_nonnegative_remainders
    (kappa p s sigma b4 b5 x y : ℝ)
    (hkappa : 0 < kappa)
    (hRtrace :
      0 ≤ 4 * kappa * (p + s) - biasSq b4 b5)
    (hRdet :
      0 ≤ kappa * det4 p s sigma - adjNumerator p s sigma b4 b5) :
    -quad p s sigma x y - bias b4 b5 x y ≤ kappa := by
  apply affine_energy_le_of_two_invariant_gates
    kappa p s sigma b4 b5 x y hkappa
  · linarith
  · linarith

/-- Strict downstream reserve is kept in the scalar budget layer. -/
theorem affine_energy_lt_of_two_invariant_gates
    (kappa K p s sigma b4 b5 x y : ℝ)
    (hkappa : 0 < kappa)
    (htraceGate : biasSq b4 b5 ≤ 4 * kappa * (p + s))
    (hdetGate :
      adjNumerator p s sigma b4 b5 ≤ kappa * det4 p s sigma)
    (hreserve : kappa < K) :
    -quad p s sigma x y - bias b4 b5 x y < K := by
  exact lt_of_le_of_lt
    (affine_energy_le_of_two_invariant_gates
      kappa p s sigma b4 b5 x y hkappa htraceGate hdetGate)
    hreserve

/--
Typed same-key source-family adapter.  The caller must provide both correlated
remainder bounds on the same domain and in the same signed coordinates.
-/
theorem source_family_affine_energy_le
    {Z : Type*}
    (D : Z → Prop)
    (kappa : ℝ)
    (p s sigma b4 b5 : Z → ℝ)
    (hkappa : 0 < kappa)
    (hRtrace : ∀ z, D z →
      0 ≤ 4 * kappa * (p z + s z) - biasSq (b4 z) (b5 z))
    (hRdet : ∀ z, D z →
      0 ≤ kappa * det4 (p z) (s z) (sigma z)
        - adjNumerator (p z) (s z) (sigma z) (b4 z) (b5 z)) :
    ∀ z, D z → ∀ x y : ℝ,
      -quad (p z) (s z) (sigma z) x y - bias (b4 z) (b5 z) x y ≤ kappa := by
  intro z hz x y
  exact affine_energy_le_of_nonnegative_remainders
    kappa (p z) (s z) (sigma z) (b4 z) (b5 z) x y
    hkappa (hRtrace z hz) (hRdet z hz)

/--
Exact near-singular family from the mathematical review.  The joint determinant
remainder is identically zero, so the branch-free gate survives at `t = 0`.
-/
theorem degenerate_family_joint_gates
    (t : ℝ) :
    biasSq (2 * t) 0 ≤ 4 * (1 : ℝ) * (t ^ 2 + 1) ∧
      adjNumerator (t ^ 2) 1 0 (2 * t) 0 ≤
        (1 : ℝ) * det4 (t ^ 2) 1 0 := by
  dsimp [biasSq, adjNumerator, det4]
  constructor <;> nlinarith [sq_nonneg t]

/-- Uniform affine-energy bound for the exact family, including the singular endpoint. -/
theorem degenerate_family_affine_bound
    (t x y : ℝ) :
    -quad (t ^ 2) 1 0 x y - bias (2 * t) 0 x y ≤ 1 := by
  have hgates := degenerate_family_joint_gates t
  exact affine_energy_le_of_two_invariant_gates
    1 (t ^ 2) 1 0 (2 * t) 0 x y (by norm_num) hgates.1 hgates.2

#print axioms sym2_scaled_qf_completion_identity
#print axioms sym2_scaled_qf_nonneg_of_trace_det4
#print axioms majorant_trace_identity
#print axioms majorant_det4_identity
#print axioms affine_majorant_scaled_identity
#print axioms affine_energy_le_of_two_invariant_gates
#print axioms affine_energy_le_of_nonnegative_remainders
#print axioms affine_energy_lt_of_two_invariant_gates
#print axioms source_family_affine_energy_le
#print axioms degenerate_family_joint_gates
#print axioms degenerate_family_affine_bound

end RouteBP5BranchFreeAffineMajorant
