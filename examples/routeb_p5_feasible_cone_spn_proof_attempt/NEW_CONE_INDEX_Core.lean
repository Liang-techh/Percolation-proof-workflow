import Mathlib.Data.Real.Basic
import Mathlib.Data.Fintype.BigOperators
import Mathlib.Tactic

/-!
Concrete finite indexing for the six reviewed P5 channel charts.
Standalone namespace: does not import or certify the existing P5 proof attempt.
The only quotient is of INDEX labels by simultaneous global sign reversal.
Closed cones and specialized matrix values are never deduplicated.
No K_path, certificate search, source/trajectory coverage, or admission here.
-/

set_option autoImplicit false

namespace RouteBP5ConeIndex

open scoped BigOperators

inductive Cone where
  | pp | nn | pnPos | pnNeg | npPos | npNeg
  deriving DecidableEq, Fintype

abbrev ConeIndex := Cone × Cone
abbrev Representative := Fin 3 × Cone

def reverse : Cone → Cone
  | .pp => .nn
  | .nn => .pp
  | .pnPos => .npNeg
  | .pnNeg => .npPos
  | .npPos => .pnNeg
  | .npNeg => .pnPos

def flip (c : ConeIndex) : ConeIndex := (reverse c.1, reverse c.2)

def representativeFirst (i : Fin 3) : Cone := ![.pp, .pnPos, .pnNeg] i

def representativeCone (r : Representative) : ConeIndex :=
  (representativeFirst r.1, r.2)

/-- false is the representative itself; true reverses BOTH channels. -/
def expand (p : Representative × Bool) : ConeIndex :=
  if p.2 then flip (representativeCone p.1) else representativeCone p.1

/-- The first channel chooses the orbit; its sign also acts on channel five. -/
def select (c : ConeIndex) : Representative × Bool :=
  match c.1 with
  | .pp => ((0, c.2), false)
  | .nn => ((0, reverse c.2), true)
  | .pnPos => ((1, c.2), false)
  | .pnNeg => ((2, c.2), false)
  | .npPos => ((2, reverse c.2), true)
  | .npNeg => ((1, reverse c.2), true)

def representative (c : ConeIndex) : Representative := (select c).1

@[simp] theorem flip_flip (c : ConeIndex) : flip (flip c) = c := by
  revert c; decide

theorem flip_ne (c : ConeIndex) : flip c ≠ c := by
  revert c; decide

@[simp] theorem expand_select (c : ConeIndex) : expand (select c) = c := by
  revert c; decide

@[simp] theorem select_expand (p : Representative × Bool) : select (expand p) = p := by
  revert p; decide

/-- A computable bijection, stronger than existence of an orbit representative. -/
def indexEquiv : ConeIndex ≃ Representative × Bool where
  toFun := select
  invFun := expand
  left_inv := expand_select
  right_inv := select_expand

theorem counts : Fintype.card ConeIndex = 36 ∧
    Fintype.card Representative = 18 := by decide

theorem select_flip (c : ConeIndex) :
    select (flip c) = ((select c).1, !(select c).2) := by
  revert c; decide

theorem same_representative_iff (c d : ConeIndex) :
    representative c = representative d ↔ c = d ∨ c = flip d := by
  revert c d; decide

theorem unique_signed_representative (c : ConeIndex) :
    ∃! p : Representative × Bool, expand p = c := by
  refine ⟨select c, expand_select c, ?_⟩
  intro p hp
  rw [← hp, select_expand]

/-- Exactly two LABELS in every fiber, irrespective of matrix specialization. -/
theorem representative_fiber (r : Representative) :
    Finset.univ.filter (fun c => representative c = r) =
      {representativeCone r, flip (representativeCone r)} := by
  revert r; decide

theorem representative_fiber_card (r : Representative) :
    (Finset.univ.filter (fun c => representative c = r)).card = 2 := by
  revert r; decide

/-- Arbitrary weights: does not assume sign invariance, or distinct values. -/
theorem sum_preserving_multiplicity {A : Type*} [AddCommMonoid A]
    (w : ConeIndex → A) :
    (∑ c, w c) = ∑ r : Representative,
      (w (representativeCone r) + w (flip (representativeCone r))) := by
  calc
    _ = ∑ p : Representative × Bool, w (expand p) :=
      (indexEquiv.symm.sum_comp w).symm
    _ = _ := by
      rw [Fintype.sum_prod_type]
      apply Finset.sum_congr rfl
      intro r _
      simp [expand, add_comm]

theorem sum_invariant {A : Type*} [AddCommMonoid A] (w : ConeIndex → A)
    (hflip : ∀ c, w (flip c) = w c) :
    (∑ c, w c) = ∑ r : Representative, (2 : ℕ) • w (representativeCone r) := by
  rw [sum_preserving_multiplicity]
  simp only [hflip, two_nsmul]

/-- This is the minimal consumer premise; invariance is not inferred from labels. -/
theorem forall_representatives_iff (p : ConeIndex → Prop)
    (hflip : ∀ c, p (flip c) ↔ p c) :
    (∀ c, p c) ↔ ∀ r, p (representativeCone r) := by
  constructor
  · intro h r; exact h _
  · intro h c
    obtain ⟨⟨r, b⟩, he, _⟩ := unique_signed_representative c
    rw [← he]
    cases b
    · exact h r
    · exact (hflip _).mpr (h r)

/-- Data-valued certificates can be lifted if the indexed object is invariant.
No equality between different representatives is needed or assumed. -/
def liftFamily {A : Type*} (value : ConeIndex → A) (Cert : A → Sort*)
    (hflip : ∀ c, value (flip c) = value c)
    (cert : ∀ r, Cert (value (representativeCone r))) : ∀ c, Cert (value c) := by
  intro c
  have hp := expand_select c
  rcases hs : select c with ⟨r, b⟩
  rw [hs] at hp
  rw [← hp]
  cases b
  · exact cert r
  · simpa only [expand, Bool.true_eq, ↓reduceIte, hflip] using cert r

/-- Generic coverage interface: retain the entire parameter witness.
It applies even when a point has several cone labels or infinitely many parameters. -/
def witnessEquiv {U : Type*} (ok : ConeIndex → U → Prop) :
    {p : ConeIndex × U // ok p.1 p.2} ≃
      {p : (Representative × Bool) × U // ok (expand p.1) p.2} where
  toFun p := ⟨(select p.val.1, p.val.2), by simpa using p.property⟩
  invFun p := ⟨(expand p.val.1, p.val.2), p.property⟩
  left_inv p := by apply Subtype.ext; simp
  right_inv p := by apply Subtype.ext; simp

theorem exists_reindexed {U : Type*} (ok : ConeIndex → U → Prop) :
    (∃ c u, ok c u) ↔ ∃ r b u, ok (expand (r, b)) u := by
  constructor
  · rintro ⟨c, u, h⟩
    exact ⟨(select c).1, (select c).2, u, by simpa using h⟩
  · rintro ⟨r, b, u, h⟩
    exact ⟨expand (r, b), u, h⟩

/- The six chart formulas below copy the reviewed table, in a separate namespace.
The companion Python audit compares them with the frozen P5 table as arithmetic
text only. This is not a typed import/adapter to the old P5 theorem namespace. -/

noncomputable section

def cx : Cone → ℝ → ℝ → ℝ
  | .pp, a, _ => a
  | .nn, a, _ => -a
  | .pnPos, a, b => a + b
  | .pnNeg, a, _ => a
  | .npPos, a, _ => -a
  | .npNeg, a, b => -a - b

def cy : Cone → ℝ → ℝ → ℝ
  | .pp, _, b => b
  | .nn, _, b => -b
  | .pnPos, a, _ => -a
  | .pnNeg, a, b => -a - b
  | .npPos, a, b => a + b
  | .npNeg, a, _ => a

abbrev Vec := Fin 4 → ℝ
def Orthant (u : Vec) : Prop := ∀ i, 0 ≤ u i

/-- State order (x4,x5,y4,y5), parameter order (a4,a5,b4,b5). -/
def chart (c : ConeIndex) (u : Vec) : Vec :=
  ![cx c.1 (u 0) (u 2), cx c.2 (u 1) (u 3),
    cy c.1 (u 0) (u 2), cy c.2 (u 1) (u 3)]

@[simp] theorem cx_reverse (c : Cone) (a b : ℝ) :
    cx (reverse c) a b = -cx c a b := by
  cases c <;> simp [reverse, cx] <;> ring

@[simp] theorem cy_reverse (c : Cone) (a b : ℝ) :
    cy (reverse c) a b = -cy c a b := by
  cases c <;> simp [reverse, cy] <;> ring

theorem chart_flip (c : ConeIndex) (u : Vec) :
    chart (flip c) u = -chart c u := by
  funext i
  fin_cases i <;> simp [chart, flip]

theorem chart_expand (r : Representative) (b : Bool) (u : Vec) :
    chart (expand (r, b)) u =
      if b then -chart (representativeCone r) u else chart (representativeCone r) u := by
  cases b <;> simp [expand, chart_flip]

theorem channel_cover (x y : ℝ) :
    ∃ c : Cone, ∃ a b : ℝ, 0 ≤ a ∧ 0 ≤ b ∧ x = cx c a b ∧ y = cy c a b := by
  by_cases hx : 0 ≤ x
  · by_cases hy : 0 ≤ y
    · exact ⟨.pp, x, y, hx, hy, rfl, rfl⟩
    · by_cases hs : 0 ≤ x + y
      · refine ⟨.pnPos, -y, x + y, ?_, hs, ?_, ?_⟩ <;>
          (try dsimp [cx, cy]) <;> linarith
      · refine ⟨.pnNeg, x, -(x + y), hx, ?_, rfl, ?_⟩ <;>
          (try dsimp [cy]) <;> linarith
  · by_cases hy : 0 ≤ y
    · by_cases hs : 0 ≤ x + y
      · refine ⟨.npPos, -x, x + y, ?_, hs, ?_, ?_⟩ <;>
          (try dsimp [cx, cy]) <;> linarith
      · refine ⟨.npNeg, y, -(x + y), hy, ?_, ?_, rfl⟩ <;>
          (try dsimp [cx]) <;> linarith
    · refine ⟨.nn, -x, -y, ?_, ?_, ?_, ?_⟩ <;>
        (try dsimp [cx, cy]) <;> linarith

theorem cone_cover (z : Vec) : ∃ c u, Orthant u ∧ chart c u = z := by
  obtain ⟨c4, a4, b4, ha4, hb4, hx4, hy4⟩ := channel_cover (z 0) (z 2)
  obtain ⟨c5, a5, b5, ha5, hb5, hx5, hy5⟩ := channel_cover (z 1) (z 3)
  refine ⟨(c4, c5), ![a4, a5, b4, b5], ?_, ?_⟩
  · intro i
    fin_cases i
    · exact ha4
    · exact ha5
    · exact hb4
    · exact hb5
  · funext i
    fin_cases i
    · simpa [chart] using hx4.symm
    · simpa [chart] using hx5.symm
    · simpa [chart] using hy4.symm
    · simpa [chart] using hy5.symm

theorem signed_representative_cover (z : Vec) :
    ∃ r b u, Orthant u ∧ chart (expand (r, b)) u = z :=
  (exists_reindexed (fun c u => Orthant u ∧ chart c u = z)).mp (cone_cover z)

/-- Preserves each chart label AND its exact parameter vector, including boundaries. -/
def coverWitnessEquiv (z : Vec) :
    {p : ConeIndex × Vec // Orthant p.2 ∧ chart p.1 p.2 = z} ≃
      {p : (Representative × Bool) × Vec //
        Orthant p.2 ∧ chart (expand p.1) p.2 = z} :=
  witnessEquiv (fun c u => Orthant u ∧ chart c u = z)

def Member (c : ConeIndex) (z : Vec) : Prop := ∃ u, Orthant u ∧ chart c u = z

def membershipWeight (c : ConeIndex) (z : Vec) : ℕ := by
  classical
  exact if Member c z then 1 else 0

/-- Count membership by INDEX. Do not form an image Finset of matrix values. -/
def multiplicity (z : Vec) : ℕ := ∑ c : ConeIndex, membershipWeight c z

theorem cover_multiplicity (z : Vec) :
    multiplicity z = ∑ r : Representative,
      (membershipWeight (representativeCone r) z +
       membershipWeight (flip (representativeCone r)) z) :=
  sum_preserving_multiplicity _

@[simp] theorem chart_zero (c : ConeIndex) : chart c 0 = 0 := by
  rcases c with ⟨c4, c5⟩
  cases c4 <;> cases c5 <;> funext i <;> fin_cases i <;> simp [chart, cx, cy]

theorem origin_member (c : ConeIndex) : Member c 0 :=
  ⟨0, fun _ => le_refl 0, chart_zero c⟩

/-- The origin has 36 covering labels, not 18 disjoint regions. -/
theorem origin_multiplicity : multiplicity 0 = 36 := by
  classical
  simp [multiplicity, membershipWeight, origin_member, counts.1]

end

#print axioms indexEquiv
#print axioms counts
#print axioms flip_ne
#print axioms select_flip
#print axioms same_representative_iff
#print axioms unique_signed_representative
#print axioms representative_fiber_card
#print axioms sum_preserving_multiplicity
#print axioms forall_representatives_iff
#print axioms liftFamily
#print axioms witnessEquiv
#print axioms chart_flip
#print axioms signed_representative_cover
#print axioms coverWitnessEquiv
#print axioms cover_multiplicity
#print axioms origin_multiplicity

end RouteBP5ConeIndex
