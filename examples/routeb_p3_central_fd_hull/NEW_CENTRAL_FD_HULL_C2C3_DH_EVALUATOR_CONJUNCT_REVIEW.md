# P3 minimal C2/C3 to DH-evaluator conjunct

Status: `OPEN_UNCOMPILED`; value-level exact-real companion only.

## Minimal conjunct

The companion adds exactly one new premise about a target evaluator
`dhEvaluator : D → ℝ`:

`dhEvaluator x = sourceM x + sourceC x + sourceG x`

on the existing source domain.  Composed with the already-defined
`source_dh_identity`, this proves

`sourceFunction x = dhEvaluator x`

at every domain point, hence also at the same `boxOf x` selected by the
existing coverage witness.  No source-binding structure is redefined.

## Composition with the margin consumer

`dh_evaluator_at_same_covered_point_has_uniform_margin` reuses the existing
endpoint-uniform consumer.  Its margin proof therefore still selects the same
covered box and consumes, in order:

- source derivative hulls transported from the Taylor fields;
- the same-box Taylor lower/remainder expression;
- source/certificate rounded-endpoint equality;
- positive per-box gap and the finite `inf'` common margin;
- the cap-load upper chain to `capMaxLoad`.

The DH evaluator equality is reported as a separate conjunct.  It is not used
to manufacture derivative hulls, rounding, coverage, or positivity.

## What remains open

This is deliberately only a value-level conjunct.  Equality of function values
does not prove that the C2/C3 derivative fields are the first/second/third
derivatives of the concrete DH evaluator.  That derivative-level binding still
requires independent exact-real source/interval evidence on the same box, with
the same rounding semantics and coverage map.

The companion does not prove the deployed Julia/MATLAB `Float64` evaluator,
central-FD error, libm rounding, flowpipe containment, residual absorption,
continuous-domain coverage, admission, or registry promotion.  It remains
`OPEN_UNCOMPILED`.

No source, numerical artifact, state, coverage, admission, or registry file was
modified, and no wide regression was run.
