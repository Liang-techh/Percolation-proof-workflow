import NEW_BODY6_SLICE_TAILINVERSE20260907

set_option autoImplicit false

namespace NEW_BODY6_SLICE_TAILSCHUR20260907

noncomputable section

open NEW_BODY6_SLICE_MASSTAIL_Core20260907 NEW_BODY6_SLICE_MASSTAIL_Source20260907
open NEW_BODY6_SLICE_VGRAM_Source20260907 NEW_BODY6_SLICE_TAILPSD20260907
open NEW_BODY6_SLICE_TAILINVERSE20260907

/- UNCOMPILED typed contraction. External row/column counts are independent;
   only the internal Fin 2 slots inherit the actual ordered tail {3,4}. -/
def schurCorrection (r c : ℕ) (z h m kappa : ℝ)
    (X : Fin r → Fin 2 → ℝ) (Y : Fin 2 → Fin c → ℝ) (i : Fin r) (j : Fin c) : ℝ :=
  ∑ a : Fin 2, ∑ b : Fin 2, X i a * inverseTail z h m kappa a b * Y b j

def explicitCorrection (r c : ℕ) (z h m kappa : ℝ)
    (X : Fin r → Fin 2 → ℝ) (Y : Fin 2 → Fin c → ℝ) (i : Fin r) (j : Fin c) : ℝ :=
  X i 0 * Y 0 j / (kappa + m * h ^ 2 * Real.sin z ^ 2) +
    X i 1 * Y 1 j / (kappa + m * h ^ 2)

/- Solve each external Y column in the same ordered two-dimensional space. -/
def solvedRight (c : ℕ) (z h m kappa : ℝ)
    (Y : Fin 2 → Fin c → ℝ) (a : Fin 2) (j : Fin c) : ℝ :=
  inverseApply z h m kappa (fun b => Y b j) a

theorem correction_expansion_attempt (r c : ℕ) (z h m kappa : ℝ)
    (X : Fin r → Fin 2 → ℝ) (Y : Fin 2 → Fin c → ℝ) (i : Fin r) (j : Fin c) :
    schurCorrection r c z h m kappa X Y i j =
      explicitCorrection r c z h m kappa X Y i j := by
  norm_num [schurCorrection, explicitCorrection, inverseTail, Fin.sum_univ_succ] <;> ring

theorem correction_via_solve_attempt (r c : ℕ) (z h m kappa : ℝ)
    (X : Fin r → Fin 2 → ℝ) (Y : Fin 2 → Fin c → ℝ) (i : Fin r) (j : Fin c) :
    schurCorrection r c z h m kappa X Y i j =
      ∑ a : Fin 2, X i a * solvedRight c z h m kappa Y a j := by
  rw [correction_expansion_attempt]
  norm_num [explicitCorrection, solvedRight, inverseApply, Fin.sum_univ_succ] <;> ring

/- A proof-only adapter: denominator positivity and inverse/solve obligations
   are distinct from the universally valid scalar reciprocal expansions. -/
structure TailEliminationAdapter (r c : ℕ) (B : Fin 2 → Fin 2 → ℝ)
    (z h m kappa : ℝ) (X : Fin r → Fin 2 → ℝ) (Y : Fin 2 → Fin c → ℝ) : Prop where
  denominatorsPositive :
    0 < kappa + m * h ^ 2 * Real.sin z ^ 2 ∧ 0 < kappa + m * h ^ 2
  leftInverse : ∀ a b, product2 B (inverseTail z h m kappa) a b = identity2 a b
  rightInverse : ∀ a b, product2 (inverseTail z h m kappa) B a b = identity2 a b
  solveColumns : ∀ j, action2 B (fun a => solvedRight c z h m kappa Y a j) = (fun a => Y a j)
  correctionFormula : ∀ i j, schurCorrection r c z h m kappa X Y i j =
    explicitCorrection r c z h m kappa X Y i j
  correctionViaSolve : ∀ i j, schurCorrection r c z h m kappa X Y i j =
    ∑ a : Fin 2, X i a * solvedRight c z h m kappa Y a j

theorem tail_elimination_adapter_attempt (r c : ℕ) (z h m kappa : ℝ)
    (hk : 0 < kappa) (hm : 0 ≤ m) (hh : 0 ≤ h ^ 2)
    (X : Fin r → Fin 2 → ℝ) (Y : Fin 2 → Fin c → ℝ) :
    TailEliminationAdapter r c (explicitTail z h m kappa) z h m kappa X Y := by
  have hi := inverse_two_sided_attempt z h m kappa hk hm hh
  refine ⟨denominators_positive_attempt z h m kappa hk hm hh, hi.1, hi.2, ?_,
    correction_expansion_attempt r c z h m kappa X Y,
    correction_via_solve_attempt r c z h m kappa X Y⟩
  intro j
  exact inverse_solves_attempt z h m kappa hk hm hh (fun a => Y a j)

/- The source constructor consumes the existing actual-source inverse/solve
   package. It does not assert that X or Y are source cross-block values. -/
theorem source_tail_elimination_adapter_attempt (hc : CenterOffsetTarget)
    (r c : ℕ) (m kappa : ℝ) (hw : SourceWeightsTarget m kappa)
    (hk : 0 < kappa) (hm : 0 ≤ m) (hh : 0 ≤ offset ^ 2) (q : Fin 6 → ℝ)
    (X : Fin r → Fin 2 → ℝ) (Y : Fin 2 → Fin c → ℝ) :
    TailEliminationAdapter r c (sourceTail q) (q 4) offset m kappa X Y := by
  have hi := source_tail_inverse_interface_attempt hc m kappa hw hk hm hh q
  refine ⟨denominators_positive_attempt (q 4) offset m kappa hk hm hh, hi.1, hi.2.1, ?_,
    correction_expansion_attempt r c (q 4) offset m kappa X Y,
    correction_via_solve_attempt r c (q 4) offset m kappa X Y⟩
  intro j
  exact hi.2.2.2 (fun a => Y a j)

/- X and Y need not be transposes, nonnegative, square, or source-derived.
   No complete Schur matrix, Schur PSD equivalence, eigenvalue, coverage,
   compilation or registry witness is claimed. -/
end
end NEW_BODY6_SLICE_TAILSCHUR20260907
