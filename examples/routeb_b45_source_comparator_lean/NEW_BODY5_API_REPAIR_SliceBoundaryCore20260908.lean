import NEW_BODY5_API_REPAIR_CodedFilterCore20260908

set_option autoImplicit false

namespace NEW_BODY5_API_REPAIR_SliceBoundaryCore20260908

/-! OPEN_UNCOMPILED. No Lean/Lake execution or proof receipt.
This extends the existing, also uncompiled, generic core without editing it.
No source data, project target, skeleton, or global equality instance is imported. -/

open NEW_BODY5_API_REPAIR_CodedFilterCore20260908

variable {α β M : Type*}

/-- A source slice is transported using complete codes and an explicit left inverse.
The code predicate must agree with the row predicate; neither binding is inferred. -/
theorem encoded_slice_fold [AddCommMonoid M]
    (enc : α → β) (dec : β → α) (hinv : ∀ x, dec (enc x) = x)
    (p : α → Bool) (pc : β → Bool) (hpred : ∀ x, pc (enc x) = p x)
    (xs ys : List α)
    (hcodes : List.Perm ((xs.map enc).filter pc) (ys.map enc))
    (f : α → M) (seed : M) :
    (xs.filter p).foldl (fun acc x => acc + f x) seed = seed + (ys.map f).sum := by
  have hp := rows_perm_of_filtered_codes enc dec hinv p pc hpred xs ys hcodes
  rw [seeded_sum, perm_sum f hp]

/-- The blocks remain Lists: repeated rows, including self-partners, are not erased. -/
theorem encoded_slice_blocks [AddCommMonoid M]
    (enc : α → β) (dec : β → α) (hinv : ∀ x, dec (enc x) = x)
    (p : α → Bool) (pc : β → Bool) (hpred : ∀ x, pc (enc x) = p x)
    (xs reps : List α) (block : α → List α)
    (hcodes : List.Perm ((xs.map enc).filter pc) ((reps.flatMap block).map enc))
    (f : α → M) (seed : M) :
    (xs.filter p).foldl (fun acc x => acc + f x) seed =
      seed + (reps.map (fun r => ((block r).map f).sum)).sum := by
  rw [encoded_slice_fold enc dec hinv p pc hpred xs (reps.flatMap block) hcodes,
    flatMap_sum]

/-- Guard-only elimination needs no commutativity and no evaluation of the atom. -/
theorem fold_zero_on [AddMonoid M] (xs : List α) (f : α → M)
    (hz : ∀ x ∈ xs, f x = 0) (seed : M) :
    xs.foldl (fun acc x => acc + f x) seed = seed := by
  revert hz
  induction xs generalizing seed with
  | nil => intro hz; rfl
  | cons x xs ih =>
      intro hz
      have hx : f x = 0 := hz x (by simp)
      have ht : ∀ y ∈ xs, f y = 0 := fun y hy => hz y (by simp [hy])
      simpa only [List.foldl_cons, hx, add_zero] using ih seed ht

/-- A column equality can be applied pointwise before any coordinate expansion.
Finset is used only for coordinates, never to represent the source rows. -/
theorem coordinate_bilinear_congr (s t : Finset α) (u u' v v' : α → M)
    [AddCommMonoid M] (term : M → M → M)
    (hu : ∀ a ∈ s, u a = u' a) (hv : ∀ b ∈ t, v b = v' b) :
    (∑ a ∈ s, ∑ b ∈ t, term (u a) (v b)) =
      ∑ a ∈ s, ∑ b ∈ t, term (u' a) (v' b) := by
  apply coordinate_sum_congr
  intro a ha b hb
  rw [hu a ha, hv b hb]

end NEW_BODY5_API_REPAIR_SliceBoundaryCore20260908
