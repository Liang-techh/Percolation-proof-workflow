# P3 minimal C2/C3 derivative-level DH binding

Status: `OPEN_UNCOMPILED`; conditional exact-real typed lemma.

## Minimal same-box premise

The companion reuses `C2C3SourceBinding` and adds only three local premises,
for supplied concrete exact-real evaluator derivative functions
`dhFirst`, `dhSecond`, and `dhThird`:

```text
taylorFirstDerivative  = dhFirst
taylorSecondDerivative = dhSecond
taylorThirdDerivative  = dhThird
```

Each equality is required on the same listed box and the same `region b x`.
The existing `same_first_derivative`, `same_second_derivative`, and
`same_third_derivative` then transport those equalities to

```text
sourceFirstDerivative  = dhFirst
sourceSecondDerivative = dhSecond
sourceThirdDerivative  = dhThird
```

at the single covered point selected by the existing `boxOf x` and `coverage`
witness.  This is the smallest typed derivative-level conjunct that closes the
source-vs-concrete-evaluator equality without duplicating the endpoint
consumer.

## Obstruction

`value_identity_does_not_force_derivative_identity` keeps the value function
identical on both sides while assigning source and evaluator derivative fields
the constants `0` and `1`.  Therefore the value-level DH evaluator conjunct
cannot be upgraded to derivative-level identity without the three same-box
derivative premises.

## Remaining open leaves

The supplied `dhFirst/dhSecond/dhThird` functions are abstract exact-real
inputs.  The companion does not prove they are derivatives of the deployed
Float64/libm DH evaluator, does not prove central-FD or rounding error bounds,
and does not prove the coverage premise.  Endpoint margin, flowpipe
containment, residual absorption, continuous-domain coverage, admission, and
registry promotion remain independent open obligations.

No source, numeric artifact, state, coverage, admission, or registry file was
modified, and no wide regression was run.
