# Exact statement-boundary contract review

## Scope and status

This sidecar starts after the real final strict consumer.  It separates the
real strict inequality, the tagged final statement, the exact statement-boundary
equivalence, and comparator-input premises.

No Lean or Lake command was run.  This is an uncompiled typed contract, not a
comparator receipt, comparator-accepted result, Lean-verification claim, or
registry promotion.

## Contract supplied

- `TaggedFinalStatement` carries an explicit tag, binder, order,
  normalization, and proposition target.
- `ExactStatementBoundaryContract` requires equality of the tag, binder,
  order, normalization, and proposition target.  The consumer theorem uses
  only the explicit target equality to transport the real strict inequality;
  the other equalities remain mandatory fields of the contract.
- `ComparatorAcceptancePremises` is separate and records checker target
  equality, zero exit code, and the exact standalone success output
  `Your solution is okay!`.  These are premises only; no theorem here claims
  that a comparator was executed or accepted the candidate.
- `StatementBoundaryObstruction` and
  `boundary_obstruction_excludes_exact_contract` record that a concrete tag,
  binder, order, normalization, or target mismatch prevents construction of
  the exact boundary contract.

## Remaining boundaries

Missing binder/order/normalization/target equality remains an open statement
boundary and cannot be replaced by numeric similarity, reordered binders, or
implicit normalization.  The sidecar does not validate source data, coverage,
digest/receipt evidence, comparator execution, comparator acceptance, Lean
compilation, or registry promotion.  No state, registry, receipt, or shared
script was modified.
