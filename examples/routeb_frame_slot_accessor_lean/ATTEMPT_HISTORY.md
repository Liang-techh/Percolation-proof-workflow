# Attempt history

## 2026-09-06 — run-hVIjPmm9

The first version used unavailable Lean 4.33 `List.get?` API. No theorem was
admitted and no persistent state changed.

## 2026-09-06 — run-4RJoHvpZ

PASS after replacing `get?` with `List.getD` and retaining matrix products
opaque. Pinned Lean, warnings-as-errors, and source restriction checks passed.
