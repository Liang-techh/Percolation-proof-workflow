import NEW_BODY6_SLICE_TAILSCHUR20260907

set_option autoImplicit false

namespace NEW_BODY6_SLICE_SCHURREMAINDER20260907

noncomputable section

open NEW_BODY6_SLICE_MASSTAIL_Source20260907 NEW_BODY6_SLICE_VGRAM_Source20260907
open NEW_BODY6_SLICE_TAILPSD20260907 NEW_BODY6_SLICE_TAILINVERSE20260907
open NEW_BODY6_SLICE_TAILSCHUR20260907

variable {r c : ℕ}

/- UNCOMPILED. A is r x c, X is r x 2, Y is 2 x c; only the internal
   two slots inherit actual tail order {3,4}. No source values for A/X/Y. -/
def schurRemainder (z h m kappa : ℝ) (A : Fin r → Fin c → ℝ)
    (X : Fin r → Fin 2 → ℝ) (Y : Fin 2 → Fin c → ℝ) (i : Fin r) (j : Fin c) : ℝ :=
  A i j - schurCorrection r c z h m kappa X Y i j

def remainderViaSolve (z h m kappa : ℝ) (A : Fin r → Fin c → ℝ)
    (X : Fin r → Fin 2 → ℝ) (Y : Fin 2 → Fin c → ℝ) (i : Fin r) (j : Fin c) : ℝ :=
  A i j - ∑ a : Fin 2, X i a * solvedRight c z h m kappa Y a j

def remainderViaProduct (z h m kappa : ℝ) (A : Fin r → Fin c → ℝ)
    (X : Fin r → Fin 2 → ℝ) (Y : Fin 2 → Fin c → ℝ) (i : Fin r) (j : Fin c) : ℝ :=
  A i j - ∑ a : Fin 2, X i a * action2 (inverseTail z h m kappa) (fun b => Y b j) a

theorem remainder_coefficient_attempt (z h m kappa : ℝ) (A : Fin r → Fin c → ℝ)
    (X : Fin r → Fin 2 → ℝ) (Y : Fin 2 → Fin c → ℝ) (i : Fin r) (j : Fin c) :
    schurRemainder z h m kappa A X Y i j = A i j -
      X i 0 * Y 0 j / (kappa + m * h ^ 2 * Real.sin z ^ 2) -
      X i 1 * Y 1 j / (kappa + m * h ^ 2) := by
  unfold schurRemainder
  rw [correction_expansion_attempt]
  unfold explicitCorrection
  ring

/- Same solved column as finite matrix action; inverse validity is carried
   separately by the imported TailEliminationAdapter. -/
theorem solved_column_product_attempt (z h m kappa : ℝ)
    (Y : Fin 2 → Fin c → ℝ) (j : Fin c) :
    (fun a => solvedRight c z h m kappa Y a j) =
      action2 (inverseTail z h m kappa) (fun b => Y b j) := by
  exact (inverse_action_formula_attempt z h m kappa (fun b => Y b j)).symm

theorem remainder_paths_attempt (z h m kappa : ℝ) (A : Fin r → Fin c → ℝ)
    (X : Fin r → Fin 2 → ℝ) (Y : Fin 2 → Fin c → ℝ) (i : Fin r) (j : Fin c) :
    schurRemainder z h m kappa A X Y i j = remainderViaSolve z h m kappa A X Y i j ∧
    schurRemainder z h m kappa A X Y i j = remainderViaProduct z h m kappa A X Y i j := by
  have hs : schurRemainder z h m kappa A X Y i j =
      remainderViaSolve z h m kappa A X Y i j := by
    unfold schurRemainder remainderViaSolve
    rw [correction_via_solve_attempt]
  refine ⟨hs, ?_⟩
  rw [hs]
  unfold remainderViaSolve remainderViaProduct
  rw [← solved_column_product_attempt z h m kappa Y j]

/- Keep the existing two-sided inverse, positive denominators and column solve
   package alongside the new A-minus-correction expressions. -/
structure SchurRemainderContract (r c : ℕ) (B : Fin 2 → Fin 2 → ℝ)
    (z h m kappa : ℝ) (A : Fin r → Fin c → ℝ)
    (X : Fin r → Fin 2 → ℝ) (Y : Fin 2 → Fin c → ℝ) : Prop where
  tailAdapter : TailEliminationAdapter r c B z h m kappa X Y
  coefficient : ∀ i j, schurRemainder z h m kappa A X Y i j = A i j -
    X i 0 * Y 0 j / (kappa + m * h ^ 2 * Real.sin z ^ 2) -
    X i 1 * Y 1 j / (kappa + m * h ^ 2)
  evaluationPaths : ∀ i j,
    schurRemainder z h m kappa A X Y i j = remainderViaSolve z h m kappa A X Y i j ∧
    schurRemainder z h m kappa A X Y i j = remainderViaProduct z h m kappa A X Y i j

theorem remainder_from_adapter_attempt (B : Fin 2 → Fin 2 → ℝ)
    (z h m kappa : ℝ) (A : Fin r → Fin c → ℝ)
    (X : Fin r → Fin 2 → ℝ) (Y : Fin 2 → Fin c → ℝ)
    (ha : TailEliminationAdapter r c B z h m kappa X Y) :
    SchurRemainderContract r c B z h m kappa A X Y :=
  ⟨ha, remainder_coefficient_attempt z h m kappa A X Y,
    remainder_paths_attempt z h m kappa A X Y⟩

theorem source_remainder_contract_attempt (hc : CenterOffsetTarget)
    (m kappa : ℝ) (hw : SourceWeightsTarget m kappa)
    (hk : 0 < kappa) (hm : 0 ≤ m) (hh : 0 ≤ offset ^ 2) (q : Fin 6 → ℝ)
    (A : Fin r → Fin c → ℝ) (X : Fin r → Fin 2 → ℝ) (Y : Fin 2 → Fin c → ℝ) :
    SchurRemainderContract r c (sourceTail q) (q 4) offset m kappa A X Y :=
  remainder_from_adapter_attempt (sourceTail q) (q 4) offset m kappa A X Y
    (source_tail_elimination_adapter_attempt hc r c m kappa hw hk hm hh q X Y)

/- Pure expression and conditional solve interface only. No binding of A/X/Y,
   complete Schur PSD, full-body matrix, coverage, compilation or admission. -/
end
end NEW_BODY6_SLICE_SCHURREMAINDER20260907
