# P3 interval-enclosure strict-slack consumer

Status: conditional exact-real proof-attempt candidate, pending independent review.

## Minimal interface

`IntervalEnclosureCertificate` uses a finite box set and an explicit region
predicate. Each box supplies:

- a positive exact-real `gapLower`;
- a sound lower-gap relation to `capLoad - weightedLoad`;
- a sound `capLoadUpper` bound and a per-box transfer to `capMaxLoad`;
- an explicit `rounding_interval_sound` premise.

`interval_enclosure_strict_slack` selects a box from the explicit coverage
witness, keeps the same point `x` through every relation, and returns both the
box certificate and strict capMax slack. The consumer theorem adds only an
existing bound by `weightedLoad`.

## Soundness obstruction

The exact-real `sampledGap` example is positive at the sampled point `false`
but nonpositive at the omitted point `true`. It demonstrates why solver output,
samples, or grid membership cannot stand in for the
`rounding_interval_sound` premise and per-box enclosure inequalities. The
formal obstruction is `sample_without_interval_soundness_not_global`.

## External obligations

The sidecar does not prove that a box is an interval, that interval arithmetic
or rounding is sound for a concrete implementation, or that the boxes cover a
continuous physical domain. Those certificates and coverage maps remain
external premises. No numerical payload, source evidence, admission, registry
promotion, or Lean compilation claim is made. No local Lean/Lake command or
broad regression was run.
