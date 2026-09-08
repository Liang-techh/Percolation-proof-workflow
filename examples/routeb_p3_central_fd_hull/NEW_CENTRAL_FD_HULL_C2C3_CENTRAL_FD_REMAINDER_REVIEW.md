# P3 central-FD remainder to exact-real DH derivative

Status: `OPEN_UNCOMPILED`; bounded conditional exact-real contract.

## Minimal interface

`CentralFDSourceContract` consumes the existing C2/C3 source binding and adds
only the central-FD seam:

1. `dh_first_binding` identifies the concrete DH first-derivative evaluator
   with the Taylor first-derivative field on the same box and region;
2. `step_pos` makes the central quotient meaningful;
3. `shift_step_semantics` identifies the two shifted points as
   `x ± step b • direction b`, and `shifted_points_same_box` requires both
   evaluations to remain in the same source box;
4. `central_fd_source_identity` identifies the evaluator with the central
   difference of the same exact source function and the same step;
5. `central_fd_remainder_sound` supplies the C3/Taylor estimate
   `|FD_h f(x) - f'(x)| ≤ h² M₃/6` on that same box;
6. `residual_absorption_budget` compares the resulting remainder to the
   residual budget used by the downstream consumer.

At a domain point, the theorem selects the existing `boxOf x`, returns the two
same-box shifted-region facts and exact evaluator identity, transports the
source derivative to the concrete DH derivative, and then proves the bounded
central-FD error by transitivity into the residual budget.

## Why the contract does not close from existing fields alone

The existing derivative hull and C2/C3 records provide pointwise hull fields,
but they do not by themselves provide a segment-level Taylor theorem for the
central quotient, a common step, or shifted-point membership in the same box.
Those are separate premises.  `cubic_zero_remainder_bound_obstruction` gives
the exact test `f(x) = x^3`, `x = 0`, `h = 1`: the central difference is `1`
while `f'(0) = 0`, so a claimed remainder bound `0` is false.

## Next frontier and independent leaves

The next frontier is a source/interval certificate proving
`central_fd_remainder_sound` for the concrete DH evaluator with the exact same
step, same shifted box, and same regularity/third-derivative hull.  A separate
budget proof must establish `residual_absorption_budget`.  Coverage is needed
to select a box for every domain point, but is not proved here.  Flowpipe
containment, residual absorption beyond the local budget inequality, source
Float64/libm correctness, continuous-domain coverage, admission, and registry
promotion remain independent open leaves.

No concrete source or numerical artifact was modified, and no local
Lean/Lake command or wide regression was run.
