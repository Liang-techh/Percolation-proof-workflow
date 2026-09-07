# Route-B P4 O0 regularizer semantics bridge

This is the coordinator-side, exact-rational interface for the recorded
`Float64(1e-6)` fact. It is intentionally limited to the regularizer seam; it
does not bind the rest of `dhport_lib.jl`.

## Scalar contract

The bridge fixes the two values as exact rationals:

```text
mu_float64 = 4722366482869645 / 4722366482869645213696
mu_exact   = 1 / 1000000
delta      = mu_exact - mu_float64
           = 3339 / 73786976294838206464000000 > 0
```

Thus `mu_float64 < mu_exact`, and the outward scalar interval is
`[mu_float64, mu_exact]`. The larger rational `1/1000000` is not a lower bound
for the deployed regularizer.

`routeb_regularizer_fact()` returns this contract. The value is anchored to
the recorded binary64 bit pattern `0x3eb0c6f7a0b5ed8d`; the function does not
execute Julia or claim a libm/operation trace.

## Matrix and block propagation

`propagate_routeb_regularizer_diagonal(base_matrix)` accepts an exact-rational
common unregularized base. Under that explicit premise it constructs

```text
M_float = M0 + mu_float64 I
M_exact = M0 + mu_exact I
M_float = M_exact - delta I.
```

The returned `RouteBRegularizerInclusion` exposes `lower_matrix = M_float`,
`upper_matrix = M_exact`, and `difference_matrix = delta I`. With the current
one-based Route-B partition `B=(4,5)`, `D=(1,2,3,6)`, the same result is
available for `BB` and `DD`; `BD` and `DB` have zero shift. This is a
conditional regularizer propagation statement, not a Float64-to-exact
enclosure for the unregularized base.

`audit_routeb_regularizer_inclusion(float64_matrix, exact_real_matrix)` checks
the same relation for matrices that have already been converted to explicit
integer/`Fraction` representations. It rejects Python floats so a machine
output cannot silently become an exact-real input.

## Resolvent boundary

`derive_routeb_resolvent_port_propagation` is a separate consumer. It returns
`PENDING_RESOLVENT_PREMISE` unless the caller supplies an explicit
`RouteBExactResolventPremise` for the exact-real `M_DD(mu_exact)` inverse. If
`K >= ||M_DD(mu_exact)^(-1)||` and `delta*K < 1`, it returns only the
conditional bounds

```text
||M_DD(mu_float)^(-1)|| <= K/(1-delta*K)
||M_DD(mu_float)^(-1)-M_DD(mu_exact)^(-1)||
    <= delta*K^2/(1-delta*K).
```

A port bound additionally requires nonnegative `M_BD` and `DeltaM_DB` norm
bounds and the same source/state key. The helper never infers invertibility,
an inverse norm bound, or a coupling bound from the regularizer alone.

The API and focused tests do not run Lean/Lake, Julia, SOS, trajectory checks,
or broad regression, and all result objects keep
`formal_certificate_allowed=False` and `registry_eligible=False`.
