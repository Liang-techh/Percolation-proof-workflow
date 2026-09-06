# Attempt history

The targeted verification wrapper produced one retained run:

| Run | Result | Notes |
| --- | --- | --- |
| `output/run-TIbpu6FN` | PASS | Lean 4.33.1, Mathlib commit pinned, warnings-as-errors, pre-run snapshot hash check passed. |

No failed targeted wrapper run was discarded. Future failures from `verify.sh`
remain in their unique `output/run-*` directory with source snapshot and full
`terminal.log`.
