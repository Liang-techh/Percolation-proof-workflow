# Attempt history

## 2026-09-06

- `run-Pma9mwVn`: the first concrete accessor attempt had incomplete import
  paths and was rejected before theorem checking.
- `run-0GExomL2`: direct source-entry expansion left the six-step `k` match
  unresolved and was not accepted.
- `run-jsmniGi2`: the same source-level expansion was stopped after about four
  minutes and roughly 1.1 GB RSS.
- `run-chSjuGmr`: a generic entry-contract rewrite was attempted, but the
  accessor import/elaboration remained too expensive and was stopped.
- `run-RUJLBr4n`: manual finite entry cases reduced proof search, but the old
  accessor dependency still reached about 1 GB RSS after four minutes and was
  stopped.

The successful replacement is split into
`routeb_concrete_step_homogeneous_lean`, whose olean is intended for reuse.
No uncompiled prefix candidate is promoted, and no runtime, Float64, comparator,
or full-project regression claim is made here.
