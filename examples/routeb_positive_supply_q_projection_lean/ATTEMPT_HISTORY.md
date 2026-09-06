# Attempt history

## Attempt 1 — initial exact Q projection formalization

Status: failed; sharp witness vector applications did not reduce under the
first proof script.  Output: `output/run-MoXdpt3f/`.

## Attempt 2 — simp-based vector reduction

Status: failed; simplification reduced the sharpness goal to a conjunction of
`True` propositions but warnings-as-errors rejected the unused simp argument.
Output: `output/run-wVW1bJeU/`.

## Attempt 3 — explicit coordinate expansion

Status: PASS.  The sharpness proof now uses a definitional `change` to expose
the six coordinates and closes each exact rational identity with `ring`.
Successful output: `output/run-TQRk7uuS/`.

All compiler errors, including linter failures under
`-DwarningAsError=true`, remain in their corresponding `output/run-*`
directories.  The successful run is recorded in `FINAL_RECEIPT.md` without
deleting this history.
