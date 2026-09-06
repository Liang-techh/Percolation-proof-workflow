import Challenge

namespace Minimal

theorem child_left_verified (n : Nat) : n ≤ n + 1 := by omega
theorem child_right_verified (n : Nat) : n + 1 ≤ n + 2 := by omega
theorem main_verified (n : Nat) : Goal n := by
  unfold Goal
  exact child_right_verified n

end Minimal
