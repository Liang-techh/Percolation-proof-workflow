import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
# Route-B M4 pure tail-budget transfer

This sidecar formalizes only the source-independent arithmetic child released
from `T-M4-006`.  It does not formalize the ramp integral, physical `rhoBar`,
P7 source binding, P8 flowpipe coverage, or any M4 admission claim.
-/

set_option autoImplicit false

namespace RouteBM4TailBudgetTransfer

noncomputable section

def oldGate : ℝ := 4483 / 2000

def newGate : ℝ := 1401 / 625

def tailScale : ℝ := 160000

/-- If the tail charge is bounded by `rhoBar/160000` and that enlarged budget
already fits the new gate, then replacing the worst-case tail by any smaller
`Dtail` preserves the gate. -/
theorem tail_budget_transfer
    (Dbase rhoBar Dtail : ℝ)
    (hDtail : Dtail ≤ rhoBar / tailScale)
    (hbudget : Dbase + rhoBar / tailScale ≤ newGate) :
    Dbase + Dtail ≤ newGate := by
  linarith

/-- Exact arithmetic identity behind the old-gate slack used by `T-M4-006`. -/
theorem old_gate_plus_rho16_exact :
    oldGate + 16 / tailScale = newGate := by
  norm_num [oldGate, newGate, tailScale]

/-- At the old C4 gate, any tail satisfying `Dtail ≤ rhoBar/160000` with
`rhoBar ≤ 16` remains within the widened exact rational gate `1401/625`.
No nonnegativity premise on `rhoBar` is needed for this pure arithmetic fact. -/
theorem old_gate_plus_tail_of_rho_le_16
    (Dbase Dtail rhoBar : ℝ)
    (hbase : Dbase ≤ oldGate)
    (hrho : rhoBar ≤ 16)
    (hDtail : Dtail ≤ rhoBar / tailScale) :
    Dbase + Dtail ≤ newGate := by
  have hscale_nonneg : 0 ≤ tailScale := by
    norm_num [tailScale]
  have hrho_scaled : rhoBar / tailScale ≤ 16 / tailScale := by
    exact div_le_div_of_nonneg_right hrho hscale_nonneg
  have htail : Dtail ≤ 16 / tailScale := hDtail.trans hrho_scaled
  calc
    Dbase + Dtail ≤ oldGate + 16 / tailScale := add_le_add hbase htail
    _ = newGate := old_gate_plus_rho16_exact

/-- Slack form: an arbitrary nonnegative allowance `Delta` may be consumed by
any tail bounded by `rhoBar/160000` once `rhoBar/160000 ≤ Delta`. -/
theorem tail_budget_from_slack
    (Dbase Dtail rhoBar Delta : ℝ)
    (hDtail : Dtail ≤ rhoBar / tailScale)
    (hrhoSlack : rhoBar / tailScale ≤ Delta)
    (hbaseSlack : Dbase + Delta ≤ newGate) :
    Dbase + Dtail ≤ newGate := by
  linarith

#print axioms tail_budget_transfer
#print axioms old_gate_plus_rho16_exact
#print axioms old_gate_plus_tail_of_rho_le_16
#print axioms tail_budget_from_slack

end

end RouteBM4TailBudgetTransfer
