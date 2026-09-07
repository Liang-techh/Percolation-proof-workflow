import NEW_BODY6_SLICE_EXACTSCHURCOEFF20260907

set_option autoImplicit false

namespace NEW_BODY6_SLICE_TAILSOLVECERT20260907

noncomputable section

open NEW_BODY6_SLICE_MARGINUNIFORM20260907 NEW_BODY6_SLICE_SCHURMARGIN20260907
open NEW_BODY6_SLICE_EXACTSCHURCOEFF20260907 NEW_BODY6_SLICE_TAILPSD20260907
open NEW_BODY6_SLICE_TAILINVERSE20260907 NEW_BODY6_SLICE_TAILSCHUR20260907
open NEW_BODY6_SLICE_VGRAM_Source20260907 NEW_BODY6_SLICE_MASSTAIL_Source20260907
open NEW_BODY6_SLICE_MASSTAIL_Core20260907

/- OPEN_UNCOMPILED. B is the actual tail, D is its proposed inverse, and
   solved columns V=D*Y are rectangular. Every field uses one q/m/kappa/offset. -/
structure SourceTailInverseCertificate (q : Config) (m kappa : ℝ) (B D : TailBlock) : Prop where
  center : CenterOffsetTarget
  weights : SourceWeightsTarget m kappa
  kappaPositive : 0 < kappa
  massNonnegative : 0 ≤ m
  offsetSquareNonnegative : 0 ≤ offset ^ 2
  sourceB : B = sourceTail q
  expressionD : D = inverseTail (q 4) offset m kappa
  denominatorsPositive :
    0 < kappa + m * offset ^ 2 * Real.sin (q 4) ^ 2 ∧ 0 < kappa + m * offset ^ 2
  BD_identity : ∀ a b, product2 B D a b = identity2 a b
  DB_identity : ∀ a b, product2 D B a b = identity2 a b

/- Consume the exact Schur seam's inverse evidence; never infer it from R's
   coefficient equality or margin alone. Actual source premises remain fields. -/
theorem inverse_certificate_from_exact_seam_attempt (hc : CenterOffsetTarget)
    (q : Config) (m kappa : ℝ) (hw : SourceWeightsTarget m kappa)
    (hk : 0 < kappa) (hm : 0 ≤ m) (hh : 0 ≤ offset ^ 2)
    (A R : FrontBlock) (X : CrossX) (Y : CrossY)
    (he : ExactSchurCoefficientContract q m kappa A X Y R) :
    SourceTailInverseCertificate q m kappa (sourceTail q) (inverseTail (q 4) offset m kappa) :=
  ⟨hc, hw, hk, hm, hh, rfl, rfl, denominators_positive_attempt (q 4) offset m kappa hk hm hh,
    he.tailCore.tailAdapter.leftInverse, he.tailCore.tailAdapter.rightInverse⟩

/- Restricted right-hand-side evidence alone is weaker than an inverse. -/
def ColumnSolveEvidence (B : TailBlock) (Y V : CrossY) : Prop :=
  ∀ j, action2 B (fun a => V a j) = (fun a => Y a j)

theorem BD_identity_solves_attempt (B D : TailBlock)
    (hi : ∀ a b, product2 B D a b = identity2 a b) (y : Fin 2 → ℝ) :
    action2 B (action2 D y) = y := by
  funext a
  have h0 := hi a 0
  have h1 := hi a 1
  fin_cases a <;>
    norm_num [product2, identity2, action2, Fin.sum_univ_succ] at h0 h1 ⊢ <;>
    linear_combination (y 0) * h0 + (y 1) * h1

structure SourceTailSolveCertificate (q : Config) (m kappa : ℝ)
    (B D : TailBlock) (Y V : CrossY) : Prop where
  inverseCertificate : SourceTailInverseCertificate q m kappa B D
  actionBinding : ∀ a j, V a j = action2 D (fun b => Y b j) a
  columnSolve : ColumnSolveEvidence B Y V

theorem solvedRight_certificate_attempt (q : Config) (m kappa : ℝ) (B D : TailBlock)
    (hi : SourceTailInverseCertificate q m kappa B D) (Y : CrossY) :
    SourceTailSolveCertificate q m kappa B D Y (solvedRight 3 (q 4) offset m kappa Y) := by
  have ha : ∀ j, action2 D (fun b => Y b j) =
      (fun a => solvedRight 3 (q 4) offset m kappa Y a j) := by
    intro j
    rw [hi.expressionD]
    exact inverse_action_formula_attempt (q 4) offset m kappa (fun b => Y b j)
  refine ⟨hi, ?_, ?_⟩
  · intro a j
    exact (congrFun (ha j) a).symm
  · intro j
    rw [← ha j]
    exact BD_identity_solves_attempt B D hi.BD_identity (fun b => Y b j)

/- Exact abstract controls only: none is a claimed physical body-6 instance.
   Lean's 1/0=0 does not supply an inverse when the first denominator is zero. -/
theorem denominator_zero_counterexample_attempt :
    (0 : ℝ) + 1 * (1 : ℝ) ^ 2 * Real.sin 0 ^ 2 = 0 ∧
    product2 (explicitTail 0 1 1 0) (inverseTail 0 1 1 0) 0 0 ≠ identity2 0 0 := by
  norm_num [explicitTail, inverseTail, product2, identity2, Fin.sum_univ_succ]

/- Positive denominators and matching 2x2 dimensions do not certify D=I. -/
theorem positive_denominators_wrong_D_attempt :
    0 < (2 : ℝ) + 1 * (1 : ℝ) ^ 2 * Real.sin 0 ^ 2 ∧
    0 < (2 : ℝ) + 1 * (1 : ℝ) ^ 2 ∧
    product2 (explicitTail 0 1 1 2) identity2 0 0 ≠ identity2 0 0 := by
  norm_num [explicitTail, product2, identity2, Fin.sum_univ_succ]

/- Even action-consistent columns V=D*Y with B*V=Y can miss a false inverse:
   B=diag(2,3), D=0, Y=V=0. The tested right-hand sides span no directions. -/
theorem solved_columns_not_inverse_attempt :
    (∀ a j, (0 : CrossY) a j = action2 (0 : TailBlock) (fun b => (0 : CrossY) b j) a) ∧
    ColumnSolveEvidence (explicitTail 0 1 1 2) (0 : CrossY) (0 : CrossY) ∧
    product2 (explicitTail 0 1 1 2) (0 : TailBlock) 0 0 ≠ identity2 0 0 := by
  refine ⟨?_, ?_, ?_⟩
  · intro a j
    norm_num [action2, Fin.sum_univ_succ]
  · intro j
    funext a
    norm_num [action2, Fin.sum_univ_succ]
  · norm_num [product2, identity2, Fin.sum_univ_succ]

/- No mixed source values are supplied by a solve certificate for arbitrary Y.
   No full-body PSD, margin, Fourier, coverage, compilation or registry claim. -/
end
end NEW_BODY6_SLICE_TAILSOLVECERT20260907
