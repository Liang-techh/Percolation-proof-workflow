# P3 uniform strict slack consumer

Status: conditional exact-real proof-attempt candidate, pending independent review.

## Pointwise-versus-uniform obstruction

The exact-real parameterized family

```text
domain       = {x : ℝ | 0 ≤ x}
reciprocalGap(x) = 1 / (x + 1)
```

has a positive gap at every domain point, but for every `ε > 0` the point
`x = 1 / ε` has `reciprocalGap(x) < ε`. Therefore pointwise strictness alone
does not supply a domain-wide positive slack. This is an analytic counterexample,
not a numerical assumption. The theorem `pointwise_positive_not_uniform`
packages both exact-real statements.

## Uniform consumer

`UniformGapCapCertificate` takes an explicit positive `uniformGap`, a pointwise
lower-bound certificate

```text
uniformGap ≤ capLoad(x) - weightedLoad(x)
```

and a pointwise cap comparison `capLoad(x) ≤ capMaxLoad(x)`. The consumer proves
the explicit margin `weightedLoad(x) + uniformGap ≤ capMaxLoad(x)` and hence the
strict capMax inequality. An optional `consumer` bounded by `weightedLoad` is
handled by the second theorem.

`FiniteUniformGapCapCertificate6` is only a typed Fin 6 adapter: it records the
finite component-gap family and forwards the already supplied uniform bound to
the generic consumer. It does not claim to derive that bound from positivity.
A compactness argument, finite minimum argument, or concrete family-to-cap map
must be supplied upstream.

## External obligations

`domain x` is an explicit coverage premise at every consumed point. The same `x`
is used in the domain, load, cap-load, and capMax expressions; no naming
convention establishes this binding. The sidecar does not establish central-FD,
derivative-hull, export-center, source, numerical, coverage, admission,
registry, or Lean compilation facts. No local Lean/Lake command was run.
