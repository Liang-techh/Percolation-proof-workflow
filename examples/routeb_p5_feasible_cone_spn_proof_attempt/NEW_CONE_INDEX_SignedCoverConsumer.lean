import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
Minimal consumer of NEW_CONE_INDEX_Core.signed_representative_cover.
Independent of the old P5 namespace and of any concrete gain/certificate.
Instantiate R := RouteBP5ConeIndex.Representative, U := Vec,
chart := chart o representativeCone, admissible := Orthant.
Core.chart_expand converts the core cover to the cover premise below.
No claim that membership at a fixed state is invariant under flipping a label.
-/

set_option autoImplicit false

namespace RouteBP5ConeIndexConsumer

section
variable {R U V : Type*} [AddGroup V]
variable (chart : R → U → V) (admissible : U → Prop)

def oriented (r : R) (b : Bool) (u : U) : V :=
  if b then -chart r u else chart r u

/-- Without evenness, both directions remain explicit in the consumer. -/
theorem all_iff_signed
    (cover : ∀ z, ∃ r b u, admissible u ∧ oriented chart r b u = z)
    (P : V → Prop) :
    (∀ z, P z) ↔ ∀ r b u, admissible u → P (oriented chart r b u) := by
  constructor
  · intro h r b u _
    exact h _
  · intro h z
    obtain ⟨r, b, u, hu, hz⟩ := cover z
    rw [← hz]
    exact h r b u hu

/-- The sole additional premise for dropping orientation is explicit evenness.
This changes neither label counts nor the number of witnesses at boundaries. -/
theorem all_iff_representatives
    (cover : ∀ z, ∃ r b u, admissible u ∧ oriented chart r b u = z)
    (P : V → Prop) (even : ∀ z, P (-z) ↔ P z) :
    (∀ z, P z) ↔ ∀ r u, admissible u → P (chart r u) := by
  rw [all_iff_signed chart admissible cover P]
  constructor
  · intro h r u hu
    exact h r false u hu
  · intro h r b u hu
    cases b
    · exact h r u hu
    · exact (even _).mpr (h r u hu)

end

/-- A non-even predicate cannot be transported from positive to negative states.
This is a guard against treating state membership as an invariant weight. -/
theorem non_even_guard :
    (∀ u : ℝ, 0 ≤ u → 0 ≤ u) ∧ ¬ (∀ z : ℝ, 0 ≤ z) := by
  constructor
  · intro u hu; exact hu
  · intro h
    have := h (-1)
    norm_num at this

#print axioms all_iff_signed
#print axioms all_iff_representatives
#print axioms non_even_guard

end RouteBP5ConeIndexConsumer
