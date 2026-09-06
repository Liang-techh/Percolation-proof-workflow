namespace Minimal

def Goal (n : Nat) : Prop := n + 1 ≤ n + 2

theorem child_left (n : Nat) : n ≤ n + 1 := by sorry
theorem child_right (n : Nat) : n + 1 ≤ n + 2 := by sorry
theorem main (n : Nat) : Goal n := by sorry

end Minimal
