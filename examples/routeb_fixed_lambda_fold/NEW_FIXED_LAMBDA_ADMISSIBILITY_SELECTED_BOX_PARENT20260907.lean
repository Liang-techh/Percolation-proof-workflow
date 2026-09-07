import NEW_FIXED_LAMBDA_ADMISSIBILITY_SPARSE_DIGEST_FOLD20260907
import Mathlib.Tactic

set_option autoImplicit false

namespace RouteBFixedLambdaSelectedBoxParent

open RouteBFixedLambdaAdmissibility
open RouteBFixedLambdaCoefficientBridge
open RouteBFixedLambdaSparseDigestFold

noncomputable section

/-!
This parent-level sidecar closes one finite logical seam left open by the
sparse digest fold: one selected box label has one selected row, and the
row's fixed-lambda margin can therefore be exposed as a box-level quantity.

The digest fields remain untouched external premises.  They are not used as
proofs of positivity, and no hash/source/coverage fact is introduced here.
-/

structure SelectedBoxRow
    (part : SparseDeclaredPartition) (b : Nat) where
  index : Nat
  index_mem : index ∈ part.rows
  label_eq : part.boxLabel index = b

theorem selectedBoxRow_unique
    (part : SparseDeclaredPartition) {b : Nat}
    (w₁ w₂ : SelectedBoxRow part b) :
    w₁.index = w₂.index := by
  apply part.oneRowPerBox w₁.index_mem w₂.index_mem
  exact w₁.label_eq.trans w₂.label_eq.symm

noncomputable def selectedBoxRowOfMem
    (part : SparseDeclaredPartition) {b : Nat}
    (hb : b ∈ boxLabels part) : SelectedBoxRow part b := by
  rcases (mem_boxLabels_iff part b).mp hb with ⟨i, hi, hbox⟩
  exact ⟨i, hi, hbox⟩

theorem selectedBoxRowOfMem_mem
    (part : SparseDeclaredPartition) {b : Nat}
    (hb : b ∈ boxLabels part) :
    (selectedBoxRowOfMem part hb).index ∈ part.rows := by
  exact (selectedBoxRowOfMem part hb).index_mem

theorem selectedBoxRowOfMem_label
    (part : SparseDeclaredPartition) {b : Nat}
    (hb : b ∈ boxLabels part) :
    part.boxLabel (selectedBoxRowOfMem part hb).index = b := by
  exact (selectedBoxRowOfMem part hb).label_eq

/- The one-row-per-box premise makes the margin independent of which
   existential witness is selected.  This is the precise box-level seam. -/
theorem candidate_margin_independent_of_selected_row
    (part : SparseDeclaredPartition) {b : Nat}
    (w₁ w₂ : SelectedBoxRow part b) :
    (part.row w₁.index).candidateMargin =
      (part.row w₂.index).candidateMargin := by
  rw [selectedBoxRow_unique part w₁ w₂]

noncomputable def selectedBoxMargin
    (part : SparseDeclaredPartition) {b : Nat}
    (hb : b ∈ boxLabels part) : ℚ :=
  (part.row (selectedBoxRowOfMem part hb).index).candidateMargin

theorem selectedBoxMargin_positive
    (p : FixedLambdaParameters ℚ)
    (part : SparseDeclaredPartition)
    (hupper : strictUpperRows p part)
    {b : Nat} (hb : b ∈ boxLabels part) :
    0 < selectedBoxMargin part hb := by
  unfold selectedBoxMargin
  apply (strict_upper_iff_positive_margin p
    (part.row (selectedBoxRowOfMem part hb).index)).mp
  exact hupper _ (selectedBoxRowOfMem_mem part hb)

theorem selected_box_margins_positive_of_uniform_upper
    (p : FixedLambdaParameters ℚ)
    (part : SparseDeclaredPartition)
    (hupper : strictUpperRows p part) :
    ∀ b, ∀ hb : b ∈ boxLabels part, 0 < selectedBoxMargin part hb := by
  intro b hb
  exact selectedBoxMargin_positive p part hupper hb

/-!
The current declared artifact has two separate sparse eta partitions.  The
following proposition is parent-level only: it says all labels selected by
either supplied partition have positive margins, retaining the original
membership proof as an explicit dependent premise.
-/
def UniformSelectedBoxMarginsPositive
    (f : Declared577SparseFold) : Prop :=
  (∀ b, ∀ hb : b ∈ boxLabels f.eta27,
    0 < selectedBoxMargin f.eta27 hb) ∧
  (∀ b, ∀ hb : b ∈ boxLabels f.eta56,
    0 < selectedBoxMargin f.eta56 hb)

theorem uniform_selected_box_margins_positive
    (f : Declared577SparseFold)
    (hupper : uniformStrictUpper f) :
    UniformSelectedBoxMarginsPositive f := by
  constructor
  · intro b hb
    exact selectedBoxMargin_positive f.params f.eta27 hupper.1 hb
  · intro b hb
    exact selectedBoxMargin_positive f.params f.eta56 hupper.2 hb

theorem uniform_admissibility_implies_uniform_selected_box_margins_positive
    (f : Declared577SparseFold)
    (hadmissible : uniformAdmissible f) :
    UniformSelectedBoxMarginsPositive f := by
  apply uniform_selected_box_margins_positive f
  exact (uniform_admissible_iff_strict_upper f).mp hadmissible

/-!
The digest/canonical-row contract is carried through the parent object but
does not enter this implication.  This projection makes that separation
explicit for a future adapter.
-/
theorem parent_margin_result_does_not_change_digest_binding
    (part : SparseDeclaredPartition) :
    part.digest = part.digestOracle (selectedRowEncoding part) := by
  exact digest_tracks_selected_rows part

/- Admission boundary: all positivity results above consume typed row
   premises.  They do not establish those premises from a receipt or source. -/

#print axioms selectedBoxRow_unique
#print axioms selectedBoxMargin_positive
#print axioms uniform_selected_box_margins_positive
#print axioms uniform_admissibility_implies_uniform_selected_box_margins_positive
#print axioms parent_margin_result_does_not_change_digest_binding

end
end RouteBFixedLambdaSelectedBoxParent
