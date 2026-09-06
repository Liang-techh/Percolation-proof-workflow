# Attempt history

This leaf was started as a narrow B45-1.2 task from the compiled
`FourierNormalForm.lean` phase bridge.  Each compile is performed in a fresh
output directory with the pinned Lean and Mathlib commits.  Failed source and
logs, if any, remain under `output/` and are recorded here before a receipt is
updated.

## Initial recursion proof — `run-ZcaasovF`

The first pinned compile exited nonzero in the FrameRecursion target.  The
generic `getLast?` proof exposed the implementation-level `List.cons`
normal form, and the first Route-B terminal-product induction left the mapped
head pair opaque.  The runner also failed to restore `set -e`, so its final
trap printed `VERIFY_EXIT_CODE=0` even though `FrameRecursion_COMPILE_EXIT_CODE`
was 1.  The exact source and terminal log are preserved under
`output/run-ZcaasovF/`; the runner was repaired before the next compile.

## Recursive terminal-frame repair — `run-k87wlFSd`

The `getLast?` theorem was replaced by the reusable `terminalFrame` recursion,
whose product identity follows by list induction and associativity.  The
Route-B chain theorem is now an instance of that generic result, avoiding an
unnecessary second induction over pairs.  The runner now captures both Lean
exit codes under `set +e` and restores `set -e` before testing them.  The
pinned compile and axiom audit succeeded; exact output is preserved under
`output/run-k87wlFSd/`.
