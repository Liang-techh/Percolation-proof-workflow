# Attempt history

This leaf starts fresh; it does not overwrite or erase the earlier inertial
leaf's failed sign derivations.

1. `run-20260905T191252Z-301371f8`: first rational filter audit, exit 0.
   It preserved audit.py, verify.py, before_run.json and terminal.log before
   evaluating any filter. It covers hypothetical caps and exact Lyapunov
   matrices. No failed mathematical assertion occurred.
2. `run-20260905T191350Z-03c0d6a3`: extended audit using the main's actual source
   caps and individual coordinate/box comparisons, exit 0. Original source
   snapshots and complete exit trailer are retained. The actual bounds input
   was then read from the main's file and recorded by hash and rational cap
   values, but not copied as a separate input snapshot in this attempt.
3. Final wrapper revision additionally copies `source_bounds.input.json` before
   the audit, and the saved script consumes that immutable copy. Final runs
   also snapshot this history and DERIVATION.md before execution. Their unique
   output directories and terminal trailers give their actual status; no
   pre-written success claim is substituted for a failed execution.

There were no Lean source files or compile attempts. During read-only discovery,
PowerShell/rg rejected wildcard file operands for an old port script and a
`*.lean` operand; a later Get-Content lookup found no main-side DERIVATION.md
at that moment. Those discovery errors are visible in tool history, not
mathematical audit failures. They did not run or mutate target code. No saved
terminal files for those exploratory reads are claimed.

All audit terminal logs use a synchronous child process writing directly to an
already-open file; the parent waits and appends AUDIT_EXIT_CODE before closing
it. There is no asynchronous tee and no missing exit-trailer workaround.
