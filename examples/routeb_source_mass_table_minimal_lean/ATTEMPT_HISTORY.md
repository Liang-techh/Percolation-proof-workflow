# Attempt history

## run-SlWaTbot — failed draft

The first Mathlib-only draft exposed `Fin 3` scalar multiplication and `Fin 6`
vector-literal expansion failures.  It was not promoted.

## run-wbyZgM4E — failed repair

A second draft still left three exact-entry goals and introduced `sorryAx` in
the failed output.  It was not promoted.

## run-TrFQWCxh — successful repair

The finite-sum proof was changed to `ring_nf`, and table-entry conjunctions
were closed by explicit constructor/reflexivity steps.  Compile and verify
both returned zero with no source restriction violation.
