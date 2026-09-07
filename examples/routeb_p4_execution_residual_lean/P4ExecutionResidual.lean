import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
# Route-B P4 execution-lift residual algebra

This sidecar formalizes only the source-independent algebraic interface from
`agent_review_inbox/review-T-P4-007-liuguanyi-20260907T0212.md`.

The central point is that a real lift of a Float64 linear solve must retain an
explicit solve defect.  The theorems below also formalize the centered
reference/runtime split and the zero-slice obstruction for a relative residual
envelope.

No Float64 error bound, DH source binding, residual coverage, P4/M4 admission,
or registry mutation is proved here.
-/

set_option autoImplicit false

namespace RouteBP4ExecutionResidual

noncomputable section

/-- The block `(4,5)` force-coordinate space, kept abstract as two real
components. -/
abbrev VecB := Fin 2 → ℝ

/-- Block projection of the lifted linear-solve defect

`M*a - (tau - C - G)`

when `massLocal = M_BB*a_B` and `massRemote = M_BD*a_D`. -/
def blockSolveDefect
    (massLocal massRemote tau C G : VecB) : VecB :=
  fun i => massLocal i + massRemote i - (tau i - C i - G i)

/-- Generalized-force residual `I_B*f_B - M0_BB*a_B`, with both already
projected to the two block coordinates. -/
def blockResidual (If M0a : VecB) : VecB :=
  fun i => If i - M0a i

/-- Rearrangement of the definition of the solve defect.  The sign is the
important interface fact: `tau` equals assembled force **minus** the defect. -/
theorem block_tau_from_solve_defect
    (massLocal massRemote tau C G : VecB) :
    tau = fun i =>
      massLocal i + massRemote i + C i + G i
        - blockSolveDefect massLocal massRemote tau C G i := by
  ext i
  simp [blockSolveDefect]
  ring

/-- Exact execution-level block residual identity with an explicit lifted
linear-solve defect.

This is the formal version of

`l_F = (I f - tau_B) + (M_BB a_B - M0 a_B) + M_BD a_D
       + C_B + G_B - solveDefect_B`.
-/
theorem block_residual_with_solve_defect
    (If M0a massLocal massRemote tau C G : VecB) :
    blockResidual If M0a = fun i =>
      (If i - tau i)
        + (massLocal i - M0a i)
        + massRemote i + C i + G i
        - blockSolveDefect massLocal massRemote tau C G i := by
  ext i
  simp [blockResidual, blockSolveDefect]
  ring

/-- The earlier exact-solve algebra is recovered only after explicitly setting
the solve defect to zero. -/
theorem block_residual_exact_solve
    (If M0a massLocal massRemote tau C G : VecB)
    (hsolve : blockSolveDefect massLocal massRemote tau C G = 0) :
    blockResidual If M0a = fun i =>
      (If i - tau i)
        + (massLocal i - M0a i)
        + massRemote i + C i + G i := by
  rw [block_residual_with_solve_defect]
  funext i
  have hs : blockSolveDefect massLocal massRemote tau C G i = 0 := by
    exact congrFun hsolve i
  rw [hs]
  ring

/-- Generic centered source/reference split.  A runtime offset at the reference
point is automatically subtracted rather than charged twice as an additive
bias. -/
theorem centered_reference_split
    {α : Type*}
    (Gexec Gref delta : α → VecB)
    (q q0 : α)
    (hG : ∀ x i, Gexec x i = Gref x i + delta x i) :
    (fun i => Gexec q i - Gexec q0 i) = fun i =>
      (Gref q i - Gref q0 i) + (delta q i - delta q0 i) := by
  ext i
  rw [hG q i, hG q0 i]
  ring

/-- Centered split with an arbitrary model term retained on the reference side.
This is the direct abstract form of

`Gexec(q)-Gexec(q0)-model(q)
 = [Gref(q)-Gref(q0)-model(q)] + [delta(q)-delta(q0)]`.
-/
theorem centered_reference_split_with_model
    {α : Type*}
    (Gexec Gref delta model : α → VecB)
    (q q0 : α)
    (hG : ∀ x i, Gexec x i = Gref x i + delta x i) :
    (fun i => Gexec q i - Gexec q0 i - model q i) = fun i =>
      (Gref q i - Gref q0 i - model q i)
        + (delta q i - delta q0 i) := by
  ext i
  rw [hG q i, hG q0 i]
  ring

/-- A scalar relative envelope forces the residual to vanish on the zero slice
of its reference coordinate. -/
theorem relative_envelope_zero_slice
    (l y k : ℝ)
    (h : |l| ≤ k * |y|)
    (hy : y = 0) :
    l = 0 := by
  subst y
  simp only [abs_zero, mul_zero] at h
  have hnonneg : 0 ≤ |l| := abs_nonneg l
  have habs : |l| = 0 := le_antisymm h hnonneg
  exact abs_eq_zero.mp habs

/-- Pointwise form of the zero-slice condition on an arbitrary state space. -/
theorem relative_envelope_zero_slice_pointwise
    {α : Type*}
    (l y : α → ℝ)
    (k : ℝ)
    (h : ∀ z, |l z| ≤ k * |y z|)
    (z : α)
    (hy : y z = 0) :
    l z = 0 := by
  exact relative_envelope_zero_slice (l z) (y z) k (h z) hy

/-- Counterexample interface: one nonzero residual on a zero slice rules out
*every* global relative envelope with the proposed coefficient `k`. -/
theorem no_relative_envelope_of_nonzero_zero_slice
    {α : Type*}
    (l y : α → ℝ)
    (k : ℝ)
    (z : α)
    (hy : y z = 0)
    (hl : l z ≠ 0) :
    ¬ (∀ x, |l x| ≤ k * |y x|) := by
  intro h
  exact hl (relative_envelope_zero_slice_pointwise l y k h z hy)

#print axioms block_tau_from_solve_defect
#print axioms block_residual_with_solve_defect
#print axioms block_residual_exact_solve
#print axioms centered_reference_split
#print axioms centered_reference_split_with_model
#print axioms relative_envelope_zero_slice
#print axioms relative_envelope_zero_slice_pointwise
#print axioms no_relative_envelope_of_nonzero_zero_slice

end

end RouteBP4ExecutionResidual
