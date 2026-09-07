import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
# Route-B P7 normalization-safe Schur transport

This source-independent sidecar formalizes the algebraic continuation in
`agent_review_inbox/companion-T-P7-002-honglianmozun-20260907T0854.md`.

It separates the physical Schur charge from any checker normalization.  The
normalization is an explicit 2x2 linear map, its exact rectangular-box cost is
computed without matrix inverses or square roots, and an untyped normalized
certificate is shown unable to provide a uniform physical cost bound.

No deployed Julia/DH binding, seven-term polynomial identification, P8
coverage, M4 closure, admission, or registry claim is made here.
-/

set_option autoImplicit false

namespace RouteBP7NormalizationSafeSchur

noncomputable section

/-- The `(1,1)` entry of `Nᵀ diag(a0,d0)⁻¹ N`. -/
def r11 (a0 d0 n11 n21 : ℝ) : ℝ :=
  n11 ^ 2 / a0 + n21 ^ 2 / d0

/-- The `(1,2)` entry of `Nᵀ diag(a0,d0)⁻¹ N`. -/
def r12 (a0 d0 n11 n12 n21 n22 : ℝ) : ℝ :=
  n11 * n12 / a0 + n21 * n22 / d0

/-- The `(2,2)` entry of `Nᵀ diag(a0,d0)⁻¹ N`. -/
def r22 (a0 d0 n12 n22 : ℝ) : ℝ :=
  n12 ^ 2 / a0 + n22 ^ 2 / d0

/-- Exact worst-case quadratic charge over an independent rectangular box for
normalized coordinates. -/
def boxCost
    (a0 d0 n11 n12 n21 n22 H1 H2 : ℝ) : ℝ :=
  r11 a0 d0 n11 n21 * H1 ^ 2
    + 2 * |r12 a0 d0 n11 n12 n21 n22| * H1 * H2
    + r22 a0 d0 n12 n22 * H2 ^ 2

/-- One-coordinate square completion with a positive diagonal weight. -/
theorem weighted_completion_one
    (a0 x u s : ℝ) (ha0 : 0 < a0) :
    -2 * s * u * x ≤ a0 * x ^ 2 + (u ^ 2 / a0) * s ^ 2 := by
  have hmul :
      (-2 * s * u * x - a0 * x ^ 2) * a0 ≤ u ^ 2 * s ^ 2 := by
    nlinarith [sq_nonneg (a0 * x + s * u)]
  have hdiv :
      -2 * s * u * x - a0 * x ^ 2 ≤ (u ^ 2 * s ^ 2) / a0 :=
    (le_div_iff₀ ha0).2 hmul
  calc
    -2 * s * u * x ≤ a0 * x ^ 2 + (u ^ 2 * s ^ 2) / a0 := by
      linarith
    _ = a0 * x ^ 2 + (u ^ 2 / a0) * s ^ 2 := by ring

/-- Diagonal-coercivity Schur completion.  Only lower positive diagonal bounds
are needed; the actual diagonal block need not be inverted. -/
theorem schur_cost_from_physical_box
    (a d a0 d0 x1 x2 u1 u2 U1 U2 s : ℝ)
    (ha0 : 0 < a0) (hd0 : 0 < d0)
    (ha : a0 ≤ a) (hd : d0 ≤ d)
    (hu1 : |u1| ≤ U1) (hu2 : |u2| ≤ U2) :
    -2 * s * (u1 * x1 + u2 * x2) ≤
      a * x1 ^ 2 + d * x2 ^ 2
        + (U1 ^ 2 / a0 + U2 ^ 2 / d0) * s ^ 2 := by
  have hU1 : 0 ≤ U1 := le_trans (abs_nonneg u1) hu1
  have hU2 : 0 ≤ U2 := le_trans (abs_nonneg u2) hu2
  have hu1sq : u1 ^ 2 ≤ U1 ^ 2 := by
    rw [sq_le_sq]
    simpa [abs_of_nonneg hU1] using hu1
  have hu2sq : u2 ^ 2 ≤ U2 ^ 2 := by
    rw [sq_le_sq]
    simpa [abs_of_nonneg hU2] using hu2
  have hq1 := weighted_completion_one a0 x1 u1 s ha0
  have hq2 := weighted_completion_one d0 x2 u2 s hd0
  have haquad : a0 * x1 ^ 2 ≤ a * x1 ^ 2 :=
    mul_le_mul_of_nonneg_right ha (sq_nonneg x1)
  have hdquad : d0 * x2 ^ 2 ≤ d * x2 ^ 2 :=
    mul_le_mul_of_nonneg_right hd (sq_nonneg x2)
  have hu1div : u1 ^ 2 / a0 ≤ U1 ^ 2 / a0 :=
    (div_le_div_iff_of_pos_right ha0).2 hu1sq
  have hu2div : u2 ^ 2 / d0 ≤ U2 ^ 2 / d0 :=
    (div_le_div_iff_of_pos_right hd0).2 hu2sq
  have hu1cost :
      (u1 ^ 2 / a0) * s ^ 2 ≤ (U1 ^ 2 / a0) * s ^ 2 :=
    mul_le_mul_of_nonneg_right hu1div (sq_nonneg s)
  have hu2cost :
      (u2 ^ 2 / d0) * s ^ 2 ≤ (U2 ^ 2 / d0) * s ^ 2 :=
    mul_le_mul_of_nonneg_right hu2div (sq_nonneg s)
  nlinarith

/-- Expanding the typed normalization map gives exactly the quadratic form
`Nᵀ diag(a0,d0)⁻¹ N`. -/
theorem transported_cost_identity
    (a0 d0 n11 n12 n21 n22 h1 h2 : ℝ) :
    (n11 * h1 + n12 * h2) ^ 2 / a0
        + (n21 * h1 + n22 * h2) ^ 2 / d0 =
      r11 a0 d0 n11 n21 * h1 ^ 2
        + 2 * r12 a0 d0 n11 n12 n21 n22 * h1 * h2
        + r22 a0 d0 n12 n22 * h2 ^ 2 := by
  simp [r11, r12, r22]
  ring

/-- Positive diagonal coercivity makes the first transported diagonal
coefficient nonnegative. -/
theorem r11_nonneg
    (a0 d0 n11 n21 : ℝ) (ha0 : 0 < a0) (hd0 : 0 < d0) :
    0 ≤ r11 a0 d0 n11 n21 := by
  simp [r11]
  positivity

/-- Positive diagonal coercivity makes the second transported diagonal
coefficient nonnegative. -/
theorem r22_nonneg
    (a0 d0 n12 n22 : ℝ) (ha0 : 0 < a0) (hd0 : 0 < d0) :
    0 ≤ r22 a0 d0 n12 n22 := by
  simp [r22]
  positivity

/-- Exact-map rectangular-box upper bound for the transported physical Schur
charge. -/
theorem transported_box_quadratic_cost
    (a0 d0 n11 n12 n21 n22 h1 h2 H1 H2 : ℝ)
    (ha0 : 0 < a0) (hd0 : 0 < d0)
    (hh1 : |h1| ≤ H1) (hh2 : |h2| ≤ H2) :
    (n11 * h1 + n12 * h2) ^ 2 / a0
        + (n21 * h1 + n22 * h2) ^ 2 / d0 ≤
      boxCost a0 d0 n11 n12 n21 n22 H1 H2 := by
  have hH1 : 0 ≤ H1 := le_trans (abs_nonneg h1) hh1
  have hH2 : 0 ≤ H2 := le_trans (abs_nonneg h2) hh2
  have hh1sq : h1 ^ 2 ≤ H1 ^ 2 := by
    rw [sq_le_sq]
    simpa [abs_of_nonneg hH1] using hh1
  have hh2sq : h2 ^ 2 ≤ H2 ^ 2 := by
    rw [sq_le_sq]
    simpa [abs_of_nonneg hH2] using hh2
  have hprod : |h1 * h2| ≤ H1 * H2 := by
    rw [abs_mul]
    exact mul_le_mul hh1 hh2 (abs_nonneg h2) hH1
  have hr11 : 0 ≤ r11 a0 d0 n11 n21 := r11_nonneg a0 d0 n11 n21 ha0 hd0
  have hr22 : 0 ≤ r22 a0 d0 n12 n22 := r22_nonneg a0 d0 n12 n22 ha0 hd0
  have hdiag1 :
      r11 a0 d0 n11 n21 * h1 ^ 2 ≤
        r11 a0 d0 n11 n21 * H1 ^ 2 :=
    mul_le_mul_of_nonneg_left hh1sq hr11
  have hdiag2 :
      r22 a0 d0 n12 n22 * h2 ^ 2 ≤
        r22 a0 d0 n12 n22 * H2 ^ 2 :=
    mul_le_mul_of_nonneg_left hh2sq hr22
  have hcrossBase :
      r12 a0 d0 n11 n12 n21 n22 * h1 * h2 ≤
        |r12 a0 d0 n11 n12 n21 n22| * (H1 * H2) := by
    calc
      r12 a0 d0 n11 n12 n21 n22 * h1 * h2
          ≤ |r12 a0 d0 n11 n12 n21 n22 * h1 * h2| := le_abs_self _
      _ = |r12 a0 d0 n11 n12 n21 n22| * |h1 * h2| := by
        simp [abs_mul, mul_assoc]
      _ ≤ |r12 a0 d0 n11 n12 n21 n22| * (H1 * H2) :=
        mul_le_mul_of_nonneg_left hprod (abs_nonneg _)
  have hcross :
      2 * r12 a0 d0 n11 n12 n21 n22 * h1 * h2 ≤
        2 * |r12 a0 d0 n11 n12 n21 n22| * H1 * H2 := by
    nlinarith
  rw [transported_cost_identity]
  simp only [boxCost]
  nlinarith

/-- For nonnegative mixed coefficient the `(+H1,+H2)` box vertex attains the
transported box cost exactly. -/
theorem box_vertex_attains_of_nonneg_cross
    (a0 d0 n11 n12 n21 n22 H1 H2 : ℝ)
    (hcross : 0 ≤ r12 a0 d0 n11 n12 n21 n22) :
    r11 a0 d0 n11 n21 * H1 ^ 2
        + 2 * r12 a0 d0 n11 n12 n21 n22 * H1 * H2
        + r22 a0 d0 n12 n22 * H2 ^ 2 =
      boxCost a0 d0 n11 n12 n21 n22 H1 H2 := by
  simp [boxCost, abs_of_nonneg hcross]

/-- For negative mixed coefficient the `(+H1,-H2)` box vertex attains the
transported box cost exactly. -/
theorem box_vertex_attains_of_neg_cross
    (a0 d0 n11 n12 n21 n22 H1 H2 : ℝ)
    (hcross : r12 a0 d0 n11 n12 n21 n22 < 0) :
    r11 a0 d0 n11 n21 * H1 ^ 2
        + 2 * r12 a0 d0 n11 n12 n21 n22 * H1 * (-H2)
        + r22 a0 d0 n12 n22 * (-H2) ^ 2 =
      boxCost a0 d0 n11 n12 n21 n22 H1 H2 := by
  simp [boxCost, abs_of_neg hcross]

/-- The rectangular-box upper bound is information-set sharp: one of two box
vertices attains it. -/
theorem box_cost_attained
    (a0 d0 n11 n12 n21 n22 H1 H2 : ℝ)
    (hH1 : 0 ≤ H1) (hH2 : 0 ≤ H2) :
    ∃ h1 h2 : ℝ,
      |h1| ≤ H1 ∧ |h2| ≤ H2 ∧
        r11 a0 d0 n11 n21 * h1 ^ 2
            + 2 * r12 a0 d0 n11 n12 n21 n22 * h1 * h2
            + r22 a0 d0 n12 n22 * h2 ^ 2 =
          boxCost a0 d0 n11 n12 n21 n22 H1 H2 := by
  by_cases hcross : 0 ≤ r12 a0 d0 n11 n12 n21 n22
  · refine ⟨H1, H2, ?_, ?_, ?_⟩
    · simp [abs_of_nonneg hH1]
    · simp [abs_of_nonneg hH2]
    · exact box_vertex_attains_of_nonneg_cross
        a0 d0 n11 n12 n21 n22 H1 H2 hcross
  · have hcross' : r12 a0 d0 n11 n12 n21 n22 < 0 := lt_of_not_ge hcross
    refine ⟨H1, -H2, ?_, ?_, ?_⟩
    · simp [abs_of_nonneg hH1]
    · simp [abs_of_nonneg hH2]
    · exact box_vertex_attains_of_neg_cross
        a0 d0 n11 n12 n21 n22 H1 H2 hcross'

/-- Main normalization-safe Schur consumer: the checker box is transported by
an explicit 2x2 map before the physical energy charge is paid. -/
theorem normalization_safe_schur_consumer
    (a d a0 d0 n11 n12 n21 n22 h1 h2 H1 H2 x1 x2 s : ℝ)
    (ha0 : 0 < a0) (hd0 : 0 < d0)
    (ha : a0 ≤ a) (hd : d0 ≤ d)
    (hh1 : |h1| ≤ H1) (hh2 : |h2| ≤ H2) :
    -2 * s *
        ((n11 * h1 + n12 * h2) * x1 +
          (n21 * h1 + n22 * h2) * x2) ≤
      a * x1 ^ 2 + d * x2 ^ 2
        + boxCost a0 d0 n11 n12 n21 n22 H1 H2 * s ^ 2 := by
  let u1 : ℝ := n11 * h1 + n12 * h2
  let u2 : ℝ := n21 * h1 + n22 * h2
  have hbase :
      -2 * s * (u1 * x1 + u2 * x2) ≤
        a * x1 ^ 2 + d * x2 ^ 2
          + (u1 ^ 2 / a0 + u2 ^ 2 / d0) * s ^ 2 := by
    simpa [sq_abs] using
      (schur_cost_from_physical_box a d a0 d0 x1 x2 u1 u2 |u1| |u2| s
        ha0 hd0 ha hd le_rfl le_rfl)
  have hcost :
      u1 ^ 2 / a0 + u2 ^ 2 / d0 ≤
        boxCost a0 d0 n11 n12 n21 n22 H1 H2 := by
    simpa [u1, u2] using
      (transported_box_quadratic_cost
        a0 d0 n11 n12 n21 n22 h1 h2 H1 H2 ha0 hd0 hh1 hh2)
  have hcostScaled := mul_le_mul_of_nonneg_right hcost (sq_nonneg s)
  dsimp [u1, u2] at hbase
  nlinarith

/-- Scalar normalization enters the physical quadratic charge exactly through
its square. -/
theorem scalar_normalization_cost
    (a0 d0 alpha h1 h2 : ℝ) :
    (alpha * h1) ^ 2 / a0 + (alpha * h2) ^ 2 / d0 =
      alpha ^ 2 * (h1 ^ 2 / a0 + h2 ^ 2 / d0) := by
  ring

/-- If `alpha² = rho`, the scalar-normalized physical charge carries exactly
one factor `rho`; it cannot be silently dropped. -/
theorem scalar_normalization_rho_cost
    (a0 d0 alpha rho h1 h2 : ℝ) (hrho : alpha ^ 2 = rho) :
    (alpha * h1) ^ 2 / a0 + (alpha * h2) ^ 2 / d0 =
      rho * (h1 ^ 2 / a0 + h2 ^ 2 / d0) := by
  rw [scalar_normalization_cost, hrho]

/-- A normalized inequality `eta < tau` supplies no finite uniform physical
cost bound when the positive normalization scale is unconstrained. -/
theorem normalized_certificate_no_uniform_cost
    (tau B : ℝ) (htau : 0 < tau) (hB : 0 < B) :
    ∃ eta rho : ℝ,
      0 < eta ∧ eta < tau ∧ 0 < rho ∧ B < rho * eta := by
  refine ⟨tau / 2, 2 * (B + 1) / tau, ?_, ?_, ?_, ?_⟩
  · linarith
  · linarith
  · positivity
  · have htau0 : tau ≠ 0 := ne_of_gt htau
    have hprod : (2 * (B + 1) / tau) * (tau / 2) = B + 1 := by
      field_simp [htau0]
    rw [hprod]
    linarith

/-- Componentwise interval transport through one row of a normalization map. -/
theorem normalized_component_abs_le
    (n1 n2 h1 h2 N1 N2 H1 H2 : ℝ)
    (hn1 : |n1| ≤ N1) (hn2 : |n2| ≤ N2)
    (hh1 : |h1| ≤ H1) (hh2 : |h2| ≤ H2) :
    |n1 * h1 + n2 * h2| ≤ N1 * H1 + N2 * H2 := by
  have hN1 : 0 ≤ N1 := le_trans (abs_nonneg n1) hn1
  have hN2 : 0 ≤ N2 := le_trans (abs_nonneg n2) hn2
  have hp1 : |n1| * |h1| ≤ N1 * H1 :=
    mul_le_mul hn1 hh1 (abs_nonneg h1) hN1
  have hp2 : |n2| * |h2| ≤ N2 * H2 :=
    mul_le_mul hn2 hh2 (abs_nonneg h2) hN2
  calc
    |n1 * h1 + n2 * h2| ≤ |n1 * h1| + |n2 * h2| := abs_add_le _ _
    _ = |n1| * |h1| + |n2| * |h2| := by rw [abs_mul, abs_mul]
    _ ≤ N1 * H1 + N2 * H2 := add_le_add hp1 hp2

/-- Interval-normalization fallback.  Entrywise bounds on an unknown exact
normalization matrix yield a safe, generally weaker, physical Schur charge. -/
theorem interval_normalization_schur_cost
    (a d a0 d0 n11 n12 n21 n22 h1 h2
      N11 N12 N21 N22 H1 H2 x1 x2 s : ℝ)
    (ha0 : 0 < a0) (hd0 : 0 < d0)
    (ha : a0 ≤ a) (hd : d0 ≤ d)
    (hn11 : |n11| ≤ N11) (hn12 : |n12| ≤ N12)
    (hn21 : |n21| ≤ N21) (hn22 : |n22| ≤ N22)
    (hh1 : |h1| ≤ H1) (hh2 : |h2| ≤ H2) :
    -2 * s *
        ((n11 * h1 + n12 * h2) * x1 +
          (n21 * h1 + n22 * h2) * x2) ≤
      a * x1 ^ 2 + d * x2 ^ 2
        + (((N11 * H1 + N12 * H2) ^ 2 / a0)
          + ((N21 * H1 + N22 * H2) ^ 2 / d0)) * s ^ 2 := by
  apply schur_cost_from_physical_box
      a d a0 d0 x1 x2
      (n11 * h1 + n12 * h2) (n21 * h1 + n22 * h2)
      (N11 * H1 + N12 * H2) (N21 * H1 + N22 * H2) s
      ha0 hd0 ha hd
  · exact normalized_component_abs_le n11 n12 h1 h2 N11 N12 H1 H2 hn11 hn12 hh1 hh2
  · exact normalized_component_abs_le n21 n22 h1 h2 N21 N22 H1 H2 hn21 hn22 hh1 hh2

#print axioms weighted_completion_one
#print axioms schur_cost_from_physical_box
#print axioms transported_cost_identity
#print axioms r11_nonneg
#print axioms r22_nonneg
#print axioms transported_box_quadratic_cost
#print axioms box_vertex_attains_of_nonneg_cross
#print axioms box_vertex_attains_of_neg_cross
#print axioms box_cost_attained
#print axioms normalization_safe_schur_consumer
#print axioms scalar_normalization_cost
#print axioms scalar_normalization_rho_cost
#print axioms normalized_certificate_no_uniform_cost
#print axioms normalized_component_abs_le
#print axioms interval_normalization_schur_cost

end

end RouteBP7NormalizationSafeSchur
