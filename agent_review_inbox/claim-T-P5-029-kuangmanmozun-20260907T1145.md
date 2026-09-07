---
kind: task_claim
task_id: T-P5-029
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
claimed_at: 2026-09-07T11:45:00-06:00
integration_status: pending
continuation_of:
  - T-P5-026
  - T-P5-026-Kpath-interface
  - T-P5-028
---

# Claim — T-P5-029

Scope: derive a source-independent inequality bridge for updating an existing feasible-cone/SPN certificate when the component gain is enlarged by a nonnegative matrix, with special attention to the rank-one moving-frame parameter correction `K_eff = K0 + kappa tensor gamma` from T-P5-028.

The target is the smallest exact theorem that can reuse existing SPN slack without recomputing a full cone search. It must keep the distinction between orthant/copoly-positive nonnegativity and global Loewner/PSD order explicit, and should include a counterexample to any invalid global matrix-order shortcut.

Boundary: no concrete `K_path`, `kappa`, `gamma`, source/Jacobian/Float64 semantics, P8 coverage, ODE continuation, registry admission, or parent closure is claimed. Existing T-P5-026 formalization and the already harvested Kpath typed interface are dependencies, not work to be repeated.
