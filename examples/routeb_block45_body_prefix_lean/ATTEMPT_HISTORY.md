# Attempt history

## 2026-09-06 — run-OtPJlbU3

The single-body source adapter was written over the fixed `Fin 7` prefix and
proved the intended block-(4,5) inactive/active formulas at the source level.
Its compile was stopped after four minutes because importing the existing
`BodyMass` and frame-prefix modules together caused continued elaboration
growth. No theorem was admitted and no persistent state changed.

The mathematical content is retained as a draft. The next implementation
uses a minimal body-semantic core module with no frame or matrix-source
imports, followed by a separate adapter theorem.
