# Terminal attempt history

All writes and compiler outputs are under `examples/routeb_signed_gap_lean/`.
The initial read-only discovery confirmed state revision45 and read the
prefix report and signed-work proposal. WSL had no rg, so narrow Mathlib
API reads used grep/sed. One overbroad state print and one shell glob search
produced truncated/read-only diagnostic output; neither changed source or
state and neither was a Lean attempt.

| Attempt | Result | Explanation |
| --- | --- | --- |
| run-PuV8q7I8 | exit 1 | First SignedGap compile: convert exposed real-instance equalities, pointwise function products needed reduction, and force-balance sums needed normalization. Full failed snapshot/log retained. |
| run-cxJmZdLH | exit 1 | Instance goals fixed; remaining Pi.mul_apply reduction and multiplication of component balance equalities by velocity were made explicit. |
| run-LngGIvXv | exit 0 | SignedGap, ResidualMultiplier, IntegratedBudget all compiled. Real finite-sum gap derivative, affine 7x7 expansion/cancellation, FTC budget, and strict-prefix bootstrap succeeded. All printed dependencies contain only propext, Classical.choice, Quot.sound. |
| run-mHNkfP57 | exit 1 | Final SignedGap and ResidualMultiplier compiled. All IntegratedBudget proofs elaborated with standard axioms, but warningAsError rejected one unnecessary `<;>` combinator in the augmentation proof. Removed that combinator; no mathematical statement changed. |
| run-iH9FGdAL | exit 0 | Final complete compile: all three modules passed warningAsError=true; every printed axiom report contains only standard axioms. Started 20:36:09 UTC and ended 20:37:50 UTC on 2026-09-05. |

Every run has a complete `terminal.log` with START_UTC, pinned toolchain,
Mathlib commit, LEAN_PATH, the actual per-module command, its exit code,
output hashes on success, and VERIFY_EXIT_CODE. `before_run.sha256` binds
the source and read-only input snapshots before compilation. Compiler
errors and their temporary sorryAx reports remain in failed attempts only;
no such attempt is presented as successful.

The main task later supplied the successful coefficient-audit reference
`examples/routeb_affine_multiplier/output/run-20260905T202634Z-e39dc9a3`.
That reference was acknowledged, without rerunning it or adding inverse
equivalence/numerical proof gates. It is a local-jet result, not global
storage feasibility. No extra physical premises were claimed.

Eta source binding, bounds and regularity remain open. All-point
HasDerivAt and the interior-point FTC interface are stronger than an AE or
sampled numerical trajectory claim; no AE/absolute-continuity adapter was
silently assumed. The README lists the remaining source, same-state,
coverage, initial-family, uniform-prefix, and continuation premises.

Final read-only checks compared all three current .lean hashes with the
successful run's frozen sources: all equal. A source-token scan found no
sorry, admit, or axiom declarations. The first PowerShell hash display was
lost when an explicit exit preempted formatting; the same read-only hash
comparison was displayed successfully as JSON. No further Lean/source
edits occurred after the successful compilation. README, this history,
and FINAL_RECEIPT were finalized afterward without modifying run snapshots.
