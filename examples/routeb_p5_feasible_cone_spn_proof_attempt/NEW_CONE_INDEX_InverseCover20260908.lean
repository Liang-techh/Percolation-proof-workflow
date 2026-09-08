import NEW_CONE_INDEX_Core

/-!
Exact inverse coordinates and finite membership fibers for the existing core.
This imports the actual ConeIndex type; no replacement enumeration or K_path.
Real membership uses classical decidability, not an executable real oracle.
-/

set_option autoImplicit false

namespace RouteBP5ConeIndexInverseCover

open RouteBP5ConeIndex
open scoped BigOperators

noncomputable section

def invA : Cone → ℝ → ℝ → ℝ
  | .pp, x, _ => x
  | .nn, x, _ => -x
  | .pnPos, _, y => -y
  | .pnNeg, x, _ => x
  | .npPos, x, _ => -x
  | .npNeg, _, y => y

def invB : Cone → ℝ → ℝ → ℝ
  | .pp, _, y => y
  | .nn, _, y => -y
  | .pnPos, x, y => x + y
  | .pnNeg, x, y => -x - y
  | .npPos, x, y => x + y
  | .npNeg, x, y => -x - y

/-- Same interleaving as the core: (a4,a5,b4,b5), not (a4,b4,a5,b5). -/
def coordinates (c : ConeIndex) (z : Vec) : Vec :=
  ![invA c.1 (z 0) (z 2), invA c.2 (z 1) (z 3),
    invB c.1 (z 0) (z 2), invB c.2 (z 1) (z 3)]

@[simp] theorem coordinates_chart (c : ConeIndex) (u : Vec) :
    coordinates c (chart c u) = u := by
  rcases c with ⟨c4, c5⟩
  cases c4 <;> cases c5 <;> funext i <;> fin_cases i <;>
    simp [coordinates, chart, invA, invB, cx, cy]

@[simp] theorem chart_coordinates (c : ConeIndex) (z : Vec) :
    chart c (coordinates c z) = z := by
  rcases c with ⟨c4, c5⟩
  cases c4 <;> cases c5 <;> funext i <;> fin_cases i <;>
    simp [coordinates, chart, invA, invB, cx, cy] <;> ring

def chartEquiv (c : ConeIndex) : Vec ≃ Vec where
  toFun := chart c
  invFun := coordinates c
  left_inv := coordinates_chart c
  right_inv := chart_coordinates c

/-- Uniqueness is per LABEL. A boundary state can still have many labels. -/
theorem parameter_unique (c : ConeIndex) (u v : Vec)
    (h : chart c u = chart c v) : u = v :=
  (chartEquiv c).injective h

theorem member_iff_coordinates (c : ConeIndex) (z : Vec) :
    Member c z ↔ Orthant (coordinates c z) := by
  constructor
  · rintro ⟨u, hu, h⟩
    rw [← h, coordinates_chart]
    exact hu
  · intro h
    exact ⟨coordinates c z, h, chart_coordinates c z⟩

/-- Drop only the uniquely determined parameter, NEVER the boundary label. -/
def witnessLabelEquiv (z : Vec) :
    {p : ConeIndex × Vec // Orthant p.2 ∧ chart p.1 p.2 = z} ≃
      {c : ConeIndex // Member c z} where
  toFun p := ⟨p.val.1, p.val.2, p.property⟩
  invFun c := ⟨(c.val, coordinates c.val z),
    (member_iff_coordinates c.val z).mp c.property, chart_coordinates c.val z⟩
  left_inv p := by
    apply Subtype.ext
    change (p.val.1, coordinates p.val.1 z) = p.val
    apply Prod.ext
    · rfl
    · exact (congrArg (coordinates p.val.1) p.property.2).symm.trans
        (coordinates_chart p.val.1 p.val.2)
  right_inv c := by apply Subtype.ext; rfl

/-- Restrict the actual 36 ≃ 18×Bool bijection to all labels covering z. -/
def memberLabelEquiv (z : Vec) :
    {c : ConeIndex // Member c z} ≃
      {p : Representative × Bool // Member (expand p) z} where
  toFun c := ⟨select c.val, by simpa using c.property⟩
  invFun p := ⟨expand p.val, p.property⟩
  left_inv c := by apply Subtype.ext; simp
  right_inv p := by apply Subtype.ext; simp

def coveringLabels (z : Vec) : Finset ConeIndex := by
  classical
  exact Finset.univ.filter (fun c => Orthant (coordinates c z))

theorem coveringLabels_spec (c : ConeIndex) (z : Vec) :
    c ∈ coveringLabels z ↔ Member c z := by
  classical
  simp [coveringLabels, member_iff_coordinates]

theorem coveringLabels_nonempty (z : Vec) : (coveringLabels z).Nonempty := by
  obtain ⟨c, u, hu, hz⟩ := cone_cover z
  exact ⟨c, (coveringLabels_spec c z).mpr ⟨u, hu, hz⟩⟩

theorem coveringLabels_card (z : Vec) :
    (coveringLabels z).card = RouteBP5ConeIndex.multiplicity z := by
  classical
  simp [coveringLabels, RouteBP5ConeIndex.multiplicity,
    membershipWeight, member_iff_coordinates]

def coordinateWeight (c : ConeIndex) (z : Vec) : ℕ := by
  classical
  exact if Orthant (coordinates c z) then 1 else 0

/-- An explicit four-inequality test on each of 36 labels, retaining both signs. -/
theorem inverse_cover_multiplicity (z : Vec) :
    (coveringLabels z).card = ∑ r : Representative,
      (coordinateWeight (representativeCone r) z +
       coordinateWeight (flip (representativeCone r)) z) := by
  classical
  rw [coveringLabels_card, cover_multiplicity]
  simp only [membershipWeight, coordinateWeight, member_iff_coordinates]

theorem origin_coveringLabels_card : (coveringLabels 0).card = 36 := by
  rw [coveringLabels_card, origin_multiplicity]

end

#print axioms coordinates_chart
#print axioms chart_coordinates
#print axioms chartEquiv
#print axioms parameter_unique
#print axioms member_iff_coordinates
#print axioms witnessLabelEquiv
#print axioms memberLabelEquiv
#print axioms coveringLabels_spec
#print axioms coveringLabels_nonempty
#print axioms coveringLabels_card
#print axioms inverse_cover_multiplicity
#print axioms origin_coveringLabels_card

end RouteBP5ConeIndexInverseCover
