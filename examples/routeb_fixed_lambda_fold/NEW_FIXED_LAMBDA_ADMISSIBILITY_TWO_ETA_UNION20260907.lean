import NEW_FIXED_LAMBDA_ADMISSIBILITY_SELECTED_BOX_PARENT20260907
import Mathlib.Data.Finset.Basic
import Mathlib.Tactic

set_option autoImplicit false

namespace RouteBFixedLambdaTwoEtaUnion

open RouteBFixedLambdaAdmissibility
open RouteBFixedLambdaSparseDigestFold
open RouteBFixedLambdaSelectedBoxParent

noncomputable section

/-!
This sidecar is the two-eta union seam.  Row indices are tagged before
unioning, so local index reuse between the eta slices is harmless.  A
separate cross-eta label-disjointness premise is required before the union
can inherit one-row-per-box for the *box labels* themselves.

Digest/canonical-row bindings remain fields of the input partitions.  They are
not computed, inspected, or used as Lean facts in this file.
-/

inductive EtaTag
  | eta27
  | eta56
deriving DecidableEq

def unionRows (f : Declared577SparseFold) :
    Finset (EtaTag × Nat) :=
  (f.eta27.rows.image (fun i => (EtaTag.eta27, i))) ∪
    (f.eta56.rows.image (fun i => (EtaTag.eta56, i)))

def unionRow
    (f : Declared577SparseFold) : EtaTag × Nat → CellMarginData ℚ
  | (EtaTag.eta27, i) => f.eta27.row i
  | (EtaTag.eta56, i) => f.eta56.row i

def unionBoxLabel
    (f : Declared577SparseFold) : EtaTag × Nat → Nat
  | (EtaTag.eta27, i) => f.eta27.boxLabel i
  | (EtaTag.eta56, i) => f.eta56.boxLabel i

def unionBoxLabels (f : Declared577SparseFold) : Finset Nat :=
  (unionRows f).image (unionBoxLabel f)

def CrossEtaLabelsDisjoint (f : Declared577SparseFold) : Prop :=
  ∀ i ∈ f.eta27.rows, ∀ j ∈ f.eta56.rows,
    f.eta27.boxLabel i ≠ f.eta56.boxLabel j

theorem union_rows_card
    (f : Declared577SparseFold) :
    (unionRows f).card =
      f.eta27.rows.card + f.eta56.rows.card := by
  have h27 :
      (f.eta27.rows.image (fun i => (EtaTag.eta27, i))).card =
        f.eta27.rows.card := by
    symm
    apply Finset.card_image_iff.mpr
    intro i hi j hj hEq
    exact (Prod.mk.inj_iff.mp hEq).2
  have h56 :
      (f.eta56.rows.image (fun i => (EtaTag.eta56, i))).card =
        f.eta56.rows.card := by
    symm
    apply Finset.card_image_iff.mpr
    intro i hi j hj hEq
    exact (Prod.mk.inj_iff.mp hEq).2
  have hdisjoint : Disjoint
      (f.eta27.rows.image (fun i => (EtaTag.eta27, i)))
      (f.eta56.rows.image (fun i => (EtaTag.eta56, i))) := by
    refine Finset.disjoint_left.mpr ?_
    intro x hx27 hx56
    rcases Finset.mem_image.mp hx27 with ⟨i, hi, rfl⟩
    rcases Finset.mem_image.mp hx56 with ⟨j, hj, hEq⟩
    cases hEq
  unfold unionRows
  rw [Finset.card_union_of_disjoint hdisjoint, h27, h56]

theorem union_oneRowPerBox
    (f : Declared577SparseFold)
    (hdisjoint : CrossEtaLabelsDisjoint f) :
    ∀ {x y : EtaTag × Nat}, x ∈ unionRows f → y ∈ unionRows f →
      unionBoxLabel f x = unionBoxLabel f y → x = y := by
  intro x y hx hy hlabel
  rcases x with ⟨tagX, i⟩
  rcases y with ⟨tagY, j⟩
  cases tagX <;> cases tagY
  · rcases Finset.mem_union.mp hx with hx | hx
    · rcases Finset.mem_image.mp hx with ⟨i', hi', hxi⟩
      cases hxi
      rcases Finset.mem_union.mp hy with hy | hy
      · rcases Finset.mem_image.mp hy with ⟨j', hj', hyj⟩
        cases hyj
        have hsame := f.eta27.oneRowPerBox hi' hj' hlabel
        cases hsame
      · rcases Finset.mem_image.mp hy with ⟨j', hj', hyj⟩
        cases hyj
        exact (hdisjoint i' hi' j' hj' hlabel).elim
    · rcases Finset.mem_image.mp hx with ⟨i', hi', hxi⟩
      cases hxi
      rcases Finset.mem_union.mp hy with hy | hy
      · rcases Finset.mem_image.mp hy with ⟨j', hj', hyj⟩
        cases hyj
        exact (hdisjoint j' hj' i' hi' hlabel.symm).elim
      · rcases Finset.mem_image.mp hy with ⟨j', hj', hyj⟩
        cases hyj
        have hsame := f.eta56.oneRowPerBox hi' hj' hlabel
        cases hsame
  · rcases Finset.mem_union.mp hx with hx | hx
    · rcases Finset.mem_image.mp hx with ⟨i', hi', hxi⟩
      cases hxi
      rcases Finset.mem_union.mp hy with hy | hy
      · rcases Finset.mem_image.mp hy with ⟨j', hj', hyj⟩
        cases hyj
        exact (hdisjoint i' hi' j' hj' hlabel).elim
      · rcases Finset.mem_image.mp hy with ⟨j', hj', hyj⟩
        cases hyj
        exact (hdisjoint j' hj' i' hi' hlabel.symm).elim
    · rcases Finset.mem_image.mp hx with ⟨i', hi', hxi⟩
      cases hxi
      rcases Finset.mem_union.mp hy with hy | hy
      · rcases Finset.mem_image.mp hy with ⟨j', hj', hyj⟩
        cases hyj
        have hsame := f.eta27.oneRowPerBox hi' hj' hlabel
        cases hsame
      · rcases Finset.mem_image.mp hy with ⟨j', hj', hyj⟩
        cases hyj
        exact (hdisjoint j' hj' i' hi' hlabel.symm).elim

theorem union_boxLabels_card
    (f : Declared577SparseFold)
    (hdisjoint : CrossEtaLabelsDisjoint f) :
    (unionBoxLabels f).card = 577 := by
  have hinj := union_oneRowPerBox f hdisjoint
  have himage : (unionRows f).card = (unionBoxLabels f).card := by
    unfold unionBoxLabels
    apply (Finset.card_image_iff.mpr ?_).symm
    intro x hx y hy hlabel
    exact hinj hx hy hlabel
  rw [← himage, union_rows_card]
  omega

/-!
The margin conclusion is stated existentially over the tagged union.  This
retains the exact sparse membership witness and does not require a canonical
box-to-row function beyond the one-row-per-box premise used above.
-/
theorem union_selected_box_has_positive_margin
    (f : Declared577SparseFold)
    (hupper : uniformStrictUpper f)
    {b : Nat} (hb : b ∈ unionBoxLabels f) :
    ∃ x ∈ unionRows f,
      0 < (unionRow f x).candidateMargin ∧ unionBoxLabel f x = b := by
  rcases Finset.mem_image.mp hb with ⟨x, hx, hlabel⟩
  rcases x with ⟨tag, i⟩
  cases tag
  · rcases Finset.mem_union.mp hx with hx | hx
    · rcases Finset.mem_image.mp hx with ⟨i', hi', hxi⟩
      cases hxi
      have hbox : f.eta27.boxLabel i' = b := hlabel
      have hm := selected_box_margins_positive_of_uniform_upper
        f.params f.eta27 hupper.1 b
      rcases hm hbox with ⟨k, hk, hpos, hkbox⟩
      exact ⟨(EtaTag.eta27, k),
        Finset.mem_union.mpr (Or.inl (Finset.mem_image.mpr ⟨k, hk, rfl⟩)),
        hpos, hkbox⟩
    · rcases Finset.mem_image.mp hx with ⟨i', hi', hxi⟩
      cases hxi
      have hbox : f.eta56.boxLabel i' = b := hlabel
      have hm := selected_box_margins_positive_of_uniform_upper
        f.params f.eta56 hupper.2 b
      rcases hm hbox with ⟨k, hk, hpos, hkbox⟩
      exact ⟨(EtaTag.eta56, k),
        Finset.mem_union.mpr (Or.inr (Finset.mem_image.mpr ⟨k, hk, rfl⟩)),
        hpos, hkbox⟩
  · rcases Finset.mem_union.mp hx with hx | hx
    · rcases Finset.mem_image.mp hx with ⟨i', hi', hxi⟩
      cases hxi
      exact False.elim (by simp at hlabel)
    · rcases Finset.mem_image.mp hx with ⟨i', hi', hxi⟩
      cases hxi
      have hbox : f.eta56.boxLabel i' = b := hlabel
      have hm := selected_box_margins_positive_of_uniform_upper
        f.params f.eta56 hupper.2 b
      rcases hm hbox with ⟨k, hk, hpos, hkbox⟩
      exact ⟨(EtaTag.eta56, k),
        Finset.mem_union.mpr (Or.inr (Finset.mem_image.mpr ⟨k, hk, rfl⟩)),
        hpos, hkbox⟩

/-!
The exact accounting theorem consumes only the declared row-count premises;
the box-label cardinality additionally consumes cross-eta disjointness.
-/
theorem union_boxLabels_card_from_declared_accounting
    (f : Declared577SparseFold)
    (hdisjoint : CrossEtaLabelsDisjoint f) :
    (unionBoxLabels f).card =
      f.eta27.rows.card + f.eta56.rows.card := by
  have hinj := union_oneRowPerBox f hdisjoint
  unfold unionBoxLabels
  apply (Finset.card_image_iff.mpr ?_).symm
  intro x hx y hy hlabel
  exact hinj hx hy hlabel

/- Admission boundary: union cardinality and margin positivity are finite
   declared-row consequences only.  Digest, source, and coverage remain
   external premises. -/

#print axioms union_rows_card
#print axioms union_oneRowPerBox
#print axioms union_boxLabels_card
#print axioms union_selected_box_has_positive_margin
#print axioms union_boxLabels_card_from_declared_accounting

end
end RouteBFixedLambdaTwoEtaUnion
