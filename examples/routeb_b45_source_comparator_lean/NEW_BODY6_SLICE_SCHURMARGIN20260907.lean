import NEW_BODY6_SLICE_SELF3MASSBIND20260907

set_option autoImplicit false

namespace NEW_BODY6_SLICE_SCHURMARGIN20260907

noncomputable section

open NEW_BODY6_SLICE_VGRAM_Source20260907 NEW_BODY6_SLICE_MASSTAIL_Source20260907
open NEW_BODY6_SLICE_TAILPSD20260907 NEW_BODY6_SLICE_TAILINVERSE20260907
open NEW_BODY6_SLICE_TAILSCHUR20260907 NEW_BODY6_SLICE_SCHURREMAINDER20260907
open NEW_BODY6_SLICE_SOURCEBLOCKBIND20260907 NEW_BODY6_SLICE_SELF3MASSBIND20260907

abbrev Front := Fin 3 → ℝ
abbrev FrontBlock := Fin 3 → Fin 3 → ℝ
abbrev CrossX := Fin 3 → Fin 2 → ℝ
abbrev CrossY := Fin 2 → Fin 3 → ℝ
abbrev TailBlock := Fin 2 → Fin 2 → ℝ

/- UNCOMPILED. S denotes solved columns D*Y; v=-S*u is the eliminated tail.
   Residuals are typed expressions, not an assembled full-matrix PSD theorem. -/
def eliminatedTail (S : CrossY) (u : Front) : Fin 2 → ℝ :=
  fun a => -(∑ j : Fin 3, S a j * u j)

def frontAction (R : FrontBlock) (u : Front) (i : Fin 3) : ℝ :=
  ∑ j : Fin 3, R i j * u j

def frontResidual (A : FrontBlock) (X : CrossX) (S : CrossY) (u : Front) (i : Fin 3) : ℝ :=
  frontAction A u i + ∑ a : Fin 2, X i a * eliminatedTail S u a

def tailResidual (B : TailBlock) (Y S : CrossY) (u : Front) (a : Fin 2) : ℝ :=
  (∑ j : Fin 3, Y a j * u j) + action2 B (eliminatedTail S u) a

/- External margin witness: mu=0 allows PSD; mu>0 is a caller-supplied
   stronger margin. No value of mu or proof of this predicate is synthesized. -/
def RemainderMargin (R : FrontBlock) (mu : ℝ) : Prop :=
  (∀ i j, R i j = R j i) ∧ 0 ≤ mu ∧
    ∀ u : Front, mu * (∑ i : Fin 3, u i ^ 2) ≤ ∑ i : Fin 3, u i * frontAction R u i

theorem front_residual_reduction_attempt (A R : FrontBlock) (X : CrossX) (S : CrossY)
    (hR : ∀ i j, R i j = A i j - ∑ a : Fin 2, X i a * S a j) (u : Front) (i : Fin 3) :
    frontResidual A X S u i = frontAction R u i := by
  unfold frontResidual frontAction eliminatedTail
  simp_rw [hR]
  norm_num [Fin.sum_univ_succ] <;> ring

theorem tail_residual_zero_attempt (B : TailBlock) (Y S : CrossY)
    (hs : ∀ j, action2 B (fun a => S a j) = (fun a => Y a j)) (u : Front) (a : Fin 2) :
    tailResidual B Y S u a = 0 := by
  have h0 := congrFun (hs 0) a
  have h1 := congrFun (hs 1) a
  have h2 := congrFun (hs 2) a
  norm_num [action2, Fin.sum_univ_succ] at h0 h1 h2
  norm_num [tailResidual, eliminatedTail, action2, Fin.sum_univ_succ]
  linear_combination -(u 0) * h0 - (u 1) * h1 - (u 2) * h2

structure SourceSchurMarginContract (q : Fin 6 → ℝ) (m kappa mu : ℝ)
    (A : FrontBlock) (X : CrossX) (Y : CrossY) (R : FrontBlock) : Prop where
  sourceBinding : SourceBlockBinding q A X Y
  tailCore : SchurRemainderContract 3 3 (sourceTail q) (q 4) offset m kappa A X Y
  remainderFormula : ∀ i j, R i j = schurRemainder (q 4) offset m kappa A X Y i j
  margin : RemainderMargin R mu

theorem source_margin_contract_attempt (hc : CenterOffsetTarget)
    (m kappa mu : ℝ) (hw : SourceWeightsTarget m kappa)
    (hk : 0 < kappa) (hm : 0 ≤ m) (hh : 0 ≤ offset ^ 2) (q : Fin 6 → ℝ)
    (A : FrontBlock) (X : CrossX) (Y : CrossY) (R : FrontBlock)
    (hb : SourceBlockBinding q A X Y)
    (hR : ∀ i j, R i j = schurRemainder (q 4) offset m kappa A X Y i j)
    (hmargin : RemainderMargin R mu) : SourceSchurMarginContract q m kappa mu A X Y R :=
  ⟨hb, source_remainder_contract_attempt hc m kappa hw hk hm hh q A X Y, hR, hmargin⟩

/- SELF3 supplies canonical A binding; the remainder margin is still external. -/
theorem canonical_margin_contract_attempt (hc : CenterOffsetTarget)
    (m kappa mu : ℝ) (hw : SourceWeightsTarget m kappa)
    (hk : 0 < kappa) (hm : 0 ≤ m) (hh : 0 ≤ offset ^ 2) (q : Fin 6 → ℝ)
    (hmargin : RemainderMargin
      (schurRemainder (q 4) offset m kappa (explicitWeightedA q m kappa) (mixedX q m kappa) (mixedY q m kappa)) mu) :
    SourceSchurMarginContract q m kappa mu (explicitWeightedA q m kappa) (mixedX q m kappa) (mixedY q m kappa)
      (schurRemainder (q 4) offset m kappa (explicitWeightedA q m kappa) (mixedX q m kappa) (mixedY q m kappa)) :=
  source_margin_contract_attempt hc m kappa mu hw hk hm hh q _ _ _ _
    (explicit_A_mixed_source_binding_attempt hc m kappa hw q) (fun _ _ => rfl) hmargin

/- Consumer: v=-inverseTail*Y*u yields zero tail residual, front residual R*u,
   and the externally supplied front margin. No unrestricted block PSD claim. -/
theorem source_residual_consumer_attempt (q : Fin 6 → ℝ) (m kappa mu : ℝ)
    (A : FrontBlock) (X : CrossX) (Y : CrossY) (R : FrontBlock)
    (hc : SourceSchurMarginContract q m kappa mu A X Y R) (u : Front) :
    (∀ a, tailResidual (sourceTail q) Y (solvedRight 3 (q 4) offset m kappa Y) u a = 0) ∧
    (∀ i, frontResidual A X (solvedRight 3 (q 4) offset m kappa Y) u i = frontAction R u i) ∧
    mu * (∑ i : Fin 3, u i ^ 2) ≤
      ∑ i : Fin 3, u i * frontResidual A X (solvedRight 3 (q 4) offset m kappa Y) u i := by
  have hR : ∀ i j, R i j = A i j - ∑ a : Fin 2, X i a * solvedRight 3 (q 4) offset m kappa Y a j := by
    intro i j
    rw [hc.remainderFormula i j]
    unfold schurRemainder
    rw [hc.tailCore.tailAdapter.correctionViaSolve i j]
  have hf := front_residual_reduction_attempt A R X (solvedRight 3 (q 4) offset m kappa Y) hR u
  refine ⟨tail_residual_zero_attempt (sourceTail q) Y _ hc.tailCore.tailAdapter.solveColumns u, hf, ?_⟩
  simp_rw [hf]
  exact hc.margin.2.2 u

/- Missing margin evidence is pending. An actual violating vector refutes it. -/
theorem margin_violation_rejects_attempt (R : FrontBlock) (mu : ℝ)
    (bad : ∃ u : Front, (∑ i : Fin 3, u i * frontAction R u i) < mu * (∑ i : Fin 3, u i ^ 2)) :
    ¬ RemainderMargin R mu := by
  intro hm
  obtain ⟨u, hu⟩ := bad
  exact (not_lt_of_ge (hm.2.2 u)) hu

/- No numerical margin/cross-block witness, full 5x5/6DOF PSD, P4 parameter
   admission, Fourier, coverage, Lean verification or registry promotion. -/
end
end NEW_BODY6_SLICE_SCHURMARGIN20260907
