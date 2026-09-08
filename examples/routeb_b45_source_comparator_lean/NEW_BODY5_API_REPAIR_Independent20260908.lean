import RouteBO1Body5SourceTraceTargets

set_option autoImplicit false

namespace NEW_BODY5_API_REPAIR_Independent20260908

/-!
OPEN_UNCOMPILED. No Lean/Lake execution, elaboration or kernel receipt.
Does not import either skeleton or any earlier API_REPAIR module.
The target import transitively imports Mathlib; this is not a minimal closure.
-/

open RouteBO1PerBodyTraceGenerated RouteBO1Body5SourceTraceTargets
open RouteBO1PerBodyExactSource

variable {α β M : Type*}

theorem perm_map_sum [AddCommMonoid M] (f : α → M)
    {xs ys : List α} (h : List.Perm xs ys) :
    (xs.map f).sum = (ys.map f).sum := by
  induction h with
  | nil => rfl
  | cons x h ih => simp only [List.map_cons, List.sum_cons, ih]
  | swap x y xs => simp only [List.map_cons, List.sum_cons, add_left_comm]
  | trans h₁ h₂ ih₁ ih₂ => exact ih₁.trans ih₂

theorem seeded_sum [AddMonoid M] (xs : List α) (f : α → M) (seed : M) :
    xs.foldl (fun a x => a + f x) seed = seed + (xs.map f).sum := by
  induction xs generalizing seed with
  | nil => simp
  | cons x xs ih => simp only [List.foldl_cons, List.map_cons,
      List.sum_cons, ih, add_assoc]

theorem flat_pairs_sum [AddMonoid M] (xs : List α) (p : α → α) (f : α → M) :
    ((xs.flatMap (fun x => [x, p x])).map f).sum =
      (xs.map (fun x => f x + f (p x))).sum := by
  induction xs with
  | nil => rfl
  | cons x xs ih =>
      rw [List.flatMap_cons, List.map_append, List.sum_append, ih]
      simp only [List.map_cons, List.map_nil, List.sum_cons, List.sum_nil, add_zero]

/-- Coordinate indices only: no conversion of source rows to a Finset. -/
theorem coordinate_sum_congr [AddCommMonoid M] (s : Finset α) (f g : α → M)
    (h : ∀ a ∈ s, f a = g a) :
    (∑ a ∈ s, f a) = ∑ a ∈ s, g a := by
  exact Finset.sum_congr rfl h

theorem coordinates3 [AddCommMonoid M] (f : Fin 3 → M) :
    (∑ k, f k) = f 0 + f 1 + f 2 := by
  simp [Fin.sum_univ_succ, add_assoc]

theorem coordinates6 [AddCommMonoid M] (f : Fin 6 → M) :
    (∑ k, f k) = f 0 + f 1 + f 2 + f 3 + f 4 + f 5 := by
  simp [Fin.sum_univ_succ, add_assoc]

/-- Explicit list induction avoids map-map/comp/id normalization. -/
theorem decode_map (enc : α → β) (dec : β → α)
    (hinv : ∀ x, dec (enc x) = x) (xs : List α) :
    (xs.map enc).map dec = xs := by
  induction xs with
  | nil => rfl
  | cons x xs ih => simp only [List.map_cons, hinv, ih]

abbrev RowCode := Fin 6 × Fin 6 × Fin 6 × (Fin 6 → ℤ) × ℤ × ℤ × ℤ × ℤ

def encode (r : BodyTraceRow) : RowCode :=
  (r.body, r.row, r.col, r.frequency, r.realCoeff.numerator,
    r.realCoeff.denominator, r.imagCoeff.numerator, r.imagCoeff.denominator)

def decode (c : RowCode) : BodyTraceRow :=
  let (b, i, j, nu, rn, rd, an, ad) := c
  ⟨b, i, j, nu, ⟨rn, rd⟩, ⟨an, ad⟩⟩

theorem decode_encode (r : BodyTraceRow) : decode (encode r) = r := by
  cases r with
  | mk b i j nu re im =>
      cases re
      cases im
      rfl

theorem row_perm (xs ys : List BodyTraceRow)
    (h : List.Perm (xs.map encode) (ys.map encode)) : List.Perm xs ys := by
  have hd := h.map decode
  rw [decode_map encode decode decode_encode xs,
    decode_map encode decode decode_encode ys] at hd
  exact hd

noncomputable section

def keepQ3 (r : BodyTraceRow) : Bool := decide (r.frequency 3 ≠ 0)

def sourceQ3 : List BodyTraceRow := bodyTraceRows5.filter keepQ3

/-- Separate membership and frequency claims; no classical representative filter. -/
theorem q3_membership (r : BodyTraceRow) :
    r ∈ sourceQ3 ↔ r ∈ bodyTraceRows5 ∧ r.frequency 3 ≠ 0 := by
  simp [sourceQ3, keepQ3]

/-- Bool cases avoid relying on the argument order of Perm.filter. -/
theorem filter_perm (p : α → Bool) {xs ys : List α} (h : List.Perm xs ys) :
    List.Perm (xs.filter p) (ys.filter p) := by
  induction h with
  | nil => exact List.Perm.refl _
  | cons x h ih =>
      cases hp : p x <;> simp only [List.filter_cons, hp] <;>
        first | exact ih | exact List.Perm.cons x ih
  | swap x y xs =>
      cases hx : p x <;> cases hy : p y <;>
        simp only [List.filter_cons, hx, hy] <;>
        first | exact List.Perm.refl _ | exact List.Perm.swap _ _ _
  | trans h₁ h₂ ih₁ ih₂ => exact ih₁.trans ih₂

theorem phase3 (u v w : ℤ) (q : Q6) :
    tracePhase (body5Frequency u v w) q =
      (u : ℝ) * q 1 + (v : ℝ) * q 2 + (w : ℝ) * q 3 := by
  unfold tracePhase
  rw [coordinates6]
  norm_num [body5Frequency]

theorem q3_product : Body5Q3ProductToSumTarget := by
  intro q
  rw [Real.cos_sub, Real.cos_add]
  ring

/-- Uncollapsed handoff: neither conjugate identity nor source Perm is invented. -/
theorem q3_fold_pairs (rs : List BodyTraceRow)
    (hCodes : List.Perm (sourceQ3.map encode)
      ((rs.flatMap (fun r => [r, body5Conjugate r])).map encode))
    (q : Q6) (i j : Fin 6) (seed : ℝ) :
    body5Fold sourceQ3 q i j seed = seed +
      (rs.map (fun r => traceRowContribution body5Index i j q r +
        traceRowContribution body5Index i j q (body5Conjugate r))).sum := by
  have hp := row_perm _ _ hCodes
  unfold body5Fold
  rw [seeded_sum, perm_map_sum (traceRowContribution body5Index i j q) hp,
    flat_pairs_sum]

end
end NEW_BODY5_API_REPAIR_Independent20260908
