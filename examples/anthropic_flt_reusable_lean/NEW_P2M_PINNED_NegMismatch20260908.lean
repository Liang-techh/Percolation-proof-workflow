import NEW_P2M_PINNED_API_20260908

/-! EXPECTED FAILURE probe, NOT RUN. Reject incompatible declaration types. -/
set_option autoImplicit false
namespace P2MPinnedNegMismatch
def card : Nat → Nat := fun x => x
def wrong : Bool → Bool := fun x => x
end P2MPinnedNegMismatch

#p2m_pinned_type_eq P2MPinnedNegMismatch.card P2MPinnedNegMismatch.wrong
