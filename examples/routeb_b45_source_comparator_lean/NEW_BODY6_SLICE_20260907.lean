import NEW_BODY6_SLICE_20260907Data

set_option autoImplicit false

namespace NEW_BODY6_SLICE_20260907

noncomputable section

open RouteBO1PerBodyExactSource RouteBBodySemanticCore
open RouteBSourceContractAdapter RouteBO1PerBodyTraceGenerated
open RouteBO1Body6CanonicalExportTargets NEW_BODY6_SLICE_20260907Data

/-!
UNCOMPILED CANDIDATES. No declaration here has been parsed, elaborated,
kernel checked or admitted in this task. Missing leaves are explicit Prop
targets, not axioms, opaque witnesses or fabricated proof receipts.

Human body 6 = Fin 6 value 5. q is arbitrary in R^6. Regularizer is excluded.
The CSV/manifest and Python literal roundtrip do not supply Lean witnesses.
-/

def sliceEvaluator (q : Q6) (i j : Fin 6) : ℝ :=
  body6CanonicalEvaluator canonicalRows q i j

def rowKey (r : BodyTraceRow) := (r.body, r.row, r.col, r.frequency)

def LabelSupportContract : Prop :=
  (taggedRows.map rowKey).Nodup ∧
  ∀ r ∈ taggedRows,
    r.body = (5 : Fin 6) ∧
    0 < r.realCoeff.denominator ∧ 0 < r.imagCoeff.denominator ∧
    Int.gcd r.realCoeff.numerator r.realCoeff.denominator = 1 ∧
    Int.gcd r.imagCoeff.numerator r.imagCoeff.denominator = 1 ∧
    (r.realCoeff.numerator ≠ 0 ∨ r.imagCoeff.numerator ≠ 0) ∧
    r.frequency (0 : Fin 6) = 0 ∧ r.frequency (5 : Fin 6) = 0

/- Counts describe the pinned candidate only. Exact keys/coefficients are the
   explicit taggedRows, with all frequencies listed in the JSON manifest.
   Counts, symmetry and missing rows cannot prove source zero support. -/
def entryCounts : Fin 6 → Fin 6 → ℕ :=
  ![![99, 44, 34, 34, 28, 12],
    ![44, 25, 25, 16, 18, 4],
    ![34, 25, 11, 8, 6, 4],
    ![34, 16, 8, 3, 0, 2],
    ![28, 18, 6, 0, 1, 0],
    ![12, 4, 4, 2, 0, 1]]

def EntryCountTarget : Prop :=
  ∀ i j, (canonicalRows.filter (fun r => decide (r.row = i ∧ r.col = j))).length =
    entryCounts i j

def EmptyEntry (i j : Fin 6) : Prop :=
  (i = 3 ∧ j = 4) ∨ (i = 4 ∧ j = 3) ∨
  (i = 4 ∧ j = 5) ∨ (i = 5 ∧ j = 4)

def EmptyFourierTarget : Prop :=
  ∀ q i j, EmptyEntry i j → sliceEvaluator q i j = 0

def SourceBindingTarget : Prop :=
  ∀ q i j, sourceBodyMass q (5 : Fin 6) i j = sliceEvaluator q i j

/- Every entry, including the four empty entries; no support-restricted premise. -/
def AllEntriesGramFourierTarget : Prop :=
  ∀ q i j, body6Gram q i j = sliceEvaluator q i j

def LegacyTraceBindingTarget : Prop :=
  ∀ q i j, sliceEvaluator q i j = bodyTraceEvaluator (5 : Fin 6) q i j

/- This is exactly the function equality required by unchanged h_body_6,
   without importing or editing the shared adapter. -/
def LegacyConsumerTarget : Prop :=
  ∀ q i j, sourceBodyMass q (5 : Fin 6) i j =
    bodyTraceEvaluator (5 : Fin 6) q i j

theorem endpoint_to_center_attempt (h : Body6EndpointTarget) :
    Body6CenterTarget := by
  intro q
  funext a
  change (((sourceContract q).origins (5 : Fin 7) a +
      (sourceContract q).origins (6 : Fin 7) a) / 2) = _
  rw [h q a]
  dsimp [body6Center]
  ring

theorem source_linear_column_attempt (hc : Body6CenterTarget)
    (q : Q6) (i : Fin 6) (a : Fin 3) :
    bodyJv (sourceContract q).origins (sourceContract q).axes (5 : Fin 6) a i =
      body6Velocity q i a := by
  have hi : i.val ≤ (5 : Fin 6).val := by have := i.isLt; omega
  rw [bodyJv_active_formula _ _ _ _ _ hi, hc q]
  rfl

theorem source_angular_column_attempt (q : Q6) (i : Fin 6) (a : Fin 3) :
    bodyJw (sourceContract q).axes (5 : Fin 6) a i =
      (sourceContract q).axes i a := by
  have hi : i.val ≤ (5 : Fin 6).val := by have := i.isLt; omega
  exact bodyJw_active_formula _ _ _ _ hi

theorem diagonal_inertia_attempt (u v : Fin 3 → ℝ) :
    (∑ a : Fin 3, ∑ b : Fin 3,
      u a * routeBInertia (5 : Fin 6) a b * v b) =
      (1 / 60 : ℝ) * (∑ a : Fin 3, u a * v a) := by
  norm_num [routeBInertia, routeBInertiaScalar, Fin.sum_univ_succ] <;> ring

theorem center_to_source_gram_attempt (hc : Body6CenterTarget) :
    Body6SourceGramTarget := by
  intro q i j
  rw [sourceBodyMass_eq_bodyMass]
  change (3 / 20 : ℝ) * (∑ a : Fin 3,
      bodyJv (sourceContract q).origins (sourceContract q).axes (5 : Fin 6) a i *
      bodyJv (sourceContract q).origins (sourceContract q).axes (5 : Fin 6) a j) +
    (∑ a : Fin 3, ∑ b : Fin 3,
      bodyJw (sourceContract q).axes (5 : Fin 6) a i *
      routeBInertia (5 : Fin 6) a b *
      bodyJw (sourceContract q).axes (5 : Fin 6) b j) = _
  rw [diagonal_inertia_attempt]
  simp only [source_linear_column_attempt hc, source_angular_column_attempt]
  rfl

/- A small structural identity for the defined Gram, independent of Fourier data.
   It says nothing about the actual source until center/source-gram is supplied. -/
theorem sixth_velocity_attempt : Body6SixthVelocityTarget := by
  intro q a
  fin_cases a <;>
    norm_num [body6Velocity, body6Center, prevOrigin, cross3] <;> ring

theorem sixth_column_of_source_gram_attempt (hg : Body6SourceGramTarget) :
    Body6SixthColumnTarget := by
  intro q i
  rw [hg q i (5 : Fin 6)]
  simp [body6Gram, sixth_velocity_attempt]

/- q 1+q 2 uses zero-based Lean indices (human angles q2+q3).
   This 23-row column cannot distinguish aggregate from body 6: bodies 1..5
   have inactive joint 6. Use the full (1,1) coefficient negative control. -/
def sixthAxisDot (q : Q6) : Fin 6 → ℝ :=
  ![Real.cos (q 1 + q 2) * Real.cos (q 4) -
      Real.sin (q 1 + q 2) * Real.cos (q 3) * Real.sin (q 4),
    Real.sin (q 3) * Real.sin (q 4),
    Real.sin (q 3) * Real.sin (q 4),
    Real.cos (q 4), 0, 1]

def sixthColumnFormula (q : Q6) (i : Fin 6) : ℝ :=
  (1 / 60 : ℝ) * sixthAxisDot q i

def SourceAxisDotTarget : Prop :=
  ∀ q i, (∑ a : Fin 3,
    (sourceContract q).axes i a * (sourceContract q).axes (5 : Fin 6) a) =
      sixthAxisDot q i

def SixthColumnFourierTarget : Prop :=
  ∀ q i, sliceEvaluator q i (5 : Fin 6) = sixthColumnFormula q i

def SixthColumnFilterTarget : Prop :=
  ∀ q i, body6CanonicalEvaluator sixthColumnRows q i (5 : Fin 6) =
    sliceEvaluator q i (5 : Fin 6)

theorem source_sixth_column_attempt (hg : Body6SourceGramTarget)
    (ha : SourceAxisDotTarget) (q : Q6) (i : Fin 6) :
    sourceBodyMass q (5 : Fin 6) i (5 : Fin 6) = sixthColumnFormula q i := by
  rw [sixth_column_of_source_gram_attempt hg q i, ha q i]
  rfl

theorem sixth_slice_seam_attempt (hg : Body6SourceGramTarget)
    (ha : SourceAxisDotTarget) (hf : SixthColumnFourierTarget) :
    ∀ q i, sourceBodyMass q (5 : Fin 6) i (5 : Fin 6) =
      sliceEvaluator q i (5 : Fin 6) := by
  intro q i
  exact (source_sixth_column_attempt hg ha q i).trans (hf q i).symm

theorem source_binding_seam_attempt (hg : Body6SourceGramTarget)
    (hf : AllEntriesGramFourierTarget) : SourceBindingTarget := by
  intro q i j
  exact (hg q i j).trans (hf q i j)

theorem source_zero_complement_attempt (hs : SourceBindingTarget)
    (hz : EmptyFourierTarget) (q : Q6) (i j : Fin 6) (he : EmptyEntry i j) :
    sourceBodyMass q (5 : Fin 6) i j = 0 := by
  exact (hs q i j).trans (hz q i j he)

theorem legacy_consumer_seam_attempt (hs : SourceBindingTarget)
    (ht : LegacyTraceBindingTarget) : LegacyConsumerTarget := by
  intro q i j
  exact (hs q i j).trans (ht q i j)

/- No unconditional SourceBindingTarget/LegacyConsumerTarget inhabitant.
   No registry, comparator or aggregate-coverage witness is constructed. -/

end
end NEW_BODY6_SLICE_20260907
