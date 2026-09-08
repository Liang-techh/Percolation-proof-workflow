import NEW_P2M_PINNED_API_20260908

/-! EXPECTED FAILURE probe, NOT RUN. Distinct statement universes must not merge. -/
set_option autoImplicit false
namespace P2MPinnedNegMerge
universe u v
def card (α : Type u) (β : Type v) : α → β → α × β := fun x y => (x, y)
def merged (α β : Type u) : α → β → α × β := fun x y => (x, y)
end P2MPinnedNegMerge

#p2m_pinned_type_eq P2MPinnedNegMerge.card P2MPinnedNegMerge.merged
