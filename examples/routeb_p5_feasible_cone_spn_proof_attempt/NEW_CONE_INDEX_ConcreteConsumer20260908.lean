import NEW_CONE_INDEX_Core
import NEW_CONE_INDEX_SignedCoverConsumer

/-!
Typed instantiation of the existing generic signed-cover consumer.
No redefinition of the six charts and no import of the old P5 proof attempt.
No concrete gain, SPN certificate, source binding, or closure instance.
-/

set_option autoImplicit false

namespace RouteBP5ConeIndexConcreteConsumer

open RouteBP5ConeIndex
open scoped BigOperators

noncomputable section

def repChart (r : Representative) (u : Vec) : Vec :=
  chart (representativeCone r) u

theorem oriented_eq_expand (r : Representative) (b : Bool) (u : Vec) :
    RouteBP5ConeIndexConsumer.oriented repChart r b u = chart (expand (r, b)) u := by
  simpa [RouteBP5ConeIndexConsumer.oriented, repChart] using (chart_expand r b u).symm

theorem concrete_signed_cover (z : Vec) :
    ∃ r b u, Orthant u ∧ RouteBP5ConeIndexConsumer.oriented repChart r b u = z := by
  obtain ⟨r, b, u, hu, hz⟩ := signed_representative_cover z
  exact ⟨r, b, u, hu, (oriented_eq_expand r b u).trans hz⟩

/-- No evenness assumption: both orientations must be checked. -/
theorem all_iff_signed (P : Vec → Prop) :
    (∀ z, P z) ↔ ∀ r b u, Orthant u →
      P (RouteBP5ConeIndexConsumer.oriented repChart r b u) :=
  RouteBP5ConeIndexConsumer.all_iff_signed repChart Orthant concrete_signed_cover P

/-- Eighteen tests suffice only for an explicitly even STATE predicate. -/
theorem all_iff_even_representatives (P : Vec → Prop)
    (heven : ∀ z, P (-z) ↔ P z) :
    (∀ z, P z) ↔ ∀ r u, Orthant u → P (repChart r u) :=
  RouteBP5ConeIndexConsumer.all_iff_representatives
    repChart Orthant concrete_signed_cover P heven

/-- Reindex all witnesses, retaining the parameter, label and orientation.
In particular this is not a choice of a single cone on closed boundaries. -/
def orientedCoverWitnessEquiv (z : Vec) :
    {p : ConeIndex × Vec // Orthant p.2 ∧ chart p.1 p.2 = z} ≃
      {p : (Representative × Bool) × Vec // Orthant p.2 ∧
        RouteBP5ConeIndexConsumer.oriented repChart p.1.1 p.1.2 p.2 = z} where
  toFun p := ⟨(select p.val.1, p.val.2), p.property.1, by
    rw [oriented_eq_expand, expand_select]
    exact p.property.2⟩
  invFun p := ⟨(expand p.val.1, p.val.2), p.property.1, by
    rw [← oriented_eq_expand]
    exact p.property.2⟩
  left_inv p := by apply Subtype.ext; simp
  right_inv p := by apply Subtype.ext; simp

/-- Covariance, not invariance at a fixed state. The same u is retained. -/
theorem member_flip_iff (c : ConeIndex) (z : Vec) :
    Member (flip c) z ↔ Member c (-z) := by
  constructor
  · rintro ⟨u, hu, hz⟩
    refine ⟨u, hu, ?_⟩
    simpa only [chart_flip, neg_neg] using congrArg Neg.neg hz
  · rintro ⟨u, hu, hz⟩
    refine ⟨u, hu, ?_⟩
    rw [chart_flip, hz, neg_neg]

def flipEquiv : ConeIndex ≃ ConeIndex where
  toFun := flip
  invFun := flip
  left_inv := flip_flip
  right_inv := flip_flip

/-- Total membership is even although individual label membership is not. -/
theorem multiplicity_neg (z : Vec) :
    RouteBP5ConeIndex.multiplicity (-z) = RouteBP5ConeIndex.multiplicity z := by
  classical
  have hw : ∀ c, membershipWeight c (-z) = membershipWeight (flip c) z := by
    intro c
    simp only [membershipWeight, member_flip_iff]
  unfold RouteBP5ConeIndex.multiplicity
  simp_rw [hw]
  exact flipEquiv.sum_comp (fun c => membershipWeight c z)

end

#print axioms oriented_eq_expand
#print axioms concrete_signed_cover
#print axioms all_iff_signed
#print axioms all_iff_even_representatives
#print axioms orientedCoverWitnessEquiv
#print axioms member_flip_iff
#print axioms multiplicity_neg

end RouteBP5ConeIndexConcreteConsumer
