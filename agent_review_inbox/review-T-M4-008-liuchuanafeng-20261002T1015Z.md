---
kind: review_result
review_id: review-T-M4-008-liuchuanafeng-20261002T1015Z
source_agent: 流川枫
created_at: 2026-10-02T10:15:00Z
inspected_commit: e70ee3f6eb45dcb7bfa88ac030910acdb9ee06e3
inspected_paths:
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/claim-T-M4-008-daai-xianzun-20260907T0053.md
  - agent_review_inbox/review-T-M4-008-daai-xianzun-20260907T0102.md
  - examples/routeb_m4_cross_branch_budget_lean/CrossBranchBudget.lean
  - examples/routeb_m4_cross_branch_budget_lean/README.md
  - examples/routeb_m4_tail_budget_transfer_lean/M4TailBudgetTransfer.lean
  - examples/routeb_m4_tail_budget_transfer_lean/README.md
  - examples/routeb_terminal_qpoly_comparator_lean/README.md
  - src/percolation_workflow/
task_id: T-M4-008
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
---

# T-M4-008 admission probe: energy-to-Schur terminal bridge

## Question

Does commit `e70ee3f6eb45dcb7bfa88ac030910acdb9ee06e3` already contain `M4.energy_to_schur_budget_bridge` such that the 81-cell geometry threshold equals the required threshold, the 2x2 comparison has exact determinant zero and nonnegative diagonals, and the conditional conclusion `p45<=12` follows from the supplied energy tube?

## Decision

**No. Keep `admission_label: pending`.** The named bridge is not present as a consumable checker or Lean child. Nearby arithmetic sidecars and the historical inbox review do not discharge the queue contract.

This is not `rejected`: the conditional implication was not disproved. It is not `compiled_candidate`: no energy-to-Schur file was compiled and no `verify.sh` was run. It is not `verified` and not architecture-only: the queue asks for an exact 2x2/threshold/terminal check, but that artifact is missing.

## Evidence inspected (read-only)

1. **Queue contract is still open.**
   `task_queue.md` lists `T-M4-008` with status `open` and scope `M4.energy_to_schur_budget_bridge`: 81-cell geometry threshold equality, exact 2x2 determinant zero with nonnegative diagonals, and conditional `p45<=12` from the supplied energy tube. Energy, q1/q6 coverage, residual, and flowpipe premises must stay separate.

2. **Historical inbox result is a different seam.**
   `review-T-M4-008-daai-xianzun-20260907T0102.md` (blob `7d861b7ed9bdfaf33f7a638140fc7b4fbbe72257`) derives a weighted moment `J_rho <= 16/3` from the P7 tail charge and the P8 ramp. It does not name `energy_to_schur_budget_bridge`, does not check an 81-cell geometry threshold, does not exhibit a 2x2 matrix with determinant zero, and does not conclude `p45<=12`. Its own admission label is `pending`. It is provenance only and is not rewritten here.

3. **Existing M4 Lean children are T-M4-007 tail transfers, not this bridge.**
   - `examples/routeb_m4_cross_branch_budget_lean/CrossBranchBudget.lean` (blob `3d45fe486c0b0181b2abd7d9b084641215e59114`) proves `D_new - D_old = 1/10000` and conditional `D_total <= D_new` under `rho_bar <= 16`. README assigns it to `T-M4-007`.
   - `examples/routeb_m4_tail_budget_transfer_lean/M4TailBudgetTransfer.lean` (blob `88737af4367e435e5d5e0752af04b3b601488352`) proves `oldGate + 16/tailScale = newGate` and the corresponding tail transfer. README assigns it to `T-M4-007`.
   Neither file mentions `p45`, a 2x2 determinant, an 81-cell geometry threshold, or an energy tube. `#print axioms` lines are source directives, not a captured axiom list from this pass. `verify.sh` was not executed.

4. **Terminal qpoly comparator is a different target.**
   `examples/routeb_terminal_qpoly_comparator_lean/README.md` (blob `563f940bfe4e7720377b87f867b69a6c2c2e41ad`) records `qpoly(1) < 12` under `D <= 4483/2000` and the direct linear split. It explicitly says a `p <= 28/5` path only yields `qpoly <= 14` and cannot discharge the terminal target. That is not a proof of `p45<=12` from an energy tube.

5. **Named symbol was not found in the workflow package listing.**
   `src/percolation_workflow/` at this commit has no module whose name contains `energy_to_schur` or `schur_budget`. GitHub code search for the symbol returned incomplete/empty; the directory listing is the positive evidence used here. Absence of a listed module is the obstruction, not a failed checker run.

## Compile obstruction

There is no file to pin. A future formalization owner must add a sidecar whose statement is exactly the queue contract, with premises kept separate:

```text
theorem energy_to_schur_budget_bridge
    (h81 : geometryThreshold = requiredThreshold)
    (hdet : det M2 = 0)
    (hdiag : M2 0 0 >= 0 ∧ M2 1 1 >= 0)
    (henergy : energyTube)
    : p45 <= 12
```

with the 81-cell equality, the 2x2 entries, and the energy tube supplied as typed hypotheses or exact witnesses, plus pinned toolchain, exit code, `#print axioms`, and placeholder scan. Until that file exists, the obstruction is missing artifact.

## Assumptions still required

- energy-tube premise, not imported from a coarse scalar-tube failure;
- q1/q6 coverage, residual binding, and flowpipe coverage as separate dependencies;
- no identification of `p45` with deployed DH coordinates;
- no use of solver status as evidence.

## Integration target and requested action

- Target: documentation / DAG metadata only. Leave `T-M4-008` open.
- Requested action: do not treat the 2026-09-07 weighted-rho review or the `T-M4-007` tail transfers as this bridge; do not edit registry, `state.json`, or formal certificates.
- Next owner should add the missing exact bridge or an explicit failed receipt, then return a pinned result.

## Forbidden-boundary compliance

- Did not call the conditional bridge a finite-time theorem.
- Did not import a coarse scalar-tube failure as proof.
- Did not use solver status.
- Did not open the M4 or formal gate.
- Did not edit registry, state, or formal proofs.
