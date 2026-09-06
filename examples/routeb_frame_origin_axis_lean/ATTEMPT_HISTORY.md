# Attempt history

## 2026-09-05 — run-CogQHM12

Failed before theorem checking because the runner omitted the upstream
`FrameRecursion` output directory from `LEAN_PATH`. No DAG or registry state
was changed.

## 2026-09-05 — run-vu1E5o1g

Lean elaboration found an over-aggressive `simp`/length proof: one `omega`
was unreachable and the six-step length theorem was not unfolded through its
wrapper. The source was repaired; no state was recorded.

## 2026-09-05 — run-H0sN55iL

PASS. Pinned Lean compilation, warnings-as-errors, and source restriction
checks all succeeded.
