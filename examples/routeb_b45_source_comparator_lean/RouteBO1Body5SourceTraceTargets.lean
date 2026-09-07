import RouteBO1PerBodyTraceAdapter

set_option autoImplicit false

namespace RouteBO1Body5SourceTraceTargets

noncomputable section

open RouteBO1PerBodyExactSource
open RouteBO1PerBodyTraceAdapter
open RouteBO1PerBodyTraceGenerated
open RouteBBodySemanticCore
open RouteBSourceContractAdapter

/-!
Human body 5 = zero-based 4. OPEN / UNPROVEN / UNCOMPILED.
These are proposition targets and explicit conditional plumbing only.
No target witness, source proof, fold proof or admission is supplied.
The frozen body_5_piecewise and generated rows are imported without edits.
-/

abbrev body5Index : Fin 6 := 4
abbrev V3 := Fin 3 → ℝ

def body5Phi (q : Q6) : ℝ := q 1 + q 2

/- Coordinates in (er, et, e3). This isolates q0 from all Gram algebra. -/
def body5Lift (q : Q6) (u : V3) : V3 :=
  ![u 0 * Real.cos (q 0) - u 1 * Real.sin (q 0),
    u 0 * Real.sin (q 0) + u 1 * Real.cos (q 0), u 2]

def body5Dot (u v : V3) : ℝ := ∑ a : Fin 3, u a * v a

def body5A (q : Q6) : ℝ :=
  2 / 25 + (21 / 100) * Real.sin (q 1) + (19 / 100) * Real.sin (body5Phi q)

def body5P (q : Q6) : ℝ :=
  (21 / 100) * Real.cos (q 1) + (19 / 100) * Real.cos (body5Phi q)

def body5Q (q : Q6) : ℝ :=
  (21 / 100) * Real.sin (q 1) + (19 / 100) * Real.sin (body5Phi q)

/- Slot 6 is deliberately outside the geometry target below. -/
def body5OriginLocal (q : Q6) (k : Fin 7) : V3 :=
  match k.val with
  | 0 => ![0, 0, 0]
  | 1 => ![2 / 25, 0, 1 / 10]
  | 2 => ![2 / 25 + (21 / 100) * Real.sin (q 1), 0,
             1 / 10 + (21 / 100) * Real.cos (q 1)]
  | 3 => ![2 / 25 + (21 / 100) * Real.sin (q 1), 1 / 20,
             1 / 10 + (21 / 100) * Real.cos (q 1)]
  | 4 => ![body5A q, 1 / 20, 1 / 10 + body5P q]
  | 5 => ![body5A q, 1 / 20, 1 / 10 + body5P q]
  | _ => 0

def body5VLocal (q : Q6) (j : Fin 6) : V3 :=
  match j.val with
  | 0 => ![-1 / 20, body5A q, 0]
  | 1 => ![body5P q, 0, -body5Q q]
  | 2 => ![(19 / 100) * Real.cos (body5Phi q), 0,
             -(19 / 100) * Real.sin (body5Phi q)]
  | _ => 0

def body5WLocal (q : Q6) (j : Fin 6) : V3 :=
  match j.val with
  | 0 => ![0, 0, 1]
  | 1 => ![0, 1, 0]
  | 2 => ![0, 1, 0]
  | 3 => ![Real.sin (body5Phi q), 0, Real.cos (body5Phi q)]
  | 4 => ![-Real.sin (q 3) * Real.cos (body5Phi q), Real.cos (q 3),
             Real.sin (q 3) * Real.sin (body5Phi q)]
  | _ => 0

/- G1: only origins 0..5 and parent axes 0..4; NOT the source axis 5.
   Obtain these from source_*_function_eq_frame_contract and DH slots.
   In particular o5=o4 uses a4=d4=0; v3=0 also uses c4-o3=(19/100)z3. -/
def Body5GeometryTarget : Prop :=
  ∀ q : Q6,
    (∀ k : Fin 7, k.val ≤ 5 →
      (sourceContract q).origins k = body5Lift q (body5OriginLocal q k)) ∧
    (∀ j : Fin 6, j.val ≤ 4 →
      (sourceContract q).axes j = body5Lift q (body5WLocal q j))

def Body5ColumnsTarget : Prop :=
  ∀ (q : Q6) (j : Fin 6),
    (fun a => bodyJv (sourceContract q).origins (sourceContract q).axes
      body5Index a j) = body5Lift q (body5VLocal q j) ∧
    (fun a => bodyJw (sourceContract q).axes body5Index a j) =
      body5Lift q (body5WLocal q j)

/- G2: midpoint, active cross products, and joint 5 inactive. -/
def Body5GeometryToColumnsTarget : Prop :=
  Body5GeometryTarget → Body5ColumnsTarget

def Body5LiftIsometryTarget : Prop :=
  ∀ (q : Q6) (u v : V3),
    body5Dot (body5Lift q u) (body5Lift q v) = body5Dot u v

def body5Gram (q : Q6) (i j : Fin 6) : ℝ :=
  (3 / 10) * body5Dot (body5VLocal q i) (body5VLocal q j) +
    (1 / 30) * body5Dot (body5WLocal q i) (body5WLocal q j)

def Body5SourceToGramTarget : Prop :=
  ∀ (q : Q6) (i j : Fin 6),
    sourceBodyMass q body5Index i j = body5Gram q i j

/- G3: diagonal inertia reduces the double sum, then use the isometry.
   This implication remains open, just like its two antecedents. -/
def Body5ColumnsToGramTarget : Prop :=
  Body5ColumnsTarget → Body5LiftIsometryTarget → Body5SourceToGramTarget

/- G4: finite entry cases and scalar trig identities, including (2,3)=0. -/
def Body5GramToPiecewiseTarget : Prop :=
  ∀ (q : Q6) (i j : Fin 6), body5Gram q i j = body_5_piecewise q i j

/- q3 is zero-based q(3); its CSV coordinate is nu4. -/
def body5Frequency (u v w : ℤ) : Fin 6 → ℤ := ![0, u, v, w, 0, 0]

def Body5PhaseTarget : Prop :=
  ∀ (u v w : ℤ) (q : Q6), tracePhase (body5Frequency u v w) q =
    (u : ℝ) * q 1 + (v : ℝ) * q 2 + (w : ℝ) * q 3

def body5ConstantRows : List BodyTraceRow := by
  classical
  exact bodyTraceRows5.filter (fun r => decide (r.frequency = body5Frequency 0 0 0))

/- Choose the first nonzero coordinate in (q1,q2,q3) positive. -/
def body5Positive (r : BodyTraceRow) : Prop :=
  0 < r.frequency 1 ∨
    (r.frequency 1 = 0 ∧ 0 < r.frequency 2) ∨
    (r.frequency 1 = 0 ∧ r.frequency 2 = 0 ∧ 0 < r.frequency 3)

def body5RepresentativeRows : List BodyTraceRow := by
  classical
  exact bodyTraceRows5.filter (fun r => decide (body5Positive r))

/- This is a proposed partner, not a new admitted source row.
   The permutation obligation below must identify every partner with a
   literal generated row, including its numerator/denominator labels. -/
def body5Conjugate (r : BodyTraceRow) : BodyTraceRow where
  body := r.body
  row := r.row
  col := r.col
  frequency := fun k => -r.frequency k
  realCoeff := r.realCoeff
  imagCoeff := { numerator := -r.imagCoeff.numerator,
                 denominator := r.imagCoeff.denominator }

/- F1: an equality of row MULTISETS, not merely existence of partners.
   Constants occur once; all nonzero rows occur in disjoint pair positions.
   No row/column transpose or frequency sign is silently identified. -/
def Body5ExactPartitionTarget : Prop :=
  bodyTraceRows5.length = 57 ∧
  body5ConstantRows.length = 7 ∧ body5RepresentativeRows.length = 25 ∧
  (bodyTraceRows5.map (fun r => (r.row, r.col, r.frequency))).Nodup ∧
  (∀ r, r ∈ bodyTraceRows5 → r.body = body5Index ∧
    r.frequency 0 = 0 ∧ r.frequency 4 = 0 ∧ r.frequency 5 = 0 ∧
    r.realCoeff.denominator ≠ 0 ∧ r.imagCoeff.denominator ≠ 0) ∧
  (∀ r, r ∈ body5ConstantRows → r.imagCoeff.numerator = 0) ∧
  List.Perm bodyTraceRows5
    (body5ConstantRows ++ body5RepresentativeRows.flatMap
      (fun r => [r, body5Conjugate r]))

def Body5ConjugateAtomTarget : Prop :=
  ∀ (r : BodyTraceRow) (q : Q6),
    traceAtom r q + traceAtom (body5Conjugate r) q =
      2 * (rationalReal r.realCoeff * Real.cos (tracePhase r.frequency q) -
        rationalImag r.imagCoeff * Real.sin (tracePhase r.frequency q))

def body5RealRow (i j : Fin 6) (u v w n d : ℤ) : BodyTraceRow where
  body := body5Index
  row := i
  col := j
  frequency := body5Frequency u v w
  realCoeff := { numerator := n, denominator := d }
  imagCoeff := { numerator := 0, denominator := 1 }

def body5Q3Representatives : List BodyTraceRow := by
  classical
  exact body5RepresentativeRows.filter (fun r => decide (r.frequency 3 ≠ 0))

/- Eight representatives = sixteen actual q3 rows.
   ±(1,1,-1) has +1/120; ±(1,1,1) has -1/120.
   The signs in each triple are correlated, not independent choices. -/
def Body5Q3ExactPairsTarget : Prop :=
  List.Perm body5Q3Representatives
    [body5RealRow 0 4 1 1 (-1) 1 120,
     body5RealRow 0 4 1 1 1 (-1) 120,
     body5RealRow 4 0 1 1 (-1) 1 120,
     body5RealRow 4 0 1 1 1 (-1) 120,
     body5RealRow 1 4 0 0 1 1 60,
     body5RealRow 4 1 0 0 1 1 60,
     body5RealRow 2 4 0 0 1 1 60,
     body5RealRow 4 2 0 0 1 1 60]

def Body5Q3ProductToSumTarget : Prop :=
  ∀ q : Q6,
    (1 / 30 : ℝ) * Real.sin (body5Phi q) * Real.sin (q 3) =
      (1 / 60 : ℝ) * (Real.cos (body5Phi q - q 3) -
        Real.cos (body5Phi q + q 3))

/- Actual API order is body, row, col, q, row-record. -/
def body5Fold (rows : List BodyTraceRow) (q : Q6)
    (i j : Fin 6) (seed : ℝ) : ℝ :=
  rows.foldl (fun acc r => acc + traceRowContribution body5Index i j q r) seed

def body5PairedValue (q : Q6) (i j : Fin 6) : ℝ :=
  (body5ConstantRows.map (fun r => traceRowContribution body5Index i j q r)).sum +
    (body5RepresentativeRows.map (fun r =>
      traceRowContribution body5Index i j q r +
      traceRowContribution body5Index i j q (body5Conjugate r))).sum

/- F2: arbitrary accumulator is essential for removing prefix/suffix folds.
   Only unfold block/body guards outside body 5, not their trigonometry. -/
def Body5FullToBlockFoldTarget : Prop :=
  ∀ (q : Q6) (i j : Fin 6) (seed : ℝ),
    body5Fold bodyTraceRows q i j seed = body5Fold bodyTraceRows5 q i j seed

/- F3: prove foldl = seed + sum(map contribution), then use F1's Perm.
   A partner-existence statement alone cannot establish this equality. -/
def Body5RegroupTarget : Prop :=
  ∀ (q : Q6) (i j : Fin 6) (seed : ℝ),
    body5Fold bodyTraceRows5 q i j seed = seed + body5PairedValue q i j

/- F4: exact constants, pairs, row/col guards and phase reduction.
   A future proof may split the q3 eight pairs from the other seventeen. -/
def Body5PairedToPiecewiseTarget : Prop :=
  ∀ (q : Q6) (i j : Fin 6), body5PairedValue q i j = body_5_piecewise q i j

/- Conditional equality plumbing only. These candidates do not discharge
   any G/F leaf and have NOT been checked by Lean in this task. -/
theorem body5_source_handoff_candidate
    (hSG : Body5SourceToGramTarget) (hGP : Body5GramToPiecewiseTarget) :
    h_body_5_expected_entry_target := by
  intro q i j
  exact (hSG q i j).trans (hGP q i j)

theorem body5_trace_handoff_candidate
    (hFull : Body5FullToBlockFoldTarget) (hRegroup : Body5RegroupTarget)
    (hPairs : Body5PairedToPiecewiseTarget) : h_body_5_trace_fold_target := by
  intro q i j
  have hBlock : body5Fold bodyTraceRows5 q i j 0 = body_5_piecewise q i j := by
    calc
      body5Fold bodyTraceRows5 q i j 0 = 0 + body5PairedValue q i j :=
        hRegroup q i j 0
      _ = body5PairedValue q i j := zero_add _
      _ = body_5_piecewise q i j := hPairs q i j
  change body_5_piecewise q i j = body5Fold bodyTraceRows q i j 0
  exact hBlock.symm.trans (hFull q i j 0).symm

end
end RouteBO1Body5SourceTraceTargets
