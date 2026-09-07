import Mathlib.Data.Finset.Basic
import Mathlib.Data.Real.Basic
import Mathlib.Tactic

set_option autoImplicit false

namespace RouteBP4FixedLambdaUniformDeclaredFold

noncomputable section

/-!
This sidecar is the source-independent interface for the P4 fixed-lambda
decomposition child.  A row is a finite-indexed declared witness, not a CSV
row and not a source evaluator.  In particular, `lambdaUpper` and
`candidateMargin` are supplied fields; no DH, interval, or decimal parser is
hidden in this file.

The finite conjunction is represented computationally by `Finset.all`.  The
row indices are arbitrary selected `Nat`s.  They are not required to be
`Fin n`, consecutive, or equal to the box labels.
-/

structure FixedLambdaWitness where
  boxLabel : Nat
  lambdaUpper : ℝ
  candidateMargin : ℝ

def rowStrict (w : FixedLambdaWitness) : Prop :=
  2 < w.lambdaUpper ∧ 0 < w.candidateMargin

def rowStrictBool (w : FixedLambdaWitness) : Bool :=
  decide (rowStrict w)

def rowStrictFold
    (row : Nat → FixedLambdaWitness) (rows : Finset Nat) : Bool :=
  rows.all (fun i => rowStrictBool (row i))

theorem rowStrictBool_eq_true_iff (w : FixedLambdaWitness) :
    rowStrictBool w = true ↔ rowStrict w := by
  simp [rowStrictBool]

theorem rowStrictFold_eq_true_iff
    (row : Nat → FixedLambdaWitness) (rows : Finset Nat) :
    rowStrictFold row rows = true ↔
      ∀ i ∈ rows, rowStrict (row i) := by
  simp [rowStrictFold, rowStrictBool]

/- The fixed value is lambda=2.  The first conjunct records the usual
   lower-side admissibility, while `rowStrict` carries the strict upper
   bound and positive margin that are the declared witness obligations. -/
def fixedLambdaAdmissible (w : FixedLambdaWitness) : Prop :=
  (1 : ℝ) < 2 ∧ rowStrict w

theorem fixedLambdaAdmissible_iff (w : FixedLambdaWitness) :
    fixedLambdaAdmissible w ↔ rowStrict w := by
  simp [fixedLambdaAdmissible]

/-!
A partition keeps its selected finite row indices and an accessor to the
corresponding witness.  `oneRowPerBox` is injectivity of the box label on the
selected rows.  It does not assert that the labels form an interval.
-/
structure DeclaredPartition where
  eta : ℝ
  rows : Finset Nat
  row : Nat → FixedLambdaWitness
  oneRowPerBox :
    ∀ {i j : Nat}, i ∈ rows → j ∈ rows →
      (row i).boxLabel = (row j).boxLabel → i = j

def partitionStrictFold (p : DeclaredPartition) : Bool :=
  rowStrictFold p.row p.rows

def uniformStrictFold (partitions : Finset DeclaredPartition) : Bool :=
  partitions.all (fun p => partitionStrictFold p)

theorem uniformStrictFold_eq_true_iff
    (partitions : Finset DeclaredPartition) :
    uniformStrictFold partitions = true ↔
      ∀ p ∈ partitions, ∀ i ∈ p.rows, rowStrict (p.row i) := by
  simp [uniformStrictFold, partitionStrictFold, rowStrictFold, rowStrictBool]

theorem uniform_strict_fold_of_each_row
    (partitions : Finset DeclaredPartition)
    (hrows : ∀ p ∈ partitions, ∀ i ∈ p.rows, rowStrict (p.row i)) :
    uniformStrictFold partitions = true := by
  exact (uniformStrictFold_eq_true_iff partitions).2 hrows

/-!
Box labels are obtained by an image of the selected row indices.  This is the
abstract sparse-label interface: membership means that some selected row has
that label.  No dense ordinal, maximum-label coverage, or `Fin n` encoding is
introduced.
-/
def boxLabels (p : DeclaredPartition) : Finset Nat :=
  p.rows.image (fun i => (p.row i).boxLabel)

theorem mem_boxLabels_iff
    (p : DeclaredPartition) (b : Nat) :
    b ∈ boxLabels p ↔
      ∃ i ∈ p.rows, (p.row i).boxLabel = b := by
  simp [boxLabels]

theorem sparse_box_label_witness
    (p : DeclaredPartition)
    (hrows : ∀ i ∈ p.rows, rowStrict (p.row i))
    {b : Nat} (hb : b ∈ boxLabels p) :
    ∃ i ∈ p.rows, rowStrict (p.row i) ∧ (p.row i).boxLabel = b := by
  rcases (mem_boxLabels_iff p b).1 hb with ⟨i, hi, hbox⟩
  exact ⟨i, hi, hrows i hi, hbox⟩

/- The row count is the sparse-label count when the selected box labels are
   unique.  This is the accounting theorem needed by the fold; it never
   replaces a sparse label set by `range (rows.card)`. -/
theorem card_rows_eq_card_sparse_boxLabels
    (p : DeclaredPartition) :
    p.rows.card = (boxLabels p).card := by
  unfold boxLabels
  apply (Finset.card_image_iff.mpr ?_).symm
  intro i hi j hj hbox
  exact p.oneRowPerBox hi hj hbox

theorem sparse_labels_need_no_dense_ordinal
    (p : DeclaredPartition) :
    (∀ i ∈ p.rows, rowStrict (p.row i)) →
      ∀ b ∈ boxLabels p,
        ∃ i ∈ p.rows, rowStrict (p.row i) ∧ (p.row i).boxLabel = b := by
  intro hrows b hb
  exact sparse_box_label_witness p hrows hb

/-!
This record packages the finite witness contract while keeping its proof
surface separate from any source/CSV binding.  A value of this type is still
only a declared finite witness; it is not a PDE coverage certificate.
-/
structure UniformDeclaredWitness where
  partitions : Finset DeclaredPartition
  rowContract :
    ∀ p ∈ partitions, ∀ i ∈ p.rows, rowStrict (p.row i)

theorem UniformDeclaredWitness.fold_passes
    (w : UniformDeclaredWitness) :
    uniformStrictFold w.partitions = true := by
  exact uniform_strict_fold_of_each_row w.partitions w.rowContract

/- A source/CSV adapter, if later added, must provide these fields as an
   external theorem or compiled bridge.  This sidecar deliberately has no
   parser, hash, CSV path, or source evaluator declaration. -/

#print axioms rowStrictBool_eq_true_iff
#print axioms rowStrictFold_eq_true_iff
#print axioms fixedLambdaAdmissible_iff
#print axioms uniformStrictFold_eq_true_iff
#print axioms uniform_strict_fold_of_each_row
#print axioms mem_boxLabels_iff
#print axioms sparse_box_label_witness
#print axioms card_rows_eq_card_sparse_boxLabels
#print axioms sparse_labels_need_no_dense_ordinal
#print axioms UniformDeclaredWitness.fold_passes

end
end RouteBP4FixedLambdaUniformDeclaredFold
