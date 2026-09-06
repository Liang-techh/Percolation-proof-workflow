# Attempt history

## 2026-09-05 — run-479iByeJ

The first concrete list expansion caused excessive elaboration because
`simp` unfolded Route-B matrix terms. The run was stopped; no state changed.

## 2026-09-05 — run-8KCH3Ouq

The six-step list theorem was generalized to an abstract `Fin 6 → RealFrame`
step function. The theorem compiled, but the proof still allowed matrix
identity simplification and was retained only as an intermediate attempt.

## 2026-09-05 — run-3FCa6JgK

PASS after preserving the source's `1 * step` left-multiplication structure.

## 2026-09-05 — run-tFcwKUbB

The theorem parsed but failed on an avoidable last-frame parenthesis error.

## 2026-09-05 — run-lVHyO9Lp

PASS. Current source snapshot compiled with pinned Lean, warnings-as-errors,
and source restriction checks. The successful form keeps the generic prefix
abstract and avoids expanding DH entries.
