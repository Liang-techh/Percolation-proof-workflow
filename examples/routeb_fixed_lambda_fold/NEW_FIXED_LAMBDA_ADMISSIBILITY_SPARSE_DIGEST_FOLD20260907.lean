import NEW_FixedLambdaUniformDeclaredFold20260907
import NEW_FIXED_LAMBDA_ADMISSIBILITY20260907
import NEW_FIXED_LAMBDA_ADMISSIBILITY_COEFFICIENT_BRIDGE20260907
import Mathlib.Data.Finset.Basic
import Mathlib.Tactic

set_option autoImplicit false

namespace RouteBFixedLambdaSparseDigestFold

open RouteBFixedLambdaAdmissibility
open RouteBFixedLambdaCoefficientBridge

noncomputable section

/-!
This sidecar is the sparse-label and digest layer for a declared finite fold.
It reuses the fixed-lambda parameter, cell data, and coefficient bridge from
the earlier sidecars.  The digest is represented by a typed external token
and an explicit binding premise; no hash implementation or receipt parser is
silently treated as a Lean theorem.
-/

structure ExactWitnessDigest where
  hex : String
  hex_length : hex.length = 64

structure SparseDeclaredPartition where
  eta : ℚ
  rows : Finset Nat
  row : Nat → CellMarginData ℚ
  boxLabel : Nat → Nat
  oneRowPerBox :
    ∀ {i j : Nat}, i ∈ rows → j ∈ rows →
      boxLabel i = boxLabel j → i = j
  rowEncoding : Nat → String
  digest : ExactWitnessDigest
  digestOracle : List String → ExactWitnessDigest
  digest_binding :
    digest = digestOracle (rows.toList.map rowEncoding)

def boxLabels (p : SparseDeclaredPartition) : Finset Nat :=
  p.rows.image p.boxLabel

theorem mem_boxLabels_iff
    (p : SparseDeclaredPartition) (b : Nat) :
    b ∈ boxLabels p ↔ ∃ i ∈ p.rows, p.boxLabel i = b := by
  simp [boxLabels]

theorem card_rows_eq_card_sparse_boxLabels
    (p : SparseDeclaredPartition) :
    p.rows.card = (boxLabels p).card := by
  unfold boxLabels
  apply (Finset.card_image_iff.mpr ?_).symm
  intro i hi j hj hbox
  exact p.oneRowPerBox hi hj hbox

def selectedRowEncoding (p : SparseDeclaredPartition) : List String :=
  p.rows.toList.map p.rowEncoding

theorem digest_tracks_selected_rows
    (p : SparseDeclaredPartition) :
    p.digest = p.digestOracle (selectedRowEncoding p) := by
  exact p.digest_binding

theorem row_encoding_mem_of_selected
    (p : SparseDeclaredPartition) {i : Nat} (hi : i ∈ p.rows) :
    p.rowEncoding i ∈ selectedRowEncoding p := by
  simp [selectedRowEncoding, hi]

/-!
These predicates retain the actual selected index set.  No conversion to
`Fin p.rows.card`, `Finset.range`, or a dense box-label interval is made.
-/

def strictUpperRows
    (p : FixedLambdaParameters ℚ)
    (part : SparseDeclaredPartition) : Prop :=
  ∀ i ∈ part.rows, p.lambda < (part.row i).lambdaUpper

def positiveMarginRows
    (part : SparseDeclaredPartition) : Prop :=
  ∀ i ∈ part.rows, 0 < (part.row i).candidateMargin

theorem strictUpperRows_iff_positiveMarginRows
    (p : FixedLambdaParameters ℚ)
    (part : SparseDeclaredPartition) :
    strictUpperRows p part ↔ positiveMarginRows part := by
  simpa [strictUpperRows, positiveMarginRows] using
    (finset_strict_upper_iff_positive_margin p part.rows part.row)

def admissibleRows
    (p : FixedLambdaParameters ℚ)
    (part : SparseDeclaredPartition) : Prop :=
  ∀ i ∈ part.rows, rowAdmissible p (part.row i)

theorem admissibleRows_iff_strictUpperRows
    (p : FixedLambdaParameters ℚ)
    (part : SparseDeclaredPartition) :
    admissibleRows p part ↔ strictUpperRows p part := by
  constructor
  · intro hadm i hi
    exact ((rowAdmissible_iff_two_upper_and_positive p (part.row i)).mp
      (hadm i hi)).1
  · intro hupper i hi
    apply (rowAdmissible_iff_two_upper_and_positive p (part.row i)).mpr
    refine ⟨?_, ?_⟩
    · exact hupper i hi
    · exact (strict_upper_iff_positive_margin p (part.row i)).mp
        (hupper i hi)

/-!
The two declared eta slices are kept as separate sparse partitions.  Their
cardinality premises record the current 256 + 321 declared-row accounting,
without making a source or coverage claim.
-/

structure Declared577SparseFold where
  params : FixedLambdaParameters ℚ
  eta27 : SparseDeclaredPartition
  eta56 : SparseDeclaredPartition
  eta27_value : eta27.eta = 27 / 10
  eta56_value : eta56.eta = 28 / 5
  eta27_rows : eta27.rows.card = 256
  eta56_rows : eta56.rows.card = 321

def uniformAdmissible (f : Declared577SparseFold) : Prop :=
  admissibleRows f.params f.eta27 ∧ admissibleRows f.params f.eta56

def uniformStrictUpper (f : Declared577SparseFold) : Prop :=
  strictUpperRows f.params f.eta27 ∧ strictUpperRows f.params f.eta56

def uniformPositiveMargin (f : Declared577SparseFold) : Prop :=
  positiveMarginRows f.eta27 ∧ positiveMarginRows f.eta56

theorem uniform_admissible_iff_strict_upper
    (f : Declared577SparseFold) :
    uniformAdmissible f ↔ uniformStrictUpper f := by
  constructor
  · intro h
    exact ⟨(admissibleRows_iff_strictUpperRows f.params f.eta27).mp h.1,
      (admissibleRows_iff_strictUpperRows f.params f.eta56).mp h.2⟩
  · intro h
    exact ⟨(admissibleRows_iff_strictUpperRows f.params f.eta27).mpr h.1,
      (admissibleRows_iff_strictUpperRows f.params f.eta56).mpr h.2⟩

theorem uniform_strict_upper_iff_positive_margin
    (f : Declared577SparseFold) :
    uniformStrictUpper f ↔ uniformPositiveMargin f := by
  constructor
  · intro h
    exact ⟨(strictUpperRows_iff_positiveMarginRows f.params f.eta27).mp h.1,
      (strictUpperRows_iff_positiveMarginRows f.params f.eta56).mp h.2⟩
  · intro h
    exact ⟨(strictUpperRows_iff_positiveMarginRows f.params f.eta27).mpr h.1,
      (strictUpperRows_iff_positiveMarginRows f.params f.eta56).mpr h.2⟩

theorem declared_row_count_is_577
    (f : Declared577SparseFold) :
    f.eta27.rows.card + f.eta56.rows.card = 577 := by
  omega

/- A selected box label carries a selected row and, under the upper premise,
   the positive fixed-lambda margin.  This is the explicit membership-to-
   margin connection; it is not an all-box or physical-domain statement. -/
theorem selected_box_has_positive_margin
    (p : FixedLambdaParameters ℚ)
    (part : SparseDeclaredPartition)
    (hupper : strictUpperRows p part)
    {b : Nat} (hb : b ∈ boxLabels part) :
    ∃ i ∈ part.rows,
      0 < (part.row i).candidateMargin ∧ part.boxLabel i = b := by
  rcases (mem_boxLabels_iff part b).mp hb with ⟨i, hi, hbox⟩
  exact ⟨i, hi,
    (strict_upper_iff_positive_margin p (part.row i)).mp (hupper i hi), hbox⟩

/-!
Admission boundary: `ExactWitnessDigest.digest_binding` and the row-count
fields are premises of this declared-artifact interface.  They do not compute
SHA-256, bind a CSV, prove true-DH coverage, or promote a registry candidate.
-/

#print axioms card_rows_eq_card_sparse_boxLabels
#print axioms digest_tracks_selected_rows
#print axioms strictUpperRows_iff_positiveMarginRows
#print axioms admissibleRows_iff_strictUpperRows
#print axioms uniform_admissible_iff_strict_upper
#print axioms uniform_strict_upper_iff_positive_margin
#print axioms declared_row_count_is_577
#print axioms selected_box_has_positive_margin

end
end RouteBFixedLambdaSparseDigestFold
