import Mathlib.Algebra.BigOperators.Group.List.Basic
import Mathlib.Algebra.BigOperators.Fin

set_option autoImplicit false

namespace NEW_BODY5_API_REPAIR_ListFinset20260907

/-!
OPEN / UNCOMPILED API repair candidates. No Lean/Lake execution or admission.
This module imports neither body-5 skeleton nor any project adapter.
Keep row multiplicity in List; Finset is used only for coordinate indices.
-/

variable {α β M : Type*}

theorem map_decode_encode (encode : α → β) (decode : β → α)
    (hinv : ∀ x, decode (encode x) = x) (xs : List α) :
    (xs.map encode).map decode = xs := by
  induction xs with
  | nil => rfl
  | cons x xs ih =>
      simp only [List.map_cons, hinv, ih]

theorem perm_of_encoded (encode : α → β) (decode : β → α)
    (hinv : ∀ x, decode (encode x) = x) (xs ys : List α)
    (h : List.Perm (xs.map encode) (ys.map encode)) : List.Perm xs ys := by
  have hd : List.Perm ((xs.map encode).map decode) ((ys.map encode).map decode) :=
    List.Perm.map decode h
  rw [map_decode_encode encode decode hinv xs,
    map_decode_encode encode decode hinv ys] at hd
  exact hd

/-- Constructor induction avoids depending on the name Perm.sum_eq. -/
theorem map_sum_perm [AddCommMonoid M] (f : α → M) {xs ys : List α}
    (h : List.Perm xs ys) : (xs.map f).sum = (ys.map f).sum := by
  induction h with
  | nil => rfl
  | cons x h ih => simp only [List.map_cons, List.sum_cons, ih]
  | swap x y xs =>
      simp only [List.map_cons, List.sum_cons, add_left_comm]
  | trans hxy hyz ihxy ihyz => exact ihxy.trans ihyz

theorem fold_add_sum [AddMonoid M] (xs : List α) (f : α → M) (seed : M) :
    xs.foldl (fun acc x => acc + f x) seed = seed + (xs.map f).sum := by
  induction xs generalizing seed with
  | nil => simp only [List.foldl_nil, List.map_nil, List.sum_nil, add_zero]
  | cons x xs ih =>
      simp only [List.foldl_cons, List.map_cons, List.sum_cons, ih, add_assoc]

theorem fold_add_perm [AddCommMonoid M] (f : α → M) {xs ys : List α}
    (h : List.Perm xs ys) (seed : M) :
    xs.foldl (fun acc x => acc + f x) seed =
      ys.foldl (fun acc x => acc + f x) seed := by
  rw [fold_add_sum, fold_add_sum, map_sum_perm f h]

/-- List.flatMap retains both positions even when partner x = x. -/
theorem pair_map_sum [AddMonoid M] (partner : α → α) (f : α → M) (xs : List α) :
    ((xs.flatMap (fun x => [x, partner x])).map f).sum =
      (xs.map (fun x => f x + f (partner x))).sum := by
  induction xs with
  | nil => rfl
  | cons x xs ih =>
      rw [List.flatMap_cons, List.map_append, List.sum_append, ih]
      simp only [List.map_cons, List.map_nil, List.sum_cons, List.sum_nil,
        add_zero]

theorem fold_pairs [AddMonoid M] (partner : α → α) (f : α → M)
    (xs : List α) (seed : M) :
    (xs.flatMap (fun x => [x, partner x])).foldl (fun acc x => acc + f x) seed =
      seed + (xs.map (fun x => f x + f (partner x))).sum := by
  rw [fold_add_sum, pair_map_sum]

theorem sum_congr_on [AddCommMonoid M] (s : Finset α) (f g : α → M)
    (h : ∀ a, a ∈ s → f a = g a) :
    (∑ a ∈ s, f a) = ∑ a ∈ s, g a := by
  exact Finset.sum_congr rfl h

theorem fin3_sum [AddCommMonoid M] (f : Fin 3 → M) :
    (∑ a : Fin 3, f a) = f 0 + f 1 + f 2 := by
  exact Fin.sum_univ_three f

/-- A six-term phase expansion with a fixed, left-associated normal form. -/
theorem fin6_sum [AddCommMonoid M] (f : Fin 6 → M) :
    (∑ a : Fin 6, f a) = f 0 + f 1 + f 2 + f 3 + f 4 + f 5 := by
  exact Fin.sum_univ_six f

end NEW_BODY5_API_REPAIR_ListFinset20260907
