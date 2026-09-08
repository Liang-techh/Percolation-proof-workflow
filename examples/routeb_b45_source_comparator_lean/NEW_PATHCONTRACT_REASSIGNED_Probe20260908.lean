import NEW_PATHCONTRACT_REASSIGNED_20260908

set_option autoImplicit false

namespace Body6PathContractReceiptProbe

open RouteBO1PerBodyExactSource RouteBO1Body6CanonicalExportTargets
open Body6PathContractReassigned

/- OPEN_UNCOMPILED. A type/axiom probe, not a contract inhabitant.
   The supplied h remains a hypothesis in every consumer below. -/

example : (5 : Fin 6).val = 5 := rfl

example (q : Q6) (i : Fin 6) :
    sourceBodyMass q (5 : Fin 6) i 5 =
      sourceBodyMass q (⟨5, by decide⟩ : Fin 6) i (⟨5, by decide⟩ : Fin 6) := rfl

theorem consume_explicit_type {X Physical : Type*}
    (embed : X → Physical) (qOf : Physical → Q6)
    (domain : ℝ → Set X) (Omega : Set Q6) (path : ℝ → X)
    (rows : List CanonicalRow)
    (physicalRow : ℝ → Physical → Fin 6 → ℝ) (cap : ℝ → Fin 6 → ℝ)
    (h : SixthColumnPathContract embed qOf domain Omega path rows physicalRow cap) :
    ∀ t ∈ Set.Icc (0 : ℝ) 1, ∀ i : Fin 6,
      |physicalRow t (embed (path t)) i| ≤ cap t i :=
  transport_physical_row_cap embed qOf domain Omega path rows physicalRow cap h

#check SixthColumnPathContract
#check SixthColumnPathContract.projection
#check SixthColumnPathContract.inclusion
#check SixthColumnPathContract.physicalIdentity
#check SixthColumnPathContract.sourceIdentity
#check SixthColumnPathContract.canonicalCap

#print Body6PathContractReassigned.physical_eq_canonical_on_path
#print Body6PathContractReassigned.transport_physical_row_cap
#print axioms Body6PathContractReassigned.physical_eq_canonical_on_path
#print axioms Body6PathContractReassigned.transport_physical_row_cap
#print axioms consume_explicit_type

end Body6PathContractReceiptProbe
