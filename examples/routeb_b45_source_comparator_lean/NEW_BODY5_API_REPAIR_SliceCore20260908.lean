import Mathlib.Algebra.BigOperators.Group.List.Basic
import Mathlib.Algebra.BigOperators.Fin

set_option autoImplicit false

namespace NEW_BODY5_API_REPAIR_SliceCore20260908

/-! OPEN_UNCOMPILED: source-level candidates only; no Lean/Lake run.
List retains source multiplicity. Finset is used only for coordinates.
No project adapter, old repair file, or skeleton is imported. -/

variable {α β M : Type*}

theorem sum_under_perm [AddCommMonoid M] (f : α → M)
    {xs ys : List α} (h : List.Perm xs ys) :
    (xs.map f).sum = (ys.map f).sum := by
  induction h with
  | nil => rfl
  | cons x h ih => simp only [List.map_cons, List.sum_cons, ih]
  | swap x y xs => simp only [List.map_cons, List.sum_cons, add_left_comm]
  | trans h₁ h₂ ih₁ ih₂ => exact ih₁.trans ih₂

theorem seeded_fold [AddMonoid M] (xs : List α) (f : α → M) (seed : M) :
    xs.foldl (fun acc x => acc + f x) seed = seed + (xs.map f).sum := by
  induction xs generalizing seed with
  | nil => simp
  | cons x xs ih => simp only [List.foldl_cons, List.map_cons,
      List.sum_cons, ih, add_assoc]

theorem pair_sum [AddMonoid M] (xs : List α) (partner : α → α) (f : α → M) :
    ((xs.flatMap (fun x => [x, partner x])).map f).sum =
      (xs.map (fun x => f x + f (partner x))).sum := by
  induction xs with
  | nil => rfl
  | cons x xs ih =>
      rw [List.flatMap_cons, List.map_append, List.sum_append, ih]
      simp only [List.map_cons, List.map_nil, List.sum_cons, List.sum_nil, add_zero]

/-- Two nested coordinate sums; no Finset conversion of trace rows. -/
theorem double_sum_congr [AddCommMonoid M] (s : Finset α) (t : Finset β)
    (f g : α → β → M) (h : ∀ a ∈ s, ∀ b ∈ t, f a b = g a b) :
    (∑ a ∈ s, ∑ b ∈ t, f a b) = ∑ a ∈ s, ∑ b ∈ t, g a b := by
  apply Finset.sum_congr rfl
  intro a ha
  exact Finset.sum_congr rfl (h a ha)

theorem decode_mapped (enc : α → β) (dec : β → α)
    (hinv : ∀ x, dec (enc x) = x) (xs : List α) :
    (xs.map enc).map dec = xs := by
  induction xs with
  | nil => rfl
  | cons x xs ih => simp only [List.map_cons, hinv, ih]

theorem decode_perm (enc : α → β) (dec : β → α)
    (hinv : ∀ x, dec (enc x) = x) {xs ys : List α}
    (h : List.Perm (xs.map enc) (ys.map enc)) : List.Perm xs ys := by
  have hd := h.map dec
  rw [decode_mapped enc dec hinv xs, decode_mapped enc dec hinv ys] at hd
  exact hd

/-- Bool reduction is intentional: simp ONLY on filter_cons can leave ite goals. -/
theorem filter_under_perm (p : α → Bool) {xs ys : List α}
    (h : List.Perm xs ys) : List.Perm (xs.filter p) (ys.filter p) := by
  induction h with
  | nil => exact List.Perm.refl _
  | cons x h ih =>
      cases hp : p x
      · simpa [List.filter_cons, hp] using ih
      · simpa [List.filter_cons, hp] using List.Perm.cons x ih
  | swap x y xs =>
      cases hx : p x <;> cases hy : p y
      all_goals simp [List.filter_cons, hx, hy]
      all_goals exact List.Perm.swap _ _ _
  | trans h₁ h₂ ih₁ ih₂ => exact ih₁.trans ih₂

theorem filter_pairs (p : α → Bool) (partner : α → α)
    (hp : ∀ x, p (partner x) = p x) (xs : List α) :
    (xs.flatMap (fun x => [x, partner x])).filter p =
      (xs.filter p).flatMap (fun x => [x, partner x]) := by
  induction xs with
  | nil => rfl
  | cons x xs ih =>
      cases hx : p x <;>
        simp [List.flatMap_cons, List.filter_append, List.filter_cons, hp, hx, ih]

/-- Derive a slice binding from a full binding, not a second closed decision. -/
theorem slice_from_full (p : α → Bool) (partner : α → α)
    (hp : ∀ x, p (partner x) = p x) (source constants reps : List α)
    (hc : constants.filter p = [])
    (hfull : List.Perm source (constants ++ reps.flatMap (fun x => [x, partner x]))) :
    List.Perm (source.filter p) ((reps.filter p).flatMap (fun x => [x, partner x])) := by
  have h := filter_under_perm p hfull
  simpa only [List.filter_append, hc, List.nil_append, filter_pairs p partner hp] using h

end NEW_BODY5_API_REPAIR_SliceCore20260908
