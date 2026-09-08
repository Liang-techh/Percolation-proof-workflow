import NEW_P2M_PINNED_API_20260908

/-! EXPECTED FAILURE probe, NOT RUN. A successful exit would violate the gate contract. -/
set_option autoImplicit false
namespace P2MPinnedNegSpecialization
universe u
def card (α : Type u) : α → α := fun x => x
def specialized (α : Type) : α → α := fun x => x
end P2MPinnedNegSpecialization

#p2m_pinned_type_eq P2MPinnedNegSpecialization.card P2MPinnedNegSpecialization.specialized
