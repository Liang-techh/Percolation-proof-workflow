import NEW_CONE_INDEX_InverseCover20260908
import NEW_CONE_INDEX_ConcreteConsumer20260908

/-!
Fixed-state fibers of the existing 36-to-18 label map.
No new Cone enumeration, no deduplication of matrices, no concrete K_path.
Orientation may be reconstructed from a NONZERO state and a covering orbit;
at the origin each orbit still has two distinct covering labels.
-/

set_option autoImplicit false

namespace RouteBP5ConeIndexOrbitFiber

open RouteBP5ConeIndex RouteBP5ConeIndexInverseCover
open RouteBP5ConeIndexConcreteConsumer
open scoped BigOperators

noncomputable section

theorem coordinates_neg (c : ConeIndex) (z : Vec) :
    coordinates c (-z) = -coordinates c z := by
  rcases c with ⟨c4, c5⟩
  cases c4 <;> cases c5 <;> funext i <;> fin_cases i <;>
    simp [coordinates, invA, invB] <;> ring

/-- Opposite CLOSED product cones meet only at the origin. Other boundary
overlaps, between different representatives, are deliberately retained. -/
theorem opposite_member_iff_zero (c : ConeIndex) (z : Vec) :
    (Member c z ∧ Member (flip c) z) ↔ z = 0 := by
  constructor
  · rintro ⟨hc, hf⟩
    have hp := (member_iff_coordinates c z).mp hc
    have hn := (member_iff_coordinates c (-z)).mp ((member_flip_iff c z).mp hf)
    rw [coordinates_neg] at hn
    have hz : coordinates c z = 0 := by
      funext i
      exact le_antisymm (neg_nonneg.mp (hn i)) (hp i)
    calc
      z = chart c (coordinates c z) := (chart_coordinates c z).symm
      _ = 0 := by rw [hz, chart_zero]
  · rintro rfl
    exact ⟨origin_member c, origin_member (flip c)⟩

/-- On the covering-label fiber of a nonzero state, representative selection
is injective. This does NOT assert uniqueness of the covering representative. -/
theorem representative_injective_on_members (z : Vec) (hz : z ≠ 0)
    (c d : ConeIndex) (hc : Member c z) (hd : Member d z)
    (hrep : representative c = representative d) : c = d := by
  rcases (same_representative_iff c d).mp hrep with h | h
  · exact h
  · exact False.elim (hz ((opposite_member_iff_zero d z).mp ⟨hd, h ▸ hc⟩))

/-- Orbit membership includes EITHER orientation; it is not membership of
the chosen positive chart alone. Real membership is classically decidable. -/
def OrbitMember (r : Representative) (z : Vec) : Prop :=
  Member (representativeCone r) z ∨ Member (flip (representativeCone r)) z

theorem orbit_member_iff (r : Representative) (z : Vec) :
    OrbitMember r z ↔ ∃ b : Bool, Member (expand (r, b)) z := by
  simp [OrbitMember, Bool.exists_bool, expand]

theorem unique_orientation (r : Representative) (z : Vec) (hz : z ≠ 0)
    (hr : OrbitMember r z) : ∃! b : Bool, Member (expand (r, b)) z := by
  obtain ⟨b, hb⟩ := (orbit_member_iff r z).mp hr
  refine ⟨b, hb, ?_⟩
  intro d hd
  by_cases hdb : d = b
  · exact hdb
  · have hzero : z = 0 := by
      apply (opposite_member_iff_zero (representativeCone r) z).mp
      cases b <;> cases d <;> simp_all [expand]
    exact False.elim (hz hzero)

/-- A finite support of covering ORBITS, not a partition of state space. -/
def coveringRepresentatives (z : Vec) : Finset Representative := by
  classical
  exact Finset.univ.filter (fun r => OrbitMember r z)

theorem coveringRepresentatives_nonempty (z : Vec) :
    (coveringRepresentatives z).Nonempty := by
  classical
  obtain ⟨r, b, u, hu, hzu⟩ := signed_representative_cover z
  refine ⟨r, ?_⟩
  simpa [coveringRepresentatives] using
    (orbit_member_iff r z).mpr ⟨b, u, hu, hzu⟩

/-- Each covering orbit contributes one label at a nonzero state. Unlike
sum_invariant, this lemma makes NO fixed-state membership-evenness assumption. -/
theorem multiplicity_eq_support_card (z : Vec) (hz : z ≠ 0) :
    RouteBP5ConeIndex.multiplicity z = (coveringRepresentatives z).card := by
  classical
  rw [cover_multiplicity]
  have hw : ∀ r : Representative,
      membershipWeight (representativeCone r) z +
        membershipWeight (flip (representativeCone r)) z =
      if OrbitMember r z then 1 else 0 := by
    intro r
    have hn : ¬ (Member (representativeCone r) z ∧
        Member (flip (representativeCone r)) z) :=
      fun h => hz ((opposite_member_iff_zero _ z).mp h)
    by_cases hp : Member (representativeCone r) z <;>
      by_cases hm : Member (flip (representativeCone r)) z <;>
      simp_all [membershipWeight, OrbitMember]
  simp_rw [hw]
  simp [coveringRepresentatives]

theorem origin_support_card : (coveringRepresentatives 0).card = 18 := by
  classical
  simp [coveringRepresentatives, OrbitMember, origin_member, counts.2]

/-- Exact multiplicity correction for erasing orientation in a fixed-state
support. The origin is the only place where that erasure loses a factor two. -/
theorem exact_multiplicity_formula (z : Vec) :
    RouteBP5ConeIndex.multiplicity z =
      if z = 0 then 2 * (coveringRepresentatives z).card
      else (coveringRepresentatives z).card := by
  classical
  by_cases hz : z = 0
  · subst z
    simp [origin_multiplicity, origin_support_card]
  · simp [hz, multiplicity_eq_support_card z hz]

/-- Explicit guard: even though the origin has 18 covering orbits, its
36 covering labels cannot be replaced by that unweighted orbit support. -/
theorem origin_orientation_erasure_loses_multiplicity :
    RouteBP5ConeIndex.multiplicity 0 ≠ (coveringRepresentatives 0).card := by
  rw [origin_multiplicity, origin_support_card]
  decide

end

#print axioms coordinates_neg
#print axioms opposite_member_iff_zero
#print axioms representative_injective_on_members
#print axioms orbit_member_iff
#print axioms unique_orientation
#print axioms coveringRepresentatives_nonempty
#print axioms multiplicity_eq_support_card
#print axioms origin_support_card
#print axioms exact_multiplicity_formula
#print axioms origin_orientation_erasure_loses_multiplicity

end RouteBP5ConeIndexOrbitFiber
