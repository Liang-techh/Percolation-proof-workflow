import Mathlib.Algebra.BigOperators.Group.List.Basic
import Mathlib.Algebra.BigOperators.Group.Finset.Basic

set_option autoImplicit false

namespace NEW_BODY5_API_REPAIR_CodedFilterCore20260908

/-! OPEN_UNCOMPILED. Source-level candidates only: no Lean/Lake execution.
No skeleton, earlier repair, project adapter, or data decision is imported.
List positions retain multiplicity; Finset is used only for coordinate sums. -/

variable {α β γ M : Type*}

theorem perm_sum [AddCommMonoid M] (f : α → M) {xs ys : List α}
    (h : List.Perm xs ys) : (xs.map f).sum = (ys.map f).sum := by
  induction h with
  | nil => rfl
  | cons x h ih => simp only [List.map_cons, List.sum_cons, ih]
  | swap x y xs => simp only [List.map_cons, List.sum_cons, add_left_comm]
  | trans h₁ h₂ ih₁ ih₂ => exact ih₁.trans ih₂

theorem seeded_sum [AddMonoid M] (xs : List α) (f : α → M) (seed : M) :
    xs.foldl (fun acc x => acc + f x) seed = seed + (xs.map f).sum := by
  induction xs generalizing seed with
  | nil => simp only [List.foldl_nil, List.map_nil, List.sum_nil, add_zero]
  | cons x xs ih =>
      simp only [List.foldl_cons, List.map_cons, List.sum_cons, ih, add_assoc]

/-- Arbitrary blocks, including empty and repeated blocks; no disjointness premise. -/
theorem flatMap_sum [AddMonoid M] (xs : List α) (block : α → List β) (f : β → M) :
    ((xs.flatMap block).map f).sum =
      (xs.map (fun x => ((block x).map f).sum)).sum := by
  induction xs with
  | nil => rfl
  | cons x xs ih =>
      rw [List.flatMap_cons, List.map_append, List.sum_append, ih]
      rfl

/-- Pointwise replacement in G3's two coordinate sums; no column witness supplied. -/
theorem coordinate_sum_congr [AddCommMonoid M] (s : Finset α) (t : Finset β)
    (f g : α → β → M) (h : ∀ a ∈ s, ∀ b ∈ t, f a b = g a b) :
    (∑ a ∈ s, ∑ b ∈ t, f a b) = ∑ a ∈ s, ∑ b ∈ t, g a b := by
  apply Finset.sum_congr rfl
  intro a ha
  exact Finset.sum_congr rfl (h a ha)

theorem decode_map (enc : α → β) (dec : β → α)
    (hinv : ∀ x, dec (enc x) = x) (xs : List α) :
    (xs.map enc).map dec = xs := by
  induction xs with
  | nil => rfl
  | cons x xs ih => simp only [List.map_cons, hinv, ih]

/-- The decision is made on code, but the result is exactly the source-row filter. -/
theorem decode_filtered_map (enc : α → β) (dec : β → α)
    (hinv : ∀ x, dec (enc x) = x) (p : α → Bool) (pc : β → Bool)
    (hpred : ∀ x, pc (enc x) = p x) (xs : List α) :
    ((xs.map enc).filter pc).map dec = xs.filter p := by
  induction xs with
  | nil => rfl
  | cons x xs ih =>
      cases hx : p x <;>
        simp [List.map_cons, List.filter_cons, hpred, hx, hinv, ih]

/-- Only a left inverse is needed. No DecidableEq on source rows is introduced. -/
theorem rows_perm_of_filtered_codes (enc : α → β) (dec : β → α)
    (hinv : ∀ x, dec (enc x) = x) (p : α → Bool) (pc : β → Bool)
    (hpred : ∀ x, pc (enc x) = p x) (xs ys : List α)
    (h : List.Perm ((xs.map enc).filter pc) (ys.map enc)) :
    List.Perm (xs.filter p) ys := by
  have hd := List.Perm.map dec h
  rw [decode_filtered_map enc dec hinv p pc hpred xs,
    decode_map enc dec hinv ys] at hd
  exact hd

end NEW_BODY5_API_REPAIR_CodedFilterCore20260908
