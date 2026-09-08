import NEW_P2M_PINNED_API_20260908

/-! OPEN_UNCOMPILED positive probes. No Mathlib, no old P2M syntax. -/
set_option autoImplicit false

namespace P2MPinnedProbe
universe u v

def identityCard (α : Type u) : α → α := fun x => x
def identityProof (α : Type u) : α → α := fun x => x
def pairCard (α : Type u) (β : Type v) : α → β → α × β := fun x y => (x, y)
def pairProof (α : Type u) (β : Type v) : α → β → α × β := fun x y => (x, y)

theorem dependentContext (α : Type u) (x y : α) (h : x = y) : y = x := by
  p2m_pinned_exact_reverting (fun _ _ _ h => h.symm)

theorem multipleGoals (n : Nat) : n = n ∧ n = n := by
  constructor
  · p2m_pinned_exact_reverting (fun _ => rfl)
  · p2m_pinned_exact_reverting (fun _ => rfl)

theorem localLet (n : Nat) : n + 0 = n := by
  let m := n
  have hm : m = n := rfl
  p2m_pinned_exact_reverting (by intros; rfl)

end P2MPinnedProbe

#p2m_pinned_type_eq P2MPinnedProbe.identityCard P2MPinnedProbe.identityProof
#p2m_pinned_type_eq P2MPinnedProbe.pairCard P2MPinnedProbe.pairProof
#print axioms P2MPinnedProbe.dependentContext
#print axioms P2MPinnedProbe.multipleGoals
#print axioms P2MPinnedProbe.localLet
