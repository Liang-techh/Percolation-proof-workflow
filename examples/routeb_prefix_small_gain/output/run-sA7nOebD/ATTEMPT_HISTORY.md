# Attempt history

This leaf owns only examples/routeb_prefix_small_gain/. No state, registry,
other example, cache or dependency is written. Compilation uses the installed
Lean executable and cached oleans directly; no lake build/update is run.
Every attempt snapshots local sources and the read-only inputs before Lean
starts, preserves failures, and closes terminal.log before displaying it.
Final status is appended here only after the actual exit codes are observed.

Read-only discovery found no applicable RouteB memory entry. The workspace is
not a Git repository; git status returned that diagnostic. Guessed reports/
and state/ directories were absent; the required current report was located at
artifacts/routeb_gain_checkpoint_20260905/REPORT.md. WSL has no rg, so further
source discovery used Windows rg. These were discovery diagnostics, not Lean
compile attempts. The original tool outputs remain in the task transcript.

## First compile: successful small-gain scalar gates

output/run-81JzZCDw completed on 2026-09-05 with LEAN_COMPILE_EXIT_CODE=0
and VERIFY_EXIT_CODE=0, pinned Lean 4.33.1 and the checked mathlib commit.
All nine printed theorems use only propext, Classical.choice and Quot.sound.
PrefixSmallGain.olean SHA256:
66aec1f0d7819017e49bbf6bc817dacfa4fe84242ed242098aa8314f5b5b6a96.
The complete log, sources and hashed read-only input snapshots are retained.
There was no failed compile attempt.

The user then supplied the main agent's new per-cell source-audit progress.
The actual audit.py, results.json and terminal.log were read without running
the audit. The next source revision adds four generic cell gates and exact
arithmetic for the last passed cell, with the new receipt snapshotted as input.
Its compile result will be recorded after completion. Actual Lipschitz, source,
eta and physical continuation premises remain explicit and unproved here.

One multi-file editor patch failed because its final DERIVATION.md context
did not match. A subsequent read confirmed none of that patch applied; it
was reapplied with corrected context. This was not a Lean compilation failure.
