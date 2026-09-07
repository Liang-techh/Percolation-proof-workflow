import RouteBO1PerBodyTraceAdapter

set_option autoImplicit false

namespace RouteBO1Body4TraceFoldTargets

noncomputable section

open RouteBO1PerBodyTraceAdapter
open RouteBO1PerBodyTraceGenerated

/-!
Narrow O1 body-4 trace-fold targets.  Human body 4 is zero-based body 3.
This file declares source-bound propositions only: it contains no row
instances, no proof, and no replacement for the existing source geometry.
-/

abbrev Body4Index : Fin 6 := 3

def body4Frequency (ν₂ ν₃ : ℤ) : Fin 6 → ℤ :=
  fun l => if l = (1 : Fin 6) then ν₂ else
    if l = (2 : Fin 6) then ν₃ else 0

def body4Phase (ν₂ ν₃ : ℤ) (q : Fin 6 → ℝ) : ℝ :=
  (ν₂ : ℝ) * q (1 : Fin 6) + (ν₃ : ℝ) * q (2 : Fin 6)

/- The guards are kept separate so a later proof can eliminate them in the
   order body, matrix row/column, and frequency support. -/
def Body4Guard (r : BodyTraceRow) : Prop :=
  r.body = Body4Index

def Body4EntryGuard (r : BodyTraceRow) (i j : Fin 6) : Prop :=
  Body4Guard r ∧ r.row = i ∧ r.col = j

def Body4KeyGuard (r : BodyTraceRow) (i j : Fin 6) (ν₂ ν₃ : ℤ) : Prop :=
  Body4EntryGuard r i j ∧ r.frequency = body4Frequency ν₂ ν₃

def Body4PrefixRows : List BodyTraceRow :=
  (bodyTraceRows1 ++ bodyTraceRows2) ++ bodyTraceRows3

def Body4SuffixRows : List BodyTraceRow :=
  bodyTraceRows5 ++ bodyTraceRows6

def Body4PartitionGuardTarget : Prop :=
  (∀ r, r ∈ Body4PrefixRows → r.body ≠ Body4Index) ∧
  (∀ r, r ∈ bodyTraceRows4 → r.body = Body4Index) ∧
  (∀ r, r ∈ Body4SuffixRows → r.body ≠ Body4Index)

def Body4RowColFrequencyGuardTarget : Prop :=
  ∀ r, r ∈ bodyTraceRows4 →
    ∃ i j : Fin 6, ∃ ν₂ ν₃ : ℤ,
      Body4KeyGuard r i j ν₂ ν₃ ∧
      r.realCoeff.denominator ≠ 0 ∧ r.imagCoeff.denominator ≠ 0

def Body4PhaseReductionTarget : Prop :=
  ∀ r, r ∈ bodyTraceRows4 →
    ∀ ν₂ ν₃ : ℤ, r.frequency = body4Frequency ν₂ ν₃ →
      ∀ q : Fin 6 → ℝ,
        tracePhase r.frequency q = body4Phase ν₂ ν₃ q

def Body4EntryGuardReductionTarget : Prop :=
  ∀ (q : Fin 6 → ℝ) (i j : Fin 6) r,
    r ∈ bodyTraceRows4 →
      traceRowContribution Body4Index q i j r =
        (if r.row = i ∧ r.col = j then traceAtom r q else 0)

def Body4OffBlockGuardReductionTarget : Prop :=
  ∀ (q : Fin 6 → ℝ) (i j : Fin 6) r,
    r ∈ Body4PrefixRows ∨ r ∈ Body4SuffixRows →
      traceRowContribution Body4Index q i j r = 0

/- A tagged conjugate pair preserves body/row/col, negates frequency, keeps
   the real coefficient, and negates the imaginary coefficient.  The
   denominator conditions make the RationalTag lift source-safe; they do not
   certify the source labels themselves. -/
def ConjugateTaggedPairTarget (r s : BodyTraceRow) : Prop :=
  r.body = s.body ∧ r.row = s.row ∧ r.col = s.col ∧
  (∀ l : Fin 6, s.frequency l = -r.frequency l) ∧
  r.realCoeff.denominator ≠ 0 ∧ s.realCoeff.denominator ≠ 0 ∧
  r.imagCoeff.denominator ≠ 0 ∧ s.imagCoeff.denominator ≠ 0 ∧
  s.realCoeff.toRat = r.realCoeff.toRat ∧
  s.imagCoeff.toRat = -r.imagCoeff.toRat

def ConjugateAtomPairTarget (r s : BodyTraceRow) : Prop :=
  ConjugateTaggedPairTarget r s ∧
  ∀ q : Fin 6 → ℝ, traceAtom s q = traceAtom r q

/- Per-pair target: the finite source rows and their exact conjugate partner
   must be supplied by the later source-bound proof; no partner is invented
   here. -/
def Body4ConjugatePairWitnessTarget (r s : BodyTraceRow) : Prop :=
  r ∈ bodyTraceRows4 ∧ s ∈ bodyTraceRows4 ∧
  ConjugateAtomPairTarget r s

def Body4ConjugatePairCoverageTarget : Prop :=
  ∀ r, r ∈ bodyTraceRows4 →
    ∃ s, s ∈ bodyTraceRows4 ∧ ConjugateAtomPairTarget r s

def body4BlockFold (q : Fin 6 → ℝ) (i j : Fin 6) : ℝ :=
  bodyTraceRows4.foldl
    (fun acc r => acc + traceRowContribution Body4Index q i j r) 0

def Body4FullToBlockFoldTarget : Prop :=
  ∀ (q : Fin 6 → ℝ) (i j : Fin 6),
    bodyTraceEvaluator Body4Index q i j = body4BlockFold q i j

def Body4BlockFoldTarget : Prop :=
  ∀ (q : Fin 6 → ℝ) (i j : Fin 6),
    body_4_piecewise q i j = body4BlockFold q i j

def Body4FoldCompositionTarget : Prop :=
  Body4FullToBlockFoldTarget ∧ Body4BlockFoldTarget

/- This is the exact handoff to the already existing body-4 target.  It is a
   proposition, not a theorem: neither component is supplied in this file. -/
def Body4TraceFoldHandoffTarget : Prop :=
  ∀ (q : Fin 6 → ℝ) (i j : Fin 6),
    body_4_piecewise q i j = bodyTraceEvaluator Body4Index q i j

end
end RouteBO1Body4TraceFoldTargets
