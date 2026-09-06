# Attempt history

## 2026-09-05 — first targeted attempt

- Implemented the smallest safe bridge: freeze the exact q=0 6x6 aggregate,
  independently re-derive it from all 610 CSV rows, then prove the regularized
  equality in Lean.
- Deliberately did not put CSV parsing or a file-content axiom in Lean.
- No `sorry`, `admit`, or non-standard axiom is used.
- Full q-dependent functional identity and Float64 semantics remain open.

### Lean repair

The first compile exposed an `if`-expression precedence error in the
entrywise statement (`else 0 = M0`).  Parentheses were added; the failed run
is retained under `output/`.
