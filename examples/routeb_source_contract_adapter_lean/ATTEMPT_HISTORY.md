# Attempt history

## 2026-09-06 — source contract adapter repair loop

- `run-7jCP3pXZ`: stopped before Lean because the slot precursor path used
  `run-4RJoHvp` instead of the verified `run-4RJoHvpZ`.
- `run-H9KI5NQj`: after fixing that path, Lean reported the missing
  transitive `FramePrefixIndex` import closure.
- `run-57yeeHyL`: after adding the frame-prefix/origin-axis/real-DH/frame
  recursion precursors, Lean reported the missing `BodySemanticCore` closure.
- `run-OEO34Kpq`: after adding the body semantic core and exposing the
  `Fin 6 → Fin 7` parent-axis indexing, Lean identified the axis slot mapping,
  unavailable structure ext theorem, and nested vector equality applications.
- `run-934sS1Nt`: the minimized proof passed all semantic theorems; only an
  ambiguous `IMat` abbreviation remained.
- `run-RSGGTurS`: qualified the contract-core inertia type; compile and
  source-restriction checks passed.

The failed runs remain as reproducible workflow evidence. No broad regression
was run and no registry promotion is made.
