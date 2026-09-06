# Actual compiler attempts

All attempts use pinned Lean 4.33.1, cached dependencies only, and
`warningAsError=true`. Each has its own immutable pre-compilation sources,
imported oleans, SHA256 manifest, full terminal log and actual exit codes.

| Attempt | Result |
| --- | --- |
| run-jeVP2yIu | ReferenceMass exit 1: finite successor indices not normalized; negated division normalization in remainder identity. No downstream compile. |
| run-0C9REMhm | ReferenceMass exit 1: remainder normalization fixed; finite successor normalization still required. No downstream compile. |
| run-VnGuiXhy | Exact source audit passed. All ReferenceMass proof axiom reports contain only standard axioms, but exit 1 because two unnecessary `<;>` linter warnings were promoted to errors. No downstream compile. |
| run-EQMuJx15 | ReferenceMass exit 0 with only standard axioms. ActualStorage exit 1: position-weight identity simplification left a trivial disjunction. Positivity and terminal theorem reports already have only standard axioms. |

Failed runs' printed `sorryAx` dependencies result from failed elaboration and
must not be treated as verified theorems. Only a zero-exit complete run is a
verification receipt.
