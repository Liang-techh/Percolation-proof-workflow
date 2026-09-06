import Mathlib

open scoped BigOperators

namespace RobotFormalEnergy

/- Verbatim declaration extracted from ExistingEnergyCore.lean (lines 178-196).
   The full frozen file is retained, but unrelated later calculus declarations
   do not compile in the current pin. Only this reused declaration is claimed. -/
theorem closed_loop_power_identity
    (kp d g q v tau : Fin 6 → ℝ) (G0 : Fin 6 → ℝ) (w dUc : ℝ)
    (htau : ∀ i, tau i = -kp i * q i - d i * v i + G0 i + g i * w)
    (hUc : dUc = ∑ i, (kp i * q i - G0 i) * v i) :
    (∑ i, v i * tau i) + dUc =
      -(∑ i, d i * v i ^ 2) + (∑ i, g i * v i * w) := by
  rw [hUc]
  rw [← Finset.sum_add_distrib]
  have hsum :
      -(∑ i, d i * v i ^ 2) + (∑ i, g i * v i * w) =
        ∑ i, (-d i * v i ^ 2 + g i * v i * w) := by
    simp [Finset.sum_add_distrib]
  rw [hsum]
  apply Finset.sum_congr rfl
  intro i hi
  rw [htau i]
  ring

end RobotFormalEnergy
