import Mathlib

noncomputable section

namespace RouteBP5SingularPSD

/-- Symmetric two-channel quadratic form. -/
def quad (p q s x y : ℝ) : ℝ :=
  p * x ^ 2 + 2 * q * x * y + s * y ^ 2

/-- Linear affine bias. -/
def bias (b4 b5 x y : ℝ) : ℝ := b4 * x + b5 * y

/-- The quantity whose finite global upper bound is classified below. -/
def residual (p q s b4 b5 x y : ℝ) : ℝ :=
  -quad p q s x y - bias b4 b5 x y

/-- Determinant of the symmetric 2x2 block. -/
def det2 (p q s : ℝ) : ℝ := p * s - q ^ 2

/-- Trace of the symmetric 2x2 block. -/
def trace2 (p s : ℝ) : ℝ := p + s

/-- First component of `adj(H) b`. -/
def k4 (q s b4 b5 : ℝ) : ℝ := s * b4 - q * b5

/-- Second component of `adj(H) b`. -/
def k5 (p q b4 b5 : ℝ) : ℝ := p * b5 - q * b4

/-- Pivot-free adjugate quadratic numerator `b^T adj(H) b`. -/
def adjNumerator (p q s b4 b5 : ℝ) : ℝ :=
  s * b4 ^ 2 - 2 * q * b4 * b5 + p * b5 ^ 2

/-- First division-free adjugate identity. -/
theorem adjugate_kernel_first
    (p q s b4 b5 : ℝ) :
    p * k4 q s b4 b5 + q * k5 p q b4 b5 = det2 p q s * b4 := by
  dsimp [k4, k5, det2]
  ring

/-- Second division-free adjugate identity. -/
theorem adjugate_kernel_second
    (p q s b4 b5 : ℝ) :
    q * k4 q s b4 b5 + s * k5 p q b4 b5 = det2 p q s * b5 := by
  dsimp [k4, k5, det2]
  ring

/-- Exact incompatibility-numerator identity from T-P5-050. -/
theorem incompatibility_norm_identity
    (p q s b4 b5 : ℝ) :
    k4 q s b4 b5 ^ 2 + k5 p q b4 b5 ^ 2 =
      trace2 p s * adjNumerator p q s b4 b5
        - det2 p q s * (b4 ^ 2 + b5 ^ 2) := by
  dsimp [k4, k5, trace2, adjNumerator, det2]
  ring

/-- Pivot-free trace completion identity. -/
theorem trace_completion_identity
    (p q s b4 b5 x y : ℝ) :
    (2 * (p * x + q * y) + b4) ^ 2 +
        (2 * (q * x + s * y) + b5) ^ 2 =
      4 * trace2 p s * (quad p q s x y + bias b4 b5 x y)
        + (b4 ^ 2 + b5 ^ 2)
        - 4 * (det2 p q s * (x ^ 2 + y ^ 2)
          + k4 q s b4 b5 * x + k5 p q b4 b5 * y) := by
  dsimp [trace2, quad, bias, det2, k4, k5]
  ring

/-- On the singular compatible branch, the squared completion is exact. -/
theorem singular_compatible_trace_identity
    (p q s b4 b5 x y : ℝ)
    (hdet : det2 p q s = 0)
    (hk4 : k4 q s b4 b5 = 0)
    (hk5 : k5 p q b4 b5 = 0) :
    (2 * (p * x + q * y) + b4) ^ 2 +
        (2 * (q * x + s * y) + b5) ^ 2 =
      4 * trace2 p s * (quad p q s x y + bias b4 b5 x y)
        + (b4 ^ 2 + b5 ^ 2) := by
  have h := trace_completion_identity p q s b4 b5 x y
  rw [hdet, hk4, hk5] at h
  simpa using h

/-- Division-free global completion bound for the compatible singular branch. -/
theorem singular_compatible_completion_cleared
    (p q s b4 b5 x y : ℝ)
    (hdet : det2 p q s = 0)
    (hk4 : k4 q s b4 b5 = 0)
    (hk5 : k5 p q b4 b5 = 0) :
    4 * trace2 p s * residual p q s b4 b5 x y ≤ b4 ^ 2 + b5 ^ 2 := by
  have hid := singular_compatible_trace_identity p q s b4 b5 x y hdet hk4 hk5
  have hsquares :
      0 ≤ (2 * (p * x + q * y) + b4) ^ 2 +
        (2 * (q * x + s * y) + b5) ^ 2 :=
    add_nonneg (sq_nonneg _) (sq_nonneg _)
  dsimp [residual] at *
  nlinarith

/-- Finite pivot-free completion cost on the nonzero rank-one branch. -/
theorem singular_compatible_completion
    (p q s b4 b5 x y : ℝ)
    (htau : 0 < trace2 p s)
    (hdet : det2 p q s = 0)
    (hk4 : k4 q s b4 b5 = 0)
    (hk5 : k5 p q b4 b5 = 0) :
    residual p q s b4 b5 x y ≤
      (b4 ^ 2 + b5 ^ 2) / (4 * trace2 p s) := by
  have hclear := singular_compatible_completion_cleared p q s b4 b5 x y hdet hk4 hk5
  have h4tau : 0 < 4 * trace2 p s := by positivity
  apply (le_div_iff₀ h4tau).2
  nlinarith

/-- Compatibility implies that `b` is the trace-eigenvector of the rank-one block. -/
theorem compatible_range_first
    (p q s b4 b5 : ℝ)
    (hk4 : k4 q s b4 b5 = 0) :
    p * b4 + q * b5 = trace2 p s * b4 := by
  dsimp [k4, trace2] at hk4 ⊢
  nlinarith

/-- Second coordinate of the compatible trace-eigenvector identity. -/
theorem compatible_range_second
    (p q s b4 b5 : ℝ)
    (hk5 : k5 p q b4 b5 = 0) :
    q * b4 + s * b5 = trace2 p s * b5 := by
  dsimp [k5, trace2] at hk5 ⊢
  nlinarith

/-- On the singular branch, the squared compatibility defect is exactly `trace * N`. -/
theorem singular_incompatibility_norm
    (p q s b4 b5 : ℝ)
    (hdet : det2 p q s = 0) :
    k4 q s b4 b5 ^ 2 + k5 p q b4 b5 ^ 2 =
      trace2 p s * adjNumerator p q s b4 b5 := by
  have h := incompatibility_norm_identity p q s b4 b5
  rw [hdet] at h
  simpa using h

/-- A nonzero compatibility defect forces a strictly positive adjugate numerator when trace is positive. -/
theorem singular_incompatible_adjnumerator_pos
    (p q s b4 b5 : ℝ)
    (htau : 0 < trace2 p s)
    (hdet : det2 p q s = 0)
    (hnz : k4 q s b4 b5 ≠ 0 ∨ k5 p q b4 b5 ≠ 0) :
    0 < adjNumerator p q s b4 b5 := by
  have hid := singular_incompatibility_norm p q s b4 b5 hdet
  rcases hnz with hk4 | hk5
  · have hsq : 0 < k4 q s b4 b5 ^ 2 := sq_pos_of_ne_zero hk4
    have hother : 0 ≤ k5 p q b4 b5 ^ 2 := sq_nonneg _
    nlinarith
  · have hsq : 0 < k5 p q b4 b5 ^ 2 := sq_pos_of_ne_zero hk5
    have hother : 0 ≤ k4 q s b4 b5 ^ 2 := sq_nonneg _
    nlinarith

/-- The adjugate defect vector is a kernel vector on `det H = 0`. -/
theorem singular_adjugate_kernel_quadratic
    (p q s b4 b5 : ℝ)
    (hdet : det2 p q s = 0) :
    quad p q s (k4 q s b4 b5) (k5 p q b4 b5) = 0 := by
  have h1 := adjugate_kernel_first p q s b4 b5
  have h2 := adjugate_kernel_second p q s b4 b5
  rw [hdet] at h1 h2
  have h1z : p * k4 q s b4 b5 + q * k5 p q b4 b5 = 0 := by simpa using h1
  have h2z : q * k4 q s b4 b5 + s * k5 p q b4 b5 = 0 := by simpa using h2
  dsimp [quad]
  linear_combination k4 q s b4 b5 * h1z + k5 p q b4 b5 * h2z

/-- Every scalar multiple of the adjugate defect remains in the quadratic kernel. -/
theorem singular_adjugate_kernel_ray_quadratic
    (p q s b4 b5 t : ℝ)
    (hdet : det2 p q s = 0) :
    quad p q s (t * k4 q s b4 b5) (t * k5 p q b4 b5) = 0 := by
  calc
    quad p q s (t * k4 q s b4 b5) (t * k5 p q b4 b5) =
        t ^ 2 * quad p q s (k4 q s b4 b5) (k5 p q b4 b5) := by
          dsimp [quad]
          ring
    _ = 0 := by rw [singular_adjugate_kernel_quadratic p q s b4 b5 hdet]; ring

/-- Pairing the adjugate defect with the bias gives exactly `N`. -/
theorem adjugate_kernel_bias
    (p q s b4 b5 : ℝ) :
    bias b4 b5 (k4 q s b4 b5) (k5 p q b4 b5) =
      adjNumerator p q s b4 b5 := by
  dsimp [bias, k4, k5, adjNumerator]
  ring

/-- A nonzero compatibility defect makes the singular residual unbounded above on an explicit kernel ray. -/
theorem singular_incompatible_unbounded
    (p q s b4 b5 : ℝ)
    (htau : 0 < trace2 p s)
    (hdet : det2 p q s = 0)
    (hnz : k4 q s b4 b5 ≠ 0 ∨ k5 p q b4 b5 ≠ 0) :
    ∀ C : ℝ, ∃ x y : ℝ, C < residual p q s b4 b5 x y := by
  intro C
  have hN : 0 < adjNumerator p q s b4 b5 :=
    singular_incompatible_adjnumerator_pos p q s b4 b5 htau hdet hnz
  have hNne : adjNumerator p q s b4 b5 ≠ 0 := ne_of_gt hN
  let t : ℝ := (C + 1) / adjNumerator p q s b4 b5
  refine ⟨-t * k4 q s b4 b5, -t * k5 p q b4 b5, ?_⟩
  have hq := singular_adjugate_kernel_ray_quadratic p q s b4 b5 (-t) hdet
  have hb0 := adjugate_kernel_bias p q s b4 b5
  have hb :
      bias b4 b5 (-t * k4 q s b4 b5) (-t * k5 p q b4 b5) =
        -t * adjNumerator p q s b4 b5 := by
    dsimp [bias] at hb0 ⊢
    nlinarith
  have ht : t * adjNumerator p q s b4 b5 = C + 1 := by
    dsimp [t]
    exact div_mul_cancel₀ (C + 1) hNne
  dsimp [residual]
  nlinarith

/-- Nonnegative diagonal entries with zero trace force both diagonals to vanish. -/
theorem zero_trace_diagonals
    (p s : ℝ)
    (hp : 0 ≤ p)
    (hs : 0 ≤ s)
    (htau : trace2 p s = 0) :
    p = 0 ∧ s = 0 := by
  dsimp [trace2] at htau
  constructor <;> nlinarith

/-- The PSD singular zero-trace branch is exactly the zero 2x2 matrix. -/
theorem zero_matrix_of_psd_singular_trace_zero
    (p q s : ℝ)
    (hp : 0 ≤ p)
    (hs : 0 ≤ s)
    (hdet : det2 p q s = 0)
    (htau : trace2 p s = 0) :
    p = 0 ∧ q = 0 ∧ s = 0 := by
  rcases zero_trace_diagonals p s hp hs htau with ⟨hp0, hs0⟩
  have hq2 : q ^ 2 = 0 := by
    dsimp [det2] at hdet
    rw [hp0, hs0] at hdet
    nlinarith
  have hq0 : q = 0 := by
    exact sq_eq_zero_iff.mp hq2
  exact ⟨hp0, hq0, hs0⟩

/-- A nonzero affine bias is unbounded above when the quadratic matrix is zero. -/
theorem zero_matrix_nonzero_bias_unbounded
    (b4 b5 : ℝ)
    (hnz : b4 ≠ 0 ∨ b5 ≠ 0) :
    ∀ C : ℝ, ∃ x y : ℝ, C < -(bias b4 b5 x y) := by
  intro C
  rcases hnz with hb4 | hb5
  · let x : ℝ := -(C + 1) / b4
    refine ⟨x, 0, ?_⟩
    have hx : x * b4 = -(C + 1) := by
      dsimp [x]
      exact div_mul_cancel₀ (-(C + 1)) hb4
    dsimp [bias]
    nlinarith
  · let y : ℝ := -(C + 1) / b5
    refine ⟨0, y, ?_⟩
    have hy : y * b5 = -(C + 1) := by
      dsimp [y]
      exact div_mul_cancel₀ (-(C + 1)) hb5
    dsimp [bias]
    nlinarith

/--
Complete pivot-free existence classifier for a finite global upper bound on the
singular PSD branch.  The compatible nonzero-rank branch and the zero-matrix
branch are deliberately separate.
-/
theorem singular_psd_finite_upper_bound_iff
    (p q s b4 b5 : ℝ)
    (hp : 0 ≤ p)
    (hs : 0 ≤ s)
    (hdet : det2 p q s = 0) :
    (∃ C : ℝ, ∀ x y : ℝ, residual p q s b4 b5 x y ≤ C) ↔
      ((0 < trace2 p s ∧ k4 q s b4 b5 = 0 ∧ k5 p q b4 b5 = 0) ∨
       (trace2 p s = 0 ∧ b4 = 0 ∧ b5 = 0)) := by
  constructor
  · rintro ⟨C, hC⟩
    have htau_nonneg : 0 ≤ trace2 p s := by
      dsimp [trace2]
      linarith
    rcases lt_or_eq_of_le htau_nonneg with htau | htau
    · left
      have hk4 : k4 q s b4 b5 = 0 := by
        by_contra hk4ne
        rcases singular_incompatible_unbounded p q s b4 b5 htau hdet (Or.inl hk4ne) C with
          ⟨x, y, hgt⟩
        have hle := hC x y
        linarith
      have hk5 : k5 p q b4 b5 = 0 := by
        by_contra hk5ne
        rcases singular_incompatible_unbounded p q s b4 b5 htau hdet (Or.inr hk5ne) C with
          ⟨x, y, hgt⟩
        have hle := hC x y
        linarith
      exact ⟨htau, hk4, hk5⟩
    · right
      have hzero := zero_matrix_of_psd_singular_trace_zero p q s hp hs hdet htau
      rcases hzero with ⟨hp0, hq0, hs0⟩
      have hb4 : b4 = 0 := by
        by_contra hb4ne
        rcases zero_matrix_nonzero_bias_unbounded b4 b5 (Or.inl hb4ne) C with ⟨x, y, hgt⟩
        have hle := hC x y
        rw [hp0, hq0, hs0] at hle
        dsimp [residual, quad] at hle
        linarith
      have hb5 : b5 = 0 := by
        by_contra hb5ne
        rcases zero_matrix_nonzero_bias_unbounded b4 b5 (Or.inr hb5ne) C with ⟨x, y, hgt⟩
        have hle := hC x y
        rw [hp0, hq0, hs0] at hle
        dsimp [residual, quad] at hle
        linarith
      exact ⟨htau, hb4, hb5⟩
  · intro hclass
    rcases hclass with hcompat | hzero
    · rcases hcompat with ⟨htau, hk4, hk5⟩
      refine ⟨(b4 ^ 2 + b5 ^ 2) / (4 * trace2 p s), ?_⟩
      intro x y
      exact singular_compatible_completion p q s b4 b5 x y htau hdet hk4 hk5
    · rcases hzero with ⟨htau, hb4, hb5⟩
      have hmatrix := zero_matrix_of_psd_singular_trace_zero p q s hp hs hdet htau
      rcases hmatrix with ⟨hp0, hq0, hs0⟩
      refine ⟨0, ?_⟩
      intro x y
      rw [hp0, hq0, hs0, hb4, hb5]
      norm_num [residual, quad, bias]

#print axioms RouteBP5SingularPSD.adjugate_kernel_first
#print axioms RouteBP5SingularPSD.adjugate_kernel_second
#print axioms RouteBP5SingularPSD.incompatibility_norm_identity
#print axioms RouteBP5SingularPSD.trace_completion_identity
#print axioms RouteBP5SingularPSD.singular_compatible_trace_identity
#print axioms RouteBP5SingularPSD.singular_compatible_completion_cleared
#print axioms RouteBP5SingularPSD.singular_compatible_completion
#print axioms RouteBP5SingularPSD.compatible_range_first
#print axioms RouteBP5SingularPSD.compatible_range_second
#print axioms RouteBP5SingularPSD.singular_incompatibility_norm
#print axioms RouteBP5SingularPSD.singular_incompatible_adjnumerator_pos
#print axioms RouteBP5SingularPSD.singular_adjugate_kernel_quadratic
#print axioms RouteBP5SingularPSD.singular_adjugate_kernel_ray_quadratic
#print axioms RouteBP5SingularPSD.adjugate_kernel_bias
#print axioms RouteBP5SingularPSD.singular_incompatible_unbounded
#print axioms RouteBP5SingularPSD.zero_trace_diagonals
#print axioms RouteBP5SingularPSD.zero_matrix_of_psd_singular_trace_zero
#print axioms RouteBP5SingularPSD.zero_matrix_nonzero_bias_unbounded
#print axioms RouteBP5SingularPSD.singular_psd_finite_upper_bound_iff

end RouteBP5SingularPSD
